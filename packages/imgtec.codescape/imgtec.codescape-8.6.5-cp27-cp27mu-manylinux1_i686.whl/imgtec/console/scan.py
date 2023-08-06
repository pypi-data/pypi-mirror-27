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

from imgtec.test import *
from imgtec.lib import rst
from imgtec.lib.namedbitfield import namedbitfield, compile_fields, Field
from imgtec.lib.bits import word_to_bits, bits_to_words, bits_to_word
from imgtec.console.support import *
from imgtec.console import results
from imgtec.console.tdd import CoreImgId, targetdata, TapType
from imgtec.console.dbudriver import *
from imgtec.console.generic_device import make_device_list
import itertools
import re
import struct
import time
from textwrap import dedent

__all__ = [
    'tap', 'tapi', 'tapd', 'devtap', 'devtapi', 'devtapd', 'pcsamp', 
    'configuretap', 'tckrate', 'tcktest', 'jtagchain', 'tapall', 'tapscan',

    'tapecr', 'tapdata', 'tapaddress', 'tapreg', 'tapboot', 'tapinfo',
    'dmseg', 'EnterDebug', 'ExitDebug', 'ReadDEPC', 'ReadConfigs', 
    'Read32', 'Write32', 'ReadRegs', 'JumpDEV', 'enterdebug', 'tcbcontrola', 
    'tcbcontrolb', 'tcbcontrolc', 'tcbcontrold', 'tcbcontrole', 'tcbdata', 
    'impcode', 'idcode', 'WriteDEPC', 'ReadRegister', 'WriteRegister',
    'SlaveAddr', 'ClusterAddr', 'RBAddr', 'RBData', 'VPEBoot', 'Control', 
    'DXAddr', 'DXData', 'RBHeader', 'RBPayload', 'FDC', 
    
    'configure_tap', 'enter_debug', 'tap_info',
    'tap_ecr', 'tap_data', 'tap_address', 'tap_reg', 'tap_boot',
    
    'mdhread', 'mdhwrite', 'tcktestmdh', 'mdhdevice',
    
#    'scandevices',
]

tcbcontrola = named('tcbcontrola')
tcbcontrolb = named('tcbcontrolb')
tcbcontrolc = named('tcbcontrolc')
tcbcontrold = named('tcbcontrold')
tcbcontrole = named('tcbcontrole')
tcbdata     = named('tcbdata')
impcode     = named('impcode')
idcode      = named('idcode')

class JtagSpeed(long):
    def __repr__(self):
        if self >= 1000000:
            return str(float(self)/1000000) + ' MHz'
        elif self >= 1000:
            return str(float(self)/1000) + ' KHz'
        else:
            return str(self) + ' Hz'
            
da_jtag_speeds = [
    JtagSpeed(20000000),
    JtagSpeed(10000000),
    JtagSpeed(5000000),
    JtagSpeed(2500000),
    JtagSpeed(1250000),
    JtagSpeed(625000),
    JtagSpeed(312000),
    JtagSpeed(156000),
]

sp_jtag_speeds = [
    JtagSpeed(30000000),
    JtagSpeed(20000000),
    JtagSpeed(10000000),
    JtagSpeed(5000000),
    JtagSpeed(2500000),
    JtagSpeed(1250000),
    JtagSpeed(1000000),
    JtagSpeed(500000),
    JtagSpeed(250000),
    JtagSpeed(100000),
    JtagSpeed(50000),
    JtagSpeed(25000),
    JtagSpeed(10000),
    JtagSpeed(5000),
    JtagSpeed(2000),
]

TEST_LOOPS = 1000

# Instruction Register values
IR_JTAG_ID          = 0x01
IR_MIPS_IMPCODE     = 0x03
IR_MIPS_ADDRESS     = 0x08
IR_MIPS_DATA        = 0x09
IR_MIPS_CONTROL     = 0x0a
IR_MIPS_ALL         = 0x0b
IR_MIPS_EJTAGBOOT   = 0x0c
IR_MIPS_NORMALBOOT  = 0x0d
IR_MIPS_FASTDATA    = 0x0e
IR_MIPS_TCBCONTROLA = 0x10
IR_MIPS_TCBCONTROLB = 0x11
IR_MIPS_TCBDATA     = 0x12
IR_MIPS_TCBCONTROLC = 0x13
IR_MIPS_PCSAMPLE    = 0x14
IR_MIPS_TCBCONTROLD = 0x15
IR_MIPS_TCBCONTROLE = 0x16
IR_MIPS_FDC         = 0x17

IR_MIPS_DBU_SLAVEADDR     = 0x4
IR_MIPS_DBU_CLUSTERADDR   = 0x5
IR_MIPS_DBU_RBADDR        = 0x6
IR_MIPS_DBU_RBDATA        = 0x7
IR_MIPS_DBU_VPEBOOT       = 0x9
IR_MIPS_DBU_CONTROL       = 0xA
IR_MIPS_DBU_DXADDR        = 0xB
IR_MIPS_DBU_DXDATA        = 0xC
IR_MIPS_DBU_RB_HEADER     = 0xD
IR_MIPS_DBU_RB_PAYLOAD    = 0xE
IR_MIPS_DBU_RB_BUSERRINFO = 0xF
IR_MIPS_DBU_FDC           = 0x17

IR_MIPS_MDH_CONTROL    = 0x4
IR_MIPS_MDH_DEVICEADDR = 0x5
IR_MIPS_MDH_APBACCESS  = 0x6
IR_MIPS_MDH_POWERSTATE = 0x7
IR_MIPS_MDH_JTAGSELECT = 0x8
IR_MIPS_MDH_DBG_IN     = 0x9
IR_MIPS_MDH_DBG_OUT    = 0xA

IR_MIPS_MDH_APB_IDCODE     = 0x01
IR_MIPS_MDH_APB_IMPCODE    = 0x02
IR_MIPS_MDH_APB_ADDRESS    = 0x03
IR_MIPS_MDH_APB_DATA       = 0x04
IR_MIPS_MDH_APB_CONTROL    = 0x05
IR_MIPS_MDH_APB_DRSEG_ADDR = 0x06
IR_MIPS_MDH_APB_DRSEG_DATA = 0x07
IR_MIPS_MDH_APB_PCSAMPLE1  = 0x08
IR_MIPS_MDH_APB_PCSAMPLE2  = 0x09
IR_MIPS_MDH_APB_FDCSTATUS  = 0x0a
IR_MIPS_MDH_APB_FDCDATA    = 0x0b
IR_MIPS_MDH_APB_DBGOUT     = 0x0c

def mips_ir_to_apb(ir):
    new_ir = {
        IR_JTAG_ID      : IR_MIPS_MDH_APB_IDCODE,
        IR_MIPS_IMPCODE : IR_MIPS_MDH_APB_IMPCODE,
        IR_MIPS_ADDRESS : IR_MIPS_MDH_APB_ADDRESS,
        IR_MIPS_DATA    : IR_MIPS_MDH_APB_DATA,
        IR_MIPS_CONTROL : IR_MIPS_MDH_APB_CONTROL,
        }.get(ir, ir)
    return new_ir
        
IR_IMG_JTAG_PNP   = 0xFFFFFFFC
IMG_JTAG_PNP_ID   = 0x9e7

JTAG_TYPE_DBU = 3
JTAG_TYPE_MDH = 4

def _prepare_tap(bitcount_value_pairs):
    """Convert a string "(<bitcount> <value>)+" into pairs of (bitcount, value).

    >>> _prepare_tap("")
    []
    >>> _prepare_tap("5 0x12 7 0x15")
    [(5, 18), (7, 21)]
    >>> _prepare_tap("1 0x12 11 0x15")
    [(1, 18), (11, 21)]
    >>> _prepare_tap("1 0x12 0x11 0x15 1")
    Traceback (most recent call last):
    ...
    ValueError: Invalid (bitcount, value) pair: 1 0x12 0x11 0x15 1
                                                            here ^
    >>> _prepare_tap("1 0x12 1 0b2 0x15 1")
    Traceback (most recent call last):
    ...
    ValueError: Invalid literal: 1 0x12 1 0b2 0x15 1
                                     here ^
    >>> _prepare_tap("1 0x12 0 0 0x15 1")
    Traceback (most recent call last):
    ...
    ValueError: Invalid bit length: 1 0x12 0 0 0x15 1
                                      here ^
    """
    r = re.compile(r'\s*((?:0[xbo])?[0-9a-f]+)\s+((?:0[xbo])?[0-9a-f]+)\s*', re.I)
    pos = 0
    pairs = []
    while pos != len(bitcount_value_pairs):
        try:
            m = r.match(bitcount_value_pairs, pos)
            bitlength = int(m.group(1), 0)
            pos = m.start(2)
            value = int(m.group(2), 0)
        except AttributeError:
            raise ValueError("Invalid (bitcount, value) pair: " + bitcount_value_pairs + '\n' +
                 '                                       ' + ' ' * pos + 'here ^')
        except ValueError:
            raise ValueError("Invalid literal: " + bitcount_value_pairs + '\n' +
                      '                        ' + ' ' * pos + 'here ^')
        if bitlength <= 0:
            raise ValueError("Invalid bit length: " + bitcount_value_pairs + '\n' +
                      '                           ' + ' ' * m.start(1) + 'here ^')
        pos = m.end()
        pairs.append((bitlength, value))
    return pairs

def anytap(da, ir, dr):
    """Perform a scan.

    >>> class _Loopback(object):
    ...     def Scan(self, a, b):
    ...         return (b or a).replace(' ', '')

    >>> anytap(_Loopback(), '', "5 0x1f 5 0x1f")
    [31, 31]
    >>> anytap(_Loopback(), '5 0x1f 5 0x1f', '1 1 1 1')
    [1, 1]
    >>> anytap(_Loopback(), '1 1 1 1', "5 0x1f 5 0x1f")
    [31, 31]
    """
    ir_pairs = _prepare_tap(ir)
    dr_pairs = _prepare_tap(dr)
    ir_bits  = ' '.join(word_to_bits(value, width) for width, value in ir_pairs)
    dr_bits  = ' '.join(word_to_bits(value, width) for width, value in dr_pairs)
    bits = da.Scan(ir_bits, dr_bits)
    pairs = dr_pairs or ir_pairs
    widths, _values = zip(*pairs)
    return bits_to_words(bits, widths)

def devanytap(da, tap_index, ir_widths, ir=None, dr_width=None, dr=None):
    """Perform a scan on a single device.

    >>> class _Loopback(object):
    ...     def Scan(self, a, b):
    ...         return (b or a).replace(' ', '')

    >>> devanytap(_Loopback(), 0, [5, 5], None, 16, 0x2a)
    42
    >>> devanytap(_Loopback(), 0, [5, 5], 0x1f)
    31
    >>> devanytap(_Loopback(), 0, [5],    0x1f, 16, 0x2a)
    42
    """
    left = tap_index
    right = len(ir_widths) - tap_index - 1
    ir_vals, dr_vals = '', ''
    if ir is not None:
        ir_words  = [0xffffffff] * left + [ir] + [0xffffffff] * right
        ir_vals = ' '.join("%d 0x%x" % (w, v) for w, v in zip(ir_widths, ir_words))
    if dr is not None:
        dr_words  = [0]    * left + [dr]       + [0]    * right
        dr_widths = [1]    * left + [dr_width] + [1]    * right
        dr_vals = ' '.join("%d 0x%x" % (w, v) for w, v in zip(dr_widths, dr_words))

    return anytap(da, ir_vals, dr_vals)[tap_index]


@command()
def tapscan(ir_bitcount_values, dr_bitcount_values, device=None):
    """Manipulate the JTAG instruction and data registers.
    
    The tapi command modifies the instruction register, and returns the bits 
    shifted out.

    The tapd command modifies the data register, and returns the bits 
    shifted out.

    The tapscan command modifies the instruction register, then the data register, 
    and returns the bits shifted out of the data register.

    The parameters should be a string of whitespace separated
    (bitcount, value) pairs.

      >>> tapi("5 0x1f 5 0x1f")           # put all IR's into bypass
      [0x1, 0x1]
      >>> tapd("1 1 1 1")                 # test the bypass in DR
      [0x1, 0x1]
      >>> tapscan("5 0x1f 5 0x1f", "1 1 1 1") # put IR's into bypass AND test it
      [0x1, 0x1]
    
    The result is formatted into words based on the bit count of the 
    appropriate incoming data.
    """
    return results.IntListResult(anytap(device.da, ir_bitcount_values, dr_bitcount_values))

@command(see='tapscan')
def tapi(bitcount_values, device=None):
    return results.IntListResult(anytap(device.da, bitcount_values, ''))

@command(see='tapscan')
def tapd(bitcount_values, device=None):
    return results.IntListResult(anytap(device.da, '', bitcount_values))
  

@command(aliases='configuretap')
def tap(tap_index=None, ir_lengths=None, device=None):
    """Configure the tap for use with :func:`devtap` and other tap commands.
    
    When the probe is in scanonly mode you must select the tap to operate on,
    the topology is detected using the ``jtagchain`` command.
    
    When the probe is in autodetected or table mode then the tap and topology
    for tapxxx() commands are automatically selected for the current device, and 
    you do not need to call tap.      
    
    For example, on a a 2-VPE MIPS32 system when in scan only mode you configure
    the tap like this:    
    
     [tap 0 of 2] >>> tap(1)
     [tap 1 of 2] >>> tapecr()  # get the ECR register from tap #1
     ...
    
    However when in autodetected/table mode you do not normally need to 
    use ``tap``, the tap_index will be set automatically ::
    
     [tap 1 of 2] >>> autodetect()
     [s0c0v0] >>> tapecr() # get the ECR register from tap #0
     ...
     [s0c0v0] >>> device(s0c0v1) 
     [s0c0v1] >>> tapecr() # get the ECR register from tap #1
    
    You can also override the automatic tap number using tap, in this case the 
    prompt will change to show that the current device tap is overridden:
    
     [s0c0v1] >>> tap(0)# get the ECR register from tap #1
     [s0c0v1 tap 0 of 2 active] >>> tapecr() # get the ECR register from tap #0
     ...
     [s0c0v1 tap 0 of 2 active] >>> device(s0c0v0)
     [s0c0v0 tap 0 of 2 active] >>> tapecr() # also get the ECR register from tap #0
    
    To restore automatic tap indexing use tap # -1 ::

     [s0c0v0 tap 0 of 2 active] >>> tap(-1)
     [s0c0v0] >>> tapecr() 

    When in scanonly mode the topology of the jtag chain will be automatically 
    detected using the jtagchain command, in the very rare situation that this 
    fails for some reason then this can be specified using the ``ir_lengths`` 
    parameter.
    
    Note: In previous versions of Codescape Console this command was called 
          configuretap, and the tap command performed a combined IR/DR scan.
          The old tap command is now renamed to :func:`tapscan`.
    """
    if isinstance(tap_index, basestring) and isinstance(ir_lengths, basestring):
        ir_bitcount_values, dr_bitcount_values = tap_index, ir_lengths
        return tapscan(ir_bitcount_values, dr_bitcount_values, device=device)    
        
    p = device.probe
    if tap_index is None:
        return p.tap_index
    if ir_lengths is None:
        if not p.ir_lengths:
            td = targetdata(device)
            p.ir_lengths = _jtag_chain_from_target_data(td)        
        ir_lengths = p.ir_lengths
    if tap_index >= len(ir_lengths) or tap_index < -1:
        s = 's' if len(ir_lengths) != 1 else ''
        raise ValueError("Index %d out of range, this probe has only %d tap%s" % 
                            (tap_index, len(ir_lengths), s))
    p.tap_index, p.ir_lengths = tap_index, ir_lengths
    
configuretap = tap
    
def _jtag_chain_from_target_data(td):
    return list(itertools.chain.from_iterable([s.ir_length]*s.taps_per_soc for s in td.socs))

def _check_config(device, cmd):
    err = "Please use tap or jtagchain before " + cmd + "."
    if device.probe.tap_index == -1 and device.tiny.GetDAMode() in ["autodetected", "table"] and len(make_device_list(device)):
        td = targetdata(device)
        try:
            tap_index = get_tap_index(td, device)
        except RuntimeError:
            raise RuntimeError("Detection of tap index failed. " + err)
       
        #A single tap command may call _check_config multiple times
        
        if not device.probe.ir_lengths:
            device.probe.ir_lengths = _jtag_chain_from_target_data(td)
        return tap_index
    else:
        if not device.probe.ir_lengths:
            raise RuntimeError(err)
        return 0 if device.probe.tap_index == -1 else device.probe.tap_index
            
@command()
def devtap(ir_value, dr_bitcount, dr_value, device=None):
    """Manipulate the JTAG instruction and data register of a single tap.
    
    :func:`tap` or :func:`jtagchain` must have been called before
    using these commands.

    The devtapi command modifies the instruction register, and returns the bits
    shifted out.

    The devtapd command modifies the data register, and returns the bits
    shifted out.

    The devtap command modifies the instruction register, then the data register,
    and returns the bits shifted out of the data register.

      >>> tap(1, [5, 5])     # Select the second tap of two
      >>> devtapi(5, 0x0a)        # Select ECR
      0x00000001
      >>> devtapd(32, 0x8004d000) # Set ECR.EjtagBrk to signal a dint
      0x0000c000    
    
    This can also be done as one operation::

      >>> devtap(0x0a, 32, 0x8004d000) # Select ECR and set ECR.EjtagBrk to signal a dint
      0x0000c000
      
    In this case the length of the IR scan is taken from the tap or 
    jtagchain command.
    
    The result is the data shifted out of the data as an integer.
    """
    p = device.probe
    tap_index = _check_config(device, 'devtap')
    return results.IntResult(devanytap(p.da, tap_index, p.ir_lengths, ir_value, dr_bitcount, dr_value))
    
@command(see='devtap')
def devtapi(bitcount, value, device=None):
    p = device.probe
    tap_index = _check_config(device, 'devtapi')
    if bitcount is not None and bitcount != p.ir_lengths[tap_index]:
        raise ValueError("Inconsistent tap length for tap %d" % tap_index)
    return results.IntResult(devanytap(p.da, tap_index, p.ir_lengths, value))
    
@command(see='devtap')
def devtapd(bitcount, value, device=None):
    p = device.probe
    tap_index = _check_config(device, 'devtapd')
    size = (bitcount + 7) // 8
    return results.IntResult(devanytap(p.da, tap_index, p.ir_lengths, None, bitcount, value), size=size)
    
def hz_to_khz(val):
    return (val + 500) // 1000
    
@command()
def tckrate(value=None, device=None):
    """Gets/sets the JTAG clock frequency in Hz.

    Valid frequencies are: 

    ========= ========
    Frequency    Value   
    ========= ========
    20MHz     20000000  
    10MHz     10000000  
    5MHz       5000000  
    2.5MHz     2500000  
    1.25MHz    1250000  
    625kHz      625000  
    312kHz      312000  
    156kHz      156000  
    ========= ========

    If a frequency is specified that is not supported, the next slowest speed is
    used. The return value can be used to determine the actual frequency set.
    
    >>> tckrate(158000)
    156000
    
    The command :func:`tcktest` can set the clock frequency automatically
    """
    if value is None:
        khz = device.da.GetJTAGClock()
    else:
        khz = device.da.SetJTAGClock(hz_to_khz(value))
    device.probe._clock  = khz
    return JtagSpeed(int(khz * 1000))
    
ecr_fields = compile_fields(dedent('''\
    Rocc     31
    Psz      30 29
    Resv     28 24
    VPED     23
    Doze     22
    Halt     21
    PerRst   20
    PRnW     19
    PrAcc    18
    Resv     17
    PrRst    16
    ProbEn   15
    ProbTrap 14
    IsaOn    13
    EjtagBrk 12
    Resv     11 4
    Dm       3
    Resv     2 0''').splitlines())

EcrValue = namedbitfield('EcrValue', ecr_fields, show_raw_value=True)

# Some useful constant values for ECR
ecrReadM     = EcrValue(Rocc=1, ProbEn=1, ProbTrap=1, PrAcc=1)
ecrCompleteM = EcrValue(Rocc=1, ProbEn=1, ProbTrap=1)
ecrBreakM    = EcrValue(Rocc=1, ProbEn=1, ProbTrap=1, PrAcc=1, EjtagBrk=1)
ecrAckResetM = EcrValue(        ProbEn=1, ProbTrap=1, PrAcc=1)

ACK_RESET_TIMEOUT =     2.0 # in seconds
ENTER_DEBUG_TIMEOUT =   0.5 # in seconds

ImpCodeValue = namedbitfield('ImpCodeValue', compile_fields('''\
    EJTAGVer 31 29
    R4kR3k   28
    DINTsup  24
    ASIDsize 22 21
    MIPS16e  16
    NoDMA    14
    Type     13 11
    TypeInfo 10 1
    MIPS64   0'''.splitlines()), show_raw_value=True)
    
IdCodeValue = namedbitfield('IdCodeValue', compile_fields('''\
    Version    31 28
    PartNumber 27 12
    ManufID    11 1
    One        0'''.splitlines()), show_raw_value=True)    


TCBControlAValue = namedbitfield('TCBControlAValue', compile_fields('''\
        SyPExt 31 30
        Impl   29 
        CID_En 28
        UTD_En 27
        _0     26
        VModes 25 24
        ADW    23
        SyP    22 20
        TB     19
        IO     18
        D      17
        E      16
        S      15
        K      14
        U      13
        ASID   12 5
        G      4
        TFCR   3
        TLSM   2
        TIM    1
        On     0'''.splitlines()))


TCBControlBValue = namedbitfield('TCBControlBValue', compile_fields('''\
        WE         31
        Impl       30 28
        TWSrcWidth 27 26
        REG        25 21
        WR         20
        STCE       19
        TRPAD      18
        FDT        17
        RM         16
        TR         15
        BF         14
        TM         13 12
        TLSIF      11
        CR         10 8
        Cal        7
        TWSrcVal   6 3
        CA         2
        OfC        1
        EN         0'''.splitlines()))

TCBControlCValueMode = namedbitfield('TCBControlCValueMode', [
    ('pc', 0),
    ('la', 1), # Load address
    ('sa', 2), # Store address
    ('ld', 3), # Load data
])

TCBControlCValue = namedbitfield('TCBControlCValue', [
        ('E_ASID',       31,  30),
        ('NumDO',        29,  28),
        ('Mode',         27,  23, TCBControlCValueMode),
        ('pc', 23),
        ('la', 24), # Load address
        ('sa', 25), # Store address
        ('ld', 26), # Load data
        ('sd', 27), # Store data
        ('CPUvalid',     22),
        ('CPUid',        21,  14),
        ('TCvalid',      13),
        ('TCnum',        12,  5),
        ('TCbits',       4, 2),
        ('MTtraceType',  1),
        ('MTtraceTC',    0)])
        
