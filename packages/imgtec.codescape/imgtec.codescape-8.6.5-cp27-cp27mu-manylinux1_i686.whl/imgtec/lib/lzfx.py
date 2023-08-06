'''
 * Copyright (c) 2009 Andrew Collette <andrew.collette at gmail.com>
 * http://lzfx.googlecode.com
 *
 * Implements an LZF-compatible compressor/decompressor based on the liblzf
 * codebase written by Marc Lehmann.  This code is released under the BSD
 * license.  License and original copyright statement follow.
 *
 *
 * Copyright (c) 2000-2008 Marc Alexander Lehmann <schmorp@schmorp.de>
 *
 * Redistribution and use in source and binary forms, with or without modifica-
 * tion, are permitted provided that the following conditions are met:
 *
 *   1.  Redistributions of source code must retain the above copyright notice,
 *       this list of conditions and the following disclaimer.
 *
 *   2.  Redistributions in binary form must reproduce the above copyright
 *       notice, this list of conditions and the following disclaimer in the
 *       documentation and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MER-
 * CHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO
 * EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPE-
 * CIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 * PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES LOSS OF USE, DATA, OR PROFITS
 * OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 * WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTH-
 * ERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
 * OF THE POSSIBILITY OF SUCH DAMAGE.
'''

import collections

# These cannot be changed, as they are related to the compressed format. 
LZFX_MAX_LIT = (1 <<  5)
LZFX_MAX_OFF = (1 << 13)
LZFX_MAX_REF = ((1 << 8) + (1 << 3))
LZFX_MIN_REF = 3 # Backref takes up to 3 bytes, so don't bother with anything smaller

''' Compressed format

    There are two kinds of structures in LZF/LZFX: literal runs and back
    references. The length of a literal run is encoded as L - 1, as it must
    contain at least one byte.  Literals are encoded as follows:

    000LLLLL <L+1 bytes>

    Back references are encoded as follows.  The smallest possible encoded
    length value is 1, as otherwise the control byte would be recognized as
    a literal run.  Since at least three bytes must match for a back reference
    to be inserted, the length is encoded as L - 2 instead of L - 1.  The
    offset (distance to the desired data in the output buffer) is encoded as
    o - 1, as all offsets are at least 1.  The binary format is:

    LLLooooo oooooooo           for backrefs of real length < 9   (1 <= L < 7)
    111ooooo LLLLLLLL oooooooo  for backrefs of real length >= 9  (L > 7)
'''

def encode_literal(lit, maxlit=LZFX_MAX_LIT, _ip=0, _debug=None):
    r'''Encode literal into zero or more literal run strings for output.
    
    >>> str(encode_literal('', 5))
    ''
    >>> str(encode_literal('hello very long world', 5))
    '\x04hello\x04 very\x04 long\x04 worl\x00d'
    >>> str(encode_literal('hello very long worl', 5))
    '\x04hello\x04 very\x04 long\x04 worl'
    '''
    out = bytearray()
    _ip -= len(lit)
    for n in range(0, len(lit), maxlit):
        chunk= lit[n:n+maxlit]
        if _debug: _debug('lit*%d@%d' % (len(chunk), _ip))
        out.append(len(chunk) - 1)
        out.extend(chunk)
        _ip += len(chunk)
    return out
    
def decode_literal(ibuf, start=0, _debug=None):
    r'''Decode a literal run, returns the literal decoded (or None if not a literal).
    
    # Format 000LLLLL: a literal byte string follows, of length L+1     
    
    >>> decode_literal(bytearray('\x04hello'))
    bytearray(b'hello')
    >>> decode_literal(bytearray('1\x04hello'), 1)
    bytearray(b'hello')
    >>> decode_literal(bytearray('\x84hello'))
    >>>
    '''
    lit = ''
    ctrl = ibuf[start]
    if ctrl < (1 << 5):
        litlen = ctrl + 1
        if start + litlen >= len(ibuf):
            raise ValueError('Corrupt Literal')
        return ibuf[start+1:start+1+litlen]
    
