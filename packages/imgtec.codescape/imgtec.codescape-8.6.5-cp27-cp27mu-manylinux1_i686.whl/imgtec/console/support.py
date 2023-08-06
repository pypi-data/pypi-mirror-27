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

import itertools
from imgtec.test import *
from imgtec.lib.format_signature import format_doc
from imgtec.lib import rst
from imgtec.lib.namedenum import namedenum
from imgtec.console.results import _display
from contextlib import contextmanager
from difflib import get_close_matches
import re
import os
import struct
import sys
import linecache
import traceback
import logging as _logging
import warnings
from inspect import getargspec

_console_logger = _logging.getLogger('console')
_ps1 = getattr(sys, 'ps1', '>>> ')
_ps2 = getattr(sys, 'ps2', '--> ')

CoreFamily = namedenum('CoreFamily',
    unknown   = 0,
    hitachi   = 1,
    arm       = 2,
    meta      = 3,
    mcp       = 4,
    mips      = 5,
    x86       = 6,
    gdbserver = 7,
    shader    = 8,
    #mips64    = 9,  # This enum is internal to DAtiny only as it is converted to mips in DAtiny.
    mipscm    = 10,
    custom_register_block = 255,
)    

def negative_to_2s_complement(values, size):
    '''Convert a mixed list of positive and negative numbers into their equivalent
    2s complement value if they are unsigned. Signed numbers pass through as long
    as they fit in the size given.

    >>> '0x%x' % negative_to_2s_complement([-1], 4)[0]
    '0xffffffff'
    >>> ['0x%x' % i for i in negative_to_2s_complement([-2, 10], 2)]
    ['0xfffe', '0xa']
    '''
    if not size:
        raise RuntimeError("Value size cannot be 0 for unsigned number conversion.")

    min_negative = -(2**(size*8-1))
    #Value of the bit 1 beyond the size
    end_value = (2**(size*8))
    #Positive numbers can use all the space
    max_positive = end_value-1
    
    ret = []
    for num in values:
        if not (min_negative <= num <= max_positive):
            raise RuntimeError("Number 0x%x out of range for size of %d byte(s), expected 0x%x <= num <= 0x%x" % (num, size, min_negative, max_positive))
        elif num < 0:
            num = end_value + num
        ret.append(num)
    return ret

def struct_format(length, size, endian, signed=False):
    endian = '<>'[endian]
    f = {1:'B', 2:'H', 4:'I', 8:'Q'}[size]
    return '%s%d%s' % (endian, length, f.lower() if signed else f)

def struct_pack(values, size, endian):
    return struct.pack(struct_format(len(values), size, endian), *values)

