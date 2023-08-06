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

__all__ = (
    "ActualStatus",
    "BinProgressInterface",
    "BreakpointType",
    "Conditions",
    "Endian",
    "ElementSize",
    "ElementType",
    "ExpressionFlags",
    "LoadType",
    "Log",
    "MachineStatus",
    "MachineStatusReason",
    "Mechanisms",
    "MemoryTypes",
    "OverlayHandler",
    "OSInfo",
    "OSType",
    "ProgressInterface",
    "RegisterInfo",
    "Reliability",
    "SingleShot",
    "Status",
    "State",
    "UnknownStatus",
    "SymbolCompleteOptions",
    "TLBEntry",
    "TargetInfo",
    "WatchAccessSize",
    "WatchAccessTypes",
)

from imgtec.lib.namedenum import namedenum as _verbose_enum
import probe_identifier
from collections import namedtuple
from imgtec.lib.namedbitfield import Field
import re

def namedenum(*args, **kwargs):
    # keep this in this module or pickling will be broken
    # if you need it elsewhere make local copies of it
    # if you need to, exclude it from automodule listings with :exclude-members: namedenum
    kwargs['_doc_usage'] = 'For information on using enumerated types, please see :class:`~imgtec.lib.namedenum.namedenum`'
    return _verbose_enum(*args, **kwargs)

Endian = namedenum('Endian', little=0, big=1)

Reliability = namedenum('Reliability', 'known', 'guess_func', 'guess_label', 'clueless',
    _doc_title="An enum indicating the reliability of the Frame's symbol name.")

ElementType = namedenum('ElementType',
    blob                = 0,
    uint8               = 1,
    uint16              = 2,
    uint32              = 4,
    uint64              = 8,
    int8                = -1,
    int16               = -2,
    int32               = -4,
    int64               = -8,
    float               = 32,
    double              = 64,
)

class ElementSize(object):
    # can't be namedenum because of duplicate values
    uint8               = 1
    uint16              = 2
    uint32              = 4
    uint64              = 8
    int8                = 1
    int16               = 2
    int32               = 4
    int64               = 8
    float               = 4
    double              = 8

class LoadType(object):
    # can't be namedenum because of "binary | symbols" etc
    binary              = 0x01
    symbols             = 0x02
    overlay             = 0x04
    uhi_cmdline_boot    = 0x01000000

    binary_and_symbols  = binary | symbols
    all                 = binary | symbols# | overlay

class MemoryTypes(object):
    Default                 = 0
    MinimDataRam            = 1
    MinimCodeRam            = 2
    DSPRamD0RamA            = 4
    DSPRamD0RamB            = 5
    DSPRamD1RamA            = 6
    DSPRamD1RamB            = 7
    WideDataMemory          = 8
    NarrowDataMemory        = 9
    RegionAMemory           = 8
    RegionBMemory           = 9
    PeripheralMemory        = 10
    MCPSystemBusRegisters   = 12
    BulkMemory              = 13
    ComplexWideDataMemory   = 14
    ComplexRegionAMemory    = 14
    ComplexNarrowDataMemory = 15
    ComplexRegionBMemory    = 15
    JTagMemory              = 16
    RegionLMemory           = 17
    ComplexRegionLMemory    = 18
    MipsEvaUserMode         = 4    
    MipsEvaKernelMode       = 5    
    

OverlayHandler = namedenum('OverlayHandler',
    ('debugger',             0, 'Debugger handles loading of overlays'),
    ('application',          1, 'Application handles loading of overlay but informs debugger of active overlays'),
    ('application_silent',   2, 'Application handles loading of overlay but does not inform debugger of active overlays. User must select overlay manually when target halts'),
)

BreakpointType = namedenum('BreakpointType',
    Code                = 0,
    Data                = 1,
    CodeSoftware        = 5,
    CodeHardware        = 6,
)

WatchAccessSize = namedenum('WatchAccessSize',
    Any	 = 0,
    Byte = 1,
    Word = 2,
    Int	 = 4,
    Quad = 8,
)
    
WatchAccessTypes = namedenum('WatchAccessTypes',
    Read                = 1,
    Write               = 2,
    Any                 = 3,
)
    
Mechanisms = namedenum('Mechanisms',
    AnyAvailable        = 0,
    Software            = 1,
    Hardware            = 2,
)

Conditions = namedenum('Conditions',
    Always                          = 0,
    Expression                      = 1,
    Trigger                         = 2,
    TriggerThenExpression           = 3,
    ExpressionThenTrigger           = 4,
    ExpressionAndTriggerDivCount    = 5,
    ExpressionOrTrigger             = 6,
    ExpressionTriggerTime           = 7,
    Hit                             = 8,
)

