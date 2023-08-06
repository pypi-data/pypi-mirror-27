from imgtec.console.support import *
from imgtec.console.program_file import load, srec, elf, setpc, nosetpc
from imgtec.lib import rst
from imgtec.console.support import named, command, namedstring
from imgtec.console.commands import reset
from textwrap import dedent
from imgtec.test import *

flashremove = named('flashremove')
erase       = named('erase')
chiperase   = named('chiperase')
protect     = named('protect')
unprotect   = named('unprotect')
bankswap    = named('bankswap')

FLASH_MEMORY_TYPE = 64

@command(size=[(flashremove, 0)])
def flashconfig(name=None, address=None, size=None, settings=None, device=None):
    '''
    Configure flash devices or get flash device configurations.
    
    To create a new flash device pass name, address, size and settings::
    
        [s0c0v0] >>> flashconfig('ROM0', 0x20000000, 0x100000, 'type:pic32mz')
        name    ROM0
        address 0x20000000
        size    0x00100000
        type    pic32mz
    
    Settings should be a list of key/value pairs. Multiple settings can be
    seperated by a comma or a new line.

        [s0c0v0] >>> flashconfig()
        ==== ========== ==========
        Name Address    Size
        ==== ========== ==========
        ROM0 0x20000000 0x00100000
        ROM1 0x30000000 0x00200000
        ==== ========== ==========
    
    To get all of the settings for a device, pass the name::
    
        [s0c0v0] >>> flashconfig('ROM1')
        name    ROM1
        address 0x30000000
        size    0x00200000
        type    pic32mz
    
    To update a devices settings, use named keyword parameters::
    
        [s0c0v0] >>> flashconfig('ROM1', size=0x300000)
        name    ROM1
        address 0x30000000
        size    0x00300000
        type    pic32mz
    
    This will fail if the device does not already exist::
    
        [s0c0v0] >>> flashconfig('ROM2', size=0x300000)
        RuntimeError: No flash device of that name, current devices are:
        ==== ========== ==========
        name address    size
        ==== ========== ==========
        ROM0 0x20000000 0x00100000
        ROM1 0x30000000 0x00300000
        ==== ========== ==========

    To create a new device you must pass address, size, and settings
    
    To remove a device, pass the name and use the 'flashremove' named parameter::
    
        [s0c0v0] >>> flashconfig('ROM1', flashremove)
        ==== ========== ==========
        name address    size
        ==== ========== ==========
        ROM0 0x20000000 0x00100000
        ==== ========== ==========
    
    To remove all devices, just use the 'flashremove' named parameter::
    
        [s0c0v0] >>> flashconfig(flashremove)
        ==== ======= ====
        name address size
        ==== ======= ====
        ==== ======= ====
    
    '''
    if size == 0:
        device.tiny.FlashDeviceRemove(name or '')
    elif name is not None:
        params = [address, size, settings]
        #New device/change all settings
        if not None in params:
            device.tiny.FlashDeviceConfigure(name, address, size, settings)
            return flashconfig(name, device=device)
            
        #Get current device settings
        elif all(x is None for x in params):
            fd =  _find_existing_flash_device(name, device)
            fd.settings = device.tiny.FlashDeviceSettings(fd.name)
            return fd
            
        #Update some part of an existing device
        else:
            fd = _find_existing_flash_device(name, device)
            fd.address  = address  if address  is not None else fd.address
            fd.size     = size     if size     is not None else fd.size
            fd.settings = settings if settings is not None else device.tiny.FlashDeviceSettings(fd.name)
            device.tiny.FlashDeviceConfigure(fd.name, fd.address, fd.size, fd.settings)
            return flashconfig(name, device=device)
        
    return FlashDeviceList([FlashDevice(*x) for x in device.tiny.FlashDeviceList()])
    
@command(cmd=[namedstring(chiperase), namedstring(erase), namedstring(reset), namedstring(protect), 
    namedstring(unprotect), namedstring(bankswap)])
def flashcommand(cmd, flash_device=None, address=0, size=0, device=None):
    '''
    Perform a flash command. 
    
    Either supply the flash name as provided in flashconfigure, or specifiy an address range:
    
        [s0c0v0] >>> flashcommand(unprotect, address=0x100000, size=0x1000)
        [s0c0v0] >>> flashcommand(protect, 'program flash')
        [s0c0v0] >>> flashcommand(reset, 'boot flash')
        [s0c0v0] >>> flashcommand(erase, address=0x100000, sise=0x1000)
        [s0c0v0] >>> flashcommand(chiperase, 'boot flash')

    '''
    if flash_device is None:
        #Use first/only device
        device.tiny.FlashDeviceCommand(cmd, address, size)
    else:
        name = flash_device.name if isinstance(flash_device, FlashDevice) else flash_device
        fdev = _find_existing_flash_device(name, device)
        device.tiny.FlashDeviceCommand(cmd, fdev.address, fdev.size)

