import sys
import os
import errno
import subprocess
import webbrowser
from multiprocessing.connection import Client

from . import GetCodescapeDebuggerPath

if sys.platform == 'win32':
    helpviewer_address = r'\\.\pipe\com.imgtec.codescape.helpviewer'
else:
    helpviewer_address = '/tmp/.com.imgtec.codescape.helpviewer'

executable_extension = {'win32': '.exe'}

def run_help_viewer(exe_dirpath, help_path):
    if sys.platform == 'darwin':
        exe_dirpath = os.path.join(exe_dirpath, 'Codescape-Help-Viewer.app/Contents/MacOS')

    exe_filename = os.path.join(exe_dirpath, 'Codescape-Help-Viewer' + executable_extension.get(sys.platform, ''))
    if not os.path.exists(exe_filename):
        raise EnvironmentError(errno.ENOENT, 'Failed to find Codescape Help Viewer application in: %s' % exe_dirpath)

    args = [exe_filename, '--url', 'file://' + help_path]
    if sys.platform == 'darwin':
        args = ['open', '-W', '-a'] + args

    startupinfo = None
    if sys.platform == 'win32':
        STARTF_FORCEOFFFEEDBACK = 0x00000080
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= STARTF_FORCEOFFFEEDBACK | subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = 10

    return subprocess.Popen(args, cwd=exe_dirpath, startupinfo=startupinfo)

def show_help_by_path(help_path, codescape_path=None):
    if codescape_path is None:
        codescape_path = GetCodescapeDebuggerPath()
    if not codescape_path:
        raise EnvironmentError(errno.ENOENT, 'Failed to find Codescape Debugger installation')

    anchor = ''
    if '#' in help_path:
        help_path, anchor = help_path.split('#', 1)
        anchor = '#' + anchor

    help_path = os.path.join(codescape_path, help_path)
    if not os.path.exists(help_path):
        raise EnvironmentError(errno.ENOENT, 'Failed to find help file: %s' % help_path)

    help_path = help_path + anchor

    if sys.platform.startswith('linux'):
        webbrowser.open_new_tab(help_path)
    else:
        try:
            client = Client(helpviewer_address)
            client.send('file://' + help_path)
        except OSError:
            return run_help_viewer(codescape_path, help_path)

def show_help(help_path, codescape_path=None):
    return show_help_by_path(os.path.join('help', help_path), codescape_path)

def show_dialog_help(dialog_name, codescape_path=None):
    return show_help_by_path(os.path.join('help', 'interface', 'dialoghelp', dialog_name + '.html'), codescape_path)
