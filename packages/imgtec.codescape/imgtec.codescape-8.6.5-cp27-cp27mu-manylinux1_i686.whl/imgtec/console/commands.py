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

# !/usr/bin/env python
from imgtec.test import *
from imgtec.console.support import *
from imgtec.console.results import *
from imgtec.console.scan import tap, tapboot
from imgtec.console.generic_device import probe, Device, go, runstate
from imgtec.console.program_file import symbol
from imgtec.console.cfg import config
from imgtec.console.breakpoints import setsw, sethw, bkpt
import pydoc
import sys
import time
import os

try:
    pyhelp = help
except NameError:
    # some environments (e.g. py2exe frozen builds) don't have help
    def pyhelp(*_args, **_kwargs):
        pass

if 0:
    def _set_exit_handler(func):
        if sys.platform == 'win32':
            import ctypes
            from ctypes import wintypes
            cbtype = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_uint)
            SetConsoleCtrlHandler = ctypes.windll.kernel32.SetConsoleCtrlHandler
            SetConsoleCtrlHandler.restype = wintypes.BOOL
            SetConsoleCtrlHandler.argtypes = (cbtype, wintypes.BOOL)
            ctypes.windll.kernel32.SetConsoleCtrlHandler(cbtype(func), True)


    def _logtime(arg1):
        with open('c:\\test.txt', 'w+') as f:
            f.write('Hello!\n' + str(time.time()) + '\n' + str(arg1) + '\n' + repr(arg1))
        return True


    _set_exit_handler(_logtime)
    if 0: _logtime(1)


@command()
def help(cmd='', html=False):
    """Display help on all commands or a specific command.

    `html` specifies if we want see help in a command line or
    open it in an html help viewer. `html` is false by default.
    """
    if html:
        html_help(cmd)
    else:
        if isinstance(cmd, Command):
            h = cmd.help()
        elif cmd == '':
            cmds = Command._sorted_commands()
            longest = max(len(cmd.__name__) for cmd in cmds)
            h = "\n".join(cmd.oneliner(longest) for cmd in cmds)
        else:
            return pyhelp(cmd)
        return pydoc.pager(h)


def html_help(cmd):
    '''Opens help in a help viewer on windows and webbrowser on linux'''
    sought_command = ''
    from imgtec.console import __all__ as allcommands

    if isinstance(cmd, Command):
        if cmd.__name__ in allcommands:
            sought_command = "#imgtec.console." + cmd.__name__
        else:
            return pydoc.pager(cmd.help())
    elif cmd != '':
        return pyhelp(cmd)

    from imgtec.codescape.help import show_help
    show_help("scripting/console.commands.html" + sought_command)


@command()
def cmdall(cmd, *args, **kwargs):
    """Utility to run a command on all devices or a list of devices.

    In systems with more than one device, cmdall allows any command to be
    executed by many devices. For example, "cmdall(runstate)" is equivalent to
    "runstate(c0v0), runstate(c0v1), etc.

    By default the command will be executed by all devices, you can do the following to
    choose a subset of all devices.

        >>> cmdall(runstate, devices=[s0c0v0, s0c0v1])
        ...

    This list will be cached and used for the next cmdall if a new list is not given.

    This is an example for a target with 5 cores, with 2 VPEs on the first
    core, and one VPE on the other 4 cores ::

        >>> cmdall(runstate)
        s0c0v0: status=exception pc=0x00000000 status_bits=0x1006
        s0c0v1: status=expected_reset pc=0x00000000
        s0c1v0: status=expected_reset pc=0x00000000
        s0c2v0: status=running
        s0c3v0: status=expected_reset pc=0x00000000
        s0c4v0: status=running

    The return type is a list of the results of each command.  e.g. in the above
    example cmdall(runstate)[0] has the same value as runstate().  Though if all
    the calls returned None then the result is ``None`` instead of a list of
    ``None``.

    Any exceptions that occur during processing are stored in the result, and a
    RuntimeError will be raised after all devices have been called with the
    exceptions formatted in the output string ::

        [s0c0v0] >>> cmdall(regs, 'epc')
        RuntimeError: One or more calls to regs('epc') failed:
        s0c0v0: 0x0ff5c860
        s0c0v1: 0x44840961
        s0c1v0: 0x81466d1b
        s0c1v1: 0x2dc25613
        s1c0v0: Error: No register found with name 'epc'
        s2c0v1: Error: No register found with name 'epc'

    """
    from imgtec.console.generic_device import make_device_list
    used_listdevices = False

    devices = kwargs.get('devices')
    if devices:
        # don't pass onto the command itself
        del kwargs['devices']
    else:
        found = [x for x in args if isinstance(x, Device)]
        if found:
            devices = found
            args = [x for x in args if not isinstance(x, Device)]
        elif not cmdall.devices:
            devices = [d for d in make_device_list() if d.core.family != CoreFamily.mipscm]
            used_listdevices = True
        else:
            devices = cmdall.devices

    devices = expand_devices(devices)

    if getattr(cmd, 'supports_multiple_devices', False):
        res = cmd(*args, devices=devices, **kwargs)
    else:
        res = AllResult()
        for vpe in devices:
            try:
                res.add(vpe.name, cmd(*args, device=vpe, **kwargs))
            except Exception as e:
                res.add(vpe.name, e)
        res = res.get_result(cmd, *args, **kwargs)

    # Store now so we only cache valid devices
    if not used_listdevices:
        cmdall.devices = devices
    return res


