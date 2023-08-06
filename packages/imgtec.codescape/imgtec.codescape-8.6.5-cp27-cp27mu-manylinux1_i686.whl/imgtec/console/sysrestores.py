# (C)2016 #################################################################
# 
# Copyright (c) 2016, Imagination Technologies Limited
# and/or its affiliated group companies ("Imagination").
# All rights reserved.
# No part of this content, either material or conceptual
# may be copied or distributed, transmitted, transcribed,
# stored in a retrieval system or translated into any
# human or computer language in any form by any means,
# electronic, mechanical, manual, or otherwise, or
# disclosed to third parties without the express written
# permission of Imagination.
#
# (C)2016 #################################################################

from imgtec.test import *
from imgtec.console.support import *
from imgtec.console.cache import cacheinfo, mappings
from imgtec.console.generic_device import device
from imgtec.console.regs import regs, is_64_bit
from imgtec.console.tlb import tlb
from imgtec.console.sysdumps import absolute_filename, memory_element_size, show_progress, set_show_progress
import os, os.path, struct

_force_restore = False
def _set_force_restore(restore):
    global _force_restore
    #org_force_restore = _force_restore
    _force_restore = restore
    return _force_restore
    
def _really_restore(restore):
    '''
    >>> _ = _set_force_restore(False)
    >>> _really_restore(False)
    False
    
    >>> _really_restore(True)
    True
    
    >>> _ = _set_force_restore(True)
    >>> _really_restore(False)
    True
    
    >>> _really_restore(True)
    True
    '''    
    return restore or _force_restore

def restoreregs(regs_vals, comment='', restore=True):
    '''Restore the specified register-values pairs.'''
    if _really_restore(restore):
        show_progress('restoring ' + comment)
        if len(regs_vals) == 1:
            register, value = regs_vals[0]
            regs(register, value)
        else:
            regs(*zip(*regs_vals))
    else:
        show_progress('skipped restoring ' + comment)
        
    
def restoretlbs(tlbfile, filesize, tlb_pages, restore=True):
    '''Restore Translation Lookaside Buffers.
    
    tlbfile: The path to a file containing data created by a previous "dump"
             which saved the tlbs, if present.
               
    filesize: The size of the file when written.
    
    tlb_pages: A list of 4-tuples each one giving:
                (virtual address (hex integer), physical address (hex integer), filename, size (hex integer))
               of a saved page to be restored.
    '''

    if _really_restore(restore):
        show_progress('restoring tlbs')
        try:
            abs_tlbfile = absolute_filename(tlbfile)
            with open(abs_tlbfile, 'rb') as f:
                tlbdata = f.read()
            
            if len(tlbdata) == filesize:
                pos = 0
                entries = []
                while pos < filesize:
                    entry = []
                    for _eix in xrange(6):
                        epos = pos + 8
                        entry.append(struct.unpack('>Q', tlbdata[pos:epos])[0])
                        pos = epos
                    entries.append(entry)
                for index, entrylo0, entrylo1, entryhi, pagemask, guestctl1 in entries:
                    tlb(index, (entrylo0, entrylo1, entryhi, pagemask, guestctl1))
                
                for vaddress, paddress, page_file, page_size in tlb_pages:
                    memelts, _binsize = read_memory_binfile(page_file, page_size)
                    if (memelts is not None) and bool(memelts):
                        memtype = _extract_memtype(page_file)
                        show_progress('restoring tlb page at virtual(physical) address %s(%s)' % (vaddress, paddress), at_level=veryverbose)
                        device().da.WriteMemoryBlock(vaddress, len(memelts), memory_element_size, memelts, memtype)
            else:
                print 'restoretlbs: specified file size (0x%x) differs from the binary file size (0x%x).' % (filesize, len(tlbdata))
        except Exception as e:
            print 'restoretlbs: file "%s", open or read failed: %s' % (tlbfile, str(e))
    else:
        show_progress('skipped restoring tlbs')
        
