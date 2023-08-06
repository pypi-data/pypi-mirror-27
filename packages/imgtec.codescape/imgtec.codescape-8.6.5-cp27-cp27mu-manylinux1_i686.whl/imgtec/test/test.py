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

"""Test is an extension to unittest. It makes creating function level tests much easier.

Usage : 

.. sourcecode :: python

    from imgtec.test import *
    
    @test
    def mytest():
       assertEqual(4, 2*2)

    @test(['*', '+'])
    def mytest(operator):
        assertEqual(4, eval('2' + operator + '2'))

    @test([
            ('-', 3, 4, 1),
            test.data('*', 4),
            test.data('+', 5, val2 = 3),
        ])
    def mytest(operator, expected, val1 = 2, val2 = 2, ):
        assertEqual(expected, eval(str(val1) + operator + str(val2)))

    if __name__ == "__main__": 
        test.main()
"""
__docformat__ = "restructuredtext en"

import doctest, difflib, unittest
import collections, inspect, os, re, sys, time, types, traceback
from textwrap import dedent

__all__ = ['test', 'skip', 'skipTest',
           'fail', 'failIf', 'failUnless', 'failUnlessRaises', 'failUnlessEqual', 
           'failIfEqual', 'failUnlessAlmostEqual', 'failIfAlmostEqual',
           'assertEqual', 'assertEquals', 'assertNotEqual', 'assertNotEquals',
           'assertAlmostEqual', 'assertAlmostEquals', 'assertNotAlmostEqual',
           'assertNotAlmostEquals', 'assertRaises', 'assertRaisesWithMessage',
           'assert_', 'assertTrue', 'assertFalse', 'assertIn', 'assertNotIn',
           'assertGreaterThan', 'assertLessThan', 'assertGreaterEqual',
           'assertLessEqual', 'assertIs', 'assertIsInstance', 'assertIsNone',
           'assertIsNot', 'assertIsNotNone', 'assertItemsEqual', 'assertListEqual', 
           'assertMultiLineEqual', 'assertLess', 'assertNotIsInstance', 
           'assertNotRegexpMatches', 'assertRaisesRegexp', 'assertRegexpMatches',
           'assertDictContainsSubset', 'assertSequenceEqual', 'assertSetEqual',
           'assertTupleEqual', 'assertDictEqual', 'assertGreater', 'failureException',
           ]
           
# notice that run_all, main, data are not exported when using import *
# this is deliberate, so that the user must do test.data/test.main/test.run_all.
# By keeping the number of exported symbols small, we reduce the risk of 
# interfering with user code.

_suites = {}
"""dict of suites indexed by module for which all test functions are added to."""

__IMG_Test_HideCallStack    =	True
"""True to hide callstack entries belonging to the test framework."""

failureException = unittest.TestCase.failureException

hide_skipped = False

class Skipped(Exception):
    """Exception to be raised when a test is to be skipping while running the test """

def hexstr(x):
    r"""As str(x) but will prefer hex(x) if x is an integer type, or list of integer types.
    
    >>> hexstr(1)
    '0x1'
    >>> hexstr(1L)
    '0x1L'
    >>> hexstr('string')
    'string'
    >>> hexstr('str\x00ing')
    'str\\x00ing'
    >>> hexstr([0, 1, 2])
    '[0x0, 0x1, 0x2]'
    >>> hexstr((0, 1, 2))
    '(0x0, 0x1, 0x2)'
    >>> hexstr({'mouse': 0, 'beaver': 1, 'badger': 2})
    "{'badger': 0x2, 'beaver': 0x1, 'mouse': 0x0}"
    >>> class A(list):  # types derived from list/dict/tuple should be repr'd
    ...    def __repr__(self):
    ...       return 'A({0})'.format(', '.join('%08X' % x for x in self))
    >>> hexstr(A([0xabc, 0xdef, 0x132]))
    'A(00000ABC, 00000DEF, 00000132)'
    """
    if type(x) == list: 
        return "[" + ", ".join(hexstr(item) for item in x) + "]"
    elif type(x) == tuple: 
        return "(" + ", ".join(hexstr(item) for item in x) + ")"
    elif type(x) == dict:
        keys = x.keys()
        keys.sort()
        return "{" + ", ".join('%r: %s' % (hexstr(k), hexstr(x[k])) for k in keys) + "}"
    elif type(x) == int:
        return hex(x)
    elif sys.hexversion < 0x03000000 and type(x) == long: 
        return hex(x)
    elif sys.hexversion < 0x03000000 and type(x) == unicode:
        return x.encode('iso-8859-1')
    elif type(x) == str:
        return x.encode('string_escape')
    else:
        return repr(x)
    
class ArgsType(object): 
    """A class that stores both the positional and keyword arguments of a future 
    function call.
    """
    def __init__(self, *args, **kwargs): 
        self.args = args
        self.kwargs = kwargs
        
    def __repr__(self):
        params = [hexstr(x) for x in self.args]
        kwparams = [name + "=" + hexstr(x) for name, x in self.kwargs.items()]
        return ",".join(params + kwparams)
        
def data(*args, **kwargs): 
    """Allows passing of both positional args and keyword args to Function.
    
    e.g.
    
    from imgtec.test import *
    
    @test([
            test.data(0, arg2=3),
            test.data(0, arg1=3),
            test.data(0),    
          ])
    def mytest(arg0, arg1=0, arg2=0): 
        pass
    
    """
    return ArgsType(*args, **kwargs)
    

def _convert_params(a):
    if isinstance(a, tuple):
        return data(*a)
    elif not isinstance(a, ArgsType): 
        return data(a)
    return a

def _convert_data(data): 
    if len(data) == 0: 
        raise TypeError("Test/Suite parameterisation must contain at least one item")
    return [_convert_params(a) for a in data]    
        
from imgtec.lib.backwards import next    

