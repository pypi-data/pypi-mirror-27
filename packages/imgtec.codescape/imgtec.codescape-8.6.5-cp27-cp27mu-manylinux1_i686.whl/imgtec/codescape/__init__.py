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

from da_exception import *

__all__ = (
    "BinProgressInterface",
    "Breakpoint",
    "BreakpointList",
    "ConnectProbe",
    "Core",
    "DiagnosticError",
    "ExpressionFlags",
    "FileServerError",
    "FindConnectedProbe",
    "FindThreads",
    "ForceAssertionFailure",
    "FoundProbe",
    "FrameError",
    "GetBreakpointThread",
    "GetCommsDiagnosticLog",
    "GetConfiguredProbes",
    "GetConnectedProbes",
    "GetDAConfigList",
    "GetFirstProbe",
    "GetFirstThread",
    "GetRegionThread",
    "GetScanTargetLog",
    "GetSelectedThread",
    "OverlayError",
    "OverlayHandler",
    "Probe",
    "ProgressInterface",
    "Reliability",
    "SoC",
    "SourceFile",
    "SourceLine",
    "SymbolCompleteOptions",
    "Thread",
    #Exceptions
    # [[[cog
    # import cog
    # from imgbuild.SConsPaths import sys_path_append_sw
    # sys_path_append_sw('tiny_scripting', 'tiny_scripting')
    # import exception_types
    # for exc in exception_types.base_first():
    #    cog.outl('"%s",' % exc)
    # ]]]
    "Error",
    "BreakpointError",
    "CommsBaseError",
    "ExecutionStateError",
    "InvalidArgError",
    "LicenseError",
    "NotAnELF",
    "OperationCancelled",
    "ProfilerError",
    "ProgramFileError",
    "TargetError",
    "ThreadInvalidError",
    "ArgumentNotSuppliedError",
    "AssertionFailed",
    "CallBackError",
    "CommsError",
    "CommsProbeError",
    "CommsTargetError",
    "CoreDisabled",
    "CoreOffline",
    "ExpressionEvaluationError",
    "InvalidConversion",
    "LicenseCheckoutError",
    "LicenseConsistencyError",
    "LoadProgramFileError",
    "ResetOccurred",
    "TargetAlreadyConnected",
    "TargetDisconnected",
    "TargetInvalid",
    "TargetNotFound",
    "UnrecoverableMemoryFault",
    "CommsBadChannelNumberError",
    "CommsDeviceInUseError",
    "CommsDeviceNotFoundError",
    "CommsNoTransportFoundError",
    "CommsPayloadMissingError",
    "CommsPayloadShortError",
    "CommsProbeConnectionRefusedError",
    "CommsProbeFatalError",
    "CommsProbeFlashDataBadError",
    "CommsProbeFlashEraseError",
    "CommsProbeFlashImageCorruptError",
    "CommsProbeFlashWriteError",
    "CommsProbeTimeoutError",
    "CommsRegisterInvalidDataSizeError",
    "CommsSimInUseError",
    "CommsSimNotFoundError",
    "CommsTargetAddressError",
    "CommsTargetChannelBufferEmptyError",
    "CommsTargetChannelBufferFullError",
    "CommsTargetCheckInquiryError",
    "CommsTargetCommandNotAvailableError",
    "CommsTargetCommandUnknownError",
    "CommsTargetCountError",
    "CommsTargetFatalError",
    "CommsTargetJtagIncompatibleError",
    "CommsTargetMmuAddressNotMappedError",
    "CommsTargetMtxMemoryFaultError",
    "CommsTargetParameterError",
    "CommsTargetRejectedBusyError",
    "CommsTargetThread0BusError",
    "CommsTargetThread0JtagError",
    "CommsTargetThread1BusError",
    "CommsTargetThread1JtagError",
    "CommsTargetThread2BusError",
    "CommsTargetThread2JtagError",
    "CommsTargetThread3BusError",
    "CommsTargetThread3JtagError",
    "CommsTimeoutError",
    "CommsUnsupportedError",
    "CommsUserAbortError",
    "LicensePlatformError",
    "LoadProgramFileNonFatalError",
    # [[[end]]]
)

