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

import os
from imgtec.test import *
from imgtec.console.support import *
from imgtec.console.results import *
from imgtec.console.textfile import parse_srec
from imgtec.console.hexfile import parse_hex
from imgtec.console.memory import CompareResult
from imgtec.console import breakpoints
from collections import namedtuple
from imgtec.lib.rst import table, headerless_table
from imgtec.codescape import program_file as pfile

class LoadException(Exception):
    pass
    
class FileExtNotSupportedError(LoadException):
    pass

class ElfNotLoadedError(LoadException):
    pass
    
class UnknownFileTypeError(LoadException):
    pass

class SourceError(Exception):
    pass

class SymbolError(RuntimeError):
    pass

def elf_required(device):
    try:
        if not device.objfile:
            raise ElfNotLoadedError("No elf has been loaded, see the load command.")
    except AttributeError:
        raise ElfNotLoadedError("No elf has been loaded, see the load command.")

class SourceResult(object):
    def __init__(self, file, line, lines, start_line):
        self.file         = file
        self.lines        = lines
        self.start_line   = start_line
        self.current_line = line

    def __repr__(self):
        ret = [':'.join([self.file, str(self.current_line)])]

        if self.lines:
            num_str = '%0{}d'.format(len(str(self.start_line+len(self.lines)-1)))

            for ln, l in enumerate(self.lines, self.start_line):
                line_no = num_str % ln
                parts = [line_no, '>' if ln == self.current_line else '|']
                if l:
                    parts.append(l)
                ret.append(' '.join(parts))

        return '\n'.join(ret)

@command()
def source(address=None, lines=3, device=None):
    '''
    Show the file path and line number of the source file at the given address.
    If 'address' is None, the PC will be used as the address. Set 'lines' to 
    change how many lines either side of the current line are shown.
    '''
    elf_required(device)
    
    if address is None:
        address = device.tiny.ReadRegister('pc')

    src = device.objfile.source_at_address(address)
    file, line = src.filename(), src.line()
    source_lines, start = None, None

    try:
        with open(file, 'r') as f:
            #Line numbers are 1 indexed
            start = max(line-lines, 1) 
            end = line + lines + 1
            source_lines = []
            for line_no, line_str in enumerate(f, 1):
                if line_no == end: 
                    break
                elif line_no >= start:
                    source_lines.append(line_str.rstrip())
    except IOError:
        pass
	
	#Note that line no.s here are 1 indexed
    return SourceResult(file, line, source_lines, start)
    
@command()
def symbol(input, device=None):
    '''
    Look up the value of a symbol by name, or the name of a symbol by its value.
    
    This can be used to display the address of function. Symbols are 
    also implicitly looked up in commands which expect an address.
    '''
    elf_required(device)
        
    if isinstance(input, (int, long)):
        syms = device.objfile.symbols_at_address(input)
        if syms:
            return SymbolResultTable([Symbol(sym) for sym in syms])
        else:
            raise SymbolError("No symbols for address 0x%x" % input)
    else:
        return Symbol(device.objfile.lookup_name_in_all_scopes(input)[0].symbol())

class SymbolResultTable(list):
    def __repr__(self):
        return '\n'.join(repr(sym) for sym in self)
        
class Symbol(long):
    def __new__(cls, symbol):
        new = super(Symbol, cls).__new__(cls, symbol.value())
        new.symbol = symbol
        return new
        
    @property
    def name(self):
        return self.symbol.name()
        
    @property
    def value(self):
        return self.symbol.value()
        
    @property
    def size(self):
        return self.symbol.size()
        
    def __repr__(self):
        return "name:%s value:0x%08X size:0x%X" % (self.name, self.value, self.size)
        
def get_symbols_string(device, address):
    if device.objfile:
        symbols = [Symbol(sym) for sym in device.objfile.symbols_at_address(address)]
        return '(%s)' % ', '.join(sorted([sym.name for sym in symbols])) if symbols else ''
    return ''

