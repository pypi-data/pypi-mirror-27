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

from imgtec.test import *
from imgtec.console.support import *
from imgtec.console.results import *
from imgtec.lib.ordered_dict import OrderedDict
from collections import namedtuple
from imgtec.lib.rst import simple_table
from imgtec.console.regs import is_64_bit, regs
from imgtec.lib.namedenum import namedenum

class TLBException(Exception):
    pass
    
TLBEntry2 = namedtuple('TLBEntry', ['Index', 'EntryLo0', 'EntryLo1','EntryHi', 'PageMask', 'GuestCtl1'])
class TLBEntry(TLBEntry2):
    def __init__(self, index, entrylo0, entrylo1, entryhi, pagemask, guestctl1):
        TLBEntry2.__init__(self, index, entrylo0, entrylo1, entryhi, pagemask, guestctl1)
        
    def set_fields(self, tlb_model):
        self._entryhi_f   = parse_entry_hi(self.EntryHi, tlb_model.architecture_revision, tlb_model.config3sp, tlb_model.pagegrainesp, tlb_model.is64)
        self._entrylo0_f  = parse_entry_lo(self.EntryLo0, tlb_model.architecture_revision, tlb_model.config3sm, tlb_model.is64)
        self._entrylo1_f  = parse_entry_lo(self.EntryLo1, tlb_model.architecture_revision, tlb_model.config3sm, tlb_model.is64)
        self._pagemask_f  = parse_page_mask(self.PageMask, tlb_model.architecture_revision, tlb_model.config3sm, tlb_model.is64)
        self._guestctl1_f = parse_guestctl1(self.GuestCtl1)
        
TLBType = namedenum('TLBType',
            none_=0,
            standard_tlb=1,
            bat=2,
            fixed_mapping=3,
            dual_vtlb_and_ftlb=4,
        )

#Cache coherency value meanings
cache_attributes = [None,
                    None,
                    'Uncached',
                    'Cacheable',
                    None,
                    None,
                    None,
                    None,
                    ]
#ISA types
isa_types = ['MIPS32',
             'microMIPS32',
             'MIPS32 and microMIPS32',
             'MIPS32 and microMIPS32',
            ]

def get_tlb(device):
    #Read registers related to the tlb, then create a tlb object from them (if one exists)
    pagegrain = None
    guestctl0 = None
    is64 = is_64_bit(device)
    
    #Note that we cannot read these from the table as they can change at runtime
    config0, config1, config2, config3, config4 = regs('config config1 config2 config3 config4', device=device)
    
    config0 = parse_config_zero(config0, is64=is64)

    #Check that an MMU is present
    mmu_type = config0['MMU type']
    if mmu_type == 'None':
        raise TLBException('No MMU found.')
        
    #Check that this type of MMU is supported
    if mmu_type not in [TLBType.standard_tlb, TLBType.dual_vtlb_and_ftlb]:
        raise TLBException("MMU type %r not supported." % mmu_type)        

    config1 = parse_config_one(config1, mmu_type)
    config2 = parse_config_two(config2)
    config3 = parse_config_three(config3, is64)
    config4 = parse_config_four(config4, is64, config0['AR'])
        
    if config2['M']:
        if config3['SP'] and config3['VZ']:
            pagegrain, guestctl0 = regs('pagegrain guestctl0', device=device)
            pagegrain = parse_page_grain(pagegrain)
        elif config3['SP']:
            #Small page support is enabled, fetch PageGrain
            pagegrain = regs("pagegrain", device=device)
            pagegrain = parse_page_grain(pagegrain)
        elif config3['VZ']:
            #To find out if GuestCtl1 exists
            guestctl0 = regs("guestctl0", device=device)
    
    return TLBModel(config0, config1, config2, config3, config4, pagegrain, guestctl0, is64)
    
def extend_size(extension, value):
    #Append the extension to the left of value
    #Assuming the value size is 6 bits
    extension = (extension << 6) & 0xFFC0
    return value | extension
    
