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

from imgtec.lib import rst
from imgtec.lib.ordered_dict import OrderedDict
from collections import namedtuple
from contextlib import contextmanager
import itertools
import math
import sys
import traceback

def get_formatter(radix, size):
    if radix == 16:
        format = '0%dx' % (size*2,)
    elif radix == 10:
        format = {1:'3d', 2:'5d', 4: '10d', 8:'20d'}.get(size, 'd')
    elif radix == -10:
        format = {1:'4d', 2:'6d', 4: '11d', 8:'21d'}.get(size, 'd')
    elif radix == 8:
        format = '%do' % ((size*8+2)//3,)
    elif radix == 2:
        format = '0%db' % (size*8,)
    else:
        raise RuntimeError('Unsupported radix : %d' % (radix,))
    format = '{0:' + format + '}'
    return format.format
    
def _display(x):
    '''Converts any builtin type into a string, preferring hex over decimal.
    
    If the value is an exact matches to int/long/list/tuple/dict then formats 
    it as hex.  Otherwise __repr__ is used.
    
    >>> _display({1:7})
    '{0x1: 0x7}'
    >>> _display(set([1, 2, 3]))
    '{0x1, 0x2, 0x3}'
    >>> _display([1, 2, 0xffffffff, -1])
    '[0x1, 0x2, 0xffffffff, -0x1]'
    >>> _display((1, 'bob', 0xffffffff))
    '(0x1, bob, 0xffffffff)'
    >>> _display(RuntimeError('oh'))
    'RuntimeError: oh'
    '''
    t = type(x)
    if t in (str, unicode):
        return x if x else repr(x)
    elif t in (int, long):
        sign = ''
        if x < 0:
            sign = '-'
            x = -x
        return '%s0x%x' % (sign, x)
    elif t in (list, tuple, set):
        p = {set:'{}', list:'[]', tuple:'()'}[t]
        c = ', ' if t == tuple and len(x) == 1 else ''
        return p[0] + ', '.join(_display(v) for v in x) + c + p[1]
    elif t == set:
        return '{' + ', '.join(_display(v) for v in x) + '}'
    elif t == dict:
        return '{' + ', '.join('%s: %s' % (_display(k), _display(v)) for k, v in x.iteritems()) + '}'
    elif isinstance(x, Exception):
        return traceback.format_exception_only(t, x)[0].rstrip()
    else:
        return repr(x)

_int_result_type_cache = dict()


def IntResultType(size=4, radix=16, doc=''):
    """Create a type that is like an int/long, but renders in hex.

    >>> IntResultType()(0x1234)
    0x00001234
    >>> IntResultType(size=2)(0x1234)
    0x1234
    >>> IntResultType(radix=10)(0x1234)
    4660
    >>> IntResultType(radix=10)
    IntResultType(size=4, radix=10)
    >>> IntResultType(radix=10, doc='This is a 32-bit register')
    This is a 32-bit register
    """
    cache_key = (radix, size, doc)
    try:
        t = _int_result_type_cache[cache_key]
    except KeyError:
        pre = {2:'0b',8:'0o', 10:'', -10:'', 16:'0x'}.get(radix, '')
        formatter = get_formatter(radix, size)
        class MetaIntResult(type):
            def __repr__(cls):
                return doc or '''IntResultType(size=%d, radix=%d)''' % (size, radix)
        class IntResult(long):
            __metaclass__ = MetaIntResult
            def __repr__(self):
                return pre + formatter(self).strip()
        t = _int_result_type_cache[cache_key] = IntResult
    # TODO signed IntResult is not correct.
    return t


def IntResult(x, radix=16, size=4):
    """Like an int/long, but renders in hex (by default).

    >>> IntResult(0x1234)
    0x00001234
    >>> IntResult(0x1234, size=2)
    0x1234
    >>> IntResult(0x1234, radix=10)
    4660
    >>> IntResult(0x1234, radix=2, size=3)
    0b000000000001001000110100
    >>> IntResult(0x1234, size=3)
    0x001234
    >>> IntResult(0x1234, size=9)
    0x000000000000001234
    >>> IntResult(0x1234, size=5, radix=8)
    0o11064
    """
    return IntResultType(radix=radix, size=size)(x)

def IntListResult(x, radix=16, size=4):
    """Like a list of int/long, but renders in hex.

    >>> IntListResult([0x1234, 0x43215678])
    [0x00001234, 0x43215678]
    >>> IntListResult([0x1234, 0x5678], size=2)
    [0x1234, 0x5678]
    >>> IntListResult([0x1234, 0x5678], radix=10)
    [4660, 22136]
    """
    pre = {2:'0b',8:'0o', 10:'', -10:'', 16:'0x'}.get(radix, '')
    formatter = get_formatter(radix, size)
    class Result(list):
        def __repr__(self):
            return '[' + ", ".join(pre + formatter(v).strip() for v in self) + ']'
    return Result(x)

class StrResult(str):
    """Like str but does not print in quotes.

    >>> StrResult('hello')
    hello
    """
    def __new__(cls, s):
        return str.__new__(cls, s)
    def __repr__(self):
        return self
        
class StrListResult(list):
    """Like [str...] but each item prints on a new line, and not in quotes.

    >>> StrListResult(['hello', 'world'])
    hello
    world
    """
    def __repr__(self):
        return "\n".join(self)
        
class NumberedListResult(list):
    """A list of entries that displays each item on a new line, with prefixed index.

    The prefix can be used to select an item more easily:

    >>> NumberedListResult('a b c d e f g h i j k l'.split())
    0 : a
    1 : b
    2 : c
    3 : d
    4 : e
    5 : f
    6 : g
    7 : h
    8 : i
    9 : j
    10: k
    11: l
    >>> _[0]
    'a'
    """
    def __repr__(self):
        width = len('%d' % len(self))
        format = '%%-%dd: %%s' % width
        return '\n'.join(format % (n, _display(x)) for n, x in enumerate(self))

class HeaderlessTableResult(list):
    """A list of lists that displays as a columnised list.  
    
    It should be initialised with a list of rows. The number of columns is 
    determined by the longest of the rows. 

    >>> HeaderlessTableResult([['a'], ['b', 'c']])
    a
    b c
    >>> HeaderlessTableResult([('muchlonger',), ['b', 'c']] * 6)
    muchlonger
    b          c
    muchlonger
    b          c
    muchlonger
    b          c
    muchlonger
    b          c
    muchlonger
    b          c
    muchlonger
    b          c
    """
    def __repr__(self):
        rows = [[_display(x) for x in row] for row in self]
        return rst.headerless_table(rows)
        

class HeaderlessNumberedTableResult(list):
    """A list of lists that displays as a columnised list, each row is numbered.

    It should be initialised with a list of rows. The number of columns is
    determined by the longest of the rows.

    >>> HeaderlessNumberedTableResult([['a'], ['b', 'c']])
    0: a
    1: b c
    >>> HeaderlessNumberedTableResult([('muchlonger',), ['b', 'c']] * 6)
    0 : muchlonger
    1 : b          c
    2 : muchlonger
    3 : b          c
    4 : muchlonger
    5 : b          c
    6 : muchlonger
    7 : b          c
    8 : muchlonger
    9 : b          c
    10: muchlonger
    11: b          c
    """
    def __repr__(self):
        width = len('%d' % len(self))
        format = '%%-%dd:' % width
        rows = [[format % n] + [_display(x) for x in row] for n, row in enumerate(self)]
        return rst.headerless_table(rows)
            
    
class OrderedDictResult(OrderedDict):
    def __repr__(self):
        rows = [(n, _display(x)) for n, x in self.items()]
        return rst.headerless_table(rows)
        
_NamedBitfieldDiff = namedtuple('_NamedBitfieldDiff', 'was now')
class NamedBitfieldDiff(_NamedBitfieldDiff):
    '''Displays old and new values in a pair of named bitfields of the same type.
    
    >>> from imgtec.lib.namedbitfield import namedbitfield
    >>> from imgtec.lib.namedenum import namedenum
    >>> e = namedenum('e', ea=0, eb=1, ec=2)
    >>> TestReg = namedbitfield('TestReg', [('b', 6, 2, e), ('a', 1), ('a', 0)], size=32)
    >>> NamedBitfieldDiff(TestReg(0), TestReg(0xff))
    Field Name  Was        Now
    <raw value> 0x00000000 0x000000ff
    b           ea(0x00)   0x1f
    a           0x0        0x1
    a           0x0        0x1
    >>> NamedBitfieldDiff(IntResult(0), IntResult(0xff))
    Was        Now
    0x00000000 0x000000ff
    >>> NamedBitfieldDiff(TestReg(0), IntResult(0xff))
    Field Name  Was        Now
    <raw value> 0x00000000 0x000000ff
    b           ea(0x00)   0x1f
    a           0x0        0x1
    a           0x0        0x1
    >>> NamedBitfieldDiff(IntResult(0), TestReg(0xff))
    Field Name  Was        Now
    <raw value> 0x00000000 0x000000ff
    b           ea(0x00)   0x1f
    a           0x0        0x1
    a           0x0        0x1
    '''
    def __repr__(self):
        richtypes = [type(x) for x in self if hasattr(x, '_display_raw')]
        if richtypes:
            t = richtypes[0]
            rows = [['Field Name', 'Was', 'Now']] # TODO 'then'
            vals = [x if isinstance(x, t) else t(x) for x in self]
            rows.append(['<raw value>'] + [x._display_raw() for x in vals])
            for fieldn, field in enumerate(t._fields):
                rows.append([field.name] + [field.format(x[fieldn], wordy=True) for x in vals])        
        else:
            rows = [['Was', 'Now']] # TODO 'then'
            rows.append([repr(x) for x in self])
        return rst.headerless_table(rows)
        
class AllResult(list):
    '''A result type that aids returning multiple results from multiple devices.
    
    For example this is used for the results of cmdall, tapall and can be used 
    by any other command that accepts multiple devices.
    '''
    def __init__(self):
        list.__init__(self)
        self.names = []
        
    def add(self, name, result):
        '''Add a single result.
        
        If result is an instance of Exception then the results is treated as a 
        failure.
        '''
        self.names.append(name)
        self.append(result)
        
    def call(self, fn, named_things, *args, **kwargs):
        '''Call fn once for each thing in named_things, store result or Exception.
        
        fn must be a callable accepting ``(thing, *args, **kwargs)``.
        
        >>> class Thing(object): 
        ...     name = 'thing0'
        ...     def f(self):
        ...        if self.name == 'thing1': raise RuntimeError('no thing1')
        >>> things = [Thing(), Thing()]
        >>> things[1].name = 'thing1'
        >>> res = AllResult()
        >>> res.call(Thing.f, things)
        >>> res
        thing0: None
        thing1: RuntimeError: no thing1
        '''
        for thing in named_things:
            try:
                self.add(thing.name, fn(thing, *args, **kwargs))
            except Exception as e:
                self.add(thing.name, e)        

    def any_valid(self):
        '''Return True if any of the results are not None.
        
        >>> res = AllResult()
        >>> res.any_valid()
        False
        >>> res.add('one', None)
        >>> res.any_valid()
        False
        >>> res.add('two', 0)
        >>> res.any_valid()
        True
        '''
        return bool(self and any(x is not None for x in self))
        
    def get_result(self, fn=None, *args, **kwargs):
        '''Get a nice return type for returning from command. 
        
        This will return None if all results were None. Raise an exception
        if any result was an exception, or if all succeeded return self.
        
        If `fn`, `args`, and `kwargs` are given they will be used to format a string 
        describing the call that caused the failure.
        
        >>> res = AllResult()
        >>> res.get_result()
        >>> res.add('one', None)
        >>> res.get_result()
        >>> res.get_result_maybe_just_one()
        >>> res.add('two', 2)
        >>> res.get_result()
        one: None
        two: 2
        >>> res.get_result_maybe_just_one()
        one: None
        two: 2
        >>> res.add('buckle', RuntimeError('my shoe'))
        >>> res.get_result(res.get_result, 'a', 'b', kwarg='kwargvalue')
        Traceback (most recent call last):
        ...
        RuntimeError: One or more calls to get_result('a', 'b', kwarg='kwargvalue') failed:
        one: None
        two: 2
        buckle: RuntimeError: my shoe
        >>> res.get_result()
        Traceback (most recent call last):
        ...
        RuntimeError: One or more calls failed:
        one: None
        two: 2
        buckle: RuntimeError: my shoe
        >>> res.get_result_maybe_just_one()
        Traceback (most recent call last):
        ...
        RuntimeError: One or more calls failed:
        one: None
        two: 2
        buckle: RuntimeError: my shoe
        
        >>> res = AllResult()
        >>> res.get_result()
        >>> res.add('one', 'One!')
        >>> res.get_result_maybe_just_one()
        'One!'
        '''        
        if fn:
            allargs = [repr(x) for x in args] + ['%s=%r' % x for x in kwargs.items()]
            fn = ' to %s(%s)' % (fn.__name__, ', '.join(allargs))
        errs = [x for x in self if isinstance(x, Exception)]
        if errs:
            raise RuntimeError('One or more calls%s failed:\n%r' % (fn or '', self))
        return self if self.any_valid() else None    
        
    def get_result_maybe_just_one(self, fn=None, *args, **kwargs):
        '''Get a nice return type which may or may not be a list.
        
        This is just like :meth:`get_result` except that if the number of 
        results stored is one then just that result is returned rather than a 
        list of results.

        >>> res = AllResult()
        >>> res.add('one', 'One!')
        >>> res.get_result_maybe_just_one()
        'One!'
        >>> res = AllResult()
        >>> res.add('one', Exception('error'))
        >>> res.get_result_maybe_just_one()
        Traceback (most recent call last):
        ...
        Exception: error
        >>> res = AllResult()
        >>> res.get_result_maybe_just_one()
        '''
        if len(self) != 1:
            res = self.get_result(fn, *args, **kwargs)
        else:
            res = self[0]
            if isinstance(res, Exception):
                raise res
        return res
            

    def __repr__(self):
        '''
        
        >>> res = AllResult()
        >>> res.add('one', 0)
        >>> res.add('two', RuntimeError('hello'))
        >>> res
        one: 0
        two: RuntimeError: hello
        '''
        chunks = []
        for n, r in zip(self.names, self):
            r = '%s: %s' % (type(r).__name__, r) if isinstance(r, Exception) else repr(r)
            chunks.append(n + ': ' + '\n'.ljust(len(n)+3).join(r.split('\n')))
        return '\n'.join(chunks)
        

class NoneGuard(object):
    '''This displays like None (i.e. displays nothing), but it can be used in a 
    with block and calls ``f(*args, **kwargs)`` on __exit__.
    '''
    def __init__(self, f, *args, **kwargs):
        self.f, self.args, self.kwargs = f, args, kwargs
    def __enter__(self):
        return self
    def __exit__(self, *exc):
        self.f(*self.args, **self.kwargs)
        
def _longest(items) :
    """Return the length of the longest item in items"""
    return 0 if not items else max(len(x) for x in items)

def _columnize_items(items, num_cols) :
    """Split a set of items into a list of columns, ordered down then across 
    (like a newspaper). Return cols, widths.
    """
    c      = int(math.ceil(float(len(items)) / num_cols))
    cols   = [items[n * c:(n + 1) * c] for n in range(num_cols)]
    for col in cols :
        if len(col) != c :
            col.extend(['']* (c - len(col)))
    widths = [_longest(col) for col in cols]
    return cols, widths

def _columnize_items_max_columns(items, width) :
    """Split a list of items into a list of columns, ordered down then across 
    (like a newspaper). The number of columns is set to minimize vertical space.
    Return cols, widths.
    """
    num_cols = min(len(items), width / _longest(items))
    cols, widths = _columnize_items(items, num_cols)
    for n in range(num_cols + 1, len(items) + 1) :
        new_cols, new_widths = _columnize_items(items, n)
        total  = sum(new_widths) + n
        if total < width :
            cols, widths = new_cols, new_widths
        else :
            break
    return cols, widths
    
def column_table(items, width=None):
    r'''Format a list of items into columns, ordered down then across (like a 
    newspaper). The number of columns is set to minimize vertical space.
    
    >>> column_table(['ham', 'spam', 'cheese'], 12)
    'ham  cheese\nspam'
    ''' 
    if width is None:
        width = get_console_width(100)
    cols, _widths = _columnize_items_max_columns(items, width)
    return rst.headerless_table(zip(*cols))
    

def _win32_get_console_width():
    from ctypes.wintypes import BOOL, HANDLE, WORD, SHORT, DWORD
    from ctypes import c_void_p, Structure, windll, byref

    class COORD(Structure):
        _fields_ = [("X", SHORT),
                    ("Y", SHORT)]

    class SMALL_RECT(Structure):
        _fields_ = [("Left", SHORT),
                    ("Top", SHORT),
                    ("Right", SHORT),
                    ("Bottom", SHORT)]

    class CONSOLE_SCREEN_BUFFER_INFO(Structure):
        _fields_ = [("dwSize", COORD),
                    ("dwCursorPosition", COORD),
                    ("wAttributes", WORD),
                    ("srWindow", SMALL_RECT),
                    ("dwMaximumWindowSize", COORD)]

    STD_OUTPUT_HANDLE = -11
    GetStdHandle = windll.kernel32.GetStdHandle
    GetStdHandle.restype = HANDLE
    GetStdHandle.argtypes = [DWORD]

    hout = GetStdHandle(STD_OUTPUT_HANDLE)
    info = CONSOLE_SCREEN_BUFFER_INFO()
    GetConsoleScreenBufferInfo = windll.kernel32.GetConsoleScreenBufferInfo
    GetConsoleScreenBufferInfo.restype = BOOL
    GetConsoleScreenBufferInfo.argtypes = [HANDLE, c_void_p] #HANDLE, PCONSOLE_SCREEN_BUFFER_INFO

    status = GetConsoleScreenBufferInfo(hout, byref(info))
    if status:
        return info.dwSize.X
    raise RuntimeError("GetConsoleScreenBufferInfo failed")

def _unix_get_console_width():
    import fcntl, struct, termios #pylint: disable=import-error
    buf = ' ' * 8
    buf = fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ, buf)
    _row, col, _rpx, _cpx = struct.unpack('hhhh', buf)
    return col

