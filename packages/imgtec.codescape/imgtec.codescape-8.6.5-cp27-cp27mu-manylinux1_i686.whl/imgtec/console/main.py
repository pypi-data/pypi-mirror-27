# encoding: utf8
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

#!/usr/bin/env python
"""Target bring up python interpreter based debugger.

Commands must obey python syntax rules, so parentheses are required, 
arguments must be comma separated, and strings must be quoted.  See
the examples section below.
"""
epilog="""\
The following examples are all equivalent :

 $ CodescapeConsole "DA-net 1234"
 $ CodescapeConsole DA-net1234
 $ CodescapeConsole danet1234

Use the command help(), or see the Codescape Console documentation for more 
information.
"""
from imgtec.console import version
welcome_message = u"""Welcome to Codescape Console %s.
Copyright \u00a9 MIPS Tech LLC.
Enter help()<enter> for help.  """ % (version,)

from imgtec.console.support import *
from imgtec.console.support import _console_logger
from imgtec.console.commands import probe, quit
from imgtec.console.results import _install_displayhook
from imgtec.console import termcolour
from imgtec.console.generic_device import _add_root_handler
import atexit
import code
import errno
import os
import sys
import traceback
# import logging as _logging

def initialise_readline(args):
    if args.no_readline or not sys.stdin.isatty():
        quit._doc = quit.__doc__ = 'Use quit() or Ctrl-Z plus Return to exit from the console.'
        return u''
    try:
        import readline
    except ImportError:
        quit._doc = quit.__doc__ = 'Use quit() or Ctrl-Z plus Return to exit from the console.'
        if sys.platform.startswith('win'):
            return u"\nUse pip pyreadline to enable <tab> completion."
        else:
            return u"\nreadline support not found in your installation of python."
    else:
        if not args.no_colour:
            termcolour.enabled = True
        quit._doc = quit.__doc__ = 'Use quit() or Ctrl-D to exit from the console.'
        readline.set_completer(ReadLineCompleter(Completer(Command._commands), readline))
        readline.set_completer_delims(readline.get_completer_delims() + ',')
        if readline.__doc__ and 'libedit' in readline.__doc__:
            readline.parse_and_bind("bind ^I rl_complete")
        else:
            readline.parse_and_bind("tab: complete")
        history_path = os.path.expanduser('~/.com.imgtec/codescape_console.history')
        try:
            readline.read_history_file(history_path)
        except EnvironmentError:
            pass
        @atexit.register
        def _write_history():
            try:
                readline.write_history_file(history_path)
            except EnvironmentError:
                pass
        return u"<tab> completion has been enabled."

try:
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, epilog=epilog,
                    formatter_class=argparse.RawDescriptionHelpFormatter)
    _parse_startup_args = parser.parse_args
    add_argument = parser.add_argument
    def format_usage():
        return parser.format_usage()
    add_argument('probe', nargs='?', type=str, help='Probe identifier, e.g. DA-net1234 or "DA-net 1234"')
except ImportError:
    import optparse
    def format_usage():
        return __doc__+'\n%prog [options] [probe]'
    parser = optparse.OptionParser(usage=format_usage(), 
        epilog="Where [probe] is the optional probe identifier, e.g. DA-net1234 or \"DA-net 1234\".")
    add_argument = parser.add_option
    def _parse_startup_args(args=None):
        if args is not None:
            options, args = parser.parse_args(args)
        else:
            options, args = parser.parse_args()
        options.probe = args[0] if args else ''
        return options
    
def parse_startup_args(args=None):
    """Parse command line arguments to Codescape Console scripts.

    This is the function used by Codescape Console to parse command line
    arguments when run in an interactive mode.  It can be used in a script
    using ``imgtec.console`` by passing the result of this function 
    directly to :func:`~imgtec.console.probe`. ::

        from imgtec.console import *

        def useful():
            pass

        if __name__ == '__main__':
            probe(args=parse_startup_args())
            useful()

    The return value is an object with at least the following properties:

        ================ ===========================================================
        Property         Description
        ================ ===========================================================
        probe            The identifier of the probe passed as the first argument
                         for example 'DA-net 1'.
        force_disconnect A boolean indicating whether --force-disconnect was passed.
        environment      Either 'standalone' if the script is run independently from
                         Codescape (this includes Connect scripts) or 'codescape' if 
                         run from within Codescape with an active connection.
                         See :ref:`integrating` for more information.
        ================ ===========================================================

    Other command line options supported by Codescape will also be available as parsed
    by the standard library module ``argparse``.
        
    """

    args = _parse_startup_args(args)
    if args.environment == 'auto':
        try:
            from imgtec.codescape import environment
            args.environment = environment
        except ImportError:
            args.environment = 'standalone'        
    return args

