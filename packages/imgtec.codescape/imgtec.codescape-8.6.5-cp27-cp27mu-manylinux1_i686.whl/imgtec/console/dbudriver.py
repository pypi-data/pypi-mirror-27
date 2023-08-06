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
import array, re, time
from imgtec.console.dbu_monitor import *
from imgtec.console.generic_device import make_device_list
from imgtec.console.memory import dasm
from imgtec.console.program_file import get_symbols_string
from imgtec.console import reginfo
from imgtec.console.socket_sim_driver import SocketDriver
from imgtec.console.support import *
from imgtec.lib.namedbitfield import namedbitfield
from imgtec.lib.namedenum import namedenum
from imgtec.console.breakpoints import TinyBreakpointType
from imgtec.console import tdd

def get_register_index(abi, name):
    '''Lookup the index of a register
    
    Single item tuple for r0-31, two items otherwise:
    
    >>> get_register_index('o32', 't0')
    (8,)
    >>> get_register_index('n32', 't0')
    (12,)
    >>> get_register_index('n64', 't0')
    (12,)
    >>> get_register_index('n64', 'Config')
    (16, 0)
    >>> get_register_index('numeric', 'Config')
    (16, 0)
    >>> get_register_index('numeric', 'Config1')
    (16, 1)
    >>> get_register_index('numeric', 'cp0.1.2')
    (1, 2)
    >>> get_register_index('numeric', 'wubble')
    Traceback (most recent call last):
    ...
    DBUError: Register 'wubble' not found.
    >>> get_register_index('x86', 'wubble')
    Traceback (most recent call last):
    ...
    DBUError: No register information for ABI 'x86'.

    '''
    name = name.lower()
    try:
        regs = reginfo.info(abi)
    except KeyError:
        raise DBUError("No register information for ABI '%s'." % abi)
    
    for n, reg in enumerate(regs[:32]):
        if reg.name.lower() == name:
            return (n,)

    info = reginfo.info_by_name(abi).get(name)
    if info:
        names = [info.name] + info.aliases
        for name in names:
            cpnums = re.match(r'cp0\.(\d+)\.(\d+)', name)
            if cpnums:
                index, sel = int(cpnums.group(1)), int(cpnums.group(2))
                return index, sel
        raise DBUError("Register '%s' not found." % repr(info))                
    raise DBUError("Register '%s' not found." % name)


try:
    from imgtec.lib.bits import word_to_bits
except ImportError:
    from imgtec.codescape.tiny import word_to_bits
        
control_dxerr = [
    'no error',
    'DMX access outside memory range',
    'Reset occurred in one or more cores.  Query CPC to determine which one(s)',
    'Both reset and DMX access range errors occurred.']
    
control_rberr = [
    'no error',
    'Endpoint Unavailable Error (EUE)',
    'Destination Not Found Error (DNFE)',
    'Bus Parity Error (BPE)']

class DbuDriverException(Exception):
    pass

class DBUError(Exception):
    pass
    
class DmxsegError(DBUError):
    pass
        
DXAddrOperation = namedtuple('LastDXAddr', 'addr size operation')
Timeouts = namedtuple('timeouts', 'dmxseg_read dmxseg_write rb_valid')

RB_ID_GIC = 24    
RB_ID_CPC = 33
RB_ID_GCR = 34

OFFSET_GCR_CONFIG           = 0x0000
OFFSET_GCR_CL_CONFIG        = 0x2010
OFFSET_GCR_GIC_STATUS       = 0x00D0
OFFSET_GCR_BEV_BASE         = 0x0680
OFFSET_CPC_ROCC_CTL_REG     = 0x0040
OFFSET_CPC_CL_CMD_REG       = 0x2000
OFFSET_CPC_CL_STAT_CONF_REG = 0x2008
OFFSET_CPC_CL_VC_RUN        = 0x2028
OFFSET_CPC_CL_VC_SUSPEND    = 0x2030 
OFFSET_GIC_SH_DEBUGM_STATUS = 0x60A0
OFFSET_GIC_SH_EJTAG_BRK     = 0x6010
OFFSET_GIC_SH_DBG_CONFIG    = 0x6080
OFFSET_GIC_SH_DINT_PART     = 0x6090
DRSEG_OFFSET_VC_CONTROL1    = 0x0000
DRSEG_OFFSET_VC_CONTROL2    = 0x0008

CPC_CL_CMD_CLOCK_OFF = 1
CPC_CL_CMD_PWR_DOWN  = 2
CPC_CL_CMD_PWR_UP    = 3
CPC_CL_CMD_RESET     = 4
    
SlaveAddr = namedbitfield('SlaveAddr', 
    [('dest_id', 17, 12), ('core_id', 11, 6), ('vpe_id', 3, 0)])
    
ClusterAddr = namedbitfield('ClusterAddr', 
    [('cluster_id', 15, 10), ('gst_id', 7, 0)])

RBAddr = namedbitfield('RBAddr',
    [('sz', 23), ('inc', 22, 21), ('wr', 20), ('addr', 19, 2),
     ('err', 1), ('valid', 0),
    ])
    
RBData = namedbitfield('RBData',
    [('data', 65, 2), ('err', 1), ('valid', 0)])

VPEBoot = namedbitfield('VPEBoot', 
    [('vpec5', 23, 20), ('vpce4', 19, 16), ('vpce3', 15, 12),
     ('vpce2', 11, 8), ('vpce1', 7, 4), ('vpce0', 3, 0)])
     
Control = namedbitfield('Control', 
    [('gt', 0), ('pracc', 1), ('rrb_reset', 2), 
     ('dxerr', 5, 4), ('rberr', 7, 6), ('rb_buserr_occured', 8),
     ('dx_Size', 14, 12), ('dx_fdcsize', 18, 16)
    ])
        
DXAddr = namedbitfield('DXAddr',
    [('sz', 23), ('inc', 22, 21), ('wr', 20), ('addr', 19, 2),
     ('err', 1), ('valid', 0),
    ])
    
DXData = namedbitfield('DXData',
    [('data', 65, 2), ('err', 1), ('valid', 0)])
                            
RBHeader = namedbitfield('RBHeader', 
    [('mcmd', 63, 62), ('dest_id', 61, 56), ('core_id', 55, 50), 
     ('vpe_id', 49, 46), ('gst_id', 45, 38),
     ('addr', 37, 18), ('wordenable', 17, 16), 
    ])

RBPayload = namedbitfield('RBPayload', 
    [('data', 63, 0)])
    
FDC = namedbitfield('FDC', 
    [('valid', 37), ('accept', 36), ('channel', 35, 32), ('data', 31, 0)])
    
VCControl1 = namedbitfield('VCControl1', 
    [('local_throttle', 0)])

VCControl2 = namedbitfield('VCControl2', 
    [('probtrap', 0), ('dmxsegen', 1), ('bootmode', 2), ('nmie', 3),
     ('inte', 4), ('rdvec', 5)])
     
GCRConfig = namedbitfield('gcr_config',
    [('numiocu', 11, 8), ('pcores', 7, 0)])
    
GCRCLConfig = namedbitfield('gcr_cl_config',
    [('iocu_type', 11, 10), ('pvpe', 9, 0)])
    
CPCROCCCTRLReg = namedbitfield('rocc_ctl_reg',
    [('cpc_rocc', 31), ('reset_cause', 30, 29), ('dbu_rocc', 17), ('cm_rocc', 16), 
     ('core5_rocc', 5), ('core4_rocc', 4), ('core3_rocc', 3), ('core2_rocc', 2), 
     ('core1_rocc', 1), ('core0_rocc', 0)])
     
CPCCLStatConfReg = namedbitfield('cpc_cl_stat_conf_reg',
    [('pwrup_event', 23), ('seq_state', 22, 19), ('clkgat_impl', 17),
     ('pwrdn_impl', 16), ('ejtag_probe', 15), ('pwrup_policy', 9, 8),
     ('io_trffc_en', 4), ('cmd', 3, 0)])
     
CPCCLCmdReg = namedbitfield('cpc_cl_cmd_reg',
    [('cmd', 3, 0)])
     
GCRGicStatus = namedbitfield('gcr_gic_status', 
    [('gic_ex', 0)])
    
CPCRevisionReg = namedbitfield('cpc_revision_reg',
    [('major_rev', 15, 8), ('minor_rev', 7, 0)])
    
GCRL2Config = namedbitfield('gcr_l2_config',
    [('reg_exists', 31), ('cop_lru_we', 26), ('cop_tag_ecc_we', 25), ('cop_data_ecc_we', 24),
    ('l2_bypass', 20), ('set_size', 15, 12), ('line_size', 11, 8), ('assoc', 7, 0)])
    
VPRunning = namedbitfield('vp_running',
    [('vc3', 3), ('vc2', 2), ('vc1', 1), ('vc0', 0)])
    
TeamIDLo = namedbitfield('teamid_lo',
    [('id_vc15', 62, 60), ('id_vc14', 58, 56), ('id_vc13', 54, 52), ('id_vc12', 50, 48),
     ('id_vc11', 46, 44), ('id_vc10', 42, 40), ('id_vc9' , 38, 36), ('id_vc8' , 34, 32),
     ('id_vc7' , 30, 28), ('id_vc6' , 26, 24), ('id_vc5' , 22, 20), ('id_vc4' , 18, 16),
     ('id_vc3' , 14, 12), ('id_vc2' , 10, 8),  ('id_vc1' ,  6, 4),  ('id_vc0' ,  2, 0)])
     
TeamIDHi = namedbitfield('teamid_hi',
    [('team_id_vc23', 30, 28), ('team_id_vc22', 26, 24), ('team_id_vc21', 22, 20),
     ('team_id_vc20', 18, 16), ('team_id_vc19', 14, 12), ('team_id_vc18', 10, 8),
     ('team_id_vc17',  6, 4), ('team_id_vc16',  2, 0)])
     
GICSHDbgConfig = namedbitfield('gic_sh_dbg_config',
    [('num_teams', 7, 4), ('sync_go_dis', 0)])
    
TeamIDExt = namedbitfield('teamid_ext',
    [('team_id_ext', 2, 0)])
    
class RBError(Exception):
    pass
    
