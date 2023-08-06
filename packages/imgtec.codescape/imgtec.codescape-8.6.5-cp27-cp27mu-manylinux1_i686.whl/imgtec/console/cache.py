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
from math import log
from contextlib import contextmanager
from imgtec.lib.rst import simple_table
from imgtec.console.dbudriver import GCRL2Config
from imgtec.console.tdd import targetdata

KSEG0_START         = 0x80000000
KSEG0_START_64      = 0xFFFFFFFF80000000
INDEX_INVALIDATE    = 0
INDEX_LOAD_TAG      = 1
INDEX_STORE_TAG     = 2
INDEX_STORE_DATA    = 3
HIT_INVALIDATE      = 4
HIT_WB_INVALIDATE_D = 5
FILL_I              = 5
HIT_WB              = 6
FETCH_AND_LOCK      = 7

ICACHE =    0
DCACHE =    1
#L2/L3 are reversed (Gray code order)
L2CACHE =   3
L3CACHE =   2

class CacheException(Exception):
    pass
    
class CacheRegs(object):
    def __init__(self, d_lo, d_hi, t_lo, t_hi):
        self.d_lo = d_lo
        self.d_hi = d_hi
        self.t_lo = t_lo
        self.t_hi = t_hi
        
    def __iter__(self):
        ls = [self.d_lo, self.d_hi, self.t_lo, self.t_hi]
        for reg in ls:
            yield reg

    def discover(self, tag_width, data_width):
        #Always going to have at least one per
        self.has_d_lo = True
        self.has_d_hi = data_width == 2
        self.has_t_lo = True
        self.has_t_hi = tag_width == 2
    
_Icache_regs  = CacheRegs("cp0.28.1", "cp0.29.1", "cp0.28.0", "cp0.29.0")
_Dcache_regs  = CacheRegs("cp0.28.3", "cp0.29.3", "cp0.28.2", "cp0.29.2")
_L2cache_regs = CacheRegs("cp0.28.5", "cp0.29.5", "cp0.28.4", "cp0.29.4")
_L3cache_regs = CacheRegs("cp0.28.5", "cp0.29.5", "cp0.28.4", "cp0.29.4")

class Cache(object):
    name = "Unknown"
    cmd_name = 'unknown' #name that would be passed to cachedump/cacheop

    def __init__(self, regs):
        self.regs            = regs
        self.associativity   = 0
        self.line_size       = 0
        self.sets_per_way    = 0
        self.tag_size        = 0
        self.data_size       = 0
        self.register_size   = 4
        self.way_size        = 0
        self.is64            = False
        self.has_shared_regs = False
        
    @property
    def is64(self):
        return self._is64
        
    @is64.setter
    def is64(self, value):
        self._is64 = value
        self.register_size = 8 if value else 4
    
    def as_string_list(self):
        size = self.line_size*self.sets_per_way*self.associativity
        unit = ' bytes'
        if not size % 1024:
            size /= 1024
            unit = 'k bytes'
        return [self.name, str(self.associativity), str(self.line_size)+' bytes', 
                str(self.sets_per_way), str(size) + unit]

    def get_info(self, device):
        '''
        Although the there is one instance of each cache object type per session, 
        this method is called during each command to get the latest settings.
        '''
        cpu_info = dict(device.da.CpuInfo(True))
        self.is64  = not cpu_info.get('cpu_is_32bit', True)
        
        if (targetdata(device).socs[0].tap_type == 0x8) and (self.name == "L2 DCache"):
            l2_config = GCRL2Config(device.tiny.ReadRegister('gcr_l2_config'))
            is_present = l2_config.set_size and l2_config.line_size
            line_size = 2*(2**l2_config.line_size)
            associativity = l2_config.assoc + 1
            sets_per_way = 64*(2**l2_config.set_size)
            tag_size = 1
            data_size = 1
        else:
            '''
            Default False because no has_bla_field means no cache and if you had that field
            you'd always have valid values for the rest.
            '''
            info_fields = [cpu_info.get(field, False) for field in self.info_fields]
            is_present, line_size, associativity, sets_per_way, tag_size, data_size = info_fields
            
        #No cache at all
        if not is_present:
            self.line_size = 0
            self.lines     = 0
        else:
            self.has_shared_regs = cpu_info.get('has_shared_cache_regs', False)
            self.associativity   = associativity
            self.line_size       = line_size
            self.sets_per_way    = sets_per_way
            self.way_size        = self.line_size * self.sets_per_way
            self.size            = self.associativity * self.way_size
            self.lines           = self.size // self.line_size if self.line_size else 0
            self.lines_per_way   = self.lines // self.associativity
            self.tag_size        = tag_size
            self.data_size       = data_size
            
            #When there are shared cache registers the Dcache uses the Icache indexes
            #L2/3 if/when supported seem to always share, but at different indexes to I/D
            if self.has_shared_regs and self.type == DCACHE:
                self.regs = _Icache_regs
            else:
                self.regs = self.default_regs
                
            self.regs.discover(self.tag_size, self.data_size)
            
    def __nonzero__(self):
        #Cache not present if line size is 0
        return self.line_size != 0

    def __repr__(self):
        return "\n".join([
                self.name,
                "associativity: " + str(self.associativity),
                "    line size: " + str(self.line_size) + " bytes",
                "     tag size: " + str(self.tag_size*self.register_size) + " bytes",
                " sets per way: " + str(self.sets_per_way)])
                