def restore_cache_data(nset_groups, nsets_per_write, nitems_per_line, cache, unpack_format, raw_cache_data, size, all_ways_mask, tag_only, raw_offset, progress_msg):
    show_progress(progress_msg, at_level=veryverbose)
    for setgroupix in xrange(nset_groups):
        setdata = []
        for _setwix in xrange(nsets_per_write):
            for _way in xrange(cache.associativity):
                for _ix in xrange(nitems_per_line):
                    setdata.append(struct.unpack(unpack_format, raw_cache_data[raw_offset:raw_offset+size])[0])
                    raw_offset += size
        device().da.WriteCache(cache.type, setgroupix * nsets_per_write * cache.line_size, nsets_per_write, all_ways_mask, tag_only, False, setdata)
    return raw_offset

def restorecache(cache_type, cache_file, writtensize, restore=False):
    '''Restore I/D, secondary and tertiary caches as required.
    
    cache_type: The cache to be restored - one of icache, dcache, secondary or tertiary  
    
    cache_file: The path to a file containing binary data for the given cache created
                by a previous "dump" which saved this cache.
                  
    file_size: The size of the file when written which must match the size of the
               given 'cache_file'.
               
    restore:   Restore the cache if True otherwise skip restoration.
    '''

    if not _really_restore(restore):
        show_progress('skipped restoring %s' % str(cache_type))
        return

    show_progress('restoring %s' % str(cache_type))
    
    cache_mappings = dict((k, v) for k, v in mappings)
    cache = None
    for cinfo in cacheinfo():
        mapped_cache = cache_mappings[cinfo.cmd_name]
        if str(cache_type) == mapped_cache and (cache_file.find(mapped_cache) + len(mapped_cache) == cache_file.find('.bin')):
            cache = cinfo
            break

    if cache is None:
        raise RuntimeError('restorecache: requested "%s" cache not supported in hardware.' % (str(cache_type),))
    
    abs_cache_file = absolute_filename(cache_file)
    binfilesize = os.stat(abs_cache_file).st_size
    if binfilesize != writtensize:
        raise RuntimeError('restorecache: requested cache file size (0x%x) differs from binary cache file size (0x%x).' % (writtensize, binfilesize))
    
    with open(abs_cache_file, 'rb') as f:
        raw_cache_data = f.read()

    cache_config = [struct.unpack(">I", raw_cache_data[ofs:ofs+4])[0] for ofs in (0, 4, 8, 12)]
    if any([cache_config[0] != cache.associativity,
       cache_config[1] != cache.sets_per_way,
       cache_config[2] != cache.line_size,
       cache_config[3] != cache.tag_size]):
        hardware_cache_config = "[%d, %d, %d, %d]" % (cache.associativity, cache.sets_per_way, cache.line_size, cache.tag_size)
        raise RuntimeError('restorecache: the configuration in the binary cache file %s differs from the current hardware cache configuration %s.' % (str(cache_config), hardware_cache_config))
        
    config = dict(device().da.CpuInfo())
    cpu_is_32bit = config['cpu_is_32bit']
    unpack_format, size = (">I", 4) if cpu_is_32bit else (">Q", 8)
    
    all_ways_mask = (2**cache.associativity)-1
    nsets_per_write = 1
    nset_groups = cache.sets_per_way / nsets_per_write
    nitems_per_line = cache.tag_size + cache.line_size / cache.associativity
    _raw_offset = restore_cache_data(nset_groups, nsets_per_write, nitems_per_line, cache, unpack_format, raw_cache_data, size, all_ways_mask, False, 16, 'restoring %s data' % (cache.name,))
    
    #filename, ext = os.path.splitext(cache_file)
    #lru_cache_file = filename + "-lru" + ext
    #abs_lru_cache_file = 
    #abs_lru_cache_file = absolute_filename(lru_cache_file)
    #with open(abs_lru_cache_file, 'rb') as f:
    #    raw_lru_cache_data = f.read()
    #with enable_cache_test_mode_for_lru_read_write():
    #    restore_cache_data(nset_groups, nsets_per_write, cache.tag_size, cache, unpack_format, raw_lru_cache_data, size, all_ways_mask, True, 0, 'restoring %s lru' % (cache.name,))

def _extract_memtype(filename):
    '''Extract the memory type from a previously encoded filename representing some
    binary data for a saved memory block.
    
    >>> _extract_memtype('02TestDA74K32bitLEo32-0x80000000.bin')
    0
    >>> _extract_memtype('02TestDA74K32bitLEo32-0x80000000-1.bin')
    1
    >>> _extract_memtype('02TestDA74K32bitLEo32-0x80000000-x.bin')
    0
    '''
    filename = os.path.splitext(filename)[0]
    pos = filename.rfind('-')
    memtype = filename[pos+1:]
    try:
        return int(memtype, 10)
    except Exception:
        pass
    return 0
    
