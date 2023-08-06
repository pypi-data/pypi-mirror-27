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

from imgtec.console.support import *
from imgtec.console import support
from imgtec.console import termcolour 
from imgtec.console.program_file import get_symbols_string, get_source_string
from imgtec.console.regdb import scanregisters
from imgtec.console import breakpoints
from imgtec.console import memory
from imgtec.console.results import *
from imgtec.console import tdd
from imgtec.console.regs import *
from imgtec.console import reginfo
from imgtec.codescape import da_exception
from imgtec.codescape.da_types import Status
from imgtec.codescape.probe_identifier import Identifier
import atexit
import re
import time
import logging as _logging
import os

nodasm = named('nodasm')
dasms  = [(memory.dasm, True), (nodasm, False)]

try:
    _nullHandler = _logging.NullHandler
except AttributeError:
    class _nullHandler(_logging.Handler):
        def handle(self, record):
            pass

        def emit(self, record):
            pass

        def createLock(self):
            self.lock = None
            
comms_logger = _logging.getLogger('comms')
comms_logger.addHandler(_nullHandler())
comms_logger.setLevel(_logging.INFO)

_global_logging = dict(comms=False, probe=False, jtag=False, console=0, simulator=0)

def _add_root_handler():
    stream_handler = _logging.StreamHandler()
    stream_handler.setLevel(_logging.DEBUG)
    stream_handler.setFormatter(_logging.Formatter('%(levelname)-7s [%(name)s] %(message)s'))
    root = _logging.getLogger('')
    root.addHandler(stream_handler)

_probe_attributes = [
    ('firmware_version', 'GetFirmwareVersion', ''),
    ('location', 'GetLocation', ''),
    ('_clock', 'GetJTAGClock', 0),
]

class Probe(Device):
    """Represents a connected probe.
    
    This is the return type of the :func:`~imgtec.console.probe()` command.

    """
    def __init__(self, tiny, exitfn=None, environment='standalone'):
        self.da = tiny
        
        self.tiny = tiny
        """The ``imgtec.codescape.tiny.Tiny`` instance for the probe."""

        self.identifier = tiny.GetIdentifier()
        """The probe identifier, e.g. 'DA-net 1234'"""
        
        self.firmware_version = ''
        """The version of the probe firmware, e.g. '5.4.3.0'."""
        
        self.location = ''
        """The location of the probe, this is typically the IP address of the probe."""
        
        # Some optional info about the probe, done like this to reduce requirements on tiny ducks
        for attr, fn, default in _probe_attributes:
            try:
                getter = getattr(tiny, fn, lambda default=default: default)
            except AttributeError:
                pass
            try:
                setattr(self, attr, getter())
            except Exception as e:
                print 'Warning, got exception %s evaluating %s()' % (e, fn)
                setattr(self, attr, default)

        self.device = None
        
        self.all_socs = []
        r'''All :class:`~imgtec.console.SoC`\s reported by the probe.

        This includes SoCs that have no debuggable cores (e.g. the CM).
        '''
        
        self.socs = []
        r"""List of :class:`~imgtec.console.SoC`\s reported by the probe."""
        
        self.environment = environment
        """Either 'standalone' if the script is run independently from Codescape 
        (this includes Connect scripts) or 'codescape' if run from within 
        Codescape with an active connection. See :ref:`integrating` for more 
        information."""

        self.ir_lengths = []
        """List of instruction register lengths. 
        
        This list is empty until :func:`~imgtec.console.scanonly`, 
        :func:`~imgtec.console.jtagchain`, or :func:`~imgtec.console.tap`
        has been called.
        """
        
        self.tap_types = []
        """List of tap types, filled in when tapinfo is called. Will either be None
        or JTAG_TYPE_MDH"""
        
        self._tap_index = -1
        self._mdh_device = None
        self._logging = _global_logging.copy()
        self._logfilenames = {}
        self._log_cache = dict(probe='', jtag='')
        self._table = None
        self._mode = None
        self.name = self.identifier
        self._exitfn = exitfn        
        self.probe_info = tiny.ProbeInfo()
        self.streaming_thread = None
        self.tap_ir_warned = False

    @property
    def probe(self):
        """All devices have a probe attribute, in this case this is a reference to self."""
        return self        
                        
    @property
    def mode(self):
        '''The current mode of the probe.'''
        return self._mode

    @property
    def all_cores(self):
        r'''All :class:`~imgtec.console.Core`\s reported by the probe, from all SoCs.

        This includes cores that are not debuggable (e.g. the CM).
        '''
        return list(itertools.chain.from_iterable(soc.all_cores for soc in self.all_socs))
        
    @property
    def cores(self):
        r"""List of :class:`~imgtec.console.Core`\s reported by the probe, from all SoCs."""
        return list(itertools.chain.from_iterable(soc.cores for soc in self.socs))
                        
    @property
    def tap_index(self):
        """The currently selected tap used by :func:`~imgtec.console.devtap`, this is -1
        if no tap has been configured."""
        return self._tap_index
    
    @tap_index.setter
    def tap_index(self, index):
        self._tap_index = index
        self._update_name()

    @property
    def mdh_device(self):
        return self._mdh_device

    @mdh_device.setter
    def mdh_device(self, dev):
        self._mdh_device = dev
        self._update_name()
            
    def _update_name(self, verbose=False):
        oldmode = self._mode
        self._mode = self.tiny.GetDAMode() if self.tiny else 'disconnected'
        
        #If we get called from scan_devices this will never be true
        if oldmode != self._mode:
            self.scan_devices(verbose=verbose)
            
        if self._mode in ('autodetected', 'table'):
            self.name = self._mode
            if not self.cores:
                try:
                    state = str(runstate(self).status)
                except Exception:
                    report_exception()
                    state = 'target_offline'
                self.name += '-' + state
        elif self._mode == 'scanonly' and self.ir_lengths:
            ti = 0 if self.tap_index == -1 else self.tap_index
            self.name = 'tap %d of %d' %  (ti, len(self.ir_lengths))

            if self._mdh_device:
                self.name += ' mdh c{}v{}'.format(*self._mdh_device)
        else:
            self.name = self._mode
        update_prompt()
        
    def _update_table(self):
        self._table = None
        table_data = self.tiny.ReadDAConfigurationData(False)
        if table_data:
            try:
                self._table = tdd.board_from_values(table_data)
            except Exception as e:
                report_exception("Failed to parse table : %s" % (e,))
                    
    def _disconnect(self, *exc_info):
        if self.tiny: self.tiny.Disconnect()
        if self._exitfn:
            self._exitfn(*exc_info)
        for soc in self.all_socs:
            _remove_from_global_namespace(soc)
            for core in soc.cores:
                _remove_from_global_namespace(core)
                for vpe in core.vpes:
                    _remove_from_global_namespace(vpe)
        self.socs = []
        self.all_socs = []
        self.tiny = self.da = None
        self.device = self
        
    def __enter__(self):
        return self
        
    def __exit__(self, *exc_info):
        self._disconnect(*exc_info)
        if Command and Command.get_probe() == self:
            Command.set_device(None)
        update_prompt()

    def _add_socs(self, tiny, name_prefix=''):
        """Add all of the cores found on the tiny interface `tiny`."""
        had_socs_before = bool(self.socs)
        new_socs = [SoC(self, tiny, n, name_prefix=name_prefix) for n in range(tiny.SoCCount())]
        self.all_socs.extend(new_socs)
        self.socs.extend([soc for soc in new_socs if soc.cores])
        
        if self.socs and not had_socs_before:
            device(self.socs[0].cores[0].vpes[0])
            
        #This is used to copy previously made DBs to cores with the same properties.
        #(name, is_64_bit) -> RegDB
        cached_dbs = {}
        
        for soc in self.socs:
            for core in soc.cores:
                cpu_info = dict(core.tiny.CpuInfo())
                key = (cpu_info.get('cpu_name', 'default'), not cpu_info.get('cpu_is_32bit', True))
                
                cached_db = cached_dbs.get(key, None)
                if cached_db is not None:
                    core.regdb = cached_db
                else:
                    #Make a new DB
                    if not core.regdb:
                        try:
                            scanregisters(read_registers=False, device=core)
                        except Exception as e:
                            report_exception("Failed to determine possible register set for %r : %s" % (core, e))
                        else:
                            #Only add if the parse was OK
                            cached_dbs[key] = core.regdb
                        
        update_prompt()
            
    def scan_devices(self, verbose=False):
        """Rebuild the codescape console device hierarchy."""
        self._table, self.socs, self.all_socs = None, [], []
        device(self)
        
        self._mode = self.tiny.GetDAMode()
        
        if self._mode in ('autodetected', 'table'):
            self._update_table()
            self._add_socs(self.tiny)
        elif self._mode == 'scanonly':
            from imgtec.console.scan import jtagchain
            jtagchain(device=self, verbose=verbose)
        self._update_name(verbose=verbose)
        
    def __repr__(self):
        rows = [('Identifier', self.identifier),
                ('Firmware', self.firmware_version),
                ("Location", self.location),
                ("Mode", self._mode),
                ]
        if self._mode != 'failsafe':
            rows += [
                ("TCK Rate", "%dkHz" % (int(self._clock), )),
                ]
        longest = max(len(x) for x, y in rows)
        return "\n".join(x.ljust(longest) + ' ' + (y or '') for x, y in rows)
        
    def on_each_command(self):
        for logname, enabled in self._logging.items():
            if enabled:
                self._collect_log(logname)
                
    def _collect_log(self, logname, display=True):
        filename = self._logfilenames.get(logname, '')
        if filename:
            log = self.tiny.GetDiagnosticFile(filename)
            self._log_cache[logname], log = _update_log(self._log_cache[logname], log)
            if log and display:
                sys.stdout.write(replace_exec_dasm(log, self.device))
                
    @property
    def targetdata(self):
        '''Return the :class:`~imgtec.console.tdd.Board` target data for the target
        connected to this probe.'''
        return self._table
                
                
