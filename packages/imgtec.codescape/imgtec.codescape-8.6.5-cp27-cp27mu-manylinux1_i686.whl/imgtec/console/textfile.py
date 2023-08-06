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


def parse_srec(data):
    r"""Parse a string as a SREC, returning a TextFile instance.
    
    >>> t = parse_srec('''\
    ... S00600004844521B
    ... S31500000000285F245F2212226A000424290008237C28
    ... S315000000100002000800082629001853812341001811
    ... S5030004F8
    ... S705800000007A''')
    >>> t.title
    'HDR'
    >>> '0x%x' % t.execution_address
    '0x80000000'
    >>> t.sections
    [(0, '(_$_"\x12"j\x00\x04$)\x00\x08#|\x00\x02\x00\x08\x00\x08&)\x00\x18S\x81#A\x00\x18')]
    """
    
    textfile = TextFile()
    for line in data.splitlines():
        code, bytes = parse_record(line)
        try:
            fn, param_width, vardata = fields[code]
        except KeyError:
            raise ValueError("Invalid field type : " + code)
        call_record(textfile, fn, param_width, vardata, bytes)
    textfile.sections = klag_sections(textfile.sections)
    return textfile
    

def klag_sections(sections):
    """Return a list of sections whose contiguous sections are merged.
        
    >>> klag_sections([])
    []
    >>> klag_sections([(0, 'abcd')])
    [(0, 'abcd')]
    >>> klag_sections([(0, 'abcd'), (16, 'qrst')])
    [(0, 'abcd'), (16, 'qrst')]
    >>> klag_sections([(0, 'abcd'), (4, 'efgh')])
    [(0, 'abcdefgh')]
    >>> klag_sections([(0, 'abcd'), (4, 'efgh'), (8, 'ijkl'), (16, 'qrst')])
    [(0, 'abcdefghijkl'), (16, 'qrst')]
    
    """
    newsections = []
    if sections:
        current_start, current_data = sections[0]
        for start, data in sections[1:]:
            if current_start + len(current_data) == start:
                current_data += data
            else:
                newsections.append((current_start, current_data))
                current_start, current_data = start, data
        if current_data:
            newsections.append((current_start, current_data))
    return newsections
        
        


def call_record(textfile, fn, param_width, vardata, bytes):
    r"""Call fn with the params decoded appropriately.
    
    >>> def test(textfile, addr, bytes):
    ...     print addr, repr(bytes)
    >>> def test_no_data(textfile, addr):
    ...     print addr
    >>> call_record(None, test, 2, True, [1, 2, 3, 4])
    258 '\x03\x04'
    >>> call_record(None, test, 2, True, [1])
    Traceback (most recent call last):
    ...
    ValueError: Expected 2 bytes for the address field, found 1
    >>> call_record(None, test, 2, True, [])
    Traceback (most recent call last):
    ...
    ValueError: Expected 2 bytes for the address field, found 0
    >>> call_record(None, test_no_data, 1, False, [1, 1, 2])
    Traceback (most recent call last):
    ...
    ValueError: Got 2 bytes of unexpected data in test_no_data
    """
    params = []
    if param_width:
        if param_width > len(bytes):
            raise ValueError('Expected %d bytes for the address field, found %d' % 
                            (param_width, len(bytes)))
        params.append(bytes_to_word(bytes[0:param_width]))
    if vardata:
        params.append(''.join(chr(x) for x in bytes[param_width:]))
    elif len(bytes) > param_width:
        raise ValueError("Got %d bytes of unexpected data in %s" % (len(bytes)-param_width, fn.__name__))
    fn(textfile, *params)
        

def validate_checksum(checksum_byte, sum_so_far):
    """Compare a checksum byte and check it is correct for sum of bytes in this record.

    >>> validate_checksum(0xf0, 0x0f)
    >>> validate_checksum(0xf0, 0x07)
    Traceback (most recent call last):
    ...
    ValueError: Read checksum of 0xf0, expected 0xf8
    """
    cmp = (~sum_so_far) & 0xff
    if cmp != checksum_byte:
        raise ValueError("Read checksum of 0x%02x, expected 0x%02x" % (checksum_byte, cmp))
            
