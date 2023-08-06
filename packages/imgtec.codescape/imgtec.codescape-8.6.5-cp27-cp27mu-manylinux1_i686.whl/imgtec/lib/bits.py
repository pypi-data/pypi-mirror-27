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

import itertools

def word_to_bits(word, width):
    """Convert a word into a string of binary of specified width.

    >>> word_to_bits(0b10101010, 5)
    '01010'
    >>> word_to_bits(0b10101010, 9)
    '010101010'
    """
    return bin(word)[2:].rjust(width, '0')[-width:]

def words_to_bits(words, widths=[], default_width=8):
    """Convert a list of words into a string of binary.

    >>> words_to_bits([0b10101010, 0b10101010], [5, 3])
    '01010010'
    >>> words_to_bits([0b10101010, 0b10101010], [5])
    '0101010101010'
    >>> words_to_bits([0b10101010, 0b10101010])
    '1010101010101010'
    """
    return ''.join(word_to_bits(*x) for x in
        itertools.izip_longest(words, widths, fillvalue=default_width))

def bits_to_word(bits):
    """Convert a string of binary into a word.

    >>> bits_to_word('100000011')
    259
    """
    return int(bits, 2)
    
def _make_offsets(bits, widths, default_width=8):
    """

    >>> _make_offsets('10101010', [4, 4])
    [0, 4, 8]
    >>> _make_offsets('10101010', [], default_width=4)
    [0, 4, 8]
    >>> _make_offsets('1010101', [], default_width=4)
    [0, 4, 8]
    """
    missing = len(bits) - sum(widths, 0)
    if missing > 0:
        widths = list(widths) + [default_width] * ((missing + default_width - 1) // default_width)
    return [sum(widths[0:n]) for n in range(len(widths)+1)]
    
def bits_to_words(bits, widths=[], default_width=8):
    """Convert a list of bits into a list of words, the width of each word in
    bits is specified in the list of widths.  Order is MS bit first.
    
    If sum(widths) is less than len(bits), further widths are taken from
    `default_width`.

    >>> bits_to_words('01010010', [5, 3])
    [10, 2]
    >>> bits_to_words('10101010' * 8)
    [170, 170, 170, 170, 170, 170, 170, 170]
    >>> bits_to_words('10101010' * 8, default_width=16)
    [43690, 43690, 43690, 43690]
    """
    offsets = _make_offsets(bits, widths, default_width)   
    starts, ends = offsets[:-1], offsets[1:]
    return [bits_to_word(bits[s:e]) for s, e in zip(starts, ends)]

if __name__ == '__main__':
    import doctest
    doctest.testmod()