class TLBModel(object):
    def __init__(self, config0, config1, config2, config3, config4, pagegrain, guestctl0, is64):
        self.config0   = config0
        self.config1   = config1
        self.config2   = config2
        self.config3   = config3
        self.config4   = config4
        self.pagegrain = pagegrain
        self.guestctl0 = guestctl0
        self.is64      = is64
        
        self.config3sm     = False
        self.config3sp     = False
        self.config3vz     = False
        self.config3bpg    = False
        
        self.type = ''
        self.architecture = ''
        self.architecture_revision = None
        self.vtlb_size = 0
        self.ftlb_size = 0
        
        self.has_guestctl1 = False
        self.pagegrainesp = False
        
        self.get_properties()
        
    def get_properties(self):
        self.type = self.config0['MMU type']
        
        #Default when config3 is not present
        self.architecture = 'MIPS32'
        
        self.vtlb_size = 0
        if self.config0['M']:
            self.vtlb_size = self.config1['MMU size']
                        
        if self.config2['M']:
            self.architecture = self.config3['ISA']
            
            if self.architecture == 'microMIPS32':
                self.architecture_revision = self.config3['MMAR']
            else:
                #Assuming dual architectures use the AR field
                self.architecture_revision = self.config0['AR']
                
            self.config3sm  = self.config3['SM']
            self.config3sp  = self.config3['SP']
            self.config3bpg = self.config3['BPG']
            self.config3vz  = self.config3['VZ']
            
            if self.guestctl0 is not None:
                if ((self.guestctl0 >> 22) & 0x1) and self.config3vz:
                    self.has_guestctl1 = True    
        else:
            #No confg3 means no microMIPS so use AR
            self.architecture_revision = self.config0['AR']
            
        #See if the size needs extending
        self.ftlb_size = 0
        if self.config3['M']:
            mmu_ext_def = self.config4['MMU Ext Def']
            
            #Extensions assume that they are applied before adding 1 to the MMU Size
            if mmu_ext_def == 1:
                #Extend size by putting the extension on the left of the current size
                self.vtlb_size = extend_size(self.config4['MMUSizeExt'], self.vtlb_size)
            
            #Difference between 2 and 3 handled by parser
            if self.type == TLBType.dual_vtlb_and_ftlb and (mmu_ext_def == 2 or mmu_ext_def == 3):
                #2^FTLBSets = actual number of sets
                #FTLBWays + 2 = number of ways
                self.ftlb_size = (1 << self.config4['FTLBSets']) * (self.config4['FTLBWays'] + 2)
                
                if mmu_ext_def == 3 and not self.is64:
                    #Extend vtlb size with VTLBSizeExt
                    self.vtlb_size = extend_size(self.config4['VTLBSizeExt'], self.vtlb_size)
                    
        #The field value is number of entries-1, so correct that
        self.vtlb_size += 1
            
        if self.pagegrain is not None:
            self.pagegrainesp = self.pagegrain['ESP']
            
    def get_size(self):
        if self.type == TLBType.dual_vtlb_and_ftlb:
            return self.vtlb_size + self.ftlb_size
        elif self.type == TLBType.standard_tlb:
            return self.vtlb_size
        
    def is_smartmips_ase_enabled(self):
        return self.config3sm
    
    def is_small_page_enabled(self):
        return self.config3sp and self.pagegrainesp
        
    def get_info_data(self):
        info_dict = OrderedDict({})
        info_dict['type'] = self.type
        
        if self.type == TLBType.dual_vtlb_and_ftlb:
            info_dict['vtlb size'] = self.vtlb_size
            info_dict['ftlb size'] = self.ftlb_size
        elif self.type == TLBType.standard_tlb:
            info_dict['size'] = self.get_size()

        #info_dict['small page support'] = 'Enabled' if self.is_small_page_enabled() else 'Disabled'
        #info_dict['smartMIPS ASE'] = 'Enabled' if self.is_smartmips_ase_enabled() else 'Disabled'
        info_dict['architecture'] = self.architecture
        info_dict['Revision'] = self.architecture_revision
        
        return info_dict
        