def info_fields(name):
    return ["has_%s" % name,
            "%s_line_size" % name,
            "%s_associativity" % name, 
            "%s_sets_per_way" % name, 
            "%s_tag_size" % name, 
            "%s_data_size" % name,
           ]
                        
class ICache(Cache):
    name       = "ICache"
    cmd_name   = 'instr'
    type       = ICACHE
    info_fields = info_fields("l1_icache")
    default_regs = _Icache_regs

class DCache(Cache):
    name       = "DCache"
    cmd_name   = 'data'
    type       = DCACHE
    info_fields = info_fields("l1_dcache")
    default_regs = _Dcache_regs

class L23Cache(Cache):
    name       = "L2/3 DCache"
    
class L2Cache(L23Cache):
    name       = "L2 DCache"
    cmd_name   = 'secondary'
    type       = L2CACHE
    info_fields = info_fields("l2_cache")
    default_regs = _L2cache_regs

class L3Cache(L23Cache):
    name       = "L3 DCache"
    cmd_name   = 'tertiary'
    type       = L3CACHE
    info_fields = info_fields("l3_cache")
    default_regs = _L3cache_regs
    
_ICache  = ICache(_Icache_regs)
_DCache  = DCache(_Dcache_regs)
_L2Cache = L2Cache(_L2cache_regs)
_L3Cache = L3Cache(_L3cache_regs)
    
cache_types = dict(
    all           = {'cache':[_ICache,_DCache,_L2Cache], 'writeback':  True},
    allnowb       = {'cache':[_ICache,_DCache,_L2Cache], 'writeback': False},
    icache        = {'cache':[_ICache],                  'writeback': False},
    dcache        = {'cache':[_DCache],                  'writeback':  True},
    dcachenowb    = {'cache':[_DCache],                  'writeback': False},
    l2cache       = {'cache':[_L2Cache],                 'writeback':  True},
    l2cachenowb   = {'cache':[_L2Cache],                 'writeback': False},
    l3cache       = {'cache':[_L3Cache],                 'writeback':  True},
    l3cachenowb   = {'cache':[_L3Cache],                 'writeback': False},
)
    
allnowb     = named('allnowb')
icache      = named('icache')
dcache      = named('dcache')
dcachenowb  = named('dcachenowb')
l2cache     = named('l2cache')
l2cachenowb = named('l2cachenowb')
l3cache     = named('l3cache')
l3cachenowb = named('l3cachenowb') 

#Legacy names
mappings = [('instr', 'icache'), ('data', 'dcache'), ('datanowb', 'dcachenowb'), 
    ('secondary', 'l2cache'), ('secondarynowb', 'l2cachenowb'), ('tertiary', 'l3cache'),
    ('tertiarynowb', 'l3cache')]
for old, new in mappings:
    cache_types[old] = cache_types[new]
    
instr         = named('instr')
data          = named('data')
datanowb      = named('datanowb')
secondary     = named('secondary')
secondarynowb = named('secondarynowb')
tertiary      = named('tertiary')
tertiarynowb  = named('tertiarynowb')

class CacheResult(list):
    def __init__(self, values, cache, size=None, endian=False, show_chars=True):
        super(CacheResult, self).__init__(values)
        self.size = size
        self.endian = endian
        self.cache = cache
        self.show_chars = show_chars

    def __repr__(self):
        return cache_dump(self, self.cache, self.size, self.endian, self.show_chars)
        