def struct_unpack(bytedata, size, endian, signed=False):
    return struct.unpack(struct_format(len(bytedata)//size, size, endian, signed), bytedata)
    
Endian = namedenum("Endian", "little big")

def swap_endian(values, size):
    """Swaps endian of values.

    >>> ['0x%16x' % x for x in swap_endian([0x123456789abcdef1], 8)]
    ['0xf1debc9a78563412']
    >>> ['0x%08x' % x for x in swap_endian([0x11223344], 4)]
    ['0x44332211']
    >>> ['0x%04x' % x for x in swap_endian([0x1122], 2)]
    ['0x2211']
    >>> ['0x%02x' % x for x in swap_endian([0x11], 1)]
    ['0x11']
    """
    return struct_unpack(struct_pack(values, size, True), size, False)
    
def sign_extend_32_to_64(address):
    if address & (1 << 31):
        return address | (0xFFFFFFFF << 32)
    else:
        return address
        
def kwarg_list(f):
    """Get the names of a function's keyword arguments.
    
    >>> kwarg_list(kwarg_list)
    []
    >>> def foo(a, b, c=1, d=None):
    ...    pass
    >>> kwarg_list(foo)
    ['c', 'd']
    """
    t = getargspec(f)
    if t.defaults is not None:
        return t.args[-len(t.defaults):]
    else:
        return []

def _arg_list(f):
    code = f.__code__ if hasattr(f, '__code__') else f.func_code
    args = code.co_varnames[0:code.co_argcount]
    defaults = f.func_defaults or []
    nondefaults = len(args) - len(defaults)
    nodefs = args[0:nondefaults]
    defs = list(zip(args[nondefaults:], defaults))
    return nodefs, defs

def _display_param_value(x):
    if hasattr(x, '__call__') and hasattr(x, '__name__'):
        return x.__name__  # e.g. builtins
    return repr(x)
    
def arg_list(f):
    """Get the argument list of a function or method.

    >>> arg_list(arg_list)
    ['f']
    >>> def some_function(a, b=1, c='x', _d=1, _e=all, *args, **kwargs):
    ...     pass
    >>> arg_list(some_function)
    ['a', 'b=1', "c='x'", '_d=1', '_e=all', '*args', '**kwargs']
    """
    nodefs, defs = _arg_list(f)
    code = f.__code__ if hasattr(f, '__code__') else f.func_code
    strs = list(nodefs)
    strs.extend(n + "=" + _display_param_value(x) for n, x in defs)
    i = code.co_argcount
    if code.co_flags & 4:
        strs.append("*" + code.co_varnames[i])
        i += 1
    if code.co_flags & 8:
        strs.append("**" + code.co_varnames[i])
        i += 1
    return strs
    
def _device_is_last_if_present(f):
    '''
    
    >>> def firstandlast(device=None):
    ...     pass
    >>> _device_is_last_if_present(firstandlast)
    True
    >>> def first(device=None, other=False):
    ...     pass
    >>> _device_is_last_if_present(first)
    False
    >>> def last(other=False, device=None):
    ...     pass
    >>> _device_is_last_if_present(last)
    True
    >>> def kwargs(device=None, **kwargs):
    ...     pass
    >>> _device_is_last_if_present(kwargs)
    True
    >>> def nodevice():
    ...     pass
    >>> _device_is_last_if_present(nodevice)
    True
    '''
    _nodefs, defs = _arg_list(f)
    defs = [x[0] for x in defs]
    return 'device' not in defs or defs.index('device') == len(defs)-1
    

def format_arg_list(f):
    """Format the argument list of a function or method. Will hide arguments that starts with at least 2 underscores.

    >>> format_arg_list(format_arg_list)
    'f'
    >>> def some_function(a, b=1, c='x', *args, **kwargs):
    ...     pass
    >>> format_arg_list(some_function)
    "a, b=1, c='x', *args, **kwargs"
    >>> def some_function(a, __a, _b, _c, __hide, _dd='x'):
    ...     pass
    >>> format_arg_list(some_function)
    "a, _b, _c, _dd='x'"
    """
    return ", ".join(a for a in arg_list(f) if not a.startswith("__"))


def _flatten_named_params(named):
    return [(kw, v, obj) for kw, vals in named.items() for obj, v in vals]


def precompile_named_params(named):
    """Reorganise the named_params to make them easier to process.

    Changes the dict(kw=[(global, value)]) order into a
    dict(id(global)=(kw, value)
    """
    return dict([(id(obj),(kw, v)) for kw, v, obj in _flatten_named_params(named)])

@test
def test_precompile_named_params():
    dec = object()
    byte = object()
    word = object()
    named = dict(radix=[(dec, 10), (hex, 16)],
               size=[(byte, 1), (word, 2)])
    pre = precompile_named_params(named)
    assertEquals(('radix', 10), pre[id(dec)])
    assertEquals(('radix', 16), pre[id(hex)])
    assertEquals(('size', 1), pre[id(byte)])
    assertEquals(('size', 2), pre[id(word)])

def _format_named_params(named_params):
    flat = _flatten_named_params(named_params)
    rows = []
    for (kw, v), objs in itertools.groupby(flat, lambda x: x[0:2]):
        rows.append((','.join(obj[2].__name__ for obj in objs), '%s=%s' % (kw, _display_param_value(v))))
    return rows
    
def _list_named_params(named_params):
    flat = _flatten_named_params(named_params)
    named = []
    for (_kw, _v), objs in itertools.groupby(flat, lambda x: x[0:2]):
        named.extend(obj[2].__name__ for obj in objs)
    return named

@test 
def test_format_named_params():
    class Named(object):
        pass
    dec = Named()
    dec.__name__ = 'dec'
    decimal = Named()
    decimal.__name__ = 'decimal'
    named = dict(radix=[(dec, 10), (decimal, 10), (hex, 16)])
    rows = _format_named_params(named)
    assertEquals([
        ('dec,decimal', 'radix=10'),
        ('hex', 'radix=16'),
    ], rows)


def decode_named_params(argnames, named_params, args, kwargs):
    """Unpack and remove any named params, moving them to kwargs
    or the correct location in args as appropriate.

    >>> dec=object()
    >>> named = dict(radix=[(dec, 10), (hex, 16)])
    >>> argnames = 'a b radix'.split()
    >>> decode_named_params(argnames, named, ['a', 'b'], dict(x=1))
    (['a', 'b'], {'x': 1})
    >>> decode_named_params(argnames, named, ['a', dec, 'b'], {})
    (['a', 'b', 10], {})
    >>> decode_named_params(argnames, named, ['a', dec], {})
    (['a'], {'radix': 10})
    >>> decode_named_params(argnames, named, ['a'], {'radix':10})
    (['a'], {'radix': 10})
    >>> decode_named_params(argnames, named, ['a'], {'radix':dec})
    (['a'], {'radix': 10})
    >>> decode_named_params('radix a'.split(), named, [dec, 'a'], {})
    ([10, 'a'], {})
    >>> decode_named_params(argnames, named, [dec, hex], {})
    Traceback (most recent call last):
    ...
    SyntaxError: keyword argument 'radix' repeated
    """
    ret = []
    retkw = {}
    allids = precompile_named_params(named_params)
    for arg in args:
        try:
            kw, value = allids[id(arg)]
        except KeyError:
            ret.append(arg)
        else:
            if kw in retkw or kw in kwargs:
                raise SyntaxError("keyword argument '%s' repeated" % (kw,))
            retkw[kw] = value
    for name, value in kwargs.items():
        try:
            kw, value = allids[id(value)]
            kwargs[name] = value
        except KeyError:
            pass
            
    for kw, value in retkw.items():
        try:
            pos = argnames.index(kw)
        except ValueError:
            pass
        else:
            if pos <= len(ret):
                ret.insert(pos, value)
                del retkw[kw]
    retkw.update(kwargs)
    return ret, retkw


def configurable_defaults(argnames, defaults, args, kwargs):
    """Allow the defaults of a function to be runtime configurable, by
    manipulating args and kwargs and looking up missing entries in the dict
    `defaults`.  argnames should be a list of the arguments for a fn.`

    >>> argnames = ['arg1', 'arg2', 'arg3']
    >>> defaults = dict(arg2=4, arg3=None)

    >>> configurable_defaults(argnames, defaults, [1, 2, 3], {})
    ([1, 2, 3], {})
    >>> configurable_defaults(argnames, defaults, [1], {})
    ([1, 4, None], {})

    >>> configurable_defaults(argnames, defaults, [], {})
    ([], {})
    >>> configurable_defaults(argnames, defaults, [], dict(arg1=1))
    ([1, 4, None], {})
    >>> defaults['arg2'] = 8
    >>> configurable_defaults(argnames, defaults, [1], {})
    ([1, 8, None], {})

    >>> configurable_defaults(argnames, defaults, [1], dict(arg2=2))
    ([1, 2, None], {})
    >>> configurable_defaults(argnames, defaults, [1], dict(arg1=2))
    ([1, 8, None], {'arg1': 2})
    >>> configurable_defaults(argnames, defaults, [1], dict(arg1=2, arg2=42))
    ([1, 42, None], {'arg1': 2})
    >>> defaults['arg1'] = 42
    >>> configurable_defaults(argnames, defaults, [1], dict(arg2=2))
    ([1, 2, None], {})
    >>> configurable_defaults(argnames, defaults, [], dict(arg2=2))
    ([42, 2, None], {})
    """
    # here we are basically reimplementing the python argument unpacking, but
    # taking defaults from defaults instead of the default params
    newargs, newkwargs = [], kwargs.copy()
    missing = object()
    for argname, arg in itertools.izip_longest(argnames, args, fillvalue=missing):
        if arg is missing:
            try:
                arg = newkwargs.pop(argname)
            except KeyError:
                try:
                    arg = defaults[argname]
                except KeyError:
                    break
        newargs.append(arg)
    return newargs, newkwargs

class Device(object):
    def __init__(self, name='device'):
        self.name = name
    def get_names(self):
        names = [self.name]
        if self.probe.tap_index != -1 and self.probe.ir_lengths:
            names.append('tap %d of %d active' %  (self.probe.tap_index, len(self.probe.ir_lengths)))
        return names
    def __repr__(self):
        return self.name
    def __enter__(self):
        self._old_device = Command.current and Command.current.device
        if Command.current:
            Command.current = self.probe
            Command.current.device = self
        return self
    def __exit__(self, *exc):
        if self._old_device and Command.current:
            Command.current = self._old_device.probe
            Command.current.device = self._old_device 

def extract_device(argnames, args, kwargs, default):
    """Find a Device instance in args or kwargs and put it in the kwargs, and 
    if not found then set it to default.
    
    If devices is in the argnames then allow multiple and assign it as a list 
    in kwargs['devices'].
    
    Returns (args, kwargs, explicit_device)
    
    Where explicit_device is None if the default was used

    >>> default, other, third = Device('default'), Device('other'), Device('third')

    >>> extract_device(['arg1'], [], {}, default)
    ([], {}, None)
    >>> extract_device(['device'], [], {}, default)
    ([], {'device': default}, None)
    >>> extract_device(['device'], [], {'device': other}, default)
    ([], {'device': other}, other)
    >>> extract_device(['device'], [other], {}, default)
    ([], {'device': other}, other)
    >>> extract_device(['devices'], [other, third], {}, default)
    ([], {'devices': [other, third]}, other)
    >>> extract_device(['device'], [other, third], {}, default)
    Traceback (most recent call last):
    ...
    ValueError: This command does not support multiple devices
    >>> extract_device(['devices'], [], {'devices':[]}, default)
    ([], {'devices': [default]}, None)
    >>> extract_device(['devices'], [], {'devices':[other, third]}, default)
    ([], {'devices': [other, third]}, other)
    
    # Check that explicit device= still works because go/halt/step used to accept device=
    >>> extract_device(['devices'], [], {'device':other}, default)
    ([], {'devices': [other]}, other)
    
    >>> extract_device(['device'], [], {}, None)
    ([], {'device': None}, None)
    >>> extract_device(['devices'], [], {}, None)
    ([], {'devices': []}, None)
    

    """
    explicit_device = None
    if 'device' in argnames:
        found = [x for x in args if isinstance(x, Device)]
        if found:
            if len(found) > 1:
                raise ValueError('This command does not support multiple devices')
            args = [x for x in args if not isinstance(x, Device)]
            kwargs['device'] = found[0]
            explicit_device = found[0]
        elif kwargs.get('device'):
            explicit_device = kwargs['device']
        else:
            kwargs['device'] = default
    if 'devices' in argnames:
        found = [x for x in args if isinstance(x, Device)]
        if found:
            args = [x for x in args if not isinstance(x, Device)]
            kwargs['devices'] = found
            explicit_device = found[0]
        elif kwargs.get('devices'):
            explicit_device = kwargs['devices'][0]
        elif kwargs.get('device'):
            explicit_device = kwargs.pop('device')
            kwargs['devices'] = [explicit_device]
        else:
            kwargs['devices'] = [default] if default else []            
    return args, kwargs, explicit_device
    
def _expand_device(device):
    '''Expand a single device into all of it's vpe devices.
    
    >>> core0, core1 = Device('s0c0'), Device('s0c1')
    >>> core0.vpes = [Device('s0c0v0'), Device('s0c0v1')]
    >>> core1.vpes = [Device('s0c1v0'), Device('s0c1v1')]
    >>> soc = Device('soc0')
    >>> soc.cores = [core0, core1]
    >>> _expand_device(soc)
    [s0c0v0, s0c0v1, s0c1v0, s0c1v1]
    >>> _expand_device(core0)
    [s0c0v0, s0c0v1]
    >>> _expand_device(core0.vpes[0])
    [s0c0v0]
    
    '''
    require_vpe(device)
    if hasattr(device, 'cores'):
        return list(itertools.chain.from_iterable(core.vpes for core in device.cores))
    elif hasattr(device, 'vpes'):
        return device.vpes
    else:
        return [device]

def expand_devices(devices):
    '''Expand a list of devices into all of their vpe devices.'''
    return list(itertools.chain.from_iterable(_expand_device(d) for d in devices))            
    
class ReadLineCompleter(object):
    """Convert a simple function into a readline completer, handling the state 
    param, and instead of text passes readline's get_line_buffer/begidx/endidx.
    """
    def __init__(self, f, readline):
        self.f = f
        self.rl = readline
    
    def __call__(self, _, state):
        if state == 0:
            self.matches = self.f(self.rl.get_line_buffer(), self.rl.get_begidx(), self.rl.get_endidx())
        return self.matches[state]

class Completer(object):
    """Completer for use with ReadLineCompleter class to look up cmds
    and args on tab press."""
    def __init__(self, cmds):
        self.cmds = cmds
    def __call__(self, line, begin, end):
        text = line[begin:end].lower()
        cmd, paren, _args = line.partition('(')
        kwargs = []
        if paren:
            add_paren = False
            if cmd in ('help', 'cmdall', 'tapall'):
                src = self.cmds.keys()
                if cmd == 'cmdall':
                    src.append('devices=')
            else:
                try:
                    c = self.cmds[cmd]
                    src = [obj.__name__ for _kw, _v, obj in _flatten_named_params(c._named_params)]
                    kwargs = [kw for kw in c._kwarg_list if not kw.startswith('_')]
                except KeyError:
                    src= []
        else:
            add_paren = True
            src = self.cmds.iterkeys()
            
        #Separate matches to account for kwargs with the same name as a named arg
        general_matching = [s for s in src if s.lower().startswith(text)]
        kwarg_matching   = [s for s in kwargs if s.lower().startswith(text)]
        
        ret = [match + '(' if add_paren else match for match in general_matching]
        ret.extend([match + '=' for match in kwarg_matching])
        
        return sorted(ret)

def prefix_lines(s, prefix):
    r"""Prefix all lines in s with prefix.
    
    >>> prefix_lines('a\nb\nc', '> ')
    '> a\n> b\n> c'
    """
    return "\n".join(prefix + x for x in s.split('\n'))

def strip_rst_inline_roles(s):
    r"""Remove all rst inline roles.

    >>> strip_rst_inline_roles('hello :adj:`cruel` world')
    'hello cruel world'
    >>> strip_rst_inline_roles('hello :adj:`~thing` world')
    'hello thing world'
    """
    return re.sub(r'\:\w+\:`~?([^`]+)`', r'\1', s)
    
def require_device(device):
    """Raise an exception if device is None"""
    if not device:
        raise RuntimeError("No probe configured, please use the probe command")
        
def require_vpe(device):
    """Raise an exception if there is not at least one vpe accessible.
    
    Returns the first vpe on the given device (or the vpe itself if given a vpe).
    """
    require_device(device)
    
    if getattr(device, 'mode', '') == 'uncommitted':
        raise RuntimeError('''\
The probe is in uncommitted mode - it has not discovered the target yet.
Use autodetect to discover the target or targetdata to configure the probe''')
    if getattr(device, 'mode', '') == 'failed-autodetection':
        raise RuntimeError('''\
The probe failed to autodetect the target. Enable logging(probe, on) and call
autodetect again.''')

    if hasattr(device, 'cores'): # probe or soc given
        if not device.cores:
            raise RuntimeError('There are no debuggable cores at present')
        device = device.cores[0]
    if hasattr(device, 'vpes'):
        if not device.vpes:
            raise RuntimeError('There are no debuggable thread present')
        return device.vpes[0]
    return device
    
def _farg(arg):
    '''Format an argument for display, replacing devices with s0c0v0 names'''
    if isinstance(arg, Device):
        return arg.name
    elif isinstance(arg, Command):
        return arg.__name__
    elif isinstance(arg, str):
        return repr(arg)
    else:
        return _display(arg)

def _get_calling_loc(upframes = 1):
    try:
        f = sys._getframe(upframes+1)
        lineno = f.f_lineno
        co = f.f_code
        filename = co.co_filename
        if filename == '<console>':
            from imgtec.console.main import get_current_lines
            return get_current_lines()
        return [linecache.getline(filename, lineno, f.f_globals).rstrip()]
    except AttributeError:
        return [''] # not all implementations of python support _getframe

@contextmanager
def _current_device_modifier(explicit_device, cmdname):
    if explicit_device:
        old = Command.get_device()
        Command.set_device(explicit_device)
    try:
        yield
    finally:
        if explicit_device and cmdname != 'device':
            # If the command didn't change the current device then restore it
            Command.set_device(old)

class Command(object):
    """

    >>> def f(arg1, arg2=4, arg3=None):
    ...     '''doc'''
    ...     print arg1, arg2, arg3

    >>> cmd = Command(f)
    >>> cmd(1, 2, 3)
    1 2 3
    >>> cmd(1)
    1 4 None
    >>> cmd()
    Traceback (most recent call last):
    ...
    TypeError: f() takes at least 1 argument (0 given)
    >>> cmd.arg2=8
    >>> cmd(1)
    1 8 None
    >>> cmd(1, arg2=16)
    1 16 None
    >>> cmd(1, arg1=16)
    Traceback (most recent call last):
    ...
    TypeError: f() got multiple values for keyword argument 'arg1'
    >>> cmd.arg1 = 42
    >>> cmd()
    42 8 None
    >>> cmd.arg1
    42
    >>> cmd.arg7
    Traceback (most recent call last):
    ...
    AttributeError: 'Command' object has no attribute 'arg7'
    """
    current = None
    _commands = {}
    _named_args = {}
    _namespace = None
    _call_depth = 0 # how many commands are currently in the stack
    _interactive = False
    '''Set to True when codescape console is being used as a REPL.'''

    @classmethod
    def set_device(cls, device):
        if device:
            cls.current = device.probe
            cls.current.device = device
        else:
            cls.current = None
        
    @classmethod
    def get_device(cls):
        return cls.current and cls.current.device
        
    @classmethod
    def get_probe(cls):
        return cls.current
        
    @staticmethod
    def _sorted_commands():
        """Return a list of commands sorted by name, aliases are not included."""
        unique = set(Command._commands.values())
        return sorted(unique, key=lambda x: x.__name__)
        
    @staticmethod
    def get_namespace():
        if Command._namespace is None:
            Command._namespace = {}
        return Command._namespace
        
    @staticmethod
    def get_globals():
        names = []
        for ns in [Command._commands, Command._named_args]:
            names.extend([k for k, v in ns.iteritems() if type(v) is not type(all)])
        return names
        
    def __init__(self, f, see='', aliases='', device_required=True, vpe_required=False, named_params=None):
        if named_params is None:
            named_params = {}
            
        self._aliases = aliases.split()
        self.__name__ = f.__name__
        self._doc = format_doc(f.__doc__ or '')
        self._see = see
        if see:
            other = Command._commands[see]
            other._commands_which_see.append(self)
        self._commands_which_see = []
        self._f = f
        self._arg_list = format_arg_list(f)
        if not _device_is_last_if_present(f):
            warnings.warn('device argument should be last if present', stacklevel=3)
        self._kwarg_list = kwarg_list(f)
        self._named_params = named_params
        nodefs, defs = _arg_list(self._f)
        self._argnames = list(nodefs) + [name for name, _default in defs]
        self._defaults = dict(defs)
        self._device_required = device_required
        self._vpe_required = vpe_required
        ns = Command.get_namespace()
        ns[self.__name__] = self
        for shortcut in self._aliases:
            ns[shortcut] = self
            
        if 'exit' not in __builtins__ and self.__name__ == 'quit':
            # when frozen builtin-exit() is not available, add it back here
            ns['exit'] = self
            
        if self.__class__._interactive: 
            # when import is called in an interpreter, print any new commands
            print self.short_help()            
            
    @property
    def supports_multiple_devices(self):
        return 'devices' in self._argnames
    
    def __setattr__(self, attr, value):
        if attr.startswith('_'):
            super(Command, self).__setattr__(attr, value)
        else:
            self._defaults[attr] = value

    def __getattr__(self, attr):
        try:
            return self._defaults[attr]
        except KeyError:
            raise AttributeError("'%s' object has no attribute '%s'" %
                        (self.__class__.__name__, attr))

    def __repr__(self):
        return self.short_help()
        
    def short_help(self):
        namedparams = ''
        if self._named_params:
            namedparams = '\nNamed: ' + ', '.join(_list_named_params(self._named_params))
        return self.definition(False) + '\n       ' + self.short_doc(False) + namedparams

    def __call__(self, *args, **kwargs):
        Command._call_depth += 1
        logit = Command._call_depth == 1 and _console_logger.isEnabledFor(_logging.INFO)
        if logit:
            lines = _get_calling_loc(1)
            line0, lines = lines[0], lines[1:]
            lines = [_ps1 + line0] + [_ps2 + line for line in lines]
            if _console_logger.isEnabledFor(_logging.DEBUG):
                allargs = [_farg(arg) for arg in args]
                allargs += ['%s=%s' % (k, _farg(v)) for k, v in kwargs.items()]
                prefix = '-> '.rjust(len(_ps1))
                lines.append('%s%s(%s)' % (prefix, self.__name__, ', '.join(allargs)))
            _console_logger.info('\n'.join(lines))

        try:
            args, kwargs, explicit = extract_device(self._argnames, args, kwargs, self.get_device())
            if 'device' in kwargs and self._device_required and kwargs['device'] is None:
                require_device(None)
            if 'devices' in kwargs and self._device_required and kwargs['devices'] == []:
                require_device(None)
            if self._vpe_required:
                kwargs['device'] = require_vpe(kwargs['device'])
            if self.supports_multiple_devices:
                kwargs['devices'] = expand_devices(kwargs['devices'])
                                
            with _current_device_modifier(explicit, self.__name__):
                args, kwargs = decode_named_params(self._argnames, self._named_params, args, kwargs)
                args, kwargs = configurable_defaults(self._argnames, self._defaults, args, kwargs)
                try:
                    res = self._f(*args, **kwargs)
                finally: 
                    if self.current and self.__name__ not in ('quit', 'help', 'logging'):
                        self.current.on_each_command()
                if logit and res is not None:
                    _console_logger.info(repr(res))
                return res
        except Exception as e:
            if logit:
                _console_logger.error(repr(e))
                
            raise
        finally:
            Command._call_depth -= 1
                
    def short_doc(self, is_rst=False):
        lnk = (lambda x: ':func:`%s`' % x) if is_rst else (lambda x: x)
        doc = self._doc.split('\n', 1)[0]
        if self._see:
            doc = 'See %s command.' % (lnk(self._see),)
        return doc if is_rst else strip_rst_inline_roles(doc)
        
    def oneliner(self, colwidth=0, is_rst=False, absolute=False):
        if is_rst and absolute:
            lnk  = lambda x: ':func:`~imgtec.console.%s`' % x
        elif is_rst:
            lnk  = lambda x: ':func:`%s`' % x
        else:
            lnk  = lambda x: x
        doc = self.short_doc(is_rst)
        doc = '%s %s' % (lnk(self.__name__).ljust(colwidth), doc)
        return doc if is_rst else strip_rst_inline_roles(doc)
        
    def definition(self, is_rst=False):
        return '%s(%s)' % (self.__name__, self._arg_list)
        
    def help(self, is_rst=False):
        name = (lambda x: '**%s**' % x)     if is_rst else (lambda x: x)
        lnk  = (lambda x: ':func:`%s`' % x) if is_rst else (lambda x: x)
        doc = self._doc
        fn = '.. function:: ' if is_rst else ''
        defns = [fn + self.definition(is_rst)]
        if self._see:
            doc = 'See %s command.' % (lnk(self._see),)
        else:
            fn = ' ' * len(fn)
            defns.extend(fn + x.definition(is_rst) for x in self._commands_which_see)
            
        aliases = ''
        if self._aliases and not self._see:
            pl = ''
            if len(self._aliases) == 1:
                aliases = name(self._aliases[0])
            elif len(self._aliases) == 2:
                pl = 'es'
                aliases = '%s and %s' % tuple(self._aliases)
            else:
                pl = 'es'
                aliases = ', '.join(name(x) for x in self._aliases[:-1])
                aliases += ', and ' + self._aliases[-1]
            aliases = '\n\nThe alias%s %s can be used for %s.' % (pl, aliases, name(self.__name__))

        namedparams = ''
        if self._named_params:
            namedparams = '\n\nThe following named parameters can be used with this command:\n\n'
            rows = _format_named_params(self._named_params)
            namedparams += rst.simple_table(['Parameter', 'Equivalent To'], rows)

        indent = '    ' if is_rst else ' '
        doc         = prefix_lines(doc, indent)
        namedparams = "\n".join(indent + x for x in namedparams.split('\n'))
        aliases = "\n".join(indent + x for x in aliases.split('\n'))
        if not is_rst:
            doc = strip_rst_inline_roles(doc)

        return "%s\n\n%s%s%s\n" % ('\n'.join(defns), doc, namedparams, aliases)

def command(aliases='', see='', device_required=True, vpe_required=False, **named_params):
    """A decorator to define a new command.

    `aliases` is a string of whitespace separated aliases that can be used
    to call this command besides the function name.

    The command should return a type that has a __repr__ or None to indicate
    that no output should be printed.  see :mod:`imgtec.console.results` for
    types that can be formatted nicely but still be used in a scripting 
    environment.

    The docstring is used for the help command.  The first line of the
    docstring should be a summary, (like in this docstring) the rest of the
    command should add more details such as parameters.  The function
    signature should not be included as that will be automatically
    generated including default parameters.
    
    If the command has a `device` parameter it should have a default value
    of None and the command system will replace it with the current device
    or the given one if specified.  Additionally, if command has a device
    parameter and `device_required` is True then an exception will be 
    raised if no device is currently available, thus the command's body
    should not check for a device of None.

    The parameters can have default values which can be of any type.

    For an example see :ref:`writing-commands`.

    """
    def decorator(f):
        if not f.__doc__ and not see:
            raise RuntimeError(f.__name__ + " requires documentation")
        cmd = Command(f, see, aliases, device_required, vpe_required, named_params)
        Command._commands[cmd.__name__] = cmd
        for shortcut in cmd._aliases:
            Command._commands[shortcut] = cmd
        return cmd
    return decorator

class Named(object):
    def __repr__(self):
        return self.__name__

def named(name=None, o=None):
    if o is None:
        o = Named()
        if name is None:
            raise RuntimeError("Can't have no name if o is not given")
        o.__name__ = name
    if name is None:
        name = o.__name__
    if name in Command._named_args:
        print "warning", name, " already in named_args"
    Command._named_args[name] = o
    Command.get_namespace()[name] = o
    return o
    
def namedstring(o):
    return o, o.__name__

binary    = named('binary')  # we allow pythons oct and bin as well as the longer binary,octal
octal     = named('octal')
decimal   = named('decimal')
udecimal  = named('udecimal')
radixes   = [(bin, 2), (binary, 2), (oct, 8), (octal, 8), (decimal, -10), (udecimal, 10), (hex, 16)]
named_all = namedstring(all)
auto      = named("auto")
little    = named('little')
big       = named('big')
endians   = [namedstring(auto), namedstring(little), namedstring(big)]
mips16    = named("mips16")
mips16e2  = named("mips16e2")
mips32    = named("mips32")
mips32r6  = named("mips32r6")
micromips = named("micromips")
micromips64 = named("micromips64")
micromipsr6 = named("micromipsr6")
micromips64r6 = named("micromips64r6")
mips64 = named("mips64")
mips64r6 = named("mips64r6")
named_isas = [  namedstring(mips16), 
                namedstring(mips16e2), 
                namedstring(mips32), 
                namedstring(mips32r6), 
                namedstring(micromips),
                namedstring(micromips64),
                namedstring(micromipsr6),
                namedstring(micromips64r6),
                namedstring(mips64),
                namedstring(mips64r6),
                namedstring(auto)]
update   = named('update')
noupdate = named('noupdate')
updates  = [(update, True), (noupdate, False)]
verify   = named('verify')
noverify = named('noverify')
verifyraise = named('verifyraise')
verifies = [(verify, True), (noverify, False), (verifyraise, 2)]
verbose   = named('verbose')
veryverbose   = named('veryverbose')
quiet     = named('quiet')
verbosity= [(quiet, 0), (verbose, 1), (veryverbose, 2)]
enable = named('enable')
disable = named('disable')
console = named('console')
comms = named('comms')
jtag = named('jtag')
on = named('on')
off = named('off')
restoredefaults    = named('restoredefaults')
normalboot    = named('normalboot')
ejtagboot     = named('ejtagboot')
tap_async     = named('tap_async')
tap_sync      = named('tap_sync')
soft          = named('soft')
hard_auto     = named('hard_auto')
hard_halt     = named('hard_halt')
hard_run      = named('hard_run')
hard_all_halt = named('hard_all_halt')
hard_all_run  = named('hard_all_run')


def eval_address(device, address):
    try:
        return int(address, 0)
    except TypeError:
        return address
    except ValueError:
        pass
    try:
        device = require_vpe(device)
    except RuntimeError:
        raise RuntimeError("There are no debuggable cores at present and one is required to evaluate %r" % (address,))
    if address.startswith('$'):
        address = address[1:]
        return device.da.ReadRegister(address)
    try:
        return device.objfile.lookup_name_in_all_scopes(address)[0].symbol().value()
    except Exception:
        return device.da.ReadRegister(address)

connectors = []

def register_connector(pattern, flags=0):
    regex = re.compile(pattern, flags)
    def registrar(connector):
        connectors.append((regex, connector))
        return connector
    return registrar
    
def format_exception(etype, einst):
    if issubclass(etype, NameError):
        name = re.match(r"[^']+'([^']+)'", str(einst))
        if name:
            name = name.group(1)
            matches = get_close_matches(name, Command.get_namespace().keys(), 10)
            if len(matches) == 1:
                einst = etype(str(einst) + '. Did you mean ' + ', '.join(matches) + '?')
            elif matches:
                einst = etype(str(einst) + '. Did you mean one of ' + ', '.join(matches) + '?')
    return ''.join(traceback.format_exception_only(etype, einst)).strip()

def check_if_name_error(etype, einst):
    if issubclass(etype, NameError):
        name = re.match(r"[^']+'([^']+)'", str(einst))
        if name:
            name = name.group(1)
            matches = get_close_matches(name, Command.get_namespace().keys(), 10)
            if len(matches) == 1:
                einst = etype(str(einst) + '. Did you mean ' + ', '.join(matches) + '?')
            elif matches:
                einst = etype(str(einst) + '. Did you mean one of ' + ', '.join(matches) + '?')
    
    return etype, einst

def display_current_exception():
    etype, einst, tb = sys.exc_info()
    etype, einst = check_if_name_error(etype, einst)

    levels = []
    while tb:
        name = tb.tb_frame.f_globals.get('__name__')
        if name not in ['code', None] and \
            not name.startswith(('imgtec.', 'bitfield_result_', 'namedstruct_', 'namedenum_')):
            levels.extend(traceback.format_tb(tb,1))
        tb = tb.tb_next

    if levels:
        levels.insert(0, 'Traceback (most recent call last):\n')
        
    exc_str = traceback.format_exception_only(etype, einst)
    # Comma to prevent an extra newline when Console prints the next '[s0c0v0] >>>'
    print ''.join(levels + exc_str).rstrip(),

def report_exception(msg=None):
    '''Report an exception to the user.
    
    If config(console, 'traceback') is on then the full traceback is displayed.
    Otherwise display the exception itself.
    '''
    from imgtec.console.cfg import console_config
    if console_config.traceback:
        traceback.print_exc()
    elif not msg:
        display_current_exception()
    if msg:
        print msg


class AddressRangeType(object):
    '''Defines a range of addresses as the semi-open interval [begin, end).
    Addresses start at begin and the last address is end - 1 with the proviso
    that begin < end. If this condition is not satisfied then an empty range
    (size of zero) starting at begin is created.
    
    Note: AddressRangeTypes are intended to be fixed with the only operation
    that can change the range being "rebasing" to a new start address (the size
    is preserved).
    
    >>> r = AddressRangeType(0x10000000, 0x10001000)
    >>> repr(r)
    "AddressRangeType(0x10000000, 0x10001000, '')"
    >>> r.empty
    False
    >>> r.contains(0x10000000)
    True
    
    >>> r = AddressRangeType(0x10000000, 0x0fffffff)
    >>> r.size
    0
    >>> repr(r)
    "AddressRangeType(0x10000000, 0x10000000, '')"
    >>> r.empty
    True
    >>> r.contains(0x10000000)
    False
    
    >>> r = AddressRangeType(0x10000000, 0x10001000)
    >>> r.rebase(0x01000000)
    >>> repr(r)
    "AddressRangeType(0x01000000, 0x01001000, '')"
    >>> r.contains(0x01000001)
    True
    >>> r.contains(0x01000fff)
    True
    >>> r.contains(0x10000fff)
    False

    >>> r = AddressRangeType(0x80200000, 0x80500000)
    >>> repr(r)
    "AddressRangeType(0x80200000, 0x80500000, '')"
    >>> r.empty
    False
    >>> r.contains(0x80300000)
    True
    >>> r.contains(0x80500000)
    False
    >>> r.contains(0x801fffff)
    False
    '''
    
    def __init__(self, begin, end, is64bit=False, name=''):
        self.name = name
        self.ndigits = 16 if is64bit else 8
        if begin <= end:
            self.__begin = begin
            self.__end = end
        else:
            self.__begin = begin
            self.__end = begin
            
    @property
    def begin(self):
        return self.__begin
        
    @property
    def end(self):
        return self.__end
            
    @property
    def size(self):
        return self.end - self.begin
        
    @property
    def empty(self):
        return self.size == 0
        
    def rebase(self, newbegin):
        size = self.size
        self.__end = newbegin + size
        self.__begin = newbegin
        
    def contains(self, address):
        return (self.begin <= address) and (address < self.end)
        
    def __repr__(self):
        return "AddressRangeType(0x%0*x, 0x%0*x, '%s')" % (self.ndigits, self.begin, self.ndigits, self.end, self.name)


def parse_memblock_size(stack_size):
    '''
    >>> parse_memblock_size('1K')
    1024
    >>> parse_memblock_size('1k')
    1024
    >>> parse_memblock_size('4K')
    4096
    >>> parse_memblock_size('1M')
    1048576
    >>> parse_memblock_size('3M')
    3145728
    >>> parse_memblock_size(0x1000)
    4096
    >>> parse_memblock_size(1024)
    1024
    >>> parse_memblock_size('xxx')
    0
    >>> parse_memblock_size(1.5)
    0
    '''
    try:
        if isinstance(stack_size, basestring):
            posK = stack_size.upper().find('K')
            posM = stack_size.upper().find('M')
            if (posK > 0) or (posM > 0):
                blk_size = 1024 if posK > 0 else 1048576
                num_blks = int(stack_size[:posK if posK != -1 else posM], 10)
                return num_blks * blk_size
            elif (posK == -1) and (posM == -1):
                for base in (10, 16):
                    try:
                        return int(stack_size, base)
                    except Exception:
                        pass
        elif isinstance(stack_size, (int, long)):
            return stack_size
    except Exception:
        pass
    return 0
    
def parse_memory_descriptor(descr):
    '''
    Returns a tuple from a memory descriptor.
    The tuple is of the form (address_range, memtype).
    address_range is of type AddressRangeType
    memtype is a positive integer defaulting to 0 (ram)
    
    Size and start are required:
        '4k@0x80000000'
    Then either type and name, or just name:
        '4k@0x80000000@1'
        '4k@0x80000000@1@RAM'
        '4k@0x80000000@RAM'
       
    >>> parse_memory_descriptor('4K@0x10000000')
    (AddressRangeType(0x10000000, 0x10001000, ''), 0)
    >>> parse_memory_descriptor('4K')
    Traceback (most recent call last):
    ...
    RuntimeError: Invalid memory descriptor '4K': Not enough parts for descriptor.
    >>> parse_memory_descriptor('K@0x10000000')
    Traceback (most recent call last):
    ...
    RuntimeError: Invalid memory descriptor 'K@0x10000000': Cannot have an empty memory range.
    >>> parse_memory_descriptor('4K@010000000')
    (AddressRangeType(0x10000000, 0x10001000, ''), 0)
    >>> parse_memory_descriptor('1M@0x10000000@1')
    (AddressRangeType(0x10000000, 0x10100000, ''), 1)
    >>> parse_memory_descriptor('4096@0x10000000@1')
    (AddressRangeType(0x10000000, 0x10001000, ''), 1)
    >>> parse_memory_descriptor('4095@0x10000000@1')
    (AddressRangeType(0x10000000, 0x10000fff, ''), 1)
    >>> parse_memory_descriptor('4095@0x10000000@0x1')
    (AddressRangeType(0x10000000, 0x10000fff, ''), 1)
    >>> parse_memory_descriptor('4095@0x10000000@0b101')
    (AddressRangeType(0x10000000, 0x10000fff, ''), 5)
    >>> parse_memory_descriptor('0x1000@0x10000000@1')
    (AddressRangeType(0x10000000, 0x10001000, ''), 1)
    >>> parse_memory_descriptor('0x1000@0x10000000@1@ram')
    (AddressRangeType(0x10000000, 0x10001000, 'ram'), 1)
    >>> parse_memory_descriptor('0x1000@0x10000000@ram')
    (AddressRangeType(0x10000000, 0x10001000, 'ram'), 0)
    '''
    mem_parts = descr.split('@')
    try:
        if len(mem_parts) >= 2:
            mem_size = parse_memblock_size(mem_parts[0])
            if not mem_size:
                raise RuntimeError('Cannot have an empty memory range.')
            
            begin = int(mem_parts[1], 16)
            
            mem_type = 0
            name = ''
            if len(mem_parts) >= 3:
                try:
                    mem_type = int(mem_parts[2], 0)
                except ValueError:
                    name = mem_parts[2]
                else:
                    if len(mem_parts) >= 4:
                        name = mem_parts[3]
            
            return AddressRangeType(begin, begin + mem_size, name=name), mem_type
        else:
            raise RuntimeError('Not enough parts for descriptor.')
    except Exception as e:
        raise RuntimeError("Invalid memory descriptor '%s': %s" % (descr, str(e)))

class ListDict(list):
    '''
    A list which can be used like a dictionary. Assumes that the keys are strings
    and that the values are not strings. 
    Init/insert/append/extend act like a dictionary and require key/value pairs.
    Iterating over it gives the values, keys come from .keys() like a dict.
    
    Assign/get can be done with keys or list indexes. l['f'], l[0], l[:] etc.
    
    >>> l = ListDict([('cat', 7), ('dog', 8)])
    >>> list(l)
    [7, 8]
    >>> l[0]
    7
    >>> l['cat']
    7
    >>> l['rhino']
    Traceback (most recent call last):
    ...
    KeyError: 'rhino'
    >>> 'dog' in l
    True
    >>> 8 in l
    True
    >>> l.insert(1, ('lemur', 12))
    >>> l
    [7, 12, 8]
    >>> l.keys()
    ['cat', 'lemur', 'dog']
    '''
    def __init__(self, pairs=None):
        if pairs is None:
            pairs = []
        self._keys = []
        values = []
        for key, value in pairs:
            self._keys.append(key)
            values.append(value)
        super(ListDict, self).__init__(values)
        
    def __getitem__(self, key):
        if isinstance(key, basestring):
            try:
                i = self._keys.index(key)
                return super(ListDict, self).__getitem__(i)
            except ValueError:
                raise KeyError(key)
        else:
            return super(ListDict, self).__getitem__(key)
            
    def __setitem__(self, key, value):
        if isinstance(key, basestring):
            try:
                i = self._keys.index(key)
                return super(ListDict, self).__setitem__(i, value)
            except ValueError:
                raise KeyError(key)
        else:
            return super(ListDict, self).__setitem__(key, value)
            
    def __delitem__(self, key):
        if isinstance(key, basestring):
            try:
                i = self._keys.index(key)
                #Deletes from the list
                super(ListDict, self).__delitem__(i)
                #Deletes from the list of keys
                self._keys.__delitem__(i)
            except ValueError:
                raise KeyError(key)
        else:
            #Remove from list
            super(ListDict, self).__delitem__(key)
            #Assuming that goes ok, del from keys
            self._keys.__delitem__(key)
            
    def __contains__(self, key):
        if isinstance(key, basestring):
            return key in self._keys
        else:
            return super(ListDict, self).__contains__(key)
            
    def __eq__(self, rhs):
        if isinstance(rhs, ListDict):
            return super(ListDict, self).__eq__(rhs) and self._keys == rhs._keys
        return False
            
    def pop(self, index=None):
        if isinstance(index, basestring): 
            try:
                index = self._keys.index(index)
            except ValueError:
                raise KeyError(index)
                
        if index is None:
            val = super(ListDict, self).pop()
            index = -1
        else:
            val = super(ListDict, self).pop(index)
            
        self._keys.__delitem__(index)
        return val
        
    def remove(self, value):
        if isinstance(value, basestring):
            try:
                index = self._keys.index(value)
            except ValueError:
                raise KeyError(value)
        else:
            try:
                index = self.index(value)
            except ValueError:
                raise ValueError('list.remove(x): x not in list')
        
        #This will also remove the key
        self.__delitem__(index)
        
    def insert(self, index, obj):
        if len(obj) != 2:
            raise TypeError('New ListDict item must be a key:value pair.')
        key, val = obj
        #The default inserts will handle index > length for us
        self._keys.insert(index, key)
        super(ListDict, self).insert(index, val)
        
    def append(self, obj):
        self.insert(len(self), obj)
        
    def extend(self, objs):
        for obj in objs:
            self.insert(len(self), obj)
            
    def keys(self):
        return self._keys
        
    def values(self):
        return list(self)
        
    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default
        
if __name__ == "__main__":
    sys.exit(test.main('__main__'))
