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

from imgtec.console.support import *
from imgtec.console.program_file import load
from imgtec.console.memory import word
from imgtec.console.flash import FlashMemoryProxy
from imgtec.console.results import StrResult
from imgtec.lib.namedbitfield import namedbitfield
from contextlib import contextmanager
from imgtec.test import *
from textwrap import dedent
import time

class FlashMemoryError(Exception):
    pass

class FlashSettings(object):
    def __init__(self):
        self.base_address        = 0xbe000000
        self.device_timeout      = 5
        self.block_write_timeout = 5
        self.erase_timeout       = 15
        self.block_size          = 0x00020000 #64k blocks * 2 devices
    
    def __repr__(self): 
        return dedent('''\
                   Base Address : 0x%x
                 Device Timeout : %ds
            Block Write Timeout : %ds
                  Erase Timeout : %ds
                     Block Size : 0x%08x''' %
                  (self.base_address, self.device_timeout, self.block_write_timeout,
                   self.erase_timeout, self.block_size))
        
flash_settings = FlashSettings()
print "The current Flash Memory settings are:"
print repr(flash_settings)
print "If these are not correct please change them using the 'flashsettings' command."

#Values written to trigger both devices
ENTER_MODE             = 0x00700070
EXIT_MODE              = 0x00FF00FF
FULL_ERASE             = 0x00300030
BLOCK_ERASE            = 0x00200020
CONFIRM                = 0x00d000d0
WRITE_WORD             = 0x00400040
MULTI_WORD             = 0x00e800e8
CLEAR_STATUS           = 0x00500050
READ_ID_CODES          = 0x00900090
QUERY                  = 0x00980098
LOCK_BIT_SETUP         = 0x00600060
LOCK_BIT_SET_CONFIRM   = 0x00010001
LOCK_BIT_CLEAR_CONFIRM = 0x00d000d0

#Offsets for reading query registers
OFFSET_PRIM_VEND_CODE     = 0x13
OFFSET_DEVICE_SIZE        = 0x27
OFFSET_MAX_MULTI_WORD     = 0x2a
OFFSET_NUM_ERASE_BLOCKS   = 0x2d
OFFSET_BLOCK_STATUS       = 0x02

#The usual register
Status = namedbitfield('Status', 
    [('wsms', 7), ('bess', 6), ('ecblbs', 5), ('wsblbs', 4), ('vpps', 3), 
        ('wss', 2), ('dps', 1), ('r', 0)])
        
#Appears during a multi word write
ExtendedStatus = namedbitfield('ExtendedStatus', [('sms', 7)])

BlockStatus = namedbitfield('BlockStatus',
    [('erase_success', 1), ('locked', 0)])
    
@command()
def flashsettings(base_address=None, device_timeout=None, block_write_timeout=None, 
    erase_timeout=None, block_size=None):
    '''
    Change the or view the current flash memory settings.
    
    =================== ================================================================================
    Parameter           Meaning
    =================== ================================================================================
    base_address        Start address of the flash memory.
    device_timeout      Amount of time to wait for the flash devices to be ready for general operations.
    block_write_timeout Amount of time to wait for a block write to complete.
    erase_timeout       Amount of time to wait for a full device erase to complete.
    block_size          Flash memory block size in 
    =================== ================================================================================
    '''
    
    if base_address is not None:
        flash_settings.base_address = base_address
    if device_timeout is not None:
        flash_settings.device_timeout = device_timeout
    if block_write_timeout is not None:
        flash_settings.block_write_timeout = block_write_timeout
    if erase_timeout is not None:
        flash_settings.erase_timeout = erase_timeout
    if block_size is not None:
        flash_settings.block_size = block_size
    return flash_settings
    
@command()
def flashinfo(device=None):
    '''
    Get the flash device's info registers.
    '''
    with flash_mode(device):
        return get_flash_info(device)
        
