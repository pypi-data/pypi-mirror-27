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
from imgtec.console.results import StrResult
from imgtec.console.cache import cacheinfo, CacheException, mappings
from imgtec.console.generic_device import device
from imgtec.console.regs import regs, cp0
from imgtec.console.tlb import tlbd, get_tlb, parse_entry_hi, parse_entry_lo, parse_page_mask
from imgtec.lib import get_user_files_dir
from imgtec.lib.namedenum import namedenum
from imgtec.lib.ordered_dict import OrderedDict
from contextlib import contextmanager
import os, os.path, struct, glob
import string
import datetime, re

# these are global for use within codescapeconsole or by the generated "sysdumpconfig"
# and "sysdump" scripts running standalone

memory_element_size = 4

def set_show_progress(loudness):
    global _verbosity
    _verbosity= loudness
    
def show_progress(msg, extra='', at_level=verbose):
    '''
    >>> show_progress('should not display')    
    >>> show_progress('should not display', extra='this')
    
    >>> set_show_progress(quiet)
    >>> show_progress('should not display', at_level=veryverbose)
    >>> show_progress('should not display', at_level=verbose)
    >>> show_progress('should not display', at_level=quiet)
    >>> show_progress('should not display', extra='this', at_level=verbose)
    >>> show_progress('should not display', extra='this', at_level=quiet)

    >>> set_show_progress(verbose)
    >>> show_progress('should display')
    should display

    >>> show_progress('should display', extra='this')
    should display this

    >>> show_progress('should not display', at_level=quiet)
    >>> show_progress('should not display', extra='this', at_level=quiet)
    
    >>> show_progress('should display', at_level=verbose)
    should display

    >>> show_progress('should display', extra='this', at_level=verbose)
    should display this
    
    >>> show_progress('should not display', at_level=veryverbose)
    >>> show_progress('should not display', extra='this', at_level=veryverbose)
    
    >>> set_show_progress(veryverbose)
    >>> show_progress('should not display', at_level=quiet)
    >>> show_progress('should not display', extra='this', at_level=quiet)
    
    >>> show_progress('should display', at_level=verbose)
    should display

    >>> show_progress('should display', extra='this', at_level=verbose)
    should display this
    
    >>> show_progress('should display', at_level=veryverbose)
    should display

    >>> show_progress('should display', extra='this', at_level=veryverbose)
    should display this
    '''
    if bool(msg):
        verbosity_map = dict(verbosity)
        current_verbosity = _verbosity if isinstance(_verbosity, (int, long)) else verbosity_map[_verbosity]
        verbosity_at_level = at_level if isinstance(at_level, (int, long)) else verbosity_map[at_level]
        if bool(current_verbosity) and bool(verbosity_at_level):
            if current_verbosity >= verbosity_at_level:
                if bool(extra):
                    msg += " %s" % extra
                print msg

def sysdumps_directory():
    return os.path.join(get_user_files_dir(), 'sysdumps').replace('\\', '/')

def ensure_sysdumps_directory_exists():
    dir = sysdumps_directory()
    if not os.path.exists(dir):
        os.mkdir(dir)

def absolute_filename(filename):
    return os.path.join(get_user_files_dir(), 'sysdumps', filename).replace('\\', '/')
    
def delete_files(filename):
    for file in glob.glob(absolute_filename(os.path.splitext(filename)[0]) + "*.*"):
        os.unlink(file)
    
def get_sysrestore_config_filename(dumpconfigfile):
    '''
    >>> get_sysrestore_config_filename('test.py')
    'test-sysrestore.py'
    
    >>> get_sysrestore_config_filename('test-sysdump.py')
    'test-sysrestore.py'
    '''
    
    sysrestore = 'sysrestore'
    if dumpconfigfile.find(sysdump.__name__) != -1:
        return dumpconfigfile.replace(sysdump.__name__, sysrestore)
    
    file, ext = os.path.splitext(dumpconfigfile)
    return file + '-' + sysrestore + ext
    
def append_restore_script(pyline):
    global _sysrestore_script
    _sysrestore_script.append(pyline)
    return pyline
    
def append_restore_script_group(group, pylines):
    global _sysrestore_script_groups
    _sysrestore_script_groups.append((group, pylines))
    
def save_restore_script(restoreconfigfile):
    try:
        abs_restoreconfigfile = absolute_filename(restoreconfigfile)
        with open(abs_restoreconfigfile, 'w') as f:
            f.write('\n'.join(_sysrestore_script))
    except Exception as e:
        print 'sysdump: directory "sysdumps", open or read of "%s" failed: %s' % (restoreconfigfile, str(e))
        

_mips_config_prelude = '''\
#
# This script will will save the state of a system generating a corresponding
# restore script file which will restore the saved data.
#
# You may edit this script at will to further tailor it to your needs by disabling
# any "save..." operations as required.
#
# It is recommmended that the order of the various dump operations are not
# changed and that the indentation of the "save..." calls be respected.
#
# The directory used for processing all scripts and data files will be:
#    
#    $(IMGTEC_USER_HOME)/sysdumps
#
# The environment variable IMGTEC_USER_HOME is set during the installation of the
# Python redistributables that are required for Codescape and Codescape Console.
#

from imgtec.console import *
from imgtec.console.generic_device import device
from imgtec.console.cache import instr, data, secondary, tertiary
from imgtec.console.sysdumps import *

if __name__ == '__main__':
    probe(args=parse_startup_args())

'''

_mips_config_postlude = '''\

if __name__ == '__main__':
    assemble_restore_script()
    restoreconfigfile = get_sysrestore_config_filename('%s')
    save_restore_script(restoreconfigfile)
'''