class StatefulTestSuite(unittest.TestSuite):
    """Give setUp and tearDown functionality to a TestSuite."""
    def __init__(self, modulename):
        unittest.TestSuite.__init__(self)
        self.suiteSetUp     = None
        self.suiteTearDown  = None
        self.modulename     = modulename
        self.suiteData      = [data()]
        self.suiteDataIndex = 0
        self.setUpGenerator = None
        self.testexprs      = []
        
    def _setUp(self, data): 
        self.suiteState = self.suiteSetUp and self.suiteSetUp(*data.args, **data.kwargs)
        if isinstance(self.suiteState, types.GeneratorType):
            if self.suiteTearDown is not None: 
                raise TypeError("suiteTearDown defined, but suiteSetUp is a generator.")
            self.setUpGenerator = self.suiteState
            self.suiteState = next(self.setUpGenerator)
                    
    def _tearDown(self): 
        if self.setUpGenerator: 
            try: 
                next(self.setUpGenerator)
            except StopIteration: 
                pass
            else: 
                raise TypeError("suiteSetUp generator did not stop")
        elif self.suiteTearDown: 
            args = () 
            if self.suiteState is not None:
                args = (self.suiteState,)
            self.suiteTearDown(*args)
        self.suiteState = None
        
    def _wrapped_run(self, result, debug=False):
        # this is needed for python 2.7, which doesn't call run, instead it 
        # calls _wrapped_run,  in turn our run then needs to call 
        # unittest.TestSuite._wrapped_run instead of
        # unittest.TestSuite.run because otherwise we have infinite recursion
        return self.run(result, unittest.TestSuite._wrapped_run)
        
    def run(self, result, runner=unittest.TestSuite.run): 
        """run the tests, calling setUp and tearDown appropriately."""
        oldcwd = os.getcwd()
        testdir = get_module_path(self.modulename)
        if testdir:
            os.chdir(testdir)
        try:
            for self.suiteDataIndex, data in enumerate(self.suiteData): 
                self._setUp(data)
                try: 
                    runner(self, result)
                finally: 
                    self._tearDown()
        except Skipped as err:
            result.addSkip(self.modulename, err)
        finally:
            os.chdir(oldcwd)
            
    def __iter__(self):
        def should_run(testname):
            testname = testname.split('(', 1)[0] # strip paramlist
            return any(e.match(testname) for e in self.testexprs)
        to_run = [x for x in self._tests if should_run(str(x))]
        to_run.sort(key=str)
        return iter(to_run)
                  
    def __str__(self): 
        extra = ''
        if len(self.suiteData) != 1:
            #extra = "[%d](%r)" % \
            #    (self.suiteDataIndex, self.suiteData[self.suiteDataIndex])
            extra = "[%d]" % (self.suiteDataIndex,)
        return self.modulename + extra 

def get_suite(modulename): 
    try: 
        return _suites[modulename]
    except KeyError:
        x = StatefulTestSuite(modulename)
        _suites[modulename] = x
        return x
       
def _suiteSetUpTearDown(fn, name): 
    suite = get_suite(fn.__module__)
    if getattr(suite, name): 
        raise TypeError("More than one " + name + "function defined")
    setattr(suite, name, fn)
    def wrapper(*args, **kwargs):
        raise TypeError("Cannot call " + name + " function directly")
    wrapper.__module__ = fn.__module__
    wrapper.__name__   = fn.__name__
    wrapper.__doc__    = fn.__doc__
    return wrapper

def suiteSetUp(fn_or_params): 
    """Mark a function to act as the suiteSetUp or suiteTearDown function.
    
    The suiteSetUp function is run just before the tests in the module are run,
    and the suiteTearDown is run just after.  In both functions, the current 
    working directory is set to the module path.
    
    .. note :: 
    
        1. Only one suiteSetUp and one suiteTearDown may be used per module.
        2. suiteSetUp can be passed either a normal function or a generator like 
           contextlib.contextmanager.
        3. If a generator is used, suiteTearDown must not be used.
        4. If the suiteSetUp function returns/yields a value (other than None) 
           that value is called the suiteState.  The suiteState is then passed 
           to the suiteTearDown function (if defined), and to all tests in the 
           module as their first parameter (test parameterisation data 
           follows the suiteState).
        5. The suiteSetUp decorator can be called with parameterised data, 
           (in exactly the same way as @test).  This calls all tests to be run
           once for each set of parameters. The suiteSetUp (and suiteTearDown)
           is called each set of parameters.
           
    .. sourcecode :: python
           
        # Separate setUp/tearDown functions
        
        @test.suiteSetUp
        def initTests(): 
            return open('filename')
            
        @test.suiteTearDown
        def uninitTests(f): 
            f.close()
        
        @test
        def mytest(f): 
            assertEquals("data", f.read(4))
            
        
        # Using a generator setUp function
        
        @test.suiteSetUp
        def initTests(): 
            f = open('filename')
            yield f
            f.close()
            
        @test
        def mytest(f): 
            assertEquals("data", f.read(4))
            
      
        # Using a generator function without returning a value
        
        @test.suiteSetUp
        def initTests(): 
            with open('filename') as f: 
               f.write('data')
            yield
            os.remove('filename')
            
        @test
        def mytest(): # note we do *not* have a parameter here 
            assertTrue(os.path.exists('filename'))
            
        # Using a generator function with parameterised suite data
        
        @test.suiteSetUp(['filename1',
                          'filename2'])
        def initTests(filename): 
            with open(filename) as f: 
               f.write('data')
            yield f
            os.remove(filename)
            
        @test
        def mytest(f):
            assertTrue(os.path.exists(f))            
    
    """
    if hasattr(fn_or_params, '__call__'):
        return _suiteSetUpTearDown(fn_or_params, 'suiteSetUp')
    else: 
        suiteData = fn_or_params
        def wrapper(fn):
            get_suite(fn.__module__).suiteData = _convert_data(suiteData)
            return suiteSetUp(fn)
        return wrapper

