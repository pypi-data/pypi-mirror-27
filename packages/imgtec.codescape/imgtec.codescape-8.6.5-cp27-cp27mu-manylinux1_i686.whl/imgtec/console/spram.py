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
from imgtec.console.results import *
from imgtec.console.cache import INDEX_LOAD_TAG, INDEX_STORE_TAG, KSEG0_START, restore_regs, cacheop
from imgtec.console.cfg import config
from imgtec.console.memory import dump
from imgtec.console.regs import regmodify
from imgtec.lib.rst import simple_table

spram_regs = ['ITagLo', 'ITagHi', 'IDataLo', 'IDataHi',
              'DTagLo', 'DTagHi', 'DDataLo', 'DDataHi',
              'ErrCtl']

class SpramException(Exception):
    pass

VALID_MASK   = 0x00000080 # Valid bit from tag, used as spram enable
LOCKED_MASK  = 0x00000020 # Lock bit may allow uncached reference (M14Kc.)
SETTING_NAME = 'Use ISPRAM'

def num_bytes_to_num_words(num):
    words = num//4
    if num % 4:
        words += 4
    return words
    
def narrow_cache(device):
    """ (M)4K M14K and uCAptiv have only 32bit wide cache data path"""
    prid = device.tiny.ReadRegister('prid')
    prid = (prid >> 8) & 0xFF
    
    return prid in [
    128, # "4K";
    131, #  "4Kmp";
    132, #  "4KEc";
    133, #  "4KEmp";
    134, #  "4KSc";
    135, #  "M4K";
    144, #  "4KEc (R2 comp)";
    145, #  "4KEmp(R2 comp)";
    146, #  "4Ksd";
    155, #  "M14KE";
    156, #  "M14KEc";
    157, #  "MicroAptiv uC";
    158, #  "MicroAptiv uP";
    166, #  "M5150 (Virtuoso) uC";
    167, #  "M5150 (Virtuoso) uP";
    ]