class FlashDevice(object):
    _columns = ['name', 'address', 'size']

    def __init__(self, name, address, size, settings=None):
        self.name, self.address, self.size, self.settings = name, address, size, settings

    @property
    def sizehr(self):
        return '0x%08x' % (self.size,) # TODO kb/mb

    def _as_cells(self):
        return (self.name, '0x%08x' % (self.address,), self.sizehr)

    def __repr__(self):
        settings = zip(FlashDevice._columns, self._as_cells())
        settings += split_settings(self.settings)
        return rst.headerless_table(settings)
        
def split_settings(setting_str):
    """
    >>> split_settings('type:pic32')
    [('type', 'pic32')]
    >>> split_settings('type=pic64')
    [('type', 'pic64')]
    >>> split_settings('type    =pic64,   size=    100')
    [('type', 'pic64'), ('size', '100')]
    >>> split_settings(\
    "type=pic45\\n"\
    "size=145\\n")
    [('type', 'pic45'), ('size', '145')]
    """
    rows = []
    for line in setting_str.splitlines():
        settings = line.split(',')
        for s in settings:
            name, value = s.split('=') if '=' in s else s.split(':')
            rows.append((name.strip(), value.strip()))
    return rows

class FlashDeviceList(list):
    def __repr__(self):
        return rst.simple_table(FlashDevice._columns,
            [x._as_cells() for x in self])

def _find_existing_flash_device(name, device):
    devices = FlashDeviceList([FlashDevice(*x) for x in device.tiny.FlashDeviceList()])
    for dev in devices:
        if dev.name == name:
            return dev
    
    raise RuntimeError(dedent('''\
        No flash device of name '%s', current devices are:
        %r
        To create a new device you must pass address, size, and settings''') % (name, devices))
    
#helper for loading flash files
class FlashMemoryProxy(object):
    def __init__(self, device, verbose=False):
        #The 'real' device, which has the real DA
        self.device = device
        #Redirect device.da calls to this object (only catching what load uses)
        self.da = self
        self.verbose = verbose
        
    def CpuInfo(self, update=False):
        return self.device.da.CpuInfo(update)
        
    def GetEndian(self):
        return self.device.da.GetEndian()
        
    def WriteMemoryBlock(self, address, count, elem_size, data):
        self.device.da.WriteMemoryBlock(address, count, elem_size, data, FLASH_MEMORY_TYPE)
        
    def ReadMemoryBlock(self, address, count, elem_size):
        #This can always be done normally
        return self.device.da.ReadMemoryBlock(address, count, elem_size)
        
    def __getattr__(self, name):
        try:
            return getattr(self.device, name)
        except AttributeError:
            return getattr(self.device.da, name)

@command(
    type=[namedstring(srec), namedstring(hex), namedstring(auto), 
           namedstring(elf), namedstring(bin)],
     verbose=verbosity,
     setpc=[(setpc, True), (nosetpc, False)],
     verify=[(verify, True), (noverify, False)],
 )
def flashload(filename, setpc=True, verify=False, verbose=True, base_addr=None, 
    erase_all=False, unprotect_all=True, type='auto', device=None):
    r'''
    Write a file to memory, automatically handling any address which reside in flash device.
    For a binary file supply a base address.
    
    ============== ============================================================================
    Parameter      Meaning
    ============== ============================================================================
    filename       The path to the file to be loaded. See note for details.
    type           Type of file to be loaded. 'srec', 'elf', 'bin', 'hex' or 'auto'.
    verify         If True data written will be read back and compared to the file's contents.
    verbose        Set True to see progress messages during the load.
    setpc          If True set the PC to the file's entry address. 'setpc' or 'nosetpc'.
    base_addr      Address to begin loading a binary file at. Only used with bin files.
    erase_all      Erase all flash devices before loading the file.
    unprotect_all  Remove write protection from all flash devices before loading the file.
    ============== ============================================================================
    
    Python will treat back slash followed by certain characters as escape sequences, for example 
    load("C:\\foo\\trunk") becomes load("C:\\foo<tab>trunk")
    
    To avoid this, you can either double up all slashes, use the raw string prefix 'r', or 
    use forward slashes. For example::
    
      load("C:\\foo\\trunk")
      load(r"C:\foo\trunk")
      load("C:/foo/trunk")
    
    '''
    if unprotect_all:
        print "Removing Flash Protection"
        for flashd in flashconfig(device=device):
            flashcommand(unprotect,flashd.name)
    
    if erase_all:
        for flashd in flashconfig(device=device):
            print "erasing device: ",flashd.name
            flashcommand(erase,flashd.name)
            
    #Replace current device.da with our proxy object
    flash_device = FlashMemoryProxy(device, verbose=verbose)
    #Load command can function normally via the proxy
    load(filename, setpc=setpc, verify=verify, verbose=verbose, base_addr=base_addr, 
        type=type, device=flash_device)
        
if __name__ == '__main__':
    test.main()