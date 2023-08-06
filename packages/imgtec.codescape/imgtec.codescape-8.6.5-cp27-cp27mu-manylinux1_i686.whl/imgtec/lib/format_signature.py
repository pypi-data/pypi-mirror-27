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

import ast
import collections
import itertools
import re
import sys
from textwrap import dedent
from imgtec.test import *

class Parameter(object):
    empty = object()
    POSITIONAL_ONLY, POSITIONAL_OR_KEYWORD, VAR_POSITIONAL, KEYWORD_ONLY, VAR_KEYWORD = range(5)
    
    def __init__(self, name, kind, default=empty):
        self.name = name
        self.kind = kind
        self.default = default
        
    def __str__(self):
        if self.kind == Parameter.VAR_POSITIONAL:
            return '*' + self.name
        if self.kind == Parameter.VAR_KEYWORD:
            return '**' + self.name
        elif self.default is Parameter.empty:
            return self.name 
        else:
            return '{}={!r}'.format(self.name, self.default)
            
    def __repr__(self):
        d = '' if self.default is Parameter.empty else ', {!r}'.format(self.default)
        return '{}({!r}, {}{})'.format(self.__class__.__name__, self.name, self.kind, d)
        
class Signature(object):
    def __init__(self, parameters):
        self.parameters = collections.OrderedDict([(x.name, x) for x in parameters])
               
    def bind(self, *args, **kwargs):
        '''Like apply, but does not actually call the function, instead returns an
        BoundArguments object that allows querying the result for the arguments that were
        passed via normal args, named args, *args, and **kwargs.
        
        >>> def justnamed(a, b, c):
        ...     pass
        >>> def nonamed(*args, **kwargs):
        ...     pass
        >>> def some_function(a, b=1, c='x', *args, **kwargs):
        ...     pass
        >>> sig = signature(some_function)
        >>> sig.bind(1, b=2, c='x', d='y').arguments
        OrderedDict([('a', 1), ('b', 2), ('c', 'x'), ('args', ()), ('kwargs', {'d': 'y'})])
        >>> sig.bind(1).arguments
        OrderedDict([('a', 1), ('b', 1), ('c', 'x'), ('args', ()), ('kwargs', {})])
        >>> sig.bind(1, 2, 3, 4, x='y').arguments
        OrderedDict([('a', 1), ('b', 2), ('c', 3), ('args', (4,)), ('kwargs', {'x': 'y'})])
        >>> signature(nonamed).bind(1, 2, x='1').arguments
        OrderedDict([('args', (1, 2)), ('kwargs', {'x': '1'})])
        >>> signature(justnamed).bind(1, 2, 3, 4)
        Traceback (most recent call last):
        ...
        TypeError: callable(a, b, c) takes exactly 3 arguments (4 given)
        '''
        fwd = ['({!r}, {})'.format(p.name, p.name) for p in self.parameters.values()]
        code = 'lambda {}: BoundArguments(self, [{}])'.format(str(self)[1:-1], ', '.join(fwd))
        f = eval(code, dict(BoundArguments=BoundArguments, self=self))
        try:
            return f(*args, **kwargs)
        except TypeError as e:
            raise TypeError, TypeError(str(e).replace('<lambda>()', 'callable' + str(self))), sys.exc_info()[2]
        
    def format(self, sep=', '):
        '''Format the signature like a parameter list.'''
        return '(' + sep.join([str(x) for x in self.parameters.values()]) + ')'

    def __str__(self):
        """Format the argument list of a function or method.

        >>> str(signature(lambda a, b=1, c='x', *args, **kwargs: None))
        "(a, b=1, c='x', *args, **kwargs)"
        >>> str(signature(lambda a, **kwargs: None))
        '(a, **kwargs)'
        """
        return self.format()
        
    def __repr__(self):
        """Format the argument list of a function or method.

        >>> Signature([Parameter('a', 1), Parameter('b', 1, 'x'), Parameter('args', 2), Parameter('kwargs', 4)])
        Signature([Parameter('a', 1), Parameter('b', 1, 'x'), Parameter('args', 2), Parameter('kwargs', 4)])
        """
        params = [repr(x) for x in self.parameters.values()]
        return '{}([{}])'.format(self.__class__.__name__, ', '.join(params))
        
