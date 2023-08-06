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

from collections import namedtuple
from imgtec.lib.namedenum import namedenum

_ENABLE_ALL_ACCESS = 0x80000000

class MemoryDetails(object):
    def __init__(self, type, name, display_size=1, element_size=1, default_display_width=16, origin=0, supports_breakpoints=False, prefix='', size=4294967295L, read_ptrs=[], write_ptrs=[], address_display_width=8, default_start_address=''):
        self.type = type
        self.name = name
        self.display_size = display_size
        self.element_size = element_size
        self.default_display_width = default_display_width
        self.origin = origin
        self.supports_breakpoints = supports_breakpoints
        self.prefix = prefix
        self.size = size
        self.read_ptrs = read_ptrs
        self.write_ptrs = write_ptrs
        self.address_display_width = address_display_width
        self.default_start_address = default_start_address # sometimes called cursor_at_start

Accessibility = namedenum('Accessibility', 'none read write read_write')
_accessibility_mapping = {'':Accessibility.none, 
                        'r':Accessibility.read, 
                        'w':Accessibility.write, 
                        'rw':Accessibility.read_write}
_accessibility_rmapping = {v:k for k, v in _accessibility_mapping.items()}

class ValidRange(object):
    '''Represents a section of memory in the HSP memory map.
    
    >>> ValidRange(0xbfc00000, 0xbfc03fff, Accessibility.read)
    ValidRange(0xbfc00000, 0xbfc03fff, Accessibility.read)
    '''
    def __init__(self, start, last, accessibility, *extras, **kwargs):
        self.start = start
        '''The first address in this range. e.g. for all memory this is 
        0x00000000.'''
        
        self.last= last
        '''The last address in this range. e.g. for all memory in a 32-bit
        address space this is 0xffffffff.'''
        
        self.accessibility = _accessibility_mapping.get(accessibility, accessibility)
        '''The :class:`Accessibility` (read/write ability) of this range.'''
        
        self.address_display_width = kwargs.get('address_display_width', 8)
        '''This is used to format the range nicely, it has no other function.
        See :attr:`Memory.address_display_width`.'''
        
    def __eq__(self, rhs):
        return type(self) == type(rhs) and \
            (self.start, self.last, self.accessibility) == \
            (rhs.start, rhs.last, rhs.accessibility)
        
    def __repr__(self):
        format = 'ValidRange(0x{:0%dx}, 0x{:0%dx}, {!r})' % \
            (self.address_display_width, self.address_display_width)
        return format.format(self.start, self.last, self.accessibility)