def suiteTearDown(fn): 
    return _suiteSetUpTearDown(fn, 'suiteTearDown')
suiteTearDown.__doc__ = suiteSetUp.__doc__

def get_module_path(modulename): 
    try: 
        file = sys.modules[modulename].__file__
    except (AttributeError, KeyError): 
        # for some reason the __main__ module in codescape doesn't have a 
        # __file__ attribute, nor do builtins, if so just use the cwd as it will
        # be correct in codescape.  Similarly if we try to import ourself, we 
        # are not in sys.modules, this is just more weird codescape embedded
        # python behaviour, the best we can do is just return cwd.  It is always
        # the right answer in these situations anyway
        return os.getcwd()
    else: 
        return os.path.abspath(os.path.dirname(file))

class FunctionRunner(unittest.TestCase):
    """Wrap a function to allow it to be called from the unittest module without
    it being necessary to derive from TestCase directly, but in this case do not
    require that there is a 'test' parameter.

    However, if a suiteSetUp function ran and returned something, then that
    will be passed as the first parameter.
    """
    def __init__(self, f, name, data, setUp, tearDown):
        self.f = f
        self.name = name
        self.data = data
        if setUp:
            self.setUp = setUp
        if tearDown: 
            self.tearDown = tearDown
        self.suite = get_suite(f.__module__)
        super(FunctionRunner, self).__init__(self.name)
        
    def __getattr__(self, name):
        if name == self.name:
            return self.runTest
        else: 
            raise AttributeError(name)
            
    def runTest(self):
        prefix = self._prefixArg()
        if prefix is not None: 
            self.f(prefix, *self.data.args, **self.data.kwargs)
        else: 
            self.f(*self.data.args, **self.data.kwargs)
            
    def shortDescription(self):
        return '{}.{}'.format(self.suite, self.name)

    def __str__(self): 
        return "%s.%s(%s)" % (self.suite, self.name, self.data)
        
    def _prefixArg(self):
        return self.suite.suiteState
        
def _make_test_case(TestClass, module):
    class LocalTestClass(TestClass):
        pass
    LocalTestClass.__name__ = module if module == '__main__' else ''
    LocalTestClass.__module__ = module
    return LocalTestClass
                
def decorate_test(fn_or_params, TestClass, setUp=None, tearDown=None):
    """Mark a function as a test, and add it to this modules suite."""
    if hasattr(fn_or_params, '__call__'):
        fn = fn_or_params
        suite = get_suite(fn.__module__)
        LocalTestClass = _make_test_case(TestClass, fn.__module__)
        suite.addTest(LocalTestClass(fn, fn.__name__, data(), setUp, tearDown))
        return fn_or_params
    elif fn_or_params is None: 
        return lambda fn : decorate_test(fn, TestClass, setUp, tearDown)
    else:
        params = fn_or_params
        def decorator(fn):
            suite = get_suite(fn.__module__)
            convparams = _convert_data(params)
            LocalTestClass = _make_test_case(TestClass, fn.__module__)
            for idx, a in enumerate(convparams):
                suite.addTest(LocalTestClass(fn, fn.__name__ + "[" + str(idx) + "]", a, setUp, tearDown))
            fn.params = convparams # this is so that functions can share params easily
            return fn
        return decorator

def get_file_line_thing_from_name(name):
    """Returns (filename, linenum, thing) when given a 'module.object.name'
    string.
    
    >>> file, line, thing = get_file_line_thing_from_name('doctest.DocTestSuite')
    >>> os.path.basename(file), line != 0, thing
    ('doctest.py', True, 'DocTestSuite')
    """
    objectname = name
    things = []
    while 1:
        try:
            mod = sys.modules[objectname]
        except KeyError:
            pass # probably tried to get a 'thing' as a module
        else:
            thing = mod
            try:
                for thingname in reversed(things):
                    thing = getattr(thing, thingname)
            except AttributeError:
                pass # probably tried to get a module from a thing!
            else:
                try:
                    line = inspect.getsourcelines(thing)[1]
                except TypeError:
                    line = 1 # never mind

                if isinstance(thing, types.ModuleType):
                    thing = '<module>'
                else:
                    thing = ".".join(reversed(things))
                file =  mod.__file__
                if file.endswith(".pyc"):
                    file = file[:-1]
                return file, line, thing
        try:
            objectname, thing  = objectname.rsplit('.', 1)
        except ValueError:
            raise NameError("name %r is not defined" % name)
        things.append(thing)
    
        
def decode_doctest_syntax_error(msg):
    """Attempt to convert a rather vague doctest syntax error into file/linenum."""
    m = re.search(r"line (\d+) of the docstring for (\S+) (.*)", msg)
    if m:
        try:
            line, thing, reason = m.groups()
            line = int(line)
            # we now have a name, something like a.b.c.d
            # some of a, b, c are module names, some are parts in a module, 
            # figure out which
            file, lineno, thing = get_file_line_thing_from_name(thing)
            line += lineno
            msg = "docstring %s\n  File \"%s\", line %d, in %s" % \
                    (reason, file, line, thing)
        except Exception:
            # so many things can go wrong there that let's just catch any
            # exceptions and use the original message
            e = sys.exc_info()[1]
            print("Warning, failed to decode doctest syntax error because %s, please notify imgtec module maintainer" % (e,))
    
    return msg    
    
def _fixup_doctest_case(test, module):
    name = test._dt_test.name
    class LocalTestClass(doctest.DocTestCase):
        def shortDescription(self):
            return name
    test.__class__ = LocalTestClass
    LocalTestClass.__name__ = name.rsplit('.', 1)[1]
    LocalTestClass.__module__ = module
                
                