def get_source_string(device, address):
    if device.objfile:
        try:
            s = device.objfile.source_at_address(address)
        except pfile.ProgramFileError:
            return ''
        else:
            return ':'.join([s.filename(), str(s.line())])
    else:
        return ''

srec       = named('srec')
elf        = named('elf')
setpc      = named('setpc')
nosetpc    = named('nosetpc')
nobinary   = named('nobinary')
nosymbols  = named('nosymbols')
nowarnings = named('nowarnings')
showwarnings = named('showwarnings')
        
def get_file_type(filename, type):
    file_type = None
    if type == 'auto':
        ext = os.path.splitext(filename)[1]
        if ext:
            #Remove the '.', allow 'ELF' or 'elf'
            file_type = ext[1:].lower()
        else:
            raise UnknownFileTypeError("Unknown file type")
    else:
        file_type = type
        
    return file_type
    
def make_table(header, get_fn_name, items):
    t = table(header, [getattr(s, get_fn_name)() for s in items])
    return ['\n\n', t]
    
def make_section_table(header, items):
    rows = []
    for name, contains in [s.for_contains() for s in items]:
        contains = contains.split()
        
        rows.append([name, contains[0]])
        rows.extend([[' ', c] for c in contains[1:]])
    
    t = table(header, rows)
    return ['\n\n', t]
    
class ELFFileInfoResult(object):
    def __init__(self, file_type, pc, endian, arch, has_dwarf, elf_class, sections,
        show_sections, segments, show_segments):
        self.file_type     = file_type
        self.pc            = pc
        self.endian        = endian
        self.arch          = arch
        self.has_dwarf     = has_dwarf
        self.elf_class     = elf_class
        self.sections      = sections
        self.show_sections = show_sections
        self.segments      = segments
        self.show_segments = show_segments
        
    def __repr__(self):
        ret = [headerless_table([
        ['File type',    self.file_type],
        ['Entry point',  '0x%x' % self.pc],
        ['Endian',       str(self.endian)],
        ['Architecture', self.arch],
        ['Class',        '%s' % self.elf_class],
        ['Has DWARF',    str(self.has_dwarf)],
        ])]
        
        if self.segments and self.show_segments:
            ret.extend(make_table(
                    ['No.', 'Type', 'Virtual Addr', 'Physical Addr', 
                      'File Size', 'Mem Size', 'Flags', 'Align'],
                    'for_repr',
                    self.segments))
            
            ret.extend(make_section_table(['Segment', 'Sections'], self.segments))
        
        if self.sections and self.show_sections:
            ret.extend(make_table(
                    ['Name', 'Address', 'Type', 'Size (bytes)'],
                    'for_repr',
                    self.sections))
        
        return ''.join(ret)

secseg_types_map = {pfile.Section.Other:"Other",
		pfile.Section.Standard:"Standard",
		pfile.Section.Uninitialised:"Uninitialised",
		pfile.Section.SymbolTable:"SymbolTable",
		pfile.Section.StringTable:"StringTable",
		pfile.Section.Relocations:"Relocations",
		pfile.Section.Information:"Information",
		pfile.Section.Dynamic:"Dynamic",
		pfile.Section.Hash:"Hash",
		pfile.Section.DebugInfo:"DebugInfo",
		pfile.Section.Phdr:"Phdr",
		pfile.Section.Interpreter:"Interpreter"}

class ELFSectionInfo(object):
    def __init__(self, section):
        self.name    = section.name()
        self.address = section.virtual_address()
        self.type    = secseg_types_map[section.kind()]
        self.size    = section.size()
        
    def for_repr(self):
        return [self.name, '0x%0x' % self.address, self.type, str(self.size)]
        