class Memory(object):
    """Represents memory accessible by a Thread."""

    def __init__(self, context, thread, details):
        self.__context = context
        self.__thread = thread
        self._details = details
        
    def _get_type(self):
        t = self._details.type
        return t if self.__thread.memory_protection else (t | _ENABLE_ALL_ACCESS)

    def GetTypeId(self):
        """Memory type ID."""
        return self._details.type

    def GetName(self):
        """Name of the memory type.
        
        For example, Ram, this will return 'Ram'.
        """
        return self._details.name

    def GetPrefix(self):
        """
        The string used in the expression evaluator to cast addresses to this memory type.

        For example, this will return the result in Narrow ram on an MCP:
        
        .. sourcecode:: python
        
            thread.Evaluate("(*(__Narrow unsigned short*) 0x1400)")
        """
        return self._details.prefix

    def GetOrigin(self):
        """The start address of this memory type. 
        
        For example for Ram and most memory types this is zero.
        """
        return self._details.origin

    def GetDefaultStartAddress(self):
        """An expression that is used to determine the default location to view
        in a memory region.
        
        For example for Ram this returns 'pc'.
        """
        return self._details.default_start_address
        
    def GetAddressDisplayWidth(self):
        """Display width of the address in nibbles.
        
        For example in a 32-bit address space this returns 8.
        """
        return self._details.address_display_width

    def GetSize(self):
        """Size of memory less one.
        
        For example in a 32-bit address space this returns 0xffffffff.
        """
        return self._details.size

    def GetElementSize(self):
        """Minimum addressable element size in bytes.
        
        For example in most memory types this returns 1, but some harvard 
        architectures cores this might return 4 if only 32-bit access to data
        spaces is supported.
        """
        return self._details.element_size

    def GetDisplaySize(self):
        """Default element size in bytes that should be used when displaying this memory."""
        return self._details.display_size

    def GetDefaultDisplayWidth(self):
        """Default width when displaying this memory."""
        return self._details.default_display_width

    def GetSupportsBreakpoints(self):
        """Returns True if this memory type supports breakpoints."""
        return self._details.supports_breakpoints

    def Check(self, address, element_size, element_count, initial_value, increment):
        """
        Checks the contents of an region of memory are set to a particular value or incrementing
        sequence of values.

        :param address:        The address to check from.
        :param element_size:
            The element size to check.

            ===== ==============
            1     8-bit
            2     16-bit
            4     32-bit
            8     64-bit
            ===== ==============
        :param element_count:  Specifies how many to elements to check.
        :param initial_value:  The starting value of the sequence.
        :param increment:      The value to increase value by at each location.
        :returns:
            True if the memory and sequence match, False if there was no match, or
            an exception is raised if an error occurred.
        """
        return self.__context.CheckMemory(address, element_size, element_count, initial_value, increment, self._get_type())

    def Fill(self, address, element_size, element_count, initial_value, increment=0):
        """
        Fills the contents of a region of memory with a value or incrementing sequence
        of values.

        :param address:        The address to fill from.
        :param element_size:   
            The element size to fill.

            ===== ==============
            1     8-bit
            2     16-bit
            4     32-bit
            8     64-bit
            ===== ==============
        :param element_count:  Specifies how many to elements to fill.
        :param initial_value:  The starting value of the sequence.
        :param increment:      The value to increase value by at each location.
        """
        self.__context.InitMemory(address, element_size, element_count, initial_value, increment, self._get_type())

    def WriteString(self, address, s):
        """Writes a null terminated string(including the null terminator) to memory at address.
        
        .. sourcecode :: python
        
            thread.memory.WriteString("global_argv[1]", "-n")
        """
        return self.__context.WriteString(address, s, self._get_type())

    def Write(self, address, data, element_type=4):
        """
        Write a value or list of values to a specified region of memory.

        .. sourcecode:: python

            >>> thread.memory.Write(0x20880280, 0xDEADC0DE)
            >>> thread.memory.Write(0x20880280, [1.61803, 2.71828, 3.14159], element_type=ElementType.float)
            >>> thread.memory.Write(0x20880280, 'spam', ElementType.blob)

        :param address:        The address to write to.
        :param data:           The value or list of values to write.
        :param element_type:   The :class:`ElementType <imgtec.codescape.da_types.ElementType>` to write.
        """
        if hasattr(data, "__len__"):
            self.__context.WriteMemoryBlock(address, len(data), element_type, data, self._get_type())
        else:
            self.__context.WriteMemoryBlock(address, 1, element_type, [data], self._get_type())

    def Read(self, address, element_type=4, count=None):
        """
        Reads a value or list of values from the specified region of memory.

        .. sourcecode:: python

            >>> thread.memory.Read(0x20880280)
            2735279136L
            >>> thread.memory.Read(0x20880280, count=2)
            [2735279136L, 2248671270L]
            >>> thread.memory.Read(0x20880280, element_type=ElementType.float)
            -7.42935245e-18
            >>> thread.memory.Read(0x20880280, element_type=ElementType.blob, count=10)
            ' \\x0c\\t\\xa3&\\x00\\x08\\x86\\xe3\\x01'

        :param address:        The address to read from.
        :param element_type:   The :class:`ElementType <imgtec.codescape.da_types.ElementType>` to read.
        :param count:          The number of elements to read (optional).
        :returns:
            A list of values if count is specified, otherwise a single value will be returned.
            When ElementType.blob is specified, a string is returned.
        """
        if count is None:
            return self.__context.ReadMemoryBlock(address, 1, element_type, self._get_type())[0]
        else:
            return self.__context.ReadMemoryBlock(address, count, element_type, self._get_type())
            
    def ReadModWrite(self, address, new_value, modify_mask=0xffffffff, operation='=', count=1, atomic=False):
        """Perform a read-modify-write operation on a target memory location.
        
        :param address:     The location in memory to read/write.
        :param new_value:   The value to apply with the old value operation.
        :param modify_mask: Mask specifying the bits to modify, only bits set in this mask will be affected.
        :param operation:   Specifies the operation to apply to the target memory.
        :param count:       Specifies the number of elements this operation should be applied to.
        :param atomic:      When True the probe will obtain the atomic lock on the debug port.  
        
        .. note:: If the core does not support atomic locking on the debug port and `atomic` is True. then
        an exception will be raised.
        
        This function is equivalent to ::

            if atomic:
                obtain_lock()
            try:
                if operation == '=' and modify_mask == 0xffffffff:
                    values = [new_value] * count
                else:
                    values = Read(address, count)
                    values = [(x & ~modify_mask) | (x OP new_value) & modify_mask) for x in values]
                Write(address, values)
            finally:
                if atomic:
                    release_lock()

        The operations available are :

        == ====================================== ==========================
        OP Description                            OP Pseudo code
        == ====================================== ==========================
        \= Assign the value.                      return new_value
        \+ Add new value to the old value.        return old_value + new_value
        \- Subtract new value from the old value. return old_value - new_value
        ^  Xor new value with the old value.      return old_value ^ new_value
        == ====================================== ==========================
        
        """
        if atomic:
            return self.__context.ReadModWriteAtomic(address, new_value, modify_mask, operation, count, self._get_type())
        else:
            return self.__context.ReadModWrite(address, new_value, modify_mask, operation, count, self._get_type())
        
        

    def ReadString(self, address, length):
        """Reads a null terminated ASCII string.

        :param address:        The address to read from.
        :param length:
            The maximum length of string to read. This length must not be larger than 4096 bytes.
        """
        return self.__context.ReadString(address, length, self._get_type())

    def LoadBinaryFile(self, filename, address, start_offset=0, length=None, progress=True):
        """
        Loads a binary file from the specified location into target memory.
        No interpretation of the binary is performed.
        
        :param filename:      The full path of the binary file.
        :param address:       The address to load the binary file to.
        :param start_offset:  The number of bytes to ignore before starting to download data
        :param length:        The number of bytes to load. If omitted or length is longer than the file,
                              the length of the file is used.
        """
        if length is None:
            length = 0xffffffff
        self.__context.LoadBinaryFileEx(filename, address, start_offset, length, progress, self._get_type())

    def SaveBinaryFile(self, filename, address, length=None, progress=True):
        """
        Save the contents of a region of target memory to a file.
        
        :param filename:      Full path of the file to receive the binary data.
        :param address:       Start address of the binary image on the target.
        :param length:        Size of the binary image in bytes.
        """
        if length is None:
            length = 0xffffffff
        self.__context.SaveBinaryFile(filename, address, length, progress, self._get_type())
        
    def SetAccessibility(self, begin, last, accessibility):
        '''Change the accessibility of a range of memory.
        
        This patches the configured memory accessibility in the HSP memory map,
        but this is a temporary change, it will be lost when the probe is 
        disconnected ::
        
            >>> from pprint import print
            >>> pprint(thread.memory.valid_ranges)
            [ValidRange(0x80000000, 0xbfffffff, Accessibility.read),
             ValidRange(0xc0000000, 0xffffffff, Accessibility.read_write)]
            >>> thread.memory.SetAccessibility(0x80000000, 0x80ffffff, Accessibility.read_write)
            >>> pprint(thread.memory.valid_ranges)
            [ValidRange(0x80000000, 0x80ffffff, Accessibility.read_write),
             ValidRange(0x81000000, 0xbfffffff, Accessibility.read),
             ValidRange(0xc0000000, 0xffffffff, Accessibility.read_write)]
        '''
        accessibility = _accessibility_rmapping.get(accessibility, accessibility)
        self.__context.SetMemoryAccessibility(self.type_id, begin, last, accessibility)
        
    def GetValidRanges(self):
        '''Get a list of :class:`ValidRange`\s that are accessible in this memory
        type as configured in the HSP memory map.
        '''
        ranges = self.__context.GetValidRanges(self.type_id)
        return [ValidRange(*r, address_display_width=self.address_display_width) for r in ranges]

    default_display_width = property(GetDefaultDisplayWidth)
    default_start_address = property(GetDefaultStartAddress)
    address_display_width = property(GetAddressDisplayWidth)
    display_size =          property(GetDisplaySize)
    element_size =          property(GetElementSize)
    name =                  property(GetName)
    origin =                property(GetOrigin)
    prefix =                property(GetPrefix)
    size =                  property(GetSize)
    supports_breakpoints =  property(GetSupportsBreakpoints)
    type_id =               property(GetTypeId)
    valid_ranges =          property(GetValidRanges)