import os
import sys
import re
from .breakpoint import Breakpoint, BreakpointEnums, BreakpointList
from .probe import Probe, GetDAScript, GetConnectedProbes
from .soc import SoC
from .core import Core
from .callstack import Frame
from .channel import Channel
from .da_exception import *
from .da_symbol import Symbol
from .da_thread import Thread
from .da_types import *
from .disassembly import *
from .dtm import DTMRequest
from .fileserver import FileServer
from .memory import Memory, Accessibility, ValidRange
from .overlays import *
from .probe_finder import FoundProbe
from .source import SourceFile, SourceLine
from . import da_config
from . import probe_identifier

def _init_script_events():
    try:
        import codescape.da as scripting_da
    except ImportError:
        pass
    else:
        module = sys.modules[__name__]
        for name in dir(scripting_da):
            if name.startswith("EVT_"):
                setattr(module, name, getattr(scripting_da, name))

_init_script_events()
del _init_script_events

version='8.6.5.1513346799'
"""Current version of imgtec.codescape."""

environment = "standalone"
'''This attribute can be used to determine if the script is running inside Codescape.
If this is the case, it has value ``codescape``, otherwise it has the value
``standalone``.'''

is_script_region = False
'''This attribute will be True if the script is running inside a script region in
Codescape, or False if the script is a non-region script (e.g. run scripts or
load scripts) or if the script is not running in Codescape.'''

try:
    from codescape import _is_region_script
    is_region_script = _is_region_script
except ImportError:
    pass

try:
    from codescape import BindEvent, UnbindEvent
except ImportError:
    def BindEvent(*args, **kwargs):
        raise Error("BindEvent() is only available when running in Codescape")
    def UnBindEvent(*args, **kwargs):
        raise Error("UnbindEvent() is only available when running in Codescape")

try:
    from codescape import ScriptCall, MultiCall, MultiCallWithReturnValues
except ImportError:
    class ScriptCall(object):
        def __init__(self, func, *args, **kwargs):
            self.func = func
            self.args = args
            self.kwargs = kwargs
    def MultiCall(calls):
        for call in calls:
            call.func(*call.args, **call.kwargs)
    def MultiCallWithReturnValues(calls):
        results = []
        for call in calls:
            results.append(call.func(*call.args, **call.kwargs))
        return results

class BatchCall(object):
    """
    Helper class to perform a batch sequence of script function or method calls
    when running in Codescape. This is used to reduce the IPC overhead when
    calling a lot of script functions or methods at once where the overhead
    takes up most of the execution time. The calls are buffered and sent to
    Codescape at the end of the with statement as a single call.

    Example::

        item_list = ['spam', 'eggs', 'bacon', 'sausage', 'spam']

        with BatchCall() as batch:
            for index, item in enumerate(item_list):
                batch(self.listbox.Append, item, index)

        with BatchCall(return_values=True) as batch:
            for index in range(self.listbox.GetCount()):
                batch(self.listbox.GetClientData, index)
        client_data_list = batch.return_values

    """

    def __init__(self, return_values=False):
        self._return_values = return_values
        self._calls = []

    def __call__(self, func, *args, **kwargs):
        self._calls.append(ScriptCall(func, *args, **kwargs))

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if type is None:
            if self._calls:
                if self._return_values:
                    self._results = MultiCallWithReturnValues(self._calls)
                else:
                    MultiCall(self._calls)
            return True
        else:
            return False

    @property
    def return_values(self):
        if not self._return_values:
            raise TypeError("You need to pass return_values=True to collect return values")
        try:
            return self._results
        except AttributeError:
            raise TypeError("The BatchCall has not been made yet, you need to exit the with block")