class ELFSegmentInfo(object):
    def __init__(self, num, segment, sections):
        self.num           = num
        self.type          = segment.kind()
        self.virtual_addr  = segment.virtual_address()
        self.physical_addr = segment.physical_address()
        self.file_size     = segment.size()
        self.mem_size      = segment.memory_size()
        self.flags         = segment.attributes()
        self.align         = segment.alignment()
        self.contains = [s.name() for s in sections if segment.contains(s)]
                
    def for_contains(self):
        return [str(self.num), ' '.join(self.contains)]
    
    @property
    def flags_str(self):
        result = ""
        if self.flags & pfile.Section.Writeable:
            result += "W"
        if self.flags & pfile.Section.Allocatable:
            result += "A"
        if self.flags & pfile.Section.Executable:
            result += "X"
        return result
        
    def for_repr(self):
        format_hex = lambda x : '0x%0x' % x
        header_type = secseg_types_map[self.type]
        result = [str(self.num), header_type, format_hex(self.virtual_addr),
                format_hex(self.physical_addr), format_hex(self.file_size), 
                format_hex(self.mem_size), self.flags_str, format_hex(self.align)]
        return result
                
class SRECHexInfoResult(object):
    def __init__(self, file_type, pc):
        self.file_type = file_type
        self.pc = pc
        
    def __repr__(self):
        rows = [['File type', self.file_type]]
        
        pc_row = ['Entry point']
        if self.pc is not None:
            pc_row.append('0x%0x' % self.pc)
        else:
            pc_row.append('unknown')
        rows.append(pc_row)
        
        return headerless_table(rows)
        
class BinInfoResult(object):
    def __init__(self, file_type, size):
        self.file_type = file_type
        self.size = size
    
    def __repr__(self):
        return headerless_table([
            ['File type', self.file_type],
            ['Size',      '%d bytes' % self.size],
            ])
            
def get_elf_info(elf, show_sections, show_segments):
    sections = [ELFSectionInfo(section) for section in elf.sections()]
    segments = [ELFSegmentInfo(segn, segment, elf.sections()) for segn, segment in enumerate(elf.segments())]
    
    program_info = elf.program_info()
    return ELFFileInfoResult('elf',
                             elf.entry_point(), 
                             Endian.little if program_info.endian == 'little' else Endian.big,
                             program_info.architecture_ase,
                             program_info.has_debug_information, 
                             program_info.address, 
                             sections,
                             show_sections,
                             segments,
                             show_segments,
                            )
                            
def get_srec_hex_info(f, file_type):
    return SRECHexInfoResult(file_type, f.execution_address)
    
def get_bin_info(filename):
    return BinInfoResult('bin', os.path.getsize(filename))

def get_endian_address_info(device):
    try:
        da = device.da
    except AttributeError:
        return False, pfile.UseAddress.dont_care
    else:
        target_is_32 = dict(da.CpuInfo()).get('cpu_is_32bit', True)
        is_big_endian = da.GetEndian() == Endian.big
        using_addresses = pfile.UseAddress.dont_care
        if target_is_32:
            using_addresses = pfile.UseAddress.use_32bit
        else:
            using_addresses = pfile.UseAddress.use_64bit
        return is_big_endian, using_addresses
    
@command(device_required=False)
def progfileinfo(filename=None, show_sections=False, show_segments=False, type='auto', device=None):
    '''
    Show information about the current program file, or the file at the path 'filename'. 
    Set 'show_sections' and/or 'show_segments' to True to show tables of sections 
    and/or segments for an elf file.

    'type' may be set to prevent autodetection of the file type. One of 
    'srec', 'elf', 'bin', 'hex' or 'auto'.
    '''
    if filename is not None:
        try:
            _, using_addresses = get_endian_address_info(device)
            objfile =  pfile.load_program(filename, False, None, using_addresses)
            return get_elf_info(objfile, show_sections, show_segments)
        except pfile.ProgramFileError as e:
            raise e
        except pfile.NotAnELF:
            file_type = get_file_type(filename, type)
            if file_type in ['srec', 'hex', 'ihex']:
                with open(filename, 'r') as f:
                    f = parse_srec(f.read()) if file_type == 'srec' else parse_hex(f.read())
                    return get_srec_hex_info(f, file_type)
                        
            elif file_type == 'bin':
                return get_bin_info(filename)
            else: 
                raise FileExtNotSupportedError("File type '%s' not supported." % file_type)
    else:
        #Show last loaded file info
        require_device(device)

        if hasattr(device, 'objfile') and device.objfile:
            return get_elf_info(device.objfile, show_sections, show_segments)
        else:
            if device.progfile_info:
                return device.progfile_info
            else:
                raise RuntimeError('No program file loaded.')
    