SingleShot = namedenum('SingleShot',
    Disabled            = 0,
    Disable             = 1,
    Delete              = 2,
)

Log = namedenum('Log',
    Disabled            = 0,
    Conditionally       = 1,
    Always              = 2,
)

OSType = namedenum('OSType',
    NoOS        = 0,
    Linux       = 1,
    Nucleus     = 2,
    MEOSMeta    = 3,
    MEOS        = 4,
    ThreadX     = 5,
    FreeRTOS    = 6,
    MyNewt      = 7,
    RIOT        = 8,
    Zephyr      = 9,
    GdbServer   = 10,
    MipsTCs     = 11,
)

ActualStatus = namedenum('ActualStatus',
    'UNDEF',
    'ERROR',
    'HALTED',
    'OFFLINE',
    'HARDRESET',
    'SOFTRESET',
    'STOPPED',
    'TRACED',
    'BREAKPOINT',
    'RUNNING',

    'BREAKSOFT',
    'BREAKHARD',
    'CPUTRACED',
    'EXCEPTION',
    'SUSPENDED',   #    The thread is an OS thread and the OS is halted
    'PAUSED',      #    Thread ispaused because breakpoint has triggered on another thread
    'EXEC',        #    The thread has exec'ed
    
    'STOPPED_GDB',  # This thread has stopped because some other thread has stopped
                    # and gdbserver has stopped all others
    'CPU_HALTED',   # The cpu has halted (which is not an exception i.e. IASim stops 
                    # all threads when one is stopped) in some cases the reason may 
                    # be known (e.g. MCP - cp-return halt)
)

MachineStatus = namedenum('MachineStatus',
    # These are effectively all ERROR states
    'UNDEF',
    'ERROR',
    'LOGICERROR',

    # This state flags a processor offline (temporarily busy due to target hardware access)
    # The SEGA Saturn and Mars have SMPC controller which can reset a processor (take it offline temporarily)
    'OFFLINE',

    # this is a transitory state after a EXECREQ_INIT has been completed, allowing the status to be (re)determined
    'INITIAL',

    # These are states where the processor execution is halted
    'HARDRESET',
    'SOFTRESET',
    'STOPPED',
    'TRACED',
    'BREAKPOINT',    # halted due to user defined breakpoint
    'BREAKINTERNAL',  # halted due to internal breakpoint

    # These are states where we expect continued processor execution
    'RUNNING',
    'TRACING',

    # BREAKSTEPPING used to step over a breakpoint
    'BREAKSTEPPING',

    # This state flags an unknown (or unexpected) processor exception encountered
    'EXCEPTION',

    # Thread is an OS thread and the main OS thread is halted
    'SUSPENDED',

    # Thread is an OS thread and is paused by a breakpoint on another thread
    'PAUSED',

    # Thread is stopped because of an assertion failre
    'ASSERT',

)

MachineStatusReason = namedenum('MachineStatusReason',
    'UNDEF',
    'USER_INSERTED_BREAKPOINT',
    'FILESERVER_BIOSCALL'
)

Status = namedenum('Status',
    # [[[cog
    # from imgbuild.SConsPaths import sys_path_append_sw
    # sys_path_append_sw('comms', 'comms')
    # import cog, joyner, outputters
    # for value in joyner.status.values:
    #     cog.outl("'%s', %s # %s" % (value.name, ' ' * (20 - len(value.name)), value.doc))
    # ]]]
    'running',               # The Probe is not preventing the core from executing
    'stopped',               # A stop was issued
    'halted_by_probe',       # The probe halted the target to access resources
    'single_stepped',        # A single step was issued
    'exception',             # An unknown exception state occurred
    'memory_fault',          # A memory fault exception state occurred
    'sw_break',              # A software breakpoint was hit
    'hw_break',              # A hardware breakpoint triggered
    'expected_reset',        # A reset was issued
    'unexpected_reset',      # A reset occurred for some other reason
    'soft_reset',            # A soft reset was issued
    'running_no_debug',      # The target is running without debug
    'in_reset',              # Target is held in reset
    'core_offline',          # A particular core in a multicore Soc has gone off-line eg clocks or power disabled by a master / host system
    'target_offline',        # The target is not connected or is powered off
    'mtx_locked_up',         # Target (MTX) has locked up
    'target_not_ready',      # The Target SoC is not communicating with the probe and needs a Hard-Reset
    'vpe_has_no_tcs',        # The VPE has no TCs bound to it so cannot run or be debugged
    'powered_off',           # The Target is powered off - no voltage present on Vsense
    'debugging_disabled',    # Debugging of the core has been disabled using coredebugging(disabled)
    'thread_offline',        # The thread is disabled
    # [[[end]]]
)