class BoundArguments(object):
    def __init__(self, signature, arguments):
        self.signature = signature
        self.arguments = collections.OrderedDict(arguments)

    def format(self):
        '''Format the arguments as they may have been passed to a function.

        Note the returned code may not be identical because the code can't be
        constructed perfectly because :

         * named params can be passed positionally or using their name,
         * default params may or not have been given.
         * kwarg order is not defined (in py2.7 anyway)

        >>> def f(a, *args, **kwargs):
        ...     pass
        >>> f(1, x=3)
        >>> f(x=3, a=1)
        >>> f(a=1, x=3)
        >>> a = signature(f).bind(a=1, x=3)
        >>> a.format()
        '(1, x=3)'
        '''
        def format(p, v):
            if p.kind == Parameter.VAR_POSITIONAL:
                return [repr(a) for a in v]
            if p.kind == Parameter.VAR_KEYWORD:
                return ['{}={!r}'.format(k, v) for k, v in sorted(v.items())]
            else:
                return [repr(v)]
        args = [format(p, v) for p, v in zip(self.signature.parameters.values(), self.arguments.values())] 
        return '(' + ', '.join(itertools.chain.from_iterable(args)) + ')'

    def __repr__(self):
        '''
        >>> def callable(a, *args):
        ...     pass
        >>> signature(callable).bind(1, 2)
        BoundArguments(Signature([Parameter('a', 1), Parameter('args', 2)]), [('a', 1), ('args', (2,))])
        '''
        args = [repr(x) for x in self.arguments.items()]
        return 'BoundArguments({!r}, [{}])'.format(self.signature, ', '.join(args))
    
def signature(callable):
    """Convert a function into a Signature object.

    >>> str(signature(signature))
    '(callable)'
    >>> def some_function(a, b=1, c='x', *args, **kwargs):
    ...     pass
    >>> str(signature(some_function))
    "(a, b=1, c='x', *args, **kwargs)"

    """
    code = callable.__code__ if hasattr(callable, '__code__') else callable.func_code
    args = code.co_varnames[0:code.co_argcount]
    defaults = callable.func_defaults or []
    num_nondefaults = len(args) - len(defaults)
    params = [Parameter(x, Parameter.POSITIONAL_OR_KEYWORD) for x in args[0:num_nondefaults]]
    params += [Parameter(x, Parameter.POSITIONAL_OR_KEYWORD, d) for x, d in zip(args[num_nondefaults:], defaults)]
    if code.co_flags & 4:
        name = code.co_varnames[code.co_argcount]
        params.append(Parameter(name, Parameter.VAR_POSITIONAL))
    if code.co_flags & 8:
        name = code.co_varnames[code.co_argcount + (1 if code.co_flags & 4 else 0)]
        params.append(Parameter(name, Parameter.VAR_KEYWORD))
    return Signature(params)

        
def arg_list(f):
    """Get the argument list of a function or method. 
    
    >>> arg_list(arg_list)
    ['f']
    >>> def some_function(a, b=1, c='x', *args, **kwargs):
    ...     pass
    >>> arg_list(some_function)
    ['a', 'b=1', "c='x'", '*args', '**kwargs']
    """    
    return [str(x) for x in signature(f).parameters.values()]
        
def format_arg_list(f, sep=', '):
    """Format the argument list of a function or method. 
    
    >>> format_arg_list(format_arg_list)
    "f, sep=', '"
    >>> def some_function(a, b=1, c='x', *args, **kwargs):
    ...     pass
    >>> format_arg_list(some_function)
    "a, b=1, c='x', *args, **kwargs"
    """
    return signature(f).format(sep=sep)[1:-1]
    
def no_args():
    ""

def one_arg(x):
    "x"
    
def one_arg_default(x=1):
    "x=1"
    
def two_args(x, y):
    "x, y"
    
def two_args_default(x, y=1):
    "x, y=1"
    
def two_args_star_args(x, y, *args):
    "x, y, *args"
    
def two_args_star_kwargs(x, y, **kwargs):
    "x, y, **kwargs"
    
def two_args_star_args_kwargs(x, y, *args, **kwargs):
    "x, y, *args, **kwargs"

def default_str(x, y='hello'):
    "x, y='hello'"
    
