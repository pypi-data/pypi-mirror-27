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

from imgtec.console.generic_device import soc, core, probe
from imgtec.console.support import comms, console, on, off, enable, disable, command, require_device, namedstring, verbosity, restoredefaults
from imgtec.console import results
from imgtec.codescape import probe_config
from imgtec.lib import rst
from imgtec.lib import get_user_files_dir
from imgtec.lib.ordered_dict import OrderedDict
import atexit
import re
from collections import namedtuple
import ConfigParser
from difflib import get_close_matches
import errno
import itertools
import os
from textwrap import dedent

__all__ = ('config',)

MetaData = namedtuple('MetaData', 'name type category category_index doc default')

global_category_order = ['']  # empty category is always first

def make_meta_data(name, default, category='', doc='', category_order=global_category_order, type=None):
    try:
        category_index = category_order.index(category)
    except ValueError:
        category_index  = len(category_order)
        category_order.append(category)
    if type is None:
        if default is None:
            raise ValueError("If default is None then type must be specified")
        type = probe_config.typeof(default)
    return MetaData(name, type, category, category_index, doc, default)
    
class ConsoleConfig(object):
    metas = [
        make_meta_data('traceback', False, 'Advanced', doc='''\
            When True any python exceptions raised during a command execution will be
            displayed in full. When False only traceback from outside the imgtec module
            will be shown with the exception. 
            '''),
        make_meta_data('toolkit',   r'${MIPS_ELF_ROOT}/bin', doc='''\
            Path to the directory containing a MIPS toolkit.'''),
        make_meta_data('toolkit_prefix', '', doc='''\
            Prefix used for toolkit executables, for example mips-mti-elf-.
            If empty then a suitable default is used for the given ISA.'''),
        make_meta_data('scripts_path',  get_user_files_dir('console_scripts'), doc='''
            Path to the console_scripts folder which can contain user commands.
            
            $console_scripts is placed on sys.path, so ``import modulename`` can be
            used to load user scripts.  Alterntively the file $scripts_path/__init__.py 
            is executed at Codescape Console startup so any imports in that file will 
            be automatically imported at startup.
            '''),
        make_meta_data('java_path', 'java', doc='''\
            Path to a java executable, this is 'java' by default so as long as java is 
            on the path this should not need configuring.'''),
        make_meta_data('dqer_path', '', doc='''\
            Path to a folder containing a CSDQer.jar or a path to the .jar itself.  
            If empty the DQer installed with Codescape Debugger will be used.'''),
    ]
    metas = OrderedDict([(m.name, m) for m in metas])
    def __init__(self):
        for meta in self.metas.values():
            setattr(self, meta.name, meta.default)

    def read_config(self, f):
        c = ConfigParser.RawConfigParser()
        c.readfp(f)
        for item in self.items():
            if c.has_option('console', item):
                current = getattr(self, item)
                try:
                    if isinstance(current, (int, long)):
                        setattr(self, item, c.getboolean('console', item))
                    elif isinstance(current, (int, long)):
                        setattr(self, item, c.getint('console', item))
                    else:
                        setattr(self, item, c.get('console', item))
                except ValueError as e:
                    print "Warning: could not convert config item %s to %s : %s" % (item, type(current).__name__, e)

    def write_config(self, f):
        c = ConfigParser.RawConfigParser()
        c.add_section('console')
        for item in self.items():
            c.set('console', item, str(getattr(self, item)))
        c.write(f)

    def read(self, name):
        return getattr(self, name)

    def write(self, name, value):
        self.read(name)
        setattr(self, name, value)#
    
    def items(self):
        return self.metas.keys()

    def list(self):
        return self.items()
        
    def meta_data(self, name):
        return self.metas[name]

console_config = ConsoleConfig()
console_config_path = os.path.expanduser('~/.com.imgtec/codescape_console.config')

def read_config():
    try:
        with open(console_config_path, 'r') as f:
            console_config.read_config(f)
    except EnvironmentError:
        pass

@atexit.register
def write_config():
    try:
        try:
            os.mkdir(os.path.dirname(console_config_path))
        except EnvironmentError as e:
            if e.errno != errno.EEXIST:
                raise
        with open(console_config_path, 'w') as f:
            console_config.write_config(f)
    except EnvironmentError as e:
        print "Failed to write config %s : %s" % (console_config_path, e)

class ConfigProvider(object):
    def read(self, name):
        pass
    def write(self, name, value):
        pass
    def list(self):
        return []
    def meta_data(self, name):
        return make_meta_data(name, 0, '', 0, '')


