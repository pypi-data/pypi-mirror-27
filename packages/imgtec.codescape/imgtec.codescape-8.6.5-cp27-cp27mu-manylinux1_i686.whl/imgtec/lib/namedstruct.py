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

import inspect
import operator
import re
import struct
import sys
from imgtec.lib import backwards


re_field_splitter = re.compile("""
^(
  [0-9]+s|                               # special case for char[]
  [a-zA-Z]                               # type char
)
(?:\s+(\w+)                            # name
  (?:\s*=\s*                           # initialisation value
    (
     \d+|                              #    decimal
     0x[0-9a-zA-Z]+|                   #    hexadecimal
     "[^"\\\r\n]*(?:\\.[^"\\\r\n]*)*"| #    " string
     '[^'\\\r\n]*(?:\\.[^'\\\r\n]*)*'| #    ' string
     False|True|                       #    boolean 
     _size                             #    size of struct
     )             
  )?  
  (?:\s+(.*))?                         # docstring
)?
$
""", re.VERBOSE | re.DOTALL)

default_init = '0'

def _decode_field(x):
    r"""Decode a typed field param to namedstruct.
    
    >>> _decode_field(('L', 'name', 0, 'docstring which may have spaces'))
    ('L', 'name', '0', 'docstring which may have spaces')
    >>> _decode_field(('L', 'name'))
    ('L', 'name', '0', '')
    >>> _decode_field('name')
    Traceback (most recent call last):
        ...
    RuntimeError: Failed to decode field input : 'name'
    >>> _decode_field('L name')
    ('L', 'name', '0', '')
    >>> _decode_field('L name=10')
    ('L', 'name', '10', '')
    >>> _decode_field('L name docstring which may have spaces')
    ('L', 'name', '0', 'docstring which may have spaces')
    >>> _decode_field('x some padding')    
    ('x', 'some', '0', 'padding')
    >>> _decode_field('x')    
    ('x', '', '0', '')
    >>> _decode_field('H size=_size')    
    ('H', 'size', '_size', '')
    """
    if isinstance(x, tuple):
        name, init, doc = '', default_init, ''
        format = x[0]
        try:
            name = x[1]
            init = x[2]
            doc  = x[3]
        except IndexError:
            pass
    else:
        try:
            format, name, init, doc = re_field_splitter.match(x).group(1, 2, 3, 4)
        except AttributeError:
            raise RuntimeError("Failed to decode field input : %r" % (x,))
        
    return format, (name or ''), (init or default_init), doc or ''
       
def _make_property(n, format_name_init_doc):
    """Make the property code for field `n`.
    
    >>> _make_property(0, _decode_field('L name=1 docstring which has spaces'))
    "name = _property(_itemgetter(0), _itemsetter(0), doc='docstring which has spaces')"
    """
    type, name, init, doc = format_name_init_doc
    setter = ''
    if init != '_size':
        setter = ", _itemsetter(%(n)d)"
    return ("%(name)s = _property(_itemgetter(%(n)d)" + setter + ", doc=%(doc)r)") % locals()
    
def _itemsetter(item):
    """Like operator.itemgetter.  Actually I don't know why this doesn't already
    exist in operator."""
    def g(obj, val):
        obj[item] = val
    return g
    
def cleandoc(docstring, required_indent=4):
    docstring = inspect.cleandoc(docstring.lstrip())
    return ("\n" + ' ' * required_indent).join(docstring.split("\n"))