class RBAccessor(object):
    def __init__(self, tap, should_read_control=True):
        self.tap = tap
        self.rb_valid_timeout = 2
        #False when this class isn't within the DBU python wrapper (which knows what global throttle should be)
        self.should_read_control = should_read_control
        
    def read(self, destId, coreId, vpeId, offset, is64bit, clusterId=0, gstId=0):
        self.tap.clusteraddr(ClusterAddr(cluster_id=clusterId, gst_id=gstId))
        self.tap.slaveaddr(SlaveAddr(dest_id=destId, core_id=coreId, vpe_id=vpeId))
        scanin = RBAddr(sz=is64bit, addr=(offset >> 2), valid=1)
        scanout = self.scanRbAddrUntilValid(scanin, check_err=False)
        scanout = self.scanRbDataUntilValid(0)
        return scanout

    def write(self, destId, coreId, vpeId, offset, is64bit, value, clusterId=0, gstId=0):
        self.tap.clusteraddr(ClusterAddr(cluster_id=clusterId, gst_id=gstId))
        self.tap.slaveaddr(SlaveAddr(dest_id=destId, core_id=coreId, vpe_id=vpeId))
        self.tap.rbaddr(RBAddr(sz=is64bit, wr=1, addr=(offset >> 2)))
        scanout = self.scanRbDataUntilValid(RBData(data=value, valid=1), check_err=False)
        # We've handed off the request, now wait for response
        scanout = self.scanRbAddrUntilValid(0)
        return scanout
        
    def doScanRbUntilValid(self, isDataScan, scanin, check_err):
        start = time.time()
        while (time.time() - start) < self.rb_valid_timeout:
            if isDataScan:
                scanout = self.tap.rbdata(scanin)                        
            else:
                scanout = self.tap.rbaddr(scanin)
            if scanout & 0x1 != 0:
                break
        else:
            raise DbuDriverException("RB scan out was not valid within re-try limit")
        
        if ((scanout & 0x2) != 0) and check_err:
            #Read control to find out what kind of error it was
            if self.should_read_control:
                val = Control(self.tap.readDbuControl())
                rberr = val.rberr
                dxerr = val.dxerr
                raise DbuDriverException(
                    "RB completed with an error indicated - RBERR=%s (%d), DXERR=%s (%d)" % (
                    control_rberr[rberr], rberr, control_dxerr[dxerr], dxerr))
            else:
                raise DbuDriverException("RB completed with an error indicated")
                
        return scanout >> 2

    def scanRbAddrUntilValid(self, scanin, check_err=True):
        return self.doScanRbUntilValid(False, scanin, check_err)

    def scanRbDataUntilValid(self, scanin, check_err=True):
        return self.doScanRbUntilValid(True, scanin, check_err)
        
class DMXSEGAccessor(object):
    def __init__(self, tap, should_read_control=True):
        self.tap = tap
        self.dmxsegwrite_timeout = 5
        self.dmxsegread_timeout  = 5
        self.should_read_control = should_read_control
        
        #This allow us to not re-write DXAddr when the same kind of access is
        #done sequentially.
        self.last_dxaddr = DXAddrOperation(None, None, None)
        
    def read(self, addr, size):
        #Convert value and size where needed
        
        #32 bit unchanged
        if size == 32:
            return self._dmxsegread(addr, 0)
        elif size == 64:
            if addr & 0x4:
                #Split into 2 32 bit reads
                lsw = self._dmxsegread(addr, 0)
                msw = self._dmxsegread(addr+4, 0)
                return lsw | (msw << 32)
            else:
                #Single 64 bit read
                return self._dmxsegread(addr, 1)
        elif size == 128:
            #2 64 bit reads, recursion handles splits
            lsw = self.read(addr, 64)
            msw = self.read(addr+8, 64)
            return lsw | (msw << 64)
        else:
            raise DbuDriverException("Unknown DMXSEG read size %d" % size)
        
    def _dmxsegread(self, addr, sz):
        #Actual tap transactions to do the read
        
        addr = addr & 0xFFFFF

        if DXAddrOperation(addr, sz, 0) != self.last_dxaddr:
            # Valid is 0 to not trigger it, always increment
            dxaddr_val = DXAddr(sz=sz, wr=0, addr=(addr>>2), valid=0, inc=1)
            self.tap.dxaddr(dxaddr_val)
        else:
            addr = self.last_dxaddr.addr
        
        #Invalidate the saved params in case the read fails
        self.last_dxaddr = DXAddrOperation(None, None, None)
        
        #Writing valid as 1 triggers the read
        self.tap.dxdata(1)
        
        #Wait for valid to return to 1
        data = DXData(0)
        start = time.time()
        while (time.time() - start) < self.dmxsegread_timeout:
            if data.valid:
                break
            data = DXData(self.tap.dxdata(0))
        else:
            raise DmxsegError('DMXSEG read of 0x%x did not finish in time' % addr)
            
        if data.err:
            if self.should_read_control:
                control = Control(self.tap.readDbuControl())
                err_msg = 'DMXSEG read of 0x%x completed with an error (%s)' % (addr, control_dxerr[control.dxerr])
                
                if control.dxerr == 2:
                    #Bit of a hack but this code won't be hit unless the tap is a DBUDevice anyway.
                    rocc = self.tap.read_rocc_mask()
                    self.tap.clear_rocc_mask()
                    err_msg  += " (ROCC_CTL: 0x%0x)" % rocc
                    
                raise DmxsegError(err_msg)
            else:
                raise DmxsegError('DMXSEG read of 0x%x completed with an error'
                        % addr)

        #DXAddr now contains incremented address
        self.last_dxaddr = DXAddrOperation(addr + (4 if sz == 0 else 8), sz, 0)
        
        res = data.data
        
        if sz == 1: #64 bit read
            return res
        elif sz == 0:
            if addr & 0x4:
                #Data transferred in upper word
                return (res & (MASK_32_BIT<<32)) >> 32
            else:
                #Data in lower word
                return res & MASK_32_BIT
                
    def write(self, addr, value, size, verify=False):
        #Convert values and size where needed
        
        if size == 32:
            #No change to 32 bit writes
            self._dmxsegwrite(addr, value, 0, verify)
        elif size == 64:
            #If address is misaligned we need to split it into 2 32 bit writes
            if addr & 0x4:
                #LSW
                self._dmxsegwrite(addr, value & MASK_32_BIT, 0, verify)
                #MSW
                self._dmxsegwrite(addr+4, (value>>32) & MASK_32_BIT, 0, verify)
            else:
                #Otherwise write normally
                self._dmxsegwrite(addr, value, 1, verify)
        elif size == 128:
            #Call this function again 2 64 bit values
            self.write(addr, value & MASK_64_BIT, 64, verify)
            self.write(addr+8, (value >> 64) & MASK_64_BIT, 64, verify)
        else:
            raise DbuDriverException("Unknown DMXSEG write size %d" % size)
                
    def _dmxsegwrite(self, addr, value, sz, verify=False):
        #Actual tap transactions to do the write
        
        original_value = value
        
        if sz == 0: # 32 bit write
            if addr & 0x4:
                #Value must be in upper word
                value = value << 32
        
        addr = (addr & 0xFFFFF)
        
        if DXAddrOperation(addr, sz, 1) != self.last_dxaddr:
            dxaddr_val = DXAddr(sz=sz, wr=1, addr=(addr>>2), valid=0, inc=1)
            self.tap.dxaddr(dxaddr_val)
        else:
            addr = self.last_dxaddr.addr
            
        #Invalidate the saved params in case the read fails
        self.last_dxaddr = DXAddrOperation(None, None, None)
        
        #Set DXData to trigger write
        dxdata_value = DXData(data=value, valid=1)
        self.tap.dxdata(dxdata_value)
        #Don't trigger more writes
        dxdata_value = dxdata_value._replace(valid=0)
        
        #Wait for completion
        data = DXData(0)
        start = time.time()
        while (time.time() - start) < self.dmxsegwrite_timeout:
            if data.valid:
                break
            data = DXData(self.tap.dxdata(dxdata_value))
        else:
            raise DmxsegError('DMXSEG write of 0x%x to 0x%x did not finish in time'
                    % (value, addr))
                    
        #Check for error
        dxdata_value = DXData(self.tap.dxdata(0))
        if dxdata_value.err:
            if self.should_read_control:
                control = Control(self.tap.readDbuControl())
                err_msg = 'DMXSEG write of 0x%x to 0x%x completed with an error (%s)' % (value, addr, control_dxerr[control.dxerr])
                
                if control.dxerr == 2:
                    #Bit of a hack but this code won't be hit unless the tap is a DBUDevice anyway.
                    rocc = self.tap.read_rocc_mask()
                    self.tap.clear_rocc_mask()
                    err_msg  += " (ROCC_CTL: 0x%0x)" % rocc
                    
                raise DmxsegError(err_msg)
            else:
                raise DmxsegError('DMXSEG write of 0x%x to 0x%x completed with an error'
                    % (value, addr))
                
        #DXAddr now contains incremented address
        self.last_dxaddr = DXAddrOperation(addr + (4 if sz == 0 else 8), sz, 1)
        
        #Read it back to verify
        if verify:
            #Size is 0, 1 and we need to give the higher level dmxseg read 32, 64
            data = self.read(addr, (sz+1)*32)
            if data != original_value:
                raise DmxsegError('Verify of dmxseg address 0x%x failed, expected 0x%x but got 0x%x' 
                        % (addr, original_value, data))
                        