def _update_log(oldlog, log):
    """Determine what, if any, new data has arrived in the log, and
    return a pair of (oldlog, newdata).
    """
    if oldlog:
        try:
            log = log[log.rindex(oldlog) + len(oldlog):]
        except ValueError:
            pass
    if log:
        oldlog += log
        oldlog = '\n'.join(oldlog.split('\n')[-4:])
    return oldlog, log
                
def connect(identifier, options):
    found = default_connector
    for regex, connector in connectors:
        if regex.match(identifier):
            found = connector
    return found(identifier, options)

def default_connector(identifier, options):
    from imgtec.codescape import tiny
    try:
        return tiny.ConnectProbe(identifier, options, comms_logger)
    except RuntimeError as e:
        if 'In use by' in str(e):
            raise RuntimeError(('%s\n\n' +
                'You can forcibly disconnect the other user using:\n\n' +
                '   >>> probe("%s", force_disconnect=True)\n\n' +
                'Or you can use --force-disconnect on the command line.\n\n' +
                'Please use with consideration for the other user.') % (e, identifier))
        raise

def _add_to_global_namespace(obj):
    ns = Command.get_namespace()
    ns[obj.name] = obj
    try:
        ns[obj.flat_name] = obj
    except AttributeError:
        pass
        
def _remove_from_global_namespace(obj):
    ns = Command.get_namespace()
    try:
        del ns[obj.name]
    except (KeyError, AttributeError):
        pass
    try:
        del ns[obj.flat_name]
    except (KeyError, AttributeError):
        pass

class SoC(Device):
    """Represents an SoC of a connected probe.

    """
    def __init__(self, probe, tiny, soc_index, name_prefix=''):
        tiny = self.tiny = tiny.SoC(soc_index)

        self.tiny = tiny
        """The ``imgtec.codescape.tiny.Tiny`` instance for this SoC."""

        self.probe = probe
        """The :class:`~imgtec.console.Probe` that this core belongs to."""
        
        self.index = soc_index
        """The index of this SoC in the probe, for example SoC0 has an index of 0."""

        self.all_cores = [Core(self, tiny, n, name_prefix=name_prefix) for n in range(tiny.CoreCount())]
        r'''All :class:`~imgtec.console.Core`\s reported by the probe.

        This includes cores that are not debuggable (e.g. the CM).
        '''
        
        self.cores = [core for core in self.all_cores if core.vpes]
        r"""List of :class:`~imgtec.console.Core`\s on this probe."""

        self._name_prefix = name_prefix
        _add_to_global_namespace(self)

    @property
    def name(self):
        '''Name of this thread, this is of the form s0c0.'''
        return  "%ssoc%d" % (self._name_prefix, self.index)
    
    @property
    def targetdata(self):
        '''Return the :class:`~imgtec.console.tdd.SoC` target data for this SoC.'''
        return self.probe._table.socs[self.index]

    def __repr__(self):
        return '%s' % (self.name,)


class Core(Device):
    """Represents a core of a connected probe.
    
    """
    def __init__(self, soc, tiny, core_index, name_prefix=''):
        tiny = self.da = tiny.Core(core_index)
        
        self.tiny = tiny
        """The ``imgtec.codescape.tiny.Tiny`` instance for this core."""

        self.soc = soc
        """The :class:`~imgtec.console.SoC` that this core belongs to."""
        
        self.index = core_index
        """The index of this core in it's SoC, for example Core0 has an index of 0."""
        
        self.vpes = [Vpe(self, tiny, n, name_prefix=name_prefix) for n in range(tiny.VpeCount())]
        r"""A list of :class:`~imgtec.console.Vpe`\s on this core."""

        self._name_prefix = name_prefix
        _add_to_global_namespace(self)
            
        self.regdb = None
        """The register database for this core, shared by its VPEs."""
        
        self.user_regdb = {}
        """User register database for this core, shared by its VPEs."""
        
        self.trace_mode = None
        
        try:
            self._family = CoreFamily(self.tiny.GetTargetFamily())
        except Exception as e:
            self._family = CoreFamily.unknown
            print 'Failed to get family of core:', e
        
    @property
    def family(self):
        return self._family

    @property
    def tracemode(self):
        """This core's current tracemode (or None if not yet read)."""
        return self.trace_mode

    @property
    def probe(self):
        """The :class:`~imgtec.console.Probe` that this core belongs to."""
        return self.soc.probe
        
    @property
    def name(self):
        '''Name of this core, this is of the form s0c0.'''
        return "%ss%dc%d" % (self._name_prefix, self.soc.index, self.index)
        
    @property 
    def flat_name(self):
        return "%score%d" % (self._name_prefix, self.tiny.GetFlatCore())

    @property
    def threads(self):
        r"""A list of :class:`~imgtec.console.Vpe`\s on this core."""
        return self.vpes
    
    @property
    def targetdata(self):
        '''Return the :class:`~imgtec.console.tdd.Core` target data for this Core.'''
        return self.soc.targetdata.cores[self.index]
        
    def __repr__(self):
        return '%s - %s' % (self.name, self.family)
        
        