class Spram(object):
    #Overidden by subclasses
    offset    = -1
    enable    = -1
    type      = None
    name      = None
    taglo_reg = None
    
    def __init__(self, device, init=True):
        self.mask                  = 0x7
        self.tag_offset            = 0
        #Is it there at all
        self.present               = False
        #Is it on
        self.enabled               = False
        self.size                  = 0
        self.base_physical_address = 0
        self.physical_address_mask = 0
        self.narrow_cache          = False
        
        if init:
            self.post_init(device)
            
    def post_init(self, device):
        self.narrow_cache = narrow_cache(device)
        config0 = device.tiny.ReadRegister('config')
        
        #Check that the SPRAM exists
        if config0 & (1 << self.enable):
            config1 = device.tiny.ReadRegister('config1')
            self.present = True
            
            #Get the 'tag offset', which is basically the line size
            tag_offset = (config1 >> self.offset) & self.mask
            
            if not self.narrow_cache and tag_offset:
                tag_offset -= 2
            
            #If the target doesn't have caches then we'll have to guess based on Prid
            #as a line size of 0 is used to indicate no cache.
            if tag_offset:
                self.tag_offset = 2 * (2 << (tag_offset - 1))
            else:
                #Guess by knowing how wide the cache interface is
                if self.narrow_cache:
                    self.tag_offset = 16 #in bytes per line
                else:
                    self.tag_offset = 8 #in words per line
                    
        if self.narrow_cache:
            #Bits 31-10 are the address
            self.physical_address_mask = 0xfffffc00
        else:
            #Bits 32-12 are the address
            self.physical_address_mask = 0xfffff000
            
        if self.narrow_cache:
            self.taglo_reg = 'ITagLo'
                
    def enable_access(self, device):
        #Set SPR, clear WST. Access will be disabled by the caller restoring registers
        regmodify('ErrCtl', _new_value=0b01<<28, _modify_mask=0b11<<28, device=device)

    def read_config(self, device):
        cacheop(self.type, KSEG0_START, self.tag_offset, INDEX_LOAD_TAG, device=device)
        spram_tag_0 = device.tiny.ReadRegister(self.taglo_reg)
        
        #Tag1 is 1 * tag_offset away
        cacheop(self.type, KSEG0_START + self.tag_offset, self.tag_offset, INDEX_LOAD_TAG, device=device)
        #This uses taglo again because the cacheop offset was changed
        spram_tag_1 = device.tiny.ReadRegister(self.taglo_reg)
        
        self._process_config(spram_tag_0, spram_tag_1)
    
    def _process_config(self, spram_tag_0, spram_tag_1):
        #Physical address is in spram_tag_0
        self.base_physical_address = spram_tag_0 & self.physical_address_mask
        
        #Bit 7 is the enable
        self.enabled = bool(spram_tag_0 & (1 << 7))
        
        #Size is in tag 1
        if self.narrow_cache:
            #Size in 16 byte lines, so multiply by 16 to get bytes
            self.size = ((spram_tag_1 & self.physical_address_mask) >> 10) * 16
        else:
            #Assuming size is in bytes otherwise
            self.size = spram_tag_1 & self.physical_address_mask
            
    def setup(self, enable, base_physical_address, device):
        #Load Tag 0
        cacheop(self.type, KSEG0_START, self.tag_offset, INDEX_LOAD_TAG, device=device)
        
        new_mask = 0
        new_value = 0
        
        if enable is not None:
            self.enabled = bool(enable)
            if enable:
                new_value |= VALID_MASK | LOCKED_MASK
            
            new_mask |= VALID_MASK | LOCKED_MASK
            
        if base_physical_address is not None:
            new_mask |= self.physical_address_mask
            self.base_physical_address = base_physical_address & self.physical_address_mask
            new_value |= self.base_physical_address
            
        regmodify(self.taglo_reg, _new_value=new_value, _modify_mask=new_mask, device=device)
        
        #Store
        cacheop(self.type, KSEG0_START, self.tag_offset, INDEX_STORE_TAG, device=device)
            
    def __nonzero__(self):
        return self.present
        
    def __repr__(self):
        return simple_table(['Type', 'Size (bytes)', 'Base Address', 'Enabled'],
                    [[self.name, str(self.size), '0x%08x' % self.base_physical_address, 
                      str(self.enabled)]])
        
class InstSpram(Spram):
    offset = 19
    enable = 24
    type   = 'instr'
    name   = 'ISPRAM'
    taglo_reg = 'ITagLo'
    
    def setup(self, enable, base_physical_address, device):
        super(InstSpram, self).setup(enable, base_physical_address, device)
        
        #Refresh probe config
        if config(SETTING_NAME, device=device):
            config(SETTING_NAME, 0, device=device)
            config(SETTING_NAME, 1, device=device)
    
    def fill(self, byte_count, device):
        old_config = config(SETTING_NAME)
        old_enabled = self.enabled
        
        try:
            config(SETTING_NAME, 0, device=device)
            #DA won't actually turn them off, just doesn't redirect data accesses
            self.setup(False, None, device)
            
            data_count = num_bytes_to_num_words(byte_count)
            virtual_addr = self.base_physical_address | KSEG0_START
            memory_data = device.tiny.ReadMemoryBlock(virtual_addr, data_count)
            
            config(SETTING_NAME, 1, device=device)
            self.setup(True, None, device)
            device.tiny.WriteMemoryBlock(virtual_addr, data_count, 4, memory_data)
        finally:
            config(SETTING_NAME, old_config, device=device)
            self.setup(old_enabled, None, device)
                    
    def dump(self, byte_count, device):
        old_config = config(SETTING_NAME)
        old_enabled = self.enabled
        
        #The read from spram may time out
        try:
            config(SETTING_NAME, 1, device=device)
            self.setup(True, None, device)
            
            data_count = num_bytes_to_num_words(byte_count)
            virtual_addr = self.base_physical_address | KSEG0_START
            spram_data = device.tiny.ReadMemoryBlock(virtual_addr, data_count)
            
            config(SETTING_NAME, 0, device=device)
            self.setup(False, None, device)
            device.tiny.WriteMemoryBlock(virtual_addr, data_count, 4, spram_data)
        finally:
            config(SETTING_NAME, old_config, device=device)
            self.setup(old_enabled, None, device)
    
