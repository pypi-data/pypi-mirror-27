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

class DisassemblyOperator(object):
    '''An operator of a disassembled instruction.
    
    For example ``MOV r0, r1`` is an operator.
    
    Most architectures have only 1 operator per instruction
    
    '''
    def __init__(self, name='', operands=[], *extra):
        self.name = name
        """The name of this operator, e.g. MOV."""

        self.operands = operands
        """List of string operands in this operator, e.g. ['r0', 'r1']."""
        
        self.is_source = False
        
    def __repr__(self):
        return '%-9s %s' % (self.name, ', '.join(self.operands))

class Disassembly(object):
    r"""Represents the result of a disassemble operation of an instruction,
    as returned by :meth:`imgtec.codescape.Thread.Disassemble`, 
    :func:`imgtec.codescape.tiny.DisassembleBytes`, or
    :meth:`imgtec.codescape.tiny.Tiny.Disassemble`.

    The type can be used to get detailed information of the result of the
    disassembly or it can be passed to repr() to get a formatted display::

        >>> from imgtec.codescape import tiny
        >>> x = tiny.DisassembleBytes(0x87fe7e70, None, 'mips32', 'o32', '\x03\xE0\x00\x08')
        >>> x.size
        4
        >>> x.opcode
        '03e00008'
        >>> x.ops[0].name
        'jr'
        >>> x.ops[0].operands
        ['ra']
        >>> '0x%08x' % (x.address,)
        '0x87fe7e70'
        >>> x
        0x87fe7e70 03e00008    jr        ra

    """

    def __init__(self, address, size, ops, opcode, symbol, src_line_info = [], slotted_instr_len = 0, src_line_info_before=[], isa = "", *extras):
        self.address = address
        """The address of the instruction."""

        self.size = size
        """The size of the instruction in bytes."""

        self.ops = [DisassemblyOperator(*op) for op in ops]
        """List of :class:`~imgtec.codescape.DisassemblyOperator` in the
        instruction.  Most architectures have only 1 operator per instruction."""

        self.opcode = opcode
        """The opcode as a python string of hex digits, this is always big endian."""

        if isinstance(opcode, (tuple, list)):
            self.opcode = long(opcode[0]) << 64 | long(opcode[1]) << 32 | long(opcode[2]) << 0
        if isinstance(opcode, str):
            self.opcode = ''.join('%02x' % (ord(x),) for x in self.opcode)
        elif self.opcode is None:
            self.opcode = ''
        else:
            self.opcode = ('%%0%dx' % (self.size*2,)) %(self.opcode,)

        self.symbol = symbol
        """The symbol for this address if symbols are loaded AND there is a symbol
        at this address."""

        self._src_line_info = src_line_info

        self.slotted_instr_len = slotted_instr_len
        """Optional length of slotted instruction in bytes."""

        self._src_line_info_before = src_line_info_before
        
        self.isa = isa
        """ISA of the disassembler."""

        self._extras  = extras

    def _repr(self, opcode_width=0, is_slot=False):
        lines = []
        slot = 'DS' if is_slot else ''
        op = self.ops[0]
        filler = ' ' * (opcode_width - self.size*2)
        lines.append("0x%08x %s%s %2s %r" % (self.address, self.opcode, filler, slot, op))
        for op in self.ops[1:]:
            filler = ' ' * opcode_width
            lines.append("%10s %s %2s %r" % ('', filler, slot, op))
        return '\n'.join(lines)

    def __repr__(self):
        return self._repr()

class DisassemblyList(list):
    r"""A list of :class:`Disassembly` instances.
    
    :meth:`imgtec.codescape.Thread.Disassemble`, 
    :func:`imgtec.codescape.tiny.DisassembleBytes`, and
    :meth:`imgtec.codescape.tiny.Tiny.Disassemble` return a DisassemblyList
    instance when the `count` parameter is not None.

    When printed it will display the disassembly in columns, and potential 
    delay slots will be indicated with 'DS'.  For example ::

        >>> x = tiny.DisassembleBytes(0x87fe7e70, None, 'mips32', 'o32', 
        ...        '\x03\xE0\x00\x08' + 
        ...        '\x27\xBD\x00\x20' +
        ...        '\x40\x03\x48\x00' +
        ...        '\x03\xE0\x00\x08')
        
        0x87fe7e70 03e00008    jr        ra
        0x87fe7e74 27bd0020 DS addiu     sp, sp, 32
        0x87fe7e78 40034800    mfc0      v1, c0_count
        0x87fe7e7c 03e00008    jr        ra
    """
    def __repr__(self):
        slot_len = 0
        lines = []
        opcode_width = max(i.size*2 for i in self)
        for i in self:
            lines.append(i._repr(opcode_width, bool(slot_len)))
            slot_len = max(slot_len - i.size, 0) + i.slotted_instr_len
        return '\n'.join(lines)