_regdb_callbacks = []    

def scanregisters_callback(callback):
    '''Appends a callback function that will be executed after `scanregisters`.
    
    :func:`~imgtec.console.scanregisters` is called by Codescape Console whenever
    a new core is created, for example during initial connection to a probe or 
    when :func:`~imgtec.console.autodetect` or :func:`~imgtec.console.targetdata`
    is called.
    
    This is done in order to initialise the 'RegDB' object that is used to 
    provide rich register type information about the fields and value in fields
    of registers.  If the 'RegDB' is incomplete or incorrect the 
    :meth:`~imgtec.console.Vpe.register_type` method can be used to override the
    built-in 'RegDB'.  This callback provides a location to hook changes that 
    need to be performed whenever a core is constructed.
    
    Normally this callback mechanism would be used in the startup script
    (by default ``$HOME/imgtec/console_scripts/__init__.py``) so that it does 
    not need to be done manually every time Codescape Console starts.
    
    For example::
    
        [s0c0v0] >>> from imgtec.console import scanregisters_callback
        [s0c0v0] >>> from imgtec.console.scan import IdCodeValue, ImpCodeValue
        [s0c0v0] >>> @scanregisters_callback
        [s0c0v0] ... def ejtag_register_types(device):
        [s0c0v0] ...     if targetdata(device).socs[0].tap_type == 6:
        [s0c0v0] ...         print 'Registering types...'
        [s0c0v0] ...         device.register_type('ejtag_idcode', IdCodeValue)
        [s0c0v0] ...         device.register_type('ejtag_impcode', ImpCodeValue)
        [s0c0v0] >>> scanregisters()
        Registering types...
        [s0c0v0] >>> regs('ejtag_idcode')
        <raw>    Version PartNumber ManufID One
        00000001 0       0000       000     1
        [s0c0v0] >>> oldid = probe().identifier
        [s0c0v0] >>> closeprobe()
        >>> probe(oldid)              # doctest: +SKIP
        Registering types...
        [s0c0v0] >>> regs('ejtag_idcode')
        <raw>    Version PartNumber ManufID One
        00000001 0       0000       000     1
    '''
    _regdb_callbacks.append(callback)
    return callback
    


class Vpe(Device):
    def __init__(self, core, tiny, vpe_index, name_prefix=''):
        tiny = self.da = tiny.Vpe(vpe_index)
        
        self.tiny = tiny
        """The ``imgtec.codescape.tiny.Tiny`` instance for this VPE."""
        
        self.core = core
        """The :class:`~imgtec.console.Core` that this VPE belongs to."""

        self.index = vpe_index
        """The index of this VPE, for example VPE0 has an index of 0."""
        
        self._name_prefix = name_prefix
        _add_to_global_namespace(self)
        self.breakpoints = {}
        self.perfcount_settings = {}
        self._abi = None
        
        self._was_running_last_time = False
        self._registers_info = None#TODO this is to get some tests to work
        self.objfile = None
        self.progfile_info = None
        
    @property 
    def abi(self):
        if self._abi is None:
            self._abi = self.tiny.GetABI()
        return self._abi
        
    def set_abi(self, newabi):
        self._abi = None
        self.tiny.SetABI(newabi)
        self._abi = self.tiny.GetABI()
        
    @property
    def family(self):
        return self.core.family

    @property
    def registers_info(self):
        """A list of registers that the underlying comms supports.  
        
        Each entry in the list is an object that has the following properties:
        name, size (in bytes), is_float, aliases.  Note that the actual probe
        and target may not support all registers.
        """        
        if self._registers_info is not None:
            return self._registers_info
        return reginfo.info(self.abi)
        
    @property
    def registers_info_by_name(self):
        """As :attr:`~imgtec.console.Vpe.registers_info` but a dict keyed on lower case name."""
        if self._registers_info is not None:
            from imgtec.console.reginfo import _make_by_name
            return _make_by_name(self._registers_info)
        return reginfo.info_by_name(self.abi)
        
    def _normalise_regname(self, name):
        try:
            return self.registers_info_by_name[name.lower()].name
        except KeyError:
            return name

    def register_type(self, name, type):
        '''Registers a type of register.
        
        Codescape Console returns rich register information for registers by
        replacing the return type of the :func:`~imgtec.console.regs` command
        with types that allow field introspection.  For example the namedbitfield
        type generator in ``imgtec.lib.namedbitfield`` is ideal for this purpose.
        
        Normally most registers that have fields are automatically assigned 
        types using an internal database of registers and their fields known as 
        the 'RegDB'.  However sometimes this information is not correct or 
        incomplete for specific cores and this method provides a mechanism for 
        overriding or augmenting the automatic types.
        
        `name` is the name of the register for which we want to change the 
        return type.
        
        `type` is the new type to use, and typically this will be a type 
        constructed using ``imgtec.lib.namedbitfield``. 
        
        For example, to specify that a register has specific fields ::
        
            [s0c0v0] >>> from imgtec.lib.namedbitfield import *
            [s0c0v0] >>> MyRegister = namedbitfield('MyRegister', 
                     ...            compile_fields('Version    31 28'))
            [s0c0v0] >>> device().register_type('ejtag_idcode', MyRegister)
            [s0c0v0] >>> regs('ejtag_idcode')
            <raw>    Version
            00000001 0
            
        If `type` is None then the overridden type will be removed and the
        automatic registered type (if any) will be used once more ::
        
            [s0c0v0] >>> regs('ejtag_idcode')
            <raw>    Version
            00000001 0      
            [s0c0v0] >>> device().register_type('ejtag_idcode', None)
            [s0c0v0] >>> regs('ejtag_idcode')
            0x00000001
            
        See :func:`~imgtec.console.scanregisters_callback` for a method to 
        automatically register types at Codescape Console probe connection.
        '''        
        if type is None:
            try:
                del self.user_regdb[name]
            except KeyError:
                pass
        else:
            self.user_regdb[name] = type
                
    @property
    def probe(self):
        """The :class:`~imgtec.console.Probe` that this thread belongs to."""
        return self.core.probe
        
    @property
    def name(self):
        '''Name of this thread, this is of the form s0c0v0.'''
        return "%ss%dc%dv%d" % (self._name_prefix, self.core.soc.index, self.core.index, self.index)

    @property
    def flat_name(self):
        return "%sc%dv%d" % (self._name_prefix, self.tiny.GetFlatCore(), self.index)
        
    @property
    def regdb(self):
        return self.core.regdb
        
    @regdb.setter
    def regdb(self, new):
        self.core.regdb = new
        
    @property
    def user_regdb(self):
        return self.core.user_regdb

    @user_regdb.setter
    def user_regdb(self, new):
        self.core.user_regdb = new        

    @property
    def offline(self):
        try:
            info = dict(self.tiny.CpuInfo())
            return not info['is_valid']
        except KeyError:
            pass
        return False

    def __repr__(self):
        family = str(self.core.family)
        description = family
        parentthreads = len(self.core.vpes)
        thread_or_vpe = 'Thread' if family == 'meta' else'VPE'
        if self.offline:
            description = '%s - offline' % family
        else:
            try:
                info = dict(self.tiny.CpuInfo())
                description = info['display_name']
            except Exception, e:
                description = '%s (%s)' % (family, str(e))
        thread = ''
        if parentthreads > 1:
            thread = '-%s%d' % (thread_or_vpe, self.index)
        return '%s - %s%s' % (self.name, description, thread)
        
    def get_names(self):
        names = [self.name]
        if self.probe.tap_index != -1 and self.probe.ir_lengths:
            names.append('tap %d of %d active' %  (self.probe.tap_index, len(self.probe.ir_lengths)))
        if self.probe.mode in ('autodetected', 'table'):
            for format, fn in [('tc%d', 'GetActiveTC'), ('asid%02x', 'GetActiveASID')]:
                fn = getattr(self.tiny, fn)
                if fn:# This is to cope with old tinys that don't have GetActiveTC/ASID yet
                    index = fn()
                    if index != -1:
                        names.append(format % (index,))
        return names