# ejtag registers
_mips_non_restore_ejtag_regs = '''\
saveejtagregs()

'''

def _check_save_ejtagregs(mips_dump_config, config):
    '''
    >>> _check_save_ejtagregs('', dict())
    ''
    >>> _check_save_ejtagregs('', dict(has_ejtag=True))
    'saveejtagregs()\\n\\n'
    '''
    
    if config.get('has_ejtag', False):
        mips_dump_config += _mips_non_restore_ejtag_regs
    return mips_dump_config


# configuration registers (CP0) registers
_mips_config = '''\
savecpuconfig()

'''


def _generate_register_list(reg, nregs):
    '''
    >>> _generate_register_list('r', 0)
    ''
    >>> _generate_register_list('r', 1)
    "'r0'"
    >>> _generate_register_list('r', 2)
    "'r0', 'r1'"
    '''
    return ', '.join(["'%s%d'" % (reg, r) for r in xrange(nregs)])
    
# general purpose registers
_o3264_registers = """\
  'zero', 'at', 'v0', 'v1', 'a0', 'a1', 'a2', 'a3',
           't0', 't1', 't2', 't3', 't4', 't5', 't6', 't7',
           's0', 's1', 's2', 's3', 's4', 's5', 's6', 's7',
           't8', 't9', 'k0', 'k1', 'gp', 'sp', 's8', 'ra'"""
               
_n3264_registers = """\
  'zero', 'at', 'v0', 'v1', 'a0', 'a1', 'a2', 'a3',
           'a4', 'a5', 'a6', 'a7', 't0', 't1', 't2', 't3',
           's0', 's1', 's2', 's3', 's4', 's5', 's6', 's7',
           't8', 't9', 'k0', 'k1', 'gp', 'sp', 's8', 'ra'"""

_abi_registers_map = dict(o32=_o3264_registers,
                          o64=_o3264_registers,
                          n32=_n3264_registers,
                          n64=_n3264_registers,
                          numeric=_generate_register_list('r', 32))

_mips_gpregs = '''\
saveregs("general purpose registers for %s abi", %d,
         %s)

'''

_mips_gpregs_pc = '''\
saveregs("general purpose register pc", %d,
         'pc')

'''

_mips_gpregs_hilo = '''\
saveregs("general purpose registers hi and lo", %d,
         'hi', 'lo')

'''

def _check_save_gpregs(mips_dump_config, config, abi):
    cpu_is_32bit = config['cpu_is_32bit']
    reg_size_bits = 32 if cpu_is_32bit else 64
    
    mips_dump_config += _mips_gpregs % (abi, reg_size_bits, _abi_registers_map[abi])
    mips_dump_config += _mips_gpregs_pc % (reg_size_bits,)
    if not config.get('has_r6_instruction_set', False):
        mips_dump_config += _mips_gpregs_hilo % reg_size_bits
    return mips_dump_config


# floating point registers (CP1)
_mips_fpu_config = '''\
saveregs("floating point configuration registers (CP1)", 32,
         'fccr', 'fcsr', 'fenr', 'fexr', 'fir')

'''

_fpu_registers = dict(fpu_supports_32bit_float=('single', 32, _generate_register_list("f", 32)),
                      fpu_supports_64bit_float=('double', 64, _generate_register_list("d", 16)))
_mips_fpuregs = '''\
saveregs("%s precision floating point registers (CP1)", %d,
         %s)

'''

def _check_save_fpuregs(mips_dump_config, config):
    if config.get('has_fpu', False) and config.get('fpu_enabled', False):
        mips_dump_config += _mips_fpu_config
        for has_fpu_prop, prop_details in _fpu_registers.iteritems():
            if config.get(has_fpu_prop, False):
                mips_dump_config += _mips_fpuregs % prop_details
    return mips_dump_config


# DSP configuration and registers
_mips_dsp_config = '''\
saveregs("DSP configuration register", 32, 'dspcontrol')

'''

_mips_dsp_registers = '''\
saveregs("DSP registers", 32,
         'hi1', 'hi2', 'hi3', 'lo1', 'lo2', 'lo3')

'''

def _check_save_dspregs(mips_dump_config, config):
    if (config.get('has_dsp1', False) or config.get('has_dsp2', False) or config.get('has_dsp3', False)) and config.get('dsp_enabled', False):
        mips_dump_config += _mips_dsp_config
        mips_dump_config += _mips_dsp_registers
    return mips_dump_config
    

# MSA configuration and registers
_mips_msa_config = '''\
saveregs("SIMD configuration registers (MSA)", 32,
         'MSAIR', 'MSACSR', 'MSAAccess', 'MSASave', 'MSAModify', 'MSARequest', 'MSAMap', 'MSAUnmap')

'''

_mips_msa_regs = '''\
saveregs("SIMD registers (MSA)", 128,
         %s)

''' % _generate_register_list("w", 32)

def _check_save_msaregs(mips_dump_config, config):
    if config.get('has_msa', False) and config.get('msa_enabled', False):
        mips_dump_config += _mips_msa_config
        mips_dump_config += _mips_msa_regs
    return mips_dump_config


# TLB data
_mips_tlbs = '''\

savetlbs("# TLB - translation look-aside buffers", '%s')
'''

def _check_save_tlbs(mips_dump_config, config, dumpconfigfile, dump):
    if dump and config.get('has_mmu', False):
        mips_dump_config += _mips_tlbs % dumpconfigfile
    return mips_dump_config
    

# Caches
_mips_caches = '''\

savecache("%s", %s, '%s')
'''