class DAEmulationMixin(object):
    def forwarder(self, name, default):
        return getattr(self.real_da, name, lambda:default)()
        
    def GetDAMode(self):
        return self.forwarder('GetDAMode', 'scanonly')
        
    def DAReset(self):
        self.real_da.DAReset()
        
    def GetIdentifier(self):
        return '%s' % (identifier_prefix)
        
    def GetFirmwareVersion(self):
        return self.forwarder('GetFirmwareVersion', '0.0.0')
        
    def RefreshLoggerLevels(self, *_args, **_kwargs):
        self.forwarder('RefreshLoggerLevels', None)
    
    def WriteDASetting(self, *args, **kwargs):
        write_da_setting = getattr(self.real_da, 'WriteDASetting', None)
        if write_da_setting is not None:
            write_da_setting(*args, **kwargs)
            
    def GetDASettingList(self):
        return self.forwarder('GetDASettingList', [])
        
    def ReadDASetting(self, name):
        rds = getattr(self.real_da, 'ReadDASetting')
        if rds is not None:
            return rds(name)
        else:
            return 0
            
    def SetJTAGClock(self, rate):
        sjc = getattr(self.real_da, 'SetJTAGClock')
        if sjc is not None:
            return sjc(rate)
        else:
            return 0
        
    def GetJTAGClock(self):
        return self.forwarder('GetJTAGClock', 1024)
        
    def Disconnect(self):
        pass
        
    def TapReset(self, type='both'):
        self.real_da.TapReset(type)
        
    def SystemReset(self):
        self.real_da.systemreset()
        
    def Scan(self, irdata, drdata):
        return self.real_da.Scan(irdata, drdata)
        
    def GetCurrentISA(self, _address):
        return 'mips64r6'
        
    def GetActiveTC(self):
        return -1
        
    def GetActiveASID(self):
        return -1
        
    def GetABI(self):
        return 'n64'
        
    def ReadDAConfigurationData(self, *_args):
        return []
        
    def ProbeInfo(self):
        return self.forwarder('ProbeInfo', [])
        
    def GetProbeSettings(self):
        rds = getattr(self.real_da, 'GetProbeSettings', None)
        if rds is not None:
            return rds()
        else:
            return {'JTAG Logging':0}
            
    def SetProbeSetting(self, name, value, scope='probe'):
        rds = getattr(self.real_da, 'SetProbeSetting', None)
        
        if rds is not None:
            return rds(name, value, scope)
        
# DBU specific things, relies on Scan and tapreset from the socket driver
class DBUDevice(Device, DAEmulationMixin):
    globalThrottle = True
    fdcSize = 0
    DBU_IR_WIDTH = 5
    
    def __init__(self, dbudriver):
        self.real_da             = dbudriver
        self.da                  = self
        self.tiny                = self
        self.rb_accessor         = RBAccessor(self)
        self.dmxseg_accessor     = DMXSEGAccessor(self)
        self.core_reset_timeout  = 100
        self.probe               = self
        self.name                = 'DBUDevice'
        
    def on_each_command(self):
        pass
        
    def SetTimeouts(self, dmxseg_read=None, dmxseg_write=None, rb_valid=None):
        if dmxseg_read is not None:
            self.dmxseg_accessor.dmxsegread_timeout = dmxseg_read
        if dmxseg_write is not None:
            self.dmxseg_accessor.dmxsegwrite_timeout = dmxseg_write
        if rb_valid is not None:
            self.rb_accessor.rb_valid_timeout = rb_valid
        return Timeouts(self.dmxseg_accessor.dmxsegread_timeout, 
                self.dmxseg_accessor.dmxsegwrite_timeout, 
                self.rb_accessor.rb_valid_timeout)
        
    tap_regs = {
        'idcode' : 
            {
                'ir' : 1,
                'numbits' : 32,
            },
        'impcode' : 
            {
                'ir' : 3,
                'numbits' : 32,
            },
        'slaveaddr' : 
            {
                'ir' : 4,
                'numbits' : 24,
            },
        'clusteraddr' : 
            {
                'ir' : 5,
                'numbits' : 24,
            },
        'rbaddr' : 
            {
                'ir' : 6,
                'numbits' : 24,
            },
        'rbdata' : 
            {
                'ir' : 7,
                'numbits' : 66,
            },
        'vpeboot' : 
            {
                'ir' : 9,
                'numbits' : 32,
            },
        'control' : 
            {
                'ir' : 0xA,
                'numbits' : 32,
            },
        'dxaddr' : 
            {
                'ir' : 0xB,
                'numbits' : 24,
            },
        'dxdata' : 
            {
                'ir' : 0xC,
                'numbits' : 66,
            },
        'rbheader' : 
            {
                'ir' : 0xD,
                'numbits' : 64,
            },
        'rbpayload' : 
            {
                'ir' : 0xE,
                'numbits' : 64,
            },
        'rbbuserrinfo' : 
            {
                'ir' : 0xF,
                'numbits' : 64,
            }
    }
    
    def read_tap_reg(self, name, value=0):
        ir = word_to_bits(self.tap_regs[name]['ir'], self.DBU_IR_WIDTH)
        dr = word_to_bits(value, self.tap_regs[name]['numbits'])
        return int(self.Scan(ir, dr), 2)
        
    def rbbuserrinfo(self):
        return self.read_tap_reg('rbbuserrinfo')

    def idcode(self):
        return self.read_tap_reg('idcode')

    def impcode(self):
        return self.read_tap_reg('impcode')

    def slaveaddr(self, val):
        return self.read_tap_reg('slaveaddr', val)

    def clusteraddr(self, val):
        return self.read_tap_reg('clusteraddr', val)

    def rbaddr(self, val):
        return self.read_tap_reg('rbaddr', val)

    def rbdata(self, val):
        return self.read_tap_reg('rbdata', val)

    def vpeboot(self, val):
        return self.read_tap_reg('vpeboot', val)

    def control(self, val):
        return self.read_tap_reg('control', val)

    def dxaddr(self, val):
        return self.read_tap_reg('dxaddr', val)

    def dxdata(self, val):
        return self.read_tap_reg('dxdata', val)

    def rbheader(self):
        return self.read_tap_reg('rbheader', 0)

    def rbpayload(self):
        return self.read_tap_reg('rbpayload')

    def rb_read(self, destId, coreId, vpeId, offset, is64bit, clusterId=0, gstId=0):
        return self.rb_accessor.read(destId, coreId, vpeId, offset, is64bit, 
            clusterId=clusterId, gstId=gstId)

    def rb_write(self, destId, coreId, vpeId, offset, is64bit, value, clusterId=0, gstId=0):
        self.rb_accessor.write(destId, coreId, vpeId, offset, is64bit, value,
            clusterId=clusterId, gstId=gstId)
        
    def reset_rb_bus(self):
        self.control(Control(dx_fdcsize=self.fdcSize & 0x7, pracc=1, gt=1 if self.globalThrottle else 0, rrb_reset=1))
        
        value = Control(rrb_reset=1)
        while value.rrb_reset == 1:
            value = Control(self.control(Control(dx_fdcsize=self.fdcSize & 0x7, pracc=1, gt=1 if self.globalThrottle else 0)))
        
    def commitDbuControl(self):
        return self.control(Control(dx_fdcsize=self.fdcSize & 0x7, pracc=1, gt=1 if self.globalThrottle else 0))

    def readDbuControl(self):
        return Control(self.commitDbuControl())
        
    def set_global_throttle(self, val):
        self.globalThrottle = val
        self.commitDbuControl()
        
    def get_global_throttle(self):
        self.globalThrottle = Control(self.readDbuControl()).gt
        return self.globalThrottle

    def set_fdcSize(self, val):
        self.fdcSize = val
        self.commitDbuControl()

    def gcr_config(self):
        return self.rb_accessor.read(RB_ID_GCR, 0, 0, OFFSET_GCR_CONFIG, True)

    def gcr_cl_config(self, coreId):
        return self.rb_accessor.read(RB_ID_GCR, coreId, 0, OFFSET_GCR_CL_CONFIG, True)

    def read_rocc_mask(self):
        return self.rb_accessor.read(RB_ID_CPC, 0, 0, OFFSET_CPC_ROCC_CTL_REG, True)
        
    def read_vcsuspend(self):
        return self.rb_accessor.read(RB_ID_CPC, 0, 0, OFFSET_CPC_CL_VC_SUSPEND, True)

    def clear_rocc_mask(self):
        return self.rb_accessor.write(RB_ID_CPC, 0, 0, OFFSET_CPC_ROCC_CTL_REG, True, MASK_32_BIT)

    def core_power(self, coreId, enable):
        val = CPC_CL_CMD_PWR_UP if enable else CPC_CL_CMD_PWR_DOWN
        self.rb_accessor.write(RB_ID_CPC, coreId, 0, OFFSET_CPC_CL_CMD_REG, True, val)
        
    def core_reset(self, coreId):
        #Issue reset
        self.rb_accessor.write(RB_ID_CPC, coreId, 0, OFFSET_CPC_CL_CMD_REG, True, CPC_CL_CMD_RESET)
        
        #Wait for power up 
        for _tries in range(self.core_reset_timeout):
            cmd = self.rb_accessor.read(RB_ID_CPC, coreId, 0, OFFSET_CPC_CL_CMD_REG, True)
            if cmd == CPC_CL_CMD_PWR_UP:
                break
        else:
            raise DbuDriverException("Timed out waiting for core %d to return from reset." % coreId)
        
    def read_vc_control1(self, coreId, vpeId):
        return self.rb_accessor.read(coreId, coreId, vpeId, DRSEG_OFFSET_VC_CONTROL1, True)

    def write_vc_control1(self, coreId, vpeId, val):
        return self.rb_accessor.write(coreId, coreId, vpeId, DRSEG_OFFSET_VC_CONTROL1, True, val)

    def read_vc_control2(self, coreId, vpeId):
        return self.rb_accessor.read(coreId, coreId, vpeId, DRSEG_OFFSET_VC_CONTROL2, True)

    def write_vc_control2(self, coreId, vpeId, val):
        return self.rb_accessor.write(coreId, coreId, vpeId, DRSEG_OFFSET_VC_CONTROL2, True, val)
        
    def core_power_up(self, coreId):
        self.rb_accessor.write(RB_ID_CPC, coreId, 0, OFFSET_CPC_CL_CMD_REG, True, CPC_CL_CMD_PWR_UP)
        
    def core_local_status(self, coreId):
        return self.rb_accessor.read(RB_ID_CPC, coreId, 0, OFFSET_CPC_CL_STAT_CONF_REG, True)
        
    def gic_status(self):
        return self.rb_accessor.read(RB_ID_GCR, 0, 0, OFFSET_GCR_GIC_STATUS, True)
        
    def set_synchronous_go(self, enable):
        self.rb_accessor.write(RB_ID_GIC, 0, 0, OFFSET_GIC_SH_DBG_CONFIG, True, 0 if enable else 1)
        
    def gic_dint_part(self, val):
        self.rb_accessor.write(RB_ID_GIC, 0, 0, OFFSET_GIC_SH_DINT_PART, True, val)
        
    def read_gic_dint_part(self):
        return self.rb_accessor.read(RB_ID_GIC, 0, 0, OFFSET_GIC_SH_DINT_PART, True)

    def write_ejtag_brk_mask(self, mask):
        self.rb_accessor.write(RB_ID_GIC, 0, 0, OFFSET_GIC_SH_EJTAG_BRK, True, mask)

    def read_ejtag_brk_mask(self):
        return self.rb_accessor.read(RB_ID_GIC, 0, 0, OFFSET_GIC_SH_EJTAG_BRK, True)
    
    def read_dm_mask(self):
        return self.rb_accessor.read(RB_ID_GIC, 0, 0, OFFSET_GIC_SH_DEBUGM_STATUS, True)
        
    def read_vc_run(self, coreId):
        return self.rb_accessor.read(RB_ID_CPC, coreId, 0, OFFSET_CPC_CL_VC_RUN, True)
        
    def write_vc_run(self, coreId, value):
        self.rb_accessor.write(RB_ID_CPC, coreId, 0, OFFSET_CPC_CL_VC_RUN, True, value)
        
    def dmxsegread(self, addr, size):
        return self.dmxseg_accessor.read(addr, size)
                
    def dmxsegwrite(self, addr, value, size, verify=False):
        self.dmxseg_accessor.write(addr, value, size, verify=verify)
        
    def is_in_debug(self, core_number, vc_number):
        brkmask = 1 << (4 * core_number + vc_number)
        return bool(self.read_dm_mask() & brkmask)
    