def update_prompt():
    device = Command.get_device()
    if device:
        # don't use blue it's unreadable on windows, and magenta is a bit yucky
        colours = ['bright_green', 'bright_yellow', 'bright_cyan', 'white', 'bright_red']  
        names = device.get_names()
        coloured = [termcolour.colourizer(name, colour) for name, colour in zip(names, colours)]        
        names, coloured = ' '.join(names), ' '.join(coloured)
        support._ps1 = '[%s] >>> ' % (names,)
        support._ps2 = sys.ps2 = ' %s  ... ' % (' ' * len(names),)
        sys.ps1 = '[%s] >>> ' % (coloured,)
    else:
        sys.ps1 = support._ps1 = '>>> '
        support._ps2 = sys.ps2 = '... '

class DeviceList(list):
    def __init__(self, devices, error=''):
        list.__init__(self, devices)
        self._error = error
    def __repr__(self):
        lines = []
        if self._error:
            lines.append(self._error)
        for vpe in self:
            indent = ''
            if len(vpe.core.vpes) > 1:
                if vpe.index == 0:        
                    lines.append(repr(vpe.core))
                indent = '  '
            lines.append(indent + repr(vpe))
        return '\n'.join(lines)
        

class OfflineCoreVpe(object):
    """ fake vpe to wrap an offline core
    """
    def __init__(self, core):
        self.core = core

    def __repr__(self):
        return repr(self.core) + ": offline"
    
    @property
    def family(self):
        return self.core.family
    
    @property
    def probe(self):
        return self.core.probe
    
    @property
    def offline(self):
        return True

    
    

def make_device_list(device = None, include_offline_devices = False):
    if device is None:
        device = Command.get_device()
        require_device(device)
    flattenned = []
    for core in device.probe.all_cores:
        if core in device.probe.cores:
            for vpe in core.vpes:
                if not vpe.offline or include_offline_devices:
                    flattenned.append(vpe)
        elif include_offline_devices:
            flattenned.append(OfflineCoreVpe(core))
    error = device.probe.mode if device.probe.mode == 'failed-autodetection' else '' 
    return DeviceList(flattenned, error)
    
@command()
def listdevices(device=None):
    """Show available devices and their types."""
    return make_device_list(device, True)
list_devices = listdevices
                
@command()
def listvpes(device=None):
    """Show available vpes on the current core."""
    if isinstance(device, Vpe):
        vpes = device.core.vpes
    elif isinstance(device, SoC):
        vpes = device.cores[0].vpes if device.cores else []
    elif isinstance(device, Probe):
        vpes = device.socs[0].cores[0].vpes if device.socs and device.socs[0].cores else []
    else:
        vpes = device.vpes
    return DeviceList(vpes)
list_vpes = listvpes

@command()
def device(device=None):
    """Make the given device current, or return the current device.
    
    After use of this command all commands will target the given device, 
    unless overridden.
    
    >>> device()
    c0v0
    >>> runstate()
    status=expected_reset pc=0x00000000
    >>> runstate(c0v0)
    status=expected_reset pc=0x00000000
    >>> runstate(c2v0)
    status=running
    >>> device(c2v0)
    >>> runstate()
    status=running
    >>> runstate
    runstate(device=None)
    >>> device()
    c2v0
    
    """
    Command.set_device(device)
    update_prompt()
    return device
    
def _get_child_device(parent, childtype, displaytype, index, identifier):
    things = getattr(parent, childtype + 's')
    try:
        return things[index]
    except IndexError:
        plural = displaytype + ('s' if len(things) > 1 else '')
        e = IndexError('Invalid {0}_index {1}, {2} has only {3} {4}'
            .format(displaytype, index, identifier, len(things), plural))
        raise type(e), e, sys.exc_info()[2]
    
@command()
def thread(soc_index, core_index, thread_index, device=None):
    '''Return a thread(vpe/vp) by soc/core/thread index.
    
    These commands are not generally useful in the interative interpreter, but 
    exist to aid writing standalone scripts because the device names soc0, core0,
    s0c0, s0c0v0 are not available in standalone scripts::
    
        from imgtec.console import *
        import time
        if __name__ == '__main__':
            probe(args=parse_startup_args())
            
            s0c0 = core(0, 0)
            
            go(s0c0)  # run all threads in s0c0
            while any(runstate(t).is_running for t in s0c0.threads):
                time.sleep(1)
            print cmdall(runstate, soc(0)) # print runstate of all threads in the soc
            print regs(thread(0, 0, 1))  # print regs from s0c0v0
    
    '''
    c = core(soc_index, core_index, device=device)
    return _get_child_device(c, 'thread', 'thread', thread_index, c.name)

@command(see='thread')
def core(soc_index, core_index, device=None):
    '''Return a core by soc/core index.'''
    s = soc(soc_index, device=device)
    return _get_child_device(s, 'all_core', 'core', core_index, s.name)

@command(see='thread')
def soc(soc_index, device=None):
    '''Return a soc by index.'''
    p = device.probe
    return _get_child_device(p, 'all_soc', 'soc', soc_index, 'the target on ' + p.identifier)

@command()
def closeprobe():
    """Disconnect from the current probe."""
    _cleanup()
    update_prompt()
    
@atexit.register
def _cleanup():
    if Command and Command.get_probe():
        from imgtec.console.commands import cmdall
        cmdall.devices = None
        Command.get_probe()._disconnect(None, None, None)
        Command.set_device(None)
    
class ExecutionState(object):
    '''The result type of go, halt, and step when a single device is specified.'''
    
    def __init__(self, state, symbol, dasm, source):
        self.status = state.status
        """The run status of the vpe/thread."""

        self.pc = state.pc
        """The current value of the PC, only valid if is_running is False."""

        self.state = state
        '''The result of the runstate call.'''
        
        self.symbol = symbol
        '''Symbol name of the pc, if one is relevant.'''
        
        self.dasm = dasm
        '''The disassembly of the instruction at the PC, or None.'''

        self.source = source
        '''File name and line number of current sourcefile, or empty string.'''
        
        self.callbacks_results = state.callbacks_results
        '''List of (name, result of onhaltcallback) for all on halt callbacks'''

        
    @property
    def is_running(self):
        """True if the status is one of the running statuses."""
        return str(self.status) in ('running', 'running_no_debug')
        
    def __repr__(self):
        str = ['%r' % self.state]
        if self.symbol:
            str.append(' %s' % self.symbol)
        if self.source:
            str.append('\n%s' % self.source)
        if self.dasm:
            str.append('\n%r' % self.dasm)
        return ''.join(str)
        
debuggable_states = frozenset([getattr(Status, x) for x in 
    '''stopped halted_by_probe single_stepped exception memory_fault sw_break 
    hw_break expected_reset unexpected_reset soft_reset'''.split()])
        
