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

import sys, itertools, types, atexit
import da_exception
import da_types
from breakpoint import BreakpointList
from soc import SoC, _create_children, _target_info_attrgetter
import logging

logger = logging.getLogger('imgtec.codescape')

try:
    _nullHandler = logging.NullHandler
except AttributeError:
    class _nullHandler(logging.Handler):
        def handle(self, record):
            pass

        def emit(self, record):
            pass

        def createLock(self):
            self.lock = None
            
logger.addHandler(_nullHandler())

class Probe(object):
    """Representation of a Probe (Debug Adapter) connecting the host computer to the debug target."""

    _cache = {}
    """Remembers existing Probe object trees created to avoid re-creating them."""

    def __init__(self, descendent_contexts):
        self.__context = descendent_contexts[0]
        self.__name = self.__context.target_info.da_identifier
        self.__location = self.__context.target_info.da_location
        self.__dns_name = self.__context.target_info.dns_name
        self.__jtag_id = self.__context.target_info.jtag
        self.__socs = _create_children(self, descendent_contexts, SoC, 'soc_index')

    def Disconnect(self):
        """Disconnects current target."""
        self.__context.RemoveTarget(self.__name)
        da_map = Probe._cache.get(self.__context.wrapped_dascript, {})
        try:
            del da_map[self.__name]
        except KeyError:
            pass

    def __str__(self):
        return self.__name

    def __repr__(self):
        return 'Probe(%s)' % (self.__name,)

    def GetProbe(self):
        """Returns this :class:`Probe <imgtec.codescape.Probe>`."""
        return self
    GetDA = GetProbe

    def GetName(self):
        """Name of the debug adapter."""
        return self.__name

    def GetDescription(self):
        """Description."""
        return self.name

    def GetLocation(self):
        """Location."""
        return self.__location

    def GetDnsName(self):
        """DNS name."""
        return self.__dns_name

    def GetJTagID(self):
        """JTAG identifier where available."""
        return self.__jtag_id
        
    def GetFirmwareVersion(self):
        '''Return the firmware version of the probe.'''
        return self.__context.GetFirmwareVersion(self.name)

    def GetSoCs(self):
        """List of :class:`SoCs <imgtec.codescape.SoC>` on this Probe."""
        return self.__socs

    def GetCores(self):
        """List of :class:`Cores <imgtec.codescape.Core>` on this Probe."""
        return list(itertools.chain.from_iterable(soc.cores for soc in self.__socs))

    def GetHardwareThreads(self):
        """List of hardware :class:`Threads <imgtec.codescape.Thread>` on this Probe."""
        return list(itertools.chain.from_iterable(soc.hwthreads for soc in self.__socs))

    def GetBreakpoints(self):
        """
        Return a :class:`~imgtec.codescape.BreakpointList` containing all
        breakpoints on this Probe.
        """
        target_breakpoints = list(itertools.chain.from_iterable(child.breakpoints for child in self.cores))
        return BreakpointList(self.__context, target_breakpoints)

    def GetDASettingList(self):
        """Returns list of DA settings names."""
        return self.__context.GetDASettingList()

    def GetDASettingValue(self, name):
        """
        Return the DA setting value associated with the setting name given.
        Raises a Error if the name given is not in the list returned by GetDASettingList.
        
        This only returns the value; previously this method returned the type of the
        value as a enum type although I cannot see where this is used. Am I correct in
        removing the value type.
        """
        value, type = self.__context.ReadDASetting(name)
        return value

    def SetDASettingValue(self, name, value):
        """
        Set the DA setting value associated with the setting name given.
        Raises :class:`~imgtec.codescape.Error` if the name given is not in the 
        list returned by GetDASettingList.
        """
        self.__context.WriteDASetting(name, value)

    def GetHSPSettings(self):
        """
        Return the current HSP path or None if no HSP has been set.
        """
        active, paths = self.__context.GetHSPSettings(self.name)
        if active and paths:
            return paths[0]
        else:
            return None

    def SetHSPSettings(self, hsp_path):
        """
        Load a HSP specified by path, or None to disable HSP.
        """
        files = [] if hsp_path is None else [hsp_path]

        self.__context.SetHSPSettings(self.name, True, files)
        self.__context.ReloadHSPFiles(self.name, None)
        
    def AcknowledgeReset(self):
        """some docs here TODO"""
        self.__context.AcknowledgeReset(self.name)
        
    def GetScanTargetLog(self):
        '''Returns the log produced during the connection to this probe.'''
        return self.__context.GetScanTargetLog(self.name)
        
    def EnableAllMemory(self):
        """Allows access to all of memory, irrespective of any HSP configurations 
        which restrict memory access.

        Calling this function allows access to all memory for all thread objects
        on this probe.

        This change can make certain operations, such as callstack decoding,
        crash the target by accessing areas of memory which are not correctly
        handled as a bus error.
        """
        self.__context.EnableAllMemory(self.name)
        
    def GetJTAGClock(self):
        '''Returns the JTAG TCK frequency in kHz.'''
        return self.__context.GetJTAGClock()
        
    def SetJTAGClock(self, frequency):
        '''Sets the JTAG TCK frequency in kHz.
        
        Valid frequencies depend on the probe type :

        +--------------+----------------------------------------+
        |DA type       | Valid frequencies                      |
        +==============+========================================+
        | SysProbe     | In the range 5kHz to 30000kHz.         |
        +--------------+----------------------------------------+
        |              | Valid frequencies are one of :         |
        |              +-----------+----------------------------+
        |              |   20MHz   | 20000                      |
        |              +-----------+----------------------------+
        |              |   10MHz   | 10000                      |
        |              +-----------+----------------------------+
        | DA-net,      |   5MHz	   |  5000                      |
        | DA-trace,    +-----------+----------------------------+
        | DA-usb       |   2.5MHz  |  2500                      |
        |              +-----------+----------------------------+
        |              |   1.25MHz |  1250                      |
        |              +-----------+----------------------------+
        |              |   625kHz  |   625                      |
        |              +-----------+----------------------------+
        |              |   312kHz  |   312                      |
        |              +-----------+----------------------------+
        |              |   156kHz  |   156                      |
        +--------------+-----------+----------------------------+
        
        As probes do not support all frequencies, the return of this function 
        can be used to determine the frequency that was actually set.
        '''
        return self.__context.SetJTAGClock(frequency)

    def CreateTeam(self, members):
        '''Create a team for synchronous run control.

        Teams allow hardware threads and cores to be started and halted together.
        Once a thread is a member of a team then a run of any thread in that
        team will cause all team members to run.  Similarly if any thread should
        halt (either because of an explicit stop command or a breakpoint is hit)
        then all team members will halt.

        To use, first create a team containing the desired members.  Currently
        it is a requirement that no thread can be a member of more than one 
        team.

        `members` is a list of socs, cores, or hardware threads.  If SoCs or
        cores are passed then all threads within that SoC or core is added to
        the team.

        ``CreateTeam`` returns the team_id, a string uniquely identifying the
        team. The returned team_id can be used with :meth:`DeleteTeam`.
        '''
        def expand(things):
            threads = []
            for thing in things:
                try:
                    threads.extend(thing.hwthreads)
                except AttributeError:
                    threads.append(thing)
            return threads
        tids = [t.id for t in expand(members)]
        return self.__context.CreateTeam(tids)

    def DeleteTeam(self, team_id):
        '''Deletes a team or all teams.

        `TeamID` is the team to delete, as returned by :meth:`CreateTeam`, or
        or "all" to delete all teams.
        '''
        self.__context.DeleteTeam(team_id)

    def ListTeams(self):
        '''List all teams and members of teams as a dictionary.

        The returned dictionary maps TeamID->members where members
        is a list of hardware threads.
        '''
        res = {}
        for team, member_ids in self.__context.ListTeams().items():
            res[team] = [t for t in self.hwthreads if t.id in member_ids]
        return res
        
    breakpoints      = property(GetBreakpoints)
    cores            = property(GetCores)
    da               = property(GetDA)
    description      = property(GetDescription)
    dns_name         = property(GetDnsName)
    da_setting_list  = property(GetDASettingList)
    hsp_settings     = property(GetHSPSettings, SetHSPSettings)
    hwthreads        = property(GetHardwareThreads)
    jtag_id          = property(GetJTagID)
    location         = property(GetLocation)
    firmware_version = property(GetFirmwareVersion)
    name             = property(GetName)
    probe            = property(GetProbe)
    socs             = property(GetSoCs)
    jtag_clock       = property(GetJTAGClock, SetJTAGClock)