def GetThreadById(tid, dascript=None):
    """
    Returns the Thread object associated with the legacy CSUtils.DA thread ID.
    Raises :class:`~imgtec.codescape.TargetNotFound` if target is not found.

    .. sourcecode:: python

        from imgtec import codescape
        from CSUtils import DA
        thread = codescape.GetThreadById(DA.GetCurrentTarget())
    """
    dascript = GetDAScript(dascript)

    for probe in GetConnectedProbes(dascript):
        for hwthread in probe.hwthreads:
            if hwthread.id == tid:
                return hwthread
            for swthread in hwthread.swthreads:
                if swthread.id == tid:
                    return swthread
    raise TargetNotFound("Thread not found: %r" % tid)

def GetRegionThread(dascript=None):
    """
    Return the thread associated with the current region. This function is only
    available when running in a Codescape script region.

    .. sourcecode:: python

        from imgtec import codescape
        thread = codescape.GetRegionThread()
    """
    dascript = GetDAScript(dascript)

    try:
        tid = dascript.GetRegionTarget()
    except AttributeError:
        raise Error("GetRegionThread() is only available when running in Codescape")

    return GetThreadById(tid, dascript)

def GetScriptThread(dascript=None):
    """
    Return the thread associated with the current script context.

    * For region scripts, this is the same as GetRegionThread().
    * For run scripts, this is the selected target when the script was run.
    * For load scripts, this is the thread to load on.
    * For breakpoint scripts, this is the thread which triggered the breakpoint.
    """
    return GetRegionThread(dascript)

def GetSelectedThread(dascript=None):
    """
    Return the thread currently selected in Codescape.

    .. sourcecode:: python

        from imgtec import codescape
        thread = codescape.GetSelectedThread()
    """
    dascript = GetDAScript(dascript)

    try:
        tid = dascript.GetSelectedThread()
    except AttributeError:
        try:
            return GetRegionThread(dascript)
        except Exception:
            raise Error("GetSelectedThread() is only available when running in Codescape")

    return GetThreadById(tid, dascript)

def GetBreakpointThread(dascript=None):
    """
    When the script has been run as a breakpoint trigger action, this returns
    the thread which triggered the breakpoint.

    .. sourcecode:: python

        from imgtec import codescape
        thread = codescape.GetBreakpointThread()
    """
    dascript = GetDAScript(dascript)

    try:
        tid = dascript.GetBreakpointThread()
    except AttributeError:
        try:
            return GetRegionThread(dascript)
        except Exception:
            raise Error("GetBreakpointThread() is only available when running in Codescape")

    return GetThreadById(tid, dascript)

def GetFirstProbe(dascript=None):
    """
    Returns the first Probe in the connected list.
    
    If running within Codescape this will be the first probe in Codescape's 
    target tree.
    
    If running standalone this function will return the first probe that was 
    connected to using :func:`~imgtec.codescape.ConnectProbe` .

    Raises :class:`~imgtec.codescape.TargetNotFound` if target is not found.

    .. sourcecode:: python

        import sys
        from imgtec import codescape
        if codescape.environment == 'standalone':
            da = codescape.ConnectProbe(sys.argv[1])
        else
            # Get the first da in codescape, though no
            da = codescape.GetFirstProbe()
    """
    dascript = GetDAScript(dascript)

    probes = GetConnectedProbes(dascript)
    if probes:
        return probes[0]

    raise TargetNotFound("No Probes available")

def GetFirstThread(dascript=None):
    """
    Returns the first hardware thread on the first probe in the connected list.
    
    Equivalent to :func:`~imgtec.codescape.GetFirstProbe()` ``.hwthreads[0]`` .  

    Raises :class:`~imgtec.codescape.TargetNotFound` if target is not found.

    .. sourcecode:: python

        from imgtec import codescape
        thread = codescape.GetFirstThread()
    """
    dascript = GetDAScript(dascript)

    for probe in GetConnectedProbes(dascript):
        if probe.hwthreads:
            return probe.hwthreads[0]

    raise TargetNotFound("No hardware threads available")