TCBControlDValue = namedbitfield('TCBControlDValue', compile_fields('''\
        MMID        31 0
        P7_CTL      31 30
        P6_CTL      29 28
        P5_CTL      27 26
        P4_CTL      25 24
        P3_CTL      23 22
        P2_CTL      21 20
        P1_CTL      19 18
        P0_CTL      17 16
        Reserved    15 12
        TWSrcVAl    11 8
        WB          7
        ST_En       6
        IO          5
        TLev        4 3
        AE          2
        Core_CM_En  1
        CM_En       0'''.splitlines()))

TCBControlEValue = namedbitfield('TCBControlEValue', compile_fields('''\
        _0          31 27
        GM          26
        TNUND       25
        MSA_En      24
        MSA         23
        GV          22
        GuestID     21 14
        _0          13
        TrIDLE      8
        _0          7  6
        PeCOvf      5
        PeCFCR      4
        PeCBP       3
        PeCSync     2
        PeCE        1
        PeC         0'''.splitlines()))
        
MDHControl = namedbitfield('MDHControl', compile_fields('''\
        JTAGDevices 12 7
        APBDevices  6 1
        AbortAPB    0'''.splitlines()))
        
DeviceAddr = namedbitfield('DeviceAddr', compile_fields('''\
        addr 31 7'''.splitlines()))
        
APBAccessIn = namedbitfield('APBAccessIn', compile_fields('''\
        data    38 7
        addr    6 2
        RnW     1
        execute 0'''.splitlines()))
        
APBAccessOut = namedbitfield('APBAccessOut', compile_fields('''\
        data       38 7
        error_code 6 2
        ok         1
        valid      0'''.splitlines()))

PCSampleValue = namedbitfield('PCSampleValue', compile_fields('''\
    PC    32 1
    New   0'''.splitlines()))
        
pcsamp = named('pcsamp')
@command(register=[namedstring(tcbcontrola), namedstring(tcbcontrolb), namedstring(tcbcontrolc),
                   namedstring(tcbcontrold), namedstring(tcbcontrole), namedstring(tcbdata),
                   namedstring(impcode), namedstring(idcode), namedstring(pcsamp)])
