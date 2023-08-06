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

from collections import namedtuple
import os
import re
import sys
import tempfile
import time
from imgtec.lib import namedstruct
from imgtec.lib import namedenum 
from imgtec.lib import rst
from imgtec.lib.cacert import get_cacert_file
from imgtec.console import command, require_device, probe, results
from imgtec.codescape import ProgressInterface

DEFAULT_URL = os.environ.get('MIPS_PROBE_FIRMWARE_URL', 'https://codescape.mips.com/components/probes/firmware/fwversions.txt')

FlashVersionHeader = namedstruct.namedstruct('FlashVersionHeader', prefix='>', fields=[
            'L major',
            'L minor',
            "3s revision=''",
            'B flash_code',
            'L crc'])

FlashFileBase = namedtuple('FlashFileBase', 'path major minor revision flash_code crc')

FlashCode = namedenum.namedenum('FlashCode', 
    any               = (0,  'No flash code set'),
    da_usb_2m         = (30, "DA-usb"),
    da_net_2m         = (31, "DA-net (2MB legacy version)"),
    da_trace          = (32, "DA-trace"),
    virtual_dash      = (33, "DA-sim"),
    da_usb_4m_no_dcl  = (34, "DA-usb (4MB no DCL legacy version)"),
    da_net_4m_no_dcl  = (35, "DA-net (4MB no DCL legacy version)"),
    da_usb            = (36, "DA-usb"),
    da_net            = (37, "DA-net"),
    da_cjtag          = (38, "DA-net CJTAG"),
    sp55e             = (55, "SP55e"),
    sp55et            = (56, "SP55et"),
    sp57et            = (57, "SP57et"),
    sp58et            = (58, "SP58et"),
)

def _as_flash_code(flash_code):
    try:
        return FlashCode(flash_code)
    except ValueError:
        return int(flash_code)

class FlashFile(FlashFileBase):
    def __str__(self):
        flash = self.flash_code.__doc__ if not isinstance(self.flash_code, int) else 'Type %d' % self.flash_code
        return '%s - %s - %s' % (self.version, flash, self.path)
    __repr__ = __str__
        
    @property
    def version(self):
        return '%d.%d.%d' % (self.major, self.minor, self.revision)

    @classmethod
    def load(cls, path):
        with open(path, 'rb') as f:
            header = f.read(FlashVersionHeader._size)
        v = FlashVersionHeader._unpack(header)
        rev = int(v.revision.rstrip('\0'))
        flash_code = _as_flash_code(v.flash_code)
        return cls(path, v.major, v.minor, rev, flash_code, v.crc)
                
def rlistdir(path, ext):
    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for f in files:
                if os.path.splitext(f)[1].lower() == ext:
                    yield os.path.join(root, f)
    
def fs_find_files(search_path):
    found = []
    search_path = os.path.expanduser(search_path)
    try:
        for path in rlistdir(search_path, '.fsh'):
            try:
                found.append(FlashFile.load(path))
            except Exception as e:
                print 'Failed to read version from %s : %s' % (path, e)
    except EnvironmentError as e:
        print 'Failed to access search path %s : %s' % (search_path, e)    
    return found

def _as_int(x, default=0):
    try:
        return int(x, 0)
    except (TypeError, ValueError):
        return default

def _as_flash_file(listing_dir, fw):
    '''Convert row of rst table into a FlashFile.
    
    >>> _as_flash_file('/dir', dict(path='a.fsh', version='5.3.2', flash_code='37'))
    5.3.2 - DA-net - /dir/a.fsh
    >>> _as_flash_file('/dir', dict(path='a.fsh', version='5.3.2', flash_code='99'))
    5.3.2 - Type 99 - /dir/a.fsh
    >>> _as_flash_file('/dir', dict(path='a.fsh', version='5.3.', flash_code='x'))
    5.3.0 - No flash code set - /dir/a.fsh
    >>> _as_flash_file('/dir', dict(path='a.fsh', version='xxx'))
    0.0.0 - No flash code set - /dir/a.fsh
    '''
    v = re.match(r'(\d*)(?:.(\d*))(?:.(\d*))', fw.get('version', ''))
    return FlashFile(listing_dir + '/' + fw['path'],
                     _as_int(v.group(1)),
                     _as_int(v.group(2)),
                     _as_int(v.group(3)),
                     _as_flash_code(_as_int(fw.get('flash_code', '0'))),
                     _as_int(fw.get('crc', '0')))