add_argument('--advanced-options', help='Advanced probe connection options.')
add_argument('--search-location', help='IP address or DNS name of probe if normal discovery mechanisms (DNS, UDP Broadcast) fail.')
add_argument('--force-disconnect', action='store_true', help='Attach to this probe even if it is in use, this will disconnect the other user')
add_argument('--no-readline', action='store_true', help='Do not enable readline, even if it is available')
add_argument('--no-colour', action='store_true', help='Do not enable colours, even if they are available')
add_argument('--logging', action='append', choices=['console', 'probe', 'comms'], default=[], help='Enable logging immediately on startup.')
add_argument('--environment', choices=['auto', 'standalone', 'codescape'], default='auto', help='Set environment, by default auto detects codescape presence.')

class MinimalTracebackInterpreter(code.InteractiveConsole):
    def showtraceback(self):
        from imgtec.console.cfg import console_config
        if console_config.traceback:
            code.InteractiveConsole.showtraceback(self)
        else:
            display_current_exception()
            print

if sys.hexversion > 0x03000000:
    def exec_function(source, filename, global_map):
        """A wrapper around exec()."""
        exec(compile(source, filename, "exec"), global_map)
else:
    # OK, this is pretty gross.  In Py2, exec was a statement, but that will
    # be a syntax error if we try to put it in a Py3 file, even if it isn't
    # executed.  So hide it inside an evaluated string literal instead.
    eval(compile("""\
def exec_function(source, filename, global_map):
    exec compile(source, filename, "exec") in global_map
""",
    "<exec_function>", "exec"
    ))
                
            
_interpreter = None
def get_current_lines():
    try:
        return _interpreter.buffer[:]
    except AttributeError:
        return ['']
        
def init_console():
    '''Perform startup operations that are normally done automatically when
    Codescape Console is being run interactively.
    
    This sets up logging, reads the global configuration, adds the 
    $HOME/imgtec/console_scripts path (or the custom path if overridden
    using ``config(console, 'scripts_path', ...)`` to sys.path.
    
    Finally the startup script ``$HOME/imgtec/console_scripts/__init__.py`` is
    executed.
    
    '''
    from imgtec.console.cfg import read_config, console_config
    _install_displayhook()
    read_config()
    _add_root_handler() #file_handler = _logging.RotatingFileHandler(

    scripts_path = os.path.expanduser(console_config.scripts_path)
    sys.path.insert(0, scripts_path)
    startup_script = os.path.join(scripts_path, '__init__.py')
    try:
        with open(startup_script) as f:
            contents = f.read()
    except EnvironmentError as e:
        if e.errno != errno.ENOENT:
            _console_logger.error('Failed to read startup_script "%s"', startup_script)
            _console_logger.error('  %s', e)
    else:
        try:
            exec_function(contents, startup_script, {})
        except Exception as e:
            print 'Failed to execute startup script:'
            display_current_exception()
startup = init_console

def interact(args):
    m = welcome_message + initialise_readline(args)
    try:
        print m.encode(sys.stdout.encoding, 'ignore')
    except Exception:  # might fail if sys.stdout.encoding is something weird (esp on MS)
        # lets assume we can at least print ascii
        print m.replace(u'\u00a9', '(c)').encode('ascii', 'ignore')
    init_console()        
    if args.probe:
        try:
            print repr(probe(args=args))
        except Exception:
            display_current_exception()
    
    global _interpreter
    Command._interactive = True
    _interpreter = MinimalTracebackInterpreter(Command.get_namespace())
    while 1:
        try:
            _interpreter.interact('')
            return
        except KeyboardInterrupt:
            print "Enter q or exit() plus Return to exit"

def main():
    interact(parse_startup_args())

if __name__ == "__main__":
    main()