def get_flash_info(device):
    word(flash_settings.base_address, READ_ID_CODES, verify=False, device=device)
    man_codes = split_word(word(flash_settings.base_address, device=device))
    dev_codes = split_word(word(flash_settings.base_address+4, device=device))
    
    word(flash_settings.base_address, QUERY, verify=False, device=device)
    
    prim_vend_codes = read_8_bit_query_register(OFFSET_PRIM_VEND_CODE, device)
    
    device_sizes = split_word(word(flash_settings.base_address+(OFFSET_DEVICE_SIZE*4), device=device))
    device_sizes = [2**size for size in device_sizes]
    
    max_multi_words = read_8_bit_query_register(OFFSET_MAX_MULTI_WORD, device, swap=True)
    max_multi_words = [2**val for val in max_multi_words]
    
    num_erase_blocks = read_8_bit_query_register(OFFSET_NUM_ERASE_BLOCKS, device, swap=True) 
    num_erase_blocks = [num+1 for num in num_erase_blocks]
                       
    return MaltaFlashDeviceList(
        MaltaFlashDevice(*details) for details in zip(
            man_codes, dev_codes, prim_vend_codes, device_sizes, max_multi_words, num_erase_blocks))
            
def read_8_bit_query_register(word_offset, device, swap=False):
    regs = [split_word(word(flash_settings.base_address+(word_offset*4), device=device)),
            split_word(word(flash_settings.base_address+((word_offset+1)*4), device=device))]
    
    if swap:
        regs = [((msw&0xff) << 8) | (lsw&0xff) for lsw,msw in zip(*regs)]
    else:
        regs = [((msw&0xff) << 8) | (lsw&0xff) for msw,lsw in zip(*regs)]
        
    return regs
        
@command()
def flasherase(device=None):
    '''
    Erase the flash contents.
    '''
    with flash_mode(device):
        word(flash_settings.base_address, FULL_ERASE, verify=False, device=device)
        word(flash_settings.base_address, CONFIRM, verify=False, device=device)
        wait_for_devices(device, timeout=flash_settings.erase_timeout)
        status_1, status_2 = _read_devices_status(device)
        
        for i, status in enumerate([status_1, status_2]):
            if status.vpps:
                raise FlashMemoryError('Full device %d erase failed with a Vpp range error.' % i)
        
            if status.wsblbs and status.ecblbs:
                raise FlashMemoryError('Full device %d erase failed with a command sequence error.' % i)
        
            if status.ecblbs:
                raise FlashMemoryError('Full device %d erase failed with a full chip erase error.' % i)
    
    print "Devices erased successfully."
    
@command()
def flashloadfile(path, verify=True, verbose=True, base_address=None, device=None):
    '''
    Write a file to flash memory, erases all contents beforehand.
    For a binary file supply a base address, for other types confirm that the file's
    addresses are in the flash range before loading.
    '''
    flasherase(device=device)
    #Replace current device.da with our proxy object
    flash_device = MaltaFlashMemoryDA(device, verbose=verbose)
    #Load command can function normally via the proxy
    load(path, setpc=False, verify=verify, verbose=verbose, base_addr=base_address, 
        device=flash_device)
    
@command()
def flasheraseblock(address, device=None):
    '''
    Erase the block of flash that contains address.
    These are in 128k (0x200000) sections, because there are 2 devices.
    '''
    with flash_mode(device):
        word(address, BLOCK_ERASE, verify=False, device=device)
        word(address, CONFIRM, verify=False, device=device)
        wait_for_devices(device)
        
@command()
def flashenterreflash(device=None):
    '''
    Enter the reflash mode and wait for the device to be ready.
    '''
    #Put us into reflash mode by writing to the start of flash
    original = word(flash_settings.base_address, device=device)
    word(flash_settings.base_address, ENTER_MODE, verify=False, device=device)
    
    #Wait for the devices to become ready
    try:
        wait_for_devices(device)
    except FlashMemoryError as e:
        word(flash_settings.base_address, original, verify=False, device=device)
        raise e
    
    return StrResult("Devices are ready.")
    
@command()
def flashexitreflash(device=None):
    '''
    Exit the reflash mode.
    '''
    word(flash_settings.base_address, EXIT_MODE, verify=False, device=device)
    