def _get_console_width(default=None):
    if sys.stdout.isatty():
        try:
            if sys.platform == 'win32':
                return _win32_get_console_width() - 1
            else:
                return _unix_get_console_width() - 1
        except Exception:
            pass
    return default
    
_console_width_stack = [_get_console_width]

def get_console_width(default=None):
    return get_console_width_getter()(default)

def get_console_width_getter():
    return _console_width_stack[-1]
    
@contextmanager
def push_console_width_getter(adjuster):
    '''Use this to adjust the default console width calculator.
    
    >>> getter = lambda x=None:42
    >>> with test_console_width(99):
    ...     get_console_width()
    ...     with push_console_width_getter(getter):
    ...         get_console_width()
    ...         with console_width_reducer(10):
    ...             get_console_width()
    ...         get_console_width()
    ...     get_console_width()
    99
    42
    32
    42
    99
    '''
    _console_width_stack.append(adjuster)
    try:
        yield
    finally:
        _console_width_stack.pop()
        
    
@contextmanager
def test_console_width(width=78):
    '''Use this around unit tests that are sensitive to console width.'''
    def _test_console_width(default=None):
        return width
    with push_console_width_getter(_test_console_width):
        yield

@contextmanager
def console_width_reducer(reduction):
    '''Use this to temporarily reduce the console width.  
    
    Used when line output from an outputter is going to be prepended with 
    something.
    '''
    prev = get_console_width_getter()
    def _reducer(default=None):
        return prev(default) - reduction
    with push_console_width_getter(_reducer):
        yield