def get_column_formatter(parameter, radix):
    #Pad with 0s to the max width
    col_width = len(('%' + radix) % (parameter-1))
    #Where radix is 'i', 'x' etc.
    format = '%0' + str(col_width) + radix
    
    return lambda x: (format % x)
        
def cache_dump(rows, cache, size, endian, show_chars):
    #Data is always 32 bit
    data_size = 4
    for row in rows:
        row['bytedata'] = struct_pack(row['data'][cache.tag_size:], data_size, endian)
    
    formatter = get_formatter(16, data_size)

    if show_chars:
        table = ''.join(chr(x) if 32<= x < 127 else '.' for x in range(256))
        for row in rows:
            row['bytedata'] = row['bytedata'].translate(table)
            
    titles = ['Offset', 'Set', 'Way']
    
    tag_titles = ['TagLo']
    if cache.tag_size == 2:
        if endian == Endian.big:
            tag_titles.insert(0, 'TagHi')
        else:
            tag_titles.insert(1, 'TagHi')
    titles.extend(tag_titles)
    
    titles.extend(['Word %i' % i for i in range(cache.line_size/data_size)])
    
    if show_chars:
        titles.append('Chars')
    
    #Tags are 32 on 32 bit target 64 on 64
    hex_formatter = get_formatter(16, size)
    offset_format = get_column_formatter(cache.way_size, 'x')
    set_format    = get_column_formatter(cache.sets_per_way, 'i')
    way_format    = get_column_formatter(cache.associativity, 'i')

    lines  = []
    for row in rows:
        line = []

        line.append(offset_format(row['offset']))
        line.append(set_format(row['set']))
        line.append(way_format(row['way']))

        #Tag
        line.extend([hex_formatter(x) for x in row['data'][0:cache.tag_size]])
		#Contents (always 32 bit formatter)
        if row['valid']:    
            line.extend([formatter(x) for x in row['data'][cache.tag_size:]])
        else:
            num_elements = len(row['data']) - cache.tag_size
            num_chars = len(formatter(row['data'][cache.tag_size]))
            line.extend(['*'*num_chars]*num_elements)
        
        if show_chars:
            chars = row['bytedata']
            if row['valid']:
                line.append(chars)
            else:
                line.append('?'*len(chars))
            
        lines.append(line)
    
    return simple_table(titles, lines)
    
def split_into_lines(data, line_size, element_size):
    #Take in a list which has elements sequentially and split it
    #into many lists each of line_size (line/element size in bytes)
    return [data[i:i+(line_size/element_size)] for i in range (0, len(data), line_size/element_size)]
    
def read_cache(device, cache, start_addr, end_addr, skip_invalid):
    endian = device.tiny.GetEndian()
    #Read all ways
    ways_mask = (2**cache.associativity)-1
    # +1 because 0x10 to 0x10 is still one set
    count = ((end_addr - start_addr) / cache.line_size) + 1
    
    res = device.tiny.ReadCache(cache.type, start_addr, count, ways_mask, False, skip_invalid)
    res = split_into_lines(res, cache.line_size + (cache.tag_size*cache.register_size), cache.register_size)
    new_res = []
    
    for line in res:
        if cache.is64:
            #Tags stay 64 bit
            new_res.append(line[:cache.tag_size])
            
            #Contents are shown as 32 bit even on a 64 bit target
            for word in line[cache.tag_size:]:
                if endian == Endian.little:
                    new_res[-1].extend([word & 0xFFFFFFFF, word >> 32])
                else:
                    new_res[-1].extend([word >> 32, word & 0xFFFFFFFF])
        else:
            new_res.append(line)
    res = new_res
    
    result = []
    offset = start_addr
    way = 0
    for line in res:
        if not skip_invalid:
            valid = True
        else:
            if endian == Endian.little or cache.tag_size == 1:
                taglo = line[0]
            else:
                taglo = line[1]
                
            prid = dict(device.tiny.CpuInfo())['prid']
            if (prid & (0xFF << 16)) and ((prid & 0xFF00) >> 8) == 0xA9: # I6400
                valid = taglo & (1<<9)
            else:
                valid = taglo & (1<<7)
                
        if valid:
            result.append({'offset': offset,
                           'set'   : offset // cache.line_size,
                           'way'   : way,
                           'data'  : line,
                           'valid' : valid,
                         })
                     
        if way != cache.associativity-1:
            way += 1
        else:
            way = 0
            offset += cache.line_size
        
    return result
              