UINT8_ARRAY_TYPE  = 'B'
UINT16_ARRAY_TYPE = 'H'
UINT32_ARRAY_TYPE = 'I'
MAX_UINT8         = 2 ** 8 - 1
MAX_UINT16        = 2 ** 16 - 1
MAX_UINT32        = 2 ** 32 - 1
MAX_UINT64        = 2 ** 64 - 1

def _maxint(size):
    if size == 1:
        return MAX_UINT8
    elif size == 2:
        return MAX_UINT16
    elif size == 4:
        return MAX_UINT32
    else:
        return MAX_UINT64

def element_size_to_array_type(ElementSize):
    if ElementSize == 1:
        return UINT8_ARRAY_TYPE
    if ElementSize == 2:
        return UINT16_ARRAY_TYPE
    if ElementSize == 4:
        return UINT32_ARRAY_TYPE
    else:
        # there is no 64bit array type :-(
        # But we will work around this by packing unpacking into 32-bits
        raise NotImplementedError()
        
def _values64_as_values32(values):
    """Reinterpret a list of 64bit values as a list of 32bit values (assumes
    little endian.

    >>> ["0x%08x" % x for x in _values64_as_values32([0x1234567887654321])]
    ['0x87654321', '0x12345678']
    """
    ret = []
    for value in values:
        ret.append(value & 0xffffffff)
        ret.append((value >> 32) & 0xffffffff)
    return ret

def _values32_as_values64(values):
    """Reinterpret a list of 32bit values as a list of 64bit values (assumes
    little endian.

    >>> ["0x%016x" % x for x in _values32_as_values64([0x87654321, 0x12345678])]
    ['0x1234567887654321']
    >>> ["0x%016x" % x for x in _values32_as_values64([0x87654321, 0x12345678, 0x10fedcba, 0xabcdef01])]
    ['0x1234567887654321', '0xabcdef0110fedcba']
    """
    return [a | (b << 32) for a, b in zip(values[::2], values[1::2])]

def _values_as_buf(values, ElementType = 4):
    """Returns the sequence of values as a binary buffer (using the given ElementType)."""
    if isinstance(values, (int, long)):
        values = [values]
    if ElementType == 8:
        return _values_as_buf(_values64_as_values32(values))
    m = _maxint(ElementType)
    values = [x & m for x in values]
    return array.array(element_size_to_array_type(ElementType), values).tostring()

def _buf_as_values(buf, ElementType = 4):
    """Returns the sequence of values as a binary buffer (using the given ElementType)."""
    if ElementType == 8:
        return _values32_as_values64(_buf_as_values(buf))
    return array.array(element_size_to_array_type(ElementType), buf).tolist()
    
