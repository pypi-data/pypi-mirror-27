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

import struct
from decimal import Decimal
from imgtec.test import *

def word_to_signed(value, elemsize):
    '''
    Convert a value to a signed number with width in bytes of elemsize, assuming
    that the value has already been limited to that size.
    
    >>> word_to_signed(127, 1)
    127
    >>> word_to_signed(128, 1)
    -128
    '''
    return value if value < (1 << (elemsize*8 - 1)) else -((1 << elemsize*8) - value)

def word_to_float(value, elemsize):
    '''
    Convert a value with width in bytes elemsize to a floating point number, 
    where elemsize is 4 or 8.
    
    >>> word_to_float(0x3fc00000, 4)
    1.5
    >>> word_to_float(0xC1100000, 4)
    -9.0
    >>> word_to_float(0x00083DFE43EBF800, 8)
    1.146213565462758e-308
    '''
    if elemsize == 4:
        return struct.unpack("=f", struct.pack("=L", value))[0]
    elif elemsize == 8:
        return struct.unpack("=d", struct.pack("=Q", value))[0]

def float_to_word(value, elemsize):
    '''
    Convert a floating point number into a word with width in bytes elemsize,
    where elemsize is 4 or 8.
    
    >>> '0x%x' % float_to_word(1.5, 4)
    '0x3fc00000'
    >>> '0x%x' % float_to_word(-9, 4)
    '0xc1100000'
    >>> '0x%x' % float_to_word(1.146213565462758e-308, 8)
    '0x83dfe43ebf800'
    '''
    if elemsize == 4:
        return struct.unpack("=L", struct.pack("=f", value))[0]
    elif elemsize == 8:
        return struct.unpack("=Q", struct.pack("=d", value))[0]

def word_to_fixed(value, n, need_shift=False, signed=True):
    '''
    Convert a word value to a fixed point number with n fractional bits. 
    If signed is True the result will be signed. In the case that n=24 or n=23 
    and signed is True, if the input value is known to be aligned to the top of 
    a 32 bit value set need_shift to correct this.
    
    >>> word_to_fixed(0x80, 7)
    Decimal('-1')
    >>> word_to_fixed(0x80, 8, signed=False)
    Decimal('0.5')
    >>> word_to_fixed(0x7f, 8)
    Decimal('0.49609375')
    >>> word_to_fixed(0x00800000, 24, need_shift=False, signed=False)
    Decimal('0.5')
    >>> word_to_fixed(0x80000000, 24, need_shift=True, signed=False)
    Decimal('0.5')
    '''
    shiftable = (n == (23 if signed else 24))
    if shiftable and need_shift:
        value = (value >> 8) & 0xffffff
    maxval = (1 << n)
    if signed and (value & maxval):
        value = (value & (maxval-1)) - maxval
    return Decimal(value) / (1 << n)

def fixed_to_word(value, n):
    '''
    Convert a fixed point number with n fractional bits into a word value.
    
    >>> '0x%x' % fixed_to_word(-1.0000, 7)
    '0x80'
    >>> '0x%x' % fixed_to_word(0.4961, 8)
    '0x7f'
    >>> '0x%x' % fixed_to_word(0.99997, 15)
    '0x7fff'
    '''
    value = int(round(value * (1 << n)))
    return value & ((1 << (n + 1)) - 1)
    
def wrap_value(value, num_bits):
    '''
    Wrap a value into a number of width in bits num_bits.
    
    >>> wrap_value(8, 3)
    0
    >>> wrap_value(-1, 3)
    7
    >>> wrap_value(2, 1)
    0
    >>> wrap_value(3, 1)
    1
    '''
    #The number that it would wrap at for example 2^4 = 16, 16 becomes 0x0, 17, 0x1 etc.
    max = 2**num_bits
    return value % max
    
@test([
( 0x0,  0x0,   1),
( 0x1,  0x1,   1),
( 0x0,  0x2,   1),
( 0x1,  0x3,   1),
( 0x1,  0x7,   1),
( 0x0,  0x8,   1),
( 0x1, -0x1,   1),
( 0x0, -0x2,   1),
( 0x1, -0x3,   1),
( 0x0, -0x4,   1),
( 0x1, -0x7,   1),
(0xff, -0x1,   8),
( 0x1, -0xff,  8),
(0x00, -0x100, 8),
(0x00,  0x100, 8),
(0x01,  0x101, 8),
(0x10,  0x110, 8),
(0x10,  0x110, 8),
])
def wrap_value_test(expected, original, num_bits):
    assertEquals(expected, wrap_value(original, num_bits))

@test([
    (0x80, 7, False, True, '-1.0000', 4),
    (0x7f, 7, False, True, '0.9922', 4),
    (0xff, 7, False, True, '-0.0078', 4),
    
    (0x80, 8, False, False, '0.5000', 4),
    (0x7f, 8, False, False, '0.4961', 4),
    (0xff, 8, False, False, '0.9961', 4),

    (0x8000, 15, False, True, '-1.00000', 5),
    (0x7fff, 15, False, True, '0.99997', 5),
    (0xffff, 15, False, True, '-0.00003', 5),
    
    (0x8000, 16, False, False, '0.50000', 5),
    (0x7fff, 16, False, False, '0.49998', 5),
    (0xffff, 16, False, False, '0.99998', 5),

    (0x80000000, 23, True, True, '-1.0000000', 7),
    (0x7fffffff, 23, True, True, '0.9999999', 7),
    (0xffffffff, 23, True, True, '-0.0000001', 7),
    
    (0x80000000, 24, True,  False, '0.5000000', 7),
    (0x00800000, 24, False, False, '0.5000000', 7),
    (0x7fffffff, 24, True,  False, '0.4999999', 7),
    (0x7fffffBD, 24, True,  False, '0.4999999', 7),
    (0xffffffff, 24, True,  False, '0.9999999', 7),

    (0x80000000, 31, False, True, '-1.0000000', 7),
    (0x7fffffff, 31, False, True, '0.9999999995', 10),
    (0xffffffff, 31, False, True, '-0.0000000005', 10),
    
    (0x80000000, 32, False, False, '0.5000000', 7),
    (0x7fffffff, 32, False, False, '0.4999999998', 10),
    (0xffffffff, 32, False, False, '0.9999999998', 10),
])
def fx_w_test(value, n, need_shift, signed, expected, p):
    f = word_to_fixed(value, n, need_shift, signed)
    assertEquals(expected, '%.*f' % (p, f))
    if need_shift:
        assertEquals('0x%x' % (value>>8), '0x%x' % (fixed_to_word(f, n)))
    else:
        assertEquals('0x%x' % (value), '0x%x' % (fixed_to_word(f, n)))
    
if __name__ == "__main__":
    test.main()
