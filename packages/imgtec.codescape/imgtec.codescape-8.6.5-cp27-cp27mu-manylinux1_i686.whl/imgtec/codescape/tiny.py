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

import sys, os
from collections import namedtuple
from contextlib import contextmanager
from imgtec.lib import namedenum
import itertools
from imgtec.codescape.da_types import Status, State, RegisterInfo, TLBEntry
from imgtec.codescape.probe_finder import FoundProbe
from imgtec.codescape.disassembly import Disassembly, DisassemblyList
from imgtec.codescape import da_exception
from imgtec.codescape import *
from imgtec.lib.bits import *
from imgtec.codescape import DAscript
from imgtec.codescape import _DAscript
_exception_mapper = da_exception._ExceptionMapper(_DAscript)

class Tiny(DAscript.DAtiny):
    """A low level debugging connection to a probe."""

    def __getattribute__(self, name):
        x = super(Tiny, self).__getattribute__(name)
        if hasattr(x, '__call__'):
            return _exception_mapper.wrap(x)
        return x

    def Disassemble(self, address, count=None, isa='auto', abi='auto', memory=None, display_options="opstrings"):
        res = DAscript.DAtiny.Disassemble(self, address, count, isa, abi, memory, display_options)
        if count is None:
            return Disassembly(*res)
        else:
            return DisassemblyList(Disassembly(*x) for x in res)

    def SoC(self, index):
        """SoC(index)

        Return a :class:`Tiny` instance which will direct it's queries to soc[index] of this probe.

        Before version 8.2 of ``imgtec.codescape.tiny``, it was not possible
        to access the SoCs of a target, all of the cores of each SoC were
        accessible as a flattened list of cores.  For example, if the target has
        the following layout:

            * soc #0
                * core #0 - s0c0
            * soc #1
                * core #0 - s1c0
                * core #1 - s1c1

        Then the cores would be accessed as ::

          assert probe.CoreCount() == 3
          s0c0 = probe.Core(0)
          s1c0 = probe.Core(1)
          s1c1 = probe.Core(2)

        This method has been maintained for backwards compatiblity.  If however
        SoC is called then the cores can be accessed directly:

          assert probe.SoCCount() == 2
          assert probe.SoC(0).CoreCount() == 1
          assert probe.SoC(1).CoreCount() == 2
          assert probe.SoC(1) == 2
          s0c0 = probe.SoC(0).Core(0)
          s1c0 = probe.SoC(1).Core(0)
          s1c1 = probe.SoC(1).Core(1)

        >>> core1 = probe.Soc(0).Core(1)
        >>> core1.ThreadCount()
        4
        >>> c1t2 = core1.Thread(2)
        >>> '0x%08x' % (c1t2.ReadRegister('pc'),)
        '0xbfc000000'
        >>> c1t2.CoreNumber(), c1t2.ThreadNumber()
        (1, 2)
        """
        soc = Tiny(self)
        soc.SetSoC(index)
        return soc

    def SoCNumber(self):
        '''Return the index of this SoC.

        This will be -1 on the default probe.
        '''
        return self.GetSoC()

    def SoCCount(self):
        '''Return the number of SoCs on the target.'''
        return self.GetSoCCount()

    def Core(self, index):
        """Core(index)

        Return a :class:`Tiny` instance which will direct it's queries to core[index] of this probe.

        >>> core1 = probe.Core(1)
        >>> core1.ThreadCount()
        4
        >>> c1t2 = core1.Thread(2)
        >>> '0x%08x' % (c1t2.ReadRegister('pc'),)
        '0xbfc000000'
        >>> c1t2.CoreNumber(), c1t2.ThreadNumber()
        (1, 2)
        """
        core = Tiny(self)
        core.SetTarget(index)
        return core

    def CoreNumber(self):
        """CoreNumber()

        Returns the number of the core on this probe.

        For the first core in a probe this is zero.
        """
        return self.GetTarget()

    def CoreCount(self):
        """CoreCount()

        Returns the number of cores on this probe."""
        return self.GetTargetCount()

    def Thread(self, index):
        """Thread(index)

        Return a :class:`Tiny` instance which will direct it's queries to 
        thread[index] of this core.

        >>> soc0 = probe.SoC(0)
        >>> s0c1 = soc0.Core(1)
        >>> s0c1t2 = s0c1.Thread(2)
        >>> '0x%08x' % (s0c1t2.ReadRegister('pc'),)
        '0xbfc000000'

        .. note:: ``Vpe`` is an alias for ``Thread``.
        """
        core = Tiny(self)
        core.SetThread(index)
        return core
    Vpe = Thread

    def ThreadCount(self):
        """ThreadCount()

        Returns the number of threads on this core.
        
        .. note:: ``VpeCount`` is an alias for ``ThreadCount``.
        """
        return self.GetThreadCount()
    VpeCount = ThreadCount

    def ThreadNumber(self):
        """ThreadNumber()

        Returns the number of this thread. For the first thread in a core this 
        is zero.
        
        .. note:: ``VpeNumber`` is an alias for ``ThreadNumber``.
        """
        return self.GetThread()
    VpeNumber = ThreadNumber        

    def GetState(self):
        """GetState()
        
        Return the current state of the thread as an instance of :class:`~imgtec.codescape.State`.

        The `State` class can be used to determine the current run state of the
        thread, for example::

           thread.Run()
           while thread.state.is_running:
                time.sleep(0.1)
           pc = thread.state.pc
        """
        return State(*DAscript.DAtiny.GetState(self))

    def RegistersInfo(self):
        return [RegisterInfo(*r) for r in DAscript.DAtiny.RegistersInfo(self)]

    def ReadTLB(self, index, guest=False):
        return TLBEntry(*DAscript.DAtiny.ReadTLB(self, index, guest))

    def __enter__(self):
        return self

    def __exit__(self, *args):
       self.Disconnect()
       
    state = property(GetState)
       