def create_failing_test_due_to_import(modulename, message):
    def failing_test_due_to_import(*args, **kwargs):
        raise Skipped(message)
    try:
        modulename, classname = modulename.rsplit('.', 1)
    except ValueError:
        modulename, classname = modulename, modulename
    failing_test_due_to_import.__name__ = classname
    failing_test_due_to_import.__module__ = modulename
    return test(failing_test_due_to_import)
        
def get_module_suite(modulename, skip_unittest=False): 
    """Return a suite containing all of the tests in the given module.  
    
    This includes 
    + doctests
    + @test decorated functions
    + classes derived from TestCase
    """
    # do the unittest_suite first so that the modules are loaded...
    suite = get_suite(modulename)
    unittest_suite = None
    try: 
        if not skip_unittest:
            unittest_suite = unittest.TestLoader().loadTestsFromName(modulename)
    except (AttributeError, ImportError, TypeError):
        e = sys.exc_info()[1]
        tb = ''.join(traceback.format_tb(sys.exc_info()[2]))
        message = "Skipped : {} due to error during import : {}\n{}".format(modulename, e, tb)
        #unittest_suite = create_failing_test_due_to_import(modulename, message)
    else:     
        try: 
            doctest_suite = doctest.DocTestSuite(modulename)
            for test in doctest_suite:
                _fixup_doctest_case(test, modulename)
        except ValueError:
            e = sys.exc_info()[1]
            # don't worry if there are no doctests in the module, this is a bit 
            # brittle to search the args of e but doctest doesn't raise an 
            # exception that we can catch by type directly
            if 'has no docstrings' not in str(e) and 'has no tests' not in str(e):
                raise ValueError(decode_doctest_syntax_error(str(e)))
        else:
            suite.addTest(doctest_suite)
    if unittest_suite:
        suite.addTest(unittest_suite)
    return suite
    
class IMGTextTestResult(unittest.TextTestResult):
    """Hides irrelevant callstack from this module."""
    def _is_relevant_tb_level(self, tb):
        return '__unittest' in tb.tb_frame.f_globals or \
                tb.tb_frame.f_globals.get('__IMG_Test_HideCallStack', False)

class TextTestResultWithSkip(IMGTextTestResult):
    def getDescription(self, test):
        return test.shortDescription() or str(test)

    def addError(self, test, err):
        if err[0] is Skipped:
            self.addSkip(test, err[1])
        else:
            if self.failfast:
                self.stop()
            super(TextTestResultWithSkip, self).addError(test, err)

    def printSkippedList(self, flavour, skipped_results):
        self.stream.writeln(self.separator1)
        for test, err in skipped_results:
            self.stream.writeln('%s: %s %s' % (flavour, err, self.getDescription(test)))
        self.stream.writeln(self.separator2)

    def printErrors(self):
        if self.dots or self.showAll:
            self.stream.writeln()
        if not hide_skipped:
            self.printSkippedList('SKIPPED', self.skipped)
        self.printErrorList('ERROR', self.errors)
        self.printErrorList('FAIL', self.failures)
        
class TextTestResult(TextTestResultWithSkip):
    pass
        
class TextTestRunner(unittest.TextTestRunner):
    """Extends TextTestRunner so that it returns our own result."""
    resultclass = TextTestResult

try:
    import junit_xml
except ImportError:
    class JUnitXml(object):
        def TestSuite(self, *args, **kwargs):
            raise RuntimeError('Please install junit_xml to get xml error reporting')
        TestCase = TestSuite
    junit_xml = JUnitXml()

class XMLTestResult(TextTestResultWithSkip):
    def __init__(self, *args, **kwargs):
        super(XMLTestResult, self).__init__(*args, **kwargs)
        self.xml_suite = junit_xml.TestSuite('suitename')

    def startTest(self, test):
        self.buffer = True
        super(XMLTestResult, self).startTest(test)
        classname, name = test.shortDescription().rsplit('.', 1)
        self.xml_suite.test_cases.append(junit_xml.TestCase(name, classname))
        self.__start = time.time()
        
    def _add_info(self, test, err, errtype):
        tc = self.xml_suite.test_cases[-1]
        if err[0] is Skipped:
            tc.add_skipped_info(err[1])
        else:
            emsg = traceback.format_exception_only(err[0], err[1])[0].strip().replace('\n', ' ')
            getattr(tc, 'add_{}_info'.format(errtype))(emsg, self._exc_info_to_string(err, test))
        
    def addError(self, test, err):
        self._add_info(test, err, 'error')
        super(XMLTestResult, self).addError(test, err)
        
    def addFailure(self, test, err):
        self._add_info(test, err, 'failure')
        super(XMLTestResult, self).addFailure(test, err)

    def stopTest(self, test):
        tc = self.xml_suite.test_cases[-1]
        tc.elapsed_sec = time.time() - self.__start
        if self.buffer:
            tc.stdout, tc.stderr = sys.stdout.getvalue(), sys.stderr.getvalue()
        else:
            tc.stdout, tc.stderr = '(not collected)', '(not collected)'
        super(XMLTestResult, self).stopTest(test)
        
    def save_xml(self, path, suitename, postfix):
        path = os.path.abspath(path)
        if not suitename:
            suitename = os.path.basename(os.path.dirname(path))
        for tc in self.xml_suite.test_cases:
            tc.name += postfix
            tc.classname = suitename + '.' + tc.classname
        suitename += postfix
        self.xml_suite.name = suitename
        path = os.path.join(path, 'TEST-{}.xml'.format(suitename))
        print 'Writing XML test report to {}'.format(path)
        try:
            os.mkdir(os.path.dirname(path))
        except EnvironmentError as e:
            pass
        with open(path, 'wb') as f:
            f.write(self.xml_suite.to_xml_string([self.xml_suite]))
           
class XMLTestRunner(unittest.TextTestRunner):
    """Extends TextTestRunner so that it returns our own result."""
    resultclass = XMLTestResult