class _ConfigAsDictProvider(ConfigProvider):
    def __init__(self, reader, writer, writer_args):
        self.reader = reader
        self.writer = writer
        self.writer_args = writer_args

    def read(self, name):
        return self._config[name]

    def write(self, name, value):
        # comms options don't typically have meta data (yet), but nor are they all ints, 
        # so use self.meta_data to coerce the value to the correct type. What is more
        # don't fail if the coeercion fails, trust the user but issue a warning
        meta = self.meta_data(name)
        try:
            value = meta.type(value)
        except Exception:
            print 'Warning : whilst setting {}, failed to coerce {!r} to {}.'.format(name, value, meta.type.__name__)
        self.writer(name, value, *self.writer_args)
        self.list()

    def list(self):
        self._config = self.reader()
        return self._config.keys()

class ProbeSettingsProvider(_ConfigAsDictProvider):
    def __init__(self, device, *writer_args):
        super(ProbeSettingsProvider, self).__init__(device.tiny.GetProbeSettings, device.tiny.SetProbeSetting, writer_args)
        configs = probe_config.get_configs_for_probe(device.probe.identifier)
        self.configs = dict([(c.name.lower(), c) for c in configs])
        self.categories = []
        for c in configs:
            if c.category not in self.categories:
                self.categories.append(c.category)

    def meta_data(self, name):
        try:
            c = self.configs[name.lower()]
            return make_meta_data(c.name, c.default, c.category, doc=c.doc, category_order=self.categories)
        except KeyError:
            return make_meta_data(name, None, 'Advanced', type=int)
        
class CommsSettingsProvider(_ConfigAsDictProvider):
    def __init__(self, device):
        super(CommsSettingsProvider, self).__init__(device.probe.tiny.GetCommsSettings, device.probe.tiny.SetCommsSetting, ())
        
    def meta_data(self, name):
        # nearly all comms options are str's. Or at least have to be passed that
        # way for now
        return make_meta_data(name, '', type=str)
        
def _format_config_results(metas, values, type):
    '''
    
    >>> catorder = ['CatB']
    >>> metas = [make_meta_data('Name1', 1, 'CatA', category_order=catorder),
    ...          make_meta_data('Name2', 0, 'CatB', category_order=catorder)]
    >>> _format_config_results(metas, [42, 43], probe)
    ===CatB=== ===CatA===
    Name2 0x2b Name1 0x2a
    '''
    meta_values = zip(metas, values)
    def catsort(meta_value):
        meta, _value = meta_value
        return meta.category_index, meta.name.lower()
    def catgroup(meta_value):
        meta, _value = meta_value
        return meta.category
    meta_values.sort(key=catsort)
    tabs = []
    for category, incategory in itertools.groupby(meta_values, key=catgroup):
        items = [(meta.name, value) for meta, value in incategory]
        tabs.append((category, items))
    return results.ConfigTabbedDict(tabs, type)

def _read_config_or_exception(provider, n):   
    try:
        return provider.read(n)
    except Exception as e:
        return e
        
def _format_config_result(meta, value, c_type, restore_func=None, restore_args=None):
    '''Return a single config value with docs and type info in the repr.
    
    >>> _format_config_result(make_meta_data('Name', 0, doc='doc'), 0, 'type')
    Name = 0x0 [default=0x0]
      doc
    >>> _format_config_result(make_meta_data('Name', '', doc='doc'), '', 'type')
    Name = '' [default='']
      doc
    >>> _format_config_result(make_meta_data('Name', None, doc='doc', type=int), 0, 'type')
    Name = 0x0
      doc
    >>> _format_config_result(make_meta_data('Name', probe_config.Namespace.unknown, doc='doc'), 0, 'type')
    Name = 0x0 (unknown) [default=0x0 (unknown)]
      doc
    <BLANKLINE>
      0x0 unknown
      0x1 probe
      0x2 meta
      0x3 mips
      0x4 dbu
      0x5 ejtag
    '''
    default, enumvalue = '', ''
    doc = dedent(meta.doc)
    if hasattr(meta.type, '_items'):
        try:
            enumvalue = ' ({0})'.format(str(meta.type(value)))
        except ValueError:
            enumvalue = '\n'
        rows = [('0x%x' % v, n) for n, v in meta.type._items()]
        doc += '\n\n' + rst.headerless_table(rows)
        if meta.default is not None:
            try:
                default = ' [default={0} ({1})]'.format(results._display(int(meta.default)), str(meta.type(meta.default)))
            except ValueError:
                pass
    elif meta.default is not None:
        default = ' [default={0}]'.format(results._display(meta.default))
    doc = '\n'.join(['  ' + x for x in doc.splitlines()])
    basetype = int if isinstance(value, bool) else type(value)
    
    class ConfigResult(basetype):
        name = meta.name
        config_type = c_type
        def __enter__(self):
            return self
        def __exit__(self, *exc):
            if not None in [restore_func, restore_args]:
                restore_func(*restore_args)
        def __repr__(self):
            return '{0} = {1}{2}{3}\n{4}'.format(meta.name, results._display(value), enumvalue, default, doc)            
    return ConfigResult(value)