class _HexLong(long):
    """As long but prints as hex, with an optionally given byte size.

    >>> _HexLong(0x1234)
    0x00001234
    >>> _HexLong(0x1234, 2)
    0x1234
    """
    def __new__(cls, value, size=4):
        x = long.__new__(cls, value)
        x._size = size
        return x

    def __repr__(self):
        return ('0x%%0%dx' % (self._size*2,)) % (long(self),)

class UnknownStatus(long):
    def __str__(self):
        return 'unknown (%d)' % long(self)
    def __repr__(self):
        return "UnknownStatus.unknown"

class State(object):
    """The state of a thread(vpe)."""
    def __init__(self, status, pc, status_bits):
        try:
            self.status = Status(status)
            """The run state of the thread(vpe)."""
        except ValueError:
            self.status = UnknownStatus(status.rsplit(' ', 1)[1][:-1])

        self.pc = _HexLong(pc, 4)
        """The current value of the PC, only valid if is_running is False."""

        self.status_bits = _HexLong(status_bits, 2)
        """Extra information about the status of the target.  This target
        specific, and not currently documented."""

    @property
    def is_running(self):
        """True if the status is one of the running statuses."""
        return self.status in (Status.running, Status.running_no_debug)

    def __repr__(self):
        pc = ''
        if not self.is_running:
            pc = 'pc=%r' % (self.pc,)
        extra = ''
        if self.status_bits:
            extra = ' status_bits=0x%04x' % (long(self.status_bits),)
        return "status=%s %s%s" % (self.status, pc, extra)


SymbolCompleteOptions = namedenum('SymbolCompleteOptions',
    'globals',                      # match against all debug symbols
    'globals_with_linkage_symbols', # match against all debug symbols together with all linkage symbols
    'scoped',                       # match against symbols that are in scope only
    'scoped_with_linkage_symbols',  # match against symbols that are in scope only together with all linkage symbols
    'registers',                    # match against symbols from hardware definition of specified target
    'types',                        # match against all debug symbols that represent types only
)

_SymbolCompleteFlags = namedtuple('SymbolCompleteFlags', ['only_symbols_in_scope', 'use_lo_symbols', 'only_hd_symbols', 'only_type_symbols'])

def _get_symbol_complete_flags(options):
    """ Convert options parameter of type SymbolCompleteOptions enum into a SymbolCompleteFlags tuple. """
    if options == SymbolCompleteOptions.globals:
        return _SymbolCompleteFlags(False, False, False, False)
    if options == SymbolCompleteOptions.globals_with_linkage_symbols:
        return _SymbolCompleteFlags(False, True, False, False)
    if options == SymbolCompleteOptions.scoped:
        return _SymbolCompleteFlags(True, False, False, False)
    if options == SymbolCompleteOptions.scoped_with_linkage_symbols:
        return _SymbolCompleteFlags(True, True, False, False)
    if options == SymbolCompleteOptions.registers:
        return _SymbolCompleteFlags(False, False, True, False)
    return _SymbolCompleteFlags(False, False, False, True)

def _get_symbol_complete_options(flags):
    """ Convert flags parameter of type SymbolCompleteFlags tuple into a SymbolCompleteOptions enum. """
    if flags.only_hd_symbols:
        return SymbolCompleteOptions.registers
    if flags.only_type_symbols:
        return SymbolCompleteOptions.types
    if flags.only_symbols_in_scope:
        if flags.use_lo_symbols:
            return SymbolCompleteOptions.scoped_with_linkage_symbols
        return SymbolCompleteOptions.scoped
    if flags.use_lo_symbols:
        return SymbolCompleteOptions.globals_with_linkage_symbols
    return SymbolCompleteOptions.globals
    
def _get_options_from_symbol_complete_parameters(options, *deprecated):
    if isinstance(options, bool):
        flags = _SymbolCompleteFlags(options, *deprecated)
        options = _get_symbol_complete_options(flags)
    return options

TLBEntry2 = namedtuple('TLBEntry2', ['entrylo0', 'entrylo1', 'entryhi', 'pagemask', 'guestctl1'])
class TLBEntry(TLBEntry2):
    def __new__(cls, entrylo0, entrylo1, entryhi, pagemask, guestctl1=0):
        return TLBEntry2(entrylo0, entrylo1, entryhi, pagemask, guestctl1)

