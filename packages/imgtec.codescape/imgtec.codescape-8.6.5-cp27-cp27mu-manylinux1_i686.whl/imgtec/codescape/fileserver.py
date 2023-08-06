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

from da_exception import FileServerError

class FileServer(object):
    '''The fileserver provides the target access to the host computers filesystem.
    
    A target library must be used to provide access, this library is not 
    documented here.

    The fileserver can be configured to work in jailed or non-jailed mode.    
    
    Jailed mode
        When the Root is not empty then Root becomes the jailed root directory for the 
        File Server.  CWD becomes the current  working directory for the target.  Any 
        target operations attempting to access files outside of the Root will result 
        in a failure with errno set to ENOENT.  Moreover, the target will not be able 
        to chdir to a location outside of the root, and any absolute paths will be 
        adjusted to be relative to the root.

        ========== =========== ============== ========================================
        Root       CWD         Target path    Host file accessed/errno
        ========== =========== ============== ========================================
        /root      /           file.txt       /root/file.txt
        /root      /           ../file.txt    failure, errno = ENOENT
        /root      /           ../../file.txt failure, errno = ENOENT
        /root      /           dir/file.txt   /root/dir/file.txt
        /root      /           /file.txt      /root/file.txt
        /root      /cwd        file.txt       /root/cwd/file.txt
        /root      /cwd        dir/file.txt   /root/cwd/dir/file.txt
        /root      /cwd        ../file.txt    /root/file.txt
        /root      /cwd        ../../file.txt failure, errno = ENOENT
        /root      /cwd        /file.txt      /root/file.txt
        ========== =========== ============== ========================================

    Unjailed mode
        When the Root is empty then the fileserver operates in unjailed mode.
        
        In this case the path (:meth:`SetPath`) must be an absolute path, and becomes 
        the default path for the File Server. In unjailed mode relative file 
        operations on the target will use this as the starting point for relative 
        paths.  Absolute paths are allowed and are used unadjusted.

        Because the File Server provides both read and write access to the file 
        system, it is recommended that the user uses a non-empty Root in all new 
        applications, and makes sure that the target application does not use 
        absolute paths.
        
        ========== =========== ============== ===========================================
        Root       CWD         Target path    Host file accessed/errno
        ========== =========== ============== ===========================================
        <empty>    /root       file.txt       /root/file.txt
        <empty>    /root       ../file.txt    /file.txt
        <empty>    /root       ../../file.txt failure, errno=ENOENT
        <empty>    /root       dir/file.txt   /root/dir/file.txt
        <empty>    /root       /file.txt      /file.txt
        <empty>    /root/cwd   file.txt       /root/cwd/file.txt
        <empty>    /root/cwd   dir/file.txt   /root/cwd/dir/file.txt
        <empty>    /root/cwd   ../file.txt    /root/file.txt
        <empty>    /root/cwd   ../../file.txt /file.txt
        <empty>    /root/cwd   /file.txt      /file.txt
        ========== =========== ============== ===========================================

    Example python code::

            thread.fileserver.SetRoot("c:\\Home")
            thread.fileserver.SetPath("Directory")

    Example Target Code :

    .. code :: c++

            fd = open("test.txt", O_RDONLY); 	 // opens c:\\Home\\Directory\\test.txt
            fd = open("/test.txt", O_RDONLY);	 // opens c:\\Home\\test.txt
            fd = open("../test.txt", O_RDONLY);	 // opens c:\\Home\\test.txt
            fd = open("d:\\test.txt", O_RDONLY); // ERROR - ENOENT

    '''
    def __init__(self, context):
        self.__context = context
    
    def GetRoot(self):
        '''Get the jailed root for the file server.
        
        If the fileserver is not currently jailed then FileServerError will be 
        raised.
        '''
        if not self.GetJailed():
            raise FileServerError('Fileserver is not jailed and hence has no root')
        return self.__context.GetFileServerRoot(False, False)

    def SetRoot(self, root):
        '''Set the jailed root for the file server.'''
        self.__context.SetFileServerRoot(root, self.GetPath(), False)

    def GetPath(self):
        """Gets the current working directory for the File Server."""
        return self.__context.GetFileServerPath(False)

    def GetAbsolutePath(self, path='.'):
        '''Converts a target path into an absolute host path.
        
        This function uses the current File Server root and default path to convert
        a target path (such as might be passed to a File Server operation in target code)
        to an absolute path on the host machine.
        '''
        try:
            return self.__context.MakeFileServerPath(path, False)
        except Exception, e:
            raise FileServerError(str(e))

    def SetPath(self, new_path):
        """Sets the fileserver current working directory.
        
        If the fileserver is not jailed the path will be treated as an absolute 
        path to the current working directory, otherwise it will be treated as a 
        relative path to the jailed root.
        """
        if self.GetJailed():
            self.GetAbsolutePath(new_path)
            self.__context.SetFileServerRoot(self.GetRoot(), new_path, False)
        else:
            self.__context.SetFileServerPath(new_path, False)
    
    def GetJailed(self):
        """Return True if the fileserver is set up to be jailed."""
        return bool(self.__context.GetFileServerRoot(False, False))

    def SetJailed(self, jailed):
        """Sets the fileserver to be jailed to the fileservers current working directory. """
        if jailed:
            self.__context.SetFileServerRoot(self.GetPath(), '/', False)
        else:
            new_path = self.__context.MakeFileServerPath('.', False)
            self.__context.SetFileServerRoot('', new_path, False)