def _check_save_caches(mips_dump_config, config, dumpconfigfile, dump):
    if dump:
        try:
            caches = cacheinfo()
            cache_mappings = dict((k, v) for k, v in mappings)
            for cacheobj in caches:
                mips_dump_config += _mips_caches % (cacheobj.name, cache_mappings[cacheobj.cmd_name], dumpconfigfile)
        except CacheException:
            pass
    return mips_dump_config


# Stack
_mips_stack_config = '''\
savestack('%s', '%s')
'''

def _check_save_stack(mips_dump_config, dumpconfigfile, stack):
    if stack:
        mips_dump_config += _mips_stack_config % (dumpconfigfile, stack)
    return mips_dump_config

_mips_memory_config = '''\
$memory
'''

_sysrestore_script_prelude = """\
#
# This script will restore the state of an identical physical system to the state at
# which this script was generated using the "sysdump" command.
#
# You may edit this script at will or the binary dump files (".bin" files) associated
# with this restoration script which can be found as parameters of the following
# funtions:
#
#     'restoretlbs'    (first parameter)
#     'restorecache'   (first parameter)
#     'restoremem'     (third parameter)
#
# when present.
#
# The names of binary data files saved during the dump are derived from the value of
# 'dumpconfigfile' parameter of 'sysdump' or from a suitable default if this is not
# given.
#
# For memory blocks, the size of a memory block is the size of the corresponding
# binary dump file (".bin" file). The name of an individual memory blocks' binary dump
# file is taken from the main dump filename:
#
#    <main dump filename>-<block address>-<asid>.bin
#
# For all binary dump files that represent blocks of memory <asid> is a decimal integer
# specifying the address space identifier.
#
# The stack, if dumped, has a binary dump filename as follows:
#
#    <main dump filename>-stack-<block address>-<asid>.bin
#
# TLB data is written to a binary dump file (".bin" file) whose name is:
#
#    <main dump filename>-tlbdata.bin
#
# TLB entries that have valid entries (physical to virtual address mappings) will be
# saved to binary dump files with names taken from the main TLB data file:
#
#    <main dump filename>-tlbdata-<virtual page address>-<asid>.bin
#
# Cache data is written to binary dump files (".bin" file) whose names are:
#
#    <main dump filename>-icache.bin
#    <main dump filename>-dcache.bin
#    <main dump filename>-secondary.bin
#    <main dump filename>-tertiary.bin
#
# according to the hardware configuration.
#
# By default, restoration of cache data is disabled in the generated restore script.
# See the comment associated with the cache restoration command in this script.
#
# It is recommmended that the order of the various restoration operations are not
# changed and that the indentation of the "restore..." calls be respected.
#
# The directory used for processing all scripts and data files will be:
#    
#    $(IMGTEC_USER_HOME)/sysdumps
#
# The environment variable IMGTEC_USER_HOME is set during the installation of the
# Python redistributables that are required for Codescape and Codescape Console.
#

from imgtec.console import *
from imgtec.console.support import *
from imgtec.console.generic_device import device
from imgtec.console.cache import icache, dcache, secondary, tertiary, invalidate
from imgtec.console.sysdumps import absolute_filename, set_show_progress
from imgtec.console.sysrestores import *
import struct

if __name__ == '__main__':
    probe(args=parse_startup_args())
else:
   def device():
       return the_device
"""

_sysrestore_script_prelude_progress = """\

if __name__ == '__main__':
    set_show_progress(verbose)
"""

_sysrestore_script_postlude = '''\
if __name__ == '__main__':
    halt()
    closeprobe()
'''

_sysrestore_order = ('memory', 'tlbs', 'caches', 'registers', 'config', 'ejtag')
_sysrestore_script_groups = []
_sysrestore_script = list()

def assemble_restore_script():
    global _sysrestore_script_groups, _sysrestore_script
    _sysrestore_script = []
    append_restore_script(_sysrestore_script_prelude)
    append_restore_script(_sysrestore_script_prelude_progress)
    for _roix, roitem in enumerate(_sysrestore_order):
        matched = []
        for gix, gitem in enumerate(_sysrestore_script_groups):
            gorder, gpylines = gitem
            if gorder == roitem:
                _sysrestore_script.extend(gpylines)
                _sysrestore_script.append('\n')
                matched.append(gix)
        matched.reverse()
        for gix in matched:
            _sysrestore_script_groups.pop(gix)
    append_restore_script(_sysrestore_script_postlude)

def _regroup_regs_result(regres):
    # regroup the registers by putting the "special cases" (principal configuration registers)
    # at the front of the list
    regres_str = str(regres).lower()
    special_cases = ['status', 'config', 'config1', 'config2', 'config3', 'config4', 'config5', 'config6', 'config7']
    sreg_vals = OrderedDict() # for the special cases
    regs_vals = OrderedDict() # for the rest
    for reg in regres.keys():
        try:
            val = regres[reg]
            # extract the string value from the display string of regres for reg
            if (val is not None) and (val != 'not found'):
                pos = 0
                while True: # check if reg is a substring another reg e.g. 'status' is in 'tcstatus' and skip
                    pos = regres_str.find(reg.lower(), pos)
                    if (pos > 0) and (regres_str[pos-1].isalnum()): # check previous char (if possible) and move past substring
                        pos += len(reg)
                    else:
                        break
                pos = pos + len(reg)
                while not regres_str[pos:pos+1].isalnum():
                    pos += 1
                epos = pos
                while regres_str[epos:epos+1].isalnum(): 
                    epos += 1
                val = regres_str[pos:epos]
                if reg.lower() in special_cases:
                    sreg_vals[reg] = val.lower()
                else:
                    regs_vals[reg] = val.lower()
        except Exception:
            pass
    
    sreg_vals.update(regs_vals) # add the rest after the specials
    return sreg_vals

