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

from imgtec.console.support import struct_pack

class HexFileException(Exception):
    pass
    
class HexFile(object):
    def __init__(self):
        #Data records only, with offsets applied
        self.sections = []
        #PC value
        self.execution_address = None

def parse_hex(data):
    r"""
    Make a HexFile object from the given data. 
    Access data records through .data_records,
    the address offsets are already applied.
    
    >>> foo = parse_hex('''\
    ... :02000004800278
    ... :10001000101112131415161718191a1b1c1d1e1f68''')
    Traceback (most recent call last):
    ...
    HexFileException: No end of file record found
    >>> foo = parse_hex('''\
    ... :02000004800278
    ... :10001000101112131415161718191a1b1c1d1e1f68
    ... :00000001ff
    ... :0200000280205c''')
    Traceback (most recent call last):
    ...
    HexFileException: End of file record is not the last line of the file
    >>> foo = parse_hex('''\
    ... :00000001ff
    ... 
    ... ''')
    >>> foo = parse_hex('''\
    ... :02000004800278
    ... :0800100010111213141516174c
    ... :0200000280205c
    ... :10002000101112131415161718191a1b1c1d1e1f58
    ... :04000005004000981F
    ... :00000001ff''')
    >>> len(foo.sections)
    2
    >>> '0x%08x' % foo.sections[0].addr
    '0x80020010'
    >>> [hex(ord(c)) for c in foo.sections[0].contents]
    ['0x10', '0x11', '0x12', '0x13', '0x14', '0x15', '0x16', '0x17']
    >>> hex(foo.sections[1].addr)
    '0x80220'
    >>> hex(foo.execution_address)
    '0x400098'
    """
    hex_file = HexFile()
    
    #Parse each line into a record object
    curr_offset    = 0x00
    has_eof_record = False
    
    for line in data.splitlines():
        record = parse_record(line)
        
        #There must only be one EOF record, and it must be the last record in the file
        if has_eof_record and record != None:
            raise HexFileException("End of file record is not the last line of the file")
        
        #Data record (type 00)
        if hasattr(record, 'contents'):
            #Add address offset
            record.addr += curr_offset
            #Add to list of data records
            hex_file.sections.append(record)
            
        #Address extension records (types 02 and 04)
        elif hasattr(record, 'ext_addr'):
            #Assuming that extensions from extended segment and extended linear 
            #records do not combine, but overwrite each other instead
            curr_offset = record.ext_addr
            
        #End of file record
        elif hasattr(record, 'start_addr'):
            #Don't stop processing, because the eof record may not be in the correct place
            #Just note that one was found.
            has_eof_record = True
            
        #Start linear address record
        elif hasattr(record, 'eip'):
            #This is what the PC should be set to
            hex_file.execution_address = record.eip
            
    #If no end of file record was found
    if not has_eof_record:
        raise HexFileException("No end of file record found")
            
    return hex_file
        
class DataRecord(object):
    def __init__(self, contents, addr):
        #A list of byte values
        self.contents = contents
        #The address to which they should be written
        self.addr     = addr
    def __getitem__(self, key):
        return self.contents if key == 1 else self.addr
        
def parse_data_record(bytes):
    """
    Data records include an address and data to be written to that address.
    This address may be extended, but this is not done in this function.
    Reading variables by index is supported to emulate the srec interface.
    
    >>> foo = parse_data_record([0x04, 0xFE, 0xDC, 0x00, 0x11, 0x22, 0x33, 0x44, 0xFF])
    >>> hex(foo.addr)
    '0xfedc'
    >>> hex(foo[0])
    '0xfedc'
    >>> [hex(ord(c)) for c in (foo.contents)]
    ['0x11', '0x22', '0x33', '0x44']
    >>> [hex(ord(c)) for c in foo[1]]
    ['0x11', '0x22', '0x33', '0x44']
    """

    #Assuming that the checksum is still present
    data_bytes = bytes[4:-1]
    #Stored as a packed string
    data_bytes = struct_pack(data_bytes, 1, False)
        
    #This needs to use the last offset also
    addr = (bytes[1] << 8) | bytes[2]
    
    return DataRecord(data_bytes, addr)
        