def file_to_modulename(file):
    modulename = os.path.splitext(file)[0].replace(os.path.sep, '.')
    if modulename.startswith(".."):
        modulename = modulename[2:]
    if modulename.startswith("."):
        modulename = modulename[1:]
    return modulename
    
def ext_is(file, ext): 
    return os.path.splitext(file)[1].lower() == ext
    
def run_all(recursive=True, verbose=False, runner=None):
    """Call run_all() to run all tests in the entire directory tree 
    starting at current path if no path is specified.
    
    If recursive is False, only modules in the current directory are searched, 
    not sub-directories.
    
    Returns the number of failures + number of errors, so that the result 
    can be passed directly to sys.exit.
    """
    dir_py_count = {} # dict of dir name and total number of python files under it.
    init_py_paths = []
    try: 
        verbosity = 1
        if verbose:
            verbosity = 2
        runner = runner or TextTestRunner(verbosity=verbosity)
        if recursive: 
            modulenames = []
            for root, dirs, files in os.walk('.'):
                if 'CVS' in dirs: dirs.remove('CVS')
                if '.svn' in dirs: dirs.remove('.svn')

                # search for .py files, and add them to the list of modulenames
                files = [os.path.join(root, f) for f in files if ext_is(f, ".py")]
                modulenames.extend(file_to_modulename(f) for f in files)
                    
                # update dict of py counts
                if files:
                    local_root = root
                    while local_root:
                        modname = file_to_modulename(local_root)
                        dir_py_count[modname] = dir_py_count.get(modname, 0) + len(files)
                        local_root, _ = os.path.split(local_root)

                # if directories don't have a __init__.py then we cannot import them as packages.
                # this is a highly stupid aspect of Python's package system if you ask me.
                skip = []
                for dir in dirs:
                    if '.' in dir: 
                        skip.append(dir)
                    elif os.path.exists(os.path.join(root, dir, '__skiptests__.py')):
                        skip.append(dir)
                    else:
                        init_py_path = os.path.join(root, dir)
                        if not os.path.exists(os.path.join(init_py_path, '__init__.py')):
                            init_py_paths.append(init_py_path)
                for dir in skip:
                    dirs.remove(dir)
            
            temp, init_py_paths = init_py_paths, []
            for init_py_path in temp:
                packagename = file_to_modulename(init_py_path)
                if packagename in dir_py_count and dir_py_count[packagename]:
                    try: 
                        open(os.path.join(init_py_path, '__init__.py'), 'w').close()
                        init_py_paths.append(init_py_path)
                    except IOError: 
                        print("Skipped : %s because couldn't create __init__.py" % (os.path.join(root, dir),))
                        modulenames = [m for m in modulenames if not m.startwith(packagename + '.')]
                            
        else: 
            modulenames = [file_to_modulename(f) for f in os.listdir('.') if ext_is(f, '.py')]
                
        return main(*modulenames, **dict(runner=runner, verbose=verbose))
        
    finally:
        for init_py_path in init_py_paths:
            try: 
                os.remove(os.path.join(init_py_path, '__init__.py'))
            except OSError: 
                pass
            try: 
                os.remove(os.path.join(init_py_path, '__init__.pyc'))
            except OSError: 
                pass
        
RunAll = run_all

def get_argument_parser(**kwargs):
    """Return an argparse.ArgumentParser instance.  This can be used to extend the 
    command line interface of the calling test module.
    
      from imgtec.test import *
      
      parser = test.get_argument_parser()
      parser.add_argument('--target', help='Specify a target to connect to')
      args = parser.parse_args()
      # do something with args.target here...
      test.main(parsed_args=args)
      
    """
    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=
    dedent(r'''
    If no expressions are specified then all tests are run.  If a module name 
    needs to be specified it should be separated from the test name using a ':'.  
    If no module name is specified __main__ is assumed.  For example :: 
    
        run_tests.py --verbose testBasics "advanced:test(Read|Write)Byte"

    The expressions are regular expressions and are matched case-insensitively 
    against the whole of the test name, so testRead will NOT match testReadByte. 
    To match both testRead and testReadByte add .* to the expression.
    
    Tests with parameterised data also have the param index appended in square brackets.  
    So testRead\[0\] will match only the first instance of testRead. 
    
    Note that the module name may also be a regular expression, so packages will need the .
    to be escaped. e.g. "package\.module:testname".
    '''), **kwargs)
    parser.add_argument('exprs', nargs='*', help='regexes to match for test names to be run.')
    parser.add_argument('--verbose', '-v', action='store_true', help='display test names as they are run')
    parser.add_argument('--xml', '-x', action='store_true', help='output jUnit xml reports')
    parser.add_argument('--xml-dir', type=str, default='test-reports', help='Directory for jUnit xml reports')
    parser.add_argument('--xml-suite', type=str, default='', help='Suite name for jUnit xml reports (defaults to parent of xml-dir)')
    parser.add_argument('--xml-postfix', type=str, default='', help='Postfix all test names (e.g. with arch)')
    parser.add_argument('-p', '--print-tests', action='store_true', help='Print all tests in test script')
    return parser

def parse_cmdline_args(args):
    """Parse command line arguments for common test suite arguments."""
    try:
        parser = get_argument_parser()
    except ImportError:
        if len(args) > 1:
            print "Python 2.6 does not support argparse, so no command line args are supported"
    else:
        return parser.parse_args(args)
        
def _format_testexprs(exprs):
    if exprs:
        def format_modulename(expr):
            if ':' in expr:
                modname, expr = expr.split(':')
            else:
                modname, expr = '__main__(?:\[\d+\])?', expr
            return r'%s\.%s$' % (modname, expr)
        return [format_modulename(s) for s in exprs]
    return ['.*']
            
def iterate_tests(accumulator):
    for modulename, suite in _suites.iteritems():
        def runner(test_suite, results, *args, **kargs):
            try:
                for test_case in test_suite:
                    runner(test_case, results)
            except TypeError:
                accumulator(str(test_suite), test_suite)
        results = None
        suite.suiteSetUp     = None
        suite.suiteTearDown  = None
        suite.run(results, runner)

