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

import re
import sys
from imgtec.lib import namedenum, backwards, rst
from operator import itemgetter
from ordered_dict import OrderedDict
from itertools import count, izip, tee, chain
import textwrap
from imgtec.lib.namedenum import validate_names
   
class FieldList(list):
    def __repr__(self):
        return '\n'.join(repr(x) for x in self)
        
re_fieldspec = re.compile('\s*(\w+)\s+((?:)0x[a-fz\d]+|\d+)(?:\s+((?:)0x[a-fz\d]+|\d+))?\s*(?:#\s*(.*))?$')

def compile_field(fieldspec):
    r"""Compile a single field spec into that a :class:`~imgtec.lib.namedbitfield.Field`.
    
    >>> compile_field('f1 7    # some description')
    f1 bit_start:7 bit_end:7 mask:0x80
        some description
    
    """
    m = re_fieldspec.match(fieldspec)
    if not m:
        raise ValueError("Could not parse %r as a valid fieldspec" % (fieldspec,))
    return Field(m.group(1), int(m.group(2), 0),
                  int(m.group(3), 0) if m.group(3) else None,
                   m.group(4) or '')

def compile_fields(fields):
    r"""Compile multiple field specs into a list of :class:`~imgtec.lib.namedbitfield.Field`.
    
    The format is ::
    
        identifier bit_start[ bit_end][ # description]
    
    Where bit_start should be greater than bit_end and is inclusive.
    
    `fields` may be either a list of strings, or a single string with each field
    spec on a separate line. Blank lines are ignored.

    >>> compile_fields(['f1 7', 'f2 9 8 '])
    f1 bit_start:7 bit_end:7 mask:0x80
    f2 bit_start:9 bit_end:8 mask:0x300
    >>> compile_fields('''\
    ...       f1 7
    ...       f2 9 8
    ...  ''')
    f1 bit_start:7 bit_end:7 mask:0x80
    f2 bit_start:9 bit_end:8 mask:0x300
    
    A list of :class:`~imgtec.lib.namedbitfield.Field`s is returned.
    """
    if isinstance(fields, (str, unicode)):
        fields = fields.splitlines()
    return FieldList(compile_field(line) for line in fields if line.strip())

def _pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