class EOFRecord(object):
    def __init__(self, start_addr):
        self.start_addr = start_addr
        
def parse_eof_record(bytes):
    """
    The end of file record appears once at the end of the file.
    The address was/may be used to set the program's start address.
    
    >>> foo = parse_eof_record([0x00, 0xAB, 0xCD, 0x01, 0xFF])
    >>> hex(foo.start_addr)
    '0xabcd'
    """
        
    #Usually set to 0
    start_addr = (bytes[1] << 8) | bytes[2]
        
    return EOFRecord(start_addr)
    
class ExtendedSegmentAddressRecord(object):
    def __init__(self, ext_addr):
        self.ext_addr = ext_addr
    
def parse_extended_segment_addr_record(bytes):
    """
    Extended segment address records extend the 16 bit addresses in data records.
    The extension is shifted left by 4 then added to all subsequent data records.
    The last significant hex digit must be 0. E.g. 0xffe0 or 0xabc0.
    
    >>> parse_extended_segment_addr_record([0x02, 0x00, 0x00, 0x2, 0xFF, 0xEE, 0xFF])
    Traceback (most recent call last):
    ...
    HexFileException: Least significant nibble of extended segment address (0xffee) is non zero
    >>> foo = parse_extended_segment_addr_record([0x02, 0x00, 0x00, 0x02, 0xFF, 0xE0, 0xFF])
    >>> '0x%x' % foo.ext_addr
    '0xffe00'
    >>> foo = parse_extended_segment_addr_record([0x02, 0x00, 0x00, 0x02, 0x80, 0x20, 0x78])
    >>> '0x%x' % foo.ext_addr
    '0x80200'
    """
   
    #The contents of the record are an address extension
    ext_seg_addr = (bytes[4]<<8)|bytes[5]
    
    #The least significant digit of which should be 0
    if (ext_seg_addr & 0xF) != 0:
        raise HexFileException("Least significant nibble of extended segment address (0x%04x) is non zero" % ext_seg_addr)
    
    ext_seg_addr <<= 4
    
    return ExtendedSegmentAddressRecord(ext_seg_addr) 
    
class StartSegmentAddressRecord(object):
    def __init__(self, cs, ip):
        self.cs = cs
        self.ip = ip
        
def parse_start_segment_addr_record(bytes):
    """
    Not exactly sure what this does (if anything) on MIPS.
    "For 80x86 processors, it specifies the initial content of the CS:IP registers."
    
    >>> foo = parse_start_segment_addr_record([0x04, 0x00, 0x00, 0x03, 0xFE, 0xDC, 0xBA, 0x98, 0xFF])
    >>> '0x%x' % foo.cs
    '0xfedc'
    >>> '0x%x' % foo.ip
    '0xba98'
    """
 
    cs_value = (bytes[4]<<8)|bytes[5]
    ip_value = (bytes[6]<<8)|bytes[7]
    
    return StartSegmentAddressRecord(cs_value, ip_value)
    
class ExtendedLinearAddressRecord(object):
    def __init__(self, addr):
        self.ext_addr = addr
    
def parse_extended_linear_addr_record(bytes):
    """
    Allows for up to 32 bit addressing. Contains the upper 16 bits of
    subsequent data record addresses.

    >>> foo = parse_extended_linear_addr_record([0x02, 0x00, 0x00, 0x04, 0xAB, 0xCD, 0xFF])
    >>> '0x%x' % foo.ext_addr
    '0xabcd0000'
    """
   
    ext_addr = ((bytes[4]<<8)|bytes[5])<<16
    
    return ExtendedLinearAddressRecord(ext_addr)
    
class StartLinearAddressRecord(object):
    def __init__(self, eip):
        self.eip = eip
    