cmdall.devices = None

reset_types = [
    namedstring(normalboot),
    namedstring(ejtagboot),
    namedstring(probe),
    namedstring(tap),
    namedstring(tap_async),
    namedstring(tap_sync),
    namedstring(soft),
    namedstring(hard_auto),
    namedstring(hard_halt),
    namedstring(hard_run),
    namedstring(hard_all_halt),
    namedstring(hard_all_run),
]


@command(type=reset_types)
def reset(type='hard_auto', device=None):
    """Resets the probe, the tap or the target.

    The following reset types are supported:

    ============= ==================================================================================================================
    Reset Type    Description
    ============= ==================================================================================================================
    probe         Reset the probe, returning it to uncommitted mode.
    soft          Perform a soft reset of the current core (where available).
    hard_run      Hard reset the system, the current core will run after reset. (see note)
    hard_halt     Hard reset the system, the current core will halt after reset. (see note)
    hard_auto     Hard reset the system, halt the current core or not based on config setting "halt after reset". (see note)
    hard_all_halt Hard reset the system, all cores will halt after reset.
    hard_all_run  Hard reset the system, all cores will run after reset.
    tap/tap_both  Perform a TAP Reset by first asserting nTRST then clocking TCK for 5+ cycles while TMS=1, then de-asserting nTRST.
    tap_async     Perform an asynchronous TAP reset, by toggling nTRST.
    tap_sync      Perform a synchronous TAP reset by clocking TCK for 5+ cycles while TMS=1.
    ============= ==================================================================================================================

    The halt/run status of the other cores after reset will depend on the last type
    of reset done on that core. For example ::

        # reset all cores, halt them all after reset...
        reset(hard_all_halt, s0c0)

        # reset all cores, run core 1 but run halt all other cores after reset because
        # the last boot indication to the other cores was a halt.
        reset(hard_run, s0c1)

    """
    tap_resets = dict(tap='both', tap_both='both', tap_async='async', tap_sync='sync')
    if type == 'probe':
        device.tiny.DAReset()
        device.probe.scan_devices()
        return device.probe
    elif type in tap_resets:
        device.tiny.TapReset(tap_resets[type])
    elif type in ('ejtagboot', 'hard_halt', 'hard_all_halt',
                  'normalboot', 'hard_run', 'hard_all_run',
                  'soft', 'hard_auto'):
        p = device.probe
        if p.mode == 'scanonly':
            if type == 'soft':
                raise RuntimeError('Soft reset not currently supported in scanonly mode')
            if type != 'hard_auto':
                tapboot(type, device=p)
            config('assert nhardreset', 0)
            time.sleep(0.5)
            config('assert nhardreset', 1)
        else:
            normaliser = dict(ejtagboot='hard_halt', normalboot='hard_run')
            device.tiny.Reset(normaliser.get(type, type))
    else:
        raise NotImplementedError("Unknown, or unsupported reset type %s" % (type,))


