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

"""
:mod:`imgtec.lib.namedenum` -- A python implementation of an enum type
======================================================================
"""
import collections
import itertools
import sys
import sys as _sys
from keyword import iskeyword as _iskeyword
from textwrap import dedent
from imgtec.lib import backwards
from imgtec.test import *
from imgtec.lib import rst

__all__ = ("namedenum", "Value")

try:
    enum_value_base_type = long
except NameError:
    long = int
    enum_value_base_type = long

def typeof(value):
    '''Get the type of an enum value, or return type(value) if it is not an 
    enum value.
    
    >>> typeof(0)
    <type 'int'>
    
    >>> E = namedenum('E', 'v0 v1 v2')
    >>> E == typeof(E.v0)
    True
    
    '''
    try:
        return value._cls
    except AttributeError:
        return type(value)    

class NamedEnumType(object):
    '''Classes generated using namedenum are subclasses of this type.
    
    >>> E = namedenum('E', 'v0 v1 v2')
    >>> issubclass(E, NamedEnumType)
    True
    
    Note that values of the generated class are not instances of NamedEnumType::

    >>> a = E.v0
    >>> isinstance(a, NamedEnumType)
    False
    >>> isinstance(a, NamedEnumValue)
    True
    
    This may be surprising because as aa convenience you can construct values of 
    E with the __call__ method::
    
    >>> E(0), E('v1')
    (E.v0, E.v1)
    
    Given an enum value, you can determine it's type with the :func:`typeof` 
    function.
    
    '''

class NamedEnumValue(long):
    """Values of instances of classes generated using namedenum are of this 
    type. It is derived from the python builtin `long`.
    
    >>> E = namedenum('E', 'a')
    >>> isinstance(E.a, NamedEnumValue)
    True
    >>> isinstance(E.a, long)
    True
    >>> issubclass(Value, long)
    True
    
    It's str representation is 'value name'. It's repr representation is 
    'type name.value name'
    
    >>> str(E.a)
    'a'
    >>> repr(E.a)
    'E.a'
    
    """
    def __new__(cls, enum_cls, cls_name, name, value, doc=''):
        self = super(Value, cls).__new__(cls, value)
        self._cls = enum_cls
        self._cls_name = cls_name
        self._name = name
        self.__doc__ = doc or ''        
        return self
    def __str__(self):
        return self._name
    def __repr__(self):
        return "%s.%s" % (self._cls_name, self._name)
    def __getnewargs__(self):
        return (self._cls, self._cls_name, self._name, long(self))
        
Value = NamedEnumValue

def _get_names_and_values(args, value=0):
    """Get name, value pairs from a sequence of enum value definitions.
    
    >>> _get_names_and_values(['a', 'b', 'c'])
    [('a', 0), ('b', 1), ('c', 2)]
    >>> _get_names_and_values(['a=1', 'b', 'c'])
    [('a', 1), ('b', 2), ('c', 3)]
    >>> _get_names_and_values(['a', 'b=1', 'c'], 14)
    [('a', 14), ('b', 1), ('c', 2)]
    """
    ret = []
    for name in args:
        try:
            name, value = name.split('=', 1)
            value = int(value, 0)
        except ValueError:
            pass
        ret.append((name, value))
        value += 1
    return ret
    
def _decode_arg(default_value, name, value=None, doc=None):
    if value is None and default_value is None:
        raise ValueError("Implicit value not allowed in **kwargs because the order is undefined in value " + name)
    return (name, default_value if value is None else value, doc)
def _decode_kwarg(name, arg):
    if not isinstance(arg, collections.Sequence):
        arg = arg,
    return _decode_arg(None, name, *arg)
def _decode_args(*args, **kwargs):
    res = []
    idx = 0
    for argn, arg in enumerate(args):
        if isinstance(arg, basestring):
            vals = _get_names_and_values(arg.split(), idx)
            for name, value in vals:
                res.append((name, value, None))
        elif isinstance(arg, collections.Sequence):
            res.append(_decode_arg(idx, *arg))
        else:
            raise TypeError("Invalid type for namedenum %r at position %d, expected string or sequence" % (args, argn))
        idx = res[-1][1] + 1
    res.extend(_decode_kwarg(name, item) for name, item in kwargs.iteritems())
    return res
        
def defaultdoc_values_formatter(name, value):
    return str(value), name
    
