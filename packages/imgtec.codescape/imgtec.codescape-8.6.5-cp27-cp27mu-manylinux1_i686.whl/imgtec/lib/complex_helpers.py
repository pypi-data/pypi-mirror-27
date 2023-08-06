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

import os, sys
from imgtec.test import *

def complex_separator():
    return "+j*"

def nibble_align_shift_offset(start, end, align_left):
    # some registers / memory are left aligned, if their size is not a multiple of 4 then they need shifting to the left
    if align_left:
        nibble_align = (end - start) % 4
        if nibble_align:
            return 4 - nibble_align
    return 0

def extract_bits(value, start, end, align_left = False):
    value = value >> start
    value &= (1 << (end-start)) -1
    return value << nibble_align_shift_offset(start, end, align_left)

def split_complex_value(value, start, end, split_point):
    upper_value = extract_bits(value, split_point, end)
    lower_value = extract_bits(value, start, split_point)
    return (upper_value, lower_value)

def calculate_Q_format_width_and_precision(fixed_widths, signed = True):
    try:
            # n bits  =   0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29  30  31  32
        required_chars = [1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10, 10, 10]
        char_width = required_chars[fixed_widths[0]] + required_chars[fixed_widths[1]] + 1 + (1 if signed else 0)
        precision = required_chars[fixed_widths[0]]
        #~ print 'calculate_Q', fixed_widths, '=>', (char_width, precision)
        return (char_width, precision)
    except IndexError:
        return (13, 10)

def sign_extend(value, bit_size):
    sign_mask = 1 << (bit_size - 1) 
    value = value & ((1 << bit_size) - 1)           # mask off the valid bits
    return (value ^ sign_mask) - sign_mask          # do the sign extend base on bit twiddling hacks

@test([
        (0x12345678,         0,      16,     False,     0x5678),
        (0x12345678,         16,     32,     False,     0x1234),
        (0x12345678,         3,      11,     False,     0x00CF),
        (0x08002000,         14,     28,     False,     0x2000),
        (0x08002000,         0,      14,     False,     0x2000),
        (0x08002000,         14,     28,     True,      0x8000),
        (0x08002000,         0,      14,     True,      0x8000),
        (0x0FFFFFEE,         14,     28,     True,      0xFFFC),
        (0x0FFFFFEE,         0,      14,     True,      0xFFB8),
        (0x0123456789ABCDEF, 24,     44,     False,     0x56789),
        (0x0123456789ABCDEF0123456789ABCDEF, 60, 76, False, 0xDEF0),
])
def test_extract_bits(value, start, end, align_left, expected):
    assertEquals(expected, extract_bits(value, start, end, align_left))

@test([
        (0x12345678,       0,      32,     16,     (0x1234, 0x5678)),
        (0xAFFFFFEE,       0,      32,     16,     (0xAFFF, 0xFFEE)),
        (0x12345678,       0,      24,     12,     (0x345, 0x678)),
        (0x12345678,       0,      16,     8,      (0x56, 0x78)),
])
def test_split_complex_value(value, start, end, split_point, expected):
    assertEquals(expected, split_complex_value(value, start, end, split_point))

@test([
        (0x3f,       6,       -1),
        (0x1f,       6,       31),
        (0x20,       6,       -32),
])
def test_sign_extend(value, bit_size, expected):
    assertEquals(expected, sign_extend(value, bit_size))

if __name__ == "__main__":
    test.main()