def _should_dasm(state):
    '''Determine if the current thread status is one that is worth disassembling.
    
    >>> from imgtec.codescape.tiny import State
    >>> from imgtec.codescape.da_types import Status
    >>> _should_dasm(State(Status.running, 0, 0))
    False
    >>> _should_dasm(State(Status.stopped, 0, 0))
    True
    >>> _should_dasm(State(Status.core_offline, 0, 0))
    False
    >>> _should_dasm(State(Status.core_offline, 0xbfc00000, 0))
    True
    >>> _should_dasm(State(Status.running, 0xbfc00000, 0))
    False
    >>> _should_dasm(State(Status.running_no_debug, 0xbfc00000, 0))
    False
    >>> _should_dasm(State(Status.core_offline, 0x9c9c9c9c, 0))
    False
    >>> _should_dasm(State(Status.core_offline, 0x9c9c9c9c9c9c9c9c, 0))
    False
    
    '''
    if state.status in debuggable_states:
        return True
    if not state.is_running and state.pc & 0xffffffff not in (0, 0x9c9c9c9c):
        # If the probe has returned us a 
        return True
    return False


on_halt_callbacks = {}
'''Callbacks to run when the device is halted'''


def _call_on_halt_callbacks(device):
    cbs = sorted(on_halt_callbacks.items())
    onhaltdata = [(name, cb(device)) for name, cb in cbs]
    onhaltdata = [(name, x) for name, x in onhaltdata if x is not None]

    return onhaltdata

def _on_halt(device, dasm=True, on_halt_callbacks=True):
    state = runstate(on_halt_callbacks, device)
    _dasm, symbol, source = None, '', ''
    if dasm and _should_dasm(state) and device.core.family != CoreFamily.meta:
        _dasm = memory.dasm(state.pc, count=1, device=device)
        memory.dasm.address = None
        symbol = get_symbols_string(device, state.pc)
        source = get_source_string(device, state.pc)

    return ExecutionState(state, symbol, _dasm, source)


@command()
def onhaltcallback(name_or_function, *args,  **kwargs):
    '''Decorator used to add callbacks that will be executed on halt.

    * Callbacks registered with the same name as an existing callback will
      replace the existing callback.
    * Callbacks are executed in alphabetical order.
    * The result of the callback (if not None) will be displayed in the
      interpreter, and is also available as the attribute `callbacks_results` of
      the :class:`ExecutionState` returned from go/step/halt, and in the 
      :class:`RunState` returned from runstate. This attribute is a list of 
      (callback name, callback result).
          
    For example ::

        [s0c0v0] >>> @onhaltcallback
                 ... def showmyregs(device):
                 ...     return regs('a0 sp', device=device)
                 ...
        [s0c0v0] >>>
        [s0c0v0] >>> @onhaltcallback('showmyregs2')
                 ... def showmyregs(device):
                 ...     return regs('ra', device=device)
                 ...
        [s0c0v0] >>> step()
        a0 802b6000 sp ffb14738
        0x8000231c
        status=single_stepped pc=0x80002388 status_bits=0x0080
        0x80002388 00000000    nop
        [s0c0v0] >>> _.callbacks_results[0]
        (showmyregs, 0x80002388)

    Callbacks can by also registered with ::

        [s0c0v0] >>> onhaltcallback(regs, 'ra sp')
        [s0c0v0] >>> step()
        ra 0000007b sp ffb14738
        status=single_stepped pc=0x80002ef0 status_bits=0x0080
        0x80002ef0 00000000    nop

    '''
    if isinstance(name_or_function, support.Command):
        def _helper(device):
            return name_or_function(*args, **kwargs)
        on_halt_callbacks[name_or_function.__name__] = _helper
    elif isinstance(name_or_function, basestring):
        def _decorator(f):
            on_halt_callbacks[name_or_function] = f
            return f
        return _decorator
    else:
        on_halt_callbacks[name_or_function.__name__] = name_or_function
        return name_or_function

def _needs_brkstep(device, state=None):
    state = runstate(device) if state is None else state
    if state.status in [Status.sw_break, Status.hw_break]:
        # This is a quick test, needs to do more than this
        # as this will not catch all cases
        addrs = [bp.address & ~1 for bp in breakpoints.all_breakpoints(device).values()]
        return (state.pc & ~1) in addrs
    elif state.status == Status.exception and (state.status_bits == 0x8000 or state.status_bits == 0x4000):
        return True  # TODO remove legacy code at some point.
    return False

def _step(devices, count, states):
    for d, state in zip(devices, states):
        if _needs_brkstep(d, state):
            breakpoints.suppress_all_bps(d)
    
    devices[0].tiny.Step(count, _get_execution_tids(devices))
    now = start = time.time()
    states = {}
    printed_message = False
    running = devices[:]
    while running:
        states.update(dict([(d.name, runstate(d)) for d in running]))
        running = [d for d in running if states[d.name].status == Status.running]
        if running:
            who = ', '.join([d.name for d in running])
            is_are = 'is' if len(running) == 1 else 'are'
            has_have = 'has' if len(running) == 1 else 'have'
            if not printed_message and (now - start) > 2.0 and sys.stdin.isatty():
                print "%s %s still running, use Ctrl-C to interrupt." % (who, is_are)
                printed_message = True
            if (now - start) > 10.0:
                raise RuntimeError("%s %s not completed the step after 10s, aborting" % (who, has_have))
            if (now - start) > 1.0:
                time.sleep(0.5)
            now = time.time()
    for device in devices:
        breakpoints.activate_all_bps(device)
        device._was_running_last_time = True
    return [states[d.name] for d in devices]
    
def _get_execution_tids(devices):
    return ['s%dc%dt%d' % (d.core.soc.index, d.core.index, d.index) for d in devices]

def _on_halts(devices, dasm, _on_halt_callbacks, msgs=[], verbose=True):
    res = AllResult()
    res.call(_on_halt, devices, dasm, _on_halt_callbacks)
    if verbose:
        for msg in msgs:
            print msg
    return res.get_result_maybe_just_one()

@command(dasm=dasms)
def step(count=1, dasm=True, on_halt_callbacks=True, devices=[]):
    """Step the specified device(s) `count` instructions.
    
    This function will wait up to 10s for the target to complete the step 
    before failing.
    
    After stepping the runstate is queried and returned. If the target is halted
    and `dasm` is True then the current disassembled instruction is also
    returned along with results of "on halt callbacks" if `on_halt_callbacks` is
    True.
    
    Like :func:`~imgtec.console.go()`, multiple devices can be specified, and
    the return type is the same as go.
    """
    states = [runstate(d) for d in devices]
    _step(devices, count, states)
    memory.dasm.address = None
    return _on_halts(devices, dasm, on_halt_callbacks)
            