def getusage(_typename, names):
    return dedent("""\
    Instances of %(name)s are initialised from properties of %(name)s, or 
    cast from integers and strings ::
    
      >>> x, y, z = %(name)s.%(first)s, %(name)s(%(firstv)d), %(name)s('%(first)s')

    Instances of %(name)s can be converted to strings and integers ::
    
      >>> str(x), repr(x), int(x)
      ('%(first)s', '%(name)s.%(first)s', %(firstv)d)
    
    Instances of %(name)s can be compared to other instances or to integers ::
      
      >>> (x == y, x == %(name)s.%(first)s, x != %(name)s.%(first)s, x == %(firstv)d)
      (True, True, False, True)
      
    The names and values of %(name)s can be iterated over using dict-like 
    class methods, prepended with an underscore to disambiguate from enum 
    values.
    
      >>> %(name)s._keys()
      [%(keys)s]
      >>> %(name)s._values()
      [%(values)s]
      >>> %(name)s._items()
      [%(items)s]""") % dict(
        name=_typename, first=names[0][0], firstv=names[0][1],
        keys=', '.join(repr(x[0]) for x in names),
        values=', '.join(repr(x[1]) for x in names),
        items=', '.join(repr(x) for x in names)
        )       
        
def validate_names(names, item_type='enum'):
    """
    Check that a list of names can be used as Python type/variable names. item_type is the 
    second noun printed in the error message. E.g. for "Type names and field names"
    it would be 'field'.
    
    >>> validate_names(['foo'])
    >>> validate_names(['!foo'])
    Traceback (most recent call last):
    ...
    ValueError: Type names and enum names can only contain alphanumeric characters and underscores: '!foo'
    >>> validate_names(['0foo'])
    Traceback (most recent call last):
    ...
    ValueError: Type names and enum names cannot start with a number: '0foo'
    >>> validate_names(['print'])
    Traceback (most recent call last):
    ...
    ValueError: Type names and enum names cannot be a keyword: 'print'
    >>> validate_names(['print'], item_type='elephant')
    Traceback (most recent call last):
    ...
    ValueError: Type names and elephant names cannot be a keyword: 'print'
    """
    
    for name in names:
        if not all(c.isalnum() or c=='_' for c in name):
            raise ValueError('Type names and %s names can only contain alphanumeric characters and underscores: %r' % (item_type, name))
        if _iskeyword(name):
            raise ValueError('Type names and %s names cannot be a keyword: %r' % (item_type, name))
        if name[0].isdigit():
            raise ValueError('Type names and %s names cannot start with a number: %r' % (item_type, name))
            
