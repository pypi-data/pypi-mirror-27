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

class Channel(object):
    """File-like interface to a Probe channel."""

    def __init__(self, context, channel_no):
        self.__context = context
        self.__channel_no = channel_no

    def __str__(self):
        return 'Channel %d' % self.__channel_no

    def Read(self):
        """Read the contents of the channel stream as a string.
        
        .. note :: Any null bytes embedded in the stream will be returned.
        """
        return self.__context.ChannelReadString(self.__channel_no)

    def Write(self, string):
        """Write a string to the channel.
        
        .. note :: Any null bytes embedded in the string will be written.
        """
        return self.__context.ChannelWriteString(self.__channel_no, string)

    def Flush(self):
        """Flush the channel.
        
        This continually reads data from the channel until no more is available.
        
        .. note :: This does not flush the write stream, the write stream is not buffered.
        """
        return self.__context.ChannelFlush(self.__channel_no)

    """ The following aliases are to provide a consistent interface with the python
    built-in file interface """
    read = Read
    write = Write