def parse_start_linear_addr_record(bytes):
    """
    Once again, might not be used.
    "The 4 byte value is loaded into the EIP register"
    
    >>> foo = parse_start_linear_addr_record([0x04, 0x00, 0x00, 0x5, 0x12, 0x34, 0x56, 0x78, 0xFF])
    >>> '0x%x' % foo.eip
    '0x12345678'
    """
        
    #4 byte EIP value
    eip = (bytes[4]<<24)|(bytes[5]<<16)|(bytes[6]<<8)|bytes[7]
    
    return StartLinearAddressRecord(eip)

record_types = [
{'name' : 'data',                     'parser' : parse_data_record,                  'addr' : None, 'byte_count' : None},
{'name' : 'end of file',              'parser' : parse_eof_record,                   'addr' : None, 'byte_count' : 0x0},
{'name' : 'extended segment address', 'parser' : parse_extended_segment_addr_record, 'addr' : 0x0,  'byte_count' : 0x2},
{'name' : 'start segment address',    'parser' : parse_start_segment_addr_record,    'addr' : 0x0,  'byte_count' : 0x4},
{'name' : 'extended linear address',  'parser' : parse_extended_linear_addr_record,  'addr' : 0x0,  'byte_count' : 0x2},
{'name' : 'start linear address',     'parser' : parse_start_linear_addr_record,     'addr' : 0x0,  'byte_count' : 0x4},
]
        
def parse_record(line):
    """
    >>> foo = parse_record(":0400940027BD002064")
    >>> [hex(ord(c)) for c in foo.contents]
    ['0x27', '0xbd', '0x0', '0x20']
    >>> parse_record("0400940027BD002064")
    Traceback (most recent call last):
    ...
    HexFileException: Line does not begin with ':' - '0400940027BD002064'
    >>> print parse_record("")
    None
    >>> parse_record(":0400940027BD00206")
    Traceback (most recent call last):
    ...
    HexFileException: Incorrect line length - ':0400940027BD00206'
    >>> parse_record(":00940064")
    Traceback (most recent call last):
    ...
    HexFileException: Incorrect line length - ':00940064'
    >>> parse_record(":0400940927BD00205b")
    Traceback (most recent call last):
    ...
    HexFileException: Invalid record type 0x09 in line ':0400940927BD00205b'
    >>> parse_record(":0400940027BD002089")
    Traceback (most recent call last):
    ...
    HexFileException: Checksum failed expected 0x89, got 0x64 in line ':0400940027BD002089'
    """

    #Ignore empty lines
    if not line:
        return None
    
    #Line must begin with a ':'
    if line[0] != ':':
        raise HexFileException("Line does not begin with ':' - '" + line + "'")
    
    #Line must be at least 11 characters, and have complete bytes 
    #not including the start character
    if (len(line[1:]) % 2) != 0 or len(line) < 11:
        raise HexFileException("Incorrect line length - '" + line + "'")

    try:
        #1: leaves out the ':'
        bytes = hex_string_to_bytes(line[1:])
        
        #Everything but the checksum, the checksum itself
        verify_checksum(bytes[:-1], bytes[-1])
        
        #Look up the record type
        record_type = bytes[3]

        try:
            #First verify the address and byte counts
            req_addr       = record_types[record_type]['addr']
            req_byte_count = record_types[record_type]['byte_count']
            name           = record_types[record_type]['name']
            verify_addr_byte_count(req_addr, req_byte_count, name, bytes)
            
            #Then call the parser for record specific things
            return record_types[record_type]['parser'](bytes)
        except IndexError as e:
            #Ends up getting re-raised below
            raise HexFileException("Invalid record type 0x%02x" % record_type)
    except (ValueError, HexFileException) as e:
        #Re-raise with the line
        raise HexFileException(str(e) + (" in line '%s'" % line))
    
def hex_string_to_bytes(string):
    """
    Convert a string of hex digits to byte values, assuming big endian.
    
    >>> [hex(item) for item in hex_string_to_bytes("FFEEDDCC")]
    ['0xff', '0xee', '0xdd', '0xcc']
    >>> hex_string_to_bytes("FFEEDDC")
    [255, 238, 221, 12]
    """
    return [int(string[n:n+2], 16) for n in range(0, len(string), 2)]
    