@command(verbose=verbosity)
def scanonly(perform_bypass_test=False, verbose=True, device=None):
    """Reset the probe and initialise the tapology.

    This command is equivalent to ::

        >>> reset(probe)
        >>> jtagchain(verbose=verbose)
        Bypass test found 1 tap
        Determine IR lengths on scan chain and validating number of taps...
        [5]
    """
    reset('probe', device=device)
    from imgtec.console.scan import jtagchain
    jtagchain(perform_bypass_test=perform_bypass_test, 
        device=device, verbose=verbose)
    Command.set_device(device.probe)


@command()
def autodetect(tapology=None, device=None):
    """Reset the probe and auto detect the targets connected to it.

    tapology [ default = None ]
        When given, this prevents the probe from attempting to discover the TAPS
        connected (described in more detail below).  It should be a list of
        the length of each IR register starting at SoC TDI. For a typical 2 core, 2 vpe
        SoC with a Coherence Manager this should be [5, 5, 5, 5, 5].

    The first step of auto detection is to determine the number of TAPs on the JTAG
    chain and also to determine the length of the instruction register(IR) for each
    TAP.

    This is done by performing a TAP Reset and transitioning the TAP state through
    The capture-IR state which will capture xxxxxx01 into each IR.  For
    most TAPS, the value captured is 000001 which allows the probe to
    detect the number of taps by searching for sequences of zeros followed by a
    single set bit.  Codescape Console provides the same algorithm in the
    jtagchain() command.

    Should this algorithm not function correctly you can prevent the JTAG chain
    discovery and provide the number and length of taps.

    After the JTAG chain has been discovered the probe will attempt to detect
    what cores are connected to each TAP.  If this algorithm fails please read
    the MIPS Debug Low-Level bring up guide which covers this topic in detail.
    """
    device.probe.da.AutoDetect(tapology)
    device.probe.scan_devices()
    from imgtec.console.generic_device import listdevices
    return listdevices()


@command(enabled=[(on, True), (off, False), (enable, True), (disable, False)])
def coredebugging(enabled=None, device=None):
    """Enable, disable or get the current state of probe debugging of the core.

    By default the probe will allow debugging of all cores that are detected,
    by disabling debugging of cores that are not of interest it can speed up
    Codescape Debugger.  It does not typically have much effect on Codescape
    Console.
    """
    if enabled is not None:
        device.tiny.EnableCore(enabled)
    return device.tiny.IsCoreEnabled()


@command()
def hsp(path=None, device=None):
    """Gets or sets the path to the active hsp for the current probe.

    To deactivate a hsp, pass an empty path :

        >>> hsp('')
        >>> hsp('custom.xml')
        'custom.xml'

    """
    id = device.da.GetIdentifier()
    if path is not None:
        if device.probe.environment == 'codescape':
            from imgtec.codescape import GetSelectedThread
            t = GetSelectedThread()
            t.probe.SetHSPSettings(path)
        else:
            active = bool(path)
            names = [path] if path else []
            device.da.SetHSPSettings(id, active, names)
    active, names = device.da.GetHSPSettings(id)
    if active and names:
        return StrResult(names[0])


@command()
def abi(newabi=None, device=None):
    """Sets the current abi, or displays the current abi.

    The abi is used to determine the register names for :func:`regs`
    and :func:`dasm`, and can be one of :

        ======= ============================================================
        Name    ABI
        ======= ============================================================
        meta    Meta.
        numeric MIPS ABI Undefined. All Registers have the numeric names.
        o32     MIPS ABI O32.
        n32     MIPS ABI N32.
        n64     MIPS ABI N64.
        ======= ============================================================

    >>> abi()
    o32
    >>> abi('n32')
    n32

    """
    if newabi is not None:
        device.set_abi(newabi)
    return StrResult(device.abi)


