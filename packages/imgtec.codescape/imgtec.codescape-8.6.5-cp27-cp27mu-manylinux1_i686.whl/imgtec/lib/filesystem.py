import os
from contextlib import contextmanager

@contextmanager
def named_temp(mode='w+b', prefix='', suffix='', delete=False, dir=None):
    """Create and open a named temp file which can be written to and
    then closed, the file will continue to exist until the with block
    is closed.

        with named_temp(prefix='myapp', suffix='.txt') as f:
            f.write('hello world')
            f.close()
            with open(f.name, 'r') as f2:
                assertEquals('hello world', f2.read())

    """
    from tempfile import NamedTemporaryFile
    f = NamedTemporaryFile(mode=mode, prefix=prefix, suffix=suffix, delete=delete, dir=dir)
    try:
        yield f
    finally:
        try:
            f.close()
            os.unlink(f.name)
        except OSError:
            pass

@contextmanager
def named_temp_dir(suffix='', prefix=''):
    """Create temp directory, the directory will continue to exist until the with block is closed."""
    import shutil
    import tempfile
    d = tempfile.mkdtemp(suffix=suffix, prefix=prefix)
    try:
        yield d
    finally:
        try:
            shutil.rmtree(d)
        except OSError:
            pass