def FindThreads(deprecated=None, probe=None, soc=None, core=None, hwthread=None, probes=None, da=None, dascript=None):
    """
    Find hardware threads matching all of the given filters.
    
    Each filter may be one of the following :
    
      ================ ======================================================
      Type             Match ...
      ================ ======================================================
      None             all (the default).
      a str            case insensitively at the start of the object name.
      a re.RegexObject the given regex using regex.match(object name).
      an int           the Nth child in it's parent object (zero-indexed).
      ================ ======================================================
      
    Filters should be specified using keyword arguments, the following filters 
    are available :

      =========== ======================================================
      Filter Name Match ...
      =========== ======================================================
      probe       Probe identifier, e.g. 'DA-net 1234'.
      soc         SoC name or index.
      core        Core name or index.
      hwthread    The hwthread name (e.g. Thread0 or Vpe0) or index.
      =========== ======================================================

    By default the core index is the index within it's SoC, but if soc==-1 then
    it is the index within the whole probe.
    
    `da` is a synonym for `probe`, if both are used `da` is ignored.

    `deprecated` should not be used, it exists for backwards compatibility 
    with an older API.
    
    """
    if probes is None:
        dascript = GetDAScript(dascript)
        probes = GetConnectedProbes(dascript)
    probe = probe if probe is not None else da
    _deprecated = _make_matcher(deprecated)
    found = []
    for d in _filter(probes, probe):
        if soc == -1 or deprecated is not None:
            for c in _filter(d.cores, core):
                ctn = 0
                for hw in _filter(c.hwthreads, hwthread):
                    name = c.name + ' ' + hw.name
                    if _deprecated(ctn, name):
                        found.append(hw)
                    ctn += 1
        else:
            for s in _filter(d.socs, soc):
                for c in _filter(s.cores, core):
                    for hw in _filter(c.hwthreads, hwthread):
                        found.append(hw)
    return found
    

def FindThread(deprecated=None, da=None, probe=None, soc=None, core=None, hwthread=None, probes=None, dascript=None):
    """
    Find a single hardware thread matching all of the given filters.
    
    raises ValueError if the number of matching hardware threads is not exactly 1.
    """
    found = FindThreads(deprecated, da=da, probe=probe, soc=soc, core=core, hwthread=hwthread, probes=probes, dascript=dascript)
    if len(found) == 1:
        return found[0]
    if not found:
        msg = "No threads found to match the filter %s :\n%s"
        found = FindThreads(probes=probes, dascript=dascript)
    else:
        msg = "Multiple matches found for the filter %s :\n%s"
    probe = probe if probe is not None else da
    filter = []
    if deprecated is not None:
        filter.append('deprecated=' + _display_filter(deprecated))
    if probe is not None:
        filter.append('probe='         + _display_filter(probe))
    if core is not None:
        filter.append('core='       + _display_filter(core))
    if soc is not None:
        if soc == -1:
            filter.append('soc=<ignore-and-flatten-core-list>')
        else:
            filter.append('soc='       + _display_filter(soc))
    if hwthread is not None:
        filter.append('hwthread='   + _display_filter(hwthread))
    found = '\n'.join('  %s - %s %s' % (x.core.probe.name, x.core.name, x.name) for x in found)
    raise ValueError(msg % (', '.join(filter), found))

def _make_matcher(matcher):
    if matcher is None:
        return lambda idx, name : True
    elif isinstance(matcher, (int, long)):
        return lambda idx, name: idx == matcher
    elif isinstance(matcher, (str, unicode)):
        matcher = matcher.lower()
        return lambda idx, name: name.lower().startswith(matcher)
    elif hasattr(matcher, 'match'):
        return lambda idx, name: matcher.match(name)
    raise TypeError("Unknown filter type %r" % (matcher,))
    
def _filter(things, matcher):
    m = _make_matcher(matcher)
    return [x for n, x in enumerate(things) if m(n, x.name)]