def _extract_address(filename):
    '''Extract the address from a previously encoded filename representing some
    binary data for a saved memory block.
    
    >>> _extract_address('02TestDA74K32bitLEo32-0x80000000.bin')
    '0x80000000'
    >>> _extract_address('02TestDA74K32bitLEo32-0x80000000-1.bin')
    '0x80000000'
    '''
    filename = os.path.splitext(filename)[0]
    fileparts = filename.split('-')
    for fp in fileparts:
        if fp.startswith('0x'):
            try:
                int(fp, 16)
                return fp
            except Exception:
                pass
    return None
    
def read_memory_binfile(binfile, size):
    '''Reads the file containing the binary data of a memory dump and return a tuple
    containing list of the binary data as 4 byte unsigned integers and the binary file
    size if size is not consistent with the file size otherwise None.
    '''
    abs_binfile = absolute_filename(binfile)
    with open(abs_binfile, 'rb') as f:
        memblk = f.read()
    if size == len(memblk):
        if bool(size):
            return [struct.unpack(">I", memblk[ofs:ofs + memory_element_size])[0] for ofs in [memory_element_size * ix for ix in xrange(size / memory_element_size)]], None
        return [], None
    return None, len(memblk)

def restoremem(address, size, binfile, device):
    '''Restore memory.
    
    address:  The start address in memory of the block to be restored.
    
    size:     The size of the memory block to be restored. This must be the same size
              as the file 'binfile'.
    
    binfile:  The path to a file containing the binary data of the memory block being restored.
              The file length must be equal to the given 'size' of the memory block.
    '''
    
    nhex_digits = 16 if is_64_bit(device) else 8
    show_progress('restoring memory [0x%0*x, 0x%0*x)' % (nhex_digits, address, nhex_digits, address+size))
    
    try:
        memelts, binsize = read_memory_binfile(binfile, size)
        if memelts is not None:
            if bool(memelts):
                memtype = _extract_memtype(binfile)
                device.da.WriteMemoryBlock(address, len(memelts), memory_element_size, memelts, memtype)
        else:
            print 'restoremem: requested memory size (0x%x) differs from binary file size (0x%x).' % (size, binsize)
    except Exception as e:
        print 'restoremem: file "%s", open or read failed: %s' % (binfile, str(e))
    
            
@command(verbose=verbosity)
def sysrestore(restorefile, verbose=quiet, force_restore=False, device=None, **kwargs):
    '''
    Restore a system from a system dump specified by the name 'restorefile'.
    The directory used for processing all scripts and data files will be:
    
        $(IMGTEC_USER_HOME)/sysdumps
    
    ================= ==============================================================================
    Parameter         Meaning
    ================= ==============================================================================
    restorefile       The path of the Python script created by a previous call to "sysdump".
    
    verbose           One of quiet, verbose or veryverbose - controls the level of output
                      produced in each restore operation.
                      
    force_restore     Follow default restoration setting of each dumped item unless set to True to
                      force restoration of all dumped data.
    
    ================= ==============================================================================
    '''

    if (kwargs is not None) and ('loudness' in kwargs):
        print 'The use of "loudness" is deprecated. Please set the parameter "verbose" instead.'
        
    _set_force_restore(False) # initialise in case of doctests
    _set_force_restore(force_restore)
    set_show_progress(verbose)
    show_progress('sysrestore executing', restorefile)
    
    abs_restorefile = absolute_filename(restorefile)
    restore_script = ''
    try:
        with open(abs_restorefile, 'r') as f:
            restore_script = f.read()
    except Exception as e:
        print 'sysrestore: open or read of file "%s" failed: %s' % (abs_restorefile, str(e))
        return
            
    try:
        if bool(restore_script):
            from imgtec.lib.backwards import exec_function
            ns = dict(the_device=device)
            exec_function(restore_script, restorefile, ns)
    except Exception as e:
        print 'sysrestore: "%s" failed: %s' % (restorefile, str(e))

if __name__ == "__main__":
    sys.exit(test.main('__main__'))
