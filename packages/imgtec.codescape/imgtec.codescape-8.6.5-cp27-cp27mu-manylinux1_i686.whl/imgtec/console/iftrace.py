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

from imgtec.console import *
from imgtec.console import trace
from imgtec.console.support import *
from imgtec.console.memory import MemoryResult
from imgtec.console.regs import *
from imgtec.console.trace import RegisterField, IDFilterWithValid
from imgtec.lib.namedbitfield import namedbitfield
from imgtec.lib.ordered_dict import OrderedDict
from imgtec.console.generic_device import *
from imgtec.lib import rst


from imgtec.console.support import command
from imgtec.console import results

# Offsets from base of TMI registers (read from drseg)
TMI_BASE = 0    # Start of trace memory
TMI_WRP  = 4    # Write pointer where next trace word will be written. If bit 0 set then buffer has wrapped
TMI_CFG  = 8    # Configuration register

drseg_tmi = 'ejtag_0008_32'

TCB_ifctl = namedbitfield('TCB_ifctl', '''\
    Illegal   31
    OfClkExt  30 29
    ExtASID  28 27
    ASID  26 19
    ASIDValid  18
    IF_VER  17 16
    FDT_CAUSE  15
    CYC  14
    FDT  13
    BM   12
    ER   11
    FCR  10
    EST   9
    SyP  8 5
    OfClk 4
    OfC 3
    IO 2
    En 1
    On 0''')

TCB_ifctl2 = namedbitfield('TCB_ifctl2', '''\
    _ 31 12
    DeltaCycle_Divide 11 10
    UTM_En 9
    GuestID 8 1
    GValid 0
    ''')


def has_tmi(device):
    # TODO : Need a good way of determining this 
    info = cpuinfo(device)
    prid = info['prid']
    company = (prid >> 16) & 0xff
    prid = (prid >> 8) & 0xff
    return company == 1 and prid == 0xb1
    

def is_version1(device):
    ifctl = TCB_ifctl(device.tiny.ReadRegisters(['ejtag_drseg_itcb_cs'])[0])
    orig_ifctl = ifctl
    ifctl = ifctl._replace(EST = 1)
    device.tiny.WriteRegisters(['ejtag_drseg_itcb_cs'], [ifctl])
    ifctl = TCB_ifctl(device.tiny.ReadRegisters(['ejtag_drseg_itcb_cs'])[0])
    device.tiny.WriteRegisters(['ejtag_drseg_itcb_cs'], [orig_ifctl])
    return ifctl.EST == 0

def determine_version(ifctl, device):
    if is_version1(device):
        return 1
    return ((ifctl >> 16) & 3) + 2    

def make_memory_accessible(addr):
    if addr < 0x20000000:
        addr |= 0xa0000000
        
    return addr

def read_tmi_reg(device):
    tmi = word(0xff300010, type = 1)
    return make_memory_accessible(tmi)
        

def GetGuestIDBitWidth(device, Config3):
    with device:
        guestIDBitCount = 0
        VZ = 1 << 23
        if (Config3 & VZ) == VZ:
            guestCtrl = regs('cp0.10.4')
            modguest = guestCtrl | 0xff
            regs('cp0.10.4', modguest)
            modguest = regs('cp0.10.4') & 0xff
            for i in range(0, 8):
                if (modguest & (1 << i)) != 0:
                    guestIDBitCount += 1
            regs('cp0.10.4', guestCtrl)
        return guestIDBitCount

def zero_wrp(device):
    if has_tmi(device):
        tmi = read_tmi_reg(device) #device.tiny.ReadRegisters([drseg_tmi])[0]
        base = word(tmi + TMI_BASE)
        word(tmi + TMI_WRP, base)
    else:
        device.tiny.WriteRegisters(["ejtag_drseg_itcb_wrp"], [0])