def _nitems_per_group(cpu_is_32bit):
    ''' The number of items to appear on each line in the restoration script
        according the register size for easier reading and editing by the user.
        
    >>> _nitems_per_group(True)
    4
    >>> _nitems_per_group(False)
    2
    '''
    return 4 if cpu_is_32bit else 2
    
def _group_items(items, cpu_is_32bit, nitems_per_group=0):
    ''' Returns a list of lists in which each sublist contains a fixed(and equal)
        number of items except for the last one which may contain less than that
        fixed number according to the register size.
        
    >>> _group_items([], True)
    []
    >>> _group_items([1], True)
    [[1]]
    >>> _group_items([1, 2], True)
    [[1, 2]]
    >>> _group_items([1, 2, 3], True)
    [[1, 2, 3]]
    >>> _group_items([1, 2, 3, 4], True)
    [[1, 2, 3, 4]]
    >>> _group_items([1, 2, 3, 4, 5], True)
    [[1, 2, 3, 4], [5]]
    >>> _group_items([1, 2, 3, 4, 5, 6, 7, 8], True)
    [[1, 2, 3, 4], [5, 6, 7, 8]]
    >>> _group_items([1, 2, 3, 4, 5, 6, 7, 8, 9], True)
    [[1, 2, 3, 4], [5, 6, 7, 8], [9]]
    >>> _group_items([], False)
    []
    >>> _group_items([1], False)
    [[1]]
    >>> _group_items([1, 2], False)
    [[1, 2]]
    >>> _group_items([1, 2, 3], False)
    [[1, 2], [3]]
    >>> _group_items([1, 2, 3, 4], False)
    [[1, 2], [3, 4]]
    >>> _group_items([1, 2, 3, 4, 5], False)
    [[1, 2], [3, 4], [5]]
    '''
    n_items = len(items)
    nitems_per_group = nitems_per_group or _nitems_per_group(cpu_is_32bit)
    return [items[gs:min(gs+nitems_per_group,n_items)] for gs in xrange(n_items) if gs % nitems_per_group == 0]

def _append_restoreregs_command(comment, register_names, register_values, max_width, cpu_is_32bit, restore, rgroup):
    regs_vals = []
    for reg, val in zip(register_names, register_values):
        regs_vals.append("(%*s, %s)" % (max_width, reg, val))        
    regval_groups = _group_items(regs_vals, cpu_is_32bit)
    gix_last = len(regval_groups) - 1
    pylines = []
    pylines.append("# " + comment)
    if not restore:
        pylines.append('# the code for the restoration of these registers has been generated but disabled')
        pylines.append('# by setting the value of the last argument "restore" to "False" because restoration')
        pylines.append('# could result in undefined or unpredictable behaviour')
        pylines.append('#')
        pylines.append('# you may enable the restoration of these registers by changing the value of "restore"')
        pylines.append('# to True at your own risk')
        pylines.append('#')
    
    restorreregs = 'restoreregs('
    restorreregs_args_indent = ' '*len(restorreregs)
    for gix, group in enumerate(regval_groups):
        group_starter = restorreregs + '[' if gix == 0 else restorreregs_args_indent + ' '
        group_trailer = ',' if gix < gix_last else '],'
        pylines.append('%s%s%s' % (group_starter, ','.join(group), group_trailer))
    pylines.append('%s%s%s' % (restorreregs_args_indent, "'%s'" % comment, ','))
    pylines.append('%srestore=%s)' % (restorreregs_args_indent, 'True' if restore else 'False'))
    append_restore_script_group(rgroup, pylines)
            
def _save_registers(comment, regs_result, group='registers', restore=True):
    '''The main function used for saving lists of registers.
    
    comment:      the comment that is output to the restore script for the register restore operation
    
    reg_results:  an instance of the object returned by the 'regs' command i.e. instance of MultipleRegResult
    
    group:        the restoration group to which these registers belong - used in determining the
                  restoration order
    
    restore:      flag indicating if the restoration of this regiater group is to be enabled
    '''
    
    config = dict(device().da.CpuInfo())
    cpu_is_32bit = config['cpu_is_32bit']
    regs_vals = _regroup_regs_result(regs_result)
    register_names = ["'%s'" % r for r in regs_vals.keys()]
    register_values = ["0x%s" % v for v in regs_vals.values()]
    max_width = max([len(r) for r in register_names] + [len(v) for v in register_values])
    register_names =  [r.rjust(max_width) for r in register_names]
    register_values = [v.rjust(max_width) for v in register_values]
    _append_restoreregs_command(comment, register_names, register_values, max_width, cpu_is_32bit, restore, group)

def _calc_max_fixed_width(names, nhex_digits):
    '''
    >>> _calc_max_fixed_width([], 10)
    12
    >>> _calc_max_fixed_width(['a', 'aa', 'abcdefghijklmnopqrstuvwxyz'], 13)
    28
    '''
    names = names if len(names) else ['',]
    max_name_len = max([len(name) for name in names]) + 2 # take into account quotes for r format
    return max([max_name_len, nhex_digits + 2])           # take into account 0x for hex format

def digit_count(n, base=16):
    ''' Use mathematical purity instead because hex(n)-2 ignores the L that may
        appear at the end of the string returned by hex!
    
    >>> digit_count(0x1)
    1
    >>> digit_count(4096)
    4
    >>> digit_count(0x100000000000)
    12
    '''
    
    from math import ceil, log
    return int(ceil(log(n+1)/log(base)))
    