class CacheInfoResult(list):
    def __repr__(self):
        titles = ['Name', 'Associativity', 'Line Size', 'Sets Per Way', 'Total Size']
        rows   = [cache.as_string_list() for cache in self]
        return rst.simple_table(titles, rows)
        
@command(cache=[namedstring(icache), namedstring(dcache), namedstring(l2cache)])
def cacheinfo(cache=None, device=None):
    '''
    Show the details of the given cache, or all caches on the target if one isn't given.
    '''
    if cache is not None:
        caches = [cache]
    else:
        caches = ['icache', 'dcache', 'l2cache', 'l3cache']
    
    try:
        caches = [cache_types[str(type)]['cache'][0] for type in caches]
    except KeyError:
        raise CacheException("Invalid cache type")
    
    #CpuInfo may fall back to register testing, but it does the restore itself
    for c in caches:
        c.get_info(device)
            
    #Remove non existent caches
    cache_objs = [c for c in caches if c]
    
    if cache_objs:
        return CacheInfoResult(cache_objs)
    else:
        if len(caches) == 1:
            raise CacheException("No %s found." % caches[0].name)
        else:
            raise CacheException("No caches found.")
        
cache_type_err = "Cache type required, one of icache, dcache or l2cache."
def get_cache_object(cache):
    if cache is None:
        raise CacheException(cache_type_err)
        
    try:
        cache = cache_types[str(cache)]['cache'][0]
    except KeyError:
        raise CacheException("Invalid cache type")
    
    return cache
        
#Details attached to a cache type override the top level details
cache_operations = {
    0 : { 
        ICACHE  : { 'name': 'index invalidate'},
        'name'  : 'Index writeback',
        'valid' : True,
        },
    1 : {
        L3CACHE : {'valid': False},
        'name'  : 'Index load tag',
        'valid' : True,
        },
    2 : {
        'name': 'Index store tag', 
        'valid' : True,
        },
    3 : {
        #This is usually INDEX_STORE_DATA which is invalid for anything but L2Cache
        #however SPRAMs use store data on i/dcache so we allow it for all types.
        'name'  : 'Implementation Dependent',
        'valid' : True,
        },
    4 : {
        'name' : 'Hit invalidate',
        'valid': True,
        },
    5 : {
        ICACHE : {'name': 'fill'},
        'name' : 'Hit writeBack invalidate',
        'valid': True,
        },
    6 : {
        ICACHE : {'valid': False},
        'name' : 'Hit writeback',
        'valid': True,
        },
    7 : {
        'name' : 'Fetch and lock',
        'valid': True,
        },
}

def validate_cache_operation(cache, operation):
    #Is it valid for any cache?
    if operation not in cache_operations.keys():
        raise CacheException('Invalid cache operation (%d)' % operation)
    
    #Is it valid for this cache?
    name  = None
    valid = None
    op = cache_operations[operation]
    
    #More specific info is attached to cache type
    op_cache = op.get(cache.type)
    if op_cache is not None:
        name  = op_cache.get('name')
        valid = op_cache.get('valid')
        
    if name is None:
        name = op['name']
    if valid is None:
        valid = op['valid']
        
    if not valid:
        raise CacheException('%s is not a valid operation for %s' % (name, cache.name))
        
