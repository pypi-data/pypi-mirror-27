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

class SourceLine(object):
    """Represents a source line entry."""

    def __init__(self, source_file, line_number):
        self.__source_file = source_file
        self.__line_number = line_number

    def GetSourceFile(self):
        """The :class:`imgtec.codescape.SourceFile` that this line is associated with."""
        return self.__source_file

    def GetLineNumber(self):
        """The line number of the source line."""
        return self.__line_number

    def __get_source_line_info(self):
        try:
            all_source_line_info = self.source_file._get_source_line_info()
            source_lines_map = dict([(line_info[0], line_info) for line_info in all_source_line_info])
            source_line_info = source_lines_map[self.line_number]

            return bool(source_line_info[1]), source_line_info[2:]
        except Exception:
            return False, []

    def GetStartAddresses(self):
        """List of start addresses for this source line."""
        in_scope, addresses = self.__get_source_line_info()
        return addresses

    def GetInScope(self):
        """False if the source file is in an inactive overlay."""
        in_scope, addresses = self.__get_source_line_info()
        return in_scope

    def GetPath(self):
        """The path of the source entry in the executable."""
        return self.source_file.path

    in_scope = property(GetInScope)
    line_number = property(GetLineNumber)
    path = property(GetPath)
    source_file = property(GetSourceFile)
    start_addresses = property(GetStartAddresses)

class SourceFile(object):
    """Represents a source file entry.
    
    You can obtain a SourceFile reference from a :class:`~imgtec.codescape.Thread` ::
    
        thread = codescape.GetFirstThread()
        for source in thread.GetSourceFiles():
            print source.path, "first line:", source.start_line.line_number
            
        source_line = thread.GetSourceLineAt("main")
        print source_line.source_file.path
    
    """

    def __init__(self, context, handle, path, found_filename, start_line, end_line, filename, has_source_and_in_current_overlay, *extras):
        self.__context = context
        self.__handle = handle
        self.__path = path
        self.__found_filename = found_filename
        self.__start_line = start_line
        self.__end_line = end_line
        self.__filename = filename
        self.__has_source_and_in_current_overlay = has_source_and_in_current_overlay

    def _get_source_line_info(self):
        """ private method made available for SourceLine """
        return self.__context.GetSourceLineInformation(self.__handle, 0, 0xffffffff)

    def GetPath(self):
        """The path of the source entry in the executable."""
        return self.__path

    def GetSourceLines(self):
        """Return a list of  :class:`~imgtec.codescape.SourceLine` 
        instances with debug information attached."""
        try:
            source_line_info = self._get_source_line_info()
            line_numbers = [source_line[0] for source_line in source_line_info]
        except Exception:
            line_numbers = []

        return [self.GetLine(line_number) for line_number in line_numbers]

    def GetSourceLineNumbers(self):
        """Return all the line numbers which have debug information attached."""
        return [source_line.line_number for source_line in self.source_lines]

    def GetLine(self, line_number):
        """Returns the :class:`~imgtec.codescape.SourceLine` for the specified line."""
        return SourceLine(self, line_number)

    def GetStartLine(self):
        """Returns the :class:`~imgtec.codescape.SourceLine` for the first line."""
        return self.GetLine(self.__start_line)

    path = property(GetPath)
    source_lines = property(GetSourceLines)
    source_line_numbers = property(GetSourceLineNumbers)
    start_line = property(GetStartLine)