class MisalignedAdaptor(object):
    """Intercepts calls to ReadMemoryBlock and WriteMemoryBlock so that accesses
    are always 32-bit aligned.
    """
    def __init__(self, reader, writer):
        self._reader, self._writer = reader, writer
        
    def read(self, Address, ElementCount, ElementType=4, MemoryType=0):
        """Convert a non 32-bit read into a 32 bit read."""
        if ElementType == 4 and (Address & 3) == 0:
            return self._reader(Address, ElementCount, ElementType, MemoryType)
        leading_misaligment = Address & 3
        bytes_to_read = ElementCount * ElementType + leading_misaligment
        trailing_misalignment = (4 - (bytes_to_read & 3)) % 4
        bytes_to_read += trailing_misalignment
        words = bytes_to_read // 4
        values = self._reader(Address - leading_misaligment, words, 4, MemoryType)
        buf = _values_as_buf(values)
        buf = buf[leading_misaligment:len(buf) - trailing_misalignment]
        return _buf_as_values(buf, ElementType)

    def write(self, Address, ElementCount, ElementType, Data, MemoryType=0):
        """Convert a non 32-bit write into 32 bit read-modify writes."""
        if ElementType == 4 and (Address & 3) == 0:
            return self._writer(Address, ElementCount, ElementType, Data, MemoryType)
        leading_misaligment = Address & 3
        bytes_to_write = ElementCount * ElementType + leading_misaligment
        trailing_misalignment = (4 - (bytes_to_write & 3)) % 4
        bytes_to_write += trailing_misalignment
        buf = _values_as_buf(Data, ElementType)
        # now read the bits that we need to read-modify-write
        first_address = Address - leading_misaligment
        last_address  = Address + ElementCount * ElementType + trailing_misalignment - 4
        read = None
        if leading_misaligment:
            read = _values_as_buf(self._reader(first_address, 1, 4, MemoryType))
            buf   = read[0:leading_misaligment] + buf
        if trailing_misalignment:
            if read is None or first_address != last_address:
                read = _values_as_buf(self._reader(last_address, 1, 4, MemoryType))
            buf  = buf + read[-trailing_misalignment:]
        self._writer(first_address, bytes_to_write // 4, 4, _buf_as_values(buf), MemoryType)
    
class ImgCore(object):
    def __init__(self, dbudriver, coren):
        self.dbudriver = dbudriver
        self.coren = coren
        self._thread = 0
        self._num_threads = self.dbudriver.vpes
        self._cpu_info = {  "cpu_is_32bit"            : False, 
                            "cpu_name"                : 'I6400',
                            "display_name"            : 'I6400',
                            "shared_cache_regs"       : False,
                            "has_l1_icache"           : True,
                            "l1_icache_line_size"     : 64,
                            "l1_icache_associativity" : 4,
                            "l1_icache_sets_per_way"  : 128,
                            "l1_icache_tag_size"      : 1,
                            "l1_icache_data_size"     : 2,
                            "has_l1_dcache"           : True,
                            "l1_dcache_line_size"     : 64,
                            "l1_dcache_associativity" : 4,
                            "l1_dcache_sets_per_way"  : 128,
                            "l1_dcache_tag_size"      : 1,
                            "l1_dcache_data_size"     : 2,
                            "has_l2_cache"            : False,
                            "has_l3_cache"            : False,
                            "has_vze"                 : False,
                            }
        
    def CpuInfo(self, update=False):
        return self._cpu_info.items()
        
    def VpeCount(self):
        return self._num_threads
        
    def Read32(self, address):
        """Read a 32-bit value from `address`."""
        return self.BlockRead32(address, 1)[0]

    def BlockRead32(self, address, count):
        """Read `count` 32-bit values starting from `address`."""
        if is_dmxseg_addr(address):
            return [self.dbudriver.dmxsegread(address+(i*4), 32) for i in range(count)]
        else:
            return monitor_read_memory(address, type=MDIMIPGVIRTUAL, count=count, size=32, device=self.dbudriver)

    def Write32(self, address, data):
        """Write the 32-bit value `data` to `address`."""
        self.BlockWrite32(address, [data])

    def BlockWrite32(self, address, data):
        """Write len(data) 32-bit values to `address`."""
        
        #Loading the monitor requires writing manually
        if is_dmxseg_addr(address):
            for value, i in zip(data, itertools.count()):
                self.dbudriver.dmxsegwrite(address+(i*4), value, 32, verify=False)
        else:
            monitor_write_memory(address, data, count=len(data), size=32, device=self.dbudriver)

    def Reset(self):
        raise Exception('TODO')
        
class Breakpoint(object):
    def __init__(self, address, type, data, isa, hw_index = -1):
        self.address = address
        '''The address of the breakpoint.'''
        
        self.enabled = False
        '''Whether the breakpoint is currently enabled.'''
        
        self.active = False
        '''Whether the breakpoint is currently active, i.e. exists on the target.'''
        
        self.type = type
        '''Whether the breakpoint is currently active, i.e. exists on the target.'''
        
        self.data = data
        '''A string, either 'sw' of 'hw', for software, or hardware breakpoints.
        Other types may be made available in the future.'''
        
        self.isa = isa
        '''The isa of the instruction breakpointed.'''
        
        self.hw_index = hw_index
        '''The hardware index of the breakpoint, if it a hardware breakpoint.'''
        
    def _for_display(self):
        return ('0x%08x' % self.address, 
                    ['Disabled', 'Enabled'][self.enabled], 
                    self.type, '0x%0*x' % (2 * 4, self.data), 
                    str(self.hw_index))
                    
    def __repr__(self):
        vals = [self._for_display()]
        return rst.simple_table(['Address', 'Enabled', 'Type', 'Data', 'HW Index'], vals)
        
class BreakpointMixin(object):
    DRSEG_BASE = 0xFFFFFFFFFF300000
    IBA        = DRSEG_BASE + 0x1100
    IBM        = DRSEG_BASE + 0x1108
    IBAsid     = DRSEG_BASE + 0x1110
    IBC        = DRSEG_BASE + 0x1118
    IBCC       = DRSEG_BASE + 0x1120
    IBPC       = DRSEG_BASE + 0x1128
    IBSTATUS   = DRSEG_BASE + 0x1000
    
    def ClearBreakpointTriggered(self):
        stat = self.ReadMemory(self.IBSTATUS, 1, 8)
        stat &= ~0x7FFF
        self.WriteMemory(self.IBSTATUS, stat, 8)
        
    def GetTriggeredBreakpointID(self):
        pc, debug = self.ReadRegisters(['pc', 'debug'])
        if debug & (1 << 31):
            #Instruction in the delay slot caused the exception
            pc += 4
        
        possible_bkpts = {}
        for id, bp in zip(self._breakpoints.keys(), self._breakpoints.values()):
            if bp.address == pc:
                possible_bkpts[id] = bp
        
        break_status = None
        for id in possible_bkpts:
            bp = possible_bkpts[id]
            if bp.type == 'sw':
                if bp.enabled:
                    return id
            else:
                if break_status is None:
                    break_status = self.ReadMemoryBlock(self.IBSTATUS, 1, 4)[0]
                if break_status & (1 << bp.hw_index):
                    return id
                    
        return -1
    
    def _check_existing_breakpoint(self, address):
        addresses = [b.address for b in self._breakpoints.values()]
        if address in addresses:
            raise RuntimeError("A breakpoint already exists at address 0x%08x" % address)
            
    def _get_new_bp_id(self):
        current_max = max(self._breakpoints.keys()) if self._breakpoints else -1
        return current_max+1
        
    def CreateBreakpoint(self, address, type, isa, _options):
        if isa == 'auto':
            isa = 'mips64r6'
        
        if type == TinyBreakpointType.Hardware:
            num_code_bps, _num_data_bps = self.GetNumTriggers()
            self._check_existing_breakpoint(address)
            break_id = self._find_free_brk(self._breakpoints, num_code_bps)
            
            if break_id != -1:
                bp = Breakpoint(address, type, 0, isa, hw_index=break_id)
                new_id = self._get_new_bp_id()
                self._breakpoints[new_id] = bp
                self._bkpt_enable(new_id, isa)
            else:
                raise RuntimeError("failed to create hard breakpoint at 0x%08x, insufficient hardware resources available" % address)
            
        elif type == TinyBreakpointType.Software:
            self._check_existing_breakpoint(address)
            self._bkpt_test(address, isa)
            data = self._read_inst_under_breakpoint(address)
            bp = Breakpoint(address, type, data[0], isa)
            
            #Make up an ID and add to main list
            new_id = self._get_new_bp_id()
            self._breakpoints[new_id] = bp
            self._bkpt_enable(new_id, isa)
            
            return new_id
        
        elif type == TinyBreakpointType.Data_Watch:
            raise RuntimeError("Data watch breakpoints not supported.")
            
    def EnableBreakpoint(self, id, enable):
        try:
            bp = self._breakpoints[id]
        except KeyError:
            raise RuntimeError('No breakpoint found with ID %d' % id)
        else:
            if enable:
                bp.enabled = True
                try:
                    self._activate(bp)
                except Exception as e:
                    bp.enabled = False
                    raise e
            else:
                bp.enabled = False
                try:
                    self._suppress_breakpoint(bp)
                except Exception as e:
                    bp.enabled = True
                    raise e
                
    def SuppressBreakpoint(self, id, suppress):
        try:
            bp = self._breakpoints[id]
        except KeyError:
            raise RuntimeError('No breakpoint found with ID %d' % id)
        else:
            if not bp.enabled:
                raise RuntimeError('Cannot suppress a disabled breakpoint.')
            else:
                if suppress:
                    self._suppress_breakpoint(bp)
                else:
                    self._activate(bp)
        
    def DeleteBreakpoint(self, id):
        try:
            bp = self._breakpoints.pop(id)
        except KeyError:
            raise RuntimeError('No breakpoint found with ID %d' % id)
        else:
            if bp.enabled:
                bp.endabled = False
                try:
                    self._suppress_breakpoint(bp)
                except Exception:
                    #Pass this exception on?
                    bp.enabled = True
        
    def FormatBreakpoint(self, _id):
        raise RuntimeError("FormatBreakpoint")
        
    def GetBreakpoint(self, id):
        try:
            bp = self._breakpoints[id]
        except KeyError:
            raise RuntimeError('No breakpoint found with ID %d' % id)
        else:
            return (bp.address, bp.enabled, bp.active, bp.type, 'mips64r6', bp.hw_index,
                    bp.data, 0x0, 'both', 32, 0x0, 0x0, 'none', 0x1ff)
        
    def GetAllBreakpointIDs(self):
        return self._breakpoints.keys()
        
    def GetNumTriggers(self):
        code_bps = 0 
        data_bps = 0
        
        dbg = self.ReadRegister('debug')
        #Check that drseg is present (active low)
        if not dbg & 0x20000000:
            #Assume that drseg exists
            instr_bp_reg_addr = self.DRSEG_BASE + 0x1000
            ibs = self.ReadMemory(instr_bp_reg_addr)
            code_bps = (ibs >> 24) & 0xf
                
            data_bp_reg_addr = self.DRSEG_BASE + 0x2000
            dbs = self.ReadMemory(data_bp_reg_addr)
            data_bps = (dbs >> 24) & 0xf
            
        return (code_bps, data_bps)
            
    def _bkpt_test(self, address, _isa):
        address = address & ~3
        size = 4
        val = self.ReadMemoryBlock(address, 1, size)
        test_val = self._make_test_value(val[0], size)
        self.WriteMemoryBlock(address, 1, size, [test_val])
        try:
            got = self.ReadMemoryBlock(address, 1, size)
            if got[0] == test_val:
                return True
            raise RuntimeError("Cannot write to address 0x%08x, expected to read 0x%x but got 0x%x"  % (address, val[0], got[0]))
        finally:
            try:
                self.WriteMemoryBlock(address, 1, size, val)
            except Exception as e:
                print "Failed to put test data back whilst testing breakpoint writeability (%s)" % (e,)
                
    def _read_inst_under_breakpoint(self, address):
        # We always read 32 bits on an aligned address
        address &= ~3
        data = self.ReadMemoryBlock(address, 1, 4)[0]
        data = [(data >> ((3-i)*8)) & 0xFF for i in range(4)]
        return data
        
    def _write_bp_inst(self, bp):
        instr = 0x0000000e # sdbbp
        address = bp.address & ~3
        self.WriteMemoryBlock(address, 1, 4, [instr])
        
    def _activate(self, bp):
        if not bp.active:
            if bp.enabled:
                if bp.type == TinyBreakpointType.Software:
                    bp.data = self._read_inst_under_breakpoint(bp.address)
                    self._write_bp_inst(bp)
                else:
                    if bp.hw_index == -1:
                        raise RuntimeError("Insufficient hardware resources available for hardware breakpoint.")

                    element_size = 8
                    memtype = 0
                    offset = 0x100
                    self.WriteMemoryBlock(self.IBA    + offset * bp.hw_index, 1, element_size, bp.address, memtype)
                    self.WriteMemoryBlock(self.IBM    + offset * bp.hw_index, 1, element_size, 0,          memtype)
                    self.WriteMemoryBlock(self.IBAsid + offset * bp.hw_index, 1, element_size, 0,          memtype)

                    # These two should only be called if Complex Break and Triggers are available
                    self.WriteMemoryBlock(self.IBCC + offset * bp.hw_index, 1, element_size, 0, memtype)
                    self.WriteMemoryBlock(self.IBPC + offset * bp.hw_index, 1, element_size, 0, memtype)

                    # Here we enable the break
                    self.WriteMemoryBlock(self.IBC + offset * bp.hw_index, 1, element_size, 1, memtype)

                bp.active = True
        
    def _bkpt_enable(self, id, isa):
        if id == "all":
            for id in self._breakpoints.keys():
                self._bkpt_enable(id, isa)
        else:
            try:
                bp = self._breakpoints[id]
                if not bp.enabled:
                    bp.enabled = True
                    try:
                        self._activate(bp)
                    except Exception:
                        bp.enabled = False
            except KeyError:
                raise RuntimeError("No breakpoint with ID %d" % id)
                
    def _make_test_value(self, existing, size):
        start = (1 << (size * 8)) - 1
        return start - existing 

    def _suppress_breakpoint(self, bp):
        if bp.active:
            if bp.type == TinyBreakpointType.Software:
                address = bp.address & ~3
                data = 0
                for i, x in enumerate(bp.data):
                    data |= (x << ((3-i)*8))
                self.WriteMemoryBlock(address, 1, 4, (data,))
            else:
                if bp.hw_index == -1:
                    raise RuntimeError("Insufficient hardware resources available for hardware breakpoint.")
                    
                element_size = 8
                memtype = 0
                self.WriteMemoryBlock(self.IBC + 0x100 * bp.hw_index, 1, element_size, 0, memtype)
                self.WriteMemoryBlock(self.IBA + 0x100 * bp.hw_index, 1, element_size, 0, memtype)

            bp.active = False
            
    def _find_free_brk(self, breakpoints, max_bps):
        hw_brks = [brk.hw_index for brk in breakpoints.values() if brk.type == 'hw']
        hw_brks.sort()
        for i, _ in enumerate(hw_brks):
            if i != hw_brks[i]:
                return i
        if len(hw_brks) < max_bps:
            return len(hw_brks)
        return -1

class ImgSoc(BreakpointMixin):
    """Provides a DAtiny like interface to a Meta SoC using scan operations."""
    def __init__(self, dbudriver, cores, core=0, vpe=0):
        self._misaligned = MisalignedAdaptor(self._aligned_read, self._aligned_write)
        self._cores = cores
        self._dbudriver = dbudriver
        self._core = core
        self._vpe = vpe
        self._abi = 'n64'  # should be o64 but DAtinyscript doesn't know about it yet
        self._breakpoints = {}
        
    def SoC(self, _soc):
        return self
        
    def SoCCount(self):
        return 1
    
    def SoCNumber(self):
        return 0
        
    def GetFlatCore(self):
        return self.CoreNumber()
    
    def CoreNumber(self):
        return self._core

    def CoreCount(self):
        return len(self._cores)

    def VpeNumber(self):
        return self._vpe

    def VpeCount(self):
        return self._cores[self._core].VpeCount()
        
    def GetTargetFamily(self):
        return CoreFamily.mips
        
    def CpuInfo(self, update=False):
        return self._cores[self.CoreNumber()].CpuInfo()

    def _aligned_write(self, Address, ElementCount, ElementType, Data, MemoryType = 0):
        if isinstance(Data, (int, long)):
            Data = [Data]
        assert ElementCount == len(Data), \
            "ElementCount %d is not equal to len(Data) %d" % (ElementCount, len(Data))
        assert ElementType == 4 and (Address % 4) == 0
        self._cores[self._core].BlockWrite32(Address, Data)

    def _aligned_read(self, Address, ElementCount, ElementType = 4, MemoryType = 0):
        assert ElementType == 4 and (Address % 4) == 0
        return self._cores[self._core].BlockRead32(Address, ElementCount)
    
    def Core(self, core):
        return ImgSoc(self._dbudriver, self._cores, core, 0)
        
    def Vpe(self, vpe):
        return ImgSoc(self._dbudriver, self._cores, self.CoreNumber(), vpe)
        
    def GetEndian(self):
        return False
        
    def SetABI(self, abi):
        self._abi = abi
        
    def GetABI(self):
        return self._abi
    
    def GetIdentifier(self):
        return 'scan_dbu_device!'
            
    def HardReset(self):
        self._cores[self.CoreNumber()].Reset()
        
    def CacheOperation(self, address, line_size, operation, count=1, flags=0):
        monitor_cache_op(address, line_size, operation, count, flags, device=self._dbudriver)
        
    def ReadMemory(self, Address, ElementType=4, MemoryType=0):
        return self.ReadMemoryBlock(Address, 1, ElementType, MemoryType)[0]
        
    def WriteMemory(self, Address, value, ElementType=4, MemoryType=0):
        self.WriteMemoryBlock(Address, 1, ElementType, [value], MemoryType)

    def ReadMemoryBlock(self, Address, ElementCount, ElementType=4, MemoryType=0):
        if not is_dmxseg_addr(Address):
            self.Stop()
        return self._misaligned.read(Address, ElementCount, ElementType, MemoryType)

    def WriteMemoryBlock(self, Address, ElementCount, ElementType, Data, MemoryType=0):
        if not is_dmxseg_addr(Address):
            self.Stop()
        return self._misaligned.write(Address, ElementCount, ElementType, Data, MemoryType)
        
    def get_register_index(self, reg):
        return get_register_index(self.GetABI(), reg)
                
    def is_fpu_reg(self, reg):
        #Detect msa/fpu register name
        re_fpu = r'([d|f|w])(\d+)'
        m = re.match(re_fpu, reg)
        if m:
            return (m.group(1), int(m.group(2)))
        else:
            return (None, None)
            
    def get_msa_control_index(self, reg):
        msa_control_names = ['msair', 'msacsr', 'msaaccess', 'msasave', 'msamodify', 
                             'msarequest', 'msamap', 'msaunmap']
        try:
            return msa_control_names.index(reg)
        except ValueError:
            raise DBUError("MSA register '%s' not found." % reg)
            
    def get_fpu_control_index(self, reg):
        fpu_control_names = {'fir'  : 0 ,
                             'fexr' : 26,
                             'fenr' : 28,
                             'fcsr' : 31,
                            }
        try:
            return fpu_control_names[reg]
        except KeyError:
            return None 

    def get_shadow_set_index(self, reg):
        m = re.match(r"r(?P<index>.+)\.(?P<set>.+)", reg)
        if m:
            return int(m.group('set')), int(m.group('index'))
        else:
            m = re.match(r"(?P<index>.+)\.(?P<set>[0-9]+)", reg)
            if m:
                return int(m.group('set')), self.get_register_index(m.group('index'))[0]

    def ReadRegister(self, reg):
        self.Stop()
        reg = reg.lower()
        
        if reg == 'pc':
            return monitor_read_pc(device=self._dbudriver)
        else:
            type, index = self.is_fpu_reg(reg)
            
            if type is not None:
                if type == 'f':
                    return monitor_read_fpu_single_register(index, 1, device=self._dbudriver)[0]
                elif type == 'd':
                    return monitor_read_fpu_double_register(index, 1, device=self._dbudriver)[0]
                elif type == 'w':
                    return monitor_read_msa_register(index, 1, device=self._dbudriver)[0]
            else:
                if reg.startswith('msa'):
                    index = self.get_msa_control_index(reg)
                    return monitor_read_msa_control_register(index, 1, device=self._dbudriver)[0]
                else:
                    cp1c_index = self.get_fpu_control_index(reg)
                    if cp1c_index is not None:
                        return monitor_read_cp1c_register(cp1c_index, 1, device=self._dbudriver)[0]
                    else:
                        shadow_info = self.get_shadow_set_index(reg)
                        if shadow_info:
                            set, index = shadow_info
                            return monitor_read_shadow_gp_register(set, index, 1)[0]

                        index = self.get_register_index(reg)
                    
                        if len(index) == 1:
                            return monitor_read_gp_register(index[0], 1, device=self._dbudriver, immediate=True)[0]
                        else:
                            return monitor_read_cp0_register(index[0], index[1], 1, device=self._dbudriver, immediate=True)[0]

    def WriteRegister(self, reg, value):
        self.Stop()
        reg = reg.lower()
        
        if reg == 'pc':
            monitor_write_pc(value, device=self._dbudriver)
            return
        else:
            type, index = self.is_fpu_reg(reg)
            
            if type is not None:
                if type == 'f':
                    monitor_write_fpu_single_register(index, [value], device=self._dbudriver)
                    return
                elif type == 'd':
                    monitor_write_fpu_double_register(index, [value], device=self._dbudriver)
                    return
                elif type == 'w':
                    monitor_write_msa_register(index, [value], device=self._dbudriver)
                    return
            else: 
                if reg.startswith('msa'):
                    index = self.get_msa_control_index(reg)
                    monitor_write_msa_control_register(index, [value], device=self._dbudriver)
                else:
                    cp1c_index = self.get_fpu_control_index(reg)
                    if cp1c_index is not None:
                        monitor_write_cp1c_register(cp1c_index, [value], device=self._dbudriver)
                    else:
                        shadow_info = self.get_shadow_set_index(reg)
                        if shadow_info:
                            set, index = shadow_info
                            monitor_write_shadow_gp_register(set, index, [value])
                        else:
                            index = self.get_register_index(reg)
                            
                            if len(index) == 1:
                                monitor_write_gp_register(index[0], [value], device=self._dbudriver, immediate=True)
                            else:
                                monitor_write_cp0_register(index[0], index[1], [value], device=self._dbudriver, immediate=True)
         
    def ReadRegisters(self, regs, float_as_int=False):
        return [self.ReadRegister(reg) for reg in regs]

    def WriteRegisters(self, regs, values, float_as_int=False):
        for reg, value in zip(regs, values):
            self.WriteRegister(reg, value)
            
    def Step(self, steps=1, threads=None):
        self.Stop()
        self.ClearBreakpointTriggered()
        
        #Turn on single step
        dbg = monitor_read_cp0_register(23, 0, 1, device=self._dbudriver)[0]
        monitor_write_cp0_register(23, 0, [dbg | (1 << 8)], device=self._dbudriver)
        
        try:
            while steps:
                monitor_resume(self.CoreNumber(), self.VpeNumber(), device=self._dbudriver)
                if not self._dbudriver.is_in_debug(self.CoreNumber(), self.VpeNumber()):
                    raise DBUError("Did not return to debug mode after a single step.")
                
                steps -= 1
        finally:
            #If it doesn't return from debug we need to force that
            self.Stop()
            dbg = monitor_read_cp0_register(23, 0, 1, device=self._dbudriver)[0]
            monitor_write_cp0_register(23, 0, [dbg & ~(1 << 8)], device=self._dbudriver)
            
    def Run(self, threads=None):
        if self._dbudriver.is_in_debug(self.CoreNumber(), self.VpeNumber()):
            self.ClearBreakpointTriggered()
            monitor_resume(self.CoreNumber(), self.VpeNumber(), device=self._dbudriver)

    def Stop(self, threads=None):    
        in_debug = self._dbudriver.is_in_debug(self.CoreNumber(), self.VpeNumber())
        rbreg('rocc_ctl_reg', 0xffffffffffffffff)

        try:
            check_monitor_version(EXPECTED_MONITOR_VERSION, device=self._dbudriver)
            check_monitor_instruction_buff_guard(device=self._dbudriver)
            check_monitor_data_buff_guard(device=self._dbudriver)
        except DebugMonitorError as e:
            print e
            
            if in_debug:
                #Stalling whilst we load should minimise any damage done
                dbuglobalthrottle(True, device=self._dbudriver)
                saved = save_monitor_debug_data(device=self._dbudriver)
                print "Warning: loading monitor whilst in debug mode."
            
            load_monitor(device=self._dbudriver)
            
            if in_debug:
                restore_monitor_debug_data(saved, device=self._dbudriver)
                dbuglobalthrottle(False, device=self._dbudriver)

        if not in_debug:
            reset_monitor_entry_level(device=self._dbudriver)
            enter_debug_dbu(False, False, self._dbudriver, 
                core_number=self.CoreNumber(), vc_number=self.VpeNumber())
        
    def GetState(self):
        from imgtec.codescape.tiny import State
        from imgtec.codescape.da_types import Status

        pc = 0x9c9c9c9c
        
        if self._dbudriver.is_in_debug(self.CoreNumber(), self.VpeNumber()):
            status = Status.halted_by_probe
            
            id = self.GetTriggeredBreakpointID()
            if id != -1:
                if self._breakpoints[id].type == 'sw':
                    status = Status.sw_break
                else:
                    status = Status.hw_break
            else:
                #Check for debug single step exception
                dbg      = self.ReadRegister('debug')
                dbg_dss  = dbg & 1
                dbg_dint = dbg & (1 << 5)
                
                #Work around where debug::DSS isn't reset
                if dbg_dss and not dbg_dint:
                    status = Status.single_stepped
            
            try:
                #Do this check manually so that we don't end up loading the monitor
                #when all we wanted was running/halted
                check_monitor_version(EXPECTED_MONITOR_VERSION, device=self._dbudriver)
                pc = monitor_read_pc(device=self._dbudriver)
            except DebugMonitorError as e:
                print e
        else:
            status = Status.running
            
        return State(status, pc, 0)
        
    def Disassemble(self, address, count, isa):
        from imgtec.codescape.tiny import DisassembleBytes
        if isa == 'auto':
            isa = 'mips64r6+msa'
        words = self.ReadMemoryBlock(address, count, 4)
        return DisassembleBytes(address, count, isa, self.GetABI(), ''.join(struct.pack('>I', value) for value in words))
        
    def GetDAMode(self):
        return 'slowmode'
        
    def WriteTLB(self, index, entrylo0, entrylo1, entryhi, pagemask):
        #Dummy guestctl1
        monitor_write_tlb(index, [[entrylo0, entrylo1, entryhi, pagemask, 0x0]], 
            device=self._dbudriver)
        
    def ReadTLB(self, index):
        #Guest support to come when TLB command is updated
        entry = monitor_read_tlb(index, 1, device=self._dbudriver)[0]
        entry = [entry.entrylo0, entry.entrylo1, entry.entryhi, entry.pagemask]
        return entry
         
    def __getattr__(self, name):
        """Forward all other commands onto the underlying device."""
        return getattr(self._dbudriver, name)
        
def is_dmxseg_addr(address):
    return DMXSEG_BEGIN <= address <= DMXSEG_END

class DBUDeviceError(DBUError):
    pass
    
def check_is_wrapped_dbu(device):
    if not isinstance(device.da, (ImgSoc, DBUDevice)):
        raise DBUDeviceError("This command cannot be used with this target.")   

def dummy_tdd(cores, vcs):
    return tdd.Board(
          taps_on_chain=0x00000001,
          socs=[
            tdd.SoC(
              pos_in_chain=0x00000001,
              ir_length=0x00000005,
              tap_type=tdd.TapType.mips_oci,
              taps_per_soc=0x00000001,
              cores=[
                tdd.MipsCore(
                  core_img_id=tdd.CoreImgId.mips64r6,
                  dcr=0x00000020,
                  prid=0x0001a920,
                  config=[0x80004a05, 0x9e6b359b, 0x80000000, 0xfc8030a8, 0xd0fc0127, 0x00002c98, 0x00000000, 0x00000000],
                  mvp_conf0=0x00000000,
                  num_vcs=vcs,
                  ibs=0x48008000,
                  dbs=0x44008000,
                  cbtc=0x00000000,
                  trace_word_length=0x00000000,
                )]*cores,
            ),
          ],
        )

@command()
def dbuscandevices(verbose=False, device=None):
    '''
    Build a list of devices for use with the device command. 
    Each VPE will have a device, with the name 'scan_cX_vY' where X and Y are 
    the core and vpe number.
    '''
    check_is_wrapped_dbu(device)
    
    def log(msg):
        if verbose:
            print msg
    
    #determine number of cores and VPEs
    numcores = (device.da.gcr_config() & 0x7) + 1
    log("Numcores: %d" % numcores)

    numvcs = []
    for _core in range(numcores):
        vcs = (device.da.gcr_cl_config(0) & 0x3) + 1
        log("NumVCs: %d" % vcs)
        numvcs.append(vcs)
        device.da.vpes = vcs
        
    device.core_count = numcores
    device.vc_counts  = numvcs
    
    tinyemu = ImgSoc(device.da, [ImgCore(device.da, coren) for coren in range(numcores)])
    device.probe.socs = []
    device.probe._table = dummy_tdd(numcores, numvcs[0])
    device.probe._add_socs(tinyemu, 'scan_')
    
    return make_device_list(device, False)
        
def enter_debug_dbu(global_throttle, verbose, device, core_number=None, vc_number=None):
    '''
    Send current or specified core and vc into debug mode.
    '''
    def log(msg):
        if verbose:
            print msg
            
    if core_number is None:
        core_number = device.da.CoreNumber()
    if vc_number is None:
        vc_number = device.da.VpeNumber()
        
    #Set global throttle before sending vc into debug
    dbuglobalthrottle(global_throttle, device=device)
            
    #Get number of cores
    numcores = rbreg('gcr_config', device=device).pcores + 1
    log("Numcores: %d" % numcores)
    
    if core_number > (numcores-1):
        raise DBUError("Core %d not present" % core_number)

    #Get number of VCs for this core
    numvcs = rbreg('gcr_cl_config', coreID=core_number, device=device).pvpe + 1
    
    if vc_number > (numvcs-1):
        raise DBUError("VC %d not present" % vc_number)
    
    #Power up core
    device.da.core_power(core_number, True)
        
    # Set Proben and ProbTRAP on the VC
    log("Setting Probeen and Probtrap")
    log("Reading vc control core %d vc %d" % (core_number, vc_number))
    vc_control2 = rbreg('vc_control_2', coreID=core_number, vpeID=vc_number, device=device)
    vc_control2 = vc_control2._replace(probtrap=1, dmxsegen=1)
    rbreg('vc_control_2', coreID=core_number, vpeID=vc_number, value=vc_control2, device=device)

    # DINT VC
    log("Sending VC into debug mode")
    brkmask = 1 << (4 * core_number + vc_number)
    device.da.gic_dint_part(brkmask)
    device.da.write_ejtag_brk_mask(brkmask)

    #Check that VC is in debug mode
    if not device.da.is_in_debug(core_number, vc_number):
        raise DBUError("DM mask does not reflect VC being in debug mode.")

    # We should see PrAcc set
    control = device.da.readDbuControl()
    if not control & 0x2:
        log("Warning: PrAcc not set")
    
    log("Core %d VC %d sent into debug mode" % (core_number, vc_number))
    
def get_rb_accessor(device):
    tap_regs = [
            ('clusteraddr', 5, 24),
            ('slaveaddr', 4, 24),
            ('rbaddr', 6, 24),
            ('rbdata', 7, 66),
        ]
    return RBAccessor(FakeDBUTap(device, tap_regs), should_read_control=False)

rb_registers = {
    # Name                   destination offset                       per_core per_vpe read_only is64bit Type
    'vc_control_1'        : ('core',     0x0,                         True,    True,   False,    True,   VCControl1),
    'vc_control_2'        : ('core',     0x8,                         False,   True,   False,    True,   VCControl2),
    'gcr_config'          : (RB_ID_GCR,  OFFSET_GCR_CONFIG,           False,   False,  True,     True,   GCRConfig),
    'gcr_cl_config'       : (RB_ID_GCR,  OFFSET_GCR_CL_CONFIG,        True,    False,  True,     True,   GCRCLConfig),
    'rocc_ctl_reg'        : (RB_ID_CPC,  OFFSET_CPC_ROCC_CTL_REG,     False,   False,  False,    True,   CPCROCCCTRLReg),
    'cpc_cl_stat_conf_reg': (RB_ID_CPC,  OFFSET_CPC_CL_STAT_CONF_REG, True,    False,  False,    True,   CPCCLStatConfReg),
    'gcr_gic_status'      : (RB_ID_GCR,  0xD0,                        False,   False,  True,     True,   GCRGicStatus),
    'cpc_revision_reg'    : (RB_ID_CPC,  0x20,                        False,   False,  True,     True,   CPCRevisionReg),
    'cpc_cl_cmd'          : (RB_ID_CPC,  OFFSET_CPC_CL_CMD_REG,       True,    False,  False,    True,   CPCCLCmdReg),
    'gic_sh_debugm_status': (RB_ID_GIC,  OFFSET_GIC_SH_DEBUGM_STATUS, False,   False,  True,     True,   None),
    'gic_sh_dint_part'    : (RB_ID_GIC,  OFFSET_GIC_SH_DINT_PART,     False,   False,  False,    True,   None),    
    'gcr_bev_base'        : (RB_ID_GCR,  OFFSET_GCR_BEV_BASE,         False,   False,  False,    True,   None),
    'gcr_l2_config'       : (RB_ID_GCR,  0x0130,                      False,   False,  False,    True,   GCRL2Config),
    'vp_stop'             : (RB_ID_CPC,  0x2020,                      True,    False,  False,    True,   VPRunning),
    'vp_run'              : (RB_ID_CPC,  0x2028,                      True,    False,  False,    True,   VPRunning),
    'vp_running'          : (RB_ID_CPC,  0x2030,                      True,    False,  True,     True,   VPRunning),
    'gic_sh_teamid_lo'    : (RB_ID_GIC,  0x6020,                      False,   False,  False,    True,   TeamIDLo),
    'gic_sh_teamid_hi'    : (RB_ID_GIC,  0x6028,                      False,   False,  False,    True,   TeamIDHi),
    'gic_sh_teamid_ext'   : (RB_ID_GIC,  0x6070,                      False,   False,  False,    True,   TeamIDExt),
    'gic_sh_dbg_config'   : (RB_ID_GIC,  0x6080,                      False,   False,  False,    True,   GICSHDbgConfig),
}

g = globals()
rbreg_named = []
for key in rb_registers:
    f = named(key)
    g[key] = f
    rbreg_named.append(namedstring(f))
    
@command(register=rbreg_named)
def rbreg(register=None, value=None, coreID=None, vpeID=None, clusterID=0, gstID=0, device=None):
    '''
    Read or write a register using the register bus.
    Set value to write a register, leave register as None to list registers. 
    
    ========== ============================================================================
    Parameter  Meaning
    ========== ============================================================================
    register   RB register name, leave this as None to list available registers. 
    value      Set value to write to the register, otherwise the current value is read.
    coreID     Required for registers which are per core. 
    vpeID      Required for registers which are per VC.
    clusterID  Destination cluster, defaults to 0.
    gstID      Guest identifier, defaults to 0.
    ========== ============================================================================
    
    '''
    try:
        check_is_wrapped_dbu(device)
        dev = device.da.rb_accessor
    except DBUDeviceError:
        dev = get_rb_accessor(device)
    
    if register is None:
        print "RB registers available:"
        for item in sorted(rb_registers):
            print item
        return
    
    try:
        reg = rb_registers[register.lower()]
    except KeyError:
        raise RBError("RB register '%s' not found." % register)
    else:
        destination, offset, per_core, per_vpe, read_only, is64bit, reg_type = reg
        
        if read_only and value is not None:
            raise RBError("RB register '%s' is read only." % register)

        if per_vpe and (coreID is None or vpeID is None):
            raise RBError("RB register '%s' requires a core ID and vpe ID." % register)
        
        if (destination == 'core' or per_core) and coreID is None:
            raise RBError("RB register '%s' requires a core ID." % register)
        
        if coreID is None:
            coreID = 0
        if vpeID is None:
            vpeID = 0
        
        #DRSEG uses the core number as its destination
        if destination == 'core':
            destination = coreID
            
        if value is None:
            #RB read
            value = dev.read(destination, coreID, vpeID, offset, is64bit, clusterId=clusterID, gstId=gstID)
            
            if reg_type is not None:
                value = reg_type(value)
            return value
        else:
            #RB Write 
            dev.write(destination, coreID, vpeID, offset, is64bit, value, clusterId=clusterID, gstId=gstID)

class FakeDBUTap(object):
    def __init__(self, device, registers):
        self.device = device
        
        def tap_accessor(ir, width):
            def f(val):
                from imgtec.console.scan import devtap
                return devtap(ir, width, val, device=device)
            return f
            
        for reg, ir, width, in registers:
            setattr(self, reg, tap_accessor(ir, width))
            
def get_dmxseg_acc(device):
    return DMXSEGAccessor(FakeDBUTap(device, 
        [('dxaddr', 0xB, 24), ('dxdata', 0xC, 66),]), 
        should_read_control=False)
            
@command()
def dmxsegwrite(addr, value, size, verify=False, device=None):
    '''
    Write to an address in dmxseg. 
    Address masking/address alignment, data alignment is done automatically. 
    Set verify to True to check the result with a dmxseg read.
    '''
    try:
        check_is_wrapped_dbu(device)
        device.da.dmxsegwrite(addr, value, size, verify)
    except DBUDeviceError:
        return get_dmxseg_acc(device).write(addr, value, size)
        
@command()
def dmxsegread(addr, size, device=None):
    '''
    Read from an address in dmxseg memory. 
    Address masking/address alignment, data alignment is done automatically.
    '''
    try:
        check_is_wrapped_dbu(device)
        return device.da.dmxsegread(addr, size)
    except DBUDeviceError:
        return get_dmxseg_acc(device).read(addr, size)

@command()
def dbuglobalthrottle(value=None, device=None):
    '''
    Set or get the value of JTAG global throttle for a DBU target.
    '''
    try:
        check_is_wrapped_dbu(device)
    except DBUError:
        from imgtec.console.scan import tapreg
        if value is not None:
            #Set via tapreg
            ctrl = tapreg('control')._replace(gt=value)
            tapreg('control', value=ctrl)
        else:
            return bool(tapreg('control').gt)
    else:
        if value is not None:
            device.da.set_global_throttle(value)
        else:
            return device.da.get_global_throttle()
    
@command()
def dbustep(single=True, address=None, verbose=True, device=None):
    '''
    Keep clearing PrAcc, if verbose print control and rb header. 
    If single is True return after clearing PrAcc once, if address is set 
    return only when that address is fetched.
    '''
    check_is_wrapped_dbu(device)
    dmseg_dbu(None, verbose, False, 'mips64r6+msa', device, single=single, address=address)
    
@command()
def dbutimeouts(dmxseg_read=None, dmxseg_write=None, rb_valid=None, device=None):
    '''
    Change or view existing value of DBU operation timeouts. 
    Values in seconds, values of None are not set and return the current value.
    '''
    check_is_wrapped_dbu(device)
    return device.da.SetTimeouts(dmxseg_read=dmxseg_read, dmxseg_write=dmxseg_write,
        rb_valid=rb_valid)
        
def dmseg_dbu(mem, verbose, issue_ejtagboot, isa, device, single=False, address=None):
    """
    See DMSEG in scan.py
    """
    core_number = device.da.CoreNumber()
    vc_number   = device.da.VpeNumber()
    is_stepping = single or address is not None
    
    def log(msg):
        if verbose > 1:
            print msg
    
    if issue_ejtagboot:
        t = rbreg('vc_control_2', coreID=core_number, vpeID=vc_number)
        t._replace(bootmode=1)
        rbreg('vc_control_2', coreID=core_number, vpeID=vc_number, value=t)
        
    tries = 10
    i = 0
    servicedDEV = False
    addr = None
    
    while i < tries:
        control= Control(device.da.readDbuControl())
        
        log("Control: ")
        log(repr(control))
            
        if check_rocc(core_number, device):
            pass
        elif control.pracc:
            if i > 1 and verbose:
                print "no access pending for %d read(s) of EJTAG Control register." % (i - 1,)
                
            rb_header = RBHeader(device.da.rbheader())
            addr = rb_header.addr
            
            log("RB Header:")
            log(repr(rb_header))
            
            if rb_header.core_id != core_number:
                raise DBUError('Core ID of rb header (%d) does not match expected core ID (%d)' % (rb_header.core_id, core_number))
            if rb_header.vpe_id != vc_number:
                raise DBUError('VC of rb header (%d) does not match expected VC (%d)' % (rb_header.vpe_id, vc_number))
            
            if servicedDEV and (addr == 0x200):
                break # Stop processing accesses on second access to 0x200.
            else:
                servicedDEV = True
                
                if rb_header.mcmd == 1: # write
                    rbpayload = device.da.rbpayload()
                    log("RBPAYLOAD:")
                    log(hex(rbpayload))
                    
                    if not is_stepping:
                        #Read back what was written
                        data = rbpayload
                        
                        #For 1 & 2 the lower 32 bits are valid (as opposed to upper/lower for dxdata)
                        if rb_header.wordenable == 1 or rb_header.wordenable == 2:
                            #lower word only
                            mem.store_value( addr + 0xff200000, data & MASK_32_BIT, verbose)
                        elif rb_header.wordenable == 3:
                            #both words
                            mem.store_value( addr + 0xff200000, data & MASK_32_BIT, verbose)
                            mem.store_value( addr + 0xff200004, (data >> 32) & MASK_32_BIT, verbose)
                        else:
                            raise DBUError("Unknown word enable (%d)" % rb_header.wordenable)
                    
                elif rb_header.mcmd == 2:
                    
                    if not is_stepping:
                        if rb_header.wordenable == 1:
                            #lower word only
                            value = mem.fetch_value( addr + 0xff200000, verbose)
                            sz = 32
                        elif rb_header.wordenable == 2:
                            #upper word only
                            value = mem.fetch_value( addr + 0xff200000, verbose)
                            sz = 32
                        elif rb_header.wordenable == 3:
                            #both words
                            value1 = mem.fetch_value( addr + 0xff200000, verbose)
                            value2 = mem.fetch_value( addr + 0xff200004, verbose)
                            value = value2 << 32 | value1
                            sz = 64
                        else:
                            raise DBUError("Unknown word enable (%d)" % rb_header.wordenable)
                        
                        dmxsegwrite(addr, value, sz, verify=False, device=device) 
                else:
                    raise DBUError('Unsupported mcmd command (%d)' % rb_header.mcmd)
                
                #Clear PrAcc
                device.da.control(control._replace(pracc=0))
                
                #Check for reset
                if check_rocc(core_number, device):
                    pass
                else:
                    i = 0
                    
                log("------------------------------------------------")
                
            if single and address is None:
                break

            if address and ((addr+DMXSEG_BEGIN) == address):
                print "Hit address 0x%x" % address
                break
                
        i += 1

    if i >= tries:
        if verbose:
            print "No processor access to dmseg seen in last %d reads of the EJTAG Control register <done>." % (tries,)
    else:
        if is_stepping:
            if addr is not None and verbose:
                print ' '.join([repr(dasm(addr+DMXSEG_BEGIN, isa=isa, count=1, device=device)), str(get_symbols_string(device, addr+DMXSEG_BEGIN))])
        else:
            print "Second access seen to debug exception vector <done>."
            
    if not is_stepping:
        return mem.results 

def check_rocc(core_num, device):
    roccmask = device.da.read_rocc_mask()
    if roccmask & (core_num + 1): # Cores start from 0
        print "Target reset detected (roccmask: 0x%08x) continuing..." % (long(roccmask))
        device.da.clear_rocc_mask()
        roccmask = device.da.read_rocc_mask()
        return True
        
    return False
    
identifier_prefix = 'DBU'
    
@register_connector(identifier_prefix, re.IGNORECASE)
def connector(identifier, _options):
    kwargs = {}
    m = re.match(r'\s*(?:(\d+)|([^:]*)(?::(\d+))?)', identifier[len(identifier_prefix):])
    if not m:
        raise RuntimeError('Bad identifier for %s. Format should be %s[ host][:][port]', 
                    identifier_prefix, identifier_prefix)
        
    port = m and m.group(1) or m.group(3)
    if m and m.group(2):
        kwargs['hostname'] = m.group(2)
    if port:
        kwargs['port'] = int(port)
    return DBUDevice(SocketDriver(**kwargs))
    
da_identifier_prefix = identifier_prefix+ ' DA-net'
@register_connector(da_identifier_prefix, re.IGNORECASE)
def connector(identifier, options):
    m = re.match(r'.*DA-net\s(\d+)', identifier)
    if not m:
        raise RuntimeError('Bad identifier for %s. Format should be %s [da number]' %
                    (da_identifier_prefix, da_identifier_prefix))
                    
    da_num = m.group(1)
    from imgtec.codescape.tiny import ConnectProbe
    dbudriver = ConnectProbe("DA-net " + da_num, options)
   
    return DBUDevice(dbudriver)
    
sysp_identifier_prefix = identifier_prefix + ' sysprobe'
@register_connector(sysp_identifier_prefix, re.IGNORECASE)
def connector(identifier, options):
    m = re.match(r'.*[sysprobe]\s(.*)', identifier)
    if not m:
        raise RuntimeError('Bad identifier for %s. Format should be %s [sysprobe identifier]' %
                    (sysp_identifier_prefix, sysp_identifier_prefix))
    
    sysp_num = m.group(1)
    from imgtec.codescape.tiny import ConnectProbe
    dbudriver = ConnectProbe("sysprobe " + sysp_num, options)
    dev = DBUDevice(dbudriver) 
    dev.da.DAReset()
    return dev
    
if __name__ == '__main__':
    test.main()