@command(dasm=dasms, verbose=verbosity)
def go(dasm=True, verbose=True, devices=[]):
    """Run the specified device(s) from the current execution point(s).
    
    After running the runstate is queried and returned. If `dasm` is True and 
    the target is halted then the current disassembled instruction is also 
    returned.
    
    Like all parameters with defaults of all commands, the default for the dasm 
    parameter can be changed for the duration of the console session::
    
        [s0c0v0] >>> halt()
        status=stopped pc=0x0ff5c188 status_bits=0x8000000000000000
        0x0ff5c188 041186f8    bal       0x0ff3dd6c
        [s0c0v0] >>> halt.dasm = False
        [s0c0v0] >>> go() and halt()
        Running from 0x0ff5c188
        status=stopped pc=0x0ff3dd74 status_bits=0x8000000000000000
    
    `go`, `halt`, and `step` accept multiple devices, and if a soc or a core is 
    provided then each of the threads(vpes) under that soc or core will be 
    started.  Some examples (assuming a soc containing 2 cores each with 2 
    threads):
    
    ================= ===============================
    Command           Threads affected
    ================= ===============================
    go(s0c0v0, s0c1)  s0c0v0, s0c1v0, s0c1v1
    go(soc0)          s0c0v0, s0c1v0, s0c1v0, s0c1v1
    go(s0c1)          s0c1v0, s0c1v1
    ================= ===============================
    
    The return value of `go` (and `step` and `halt`) is an instance of 
    :class:`ExecutionState` which  can be queried for it's running state, the
    PC, and the disassembly (if it was performed).  When multiple devices are 
    used, then a list of state objects is returned::
    
        [s0c0v0] >>> go(core0)
        Running from 0x80000000
        Running from 0x80000e30
        s0c0v0: status=running
        s0c0v1: status=running
        [s0c0v0] >>> _[0].state.is_running, _[0].state.pc
        (True, 0x00000000)    
    
    """
    states = [(d, runstate(d)) for d in devices]
    
    msgs = ['Running from 0x%08x %s' % (state.pc, get_symbols_string(d, state.pc)) for d, state in states if not state.is_running] if verbose else []
    try:
        need_stepping = [(d, state) for d, state in states if _needs_brkstep(d, state)]
        if need_stepping:
            devs, states = zip(*need_stepping)
            after_step_states = _step(devs, 1, states)
        if not need_stepping or all(state.status == Status.single_stepped for state in after_step_states):
            devices[0].tiny.Run(_get_execution_tids(devices))
    finally:
        memory.dasm.address = None
        for device in devices:
            device._was_running_last_time = True
    return _on_halts(devices, dasm, on_halt_callbacks, msgs, verbose=verbose)

@command(dasm=dasms)
def halt(dasm=True, on_halt_callbacks=True, devices=[]):
    r"""Halt the specified device(s).
    
    After halting the runstate is queried and returned. If the target is halted
    and `dasm` is True then the current disassembled instruction is also
    returned along with executing any registered :func:`onhaltcallback`\s if 
    `_on_halt_callbacks` is True.
    
    Like :func:`~imgtec.console.go()`, multiple devices can be specified, and 
    the return type is the same as go.
    """
    devices[0].tiny.Stop(_get_execution_tids(devices))
    memory.dasm.address = None
    return _on_halts(devices, dasm, on_halt_callbacks)

class Runstate(object):
    """The state of a vpe/thread."""
    def __init__(self, state, callbacks_results = []):
        self.status = state.status
        """The run status of the vpe/thread."""

        self.pc = state.pc
        """The current value of the PC, only valid if is_running is False."""

        self.status_bits = state.status_bits
        """Extra information about the status of the target.  This target
        specific, and not currently documented."""

        self.callbacks_results = callbacks_results
        '''List of (name, result of onhaltcallback) for all on halt callbacks'''

    @property
    def is_running(self):
        """True if the status is one of the running statuses."""
        return str(self.status) in ('running', 'running_no_debug')
        
    def __repr__(self):
        cbresults = ''
        for _name, cbresult in self.callbacks_results:
            res = cbresult if isinstance(cbresult, basestring) else repr(cbresult)
            cbresults += res + '\n'
        pc = ''
        if not self.is_running:
            pc = 'pc=%r' % (self.pc,)
        extra = ''
        if self.status_bits:
            extra = ' status_bits=0x%04x' % (long(self.status_bits),)
        return cbresults + "status=%s %s%s" % (self.status, pc, extra)
            
@command()
def runstate(on_halt_callbacks=True, devices=[]):
    r"""Get the running/halted state of the specified device(s).
    
    This command returns an instance of :class:`Runstate` which can be queried
    for various states::
        
        state = runstate()
        if state.is_running:
            print 'Target is running'
        else:
            print 'Target is %s at pc=%r' % (state.status, state.pc)

    If `on_halt_callbacks` is True and the target is newly halted then all 
    registered :func:`onhaltcallback`\s will be called and their results 
    displayed.

    """
    def _runstate(device):
        state = device.tiny.GetState()
        cbs = []
        was_running, device._was_running_last_time = device._was_running_last_time, state.is_running
        if not state.is_running and was_running and on_halt_callbacks:
            cbs = _call_on_halt_callbacks(device)
        return Runstate(state, cbs)    
        
    res = AllResult()
    res.call(_runstate, devices)
    return res.get_result_maybe_just_one()    

    
def string_to_advanced_options(ao):
    if ao:
        try:
            return dict([opt.split('=', 1) for opt in ao.split(',')])
        except Exception:
            raise RuntimeError('Invalid advanced-options string, should be in the form "key1=foo,key2=bla"')
    else:
        return dict()


def _restore_logging_settings(logging_settings):
    for k, v in logging_settings.iteritems():
        try:
            _set_logging(None, k, v, False)
        except da_exception.Error:
            pass # JTAG Logging is frequently not available, don't panic


@command(verbose=verbosity)
def probe(identifier=None, ip_address='', force_disconnect=False, advanced_options={}, args=None, verbose=True, __codescape=None):
    """Connect to a probe, or displays information about the current probe.

    The identifier should be of the following form    

            ================ ====================================
            DA Type          Identifier Format
            ================ ====================================
            DA-net           "DA-net 1"
            Local Simulator  "Simulator HTP221"
            Remote Imperas   "RemoteImperas hostname:port"
            Remote Simulator "RemoteSimulator hostname:port"
            ================ ====================================
            
    If force_disconnect is True, and the probe is currently in use, then the
    other user will be forcibly disconnected.  This should be used with 
    consideration for others.
    
    If the probe cannot be located using DNS, or UDP broadcast, then it may
    be necessary to specify an IP address using `ip_address`.
    
    `advanced_options` is a dictionary of options that are passed to the 
    comms layer.  It is not normally necessary to use these.
    
    If this command is to be used from a script you can also pass it the result 
    of the ``parse_startup_args`` function ::
    
      with probe(args=parse_startup_args()):
          startup()
          
    Using this method will automatically accept the correct arguments from 
    Codescape Debugger when used as a Connect Script. When the script is called
    as a Reset/Breakpoint/Run Script or Script Region then the correct probe
    will be determined and Codescape Debugger will be prevented from accessing 
    the target for the duration of the with block. See the help page on 
    :ref:`integrating` for examples and more information.
        
    """
    environment, csthread = 'standalone', None
    if args is not None:
        identifier = args.probe
        force_disconnect = args.force_disconnect
        ip_address = args.search_location
        advanced_options = string_to_advanced_options(args.advanced_options)
        if not identifier and args.environment != 'standalone':    
            if not __codescape:
                from imgtec import codescape as __codescape
            csthread = __codescape.GetSelectedThread()
            identifier = csthread.probe.name
        if not identifier:
            from imgtec.console.main import format_usage
            raise TypeError("probe identifier argument not specified:\n" + format_usage())
        environment = args.environment 
        for log in args.logging:
            try:
                _global_logging[log] += 1
            except KeyError:
                print 'Unknown log', log

    if identifier is not None:
        if not isinstance(identifier, basestring):
            extra = ''
            from imgtec.console.commands import reset
            from imgtec.console.cfg import config
            if identifier in (reset, logging, config):
                extra = '\nDid you mean %s(probe)?' % (identifier.__name__,)
            raise TypeError("probe identifier argument must be a string of the form 'DA-net xxx'" + extra)
        closeprobe()
        options = dict(advanced_options)
        if force_disconnect:
            options['force-disconnect'] = True
        if ip_address:
            options['search-location'] = ip_address
        exitfn = None
        if csthread:
            t = csthread.Locked()
            t.__enter__()
            exitfn = t.__exit__
            
        _restore_logging_settings(_global_logging)
        tiny = connect(identifier, options)
        p = Probe(tiny, environment=environment, exitfn=exitfn)
        Command.set_device(p)
        _restore_logging_settings(p._logging)
        p.scan_devices(verbose=verbose)
        from imgtec.console.commands import cmdall
        cmdall.devices = None
        
    else:
        if ip_address:
            raise RuntimeError("An identifier is required when using an IP address.")

        p = Command.get_probe()
        if not p and verbose:
            print "No probe selected, use probe('DA-net 1234') to configure a probe."
    return p


