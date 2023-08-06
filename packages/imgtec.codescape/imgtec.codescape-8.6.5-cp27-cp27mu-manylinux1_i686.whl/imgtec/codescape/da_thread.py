###############################################################################
#
# Disclaimer of Warranties and Limitation of Liability
#
# This software is available under the following conditions:
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL IMAGINATION TECHNOLOGIES LLC OR IMAGINATION
# TECHNOLOGIES LIMITED BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Copyright (c) 2016, Imagination Technologies Limited and/or its affiliated
# group companies ("Imagination").  All rights reserved.
# No part of this content, either material or conceptual may be copied or
# distributed, transmitted, transcribed, stored in a retrieval system or
# translated into any human or computer language in any form by any means,
# electronic, mechanical, manual, or otherwise, or disclosed to third parties
# without the express written permission of Imagination.
#
###############################################################################

__all__ = 'Thread'

import os, re
from collections import namedtuple
from contextlib import contextmanager
from functools import wraps

import da_types
from breakpoint import Breakpoint, BreakpointList, BreakpointEnums, _get_breakpoint_info
from callstack import Frame
from channel import Channel
from da_exception import Error, DiagnosticError, ExecutionStateError, LoadProgramFileError, OverlayError, FrameError, InvalidArgError
from da_symbol import Symbol
from disassembly import Disassembly, DisassemblyList
from dtm import DTMRequest
from fileserver import FileServer
from memory import Memory, MemoryDetails
from overlays import OverlayArea
from source import SourceFile, SourceLine
from imgtec.lib import format_signature
from imgtec.lib.namedenum import namedenum
from imgtec.lib.namedbitfield import namedbitfield, Field

SymbolCompleteResult = namedtuple('SymbolCompleteResult', 'exact icase loose')


def _carry_docs(wrapper, original):
    wrapper.__func__ = original
    if not hasattr(original, '__func__'):
        docs = format_signature.format_doc(original.__doc__ or '')
        docs = "%s\n\n%s" % (format_signature.format_signature(original), docs)
        wrapper.__doc__ = docs
    else:
        wrapper.__doc__ = original.__doc__
        
def _get_child_threads(context, parent_thread, old_swthread_cache):
    new_swthread_cache = {}
    for tid in context.GetChildThreads():
        thread = old_swthread_cache.get(tid)
        if thread is None:
            child_context = context.GetTargetContext(tid)
            thread = Thread(parent_thread.index, parent_thread.core, child_context, parent_thread)
        if thread is not None:
            new_swthread_cache[tid] = thread
    return new_swthread_cache

def raise_if_not_in_range(min, value, max, message):
    if not min <= value < max:
        raise ValueError(message)
        

_status_conversions = dict(
    UNDEF=da_types.Status.target_offline,
    ERROR=da_types.Status.target_offline,
    HALTED=da_types.Status.stopped, # or maybe not?
    OFFLINE=da_types.Status.target_offline,
    HARDRESET=da_types.Status.expected_reset,
    SOFTRESET=da_types.Status.expected_reset,
    STATUS=da_types.Status.stopped,
    TRACED=da_types.Status.single_stepped, # maybe?
    BREAKPOINT=da_types.Status.sw_break,# ?
    BREAKSOFT=da_types.Status.sw_break,
    BREAKHARD=da_types.Status.hw_break,
    CPUTRACED=da_types.Status.single_stepped,
    EXCEPTION=da_types.Status.exception,
    SUSPENDED=da_types.Status.stopped, # ?
    PAUSED=da_types.Status.stopped, # ?
    EXEC=da_types.Status.running, # ?
    RUNNING=da_types.Status.running,
    STOPPED_GDB=da_types.Status.stopped,
    CPU_HALTED=da_types.Status.stopped,
)  

def raise_if_running(fn):
    @wraps(fn)
    def raise_if_running_wrapper(thread, *args, **kargs):
        if thread.is_running:
            raise ExecutionStateError('%s is not available when the thread is running' % fn.__name__)
        return fn(thread, *args, **kargs)
    _carry_docs(raise_if_running_wrapper, fn)
    return raise_if_running_wrapper