class CaseInsensitiveDict(dict):
    @classmethod
    def _k(cls, key):
        return key.lower() if isinstance(key, basestring) else key

    def __init__(self, *args, **kwargs):
        super(CaseInsensitiveDict, self).__init__(*args, **kwargs)
        self._convert_keys()
    def __getitem__(self, key):
        return super(CaseInsensitiveDict, self).__getitem__(self.__class__._k(key))
    def __setitem__(self, key, value):
        super(CaseInsensitiveDict, self).__setitem__(self.__class__._k(key), value)
    def __delitem__(self, key):
        return super(CaseInsensitiveDict, self).__delitem__(self.__class__._k(key))
    def __contains__(self, key):
        return super(CaseInsensitiveDict, self).__contains__(self.__class__._k(key))
    def has_key(self, key):
        return super(CaseInsensitiveDict, self).has_key(self.__class__._k(key))
    def pop(self, key, *args, **kwargs):
        return super(CaseInsensitiveDict, self).pop(self.__class__._k(key), *args, **kwargs)
    def get(self, key, *args, **kwargs):
        return super(CaseInsensitiveDict, self).get(self.__class__._k(key), *args, **kwargs)
    def setdefault(self, key, *args, **kwargs):
        return super(CaseInsensitiveDict, self).setdefault(self.__class__._k(key), *args, **kwargs)
    def update(self, E=None, **F):
        super(CaseInsensitiveDict, self).update(self.__class__(E))
        super(CaseInsensitiveDict, self).update(self.__class__(**F))
    def _convert_keys(self):
        for k in list(self.keys()):
            v = super(CaseInsensitiveDict, self).pop(k)
            self.__setitem__(k, v)