class DataSpram(Spram):
    offset = 10
    enable = 23
    type   = 'data'
    name   = 'DSPRAM'
    taglo_reg = 'DTagLo'
    
def get_and_validate_spram(spram_type, device):
    spram = spram_type(device)

    if not spram:
        raise SpramException('%s not found' % spram.name)
        
    spram.enable_access(device)
    spram.read_config(device)
    
    if spram.size == 0:
        raise SpramException('%s has a size of 0 bytes' % spram.name)
        
    return spram
    
@command(enable=[namedstring(disable), namedstring(enable)])
def ispram(enable=None, base_addr_phys=None, device=None):
    '''
    Display or modify ISPRAM configuration.
    
    =============== =========================================================================
    Parameter       Meaning
    =============== =========================================================================
    enable          Enable or disable ISPRAM.
    base_addr_phys  The base physical address for the ISPRAM. If this is None the existing
                    address will be used.
    =============== =========================================================================
    
    '''
    return setup_spram(InstSpram, enable, base_addr_phys, device)
        
@command(enable=[namedstring(disable), namedstring(enable)])
def dspram(enable=None, base_addr_phys=None, device=None):
    '''
    Display or modify DSPRAM configuration.
    
    =============== =========================================================================
    Parameter       Meaning
    =============== =========================================================================
    enable          Enable or disable DSPRAM.
    base_addr_phys  The base physical address for the DSPRAM. If this is None the existing
                    address will be used.
    =============== =========================================================================
    
    '''
    return setup_spram(DataSpram, enable, base_addr_phys, device)
    
def setup_spram(spram_type, enable, base_addr_phys, device):
    if enable is not None and not isinstance(enable, (bool, int, long)):
        raise SpramException('Expected True/False or 0/1 for enable')
            
    with restore_regs(device, spram_regs):
        spram = get_and_validate_spram(spram_type, device)
        
        if enable is not None or base_addr_phys is not None:
            #Apply settings, otherwise we just print
            spram.setup(enable, base_addr_phys, device)
        
        return spram
        
def check_spram_byte_count(spram, byte_count):
    if byte_count > spram.size:
        raise SpramException('Byte count is larger than SPRAM size (%d bytes)' % spram.size)
      
@command()
def ispramfill(byte_count=None, device=None):
    '''
    Fill ISPRAM from memory at same physical location.
    
    ============ =========================================================================
    Parameter    Meaning
    ============ =========================================================================
    byte_count   The number of bytes of ISPRAM to fill (starting from it's base address).
                 If this is None then the whole ISPRAM will be filled.
    ============ =========================================================================
    '''
    with restore_regs(device, spram_regs):
        spram = get_and_validate_spram(InstSpram, device)
            
        #Default to filling the whole SPRAM
        if byte_count is None:
            byte_count = spram.size
        else:
            check_spram_byte_count(spram, byte_count)
        
        if config(SETTING_NAME, device=device) == 1:
            print "Warning, config item '%s' != 0" % SETTING_NAME
            
        spram.fill(byte_count, device)

@command()
def ispramdump(byte_count=None, show_result=False, device=None):
    '''
    Dump ISPRAM to memory at same physical location.
    
    ============ ===============================================================
    Parameter    Meaning
    ============ ===============================================================
    byte_count   The number of bytes of ISPRAM to dump (to its base address).
                 If this is None then the whole ISPRAM will be dumped.
    show_result  If True and byte_count is also given, the memory dumped to will
                 be shown.
    ============ ===============================================================
    '''
    with restore_regs(device, spram_regs):
        spram = get_and_validate_spram(InstSpram, device)
        
        #Default to dumping whole SPRAM
        if byte_count is None:
            byte_count = spram.size
        else:
            check_spram_byte_count(spram, byte_count)

        spram.dump(byte_count, device)
        
        if show_result and byte_count is not None:
            return dump(KSEG0_START | spram.base_physical_address, count=byte_count/4, 
                        device=device)