class IFTraceMode(trace.TraceModeBase):
    renames   = dict(gvalid='guestfilter', guestid='guestfilter', g='asidfilter', asid='asidfilter')
    
    on = RegisterField('on', default=1, valid='1|0', fields=['ifctl.On'], requires=[],
        doc='Turn on trace for this core')
    io = RegisterField('io', default=1, valid='1|0', fields=['ifctl.IO'], requires=[],
        doc='Enable/disable inhibit overflow e.g tracemode(io=0) turns it off.')
    fcr = RegisterField('fcr', default=0, valid='1|0', fields=['ifctl.FCR'], requires=[],
        doc='Enable/disable tracing of all function call and returns, requires est=1.', version=2)
    offchip = RegisterField('offchip', default=0, valid='1|0', fields=['ifctl.OfC'], requires=[],
        doc='Specify where trace data is sent when both onchip and offchip are available.')
    syp = RegisterField('syp', default=0, valid='n', fields=['ifctl.SyP'], requires=[],
        doc="Specify sync mode period (see Programmer's Guide for values).", version=2)
    cr = RegisterField('cr', default=0, valid='0-7', fields=['ifctl.OfClk', 'ifctl.OfClkExt'], requires=[],
        doc='Set the off chip clock ratio.')
    est = RegisterField('est', default=0, valid='1|0', fields=['ifctl.EST'], requires=[],
        doc='Enable/disable special trace modes.', version=2)
    dc = RegisterField('dc', default=0, valid='1|0', fields=['ifctl.CYC'], requires=[],
        doc='Enable/disable tracing of delta cycles, requires est=1.', version=2)
    fdt = RegisterField('fdt', default=0, valid='1|0', fields=['ifctl.FDT'], requires=[],
        doc='Enable/disable filtered data trace mode, requires est=1.', version=2)
    bm = RegisterField('bm', default=0, valid='1|0', fields=['ifctl.BM'], requires=[],
        doc='Enable/disable breakpoint match mode.', version=2)
    ecr = RegisterField('ecr', default=0, valid='1|0', fields=['ifctl.ER'], requires=[],
        doc='Enable/disable tracing of exceptions and returns, requires est=1.', version=2)
    efdt = RegisterField('efdt', default=0, valid='1|0', fields=['ifctl.FDT_CAUSE'], requires=[],
        doc='Enable/disable extended filtered data trace mode, requires est=1.', version=2)
    utm = RegisterField('utm', default=1, valid='1|0', fields=['ifctl2.UTM_En'], requires=[],
        doc='Enable/disable trace of user trace messages.', version=3)
    asidfilter = IDFilterWithValid('asidfilter', default=None, valid='None|x', fields=['ifctl.ASIDValid', 'ifctl.ASID', 'ifctl.ExtASID'], requires=[],
        doc='Specify which ASID/process to trace, None means all, 0-x specify asid.', version=3)
    guestfilter = IDFilterWithValid('guestfilter', default=None, valid='None|x', fields=['ifctl2.GValid', 'ifctl2.GuestID'], requires=[],
        doc='Specify which guestid to trace. None means all, 0-x specify guest id.', version=3)
    dc_divide = RegisterField('dc_divide', default=0, valid='x', fields=['ifctl2.DeltaCycle_Divide'], requires=[],
        doc='Set the value of the delta cycle divider (if available).', version=3)
        
    def __init__(self, ifctl, ifctl2, version):
        self._ifctl = TCB_ifctl(ifctl)
        self._ifctl2 = TCB_ifctl2(ifctl2)
        self.trace_version = version
        
    def set_reg_field(self, regname, field, value):
        write = {field : value}
        setattr(self, '_' + regname, getattr(self, '_' + regname)._replace(**write))
        
    def get_reg_type(self, regname):
        return type(getattr(self, '_' + regname))
        
    def get_reg_field(self, regname, field):
        return getattr(getattr(self, '_' + regname), field)
        
    def write(self, device):
        with device:
            if self._ifctl.IF_VER != 0:
                regs("ejtag_drseg_itcb_cs2", self._ifctl2, device=device)
            regs("ejtag_drseg_itcb_cs", self._ifctl, device=device)
        
    def is_offchip_trace(self, device):
        return self.get_reg_field('ifctl', 'OfC') != 0

    @classmethod
    def read(cls, device):
        with device:
            ifctl = TCB_ifctl(regs("ejtag_drseg_itcb_cs", device=device))
            if ifctl.IF_VER != 0:
                ifctl2 = TCB_ifctl2(regs("ejtag_drseg_itcb_cs2", device=device))
            else:
                ifctl2 = TCB_ifctl2()
            version = determine_version(ifctl, device)
        return cls(ifctl, ifctl2, version)
        
    def config(self, read_perfs, device):
        with device:
            lines = []
            core = device if isinstance(device, Core) else device.core
            core_index = core.index
            targdata = targetdata(device=device)
            table = targdata.socs[core.soc.index].cores[core_index]
            Config = table.config[0]
            Config1 = table.config[1]
            Config3 = table.config[3]
            Config4 = table.config[4]
            Config5 = table.config[5]
            Config7 = table.config[7]
            PRId = table.prid
            tcbsys = 0
            if read_perfs:
                tcbsys = device.tiny.ReadRegisters(['gcr_db_tcbsys'])[0]
            lines.append("[section 1]" )
            lines.append("VERSION=4.0" )
            lines.append("Core=0") # TODO << m_pMIPS->CommsInfo().core.core_index )
            lines.append("TCBCONTROLA=0x%08x" % long(0))
            lines.append("TCBCONTROLB=0x%08x" % long(0))
            lines.append("TCBCONTROLC=0x%08x" % long(0))
            lines.append("TCBCONTROLD=0x%08x" % long(0))
            lines.append("TCBCONTROLE=0x%08x" % long(0))
            lines.append("TCBCONFIG=0x%08x" % long(0))
            lines.append("CONFIG=0x%08x" % long(Config))
            lines.append("CONFIG1=0x%08x" % long(Config1))
            lines.append("CONFIG3=0x%08x" % long(Config3))
            lines.append("CONFIG4=0x%08x" % long(Config4))
            lines.append("CONFIG5=0x%08x" % long(Config5))
            lines.append("CONFIG7=0x%08x" % long(Config7))
            lines.append("PRID=0x%08x" % long(PRId))
            lines.append("IFCTL=0x%08x" % self._ifctl)
            lines.append("IFCTL2=0x%08x" % self._ifctl2)
            lines.append("TCBSYS=0x%08x" % tcbsys)
            lines.append("guestIDBitWidth=0x%08x" % GetGuestIDBitWidth(device, Config3))
            lines.append("[section 2]")
            lines.append("[section 3]")
            return '\n'.join(lines)

    
    @classmethod
    def start_trace(cls, cores, offchip_mode = None, offchip_size = 0, imon = False, path = None):
        device = cores[0]
        mode = cls.read(device)            
        if mode.is_offchip_trace(device):
            if offchip_mode is None:
                offchip_mode = 'circular_buffer'
            caps = device.probe.probe_info
            if not caps.get('has_iflowtrace_connector', False):
                raise RuntimeError('Probe does not support offchip iFlowtrace.')

            trace.start_offchip_trace(device, offchip_mode, offchip_size, path)
        elif offchip_mode or offchip_size or imon:
            msg = 'offchip_mode' if offchip_mode else 'offchip_size' if offchip_size else 'imon'
            raise  RuntimeError('%s is only valid when tracing offchip' % (msg))
        
        for device in cores:
            zero_wrp(device)
            mode = cls.read(device)
            on = mode.get_reg_field('ifctl', 'On')
            mode.set_reg_field('ifctl', 'On', 1)
            if on:
                mode.set_reg_field('ifctl', 'En', 1)
                
            mode.write(device)

        
    @classmethod
    def stop_trace(cls, cores):
        for device in cores:
            mode = cls.read(device)
            on = mode.get_reg_field('ifctl', 'On')
            mode.set_reg_field('ifctl', 'On', 0)
            mode.set_reg_field('ifctl', 'En', 0)
            mode.write(device)
            mode.set_reg_field('ifctl', 'On', on)
            mode.write(device)

            if mode.is_offchip_trace(device):
                device.tiny.ConfigureTrace('stop_trace', 'trace_only', 0, 5511)
                status, count = device.tiny.PollTrace()