class TargetInfo(object):
    """Used to decode the return of GetTargetInfo."""
    def __init__(self, da_identifier, da_location, core_index, core_type, hwthread_name, swthread_name = '', dns_name='', jtag = 0, core_offline_any = True, core_id = 0, processor_family='', is_64bit=False, soc_index=0, soc_name='', *args):
        self.da_identifier = probe_identifier.normalise(da_identifier)
        """The identifier of the probe, e.g. DA-net 00022"""

        self.da_location = da_location
        """The location of the probe, e.g. '192.168.1.2' or 'USB'."""

        self.core_index = int(core_index)
        """The zero-indexed index of this core. (integer)."""

        self.core_type = core_type
        """The type of the core, e.g. 'META-122-1'."""

        self.hwthread_name = hwthread_name
        """The name of the hardware thread processor, e.g. 'Thread0-DSP'."""

        self.swthread_name = swthread_name
        """The software thread name or number if this is a software thread.
        e.g. '0' or 'MeOS Task name'. An empty string if this is not a software
        thread."""

        self.dns_name = dns_name
        """The DNS name of the probe, if valid."""

        self.jtag = jtag
        """The jtag id of the SoC this target comes from."""

        """ The core is offline if any thread is offline, otherwise if the specific thread is offline """
        self.core_offline_any = core_offline_any

        """ The core id of the target. Used to identify the core. """
        self.core_id = core_id

        """ The processor family of the target, e.g. 'mips', 'meta' or 'mcp'."""
        self.processor_family = processor_family

        self.is_64bit = is_64bit
        """True if the processor has a 64-bit architecture."""

        self.soc_index = soc_index
        """The zero-indexed index of the soc in the target."""
        
        self.soc_name = soc_name
        """The name of this soc if a HSP was loaded, otherwise it is an empty string."""
        

        self._args = args

    def _as_tuple(self):
        return (self.da_identifier, self.da_location, self.core_index,
                self.core_type, self.hwthread_name, self.swthread_name,
                self.dns_name)

    def __cmp__(self, rhs):
        return cmp(self._as_tuple(), rhs._as_tuple())

    def __repr__(self):
        return "%s%r" % (self.__class__.__name__, self._as_tuple())

    def __str__(self):
        try:
            thread = '^Software Thread %d' % int(self.swthread_name)
        except ValueError:
            thread = ''
            if self.swthread_name:
                thread = '^%s' % self.swthread_name
        return "%s @ %s : %d - %s-%s%s" % (self.da_identifier, self.da_location,
            self.core_index, self.core_type, self.hwthread_name, thread)

class RegisterInfo(object):
    """Used to decode the return of RegistersInfo."""
    def __init__(self, name, index, size, is_float, aliases=[], fields=[], description='', *_extras):
        self.name = name
        """The canonical name of the register."""
        
        self.index = index
        """The internal index of the register."""

        self.size = size
        """The size of the register in bytes."""
        
        self.is_float = is_float
        """True if this is a float register."""
        
        self.aliases = aliases
        """A list of alternative names for this register."""
        
        self.fields = [Field(*field) for field in fields]
        for field in self.fields:
            if field.type != long:
                #List of names that have been seen in the original field type
                used_names = []
                
                for enum_val in field.type:
                    old_name = enum_val[0]
                    
                    if enum_val[0] in used_names:
                        #Can't have duplicate names
                        enum_val[0] = '_'.join([enum_val[0], str(used_names.count(enum_val[0]))])
                    
                    if enum_val[0] == 'None':
                        #Can't assign to None
                        enum_val[0] = '_None'
                    if enum_val[0].startswith('_'):
                        #Can't have underscores at the beginning
                        enum_val[0] = 'e' + enum_val[0]
                        
                    # Append here so that the first instance doesn't look like a duplicate
                    # but append the original name so that we can still count the number of times
                    # the name appears in the original fields.
                    used_names.append(old_name)
                    
                while True:                    
                    try:
                        field.type = namedenum(field.name, *field.type)
                    except ValueError as e:
                        pattern = r"Encountered\sduplicate\senum\svalue:\s.*=(?P<value>\d+)\s\([^\']*'(?P<name>[^']+)'\)"
                        m = re.match(pattern, e.message)
                        if m:
                            field.type.remove([m.group('name'), int(m.group('value'))])
                        else:
                            raise e
                    else:
                        break
                    
        """A list of Field objects"""
        
        self.description = description
        self._extras = _extras
        
    def __repr__(self):
        return "%s (size=%s, is_float=%s, aliases=%s, description=%s)" % (
            self.name, self.size, self.is_float, ', '.join(self.aliases), self.description)