@command(cache=[namedstring(icache), namedstring(dcache), namedstring(l2cache)])
def cacheop(cache, address, line_size, operation, count=1, flags=0, device=None):
    '''
    Perform a cache operation.
        
    For operations that refer to an 'index' address will be an offset into 
    the cache data array. For example index 2 aka set 2 will be at 2 * the line
    size.

    'line_size' is the size of the cache line in bytes (contents only, found 
    in the Config regs or from the cacheinfo command).
    
    'operation' is the action to be taken. These are shown in this table, where 
    I,D,S,T mean instruction, data, secondary, and tertiary respectively.

    ============ =======================================================
    Operation    Meaning
    ============ =======================================================
    0 (I)        Index invalidate, set the cache line at the given 
                 index (offset address) to be invalid.
    0 (D,S,T)    Index Writeback Invalidate, if the line at the index 
                 is valid and dirty, write it back to memory. Set the 
                 line to invalid regardless.
    1 (I,D,S)    Index load tag, read the tag for the cache line at
                 the given index into the TagLo/TagHi register(s).
                 Read the data word at the given address into the 
                 DataLo/DataHi register(s).
                 Read precode and data parity bits into the ErrCtl
                 register.
    2 (I,D,S,T)  Index store tag, write the tag for the given cache 
                 line using the values in the corresponding
                 TagHi/TagLo registers.
    3 (S)        Index store data, write the data in L23DataHi/Lo
                 to the way and index specified.
    4 (I,D,S,T)  Hit invalidate, if the cache contains the specified
                 address, set it to invalid.
    5 (D,S,T)    Hit WriteBack invalidate. As above, but write the 
                 contents of the line back to memory first.
    5 (I)        Fill the cache from the given address. Data is 
                 re-fetched even if it is already cached.
    6 (D,S,T)    Hit Writeback, if the cache contains the given address
                 and it is valid and dirty write that line back to 
                 memory. Leave line valid but clear dirty state.
    7 (I,D,S,T)  Fetch and lock, if the cache does not contain the 
                 given address, fill it from memory, doing a writeback 
                 if required. Set the line to valid and locked. If the 
                 data is already in the cache, just lock it. The least 
                 recently used way is used for the fill.
                 The lock can be cleared by using an index, index
                 writeback, hit or hit writeback invalidate operation.
                 Alternatively an index store tag operation could be 
                 used.
    ============ =======================================================
    
    'cache' is one of the named parameters, icache, dcache, l2cache or l3cache.
    
    If 'count' is greater than 1 then the operation will be performed on 
    multiple lines (assuming that the operation can do so).

    'flags' may also be given indicating:
    
    ======= ========================================================
    Flags   Meaning
    ======= ========================================================
    0       Normal virtual address.
    1       EVA mode user virtual address (uses CACHEE instruction).
    ======= ========================================================
    
    Examples::

        def op_addr(way, line, way_size, line_size):
            'Calculate an address based on way/line number.'
            KSEG0_START  = 0x80000000
            way_shift    = log(way_size, 2) # log base 2 of the way size 
            start        = KSEG0_START | (way << way_shift) # start of the way
            return start + (line_size * line_number)

        way_size            = 0x1fe0
        line_size           = 32
        op_address = op_addr(1, 1, way_size, line_size)
        assertEquals(0x80001020, op_address)
        
        # Index invalidate way 1, line 1 of icache
        cacheop(icache, op_address, line_size, 0)
        # invalidate 10 lines from 0x80001020 onwards
        cacheop(icache, op_address, line_size, 0, 10)
        # data cache hit writeback the address 0x8000BEEF
        cacheop(dcache, op_address, line_size, 6)
    '''
    cache = get_cache_object(cache)
    validate_cache_operation(cache, operation)
    
    cache = cache.type
    operation = cache | (operation << 2)
    device.tiny.CacheOperation(address, line_size, operation, count, flags)
        
@command(cache=[namedstring(icache), namedstring(dcache), namedstring(l2cache)])
def cachedump(cache=None, start_addr=0x00, end_addr=None, show_chars=True, 
    skip_invalid=False, device=None):
    """Show the contents of the cache for a given address range.

    This command displays the cache lines associated with the given address range.
    Where 'cache' is one of the named parameters, icache, dcache, l2cache, l3cache.

    * The address range is converted into an offset range within the cache.

    * Each way has a number of lines within it, the offset is the address of the
      first byte of a line, within that way.

    * For example, with a 32 byte line size way 0, set 0 will be at offset 0x00,
      set 1 at 0x20, set 2 at 0x40. These offsets are the same for each way. Way
      0 set 1 has the same offset as way 1, set 1.

    * This offset determines the bottom bits of the addresses which may be cached within
      that line. The address 0x80100040 would be at offset 0x40, which would be line 2
      within each way. For a 4 way associative cache that would be 4 possible lines.
      
    Set show_chars to True to enable display of ASCII characters generated from the 
    cache line contents. 
    
    Set skip_invalid to True to only read cache lines which are valid.
    """
    cache = get_cache_object(cache)

    if end_addr is None:
        end_addr = start_addr

    cache.get_info(device)
    start_addr, end_addr = cache_dump_range_check(cache, start_addr, end_addr)
    results = read_cache(device, cache, start_addr, end_addr, skip_invalid)
            
    return CacheResult(results, cache, size=cache.register_size, 
                       endian=device.da.GetEndian(), show_chars=show_chars)
    
