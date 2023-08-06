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

import socket
import struct

#Provides Scan and Tapreset methods
class SocketDriver(object):

    # Constants
    SIGNALS_SERVER_MSG_IR = 0
    SIGNALS_SERVER_MSG_DR = 1
    SIGNALS_SERVER_MSG_SET_SIGNAL = 2
    SIGNALS_SERVER_MSG_GET_SIGNAL = 3

    SIGNAL_NTRST = 0x00
    SIGNAL_RESETOUT = 0x01
    SIGNAL_DBGREQ = 0x03

    SIGNAL_VALUE_OFF = 0
    SIGNAL_VALUE_LOW = 2
    SIGNAL_VALUE_HIGH = 3

    def __init__(self, port=44444, hostname='localhost'):
        try:
            self.sock = socket.create_connection((hostname, port))
        except socket.error as e:
            raise e.__class__('Failed to connect to %s:%d : %s' % (hostname, port, str(e)))

    def write_req(self, req):
        #Send a packet to the sim socket
        left = len(req)
        last = len(req)
        offset = 0
        while left != 0:
            numwritten = self.sock.send(req[offset:last])
            if numwritten <= 0:
                break
            left -= numwritten
            offset += numwritten
        return offset

    def do_recv(self, numbytes):
        left = numbytes
        chunklist = []
        while left != 0:
            chunk = self.sock.recv(left)
            if not chunk:
                break
            chunklist.append(chunk)
            left -= len(chunk)
        return bytearray(''.join(chunklist))

    def req_ir_dr(self, ir, numbits, val):
        fixed = struct.pack('!II', self.SIGNALS_SERVER_MSG_IR if ir else self.SIGNALS_SERVER_MSG_DR, numbits)
        variable = bytearray()
        left = numbits
        while left != 0:
            chunk = min(left, 8)
            byteval = val & 0xFF
            variable.append(byteval)
            val >>= 8
            left -= chunk
        return fixed + variable

    def resp_ir_dr(self, numbits):
        bytes = self.do_recv(8 + (numbits+7)/8)
        index = 0
        val = 0
        for b in bytes[8:]:
            val |= (b << (index*8))
            index += 1
        return val


    def resp_setsignal(self):
        bytes = self.do_recv(4)
        fields = struct.unpack_from('!I', bytes)
        return fields[0]

    def resp_getsignal(self):
        bytes = self.do_recv(8)
        fields = struct.unpack_from('!II', bytes)
        return fields[1]

    def req_setsignal(self, signal, val):
        fixed = struct.pack('!III', self.SIGNALS_SERVER_MSG_SET_SIGNAL, signal, val)
        return fixed

    def req_getsignal(self, signal):
        fixed = struct.pack('!II', self.SIGNALS_SERVER_MSG_GET_SIGNAL, signal)
        return fixed


    def systemreset(self):
        # drive rst signal low then high
        r = self.req_setsignal(self.SIGNAL_RESETOUT, self.SIGNAL_VALUE_LOW)
        self.write_req(r)
        self.resp_setsignal()
        r = self.req_setsignal(self.SIGNAL_RESETOUT, self.SIGNAL_VALUE_HIGH)
        self.write_req(r)
        self.resp_setsignal()

    def TapReset(self, type=None):
        # drive NTRST low then high
        r = self.req_setsignal(self.SIGNAL_NTRST, self.SIGNAL_VALUE_LOW)
        self.write_req(r)
        self.resp_setsignal()
        r = self.req_setsignal(self.SIGNAL_NTRST, self.SIGNAL_VALUE_HIGH)
        self.write_req(r)
        self.resp_setsignal()


    def Scan(self, irdata, drdata):
        # ir/dr data are binary strings
        ir_ret = None
        dr_ret = None

        if irdata:
            ir_ret = self.irdr(irdata, self.ir)

        if drdata:
            dr_ret = self.irdr(drdata, self.dr)
            #If we do a dr scan, return that
            return dr_ret
        else:
            #Otherwise return the result of the ir scan
            return ir_ret

    def irdr(self, data, op):
        #Generic conversion of binary strings to len/val
        ret = None
        num_bits = 0

        if data:
            num_bits = len(data)
            val      = int(data, 2)
            ret      = op(num_bits, val)

        #Return value is expected as a binary string
        #The response from the sim is always 16 bytes so we trim
        #the unused bits
        ret = "{0:b}".format(ret).rjust(num_bits, '0')

        if len(ret) > num_bits:
            #Char 0 is the msb, last char is the lsb
            ret = ret[len(ret)-num_bits:]
        return ret

    def ir(self, numbits, val):
        r = self.req_ir_dr(True, numbits, val)
        self.write_req(r)
        return self.resp_ir_dr(numbits)

    def dr(self, numbits, val):
        r = self.req_ir_dr(False, numbits, val)
        self.write_req(r)
        return self.resp_ir_dr(numbits)