_savememory_format = "\nsavememory('%s', 0x%0*x, 0x%x, %d)"
def _build_savememory(memory_block_descriptors, nhex_digits, filename):
    '''Returns the string that forms the memory save commands from a list of memory descriptors.
    
    >>> _build_savememory('4K@0x80008000', 8, 'test_save_memory.py')
    "\\nsavememory('test_save_memory.py', 0x80008000, 0x1000, 0)"
    
    >>> _build_savememory('4K@0x800080008000', 8, 'test_save_memory.py')
    "\\nsavememory('test_save_memory.py', 0x800080008000, 0x1000, 0)"
    
    >>> _build_savememory('4K@0x8000', 8, 'test_save_memory.py')
    "\\nsavememory('test_save_memory.py', 0x00008000, 0x1000, 0)"

    >>> _build_savememory('4K@0x8000,4K@0x80008000', 8, 'test_save_memory.py')
    "\\nsavememory('test_save_memory.py', 0x00008000, 0x1000, 0)\\nsavememory('test_save_memory.py', 0x80008000, 0x1000, 0)"
    '''
    
    savemem_str = ''
    if memory_block_descriptors:
        memory_block_descriptors = memory_block_descriptors.split(',')
        for memblk_desc in memory_block_descriptors:
            parsed_descriptor = parse_memory_descriptor(memblk_desc)
            if bool(parsed_descriptor):
                address_range, memtype = parsed_descriptor
                ndigits = max(nhex_digits, digit_count(address_range.begin))
                savemem_str += _savememory_format % (filename, ndigits, address_range.begin, address_range.size, memtype)
    return savemem_str
    
def _check_filename_part(part):
    '''
    >>> _check_filename_part('part')
    '-part'
    
    >>> _check_filename_part('')
    ''
    '''
    
    if bool(part):
        return '-' + part
    return ''

def _dumpconfig_filename(system_id, cpu_name=None, title=None, when=None):
    '''Returns a filename comprising the system_id and supplied title(if any) and other information.
    
    >>> _dumpconfig_filename('TestDA', when='now')
    'sysdump-TestDA-now.py'

    >>> _dumpconfig_filename('TestDA', title='title', when='tomorrow')
    'sysdump-TestDA-title-tomorrow.py'
    
    >>> _dumpconfig_filename('TestDA', cpu_name='test-cpu', when='now')
    'sysdump-TestDA-test-cpu-now.py'
    
    >>> _dumpconfig_filename('', when='tomorrow')
    'sysdump-dump-config-supplied-da-name-tomorrow.py'
    '''
    system_id = system_id if bool(system_id) else 'dump-config-supplied-da-name'
    cpu_name = _check_filename_part(cpu_name)
    title = _check_filename_part(title)
    now = datetime.datetime.now()
    now = now.replace(microsecond=0)
    when = '-' + (when if bool(when) else now.isoformat())
    filename = re.sub('[ :]+', '-', "sysdump-" + system_id + cpu_name + title + when + '.py')
    return filename
    
_verbosity = quiet

# dumpers start here
_dumpers = {}
def dumper(f):
    _dumpers[f.__name__] = f
    return f

@dumper
def saveejtagregs():
    '''Save the e-jtag registers.'''
    show_progress('saving e-jtag registers')        
    registers = ['ejtag_idcode',      'ejtag_impcode',  'ejtag_ecr',         'ejtag_tcbcontrola', 'ejtag_tcbcontrolb', 'ejtag_tcbdata',
                 'ejtag_tcbcontrolc', 'ejtag_pcsample', 'ejtag_tcbcontrold', 'ejtag_tcbcontrole', 'ejtag_fdc',         'ejtag_dcr']
    _save_registers("ejtag registers", regs(registers), restore=False, group='ejtag')
    
@dumper
def savecpuconfig():
    '''Save the cpu configuration i.e. cp0.'''
    show_progress('saving configuration registers (CP0)')
    _save_registers("configuration registers (CP0)", cp0(), restore=False, group='config')

@dumper
def saveregs(comment, reg_size_bits, *names):
    '''Saves a list of registers specified by the list names.'''
    show_progress('saving %s' % (comment,))
    values = regs(names)
    if len(names) == 1:
        nhex_digits = {32:8, 64:16, 128:32}[reg_size_bits]
        pylines = []
        pylines.append("# register %s" % names[0])
        pylines.append("restoreregs([(%r, 0x%0*x),], '%s')" % (names[0], nhex_digits, values, comment))
        append_restore_script_group('registers', pylines)
    else:
        _save_registers(comment, values)

def _read_page_at_virtual_address(nhex_digits, vaddress, paddress, page_size, asid):
    show_progress('saving page at virtual(physical) 0x%0*x(0x%0*x)' % (nhex_digits, vaddress, nhex_digits, paddress), at_level=veryverbose)
    return device().da.ReadMemoryBlock(vaddress, page_size / memory_element_size, memory_element_size, asid)

def _write_memory_block_to_file(filename, memblk):
    abs_filename = absolute_filename(filename)
    with open(abs_filename, 'wb') as f:
        for memelt in memblk:
            f.write(struct.pack('>I', memelt))
    return os.stat(abs_filename).st_size
    
def _write_physical_page_to_file(saved_pages, file, nhex_digits, vaddress, asid, memblk, paddress):
    filename = "%s-tlbdata-0x%0*x-%d" % (file, nhex_digits, vaddress, asid) + '.bin'
    filesize = _write_memory_block_to_file(filename, memblk)
    saved_pages.append(('0x%0*x' % (nhex_digits, vaddress), '0x%0*x' % (nhex_digits, paddress), "'%s'" % filename, "0x%08x" % filesize))
    return saved_pages
    