class MemorySection(object):
    def __init__(self, address, data, name=None):
        self.address = address
        self.data    = data
        self.name    = name
        self.write_success = False
        
    def __nonzero__(self):
        return self.write_success
        
def _should_set_pc(setpc, load_binary, new_pc):
    return (setpc or (setpc is None and load_binary)) and new_pc is not None

@command(type=[namedstring(srec), namedstring(hex), namedstring(auto), 
               namedstring(elf), namedstring(bin)],
         verbose=verbosity,
         setpc=[(setpc, True), (nosetpc, False)],
         verify=[(verify, True), (noverify, False)],
         load_binary=[(nobinary, False)],
         load_symbols=[(nosymbols, False)],
         show_warnings=[(showwarnings, True), (nowarnings, False)]
        )
def load(filename, type='auto', verify=False, verbose=False, setpc=None, base_addr=None, 
    init_bss=True, load_binary=True, load_symbols=True, sign_extend_addr=False, physical=True,
    _use_sections=False, show_warnings=False, device=None):
    r'''Load a program file.
    
    ================= ==============================================================================
    Parameter         Meaning
    ================= ==============================================================================
    filename          The path to the file to be loaded. See note for details.
    type              Type of file to be loaded. 'srec', 'elf', 'bin', 'hex' or 'auto'.
    verify            If True data written will be read back and compared to the file's contents. If 
                      load_binary is False the write is skipped but the verify will still take 
                      place. 'verify' or 'noverify'.
    verbose           Set True to see progress messages during the load.
    setpc             If True set the PC to the file's entry address. Default value of None means 
                      set it only when load_binary is True. 'setpc' or 'nosetpc' can also be used.
    base_addr         Address to begin loading a binary file at. Only used with bin files.
    init_bss          If True the '.bss' and '.sbss' sections will be initialised.
    load_binary       If True binary data will be written to the target.
    load_symbols      If True symbols will be loaded from the file. Elf files only.
    sign_extend_addr  Set this True to enable loading of 32 bit elfs onto 64 bit targets by sign 
                      extending the addresses. (also applies to symbols from that elf)
    physical          Load using physical addresses rather than virtual addresses.
    show_warnings     Set True to show any warnings generated in the load.
    ================= ==============================================================================
        
    Python will treat back slash followed by certain characters as escape sequences, for example 
    load("C:\\foo\\trunk") becomes load("C:\\foo<tab>trunk")
    
    To avoid this, you can either double up all slashes, use the raw string prefix 'r', or 
    use forward slashes. For example::
    
      load("C:\\foo\\trunk")
      load(r"C:\foo\trunk")
      load("C:/foo/trunk")
    '''
    def log_progress(string):
        if verbose:
            print string
    
    #Don't leave the current file hanging around if this load fails.
    unload(device=device)

    #Intermediate list of address/sections to write to the target
    to_write = []

    file_type = type
    if file_type in ['auto', 'elf']:
        try:
            _, using_addresses = get_endian_address_info(device)
            objfile = pfile.load_program(filename, False, None, using_addresses)
            validate_elf_options(objfile, device, sign_extend_addr)
            device.objfile = objfile
            file_type = 'elf'

            if show_warnings:
                for warning in device.objfile.warnings():
                    print warning
        except pfile.ProgramFileError as e:
            raise e
        except pfile.NotAnELF:
            file_type = get_file_type(filename, type)

    if file_type == 'elf':
        #Set PC reg to the entry point
        new_pc = device.objfile.entry_point()
        if _should_set_pc(setpc, load_binary, new_pc):
            device.da.WriteRegister('pc', new_pc)
            
            log_progress("Set PC to 0x%08x" % new_pc)
            
        if load_symbols:
            device.objfile.load_symbols()
            
        if load_binary or verify:
            if _use_sections:
                to_write = elf_data_from_sections(device.objfile, init_bss)
            else:
                to_write = elf_data_from_segments(device.objfile, init_bss, physical)

    elif file_type in ['srec', 'hex', 'ihex']:
        with open(filename, 'r') as f:
            f = parse_srec(f.read()) if file_type == 'srec' else parse_hex(f.read())
            
            device.progfile_info = get_srec_hex_info(f, file_type)
            
            if _should_set_pc(setpc, load_binary, f.execution_address):
                device.da.WriteRegister('pc', f.execution_address)
                log_progress("Set PC to 0x%08x" % f.execution_address)
                
            if load_binary or verify:
                to_write = [MemorySection(section[0], section[1]) for section in f.sections]

    elif file_type == 'bin':
        if base_addr is None:
            raise LoadException('Base address (base_addr) required to load a bin file')
        
        device.progfile_info = get_bin_info(filename)
        
        if load_binary or verify:
            with open(filename, 'rb') as f:
                to_write.append(MemorySection(base_addr, f.read()))
    else:
        raise FileExtNotSupportedError("File type '%s' not supported." % file_type)

    breakpoints.suppress_all_bps(device)
    for mem_section in to_write:
        if mem_section.name and load_binary:
            log_progress("Writing section '%s'" % mem_section.name)
        mem_section.write_success = (write_data(mem_section.data, 
            mem_section.address, verify, verbose, device, do_write=load_binary))
        
    breakpoints.activate_all_bps(device)
    if not all(to_write):
        raise LoadException("A section did not verify correctly.")
        
