from collections import namedtuple
import itertools
import operator
import re
import sys

class RegisterPrerequisiteDoesNotExist(Exception):
    pass

class RegisterAccessError(Exception):
    pass

class RegisterUnreadable(Exception):
    '''Because read_registers is False.'''

def namedtuple_with_defaults(name, spec):
    '''Create a namedtuple but the field list may include default values.

    The repr of the fn also uses the minimum number of positional arguments,
    rather than named parameters like the default repr of namedtuple classes.

    >>> T = namedtuple_with_defaults('T', 'a b=1 c="hello"')
    >>> t = T(0)
    >>> t
    T(0)
    >>> (t.a, t.b, t.c)
    (0, 1, 'hello')

    At present the spec parsing is not very intelligent, and some things won't
    work correctly:

    * Whitespace in the default value
    * Missing defaults after a defaulted item (e.g. a b=0 c d=1)

    '''
    fields = [x.split('=', 1) for x in spec.split()]
    t = namedtuple(name, ' '.join([x[0] for x in fields]))
    t.__new__.__defaults__ = tuple([eval(x[1]) for x in fields if len(x) > 1])
    def shortrepr(self):
        fields, sentinel = [], object()
        cls = self.__class__
        for value, default in itertools.izip_longest(reversed(self),
                        reversed(cls.__new__.__defaults__), fillvalue=sentinel):
            if value != default or fields:
                fields.append(repr(value))
        return '%s(%s)' % (cls.__name__, ', '.join(reversed(fields)))
    t.__repr__ = shortrepr
    # For pickling to work, the __module__ variable needs to be set to the frame
    # where the named tuple is created.  Bypass this step in enviroments where
    # sys._getframe is not defined (Jython for example).
    if hasattr(sys, '_getframe'):
        t.__module__ = sys._getframe(1).f_globals.get('__name__', '__main__')
    return t

ViewOptions = namedtuple_with_defaults('ViewOptions', 
    'show_fields=True show_vertical=True show_raw_value=True show_bit_position=False, view=None')

class Bits(namedtuple_with_defaults('Bits', 'start end_=None')):
    '''
    >>> Bits(3)
    Bits(3)
    >>> Bits(7, 4)
    Bits(7, 4)
    >>> '%x' % Bits(3).mask
    '8'
    >>> '%x' % Bits(7, 4).mask
    'f0'
    '''

    @property
    def end(self):
        end = self.end_
        return self.start if end is None else end

    @property
    def mask(self):
        return ((1 << self.num_bits) - 1) << self.end

    @property
    def num_bits(self):
        return self.start - self.end + 1


class Register(namedtuple_with_defaults('Register', "id comms_name_='' name='' procs_data=None description='' fields=[] size=32 condition=True rwflag='rw'")):
    '''This stores the meta data about registers.
    
    There may be multiple entries for a single comms register, usually only one
    will have conditions satisified for a particular target.  Sometimes there 
    will be multiple even on a single target, in this case these are called views.
    
    Currently these are determined by finding the first whitespace in the name.
    Consequently there are several ways of getting a displayable name::
    
    >>> views = [Register('index_0', 'Index', 'Index (View0)'), Register('index_0', 'Index', 'Index (View1)')]
    >>> [v.view_name for v in views]
    ['View0', 'View1']
    >>> [v.display_name for v in views]
    ['Index_View0', 'Index_View1']
    >>> [v.display_name_no_view for v in views]
    ['Index', 'Index']
    '''
    
    @property
    def comms_name(self):
        return self.comms_name_ or self.id
    @property
    def display_name(self):
        name = self.name or self.id
        return re.sub(r'\W+', '_', name).strip('_')
    @property
    def display_name_no_view(self):
        '''The display_name without the view name, for most registers
        this == display_name.'''
        name = (self.name or self.id).split(None, 1)[0]
        return re.sub(r'\W+', '_', name).strip('_')
    @property
    def view_name(self):
        '''Return just the view name, or an empty string.'''
        names = (self.name or self.id).split(None, 1)
        name = names[1] if len(names) > 1 else ''
        return re.sub(r'\W+', '_', name).strip('_')        

Field = namedtuple_with_defaults('Field', "name bits description='' values=[] xlt_bits=None proc=None")
Value = namedtuple_with_defaults('Value', "name value description='' reserved=False")

class Node(object):
    '''Base class for all condition expression nodes.'''
    __slots__ = ['args']
    def __init__(self, *args):
        self.args = args
    def __eq__(self, other):
        return type(self) is type(other) and self.args == other.args
    def __repr__(self):
        args = [repr(x) for x in self.args]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(args))

def evaluate(node, env):
    '''Evaluate the conditional node.

    This is a free function because it allows terminal expressions (int, bool)
    to be pseudeo-nodes and avoids the need for a Const node.  This keeps the
    repr of expressions simpler.
    '''
    try:
        ev = node.evaluate
    except AttributeError:
        return node
    else:
        return ev(env)

class Op(Node):
    def evaluate(self, env):
        op = {  'gt': operator.gt,  'lt': operator.lt,
                'gte': operator.ge, 'lte': operator.le,
                '==': operator.eq,  '!=': operator.ne,
                'and': operator.and_, # bitwise and - &
        }[self.args[0]]
        return op(*[evaluate(arg, env) for arg in self.args[1:]])

class Condition(Node):
    def evaluate(self, env):
        return evaluate(env.conditions[self.args[0]], env)

class Reg(Node):
    def evaluate(self, env):
        try:
            return env.constants[self.args[0]]
        except KeyError:
            pass
        expr = env.register_field_aliases.get(self.args[0], self.args[0])
        try:
            reg, field = env.get_register_and_field(expr)
            value = env.read_register(reg, field)
        except RegisterAccessError as e:
            if env.verbose:
                sexpr = expr if expr == self.args[0] else '{}({})'.format(expr, self.args[0])
                print('Warning failed to read register/field {}, reason : {}'.format(sexpr, e))
            raise
        if field:
            return (value & field.bits.mask) >> field.bits.end
        else:
            return value

class CPUNameMatches(Node):
    def evaluate(self, env):
        cpu_pattern = self.args[0]
        if ',' in cpu_pattern:
            cpu_pattern = '(%s)' % cpu_pattern.replace(', ', '|').replace(',', '|')
        cpu_pattern = cpu_pattern + '$'
        cpu_pattern = re.compile(cpu_pattern, flags=re.I)
        matched = bool(cpu_pattern.match(env.cpu_name))
        return matched

class Logical(Node):
    pass

class And(Logical):
    def evaluate(self, env):
        return all(evaluate(part, env) for part in self.args)

class Or(Logical):
    def evaluate(self, env):
        return any(evaluate(part, env) for part in self.args)

class Not(Logical):
    def evaluate(self, env):
        return not any(evaluate(part, env) for part in self.args)

if __name__ == '__main__':
    import doctest
    doctest.testmod()