@dumper
def savetlbs(comment, filename):
    '''Saves the Translation Lookaside Buffers to the specifed file filename.
    Then for each valid TLB entry, saves the data from mapped pages at specified
    virtual/physical addresses.
    
    The main TLB data file name has the form:
        <value of filename argument>-tlbdata.txt
    
    The file name of each page of memory data has the form:
        <value of filename argument>-tlbdata-<virtual address>-<asid>.bin
    
    '''
    show_progress('saving tlbs')
        
    file, _ext = os.path.splitext(filename)
    filename = "%s-tlbdata" % (file,) + '.bin'
    binsize = 0

    v = tlbd()
    entries = [tuple(x) for x in v]
    abs_filename = absolute_filename(filename)
    with open(abs_filename, 'wb') as f:
        for entry in entries:
            for item in entry:
                f.write(struct.pack('>Q', item))
    binsize = os.stat(abs_filename).st_size
    
    config = dict(device().da.CpuInfo())
    nhex_digits = 8 if config['cpu_is_32bit'] else 16
    
    tlb_model = get_tlb(device())
    saved_pages = []
    for x in v:
        entryhi_f   = parse_entry_hi(x.EntryHi, tlb_model.architecture_revision, tlb_model.config3sp, tlb_model.pagegrainesp, tlb_model.is64)
        vaddress = entryhi_f['virtual addr']
        asid = entryhi_f['addr space id']
        pagemask_f  = parse_page_mask(x.PageMask, tlb_model.architecture_revision, tlb_model.config3sm, tlb_model.is64)
        page_size = parse_memblock_size(pagemask_f['page size'].replace(' ', ''))
        
        entrylo0_f  = parse_entry_lo(x.EntryLo0, tlb_model.architecture_revision, tlb_model.config3sm, tlb_model.is64)
        paddress_lo0 = entrylo0_f['physical addr']
        if entrylo0_f['valid']:
            try:
                memblk = _read_page_at_virtual_address(nhex_digits, vaddress, paddress_lo0, page_size, asid)
            except Exception as e:
                show_progress("savetlbs: failed to save page at virtual(physical) 0x%0*x(0x%0*x) - %s" % (nhex_digits, vaddress, nhex_digits, paddress_lo0, str(e)), at_level=veryverbose)
            else:
                saved_pages = _write_physical_page_to_file(saved_pages, file, nhex_digits, vaddress, asid, memblk, paddress_lo0)
        
        entrylo1_f  = parse_entry_lo(x.EntryLo1, tlb_model.architecture_revision, tlb_model.config3sm, tlb_model.is64)
        if entrylo1_f['valid']:
            paddress_lo1 = entrylo1_f['physical addr']
            vaddress += (paddress_lo1 - paddress_lo0)            
            try:
                memblk = _read_page_at_virtual_address(nhex_digits, vaddress, paddress_lo1, page_size, asid)
            except Exception as e:
                show_progress("savetlbs: failed to save page at virtual(physical) 0x%0*x(0x%0*x) - %s" % (nhex_digits, vaddress, nhex_digits, paddress_lo1, str(e)), at_level=veryverbose)
            else:
                saved_pages = _write_physical_page_to_file(saved_pages, file, nhex_digits, vaddress, asid, memblk, paddress_lo1)
    
    restoretlbs = 'restoretlbs('
    restoretlbs_indent = ' '*len(restoretlbs)

    pylines = []
    pylines.append(comment)
    pylines.append("%s'%s', 0x%x," % (restoretlbs, filename, binsize))

    if bool(saved_pages):
        spix_last = len(saved_pages) - 1
        for spix, sp in enumerate(saved_pages):
            group_starter = '[(' if spix == 0 else ' ('
            group_trailer = '),' if spix < spix_last else ')],'
            pylines.append('%s%s%s%s' % (restoretlbs_indent, group_starter, ', '.join(sp), group_trailer))
    else:
        pylines.append('%s[],' % (restoretlbs_indent,))
        
    pylines.append('%srestore=True)' % (restoretlbs_indent,))
    append_restore_script_group('tlbs', pylines)
    
@contextmanager
def enable_cache_test_mode_for_lru_read_write():
    try:
        errctl_reg = 'ErrCtl'
        errctl_value = device().da.ReadRegister(errctl_reg)
        wst_bit = 1 << 29 # set way select test mode - for load tag reads the lru
        knockout_spr_pco_bits = 0xe7ffffff # ~ (3 << 27) i.e ~0x18000000
        device().da.WriteRegister(errctl_reg, (errctl_value | wst_bit) & knockout_spr_pco_bits)
        yield
    finally:
        device().da.WriteRegister(errctl_reg, errctl_value)
         
def target_read_cache_data(cinfo, tag_only):
    cache_sets = []
    all_ways_mask = (2**cinfo.associativity)-1
    for setix in xrange(cinfo.sets_per_way):
        offset = setix * cinfo.line_size
        cache_sets.append(device().da.ReadCache(cinfo.type, offset, 1, all_ways_mask, tag_only, False))
    return cache_sets
    
def file_write_cache_data(cache_data, f, pack_format, progress_msg):
    show_progress(progress_msg, at_level=veryverbose)
    for cset in cache_data:
        for item in cset:
            f.write(struct.pack(pack_format, item))
    