def max_trace_entries(device, twsize):
    if has_tmi(device):
        tmi = read_tmi_reg(device) #device.tiny.ReadRegisters([drseg_tmi])[0]
        cfg = word(tmi + TMI_CFG)
        max_bit = cfg & 0x1f
        num_entries = 1 << (max_bit + 1)
    else:
        rdp = regs("ejtag_drseg_itcb_rdp", device = device)
        regs("ejtag_drseg_itcb_rdp", 0x7fffffff, device = device)
        max_rd = regs("ejtag_drseg_itcb_rdp", device = device)
        num_entries = max_rd        
        if max_rd:
            num_entries += 8 
        regs("ejtag_drseg_itcb_rdp", rdp, device = device)
    return num_entries / (8 * twsize)


class IFlowTraceReader(trace.TraceReaderBase):
        
    def init_rdp(self):    
        if has_tmi(device):
            tmi = read_tmi_reg(device) #device.tiny.ReadRegisters([drseg_tmi])[0]
            wrp = word(tmi + TMI_WRP)
            base = word(tmi + TMI_BASE)
            if (wrp & 1) != 0:
                wrp &= ~1
                wrp -= base
            else:
                wrp = 0
        else:
            wrp = regs("ejtag_drseg_itcb_wrp", device = self.device)
            offset = self.start_frame * self.twsize * 8
            wrp = (wrp + offset )& 0x7fffffff if wrp & 0x80000000 else offset
            regs("ejtag_drseg_itcb_rdp", wrp, device = self.device)
    
        return wrp
    
    def read(self, num_to_read):

        if has_tmi(device):
            if self.num_read == 0:
                self.rdp = self.init_rdp()
            num_left = self.max_entries - self.num_read
            num_to_read = min(num_left, num_to_read)
            
            tmi = read_tmi_reg(device) #device.tiny.ReadRegisters([drseg_tmi])[0]
            addr_base = make_memory_accessible(word(tmi + TMI_BASE))
            data = []
            last_addr = max_trace_entries(self.device, 1) * 8
            
            while num_to_read > 0:
                wrap_amount = last_addr - self.rdp
                wrap_amount /= self.twsize * 8
                this_read = min(num_to_read, 512)
                this_read = min(wrap_amount, this_read)
                offset = self.rdp
                trace = doubleword(addr_base + offset, count=this_read * self.twsize, device = self.device)
                data += trace
                num_to_read -= this_read
                self.num_read += this_read
                self.rdp += this_read * self.twsize * 8
                if self.rdp == last_addr:
                    self.rdp = 0
             
            return data, []   
        else:
            return super(IFlowTraceReader, self).read(num_to_read)