def namedstruct(typename, fields, prefix='', docstring='', verbose=False, expected_size=None):
    r"""Creates types that can be used for named field extraction from
    byte sequence.  This is a hybrid of collections.namedtuple and 
    struct.Struct.
    
    Unlike namedtuple, the instances of the created type are mutable.
    
    `typename` gives the name of the struct.
    
    `fields` is an iterable of strings which define the struct layout.  Each
    field is of the format :

        ::
    
            fieldformat [ fieldident [= fieldinit ] [ fielddoc ] ]
                
        Where `fieldformat` is one of the struct format characters. `fieldident`
        is the field name, and should be a valid python idenfifier, and not 
        begin with an underscore (to avoid clashes with the namedstruct 
        properties). 

        If `fieldformat` is ``x`` then `fieldident` should be omitted and the 
        field will not be accessible; this is useful for padding bytes.
        
        `fieldinit` is how the field should be initialised, this can be a decimal 
        or hexadecimal literal, a boolean, a string, or defaults to 0. 
        Alternatively this field can also be `_size`, in which case the field will 
        be initialised to the size of the structure.
        
        `fielddoc` is used for the field's docstring.
        
    `prefix` is used to prefix the struct format, and it is usually used to 
    configure the endian and alignment of the structure.
    
    `docstring` is the class's docstring.
    
    If `verbose` is true, the class definition is printed just before being
    built.
    
    Named struct instances do not have per-instance dictionaries, so they are 
    as lightweight and require no more memory than a list.
    
    >>> Point = namedstruct('Point', ('L x=0', 'L y=1', 'x', 'L sz=_size docstring'), prefix='<')
    >>> pt = Point(x=2, y=5)
    >>> pt.sz
    13
    >>> pt.x, pt.y
    (2, 5)
    >>> pt = Point(2)
    >>> pt.x, pt.y
    (2, 1)
    
    struct.Struct methods and properties are available, but they are prefixed
    with an underscore so they don't clash with field names :
    
    >>> Point._size, Point._format
    (13, '<LLxL')
    >>> s = pt._pack()
    >>> s
    '\x02\x00\x00\x00\x01\x00\x00\x00\x00\r\x00\x00\x00'
    >>> pt2 = Point._unpack(s)
    >>> pt2.x, pt2.y
    (2, 1)
    
    >>> pt2 = Point._unpack_from(s + s, 4)
    >>> pt2.x, pt2.y
    (1, 3328)
    
    The type is also an iterable sequence, making it easy to substitute for
    existing struct.Struct usages: 
    
    >>> len(pt)
    3
    >>> "...".join(str(x) for x in pt)
    '2...1...13'
    >>> pt[0]
    2
    
    The initialiser, arguments to the constructor, and assignments to properties
    must all be an appropriate type for the format character :
    
    >>> pt.x = 'spam'
    Traceback (most recent call last):
        ...
    error: value for field x is incorrect type for format 'L': 'spam'
    >>> Point = namedstruct('Point', ('L x="hello"', 'L y=1'))
    Traceback (most recent call last):
        ...
    error: initialiser for field x is incorrect type for format 'L': "hello"
    >>> Point = namedstruct('Point', ('s x=_size', 'L y=1'))
    Traceback (most recent call last):
        ...
    error: initialiser for field x is incorrect type for format 's': _size
    >>> pt3 = Point(x="hello")
    Traceback (most recent call last):
        ...
    error: value for field x is incorrect type for format 'L': 'hello'

    Invalid keyword arguments will be caught :

    >>> pt4 = Point(bob=1)
    Traceback (most recent call last):
        ...
    TypeError: 'bob' is an invalid keyword argument for this function

    
    Optionally you can specify an expected_size for the struct, if this 
    different from the calculated size struct.error will be raised:
    
    >>> namedstruct('BadSize', ('L field',), expected_size=6, prefix='=')
    Traceback (most recent call last):
        ...
    error: calculated size of BadSize(4) is different to expected(6)
    
    >>> Point = namedstruct('Point', ('4s e_ident="?"', 'L other'), prefix='=')
    >>> pt = Point()
    >>> pt.e_ident, pt.other
    ('?', 0)
    >>> pt = Point._unpack('OK\x00?\x00\x00\x00\x00toolong')
    Traceback (most recent call last):
        ...
    error: unpack requires a string argument of length 8
    >>> pt = Point._unpack('OKshort')
    Traceback (most recent call last):
        ...
    error: unpack requires a string argument of length 8
    >>> pt = Point._unpack('OK\x00?\x00\x00\x00\x00')
    >>> pt.e_ident, pt.other
    ('OK\x00?', 0)
    """
    decoded = [_decode_field(x) for x in fields]
    _format_separate = [x[0] for x in decoded]
    _format = "".join(_format_separate)
    actual_size = struct.calcsize(prefix + _format)
    if expected_size is not None and actual_size != expected_size:
        raise struct.error("calculated size of %s(%d) is different to expected(%d)" %
                                (typename, actual_size, expected_size))
        
    decoded = [x for x in decoded if x[0] != 'x'] # skip padding bytes
    for format, name, init, doc in decoded: # check that the default vals are good
        _init = init
        if init == '_size':
            _init = '12'
        try:
            struct.pack(format, eval(_init))
        except (TypeError, struct.error):
            raise struct.error("initialiser for field %s is incorrect type for format '%s': %s" % 
                                (name, format, init))
        
                
    _fields        = ", ".join(repr(x[1]) for x in decoded)
    _args          = ", ".join(x[1] for x in decoded)
    _args_defaults = ", ".join("%s=%s" % x[1:3] for x in decoded)
    _properties    = "\n    ".join(_make_property(*x) for x in enumerate(decoded))
    
    if docstring:
        docstring = '"""' + cleandoc(docstring) + '"""'
        
    template = """
class %(typename)s(object):
    %(docstring)s
    
    _format  = '%(prefix)s' + '%(_format)s'
    '''The format string used to construct the struct.Struct instance.'''
    
    _struct  = _struct.Struct(_format)
    
    _size    = _struct.size
    '''The calculated size of the struct (and hence of the packed string).'''
    
    _fields  = (%(_fields)s)
    '''A tuple containing all of the field names.'''
    
    _formats = '%(_format)s'
    _format_separates = [x for x in %(_format_separate)s if x != 'x']
    
    __slots__ = ('_values',)

    def __init__(self, %(_args_defaults)s, **kwargs):
        if kwargs.pop('__skip_checks', False):
            self._values=[%(_args)s]
        else:
            self._values=[self.__check(n, x) for n, x in enumerate([%(_args)s])]
        if kwargs:
            raise TypeError("'" + kwargs.popitem()[0] + "' is an invalid keyword argument for this function")
        
    def _pack(self):
        '''Return a string containing the members packed according to the format
        `len(result)` will equal `self._size`.'''
        return self._struct.pack(*self._values)
        
    def _pack_into(self, buffer, offset=0):
        '''Pack the members packed according to the format, write the packed 
        bytes into the writeable buffer starting at offset.
        '''
        return self._struct.pack_into(buffer, offset, *self._values)
        
    @_classmethod
    def _unpack(cls, string):
        '''Create an instance of %(typename)s which is initialised by unpacking 
        the `string` into the members according to the format. The `string` must 
        contain exactly the amount of data required by the format (`len(string)` 
        must equal `self._size`).
        '''
        return cls(*cls._struct.unpack(string), __skip_checks=True)
        
    @_classmethod
    def _unpack_from(cls, buffer, offset=0):
        '''Create an instance of %(typename)s which is initialised by unpacking
        the `buffer` starting from `offset`. The `buffer` must contain at least 
        the amount of data required by the format (len(buffer[offset:]) must be 
        at least `self._size`).
        '''
        return cls(*cls._struct.unpack_from(buffer, offset), __skip_checks=True)
        
    def __getitem__(self, idx):
        return self._values[idx]

    @_classmethod    
    def __check(cls, idx, val):
        '''Check that val is a valid type for field idx.'''
        try:
            format = cls._format_separates[idx]
            _struct.pack(format, val)
            return val
        except (TypeError, _struct.error):
            raise _struct.error("value for field %%s is incorrect type for format '%%s': %%r" %% 
                                (cls._fields[idx], format, val))
                                
    def __setitem__(self, idx, val):
        self._values[idx] = self.__check(idx, val)
        
    def __len__(self):
        return len(self._values)
        
    def __iter__(self):
        return iter(self._values)
        
    def __repr__(self):
        vals = [repr(getattr(self, field)) for field in self.__class__._fields]
        return "%%s(%%s)" %% (self.__class__.__name__, ', '.join(vals))
      
    %(_properties)s
        
""" % locals()
    if verbose:
        sys.stdout.write(template)

    # Execute the template string in a temporary namespace and
    # support tracing utilities by setting a value for frame.f_globals['__name__']
    namespace = dict(__name__='namedstruct_%s' % typename,
                     _property=property, _classmethod=classmethod, 
                    _itemgetter=operator.itemgetter, _itemsetter=_itemsetter,
                    _struct=struct)
    try:
        backwards.exec_function(template, '<string>', namespace)
    except SyntaxError:
        e = sys.exc_info()[1]
        raise SyntaxError(str(e) + ':\n' + template)
    result = namespace[typename]
    # For pickling to work, the __module__ variable needs to be set to the frame
    # where the named tuple is created.  Bypass this step in enviroments where
    # sys._getframe is not defined (Jython for example).
    if hasattr(sys, '_getframe'):
        result.__module__ = sys._getframe(1).f_globals.get('__name__', '__main__')
    return result

if __name__ == "__main__":
    import doctest
    doctest.testmod()