def _display_filter(filter):
    try:
        flags = 'i' if filter.flags & re.I else ''
        return '/%s/%s' % (filter.pattern, flags)
    except AttributeError:
        return repr(filter)

def FindConnectedProbe(identifier, dascript=None):
    """
    Find a Probe that has already been connected to by ConnectProbe.
    """
    dascript = GetDAScript(dascript)

    identifier = probe_identifier.normalise(identifier)
    for probe in GetConnectedProbes(dascript):
        if probe.name == identifier:
            return probe
            
_exe_dir = None
def _find_exe_dir(root=os.path.abspath(__file__), _exists=os.path.exists):
    # This is harder than it looks because there are three possible situations:
    #  1. frozen as in Codescape-Debugger/Console
    #  2. not-frozen as in Codescape-Python
    #  3. not-frozen as in installed via pip
    # The number of dirnames varies between 1 and 7 on different platforms, so
    # we do it dynamically looking for a landmark
    global _exe_dir
    if _exe_dir is None:
        landmark = 'CSDQer.jar' # use dqer because it doesn't change name
        d = root
        while d != os.path.dirname(d) and not _exe_dir: 
            if _exists(os.path.join(d, landmark)):
                _exe_dir = d
            d = os.path.dirname(d)
        if not _exe_dir:
            # This is a fail, but it's a best guess, and we can't raise an 
            # exception because this is called when connecting to a probe that
            # doesn't require virtual probe or DQer.
            _exe_dir = os.path.dirname(root)
    return _exe_dir

_get_default_dqer_directory = _get_default_probe_directory = _find_exe_dir
    
def _get_virtual_probe_location(root=None):
    if root is None:
        root = _get_default_probe_directory()
    exe = 'virtual_probe' + ('.exe' if sys.platform == 'win32' else '')
    return os.path.join(root, exe)            
            
def _set_virtual_probe_location(options, root=None):
    if 'virtual-probe-location' not in options:
        options = dict(options)
        options['virtual-probe-location'] = _get_virtual_probe_location(root)
    return options
    
def ConnectProbe(identifier, options={}, logger=None, dascript=None):
    """Connect to a specified Probe and adds it to the list of connected Probes. 
    
    The identifier can take one of the following forms:

        ================ ====================================
        DA Type          Identifier Format
        ================ ====================================
        DA-net           "DA-net 1"
        Local Simulator  "Simulator HTP221"
        Remote Simulator "RemoteSimulator hostname:port"
        Remote Imperas   "RemoteImperas hostname:port"
        GDB Server       "GDBServer hostname:port"
        ================ ====================================
    
    A :class:`~imgtec.codescape.probe.Probe` instance is returned if successful,
    or :class:`~imgtec.codescape.Error` is raised if the connection to the 
    probe fails.
    
    `options` can be either a dictionary (or a list of ``key, value`` pairs),
    used to set options for the connection.

    The possible keys of this parameter depends on the communications type, some 
    common options include :

    ==================== ==========================================================
    Name                 Meaning
    ==================== ==========================================================
    force-disconnect     If not False connect to the DA even if it is already in
                         use by another user. Please use responsibly.
    search-location      Specify an ip address to find the DA, if dns lookup fails.
    ==================== ==========================================================

    If the specified probe is already in the connected list an exception is raised.
    
    .. sourcecode:: python

        from imgtec import codescape
        da = codescape.ConnectProbe('DA-net 89')
        
        # spawn a HTP221 simulator and connect to it,
        sim = codescape.ConnectProbe("Simulator HTP221")        

    """

    dascript = GetDAScript(dascript)

    da = FindConnectedProbe(identifier, dascript)
    if not da:
        options = _set_virtual_probe_location(options)
        dascript.AddTarget(identifier, options, logger)
        dascript.InvalidateSelectedTarget()

    da = FindConnectedProbe(identifier, dascript)
    if not da:
        raise TargetNotFound("Failed to connect to %s" % identifier)

    return da