@command()
def probemode(device=None):
    '''Get the operating mode of the probe.
    
    This is one of 'uncommitted', 'scanonly', 'table', or 'autodetected'.
    
    Debugging connections which do not support operating mode will typically
    return 'autodetected'.
    
    See :ref:`tdd-intro` for more information about the operating modes of the 
    probe.
    '''
    p = device.probe
    p._update_name()
    return StrResult(p.mode)

@command()
def simulators(filter=None):
    """List available simulators.

    Simulators can be connected to using probe().
    
    If `filter` is given then only those simulator names containing the filter
    are returned.
    
        >>> simulators('1004kc')
        0: Simulator IAsim-1004K_1004Kc-BE
        1: Simulator IAsim-1004K_1004Kc-LE
        >>> probe(_[0])        
        Identifier Simulator IAsim-1004K_1004Kc-BE
        Firmware   2.0.0.220
        Mode       autodetected
        TCK Rate   31kHz        

    """
    from imgtec.codescape.tiny import GetConfiguredSimulators
    sims = GetConfiguredSimulators()
    if filter:
        sims = [x for x in sims if filter.lower() in x.lower()]
    return NumberedListResult(sims)
    
    
@command()
def discoverprobes():
    """Return a list of nearby probes.

    Probes in the local subnet and connected via USB are discovered and returned
    as a list of identifiers.

        >>> discoverprobes()
        0: SysProbe 1234
        1: DA-net 1234
        >>> probe(_[0])
        Identifier SysProbe 1234
        Firmware   2.0.0.220
        Mode       autodetected
        TCK Rate   31kHz

    """
    from imgtec.codescape.tiny import DiscoverProbes
    sims = [Identifier(x[0]) for x in DiscoverProbes()]
    return NumberedListResult(sims)


    
@command(vpe_required=True, update=updates)
def cpuinfo(update=False, device=None):
    """Get information about the current device. 
    Set 'update' to fill in cache information which is not read by default.
    """
    info = device.tiny.CpuInfo(update)
    if not info:
        raise RuntimeError("Device %r has no cpu info" % (device,))
    return OrderedDictResult(info)
    
@command(vpe_required=True)
def endian(device=None):
    """Get current endianness of the current device.

    Returns a string 'big' or 'little' for the current state of the processor.
    """
    end = ['little', 'big'][device.tiny.GetEndian()]
    return StrResult(end)
    

class OnOff(int):
    def __repr__(self):
        if self == 1:
            return 'on'
        elif self == 0:
            return 'off'
        else: 
            return '%d' % (self,)

@command(enable=[(on, True), (off, False), (enable, True), (disable, False)],
         type=[namedstring(console), namedstring(probe), namedstring(jtag), namedstring(comms)],
         device_required=False)
def logging(type=None, enable=None, show_previous=False, device=None):
    """Enable, disable, or show the logging state of various components.

    At present the log types supported are

    comms
        Shows logging of console comms commands (i.e. the commands
        sent to the probe), these are printed as a command completes.

    probe/jtag
        Shows info level, verbose, or JTAG level logging from the probe. This
        is stored as a circular buffer in the DA.  After each command is
        executed the circular buffer is retrieved and any new data is
        displayed.
    
    console
        Show the called commands and returned values from all Codescape Console
        commands.  This is of no use in an interactive shell, but in console
        scripts it can be useful.

    If `show_previous` is True, and the log type is one stored on the probe
    in a circular buffer, then the entire log contents up to this point is
    displayed immediately.  This might include a lot of irrelevant log info
    so it is not normally advised, but if you want to capture the log of an
    event which has already occurred this can be useful ::

        >>> logging(probe, on, show_previous=True)

        <<<<<<<<<<<<<<<<<<   LOG WRAPPED  >>>>>>>>>>>>>>>>>>>>>>>
        0x00000000 from address 0xff20021c
        2088154.109:SoC  0:Core  0 : <info> : cache_mips_info           : DCR: 0x200303db, Endian Big Endian
        2088154.109:SoC  0:Core  0 : <info> : cache_mips_info           : Enabling PC Sampling
        2088154.109:SoC  0:Core  0 :<verbos>: write32                   :
        2088154.109:SoC  0:Core  0 :<verbos>: execute                   : eJTAG-DMSEG: exec 0xff200204 3c08ff30    lui
        2088154.110:SoC  0:Core  0 :<verbos>: execute                   : eJTAG-DMSEG: exec 0xff200208 35080000    ori
        ...

    Otherwise, if `show_previous` is False(the default),  then the circular
    log is retrieved but not displayed.

        >>> logging()
        comms   off
        console off
        probe   off
        jtag    off

        >>> logging(comms)
        comms off

        >>> logging(comms, on)
        comms on

    If the probe has Verbose logging enabled and logging(probe) is on, then the
    probe's verbose log will be read.

        >>> config('Verbose Logging', True)
        1

    """
    logging = device.probe._logging if device else _global_logging
    if enable is not None and type is not None:
        was = logging[type]
        enable = int(enable)
        logging[type] = enable
        if was != enable:
            _set_logging(device, type, enable, show_previous) 

    if type is None:
        items = logging.items()
    else:
        items = [(type, logging[type])]
    rows = [(k, OnOff(v)) for k, v in sorted(items)]
    return HeaderlessTableResult(rows)

def _getChild(logger, name):
    _logging.getLogger(logger.name + '.' + name)

def _set_logging(device, type, enable, show_previous):
    logger = None
    if type == 'comms':
        logger = comms_logger
    elif type == 'console':
        logger = _logging.getLogger('console')
    elif type == 'jtag':
        if device and 'Simulator' not in device.probe.identifier:
            from imgtec.console.cfg import config
            config('JTAG Logging', int(bool(enable)), device=device)
            if 0 and 'SysProbe' in device.probe.identifier:
                logger = _getChild(comms_logger, 'jtag')
            else:
                # fall back on diagnostic file collection
                device.probe._logfilenames['jtag'] = 'DA JTAG Log'
    elif type == 'simulator':
        logger = _getChild(comms_logger, 'simulator')
    elif type == 'probe':
        if device and 'Simulator' not in device.probe.identifier:
            if 0 and 'SysProbe' in device.probe.identifier:
                logger = _getChild(comms_logger, 'probe')
            else:
                # fall back on diagnostic file collection
                device.probe._logfilenames['probe'] = 'DA Verbose Log'

    if logger:
        if enable == 0:
            logger.setLevel(_logging.WARNING)
        elif enable == 1:
            logger.setLevel(_logging.INFO)
        elif enable > 1:
            logger.setLevel(_logging.DEBUG)
        root = _logging.getLogger('')
        if not root.handlers:
            _add_root_handler()
            
    elif enable and device:
        device.probe._collect_log(type, show_previous)
        
    if device and device.tiny and hasattr(device.tiny, 'RefreshLoggerLevels'):
        device.tiny.RefreshLoggerLevels()


