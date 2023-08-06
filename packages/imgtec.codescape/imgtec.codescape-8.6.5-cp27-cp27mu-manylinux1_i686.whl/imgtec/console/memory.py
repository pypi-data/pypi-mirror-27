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
import itertools
          
def memory_dump_lines(data, size=4, bytes_per_line=16, endian=False, address=None, radix=16):
    bytes_per_line = max(size, bytes_per_line)
    elems_per_line = bytes_per_line // size
    bytedata = struct_pack(data, size, endian)
    formatter = get_formatter(radix, size)
    if radix == -10:
        data = struct_unpack(bytedata, size, endian, True)
        
    table = ''.join(chr(x) if 32<= x < 127 else '.' for x in range(256))
    bytedata = bytedata.translate(table)
    colwidth = elems_per_line * (len(formatter(0)) + 1)
    lines = []
    for offs in range(0, len(data), elems_per_line):
        line = ''
        if address is not None:
            line += '0x%08x ' % (address,)
            address += elems_per_line * size
        line += " ".join([formatter(x) for x in data[offs:offs+elems_per_line]]).ljust(colwidth)
        byte_offset = offs*size
        line += bytedata[byte_offset:byte_offset+bytes_per_line]
        #line += '.'.join(str(ord(x)) for x in bytedata[byte_offset:byte_offset+bytes_per_line])
        lines.append(line)
    return lines
    
def memory_dump(data, size=4, bytes_per_line=16, endian=False, address=None, radix=16):
    lines = memory_dump_lines(data, size, bytes_per_line, endian, address, radix)
    return "\n".join(lines)
                
class MemoryResult(list):
    """Like a list of int/long, but renders in a pretty form.

    >>> MemoryResult([0x1234, 0x43215678], 4, 16, endian=True)
    00001234 43215678                   ...4C!Vx
    >>> MemoryResult([0x1234, 0x43215678], 4, 16, endian=False)
    00001234 43215678                   4...xV!C
    >>> MemoryResult([0x1234, 0x43215678], 4, 16, radix=10)
          4660 1126258296                       4...xV!C
    >>> MemoryResult([0x1234, 0x43215678], 4, 16, radix=8)
          11064 10310253170                         4...xV!C
    >>> MemoryResult([0x12, 0x33, 0x44, 0x55], 1, 16)
    12 33 44 55                                     .3DU
    >>> MemoryResult([0x1234, 0x43215678], 4, 8, radix=2, endian=False)
    00000000000000000001001000110100 01000011001000010101011001111000 4...xV!C
    >>> MemoryResult([0x12, 0x33, 0x44, 0x55], 1, 16, address=0x1233)
    0x00001233 12 33 44 55                                     .3DU
    >>> MemoryResult([0x12, 0x33, 0x44, 0x55], 1, 16, address=0x1233, radix=10)
    0x00001233  18  51  68  85                                                 .3DU
    >>> MemoryResult([0x12, 0x7f, 0x80, 0xff], 1, 16, address=0x1233, radix=-10)
    0x00001233   18  127 -128   -1                                                             ....
    >>> MemoryResult([0x12, 0x33, 0x44, 0x55], 1, 16, address=0x1233, radix=-10)
    0x00001233   18   51   68   85                                                             .3DU
    >>> MemoryResult([0x1234, 0x43215678], 8, 16)[0]
    0x0000000000001234
    >>> '0x%x' % (MemoryResult([0x1234, 0x43215678], 4, 16)[0]+1,)
    '0x1235'
    """
    def __init__(self, values, size=None, bytes_per_line=None, address=None, endian=False, radix=16):
        super(MemoryResult, self).__init__([IntResult(x, radix, size) for x in values])
        self.bytes_per_line = bytes_per_line
        self.size = size
        self.address = address
        self.endian = endian
        self.radix = radix
        
    def __repr__(self):
        return memory_dump(self, self.size, self.bytes_per_line, 
                    endian=self.endian, address=self.address, radix=self.radix)
        