class ExpressionFlags(object):
    """Flags which can be passed to the flags parameter of    
    Thread.\ :meth:`~imgtec.codescape.Thread.Evaluate` and
    Thread.\ :meth:`~imgtec.codescape.Thread.GetSymbol`.

    .. versionadded:: imgtec.codescape 1.2.3.0

    """

    allow_function_calls = 0x1
    """
    Allow function calls to form part of the expression ::
    
        from imgtec import codescape

        def call_fn_on_target(thread, fn):
            return thread.Evaluate(fn, codescape.ExpressionFlags.allow_function_calls)

        assertEquals(100, call_fn_on_target(thread, "abs(-100)"))

    .. note :: Calling functions on the target is not available on all targets and OSs.

    """

    allow_read_once      = 0x2
    """
    Allow reading of memory locations which are marked as read once ::

        from imgtec import codescape
        def get_byte_from_serial_port(port):
            return thread.Evaluate("UART_PORT_%d" % (port,), codescape.ExpressionFlags.allow_read_once)

    """

class OSInfo(object):
    """Operating system information returned from DA.GetOSInfo()."""

    def __init__(self, os_type=0, uses_stub=False, bp_instr_size=0, bp_instr=0, barred_addresses=[], is_kernel_thread=False, is_gdb_linux=False, is_smp=False, *extra_args):
        try:
            self.os_type = OSType(os_type)
        except ValueError:
            self.os_type = os_type
        self.uses_stub = uses_stub
        self.bp_instr_size = bp_instr_size
        self.bp_instr = bp_instr
        self.barred_addresses = barred_addresses
        self.is_kernel_thread = is_kernel_thread
        self.is_gdb_linux = is_gdb_linux
        self.extra_args = extra_args
        self.is_smp = is_smp
        
class ProgressInterface(object):
    """The interface expected by functions taking a Progress object.

    imgtec.codescape will call methods of the progress object (which need not be
    derived from this object but it should have all of the methods) at
    certain points during the action.

    Example usage ::

        from imgtec import codescape

        class ConsoleProgress(codescape.ProgressInterface):
            def __init__(self):
                self._previous_percentage = None
            def set_percentage(self, percentage):
                p = int(percentage)
                if p != self._previous_percentage:
                    print "set_percentage : %d%%" % p
                self._previous_percentage = p

        progress = ConsoleProgress()
        thread = codescape.GetSelectedThread()
        thread.memory.SaveBinaryFile('core_mem.bin', 0x80000000, 64 * 1024, progress)

    """
    def should_continue(self):
        """Called periodically, return False to interrupt the action.

        This implementation returns True.
        """
        return True
    def set_percentage(self, percentage):
        """Called periodically with a float argument in the range [0, 100] to
        indicate the progress of the main action."""
    def add_message(self, message):
        """Called periodically whenever an event occurs. The message does
        not include a line feed."""
    def enable_progress(self, enable):
        """Called with a boolean argument at the start of an action to
        indicate that the progress of the main action is active (or not)."""

class BinProgressInterface(ProgressInterface):
    """The interface expected by functions taking a BinProgress object.

    The progress of the loading of the debug information and the downloading
    of the binary to the target are split into two actions because they are
    executed synchronously.  The main action is the loading of the debug
    information and the 'bin' action is the binary download.

    The 'bin' actions will typically be called in a separate thread so you
    may need to take care to correctly protect any shared state.

    Example usage ::

        from imgtec import codescape

        class BinConsoleProgress(codescape.BinProgressInterface):
            def __init__(self):
                self._previous_percentage = None
                self._previous_bin_percentage = None
            def set_percentage(self, percentage):
                p = int(percentage)
                if p != self._previous_percentage:
                    print "set_percentage : %d%%" % p
                self._previous_percentage = p
            def set_bin_percentage(self, percentage):
                p = int(percentage)
                if p != self._previous_bin_percentage:
                    print "set_bin_percentage : %d%%" % p
                self._previous_bin_percentage = p

        progress = BinConsoleProgress()
        thread = codescape.GetSelectedThread()
        thread.LoadProgramFileEx('file.py', 3, True, progress)

    """
    def set_bin_percentage(self, percentage):
        """Called periodically with a float argument in the range [0, 100] to
        indicate the progress of the main action."""
    def enable_bin_progress(self, enable):
        """Called with a boolean argument at the start of an action to indicate that
        the progress of the binary download action is active (or not)."""