non_target_functions = frozenset([
    'AcquireTargetsExclusively',
    'AddTarget',
    'AddTargetOn',
    'ClearAllBreakpointsOnTarget',
    'ConfigureTarget',
    'CopyData',
    'CreateBreakpointOnTarget',
    'CurrentTarget',
    'DTMAddDataRequest',
    'DTMDeleteAllRequests',
    'DTMDeleteRequest',
    'DTMRequestSetup',
    'DTMStartAllRequests',
    'DTMStopAllRequests',
    'Disconnect',
    'DuplicateBreakpointToTarget',
    'EnableOSDebug',
    'EnableTargetEvents',
    'EnableAllMemory',
    'ForceDisconnectOwner',
    'GetAllTargets',
    'GetBSPErrors',
    'GetCommsDiagnosticLog',
    'GetCommsErrorLog',
    'GetCurrentTarget',
    'GetDevicesToConnect',
    'GetFirmwareVersion',
    'GetFirstTarget',
    'GetName',
    'GetNextTarget',
    'GetScanTargetLog',
    'GetUnconnectedTargets',
    'GetVersion',
    'IsChildThread',
    'IsTargetRunning',
    'Reflash',
    'RemoveTarget',
    'RunAllTargets',
    'RunTarget',
    'SelectTarget',
    'SetBreakpointLogger',
    'SetFileServerOutput',
    'SetOSFeature',
    'SetOverlayHandlingMode',
    'SetSharedLibLogger',
    'SetSharedLibrarySearchPaths',
    'StopAllTargets',
    'StopTarget',
    'TryConnectTarget',
    'UpdateTargets',
    'UseTarget',
    'UseTargetOn',
    'ValidCurrentTarget',
])