def _get_provider(type, device=None):
    if type in ('probe', 'soc', 'core'):
        require_device(device)
        return ProbeSettingsProvider(device, type)
    elif type == 'comms':
        require_device(device)
        return CommsSettingsProvider(device)
    elif type == 'console':
        return console_config
    else:
        raise RuntimeError("Unknown config type %r"  % (type,))

def _get_default_config_values(type, device):
    provider = _get_provider(type, device)
    if type in ('probe', 'soc', 'core'):
        valid_options = set(provider.configs.keys()).intersection(set(provider.list()))
        return {provider.configs[option].name:provider.configs[option].default
                for option in valid_options}
    elif type == 'console':
        return {provider.metas[option].name:provider.metas[option].default 
                for option in provider.metas}
    elif type == 'comms':
        raise RuntimeError('Cannot restore comms options to default.')

def _restore_single_config_option(new_config, option_name, value_to_restore, 
                                  config_type, verbose, device):
    try:
        if new_config.get(option_name) == value_to_restore:
            return config(type=config_type, name=option_name, device=device)
        elif new_config.get(option_name) is None:
            if verbose > 0:
                print 'Warning:', option_name, 'is not a valid option in the most recent configuration, but was valid when it has been saved. Restoring it...'
        m = re.match(r'^(.+?)\.s(\d+)c(\d+)$', option_name)
        if not m:
            try:
                config(name=option_name, value=value_to_restore, type=config_type, device=device)
            except KeyError:
                device.tiny.SetProbeSetting(option_name, value_to_restore, config_type)
        else:
            name, s, c = m.group(1), int(m.group(2)), int(m.group(3))
            device.tiny.SoC(s).Core(c).SetProbeSetting(name, value_to_restore, 'core')
        if verbose > 1:
            print 'Option {} has been changed from {} to {}.'.format(option_name, new_config.get(option_name), value_to_restore)
        return config(type=config_type, name=option_name, device=device)
    except Exception as e:
        if not option_name.startswith('fast mon cache mode'):
            if verbose > 0:
                print 'Warning: Could not restore {} option {}={} [error: {}]'.format(config_type, option_name, value_to_restore, e)
      
def _restore_previously_saved_config(restore, device, verbose):
    new_config = config(type=restore.config_type)

    # Special handling for single-result config.
    if not isinstance(restore, results.ConfigTabbedDict):
        return _restore_single_config_option(new_config, restore.name, 
                                             restore, restore.config_type, verbose, device)

    newly_added_options = list(set(new_config.keys()) - set(restore.keys()))
    
    for option in sorted(newly_added_options):
        if verbose > 0:
            print 'Warning:', option, 'has been added since the latest saved config result.'

    for name, value in restore.items():
        if new_config.get(name) == value:
            continue
        _restore_single_config_option(new_config, name, value, 
                                      restore.config_type, verbose, device)
    
    return config(type=restore.config_type)

def _restore_default_values(config_type, verbose, device):
    new_config = config(type=config_type)
    defaults = _get_default_config_values(config_type, device)
    
    for name, value in defaults.items():
        if new_config.get(name) == value:
            continue
        _restore_single_config_option(new_config, name, value, 
                                      config_type, verbose, device)

    return config(type=config_type)

@command(type=[namedstring(console), namedstring(probe), namedstring(soc), namedstring(core), namedstring(comms)],
         value=[(on, True), (off, False), (enable, True), (disable, False)],
         restore=[namedstring(restoredefaults)],
         device_required=False, verbose=verbosity)