def get_test_list():
    result = []
    iterate_tests(lambda name, test_case: result.append(name))
    result.append('')
    return result

def print_tests(output=sys.stdout):
    output.write('\n'.join(get_test_list()))

def run(*modulenames, **kwargs):
    """Call this to call all of the @test decorated functions, doctests
    and unittests.TestCase derived classes in the specified module, (which 
    defaults to the current module).
    
    Returns a unittest.TestResult instance that can be queried for failures, 
    errors, and skipped.
    
    To get a simple fn that returns fails+errors so that the result 
    can be passed directly to sys.exit use test.main.
    """
    skip_unittest = 'skip_unittest' in kwargs
    global hide_skipped
    hide_skipped = kwargs.get('hide_skipped', False)
    args = kwargs.get('parsed_args', None)
    if not args:
        args = parse_cmdline_args(kwargs.get('args', sys.argv[1:]))
    try:
        runner = kwargs['runner']
    except KeyError:
        if args.xml:
            import junit_xml
            cls = XMLTestRunner
        else:
            cls = TextTestRunner
        runner = cls(stream=sys.stderr, failfast=getattr(args, 'failfast', False))
    verbose=args and args.verbose
    testexprs = _format_testexprs(args and args.exprs)
    testexprs = [re.compile(x) for x in testexprs]
    verbose = kwargs.get('verbose', verbose)
    if verbose:
        runner.verbosity = 2
    master_suite = unittest.TestSuite()
    for modulename in modulenames or ['__main__']:
        try:
            if verbose:
                print("Adding module %s" % (modulename,))
            suite = get_module_suite(modulename, skip_unittest)
            suite.testexprs = testexprs
            suite._tests.sort(key=str)
            master_suite.addTest(suite)
        except Exception:
            print("Exception whilst loading module %s:" %(modulename ,))
            raise
            
    if args and args.print_tests:
        print_tests()
        for modulename in modulenames or ['__main__']:
            del _suites[modulename]
        return

    result = runner.run(master_suite)
    if args.xml:
        result.save_xml(args.xml_dir, args.xml_suite, args.xml_postfix)
    for modulename in modulenames or ['__main__']:
        del _suites[modulename]
    return result
        
def main(*modulenames, **kwargs):
    """Call this to call all of the @test decorated functions, doctests
    and unittests.TestCase derived classes in the specified module, (which
    defaults to the current module).

    Returns the number of failures + number of errors, so that the result
    can be passed directly to sys.exit.

    Add this to the end of a module to make it unittestable on running, e.g. :

    .. sourcecode :: python
        from imgtec.test import *
        import sys

        ... tests ...

        if __name__ == "__main__":
            sys.exit(test.main())
    """
    result = run(*modulenames, **kwargs)
    if result is not None:
        return len(result.failures) + len(result.errors)

# assertions, these are the same as the unittest ones for the most part, except 
# that they are free functions not members of the unittest.TestCase class.
# Also the error message for assertEqual has been improved.

def skipTest(msg=None):
    """Skip the currently running test without registering either a success or failure.
    
    A separate list of skipped tests is maintained.
    """
    raise Skipped(msg)
skip=skipTest

def fail(msg=None):
    """Fail immediately, with the given message."""
    raise failureException(msg)

def assertFalse(expr, msg=None):
    "Fail the test if the expression is true."
    if expr: raise failureException(msg)

def failUnless(expr, msg=None):
    """Fail the test unless the expression is true."""
    if not expr: raise failureException(msg)

def assertIn(first, second, msg=None):
    """Fails if first is not present in second."""
    assertTrue(first in second, \
        msg or '%r expected to be found in %r' % (first, second))

def assertNotIn(first, second, msg=None):
    """Fails if first is present in second."""
    assertTrue(first not in second, \
        msg or '%r not expected to be found in %r' % (first, second))

class _AssertRaisesContext(object):
    """A context manager used to implement TestCase.assertRaises method."""

    def __init__(self, expected, expected_regexp=None):
        self.expected = expected
        self.expected_regexp = expected_regexp
        self.exception = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is None:
            try:
                exc_name = self.expected.__name__
            except AttributeError:
                exc_name = str(self.expected)
            raise failureException(
                "%s not raised" % (exc_name,))
        if not issubclass(exc_type, self.expected):
            # let unexpected exceptions pass through
            return False
        self.exception = exc_value # store for later retrieval
        if self.expected_regexp is None:
            return True

        expected_regexp = self.expected_regexp
        if isinstance(expected_regexp, basestring):
            expected_regexp = re.compile(expected_regexp)
        if not expected_regexp.search(str(exc_value)):
            raise failureException('"%s" does not match "%s"' %
                     (expected_regexp.pattern, str(exc_value)))
        return True


def assertRaises(excClass, callableObj=None, *args, **kwargs):
    """Fail unless an exception of class excClass is thrown by callableObj
    when invoked with arguments args and keyword arguments kwargs. If a
    different type of exception is thrown, it will not be caught, and the
    test case will be deemed to have suffered an error, exactly as for an
    unexpected exception.
    
    If called with callableObj omitted or None, will return a
    context object used like this::

        with self.assertRaises(SomeException):
            do_something()

    The context manager keeps a reference to the exception as
    the 'exception' attribute. This allows you to inspect the
    exception after the assertion::

        with self.assertRaises(SomeException) as cm:
           do_something()
        the_exception = cm.exception
        self.assertEqual(the_exception.error_code, 3)
        
    """
    if callableObj is None:
        return _AssertRaisesContext(excClass)
    try:
        callableObj(*args, **kwargs)
    except excClass:
        return

    if hasattr(excClass,'__name__'):
        excName = excClass.__name__
    else:
        excName = str(excClass)
    raise failureException, "%s not raised" % excName 
    
