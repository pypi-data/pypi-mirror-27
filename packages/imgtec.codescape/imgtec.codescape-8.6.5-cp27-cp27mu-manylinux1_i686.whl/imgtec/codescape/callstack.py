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

from da_exception import FrameError
from da_symbol import Symbol
from da_types import Reliability

class Frame(object):
    """Represents a callstack Frame, a Frame can be obtained using :class:`~imgtec.codescape.Thread`'s 
    :meth:`~imgtec.codescape.Thread.GetFrame` method ::
    
        def arg_value(frame, arg):
            try:
                return hex(frame.Evaluate(arg.handle or arg.name))
            except Exception as e:
                return "?"    
            
        thread = codescape.GetFirstThread()
        frame = thread.GetFrame(level=0)
        args = frame.GetArguments()
        values = [arg_value(frame, x) for x in args]
        names = [x.name for x in args]
        names_values = ', '.join('%s=%s' % x for x in zip(names, values))
        print "%s(%s)" % (frame.name, names_values)

    """
    def __init__(self, context, level):
        self.__context = context
        self.__level = level

        init_data = self.__context.FrameDetails(level)
        self.__address = init_data[0]
        self.__name = init_data[1]
        self.__offset_from_name = init_data[2]
        self.__sym_reliability = Reliability(init_data[3])
        self.__is_interrupt = init_data[4]
        self.__is_guess = init_data[5]
        self.__return_pc = init_data[6]
        self.__is_inlined = init_data[7]
        
        self.__arguments = None

    def __repr__(self):
        if self.__arguments is None:
            args = '???'
        else:
            args = ', '.join(x.name for x in self.__arguments)            
        interrupt = '!' if self.is_interrupt else ''
        offset  = '+%d' % self.offset_from_name if self.offset_from_name else ''
        reliability = '' if self.sym_reliability == Reliability.known else '{%s}' % (self.sym_reliability,)
        return '0x%08x %s%s%s%s(%s)' % (self.address, interrupt, self.name, reliability, 
            offset, args)
        

    def GetAddress(self):
        """Address of the beginning of this frame."""
        return self.__address

    def GetName(self):
        """The name of the function.
        
        Under some circumstances this name may be an address.
        """
        return self.__name

    def GetOffsetFromName(self):
        '''Difference between the program counter in this frame and the address
        of the symbol given in :meth:`GetName`.'''
        return self.__offset_from_name

    def GetSymReliability(self):
        '''When the debug information is not enough Codescape will sometimes use
        code reading techniques to calculate the name and address of this frame.
        
        This is an instance of :class:`~imgtec.codescape.Reliability`.
        '''
        return self.__sym_reliability

    def GetIsInterrupt(self):
        """Whether the frame is an interrupt frame."""
        return self.__is_interrupt

    def GetIsGuess(self):
        """Whether details of this frame have been calculated using guessed 
        register information."""
        return self.__is_guess
        
    def GetIsInlined(self):
        """Whether the function is an instance of an inlined function."""
        return self.__is_inlined

    def GetReturnPC(self):
        """Address to which this frame will return."""
        return self.__return_pc

    def GetLocals(self):
        """Return the list of local :doc:`symbol` passed in this frame."""
        try:
            symbol_details = self.__context.FrameLocals(self.__level)
            return [Symbol(*details) for details in symbol_details]
        except Exception:
            return []

    def GetArguments(self):
        """Return the list of :doc:`symbol` passed into this frame as arguments."""
        if self.__arguments is None:
            symbol_details = self.__context.FrameArguments(self.__level)
            self.__arguments = [Symbol(*details) for details in symbol_details]
        return self.__arguments

    def Evaluate(self, expression, flags=0):
        """Evaluate an expression in the context of this frame."""
        symbol, value = self.__context.FrameEvaluateSymbol(self.__level, expression, 0xffffffff, 0, flags)
        return value

    def GetSymbol(self, expression, flags=0):
        """Returns a :class:`Symbol <imgtec.codescape.Symbol>` representing
        the type of the given expression on the current frame.
        """
        symbol, value = self.__context.FrameEvaluateSymbol(self.__level, expression, 0xffffffff, 0, flags)
        return Symbol(*symbol)

    def GetSymbolAndValue(self, expression, flags=0):
        """Returns a pair of (:class:`~imgtec.codescape.Symbol`, value)
        representing the type and result of evaluating the given expression on the
        current frame.

        The `flags` parameter enables additional options and can be one
        or more of the flags defined in imgtec.codescape.\ :class:`~imgtec.codescape.ExpressionFlags`.
        """
        symbol, value = self.__context.FrameEvaluateSymbol(self.__level, expression, 0xffffffff, 0, flags)
        return Symbol(*symbol), value
            
    def Assign(self, destination, source):
        """Assign evaluated `source` expression to evaluated `destination` 
        expression in the context of this frame.

        This method evaluates the `source` expression and writes the result
        to the location of the result of evaluating the `destination`
        expression.

        The destination must be an lvalue but may reside in a register, in
        memory, or even in a bitfield ::

          thread.Assign("Point.x", 100)
          thread.Assign("array[n]", "(unsigned char) Point.x")
          thread.Assign("argv[argc-1]", "&Person->name[0]")
        """
        result = self.__context.FrameAssignSymbol(self.__level, destination, source)
        error_message, last_value = result
        if error_message:
            raise FrameError(error_message)
        return last_value

    def SetCurrent(self):
        """Make this frame the current frame on its thread."""
        return self.__context.FrameSetCurrent(self.__level)

    address           = property(GetAddress)
    arguments         = property(GetArguments)
    is_guess          = property(GetIsGuess)
    is_inlined        = property(GetIsInlined)
    is_interrupt      = property(GetIsInterrupt)
    locals            = property(GetLocals)
    name              = property(GetName)
    offset_from_name  = property(GetOffsetFromName)
    return_pc         = property(GetReturnPC)
    sym_reliability   = property(GetSymReliability)