@command()
def flashwriteblock(address, values, verbose=False, device=None):
    '''
    Write a list of 32 bit values starting from address (data size may exceed a 
    single flash block).
    '''
    with flash_mode(device):
        _flashwrite32_from_list(address, values, device, verbose=verbose)
        
@command()
def flashwrite32(address, value, device=None):
    '''
    Write a single 32 bit word to the address given.
    '''
    with flash_mode(device):
        word(address, WRITE_WORD, verify=False, device=device)
        word(address, value, verify=False, device=device)
        wait_for_devices(device)
            
@command()
def flashclearstatus(device=None):
    '''
    Reset the status register. Do this after an error to reset the device.
    '''
    with flash_mode(device):
        word(flash_settings.base_address, CLEAR_STATUS, device=device)
        
@command()
def flashclearlockbits(device=None):
    '''
    Clear all block lock bits.
    '''
    with flash_mode(device):
        word(flash_settings.base_address, LOCK_BIT_SETUP, device=device)
        word(flash_settings.base_address, LOCK_BIT_CLEAR_CONFIRM, device=device)
        wait_for_devices(device)

@command()
def flashsetlockbit(address, device=None):
    '''
    Set the lock bit on the block that starts at the given address.
    '''
    if (address-flash_settings.base_address) % flash_settings.block_size:
        raise FlashMemoryError('Address must be the beginning of a block.')
    
    with flash_mode(device):
        word(address, LOCK_BIT_SETUP, device=device)
        word(address, LOCK_BIT_SET_CONFIRM, device=device)
        wait_for_devices(device)
        
class BlockStatusList(list):
    def __repr__(self):
        return '\n'.join([repr(i) for i in self])
    
@command()
def flashblockstatus(address, device):
    '''
    Get the status of the block at address.
    '''
    #Align to the nearest block start
    address -= ((address-flash_settings.base_address) % flash_settings.block_size)
    
    with flash_mode(device):
        word(flash_settings.base_address, QUERY)
        # At this point the first word will be 0x00b000b0, this is NOT an error
        # it just looks a lot like one but is in fact part of the manufacture code.
        stat = [BlockStatus(val) for val in split_word(word(address+(OFFSET_BLOCK_STATUS*4), device=device))]
        return BlockStatusList(stat)

def split_word(value):
    '''
    Given a 32 bit value return a tuple of 2 16 bit values, most significant
    then least significant.
    Used because we have 2 16 bit devices to make up the 32 bit width.
    '''
    return (value >> 16, value & 0xffff)
    
def wait_for_devices(device, timeout=None):
    if timeout is None:
        timeout = flash_settings.device_timeout
        
    status_1, status_2 = Status(0), Status(0)
    start = time.time()
    
    while True:
        status_1, status_2 = _read_devices_status(device) 
        if status_1.wsms and status_2.wsms:
            break 

        if (time.time() - start) > timeout:
            raise FlashMemoryError(
                'Timed out waiting for a flash device to be ready. Status1: 0x%04x Status2: 0x%04x'
                % (status_1, status_2))
        
    if status_1.dps or status_2.dps:
        raise FlashMemoryError('Operation failed with a device protect error.')
        
def _read_device_register(device):
    '''
    Read a word from the devices and return it split into 2 16 bit words.
    '''
    return split_word(word(flash_settings.base_address, device=device))
    
def _read_devices_status(device):
    #32 bit word contains both device's status register value
    status_1, status_2 = _read_device_register(device)
    status_1, status_2 = Status(status_1), Status(status_2)
    return (status_1, status_2)
    
@contextmanager
def flash_mode(device):
    #Use this to run code in reflash mode
    flashenterreflash(device=device)
    try:
        yield
    finally:
        #Exit even if there's an issue
        flashexitreflash(device=device)
        