def parse_entry_hi(value, release, config3sp, pagegrainesp, is64=False):
    entry = OrderedDict({})
    
    if is64:
        region_lookup = {
            0x0 : 'xuseg',
            0x1 : 'xsseg',
            0x2 : 'xkphys',
            0x3 : 'xkseg',
        }
        entry['region'] = region_lookup[(value >> 62) & 0x3]
        
        #Mask up to bit 61 as they'll be 0 anyway/used in later releases
        entry['virtual addr'] = value & (0x7FFFFFFFFFFF << 15)
        entry['virtual page no.'] = entry['virtual addr'] >> 15
    else:
        #Release 1 does not use VPN2X at all
        #Both config3sp and pagegrainesp must be set to use it on 2 or 3
        shift = 13 if (not config3sp) or (not pagegrainesp) or (release == 1) else 11
        entry['virtual addr'] = (value & 0xFFFFF800)
        #Should this be // 2?
        entry['virtual page no.'] = entry['virtual addr'] >> shift
            
    entry['invalidate'] = bool((value >> 10) & 1)
        
    #Include ASIDX as they'll be 0 if not enabled
    entry['addr space id'] = value & 0x3FF

    return entry
        
def parse_entry_lo(value, release, config3sm, is64=False):
    entry = OrderedDict({})

    #Release 3 adds these, 64 bit always has them
    if release > 2 and config3sm or is64:
        #Dependant on Config3sm bit
        entry['read inhibit']    = bool((value >> (63 if is64 else 31)) & 1)
        entry['execute inhibit'] = bool((value >> (62 if is64 else 30)) & 1)
    
    #The fill before this is determined by the PABITs value but as
    #the fill reads as 0 we can just mask off the top two bits and leave
    #the rest.
    entry['page frame no.'] = (value >> 6) & (0xFFFFFFFFF if is64 else 0xFFFFFF)
    
    #Page frame number contains everything down to bit 12 of the physical address
    entry['physical addr'] = entry['page frame no.'] << 12
    
    #Get raw value for cache coherency
    entry['coherency'] = (value >> 3) & 0b111
    
    #See if there is not a known meaning, fall back on the number
    if cache_attributes[entry['coherency']]:
        #If there is show the string
        entry['coherency'] = cache_attributes[entry['coherency']]
    
    entry['dirty']  = bool((value >> 2) & 1)
    entry['valid']  = bool((value >> 1) & 1)
    entry['global'] = bool(value & 0b1)
    
    return entry
    
def parse_guestctl1(value):
    entry = {}
    
    entry['guest eid'] = (value >> 24) & 0xFF
    entry['guest rid'] = (value >> 16) & 0xFF
    entry['guest id']  = value & 0xFF
    
    return entry
    
def parse_config_zero(value, is64):
    #Bits 9:7 indicate the MMU type
    entry = {}
    entry['M'] = (value >> 31) & 0x1
    
    #Mask out bits
    mmu_val = (value >> 7) & 0b111
        
    #If there is a set name for the value, use that otherwise fall back to the number
    try:
        entry['MMU type'] = TLBType(mmu_val)
    except ValueError:
        entry['MMU type'] = mmu_val
        
    #Bit 31 indicates whether Config1 exists
    entry['M'] = bool(value & 0x80000000)
    
    #Bits 12:10 represent the MIPS32 Architecture revision level
    entry['AR'] = ((value >> 10) & 0b111)
    
    if is64:
        #2 means r6 on 64bit
        entry['AR'] = 6 if entry['AR'] == 2 else None
    else:
        if entry['AR'] < 2:
            #0 = 1, 1 = 2
            entry['AR'] += 1
        else:
            #2-7 reserved
            entry['AR'] = None
    
    return entry
    
def parse_config_one(value, config_zero_mt):
    #Bits 30 through 25 hold (MMU size - 1)
    entry = {}
    
    #If the mmu type is 0, there are 0 tlb entries
    if config_zero_mt == 'None':
        entry['MMU size'] = 0
    else:
        #Otherwise mask it out as normal (don't add one yet)
        entry['MMU size'] = ((value >> 25) & 0x3F)
        
    #Bit 31 indicates whether Config2 exists
    entry['M'] = bool(value & 0x80000000)
    
    return entry
    
def parse_config_two(value):
    entry = {}
    
    #Bit 31 indicates whether Config3 exists
    entry['M'] = bool(value & 0x80000000)
    
    return entry
   