def namedenum(_typename, *args, **kwargs):
    """Constructs a type that can be used as an enumerated type.
    
    Main features :
    
    * The type is 'named', and belongs to the module in which it was created.
    * Values can be sparse.
    * Both names (keys), values and items (key/value pairs) can be iterated.    
    * The values are longs, but are printable as strings.
    
    If '_verbose' is specified in kwargs then the generated class definition
    is written to sys.stdout.

    Types may be constructed using string parameters, in which case implicit
    ascending values are used starting from 0, like a C enum:
        
        >>> MyEnum = namedenum('MyEnum', 'a', 'b', 'c')
    
    They can also be specified with more than one identifier per string, 
    allowing multiple values to be specified in a multiline string:    
    
        >>> MyEnum2 = namedenum('MyEnum2', '''
        ...    a b c
        ... ''')
        >>> MyEnum2._keys() == MyEnum._keys()
        True
    
    They can also be specified as keyword args.
    
        >>> MyEnum3 = namedenum('MyEnum', 'a b', c=2)
        >>> MyEnum3._keys() == MyEnum._keys()
        True
        >>> MyEnum
        ===== ====
        Value Name
        ===== ====
        0     a
        1     b
        2     c
        ===== ====
        
    Docstrings for the values can be included as well ::
    
        >>> DocumentedEnum = namedenum('DocumentedEnum', 'a', ('b', 1, 'Docs for b'), c=(2, 'C doc'))
        >>> int(DocumentedEnum.a), DocumentedEnum.a.__doc__
        (0, '')
        >>> int(DocumentedEnum.b), DocumentedEnum.b.__doc__
        (1, 'Docs for b')
        >>> int(DocumentedEnum.c), DocumentedEnum.c.__doc__
        (2, 'C doc')
        
    In this case docstrings should be included as a positional argument with a 
    (name, value, doc) tuple, or as a keyword argument name=(value, doc).  
    Positional arguments may use None for value to indicate that the previous 
    ``value + 1`` should be used.
    
    Docs are included in the generated documentation if any of the values have docstrings.

    Values are comparable to each other and integers/longs:
    
        >>> e = MyEnum.a
        >>> (e == MyEnum.a, e == MyEnum.b, e == 0)
        (True, False, True)
        >>> (e < MyEnum.b, e > MyEnum.a, e < 2)
        (True, False, True)
    
    Note they are also comparable to enum values from other distinct enum types:
    
    >>> MyEnum.a == MyEnum2.a == MyEnum3.a
    True
    
    Values are convertible to strings as their value name, and they are derived
    from long so can be used in integer/long contexts:
    
        >>> str(e)
        'a'
        >>> long(e)
        0L
        >>> '%d' % long(e)    # These casts are necessary due to a bug in CPython
        '0'
        >>> '%08x' % long(e)  # interpreter.
        '00000000'
        >>> isinstance(e, long)
        True
        >>> repr(e)
        'MyEnum.a'
        >>> e
        MyEnum.a
    
    They can be constructed from integers/longs and strings:
    
        >>> MyEnum(2) == MyEnum.c
        True
        >>> MyEnum(7) == MyEnum.b
        Traceback (most recent call last):
          File "<stdin>", line 1, in ?
        ValueError: Cannot convert 7 to MyEnum
        >>> MyEnum('c') == MyEnum.c
        True
        >>> MyEnum('badger') == MyEnum.c
        Traceback (most recent call last):
          File "<stdin>", line 1, in ?
        ValueError: Cannot convert 'badger' to MyEnum
    
    The values of an enum can be accessed using the class methods _items, _keys, 
    and _values. Much like the dict methods:
    
        >>> list(MyEnum._items())
        [('a', 0), ('b', 1), ('c', 2)]
        >>> list(MyEnum._keys())
        ['a', 'b', 'c']
        >>> list(MyEnum._values())
        [0, 1, 2]
        
    Enum type names must be valid python identifiers:
    
        >>> namedenum('not valid')
        Traceback (most recent call last):
          File "<stdin>", line 1, in ?
        ValueError: Type names and enum names can only contain alphanumeric characters and underscores: 'not valid'
    
    Enum values must not contain duplicate names or duplicate values:
    
        >>> namedenum('valid', 'seen', 'seen')
        Traceback (most recent call last):
          File "<stdin>", line 1, in ?
        ValueError: Encountered duplicate enum name: 'seen'
        >>> namedenum('valid', 'seen', notseen=0)
        Traceback (most recent call last):
          File "<stdin>", line 1, in ?
        ValueError: Encountered duplicate enum value: 'notseen'=0 (same value as 'seen')
        >>> namedenum('MyEnum', 'a=1 b c')._items()
        [('a', 1), ('b', 2), ('c', 3)]
    
    """
    # parse and remove any optional arguments
    verbose = kwargs.pop('_verbose', False)
    doc_title =  kwargs.pop('_doc_title', 'Enumerated type %s.' % (_typename,))
    doc = kwargs.pop('_doc', None)
    doc_values = kwargs.pop('_doc_values', None)
    doc_values_header = kwargs.pop('_doc_values_header', ('#', 'Symbolic Name'))
    doc_values_formatter = kwargs.pop('_doc_values_formatter', defaultdoc_values_formatter)
    doc_usage = kwargs.pop('_doc_usage', None)
    
    names_with_docs = _decode_args(*args, **kwargs)
    names     = [(name, value) for name, value, valuedoc in names_with_docs]
    
    validate_names([_typename] + [item[0] for item in names])
            
    seen_names = set()
    seen_values = dict()
    for name, value in names:
        if name.startswith('_'):
            raise ValueError('Enum names cannot start with an underscore: %r' % name)
        if name in seen_names:
            raise ValueError('Encountered duplicate enum name: %r' % name)
        existing = seen_values.get(value)
        if existing:
            raise ValueError('Encountered duplicate enum value: %r=%d (same value as %r)' % (name, value, existing))
        seen_names.add(name)
        seen_values[value] = name
              
    numfields = len(names)
    argtxt = repr(names).replace("'", "")[1:-1]   # tuple repr without parens or quotes
    reverse = "{" + ",".join("%d:%r" % (value, name) for (name, value) in names) + "}"
    forward = repr(names)
    properties = "\n".join("%s.%s = NamedEnumValue(%s, %s.__name__, %r, %d, %r)" % \
                        (_typename, name, _typename, _typename, name, value, valuedoc)
                           for name, value, valuedoc in names_with_docs)

    #Declared here so that it always exists (metaclass repr checks it)
    valuedocs = []
    if doc_values is None:
        items = sorted(names_with_docs, key=lambda x:x[1])
        cells = [doc_values_formatter(name, value) for name, value, valuedoc in items]
        valuedocs = [valuedoc or '' for name, value, valuedoc in items]
        if any(valuedocs):
            cells = zip(*cells)
            cells.append(valuedocs)
            cells = zip(*cells)
            if len(doc_values_header) < 3:
                doc_values_header = list(doc_values_header)
                doc_values_header.append('Description')
        doc_values = rst.table(doc_values_header, cells)
    if doc_usage is None:
        doc_usage = getusage(_typename, names)
    if doc is None:
        doc = '\n\n'.join(x for x in [doc_title, doc_values, doc_usage] if x)
        doc = '\n    '.join(doc.split('\n'))
    
    template = """
class meta_%(_typename)s(type):
    def __repr__(self):
        titles = ['Value', 'Name']
        rows = []
        docs = self._value_docs
        
        if not docs:
            #Make sure we can loop over them
            docs = ['']*len(self._items())
        else:
            #Docs might all be empty
            if any(docs):
                titles.append('Description')

        for item, doc_string in zip(self._items(), docs):
            name, value = item
            rows.append([str(value), name, doc_string])
        return table(titles, rows)
        
    def __len__(self):
        return len(self._items())
        
class %(_typename)s(NamedEnumType):
    '''%(doc)s'''
    
    _forward = %(forward)s
    _reverse = %(reverse)s
    _value_docs = %(valuedocs)s

    __slots__ = ()
    __metaclass__ = meta_%(_typename)s
    

    @classmethod
    def _items(cls):  return [(k, v) for k, v in cls._forward]
    @classmethod
    def _keys(cls):   return [k for k, v in cls._forward]
    @classmethod
    def _values(cls): return [v for k, v in cls._forward]

    def __new__(self, value):
        try:
            return getattr(self, value)
        except AttributeError:
            raise ValueError("Cannot convert " + repr(value) + " to %(_typename)s")
        except TypeError:
            try:
                value = %(_typename)s._reverse[long(value)]
            except KeyError:
                raise ValueError("Cannot convert " + repr(value) + " to %(_typename)s")
            else:
                return getattr(self, value)
%(properties)s
""" % locals()
    # Execute the template string in a temporary namespace and
    # support tracing utilities by setting a value for frame.f_globals['__name__']
    if verbose:
        sys.stdout.write(template)
    namespace = dict(__name__='namedenum_%s' % _typename,
                     _property=property, _tuple=tuple, table=rst.table,
                     NamedEnumValue=NamedEnumValue, NamedEnumType=NamedEnumType)
    try:
        backwards.exec_function(template, '<string>', namespace)
    except SyntaxError:
        e = _sys.exc_info()[1]
        raise SyntaxError(str(e) + ':\n' + template)
    result = namespace[_typename]
    # For pickling to work, the __module__ variable needs to be set to the frame
    # where the named tuple is created.  Bypass this step in enviroments where
    # sys._getframe is not defined (Jython for example).
    if hasattr(_sys, '_getframe'):
        result.__module__ = _sys._getframe(1).f_globals.get('__name__', '__main__')
    return result