__global_tiny = None
def _global_tiny():
    global __global_tiny
    if not __global_tiny:
        __global_tiny = ConnectProbe('')
    return __global_tiny

def DisassembleBytes(address, count, isa, abi, bytes):
    """Disassemble some bytes without connecting to a target.

    Neither `isa` nor `abi` can be "auto".  See :meth:`Tiny.GetABI`, and
    :meth:`Tiny.GetCurrentISA`, for valid values for these parameters.

    If `count` is None then a single instruction is disassembled and returned as
    an instance of :class:`~imgtec.codescape.disassembly.Disassembly`.  If `count` is a positive
    integer then `count` instructions are disassembled and returned as an instance of
    :class:`~imgtec.codescape.disassembly.DisassemblyList`.  If `count` is -1 then as many
    instructions as can be decoded from the given bytes will be disassembled.

        >>> tiny.DisassembleBytes(0x87fe7e70, None, 'mips32', 'o32', '\x03\xE0\x01\x08')
        0x87fe7e70 03e00108    jr        ra

    To disassemble target memory, see :meth:`Tiny.Disassemble`.
    """
    return _global_tiny().Disassemble(address, count, isa, abi, bytes)

def ConnectProbe(da_name, options={}, logger=None):
    """ConnectProbe(identifier[, options])

    Connects to a probe, returning a :class:`Tiny` instance.

    `identifier` is the type and name/number of the probe to connect to.

    ================ ====================================
    DA Type          Identifier Format
    ================ ====================================
    DA-usb           "DA-usb 1"
    DA-net           "DA-net 1"
    Local Simulator  "Simulator HTP221"
    Remote Simulator "RemoteSimulator hostname:port"
    ================ ====================================

    `options` can be either a dictionary (or a list of ``key, value`` pairs),
    used to set options for the connection.

    The possible keys of this parameter depends on the communications type, and
    can be discovered using :func:`~imgtec.codescape.tiny.GetCommsOptions`. Some
    common options include :

    ==================== ==========================================================
    Name                 Meaning
    ==================== ==========================================================
    force-disconnect     If not False connect to the DA even if it is already in
                         use by another user. Please use responsibly.
    search-location      Specify an ip address to find the DA, if dns lookup fails.
    ==================== ==========================================================
    
    logger is an object to receive diagnostic messages. It can be None, a file 
    like object with a write(str) method, or a standard python library 
    logging.Logger instance.

    .. note :: ConnectDA is an alias for this function.

    """
    from imgtec.codescape import _set_virtual_probe_location
    options = _set_virtual_probe_location(options)
    return _exception_mapper.wrap(Tiny)(da_name, options, logger)