class DAScriptWrapper(object):
    def __init__(self, dascript, real_dascript):
        self.__dascript = dascript
        self.__real_dascript = real_dascript
        self.__selected_target = None
        self.__contexts = {}
        self.__exception_mapper = da_exception._ExceptionMapper(real_dascript)

    def GetTargetContext(self, target):
        """ Get Context associated with specified target."""
        context = self.__contexts.get(target)
        if context is None:
            context = TargetContext(self, target)
            self.__contexts[target] = context
        return context

    def SelectTarget(self, target, magic=False):
        if not magic:
            raise TypeError("SelectTarget should not be called explicitly. Please use GetTargetContext() instead.")
        if target != self.__selected_target:
            self.__dascript.SelectTarget(target)
            self.__selected_target = target

    def UsingDAscript(self):
        return bool(self.__real_dascript)

    def InvalidateSelectedTarget(self):
        self.__selected_target = None

    def __getattr__(self, name):
        dascriptfn = getattr(self.__dascript, name)
        return self.__exception_mapper.wrap(dascriptfn)

class TargetContext(object):
    """
    Looks like DAscript but automatically selects the target before
    script functions are called. This is optimised so that SelectTarget
    is not called if it is already the current target.
    """

    def __init__(self, wrapped_dascript, target):
        self.wrapped_dascript = wrapped_dascript
        self.target = target
        self.target_info = da_types.TargetInfo(*self.GetTargetInfo())

    def __getattr__(self, name):
        da_func = getattr(self.wrapped_dascript, name)
        if name in non_target_functions or hasattr(DAScriptWrapper, name):
            return da_func
        else:
            def wrapper(*args, **kwargs):
                self.wrapped_dascript.SelectTarget(self.target, True)
                return da_func(*args, **kwargs)
            return wrapper

class GetWrappedDAScript(object):
    def __init__(self):
        self.dascript = None
        self.wrapped_dascript = None

    def disconnect(self):
        dascript, self.dascript = self.dascript, None
        if (dascript is not None and dascript.__module__ in sys.modules
            and getattr(sys.modules[dascript.__module__], "_DAscript", None) is not None):
            dascript.Disconnect()

    def __call__(self):
        if self.dascript is None:
            real_dascript = None
            try:
                # Try Codescape DA interface
                from codescape.da import GetLegacyDA
                self.dascript = GetLegacyDA()
            except ImportError:
                # Use extension module
                import DAscript
                if getattr(DAscript, "_DAscript", None) is None:
                    raise ImportError("DAscript module has been unloaded")
                self.dascript = DAscript.CreateDA()
                # Disable automatic connection to targets
                try:
                    self.dascript.DoNotScanTargets()
                except AttributeError:
                    pass
                self.dascript.SetLogger(logger)
                atexit.register(self.disconnect)
                # Put it here so CSUtils can find it (for load scripts)
                def CreateDA():
                    return self.dascript
                CreateDA.__module__ = "DAscript"
                fake_module = types.ModuleType("DAscript")
                fake_module.CreateDA = CreateDA
                sys.modules["DAscript"] = fake_module
                real_dascript = DAscript._DAscript
            self.wrapped_dascript = DAScriptWrapper(self.dascript, real_dascript)
        return self.wrapped_dascript

GetWrappedDAScript = GetWrappedDAScript()

def GetDAScript(dascript=None):
    """
    Returns global DAscript object if dascript argument is None, otherwise
    checks argument is an instance of DAScriptWrapper and returns it.
    """
    if dascript is None:
        return GetWrappedDAScript()
    if not hasattr(dascript, 'GetTargetContext'):
        raise ValueError("dascript argument must be an instance of imgtec.codescape.probe.DAScriptWrapper")
    return dascript

def GetConnectedProbes(dascript=None):
    """
    Return a list of all connected probes (:class:`~imgtec.codescape.Probe` objects).
    
    Only those probes which are already connected to will be returned. If running 
    within Codescape this will include all the probes in Codescape's target tree.  
    If running standalone you should call 
    :func:`~imgtec.codescape.ConnectProbe` before calling this function.
    
    .. sourcecode:: python

        import sys
        from imgtec import codescape
        if codescape.environment == 'standalone':
            codescape.ConnectProbe(sys.argv[1])
        for da in codescape.GetConnectedProbes():
            print da.name
    """
    dascript = GetDAScript(dascript)
    da_map = Probe._cache.get(dascript, {})
    Probe._cache[dascript] = da_map

    context_list = []
    for tid in dascript.GetAllTargets():
        try:
            context_list.append(dascript.GetTargetContext(tid))
        except Exception:
            pass

    da_list = []
    for da_id, contexts in itertools.groupby(context_list, _target_info_attrgetter('da_identifier')):
        try:
            da = da_map[da_id]
        except KeyError:
            da = da_map[da_id] = Probe(list(contexts))
        da_list.append(da)
    return da_list