@dumper
def savecache(comment, cache, dumpconfigfile):
    show_progress('saving %s' % (comment,))
        
    config = dict(device().da.CpuInfo())
    cpu_is_32bit = config['cpu_is_32bit']
    cinfo = cacheinfo(cache)[0]
    
    cache_sets = target_read_cache_data(cinfo, False)        
    with enable_cache_test_mode_for_lru_read_write():
        cache_lru_sets = target_read_cache_data(cinfo, True)
    
    filename = "%s-%s" % (os.path.splitext(dumpconfigfile)[0], str(cache)) + ".bin"
    pack_format = ">I" if cpu_is_32bit else ">Q"
    abs_filename = absolute_filename(filename)
    with open(abs_filename, 'wb') as f:
        # first four 4-byte items are the cache configuration
        f.write(struct.pack(">I", cinfo.associativity))
        f.write(struct.pack(">I", cinfo.sets_per_way))
        f.write(struct.pack(">I", cinfo.line_size))
        f.write(struct.pack(">I", cinfo.tag_size))
        file_write_cache_data(cache_sets, f, pack_format, 'saving %s data' % (cinfo.name,))
    binsize = os.stat(abs_filename).st_size
    
    lru_filename = "%s-%s" % (os.path.splitext(dumpconfigfile)[0], str(cache)) + "-lru.bin"
    abs_lru_filename = absolute_filename(lru_filename)
    with open(abs_lru_filename, 'wb') as f:
        file_write_cache_data(cache_lru_sets, f, pack_format, 'saving %s lru' % (cinfo.name,))
    
    pylines = []
    pylines.append('# %s' % comment)
    pylines.append('# the code for the restoration of the %s has been generated but disabled by setting' % (cinfo.name,))
    pylines.append('# the value of the last argument "restore" to False because it could result in undefined')
    pylines.append('# or unpredictable behaviour')
    pylines.append('#')
    pylines.append('# you may enable restoration of the %s by setting the value of "restore" to True' % (cinfo.name,))
    pylines.append('# at your own risk')
    pylines.append('#')
    pylines.append("restorecache(%s, '%s', 0x%08x, restore=False)" % (str(cache), filename, binsize))
    append_restore_script_group('caches', pylines)

@contextmanager
def setup_physical_memory_access(address):
    class _address_error(Exception):
        pass
        
    class _uncached_unmapped_addresses(object):
        def __init__(self, adjustment):
            self.adjustment = adjustment
            
        def adjust(self, address):
            return address #+ self.adjustment
        
    config = dict(device().da.CpuInfo())
    cpu_is_32bit = config['cpu_is_32bit']
    nhex_digits = 8 if cpu_is_32bit else 16
    try:
        if address < 0x8000000 or address >= 0xc0000000:
            raise _address_error('0x%0*x is always mapped through the MMU' % (nhex_digits, address))
        
        yield _uncached_unmapped_addresses(0x20000000 if address < 0xa0000000 else 0)
    finally:
        pass

def make_memory_binfile_name(sysdump_filename, nhex_digits, address, memtype):
    '''
    >>> make_memory_binfile_name('test.py', 8, 0x80000000, 0)
    'test-0x80000000-0.bin'
    '''
    return "%s-0x%0*x-%d" % (os.path.splitext(sysdump_filename)[0], nhex_digits, address, memtype) + ".bin"
    
@dumper
def savememory(filename, address, size, memtype=0, title=''):
    '''Saves a block of memory using 'filename' as a root for the name of the file
    containing the binary contents of the memory block.
    '''
    show_progress('saving memory [0x%08x, 0x%08x)' % (address, address+size), title)
    config = dict(device().da.CpuInfo())
    cpu_is_32bit = config['cpu_is_32bit']
    nhex_digits = 8 if cpu_is_32bit else 16
    
    try:
        with setup_physical_memory_access(address) as address_adjuster:
            memblk = device().da.ReadMemoryBlock(address_adjuster.adjust(address), size / memory_element_size, memory_element_size, memtype)
    except Exception as e:
        show_progress("savememory: failed %s" % str(e), at_level=veryverbose)
    else:
        # for uniqueness take the address and memory type and encode them into the filename for the binary memory data
        filename = make_memory_binfile_name(filename, nhex_digits, address, memtype)
        _write_memory_block_to_file(filename, memblk)

        restore = 'restore'
        comment = "%s memory block [%s) - %d bytes in memory type %d" % (restore, str(AddressRangeType(address, address + size)), size, memtype)
        if bool(title):
            lrestore = comment.find(restore) + len(restore)
            comment = comment[0:lrestore] + " " + title + comment[lrestore:]

        pylines = []
        pylines.append("# %s" % comment)
        pylines.append("restoremem(0x%0*x, 0x%x, '%s', device=device())" % (nhex_digits, address, size, filename))
        append_restore_script_group('memory', pylines)
    
@dumper
def savestack(filename, stack_size):
    stack_size = parse_memblock_size(stack_size)
    if bool(stack_size):
        filepart, ext = os.path.splitext(filename)    
        stack_ptr = device().da.ReadRegister('sp' if device().da.GetABI() != 'numeric' else 'r29')
        savememory(filepart + "-stack" + ext, stack_ptr, stack_size, title='stack')


# commands start here