@test
def testnamedenum() :
    MyEnum = namedenum('MyEnum', 'a', 'b', 'c')
    a = MyEnum.a
    A = MyEnum(0)
    assertEquals(MyEnum.a, a)
    assertEquals(MyEnum.a, A)
    assertEquals('a', str(A))
    assertEquals('a', str(MyEnum.a))
    assertEquals('a', str(a))
    assertEquals(0, A)
    assertEquals(0, long(A))
    assertTrue(MyEnum.b > MyEnum.a)
    assertTrue(MyEnum.b > 0)
    assertTrue(MyEnum.b < MyEnum.c)
    assertEquals(['a', 'b', 'c'], [x for x in MyEnum._keys()])
    assertRaises(ValueError, MyEnum, 7)
    assertEquals(MyEnum.a, MyEnum('a'))
    assertRaises(ValueError, MyEnum, 'badger')
    
@test
def testnamedenum_with_whitespace() :
    MyEnum = namedenum('MyEnum', 'a b c', 'd')
    assertEquals(['a', 'b', 'c', 'd'], [x for x in MyEnum._keys()])
    
@test
def testEnumWithKwArgs() :
    MyEnum = namedenum("MyEnum", a=7, b=9)
    assertEquals(7, MyEnum.a)
    assertEquals(9, MyEnum.b)