def validate_elf_options(elf, device, sign_extend_addr):
    #Check 32/64 bit compatibility
    target_is_32 = dict(device.da.CpuInfo()).get('cpu_is_32bit', True)
    elf_is_32 = elf.program_info().address == '32bit'
    
    if target_is_32 and not elf_is_32:
        raise LoadException("A 64 bit elf is not compatible with a 32 bit target")
        
    if not target_is_32 and elf_is_32 and not sign_extend_addr:
        raise LoadException("Cannot load a 32 bit elf on a 64 bit target with sign_extend_addr False")
        
def elf_data_from_sections(elf, init_bss):
    to_write = []
    for section in elf.sections():
        sectype = section.kind()
        if ((sectype == pfile.Section.Standard) or (sectype == pfile.Section.Uninitialised)) and (section.size() > 0):
            if sectype == pfile.Section.Uninitialised:
                #Skip unless we need to init them
                if section.name() in ['.bss', '.sbss'] and init_bss:
                    #Set data to zeros
                    data = '\x00'*section.size()
                else:
                    continue
            else:
                data = ''.join(section.contents())
                
            address = section.virtual_address()
            to_write.append(MemorySection(address, data, name=section.name()))
    
    return to_write
    
def elf_data_from_segments(elf, init_bss, physical):
    to_write = []
    for segn, segment in enumerate(elf.segments()):
        if segment.kind() == pfile.Section.Standard:
            address = segment.physical_address() if physical else segment.virtual_address()
            
            data = ''.join(segment.contents())
            if init_bss:
                data += '\x00' * (segment.memory_size() - segment.size())
                
            name = 'segment%d' % (segn,)
            to_write.append(MemorySection(address, data, name=name))
            
    return to_write
                