@command()
def sysdumpconfig(dumpconfigfile=None, stack=0, memory='', title=None, dump_tlbs=True, dump_caches=True, device=None):
    r'''Generates a :func:`~imgtec.console.sysdump` script which will save all specified target data.
    
    The generated script is based on the configuration and supplied arguments specifying
    what data to read from the current target which can be used in a subsequent call to :func:`~imgtec.console.sysdump`.
    The name of the script is the value returned by this command.
    
    For a more detailed description and example see :ref:`sysdump-intro`.
    
    The directory used for processing all scripts and data files will be:
    
        $(IMGTEC_USER_HOME)/sysdumps
        
    The returned path is relative to the directory specified above.
        
    ================= ==============================================================================
    Parameter         Meaning
    ================= ==============================================================================
    dumpconfigfile    The name to be used for the file to contain the generated script.
                      If not supplied a suitable one will be created utilising the 'title' parameter.
                      
    stack             The number of bytes of memory to save starting at the location in the
                      "stack pointer" register: either "sp" for o32/64 or n32/64 abi's,
                      or "r29" for numeric abi. It can be either an integer or the abbreviated form
                      described in <block size> for a memory block below.
            
    memory            A string of comma separated memory descriptors.
                      Each descriptor has the syntax:
                      
                        <block size>@<address>[@<memory type>]
                        
                      <block size> indicates the size of the memory block and must be integral
                      or an abbreviation as follows:
                      
                        <decimal integer>[K | M]
                        
                      where K means 1024 bytes (kilobyte - binary)
                      and   M means 1048576 bytes (megabyte - binary)
                      
                      <address> the virtual address of the start of the block
                      
                      <memory type> if present is a positive integer.
                      
                      Note: since sysdumpconfig/sysdump is primarily for use on "bare metal" systems
                      it is assumed that addresses are either in kseg0 or kseg1 i.e. addresses are in
                      the semi-open intervals [0x80000000, 0xa0000000) or [0xa0000000, 0xc0000000).
            
    title             An optional string used in constructing the returned path for the dump
                      configuration if 'dumpconfigfile' argument is not present.
                      
    dump_tlbs         A flag for deciding whether to dump the TLB, defaulting to True - dump the
                      TLB. Disabled when False - this is suitable for applications that to not make
                      use of the TLB.
                      
    dump_caches       A flag for deciding whether to dump the cahces, defaulting to True - dump the
                      caches. Disabled when False.
    
    ================= ==============================================================================
    '''

    config = dict(device.da.CpuInfo())
    if dumpconfigfile is None:
        dumpconfigfile = _dumpconfig_filename(device.da.GetIdentifier(), title=title, cpu_name=config['cpu_name'])
        
    cpu_is_32bit = config['cpu_is_32bit']
    reg_size_bits = 32 if cpu_is_32bit else 64
    nhex_digits = {32:8, 64:16}[reg_size_bits]
    abi = device.da.GetABI()
    
    mips_dump_config = _mips_config_prelude
    
    mips_dump_config += _mips_config
    mips_dump_config = _check_save_ejtagregs(mips_dump_config, config)
    mips_dump_config = _check_save_dspregs(mips_dump_config, config)
    mips_dump_config = _check_save_msaregs(mips_dump_config, config)    
    mips_dump_config = _check_save_fpuregs(mips_dump_config, config)
    mips_dump_config = _check_save_gpregs(mips_dump_config, config, abi)
    
    mips_dump_config = _check_save_tlbs(mips_dump_config, config, dumpconfigfile, dump_tlbs)
    mips_dump_config = _check_save_caches(mips_dump_config, config, dumpconfigfile, dump_caches)
    
    mips_dump_config = _check_save_stack(mips_dump_config, dumpconfigfile, stack)
    mips_dump_config += _mips_memory_config
    
    mips_dump_config += _mips_config_postlude % dumpconfigfile

    t = string.Template(mips_dump_config)
    sysdump_script = t.safe_substitute(memory=_build_savememory(memory, nhex_digits, dumpconfigfile))
    
    abs_dumpconfigfile = absolute_filename(dumpconfigfile)
    ensure_sysdumps_directory_exists()
    with open(abs_dumpconfigfile, 'w') as f:
        f.write(sysdump_script)
    # TODO display(?) the configuration save script filename
    #print 'sysdumpconfig: the script to save the current configuration is "%s"' % abs_dumpconfigfile
    return StrResult(dumpconfigfile)


@command(verbose=verbosity)
def sysdump(dumpconfigfile=None, stack=0, memory='', title=None, dump_tlbs=True, dump_caches=True, verbose=quiet, device=None, **kwargs):
    r'''
    Save system data, returning the path of a script that will restore the saved data.
    
    ================= ==============================================================================
    Parameter         Meaning
    ================= ==============================================================================
    verbose           One of quiet, verbose or veryverbose - controls the level of output
                      produced in each save operation.
    
    ================= ==============================================================================
    
    See "sysdumpconfig" for details regarding the remaining arguments and returned value.
    '''
    
    if kwargs is not None:
        if 'loudness' in kwargs:
            print 'The use of "loudness" is deprecated. Please set the parameter "verbose" instead.'
        elif len(kwargs):
            raise TypeError('sysdump() got an unexpected keyword argument(s) "%s"' % ' '.join(kwargs.keys()))
    
    set_show_progress(verbose)
    if dumpconfigfile is None:
        dumpconfigfile = sysdumpconfig(stack=stack, memory=memory, title=title, dump_tlbs=dump_tlbs, dump_caches=dump_caches, device=device)
    
    show_progress('sysdump executing', dumpconfigfile)

    dumpconfig = ''
    abs_dumpconfigfile = absolute_filename(dumpconfigfile)
    try:
        with open(abs_dumpconfigfile, 'r') as f:
            dumpconfig = f.read()
    except Exception as e:
        print 'sysdump: file "%s", open or read failed: %s' % (abs_dumpconfigfile, str(e))
        return StrResult('')

    if bool(dumpconfig):
        from imgtec.lib.backwards import exec_function
        ns = dict(_dumpers)
        ns.update(dict(the_device=device))
        
        exec_function(dumpconfig, dumpconfigfile, ns)
        assemble_restore_script()
        
        restoreconfigfile = get_sysrestore_config_filename(dumpconfigfile)
        save_restore_script(restoreconfigfile)
        # TODO display(?) the configuration restore script filename
        #print 'sysdump: the script to restore the current configuration is "%s"' % absolute_filename(restoreconfigfile)
        return StrResult(restoreconfigfile)
    return StrResult('')
    

if __name__ == "__main__":
    sys.exit(test.main('__main__'))