class MaltaFlashDevice(object):
    def __init__(self, man_code, dev_code, prim_vend_code, size, max_multi_words, 
        num_erase_blocks):
        self.man_code         = man_code
        self.dev_code         = dev_code
        self.prim_vend_code   = prim_vend_code
        self.size             = size
        self.max_multi_words  = max_multi_words
        self.num_erase_blocks = num_erase_blocks
        
    def __repr__(self):
        return dedent('''\
                Manufacturer ID   : 0x%x
                      Device ID   : 0x%x
            Primary Vendor Code   : 0x%x
            Size                  : %dM bytes
            Max Multi Byte Write  : %d bytes
            Number of erase blocks: %d''') % (
                self.man_code, self.dev_code, self.prim_vend_code, 
                self.size//(1024**2), self.max_multi_words, 
                self.num_erase_blocks)
        
class MaltaFlashDeviceList(list):
    def __repr__(self):
        return '\n'.join([repr(item) for item in self])
        
def _flashwrite32_from_list(address, values, device, verbose=False):
    # No more than 15 words per block write
    # The write cannot go across blocks
    write_blocks = split_values_for_block_write(address, values)
    for addr, vals in write_blocks:
        flash_write_block(addr, vals, device, verbose=verbose)
    
def split_values_for_block_write(address, values):
    '''
    Given a list of values to be written starting at address, split those values
    into chunks of either 15 words or as much as can fit before a block boundary.
    Returns a list of tuples of (address, [values]).
    
    Note: doesn't handle addresses that aren't 32 bit aligned, may cause issues.
    '''
    #Final list of write operations
    write_chunks = []
    #Rolling address value
    temp_addr    = address
    #The block we're starting in
    block        = address // flash_settings.block_size
    temp_chunk   = []
    #The start address of the current list we're building
    chunk_addr   = address
    
    for value in values:
        #Not really interested in which block in particular, just when it changes
        current_block = (temp_addr)//flash_settings.block_size
        
        #If we've changed block or are at max size add this operation to the main list
        if current_block != block or len(temp_chunk) >= 16:
            write_chunks.append((chunk_addr, temp_chunk))
            #The next operation will start at the current rolling address
            chunk_addr = temp_addr
            #Note the new block we're in
            block = current_block
            temp_chunk = []
        
        temp_chunk.append(value)
        temp_addr += 4
    
    #Get last section which isn't caught by the if
    write_chunks.append((chunk_addr, temp_chunk))
    
    return write_chunks
    
def flash_write_block(address, values, device, verbose=False):
    if verbose:
        print "Writing block at 0x%x" % (address)
    
    if len(values) > 16:
        raise FlashMemoryError('Cannot write more than 16 32 bit words in one command.')
    
    #Triggers command
    word(address, MULTI_WORD, verify=False, device=device)
    
    _wait_for_extended_ready(device, address, command=MULTI_WORD)
    
    #Number of words - 1
    num_words = len(values)-1
    #Must be given to both devices
    num_words = num_words | (num_words << 16)
    word(address, num_words, verify=False, device=device)
    
    # Write the data starting at the destination address
    # The spec claims you write the first one at the start and subsequent at device,
    # but this works fine.
    word(address, values, device=device)
        
    #Finish command
    word(flash_settings.base_address, CONFIRM, device=device)
    
    wait_for_devices(device)
    
def _wait_for_extended_ready(device, address, command=None, timeout=None):
    if timeout is None:
        timeout = flash_settings.block_write_timeout
    
    #Wait to see if the device is ready for multi word writes
    start = time.time()
    
    while True:
        #Make sure to not write the command more than once
        sms_1, sms_2 = _read_device_register(device)
        sms_1, sms_2 = (ExtendedStatus(val).sms for val in [sms_1, sms_2])
        
        if sms_1 and sms_2:
            break
            
        if (time.time() - start) > timeout:
            raise FlashMemoryError('Timed out waiting for devices to be ready for multi word write.')
        
        if command is not None:
            #Write the command again
            word(address, MULTI_WORD, verify=False, device=device)
        
class MaltaFlashMemoryDA(FlashMemoryProxy):
    def WriteMemoryBlock(self, address, count, elem_size, data):
        #Note that the command will exit reflash mode, so subsequent reads
        #(for verify) will read normally.
        flashwriteblock(address, data[:count], device=self.device, verbose=self.verbose)