def GetCommsOptions(identifier_or_comms_type, include_type_and_documentation=False):
    """Get the available and default values of options which can be used with AddTarget_.

    GetCommsOptions_ returns a dictionary (or a list of ``key, value`` pairs
    if the scripting engine does not support dictionaries) which can be used
    to get the default options for an installed Local Simulator. This can then
    be used to modify the settings used at connection time with AddTarget_.  As
    the following example demonstrates.

    .. sourcecode :: python

        from imgtec.codescape import tiny

        def connect_to_simulator_with_arguments(identifier, *args):
            default_options = tiny.GetCommsOptions(identifier)
            args = "".join((' "%s"' if ' ' in arg else " %s") % (arg,) for arg in args)
            opts = dict(sim=default_options['sim'] + args)
            return tiny.ConnectProbe(identifier, opts)

        target_ids = connect_to_simulator_with_arguments("Simulator HTP265", "--verbose")

    `identifier_or_comms_type` is the identifier of the target, or the comms
    type prefix. For most comms types passing an identifier or a comms type
    produces the same results.

    But for Local Simulators, this will return the options retrieved
    from the .ini file installed with the HSP.

        ================ ================= ================================
        Probe Type       Comms Type        Identifier Format
        ================ ================= ================================
        SysProbe         "SysProbe"        "SysProbe 1"
        DA-net           "DA-net"          "DA-net 1"
        Local Simulator  "Simulator"       "Simulator HTP221"
        Remote Simulator "RemoteSimulator" "RemoteSimulator hostname:port"
        Remote Imperas   "RemoteImperas"   "RemoteImperas hostname:port"
        ================ ================= ================================

    If `include_type_and_documentation` is specified and True, then the returned
    values also contain the type of the option, and a brief explanation of what
    the option is.  It is encoded as a multiline string, where the first line is
    the option value, the second the option type, and documentation follows on any
    remaining lines.
    """
    return _global_tiny().GetCommsOptions(identifier_or_comms_type,
                                       include_type_and_documentation)


def DiscoverProbes(comms_type=''):
    """Returns a list of nearby probes.

    The return is a list of :class:`~imgtec.codescape.FoundProbe`,
    a named tuple containing (identifier, ip, protocol).

    If comms_type is given, then only probes of the given type are returned.

        ================ =================== ================================
        Probe Type       Comms Type          Identifier Format
        ================ =================== ================================
        SysProbe/DA-net  "SysProbe"/"DA-net" "DA-net 1"
        BusBlaster       "BusBlaster"        "BusBlaster BUSBLASTERv3c"
        ================ =================== ================================
    """
    from imgtec.codescape import _set_virtual_probe_location
    options = _set_virtual_probe_location({})
    return [FoundProbe(*x) for x in _global_tiny().DiscoverProbes(comms_type, options)]


def GetConfiguredSimulators():
    """Retrieve a list of the simulators currently available.

    The identifiers returned are suitable for passing directly to ``ConnectProbe``.
    """
    return _global_tiny().GetConfiguredSimulators()


ConnectDA = ConnectProbe