def GetDAConfigList():
    """
    Return the list of DA identifiers for each of the DAs which are ticked in 
    DAConfig.
    
    This can be used to manually connect to each DA, detecting errors raised
    from :func:`~imgtec.codescape.ConnectProbe`.
    
    .. sourcecode :: python

        import sys
        das = []
        from imgtec import codescape
        for serial in codescape.GetDAConfigList():
            try:
                das.append(codescape.ConnectProbe(serial))
            except DA.Error as e:
                sys.exit("Failed to connect to %s : %s" % (serial, e))
        for da in das:
            print da.name
        
    """
    return [da.serial for da in da_config.DAConfigList() if da.scan_for_it]

def GetConfiguredProbes(dascript=None):
    """
    Connects to each probe configured in DAConfig, adds it to the connected list
    and returns list of Probe objects.
    
    No exceptions are raised in the case of failure to connect to a DA.
    See :func:`~imgtec.codescape.GetDAConfigList` for an example of how to 
    detect errors.

    .. sourcecode:: python

        from imgtec import codescape
        for da in codescape.GetConfiguredProbes():
            print da.name
    """

    dascript = GetDAScript(dascript)

    probes = []
    for da_name in GetDAConfigList():
        try:
            probes.append(ConnectProbe(da_name, dascript=dascript))
        except Exception, e:
            print e

    return probes

def GetScanTargetLog(dascript=None):
    """Retrieve the log of the last attempt to connect to a target."""
    dascript = GetDAScript(dascript)
    return dascript.GetScanTargetLog()

def GetCommsDiagnosticLog(dascript=None):
    """
    Retrieve the log of the low level comms.
    
    This circular buffer log is useful for Codescape support engineers 
    to diagnose various problems.
    """
    dascript = GetDAScript(dascript)
    return dascript.GetCommsDiagnosticLog()

def ForceAssertionFailure(assert_behaviour, dascript=None):
    """
    Configures the way that target assertion failures should be handled.

    .. param:: assert_behaviour

        * If non-zero, target assertions will be converted into exceptions on the next DA-script
        command, and the target will continue to run.

        * If zero, target assertions will result in a dialog box appearing, which will wait for
        user interaction.  This is the default behaviour, but it is often unsuitable
        for automated scripts and tests.

        * If AssertBehaviour is an object with an "on_assert" member function, this member function
        will be called when a target assertion fails.  The member function should have the following
        signature ::

        on_assert(self, TargetIdentifier, Address, Message, File, LineNumber)

        If the member returns non-zero the target is halted, otherwise the target will continue to run.
    """
    dascript = GetDAScript(dascript)
    dascript.ForceAssertionFailure(assert_behaviour)

# Aliases for old names
GetDebugAdapters = GetConnectedProbes
GetFirstDA = GetFirstProbe
FindConnectedDA = FindConnectedProbe
ConnectDA = ConnectProbe
GetConfiguredDAs = GetConfiguredProbes

def _codescape_debugger_search_locations():
    csver = 'Codescape-' + '.'.join(version.split('.')[:2])
    EXEC = os.path.realpath(sys.executable)
    if os.path.basename(EXEC).startswith('Codescape-'):
        # e.g. Codescape-(Python|Pythonw|Console|Debugger|Help-Viewer)
        yield os.path.dirname(EXEC)
    if sys.platform == 'win32':
        try:
            import _winreg as winreg
            k = winreg.HKEY_CURRENT_USER
            for p in 'Software/Imagination Technologies/imgtec/Current'.split('/'):
                k = winreg.OpenKey(k, p)
            path = winreg.QueryValueEx(k, 'location')[0]
            path = os.path.join(path, csver)
            if os.path.isdir(path):
                yield path
        except Exception:
            pass
        pfiles = os.environ.get('ProgramFiles', '')
        yield os.path.join(pfiles, 'Imagination Technologies', csver)
    elif sys.platform.startswith('linux'):
        yield os.path.join(os.path.expanduser('~/.local/opt/imgtec'), csver)
        yield os.path.join('/opt/imgtec', csver)
        