powers = [2**n for n in range(4, 32)]

def find_power_of2(size):
    try:
        return powers.index(size)
    except:
        raise ValueError('Memory size must be a power of 2')

def tracemem_overlaps_regs(tmi, size, device):
    base = make_memory_accessible(word(tmi + TMI_BASE))
    return base <= tmi < base + size
    
class IFTrace(trace.TraceBase):
    TraceMode = IFTraceMode
    
    def is_offchip_trace(self, device):
        mode = self.tracemode(device)
        return mode.get_reg_field('ifctl', 'OfC') != 0
            
    def traceentries(self, device, twsize):
        '''Discover how many trace entries are pending.'''
        with device:
            # If we are in offchip mode need to ask the probe
            if self.is_offchip_trace(device):
                return trace.offchip_traceentries(device, twsize)
            else:
                self.tracemode(device, off)
                if has_tmi(device):
                    tmi = read_tmi_reg(device) #device.tiny.ReadRegisters([drseg_tmi])[0]
                    base = word(tmi + TMI_BASE)
                    wrp = word(tmi + TMI_WRP) & ~int(base)
                    buffer_wrapped = wrp & 1
                else:
                    wrp = regs("ejtag_drseg_itcb_wrp", device = device)
                    buffer_wrapped = wrp & 0x80000000
                if buffer_wrapped:
                    return max_trace_entries(device, twsize)
                else:
                    return wrp / (8 * twsize)
            
        
    def traceread(self, device, start_frame, num_entries, twsize, init_rdp = True):  
        with device:
            if self.is_offchip_trace(device):
                return trace.offchip_traceread(device, start_frame, num_entries, twsize)
            else:
                max_entries = self.traceentries(device, twsize)
                if not num_entries:
                    num_entries =  max_entries
                num_entries = min(num_entries, max_entries)
                reader = IFlowTraceReader(device, start_frame, num_entries, twsize)
                return reader
            
    def tcbrev(self, device):
        ifctl = regs("ejtag_drseg_itcb_cs", device=device)
        # Need to check for V1 first 
        return 2 + ((ifctl >> 16) & 3)   
        
    def tracememsize(self, size, device):
        if has_tmi(device):
            tmi = read_tmi_reg(device)
            if size is not None:
                size = parse_memblock_size(size)
                if tracemem_overlaps_regs(tmi, size, device):
                    raise RuntimeError('Trace buffer size too large for this device.')
                mask = find_power_of2(size) + 3
                cfg = word(tmi + TMI_CFG)
                cfg &= ~0x1f
                cfg |= (mask & 0x1f)
                word(tmi + TMI_CFG, cfg)
            return 8 * max_trace_entries(device, 1)
        elif size is None:
            return 8 * max_trace_entries(device, 1)
        else:
            raise RuntimeError('This device has a fixed trace buffer size.')
    
  
                   