def get_isa_and_abi(isa, abi, address=None, device=None):
    """Convert 'auto' in isa and abi as appropriate.

    >>> get_isa_and_abi('mips32', 'auto')
    ('mips32', 'o32')
    >>> get_isa_and_abi('auto', 'auto')
    Traceback (most recent call last):
    ...
    RuntimeError: No probe is configured, please provide an isa, or use the probe command

    """
    if isa == 'auto':
        if not device:
            raise RuntimeError("No probe is configured, please provide an isa, or use the probe command")
        isa = device.tiny.GetCurrentISA(address)
    if abi == 'auto':
        if device:
            abi = device.tiny.GetABI()
        else:
            abi = 'n64' if '64' in isa else 'o32'
    return isa, abi


@command(isa=named_isas,
        update=updates)
def dasm(address=None, count=4, isa='auto', update=True, device=None):
    """Display memory as disassembled instructions.
    
    dasm keeps a static address as the default if no address is specified,
    if `update` is True (i.e. noupdate is not specified) then the dasm address
    is updated after each command so that the next line of memory may be viewed
    without entering another address.
    
    If the ISA is not explicitly specified then the current ISA will be 
    determined based on the capabilities of the core and the LSB of the DEPC.
    
    The ISA can be explicitly specified using the named parameters below.
    
    """
    if address is None:
        address = dasm.address or 'pc'
    address = eval_address(device, address)
    isa_mode = address & 1
    instructions = device.tiny.Disassemble(address, count, isa)
    if update:
        last = instructions if count is None else instructions[-1]
        dasm.address = last.address + last.size + isa_mode
    return instructions

@command(isa=named_isas, device_required=False)
def dasmbytes(address, bytes, isa='auto', abi='auto', device=None):
    r"""Display byte values as disassembled instructions.
    
    If there is a current device then `isa` and `abi` may be 'auto' in which 
    case the current ISA of the cpu, and the currently configured abi is used.
    
    If there is no current device then `isa` must be specified, valid values
    are listed in the help for :func:`isa` and :func:`abi`. If `abi` is not
    specified then 'o32' is used for MIPS targets.  The ISA can also be 
    explicitly specified using the named parameters below.
    
    The bytes should always be given in big endian order, the python standard
    library function struct.pack can help with this :: 
    
        >>> dasmbytes(0x80004010, '\x10\x00\x00\x01')
        0x80004010 10000001    b         0x80004018
        >>> import struct
        >>> dasmbytes(0x80004010, struct.pack('>L', 0x100000001), mips32)
        0x80004010 10000001    b         0x80004018
    
    """
    from imgtec.codescape import tiny
    isa, abi = get_isa_and_abi(isa, abi, address, device=device)
    address = eval_address(device, address)
    return tiny.DisassembleBytes(address, -1, isa, abi, bytes)
dasm_bytes = dasmbytes

class MemTestException(Exception):
    pass
    
class WrappedProgress(object):
    def __init__(self, per_word, verbose):
        from imgtec.console.firmware import make_progress
        self.perc = 0
        self.per_word = per_word
        self.verbose = verbose
        self.progress = make_progress() if self.verbose else None
        
    def add_message(self, msg):
        if self.progress:
            self.progress.add_message(msg)
        
    def inc_percentage(self):
        if self.progress:
            self.perc += self.per_word
            self.progress.set_percentage(self.perc)
            
    def set_percentage(self, perc):
        if self.progress:
            self.progress.set_percentage(perc)
            
    def __enter__(self):
        return self
        
    def __exit__(self, *args):
        if self.progress:
            self.progress.__exit__()
        
@command(verbose=verbosity,)
def memtest(section_begin, words, memory_type=0, data_test=True, addr_test=True, device_test=True, verbose=True, device=None):
    '''
    Verify that the memory starting at section_begin is working correctly. 
    It will stop at the first failure so you can assume that all previous tests
    passed.
    
    =============== ============================================================
    Parameter       Meaning
    =============== ============================================================
    section_begin   The start address of the section of memory to test.
    words           Number of words of memory to test.
    memory_type     Type of memory to test. (default 0)
    data_test       If True, run the data test. This individually writes each 
                    bit of the value at each address. Checking that only the
                    correct bit is set each time.
    addr_test       If True, run the address test. This fills the section with a
                    known value then writes a single address with a different 
                    value and reads the section back to confirm only that 
                    address has changed. This is repeated for each address in
                    the section.
    device_test     If True, run the device test. This writes and verifies a 
                    value and then its inverse value, to each address in turn.
    verbose         Set True to see progress messages during the tests. The
                    percentage shown is for the overall command, not the 
                    current test.
    =============== ============================================================
    '''
    per_word = (1/float((addr_test, device_test, data_test).count(True)*words))*100
    
    with WrappedProgress(per_word, verbose) as prog:
        #Check that a value sent to a single address is received correctly
        if data_test:
            prog.add_message("Beginning data test")
            memtest_values(section_begin, words, memory_type, device, prog)
            prog.add_message("Data test passed")
            
        #Check that a value sent to a specific address goes to that addr and that addr only
        if addr_test:
            prog.add_message("Beginning address test")
            memtest_addresses(section_begin, words, memory_type, device, prog)
            prog.add_message("Address test passed")

        #Check that all the bits at addresses in the range work
        if device_test:
            prog.add_message("Beginning device test")
            memtest_values_at_addresses(section_begin, words, memory_type, device, prog)
            prog.add_message("Device test passed")
            
        prog.add_message("All tests passed")
        prog.set_percentage(100)
        