def parse_config_three(value, is64):
    entry = {}
    
    #Bit 4 is SP (small page support on/off)
    entry['SP'] = bool((value >> 4) & 0x01)
    
    #Bit 1 is SM (SmartMIPS AE on/off)
    entry['SM'] = bool((value >> 1) & 0x01)
    
    #Bit 31 indicates whether Config4 exists
    entry['M'] = bool(value & 0x80000000)
    
    #Bits 15:14 is instruction set availability (ISA)
    entry['ISA'] = 'MIPS64' if is64 else isa_types[(value >> 14) & 0x3]
    
    #Bits 20:18 is micro mips architecture revision
    entry['MMAR'] = (value >> 18) & 0x7
    
    if entry['MMAR'] == 0 and not is64:
        #0 means release 3 unless we're on 64 bit
        entry['MMAR'] = 3
    else:
        #Anything else is reserved
        entry['MMAR'] = None
        
    #BPG means that the pagemask can be > 32 bits
    entry['BPG'] = (value >> 30) & 0x1
    
    #Virtualization
    entry['VZ'] = (value >> 23) & 0x1
    
    return entry
    
def parse_config_four(value, is64, ar):
    entry = {}
    
    #Bits 15:14 is MMU Ext def, defines formatting of following bits
    #On 64 bit R6 this is 0 but the fields always refer to the FTLB (but could still be 0 for no FTLB)
    entry['MMU Ext Def'] = 0x3 if (is64 and ar == 6) else (value >> 14) & 0x3
    
    #The rest is based on MMU Ext def
    #0 = reserved, rest not used
    #1 = 7:0 used as MMU size extension
    #2 = 3:0 ftlb sets, 7:4 ftlb ways, 10:8 ftlb page size
    #3 = ftlb and vtlb, same as 2 but 27:24 are vtlb size extension
    if entry['MMU Ext Def'] == 0:
        pass
    elif entry['MMU Ext Def'] == 1:
        entry['MMUSizeExt'] = value & 0xFF
        
    elif entry['MMU Ext Def'] == 2:
        entry['FTLBSets']     = value & 0xF
        entry['FTLBWays']     = (value >> 4) & 0xF
        entry['FTLBPageSize'] = (value >> 8) & 0x7
        
    elif entry['MMU Ext Def'] == 3:
        entry['FTLBSets']     = value & 0xF
        entry['FTLBWays']     = (value >> 4) & 0xF
        entry['FTLBPageSize'] = (value >> 8) & 0x1F
        
        if not is64:
            entry['VTLBSizeExt']  = (value >> 24) & 0xF
        
    return entry
    
def parse_page_grain(value):
    entry = {}
    
    #Bit 28 is ESP (small page support)
    entry['ESP'] = bool(value & 0x010000000)
    
    return entry
    
def parse_page_mask(value, release, config3sp, pagegrainesp):
    #Bits 28/30 (64 bit):13 Mask
    entry = {}
    
    #Will always be 0 if we don't have small pages
    MaskX = value & (0x3 << 11)
    
    #Since the upper bits must be 0 if not used we just take 13 upwards
    Mask = value & ~0x1FFF
    
    #Lookup doesn't include possible MaskX (which is used for small pages)
    entry['page size'] = {
            0x000000000: '4 K',
            0x000006000: '16 K',
            0x00001E000: '64 K',
            0x00007E000: '256 K',
            0x0001FE000: '1 M', 
            0x0007FE000: '4 M',
            0x001FFE000: '16 M',
            0x007FFE000: '64 M',
            0x01FFFE000: '256 M',
            0x07FFFE000: '1 G',
            0x1FFFFE000: '4 G'
        }.get(Mask, 'Unknown')
    
    #Use both as X will be 0 if not used
    entry['page mask'] = Mask | MaskX
    
    if (release != 1) and config3sp and pagegrainesp:
        if MaskX == 0 and Mask == 0:
            entry['page size'] = '1 K'
    
    return entry
    
class TLBResult(list):
    def __init__(self, lines, size, radix, show_guestctl1, pagemask64):
        super(TLBResult, self).__init__(lines)
        self.size = size
        self.radix = 16
        self.show_guestctl1 = show_guestctl1
        self.pagemask64 = pagemask64

    def __repr__(self):
        return tlb_dump(self, self.size, self.radix, self.show_guestctl1, self.pagemask64)
  