def parse_record(line):
    """Parse a single SREC record, returning (type, bytes).
    
    >>> parse_record(' S0')
    Traceback (most recent call last):
    ...
    ValueError: Badly formatted S record: S0
    >>> parse_record(' S006')
    Traceback (most recent call last):
    ...
    ValueError: Badly formatted S record: invalid length: S006
    >>> parse_record(' S0060')
    Traceback (most recent call last):
    ...
    ValueError: Badly formatted S record: S0060
    >>> parse_record(' S00612')
    Traceback (most recent call last):
    ...
    ValueError: Badly formatted S record: invalid length: S00612
    >>> parse_record(' S00600004844521B')
    ('0', [0, 0, 72, 68, 82])
    >>> parse_record('S0060000004844521B')
    Traceback (most recent call last):
    ...
    ValueError: Badly formatted S record: invalid length: S0060000004844521B
    >>> parse_record('xS00600004844521B')
    Traceback (most recent call last):
    ...
    ValueError: Badly formatted S record: xS00600004844521B
    >>> parse_record('S00600004844521B1') # odd num chars
    Traceback (most recent call last):
    ...
    ValueError: Badly formatted S record: S00600004844521B1
    
    """
    line = line.strip()
    if not line or line[0] != 'S' or len(line) <= 2 or (len(line) % 2) != 0:
        raise ValueError("Badly formatted S record: " + line)
    code = line[1]
    bytes = [int(line[n:n+2], 16) for n in range(2, len(line)-1, 2)]
    count, data, checksum = bytes[0], bytes[1:-1], bytes[-1]
    if count != len(bytes) - 1:
        raise ValueError("Badly formatted S record: invalid length: " + line)
    validate_checksum(checksum, sum(data, count))
    return code, data

class TextFile(object):
    def __init__(self):
        self.sections = []
        self.execution_address = None
        self.title = ''

def calculate_sum(data, initial_value):
    """Calculate sum of data values.
    
    >>> calculate_sum([1, 2, 3], 0)
    6
    >>> calculate_sum([0xff01, 0xff02, 0xff03], 4)
    10
    
    """
    return sum(data, initial_value) & 0xff

def bytes_to_word(bytes):
    """Convert some bytes into a word, assumes big endian.

    >>> '0x%06x' % (bytes_to_word([1, 2, 3]),)
    '0x010203'
    >>> '0x%08x' % (bytes_to_word([1, 2, 3, 4]),)
    '0x01020304'
    """
    w = 0
    for b in bytes:
        w <<= 8
        w += b
    return w

def header_record(textfile, address, title):
    """Parse a header record.
    
    >>> tf = TextFile()
    >>> header_record(tf, 0, '\x48\x44\x52')
    >>> tf.title
    'HDR'
    """
    if address != 0:
        raise ValueError("Expected header to have address of 0, but got 0x%04x" % (address,))
    textfile.title = title

def s5_record(*_args):
    pass
  
def execution_address_record(textfile, address):
    textfile.execution_address = address

def data_record(textfile, address, data):
    r"""
    >>> tf = TextFile()
    >>> data_record(tf, 0x1234, '\x00\x28\x5F\x24\x5F\x22')
    >>> repr(tf.sections[0])
    '(4660, \'\\x00(_$_"\')'
    """   
    textfile.sections.append((address, data))

fields = {
    '0':(header_record,            2, True),
    '1':(data_record,              2, True), # 16 bit address field
    '2':(data_record,              3, True), # 24 bit address field
    '3':(data_record,              4, True), # 32 bit address field
    '5':(s5_record,                2, False), # check sum of 1 + 2 + 3 fields sent already
    '7':(execution_address_record, 4, False), # 32 bit execution address field
    '8':(execution_address_record, 3, False), # 24 bit execution address field
    '9':(execution_address_record, 2, False), # 16 bit execution address field
}

if __name__ == "__main__":
    import doctest
    doctest.testmod()