class Field(object):
    '''Represents a part of a namedbitfield.
    
    Construct a Field directly or use :func:`~imgtec.lib.namedbitfield.compile_field`
    or :func:`~imgtec.lib.namedbitfield.compile_fields`.
    
    If `bit_end` is None at construction then this field is a single bit field
    and so :attr:`bit_end` == :attr:`bit_start`.
    '''
    def __init__(self, name, bit_start, bit_end=None, description='', type=long):
        self.name = name
        '''The name of this field.'''
        self.bit_start = bit_start
        '''The most significant bit of this field.'''
        self.bit_end = bit_end if bit_end is not None else bit_start
        '''The least significant bit of this field.'''
        self.description = description
        '''A description which will be shown in docstrings.'''
        self.type = type
        '''The type of the field.  Generally it is long, but it may be something
        that behaves like a long, e.g. another type constructed using 
        :func:`~imgtec.lib.namedbitfield.namedbitfield` or 
        :func:`~imgtec.lib.namedenum.namedenum`.
        '''
        
    def format(self, value, wordy=False):
        """Extract a (name, str) pair based on the field and it's value.

        If `wordy` is True, more information is returned, for example the radix
        and any enum equivalence.

        >>> Field('n1', 15, 12).format(0xd)
        'd'
        >>> Field('n1', 1, 0).format(0x3)
        '3'
        >>> E = namedenum.namedenum('E', 'a b c')
        >>> Field('n1', 1, 0).format(E.b, wordy=True)
        'b(0x1)'
        """
        size = self.size
        f = ('%%0%dx' % ((size+3)//4,))
        if wordy:
            f = '0x' + f
            if isinstance(value, namedenum.Value):
                f = str(value) + '(' + f + ')'
        return f % value

    @property
    def size(self):
        '''Return the number of bits in the bitfield.'''
        return self.bit_start - self.bit_end + 1        
        
    @property
    def mask(self):
        '''The mask for this field, shifted down to bit zero.
        
        >>> f = Field('f', 10, 7)
        >>> '0x%04x' % (f.mask,)
        '0x000f'
        >>> '0x%04x' % (f.mask << f.shift)
        '0x0780'
        '''
        return (1 << self.size) - 1
        
    @property
    def shift(self):
        '''The shift for this field.
        
        >>> Field('f', 10, 7).shift
        7
        '''
        return self.bit_end        

    def _repr_for_generation(self):
        #This is used to generate reginfo instances
        #The usual repr of a type gives <type bla> which can't be used as code
        desc, type = '', ''
        if self.description:
            desc = ', '+ repr(self.description)
        if self.type != long:
            type = ', type=' + self.type.__name__
        return 'Field(%r, %r, %r%s%s)' % (
                    self.name, self.bit_start, self.bit_end, desc, type)

    def __repr__(self):
        #This is used to actually print the field
        desc = ''
        if self.description:
            desc = '\n    ' + self.description
        bits = self.bit_start-self.bit_end+1
        mask = ((2**bits)-1) << self.bit_end
        ret = '%s bit_start:%d bit_end:%d mask:0x%x%s' % (self.name, self.bit_start, self.bit_end, mask, desc) 
        if self.type != long:
            ret += '\n        ' + repr(self.type).replace('\n', '\n        ')
        return ret
        
    def _as_tuple(self):
        return (self.name, self.bit_start, self.bit_end, self.description, self.type)
    
    def __eq__(self, rhs):
        if not isinstance(rhs, Field):
            return False
        return self._as_tuple() == rhs._as_tuple()

def namedbitfield(name, fields, size=None, description='', verbose=False,
                  show_vertical=False, show_raw_value=False, show_bit_position=False):
    """Create a class which behaves like a long but which exposes read-only
    properties to access its constituent bitfields.

    Duplicate field names are allowed, but the fields are not then available
    as properties, nor are they replaceable using the _replace method.

    `fields` is a list of (name, startbit, endbit), where startbit and endbit
    are inclusive, and endbit can be omitted for a single bit.  startbit should
    always be greater than or equal to endbit.  Alternatively `fields` may be a 
    list of :class:`Field` instances, or if it is a single string then the 
    field list is parsed using :func:`~imgtec.lib.namedbitfield.compile_fields` 
    from a simple string format.
    
    `description` is the description of the overall class. For example the 
    purpose of the register being shown.

    `size` is the size of the bitfield in bits, and is used to format the raw
    value.  If not given it is set to the largest startbit+1 ::

        >>> TestReg = namedbitfield('TestReg', [('b', 6, 2), ('a', 1), ('a', 0)], size=8)
        >>> x = TestReg(0xf1)
        >>> x
        b  a a
        1c 0 1
        >>> '0x%x' % (x.b,)
        '0x1c'

    Return a modified value using the _replace method ::

        >>> TestReg = namedbitfield('TestReg', '''b 6 2
        ...                                       a 1
        ...                                       a 0''')
        >>> x = TestReg(0xf1)
        >>> x._replace(b=0x1e)
        b  a a
        1e 0 1

    Duplicate, or invalid field names are not available as properties ::

        >>> x.a
        Traceback (most recent call last):
        ...
        AttributeError: 'TestReg' object has no attribute 'a'

    By default namedbitfield displays the fields in a horizontal layout and does
    not include the raw value of the bitfield.  This default  behaviour can
    be changed using the ``show_vertical`` and ``show_raw_value``, options to
    namedbitfield. Additionally, the  defaults can be overridden by calling
    _display ::

        >>> VertRaw = namedbitfield('VertRaw', [('b', 6, 2), ('a', 1), ('a', 0)],
        ...                 show_vertical=True, show_raw_value=True)
        >>> r = VertRaw(0xf1)
        >>> r
        <raw value> 0xf1
        b           0x1c
        a           0x0
        a           0x1
        
        >>> print r._display(show_vertical=False, show_raw_value=False)
        b  a a
        1c 0 1

    """

    def normtuple(name, start, end=None, type=long):
        return Field(name, start, end if end is not None else start, type=type)

    if isinstance(fields, (str, unicode)):
        fields = compile_fields(fields)
    fields = [f if isinstance(f, Field) else normtuple(*f) for f in fields]
    validate_names([f.name for f in fields] + [name], item_type='field')

    # sort by most significant first
    #Check for bit start being before the end, where start is the most significant
    for f in sorted(fields, key=lambda f: -f.bit_start):
        if f.bit_start < f.bit_end:
            raise ValueError("Field %s[%d:%d] has bits start < end" % (f.name, f.bit_start, f.bit_end))

    # The default __repr__ on a field is made to be human readable. They are 
    # converted to evaluateable strings here.
    fields_as_code = ''.join(['[', ', '.join([field._repr_for_generation() for field in fields]), ']'])

    if size is None:
        size = max(f.bit_start+1 for f in fields)

    template = '''\
    
class meta_%(name)s(type):
    def __repr__(self):
        parts = [] 
        if self.__doc__.strip():
            parts.append(_textwrap.dedent(self.__doc__).strip())
        if self._fields:
            if parts:
                parts[0] += '\\n\\n'
            parts.append('\\n'.join([repr(field) for field in self._fields]))
        return ''.join(parts)
    
class %(name)s(long):
    \'''\\
    %(description)s
    \'''
    __metaclass__ = meta_%(name)s
    
    _fields = %(fields)s
    \'''A list of :class:`imgtec.lib.namedbitfield.Field` instances for all 
    fields in the bitfield.\'''
    
    _size = %(size)d
    \'''A list of :class:`imgtec.lib.namedbitfield.Field` instances for all
    fields in the bitfield.\'''
    
    _show_vertical = %(show_vertical)s
    \'''Whether instances of %(name)s should display vertically or horizontally..\'''
    
    _show_raw_value = %(show_raw_value)s
    \'''Whether instances of %(name)s should display vertically or horizontally..\'''

    _show_bit_position = %(show_bit_position)s
    \'''Whether instances of %(name)s should show bitfield positions..\'''
    
    __slots__ = ()

    def __new__(_cls, initial_value=0, **field_values):
        """Create a %(name)s with `initial_value` and with specified fields replaced."""
        return long.__new__(_cls, initial_value)._replace(**field_values)

    def __getitem__(self, n):
        """Access fields by index, in field order."""
        field = self._fields[n] 
        v = (long(self) >> field.shift) & field.mask
        try:
            return field.type(v)
        except ValueError:
            return v

    def __len__(self):
        return len(self.__class__._fields)

    def _items(self):
        """Return a list of (name, value) pairs.

        The order is the order the namedbitfield was created with.
        """
        return [(f.name, value) for f, value in zip(self.__class__._fields, self)]
        
    @classmethod
    def _find_field(cls, fieldname):
        """Find the field named `fieldname` and return it's meta data as an 
        instance of :class:`imgtec.lib.namedbitfield.Field`.

        ValueError is raised if either there are no matching fields, or there
        are multiple matching fields.        
        """
        fields = cls._find_fields(fieldname)
        if len(fields) == 0:
            raise ValueError('{0} has no field {1}'.format(cls.__name__, fieldname))
        elif len(fields) > 1:
            raise ValueError('{0} has multiple fields named {1}, use _find_fields'.format(cls.__name__, fieldname))
        return fields[0]
            
    @classmethod
    def _find_fields(cls, fieldname):
        """Find all fields named `fieldname` and return theirs meta data as a list
        of :class:`imgtec.lib.namedbitfield.Field`.

        An empty list is returned if no fields match.
        """
        return [f for f in cls._fields if f.name == fieldname]

    def _replace(_self, **field_values):
        """Return a new %(name)s value replacing specified fields with new values."""
        val = long(_self)

        fields = [x for x in _self.__class__._fields if x.name in field_values]
        fields = sorted(fields, key=lambda f: -f.bit_start) # sort by most sig first
        for left, right in _pairwise(fields):
            if left.bit_end <= right.bit_start:
                raise TypeError('Cannot construct or _replace a %(name)s with overlapping fields %%s[%%d:%%d] and %%s[%%d:%%d]' %%
                    (left.name, left.bit_start, left.bit_end, right.name, right.bit_start, right.bit_end))

        for f in _self.__class__._fields:
            try:
                v = field_values.pop(f.name)
                mask = f.mask
                masked = v & mask
                val &= ~(mask << f.shift)
                if masked != v:
                    raise OverflowError("Value %%r for field %%s bits[%%d:%%d] is out of range"
                                    %% (v, f.name, f.bit_start, f.bit_end))
                val |= (masked << f.shift)
            except KeyError:
                pass
        if field_values:
            raise ValueError("Got unexpected field names: %%r" %% (field_values.keys(),))
        return long.__new__(_self.__class__, val)
        
    def _display_raw(self, wordy=True):
        pre = '0x' if wordy else ''
        return   ('%%s%%%%0%%dx' %% (pre, (self._size+3)//4,)) %% (long(self),)
        
    def _display(self, show_raw_value=None, show_vertical=None, show_bit_position=None):
        """Format the bitfield with various options."""
        if show_raw_value is None: show_raw_value = self._show_raw_value
        if show_vertical is None:  show_vertical = self._show_vertical
        if show_bit_position is None: show_bit_position = self._show_bit_position
        raw_value = ''
        if show_raw_value or not self._items():
            raw_value = self._display_raw(wordy=show_vertical)
        if self._items():
            rows = []
            if show_raw_value:
                raw_row = ['<raw value>' if show_vertical else '<raw>']
                if show_bit_position:
                    raw_row.append(' ')
                raw_row.append(raw_value)
                rows.append(raw_row)

            for f, v in zip(self._fields, self):
                row = [f.name,]
                if show_bit_position:
                    if f.bit_start == f.bit_end:
                        row.append('%%d' %% f.bit_start)
                    else:
                        row.append('%%d..%%d' %% (f.bit_start, f.bit_end))
                row.append(f.format(v, wordy=show_vertical))
                rows.append(row)
            
            if not show_vertical:
                rows = zip(*rows)
            return _rst.headerless_table(rows)
        else:
            return raw_value
        
    def __reduce__(self):
        cls = self.__class__
        m = _sys.modules[cls.__module__]
        if hasattr(m, cls.__name__):
            return (self.__class__, (long(self),))
        else:
            return (long, (long(self),))

    def __repr__(self):
        return self._display()

''' % dict(name=name, size=size, fields=fields_as_code, 
           show_vertical=show_vertical, show_raw_value=show_raw_value,
           show_bit_position=show_bit_position,
           description='\n    '.join(description.split('\n')))

    names = [f.name for f in fields]
    for n, f in enumerate(fields):
        if names.count(f.name) == 1:
            template += "    %s = property(itemgetter(%d), doc='Accessor for field %s[%d:%d]')\n" % (f.name, n, f.name, f.bit_start, f.bit_end)

    if verbose:
        sys.stdout.write(template)

    types = [f.type for f in fields]
    enums = dict([(t.__name__, t) for t in types])
    ns = dict(enums, __name__='bitfield_result_%s' % name, property=property, 
              itemgetter=itemgetter, _pairwise=_pairwise, _sys=sys, _rst=rst,
              _textwrap=textwrap, Field=Field)

    try:
        backwards.exec_function(template, '<string>', ns)
    except SyntaxError:
        e = sys.exc_info()[1]
        lines = ['%d: %s' % x for x in enumerate(template.splitlines(), 1)]
        raise SyntaxError(str(e) + ':\n' + '\n'.join(lines))

    result = ns[name]
    # For pickling to work, the __module__ variable needs to be set to the frame
    # where the named tuple is created.  Bypass this step in environments where
    # sys._getframe is not defined (Jython for example).
    if hasattr(sys, '_getframe'):
        result.__module__ = sys._getframe(1).f_globals.get('__name__', '__main__')
    return result
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()