def GetCodescapeDebuggerPath(entry_looking_for = ''):
    '''Return path of codespace debugger installation.
    
    `entry_looking_for` is a file or a directory to look for, it is empty by default 
    Function returns None if nothing found.
    '''
    seen = set()
    for path in _codescape_debugger_search_locations():
        if path in seen:
            continue
        seen.add(path)
        dir_path = os.path.join(path, entry_looking_for)
        if os.path.exists(dir_path):
            return dir_path
            
def GetCommsOptions(identifier_or_comms_type, *args):
    """Get the available and default values of comms options.
    
    The returned dictionary can be used to get the default comms options for 
    probes or installed Simulators. 
    
    This can then be used to modify the settings used at connection time with 
    :func:`ConnectProbe`.  As the following example demonstrates.

    .. sourcecode :: python

        from imgtec.codescape import GetCommsOptions, ConnectProbe

        def connect_to_sim_with_argv(identifier, *argv):
            default_options = GetCommsOptions(identifier)
            args = "".join((' "%s"' if ' ' in arg else " %s") % (arg,) for arg in argv)
            opts = dict(sim=default_options['sim'] + args)
            return ConnectProbe(identifier, opts)

        probe = connect_to_sim_with_argv("Simulator SimName", "--verbose")

    `identifier_or_comms_type` is either a full probe or simulator identifier,
    or just the comms type prefix, e.g. 'SysProbe'. For most comms types passing 
    an identifier or a comms type produces the same result. But for Local 
    Simulators this will return the options retrieved from the .ini file for the 
    specific Simulator.

    ================ ================= ================================
    DA Type          Comms Type        Identifier Format
    ================ ================= ================================
    SysProbe	     "SysProbe"        "SysProbe 1"
    DA-net           "DA-net"          "DA-net 1"
    Local Simulator  "Simulator"       "Simulator HTP221"
    Remote Simulator "RemoteSimulator" "RemoteSimulator hostname:port"
    Remote Imperas   "RemoteImperas"   "RemoteImperas hostname:port"
    ================ ================= ================================

    """
    from imgtec.codescape import GetDAScript
    da = GetDAScript(None)
    return da.GetCommsOptions(identifier_or_comms_type, *args)

def DiscoverProbes(comms_type=''):
    """Returns a list of nearby probes.

    The return is a list of :class:`~imgtec.codescape.FoundProbe`\s,
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
    dascript = GetDAScript(None)
    return [FoundProbe(*x) for x in dascript.DiscoverProbes(comms_type, options)]


def GetProbeHSP(probe_identifier):
    """Return the HSP path for `probe_identifier` or None if no HSP is configured."""
    dascript = GetDAScript(None)
    active, hsps = dascript.GetHSPSettings(probe_identifier)
    if active and hsps:
        return hsps[0]

def SetProbeHSP(identifier, hsp_path):
    """Set the HSP path for `probe_identifier`.
    
    Set the HSP path to None or an empty string to deactivate the current HSP.
    """
    dascript = GetDAScript(None)
    if hsp_path:
        active, hsps = True, [hsp_path]
    else:
        active, hsps = False, []
    dascript.SetHSPSettings(probe_identifier, active, hsps)

# make all classes and functions appear to be implemented directly in imgtec.codescape
# this is just to keep sphinx happy
exported = set()
for name, thing in globals().items():
    if not name.startswith('_') and getattr(thing, '__module__', '').startswith('imgtec.codescape'):
        thing.__module__ = 'imgtec.codescape'
        exported.add(name)
del thing
if 0:
    print ' --exported things---'
    print sorted(exported)
    print

    print ' --in all but not exported--- '
    print sorted(set(__all__) - exported)
    print
    print ' --in exported but not all--- '
    print sorted(exported - set(__all__))
    print
del exported