def http_find_files(search_path):
    import urllib2
    listing_dir = os.path.dirname(search_path)
    try:
        listing = urllib2.urlopen(search_path, timeout=10, cafile=get_cacert_file()).read()
        fields, fws = rst.parse_simple_table(listing)
        fws = [dict(zip(fields, fw)) for fw in fws]
        return [_as_flash_file(listing_dir, fw) for fw in fws]
    except Exception as e:
        print 'Failed to retrieve file list from %s : %s' % (search_path, e)
    return []
    
def find_files(search_paths):
    found = []
    for search_path in search_paths:
        if search_path.startswith('http:') or search_path.startswith('https:'):
            found.extend(http_find_files(search_path))
        else:
            found.extend(fs_find_files(search_path))
    return found
        
def sorted_firmwares(found, desired_flash_enc=37, reverse=True):
    return sorted(found,
        key=lambda f: (f.flash_code == desired_flash_enc, f.major, f.minor, f.revision),
        reverse=reverse)
        
def filter_incompatible(found, desired_flash_enc=37):
    return [x for x in found if x.flash_code == desired_flash_enc]

def stable_unique(items, key=None):
    seen = set()
    ret = []
    if not key:
        key = lambda x: x
    for x in items:
        k = key(x)
        if k not in seen:
            seen.add(k)
            ret.append(x)
    return ret
    
def filter_similar(found):
    return stable_unique(found, lambda x:(x.version, x.crc))

def filter_firmware_list(found, flash_code, force=False):
    found = sorted_firmwares(found, flash_code)
    if not force:
        found = filter_incompatible(found, flash_code)
    return filter_similar(found)

class Progress(ProgressInterface):
    def __init__(self):
        self._percentage = 0
        self._last_reported = 0
    def __enter__(self):
        return self
    def __exit__(self, *args):
        pass
        
    def add_message(self, s):
        self._last_reported = self._percentage
        print '%3d%% complete.%s' % (self._percentage, (' ' + s) if s else '')
    def set_percentage(self, percentage):
        self._percentage = int(percentage)
        if (self._percentage - self._last_reported) >= 10:
            self.add_message('')

class AttyProgress(ProgressInterface):
    def __init__(self, width=-1, stream=sys.stdout):
        self._percentage = None
        self._message = ''
        self._previous = 0
        self._stream = stream
        self._width = width

    def __enter__(self):
        self._update()
        return self

    def __exit__(self, *args):
        self._stream.write('\n')
        self._stream.flush()

    def _update(self):
        prefix = '%3d%% - ' % (self._percentage or 0, )
        maxwidth = sys.maxint if self._width == -1 else self._width - len(prefix)
        if len(self._message) > maxwidth:
            maxwidth -= len('...')
            lhalf = rhalf = maxwidth//2
            if lhalf + rhalf < maxwidth:
                lhalf += 1
            message = self._message[:lhalf] + '...' + self._message[-rhalf:]
        else:
            message = self._message.ljust(self._previous)
        self._previous = len(message.rstrip())
        self._stream.write('\r' + prefix + message)
        self._stream.flush()

    def add_message(self, s):
        self._message = s
        self._update()    

    def set_percentage(self, percentage):
        old, self._percentage = self._percentage, int(percentage)
        if self._percentage != old:
            self._update()

def make_progress():
    if sys.stdout.isatty():
        width = results.get_console_width(78)
        return AttyProgress(width=width)
    else:
        return Progress()
        
def default_search_paths():
    return [DEFAULT_URL]
        
#@command()
def firmwareflashcode(device=None):
    '''Get the firmware flash code for the current device.'''
    if device is None:
        device = probe()
    flash_code = device.probe.tiny.GetFirmwareFlashCode()
    try:
        return FlashCode(flash_code)
    except ValueError:
        return flash_code

