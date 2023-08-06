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

from imgtec.console import *
from imgtec.console import main
from imgtec.console import support
import itertools
import logging
import re
import sys
import unittest
from textwrap import dedent

AssertionError = unittest.TestCase.failureException
logger = logging.getLogger('run_consoletest')
#logger.addHandler(logging.NullHandler())
handler = logging.StreamHandler(sys.__stdout__)
logger.addHandler(handler)
handler.setLevel(logging.WARNING)
logger.setLevel(logging.WARNING)

__IMG_Test_HideCallStack    = True
"""True to hide callstack entries belonging to the test framework."""

_OPTION_DIRECTIVE_RE = re.compile(r'#\s*consoletest:\s*([^\n\'"]*)$',
                                      re.MULTILINE)

def parse_options(expected, options, singleline=None):
    r'''Parse option directives in the output or in the last cmd.

    Values are stored in the dictionary options.

    =================================== =====================
    Desired Action                      Syntax
    =================================== =====================
    Turn on option :                    # consoletest:+OPT
    Turn off option :                   # consoletest:-OPT
    Turn on option for just this line : # consoletest:OPT
    =================================== =====================

    For just a single line modifier, the option name will be added to the set
    `singleline`. If singleline is not given (because we are in the
    test, not in the expected output, a RuntimeError will be raised.

    >>> options, singleline = {}, set()
    >>> parse_options('nothing of interest', options, singleline)
    'nothing of interest'
    >>> options, singleline
    ({}, set([]))
    >>> parse_options('nothing of interest #consoletest:+OPT', options, singleline)
    'nothing of interest '
    >>> options, singleline
    ({'OPT': True}, set([]))

    >>> parse_options(">>> start(\n... because)   #consoletest:+OPT", options, singleline)
    '>>> start(\n... because)   '
    >>> options, singleline
    ({'OPT': True}, set([]))

    >>> parse_options('nothing of interest #consoletest:-OPT', options, singleline)
    'nothing of interest '
    >>> options, singleline
    ({'OPT': False}, set([]))

    >>> parse_options('nothing of interest #consoletest:OPT', options, singleline)
    'nothing of interest '
    >>> options, singleline
    ({'OPT': True}, set(['OPT']))

    >>> parse_options('nothing of interest #consoletest:OPT', options)
    Traceback (most recent call last):
    ...
    RuntimeError: Cannot use single line options in the test code itself.
    '''
    opt = _OPTION_DIRECTIVE_RE.search(expected)
    if opt:
        expected = expected[:opt.start(0)]
        for o in opt.group(1).split(','):
            if o.startswith('+'):
                options[o[1:]] = True
            elif o.startswith('-'):
                options[o[1:]] = False
            else:
                if singleline is None:
                    raise RuntimeError('Cannot use single line options in the test code itself.')
                options[o] = True
                singleline.add(o)
    return expected

def compare(expected_cmd, actual_cmd, expected, actual):
    last_cmd = '\n'.join(expected_cmd)
    if not expected and actual:
        lines = ['Unexpected output following:', last_cmd]
        lines += actual
        return '\n'.join(lines)
    lines = ['Expected(-) != actual(+):']
    differ = False
    options = {'PROMPT':True,'REGEX':False}
    parse_options(last_cmd, options)
    had_eof = False
    pending_eof = True
    if options.get('PROMPT'):
        expected = expected_cmd + expected
        actual   = actual_cmd + actual
    for e, a in itertools.izip_longest(expected, actual, fillvalue=None):
        singleline = set()
        if e:
            e = parse_options(e, options, singleline)
            e = e.rstrip()
        if a: a = a.rstrip()
        if e is not None and a is not None and options.get('REGEX', False):
            match = bool(re.compile(e + '$').match(a))
        else:
            match = e == a
        if not match:
            if e is None and not had_eof:
                lines.append('- EOF')
                had_eof = True
            elif a is None:
                pending_eof = True
            if e is not None: lines.append('- ' + e)
            if a is not None: lines.append('+ ' + a)
            differ = True
        else:
            lines.append('  ' + a)
        for off in singleline:
            options[off] = False
    if pending_eof:
        lines += ['+ EOF']
    if differ:
        return '\n'.join(lines)


class Runner(main.MinimalTracebackInterpreter):
    def __init__(self, code, **kwargs):
        main.MinimalTracebackInterpreter.__init__(self, **kwargs)
        self.__lines = code.splitlines()
        self.__oldstdout, sys.stdout = sys.stdout, self
        self.__oldstderr, sys.stderr = sys.stderr, self
        self.__buffer = ''
        self.__expected_cmd, self.__actual_cmd = [], []

    def __enter__(self):
        return self

    def write(self, s):
        self.__buffer += s
        logger.debug('OUT : %r', s)
        
    def isatty(self):
        return False

    def __exit__(self, *exc):
        if not (exc and exc[0]):
            self._check_expected()
        sys.stdout = self.__oldstdout
        sys.stderr = self.__oldstderr

    def split_prompt(self, s):
        prefix, prompt, code = s.partition('>>> ')
        if not prompt:
            prefix, prompt, code = s.partition('... ')
        return prefix, prompt, code

    def is_prompt(self, s):
        return bool(self.split_prompt(s)[1])

    def _check_expected(self):
        expected_lines = []
        while self.__lines:
            if self.is_prompt(self.__lines[0]):
                break
            expected_lines.append(self.__lines.pop(0))
        actual_lines = self.__buffer.rstrip().splitlines()
        message = compare(self.__expected_cmd, self.__actual_cmd, expected_lines, actual_lines)
        if message:
            raise AssertionError(message)
        self.__buffer = ''
        self.__expected_cmd, self.__actual_cmd = [], []

    def raw_input(self, actual_prompt):
        self._check_expected()
        try:
            line = self.__lines.pop(0)
            logger.debug('IN  : %r', line)
        except IndexError:
            logger.debug('EOF')
            raise EOFError()

        prefix, prompt, code = self.split_prompt(line)
        if not prompt:
            logger.debug('NO PROMPT! : %r', line)
        self.__expected_cmd.append(line)
        self.__actual_cmd.append(actual_prompt + code)
        return code + '\n'


def consoletest(code, locals=None, globals=None):
    r"""Test a codescape console script using doctest like features.

    Some notable differences from doctest:

    * Trailing whitespace is ignored on the examples
    * Formatting of results follows the same rules as Codescape Console (e.g.
      prefers hex)
    * The option #consoletest:REGEX enables regexes on the current line
    * The option #consoletest:+REGEX enables regexes for the rest of the example
    * The option #consoletest:+REGEX disables regexes for the rest of the example
    * Support for Codescape Console commands directly.
    * Support for the Codescape Console prompt.

    e.g.

    from imgtec.console import *
    from imgtec.test import *
    from imgtec.console.consoletest import consoletest

    @test
    def test_write_register():
        # do some setup
        probe('danet 1234')
        autodetect()
        reset(ejtagboot)
        consoletest('''\
            [s0c0v0] >>> regs('a0', 0x1235)
            0x0000123[45]       #consoletest:REGEX
            ''')
    """
    main._install_displayhook()
    ns = dict(support.Command.get_namespace())
    if globals:
        ns.update(globals)
    if locals:
        ns.update(locals)
    with Runner(dedent(code), locals=ns) as r:
        r.interact(banner='')