@command()
def isa(address=None, device=None):
    """Displays the current ISA .

    The current ISA and ASE is determined by checking the ISA and ASE support
    on the current target, and comparing the least significant bit of the
    given address.

    If `address` is None then the current value of the PC will be read and used.

    The ISA is a combination of "mips16", "mips32", or "micromips", and none
    or more ASE's, separated with '+' : "3d", "smart", "mt", "dsp", "msa".

    For example, "mips32", "mips32+mt", "micromips+mt+dsp"

    >>> isa()
    mips32

    """
    return StrResult(device.da.GetCurrentISA(address))


@command(aliases='q')
def quit():
    """Use quit() or Ctrl-D or without readline Ctrl-Z<enter> to exit from the console."""
    # Do we need to remove breakpoints here (prompt?)
    sys.exit()


q = quit


@command(verbose=verbosity,
         bptype=[namedstring(set), namedstring(setsw), namedstring(sethw)], )
def runtoaddress(address, bptype='set', timeout=20, verbose=1, device=None):
    '''Runs to specified address using a breakpoint.

    After the breakpoint has been hit the breakpoint is automatically removed.
    If `bptype` is not specified then 'set' will be used, alternatively a software
    or hardware breakpoint can be specified using 'setsw' or 'sethw' respectively.

    `Address` can be name like 'main' or address in memory.
    `Timeout` is is a time after which it raises RuntimeError. By default is set to 20 seconds.
    `Verbose` is set to 1 by default.

    Raises a RuntimeError if did not stop at desired destination.

    Returns actual runstate object
    '''
    if isinstance(address, basestring):
        try:
            address = symbol(address)
        except RuntimeError:
            pass

    bkpt(bptype, address)
    try:
        go(verbose=verbose)
        waitforhalt(timeout)
        actual = runstate()
        if actual.pc != address:
            raise RuntimeError('Target did not stop at destination 0x{0:08x}, '
                               'stopped at 0x{1:08x}.'.format(address, actual.pc))
        return actual
    finally:
        bkpt('clear', address)


def _halted(d):
    return not runstate(d).is_running

@command(any_or_all=[(any, any), (all, all)])
def waitforhalt(timeout=0, any_or_all=all, devices=[],):
    '''Wait until the device (or devices) have stopped.

    any_or_all may be any, or all. Meaning wait until any device has halted
    or all devices have halted.

    If the timeout argument (given in seconds) is given then RuntimeError will
    be raised if all/any devices have not stopped until after this time,

    For example::

        waitforhalt(any, soc0)         # wait for any device on soc0 to halt
        waitforhalt(all, s0c0, s0c1)   # wait for all devices on s0c0 and s0c1 to halt
        waitforhalt()  # wait for the current device to halt

    '''
    target = time.time() + timeout
    while not any_or_all(_halted(d) for d in devices):
        if timeout and time.time() > target:
            raise RuntimeError('Target has not stopped after {0} seconds.'.format(timeout))
        time.sleep(0.1)


@command()
def apropos(keyword, *keywords):
    '''Search help for all commands that contain the given keyword.

    Keywords needs to consist of at least 3 letters. For example::
    
        >>> apropos('cache')
        invalidate(cache=None, device=None)
          Invalidate, or writeback invalidate the instruction, data or secondary  caches.
        
        cachedump(cache=None, start_addr=0, end_addr=None, show_chars=True, skip_invalid=False, device=None)
          Show the contents of the cache for a given address range.
        ...
        cacheinfo(cache=None, device=None)
          Show the details of the given cache, or all caches on the target if one isn't given.
          
        cacheop(cache, address, line_size, operation, count=1, flags=0, device=None)
          Perform a cache operation.
    '''

    def _match_keyword(cmd, keyword):
        if keyword in cmd.definition():
            return Result(cmd, None)
        line = _find_line_with_word(keyword, cmd._doc)
        if line and cmd.__name__ != "apropos":
            return Result(cmd, "..." + line + "...")
        return None

    def _remove_example_lines(doc):
        return ' '.join(s for s in doc.splitlines() if not s.startswith("   "))

    def _find_line_with_word(keyword, doc):
        doc = _remove_example_lines(doc)
        for line in re.split(r"\.|    ", doc):
            if keyword in line:
                return line.strip()
        return None

    results = Aproporesult()
    for cmd in Command._sorted_commands():
        result = _match_keyword(cmd, keyword)
        if result:
            results.append(result)

    if keywords:
        non_matching = [r for k in keywords for r in results if k not in (r.cmd.definition() + _remove_example_lines(r.cmd._doc))]
        results[:] = [r for r in results if r not in non_matching]

    return results