class A(object):
    def __repr__(self):
        return 'A()'
    def method_no_args(self):
        "self"
    def method_one_arg(self, x):
        "self, x"
    def method_two_arg(self, x, y):
        "self, x, y"
    
def default_A(x, y=A()):
    "x, y=A()"        
    
@test([
    no_args,
    one_arg,
    one_arg_default,
    two_args,
    two_args_default,
    two_args_star_args,
    two_args_star_kwargs,
    two_args_star_args_kwargs,
    A.method_no_args,
    A.method_one_arg,
    A.method_two_arg,
    default_str,
    default_A,
])
def test_format_arg_list(f):
    assertEquals(f.__doc__, format_arg_list(f))
    
def _can_call_function(num_calling_args, num_args, num_defaults, has_varargs):
    """Determine if the number of args allow a call to take place.
    
    >>> _can_call_function(1, 2, 1, False)
    True
    >>> _can_call_function(3, 2, 1, False)
    False
    >>> _can_call_function(3, 2, 1, True)
    True
    """
    nondefaults = num_args - num_defaults
    return bool(num_calling_args >= nondefaults and \
          (num_calling_args <= num_args or has_varargs))

def _find_fn_in_script(script, file_name, fn_name):
    script = script.replace('\\r\\n', '\\n')
    c = ast.parse(script, file_name)
    fns = [x for x in c.body if isinstance(x, ast.FunctionDef)]
    fns = [fn for fn in fns if fn.name == fn_name]
    try:
        return fns[-1] # use the last one - last one wins in python
    except IndexError:
        raise ValueError("module %s has no function %r" % (file_name, fn_name))

def can_call_function_in_script(script, file_name, fn_name, num_calling_args):
    """Returns True if there is a function 'fn_name' in script which can be 
    called with num_calling_args. i.e. are the signatures compatible?
    """
    try:
        fn = _find_fn_in_script(script, file_name, fn_name)
    except ValueError:
        return False
    else:
        return _can_call_function(num_calling_args, len(fn.args.args), len(fn.args.defaults), bool(fn.args.vararg))


@test([
    ('def main(): pass', False),
    ('def main(a): pass', False),
    ('def main(a, b): pass', False),
    ('def main(a, b, c): pass', True),
    ('def main(a, b, c, d): pass', False),
    ('def main(a, b, c, d=0): pass', True),
    ('def main(*args): pass', True),
    ('def main(a, *args): pass', True),
    ('def main(a, b, *args): pass', True),
    ('def main(a, b, c, *args): pass', True),
    ('def main(a=0, b=0, c=0): pass', True),
    ('def main(a, b=0, c=0): pass', True),
    ('def main(a, b, c=0): pass', True),
    ('def main(a=0, b=0, c=0, *args): pass', True),
    ('def main(a, b=0, c=0, *args): pass', True),
    ('def main(a, b, c=0, *args): pass', True),
])
def test_can_call_function_in_script(defn, expected):
    assertEquals(expected, can_call_function_in_script(defn, '_script_.py', "main", 3))

def get_docstring(script, file_name, fn_name):
    return ast.get_docstring(_find_fn_in_script(script, file_name, fn_name)) 

@test([
    ('def fn(): \n    pass\n    "This isnt a doc string"\n', None),
    ('def fn(): \n    x = "This isnt a doc string"\n', None),
    ('def fn(): \n    "This is a doc string"\n', 'This is a doc string'),
    ('def fn(): \n    """This is a doc string"""\n', 'This is a doc string'),
    ('def fn(): \n    pass\n', None),
    ('def fnx(): \n    pass\n', ValueError("module _script_.py has no function 'fn'")),

])
def test_get_docstring(defn, expected):
    if isinstance(expected, Exception):
        assertRaisesWithMessage(type(expected), str(expected), get_docstring, defn, '_script_.py', "fn")
    else:
        assertEquals(expected, get_docstring(defn, '_script_.py', "fn"))