def encode_backref(off, matchlen):
    '''
    >>> match = encode_backref(0xff, 5)
    >>> [bin(x) for x in match]
    ['0b1100000', '0b11111111']
    >>> match = encode_backref(0xff, 9)
    >>> [bin(x) for x in match]
    ['0b11100000', '0b0', '0b11111111']
    >>> match = encode_backref(0xff, 10)
    >>> [bin(x) for x in match]
    ['0b11100000', '0b1', '0b11111111']
    >>> match = encode_backref(8470-174-1, 3)
    Traceback (most recent call last):
    ...
    ValueError: Can't create a backref 8295 bytes back
    '''
    if off >= LZFX_MAX_OFF:     
        raise ValueError('Can\'t create a backref %d bytes back' % (off,))
    # Format 1: [LLLooooo oooooooo] 
    matchlen -= 2
    if matchlen < 7:
        return bytearray([((off >> 8) & 0x1f) + (matchlen << 5), 
                        off & 0xff])

    # Format 2: [111ooooo LLLLLLLL oooooooo] 
    else:
        return bytearray([((off >> 8) & 0x1f) + 0b11100000,
              (matchlen - 7) & 0xff,
              off & 0xff])    
    
def decode_backref(ibuf):
    '''Returns (bytes consumed, offset, matchlen).
    
    This is one of two formats::
    
      Format #1 [LLLooooo oooooooo]: backref of length L+2
                    ^^^^^ ^^^^^^^^
                      A       B
             #2 [111ooooo LLLLLLLL oooooooo] backref of length L+7+2
                    ^^^^^          ^^^^^^^^
                      A               B
     In both cases the location of the backref is computed from the
     remaining part of the data as follows::
     
        location = op - A*256 - B - 1

    >>> decode_backref(bytearray([0b1100000, 0b11111111]))
    (2, 256, 5)
    >>> decode_backref(bytearray([0b11100000, 0b0, 0b11111111]))
    (3, 256, 9)
    >>> decode_backref(bytearray([0b11100000, 0b1, 0b11111111]))
    (3, 256, 10)
    '''
    ctrl = ibuf[0]
    if (ctrl & 0b11100000) != 0b11100000:
        matchlen = (ctrl >> 5) + 2
        off     = (ctrl & 0x1f) * 256 + ibuf[1] + 1
        consumed = 2
    else:
        matchlen = ibuf[1] + 9
        off     = (ctrl & 0x1f) * 256  + ibuf[2] + 1
        consumed = 3
    return consumed, off, matchlen

    
def _make_table(buf, ip):
    table = collections.defaultdict(list)
    _add_lookups(table, buf, 0, ip)
    return table        
    
def _add_lookups(table, buf, start, end=None):
    if end is None:
        end = start+1
    for n in range(start, end):
        table[str(buf[n:n+3])].append(n)
        
def delete_old_refs(refs, ip, max_offset=LZFX_MAX_OFF):
    '''
    >>> refs = [0, 100, 200]
    >>> delete_old_refs(refs, 100, 100)
    >>> refs
    [100, 200]
    >>> delete_old_refs(refs, 200, 100)
    >>> refs
    [200]
    '''
    first_valid = len(refs)
    for n, ref in enumerate(refs):
        if (ip - ref) < max_offset:
            first_valid = n
            break
    del refs[:first_valid]
                
def find_best_match(table, buf, ip):
    '''
   
    >>> find_best_match(None, bytearray('hello hello hello world hello world'), 24)
    (12, 11)
    >>> find_best_match(None, bytearray('hello hello hello hello'), 12)
    (0, 11)
    >>> find_best_match(None, bytearray('hello hello hello hello'), 18)
    (12, 5)
    >>> find_best_match(None, bytearray('hello cruel world'), 12)
    (-1, 0)
    >>> find_best_match(None, bytearray('hello'), 0)
    (-1, 0)
    '''
    if table is None:
        table = _make_table(buf, ip)
        
    lookup = str(buf[ip:ip+3])
    refs = table[lookup]
        
    # first remove any refs that are too far away, as they are added in order
    # the oldest are at the front. Find the first one in the list that is not 
    # too far away
    delete_old_refs(refs, ip)
    if not refs:
        return (-1, 0)
        
    def subseqlen(ref):
        if (ip - ref) < LZFX_MIN_REF:
            return 0
            
        maxmatchlen = min(LZFX_MAX_REF, len(buf) - ip, ip - ref)
        matchlen = 3
        while matchlen < maxmatchlen and buf[ref+matchlen] == buf[ip+matchlen]:
            matchlen += 1
        return matchlen
        
    lengths = [(subseqlen(ref), ref) for ref in refs]
    maxlen, maxref = max(lengths)
    return maxref, maxlen
    