@command(device_required=False)
def firmwarelist(version=None, search_paths=None, force=False, flash_code=None, max_items=10, device=None):
    '''Find and list firmware releases compatible with the probe.
    
    All of the paths in search_paths are searched recursively for any .fsh 
    files. search_paths may be a list or a string with one or more paths in it, 
    separated by colons on POSIX platforms, or semi-colons on Windows.
    
    If search_paths is not specified then the locations where Codescape 
    Debugger installs firmware are searched.
    
    If version is not None, only versions which match are returned, e.g. 
    version='5.4' will return versions 5.4.9 through 5.4.0.

    If force is False then only firmware releases with compatible flash codes
    are returned.  If flash_code is not given then there must be an active 
    connection to a probe.
    
    The items returned are ordered so that matching firmwares with the greatest 
    firmware version number are first in the list.
    
    '''
    if flash_code is None and not force:
        require_device(device)
        flash_code = device.probe.tiny.GetFirmwareFlashCode()
    if search_paths is None:
        search_paths = default_search_paths()
    if isinstance(search_paths, basestring):
        search_paths = search_paths.split(os.pathsep) 
    original = found = find_files(search_paths)
    if not found:
        raise RuntimeError("No firmware releases found in:\n  " +
            '\n  '.join(search_paths))
    found = sorted_firmwares(found, flash_code)
    if not force:
        found = filter_incompatible(found, flash_code)
    if not found:
        raise RuntimeError("No compatible firmware releases found, candidates were:\n  " +
            '\n  '.join(repr(x) for x in original))
    found = filter_similar(found)
    if version is not None:
        regex = version.replace('.', r'\.').replace('*', r'\d+')
        r = re.compile(regex)
        found = [x for x in found if r.match(x.version)]
    if not found:
        raise RuntimeError("No compatible firmware releases matching filter %s, candidates were:\n  " % version +
            '\n  '.join(repr(x) for x in original))
    return results.NumberedListResult(found[:max_items])

def _read_file(progress, path):
    if path.startswith('http:') or path.startswith('https:'): 
        import urllib2
        progress.add_message('Downloading %s' % (path,))
        with tempfile.NamedTemporaryFile(delete=False) as f:
            try:
                f.write(urllib2.urlopen(path, timeout=60, cafile=get_cacert_file()).read())
                path = f.name
            except Exception:
                f.close()
                os.remove(f.name)
                raise            
    return path

@command()
def firmwareupgrade(path=None, version=None, search_paths=None, force=False, _progress=None, device=None):
    '''Upgrade the firmware of the probe.
    
    path may be a path to a file or one of the results of :func:`~imgtec.console.firmwarelist`.
    
    If path is not specified then the first result from :func:`~imgtec.console.firmwarelist`
    (using the specified search/filter parameters) is used. This updates the 
    probe firmware to the newest firmware.
    
    By default you can not change the flash code of the firmware, under certain 
    circumstances this may be necessary, in which case use force=True.
    '''
    with (_progress or make_progress()) as p:
        flash_code = _as_flash_code(device.probe.tiny.GetFirmwareFlashCode())
        if path is None:
            path = firmwarelist(version, search_paths, force, flash_code, device=device)[0]
        
        if isinstance(path, FlashFile):
            flash_file = path
            path = _read_file(p, flash_file.path)
        else:
            path = _read_file(p, path)
            flash_file = FlashFile.load(path)
            
        if flash_file.flash_code != flash_code:
            if force:
                p.add_message('Warning, flashing target with an incompatible firmware')
                raise NotImplementedError()
            raise RuntimeError(('This firmware (Type %s) is incompatible with the probe (Type %s)\n' + 
                                'Use the force option to override if you are absolutely sure.') % (flash_file.flash_code, flash_code))
        p.add_message('Using flash file: %s' % (flash_file.path,))
        try:
            device.probe.tiny.ReflashFirmware(path, p, None)
            fw = device.tiny.GetFirmwareVersion()
            device.probe.firmware_version = fw
            device.probe.scan_devices()
            device.probe.probe_info = device.probe.tiny.ProbeInfo() # Need to re-read probe caps
            return device.probe
        finally:
            if path != flash_file.path:
                os.remove(path)

def _testprogress():
    values = [0, 10.0, 'New message', 12.0, 13.0, 14.0, 15.0, 30.0, 80.0, 'Nice', 100.0]
    with make_progress() as p:
        for value in values:
            if isinstance(value, str):
                p.add_message(value)
            else:
                p.set_percentage(value)
            time.sleep(0.5)
            
if __name__ == '__main__':
    import doctest
    if doctest.testmod():
        sys.exit()
   
