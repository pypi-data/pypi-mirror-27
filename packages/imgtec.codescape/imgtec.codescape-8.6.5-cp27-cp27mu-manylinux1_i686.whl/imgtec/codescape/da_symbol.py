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

__all__ = 'Symbol'

from imgtec.lib.namedenum import namedenum

SymbolFlags = namedenum('SymbolFlags', 
    watchable           = 0x0001,
    expandable          = 0x0002,
    array               = 0x0004,
    suc                 = 0x0008,
    enum                = 0x0010,
    pointer             = 0x0020,
    reference           = 0x0040,
    function            = 0x0080,
    signed              = 0x0100,
    string              = 0x0200,
    char                = 0x0400,
    register            = 0x0800,
    assignable          = 0x1000,
)

class Symbol(object):

    def __init__(self, type, name, handle, hidden, aliased, optimised_out, location, type_handle, flags, size, element_count, description, extended_location, *extras):
        self.__type = type
        self.__name = name
        self.__handle = handle
        self.__hidden = hidden
        self.__optimised_out = optimised_out
        self.__location = location
        self.__type_handle = type_handle
        self.__flags = flags
        self.__size = size
        self.__element_count = element_count
        self.__description = description
        self.__extended_location = extended_location

        self._aliased = aliased
        """Reserved."""

        self._extras = extras
        """Reserved for future expansion."""
        
    def __repr__(self):
        return "Symbol(type=%r, name=%r, handle=%r, hidden=%r, aliased=%r, optimised_out=%r, location=%r, type_handle=%r, flags=%r, size=%r, element_count=%r, description=%r, extended_location=%r)" % (
            self.__type, self.__name, self.__handle, self.__hidden, self._aliased, 
            self.__optimised_out, self.__location, self.__type_handle, self.__flags, 
            self.__size, self.__element_count, self.__description, self.__extended_location)

    def GetFlags(self):
        """The underlying flags used to describe the symbol."""
        return self.__flags

    def GetType(self):
        """The type of the symbol as a human readable string."""
        return self.__type

    def GetName(self):
        """The name of the symbol."""
        return self.__name

    def GetHandle(self):
        """A handle that can be used with :meth:`~imgtec.codescape.Thread.Evaluate` for faster evaluations."""
        return self.__handle

    def GetLocation(self):
        """A string indicating the location of the evaluated expression,
        this may be a hex representation of the address or a register definition
        or an empty string if the symbol/result has no location."""
        return self.__location

    def GetTypeHandle(self):
        """A handle that may be passed to functions expecting TypeHandle's."""
        return self.__type_handle

    def GetSize(self):
        """The size of the type in bytes, e.g. for char the size is 1."""
        return self.__size

    def GetElementCount(self):
        """If the flags attribute indicates that the symbol is an array, this indicates
        the number of elements in the array."""
        return self.__element_count

    def GetDescription(self):
        """For Peripheral region symbols only this contains the description field."""
        return self.__description

    def GetExtendedLocation(self):
        """For Peripheral region symbols only this contains extended location information."""
        return self.__extended_location

    def GetIsHidden(self):
        """Only valid for FrameLocals. Whether the local variable is hidden by another variable in the same scope."""
        return self.__hidden

    def SetIsHidden(self, value):
        """Only valid for FrameLocals. Whether the local variable is hidden by another variable in the same scope."""
        self.__hidden = value

    def GetIsOptimisedOut(self):
        """True if the compiler has optimised the variable away."""
        return self.__optimised_out

    def GetIsWatchable(self):
        """The symbol is a valid target for a watch breakpoint."""
        return bool(self.__flags & SymbolFlags.watchable)

    def GetIsAssignable(self):
        """The symbol is a valid LHS for assignment."""
        return bool(self.__flags & SymbolFlags.assignable)

    def GetIsExpandable(self):
        """The symbol has members, is an array, or is a pointer to a non void type."""
        return bool(self.__flags & SymbolFlags.expandable)

    def GetIsArray(self):
        """The symbol is an array. The element_count contains the number of elements."""
        return bool(self.__flags & SymbolFlags.array)

    def GetIsSuc(self):
        """The symbol is a struct, union, or class."""
        return bool(self.__flags & SymbolFlags.suc)

    def GetIsEnum(self):
        """The symbol is an enum."""
        return bool(self.__flags & SymbolFlags.enum)

    def GetIsPointer(self):
        """The symbol is a pointer."""
        return bool(self.__flags & SymbolFlags.pointer)

    def GetIsReference(self):
        """The symbol is a reference."""
        return bool(self.__flags & SymbolFlags.reference)

    def GetIsFunction(self):
        """The symbol is a function."""
        return bool(self.__flags & SymbolFlags.function)

    def GetIsSigned(self):
        """The symbol is a signed fundamental type."""
        return bool(self.__flags & SymbolFlags.signed)

    def GetIsString(self):
        """The symbol is a ptr/array of char type."""
        return bool(self.__flags & SymbolFlags.string)

    def GetIsChar(self):
        """The symbol is a char type."""
        return bool(self.__flags & SymbolFlags.char)

    def GetIsRegister(self):
        """The symbol is a register."""
        return bool(self.__flags & SymbolFlags.register)
        
    flags = property(GetFlags)
    description = property(GetDescription)
    element_count = property(GetElementCount)
    extended_location = property(GetExtendedLocation)
    handle = property(GetHandle)
    is_array = property(GetIsArray)
    is_assignable = property(GetIsAssignable)
    is_char = property(GetIsChar)
    is_enum = property(GetIsEnum)
    is_expandable = property(GetIsExpandable)
    is_function = property(GetIsFunction)
    is_hidden = property(GetIsHidden)
    hidden = property(GetIsHidden, SetIsHidden)
    is_optimised_out = property(GetIsOptimisedOut)
    optimised_out = property(GetIsOptimisedOut)
    is_pointer = property(GetIsPointer)
    is_reference = property(GetIsReference)
    is_register = property(GetIsRegister)
    is_signed = property(GetIsSigned)
    is_string = property(GetIsString)
    is_suc = property(GetIsSuc)
    is_watchable = property(GetIsWatchable)
    location = property(GetLocation)
    name = property(GetName)
    size = property(GetSize)
    type = property(GetType)
    type_handle = property(GetTypeHandle)