def tlb_dump(entries, size, radix, show_guestctl1, pagemask64):
    regsize_formatter = get_formatter(radix, size)
    default_formatter = get_formatter(radix, 4)
    
    titles = ['Index', 'EntryLo0', 'EntryLo1', 'EntryHi', 'Page Mask']
    if show_guestctl1:
        titles.append('GuestCtl1')
        
    new_rows = []
    
    for entry in entries:
        new_row = []
        new_row.append('%d' % entry.Index)
        
        #These are register size
        for n in [entry.EntryLo0, entry.EntryLo1, entry.EntryHi]:
            new_row.append(regsize_formatter(n))
            
        #Depends on BPG
        if pagemask64:
            new_row.append(regsize_formatter(entry.PageMask))
        else:
            new_row.append(default_formatter(entry.PageMask))
            
        if show_guestctl1:
            #Always 32 bit
            new_row.append(default_formatter(entry.GuestCtl1))
        
        new_rows.append(new_row)

    return simple_table(titles, new_rows)
    
def read_tlb_entry(index, guest, device):
    entry = device.da.ReadTLB(index, guest)
    return TLBEntry(index, *entry)

@command(vpe_required=True)    
def tlbd(start_index=0, end_index=None, guest=False, device=None):
    '''
    Show the TLB entries at the indexes within the range start_index to end_index.

    [s0c0v0] >>> tlbd(3, 5)
    ===== ======== ======== ======== =========
    Index EntryLo0 EntryLo1 EntryHi  Page Mask
    ===== ======== ======== ======== =========
    3     00b1d506 42b31a9e 00000000 00000000
    4     c21b5264 c357a598 00000000 00000000
    5     00b3a420 01a2b7d2 00000000 00000000
    ===== ======== ======== ======== =========
    
    * The range can be from 0 to the number of TLB entries - 1.
    
    * start_index defaults to 0 and end_addr defaults to the last index,
      so calling tlbd without arguments will dump the whole TLB.
    '''

    tlb_model = get_tlb(device)
    
    tlb_size = tlb_model.get_size()
    if (start_index+1) > tlb_size:
        raise TLBException("Start index exceeds TLB size (%d)" % tlb_size)
        
    if end_index is None:
        end_index = tlb_model.get_size()-1
    elif (end_index+1) > tlb_model.get_size():
        print "End index exceeds TLB size (%i), reading until end of TLB" % tlb_size
        end_index = tlb_model.get_size()-1
        
    if start_index > end_index:
        raise TLBException("Start index exceeds end index")
    
    lines = []
    for i in range(start_index, end_index+1):
        lines.append(read_tlb_entry(i, guest, device))
    
    return TLBResult(lines, 8 if is_64_bit(device) else 4, 16, tlb_model.has_guestctl1, tlb_model.config3bpg)

@command(vpe_required=True)    
def tlb(index, values=None, guest=False, device=None):
    '''
    Show a single TLB entry or write to a single TLB entry.

    [s0c0v0] >>> tlb(1, values=[0, 2, 3, 0])
    [s0c0v0] >>> tlb(1)
    ===== ======== ======== ======== =========
    Index EntryLo0 EntryLo1 EntryHi  Page Mask
    ===== ======== ======== ======== =========
    1     00000000 00000002 00000003 00000000
    ===== ======== ======== ======== =========
    
    * index can be in the range 0 to the number of TLB entries - 1.
    
    * values is a list in the order EntryLo0, EntryLo1, EntryHi, PageMask and 
	  optionally GuestCtl1.
    
    * If values are given the entry at the index will be written with those
      values, otherwise that index will be read.
    '''

    tlb_model = get_tlb(device)
    
    tlb_size = tlb_model.get_size()
    if (index+1) > tlb_size:
        raise TLBException("Index exceeds TLB size (%d)" % tlb_size)
    elif index < 0:
        raise TLBException("Invalid index")
        
    if values is not None:
        values = list(values)
        #Previous versions didn't have GuestCtl1
        if len(values) == 4:
            values.append(tlb(index, guest=guest, device=device)[0].GuestCtl1)
        
        args = values + [guest]
        device.da.WriteTLB(index, *args)
        return
    else:
        line = [read_tlb_entry(index, guest, device)]
        ret = TLBResult(line, 8 if is_64_bit(device) else 4, 16, tlb_model.has_guestctl1, tlb_model.config3bpg)
        return ret