@test
def testEnumWithSetNumberThenAutoIncrement() :
    MyEnum = namedenum("MyEnum", "a=7 b")
    assertEquals(7, MyEnum.a)
    assertEquals(8, MyEnum.b)

@test
def testReusingValueRaises() :
    assertRaises(ValueError, namedenum, "MyEnum", 'a', b=0)

@test
def testReusingNameRaises() :
    assertRaises(ValueError, namedenum, "MyEnum", 'b', b=1)
@test
def testBadNameRaises() :
    assertRaises(ValueError, namedenum, "My Enum", 'x', b=1)

@test
def testOrderMaintained():
    e = namedenum("e", *('the quick brown fox'.split()))
    assertEquals("the quick brown fox", " ".join(e._keys()))
    
@test 
def valuesAreDeepCopyable():
    e = namedenum("e", "a b c")
    a = e.a
    import copy
    a2 = copy.deepcopy(a)

@test 
def docstring():
    e = namedenum("e", "a b c")
    assertEqual('''Enumerated type e.
    
    = =============
    # Symbolic Name
    = =============
    0 a
    1 b
    2 c
    = =============
    
    Instances of e are initialised from properties of e, or 
    cast from integers and strings ::
    
      >>> x, y, z = e.a, e(0), e('a')
    
    Instances of e can be converted to strings and integers ::
    
      >>> str(x), repr(x), int(x)
      ('a', 'e.a', 0)
    
    Instances of e can be compared to other instances or to integers ::
    
      >>> (x == y, x == e.a, x != e.a, x == 0)
      (True, True, False, True)
    
    The names and values of e can be iterated over using dict-like 
    class methods, prepended with an underscore to disambiguate from enum 
    values.
    
      >>> e._keys()
      ['a', 'b', 'c']
      >>> e._values()
      [0, 1, 2]
      >>> e._items()
      [('a', 0), ('b', 1), ('c', 2)]''', e.__doc__)


@test 
def docstring_with_no_examples():
    e = namedenum("e", "a b c", _doc_usage='')
    assertEqual('''Enumerated type e.
    
    = =============
    # Symbolic Name
    = =============
    0 a
    1 b
    2 c
    = =============''', e.__doc__)

def f(**kwargs):
    pass


@test
def docstring_with_no_examples_order_correct_with_kwargs():
    e = namedenum("e", a=0, b=1, c=2, _doc_usage='')
    assertEqual('''Enumerated type e.
    
    = =============
    # Symbolic Name
    = =============
    0 a
    1 b
    2 c
    = =============''', e.__doc__)


@test 
def docstring_with_no_examples_and_no_values():
    e = namedenum("e", "a b c", _doc_usage='', _doc_values='')
    assertEqual('Enumerated type e.', e.__doc__)
    
@test 
def docstring_with_no_examples_and_no_title():
    e = namedenum("e", "a b c", _doc_usage='', _doc_title='')
    assertEqual('''= =============
    # Symbolic Name
    = =============
    0 a
    1 b
    2 c
    = =============''', e.__doc__)
        
@test
def docstring_includes_docvalues_if_one_present():
    e = namedenum("e", ("a", 0, "adoc"), "b", "c", _doc_usage='', _doc_title='')
    assertEqual('''= ============= ===========
    # Symbolic Name Description
    = ============= ===========
    0 a             adoc
    1 b
    2 c
    = ============= ===========''', e.__doc__)
@test
def docstring_allows_override_of_value_header():
    e = namedenum("e", ("a", 0, "adoc"), "b", "c", _doc_usage='', _doc_title='', _doc_values_header=('_', 'Nm', 'De'))
    assertEqual('''= == ====
    _ Nm De
    = == ====
    0 a  adoc
    1 b
    2 c
    = == ====''', e.__doc__)