def memtest_percentage(words, max_percentage):
    perc_per = int((1/float(words))*max_percentage)
    perc = 0
    while words:
        words -= 1
        perc += perc_per
        yield perc
    
def memtest_values_at_addresses(section_begin, words, memory_type, device, progress, memory_unit=4):
    '''
    Write a value, then the opposite of a value to each address.
    Memory unit will always be 4 for the time being.
    '''
    
    section_end = section_begin + (words*4)
    
    initial      = 0xAAAAAAAA
    opp_initial  = 0x55555555
    
    for i in range(memory_unit//4):
        initial     |= (0xAAAAAAAA << (32*i))
        opp_initial |= (0x55555555 << (32*i))
    
    for address in range(section_begin, section_end, memory_unit):
        for value in [initial, opp_initial]:
            #Write value
            device.tiny.WriteMemoryBlock(address, 1, memory_unit, [value], memory_type)
            #Read back
            read = device.tiny.ReadMemoryBlock(address, 1, memory_unit, memory_type)[0]
            #Check that they are equal
            if read != value:
                raise MemTestException('Should have written 0x%x to address 0x%x but wrote 0x%x instead' % (value, address, read))

        progress.inc_percentage()
        progress.add_message("Value at address test: 0x%x passed" % address)
    
def memtest_addresses(section_begin, words, memory_type, device, progress):
    '''
    Fill the range with a fixed value, then write the opposite to a single address.
    Read the block back and make sure there is only one instance of that value, 
    and that it is at the expected address. Repeat until the end of the block.
    Assumes that values and the bits in each word work correctly.
    '''
    
    section_end = section_begin + (words*4)
    
    #Make sure addresses don't overlap
    initial     = 0xAAAAAAAA
    opp_initial = 0x55555555
    
    for address in range(section_begin, section_end, 4):
        #Write the initial value to all the locations we're interested in
        device.tiny.WriteMemoryBlock(section_begin, words, 4, [initial]*words, memory_type)
        
        #Write the opposite value to the address
        device.tiny.WriteMemoryBlock(address, 1, 4, [opp_initial], memory_type)
        
        #Read the whole block back
        block = device.tiny.ReadMemoryBlock(section_begin, words, 4, memory_type)
        
        #Look for indexes of words set to opp_initial
        found = []
        for item, index in zip(block, itertools.count()):
            effective_addr = (index*4)+section_begin
            if item == opp_initial:
                found.append(effective_addr)
                
        error_str = "Should have written to address 0x%x " % address
        
        if len(found) == 1 and address in found:
            pass
        elif not found:
            error_str += 'but did not'
            raise MemTestException(error_str)
        else:
            error_str += 'but instead wrote to '
            error_str += ', '.join(['0x%x' % addr for addr in found])
            raise MemTestException(error_str)
        
        progress.inc_percentage()
        progress.add_message("Address test: 0x%x passed" % address)
             
def memtest_values(section_begin, words, memory_type, device, progress):
    '''
    Write an incrementing number to a single address and read to back 
    to compare. Assumes that addressing and all the bits in the word work.
    '''
    
    #Test that values sent are the same ones that reach the memory
    
    section_end = section_begin + (words*4)
    for address in range(section_begin, section_end, 4):
        for i in range(0, 32):
            value = 1 << i
            device.tiny.WriteMemoryBlock(section_begin, 1, 4, [value], memory_type)
            read = device.tiny.ReadMemoryBlock(section_begin, 1, 4, memory_type)[0]
            
            if value != read:
                raise MemTestException("Failed to write value 0x%x to address 0x%x (wrote 0x%x but read back 0x%x)" % (value, address, value, read))

        progress.inc_percentage()
        progress.add_message("Data test: 0x%x passed" % address)
            
class CopyException(Exception):
    pass

@command(verify=[(verify, True), (noverify, False)])
def copy(source_begin, source_end, dest, size=4, verify=False, line_limit=None, memory_type=0, device=None):
    '''
    Copy the memory in the range source_begin to source_end, to the address dest. 
    
    =============== =========================================================================
    Parameter       Meaning
    =============== =========================================================================
    source_begin    Start of source address range
    source_end      End of source address range
    dest            Address to copy to
    size            Element size to use for the copy. 1, 2 or 4, default of 4.
    verify          Verify memory was copied correctly.
    line_limit      The maximum number of differing sequential lines to show 
                    in the event of a verify failure.
    memory_type     Type of memory to copy, defaults of 0.
    =============== =========================================================================
    '''
    if source_end < source_begin:
        raise CopyException("End source address precedes start source address")
    
    elem_count = int((source_end-source_begin)//size)
    read = device.tiny.ReadMemoryBlock(source_begin, elem_count, size, memory_type)
    device.tiny.WriteMemoryBlock(dest, elem_count, size, read, memory_type)
    
    if verify:
        wrote = device.tiny.ReadMemoryBlock(dest, elem_count, size, memory_type)
        return CompareResult(wrote, read, size, source_begin, dest, 16, device.tiny.GetEndian(), line_limit=line_limit)
        
class CompareException(Exception):
    pass
            
@command()
def compare(block_one, block_two, block_one_end=None, size=4, memory_type=0, bytes_per_line=16, line_limit=None, device=None):
    '''
    Compare two blocks of memory.
    
    =============== ============================================================
    Parameter       Meaning
    =============== ============================================================
    block_one       The start address of the first memory block, or a list of 
                    values.
    block_two       The start address of the second memory block, or a list of 
                    values.
    block_one_end   The end address of the first memory block. Only required 
                    if block_one is an address.
    size            Element size to use for the read. 1, 2 or 4, default of 4.
                    Only required when one of block_one and block_two are
                    addresses.
    memory_type     Type of memory to compare, defaults of 0.
    bytes_per_line  Bytes per line of the results.
    line_limit      The maximum number of differing sequential lines to show 
                    in the result. None means there is no limit.
    =============== ============================================================
    '''
    
    final_block_one  = None
    final_block_two  = None
    addr_one   = None
    addr_two   = None
    elem_count = None
    
    #block_one and block_two may be addresses, lists or MemoryResults (also a list)
    if isinstance(block_one, (int, long)):
        #section_one is an address therefore section_one_end must also be
        if block_one_end is None:
            raise CompareException("Block one end address required when its start address is given")
        if block_one_end < block_one:
            raise CompareException("Block one end address precedes its start address")
            
        #Number of elements to read
        elem_count = int((block_one_end-block_one)//size)   
    
        #Read from memory
        final_block_one = device.tiny.ReadMemoryBlock(block_one, elem_count, size, memory_type)
        addr_one  = block_one
        
    elif isinstance(block_one, MemoryResult):
        #Use it directly
        final_block_one = block_one
        #Take our size from the memory result instead of params
        size = block_one.size
        #And then use the address from the MemoryResult
        addr_one = final_block_one.address
        
    else:
        #Otherwise it's a list or MemoryResult and we'll use the size given in params
        final_block_one = block_one
        addr_one = None
        
    if isinstance(block_two, (int, long)):
        #section_two must be an address
        
        #If section_one was an address we won't know the element count yet
        if elem_count is None:
            #Assume that each item in section_one is an element
            elem_count = len(block_one)
    
        #Read section two from memory
        final_block_two = device.tiny.ReadMemoryBlock(block_two, elem_count, size, memory_type)
        addr_two = block_two
        
    elif isinstance(block_two, MemoryResult):
        #Check that the size matches the size we got from section_one/params
        if block_two.size != size:
            #Not sure what to do here so except for the time being
            raise CompareException("Block two element size (%d) does not match block one's element size (%d).")
            
        #Otherwise use it directly
        final_block_two = block_two
        #And then use the address from the MemoryResult
        addr_two = final_block_two.address
    else:
        #Must be another list
        final_block_two = block_two
        addr_two = None

    return CompareResult(final_block_one, final_block_two, size, addr_one, addr_two, bytes_per_line, device.tiny.GetEndian(), line_limit)

class CompareResult(object):
    def __init__(self, block_one, block_two, size, address_one, address_two, bytes_per_line, endian, line_limit=None):
        self.string_result, self.match = do_compare([block_one, block_two], size, [address_one, address_two], bytes_per_line, endian, line_limit)
        
    def __repr__(self):
        return self.string_result
        
    def __nonzero__(self):
        return self.match

class CompareListResult(list):
    def __init__(self, block_one, block_two, size, address_one, address_two, bytes_per_line, endian, line_limit=None):
        #block_two is a MemoryResult
        list.__init__(self, block_two)
        self.block_two = block_two
        self.string_result, self.match = do_compare([block_one, block_two], size, [address_one, address_two], bytes_per_line, endian, line_limit)
        
    def __repr__(self):
        return repr(self.block_two) if self.match else self.string_result

class CompareNumberResult(long):
    def __new__(cls, block_one, block_two, size, address_one, address_two, bytes_per_line, endian, line_limit=None):
        #block_two is an IntResult
        new = super(CompareNumberResult, cls).__new__(cls, block_two)
        new.int_res = block_two
        new.string_result, new.match = do_compare([block_one, [block_two]], size, [address_one, address_two], bytes_per_line, endian, line_limit)
        return new

    def __repr__(self):
        return repr(self.int_res) if self.match else self.string_result

class ReadModWriteResult(object):
    def __init__(self, was, then, now, size, address, endian):
        blocks, names = [was, now], ['was', 'now']
        if then:
            blocks.insert(1, then)
            names.insert(1, 'then')
        diffs = [(0, len(was), 0)]
        lines = render_differences(diffs, blocks, size, [address]*len(blocks), 16, endian, names=names)
        self._str = '\n'.join(lines)
        self.was = was
        self.then = then
        self.now = now

    def __repr__(self):
        return self._str


def do_compare(blocks, size, addresses, bytes_per_line, endian, line_limit=None, names=None):
    if names is None:
        names = ['+', '-']
    lines = []
    
    assert len(blocks) == len(addresses)
    bytes_per_line = max(size, bytes_per_line)
    
    #If there are no addresses assume 0x00 so you can see at what point the diff occurs
    #but don't print it in output messages.
    addr_real = [addr is not None for addr in addresses]
    addresses = [addr or 0 for addr in addresses]
    blocks    = [tuple(block) for block in blocks]
    
    #Check for a size mismatch
    maxlen = min(len(block) for block in blocks)
    if len(blocks[0]) > len(blocks[1]):
        lines.append("First memory block is larger than the second, comparing until the end of the second block.")
    elif len(blocks[1]) > len(blocks[0]):
        lines.append("Second memory block is larger than the first, comparing until the end of the first block.")
    elif not all(len(block) == maxlen for block in blocks):
        longer = ['#%d' %(n,) for n, block in enumerate(blocks, 1) if len(block) > maxlen]
        lines.append("Blocks %s are larger than the shortest block, comparing until the end of the shortest block." % (longer,))
        
    #Build a list of diff ranges, where a range is (start index, end index, lines beyond limit)
    diffs = []
    temp_start = None
    temp_end = None
    temp_lines = 0
    elements_per_line = bytes_per_line/size
    
    line_differ = _make_line_differ(len(blocks))

    for n in xrange(0, maxlen, elements_per_line):
        #Keep groups of contiguous lines together
        end_line = n + elements_per_line
        blk_lines = [block[n:end_line] for block in blocks]        
        end_diff = False       
        
        # compare line by line but using the values                
        # If not the same start a new diff range or expand the existing one
        if line_differ(blk_lines):
            temp_lines += 1
            
            if temp_start is None:
                temp_start = n
            
            #Only move the end index if we're below the line limit
            if line_limit is None or temp_lines <= line_limit:
                temp_end = maxlen if end_line > maxlen else end_line
                    
            #Always end the range if we've reached the end of the block, regardless of limit
            if end_line >= maxlen:
                end_diff = True
        else:
            #Stop any current range as this line was the same
            end_diff = True
        
        if end_diff and temp_start is not None:
            #Finish a range and add it to main list
            overflow = 0 
            if line_limit is not None and temp_lines > line_limit:
                overflow = temp_lines - line_limit
            diffs.append((temp_start, temp_end, overflow))
            temp_start = None
            temp_end   = None
            temp_lines = 0
            
    def message(msg):
        if all(addr_real):
            if all(addr == addresses[0] for addr in addresses):
                lines.append("The blocks at 0x%08x %s" % (addresses[0], msg))
            else:
                hexaddrs = ' and '.join('0x%08x' % a for a in addresses)
                lines.append("The blocks at %s %s" % (hexaddrs, msg))
        else:
            lines.append("The blocks %s" % (msg,))
            
    match = not diffs
    if diffs:
        message('do not match')
        lines.extend(render_differences(diffs, blocks, size, addresses, bytes_per_line, endian, line_limit=line_limit, names=names))
    else:
        message('match')
    return '\n'.join(lines), match
    
def render_differences(diffs, blocks, size, addresses, bytes_per_line, endian, line_limit=None, names=None):
    if names is None:
        names = ['+', '-']
    lines = []
    names = names + ['']  # for the ^^^ diff row
    maxname = max(len(n) for n in names)
    names = [n.ljust(maxname) for n in names]
    if line_limit != 0:
        #Build memory results out of the diff pairs to show the output of the comparison
        for diff in diffs:
            # The difference of end_i and start_ is always equal to or less than the element limit
            # so nothing is rendered for no reason.
            s, e, overflow_lines = diff
            address_offset = s*size
            
            addr0  = addresses[0] + address_offset
            compare_lines = [memory_dump_lines(block[s:e], size, bytes_per_line, endian, addr0) for block in blocks]
            
            #Now make a version of block 2+ with their own addresses for display
            display_lines = [compare_lines[0]]
            for address, block in zip(addresses[1:], blocks[1:]):
                display_lines.append(memory_dump_lines(block[s:e], size, bytes_per_line, endian, address + address_offset))
                            
            lines.extend(_get_diff_output(names, compare_lines, display_lines))
            
            if overflow_lines:
                #Might be odd to say number of lines? perhaps this limit should be elements
                lines.append('%d line(s) after those above had differences\n' % overflow_lines)
    return lines
    
def _make_line_differ(N):
    # I did have a non-eval based version using any() but the performance was
    # about x100 worse.  This version unrolls the loop for the number of blocks
    return eval("lambda lines:not %s" % (
                    ' == '.join('lines[%d]' % n for n in range(N)),
                ))

def _line_differ(blocks):
    '''    
    >>> _line_differ([[0, 1], [1, 1], [1, 1]])
    True
    >>> _line_differ([[1, 1], [1, 1], [1, 1]])
    False
    '''
    return _make_line_differ(len(blocks))(blocks)
    
def _make_char_differ(N):
    # I did have a non-eval based version using any() but the performance was
    # about x100 worse.  This version unrolls the loop for the number of strings
    return eval("lambda strings:''.join([' ^'[%s] for %s in zip(*strings)])" % (
                    ' or '.join('c0 != c%d' % n for n in range(1, N)),
                    ', '.join('c%d' % n for n in range(N))))
   
def _char_diff(*strings):
    '''
    >>> _char_diff('abc', 'aBc')
    ' ^ '
    >>> _char_diff('abc', 'aBc', 'ayZ')
    ' ^^'
    '''
    return _make_char_differ(len(strings))(strings)
    
def _get_diff_output(names, compare_lines, display_lines):
    r'''
    
    >>> x =_get_diff_output('+- ', [['abcdef', 'uvwxyz'], ['abCDef', 'uvWXyz']],
    ...                            [['123456', '..++..'], ['123456', '--##--']])
    >>> print '\n'.join(x)
    + 123456
    - 123456
        ^^
    + ..++..
    - --##--
        ^^
    >>> x =_get_diff_output('+- ', [['abcdef', 'uvwxyz'], ['abcdef', 'uvwxyz']],
    ...                            [['123456', '..++..'], ['123456', '--##--']])
    >>> print '\n'.join(x)
    + 123456
    - 123456
    + ..++..
    - --##--
    '''
    differ = _make_char_differ(len(compare_lines))
    diff_lines = []
    for line, xlines in enumerate(zip(*compare_lines)):
        chardiff = differ(xlines).rstrip()
        for name, display in zip(names, display_lines):
            diff_lines.append('%s %s' % (name, display[line]))
        if chardiff:
            diff_lines.append('%s %s' % (names[-1], chardiff))
    return diff_lines

def _get_mem_address(cmd, address):
    if address is None:
        address = cmd.address
        if address is None:
            raise RuntimeError("No previous address to continue")
    return address

class VerifyException(Exception):
    def __init__(self, res):
        Exception.__init__(self)
        self.res = res

    def __str__(self):
        return repr(self.res)

def generic_memory(device, cmd, address, values, count, size, type, radix, bytes_per_line, endian, verify, update, line_limit=None):
    address = _get_mem_address(cmd, address)
    address = eval_address(device, address)
    to_write = None
    xcount = count
    devendian = device.tiny.GetEndian()
    bendian = {'little':False, 'big':True, 'auto':devendian}[endian]

    is_values_a_list = False
    if values is not None:
        try:
            len(values)
            is_values_a_list = True
        except TypeError:
            values = [values]  # for the single value case
        if count is None:
            to_write = values
        else:
            to_write = list(itertools.islice(itertools.cycle(values), count))
        to_write = negative_to_2s_complement(to_write, size)
        count = len(to_write)
        if endian != 'auto' and bendian != devendian:
            to_write = swap_endian(to_write, size)
        device.tiny.WriteMemoryBlock(address, count, size, to_write, type)
    elif count is None:
        count = 1

    if verify or to_write is None:
        values = list(device.tiny.ReadMemoryBlock(address, count, size, type))

        if update:
            cmd.address = address + count * size

        #Only swap for reads not writes
        if endian != 'auto' and bendian != devendian and to_write is None:
            values = swap_endian(values, size)

        int_res = None
        mem_res = None
        if xcount is None and not is_values_a_list:
            int_res = IntResult(values[0], radix, size)
        else:
            mem_res = MemoryResult(values, size, bytes_per_line, address, bendian, radix)

        if to_write is not None:
            if int_res is not None:
                res = CompareNumberResult(to_write, int_res, size, address, address, bytes_per_line, bendian, line_limit=line_limit)
            else:
                res = CompareListResult(to_write, mem_res, size, address, address, bytes_per_line, bendian, line_limit=line_limit)

            if verify == 2 and values != list(to_write):
                raise VerifyException(res)
            else:
                return res

        return int_res if int_res is not None else mem_res
        
@command(radix=radixes, aliases='size1', endian=endians, update=updates, verify=verifies)
def byte(address=None, values=None, count=None, type=0, radix=16, bytes_per_line=16, line_limit=3, endian='auto', verify=True, update=True, device=None):
    """Read and write memory.
    
    These commands read or write memory. With no values argument (or for the dump command), the 
    commands display `count` memory items of the given size covering [addr, addr+count*size).
    
    If values is given then the items in the list are written to memory starting at the specified 
    address.  If `count` is given and larger than the length of `values`, then items in 
    the list are repeated to cover the range. If `count` is not None then at most `count` 
    elements are written, even if the `values` list contains more items.

    Negative values will be converted into their equivalent 2s complement value for the size 
    being used. This means that for a byte the value range is 255 (0xff) to -128 (0x80).
    
    The probe always updates the instruction and data caches when memory is written 
    through the debugger.
    
    =============== =========================================================================
    Parameter       Meaning
    =============== =========================================================================
    bytes_per_line  The number of bytes per row, and is analogous to the col param in NavCon.
    line_limit      The maximum number of differing sequential lines to show 
                    in the event of a verify failure.
    radix           Can be 2, 8, 10, -10 or 16.
    endian          Byte order of the access. 'little', 'big', or 'auto'.
    size            dump only - element size of access and display.
    verify          If True the memory read back will be compared 
    =============== =========================================================================
    
    Most of these parameters have named parameters detailed below.
    
    >>> dump('pc')
    0x87fe76f8 26100001 1440fff9 304400ff 8fbf001c &....@..0D......
    >>> dump.bytes_per_line = 24
    >>> dump('pc', count=6)
    0x87fe76f8 26100001 1440fff9 304400ff 8fbf001c 8fb00018 03e00008 &....@..0D..............
    >>> dump.radix=-10    # signed decimal
    >>> dump('pc', big, count=6)
    0x87fe76f8   638582785   339804153   809763071 -1883308004 -1884291048    65011720 &.
    >>> dump('pc', big, count=4, bytes_per_line=16)
    0x87fe76f8   638582785   339804153   809763071 -1883308004 &....@..0D......        
    >>> hex(dump('pc')[0]+4)
    '0x40024804L'
                
    .. note::
        
        The NavCon options: addr, noaddr, noformat are not implemented in Codescape Console, 
        this is because the memory commands actually return a list of integers with a special 
        __repr__ method to format nicely.  Thus the list can be indexed as a normal python list.
        
   
    """
    # TODO add the endian aliases 
    # There are aliases available:
    #The halfword_le aliases "halfword little", reading and writing memory in little endian regardless of the processor state.
    #The halfword_be aliases "halfword big", reading and writing memory in big endian regardless of the processor state.
    #The word_le aliases "word little", reading and writing memory in little endian regardless of the processor state.
    #The word_be aliases "word big", reading and writing memory in big endian regardless of the processor state.
    return generic_memory(device, byte, address, values, count, 1, type, radix, bytes_per_line, endian, verify, update, line_limit)
size1=byte

@command(radix=radixes, endian=endians, aliases='half size2', update=updates, verify=verifies, see='byte')
def halfword(address=None, values=None, count=None, type=0, radix=16, bytes_per_line=16, line_limit=3, endian='auto', verify=True, update=True, device=None):
    return generic_memory(device, halfword, address, values, count, 2, type, radix, bytes_per_line, endian, verify, update, line_limit)
half = halfword
size2 = halfword

@command(radix=radixes, endian=endians, aliases='size4', update=updates, verify=verifies, see='byte')
def word(address=None, values=None, count=None, type=0, radix=16, bytes_per_line=16,line_limit=3, endian='auto', verify=True, update=True, device=None):
    return generic_memory(device, word, address, values, count, 4, type, radix, bytes_per_line, endian, verify, update, line_limit)
size4 = word

@command(radix=radixes, endian=endians, aliases='size8', update=updates, verify=verifies, see='byte')
def doubleword(address=None, values=None, count=None, type=0, radix=16, bytes_per_line=16, endian='auto', verify=True, update=True, device=None):
    return generic_memory(device, doubleword, address, values, count, 8, type, radix, bytes_per_line, endian, verify, update)
size8 = doubleword

@command(radix=radixes, endian=endians,
         size=[(byte, 1), (halfword, 2), (word, 4), (doubleword, 8)],
         update=updates, 
         see='byte')
def dump(address=None, count=4, size=4, type=0, radix=16, bytes_per_line=16, endian='auto', update=True, device=None):
    return generic_memory(device, dump, address, None, count, size, type, radix, bytes_per_line, endian, False, update)


@command()
def wordmodify(address, newvalue, mask, count=1, memtype=0, _restore=False, device=None):
    '''Perform a read mod write operation of one or more words in memory.
    
    This is equivalent to::
    
        values = word(address, count=count)
        values = [(x & ~modify_mask) | (new_value & modify_mask) for x in values]
        word(address, values)

    '''
    ops = ['=', 'new_values', 'old_values']
    if _restore : 
        ops.append('restore')
    old, new = device.tiny.ReadModWrite(address, newvalue, mask, ','.join(ops), count, memtype)
    if _restore:
        now = word(address, count=count)
        return ReadModWriteResult(old, new, now, 4, address, device.tiny.GetEndian())
    return ReadModWriteResult(old, None, new, 4, address, device.tiny.GetEndian())


@command()
def asid(asid=None, device=None):
    '''Get or Set the active ASID used for accessing memory.
    
    If the active ASID is -1 then the 'current' ASID will be used, on MIPS 
    this is the value currently in the register entryhi.
    
    ``asid()`` can also be used in a with block, so that the old active asid is
    automatically restored::
    
        with asid(1):
            word(0x200000000) # read word using asid 1
        word(0x200000000) # read word using previous asid
        
    '''
    from imgtec.console.generic_device import update_prompt
    old = device.tiny.GetActiveASID()
    if asid is not None:
        def set_asid(new_asid):
            device.tiny.SetActiveASID(new_asid)
            update_prompt()
        set_asid(asid)
        return NoneGuard(set_asid, old)
    return old
        

if __name__ == '__main__':
    import doctest
    doctest.testmod()