def tapreg(register='tcbcontrola', value=None, width=32, device=None):
    """Read or write one of the the eJTAG registers.
    
    Valid registers are show below.
    
    >>> jtagchain()
    >>> tapreg(impcode)
    0x60414000
    EJTAGVer R4kR3k DINTsup ASIDsize MIPS16e NoDMA Type TypeInfo MIPS64
    3        0      0       2        1       1     0    0        0
    >>> tapreg(impcode).MIPS64
    0L
    >>> tapreg(idcode)
    0x1fa1166d
    Version PartNumber ManufID One
    1       fa11       336     1
    >>> tapreg(idcode).Version
    1L

    At present this command will display registers of the selected TAP only, use
    :func:`tap` to change the current device.
    """
    
    def SizedIntResult(bits):
        return lambda x: results.IntResult(x, size=(bits+7)//8)
    
    regs = dict(
        tcbcontrola=(IR_MIPS_TCBCONTROLA, TCBControlAValue, True, 32),
        tcbcontrolb=(IR_MIPS_TCBCONTROLB, TCBControlBValue, True, 32),
        tcbcontrolc=(IR_MIPS_TCBCONTROLC, TCBControlCValue, True, 32),
        tcbcontrold=(IR_MIPS_TCBCONTROLD, TCBControlDValue, True, 32),
        tcbcontrole=(IR_MIPS_TCBCONTROLE, TCBControlEValue, True, 32),
            tcbdata=(IR_MIPS_TCBDATA,     SizedIntResult(width), True, width),
            impcode=(IR_MIPS_IMPCODE,     ImpCodeValue,     False, 32),
             idcode=(IR_JTAG_ID,          IdCodeValue,      False, 32),
             pcsamp=(IR_MIPS_PCSAMPLE,    PCSampleValue,    False, 41),
             
          slaveaddr=(IR_MIPS_DBU_SLAVEADDR,     SlaveAddr,    True,  24),
        clusteraddr=(IR_MIPS_DBU_CLUSTERADDR,   ClusterAddr,  True,  24),
             rbaddr=(IR_MIPS_DBU_RBADDR,        RBAddr,       True,  24),
             rbdata=(IR_MIPS_DBU_RBDATA,        RBData,       True,  66),
            vpeboot=(IR_MIPS_DBU_VPEBOOT,       VPEBoot,      True,  32),
            control=(IR_MIPS_DBU_CONTROL,       Control,      True,  32),
             dxaddr=(IR_MIPS_DBU_DXADDR,        DXAddr,       True,  24),
             dxdata=(IR_MIPS_DBU_DXDATA,        DXData,       True,  66),
           rbheader=(IR_MIPS_DBU_RB_HEADER,     RBHeader,     False, 64),
          rbpayload=(IR_MIPS_DBU_RB_PAYLOAD,    RBPayload,    False, 64),
                fdc=(IR_MIPS_DBU_FDC,           FDC,          True,  38),
        rbbuserrinfo=(IR_MIPS_DBU_RB_BUSERRINFO, SizedIntResult(64), False, 64),
            
        #because the DBU also has a control in a different place
           mdhcontrol=(IR_MIPS_MDH_CONTROL,    MDHControl,           True,  32),
           deviceaddr=(IR_MIPS_MDH_DEVICEADDR, DeviceAddr,           True,  32),
            apbaccess=(IR_MIPS_MDH_APBACCESS,  APBAccessOut,         True,  39),
           powerstate=(IR_MIPS_MDH_POWERSTATE, SizedIntResult(32), False, 32),
           jtagselect=(IR_MIPS_MDH_JTAGSELECT, SizedIntResult(32), True,  32),
                dbgin=(IR_MIPS_MDH_DBG_IN,     SizedIntResult(32), True,  32),
               dbgout=(IR_MIPS_MDH_DBG_OUT,    SizedIntResult(32), True,  32),
    )
    
    try:
        ir, type, writeable, width = regs[register]        
    except KeyError:
        raise RuntimeError("Unknown register %s" % (register,))
    _check_config(device, 'tapreg')
    if value is not None and not writeable:
        raise RuntimeError("Register %s is readonly" % (register,))
    oldvalue = type(devtap(ir, width, value or 0, device=device))
    if value is None:
        if writeable: # Need to put it back as we can't do passive reads
            devtap(ir, width, oldvalue, device=device)
        return oldvalue
        
def get_tap_type(device):
    try:
        return device.probe.tap_types[device.probe.tap_index]
    except (AttributeError, IndexError):
        return None

@command()
def tapecr(value=None, device=None):
    """Read and write the current value of the eJTAG Control Register(ECR).
    
    >>> tapecr()
    0x4004c008L
    Rocc Psz Resv VPED Doze Halt PerRst PRnW PrAcc Resv PrRst ProbEn ProbTrap IsaOn EjtagBrk Resv Dm Resv
    0    2   0    0    0    0    0      0    1     0    0     1      1        0     0        0    1  0
    
    >>> hex(tapecr()) # the result is a long, so can be printed, or used as a normal long
    '0x4004c008L'
    >>> tapecr().Psz  # or the fields can be named
    2L
    
    Without a given value the value 0x8004c000 is written, as this performs a non-disruptive read.

    At present this command will display the current ECR of the selected TAP only, use
    :func:`tap` to change the current device.
    """
    _check_config(device, 'tapecr')
    if value is None:
        value = ecrReadM
        
    if get_tap_type(device) == JTAG_TYPE_MDH:
        val = tapecr_mdh(device, value=value)
    else:
        val = long(devtap(IR_MIPS_CONTROL, 32, value, device=device))
        
    return EcrValue(val)
    
def tapecr_mdh(device, value=None):
    ir = mips_ir_to_apb(IR_MIPS_CONTROL)
    ret = mdh_transaction(device.probe, ir, None)
    
    if value is not None:
        mdh_transaction(device.probe, ir, value)
        
    return ret
    
@command()
def tapall(cmd, *args, **kwargs):
    """Issue a command to all taps.
    
    Run ``cmd(*args, **kwargs)`` on all taps.
    
    The python syntax ``cmd(*args, **kwargs)`` forwards all arguments from tapall
    after the cmd parameter onto cmd, for example::
      
        tapall(tapboot, 'ejtagboot')
        
    will call ``tapboot('ejtagboot')`` for each tap on the scan chain.
    
    The return type is a list of the results of each command.  e.g. 
    ``tapall(tapecr)`` returns a list of ecr registers on all taps.
    """
    p = Command.current
    _check_config(p, 'tapall')
    old = p.tap_index
    res = results.AllResult()
    try:
        for n in range(len(p.ir_lengths)):
            name = 'tap %d of %d' % (n, len(p.ir_lengths))
            p.tap_index = n
            try:
                res.add(name, cmd(*args, **kwargs))
            except Exception as e:
                res.add(name, e)
    finally:
        tap(old)
    if res.any_valid():
        return res

reset_types = [
    namedstring(normalboot),
    namedstring(ejtagboot),
    namedstring(hard_halt),
    namedstring(hard_run),
    namedstring(hard_all_halt),
    namedstring(hard_all_run),
]

@command(type=reset_types)
def tapboot(type='ejtagboot', device=None):
    """Issue a ejtagboot or normalboot tap instruction.
    
    Note this does not actually reset the target.
    
    hard_halt is equivalent to ejtagboot, and hard_run is equivalent to normalboot.
    The _all_ variants issue the command to all taps.
        
    """
    _check_config(device, 'tapboot')
    valid = [str(k) for k, _v in reset_types]
    if type not in valid:
        raise ValueError("Expected one of {%s} in 'type' parameter" % ', '.join(valid))
        
    normaliser = dict(hard_halt='ejtagboot', hard_run='normalboot', 
                      hard_all_halt='ejtagboot', hard_all_run='normalboot')
    normalised = normaliser.get(type, type)
    do_all = '_all_' in type
    if get_tap_type(device) == JTAG_TYPE_MDH:        
        if do_all:
            tapall(tapboot_mdh, device, normalised == 'ejtagboot')
        else:
            tapboot_mdh(device, normalised == 'ejtagboot')
    else:
        cmd = IR_MIPS_EJTAGBOOT if normalised == 'ejtagboot' else IR_MIPS_NORMALBOOT
        if do_all:
            values = ' '.join('%d 0x%x' % (l, cmd) for l in device.probe.ir_lengths)
            tapi(values, device)
        else:
            devtapi(None, cmd, device=device)
        
def tapboot_mdh(device, ejtagboot):
    original = tapecr_mdh(device)
    if ejtagboot:
        original |= 1
    else:
        original &= ~1
    tapecr_mdh(device, value=original)

def check_ir_return(ir, device):
    if ir != 1 and not device.probe.tap_ir_warned:
        print "Warning: Tap instruction scan returned 0x%08x! (expected b00001)." % (long(ir),)
        device.probe.tap_ir_warned = True
            
@command()
def tapaddress(value=0, device=None):
    """Read and write the eJTAG address register."""
    _check_config(device, 'tapaddress')
    
    if get_tap_type(device) == JTAG_TYPE_MDH:
        return tapaddress_mdh(device)
    else:
        ir = devtapi(None, IR_MIPS_ADDRESS, device=device)
        check_ir_return(ir, device)
        return devtapd(32, value, device=device)
        
def tapaddress_mdh(device):
    ir = mips_ir_to_apb(IR_MIPS_ADDRESS)
    #Ignore write value just read it
    return mdh_transaction(device.probe, ir, None)

@command()
def tapdata(value, device=None):
    """Read and write the eJTAG data register."""
    _check_config(device, 'tapdata')
    
    if get_tap_type(device) == JTAG_TYPE_MDH:
        return tapdata_mdh(value, device)
    else:
        ir = devtapi(None, IR_MIPS_DATA, device=device)
        check_ir_return(ir, device)
        return devtapd(32, value, device=device)
    
def tapdata_mdh(value, device):
    ir = mips_ir_to_apb(IR_MIPS_DATA)
    
    #Just do the right thing depending on PRnW
    PRnW = tapecr(device=device).PRnW
    
    if PRnW:
        #Processor is writing, so we want to read that value
        return mdh_transaction(device.probe, ir, None)
    else:
        #Processor is reading, so we should write a value
        mdh_transaction(device.probe, ir, value)
        #Just assume the write took, some calls will expect a return value
        return value
        
def get_mdh_error(code):
    return {
        0 : 'no error', 
        1 : 'device was powered down or is unavailable', 
        2 : 'APB cycle aborted due to bus reset or probe abort',
    }.get(code, 'reserved')

def get_mdh_addresses(core, vpe, addr, value):
    #Set device address
    reg_addr_mask = 0x7F
    #Each device has a 4k block allocated to it
    device_addr = (core * 0x1000) + (vpe * 0x100)

    #Also take any high bits from the register address
    device_addr += addr & ~reg_addr_mask
    device_addr >>= 7

    #Initially execute=1 to start a new transaction
    apb_access = APBAccessIn(data=value if value is not None else 0, 
                     addr=(addr & reg_addr_mask) >> 2, 
                     RnW=0 if value is not None else 1, 
                     execute=1)
    
    return DeviceAddr(addr=device_addr), apb_access
        
def mdh_transaction(probe, addr, value=None):
    da  = probe.da

    #Don't use probe.tap_index directly as it might be -1 even in scanonly mode
    tap_index  = _check_config(probe, 'mdh_transaction')

    #Must have an MDH device no. set
    if probe.mdh_device is None:
        raise RuntimeError("Set an MDH device with 'mdhdevice' before using this command.")
    ir_lengths = probe.ir_lengths

    core, vpe = probe.mdh_device
    device_addr, apb_access = get_mdh_addresses(core, vpe, addr, value)

    devanytap(da, tap_index, ir_lengths, ir=IR_MIPS_MDH_DEVICEADDR, dr_width=32, 
        dr=device_addr)
    
    #Then check that the returned valid was 1
    ret = APBAccessOut(devanytap(da, tap_index, ir_lengths, ir=IR_MIPS_MDH_APBACCESS, dr_width=39, dr=apb_access))
            
    if not ret.ok:
        raise RuntimeError('Returned OK was not 1 from APBAccess with execute=1, error_code=0x%x (%s)' % 
                    (ret.error_code, get_mdh_error(ret.error_code)))
    else:
        #Wait for actual result of the op
        apb_access = apb_access._replace(execute=0)
        
        start = time.time()
        while (time.time() - start) < 1:
            ret = APBAccessOut(devanytap(da, tap_index, ir_lengths, ir=IR_MIPS_MDH_APBACCESS,
                    dr_width=39, dr=apb_access))
                    
            #In case we just resent because ok=1, valid=0
            apb_access = apb_access._replace(execute=0)
            
            if ret.valid:
                break
            else:
                if ret.ok:
                    #Assume that we won't be getting many of these
                    raise  RuntimeError('Warning: Got OK=1 but valid=0 from APB access, consider reducing JTAG speed.')
                
        if ret.valid:
            if value is None:
                return ret.data
        else:
            ret = APBAccessOut(devanytap(da, tap_index, ir_lengths, ir=IR_MIPS_MDH_CONTROL, dr_width=32, 
                dr=MDHControl(AbortAPB=1)))
                
            if ret.ok:
                raise RuntimeError('APB access timed out waiting for valid=1')
            else:
                raise RuntimeError('APB access got OK=0, error_code=0x%x (%s)' % 
                        (ret.error_code, get_mdh_error(ret.error_code)))

@command()
def mdhdevice(core=None, vpe=None, device=None):
    """Choose which core/vpe number MDH operations such as mdhread will use.
    
    This only affects the console commands mdhread/mdhwrite, it does not affect
    any high level operations of the probe when in autodetected mode.  
    (For example regs will use the current console devicem, not the mdhdevice.)
    
    If either one of `core` or `vpe` are not given then 0 will be assumed. If 
    both `core` and `vpe` are not given then the current settings will be 
    returned as a pair of ``(core, vpe)``.
    
    """
    if core is None and vpe is None:
        return device.probe.mdh_device
    device.probe.mdh_device = (core or 0, vpe or 0)
       
@command()
def mdhread(addr, device=None):
    """Read the register at addr from a device behind a MIPS Debug Hub.
    
    The device number must have been set with mdhdevice to use this command.
    That number will be multiplied by 4k to get the block address. 
    addr is the address of the register to read within that block.
    """
    return mdh_transaction(device.probe, addr)
    
@command()
def mdhwrite(addr, value, device=None):
    """Write the register at addr from a device behind a MIPS Debug Hub.
    
    The device number must have been set with mdhdevice to use this command.
    That number will be multiplied by 4k to get the block address. 
    addr is the address of the register to write within that block.
    """
    return mdh_transaction(device.probe, addr, value=value)

def _assemble_list(address, assembly, isa, abi, toolkit=None, prefix=None):
    from imgtec.console import asmbytes
    return asmbytes(address, assembly, isa, abi, toolkit=toolkit, prefix=prefix)
    
def _parse_name(name):
    if name.endswith('[]'):
        return True, name[:-2], results.IntListResult([]), 
    else:
        return False, name, 0xdeadbeef


class DmsegList(object):
    def __init__(self, name, assembly='', names=None, doc='', start_address=0xff200200, assembled=None):
        self.name = name
        self.start_address = start_address
        self.assembly = assembly
        self.names = {} if names is None else names
        self.doc = doc
        self.assembled = assembled or {}
        for isa, instructions in self.assembled.items()[:]:
            if instructions is mips32:
                self.assembled[isa] = self.assembled['mips32']
        
    def __call__(self, isa='mips32', _params={}, **kwargs):
        data = {}
        for address, name in self.names.items():
            _, name, default_value = _parse_name(name)
            data[address] = kwargs.get(name, default_value)
        data.update(_params)
        return DmsegMemory(dict(self.names), data, self.code(isa), isa=isa)
        
    def code(self, isa):
        try:
            asm = self.assembled[isa]
        except KeyError:
            asm = _assemble_list(self.start_address, self.assembly, isa, 'o32')
            if not isinstance(asm, list):
                asm = [asm]
            asm = [(results.IntResult(op.address), results.IntResult(int(op.opcode, 16))) for op in asm]
            self.assembled[isa] = asm
        return dict(asm)
        
    def __repr__(self):
        lines = []
        if self.name != '<unnamed>':
            lines.append(self.name)
        if self.doc:
            lines.append('    ' + self.doc)
        if lines:
            lines.append('')
        if self.names:
            lines.extend('%s@0x%08x' % (name, address) for address, name in self.names.items())
            if self.assembly:
                lines.append('')
        address = '0x%08x' % (self.start_address,)
        for line in self.assembly.splitlines():
            line = line.strip()
            if line:
                lines.append("%s %s" % (address, line.strip()))
                address = ' ' * len(address)
        return '\n'.join(lines)

# [[[cog
# import sys, os, struct
# from imgtec.console import scan
# ]]]
# [[[end]]]

def _precog_list(cog, lst):
    try:
        isas = ['mips32', 'micromips', 'mips32r6', 'mips64r6', 'nanomips']
        
        toolkits  = dict(nanomips=r'D:\temp\nanomips-img-elf_i686-w64-mingw32\bin')
        prefixes  = dict(nanomips='nanomips-img-elf-')
        abis      = dict(nanomips='p32')
        assembled = dict()
        for isa in isas:
            asm = assembled[isa] = _assemble_list(lst.start_address, lst.assembly, isa,
                            abis.get(isa, 'o32'),
                            prefix=prefixes.get(isa),
                            toolkit=toolkits.get(isa),
                            )
            if isa == 'mips32r6' and \
               'mips32' in assembled and \
               [d.opcode for d in asm] == [d.opcode for d in assembled['mips32']]:
                cog.outl('mips32r6=mips32,')
            else:
                cog.outl('%s=[' % (isa,))
                asm = ["  (0x%08x, 0x%-8s), # %r" % (op.address, op.opcode, op.ops[0]) for op in asm]
                cog.outl('\n'.join(asm))
                cog.outl('],')
    except Exception as e:
        print "\nAssemble %s failed for %s, leaving output as it was:\n " % (lst.name, isa),
        print '\n  '.join(str(e).splitlines())
        cog.out(cog.previous)
    
_builtin_lists = []
def builtin_list(lst):
    _builtin_lists.append(lst)
    return named(lst.name, lst)
    
ReadDEPC = builtin_list(DmsegList('ReadDEPC', '''\
    nop
    nop
    mfc0      at, depc
    mfc0      v0, ebase
    lui       v1, 0xff20
    sw        at, 0(v1)
    sw        v0, 4(v1)
    sync
    ori       v1, v1, 0x200
    jalr      zero, v1
    nop
    ''',
    names={
        0xff200000:'DEPC',
        0xff200004:'EBase',
    },
    doc='A list for use with the dmseg command to read DEPC and EBase',
    assembled=dict(
        # [[[cog
        # scan._precog_list(cog, scan.ReadDEPC)
        # ]]]
        mips32=[
          (0xff200200, 0x00000000), # nop       
          (0xff200204, 0x00000000), # nop       
          (0xff200208, 0x4001c000), # mfc0      at, DEPC
          (0xff20020c, 0x40027801), # mfc0      v0, EBase
          (0xff200210, 0x3c03ff20), # lui       v1, 0xff20
          (0xff200214, 0xac610000), # sw        at, 0(v1)
          (0xff200218, 0xac620004), # sw        v0, 4(v1)
          (0xff20021c, 0x0000000f), # sync      
          (0xff200220, 0x34630200), # ori       v1, v1, 0x200
          (0xff200224, 0x00600009), # jalr      zero, v1
          (0xff200228, 0x00000000), # nop       
        ],
        micromips=[
          (0xff200200, 0x0c00    ), # nop       
          (0xff200202, 0x0c00    ), # nop       
          (0xff200204, 0x003800fc), # mfc0      at, DEPC
          (0xff200208, 0x004f08fc), # mfc0      v0, EBase
          (0xff20020c, 0x41a3ff20), # lui       v1, 0xff20
          (0xff200210, 0xf8230000), # sw        at, 0(v1)
          (0xff200214, 0xe931    ), # sw        v0, 4(v1)
          (0xff200216, 0x00006b7c), # sync      
          (0xff20021a, 0x50630200), # ori       v1, v1, 0x200
          (0xff20021e, 0x00030f3c), # jr        v1
          (0xff200222, 0x00000000), # nop       
          (0xff200226, 0x0c00    ), # nop       
        ],
        mips32r6=mips32,
        mips64r6=[
          (0xff200200, 0x00000000), # nop       
          (0xff200204, 0x00000000), # nop       
          (0xff200208, 0x4001c000), # mfc0      at, DEPC
          (0xff20020c, 0x40027801), # mfc0      v0, EBase
          (0xff200210, 0x3c03ff20), # lui       v1,  0xff20
          (0xff200214, 0xac610000), # sw        at, 0(v1)
          (0xff200218, 0xac620004), # sw        v0, 4(v1)
          (0xff20021c, 0x0000000f), # sync      
          (0xff200220, 0x34630200), # ori       v1, v1, 0x200
          (0xff200224, 0x00600009), # jr        v1
          (0xff200228, 0x00000000), # nop       
        ],
        # [[[end]]]
    )
))
    
WriteDEPC = builtin_list(DmsegList('WriteDEPC', '''\
    nop
    nop
    mtc0      at, desave # save at to desave
    lui       at, 0xff20 # Set at to value location
    lw        at, 0(at)  # Load value 
    mtc0      at, depc   # Set DEPC
    lui       at, 0xff20 # Set at to start of debug code
    ori       at, at, 0x200
    jalr      zero, at   # Jump back to beginning
    mfc0      at, desave # Restore at value
    ''',
    names={
        0xff200000:'value',
    },
    doc='A list for use with the dmseg command to write DEPC',
    assembled=dict(
        # [[[cog
        # scan._precog_list(cog, scan.WriteDEPC)
        # ]]]
        mips32=[
          (0xff200200, 0x00000000), # nop       
          (0xff200204, 0x00000000), # nop       
          (0xff200208, 0x4081f800), # mtc0      at, DESAVE
          (0xff20020c, 0x3c01ff20), # lui       at, 0xff20
          (0xff200210, 0x8c210000), # lw        at, 0(at)
          (0xff200214, 0x4081c000), # mtc0      at, DEPC
          (0xff200218, 0x3c01ff20), # lui       at, 0xff20
          (0xff20021c, 0x34210200), # ori       at, at, 0x200
          (0xff200220, 0x00200009), # jalr      zero, at
          (0xff200224, 0x4001f800), # mfc0      at, DESAVE
        ],
        micromips=[
          (0xff200200, 0x0c00    ), # nop       
          (0xff200202, 0x0c00    ), # nop       
          (0xff200204, 0x003f02fc), # mtc0      at, DESAVE
          (0xff200208, 0x41a1ff20), # lui       at, 0xff20
          (0xff20020c, 0xfc210000), # lw        at, 0(at)
          (0xff200210, 0x003802fc), # mtc0      at, DEPC
          (0xff200214, 0x41a1ff20), # lui       at, 0xff20
          (0xff200218, 0x50210200), # ori       at, at, 0x200
          (0xff20021c, 0x00010f3c), # jr        at
          (0xff200220, 0x003f00fc), # mfc0      at, DESAVE
        ],
        mips32r6=mips32,
        mips64r6=[
          (0xff200200, 0x00000000), # nop       
          (0xff200204, 0x00000000), # nop       
          (0xff200208, 0x4081f800), # mtc0      at, DESAVE
          (0xff20020c, 0x3c01ff20), # lui       at,  0xff20
          (0xff200210, 0x8c210000), # lw        at, 0(at)
          (0xff200214, 0x4081c000), # mtc0      at, DEPC
          (0xff200218, 0x3c01ff20), # lui       at,  0xff20
          (0xff20021c, 0x34210200), # ori       at, at, 0x200
          (0xff200220, 0x00200009), # jr        at
          (0xff200224, 0x4001f800), # mfc0      at, DESAVE
        ],
        # [[[end]]]
    )
))

write_reg = '''\
R%d:
    lw        $%d, 4(at)     # Save register to 'value'
    b         End            #
    lw        v0, 8(at)      # Get v0 back from memory
'''
WriteRegister = builtin_list(DmsegList('WriteRegister', '''\
    nop
    nop
    b         Prog
    mtc0      at, desave     # save at
JumpTable:
'''
+ '\n'.join(['.word R%d' % i for i in range(32)]) +
'''
Prog:
    lui       at, 0xff20     # points to 0xff200000
    sw        v0, 8(at)      # Save v0
    lw        at, 0(at)      # Get register index
    sll       at, at, 2      # Multiply index by 4 to get offset
    la        v0, JumpTable  # Load address of table
    addu      v0, at, v0     # Add offset to start of table
    lw        v0, 0(v0)      # Read the word in jump table at the offset
    jalr      zero, v0       # Jump to that location
    lui       at, 0xff20     # set at to 0xff200000 
'''
+ write_reg % (0, 0) +
'''
R1:                          # at is a special case
    lw        at, 4(at)      # Write at
    b         EndWriteAt     # Go to at specific cleanup
    lui       v0, 0xff20     # Use v0 for return
    
R2:                          # V0 is used as a temp
    lw        $2, 4(at)      # Write v0
    b         End            #
    nop                      # Don't restore V0
'''
+ '\n'.join([write_reg % (i, i) for i in range(3, 32)]) + 
'''
End:
    ori       at, at, 0x200  # at points to 0xff200200
    jalr      zero, at       # jump back to beginning
    mfc0      at, desave     # restore at
EndWriteAt:
    ori       v0, v0, 0x200  #
    jalr      zero, v0       # Jump back to beginning
    lw        v0, 8(at)      # Restore v0
''',
    names={
        0xff200000:'index',
        0xff200004:'value',
    },
    doc='Write a register',
    assembled=dict(
        # [[[cog
        # scan._precog_list(cog, scan.WriteRegister)
        # ]]]
        mips32=[
          (0xff200200, 0x00000000), # nop       
          (0xff200204, 0x00000000), # nop       
          (0xff200208, 0x10000021), # b         0xff200290
          (0xff20020c, 0x4081f800), # mtc0      at, DESAVE
          (0xff200210, 0xff2002b8), # .word     0xff2002b8
          (0xff200214, 0xff2002c4), # .word     0xff2002c4
          (0xff200218, 0xff2002d0), # .word     0xff2002d0
          (0xff20021c, 0xff2002dc), # .word     0xff2002dc
          (0xff200220, 0xff2002e8), # .word     0xff2002e8
          (0xff200224, 0xff2002f4), # .word     0xff2002f4
          (0xff200228, 0xff200300), # .word     0xff200300
          (0xff20022c, 0xff20030c), # .word     0xff20030c
          (0xff200230, 0xff200318), # .word     0xff200318
          (0xff200234, 0xff200324), # .word     0xff200324
          (0xff200238, 0xff200330), # .word     0xff200330
          (0xff20023c, 0xff20033c), # .word     0xff20033c
          (0xff200240, 0xff200348), # .word     0xff200348
          (0xff200244, 0xff200354), # .word     0xff200354
          (0xff200248, 0xff200360), # .word     0xff200360
          (0xff20024c, 0xff20036c), # .word     0xff20036c
          (0xff200250, 0xff200378), # .word     0xff200378
          (0xff200254, 0xff200384), # .word     0xff200384
          (0xff200258, 0xff200390), # .word     0xff200390
          (0xff20025c, 0xff20039c), # .word     0xff20039c
          (0xff200260, 0xff2003a8), # .word     0xff2003a8
          (0xff200264, 0xff2003b4), # .word     0xff2003b4
          (0xff200268, 0xff2003c0), # .word     0xff2003c0
          (0xff20026c, 0xff2003cc), # .word     0xff2003cc
          (0xff200270, 0xff2003d8), # .word     0xff2003d8
          (0xff200274, 0xff2003e4), # .word     0xff2003e4
          (0xff200278, 0xff2003f0), # .word     0xff2003f0
          (0xff20027c, 0xff2003fc), # .word     0xff2003fc
          (0xff200280, 0xff200408), # .word     0xff200408
          (0xff200284, 0xff200414), # .word     0xff200414
          (0xff200288, 0xff200420), # .word     0xff200420
          (0xff20028c, 0xff20042c), # .word     0xff20042c
          (0xff200290, 0x3c01ff20), # lui       at, 0xff20
          (0xff200294, 0xac220008), # sw        v0, 8(at)
          (0xff200298, 0x8c210000), # lw        at, 0(at)
          (0xff20029c, 0x00010880), # sll       at, at, 0x2
          (0xff2002a0, 0x3c02ff20), # lui       v0, 0xff20
          (0xff2002a4, 0x24420210), # addiu     v0, v0, 528
          (0xff2002a8, 0x00221021), # addu      v0, at, v0
          (0xff2002ac, 0x8c420000), # lw        v0, 0(v0)
          (0xff2002b0, 0x00400009), # jalr      zero, v0
          (0xff2002b4, 0x3c01ff20), # lui       at, 0xff20
          (0xff2002b8, 0x8c200004), # lw        zero, 4(at)
          (0xff2002bc, 0x1000005e), # b         0xff200438
          (0xff2002c0, 0x8c220008), # lw        v0, 8(at)
          (0xff2002c4, 0x8c210004), # lw        at, 4(at)
          (0xff2002c8, 0x1000005e), # b         0xff200444
          (0xff2002cc, 0x3c02ff20), # lui       v0, 0xff20
          (0xff2002d0, 0x8c220004), # lw        v0, 4(at)
          (0xff2002d4, 0x10000058), # b         0xff200438
          (0xff2002d8, 0x00000000), # nop       
          (0xff2002dc, 0x8c230004), # lw        v1, 4(at)
          (0xff2002e0, 0x10000055), # b         0xff200438
          (0xff2002e4, 0x8c220008), # lw        v0, 8(at)
          (0xff2002e8, 0x8c240004), # lw        a0, 4(at)
          (0xff2002ec, 0x10000052), # b         0xff200438
          (0xff2002f0, 0x8c220008), # lw        v0, 8(at)
          (0xff2002f4, 0x8c250004), # lw        a1, 4(at)
          (0xff2002f8, 0x1000004f), # b         0xff200438
          (0xff2002fc, 0x8c220008), # lw        v0, 8(at)
          (0xff200300, 0x8c260004), # lw        a2, 4(at)
          (0xff200304, 0x1000004c), # b         0xff200438
          (0xff200308, 0x8c220008), # lw        v0, 8(at)
          (0xff20030c, 0x8c270004), # lw        a3, 4(at)
          (0xff200310, 0x10000049), # b         0xff200438
          (0xff200314, 0x8c220008), # lw        v0, 8(at)
          (0xff200318, 0x8c280004), # lw        t0, 4(at)
          (0xff20031c, 0x10000046), # b         0xff200438
          (0xff200320, 0x8c220008), # lw        v0, 8(at)
          (0xff200324, 0x8c290004), # lw        t1, 4(at)
          (0xff200328, 0x10000043), # b         0xff200438
          (0xff20032c, 0x8c220008), # lw        v0, 8(at)
          (0xff200330, 0x8c2a0004), # lw        t2, 4(at)
          (0xff200334, 0x10000040), # b         0xff200438
          (0xff200338, 0x8c220008), # lw        v0, 8(at)
          (0xff20033c, 0x8c2b0004), # lw        t3, 4(at)
          (0xff200340, 0x1000003d), # b         0xff200438
          (0xff200344, 0x8c220008), # lw        v0, 8(at)
          (0xff200348, 0x8c2c0004), # lw        t4, 4(at)
          (0xff20034c, 0x1000003a), # b         0xff200438
          (0xff200350, 0x8c220008), # lw        v0, 8(at)
          (0xff200354, 0x8c2d0004), # lw        t5, 4(at)
          (0xff200358, 0x10000037), # b         0xff200438
          (0xff20035c, 0x8c220008), # lw        v0, 8(at)
          (0xff200360, 0x8c2e0004), # lw        t6, 4(at)
          (0xff200364, 0x10000034), # b         0xff200438
          (0xff200368, 0x8c220008), # lw        v0, 8(at)
          (0xff20036c, 0x8c2f0004), # lw        t7, 4(at)
          (0xff200370, 0x10000031), # b         0xff200438
          (0xff200374, 0x8c220008), # lw        v0, 8(at)
          (0xff200378, 0x8c300004), # lw        s0, 4(at)
          (0xff20037c, 0x1000002e), # b         0xff200438
          (0xff200380, 0x8c220008), # lw        v0, 8(at)
          (0xff200384, 0x8c310004), # lw        s1, 4(at)
          (0xff200388, 0x1000002b), # b         0xff200438
          (0xff20038c, 0x8c220008), # lw        v0, 8(at)
          (0xff200390, 0x8c320004), # lw        s2, 4(at)
          (0xff200394, 0x10000028), # b         0xff200438
          (0xff200398, 0x8c220008), # lw        v0, 8(at)
          (0xff20039c, 0x8c330004), # lw        s3, 4(at)
          (0xff2003a0, 0x10000025), # b         0xff200438
          (0xff2003a4, 0x8c220008), # lw        v0, 8(at)
          (0xff2003a8, 0x8c340004), # lw        s4, 4(at)
          (0xff2003ac, 0x10000022), # b         0xff200438
          (0xff2003b0, 0x8c220008), # lw        v0, 8(at)
          (0xff2003b4, 0x8c350004), # lw        s5, 4(at)
          (0xff2003b8, 0x1000001f), # b         0xff200438
          (0xff2003bc, 0x8c220008), # lw        v0, 8(at)
          (0xff2003c0, 0x8c360004), # lw        s6, 4(at)
          (0xff2003c4, 0x1000001c), # b         0xff200438
          (0xff2003c8, 0x8c220008), # lw        v0, 8(at)
          (0xff2003cc, 0x8c370004), # lw        s7, 4(at)
          (0xff2003d0, 0x10000019), # b         0xff200438
          (0xff2003d4, 0x8c220008), # lw        v0, 8(at)
          (0xff2003d8, 0x8c380004), # lw        t8, 4(at)
          (0xff2003dc, 0x10000016), # b         0xff200438
          (0xff2003e0, 0x8c220008), # lw        v0, 8(at)
          (0xff2003e4, 0x8c390004), # lw        t9, 4(at)
          (0xff2003e8, 0x10000013), # b         0xff200438
          (0xff2003ec, 0x8c220008), # lw        v0, 8(at)
          (0xff2003f0, 0x8c3a0004), # lw        k0, 4(at)
          (0xff2003f4, 0x10000010), # b         0xff200438
          (0xff2003f8, 0x8c220008), # lw        v0, 8(at)
          (0xff2003fc, 0x8c3b0004), # lw        k1, 4(at)
          (0xff200400, 0x1000000d), # b         0xff200438
          (0xff200404, 0x8c220008), # lw        v0, 8(at)
          (0xff200408, 0x8c3c0004), # lw        gp, 4(at)
          (0xff20040c, 0x1000000a), # b         0xff200438
          (0xff200410, 0x8c220008), # lw        v0, 8(at)
          (0xff200414, 0x8c3d0004), # lw        sp, 4(at)
          (0xff200418, 0x10000007), # b         0xff200438
          (0xff20041c, 0x8c220008), # lw        v0, 8(at)
          (0xff200420, 0x8c3e0004), # lw        s8, 4(at)
          (0xff200424, 0x10000004), # b         0xff200438
          (0xff200428, 0x8c220008), # lw        v0, 8(at)
          (0xff20042c, 0x8c3f0004), # lw        ra, 4(at)
          (0xff200430, 0x10000001), # b         0xff200438
          (0xff200434, 0x8c220008), # lw        v0, 8(at)
          (0xff200438, 0x34210200), # ori       at, at, 0x200
          (0xff20043c, 0x00200009), # jalr      zero, at
          (0xff200440, 0x4001f800), # mfc0      at, DESAVE
          (0xff200444, 0x34420200), # ori       v0, v0, 0x200
          (0xff200448, 0x00400009), # jalr      zero, v0
          (0xff20044c, 0x8c220008), # lw        v0, 8(at)
        ],
        micromips=[
          (0xff200200, 0x0c00    ), # nop       
          (0xff200202, 0x0c00    ), # nop       
          (0xff200204, 0xcc43    ), # b         0xff20028c
          (0xff200206, 0x003f02fc), # mtc0      at, DESAVE
          (0xff20020a, 0x0c00    ), # nop       
          (0xff20020c, 0xff2002b3), # lw        t9, 691(zero)
          (0xff200210, 0xff2002bd), # lw        t9, 701(zero)
          (0xff200214, 0xff2002c7), # lw        t9, 711(zero)
          (0xff200218, 0xff2002cf), # lw        t9, 719(zero)
          (0xff20021c, 0xff2002d9), # lw        t9, 729(zero)
          (0xff200220, 0xff2002e3), # lw        t9, 739(zero)
          (0xff200224, 0xff2002ed), # lw        t9, 749(zero)
          (0xff200228, 0xff2002f7), # lw        t9, 759(zero)
          (0xff20022c, 0xff200301), # lw        t9, 769(zero)
          (0xff200230, 0xff20030b), # lw        t9, 779(zero)
          (0xff200234, 0xff200315), # lw        t9, 789(zero)
          (0xff200238, 0xff20031f), # lw        t9, 799(zero)
          (0xff20023c, 0xff200329), # lw        t9, 809(zero)
          (0xff200240, 0xff200333), # lw        t9, 819(zero)
          (0xff200244, 0xff20033d), # lw        t9, 829(zero)
          (0xff200248, 0xff200347), # lw        t9, 839(zero)
          (0xff20024c, 0xff200351), # lw        t9, 849(zero)
          (0xff200250, 0xff20035b), # lw        t9, 859(zero)
          (0xff200254, 0xff200365), # lw        t9, 869(zero)
          (0xff200258, 0xff20036f), # lw        t9, 879(zero)
          (0xff20025c, 0xff200379), # lw        t9, 889(zero)
          (0xff200260, 0xff200383), # lw        t9, 899(zero)
          (0xff200264, 0xff20038d), # lw        t9, 909(zero)
          (0xff200268, 0xff200397), # lw        t9, 919(zero)
          (0xff20026c, 0xff2003a1), # lw        t9, 929(zero)
          (0xff200270, 0xff2003ab), # lw        t9, 939(zero)
          (0xff200274, 0xff2003b5), # lw        t9, 949(zero)
          (0xff200278, 0xff2003bf), # lw        t9, 959(zero)
          (0xff20027c, 0xff2003c9), # lw        t9, 969(zero)
          (0xff200280, 0xff2003d3), # lw        t9, 979(zero)
          (0xff200284, 0xff2003dd), # lw        t9, 989(zero)
          (0xff200288, 0xff2003e7), # lw        t9, 999(zero)
          (0xff20028c, 0x41a1ff20), # lui       at, 0xff20
          (0xff200290, 0xf8410008), # sw        v0, 8(at)
          (0xff200294, 0xfc210000), # lw        at, 0(at)
          (0xff200298, 0x00211000), # sll       at, at, 0x2
          (0xff20029c, 0x41a2ff20), # lui       v0, 0xff20
          (0xff2002a0, 0x3042020c), # addiu     v0, v0, 524
          (0xff2002a4, 0x00411150), # addu      v0, at, v0
          (0xff2002a8, 0x6920    ), # lw        v0, 0(v0)
          (0xff2002aa, 0x00020f3c), # jr        v0
          (0xff2002ae, 0x41a1ff20), # lui       at, 0xff20
          (0xff2002b2, 0xfc010004), # lw        zero, 4(at)
          (0xff2002b6, 0xcc9c    ), # b         0xff2003f0
          (0xff2002b8, 0xfc410008), # lw        v0, 8(at)
          (0xff2002bc, 0xfc210004), # lw        at, 4(at)
          (0xff2002c0, 0xcc9d    ), # b         0xff2003fc
          (0xff2002c2, 0x41a2ff20), # lui       v0, 0xff20
          (0xff2002c6, 0xfc410004), # lw        v0, 4(at)
          (0xff2002ca, 0xcc92    ), # b         0xff2003f0
          (0xff2002cc, 0x0c00    ), # nop       
          (0xff2002ce, 0xfc610004), # lw        v1, 4(at)
          (0xff2002d2, 0xcc8e    ), # b         0xff2003f0
          (0xff2002d4, 0xfc410008), # lw        v0, 8(at)
          (0xff2002d8, 0xfc810004), # lw        a0, 4(at)
          (0xff2002dc, 0xcc89    ), # b         0xff2003f0
          (0xff2002de, 0xfc410008), # lw        v0, 8(at)
          (0xff2002e2, 0xfca10004), # lw        a1, 4(at)
          (0xff2002e6, 0xcc84    ), # b         0xff2003f0
          (0xff2002e8, 0xfc410008), # lw        v0, 8(at)
          (0xff2002ec, 0xfcc10004), # lw        a2, 4(at)
          (0xff2002f0, 0xcc7f    ), # b         0xff2003f0
          (0xff2002f2, 0xfc410008), # lw        v0, 8(at)
          (0xff2002f6, 0xfce10004), # lw        a3, 4(at)
          (0xff2002fa, 0xcc7a    ), # b         0xff2003f0
          (0xff2002fc, 0xfc410008), # lw        v0, 8(at)
          (0xff200300, 0xfd010004), # lw        t0, 4(at)
          (0xff200304, 0xcc75    ), # b         0xff2003f0
          (0xff200306, 0xfc410008), # lw        v0, 8(at)
          (0xff20030a, 0xfd210004), # lw        t1, 4(at)
          (0xff20030e, 0xcc70    ), # b         0xff2003f0
          (0xff200310, 0xfc410008), # lw        v0, 8(at)
          (0xff200314, 0xfd410004), # lw        t2, 4(at)
          (0xff200318, 0xcc6b    ), # b         0xff2003f0
          (0xff20031a, 0xfc410008), # lw        v0, 8(at)
          (0xff20031e, 0xfd610004), # lw        t3, 4(at)
          (0xff200322, 0xcc66    ), # b         0xff2003f0
          (0xff200324, 0xfc410008), # lw        v0, 8(at)
          (0xff200328, 0xfd810004), # lw        t4, 4(at)
          (0xff20032c, 0xcc61    ), # b         0xff2003f0
          (0xff20032e, 0xfc410008), # lw        v0, 8(at)
          (0xff200332, 0xfda10004), # lw        t5, 4(at)
          (0xff200336, 0xcc5c    ), # b         0xff2003f0
          (0xff200338, 0xfc410008), # lw        v0, 8(at)
          (0xff20033c, 0xfdc10004), # lw        t6, 4(at)
          (0xff200340, 0xcc57    ), # b         0xff2003f0
          (0xff200342, 0xfc410008), # lw        v0, 8(at)
          (0xff200346, 0xfde10004), # lw        t7, 4(at)
          (0xff20034a, 0xcc52    ), # b         0xff2003f0
          (0xff20034c, 0xfc410008), # lw        v0, 8(at)
          (0xff200350, 0xfe010004), # lw        s0, 4(at)
          (0xff200354, 0xcc4d    ), # b         0xff2003f0
          (0xff200356, 0xfc410008), # lw        v0, 8(at)
          (0xff20035a, 0xfe210004), # lw        s1, 4(at)
          (0xff20035e, 0xcc48    ), # b         0xff2003f0
          (0xff200360, 0xfc410008), # lw        v0, 8(at)
          (0xff200364, 0xfe410004), # lw        s2, 4(at)
          (0xff200368, 0xcc43    ), # b         0xff2003f0
          (0xff20036a, 0xfc410008), # lw        v0, 8(at)
          (0xff20036e, 0xfe610004), # lw        s3, 4(at)
          (0xff200372, 0xcc3e    ), # b         0xff2003f0
          (0xff200374, 0xfc410008), # lw        v0, 8(at)
          (0xff200378, 0xfe810004), # lw        s4, 4(at)
          (0xff20037c, 0xcc39    ), # b         0xff2003f0
          (0xff20037e, 0xfc410008), # lw        v0, 8(at)
          (0xff200382, 0xfea10004), # lw        s5, 4(at)
          (0xff200386, 0xcc34    ), # b         0xff2003f0
          (0xff200388, 0xfc410008), # lw        v0, 8(at)
          (0xff20038c, 0xfec10004), # lw        s6, 4(at)
          (0xff200390, 0xcc2f    ), # b         0xff2003f0
          (0xff200392, 0xfc410008), # lw        v0, 8(at)
          (0xff200396, 0xfee10004), # lw        s7, 4(at)
          (0xff20039a, 0xcc2a    ), # b         0xff2003f0
          (0xff20039c, 0xfc410008), # lw        v0, 8(at)
          (0xff2003a0, 0xff010004), # lw        t8, 4(at)
          (0xff2003a4, 0xcc25    ), # b         0xff2003f0
          (0xff2003a6, 0xfc410008), # lw        v0, 8(at)
          (0xff2003aa, 0xff210004), # lw        t9, 4(at)
          (0xff2003ae, 0xcc20    ), # b         0xff2003f0
          (0xff2003b0, 0xfc410008), # lw        v0, 8(at)
          (0xff2003b4, 0xff410004), # lw        k0, 4(at)
          (0xff2003b8, 0xcc1b    ), # b         0xff2003f0
          (0xff2003ba, 0xfc410008), # lw        v0, 8(at)
          (0xff2003be, 0xff610004), # lw        k1, 4(at)
          (0xff2003c2, 0xcc16    ), # b         0xff2003f0
          (0xff2003c4, 0xfc410008), # lw        v0, 8(at)
          (0xff2003c8, 0xff810004), # lw        gp, 4(at)
          (0xff2003cc, 0xcc11    ), # b         0xff2003f0
          (0xff2003ce, 0xfc410008), # lw        v0, 8(at)
          (0xff2003d2, 0xffa10004), # lw        sp, 4(at)
          (0xff2003d6, 0xcc0c    ), # b         0xff2003f0
          (0xff2003d8, 0xfc410008), # lw        v0, 8(at)
          (0xff2003dc, 0xffc10004), # lw        s8, 4(at)
          (0xff2003e0, 0xcc07    ), # b         0xff2003f0
          (0xff2003e2, 0xfc410008), # lw        v0, 8(at)
          (0xff2003e6, 0xffe10004), # lw        ra, 4(at)
          (0xff2003ea, 0xcc02    ), # b         0xff2003f0
          (0xff2003ec, 0xfc410008), # lw        v0, 8(at)
          (0xff2003f0, 0x50210200), # ori       at, at, 0x200
          (0xff2003f4, 0x00010f3c), # jr        at
          (0xff2003f8, 0x003f00fc), # mfc0      at, DESAVE
          (0xff2003fc, 0x50420200), # ori       v0, v0, 0x200
          (0xff200400, 0x00020f3c), # jr        v0
          (0xff200404, 0xfc410008), # lw        v0, 8(at)
        ],
        mips32r6=mips32,
        mips64r6=[
          (0xff200200, 0x00000000), # nop       
          (0xff200204, 0x00000000), # nop       
          (0xff200208, 0x10000021), # b         0x00000000ff200290
          (0xff20020c, 0x4081f800), # mtc0      at, DESAVE
          (0xff200210, 0xff2002b8), # sd        zero, 696(t9)
          (0xff200214, 0xff2002c4), # sd        zero, 708(t9)
          (0xff200218, 0xff2002d0), # sd        zero, 720(t9)
          (0xff20021c, 0xff2002dc), # sd        zero, 732(t9)
          (0xff200220, 0xff2002e8), # sd        zero, 744(t9)
          (0xff200224, 0xff2002f4), # sd        zero, 756(t9)
          (0xff200228, 0xff200300), # sd        zero, 768(t9)
          (0xff20022c, 0xff20030c), # sd        zero, 780(t9)
          (0xff200230, 0xff200318), # sd        zero, 792(t9)
          (0xff200234, 0xff200324), # sd        zero, 804(t9)
          (0xff200238, 0xff200330), # sd        zero, 816(t9)
          (0xff20023c, 0xff20033c), # sd        zero, 828(t9)
          (0xff200240, 0xff200348), # sd        zero, 840(t9)
          (0xff200244, 0xff200354), # sd        zero, 852(t9)
          (0xff200248, 0xff200360), # sd        zero, 864(t9)
          (0xff20024c, 0xff20036c), # sd        zero, 876(t9)
          (0xff200250, 0xff200378), # sd        zero, 888(t9)
          (0xff200254, 0xff200384), # sd        zero, 900(t9)
          (0xff200258, 0xff200390), # sd        zero, 912(t9)
          (0xff20025c, 0xff20039c), # sd        zero, 924(t9)
          (0xff200260, 0xff2003a8), # sd        zero, 936(t9)
          (0xff200264, 0xff2003b4), # sd        zero, 948(t9)
          (0xff200268, 0xff2003c0), # sd        zero, 960(t9)
          (0xff20026c, 0xff2003cc), # sd        zero, 972(t9)
          (0xff200270, 0xff2003d8), # sd        zero, 984(t9)
          (0xff200274, 0xff2003e4), # sd        zero, 996(t9)
          (0xff200278, 0xff2003f0), # sd        zero, 1008(t9)
          (0xff20027c, 0xff2003fc), # sd        zero, 1020(t9)
          (0xff200280, 0xff200408), # sd        zero, 1032(t9)
          (0xff200284, 0xff200414), # sd        zero, 1044(t9)
          (0xff200288, 0xff200420), # sd        zero, 1056(t9)
          (0xff20028c, 0xff20042c), # sd        zero, 1068(t9)
          (0xff200290, 0x3c01ff20), # lui       at,  0xff20
          (0xff200294, 0xac220008), # sw        v0, 8(at)
          (0xff200298, 0x8c210000), # lw        at, 0(at)
          (0xff20029c, 0x00010880), # sll       at, at, 0x2
          (0xff2002a0, 0x3c02ff20), # lui       v0,  0xff20
          (0xff2002a4, 0x24420210), # addiu     v0, v0, 528
          (0xff2002a8, 0x00221021), # addu      v0, at, v0
          (0xff2002ac, 0x8c420000), # lw        v0, 0(v0)
          (0xff2002b0, 0x00400009), # jr        v0
          (0xff2002b4, 0x3c01ff20), # lui       at,  0xff20
          (0xff2002b8, 0x8c200004), # lw        zero, 4(at)
          (0xff2002bc, 0x1000005e), # b         0x00000000ff200438
          (0xff2002c0, 0x8c220008), # lw        v0, 8(at)
          (0xff2002c4, 0x8c210004), # lw        at, 4(at)
          (0xff2002c8, 0x1000005e), # b         0x00000000ff200444
          (0xff2002cc, 0x3c02ff20), # lui       v0,  0xff20
          (0xff2002d0, 0x8c220004), # lw        v0, 4(at)
          (0xff2002d4, 0x10000058), # b         0x00000000ff200438
          (0xff2002d8, 0x00000000), # nop       
          (0xff2002dc, 0x8c230004), # lw        v1, 4(at)
          (0xff2002e0, 0x10000055), # b         0x00000000ff200438
          (0xff2002e4, 0x8c220008), # lw        v0, 8(at)
          (0xff2002e8, 0x8c240004), # lw        a0, 4(at)
          (0xff2002ec, 0x10000052), # b         0x00000000ff200438
          (0xff2002f0, 0x8c220008), # lw        v0, 8(at)
          (0xff2002f4, 0x8c250004), # lw        a1, 4(at)
          (0xff2002f8, 0x1000004f), # b         0x00000000ff200438
          (0xff2002fc, 0x8c220008), # lw        v0, 8(at)
          (0xff200300, 0x8c260004), # lw        a2, 4(at)
          (0xff200304, 0x1000004c), # b         0x00000000ff200438
          (0xff200308, 0x8c220008), # lw        v0, 8(at)
          (0xff20030c, 0x8c270004), # lw        a3, 4(at)
          (0xff200310, 0x10000049), # b         0x00000000ff200438
          (0xff200314, 0x8c220008), # lw        v0, 8(at)
          (0xff200318, 0x8c280004), # lw        t0, 4(at)
          (0xff20031c, 0x10000046), # b         0x00000000ff200438
          (0xff200320, 0x8c220008), # lw        v0, 8(at)
          (0xff200324, 0x8c290004), # lw        t1, 4(at)
          (0xff200328, 0x10000043), # b         0x00000000ff200438
          (0xff20032c, 0x8c220008), # lw        v0, 8(at)
          (0xff200330, 0x8c2a0004), # lw        t2, 4(at)
          (0xff200334, 0x10000040), # b         0x00000000ff200438
          (0xff200338, 0x8c220008), # lw        v0, 8(at)
          (0xff20033c, 0x8c2b0004), # lw        t3, 4(at)
          (0xff200340, 0x1000003d), # b         0x00000000ff200438
          (0xff200344, 0x8c220008), # lw        v0, 8(at)
          (0xff200348, 0x8c2c0004), # lw        t4, 4(at)
          (0xff20034c, 0x1000003a), # b         0x00000000ff200438
          (0xff200350, 0x8c220008), # lw        v0, 8(at)
          (0xff200354, 0x8c2d0004), # lw        t5, 4(at)
          (0xff200358, 0x10000037), # b         0x00000000ff200438
          (0xff20035c, 0x8c220008), # lw        v0, 8(at)
          (0xff200360, 0x8c2e0004), # lw        t6, 4(at)
          (0xff200364, 0x10000034), # b         0x00000000ff200438
          (0xff200368, 0x8c220008), # lw        v0, 8(at)
          (0xff20036c, 0x8c2f0004), # lw        t7, 4(at)
          (0xff200370, 0x10000031), # b         0x00000000ff200438
          (0xff200374, 0x8c220008), # lw        v0, 8(at)
          (0xff200378, 0x8c300004), # lw        s0, 4(at)
          (0xff20037c, 0x1000002e), # b         0x00000000ff200438
          (0xff200380, 0x8c220008), # lw        v0, 8(at)
          (0xff200384, 0x8c310004), # lw        s1, 4(at)
          (0xff200388, 0x1000002b), # b         0x00000000ff200438
          (0xff20038c, 0x8c220008), # lw        v0, 8(at)
          (0xff200390, 0x8c320004), # lw        s2, 4(at)
          (0xff200394, 0x10000028), # b         0x00000000ff200438
          (0xff200398, 0x8c220008), # lw        v0, 8(at)
          (0xff20039c, 0x8c330004), # lw        s3, 4(at)
          (0xff2003a0, 0x10000025), # b         0x00000000ff200438
          (0xff2003a4, 0x8c220008), # lw        v0, 8(at)
          (0xff2003a8, 0x8c340004), # lw        s4, 4(at)
          (0xff2003ac, 0x10000022), # b         0x00000000ff200438
          (0xff2003b0, 0x8c220008), # lw        v0, 8(at)
          (0xff2003b4, 0x8c350004), # lw        s5, 4(at)
          (0xff2003b8, 0x1000001f), # b         0x00000000ff200438
          (0xff2003bc, 0x8c220008), # lw        v0, 8(at)
          (0xff2003c0, 0x8c360004), # lw        s6, 4(at)
          (0xff2003c4, 0x1000001c), # b         0x00000000ff200438
          (0xff2003c8, 0x8c220008), # lw        v0, 8(at)
          (0xff2003cc, 0x8c370004), # lw        s7, 4(at)
          (0xff2003d0, 0x10000019), # b         0x00000000ff200438
          (0xff2003d4, 0x8c220008), # lw        v0, 8(at)
          (0xff2003d8, 0x8c380004), # lw        t8, 4(at)
          (0xff2003dc, 0x10000016), # b         0x00000000ff200438
          (0xff2003e0, 0x8c220008), # lw        v0, 8(at)
          (0xff2003e4, 0x8c390004), # lw        t9, 4(at)
          (0xff2003e8, 0x10000013), # b         0x00000000ff200438
          (0xff2003ec, 0x8c220008), # lw        v0, 8(at)
          (0xff2003f0, 0x8c3a0004), # lw        k0, 4(at)
          (0xff2003f4, 0x10000010), # b         0x00000000ff200438
          (0xff2003f8, 0x8c220008), # lw        v0, 8(at)
          (0xff2003fc, 0x8c3b0004), # lw        k1, 4(at)
          (0xff200400, 0x1000000d), # b         0x00000000ff200438
          (0xff200404, 0x8c220008), # lw        v0, 8(at)
          (0xff200408, 0x8c3c0004), # lw        gp, 4(at)
          (0xff20040c, 0x1000000a), # b         0x00000000ff200438
          (0xff200410, 0x8c220008), # lw        v0, 8(at)
          (0xff200414, 0x8c3d0004), # lw        sp, 4(at)
          (0xff200418, 0x10000007), # b         0x00000000ff200438
          (0xff20041c, 0x8c220008), # lw        v0, 8(at)
          (0xff200420, 0x8c3e0004), # lw        s8, 4(at)
          (0xff200424, 0x10000004), # b         0x00000000ff200438
          (0xff200428, 0x8c220008), # lw        v0, 8(at)
          (0xff20042c, 0x8c3f0004), # lw        ra, 4(at)
          (0xff200430, 0x10000001), # b         0x00000000ff200438
          (0xff200434, 0x8c220008), # lw        v0, 8(at)
          (0xff200438, 0x34210200), # ori       at, at, 0x200
          (0xff20043c, 0x00200009), # jr        at
          (0xff200440, 0x4001f800), # mfc0      at, DESAVE
          (0xff200444, 0x34420200), # ori       v0, v0, 0x200
          (0xff200448, 0x00400009), # jr        v0
          (0xff20044c, 0x8c220008), # lw        v0, 8(at)
        ],
        # [[[end]]]
    )
))

save_reg = '''\
R%d:
    sw        $%d, 4(at)    # Store the register in the value location
    b         End           # Jump to cleanup
    lw        v0, 8(at)     # Restore v0
'''
ReadRegister = builtin_list(DmsegList('ReadRegister', '''\
    nop
    nop
    b         Prog          # branch over the jump table
    mtc0      at, desave    # save at
JumpTable:                  # Table of label addresses of each reg read
'''
 + '\n'.join(['\t.word R%d' % i for i in range(32)]) + 
'''
Prog:
    lui       at, 0xff20    # points to 0xff200000
    sw        v0, 8(at)     # Save v0
    lw        at, 0(at)     # Get register index
    sll       at, at, 2     # Multiply index by 4
    la        v0, JumpTable # Load start address of table
    addu      v0, at, v0    # Add index to start of jump table
    lw        v0, 0(v0)     # Read the word at jump table plus index
    jalr      zero, v0      # Jump to that location
    lui       at, 0xff20    # set at to 0xff200000 so we can do the store
'''
+ save_reg % (0, 0) + 
'''
R1:                         
    move      v0, at        # v0 becomes our save offset
    mfc0      at, desave    # Restore at
    sw        $1, 4(v0)     # Save at to memory
    move      at, v0        # Put offset back
    b         End
    lw        v0, 8(at)     # Restore v0
R2:                         # v0 needs to be restored as we used it as temp
    lw        v0, 8(at)     # Get v0 back from memory
    sw        $2, 4(at)     # Store it in the result position
    b         End           # 
    nop                     # Restore is already done
'''
+ '\n'.join([save_reg % (i, i) for i in range(3, 32)]) +
'''
End:
    ori       at, at, 0x200 # Was save address, now points to 0xff200200
    jalr      zero, at      # jump back to beginning
    mfc0      at, desave    # restore at
    ''',
    names={
        0xff200000:'index',
        0xff200004:'result',
    },
    doc='Read a GP register',
    assembled=dict(
        # [[[cog
        # scan._precog_list(cog, scan.ReadRegister)
        # ]]]
        mips32=[
          (0xff200200, 0x00000000), # nop       
          (0xff200204, 0x00000000), # nop       
          (0xff200208, 0x10000021), # b         0xff200290
          (0xff20020c, 0x4081f800), # mtc0      at, DESAVE
          (0xff200210, 0xff2002b8), # .word     0xff2002b8
          (0xff200214, 0xff2002c4), # .word     0xff2002c4
          (0xff200218, 0xff2002dc), # .word     0xff2002dc
          (0xff20021c, 0xff2002ec), # .word     0xff2002ec
          (0xff200220, 0xff2002f8), # .word     0xff2002f8
          (0xff200224, 0xff200304), # .word     0xff200304
          (0xff200228, 0xff200310), # .word     0xff200310
          (0xff20022c, 0xff20031c), # .word     0xff20031c
          (0xff200230, 0xff200328), # .word     0xff200328
          (0xff200234, 0xff200334), # .word     0xff200334
          (0xff200238, 0xff200340), # .word     0xff200340
          (0xff20023c, 0xff20034c), # .word     0xff20034c
          (0xff200240, 0xff200358), # .word     0xff200358
          (0xff200244, 0xff200364), # .word     0xff200364
          (0xff200248, 0xff200370), # .word     0xff200370
          (0xff20024c, 0xff20037c), # .word     0xff20037c
          (0xff200250, 0xff200388), # .word     0xff200388
          (0xff200254, 0xff200394), # .word     0xff200394
          (0xff200258, 0xff2003a0), # .word     0xff2003a0
          (0xff20025c, 0xff2003ac), # .word     0xff2003ac
          (0xff200260, 0xff2003b8), # .word     0xff2003b8
          (0xff200264, 0xff2003c4), # .word     0xff2003c4
          (0xff200268, 0xff2003d0), # .word     0xff2003d0
          (0xff20026c, 0xff2003dc), # .word     0xff2003dc
          (0xff200270, 0xff2003e8), # .word     0xff2003e8
          (0xff200274, 0xff2003f4), # .word     0xff2003f4
          (0xff200278, 0xff200400), # .word     0xff200400
          (0xff20027c, 0xff20040c), # .word     0xff20040c
          (0xff200280, 0xff200418), # .word     0xff200418
          (0xff200284, 0xff200424), # .word     0xff200424
          (0xff200288, 0xff200430), # .word     0xff200430
          (0xff20028c, 0xff20043c), # .word     0xff20043c
          (0xff200290, 0x3c01ff20), # lui       at, 0xff20
          (0xff200294, 0xac220008), # sw        v0, 8(at)
          (0xff200298, 0x8c210000), # lw        at, 0(at)
          (0xff20029c, 0x00010880), # sll       at, at, 0x2
          (0xff2002a0, 0x3c02ff20), # lui       v0, 0xff20
          (0xff2002a4, 0x24420210), # addiu     v0, v0, 528
          (0xff2002a8, 0x00221021), # addu      v0, at, v0
          (0xff2002ac, 0x8c420000), # lw        v0, 0(v0)
          (0xff2002b0, 0x00400009), # jalr      zero, v0
          (0xff2002b4, 0x3c01ff20), # lui       at, 0xff20
          (0xff2002b8, 0xac200004), # sw        zero, 4(at)
          (0xff2002bc, 0x10000062), # b         0xff200448
          (0xff2002c0, 0x8c220008), # lw        v0, 8(at)
          (0xff2002c4, 0x00201025), # move      v0, at
          (0xff2002c8, 0x4001f800), # mfc0      at, DESAVE
          (0xff2002cc, 0xac410004), # sw        at, 4(v0)
          (0xff2002d0, 0x00400825), # move      at, v0
          (0xff2002d4, 0x1000005c), # b         0xff200448
          (0xff2002d8, 0x8c220008), # lw        v0, 8(at)
          (0xff2002dc, 0x8c220008), # lw        v0, 8(at)
          (0xff2002e0, 0xac220004), # sw        v0, 4(at)
          (0xff2002e4, 0x10000058), # b         0xff200448
          (0xff2002e8, 0x00000000), # nop       
          (0xff2002ec, 0xac230004), # sw        v1, 4(at)
          (0xff2002f0, 0x10000055), # b         0xff200448
          (0xff2002f4, 0x8c220008), # lw        v0, 8(at)
          (0xff2002f8, 0xac240004), # sw        a0, 4(at)
          (0xff2002fc, 0x10000052), # b         0xff200448
          (0xff200300, 0x8c220008), # lw        v0, 8(at)
          (0xff200304, 0xac250004), # sw        a1, 4(at)
          (0xff200308, 0x1000004f), # b         0xff200448
          (0xff20030c, 0x8c220008), # lw        v0, 8(at)
          (0xff200310, 0xac260004), # sw        a2, 4(at)
          (0xff200314, 0x1000004c), # b         0xff200448
          (0xff200318, 0x8c220008), # lw        v0, 8(at)
          (0xff20031c, 0xac270004), # sw        a3, 4(at)
          (0xff200320, 0x10000049), # b         0xff200448
          (0xff200324, 0x8c220008), # lw        v0, 8(at)
          (0xff200328, 0xac280004), # sw        t0, 4(at)
          (0xff20032c, 0x10000046), # b         0xff200448
          (0xff200330, 0x8c220008), # lw        v0, 8(at)
          (0xff200334, 0xac290004), # sw        t1, 4(at)
          (0xff200338, 0x10000043), # b         0xff200448
          (0xff20033c, 0x8c220008), # lw        v0, 8(at)
          (0xff200340, 0xac2a0004), # sw        t2, 4(at)
          (0xff200344, 0x10000040), # b         0xff200448
          (0xff200348, 0x8c220008), # lw        v0, 8(at)
          (0xff20034c, 0xac2b0004), # sw        t3, 4(at)
          (0xff200350, 0x1000003d), # b         0xff200448
          (0xff200354, 0x8c220008), # lw        v0, 8(at)
          (0xff200358, 0xac2c0004), # sw        t4, 4(at)
          (0xff20035c, 0x1000003a), # b         0xff200448
          (0xff200360, 0x8c220008), # lw        v0, 8(at)
          (0xff200364, 0xac2d0004), # sw        t5, 4(at)
          (0xff200368, 0x10000037), # b         0xff200448
          (0xff20036c, 0x8c220008), # lw        v0, 8(at)
          (0xff200370, 0xac2e0004), # sw        t6, 4(at)
          (0xff200374, 0x10000034), # b         0xff200448
          (0xff200378, 0x8c220008), # lw        v0, 8(at)
          (0xff20037c, 0xac2f0004), # sw        t7, 4(at)
          (0xff200380, 0x10000031), # b         0xff200448
          (0xff200384, 0x8c220008), # lw        v0, 8(at)
          (0xff200388, 0xac300004), # sw        s0, 4(at)
          (0xff20038c, 0x1000002e), # b         0xff200448
          (0xff200390, 0x8c220008), # lw        v0, 8(at)
          (0xff200394, 0xac310004), # sw        s1, 4(at)
          (0xff200398, 0x1000002b), # b         0xff200448
          (0xff20039c, 0x8c220008), # lw        v0, 8(at)
          (0xff2003a0, 0xac320004), # sw        s2, 4(at)
          (0xff2003a4, 0x10000028), # b         0xff200448
          (0xff2003a8, 0x8c220008), # lw        v0, 8(at)
          (0xff2003ac, 0xac330004), # sw        s3, 4(at)
          (0xff2003b0, 0x10000025), # b         0xff200448
          (0xff2003b4, 0x8c220008), # lw        v0, 8(at)
          (0xff2003b8, 0xac340004), # sw        s4, 4(at)
          (0xff2003bc, 0x10000022), # b         0xff200448
          (0xff2003c0, 0x8c220008), # lw        v0, 8(at)
          (0xff2003c4, 0xac350004), # sw        s5, 4(at)
          (0xff2003c8, 0x1000001f), # b         0xff200448
          (0xff2003cc, 0x8c220008), # lw        v0, 8(at)
          (0xff2003d0, 0xac360004), # sw        s6, 4(at)
          (0xff2003d4, 0x1000001c), # b         0xff200448
          (0xff2003d8, 0x8c220008), # lw        v0, 8(at)
          (0xff2003dc, 0xac370004), # sw        s7, 4(at)
          (0xff2003e0, 0x10000019), # b         0xff200448
          (0xff2003e4, 0x8c220008), # lw        v0, 8(at)
          (0xff2003e8, 0xac380004), # sw        t8, 4(at)
          (0xff2003ec, 0x10000016), # b         0xff200448
          (0xff2003f0, 0x8c220008), # lw        v0, 8(at)
          (0xff2003f4, 0xac390004), # sw        t9, 4(at)
          (0xff2003f8, 0x10000013), # b         0xff200448
          (0xff2003fc, 0x8c220008), # lw        v0, 8(at)
          (0xff200400, 0xac3a0004), # sw        k0, 4(at)
          (0xff200404, 0x10000010), # b         0xff200448
          (0xff200408, 0x8c220008), # lw        v0, 8(at)
          (0xff20040c, 0xac3b0004), # sw        k1, 4(at)
          (0xff200410, 0x1000000d), # b         0xff200448
          (0xff200414, 0x8c220008), # lw        v0, 8(at)
          (0xff200418, 0xac3c0004), # sw        gp, 4(at)
          (0xff20041c, 0x1000000a), # b         0xff200448
          (0xff200420, 0x8c220008), # lw        v0, 8(at)
          (0xff200424, 0xac3d0004), # sw        sp, 4(at)
          (0xff200428, 0x10000007), # b         0xff200448
          (0xff20042c, 0x8c220008), # lw        v0, 8(at)
          (0xff200430, 0xac3e0004), # sw        s8, 4(at)
          (0xff200434, 0x10000004), # b         0xff200448
          (0xff200438, 0x8c220008), # lw        v0, 8(at)
          (0xff20043c, 0xac3f0004), # sw        ra, 4(at)
          (0xff200440, 0x10000001), # b         0xff200448
          (0xff200444, 0x8c220008), # lw        v0, 8(at)
          (0xff200448, 0x34210200), # ori       at, at, 0x200
          (0xff20044c, 0x00200009), # jalr      zero, at
          (0xff200450, 0x4001f800), # mfc0      at, DESAVE
        ],
        micromips=[
          (0xff200200, 0x0c00    ), # nop       
          (0xff200202, 0x0c00    ), # nop       
          (0xff200204, 0xcc43    ), # b         0xff20028c
          (0xff200206, 0x003f02fc), # mtc0      at, DESAVE
          (0xff20020a, 0x0c00    ), # nop       
          (0xff20020c, 0xff2002b3), # lw        t9, 691(zero)
          (0xff200210, 0xff2002bd), # lw        t9, 701(zero)
          (0xff200214, 0xff2002cf), # lw        t9, 719(zero)
          (0xff200218, 0xff2002db), # lw        t9, 731(zero)
          (0xff20021c, 0xff2002e5), # lw        t9, 741(zero)
          (0xff200220, 0xff2002ef), # lw        t9, 751(zero)
          (0xff200224, 0xff2002f9), # lw        t9, 761(zero)
          (0xff200228, 0xff200303), # lw        t9, 771(zero)
          (0xff20022c, 0xff20030d), # lw        t9, 781(zero)
          (0xff200230, 0xff200317), # lw        t9, 791(zero)
          (0xff200234, 0xff200321), # lw        t9, 801(zero)
          (0xff200238, 0xff20032b), # lw        t9, 811(zero)
          (0xff20023c, 0xff200335), # lw        t9, 821(zero)
          (0xff200240, 0xff20033f), # lw        t9, 831(zero)
          (0xff200244, 0xff200349), # lw        t9, 841(zero)
          (0xff200248, 0xff200353), # lw        t9, 851(zero)
          (0xff20024c, 0xff20035d), # lw        t9, 861(zero)
          (0xff200250, 0xff200367), # lw        t9, 871(zero)
          (0xff200254, 0xff200371), # lw        t9, 881(zero)
          (0xff200258, 0xff20037b), # lw        t9, 891(zero)
          (0xff20025c, 0xff200385), # lw        t9, 901(zero)
          (0xff200260, 0xff20038f), # lw        t9, 911(zero)
          (0xff200264, 0xff200399), # lw        t9, 921(zero)
          (0xff200268, 0xff2003a3), # lw        t9, 931(zero)
          (0xff20026c, 0xff2003ad), # lw        t9, 941(zero)
          (0xff200270, 0xff2003b7), # lw        t9, 951(zero)
          (0xff200274, 0xff2003c1), # lw        t9, 961(zero)
          (0xff200278, 0xff2003cb), # lw        t9, 971(zero)
          (0xff20027c, 0xff2003d5), # lw        t9, 981(zero)
          (0xff200280, 0xff2003df), # lw        t9, 991(zero)
          (0xff200284, 0xff2003e9), # lw        t9, 1001(zero)
          (0xff200288, 0xff2003f3), # lw        t9, 1011(zero)
          (0xff20028c, 0x41a1ff20), # lui       at, 0xff20
          (0xff200290, 0xf8410008), # sw        v0, 8(at)
          (0xff200294, 0xfc210000), # lw        at, 0(at)
          (0xff200298, 0x00211000), # sll       at, at, 0x2
          (0xff20029c, 0x41a2ff20), # lui       v0, 0xff20
          (0xff2002a0, 0x3042020c), # addiu     v0, v0, 524
          (0xff2002a4, 0x00411150), # addu      v0, at, v0
          (0xff2002a8, 0x6920    ), # lw        v0, 0(v0)
          (0xff2002aa, 0x00020f3c), # jr        v0
          (0xff2002ae, 0x41a1ff20), # lui       at, 0xff20
          (0xff2002b2, 0xf8010004), # sw        zero, 4(at)
          (0xff2002b6, 0xcca2    ), # b         0xff2003fc
          (0xff2002b8, 0xfc410008), # lw        v0, 8(at)
          (0xff2002bc, 0x0c41    ), # move      v0, at
          (0xff2002be, 0x003f00fc), # mfc0      at, DESAVE
          (0xff2002c2, 0xf8220004), # sw        at, 4(v0)
          (0xff2002c6, 0x0c22    ), # move      at, v0
          (0xff2002c8, 0xcc99    ), # b         0xff2003fc
          (0xff2002ca, 0xfc410008), # lw        v0, 8(at)
          (0xff2002ce, 0xfc410008), # lw        v0, 8(at)
          (0xff2002d2, 0xf8410004), # sw        v0, 4(at)
          (0xff2002d6, 0xcc92    ), # b         0xff2003fc
          (0xff2002d8, 0x0c00    ), # nop       
          (0xff2002da, 0xf8610004), # sw        v1, 4(at)
          (0xff2002de, 0xcc8e    ), # b         0xff2003fc
          (0xff2002e0, 0xfc410008), # lw        v0, 8(at)
          (0xff2002e4, 0xf8810004), # sw        a0, 4(at)
          (0xff2002e8, 0xcc89    ), # b         0xff2003fc
          (0xff2002ea, 0xfc410008), # lw        v0, 8(at)
          (0xff2002ee, 0xf8a10004), # sw        a1, 4(at)
          (0xff2002f2, 0xcc84    ), # b         0xff2003fc
          (0xff2002f4, 0xfc410008), # lw        v0, 8(at)
          (0xff2002f8, 0xf8c10004), # sw        a2, 4(at)
          (0xff2002fc, 0xcc7f    ), # b         0xff2003fc
          (0xff2002fe, 0xfc410008), # lw        v0, 8(at)
          (0xff200302, 0xf8e10004), # sw        a3, 4(at)
          (0xff200306, 0xcc7a    ), # b         0xff2003fc
          (0xff200308, 0xfc410008), # lw        v0, 8(at)
          (0xff20030c, 0xf9010004), # sw        t0, 4(at)
          (0xff200310, 0xcc75    ), # b         0xff2003fc
          (0xff200312, 0xfc410008), # lw        v0, 8(at)
          (0xff200316, 0xf9210004), # sw        t1, 4(at)
          (0xff20031a, 0xcc70    ), # b         0xff2003fc
          (0xff20031c, 0xfc410008), # lw        v0, 8(at)
          (0xff200320, 0xf9410004), # sw        t2, 4(at)
          (0xff200324, 0xcc6b    ), # b         0xff2003fc
          (0xff200326, 0xfc410008), # lw        v0, 8(at)
          (0xff20032a, 0xf9610004), # sw        t3, 4(at)
          (0xff20032e, 0xcc66    ), # b         0xff2003fc
          (0xff200330, 0xfc410008), # lw        v0, 8(at)
          (0xff200334, 0xf9810004), # sw        t4, 4(at)
          (0xff200338, 0xcc61    ), # b         0xff2003fc
          (0xff20033a, 0xfc410008), # lw        v0, 8(at)
          (0xff20033e, 0xf9a10004), # sw        t5, 4(at)
          (0xff200342, 0xcc5c    ), # b         0xff2003fc
          (0xff200344, 0xfc410008), # lw        v0, 8(at)
          (0xff200348, 0xf9c10004), # sw        t6, 4(at)
          (0xff20034c, 0xcc57    ), # b         0xff2003fc
          (0xff20034e, 0xfc410008), # lw        v0, 8(at)
          (0xff200352, 0xf9e10004), # sw        t7, 4(at)
          (0xff200356, 0xcc52    ), # b         0xff2003fc
          (0xff200358, 0xfc410008), # lw        v0, 8(at)
          (0xff20035c, 0xfa010004), # sw        s0, 4(at)
          (0xff200360, 0xcc4d    ), # b         0xff2003fc
          (0xff200362, 0xfc410008), # lw        v0, 8(at)
          (0xff200366, 0xfa210004), # sw        s1, 4(at)
          (0xff20036a, 0xcc48    ), # b         0xff2003fc
          (0xff20036c, 0xfc410008), # lw        v0, 8(at)
          (0xff200370, 0xfa410004), # sw        s2, 4(at)
          (0xff200374, 0xcc43    ), # b         0xff2003fc
          (0xff200376, 0xfc410008), # lw        v0, 8(at)
          (0xff20037a, 0xfa610004), # sw        s3, 4(at)
          (0xff20037e, 0xcc3e    ), # b         0xff2003fc
          (0xff200380, 0xfc410008), # lw        v0, 8(at)
          (0xff200384, 0xfa810004), # sw        s4, 4(at)
          (0xff200388, 0xcc39    ), # b         0xff2003fc
          (0xff20038a, 0xfc410008), # lw        v0, 8(at)
          (0xff20038e, 0xfaa10004), # sw        s5, 4(at)
          (0xff200392, 0xcc34    ), # b         0xff2003fc
          (0xff200394, 0xfc410008), # lw        v0, 8(at)
          (0xff200398, 0xfac10004), # sw        s6, 4(at)
          (0xff20039c, 0xcc2f    ), # b         0xff2003fc
          (0xff20039e, 0xfc410008), # lw        v0, 8(at)
          (0xff2003a2, 0xfae10004), # sw        s7, 4(at)
          (0xff2003a6, 0xcc2a    ), # b         0xff2003fc
          (0xff2003a8, 0xfc410008), # lw        v0, 8(at)
          (0xff2003ac, 0xfb010004), # sw        t8, 4(at)
          (0xff2003b0, 0xcc25    ), # b         0xff2003fc
          (0xff2003b2, 0xfc410008), # lw        v0, 8(at)
          (0xff2003b6, 0xfb210004), # sw        t9, 4(at)
          (0xff2003ba, 0xcc20    ), # b         0xff2003fc
          (0xff2003bc, 0xfc410008), # lw        v0, 8(at)
          (0xff2003c0, 0xfb410004), # sw        k0, 4(at)
          (0xff2003c4, 0xcc1b    ), # b         0xff2003fc
          (0xff2003c6, 0xfc410008), # lw        v0, 8(at)
          (0xff2003ca, 0xfb610004), # sw        k1, 4(at)
          (0xff2003ce, 0xcc16    ), # b         0xff2003fc
          (0xff2003d0, 0xfc410008), # lw        v0, 8(at)
          (0xff2003d4, 0xfb810004), # sw        gp, 4(at)
          (0xff2003d8, 0xcc11    ), # b         0xff2003fc
          (0xff2003da, 0xfc410008), # lw        v0, 8(at)
          (0xff2003de, 0xfba10004), # sw        sp, 4(at)
          (0xff2003e2, 0xcc0c    ), # b         0xff2003fc
          (0xff2003e4, 0xfc410008), # lw        v0, 8(at)
          (0xff2003e8, 0xfbc10004), # sw        s8, 4(at)
          (0xff2003ec, 0xcc07    ), # b         0xff2003fc
          (0xff2003ee, 0xfc410008), # lw        v0, 8(at)
          (0xff2003f2, 0xfbe10004), # sw        ra, 4(at)
          (0xff2003f6, 0xcc02    ), # b         0xff2003fc
          (0xff2003f8, 0xfc410008), # lw        v0, 8(at)
          (0xff2003fc, 0x50210200), # ori       at, at, 0x200
          (0xff200400, 0x00010f3c), # jr        at
          (0xff200404, 0x003f00fc), # mfc0      at, DESAVE
        ],
        mips32r6=mips32,
        mips64r6=[
          (0xff200200, 0x00000000), # nop       
          (0xff200204, 0x00000000), # nop       
          (0xff200208, 0x10000021), # b         0x00000000ff200290
          (0xff20020c, 0x4081f800), # mtc0      at, DESAVE
          (0xff200210, 0xff2002b8), # sd        zero, 696(t9)
          (0xff200214, 0xff2002c4), # sd        zero, 708(t9)
          (0xff200218, 0xff2002dc), # sd        zero, 732(t9)
          (0xff20021c, 0xff2002ec), # sd        zero, 748(t9)
          (0xff200220, 0xff2002f8), # sd        zero, 760(t9)
          (0xff200224, 0xff200304), # sd        zero, 772(t9)
          (0xff200228, 0xff200310), # sd        zero, 784(t9)
          (0xff20022c, 0xff20031c), # sd        zero, 796(t9)
          (0xff200230, 0xff200328), # sd        zero, 808(t9)
          (0xff200234, 0xff200334), # sd        zero, 820(t9)
          (0xff200238, 0xff200340), # sd        zero, 832(t9)
          (0xff20023c, 0xff20034c), # sd        zero, 844(t9)
          (0xff200240, 0xff200358), # sd        zero, 856(t9)
          (0xff200244, 0xff200364), # sd        zero, 868(t9)
          (0xff200248, 0xff200370), # sd        zero, 880(t9)
          (0xff20024c, 0xff20037c), # sd        zero, 892(t9)
          (0xff200250, 0xff200388), # sd        zero, 904(t9)
          (0xff200254, 0xff200394), # sd        zero, 916(t9)
          (0xff200258, 0xff2003a0), # sd        zero, 928(t9)
          (0xff20025c, 0xff2003ac), # sd        zero, 940(t9)
          (0xff200260, 0xff2003b8), # sd        zero, 952(t9)
          (0xff200264, 0xff2003c4), # sd        zero, 964(t9)
          (0xff200268, 0xff2003d0), # sd        zero, 976(t9)
          (0xff20026c, 0xff2003dc), # sd        zero, 988(t9)
          (0xff200270, 0xff2003e8), # sd        zero, 1000(t9)
          (0xff200274, 0xff2003f4), # sd        zero, 1012(t9)
          (0xff200278, 0xff200400), # sd        zero, 1024(t9)
          (0xff20027c, 0xff20040c), # sd        zero, 1036(t9)
          (0xff200280, 0xff200418), # sd        zero, 1048(t9)
          (0xff200284, 0xff200424), # sd        zero, 1060(t9)
          (0xff200288, 0xff200430), # sd        zero, 1072(t9)
          (0xff20028c, 0xff20043c), # sd        zero, 1084(t9)
          (0xff200290, 0x3c01ff20), # lui       at,  0xff20
          (0xff200294, 0xac220008), # sw        v0, 8(at)
          (0xff200298, 0x8c210000), # lw        at, 0(at)
          (0xff20029c, 0x00010880), # sll       at, at, 0x2
          (0xff2002a0, 0x3c02ff20), # lui       v0,  0xff20
          (0xff2002a4, 0x24420210), # addiu     v0, v0, 528
          (0xff2002a8, 0x00221021), # addu      v0, at, v0
          (0xff2002ac, 0x8c420000), # lw        v0, 0(v0)
          (0xff2002b0, 0x00400009), # jr        v0
          (0xff2002b4, 0x3c01ff20), # lui       at,  0xff20
          (0xff2002b8, 0xac200004), # sw        zero, 4(at)
          (0xff2002bc, 0x10000062), # b         0x00000000ff200448
          (0xff2002c0, 0x8c220008), # lw        v0, 8(at)
          (0xff2002c4, 0x00201025), # move      v0, at
          (0xff2002c8, 0x4001f800), # mfc0      at, DESAVE
          (0xff2002cc, 0xac410004), # sw        at, 4(v0)
          (0xff2002d0, 0x00400825), # move      at, v0
          (0xff2002d4, 0x1000005c), # b         0x00000000ff200448
          (0xff2002d8, 0x8c220008), # lw        v0, 8(at)
          (0xff2002dc, 0x8c220008), # lw        v0, 8(at)
          (0xff2002e0, 0xac220004), # sw        v0, 4(at)
          (0xff2002e4, 0x10000058), # b         0x00000000ff200448
          (0xff2002e8, 0x00000000), # nop       
          (0xff2002ec, 0xac230004), # sw        v1, 4(at)
          (0xff2002f0, 0x10000055), # b         0x00000000ff200448
          (0xff2002f4, 0x8c220008), # lw        v0, 8(at)
          (0xff2002f8, 0xac240004), # sw        a0, 4(at)
          (0xff2002fc, 0x10000052), # b         0x00000000ff200448
          (0xff200300, 0x8c220008), # lw        v0, 8(at)
          (0xff200304, 0xac250004), # sw        a1, 4(at)
          (0xff200308, 0x1000004f), # b         0x00000000ff200448
          (0xff20030c, 0x8c220008), # lw        v0, 8(at)
          (0xff200310, 0xac260004), # sw        a2, 4(at)
          (0xff200314, 0x1000004c), # b         0x00000000ff200448
          (0xff200318, 0x8c220008), # lw        v0, 8(at)
          (0xff20031c, 0xac270004), # sw        a3, 4(at)
          (0xff200320, 0x10000049), # b         0x00000000ff200448
          (0xff200324, 0x8c220008), # lw        v0, 8(at)
          (0xff200328, 0xac280004), # sw        t0, 4(at)
          (0xff20032c, 0x10000046), # b         0x00000000ff200448
          (0xff200330, 0x8c220008), # lw        v0, 8(at)
          (0xff200334, 0xac290004), # sw        t1, 4(at)
          (0xff200338, 0x10000043), # b         0x00000000ff200448
          (0xff20033c, 0x8c220008), # lw        v0, 8(at)
          (0xff200340, 0xac2a0004), # sw        t2, 4(at)
          (0xff200344, 0x10000040), # b         0x00000000ff200448
          (0xff200348, 0x8c220008), # lw        v0, 8(at)
          (0xff20034c, 0xac2b0004), # sw        t3, 4(at)
          (0xff200350, 0x1000003d), # b         0x00000000ff200448
          (0xff200354, 0x8c220008), # lw        v0, 8(at)
          (0xff200358, 0xac2c0004), # sw        t4, 4(at)
          (0xff20035c, 0x1000003a), # b         0x00000000ff200448
          (0xff200360, 0x8c220008), # lw        v0, 8(at)
          (0xff200364, 0xac2d0004), # sw        t5, 4(at)
          (0xff200368, 0x10000037), # b         0x00000000ff200448
          (0xff20036c, 0x8c220008), # lw        v0, 8(at)
          (0xff200370, 0xac2e0004), # sw        t6, 4(at)
          (0xff200374, 0x10000034), # b         0x00000000ff200448
          (0xff200378, 0x8c220008), # lw        v0, 8(at)
          (0xff20037c, 0xac2f0004), # sw        t7, 4(at)
          (0xff200380, 0x10000031), # b         0x00000000ff200448
          (0xff200384, 0x8c220008), # lw        v0, 8(at)
          (0xff200388, 0xac300004), # sw        s0, 4(at)
          (0xff20038c, 0x1000002e), # b         0x00000000ff200448
          (0xff200390, 0x8c220008), # lw        v0, 8(at)
          (0xff200394, 0xac310004), # sw        s1, 4(at)
          (0xff200398, 0x1000002b), # b         0x00000000ff200448
          (0xff20039c, 0x8c220008), # lw        v0, 8(at)
          (0xff2003a0, 0xac320004), # sw        s2, 4(at)
          (0xff2003a4, 0x10000028), # b         0x00000000ff200448
          (0xff2003a8, 0x8c220008), # lw        v0, 8(at)
          (0xff2003ac, 0xac330004), # sw        s3, 4(at)
          (0xff2003b0, 0x10000025), # b         0x00000000ff200448
          (0xff2003b4, 0x8c220008), # lw        v0, 8(at)
          (0xff2003b8, 0xac340004), # sw        s4, 4(at)
          (0xff2003bc, 0x10000022), # b         0x00000000ff200448
          (0xff2003c0, 0x8c220008), # lw        v0, 8(at)
          (0xff2003c4, 0xac350004), # sw        s5, 4(at)
          (0xff2003c8, 0x1000001f), # b         0x00000000ff200448
          (0xff2003cc, 0x8c220008), # lw        v0, 8(at)
          (0xff2003d0, 0xac360004), # sw        s6, 4(at)
          (0xff2003d4, 0x1000001c), # b         0x00000000ff200448
          (0xff2003d8, 0x8c220008), # lw        v0, 8(at)
          (0xff2003dc, 0xac370004), # sw        s7, 4(at)
          (0xff2003e0, 0x10000019), # b         0x00000000ff200448
          (0xff2003e4, 0x8c220008), # lw        v0, 8(at)
          (0xff2003e8, 0xac380004), # sw        t8, 4(at)
          (0xff2003ec, 0x10000016), # b         0x00000000ff200448
          (0xff2003f0, 0x8c220008), # lw        v0, 8(at)
          (0xff2003f4, 0xac390004), # sw        t9, 4(at)
          (0xff2003f8, 0x10000013), # b         0x00000000ff200448
          (0xff2003fc, 0x8c220008), # lw        v0, 8(at)
          (0xff200400, 0xac3a0004), # sw        k0, 4(at)
          (0xff200404, 0x10000010), # b         0x00000000ff200448
          (0xff200408, 0x8c220008), # lw        v0, 8(at)
          (0xff20040c, 0xac3b0004), # sw        k1, 4(at)
          (0xff200410, 0x1000000d), # b         0x00000000ff200448
          (0xff200414, 0x8c220008), # lw        v0, 8(at)
          (0xff200418, 0xac3c0004), # sw        gp, 4(at)
          (0xff20041c, 0x1000000a), # b         0x00000000ff200448
          (0xff200420, 0x8c220008), # lw        v0, 8(at)
          (0xff200424, 0xac3d0004), # sw        sp, 4(at)
          (0xff200428, 0x10000007), # b         0x00000000ff200448
          (0xff20042c, 0x8c220008), # lw        v0, 8(at)
          (0xff200430, 0xac3e0004), # sw        s8, 4(at)
          (0xff200434, 0x10000004), # b         0x00000000ff200448
          (0xff200438, 0x8c220008), # lw        v0, 8(at)
          (0xff20043c, 0xac3f0004), # sw        ra, 4(at)
          (0xff200440, 0x10000001), # b         0x00000000ff200448
          (0xff200444, 0x8c220008), # lw        v0, 8(at)
          (0xff200448, 0x34210200), # ori       at, at, 0x200
          (0xff20044c, 0x00200009), # jr        at
          (0xff200450, 0x4001f800), # mfc0      at, DESAVE
        ],
        # [[[end]]]
    )
))

ReadRegs = builtin_list(DmsegList('ReadRegs', '''\
    nop
    nop
    mtc0      v0, desave    # save v0
    lui       v0, 0xff20
    sw        $0, 0(v0)
    sw        $1, 0(v0)  # now we have saved at, use at for offset for future
    mfc0      v0, desave   #  restore v0
    mtc0      at, desave    # save at
    lui       at, 0xff20
    sw        $2, 0(at)
    sw        $3, 0(at)
    sw        $4, 0(at)
    sw        $5, 0(at)
    sw        $6, 0(at)
    sw        $7, 0(at)
    sw        $8, 0(at)
    sw        $9, 0(at)
    sw        $10, 0(at)
    sw        $11, 0(at)
    sw        $12, 0(at)
    sw        $13, 0(at)
    sw        $14, 0(at)
    sw        $15, 0(at)
    sw        $16, 0(at)
    sw        $17, 0(at)
    sw        $18, 0(at)
    sw        $19, 0(at)
    sw        $20, 0(at)
    sw        $21, 0(at)
    sw        $22, 0(at)
    sw        $23, 0(at)
    sw        $24, 0(at)
    sw        $25, 0(at)
    sw        $26, 0(at)
    sw        $27, 0(at)
    sw        $28, 0(at)
    sw        $29, 0(at)
    sw        $30, 0(at)
    sw        $31, 0(at)
    ori       at, at, 0x200
    jalr      zero, at
    mfc0      at, desave   #  restore at
    ''',
    names={
        0xff200000:'result[]',
    },
    doc='Read all of the GP registers',
    assembled=dict(
        # [[[cog
        # scan._precog_list(cog, scan.ReadRegs)
        # ]]]
        mips32=[
          (0xff200200, 0x00000000), # nop       
          (0xff200204, 0x00000000), # nop       
          (0xff200208, 0x4082f800), # mtc0      v0, DESAVE
          (0xff20020c, 0x3c02ff20), # lui       v0, 0xff20
          (0xff200210, 0xac400000), # sw        zero, 0(v0)
          (0xff200214, 0xac410000), # sw        at, 0(v0)
          (0xff200218, 0x4002f800), # mfc0      v0, DESAVE
          (0xff20021c, 0x4081f800), # mtc0      at, DESAVE
          (0xff200220, 0x3c01ff20), # lui       at, 0xff20
          (0xff200224, 0xac220000), # sw        v0, 0(at)
          (0xff200228, 0xac230000), # sw        v1, 0(at)
          (0xff20022c, 0xac240000), # sw        a0, 0(at)
          (0xff200230, 0xac250000), # sw        a1, 0(at)
          (0xff200234, 0xac260000), # sw        a2, 0(at)
          (0xff200238, 0xac270000), # sw        a3, 0(at)
          (0xff20023c, 0xac280000), # sw        t0, 0(at)
          (0xff200240, 0xac290000), # sw        t1, 0(at)
          (0xff200244, 0xac2a0000), # sw        t2, 0(at)
          (0xff200248, 0xac2b0000), # sw        t3, 0(at)
          (0xff20024c, 0xac2c0000), # sw        t4, 0(at)
          (0xff200250, 0xac2d0000), # sw        t5, 0(at)
          (0xff200254, 0xac2e0000), # sw        t6, 0(at)
          (0xff200258, 0xac2f0000), # sw        t7, 0(at)
          (0xff20025c, 0xac300000), # sw        s0, 0(at)
          (0xff200260, 0xac310000), # sw        s1, 0(at)
          (0xff200264, 0xac320000), # sw        s2, 0(at)
          (0xff200268, 0xac330000), # sw        s3, 0(at)
          (0xff20026c, 0xac340000), # sw        s4, 0(at)
          (0xff200270, 0xac350000), # sw        s5, 0(at)
          (0xff200274, 0xac360000), # sw        s6, 0(at)
          (0xff200278, 0xac370000), # sw        s7, 0(at)
          (0xff20027c, 0xac380000), # sw        t8, 0(at)
          (0xff200280, 0xac390000), # sw        t9, 0(at)
          (0xff200284, 0xac3a0000), # sw        k0, 0(at)
          (0xff200288, 0xac3b0000), # sw        k1, 0(at)
          (0xff20028c, 0xac3c0000), # sw        gp, 0(at)
          (0xff200290, 0xac3d0000), # sw        sp, 0(at)
          (0xff200294, 0xac3e0000), # sw        s8, 0(at)
          (0xff200298, 0xac3f0000), # sw        ra, 0(at)
          (0xff20029c, 0x34210200), # ori       at, at, 0x200
          (0xff2002a0, 0x00200009), # jalr      zero, at
          (0xff2002a4, 0x4001f800), # mfc0      at, DESAVE
        ],
        micromips=[
          (0xff200200, 0x0c00    ), # nop       
          (0xff200202, 0x0c00    ), # nop       
          (0xff200204, 0x005f02fc), # mtc0      v0, DESAVE
          (0xff200208, 0x41a2ff20), # lui       v0, 0xff20
          (0xff20020c, 0xe820    ), # sw        zero, 0(v0)
          (0xff20020e, 0xf8220000), # sw        at, 0(v0)
          (0xff200212, 0x005f00fc), # mfc0      v0, DESAVE
          (0xff200216, 0x003f02fc), # mtc0      at, DESAVE
          (0xff20021a, 0x41a1ff20), # lui       at, 0xff20
          (0xff20021e, 0xf8410000), # sw        v0, 0(at)
          (0xff200222, 0xf8610000), # sw        v1, 0(at)
          (0xff200226, 0xf8810000), # sw        a0, 0(at)
          (0xff20022a, 0xf8a10000), # sw        a1, 0(at)
          (0xff20022e, 0xf8c10000), # sw        a2, 0(at)
          (0xff200232, 0xf8e10000), # sw        a3, 0(at)
          (0xff200236, 0xf9010000), # sw        t0, 0(at)
          (0xff20023a, 0xf9210000), # sw        t1, 0(at)
          (0xff20023e, 0xf9410000), # sw        t2, 0(at)
          (0xff200242, 0xf9610000), # sw        t3, 0(at)
          (0xff200246, 0xf9810000), # sw        t4, 0(at)
          (0xff20024a, 0xf9a10000), # sw        t5, 0(at)
          (0xff20024e, 0xf9c10000), # sw        t6, 0(at)
          (0xff200252, 0xf9e10000), # sw        t7, 0(at)
          (0xff200256, 0xfa010000), # sw        s0, 0(at)
          (0xff20025a, 0xfa210000), # sw        s1, 0(at)
          (0xff20025e, 0xfa410000), # sw        s2, 0(at)
          (0xff200262, 0xfa610000), # sw        s3, 0(at)
          (0xff200266, 0xfa810000), # sw        s4, 0(at)
          (0xff20026a, 0xfaa10000), # sw        s5, 0(at)
          (0xff20026e, 0xfac10000), # sw        s6, 0(at)
          (0xff200272, 0xfae10000), # sw        s7, 0(at)
          (0xff200276, 0xfb010000), # sw        t8, 0(at)
          (0xff20027a, 0xfb210000), # sw        t9, 0(at)
          (0xff20027e, 0xfb410000), # sw        k0, 0(at)
          (0xff200282, 0xfb610000), # sw        k1, 0(at)
          (0xff200286, 0xfb810000), # sw        gp, 0(at)
          (0xff20028a, 0xfba10000), # sw        sp, 0(at)
          (0xff20028e, 0xfbc10000), # sw        s8, 0(at)
          (0xff200292, 0xfbe10000), # sw        ra, 0(at)
          (0xff200296, 0x50210200), # ori       at, at, 0x200
          (0xff20029a, 0x00010f3c), # jr        at
          (0xff20029e, 0x003f00fc), # mfc0      at, DESAVE
          (0xff2002a2, 0x0c00    ), # nop       
        ],
        mips32r6=mips32,
        mips64r6=[
          (0xff200200, 0x00000000), # nop       
          (0xff200204, 0x00000000), # nop       
          (0xff200208, 0x4082f800), # mtc0      v0, DESAVE
          (0xff20020c, 0x3c02ff20), # lui       v0,  0xff20
          (0xff200210, 0xac400000), # sw        zero, 0(v0)
          (0xff200214, 0xac410000), # sw        at, 0(v0)
          (0xff200218, 0x4002f800), # mfc0      v0, DESAVE
          (0xff20021c, 0x4081f800), # mtc0      at, DESAVE
          (0xff200220, 0x3c01ff20), # lui       at,  0xff20
          (0xff200224, 0xac220000), # sw        v0, 0(at)
          (0xff200228, 0xac230000), # sw        v1, 0(at)
          (0xff20022c, 0xac240000), # sw        a0, 0(at)
          (0xff200230, 0xac250000), # sw        a1, 0(at)
          (0xff200234, 0xac260000), # sw        a2, 0(at)
          (0xff200238, 0xac270000), # sw        a3, 0(at)
          (0xff20023c, 0xac280000), # sw        t0, 0(at)
          (0xff200240, 0xac290000), # sw        t1, 0(at)
          (0xff200244, 0xac2a0000), # sw        t2, 0(at)
          (0xff200248, 0xac2b0000), # sw        t3, 0(at)
          (0xff20024c, 0xac2c0000), # sw        t4, 0(at)
          (0xff200250, 0xac2d0000), # sw        t5, 0(at)
          (0xff200254, 0xac2e0000), # sw        t6, 0(at)
          (0xff200258, 0xac2f0000), # sw        t7, 0(at)
          (0xff20025c, 0xac300000), # sw        s0, 0(at)
          (0xff200260, 0xac310000), # sw        s1, 0(at)
          (0xff200264, 0xac320000), # sw        s2, 0(at)
          (0xff200268, 0xac330000), # sw        s3, 0(at)
          (0xff20026c, 0xac340000), # sw        s4, 0(at)
          (0xff200270, 0xac350000), # sw        s5, 0(at)
          (0xff200274, 0xac360000), # sw        s6, 0(at)
          (0xff200278, 0xac370000), # sw        s7, 0(at)
          (0xff20027c, 0xac380000), # sw        t8, 0(at)
          (0xff200280, 0xac390000), # sw        t9, 0(at)
          (0xff200284, 0xac3a0000), # sw        k0, 0(at)
          (0xff200288, 0xac3b0000), # sw        k1, 0(at)
          (0xff20028c, 0xac3c0000), # sw        gp, 0(at)
          (0xff200290, 0xac3d0000), # sw        sp, 0(at)
          (0xff200294, 0xac3e0000), # sw        s8, 0(at)
          (0xff200298, 0xac3f0000), # sw        ra, 0(at)
          (0xff20029c, 0x34210200), # ori       at, at, 0x200
          (0xff2002a0, 0x00200009), # jr        at
          (0xff2002a4, 0x4001f800), # mfc0      at, DESAVE
        ],
        # [[[end]]]
    )
))


ReadConfigs = builtin_list(DmsegList('ReadConfigs', '''\
    nop
    nop
    lui       v1, 0xff20
    mfc0      at, Config
    sw        at, 0(v1)
    mfc0      at, Config1
    sw        at, 0(v1)
    mfc0      at, Config2
    sw        at, 0(v1)
    mfc0      at, Config3
    sw        at, 0(v1)
    mfc0      at, Config4
    sw        at, 0(v1)
    mfc0      at, Config5
    sw        at, 0(v1)
    ori       v1, v1, 0x200
    jalr      zero, v1
    nop
    ''',
    names = {
        0xff200000:'Config[]',
    },
    doc='A list for use with the dmseg command to read Config, Config1-5',
    assembled=dict(
        # [[[cog
        # scan._precog_list(cog, scan.ReadConfigs)
        # ]]]
        mips32=[
          (0xff200200, 0x00000000), # nop       
          (0xff200204, 0x00000000), # nop       
          (0xff200208, 0x3c03ff20), # lui       v1, 0xff20
          (0xff20020c, 0x40018000), # mfc0      at, Config
          (0xff200210, 0xac610000), # sw        at, 0(v1)
          (0xff200214, 0x40018001), # mfc0      at, Config1
          (0xff200218, 0xac610000), # sw        at, 0(v1)
          (0xff20021c, 0x40018002), # mfc0      at, Config2
          (0xff200220, 0xac610000), # sw        at, 0(v1)
          (0xff200224, 0x40018003), # mfc0      at, Config3
          (0xff200228, 0xac610000), # sw        at, 0(v1)
          (0xff20022c, 0x40018004), # mfc0      at, Config4
          (0xff200230, 0xac610000), # sw        at, 0(v1)
          (0xff200234, 0x40018005), # mfc0      at, Config5
          (0xff200238, 0xac610000), # sw        at, 0(v1)
          (0xff20023c, 0x34630200), # ori       v1, v1, 0x200
          (0xff200240, 0x00600009), # jalr      zero, v1
          (0xff200244, 0x00000000), # nop       
        ],
        micromips=[
          (0xff200200, 0x0c00    ), # nop       
          (0xff200202, 0x0c00    ), # nop       
          (0xff200204, 0x41a3ff20), # lui       v1, 0xff20
          (0xff200208, 0x003000fc), # mfc0      at, Config
          (0xff20020c, 0xf8230000), # sw        at, 0(v1)
          (0xff200210, 0x003008fc), # mfc0      at, Config1
          (0xff200214, 0xf8230000), # sw        at, 0(v1)
          (0xff200218, 0x003010fc), # mfc0      at, Config2
          (0xff20021c, 0xf8230000), # sw        at, 0(v1)
          (0xff200220, 0x003018fc), # mfc0      at, Config3
          (0xff200224, 0xf8230000), # sw        at, 0(v1)
          (0xff200228, 0x003020fc), # mfc0      at, Config4
          (0xff20022c, 0xf8230000), # sw        at, 0(v1)
          (0xff200230, 0x003028fc), # mfc0      at, Config5
          (0xff200234, 0xf8230000), # sw        at, 0(v1)
          (0xff200238, 0x50630200), # ori       v1, v1, 0x200
          (0xff20023c, 0x00030f3c), # jr        v1
          (0xff200240, 0x00000000), # nop       
        ],
        mips32r6=mips32,
        mips64r6=[
          (0xff200200, 0x00000000), # nop       
          (0xff200204, 0x00000000), # nop       
          (0xff200208, 0x3c03ff20), # lui       v1,  0xff20
          (0xff20020c, 0x40018000), # mfc0      at, Config
          (0xff200210, 0xac610000), # sw        at, 0(v1)
          (0xff200214, 0x40018001), # mfc0      at, Config1
          (0xff200218, 0xac610000), # sw        at, 0(v1)
          (0xff20021c, 0x40018002), # mfc0      at, Config2
          (0xff200220, 0xac610000), # sw        at, 0(v1)
          (0xff200224, 0x40018003), # mfc0      at, Config3
          (0xff200228, 0xac610000), # sw        at, 0(v1)
          (0xff20022c, 0x40018004), # mfc0      at, Config4
          (0xff200230, 0xac610000), # sw        at, 0(v1)
          (0xff200234, 0x40018005), # mfc0      at, Config5
          (0xff200238, 0xac610000), # sw        at, 0(v1)
          (0xff20023c, 0x34630200), # ori       v1, v1, 0x200
          (0xff200240, 0x00600009), # jr        v1
          (0xff200244, 0x00000000), # nop       
        ],
        # [[[end]]]
    )
))

Read32 = builtin_list(DmsegList('Read32', '''\
      nop
      nop
      mtc0      at, desave    # save at
      lui       at, 0xff20    # at now points at dmseg
      sw        v0, 0x100(at) # save v0, v1, and t0
      sw        v1, 0x104(at)
      sw        t0, 0x108(at)
      lw        v0, 0(at) # address to read
      lw        t0, 4(at) # num of elements
      lw        v1, 0(v0) # read it in
      sw        v1, 8(at) # save it out
      subu      t0, 1     # dec count
      addu      v0, 4     # inc address
      bne       t0, zero, 0xff200224
      nop
      lw        t0, 0x108(at) # restore t0, v1, and v0
      lw        v1, 0x104(at)
      lw        v0, 0x100(at)
      ori       at, at, 0x200
      jalr      zero, at
      mfc0      at, desave   #  restore at
    ''',
    names={
      0xff200000:'address',
      0xff200004:'count',
      0xff200008:'result[]',
    },
    doc='''Read 32-bit values from memory.
    
    [c0v0] >>> dmseg(quiet, Read32(address=0x801660ac, count=8))['result']
    [0xac880000, 0x00000001, 0x00000002, 0x00000003, 0x00000004, 0x24840020, 0xac8affe8, 0xac8bffec]
    ''',
    assembled=dict(
        # [[[cog
        # scan._precog_list(cog, scan.Read32)
        # ]]]
        mips32=[
          (0xff200200, 0x00000000), # nop       
          (0xff200204, 0x00000000), # nop       
          (0xff200208, 0x4081f800), # mtc0      at, DESAVE
          (0xff20020c, 0x3c01ff20), # lui       at, 0xff20
          (0xff200210, 0xac220100), # sw        v0, 256(at)
          (0xff200214, 0xac230104), # sw        v1, 260(at)
          (0xff200218, 0xac280108), # sw        t0, 264(at)
          (0xff20021c, 0x8c220000), # lw        v0, 0(at)
          (0xff200220, 0x8c280004), # lw        t0, 4(at)
          (0xff200224, 0x8c430000), # lw        v1, 0(v0)
          (0xff200228, 0xac230008), # sw        v1, 8(at)
          (0xff20022c, 0x2508ffff), # addiu     t0, t0, -1
          (0xff200230, 0x24420004), # addiu     v0, v0, 4
          (0xff200234, 0x1500fffb), # bnez      t0, 0xff200224
          (0xff200238, 0x00000000), # nop       
          (0xff20023c, 0x8c280108), # lw        t0, 264(at)
          (0xff200240, 0x8c230104), # lw        v1, 260(at)
          (0xff200244, 0x8c220100), # lw        v0, 256(at)
          (0xff200248, 0x34210200), # ori       at, at, 0x200
          (0xff20024c, 0x00200009), # jalr      zero, at
          (0xff200250, 0x4001f800), # mfc0      at, DESAVE
        ],
        micromips=[
          (0xff200200, 0x0c00    ), # nop       
          (0xff200202, 0x0c00    ), # nop       
          (0xff200204, 0x003f02fc), # mtc0      at, DESAVE
          (0xff200208, 0x41a1ff20), # lui       at, 0xff20
          (0xff20020c, 0xf8410100), # sw        v0, 256(at)
          (0xff200210, 0xf8610104), # sw        v1, 260(at)
          (0xff200214, 0xf9010108), # sw        t0, 264(at)
          (0xff200218, 0xfc410000), # lw        v0, 0(at)
          (0xff20021c, 0xfd010004), # lw        t0, 4(at)
          (0xff200220, 0x69a0    ), # lw        v1, 0(v0)
          (0xff200222, 0xf8610008), # sw        v1, 8(at)
          (0xff200226, 0x3108ffff), # addiu     t0, t0, -1
          (0xff20022a, 0x30420004), # addiu     v0, v0, 4
          (0xff20022e, 0xb408fff9), # bnez      t0, 0xff200224
          (0xff200232, 0x0c00    ), # nop       
          (0xff200234, 0xfd010108), # lw        t0, 264(at)
          (0xff200238, 0xfc610104), # lw        v1, 260(at)
          (0xff20023c, 0xfc410100), # lw        v0, 256(at)
          (0xff200240, 0x50210200), # ori       at, at, 0x200
          (0xff200244, 0x00010f3c), # jr        at
          (0xff200248, 0x003f00fc), # mfc0      at, DESAVE
        ],
        mips32r6=mips32,
        mips64r6=[
          (0xff200200, 0x00000000), # nop       
          (0xff200204, 0x00000000), # nop       
          (0xff200208, 0x4081f800), # mtc0      at, DESAVE
          (0xff20020c, 0x3c01ff20), # lui       at,  0xff20
          (0xff200210, 0xac220100), # sw        v0, 256(at)
          (0xff200214, 0xac230104), # sw        v1, 260(at)
          (0xff200218, 0xac280108), # sw        t0, 264(at)
          (0xff20021c, 0x8c220000), # lw        v0, 0(at)
          (0xff200220, 0x8c280004), # lw        t0, 4(at)
          (0xff200224, 0x8c430000), # lw        v1, 0(v0)
          (0xff200228, 0xac230008), # sw        v1, 8(at)
          (0xff20022c, 0x2508ffff), # addiu     t0, t0, -1
          (0xff200230, 0x24420004), # addiu     v0, v0, 4
          (0xff200234, 0x1500fffb), # bnez      t0, 0x00000000ff200224
          (0xff200238, 0x00000000), # nop       
          (0xff20023c, 0x8c280108), # lw        t0, 264(at)
          (0xff200240, 0x8c230104), # lw        v1, 260(at)
          (0xff200244, 0x8c220100), # lw        v0, 256(at)
          (0xff200248, 0x34210200), # ori       at, at, 0x200
          (0xff20024c, 0x00200009), # jr        at
          (0xff200250, 0x4001f800), # mfc0      at, DESAVE
        ],
        # [[[end]]]
    )
))

Write32 = builtin_list(DmsegList('Write32', '''\
      nop
      nop
      mtc0      at, desave
      lui       at, 0xff20
      sw        v0, 264(at)
      sw        v1, 268(at)
      sw        t0, 272(at)
      lw        v0, 0(at) # address to read
      lw        t0, 4(at) # num of elements
      lw        v1, 8(at) # read it in (from the data param list)
      sw        v1, 0(v0) # save it out (to memory)
      subu      t0, 1     # dec count
      addu      v0, 4     # inc address
      bne       t0, zero, 0xff200224
      nop
      lw        v1, 268(at)
      lw        v0, 264(at)
      ori       at, at, 0x200
      jalr      zero, at
      mfc0      at, desave # restore at
    ''',
    names={
      0xff200000: 'address',
      0xff200004: 'count',
      0xff200008: 'data[]',
    },
    doc='''Write 32-bit values to memory.
    
    [c0v0] >>> dmseg(quiet, Write32(address=0x801660b0, count=4, data=[1, 2, 3, 4]))
    ''',
    assembled=dict(
        # [[[cog
        # scan._precog_list(cog, scan.Write32)
        # ]]]
        mips32=[
          (0xff200200, 0x00000000), # nop       
          (0xff200204, 0x00000000), # nop       
          (0xff200208, 0x4081f800), # mtc0      at, DESAVE
          (0xff20020c, 0x3c01ff20), # lui       at, 0xff20
          (0xff200210, 0xac220108), # sw        v0, 264(at)
          (0xff200214, 0xac23010c), # sw        v1, 268(at)
          (0xff200218, 0xac280110), # sw        t0, 272(at)
          (0xff20021c, 0x8c220000), # lw        v0, 0(at)
          (0xff200220, 0x8c280004), # lw        t0, 4(at)
          (0xff200224, 0x8c230008), # lw        v1, 8(at)
          (0xff200228, 0xac430000), # sw        v1, 0(v0)
          (0xff20022c, 0x2508ffff), # addiu     t0, t0, -1
          (0xff200230, 0x24420004), # addiu     v0, v0, 4
          (0xff200234, 0x1500fffb), # bnez      t0, 0xff200224
          (0xff200238, 0x00000000), # nop       
          (0xff20023c, 0x8c23010c), # lw        v1, 268(at)
          (0xff200240, 0x8c220108), # lw        v0, 264(at)
          (0xff200244, 0x34210200), # ori       at, at, 0x200
          (0xff200248, 0x00200009), # jalr      zero, at
          (0xff20024c, 0x4001f800), # mfc0      at, DESAVE
        ],
        micromips=[
          (0xff200200, 0x0c00    ), # nop       
          (0xff200202, 0x0c00    ), # nop       
          (0xff200204, 0x003f02fc), # mtc0      at, DESAVE
          (0xff200208, 0x41a1ff20), # lui       at, 0xff20
          (0xff20020c, 0xf8410108), # sw        v0, 264(at)
          (0xff200210, 0xf861010c), # sw        v1, 268(at)
          (0xff200214, 0xf9010110), # sw        t0, 272(at)
          (0xff200218, 0xfc410000), # lw        v0, 0(at)
          (0xff20021c, 0xfd010004), # lw        t0, 4(at)
          (0xff200220, 0xfc610008), # lw        v1, 8(at)
          (0xff200224, 0xe9a0    ), # sw        v1, 0(v0)
          (0xff200226, 0x3108ffff), # addiu     t0, t0, -1
          (0xff20022a, 0x30420004), # addiu     v0, v0, 4
          (0xff20022e, 0xb408fff9), # bnez      t0, 0xff200224
          (0xff200232, 0x0c00    ), # nop       
          (0xff200234, 0xfc61010c), # lw        v1, 268(at)
          (0xff200238, 0xfc410108), # lw        v0, 264(at)
          (0xff20023c, 0x50210200), # ori       at, at, 0x200
          (0xff200240, 0x00010f3c), # jr        at
          (0xff200244, 0x003f00fc), # mfc0      at, DESAVE
        ],
        mips32r6=mips32,
        mips64r6=[
          (0xff200200, 0x00000000), # nop       
          (0xff200204, 0x00000000), # nop       
          (0xff200208, 0x4081f800), # mtc0      at, DESAVE
          (0xff20020c, 0x3c01ff20), # lui       at,  0xff20
          (0xff200210, 0xac220108), # sw        v0, 264(at)
          (0xff200214, 0xac23010c), # sw        v1, 268(at)
          (0xff200218, 0xac280110), # sw        t0, 272(at)
          (0xff20021c, 0x8c220000), # lw        v0, 0(at)
          (0xff200220, 0x8c280004), # lw        t0, 4(at)
          (0xff200224, 0x8c230008), # lw        v1, 8(at)
          (0xff200228, 0xac430000), # sw        v1, 0(v0)
          (0xff20022c, 0x2508ffff), # addiu     t0, t0, -1
          (0xff200230, 0x24420004), # addiu     v0, v0, 4
          (0xff200234, 0x1500fffb), # bnez      t0, 0x00000000ff200224
          (0xff200238, 0x00000000), # nop       
          (0xff20023c, 0x8c23010c), # lw        v1, 268(at)
          (0xff200240, 0x8c220108), # lw        v0, 264(at)
          (0xff200244, 0x34210200), # ori       at, at, 0x200
          (0xff200248, 0x00200009), # jr        at
          (0xff20024c, 0x4001f800), # mfc0      at, DESAVE
        ],
        # [[[end]]]
    )
))

EnterDebug = builtin_list(DmsegList('EnterDebug',
    '''\
        nop       
        sync      
        b         0xff200200
        nop       
    ''',
    assembled=dict(
        # [[[cog
        # scan._precog_list(cog, scan.EnterDebug)
        # ]]]
        mips32=[
          (0xff200200, 0x00000000), # nop       
          (0xff200204, 0x0000000f), # sync      
          (0xff200208, 0x1000fffd), # b         0xff200200
          (0xff20020c, 0x00000000), # nop       
        ],
        micromips=[
          (0xff200200, 0x0c00    ), # nop       
          (0xff200202, 0x00006b7c), # sync      
          (0xff200206, 0x9400fffb), # b         0xff200200
          (0xff20020a, 0x0c00    ), # nop       
        ],
        mips32r6=mips32,
        mips64r6=[
          (0xff200200, 0x00000000), # nop       
          (0xff200204, 0x0000000f), # sync      
          (0xff200208, 0x1000fffd), # b         0x00000000ff200200
          (0xff20020c, 0x00000000), # nop       
        ],
        nanomips=[
          (0xff200200, 0x9008    ), # nop       
          (0xff200202, 0x8000c006), # sync      0x0
          (0xff200206, 0x28dffdf6), # bc        0x00000000
          (0xff20020a, 0x9008    ), # nop       
        ],
        # [[[end]]]
    )
))

ExitDebug = builtin_list(DmsegList('ExitDebug', 
    '''\
       deret     
       nop       
       nop       
       nop       
       deret     
       nop       
       nop       
       nop       
    ''',
    assembled=dict(
        # [[[cog
        # scan._precog_list(cog, scan.ExitDebug)
        # ]]]
        mips32=[
          (0xff200200, 0x4200001f), # deret     
          (0xff200204, 0x00000000), # nop       
          (0xff200208, 0x00000000), # nop       
          (0xff20020c, 0x00000000), # nop       
          (0xff200210, 0x4200001f), # deret     
          (0xff200214, 0x00000000), # nop       
          (0xff200218, 0x00000000), # nop       
          (0xff20021c, 0x00000000), # nop       
        ],
        micromips=[
          (0xff200200, 0x0000e37c), # deret     
          (0xff200204, 0x0c00    ), # nop       
          (0xff200206, 0x0c00    ), # nop       
          (0xff200208, 0x0c00    ), # nop       
          (0xff20020a, 0x0000e37c), # deret     
          (0xff20020e, 0x0c00    ), # nop       
          (0xff200210, 0x0c00    ), # nop       
          (0xff200212, 0x0c00    ), # nop       
        ],
        mips32r6=mips32,
        mips64r6=[
          (0xff200200, 0x4200001f), # deret     
          (0xff200204, 0x00000000), # nop       
          (0xff200208, 0x00000000), # nop       
          (0xff20020c, 0x00000000), # nop       
          (0xff200210, 0x4200001f), # deret     
          (0xff200214, 0x00000000), # nop       
          (0xff200218, 0x00000000), # nop       
          (0xff20021c, 0x00000000), # nop       
        ],
        nanomips=[
          (0xff200200, 0x2000e37f), # deret     
          (0xff200204, 0x9008    ), # nop       
          (0xff200206, 0x9008    ), # nop       
          (0xff200208, 0x9008    ), # nop       
          (0xff20020a, 0x2000e37f), # deret     
          (0xff20020e, 0x9008    ), # nop       
          (0xff200210, 0x9008    ), # nop       
          (0xff200212, 0x9008    ), # nop       
        ],
        # [[[end]]]
    )
))

#@command(device_required=False)
def dmseg_asm(assembly, start_address=results.IntResult(0xff200200), isa='mips32', name='<unnamed>', device=None):
    """Assemble source code ready to execute with :func:`dmseg`.
    
    #>>> lst = dmseg_asm('''
    ...     nop
    ...     nop
    ...     mfc0      at, Config
    ...     lui       v1, 0xff20
    ...     sw        at, 0(v1)
    ...     ori       v1, v1, 0x200
    ...     jalr      zero, v1
    ...     nop
    ... ''', names={0xff200000:'result'})
    #>>> dmseg(lst, quiet)['result']
    0x80248482
    
    If `start_address` is not specified then it defaults to the debug 
    exception vector 0xff200200.
    """
    lst = DmsegList(name, assembly, start_address=start_address)
    lst.code(isa)
    return lst
    
class BadAccessError(RuntimeError):
    pass
    
class DmsegResult(dict):
    def __repr__(self):
        if self:
            rows = [[results._display(x) for x in row] for row in sorted(self.items())]
            return rst.headerless_table(rows)
        return ''
        
class DmsegMemory(object):
    '''Represents writeable memory for use with the dmseg command.'''
    def __init__(self, names, data, code, isa='mips32'):
        self.names = names
        self.data = data
        self.code = code
        self.isa = isa
        self.results = DmsegResult()
        for address, name in sorted(names.items(), key=lambda x:x[1]):
            try:
                val = data[address]
            except KeyError:
                pass
            else:
                if name.endswith('[]') and not isinstance(val, list):
                    raise TypeError("Expected list for parameter %s" % (name,))
                elif not name.endswith('[]') and not isinstance(val, (int, long)):
                    raise TypeError("Expected int/long for parameter %s" % (name,))

    def _address(self, address):
        name = self.names.get(address, '')
        if name:
            name += '@'
        return '%s0x%08x' % (name, address)

    def store_value(self, address, value, verbose=False):
        '''A value has been received from the tapdata register'''
        name = self.names.get(address, '')
        extra = ''
        if name:
            if name.endswith('[]'):
                store = self.results.setdefault(name[:-2], results.IntListResult([]))
                store.append(value)
                extra = ', %d item%s in list' % (len(store), '' if len(store) == 1 else 's')
            else:
                self.results[name] = value
        else:
            store = self.results.setdefault(address, results.IntListResult([]))
            store.append(value)
        store = self.code if address in self.code else self.data
        store[address] = value
        if verbose:
            print "write to %s data: 0x%08x%s" % (self._address(address), value, extra)

    def fetch_value(self, address, verbose=False):
        '''A value has been requested for the tapdata register'''
        try:
            value = self.data[address]
            extra = ''
            name = self.names.get(address, '')
            if isinstance(value, list):
                try:
                    extra = ', %d item%s remaining' % (len(value) - 1, '' if len(value) == 2 else 's')
                    value = value.pop(0)
                except IndexError:
                    raise BadAccessError("read of address %s not possible because list is empty" % (self._address(address), ))
            if verbose:
                print "read of %s data: 0x%08x%s" % (self._address(address), value, extra)
            return value
        except KeyError:
            pass
        try:
            value = self.code[address]
            if verbose:
                try:
                    from imgtec.codescape.tiny import DisassembleBytes
                    dasm = DisassembleBytes(address, None, self.isa, 'o32', struct.pack('>I', value))
                    print "read of %s %-8s %s" % (self._address(address), dasm.opcode, repr(dasm.ops[0]).replace('c0_', ''))
                except ImportError:
                    print "read of %s %08x (no disassembler available)" % (self._address(address), value)                
            return value
        except KeyError:
            raise BadAccessError("read of address %s not in dmseglist" % (self._address(address), ))

class _JumpDEV(DmsegMemory):
    '''A special DmsegMemory that will issue alternate j 0xff200200 and nops
    irrespective of the address requested to get back to the DEV.'''
    def __init__(self):
        DmsegMemory.__init__(self, {}, {}, self)
    def __getitem__(self, address):
        return 0x0bc80080 if address & 4 else 0
        
JumpDEV = named('JumpDEV', _JumpDEV())

@command(verbose=verbosity)
def dmseg(entries, verbose=True, issue_ejtagboot=True, isa='mips32', names={}, data={}, device=None):
    """Satisfy dmseg requests from the given values.
    
    Using devtapi and devtapd dmseg is satisfied based on a supplied list of 
    memory locations and corresponding instruction/data values.
    
    The parameter can either be a predefined list, or assembler which will be 
    assembled using the gcc assembler.  See :func:`asm` for information on 
    configuring the assembler.
    
    Any named locations written to by the script will be displayed at the end 
    of the run using the supplied comment and will also be returned in a dictionary
    that allows results to be extracted easily.  Names are specified as an address:name
    dictionary in the `names` parameter. For example:
    
        >>> dmseg('''
        ...    mfc0      at, depc
        ...    lui       v1, 0xff20
        ...    sw        at, 0(v1)
        ...    ori       v1, v1, 0x200
        ...    jalr      zero, v1
        ...    nop''', quiet, names={0xff200000:'depc'})['depc'] # doctest: +SKIP
        0x87fe7e5c
    
    The run will continue until 10 reads of ECR result without a PrAcc request, 
    or the debug exception vector (0xff200200) is accessed for a second time, 
    or if a request is made for an address not in `entries`.  
    
    There are also a number of predefined scripts that can be used : EnterDebug,
    ExitDebug, ReadDEPC, and ReadConfigs, Read32, Write32, and ReadRegs.  Some of 
    the predefined lists take parameters:
    
        >>> dmseg(Read32(address=0x80000000, count=1), quiet) # doctest: +SKIP
        result [0x0000002a]
        >>> dmseg(Write32(address=0x80000000, count=2, data=[1, 2]), quiet) # doctest: +SKIP
        >>> dmseg(Read32(address=0x80000000, count=3), quiet) # doctest: +SKIP
        result [0x00000001, 0x00000002, 0x8f7b0000]
        
    If `issue_ejtagboot` is True (the default), an EJTAGBOOT is issued before 
    satisfying any requests so that any exceptions can be caught by re-entry 
    to debug mode.
    """
    _check_config(device, 'dmseg')
    
    if isinstance(entries, basestring):
        entries = DmsegList('<unnamed>', entries, names=names)
    if isinstance(entries, DmsegList):
        mem = entries(isa=isa, _params=data)  # 'compile' it
    elif isinstance(entries, DmsegMemory):
        mem = entries
    else:
        raise RuntimeError("Expected either a string containing assembly, a DmsegList or a DmsegMemory instance., got %r" % (entries,))
    
    type = tapreg('impcode', device=device).Type
    f = dmseg_dbu if type == JTAG_TYPE_DBU else _dmseg
    return f(mem, verbose, issue_ejtagboot, isa, device)
    
def _dmseg(mem, verbose, issue_ejtagboot, isa, device):
    trys = 10
    i = 0
    servicedDEV = False
    
    if issue_ejtagboot:
        tapboot(device=device)
    
    while i < trys:
        ecr = tapecr(device=device)
        if verbose == 2:
            print repr(ecr)
        if ecr.Rocc:
            if verbose == 1:
                print "Target reset detected (EJTAG Control: 0x%08x) continuing..." % (long(ecr),)
            tapecr(ecrAckResetM, device=device)
        elif ecr.PrAcc:
            if i > 1 and verbose:
                print "no access pending for %d read(s) of EJTAG Control register." % (i - 1,)
            addr = tapaddress(tapaddress(0, device=device), device=device)

            if servicedDEV and addr == 0xff200200:
                break       # Stop processing accesses on second access to 0xff200200.
            else:
                servicedDEV = True
                if ecr.PRnW:
                    value = tapdata(0, device=device)
                    mem.store_value(addr, value, verbose)
                else:
                    value = mem.fetch_value(addr, verbose)
                    tapdata(value, device=device)
                
                ecr = tapecr(ecrCompleteM, device=device)
                if ecr.Rocc:
                    if verbose:
                        if verbose == 2:
                            print repr(ecr)
                        print "Target reset detected continuing..."
                    tapecr(ecrAckResetM, device=device)
                else:
                    i = 0 # Access completed: reset the try counter.
        i += 1

    if verbose:
        if i >= trys:
            print "No processor access to dmseg seen in last %d reads of the EJTAG Control register <done>." % (trys,)
        else:
            print "Second access seen to debug exception vector <done>."
    return mem.results
    
ImgPnp = namedbitfield('ImgPnp', compile_fields('''\
    id          11 0
    version     15 12
    num_cores   23 16
    jtag_eregsi 25 24
    jtag_eregso 27 26
    reserved    31 28'''.splitlines()), show_vertical=True)
    
def make_img_pnp_bitfield(num_cores, version, ir_width):
    fields = ImgPnp._fields[:]
    def add_field(fields, name, fieldwidth, type=long):
        current = fields[-1].bit_start+1 if fields else 0
        fields.append(Field(name, fieldwidth-1 + current, current, type=type))
    add_field(fields, 'j_img_attn', ir_width)
    
    core_fields = []
    add_field(core_fields, 'core_img_id', 8, CoreImgId)
    add_field(core_fields, 'debug_rev', 4)
    add_field(core_fields, 'j_img', ir_width)
    add_field(core_fields, 'j_img_f', ir_width)
    add_field(core_fields, 'j_img_m', ir_width)    
    ImgPnpCore = namedbitfield('ImgPnpCore', core_fields, show_vertical=True)
    for n in range(num_cores):
        add_field(fields, 'core%d' % n, ImgPnpCore._size)
    if version > 1:
        add_field(fields,'j_img_status', ir_width)
    if version > 2:
        add_field(fields, 'j_img_control', ir_width)
    return (namedbitfield('ImgPnpData', fields, show_vertical=True), 
            namedbitfield('ImgPnpCore', core_fields, show_vertical=True))

def imgpnp_detect(device, pnp=None):
    tap_index = _check_config(device, 'imgpnp_detect')
    if pnp is None:
        #read jtag id
        pnp = ImgPnp(devtap(IR_IMG_JTAG_PNP, 32, 0x00000000, device=device))
        if pnp.id != IMG_JTAG_PNP_ID:
            raise RuntimeError("Tap %d does not have IMG Plug and Play, got id=0%03x expected id=0x%03x" % 
                                (tap_index, pnp.id, IMG_JTAG_PNP_ID))
    ir_width = device.probe.ir_lengths[tap_index]
    ImgPnpData, ImgPnpCore = make_img_pnp_bitfield(pnp.num_cores, pnp.version, ir_width)
    pnp = ImgPnpData(devtap(IR_IMG_JTAG_PNP, ImgPnpData._size, 0, device=device))
    cores = [ImgPnpCore(getattr(pnp, 'core%d' % n)) for n in range(pnp.num_cores)]
    return pnp, cores

def show_tap_info(tap_index, width, device):
    """check tap to see if meta or mips and print JTAG ID."""
    tap(tap_index, device=device)
    
    if not device.probe.tap_types:
        device.probe.tap_types = [None]*(tap_index+1)
    elif len(device.probe.tap_types) < tap_index:
        device.probe.tap_types.extend([None]*(tap_index-len(device.probe.tap_types)))

    #read jtag id
    jtag_id = devtap(IR_JTAG_ID,32,0x00000000, device=device)

    #is it a meta tap (look for JTAG PnP)
    pnp = ImgPnp(devtap(IR_IMG_JTAG_PNP, 32, 0x00000000, device=device))

    if pnp.id == IMG_JTAG_PNP_ID:
        print "TAP %d is a IMG META/UCC TAP with JTAG ID of 0x%08x, IMG PnP:" % (tap_index,jtag_id)
        rows = pnp._items()
        pnp, cores = imgpnp_detect(device, pnp=pnp)
        for code in ['j_img_attn', 'j_img_status', 'j_img_control']:
            try:
                rows.append((code, getattr(pnp, code)))
            except AttributeError:
                pass
        rows = [(x, '0x%x' % v) for x, v in rows]
        print rst.headerless_table(rows)
        rows = []
        for n, c in enumerate(cores):
            rows.append((str(n), str(c.core_img_id), '0x%x' % c.debug_rev, '0x%x' % c.j_img, '0x%x' % c.j_img_f, '0x%x' % c.j_img_m))
        print rst.simple_table(['Core #', 'Core IMG ID', 'debug_rev', 'j_img', 'j_img_f', 'j_img_f'], rows)
        return
        
    impcode = tapreg('impcode', device=device)
    # TODO what is this magic number?
    if (impcode & 0x0E9E9000) == 0 and impcode.EJTAGVer != 0:
        #impcode looks good.
        if impcode.MIPS64:
            print "Warning TAP looks like an unsupported MIPS64 TAP !!"

        #now try control register
        ecr = tapecr(device=device)

        if (ecr & 0x1F020FF7) == 0 : # TODO what is this magic number?
            #ECR look good can we read/write the data register ?
            data = tapdata(0x12345678, device=device)
            data = devtapd(32, 0x00000000, device=device)
            if data == 0x12345678 :
                print "TAP %d is a MIPS32 TAP with JTAG ID of 0x%08x" % (tap_index, jtag_id)
                if width != 5:
                    print "    Warning MIPS TAP discovered with IR Length != 5, (%d)" % width
                return
                
    if impcode.Type == 3:
        print "TAP %d is a DBU TAP with a JTAG ID of 0x%08x and IR width of %d" % (tap_index, jtag_id, width)
        device.probe.tap_types[tap_index] = JTAG_TYPE_DBU
        return

    if (impcode & 0x0E9E9000) == 0x1000 and impcode.EJTAGVer != 0:
        #impcode looks good.
        if impcode.MIPS64:
            print "Warning TAP looks like an unsupported MIPS64 TAP !!"

        #now try control register
        tcba = devtap(IR_MIPS_TCBCONTROLA, 32, 0x00001234, device=device)
        tcba = devtapd(32,0x00000000, device=device)

        if (tcba & 0xFFFF) == 0x1234 :
            print "TAP %d is a MIPS CM TAP with JTAG ID of 0x%08x" % (tap_index, jtag_id)
            if width != 5:
                print "    Warning MIPS TAP discovered with IR Length != 5, (%d)" % width
        else:
            print "TAP %d may be a MIPS CM TAP with no trace hardware so the test is limited and could be a false positive (JTAG ID 0x%08x)" % (tap_index,jtag_id)
        return
        
    if impcode.Type == 4:
        print "TAP %d is an MDH with a JTAG ID of 0x%08x and IR width of %d" % (tap_index, jtag_id, width)
        device.probe.tap_types[tap_index] = JTAG_TYPE_MDH
        return

    print "TAP %d is an unrecognised TAP with JTAG ID of 0x%08x and IR width of %d" % (tap_index, jtag_id, width)

def get_tap_index(td, device):
    wanted = device.tiny.SoCNumber(), device.tiny.CoreNumber(), device.tiny.VpeNumber()
    return _get_tap_index(td, *wanted)
    
def _get_num_vpes_from_mvpconf0(mvpconf0):
    '''
    
    >>> int(_get_num_vpes_from_mvpconf0(0xe8008401))
    2
    >>> int(_get_num_vpes_from_mvpconf0(0xe8008c01))
    4
    >>> int(_get_num_vpes_from_mvpconf0(0xffffffff))
    1
    >>> int(_get_num_vpes_from_mvpconf0(0xffffffff))
    1
    '''
    if mvpconf0 in (0, 0xffffffff): return 1
    return int(((mvpconf0 >> 10) & 0xf) + 1)
    
def _get_num_threads_from_core(core):
    '''
    
    >>> from imgtec.console.tdd import MipsCore, Core
    >>> _get_num_threads_from_core(MipsCore(mvp_conf0=0xffffffff))
    1
    >>> _get_num_threads_from_core(MipsCore(mvp_conf0=0))
    1
    >>> _get_num_threads_from_core(MipsCore(mvp_conf0=0xe8008c01))
    4
    >>> _get_num_threads_from_core(MipsCore(mvp_conf0=0xe8008401))
    2
    >>> _get_num_threads_from_core(Core())
    1
    '''
    return _get_num_vpes_from_mvpconf0(getattr(core, 'mvp_conf0', 0))
    
def _get_tap_index(td, wanted_soc, wanted_core, wanted_vpe):
    tap_index = sum(soc.taps_per_soc for soc in td.socs[:wanted_soc])
    soc = td.socs[wanted_soc]
    if soc.tap_type == TapType.mips_ejtag: #classic EJTAG
        tap_index += sum(_get_num_threads_from_core(core) for core in soc.cores[:wanted_core])
        tap_index += wanted_vpe
        return tap_index
    elif soc.tap_type in (TapType.IMG, TapType.mips_oci, TapType.mips_mdh, TapType.mips_cm):
        # One tap for all cores/threads
        return tap_index
    else:
        raise RuntimeError("Cannot deduce tap index for a tap of type %s." % soc.tap_type)

    raise RuntimeError("Failed to deduce tap index.")

def _decode_count_taps(result, test_pattern, max_taps=32, verbose=False):
    """Count the number of taps based on running `max_taps` bits through the DR register
    when all of the taps are in bypass.

    >>> _decode_count_taps(0x1235, 0x1235, 16)
    Traceback (most recent call last):
    ...
    RuntimeError: No taps founds via bypass test, received pattern 0x00001235 after sending 0x00001235
    This could be due to poor signal integrity, check JTAG signals with oscilloscope
    and look for ringing / non monotonic edges etc.
    >>> _decode_count_taps(0x1235 << 1, 0x1235, 16)
    1
    >>> _decode_count_taps(0x1235 << 2, 0x1235, 16)
    2
    >>> _decode_count_taps(0x2350, 0x1235, 16)
    4
    >>> _decode_count_taps(0x8000, 0x1235, 16)
    15
    >>> _decode_count_taps(0x0000, 0x1235, 16)
    Traceback (most recent call last):
    ...
    RuntimeError: More than 16 taps detected, this result may not be valid due to only
    shifting 16 bits and in any case the DA only supports 12 TAPs
    
    >>> _decode_count_taps(0x48d159e6, 0x12345679, 32)
    2
    
    """
    mask = (1 << max_taps) - 1
    if verbose > 1:
        print hex(result), hex(test_pattern), hex(mask)
    if (result & mask) == (test_pattern & mask):
        raise RuntimeError("No taps founds via bypass test, received pattern 0x%08x after sending 0x%08x\n"
                        "This could be due to poor signal integrity, check JTAG signals with oscilloscope\n"
                        "and look for ringing / non monotonic edges etc." % (result, test_pattern))
    for taps in range(1, max_taps):
        mask = (1 << (max_taps - taps)) - 1
        right = (result >> taps) & mask
        left = test_pattern & mask
        ok = left == right
        if verbose > 1:
            s = 's' if taps != 1 else ' '
            print "%-2d tap%s : test_pattern:0x%08x %s= got:0x%08x" % (taps, s, left, '!='[ok], right)
        if ok:
            return taps
    raise RuntimeError("More than %d taps detected, this result may not be valid due to only\n"
                     "shifting %d bits and in any case the DA only supports 12 TAPs" % (max_taps, max_taps))

def _count_taps(max_chain_length, probe, verbose=False):
    """Runs a Bypass Test and an IR Scan to determine the targets scan chain
    layout and test connectivity.
    """
    _prepare_for_bypass_test(probe, max_chain_length)
    # Scan through test pattern (on DR)
    test_pattern = 0x12345679
    scanned = word_to_bits(test_pattern, 32)
    res = probe.Scan(None, scanned)
    result = bits_to_word(res)
    if verbose > 1:
        print "DR Scanned in : %s(0x%08x)" % (scanned, test_pattern)
        print "          out : %s(0x%08x)" % (res, result)
    if result == 0:
        raise RuntimeError(dedent("""\
        The test has failed due to the return data from the bypass scan being all zero.

        There are a few potential reasons for this:

        * The JTAG connectivity is wrong and the TDO signal into the probe from the target is stuck at logic '0'
        * The target has more than 32 TAPs in a chain, this is unsupported by this test script
        * The target is powered off"""))

    if result == 0xFFFFFFFF:
        raise RuntimeError(dedent("""\
        The test has failed due to the return data from the bypass scan being all ones.

        There are a few potential reasons for this:

        * The JTAG connectivity is wrong and the TDO signal into the probe from the target is stuck at logic '1'
        * There is a problem with the TDO drive at the target or its unconnected and we are reading logic '1'
          from a pull-up resistor on the line
        * The target is powered off"""))
    return _decode_count_taps(result, test_pattern, max_taps=32, verbose=verbose)
    
def _decode_ir_bits(bits):
    """Decodes a post tap reset IR scan into a list of ir lengths.

    >>> _decode_ir_bits('11111111' '00000001')
    [8]
    >>> _decode_ir_bits('11111111' '00000011')
    [7]
    >>> _decode_ir_bits('11111111' '00000111')
    [6]
    >>> _decode_ir_bits('11111111' '00001111')
    []
    >>> _decode_ir_bits('11111111' '00000101')
    [6, 2]
    >>> _decode_ir_bits('11111111' '00001101')
    [5, 2]
    >>> _decode_ir_bits('11111111' '00011101')
    [4, 2]
    >>> _decode_ir_bits('11111111' '00111101')
    [2]
    >>> _decode_ir_bits('11100000001' '00000101')
    [8, 6, 2]
    >>> _decode_ir_bits('11111111' '11111111' '00000001' '00000001')
    [8, 8]
    >>> _decode_ir_bits('11111' '000001' '00001' '0001')
    [6, 5, 4]
    >>> _decode_ir_bits('11111111' '11111111' '00001' '00001' '000001' '00001' '00001' '00001' '00001' '00001' '00001')
    [5, 5, 6, 5, 5, 5, 5, 5, 5]
    """
    # The data has been primed with a tap reset to load a 1 into each IR, which will appear as 0...01
    # throw away everything after the last sequence of 4 1's
    _beforeones, _ones, bits = bits.rpartition('1111')
    # Now find each '0'*n '1' pattern, the length of that IR is the length of the pattern
    return [len(pattern) for pattern in re.findall('0+1', bits)]

@command(verbose=verbosity)
def jtagchain(max_chain_length=128, verbose=True, perform_bypass_test=False, device=None):
    """Determines the JTAG chain topology by performing a TAP reset and IR Scan.
 
    The JTAG chain is an ordered list of IR lengths of each node on the JTAG 
    chain. It starts with the node closest to TDO.
    
    Use this command to detect the number of taps and the length of each tap
    on the chain, after use of this command you can select the active tap
    using :func:`tap` ::
    
        >>> jtagchain()
        [5, 5]
        >>> tap(1)
        >>> pcsamp()
        0x17f800001
        PC       New
        bfc00000 1
    
    `max_chain_length` determines the total number of bits to scan through 
    the TDO, it defaults to 128. Note that the DA does not support more than
    255 bits.  Some taps have bugs which can be worked around by setting a 
    smaller value of max_chain_length.

    If this is the case or you have a target that has a maximum IR chain
    length you can set max_chain_length for the duration of the session.

        >>> jtagchain.max_chain_length = 56
        >>> jtagchain()
        [5, 5]
        
    If `perform_bypass_test` is given then an additional test is run to determine
    the number of taps by setting all TAPS into bypass and scanning through a 
    test pattern.  This is not 100% reliable so it is off by default.
    
        >>> jtagchain(perform_bypass_test=True)
        Bypass test found 2 taps
        [5, 5]
    
    """
    
    if perform_bypass_test:
        num_taps = _count_taps(max_chain_length, device.da, verbose)
        if verbose:
            print 'Bypass test found %d tap%s' % (num_taps, 's' if num_taps != 1 else '')
    #reset tap to place 0x1 into IR regs
    device.da.TapReset()    # shift 1's through the IR path
    bits = device.da.Scan('1' * max_chain_length, None)
    if verbose > 1:
        print "IR Scanned in: " + '1' * max_chain_length
        print "          out: " + bits
    ir_lengths = _decode_ir_bits(bits)
    if verbose > 1:
        print "IR Lengths   : " + repr(ir_lengths)
    if perform_bypass_test and num_taps != len(ir_lengths):
        print dedent("""\
            Warning: Number of taps discovered by IR Scan (%d) does not match number from
                     DR Bypass Scan (%d).  This is probably a bug in the tap, please try 
                     passing a smaller max_chain_length parameter.""") % (len(ir_lengths), num_taps)
    device.probe.ir_lengths = ir_lengths
    device.probe.tap_index = -1
    return ir_lengths

@command()
def tapinfo(device=None):
    """Examines the taps on the jtag chain and prints info about them.
    
    This command, when used in conjunction with :func:`tcktest` and :func:`jtagchain`
    forms a good starting point for a basic JTAG bring up test.
    
        >>> tcktest()
        Running bypass test at 156 KHz (slowest JTAG clock setting) to check connectivity and to count the number of taps...
        Performing Speed test to determine max TCK
        Running Speed Test at 20 MHz TCK PASSED

        >>> jtagchain()
        Bypass test found 2 taps
        Determine IR lengths on scan chain and validating number of taps...
        [5, 5]
        
        >>> tapinfo()
        TAP 0 is a MIPS32 TAP with JTAG ID of 0x00000001
        TAP 1 is a MIPS32 TAP with JTAG ID of 0x00001001
    
    """
    _check_config(device, 'tapinfo')
    old_tap_index = device.probe.tap_index
    try:
        for tap_index, width in enumerate(device.probe.ir_lengths):
            show_tap_info(tap_index, width, device=device)
    finally:
        tap(old_tap_index)

'''
@command()
def scandevices(device=None):
    """Create devices which provide higher level debugging access to devices.

    Note that this emulates the probes higher level functions in python
    and may not be as robust or as feature complete as the probe.
    
    [uncommitted] >>> scanonly()
    Bypass test found 1 tap
    Determine IR lengths on scan chain and validating number of taps...
    [tap 0 of 1] >>> scandevices()
    Core 0
      scan_c0v0 - HTP-213-2-Thread0
      scan_c0v1 - HTP-213-2-Thread1
    scan_c1v0 - MTX-122-0
    scan_c2v0 - mcp
    scan_c3v0 - MTX-122-0
    scan_c4v0 - mcp
    [scan_c0v0] >>> word(0x04800000)
    0x02010032
    [scan_c0v0] >>> word(0x04800000, scan_c1v0)
    0x01029822
    [scan_c0v0] >>> device(scan_c1v0)
    scan_c1v0 - MTX-122-0
    [scan_c1v0] >>> cpuinfo()
    core_id 0x00000000
    is_mtx  True
    version 122-0

    """
    from imgtec.console.scan_meta import connect_tap
    from imgtec.console.generic_device import listdevices
    tap_index = _check_config(device, "scan_devices")
    if device.probe.mode != 'scanonly':
        raise RuntimeError("scan_devices can only be used when in scanonly mode, use the scanonly() command")
    pnp, cores = imgpnp_detect(device=device)
    behind_meta_tap = connect_tap(device, tap_index, pnp, cores)
    device.probe._add_socs(behind_meta_tap, 'scan_')
    return listdevices(device=device)
'''


def _prepare_for_bypass_test(probe, max_scan_length):
    """Shift lots of ones through the IR register(s) to get them all in bypass
    This will not work if the sum of all the IR lengths in the JTAG chain exceeds 128 bits
    Prime the bypass registers with 0, this will not work for more than 64 TAPs (DA only support up to 12 TAPs in a chain anyway).
    """
    ir_len = min(8*16, max_scan_length)
    dr_len = min(8*8, max_scan_length)
    probe.Scan('1' * ir_len, '0' * dr_len)

def _bypass_test(probe, num_taps):
    """Performs a bypass test send the pattern 0x12345678 and checking the return
    value, compensating for the bypass registers in the chain.
    """
    test_value = 0x12345678
    test_length = 32
    test_pattern = '0' * num_taps + word_to_bits(test_value, test_length)
    out = probe.Scan(None, test_pattern)
    got, _res2 = bits_to_words(out, [test_length, num_taps])
    if got != test_value:
        raise ValueError("FAILED: expected 0x%08x but got 0x%08x" % (test_value, got))

def _speed_test(device, max_scan_length, verbose=True):
    """Performs bypass tests at different frequencies to determine the max TCK 
    the target can support.
    """
    jtag_speeds = da_jtag_speeds
    if device.probe.identifier.startswith('SysProbe'):
        jtag_speeds = sp_jtag_speeds
        
    original = device.tiny.GetJTAGClock()
    slowest = jtag_speeds[-1]
    if verbose:
        print "Running bypass test at %s (slowest JTAG clock setting) to check connectivity and to count the number of taps..." % (repr(slowest),)
    device.tiny.SetJTAGClock(hz_to_khz(slowest))
    _prepare_for_bypass_test(device.da, max_scan_length)
    num_taps = _count_taps(max_scan_length, device.da, verbose)
    if verbose:
        print "Performing Speed test to determine max TCK"
    for speed in jtag_speeds:
        if verbose:
            print "Running Speed Test at %s TCK" % (repr(speed),),
        try:
            device.tiny.SetJTAGClock(hz_to_khz(speed))
            _prepare_for_bypass_test(device.da, max_scan_length)
            for _ in range(TEST_LOOPS):
                _bypass_test(device.da, num_taps)
            if  verbose:
                print "PASSED"
            return speed
        except Exception as e:
            if verbose:
                print str(e)
    device.tiny.SetJTAGClock(original)
    raise ValueError("No JTAG Speed found which passed the bypass test")

@command(verbose=verbosity)
def tcktest(verbose=True, max_scan_length=128, device=None):
    """Set the TCK rate to the the maximum rate supported by the target.
    
    Test the target to find out what the maximum TCK rate can be and set 
    tckrate to that value. Running the target at the highest possible TCK 
    rate will improve performance. This can be quite noticeable when downloading
    large programs.
    
    The test is run from the high TCK rate to the low TCK rate.  The possible
    values range from 20MHz (high-tck-rate) to 156KHz (low-tck-rate) if they 
    are not specified in the command parameters. The highest found within that 
    range will be set if there is no second highest.
    """
    _speed_test(device, max_scan_length, verbose)
    return tckrate(device=device)
    
def _speed_test_mdh(device, verbose=True):
    jtag_speeds = da_jtag_speeds
    if device.probe.identifier.startswith('SysProbe'):
        jtag_speeds = sp_jtag_speeds
        
    slowest = jtag_speeds[-1]
    if verbose:
        print "Running MDH test at %s (slowest JTAG clock setting) to check connectivity..." % (repr(slowest),)
    
    device.tiny.SetJTAGClock(hz_to_khz(slowest))
    mdh_transaction(device.probe, IR_MIPS_IMPCODE, value=None)
    if verbose:
        print "Performing Speed test to determine max TCK"
    for speed in jtag_speeds:
        if verbose:
            print "Running Speed Test at %s TCK" % (repr(speed),),
        try:
            device.tiny.SetJTAGClock(hz_to_khz(speed))
            for _ in range(TEST_LOOPS):
                mdh_transaction(device.probe, IR_MIPS_IMPCODE, value=None)
            if verbose:
                print "PASSED"
            return speed
        except Exception as e:
            if verbose:
                print str(e)
    raise ValueError("No JTAG Speed found which passed the MDH test")
    
@command(verbose=verbosity)
def tcktestmdh(device=None):
    """
    Set the TCK rate to the the maximum rate supported by this MDH target.
    In other words, the highest rate at which valid=0 is not returned.
    """
    _speed_test_mdh(device)
    return tckrate(device=device)

def ack_reset(timeout, device):
    """Acknowledge the Rocc bit in the ECR register """
    target_time = time.time() + timeout
    while time.time() < target_time:
        ctrl = tapecr(device=device)
        if ctrl.Rocc:
            tapecr(ecrAckResetM, device=device)
        else:
            return True
    return False

@command(verbose=verbosity)
def enterdebug(timeout=0.5, global_throttle=False, verbose=True, device=None):
    """Attempts to get the core/vpe connected to the current tap into debug mode.
    
    This is done by setting ECR.EjtagBrk, whilst acknowledging any reset occurred
    and checking for any pending write access to dmseg.
    
    Once ECR.EjtagBrk has been set, the EnterDebug dmseg is serviced ::
    
        >>> jtagchain()
        Bypass test found 1 tap
        Determine IR lengths on scan chain and validating number of taps...
        [5]
        >>> tap(0)
        >>> enter_debug()
        read of 0xff200204 0000000f    sync
        read of 0xff200208 1000fffd    b         0xff200200
        read of 0xff20020c 00000000    nop
        Second access seen to debug exception vector <done>.
        
    To change the current tap use :func:`tap`.
    
    `timeout` is the number of seconds to wait for the target to request 
    a dmseg access.  It is extended by 2 seconds every time a reset is 
    detected.
    """
    
    type = tapreg('impcode', device=device).Type
    
    if type == JTAG_TYPE_DBU:
        #DBU
        return enter_debug_dbu(global_throttle, verbose, device)
    else:
        #classic
        return _enter_debug(timeout, verbose, device)
    
def _enter_debug(timeout, verbose, device):
    target_time = time.time() + timeout
    while time.time() < target_time:
        ctrl = tapecr(device=device)
        if ctrl.Rocc:
            if verbose:
                print "Pending Reset or Reset Occurred clearing Rocc"
            if ack_reset(ACK_RESET_TIMEOUT, device):
                # restart the timer after a reset
                target_time = time.time() + timeout
            else:
                raise RuntimeError("Timeout waiting to acknowledge Rocc (device may be stuck in reset)")

        if ctrl.Dm and ctrl.PrAcc:
            if ctrl.PRnW:
                raise RuntimeError("Write access pending on entry to debug mode")
            else:
                return dmseg(EnterDebug, device=device, issue_ejtagboot=False, verbose=verbose)
        else:
            tapecr(ecrBreakM, device=device)
    if ctrl.VPED :
        raise RuntimeError("VPE Disabled (No TC's Bound to it) when trying to enter debug mode")
    raise RuntimeError("Timeout waiting to enter debug mode, ECR: %r" % (ctrl,))

(configure_tap, enter_debug, tap_info, tap_ecr, tap_data, tap_address, tap_reg, tap_boot) = \
  (tap, enterdebug, tapinfo, tapecr, tapdata, tapaddress, tapreg, tapboot)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