'''before longest subseq
===== ===== ======= =====
Name  None  ByteRLE LZFX
===== ===== ======= =====
.text 48544 83841   20066
===== ===== ======= =====

===== ===== ======= =====
Name  None  ByteRLE LZFX
===== ===== ======= =====
.text 48544 83841   22487
===== ===== ======= =====

''' 
    
    
def compress(ibuf, _debug=None):
    table = collections.defaultdict(list)
    ibuf = bytearray(ibuf)
    ip = 0
    in_end = len(ibuf)

    obuf = bytearray()
    
    lit = bytearray('')    # current literal run
    off = 0
    while ip + 2 < in_end: #   The lookup reads 2 bytes ahead 
        ref, matchlen = find_best_match(table, ibuf, ip)
        if matchlen:
            #print ip, ref, matchlen, repr(str(ibuf[ip:ip+matchlen])), repr(str(ibuf[ref:ref+matchlen]))
            obuf += encode_literal(lit, _ip=ip, _debug=_debug)
            lit = bytearray('')
            
            off = ip - ref - 1            
            obuf += encode_backref(off, matchlen)
            if _debug: 
                _debug('backref%d@%d[%d:%d] %s' % (len(encode_backref(off, matchlen))-1, ip, ref, matchlen, ' '.join(bin(x)[2:].rjust(8, '0') for x in encode_backref(off, matchlen)), 
                    ##repr(str(ibuf[ip:ip+matchlen])), repr(str(ibuf[ref:ref+matchlen]))))
                    ))

            #_add_lookups(table, ibuf, ip, ip+matchlen) 
            ip += matchlen

        else:
            # Keep copying literal bytes 
            _add_lookups(table, ibuf, ip)
            lit.append(ibuf[ip])
            ip += 1

    # copy everything remaining as a literal
    lit += ibuf[ip:]
    ip += len(lit)
    obuf += encode_literal(lit, _ip=ip, _debug=_debug)
    return str(obuf)
        
def decompress(ibuf, _debug=None):
    ip = 0
    in_end = len(ibuf)
    ibuf = bytearray(ibuf)
    obuf = bytearray()
    while ip < in_end:
        literal = decode_literal(ibuf, ip)
        if literal:
            if _debug: _debug('lit*%d@%d' % (len(literal),len(obuf)))
            obuf += literal
            ip += len(literal) + 1
        
        else:
            consumed, off, matchlen = decode_backref(ibuf[ip:])
            ref  = len(obuf) - off
            if _debug: _debug('backref%d@%d[%d:%d] %s' % (consumed-1, len(obuf), ref, matchlen, ' '.join(bin(x)[2:].rjust(8, '0') for x in ibuf[ip:ip+consumed])))
            if ref < 0 or ref+matchlen > len(obuf):
                raise ValueError('Corrupt BackRef')
            ip += consumed
            obuf += obuf[ref:ref+matchlen]

    return str(obuf)

def _debug(input):
    from imgtec.lib import rst
    import traceback
    comp, deco = [], []
    try:
        compressed = compress(input, _debug=comp.append)
        uncompressed = decompress(compressed, _debug=deco.append)
        if uncompressed != input:
            raise Exception('output different')
    except Exception as e:
        traceback.print_exc()

    rows = [(str(n), ip, op, '==' if ip==op else '!=') for n, (ip, op) in enumerate(zip(comp, deco))]
    return rst.table(['#', 'comp', 'decomp', 'equal'], rows)

if __name__ == '__main__':
    testdata = 'Marymary had a little lamb' + ' whose name was Marymary wasnt it.'
    compressed = compress(testdata)
    WIDTH = 40
    for n in range(0, len(compressed), WIDTH):
        print '"' + ''.join(['\\x%02x' % ord(x) for x in compressed[n:n+WIDTH]]) + '"'
    
    #testdata =open(__file__, 'r').read()
    #print _debug(testdata)
    test.main()


