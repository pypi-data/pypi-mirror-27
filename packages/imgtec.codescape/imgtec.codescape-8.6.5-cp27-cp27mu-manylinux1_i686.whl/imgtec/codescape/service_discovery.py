from imgtec.lib.namedstruct import namedstruct
from textwrap import dedent
from contextlib import contextmanager
import sys
from ctypes import *

LocalService = namedstruct('LocalService', dedent('''\
    256s host=""
    64s  type=""
    64s  name=""
    H    port
    510s desc=""
    124s spare=""
    I    hash''').splitlines(), prefix='=')
assert LocalService._size == 1024

LocalServicesHeader = namedstruct('LocalServices', dedent('''\
    I    size''').splitlines(), prefix='=')

MAX_SERVICES = 256
REVERSE_COMPANY_NAME = 'com.imgtec'


def _make_private_fs_name(name):
    return ".{}.{}".format(REVERSE_COMPANY_NAME, name)

def _make_service_name(service_type, property):
    return _make_private_fs_name("service.{}.{}".format(service_type, property))

def _shm_name(service_type):
    return _make_service_name(service_type, 'shm')

def _named_mutex_name(service_type):
    return _make_service_name(service_type, 'mutex')

def _service_lock_name(service):
    name = 'lock.' + service.name
    if service.hash:
        name += '!{:08x}'.format(service.hash)
    return _make_service_name(service.type, name)


class NamedMutexBase(object):
    @contextmanager
    def lock(self):
        '''Lock the mutex, block until available.'''
        try:
            yield self._timed_lock(None)
        finally:
            self._unlock()

    @contextmanager
    def timed_lock(self, seconds):
        '''Try to lock the mutex for a period of time, if it was
        successfully locked yield True.'''
        try:
            yield self._timed_lock(seconds)
        finally:
            self._unlock()

    @contextmanager
    def try_lock(self):
        '''Try to lock the mutex, if it was successfully locked yield a True.

        with l.try_lock() as locked:
            if locked:
                print 'The lock was successfully acquired'
            else
                print 'The lock was not acquired because another process had it locked'
        '''
        try:
            yield self._timed_lock(0)
        finally:
            self._unlock()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._close()

if sys.platform == 'win32':
    from ctypes.wintypes import BOOL
    DWORD     = c_ulong
    HANDLE    = c_void_p
    LPVOID    = c_void_p
    CloseHandle               = windll.kernel32.CloseHandle
    CloseHandle.args          = [HANDLE]
    OpenFileMapping           = windll.kernel32.OpenFileMappingA
    OpenFileMapping.restype   = HANDLE
    OpenFileMapping.args      = [HANDLE, LPVOID, DWORD, DWORD, DWORD, c_char_p]
    CreateFileMapping         = windll.kernel32.CreateFileMappingA
    CreateFileMapping.restype = HANDLE

    GetLastError          = windll.kernel32.GetLastError
    MapViewOfFile         = windll.kernel32.MapViewOfFile
    MapViewOfFile.restype = c_void_p
    UnmapViewOfFile       = windll.kernel32.UnmapViewOfFile

    PAGE_READWRITE = DWORD(4)
    FILE_MAP_WRITE = DWORD(2)

    CreateMutex = windll.kernel32.CreateMutexA
    CreateMutex.restype = HANDLE
    CreateMutex.args = [LPVOID, BOOL, c_char_p]
    ReleaseMutex = windll.kernel32.ReleaseMutex
    ReleaseMutex.args = [HANDLE]
    WaitForSingleObject = windll.kernel32.WaitForSingleObject
    WaitForSingleObject.restype = DWORD
    WaitForSingleObject.args = [HANDLE, DWORD]

    WAIT_TIMEOUT = 0x102
    WAIT_OBJECT_0 = 0
    WAIT_ABANDONED = 0x80
    WAIT_FAILED = 0xffffffff
    INFINITE = 0xffffffff

    class NamedMutex(NamedMutexBase):
        def __init__(self, name):
            self.m = CreateMutex(None, False, name)
            print name, self.m
            self.name = name

        def _timed_lock(self, seconds=None):
            timeout = INFINITE if seconds is None else int(seconds * 1000.0)
            res = WaitForSingleObject(self.m, timeout)
            if res == WAIT_FAILED:
                res
            print hex(res), self.name, GetLastError(), self.m
                
            return res != WAIT_TIMEOUT

        def _unlock(self):
            ReleaseMutex(self.m)

        def _close(self):
            if self.m:
                CloseHandle(self.m)
            self.m = None

    @contextmanager
    def open_or_create_mapping(name, size):
        handle = OpenFileMapping(FILE_MAP_WRITE, False, name)
        created = not bool(handle)
        if not handle:
            handle = CreateFileMapping(HANDLE(-1), None, PAGE_READWRITE, 0, size, name)
        if not handle:
            raise RuntimeError('failed to create shared memory %d' % GetLastError())
        try:
            yield handle, created
        finally:
            CloseHandle(handle)

    @contextmanager
    def map_view(handle, size):
        ptr    = MapViewOfFile(handle, FILE_MAP_WRITE, 0, 0, size)
        if not ptr:
            raise RuntimeError('failed to map view of shared memory %d' % GetLastError())
        try:
            yield ptr
        finally:
            UnmapViewOfFile(ptr)

    def read_shared_memory(name, size):
        with open_or_create_mapping(name, size) as (handle, created):
            with map_view(handle, size if created else 0) as ptr:
                buffer = create_string_buffer(size)
                memmove(byref(buffer), ptr, size)
                return buffer.raw
