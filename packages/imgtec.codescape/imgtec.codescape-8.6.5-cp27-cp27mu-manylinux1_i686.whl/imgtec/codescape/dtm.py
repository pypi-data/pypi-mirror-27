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

class DTMRequest(object):
    """
    Allows definition of a DTM Request. To create an instance of
    this class use :py:meth:`imgtec.codescape.Thread.CreateDTMRequest`.

    * DTM is an acronym for DA Target Monitoring.
    * DTM will allow you to Read or Write Bulk Memory, Core Memory or
      Registers.
    * Data that is read will be placed into a channel.
    * Your DTM actions can be performed once, 'n' times or repeated forever
      with a specified period between each set of actions.
    * :py:meth:`imgtec.codescape.DTMRequest.Setup` configures the DTM Request. You then need to add the data
      requests you wish to perform as part of this request. Use
      :py:meth:`imgtec.codescape.DTMRequest.AddReadRequest` or :py:meth:`imgtec.codescape.DTMRequest.AddWriteRequest` to do this.
    * You can have many DTMRequests simultaneously active.
    * Each DTMRequest can have many Data Requests.

    .. note::

        If you setup too many requests then the DA will become less
        responsive.

    Example ::

        from imgtec import codescape
        thread = codescape.GetFirstThread()
        MyID = 0x01010101           # User ID - This ID is used to attach Data operations to this request.
                                    # This ID is the header to the data block (if requested)
        Period          = 1000      # 1000us or 1ms
        Repeat          = 0         # Forever
        ChannelNo       = 6
        Flags           = 0         # Request data in packet form - with header & timestamps (if specified).
        TimeStamp       = 3         # Request both Start and End Timestamps

        try:
            request = thread.CreateDTMRequest(MyID, Period, Repeat, ChannelNo, Flags, TimeStamp)

            # Read Bulk Memory Address 0x80000000 and place the 32 bit result up the channel
            PortID    = 0               # Bulk Memory read
            PortParam = 0               # not used for Bulk Memory read
            Address   = 0x80000000
            request.AddReadRequest(PortID, PortParam, Address)

            # Read register PC and place the 32 bit result up the channel
            PortID    = 1               # Core Reg read
            PortParam = 0               # not used for Core Reg read
            Register  = "PC"            # specifier for PC.0 (MetaIP)
            request.AddReadRequest(PortID, PortParam, Register)

            # Write 0x1 to address 0x00000100 in Core Memory 0x10
            PortID    = 2               # Core Memory
            UnitSpec  = 0x10            # Core memory unit specifier
            Address   = 0x00000100      # Address in that core memory unit
            Value     = 0x1             # Value to write
            request.AddWriteRequest(PortID, UnitSpecifier, Address, Value)

            thread.DTMStartAll()
        except codescape.Error as e:
            print e
    """

    def __init__(self, context, request_id):
        self.__context = context
        self.__request_id = request_id
        self.__deleted = False

    def AddReadRequest(self, port_id, port_param, address):
        """AddReadRequest(port_id, port_param, address)

        Adds a read data command to this request.

        :param port_id:

            ===== ===================
            Value Meaning
            ===== ===================
            0     Bulk Memory (RAM)
            1     Core Registers
            2     Core Memory
            ===== ===================

        :param port_param:

            * Bulk Memory: No effect

            * Core Registers

                ===== ===================================================
                Value Meaning
                ===== ===================================================
                0     Address field is TXREG port number e.g. 0x00000005
                1     Address field is a register name e.g. "PC"
                ===== ===================================================

                .. note:: If you need to read/write a core register on a different thread use.
                        RegName\@ThreadNumber e.g. "PC\@1"  is PC on thread 1.

            * Core Memory : Unit Specifier

                ===== ========================================
                Value Memory Type
                ===== ========================================
                0     Normal memory
                1     MiniM Data            {LTP/MTP/HTP}
                2     MiniM Code            {LTP/MTP/HTP}
                4     DspD0RamA             {MetaIP}
                5     DspD0RamB             {MetaIP}
                6     DspD1RamA             {MetaIP}
                7     DspD1RamB             {MetaIP}
                8     Data24Ram             {UCC310 and below}
                8     A-region RAM          {UCC320 and above}
                9     Data16Ram             {UCC310 and below}
                9     B-region RAM          {UCC320 and above}
                10    PeripheralRegisters   {UCC}
                12    System Bus Memory     {UCC}
                13    Bulk Memory           {UCC}
                14    Data24Ram Complex     {UCC310 and below}
                14    A-region RAM Complex  {UCC320 and above}
                15    Data16Ram Complex     {UCC310 and below}
                15    B-region RAM Complex  {UCC320 and above}
                16    JTAG Interface        {UCC320 and above}
                17    L-region RAM          {UCC320 and above}
                18    L-region RAM Complex  {UCC320 and above}
                ===== ========================================

        :param address:

            Address, TXREG port number or register name.

        .. note::

            You must configure this request using :py:meth:`imgtec.codescape.DTMRequest.Setup` before
            adding read or write requests.
        """
        if self.__deleted:
            raise Exception("DTMRequest must be setup first")
        if self.__context.DTMAddDataRequest(self.__context.target, self.__request_id, 0, port_id, port_param, address, 0) == 0:
            raise Exception("DTMAddDataRequest failed")

    def AddWriteRequest(self, port_id, port_param, address, value):
        """AddWriteRequest(port_id, port_param, address, value)

        Adds a write data command to this request.

        :param port_id:

            ===== ===================
            Value Meaning
            ===== ===================
            0     Bulk Memory (RAM)
            1     Core Registers
            2     Core Memory
            ===== ===================

        :param port_param:

            * Bulk Memory: No effect

            * Core Registers

                ===== ===================================================
                Value Meaning
                ===== ===================================================
                0     Address field is TXREG port number e.g. 0x00000005
                1     Address field is a register name e.g. "PC"
                ===== ===================================================

                .. note:: If you need to read/write a core register on a different thread use.
                        RegName\@ThreadNumber e.g. "PC\@1"  is PC on thread 1.

            * Core Memory : Unit Specifier

                ===== ========================================
                Value Memory Type
                ===== ========================================
                0     Normal memory
                1     MiniM Data            {LTP/MTP/HTP}
                2     MiniM Code            {LTP/MTP/HTP}
                4     DspD0RamA             {MetaIP}
                5     DspD0RamB             {MetaIP}
                6     DspD1RamA             {MetaIP}
                7     DspD1RamB             {MetaIP}
                8     Data24Ram             {UCC310 and below}
                8     A-region RAM          {UCC320 and above}
                9     Data16Ram             {UCC310 and below}
                9     B-region RAM          {UCC320 and above}
                10    PeripheralRegisters   {UCC}
                12    System Bus Memory     {UCC}
                13    Bulk Memory           {UCC}
                14    Data24Ram Complex     {UCC310 and below}
                14    A-region RAM Complex  {UCC320 and above}
                15    Data16Ram Complex     {UCC310 and below}
                15    B-region RAM Complex  {UCC320 and above}
                16    JTAG Interface        {UCC320 and above}
                17    L-region RAM          {UCC320 and above}
                18    L-region RAM Complex  {UCC320 and above}
                ===== ========================================

        :param address:

            Address, TXREG port number or register name.

        :param value:

            Value To write (only used if this is a write command).

        .. note::

            You must configure this request using :py:meth:`imgtec.codescape.DTMRequest.Setup` before
            adding read or write requests.
        """
        if self.__deleted:
            raise Exception("DTMRequest must be setup before calling AddWriteRequest")
        if self.__context.DTMAddDataRequest(self.__context.target, self.__request_id, 1, port_id, port_param, address, value) == 0:
            raise Exception("DTMAddDataRequest failed")

    def Setup(self, period, repeat, channel_no, flags=1, timestamp=0):
        """Setup(period, repeat, channel_no, flags=1, timestamp=0)

        Configures this DTM request, which can have data requests added with
        :py:meth:`imgtec.codescape.DTMRequest.AddReadRequest` and :py:meth:`imgtec.codescape.DTMRequest.AddWriteRequest`.

        :param period:

                The time period between gathering the DTM data (in uS).
                Currently this can only be set to even number of mS or 100uS (it will round up automatically).
                The current minimum time period is 1000us (1ms).

        :param repeat:

            The number of times to repeat the operation. 0 = Forever.

        :param channel_no:

            The Channel number to place the data in.

            .. note:: It is recommended that you use channels 6 to 31 (Channels 0 to 5 can be used by CODESCAPE).

        :param flags:

            ===== =============================================================
            Value Meaning
            ===== =============================================================
            0     Add the ID as a header to each data block.  Also include
                  timestamp data if requested in the TimeStamp parameter.
            1     Place only Raw Data in the channel i.e. no ID or TimeStamps.
            ===== =============================================================

        :param timestamp:

            A combination of none or more of the following bit patterns

            ===== ============================================
            Value Meaning
            ===== ============================================
            0x1   Include Start Timestamp in the output data.
            0x2   Include End Timestamp in the output data.
            ===== ============================================

            The TimeStamp parameter will be ignored unless the flags parameter
            is set to 0.


        This function will throw an exception if the DTMRequest with the RequestID already exists.
        The exception message is ::

          "Failed DTMRequestSetup : ID <id-number> already exists"

        If this function throws, you need to either change the UserID or if you
        a setting up the same DTMRequest again, then you will need to call
        either :py:meth:`imgtec.codescape.DTMRequest.Delete` or :py:meth:`~imgtec.codescape.Thread.DTMDeleteAll` to delete
        the previous request.

        """
        self.Delete()
        if self.__context.DTMRequestSetup(self.__context.target, self.__request_id, period, repeat, channel_no, flags, timestamp) == 0:
            raise Exception("DTMRequestSetup failed")
        self.__deleted = False

    def Delete(self):
        """Delete()

        Removes this request from the list of requests to be processed."""
        if not self.__deleted:
            self.__context.DTMDeleteRequest(self.__context.target, self.__request_id)
            self.__deleted = True