@command()
def logfile(names=None, filename=None, device=None):
    """Display the contents of a log file from the probe.
    
    Whilst logging allows you to see a live log of messages from the probe, 
    this command allows you to see the entire log in one go.
    
    When called without arguments, the logs available on the probe are returned
    as a list.
    
    If `filename` is given the log is written to `filename`.  If filename is 
    given and names is None, all available logfiles are written to `filename`.

    `names` should be one name of log file or list of names
    (then contents will be merged but all of them must have timestamps).
    """

    files = device.tiny.GetDiagnosticFileList()
    if not names:
        if filename:
            res = _get_logs_contents(files, device)
        else:
            return StrListResult(files)       
    else:
        names = [names] if not isinstance(names, list) else names
        case_match = dict((x.lower(), x) for x in files)
        names = [case_match.get(name.lower(), name) for name in names]
        res = _get_logs_contents(names, device)

    if filename:
        with open(filename, 'w') as f:
            f.write(replace_exec_dasm(res))
        return os.path.abspath(filename)
    else:
        return res


def _get_logs_contents(names, device):
    if len(names) == 1:
        return device.tiny.GetDiagnosticFile(names[0])
    else:
        contents = set()
        for name in names:
            content = device.tiny.GetDiagnosticFile(name)
            splited = _get_split_timestamps_and_text(content, name)
            contents.update(splited)
        logs = sorted(contents, key=lambda t: (t[0], t[1]))
        res = "\n".join("{0}.{1}:{2}".format(t[0], t[1], t[2]) for t in logs)
        return res


def _get_split_timestamps_and_text(content, name):
    """
    >>> content = '''80020.935:s0c0:mem : read_memory : cnt = 72, sz = 4
    ... 171790.901:s0c0:info: halt : Halt [thread 0]
    ...
    ... 1641027.874:s0c0:info: reset : reset'''
    >>> sorted(_get_split_timestamps_and_text(content, "name"))
    [(80020, 935, 's0c0:mem : read_memory : cnt = 72, sz = 4'), (171790, 901, 's0c0:info: halt : Halt [thread 0]'), (1641027, 874, 's0c0:info: reset : reset')]

    >>> content = '''80020.935:s0c0:mem : read_memory : cnt = 72, sz = 4
    ... some content without time stamp some content without time stamp
    ... 1641027.874:s0c0:info: reset : reset'''
    >>> _get_split_timestamps_and_text(content, "log_name")
    Traceback (most recent call last):
       ...
    RuntimeError: Cannot merge logfiles because 'log_name' has got logs without timestamps.
    Please pass only one log name.

    >>> content = '''
    ... <<<<<<<<<<<<<<<<<<   LOG WRAPPED  >>>>>>>>>>>>>>>>>>>>>>>
    ... not mapped in mmu
    ... 1641027.874:s0c0:info: reset : reset
    ... 1641027.704:s0c0:info: context_block : read of general'''
    >>> sorted(list(_get_split_timestamps_and_text(content, "name")), key=lambda x: x[1])
    [(1641027, 704, 's0c0:info: context_block : read of general'), (1641027, 874, 's0c0:info: reset : reset')]

    """
    contents = set()
    content = content.splitlines()
    if len(content) > 3:
        if not content[0].split() and "LOG WRAPPED" in content[1]:
            content = content[3:]
    for line in content:
        m = re.match(r"\s*(\d+)\.(\d+):(.*)", line)
        if m:
            sec, msec, txt = m.groups()
            contents.add((int(sec), int(msec), txt))
        elif line.strip():
            raise RuntimeError("Cannot merge logfiles because '{0}' has got logs without timestamps.\n"
                               "Please pass only one log name.".format(name))
    return contents


regex_broken_timestamp = re.compile(r"^(\d+)\.(429\d{4}):", re.M)
regex_disasm = re.compile(r"eJTAG-(?:DMSEG|DMESG):(\w+): executing 0x([0-9a-f]{0,8})([0-9a-f]{8}) from address 0x([0-9a-f]+)", re.I)


max_uint32 = 1 << 32

def _fixup_overflowed_timestamp(seconds, milliseconds):
    '''
    
    >>> '%d.%03d' % _fixup_overflowed_timestamp(10, (max_uint32 / 1000) -999)
    '9.001'
    >>> '%d.%03d' % _fixup_overflowed_timestamp(10, (max_uint32 / 1000) -1)
    '9.999'
    >>> '%d.%03d' % _fixup_overflowed_timestamp(10, 999)
    '10.999'
    '''
    if milliseconds > 999:
        milliseconds = 1000 - (max_uint32/1000 - milliseconds)
        return (seconds-1, milliseconds)
    else:
        return (seconds, milliseconds)
    
    

def replace_exec_dasm(s, device=None):
    '''
    >>> replace_exec_dasm('57965.4294187:s0c0:info: execute                   : eJTAG-DMSEG: exec 0xff20020c fc288010    sd        t0, -32752(at)')
    '57964.220:s0c0:info: execute                   : eJTAG-DMSEG: exec 0xff20020c fc288010    sd        t0, -32752(at)'
    >>> replace_exec_dasm('57965.999:s0c0:info: execute                   : eJTAG-DMSEG: exec 0xff20020c fc288010    sd        t0, -32752(at)')
    '57965.999:s0c0:info: execute                   : eJTAG-DMSEG: exec 0xff20020c fc288010    sd        t0, -32752(at)'
    >>> replace_exec_dasm('eJTAG-DMSEG:mips64r6: executing 0x40a8c000ff200210 from address 0x0068a0d0')
    'eJTAG-DMSEG: exec 0xff200210 40a8c000    dmtc0     t0, DEPC '
    >>> replace_exec_dasm('eJTAG-DMSEG:mips64r6: executing 0xfff200214 from address 0x0068a0d0')
    'eJTAG-DMSEG: exec 0xff200214 0000000f    sync       '
    >>> replace_exec_dasm('eJTAG-DMSEG:mips64r6: executing 0x0068a0d0 from address 0xff200214')
    'eJTAG-DMSEG: exec 0xff200214 0068a0d0    clz       s4,  v1 '
    '''
    try:
        from imgtec.codescape import tiny
    except ImportError:
        return s
    else:
        def disasm(m):
            isa, word_bug, word, addr = m.group(1, 2, 3, 4) 
            if word_bug:        # sysprobe on mips64 sometimes formats the word badly using llx instead of x.
                addr, word = word, word_bug            
            bytes = struct.pack('>I', int(word or '0', 16))
            try:
                addr = int(addr, 16)
                if device is not None:
                    isa = device.tiny.GetCurrentISA(addr)
                return 'eJTAG-DMSEG: exec %r ' % (tiny.DisassembleBytes(addr, None, isa, 'o32', bytes),)
            except Exception as e:
                print "Warning : %s" % (e,)
                return m.group(0)
        def timestamp(m):
            seconds, milliseconds = m.group(1, 2)
            return '%4d.%3d:' % _fixup_overflowed_timestamp(int(seconds), int(milliseconds))
            
        s = regex_disasm.sub(disasm, s)    
        return regex_broken_timestamp.sub(timestamp, s)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