class TabbedDict(CaseInsensitiveDict):
    '''Display case insensitively keyed pairs in a particular order, grouped into tabs.

    Additionally the type is a dict, keyed 

    (A fairly specialised display type used by config()).
    
    >>> t = TabbedDict([('tab0', [('r0', 'value00'),('r1', 'value01')]),
    ...             ('tab1', [('s0', 'value10'),('s1', 'value11')])])
    >>> with test_console_width(100):
    ...    t
    ===tab0=== ===tab1===
    r0 value00 s0 value10
    r1 value01 s1 value11
    >>> t['R0']
    'value00'
    >>> with test_console_width(12):
    ...    t
    ===tab0===
    r0 value00
    r1 value01
    <BLANKLINE>
    ===tab1===
    s0 value10
    s1 value11
    
    '''

    def __init__(self, tabs):
        allitems = {}
        for _tab, items in tabs:
            allitems.update([(k.lower(), v) for k, v in items])
        super(TabbedDict, self).__init__(allitems)
        self._tabs = tabs

    def __repr__(self):
        tables = []
        widths = []
        for tab, items in self._tabs:
            if items:
                rows = []
                for item in items:
                    rows.append((_display(item[0]), _display(item[1])))
                table = rst.headerless_table(rows).splitlines()
                longest = max(len(r) for r in table)
                if tab:
                    table.insert(0, tab.center(longest, '='))
                tables.append(table)
                widths.append(longest)
        lines = []
        maxwidth = get_console_width(200)
        while tables:
            if lines:
                lines.append('')
            numtables = 0
            width = 0
            while width < maxwidth and numtables < len(tables):
                numtables += 1
                width = sum(widths[:numtables]) + numtables - 1
            if width >= maxwidth and numtables > 1:
                numtables -= 1
            for cells in itertools.izip_longest(*tables[:numtables], fillvalue=''):
                lines.append(' '.join(cell.ljust(width) for width, cell in zip(widths, cells)))            
            tables = tables[numtables:]
            widths = widths[numtables:]
        return '\n'.join(lines)
        
class ConfigTabbedDict(TabbedDict):
    def __init__(self, tabs, config_type):
        TabbedDict.__init__(self, tabs)
        self.config_type = config_type
    
def _displayhook(x):
    if x is not None and not isinstance(x, NoneGuard):
        print _display(x)
    __builtins__['_'] = x

def _install_displayhook():
    sys.displayhook = _displayhook

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    #import cProfile
    #cProfile.run('[IntResult(x) for x in range(100*1024)]')