else:
    import errno
    import fcntl
    import os
    import time

    # code adapted from Stevens - Advanced Programming In The UNIX Environment 12.3
    class NamedMutex(NamedMutexBase):
        def __init__(self, name):
            path =  "/var/tmp/" + _make_private_fs_name(name)
            old = os.umask(0)
            try:
                self.fd = os.open(path, os.O_WRONLY | os.O_CREAT, int('0666', 0))
            finally:
                os.umask(old)
            self.name = name

        def _try_lock(self):
            try:
                fcntl.lockf(self.fd, fcntl.LOCK_EX|fcntl.LOCK_NB, 1)
                return True
            except IOError as e:
                if e.errno in (errno.EACCES, errno.EAGAIN):
                    return False
                raise

        def _timed_lock(self, seconds=None):
            target = None
            if seconds:
                target = time.time() + seconds
            while 1:
                locked = self._try_lock()
                if locked:
                    print 'Now locked'
                    return True
                elif seconds == 0 or (target and target > time.time()):
                    return False
                time.sleep(0.05)

        def _unlock(self):
            fcntl.lockf(self.fd, fcntl.LOCK_UN, 1)

        def _close(self):
            if self.fd:
                os.close(self.fd)
            self.fd = None

    def read_shared_memory(name, size):
        with open('/dev/shm/'+ name) as f:
            return f.read(size)

def _trim_nulls_from_string(struct, field):
    s = getattr(struct, field)
    try:
        s = s[:s.index('\x00')]
        setattr(struct, field, s)
    except ValueError:
        pass

def parse_local_services(buffer):
    entries = []
    header = LocalServicesHeader._unpack_from(buffer)
    offset = LocalServicesHeader._size
    while (len(buffer) - offset) > LocalService._size and len(entries) < header.size:
        service = LocalService._unpack_from(buffer, offset)
        for field in ['host', 'type', 'name', 'desc', 'spare']:
            _trim_nulls_from_string(service, field)
        if service.host and service.type and service.name and service.port:
            entries.append(service)
        else:
            break
        offset += LocalService._size
    return entries

def read_services(service_type):
    with NamedMutex(_named_mutex_name(service_type)) as m:
        with m.lock():
            shm = read_shared_memory(_shm_name(service_type), LocalService._size*MAX_SERVICES+LocalServicesHeader._size)
            services = parse_local_services(shm)
            alive_services = []
            for service in services:
                with NamedMutex(_service_lock_name(service)) as slock:
                    with slock.try_lock() as now_locked:
                        if not now_locked:
                            alive_services.append(service)
            return alive_services

if __name__ == '__main__':
    from imgtec.lib import rst
    JOYNER_SERVICE = '_imgtec-da._tcp'
    rows = []
    for service in read_services(JOYNER_SERVICE):
        rows.append([service.name, '{}:{}'.format(service.host, service.port)])
    print rst.simple_table(['Name', 'Location'], rows)