def assertRaisesWithMessage(excClass, message, callableObj=None,  *args, **kwargs):
    """Fail unless an exception of class excClass is thrown by callableObj
    when invoked with arguments args and keyword arguments kwargs. 
    If a different type of exception is thrown, it will not be caught, and the
    test case will be deemed to have suffered an error, exactly as for an
    unexpected exception.
    """
    return assertRaisesRegexp(excClass, re.escape(message), callableObj,  *args, **kwargs)

def assertRaisesRegexp(excClass, exp_regexp, callable_obj=None, *args, **kwargs):
    """Asserts that the message in a raised exception matches a regexp.

    Args:
        excClass: Exception class expected to be raised.
        exp_regexp: Regexp (re pattern object or string) expected
                to be found in error message.
        callable_obj: Function to be called.
        args: Extra args.
        kwargs: Extra kwargs.
    """
    if callable_obj is None:
        return _AssertRaisesContext(excClass, exp_regexp)
    try:
        callable_obj(*args, **kwargs)
    except excClass, exc_value:
        if isinstance(exp_regexp, basestring):
            exp_regexp = re.compile(exp_regexp)
        if not exp_regexp.search(str(exc_value)):
            raise failureException('"%s" does not match "%s"' %
                     (exp_regexp.pattern, str(exc_value)))
    else:
        if hasattr(excClass, '__name__'):
            excName = excClass.__name__
        else:
            excName = str(excClass)
        raise failureException, "%s not raised" % excName
                                               
def assertEqual(expected, actual, msg=None):
    """Fail if the two objects are unequal as determined by the '=='
       operator.
       
    The output message is subtly different to the unittest equivalent
     +  prints "Expected and Got" values.
     +  prefers hex output for integer types.
    """
    xmsg = ''
    if msg:
        xmsg = msg + "\n  "
    if not expected == actual:
        if isinstance(expected, basestring) and isinstance(actual, basestring) and expected.count('\n') > 2:
            diff = difflib.unified_diff(expected.split("\n"), actual.split("\n"), fromfile='expected', tofile='actual')
            raise failureException(xmsg + "\n".join(diff))

        raise failureException(xmsg + "\n" +
        "  Expected " + hexstr(expected) + "\n" + 
        ", but got  " + hexstr(actual))
    
def assertGreaterThan(expected, actual, msg=None):
    """Fail if expected object is not greater than actual object
	as determined by the '>' operator
       
    The output message is subtly different to the unittest equivalent
     +  prints "Expected and Got" values.
     +  prefers hex output for integer types.
    """
    xmsg = ''
    if msg:
        xmsg = msg + "\n  "
    if not expected > actual:
        raise failureException(xmsg + "\n" +
        "  Number            " + hexstr(expected) + "\n" + 
        "is not greater than " + hexstr(actual))
    
def assertGreaterEqual(expected, actual, msg=None):
    """Fail if expected object is not greater than or equal to 
	actual object as determined by the '>=' operator
       
    The output message is subtly different to the unittest equivalent
     +  prints "Expected and Got" values.
     +  prefers hex output for integer types.
    """
    xmsg = ''
    if msg:
        xmsg = msg + "\n  "
    if not expected >= actual:
        raise failureException(xmsg + "\n" +
        "  Number            		 " + hexstr(expected) + "\n" + 
        "is not greater than or equal to " + hexstr(actual))
    
def assertLessThan(expected, actual, msg=None):
    """Fail if expected object is not less than actual object
	as determined by the '<' operator
       
    The output message is subtly different to the unittest equivalent
     +  prints "Expected and Got" values.
     +  prefers hex output for integer types.
    """
    xmsg = ''
    if msg:
        xmsg = msg + "\n  "
    if not expected < actual:
        raise failureException(xmsg + "\n" +
        "  Number         " + hexstr(expected) + "\n" + 
        "is not less than " + hexstr(actual))
    
def assertLessEqual(expected, actual, msg=None):
    """Fail if expected object is not less than or equal to
	actual object as determined by the '<' operato.r
       
    The output message is subtly different to the unittest equivalent
     +  prints "Expected and Got" values.
     +  prefers hex output for integer types.
    """
    xmsg = ''
    if msg:
        xmsg = msg + "\n  "
    if not expected <= actual:
        raise failureException(xmsg + "\n" +
        "  Number            	      " + hexstr(expected) + "\n" + 
        "is not less than or equal to " + hexstr(actual))
    
def assertNotEquals(first, second, msg=None):
    """Fail if the two objects are equal as determined by the '=='
       operator.
    """
    if first == second:
        raise failureException(msg or '%r == %r' % (first, second))

def failUnlessAlmostEqual(first, second, places=7, msg=None):
    """Fail if the two objects are unequal as determined by their
       difference rounded to the given number of decimal places
       (default 7) and comparing to zero.

       Note that decimal places (from zero) are usually not the same
       as significant digits (measured from the most signficant digit).
    """
    if round(abs(second-first), places) != 0:
        raise failureException(msg or '%r != %r within %r places' % (first, second, places))

def failIfAlmostEqual(first, second, places=7, msg=None):
    """Fail if the two objects are equal as determined by their
       difference rounded to the given number of decimal places
       (default 7) and comparing to zero.

       Note that decimal places (from zero) are usually not the same
       as significant digits (measured from the most signficant digit).
    """
    if round(abs(second-first), places) == 0:
        raise failureException(msg or '%r == %r within %r places' % (first, second, places))

def assertIs(first, second, msg=None):
    """Fails if first is not the same object as the second."""
    assertTrue(first is second, \
        msg or '%r expected to be the same object as %r' % (first, second))

def assertIsInstance(expected, actual, msg=None):
    """Fails if actual object is not the same instance as the 
       expected object."""
    assertTrue(isinstance(expected, actual), \
        msg or '%r expected to be an instance of as %r' % (actual, expected))

