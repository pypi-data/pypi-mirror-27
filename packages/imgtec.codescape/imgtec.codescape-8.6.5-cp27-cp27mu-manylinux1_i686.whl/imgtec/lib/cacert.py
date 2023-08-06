import os
import platform
import sys

def get_cacert_file():
    cacert = os.environ.get('MIPS_CACERT_FILE')
    if cacert is None and platform.system() != 'Windows':
        if not hasattr(sys, 'frozen'):
            try:
                import certifi
                cacert = certifi.where()
            except ImportError:
                pass
        else:
            exeroot = os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding()))
            cacert = os.path.join(exeroot, 'cacert.pem')
    if cacert is not None:
        if os.path.isfile(cacert):
            return cacert
        else:
            print 'Warning: SSL certificate file does not exist: %s' % cacert
            print 'Override by setting environment variable MIPS_CACERT_FILE'

if __name__ == '__main__':
    print get_cacert_file()