def verify_addr_byte_count(req_addr, req_byte_count, name, bytes):
    """
    Verify that 'bytes' conforms to the required address and byte count.
    Where byte count is the length of the data in the record, not the size of the whole record.
    If it does not, throw an exception using 'name' to identify the record.
    A value of none for req_addr or req_byte_count means there is no required value.
    
    >>> verify_addr_byte_count(0x0123, 0x2, 'foo', [0x02, 0x01, 0x23, 0xFF, 0xDE, 0xAD, 0xFF])
    >>> verify_addr_byte_count(0x0123, 0x2, 'foo', [0x02, 0x01, 0x23, 0xFF, 0xDE, 0xFF])
    Traceback (most recent call last):
    ...
    HexFileException: Incorrect number of bytes in foo record, expected 0x02 got 0x01
    >>> verify_addr_byte_count(0x0123, 0x2, 'foo', [0x03, 0x01, 0x23, 0xFF, 0xDE, 0xAD, 0xFF])
    Traceback (most recent call last):
    ...
    HexFileException: Incorrect byte count in foo record, expected 0x02 got 0x03
    >>> verify_addr_byte_count(0x0123, 0x2, 'foo', [0x02, 0xEE, 0x23, 0xFF, 0xDE, 0xAD, 0xFF])
    Traceback (most recent call last):
    ...
    HexFileException: Incorrect address in foo record, expected 0x0123 got 0xee23
    >>> verify_addr_byte_count(0x0123, None, 'foo', [0x02, 0x01, 0x23, 0xFF, 0xDE, 0xFF])
    >>> verify_addr_byte_count(None, 0x2, 'foo', [0x02, 0xEE, 0x23, 0xFF, 0xDE, 0xAD, 0xFF])
    """
    if req_byte_count is not None:
        byte_count = bytes[0]
        #Check value of byte_count field
        if byte_count != req_byte_count:
            raise HexFileException("Incorrect byte count in %s record, expected 0x%02x got 0x%02x" % (name, req_byte_count, byte_count))
          
        #Check actual number of bytes in the record overall. Note that the ':' is missing, but the checksum is still present
        len_content = (len(bytes)-5) #1 byte count + 2 address + 1 type + 1 checksum = 5
        if len_content != req_byte_count:
            raise HexFileException("Incorrect number of bytes in %s record, expected 0x%02x got 0x%02x" % (name, req_byte_count, len_content))

    if req_addr is not None:
        addr = (bytes[1]<<8)|bytes[2]
        if addr != req_addr:
            raise HexFileException("Incorrect address in %s record, expected 0x%04x got 0x%04x" % (name, req_addr, addr))
            
def verify_checksum(data, checksum):
    """
    To calculate the checkusm of a record sum the bytes excluding the initial
    ':' and the checksum itself. Then take the least significant byte of that 
    and subtract it from 0x100, the result should equal the checksum in the 
    record.
    
    >>> verify_checksum([0x03, 0x00, 0x30, 0x00, 0x02, 0x33, 0x7A], 0x1E)
    >>> verify_checksum([0x03, 0x00, 0x30, 0x00, 0x02, 0x44, 0x7A], 0x1E)
    Traceback (most recent call last):
    ...
    HexFileException: Checksum failed expected 0x1e, got 0x0d
    >>> data = [
    ... 0x10, 0x26, 0x70, 0x00, 0x21, 0x80, 0x80, 0x00, 0x04, 0x00, 0x84, 0x8C,
    ... 0x00, 0x80, 0x02, 0x3C, 0xB0, 0x51, 0x42, 0x24, 0x00]
    >>> verify_checksum(data, 0x00)
    """
    got = (0x100 - (sum(data) & 0xFF)) & 0xFF
    
    if got != checksum:
        raise HexFileException("Checksum failed expected 0x%02x, got 0x%02x" % (checksum, got))
        
if __name__ == "__main__":
    import doctest
    doctest.testmod()