def assertIsNone(first, msg=None):
    """Fails if object is not None."""
    assertTrue(first is None, \
        msg or '%r expected to be None' % (first))

def assertIsNot(first, second, msg=None):
    """Fails if first is the same object as the second."""
    assertTrue(first is not second, \
        msg or '%r expected not to be the same object as %r' % (first, second))

def assertIsNotNone(first, msg=None):
    """Fails if object is None."""
    assertTrue(first is not None, \
        msg or '%r expected to be not None' % (first))

def assertItemsEqual(expected, actual, msg=None):
    """Fail if the two lists do not contain the same elements and/or 
       are not of the same size.
       
    The output message is subtly different to the unittest equivalent
     +  prints "Expected and Got" values.
     +  prefers hex output for integer types.
    """
    xmsg = ''
    if msg:
        xmsg = msg + "\n  "
    if len(expected) != len(actual) or sorted(expected) != sorted(actual):
        raise failureException(xmsg + "\n" +
        "  Expected " + str(expected) + "\n" + 
        ", but got  " + str(actual))
    
def assertMultiLineEqual(expected, actual, msg=None):
    import difflib
    if expected != actual : 
        diff = difflib.unified_diff(expected.split("\n"), actual.split("\n"), fromfile='expected', tofile='actual')
        if msg:
            raise failureException(msg)
        else:
            raise failureException("The two strings are not equal\n" + "\n".join(diff))

def assertNotIsInstance(expected, actual, msg=None):
    """Fails if actual object is the same instance as the 
       expected object."""
    assertTrue(not isinstance(expected, actual), \
        msg or '%r expected not to be an instance of as %r' % (actual, expected))

def assertRegexpMatches(text, regexp, msg=None):
    """Fails if the regexp doesn't match any part of the text (regexp.search(text) == True).
    Regexp can be either a string or compiled regex.
    """
    import re
    regexp = re.compile(regexp)
    assertTrue(regexp.search(text), \
        msg or "Pattern %r expected to appear in %s" %(regexp.pattern, text))

def assertNotRegexpMatches(text, regexp, msg=None):
    """Fails if the regexp matches any part of the text (regexp.search(text) == False). 
    Regexp can be either a string or compiled regex.
    """
    import re
    regexp = re.compile(regexp)
    assertTrue(not regexp.search(text), \
        msg or "Pattern %r expected to appear in %s" %(regexp.pattern, text))


def assertDictContainsSubset(expected, actual, msg=None):
    assertTrue(all(item in actual.items() for item in expected.items()), \
            msg or "%r doesn't contain %r" %(actual, expected))

# Synonyms for assertion methods
failUnlessEqual = assertEquals = assertEqual
failIfEqual = assertNotEqual = assertNotEquals
assertAlmostEqual = assertAlmostEquals = failUnlessAlmostEqual
assertNotAlmostEqual = assertNotAlmostEquals = failIfAlmostEqual
failUnlessRaises = assertRaises
assert_ = assertTrue = failUnless
failIf = assertFalse
assertLess = assertLessThan
assertListEqual = assertItemsEqual
assertGreater = assertGreaterThan
assertSequenceEqual = assertItemsEqual
assertSetEqual = assertItemsEqual
assertTupleEqual = assertItemsEqual
assertDictEqual = assertItemsEqual

def test(data=None, setUp=None, tearDown=None): 
    """Decorates the function as a test function, to be called in this modules tests.
    
    If given an iterable parameter, one test will be created for each item 
    in the list, with the test passed the item as it's second argument.
    
    If the items in the list are tuples, the tuples will be expanded into the 
    parameters of the function.
    
    If given, setUp and tearDown should be callables accepting no arguments, and
    will be called before and after each test case.
    
    .. sourcecode :: python
        
        @test([ ("a", "A"), ("b", "B")])
        def testUpper(in, expected):
            test.assertEquals(expected, in.upper())
            
        @test
        def testUpper():
            test.assertEqual('SPAM', 'spam'.upper())
            
        def mySetup(): 
            open('eggs.txt', 'w').write('spam')

        def myTearDown(): 
            if os.path.exists('eggs.txt'): 
                os.remove('eggs.txt')

        @test(setUp=myTearDown, tearDown=myTearDown)
        def testPathExists(): 
           assertTrue(os.path.exists('eggs.txt'))
            
            
    test is also a pseudo module, which contains all of the assertion macros,
    this is to make migrating from the unittest interface easier, and also
    to provide a means to avoid ambiguity in the event of user names clashing
    with the assertion functions.
    """
    return decorate_test(data, FunctionRunner, setUp, tearDown)

test.get_argument_parser = get_argument_parser
test.main = main
test.run  = run
test.data = data
test.run_all = run_all
test.suiteSetUp           = suiteSetUp
test.suiteTearDown        = suiteTearDown
test.assertEqual          = test.assertEquals          = test.failUnlessEqual       = assertEqual
test.assertNotEqual       = test.assertNotEquals       = test.failIfEqual           = assertNotEqual
test.assertAlmostEqual    = test.assertAlmostEquals    = test.failUnlessAlmostEqual = assertAlmostEqual
test.assertNotAlmostEqual = test.assertNotAlmostEquals = test.failIfAlmostEqual     = assertNotAlmostEqual
test.assertRaises         = test.failUnlessRaises                                   = assertRaises
test.assertRaisesWithMessage = test.failUnlessRaisesWithMessage                     = assertRaisesWithMessage
test.assert_              = test.assertTrue            = test.failUnless            = assertTrue
test.assertFalse          = test.failIf                                             = assertFalse
test.asssertIn                                                                      = assertIn

if __name__ == "__main__":
    # skip the unittests because we have classes that derive from 
    # unittest.TestCase which are not actual test cases...
    test.main(skip_unittest=True)