def write_data(data, address, verify, verbose, device, do_write=True):
    def log_progress(string):
        if verbose:
            print string
            
    if not data:
        return True
            
    # although this is binary data, the DA seems to get byte access all wrong
    # so we will reinterpret the data as 32-bit words, which needs to be endian
    # sensitive
    
    #Mask used to set to 0s bytes which should be overwritten
    #E.g. a 3 byte overflow on big endian leaves the bottom byte, top byte on little
    #           0 byte (aligned) 1 byte      2 bytes      3 bytes
    masks_be = [None,            0x00ffffff, 0x0000ffff, 0x000000ff]
    masks_le = [None,            0xffffff00, 0xffff0000, 0xff000000]
    
    endian = device.da.GetEndian() == Endian.big
    
    #Check start address alignment
    underflow = address % 4
    if underflow:
        #First aligned address before the start address
        before_word_addr = address - underflow
        previous_word = device.da.ReadMemoryBlock(before_word_addr, 1, 4)[0]
        #Get the parts of the data that overlap that word
        underflow_word = data[:4-underflow]
        #Pad behind it with 0 to make a full word
        underflow_word = ''.join(['\x00']*underflow) + underflow_word
        
        #If the data was in the middle of a word add dummy bytes on the end
        #Allows us to align the start and end in one step. 
        added_bytes = 4-len(underflow_word)
        underflow_word += ''.join(['\x00']*added_bytes)

        #Unpack the word into a value in the target's endian
        underflow_word = struct_unpack(underflow_word, 4, endian)[0]
        
        mask = masks_le[underflow] if endian else masks_be[underflow]
        if added_bytes:
            #Special masks for values within a word, where being and end are misaligned
            alt_masks = {
                (True,  1, 1) : 0xFF0000FF,
                (False, 1, 1) : 0xFF0000FF,
                (True,  2, 1) : 0xFF00FFFF,
                (False, 2, 1) : 0xFFFF00FF,
                (True,  1, 2) : 0xFFFF00FF,
                (False, 1, 2) : 0xFF00FFFF,
            }
            mask = alt_masks[(endian, added_bytes, underflow)]
        
        #Mask out of the existing value the bytes which are in the new value
        underflow_word |= (previous_word & mask)
        #Re-pack it in target endian
        underflow_word = struct_pack([underflow_word], 4, endian)
        data = underflow_word + data[4-underflow:]
        
        #The new start address is aligned
        address = before_word_addr

    #Align the end of the data, start address is always aligned by this point
    overflow = len(data) % 4
    if overflow:
        #The last word that would be modified
        word_addr = address + len(data) - overflow
        last_word = device.da.ReadMemoryBlock(word_addr, 1, 4)[0]
        
        #Overflowing bytes from data
        overflow_word = data[-overflow:]
        #Pad to a word by adding 0s
        overflow_word += ''.join(['\x00']*(4-overflow))
        #Unpack in the target's endian
        overflow_word = struct_unpack(overflow_word, 4, endian)[0]
        
        mask = masks_be[overflow] if endian else masks_le[overflow]
        overflow_word |= (last_word & mask)
        #Re-pack that word in the target's endian
        overflow_word = struct_pack([overflow_word], 4, endian)
        #Remove overflow and add new full word to the data
        data = data[:-overflow] + overflow_word
    
    data  = struct_unpack(data, 4, endian)
    count = len(data)
    
    if do_write:
        device.da.WriteMemoryBlock(address, count, 4, data)
        log_progress("Wrote %d words to address 0x%08x" % (count, address))
    
    if verify:
        wrote = tuple(device.da.ReadMemoryBlock(address, count, 4))
        if wrote != data:
            print CompareResult(data, wrote, 4, address, address, 16, device.da.GetEndian(), line_limit=3)
            return False
        else:
            log_progress("Verification successful for memory at 0x%08x" % address)
            
    return True

@command()
def unload(device=None):
    '''
    Unload the current program file.
    Does nothing if there is no program file loaded.
    '''
    device.objfile = None
    device.progfile_info = None
    