class Aproporesult(list):
    def __repr__(self):
        def _format(cmd, doc_part):
            return '{0}\n\t{1}\n'.format(cmd.definition(), doc_part or cmd.short_doc())

        return '\n'.join(_format(cmd, doc_part) for cmd, doc_part in self)


Result = namedtuple('Result', ['cmd', 'doc_part'])


@command()
def installexamples(example=None, auto=False, overwrite=False, __filename=None, __init_file=None, __examples=None):
    """
    Install examples into the user console scripts folder.

    If `example` is not specified then will list all available examples.
    If `auto` is True then examples will be imported at every codescape console startup.
    If there is already a file called the same as the example
    it will not be overwritten until `overwrite` or `auto` is set to True.
    """
    try:
        from imgtec.console.examples import examples
    except ImportError:
        raise Exception("There are no examples that can be installed in user console scripts folder.")
    if not example:
        print "Use this to install example and/or extension scripts:"
        _print_info_from_encoded_examples(__examples or examples)

    else:
        _check_if_example_exist(example, examples)

        filename = __filename or os.path.join(config(console, 'scripts_path'), example + ".py")
        folder = os.path.dirname(filename)
        if not os.path.isdir(folder):
            os.mkdir(folder)

        if os.path.isfile(filename) and not overwrite:
            if not auto:
                raise Exception("File already exists. Set overwrite=True if you want to overwrite it.")
            else:
                was_in_init = _prepend_import_to_init_file(example, __init_file)
                if was_in_init:
                    raise Exception("File already exists and it is set to be imported automatically. "
                                    "Set overwrite=True if you want to overwrite it.")
                else:
                    print "File already exists but example was set to be imported every codescape console startup. " \
                          "Set overwrite=True if you want to overwrite the example file."
                    return
        else:
            with open(filename, "w+") as f:
                f.write(examples[example])

        if auto:
            _prepend_import_to_init_file(example, __init_file)

        print "Example is installed, now you can import it typing:"
        print "    >>> import {0}".format(example)


def _check_if_example_exist(example, examples):
    if example not in examples:
        matches = get_close_matches(example, examples, 10)
        msg = "There is no example called {0}.".format(example)
        if len(matches) == 1:
            msg += " Did you mean {0} ?".format(matches[0])
        elif matches:
            msg += " Did you mean one of {0} ?".format(', '.join(matches))
        raise ValueError(msg)


def _print_info_from_encoded_examples(examples):
    for ex_name, ex_content in examples.iteritems():
        print
        print " - " + ex_name
        print

        first_line = ex_content.splitlines()[0]
        if first_line.startswith("'''") or first_line.startswith('"""'):
            print '"' + first_line.replace("'''", "").replace('"""', "") + '"'

        found_commands = _get_commands_from_code(ex_content)
        if found_commands:
            print "Commands:  " + ", ".join(found_commands)


def _get_commands_from_code(text):
    def is_command(f):
        for dec in f.decorator_list:
            try:
                if dec.func.id == "command":
                    return True
            except AttributeError:
                pass
        return False

    import ast
    functions = [x for x in ast.parse(text).body if isinstance(x, ast.FunctionDef)]

    return [f.name for f in functions if is_command(f)]


def _prepend_import_to_init_file(module, __init_file):
    filename = __init_file or os.path.join(config(console, 'scripts_path'), "__init__.py")
    import_to_append = "import {0}".format(module)
    try:
        with open(filename, "r+") as f:
            original_content = f.read()
    except IOError:
        original_content = ""

    if import_to_append not in original_content:
        with open(filename, "w+") as f:
            f.write(import_to_append)
            f.write("\n")
            f.write(original_content)
        return False
    return True
    