@test
def docstring_doc_values_header():
    e = namedenum("e", "a b c", _doc_values_header=('v', 'Name'), _doc_usage='', _doc_title='')
    assertEqual('''= ====
    v Name
    = ====
    0 a
    1 b
    2 c
    = ====''', e.__doc__)
    
@test
def docstring_doc_values_formatter():
    def formatter(name, value):
        return '%X' % value, name
    e = namedenum("e", "a=10 b c", _doc_values_formatter=formatter, _doc_usage='', _doc_title='')
    assertEqual('''= =============
    # Symbolic Name
    = =============
    A a
    B b
    C c
    = =============''', e.__doc__)

@test
def docstring_doc_values():
    def formatter(name, value):
        return '%X' % value, name
    e = namedenum("e", "a=10 b c", _doc_values='I like a, b, c', _doc_usage='', _doc_title='')
    assertEqual('I like a, b, c', e.__doc__)
    
@test
def docstring_doc_values_default_title():
    def formatter(name, value):
        return '%X' % value, name
    e = namedenum("e", "a=10 b c", _doc_values='I like a, b, c', _doc_usage='')
    assertEqual('Enumerated type e.\n    \n    I like a, b, c', e.__doc__)
    
@test 
def default_docstring_is_overridable():
    e = namedenum("e", "a b c", _doc='wibble')
    assertEqual('wibble', e.__doc__)
    
@test 
def doc_title_is_overridable():
    e = namedenum("e", "a b c", _doc_title='wibble', _doc_usage='')
    assertEqual('''wibble
    
    = =============
    # Symbolic Name
    = =============
    0 a
    1 b
    2 c
    = =============''', e.__doc__)
    
@test([
(namedenum("repr_example_1", ('a', 0, 'description of a'), ('b', 1, 'description of b')), 
dedent('''\
            ===== ==== ================
            Value Name Description
            ===== ==== ================
            0     a    description of a
            1     b    description of b
            ===== ==== ================'''),
),
(namedenum("repr_example_2", ('c', 2, 'description of c'), ('d', 3, ''                )),
dedent('''\
            ===== ==== ================
            Value Name Description
            ===== ==== ================
            2     c    description of c
            3     d
            ===== ==== ================'''),
),
(namedenum("repr_example_3", ('e', 4,                   ), ('f', 5,                   )),
dedent('''\
            ===== ====
            Value Name
            ===== ====
            4     e
            5     f
            ===== ===='''),
),
])
def namedenum_repr(e, expected):
    assertEquals(expected, repr(e))

@test
def enums_values_without_docstrings():
    args = _decode_args("a b", "c", d=42)
    assertEquals([('a', 0, None),
                  ('b', 1, None),
                  ('c', 2, None),
                  ('d', 42, None)], args)

@test
def enums_values_without_docstrings_and_an_assignment():
    args = _decode_args("a=5 b", "c", d=42)
    assertEquals([('a', 5, None),
                  ('b', 6, None),
                  ('c', 7, None),
                  ('d', 42, None)], args)

@test
def enums_values_specigfying_idx_sets_new_default():
    args = _decode_args("a", ("b", 5, "bdoc"), "c")
    assertEquals([('a', 0, None),
                  ('b', 5, 'bdoc'),
                  ('c', 6, None)], args)

@test
def enums_values_no_docstrings():
    args = _decode_args(("a", 0), ('b', 1), ('c', 42))
    assertEquals([('a', 0, None),
                  ('b', 1, None),
                  ('c', 42, None)], args)



@test
def enums_values_with_docstrings():
    args = _decode_args("a", ("b", None, "bdoc"), c=(42, "cdoc"))
    assertEquals([('a', 0, None),
                  ('b', 1, 'bdoc'),
                  ('c', 42, 'cdoc')], args)

    e = namedenum('e', "a", ("b", None, "bdoc"), c=(42, "cdoc"))
    assertEquals('cdoc', e.c.__doc__)

@test
def enums_values_dont_allow_implicit_idx_in_kwargs():
    assertRaisesWithMessage(ValueError, 'Implicit value not allowed', _decode_args, "a", ("b", None, "bdoc"), c=(None, "cdoc"))

@test
def is_possible_to_determine_when_we_have_a_namedenum_ctored_type():
    A = namedenum('A', 'a b c')
    assertTrue(issubclass(A, NamedEnumType))
    a = A(0)
    assertTrue(isinstance(a, NamedEnumValue))
    #assertTrue(isinstance(a, A))
    

if __name__ == "__main__": 
    test.main()
    