def cache_dump_range_check(cache, start_addr, end_addr):
    if cache.lines == 0:
        raise CacheException("Cache not present")
        
    if start_addr > end_addr:
        raise CacheException("Start address is larger than end address")
        
    #Work out byte offsets
    #addr & way_size-1 leaves the bits relating to the position within the way
    #& (0xFFFFFFFF etc.) rounds the address down to the nearest line by removing the lower bits
    start_addr = (start_addr & (cache.way_size-1)) & (0xFFFFFFFF ^ (cache.line_size-1))
    end_addr   = (end_addr & (cache.way_size-1)) & (0xFFFFFFFF ^ (cache.line_size-1))

    if end_addr >= cache.way_size:
        print "End address larger than way size, reading until end of cache"
        end_addr = cache.way_size-1
    
    return (start_addr, end_addr)    
    
@command(cache=[named_all, namedstring(allnowb), namedstring(icache), namedstring(dcache), 
                namedstring(dcachenowb), namedstring(l2cache), namedstring(l2cachenowb)])
def invalidate(cache=None, device=None):
    '''Invalidate one or more of the instruction, data and secondary caches.
    Cache can be one of the following:
    
    =========== =============================================================
    cache       Meaning
    =========== =============================================================
    all         Writeback invalidate instruction, data and secondary cache.
    allnowb     Invalidate the instruction and data cache, without writeback.
    icache      Invalidate the instruction cache.
    dcache      Writeback invalidate the data cache.
    dcachenowb  Invalidate the data cache without writeback.
    l2cache     Writeback invalidate the secondary cache.
    l2cachenowb Invalidate the secondary cache without writeback.
    =========== =============================================================
    
    '''
    if cache is None:
        raise CacheException(cache_type_err)
    
    try:
        #Because the legacy names aren't in the autocomplete list they don't get converted to strings
        cache = cache_types[str(cache)]
    except KeyError:
        raise CacheException("Invalid cache type")
       
    caches = cache['cache']
    did_invalidate = False
    for _cache in caches:
        #Discovery
        _cache.get_info(device)
        
        if _cache.lines == 0:
            #If they have asked for a specific cache throw, otherwise do all we can find
            if len(caches) == 1:
                raise CacheException("Cache not present")
            else:
                continue

        #This does need restore as we do the ops manually
        with restore_regs(device, list(_cache.regs)):        
            invalidate_cache(_cache, cache['writeback'], device)
            did_invalidate = True
            
    if not did_invalidate and len(caches) > 1:
        raise CacheException("No caches invalidated because no caches were found.")
        
def invalidate_cache(cache, writeback, device):
    way_shift = int(log(cache.way_size, 2))
    start_address = (KSEG0_START_64 if cache.is64 else KSEG0_START) | way_shift
    flags = 0
    
    if writeback:
        #Invalidate with writeback
        operation = INDEX_INVALIDATE
    else:
        #Clear tag to invalidate without a writeback
        operation = INDEX_STORE_TAG
        #Set tag regs to 0
        if cache.regs.has_t_hi:
            device.da.WriteRegister(cache.regs.t_hi, 0x00000000)
        device.da.WriteRegister(cache.regs.t_lo, 0x00000000)
    
    cacheop(cache.cmd_name, 
            start_address, 
            cache.line_size, 
            operation,
            count=cache.lines, 
            flags=flags, 
            device=device)
            
@contextmanager
def restore_regs(device, regs):
    #Try to write all of them at once
    reg_names = []
    values    = []
    
    try:
        values = device.da.ReadRegisters(regs)
        reg_names = regs
    except RuntimeError:
        #If one of them doesn't exist write individually
        for reg in regs:
            try:
                values.append(device.da.ReadRegister(reg))
                reg_names.append(reg)
            except RuntimeError:
                pass
    try:
        yield
    finally:
        try:
            device.da.WriteRegisters(reg_names, values)
        except RuntimeError:
            for reg, value in zip(reg_names, values):
                try:
                    device.da.WriteRegister(reg, value)
                except RuntimeError:
                    pass