class Thread(object):

    """Representation of a hardware or software thread."""

    def __init__(self, index, core, context, hw_thread=None):
        self.__index = index
        self.__context = context
        self.__target_info = self.__context.target_info
        self.__core = core
        self.__hwthread = hw_thread or self
        self.__name = self.__target_info.hwthread_name if self.is_hwthread else self.__target_info.swthread_name
        self.__swthread_cache = {}
        self.__breakpoint_cache = {}
        self.__events_enabled = False
        self.__registers_info = {}
        self.__register_types = {}
        self.__memory_cache = {}
        self.__provided_memory_details = {}
        self.__memory_protection = False
        
    @property
    def index(self):
        '''Return the zero based index of the hardware thread in it's core. 
        
        For software threads this returns the index of it's parent thread.
        '''
        return self.__index

    def __str__(self):
        return self.__name

    def __repr__(self):
        parent = (', core=%s' % self.core.name) if self.is_hwthread else ', parent=%s' % (self.hwthread.name,)
        return 'Thread(%s, index=%d, state=%s%s)' % (self.__name, self.index, self.state, parent)

    def GetName(self):
        return self.__name

    def GetId(self):
        return self.__context.target

    def GetInfo(self):
        return self.__target_info

    def GetProbe(self):
        """Parent :class:`Probe <imgtec.codescape.Probe>` of this SoC."""
        return self.core.probe
    GetDA = GetProbe

    def GetCore(self):
        """Parent :class:`Core <imgtec.codescape.Core>` of this thread."""
        return self.__core

    def GetDescription(self):
        """Returns a string describing the thread as seen in the target tree."""
        if self.is_hwthread:
            try:
                program_file = os.path.split(self.program_file_name)[1]
                return '%s-%s %s - %s' % (self.core.name, self.name, self.state, program_file)
            except LoadProgramFileError:
                return '%s-%s %s' % (self.core.name, self.name, self.state)
        else:
            if self.state:
                return '%s %s' % (self.name, self.state)
            else:
                return self.name

    def GetHardwareThread(self):
        """
        If this is a hardware thread then this thread is returned. 
        If this is a software thread then the parent of this thread is returned.
        """
        return self.__hwthread

    def GetState(self):
        """Return the current state of the thread as an instance of :class:`~imgtec.codescape.State`.
        
        The `State` class can be used to determine the current run state of the 
        thread, for example::
        
           thread.Run()
           while thread.state.is_running:
                time.sleep(0.1)
           pc = thread.state.pc
        """
        ts = self.__context.GetThreadStatus()
        tstatus, description, pc = ts[0], ts[4], ts[6]
        try:
            status = str(da_types.ActualStatus(tstatus))
            status = _status_conversions[status]
        except (KeyError, ValueError):
            status = '<unknown : %d>' % (int(tstatus),)
        s =  da_types.State(status, pc, 0)
        s.legacy = description
        return s

    def GetStatus(self):
        """Deprecated access to the thread status.
        
        This function returns a :class:`~imgtec.codescape.ThreadStatus` object 
        describing the status of the thread.  However the object returned is 
        difficult to interpret and it has been replaced with :meth:`GetState`."""
        return ThreadStatus(*self.__context.GetThreadStatus())

    def GetSoftwareThreads(self):
        """Returns the child software threads of this thread."""
        self.__swthread_cache = _get_child_threads(self.__context, self, self.__swthread_cache)
        return sorted(self.__swthread_cache.itervalues(), key=lambda t: t.id)

    def GetIsSoftwareThread(self):
        """Returns True if this is a software thread. False otherwise."""
        return not self.is_hwthread

    def GetIsHardwareThread(self):
        """Returns True if this is a hardware thread. False otherwise."""
        return self.hwthread == self

    def GetEndian(self):
        """
        Get the endianness of the thread.

        :return: Endian.big or Endian.little.

        .. sourcecode:: python

            from imgtec.codescape import Endian

            if thread.endian == Endian.big:
                print "Big Endian"
        """
        return da_types.Endian(self.__context.GetEndian())

    def GetCPUInfo(self):
        """
        Get information about the current VPE.

        Returns a list of tuples of (property_name, value).  The availability
        of properties is subject to change and should not be relied upon.

        Example output:

        =================================== =============================
        Property                            Value
        =================================== =============================
        prid                                0x0001974c
        company_name                        Imagination Technologies MIPS
        cpu_name                            74Kc
        cpu_is_32bit                        True
        bus_is_32bit                        True
        has_mmu                             True
        has_fpu                             False
        has_ejtag                           True
        has_mips32                          True
        has_micro_mips                      False
        has_mips_16e                        True
        has_dsp1                            True
        has_dsp2                            True
        has_mt                              False
        has_smart                           False
        has_msa                             False
        has_3d                              False
        dsp_enabled                         True
        msa_enabled                         False
        fpu_max_register_size               0x00000000
        fpu_enabled                         False
        fpu_split_64bit_mode                True
        fpu_supports_64bit_float            False
        fpu_supports_32bit_float            False
        fpu_supports_64bit_fixed            False
        fpu_supports_32bit_fixed            False
        fpu_supports_3D_ASE_fixed           False
        fpu_supports_paired_registers_fixed False
        =================================== =============================
        """
        return self.__context.CpuInfo()
        
    def GetMemoryProtection(self):
        '''Prevent script access to memory locations not covered in the HSP.
        
        When set to True, all memory accesses that come directly from the script
        will not be allowed to access memory that is not marked as readable
        (or writeable for read-only locations) in the HSP.  
        
        When set to False (the default), '''
        return self.__memory_protection
        
    def SetMemoryProtection(self, enable):
        '''Prevent script access to memory locations not covered in the HSP.

        When set to True, memory accesses that come directly from the script
        will not be allowed to access memory that is not marked as readable
        (or writeable for read-only locations) in the HSP.  An error will be
        raised indicating that the access was denied.

        When set to False (the default), all memory accesses that come directly
        from the script are allowed.
        
        .. versionadded: 8.6.2
            Previously memory accesses behaved as if this setting was always set 
            to True.
        '''
        self.__memory_protection = enable

    def GetMemoryNames(self):
        """
        Returns a set of memory names associated with this thread.

        Any of these names may be passed into :py:meth:`imgtec.codescape.Thread.GetMemory` to 
        access read and write operations
        """
        self.memory # force an update of the cache
        return {m.name for m in self.__memory_cache.values()}

    def GetMemory(self, name=None):
        """
        Return a :class:`Memory <imgtec.codescape.Memory>` to access memory on this thread.
        
        The name can be specified by memory name or memory type enum.

        The list of enums are :class:`MemoryTypes <imgtec.codescape.MemoryTypes>`

        A list of valid memory names supported by this hardware can be found by calling 
        :py:meth:`imgtec.codescape.Thread.GetMemoryNames`

        If no memory name is given access to the main memory is returned. The main 
        memory is also available through the :attr:`~imgtec.codescape.Thread.memory`

        Access to an arbitary memory can be given by providing custom memory details.

        .. sourcecode:: python

            from imgtec.codescape.memory import MemoryDetails

            undefined_memory_type = 1234
            memory_details = MemoryDetails(undefined_memory_type, "Memory Name", address_size=8)
            memory = thread.GetMemory(memory_details)
            memory.Write(0x80000000, 'write_data')

        """

        if name is None:
            name = 0
        if not isinstance(name, (int, long, basestring, MemoryDetails)):
            raise TypeError('Invalid type for parameter "name": %r, expected integer, string, or NoneType' % name)
        if isinstance(name, basestring):
            name = name.lower()
        if isinstance(name, MemoryDetails):
            name, details = name.name.lower(), name
            self.__provided_memory_details[name] = details

        # Call GetMemoryDetails() to see if details have changed then rebuild 
        # caches, reusing existing Memory objects
        all_memory_details = [MemoryDetails(*m) for m in self.__context.GetMemoryDetails(True)]
        memory_cache = {}
        for details in all_memory_details + self.__provided_memory_details.values():
            if details.type in self.__memory_cache:
                memory = self.__memory_cache[details.type]
                memory._details = details
            else:
                memory = Memory(self.__context, self, details)
            memory_cache[memory.type_id] = memory
            memory_cache[memory.name.lower()] = memory
        self.__memory_cache = memory_cache
        
        # Try again to find memory from updated cache
        if name not in self.__memory_cache and isinstance(name, (int, long)):
            details = MemoryDetails(name, "Memory Type %d" % name)
            memory = Memory(self.__context, self, details)
            self.__memory_cache[memory.type_id] = memory
            self.__memory_cache[memory.name.lower()] = memory
            self.__provided_memory_details[memory.name.lower()] = details

        try:
            return self.__memory_cache[name]
        except KeyError:
            known_types = ', '.join(sorted({repr(x.name) for x in self.__memory_cache.values()}))
            raise ValueError('Unknown memory type name: %r. Valid types are: %s' % (name, known_types))

    def GetProgramFileName(self):
        """Returns the program filename or an empty string if no program file is loaded."""
        return self.__context.GetProgramFileName()

    def GetIsRunning(self):
        """Returns True if this thread is running. False otherwise."""
        return self.__context.IsRunning()

    def _refresh_breakpoints(self):
        bpinfos = _get_breakpoint_info(self.__context)

        breakpoints = {}
        for bpinfo in bpinfos:
            bpid = bpinfo["bpid"]
            bp = self.__breakpoint_cache.get(bpid)
            if bp:
                bp._set_info(bpinfo)
            else:
                bp = Breakpoint(self.__context, self, bpinfo["bpid"])
            breakpoints[bpid] = bp

        for bp in self.__breakpoint_cache.itervalues():
            if bp.GetId() not in breakpoints:
                bp._set_dead()

        self.__breakpoint_cache = breakpoints

    def GetBreakpoints(self):
        """
        Return a :class:`~imgtec.codescape.BreakpointList` containing all
        breakpoints on this thread.
        """
        self._refresh_breakpoints()
        bplist = BreakpointList(self.__context, self.__breakpoint_cache.itervalues())
        bplist.sort(key=lambda bp: bp.GetId())
        return bplist

    def GetChannel(self, channel_no):
        """Returns a :class:`Channel <imgtec.codescape.Channel>` on the specified channel."""
        if not self.__context.ChannelValidate(channel_no):
            raise ValueError('Invalid channel ID: %s' % channel_no)
        return Channel(self.__context, channel_no)

    def LoadSymbols(self, filename, progress=False):
        """
        Load just the debug info/symbols from a program file onto the thread.
        
        This is a convenience method and is equivalent to ::
        
         t.LoadProgramFile(filename, hard_reset=False, 
                           load_type=codescape.LoadType.symbols,
                           progress=progress)
        
        :param filename:   File name of the program file to load.
        :param progress:   Show progress? (False by default).
        """
        return self.LoadProgramFile(filename, False, da_types.LoadType.symbols, progress)
        
    def LoadProgramFile(self, filename, hard_reset=True, load_type=da_types.LoadType.binary_and_symbols, progress=False, args=None):
        """
        Load a program file onto the thread.

        :param filename:   File name of the program file to load.
        :param hard_reset: Hard reset the thread? (True by default).
        :param load_type:  :class:`LoadType <imgtec.codescape.LoadType>` specifying how to load the program file.
        :param progress:   Show progress? (False by default).
        :param args:       Argument string. If set on none gdb server based thread, it will automatically add 'uhi_cmdline_boot'
                           to the load_type.
        """
        use_throw = 0x40000000

        if args is None:
            args = ""
        else:
            target_info = da_types.TargetInfo(*self.__context.GetTargetInfo())
            if "gdbserver" not in target_info.processor_family:
                load_type |= da_types.LoadType.uhi_cmdline_boot

        self.__context.LoadProgramFileEx(filename, hard_reset, load_type | use_throw, progress, args)
        
    def IsSameProgramFile(self, path):
        """Compares the path/name and date/time of the program file loaded with the file specified.
        
        Returns True if the file is the same.
        """
        return self.__context.IsSameProgramFile(path)

    def LoadScript(self, filename, hard_reset=True, load_type=da_types.LoadType.binary_and_symbols, progress=False):
        """
        Initialize the thread with a load script file.
        
        :param filename:   File name of the load script file.
        :param hard_reset: Hard reset the thread? (True by default).
        :param load_type:  :class:`LoadType <imgtec.codescape.LoadType>` specifying how to load the program file.
        :param progress:   Show progress? (False by default).
        """
        if self.__context.UsingDAscript():
            try:
                from CSUtils import DA
                DA.SelectTarget(self.__context.target)
                DA.LoadProgramFileEx(filename, hard_reset, load_type, progress)
            except ImportError:
                raise Error("CSUtils is required for load scripts")
            finally:
                self.__context.InvalidateSelectedTarget()
        else:
            self.LoadProgramFile(filename, hard_reset, load_type, progress)

    def LoadSREC(self, filename):
        """
        Load a Motorola SREC file on to the thread.

        :param filename:   File name of the SREC file to load.
        """
        self.__context.LoadSREC(filename)

    def LoadHex(self, filename):
        """
        Load an Intel Hex file on to the thread.

        :param filename:   File name of the hex file to load.
        """
        self.__context.LoadHex(filename)

    def UnloadProgramFileInfo(self):
        """Unloads the debug information for all files."""
        self.__context.UnloadProgramFileInfo()
        
    def LoadProgramFileSymbolsAtAddress(self, path, base_address, progress=False):
        """Loads debug information for a program file at a base address.
        
        This function does not clear the existing loaded program files(s): it augments them.
        
        This is intended for use with Linux kernel modules but it can also be used
        for Linux shared objects or for loading alternative debug sections that are 
        stored in separate files. Kernel modules and shared objects can be loaded in 
        isolation (i.e. it is not required to have a main executable loaded).

        :param path:         The path of the file to load.
        :param base_address: The base address at which the program file is to be loaded for symbol relocation.
        :param progress:     Show progress? (False by default).

        .. note:: This function does not perform a hard reset.
        """
        self.__context.LoadProgramFileSymbolsAtAddress(path, base_address, progress)

    def UnloadProgramFileSymbols(self, path):
        """Unloads the debug information for a particular linux kernel module or shared library.
        
        This is intended for use with Linux kernel modules but it can also be used
        for Linux shared objects.

        :param path:  The path of the file to unload.
       
        """
        self.__context.UnloadProgramFileSymbols(path)

    def SetOSFeature(self, os_type, os_feature, new_value):
        """
        SetOSFeature(TargetID, OSType, OSFeature, NewValue)

        Sets the OS feature for the specified target. On error (such as bad parameters, etc.) the function will throw.

        :param TargetID:

            The target to find out about.

        :param OSType:

            ===== ===============================
            Value Operating System
            ===== ===============================
            0     MeOS
            1     Threadx
            2     MeOS2
            3     FreeRTOS
            ===== ===============================

        :param OSFeature:


            ===== =======================================
            Value Operating System Feature
            ===== =======================================
            0     Debug sub-tasks (valid feature settings are on = 1, off = 0)
            ===== =======================================

        :param NewValue:

            Feature specific setting.

        :return: the previous setting or one of the following errors :

            ===== =====================================
            Value Meaning
            ===== =====================================
            -1    Feature not supported on this target.
            -2    Feature not configurable for this target.
            ===== =====================================
        """
        self.__context.SetOSFeature(self.__context.target, os_type, os_feature, new_value)
        
    def RegistersInfo(self):
        """Get information about the registers available with the current ABI."""
        abi = self.GetABI()
        return self.__get_cached_registers_info(abi).values()
        
    def __get_cached_registers_info(self, abi):
        try:
            return self.__registers_info[abi]
        except KeyError:
            regs_info = [da_types.RegisterInfo(*info) for info in self.__context.RegistersInfo(abi)]
            #Dict keyed on register name
            self.__registers_info[abi] = dict((info.name.lower(), info) for info in regs_info)
            return self.__registers_info[abi]
            
    def __get_cached_register_type(self, name):
        try:
            #Keyed on name only as imgtec.codescape doesn't deal with views
            return self.__register_types[name]
        except:
            registers_info = self.__get_cached_registers_info(self.GetABI())
            reg_info = None
            
            #First try with just the register name
            try:
                reg_info = registers_info[name.lower()]
            except KeyError:
                #Then slower search through the aliases (cpx.y.z names)
                for info in registers_info.values():
                    if name in info.aliases:
                        reg_info = info
                        #Cant have dots in a class name
                        name = name.replace('.', '_')
                        break
                else:
                    pass
                
            if reg_info is not None:
                fields = reg_info.fields
                if fields:
                    self.__register_types[name] = namedbitfield(name, fields, size=reg_info.size*8, show_raw_value=True,
                                             show_vertical=True)
                    return self.__register_types[name]
            else:
                return None
            
    def _make_reg_type(self, name, value):
        reg_type = self.__get_cached_register_type(name)
        if reg_type is not None:
            return reg_type(value)
        else:
            return value
            
    def ReadRegister(self, name, float_as_int=False):
        """Reads a register from the target.
        
        See :meth:`ReadRegisters` for more information.
        """
        return self.ReadRegisters([name], float_as_int)[0]
            
    def ReadRegisters(self, names, float_as_int=False):
        """Reads one or more registers from the target.
        
        If `float_as_int` is True then floating point registers will have their 
        values returned as their raw integer representations. For example the 
        float value 0.5 when read from a 32-bit bit FP register will be returned 
        as 0x3f000000.

        If `float_as_int` is False then float registers will be returned as 
        floating point values.  For example the float value 0.5 will be returned 
        as 0.5.

        .. note :: This function reads the actual register values from the target,
                   it is not affected by the current callstack level.
        """
        values = self.__context.ReadRegisters(names, float_as_int)
        return [self._make_reg_type(n, v) for n, v in zip(names, values)]
            
    def ModifyRegister(self, name, **kwargs):
        """Read modify write the register, changing the given fields. 
        
        The field's value can be given as a numerical value or a string. Strings 
        are looked up in the field's enum type (if present) and converted to the 
        corresponding number.
        
        Exceptions will be raised when trying to modify a register that has no
        information associated with it, or trying to assign an enum value (a string)
        to a field which doesn't have an enum.
       
        .. sourcecode:: python
        
            t.ModifyRegister('Status', CU1='Access_not_allowed', CU2=1)
            
        """
        value = self.__context.ReadRegister(name, False)
        reg_type = self.__get_cached_register_type(name)
        
        try:
            fields = dict((field.name, field.type) for field in reg_type._fields)
            lower_fields = dict((name.lower(), name) for name in fields)
        except AttributeError:
            raise AttributeError("Register '%s' does not have a rich type associated with it." % name)
        
        #Search kwargs for things that look like field names
        for arg in kwargs:
            if arg.lower() in lower_fields:
                arg_value = kwargs[arg]

                #Sub in the correctly formatted name
                del kwargs[arg]
                arg = lower_fields[arg.lower()]
                kwargs[arg] = arg_value

                if isinstance(arg_value, basestring):
                    #Try to find a matching enum value
                    try:
                        #Lower for case insensitive
                        enum_items = dict((k.lower(), v) for k, v in fields[arg]._items())
                    except AttributeError:
                        raise ValueError("Got string value '%s' for field '%s' which has no enum type." % (arg_value, arg))
                    else:
                        arg_value_lower = arg_value.lower()
                        try:
                            #Put in the numeric value
                            kwargs[arg] = enum_items[arg_value_lower]
                        except KeyError:
                            raise ValueError("Got unknown value '%s' for field '%s'" % (arg_value, arg))
    
        new_value = reg_type(value)._replace(**kwargs)
        return self.__context.WriteRegister(name, new_value, False)

    def WriteRegister(self, name, value):
        """Writes a value to the register on the target.

        .. note :: This function writes the actual register value from the target,
                   it is not affected by the current callstack level.
        """
        return self.__context.WriteRegister(name, value, False)

    def ReadTLB(self, index, guest=False):
        """Read the entry at the given index in the target's TLB."""
        return da_types.TLBEntry(*self.__context.ReadTLB(index, guest))

    def WriteTLB(self, index, entry, guest=False):
        """Write an entry to the target's TLB at the given index,
        where that entry consists of EntryLo0, EntryLo1, EntryHi, PageMask and GuestCtl1 values."""
        _entry = list(entry)
        if len(_entry) == 4:
            _entry.append(self.ReadTLB(index, guest).guestctl1)
        _entry.append(guest)
        self.__context.WriteTLB(index, *_entry)
        
    def CacheOperation(self, address, line_size, operation, count=1, flags=0):
        """Perform a cache operation.
        
        For operations that refer to an 'index' `address` will be an offset into 
        the cache data array.

        `line_size` is the size of the cache line in bytes (contents only, as found 
        in the Config regs).
        
        `operation` should be a bitwise or of the action to be taken, and the cache type. 
        The action should be taken from this table, where I,D,S,T mean instruction,
        data, secondary, tertiary respectively, 

        =============== ======================================================
        Operation       Meaning
        =============== ======================================================
        0<<2 (I)        Index invalidate, set the cache line at the given 
                        index (offset address) to be invalid.
        0<<2 (D,S,T)    Index Writeback Invalidate, if the line at the index 
                        is valid and dirty, write it back to memory. Set the 
                        line to invalid regardless.
        1<<2 (I,D,S)    Index load tag, read the tag for the cache line at
                        the given index into the TagLo/TagHi register(s).
                        Read the data word at the given address into the 
                        DataLo/DataHi register(s).
                        Read precode and data parity bits into the ErrCtl
                        register.
        2<<2 (I,D,S,T)  Index store tag, write the tag for the given cache 
                        line using the value(s) in the corresponding
                        TagHi/TagLo registers.
        3<<2 (I,D,T)    Reserved, executes a no-op.
        3<<2 (S)        Index store data, write the data in L23DataHi/Lo
                        to the way and index specified.
        4<<2 (I,D,S,T)  Hit invalidate, if the cache contains the specified
                        address, set it to invalid.
        5<<2 (D,S,T)    Hit WriteBack invalidate. As above, but write the 
                        contents of the line back to memory first.
        5<<2 (I)        Fill the cache from the given address. Data is 
                        re-fetched even if it is already cached.
        6<<2 (D,S,T)    Hit Writeback, if the cache contains the given address
                        and it is valid and dirty write that line back to 
                        memory. Leave line valid but clear dirty state.
        7<<2 (I,D,S,T)  Fetch and lock, if the cache does not contain the 
                        given address, fill it from memory, doing a writeback 
                        if required. Set the line to valid and locked. If the 
                        data is already in the cache, just lock it. The least 
                        recently used way is used for the fill.
                        The lock can be cleared by using an index, index
                        writeback, hit or hit writeback invalidate operation.
                        Alternatively an index store tag operation could be 
                        used.
        =============== ======================================================
                           
        cache type must be one of:
                
        ========== ========================
        Cache type Meaning
        ========== ========================
        0 (0b00)   Instruction cache
        1 (0b01)   Data cache
        3 (0b11)   Level 2/Secondary cache
        2 (0b10)   Level 3/Tertiary cache
        ========== ========================
        
        .. note :: cache types are in Gray code order, so level 2 cache is 3 not 
                   2 as you might expect.
        
        If `count` is greater than 1 then the operation will be performed on multiple
        lines (assuming that the operation can do so).
        
        .. note :: the range of the cache operation is given by count*line size. 
                   This cannot exceed 0x7fff, anything larger must be split into multiple 
                   operations.

        `flags` may also be given indicating :
        
        ======= ========================================================
        Flags   Meaning
        ======= ========================================================
        0       normal virtual address.
        1       EVA mode user virtual address (uses CACHEE instruction).
        ======= ========================================================
        
        Examples::

            def op_addr(way, line, way_size, line_size):
                'Calculate an address based on way/line number.'
                KSEG0_START  = 0x80000000
                way_shift    = log(way_size, 2) # log base 2 of the way size 
                start        = KSEG0_START | (way << way_shift) # start of the way
                return start + (line_size * line_number)

            way_size            = 0x1fe0
            line_size           = 32
            op_address = op_addr(1, 1, way_size, line_size)
            assertEquals(0x80001020, op_address)
        
            CacheOperation(op_address, line_size, (0<<2)|0)     # Index invalidate way 1, line 1 of icache
            CacheOperation(op_address, line_size, (0<<2)|0, 10) # invalidate 10 lines from 0x80001020 onwards
            CacheOperation(0x8000BEEF, line_size, (6<<2)|1)     # hit writeback the address 0x8000BEEF
        """
        self.__context.CacheOperation(address, line_size, operation, count, flags)

    def SetOverlayHandlingMode(self, OverlayHandler):
        """Sets this thread overlay handling mode.
        
        OverlayHandler is one of the enum values in :class:`~imgtec.codescape.OverlayHandler`.

        Returns the previous mode or raises an OverlayError if overlays are not supported or not configurable.
        """
        result = self.__context.SetOverlayHandlingMode(self.__context.target, OverlayHandler)
        if result == -1:
            raise OverlayError('Overlays not supported')
        elif result == -2:
            raise OverlayError('Overlays not configurable')

    def GetOverlayAreas(self):
        """Returns a collection of :class:`~imgtec.codescape.OverlayArea` 
        representing the overlay areas on this thread.
        """
        overlay_area_count = self.__context.GetOverlayAreaCount()
        return [OverlayArea(self.__context, index) for index in range(overlay_area_count)]

    def GetTypeMembers(self, type_handle):
        """Returns a list of :class:`~imgtec.codescape.Symbol` for the members of the given type handle."""
        return [Symbol(*sym) for sym in self.__context.TypeMembers(type_handle)]

    def GetTypeEnumMembers(self, type_handle):
        """Returns a list of (:class:`~imgtec.codescape.Symbol`, value) pairs for the enum values of the given enum type handle."""
        return [(Symbol(*sym), val) for sym, val in self.__context.TypeEnumMembers(type_handle)]

    def GetTypeBases(self, type_handle):
        """Returns a list of :class:`~imgtec.codescape.Symbol` for the base classes for the given type handle."""
        return [Symbol(*sym) for sym in self.__context.TypeBases(type_handle)]

    @raise_if_running
    def StepIn(self, source=False):
        """
        Steps a single instruction or single source line depending on the `source`
        parameter.  
        
        It will step into function calls, and is equivalent to Single Step in 
        Codescape Debugger.
        """
        if source:
            self.__context.StepSrc()
        else:
            self.__context.Step()

    @raise_if_running
    def StepOut(self):
        """
        Steps out of the current function to the next source line or instruction 
        past the call-site. Note that this does not require callstack information.
        
        Repeatedly calls StepOver until the current function exits.  This can be 
        useful for stepping out of inline functions or in case of bad/missing
        callstack info.
        """
        self.__context.StepOut()

    @raise_if_running
    def StepInForce(self, source=False):
        """ 
        Steps a single instruction or single source line depending on the `source`
        parameter.
        
        This is the same as the :meth:`StepIn` function but can step single 
        iterations of single instruction hardware loops (for example on MCP).
        """
        if source:
            self.__context.StepForceSrc()
        else:
            self.__context.StepForce()

    @raise_if_running
    def StepOver(self, source=False):
        """ 
        Performs a single step. Steps over function calls if present.

        If source is True then the code is run the source line changes, else 
        performs a single disassembly step, treating function calls as a single
        instruction.
        """
        if source:
            self.__context.StepOverSrc()
        else:
            self.__context.StepOver()

    @raise_if_running
    def Return(self):
        """Runs to the return address calculated by the callstack using a 
        breakpoint.
        
        This is equivalent to Step Out in Codescape Debugger.
        
        .. note:: This function will fail if the return address of the current
                  callstack frame cannot be evaluated.
        """
        self.__context.StepReturn()

    def Run(self):
        """Runs the thread, returns immediately."""
        self.__context.Run()

    @raise_if_running
    def RunToAddress(self, address, condition=""):
        """Runs the thread until it reaches the given address/expression."""
        return self.__context.RunToAddress(address, condition)

    def Stop(self):
        """Halts the thread, returns immediately."""
        self.__context.Stop()

    def CreateCodeBreakpoint(self, location_expression, mechanism=BreakpointEnums.Mechanisms.AnyAvailable):
        """
        Create a code breakpoint specifing the mechanism (of type 
        :class:`~imgtec.codescape.Mechanisms`), returns a
        :class:`~imgtec.codescape.Breakpoint`.
        """

        dali_breakpoint_type = {
            BreakpointEnums.Mechanisms.AnyAvailable:         da_types.BreakpointType.Code,
            BreakpointEnums.Mechanisms.Hardware:             da_types.BreakpointType.CodeHardware,
            BreakpointEnums.Mechanisms.Software:             da_types.BreakpointType.CodeSoftware,
        } [mechanism]

        bpid = self.__context.CreateBreakpoint(dali_breakpoint_type, location_expression)
        self._refresh_breakpoints()
        return self.__breakpoint_cache[bpid]

    def CreateDataBreakpoint(self, location_expression):
        """
        Create a data breakpoint, returns a 
        :class:`~imgtec.codescape.Breakpoint`.
        """
        dali_breakpoint_type = da_types.BreakpointType.Data
        bpid = self.__context.CreateBreakpoint(dali_breakpoint_type, location_expression)
        self._refresh_breakpoints()
        return self.__breakpoint_cache[bpid]

    def GetFileServer(self):
        """
        Returns a :py:class:`FileServer <imgtec.codescape.FileServer>`.
        """
        return FileServer(self.__context)

    GetSemiHosting = GetFileServer

    def GetOSInfo(self):
        """
        Returns operating system information in an :py:class:`OSInfo <imgtec.codescape.OSInfo>` object.
        """
        return da_types.OSInfo(*self.__context.GetOSInfo())

    def GetDiagnosticFileList(self):
        """
        Returns a list of a diagnostic filenames that can be passed to :meth:`~Thread.GetDiagnosticFile`.
        """
        return self.__context.GetDiagnosticFileList()

    def GetDiagnosticFile(self, filename):
        """Returns the contents of a diagnostic file from the Probe.   
        
        Typically the diagnostic files are shared between threads and cores, but this depends on the 
        probe type.
        
        Raises a DiagnosticError if the filename is not in the DiagnosticFileList as returned by 
        :meth:`~Thread.GetDiagnosticFileList`.
        """
        if filename not in self.diagnostic_file_list:
            raise DiagnosticError('Invalid diagnostic file: %s' % filename)
        return self.__context.GetDiagnosticFile(filename)

    @raise_if_running
    def GetFrame(self, level):
        """
        Return the :class:`~imgtec.codescape.Frame` on this callstack at the given level.

        Raises a :class:`~imgtec.codescape.FrameError` if the callstack level is not available.
        """
        return Frame(self.__context, level)

    @raise_if_running
    def GetFrameCount(self):
        """Returns the number of frames in the callstack."""
        return self.__context.FrameCount()

    @raise_if_running
    def GetFrames(self):
        """Decodes and returns all frames of the callstack as a list of 
        :class:`Frame <imgtec.codescape.Frame>`\ s.
        """
        return [Frame(self.__context, level) for level in range(self.__context.FrameCount())]

    @raise_if_running
    def GetCurrentFrame(self):
        """Return a :class:`~imgtec.codescape.Frame` that gives access to the current frame."""
        current_level = self.__context.FrameGetCurrent()
        return self.GetFrame(current_level)

    def Evaluate(self, expression, flags=0):
        """Evaluates an expression in the context of the current frame, returns 
        the result of the expression ::
        
           thread.Evaluate("1 + 1")
           thread.Evaluate("*(pInt + 7)")
           symbol = thread.GetSymbol("UART_CTRL")
           thread.Evaluate(symbol.handle)
           
        More detailed explanation of valid expressions can be found in the 
        documentation for the :ref:`ExpressionDialog`.
        
        The `flags` parameter enables additional options and can be one 
        or more of the flags defined in imgtec.codescape.\ :class:`~imgtec.codescape.ExpressionFlags`.
        """
        if self.is_running:
            return self.__context.FrameEvaluateSymbol(-1, expression, 0xffffffff, 0, flags)[1]
        else:
            return self.current_frame.Evaluate(expression, flags)

    def GetSymbol(self, expression, flags=0):
        """Returns a :class:`~imgtec.codescape.Symbol` representing
        the type of the given expression on the current frame.

        The `flags` parameter enables additional options and can be one
        or more of the flags defined in imgtec.codescape.\ :class:`~imgtec.codescape.ExpressionFlags`.
        """
        if self.is_running:
            symbol, value = self.__context.FrameEvaluateSymbol(-1, expression, 0xffffffff, 0, flags)
            return Symbol(*symbol)
        else:
            return self.current_frame.GetSymbol(expression, flags)

    def GetSymbolAndValue(self, expression, flags=0):
        """Returns a pair of (:class:`~imgtec.codescape.Symbol`, value)
        representing the type and result of evaluating the given expression on the 
        current frame.

        The `flags` parameter enables additional options and can be one
        or more of the flags defined in imgtec.codescape.\ :class:`~imgtec.codescape.ExpressionFlags`.
        """
        if self.is_running:
            symbol, value = self.__context.FrameEvaluateSymbol(-1, expression, 0xffffffff, 0, flags)
            return Symbol(*symbol), value
        else:
            return self.current_frame.GetSymbolAndValue(expression, flags)

    def Assign(self, destination, source):
        """Assign evaluated `source` expression to evaluated `destination` 
        expression in the context of the current frame.
        
        This method evaluates the `source` expression and writes the result 
        to the location of the result of evaluating the `destination` 
        expression. 
        
        The destination must be an lvalue but may reside in a register, in 
        memory, or even in a bitfield ::
        
          thread.Assign("Point.x", 100)
          thread.Assign("array[n]", "(unsigned char) Point.x")
          thread.Assign("argv[argc-1]", "&Person->name[0]")
       
        """
        if self.is_running:
            error_message, value = self.__context.FrameAssignSymbol(-1, destination, source)
            if error_message:
                raise FrameError(error_message)
            return value
        else:
            return self.current_frame.Assign(destination, source)

    def SymbolComplete(self, partial, options=da_types.SymbolCompleteOptions.globals, *deprecated):
        """
        Retrieves a list of symbol names that match the partial string.

        :param partial:
            The string to match.  If partial is an empty string then all symbols
            will be returned in the exact field, whilst icase and loose will be
            empty lists.

        :param options:
            ======================= =================================================
            Type                    Meaning
            ======================= =================================================
            SymbolCompleteOptions   see enumeration in da_types
            Boolean                 if True indicates symbols that are currently
                                    in scope should be searched, otherwise all
                                    debug symbols
            ======================= =================================================

        :param deprecated:
            More booleans representing the flags:

            use_linkage_symbols: if True indicates that as well as global or scopes
                                 symbols, linkage level symbols should be searched
                                 as well.

            search_hd_instead: if True indicates it search symbols from the Hardware
                               Definition data only.
                               
            search_only_types: if True, search only debug symbols that represent
                               types only.

        :returns:
            A tuple containing three lists of strings:

            = ===== ===========================================
            # Field Symbols which contain the partial string...
            = ===== ===========================================
            0 exact precisely
            1 icase with case mismatches
            2 loose in a different order
            = ===== ===========================================

            If no symbols are loaded or if no symbol names match then all three lists
            will be empty.

            All three lists are ordered by closeness of match.
        """
        options = da_types._get_options_from_symbol_complete_parameters(options, *deprecated)
        flags = da_types._get_symbol_complete_flags(options)        
        return SymbolCompleteResult(*self.__context.SymbolComplete(partial, *flags))
        
    def LookUpSymbol(self, address):
        '''Returns the debug symbol at the given address.
        
        :param address: The address to lookup.

        Returns a string containing the name of the symbol at that address.
        If no symbol exists at that address an InvalidArgError is raised.
        
        Example::
        
            def StopAndPrintLocation(thread):
                if thread.IsRunning():
                    thread.Stop()
                pc = thread.ReadRegister('PC')
                try:
                    symbol = thread.LookUpSymbol(pc)
                except DA.Error:
                    symbol = ''
                print("Target halted at 0x%08x:%s" % (pc, symbol or '<no symbol found>'))
        '''
        return self.__context.LookUpSymbol(address)

    def GetSourceFiles(self):
        """Return all :class:`SourceFiles <imgtec.codescape.SourceFile>` of the currently loaded program."""
        return [SourceFile(self.__context, *details) for details in self.__context.GetAllSourceFiles()]

    def GetSourceLineAt(self, address):
        """Returns a :class:`SourceLine <imgtec.codescape.SourceLine>` associated with the address."""
        source_file = SourceFile(self.__context, *self.__context.SourceFileInfoAt(address))
        return source_file.GetStartLine()

    def Disassemble(self, address, count=None):
        """
        Returns a :class:`DisassemblyList <imgtec.codescape.DisassemblyList>`
        results of `count` instructions from the thread at `address`. Or if `count` is None
        returns a single :class:`Disassembly <imgtec.codescape.Disassembly>`
        """
        r = DisassemblyList(Disassembly(*x) for x in self.__context.DisassembleRaw(address, count or 1))
        return r[0] if count is None else r

    def SetStandardInput(self, reader):
        self.__context.SetStandardInput(reader)

    def SetStandardOutput(self, logger):
        """Set the logger to which any stdout messages will be outputted.
        The logger must be a python 'file like' object."""
        self.__context.SetStandardOutput(logger)

    def SetStandardError(self, logger):
        """Set the logger to which any stderr messages will be outputted.
        The logger must be a python 'file like' object."""
        self.__context.SetStandardError(logger)

    def SetLogF(self, logger):
        """Set the logger to which any logf messages will be outputted.
        The logger must be a python 'file like' object."""
        self.__context.SetLogF(logger)

    def SetFileServerOutput(self, logger):
        """Set the logger to which any file server messages will be outputted.
        The logger must be a python 'file like' object."""
        self.__context.SetFileServerOutput(logger)

    def SetSharedLibLogger(self, logger):
        """Set the logger to which any shared library messages will be outputted.
        The logger must be a python 'file like' object."""
        self.__context.SetSharedLibLogger(logger)

    def SetThreadExitHandler(self, logger):
        """Set the logger to which any thread exit messages will be outputted.
        The logger must be a python 'file like' object."""
        self.__context.SetThreadExitHandler(logger)

    def SetBreakpointLogger(self, logger):
        """Set the logger to which any breakpoint log messages will be outputted.
        The logger must be a python 'file like' object."""
        self.__context.SetBreakpointLogger(logger)

    def GetABI(self):
        """Gets the function call ABI name.

        The ABIs available for the thread depends on the target type:

        ======= ============================================================
        Name    ABI
        ======= ============================================================
        meta    Meta.
        numeric MIPS ABI Undefined. All Registers have the numeric names.
        o32     MIPS ABI O32.
        n32     MIPS ABI N32.
        n64     MIPS ABI N64.
        ======= ============================================================
        """
        return self.__context.GetABI()
        
    def GetABIs(self):
        """Gets a list of the valid function call ABI names.
        
        The ABIs available for the thread depends on the target type, see 
        :meth:`GetABI`.
        """
        return self.__context.GetABIs()        

    def SetABI(self, abi):
        """Sets the function call ABI.

        :param abi: The ABI to use.

        The ABIs available for the thread depends on the target type, see
        :meth:`GetABI`.
        """
        self.__context.SetABI(abi)
        
    def GetISA(self):
        """Returns the currently configured ISAs.

        A tuple containing two strings for the ISA for known areas and unknown areas.
        A setting of 'auto' identifies that the sytem will do the default and work it out
        from the elf or processor state.

        To set all addresses to be a specific ISA, set both values to be the 
        same using :meth:`SetISA`.
        
        The ISAs available for the current target depends on the target type :
        
        ============= ======================================================
        name          ISA
        ============= ======================================================
        auto          use the default ISA
        mips16        MIPS16e
        mips32        MIPS32 rev1 - rev5
        mips32r6      MIPS32 rev6
        micromips     MicroMIPS32 rev1 - rev5
        micromips64   MicroMIPS64 rev1 - rev5
        micromipsr6   MicroMIPS32 rev6
        micromips64r6 MicroMIPS64 rev6
        mips64        MIPS64 rev1 - rev5
        mips64r6      MIPS64 rev6
        mcp           MCP
        meta          META
        ============= ======================================================
        """
        return self.__context.GetISA()


    def SetISA(self, known_areas_isa, unknown_areas_isa):
        """Returns a list of the valid ISA names for the current target.
        
        :param known_areas_isa:    For address ranges with debug information which defines the ISA.
        :param unknown_areas_isa:  For address ranges which do not have debug information which defines the ISA.

        By default the `known_areas_isa` will be ``auto``, meaning to extract the 
        ISA from the debug information.  `unknown_areas_isa` will also be set to 
        ``auto``, meaning that the current state of the core will be used.

        See :meth:`GetISA` for a list of possible ISAs for these parameters.
        """
        return self.__context.SetISA(known_areas_isa, unknown_areas_isa)

    def GetISAs(self):
        """Returns a list of the valid ISA names for the current target.
        
        See :meth:`GetISA` for a list of possible ISAs returned.
        """
        return self.__context.GetISAs()
        
    def GetSharedLibraryPath(self):
        '''Gets the current search paths for shared libraries.
        
        Returns a list of the search paths used to locate shared libraries when
        debugging using gdbserver.
        '''
        return self.__context.GetSharedLibraryPath(False)
    
    def SetSharedLibraryPath(self, paths):
        '''Sets the current search paths for shared libraries.

        :param paths: The new list of paths that should be searched for shared libraries.
        
        The shared library path is used to locate shared libraries when 
        debugging using gdbserver ::
        
           paths = thread.GetSharedLibraryPath()
           paths.append('/libs')
           thread.SetSharedLibraryPaths(paths)
        
        '''
        return self.__context.SetSharedLibraryPath(paths, False)

    def BindTC(self, index, start_address):
        """
        Bind a thread context to target/VPE.

        If a VPE is offline and this command executes successfully it will bring
        the VPE online, if already on-line (and successful) another TC is added 

        :param index: The index of the thread context which should be bound.
        :param start_address: Address at which code can be run.
        """
        self.__context.BindTC(index, start_address)

    def GetTCs(self):
        """Return a list of thread context IDs."""
        return self.__context.GetTCs()

    def CreateDTMRequest(self, request_id, period, repeat, channel_no, flags=1, timestamp=0):
        """Create a new :class:`~imgtec.codescape.DTMRequest` object for this thread."""
        dtm = DTMRequest(self.__context, request_id)
        dtm.Setup(period, repeat, channel_no, flags, timestamp)
        return dtm

    def DTMStartAll(self):
        """Start all DTM requests."""
        self.__context.DTMStartAllRequests(self.__context.target)

    def DTMStopAll(self):
        """Stop all DTM requests."""
        self.__context.DTMStopAllRequests(self.__context.target)

    def DTMDeleteAll(self):
        """Delete all DTM requests."""
        self.__context.DTMDeleteAllRequests(self.__context.target)
        
    @contextmanager
    def Locked(self):
        """
        Locks the thread and returns a context which can be used to automatically
        unlock the thread.
        
        .. sourcecode:: python
        
            with thread.Locked():
                pc = thread.ReadRegister("PC")
                thread.WriteRegister("PC", pc + 4)
        """
        self.__context.LockThread()
        try:
            yield
        finally:
            self.__context.UnlockThread()

    def GetEventId(self):
        return "tid:%s" % self.__context.target

    def Bind(self, evt_type, handler):
        """
        Bind an event type to an event handler function.

        Raises :class:`~imgtec.codescape.Error` when not called from within Codescape.
        """
        try:
            from codescape import BindEvent
        except ImportError:
            raise Error("Bind() is only available when running in Codescape")
        else:
            if not self.__events_enabled:
                self.__context.EnableTargetEvents(self.__context.target)
                self.__events_enabled = True
            BindEvent(evt_type, handler, self.GetEventId())

    def Unbind(self, evt_type, handler=None):
        """
        Unbind an event. If handler is specified, that specific handler will
        be unbound. Otherwise, all handlers will be unbound for the specified
        event type.

        Raises :class:`~imgtec.codescape.Error` when not called from within Codescape.
        """
        try:
            from codescape import UnbindEvent
        except ImportError:
            raise Error("Unbind() is only available when running in Codescape")
        else:
            UnbindEvent(evt_type, self.GetEventId(), handler)
            
    def GetProgramFile(self):
        """Return a ProgramFile object for the currently loaded program file."""
        program_file = self.__context.GetProgramFile()
        if not program_file:
            raise Error("GetProgramFile() there is no currently loaded program file")
        return program_file

    abi                  = property(GetABI, SetABI)
    isa                  = property(GetISA, SetISA)
    breakpoints          = property(GetBreakpoints)
    core                 = property(GetCore)
    current_frame        = property(GetCurrentFrame)
    da                   = property(GetDA)
    description          = property(GetDescription)
    diagnostic_file_list = property(GetDiagnosticFileList)
    endian               = property(GetEndian)
    file_server          = property(GetFileServer)
    hwthread             = property(GetHardwareThread)
    id                   = property(GetId)
    info                 = property(GetInfo)
    cpu_info             = property(GetCPUInfo)
    is_hwthread          = property(GetIsHardwareThread)
    is_running           = property(GetIsRunning)
    is_swthread          = property(GetIsSoftwareThread)
    memory               = property(GetMemory)
    memory_names         = property(GetMemoryNames)
    name                 = property(GetName)
    overlay_areas        = property(GetOverlayAreas)
    probe                = property(GetProbe)
    program_file_name    = property(GetProgramFileName)
    semi_hosting         = property(GetSemiHosting)
    source_files         = property(GetSourceFiles)
    state                = property(GetState)
    swthreads            = property(GetSoftwareThreads)
    shared_library_path  = property(GetSharedLibraryPath, SetSharedLibraryPath)
    program_file         = property(GetProgramFile)
    memory_protection    = property(GetMemoryProtection, SetMemoryProtection)
    

class ThreadStatus(object):
    def __init__(self, actual, machine, machine_reason, sequence, description, child_threads, curr_pc = None, callstack_level = None, callstack_pc = None, has_step_out_info = None, notifications = None, child_statuses = None, *args):
        self.actual             = da_types.ActualStatus(actual)
        self.machine            = da_types.MachineStatus(machine)
        self.machine_reason     = da_types.MachineStatusReason(machine_reason)
        self.sequence           = sequence
        self.description        = description.capitalize()
        self.child_threads      = child_threads
        self.curr_pc            = curr_pc
        self.callstack_level    = callstack_level
        self.callstack_pc       = callstack_pc
        self.has_step_out_info  = has_step_out_info
        self.notifications      = notifications
        self.child_statuses     = child_statuses

    @property
    def running(self):
        return self.actual == da_types.ActualStatus.RUNNING or \
               self.machine == da_types.MachineStatus.RUNNING or \
               self.machine == da_types.MachineStatus.TRACING or \
               self.machine == da_types.MachineStatus.BREAKSTEPPING

    def __str__(self):
        return self.description