def can_call_function(f, num_calling_args):
    """Returns True if the calling f with num_calling_args wouldn't fail at 
    call time, i.e. are the signatures compatible?
    
    >>> import os
    >>> can_call_function(os.path.relpath, 0) # os.path.relpath(path [,start])
    False
    >>> can_call_function(os.path.relpath, 1)
    True
    >>> can_call_function(os.path.relpath, 2)
    True
    >>> can_call_function(os.path.relpath, 3)
    False
    """
    sig = signature(f)
    numargs = len([p for p in sig.parameters.values() if p.kind == Parameter.POSITIONAL_OR_KEYWORD])
    numdefs = len([p for p in sig.parameters.values() if p.default is not Parameter.empty])
    has_star_args = bool([x for x in sig.parameters.values() if x.kind == Parameter.VAR_POSITIONAL])
    return _can_call_function(num_calling_args, numargs, numdefs, has_star_args)
    
@test([
    (no_args, 0, True), 
    (no_args, 1, False), 
    (one_arg, 0, False), 
    (one_arg, 1, True), 
    (one_arg, 2, False), 
    (one_arg_default, 0, True),
    (one_arg_default, 1, True),
    (one_arg_default, 2, False),
    (two_args_star_args, 0, False),
    (two_args_star_args, 1, False),
    (two_args_star_args, 2, True),
    (two_args_star_args, 3, True),
    (two_args_star_args, 4, True),
])
def test_can_call_function(f, num_args, expected):
    assertEquals(expected, can_call_function(f, num_args))

def format_doc(s, indent=0):
    r"""Format the whitespace of a docstring so that it is *all* indented to the 
    correct level.
    
    This function needs to take care that the first line which may be empty,
    or may be a single line description followed by 
    indented text.
        
    >>> format_doc('this is a doc.\n    line 2.', 1)
    ' this is a doc.\n line 2.'
    >>> format_doc('single line', 1)
    ' single line'
    >>> format_doc('\n    this is a doc.\n    line 2.', 1)
    ' this is a doc.\n line 2.'
    >>> format_doc(' \n    this is a doc.\n    line 2.', 1)
    ' this is a doc.\n line 2.'
    >>> format_doc('this is a doc.\n        x\n    line 3.', 1)
    ' this is a doc.\n     x\n line 3.'
    >>> format_doc('this is a doc.\n        x\n    line 3.\n        this line indented and must stay so', 1)
    ' this is a doc.\n     x\n line 3.\n     this line indented and must stay so'
    """
    s = s.expandtabs(8)
    lines = s.split('\n')
    first = lines[0]
    lines = dedent("\n".join(lines[1:])).split("\n")
    if first.strip():
        lines.insert(0, first.strip())
    return "\n".join(" " * indent + line for line in lines).rstrip()
    
@test([
        ('''
        GetFullTextExtent(String string, Font font=None) ->
           (width, height, descent, externalLeading)

        Get the width, height, decent and leading of the text using the
        current or specified font.
        ''',
        '''GetFullTextExtent(String string, Font font=None) ->
   (width, height, descent, externalLeading)

Get the width, height, decent and leading of the text using the
current or specified font.'''),
])
def test_dont_strip_content_when_indenting_unusual(input, output):
    assertEqual(output, format_doc(input))

def format_signature(f, name=None, sep=', '):
    """Get the signature of a function including default arguments.
    
    If `name` is None the name is taken from f.__name__.
    
    >>> format_signature(format_signature)
    "format_signature(f, name=None, sep=', ')"
    >>> format_signature(format_signature, 'monty')
    "monty(f, name=None, sep=', ')"
    """
    sig = signature(f)
    return (name or f.__name__) + sig.format(sep)

def remove_self_from_signature(sig):
    try:
        a, b = sig.split("(", 1)
        self, args = b.split('self')
        if args.lstrip().startswith(','):
            args = args.lstrip()[1:].lstrip()
        return a + "(" + args
    except ValueError:
        return sig
        
@test([
    ('fnname(self)', 'fnname()'),
    ('fnname(self, a)', 'fnname(a)'),
    ('fnname(self , a)', 'fnname(a)'),
    ('fnname(a)', 'fnname(a)'),
])
def test_remove_self_from_signature(sig, exp):
    assertEquals(exp, remove_self_from_signature(sig))
        
def first_line_looks_like_signature(doc):
    lines = doc.lstrip().split("\n")
    return looks_like_signature(lines[0])