def config(name=None, value=None, type='probe', restore=None, verbose=1, device=None):
    """Gets, sets, or lists settings for the Probe or the Console.
    
    If no type is specified then this command changes settings on the probe. It
    can also change console setting (such as toolkit location) using ::
    
        [s0c0v0] >>> config(console, 'toolkit', '${MIPS_ELF_ROOT}/bin')
    
    The probe has many configurable settings which can be listed and modified 
    with this command.  To obtain a list of config options available call config()
    with no name, in this case the return type is a case insensitive dictionary ::
    
        [s0c0v0] >>> config()
        ===========Global========== ===================MIPS==================
        APB Timeout       0x64      Allow FixedMap Accesses        0x0
        Assert DINT       0x0       Allow KUSEG Accesses           0x0
        ...
        [s0c0v0] >>> _['apb timeout']
        0x64
        
    This list can be quite long, so to narrow the list down specify a few 
    letters of the name to filter the list down::
    
        [s0c0v0] >>> config('monitor')
        ValueError: No config options match 'monitor', could be one of :
        ===============MIPS===============
        Fast Monitor Address    0x80000000
        Force Reload Monitor    0x0
        Lock Monitor in Cache   0x0
        Monitor Command Timeout 0x1f4        
        
    Additionally documentation and interpretation of values is shown when a 
    single config value is read, though the return type is an int::
    
        [s0c0v0] >>> config('fast monitor address')
        Fast Monitor Address = 0x80000000
          Address to which fast transfer monitor is loaded to before it gets locked
          into the cache, this must be a KSEG0 address    
        [s0c0v0] >>> _ & 0xff000000
        0x80000000
              
    By default settings will be applied to all cores::
    
        [s0c0v0] >>> config('fast monitor address', 0xa0000000)
        Fast Monitor Address = 0xa0000000
          Address to which fast transfer monitor is loaded to before it gets locked
          into the cache, this must be a KSEG0 address
          
    Sysprobes, however, support per-core options, for example to set a different
    Fast Monitor Address for all cores in soc0, or for just s0c1 ::

        [s0c0v0] >>> config('fast monitor address', 0x90000000)
        [s0c0v0] >>> config('fast monitor address', 0xa0000000, soc, soc0)
        [s0c0v0] >>> config('fast monitor address', 0xb0000000, core, s0c1)
        [s0c0v0] >>> config('fast monitor')
        ValueError: No config options match 'fast monitor', could be one of :
        ==============MIPS============= ==============Advanced==============
        Fast Monitor Address 0x90000000 fast monitor address.s0c0 0xa0000000
                                        fast monitor address.s0c1 0xb0000000
    
    There is also the possiblilty to restore a previously saved config result.
    Simply set the restore parameter to be your desired saved config result:

        [s0c0v0] >>> config(restore=saved_config)
    
    All the other parameters are ignored (except for device and verbose) and the restored 
    config is of the same type as the one given as parameter. 

    Additionally, default values can be restored by setting the restore parameter
    to restoredefalults:

        [s0c0v0] >>> config(restore=restoredefaults)
    
    The previous example restores the defaults for the default value of 
    the type ('probe'). However, other types can be reset to default too:

         [s0c0v0] >>> config(console, restore=restoredefaults)
         [s0c0v0] >>> config(core, restore=restoredefaults)
    """
    if restore is not None and restore != 'restoredefaults':
        try:
            return _restore_previously_saved_config(restore, device, verbose)
        except Exception:
            raise RuntimeError('The configuration parameter is invalid.')
    elif restore == 'restoredefaults':
        return _restore_default_values(type, verbose, device)

    c = _get_provider(type, device)
    cases = dict([(k.lower(), k) for k in c.list()])
    if name is None or (name.lower() not in cases and value is None):
        names = cases.values()
        if name is not None:
            names = [n for n in names if name.lower() in n.lower()]
            if not names:
                names = get_close_matches(name, cases.values(), 10)
        if not names:
            raise ValueError('No config options match %r'% (name,))
        metas = [c.meta_data(n) for n in names]
        values = [_read_config_or_exception(c, n) for n in names]
        res = _format_config_results(metas, values, type)
        if name is None:
            return res
        raise ValueError('No config options match %r, could be one of :\n%r'% (name,res))

    def doconfig(name, value):
        writer, args = None, None
        if value is not None:
            writer = c.write
            args = [name, c.read(name)]
            c.write(name, value)
        return _format_config_result(c.meta_data(name), c.read(name), type, writer, args)
    name = cases.get(name.lower(), name)
    return doconfig(name, value)
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()