def pull_signature_from_doc(doc):
    """Extract the first line of a doc string."""
    lines = doc.lstrip().split("\n")
    return lines[0].lstrip(), "\n".join(lines[1:])


def format_function_info(function, doc=None, indent=4, name=None):
    r"""Get a description of the function/method, including signature and 
    docstring if present. 
    
    The returned string is suitable for usage as a sphinx
    function/method description :: 
    
         f.write('.. method:: %s\n\n' % format_function_info(f))
    
    If `doc` is None, the functions docstring is taken from function.__doc__.
    
    If `name` is None, the functions name is taken from function.__name__.
    
    If the method has documentation the docs will follow the signature 
    separatated by a blank line and indented by `indent` spaces.
    
    The signature is taken from the first line of the docstring if it looks
    like a signature (see :func:`looks_like_signature`), alternatively it is 
    derived by inspecting the actual signature of the docstring (including 
    defaults arguments).
    
    >>> format_function_info(pull_signature_from_doc)
    'pull_signature_from_doc(doc)\n\n    Extract the first line of a doc string.'
    
    >>> format_function_info(first_line_looks_like_signature)
    'first_line_looks_like_signature(doc)'
    
    """
    signature = format_signature(function, name).lstrip()
    doc = doc or function.__doc__
    if doc and first_line_looks_like_signature(doc):
        signature, doc = pull_signature_from_doc(doc)
    signature = remove_self_from_signature(signature)
    if doc:
        return signature + "\n\n" + format_doc(doc, indent)
    else:
        return signature

def format_call(func_or_name, args, kwargs):
    """
    >>> def foo(): pass
    
    >>> format_call(foo, [], {})
    'foo()'
    
    >>> format_call(foo, [None], {})
    'foo(None)'
    >>> format_call(foo, ['AString'], {})
    "foo('AString')"
    >>> format_call(foo, [], dict(param1=1))
    'foo(param1=1)'
    
    >>> format_call(foo, [1, 2, 3], {})
    'foo(1, 2, 3)'
    >>> format_call(foo, [], dict(abc=1, xyz=2, lmn=3, ghi=4))
    'foo(abc=1, ghi=4, lmn=3, xyz=2)'
    
    >>> format_call(foo, ['Larry', 'Curly', 'Mo'], dict(abc={'Dict': 'ionary'}, xyz=['List'], lmn=3))
    "foo('Larry', 'Curly', 'Mo', abc={'Dict': 'ionary'}, lmn=3, xyz=['List'])"
    """
    return "%s(%s)" % (getattr(func_or_name, "__name__", func_or_name), ", ".join(map(repr, args) + ["%s=%r" % x for x in sorted(kwargs.iteritems())]))

def looks_like_signature(s):
    """Returns true if the string looks like a (possibly annotated) signature of 
    a function, used to override the generated signature in docstrings.
    
    >>> looks_like_signature('FnName(sometype argname=const)') # wx style annotations
    True
    >>> looks_like_signature('FnName(argname : sometype =const)') # py 2.7 annotations
    True
    >>> looks_like_signature('add_line(x, [y = something()])') # sphinx style defaults
    True
    >>> looks_like_signature('FnName(arg1) -> Type object') # py 2.7 and wx return type annotations
    True
    >>> looks_like_signature('This function (does something)')
    False
    """
    try:
        parens = s.index('('), s.rindex(')')
        fnname = s[0:parens[0]]
        if parens[0] > parens[1] or \
           not re.match(r'^\w+$', fnname):
            return False
        #~ arg_wx = r"(?:\w+\s+)?\w+"
        #~ # strictly speaking this isn't correct because the annotation is any expression
        #~ # but an identifier should be enough
        #~ arg_py = r"\w+(?:\s*:\s*\w+)"
        #~ default = r"""(?:'[^']*'|"["[^"]"|\w+)"""
        #~ arg = "(?:(?:" + arg_wx + ")|(?:" + arg_py + "))" + r"(?:\s*=\s*" + default + ")?"
        #~ returntype = r"(?:->\s*.*)?"
        #~ re_sig = re.compile(r"\w+\s*\(\s*(?:" + arg + r")?(?:\s*,\s*" + arg + r")*\s*\)\s*" + returntype)
        #~ return bool(re_sig.match(s))
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    test.main()
