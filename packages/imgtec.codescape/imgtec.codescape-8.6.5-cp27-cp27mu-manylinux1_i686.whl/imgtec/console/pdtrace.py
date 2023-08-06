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

from imgtec.console import cpuinfo, compile_fields, regs, runstate, Core, targetdata, config
from imgtec.console.support import command
from imgtec.console.support import *
from imgtec.console.scan import (TCBControlAValue, TCBControlBValue, 
                    TCBControlCValue, TCBControlDValue, TCBControlEValue)
from imgtec.console.memory import MemoryResult
from imgtec.console.mt import tcactive, iterate_tcs
from imgtec.console.regs import _calculate_rmw_value
from imgtec.console.trace import TraceModeArgument, RegisterField, IDFilterWithValid, get_trace_master, find_cm_device
from imgtec.console import results
from imgtec.console import trace
from imgtec.codescape.da_types import Status
from imgtec.lib.namedbitfield import namedbitfield
from imgtec.lib.ordered_dict import OrderedDict
from imgtec.lib import rst
import threading
import time


def is_oci(device):
    
    try:
        info = cpuinfo(device)
        prid = info.get('prid')
        c = (prid >> 16) & 0xff
        p = (prid >> 8) & 0xff
        return c == 0x01 and p == 0xb0
    except:
        return False

TCBSysValue = namedbitfield('TCBSysValue', compile_fields('''\
        STA         31
        UsrCtl      30 0'''.splitlines()))    

STUserValue = namedbitfield('TCBSysValue', compile_fields('''\
        UsrCtl      31 0'''.splitlines()))    

PMCtrlValue = namedbitfield('PMCtrlValue', compile_fields('''\
        PERFC_TC_DELAY   10 1
        PERFC_TC_EN      0'''.splitlines()))    

STControlValue = namedbitfield('STControlValue', compile_fields('''\
        _         31 1
        ST_En     0'''.splitlines()))
    
TCBControlA = 'ejtag_tcbcontrola'
TCBControlB = 'ejtag_tcbcontrolb'
TCBControlC = 'ejtag_tcbcontrolc'
TCBControlD = 'ejtag_tcbcontrold'
TCBControlE = 'ejtag_tcbcontrole'
TCBConfig   = 'ejtag_tcbconfig'
TCBData = 'ejtag_tcbdata'
TCBwrp  = 'ejtag_tcbwrp'
TCBrdp  = 'ejtag_tcbrdp'
TCBSys = 'gcr_db_tcbsys'

DrsegTCBControlA = 'drseg_tcbcontrola'
DrsegTCBControlB = 'drseg_tcbcontrolb'
DrsegTCBControlC = 'drseg_tcbcontrolc'
DrsegTCBControlD = 'drseg_tcbcontrold'    # Note this is a hack for now, needs replacing with the real reg
DrsegTCBControlE = 'drseg_tcbcontrole' 
DrsegTCBConfig   = 'drseg_tcbconfig'
DrsegTCBData     = ''
DrsegTCBwrp      = 'dbu_tf_writeptr'
DrsegTCBrdp      = 'dbu_tf_readptr'
TF_Control       = 'dbu_tf_control'
TF_Config        = 'dbu_tf_config'
PMCtrl           = 'gcr_db_tcbperfcntr'
STControl        = 'dbu_tf_stcontrol'

# 'addresses' in mem type 31 for tcb register access on DA-net and old sysprobe
tcbreg_indexes = {
TCBControlA : 0x10,
TCBControlB : 0x11,
TCBControlC : 0x13,
TCBControlD : 0x15,
TCBControlE : 0x16,
TCBData : 0x12,
}
tcbdatareg_indexes = {
TCBConfig : 0,
TCBrdp  : 5,
TCBwrp  : 6,
}
# Memory types
TCB_CONTROL = 31
TCB_DATA = 32

TCBConfigValue = namedbitfield('TCBConfigValue', '''\
    CF1   31
    Impl  30 25
    TRIG  24 21
    SZ  20 17
    CRMax  16 14
    CRMin  13 11
    PW  10 9
    PiN  8 6
    OnT  5
    OfT  4
    REV  3 0''')

TF_ControlValue = namedbitfield( 'TF_ControlValue', '''\
    WE 31
    STCE 20
    IDLE 19
    TL 18
    TO 17
    RM 16
    TR 15
    BF 14
    TM 9 8
    CR 7 5
    Cal 4
    PIB_MCP 2
    OfC 1
    EN 0'''
)

TF_ConfigValue = namedbitfield( 'TF_ConfigValue', '''\
    TAG_B 25 24
    SRC_B 22 21
    SZ    20 17
    CRMAX 14 12
    CRMIN 10 8
    PW    7 6
    OnT   5
    OfT   4
    REV   3 0'''
)

tcbregtypes = {TCBControlA : (TCBControlAValue),
    TCBControlB : (TCBControlBValue),
    TCBControlC : (TCBControlCValue),
    TCBControlD : (TCBControlDValue),
    TCBControlE : (TCBControlEValue),
    TCBData : (lambda x: results.IntResult(x, size = 32//8)),
    TCBrdp : (lambda x: results.IntResult(x, size = 32//8)),
    TCBwrp : (lambda x: results.IntResult(x, size = 32//8)),
    TCBConfig : (TCBConfigValue),
    TCBSys : (TCBSysValue),
    DrsegTCBControlA : (TCBControlAValue),
    DrsegTCBControlB : (TCBControlBValue),
    DrsegTCBControlC : (TCBControlCValue),
    DrsegTCBControlD : (TCBControlDValue),
    DrsegTCBControlE : (TCBControlEValue),
    DrsegTCBConfig   : (TCBConfigValue),
    DrsegTCBData     : (lambda x: results.IntResult(x, size = 32//8)),
    DrsegTCBwrp      : (lambda x: results.IntResult(x, size = 32//8)),
    DrsegTCBrdp      : (lambda x: results.IntResult(x, size = 32//8)),
    TF_Control       : (TF_ControlValue),
    TF_Config        : (TF_ConfigValue),
    'gcr_db_tcbcontrold' : (TCBControlDValue),
    'dbu_tf_stuser'  : (STUserValue),
    }

perf_regs = ['perfctl0', 'perfctl1', 'perfctl2', 'perfctl3']

class TCBDataRegs(object):
    def read(self, device, names):
        raise NotImplementedError()
    def write(self, device, names, values):
        raise NotImplementedError()
    def read_mod_write(self, device, name, new_value, modify_mask):
        old = self.read(device, [name])[0]
        value = (old & ~modify_mask) | (new_value & modify_mask)
        self.write(device, [name], [value])

class TCBDataRegsViaMemory(TCBDataRegs):
    def read(self, device, names):
        return [self._read(device, name) for name in names]
            
    def _read(self, device, name):
        if name in tcbdatareg_indexes:
            index = tcbreg_indexes[TCBControlB]
            b = device.tiny.ReadMemoryBlock(index * 4, 1, 4, TCB_CONTROL)[0]
            b = TCBControlBValue(b)
            value = b._replace(WE=1, REG=tcbdatareg_indexes[name])
            device.tiny.WriteMemoryBlock(index * 4, 1, 4, [int(value)], TCB_CONTROL)
            name = TCBData  # now that tcbcontrolb is configured the value we want is in tcbdata
        index = tcbreg_indexes[name]
        return device.tiny.ReadMemoryBlock(index * 4, 1, 4, TCB_CONTROL)[0]
        
    def write(self, device, names, values):
        for name, value in zip(names, values):
            self._write(device, name, value)
        
    def _write(self, device, name, value):
        if name in tcbdatareg_indexes:
            raise NotImplementedError('writing of tcbdata regs not implemented yet')
        index = tcbreg_indexes[name]        
        device.tiny.WriteMemoryBlock(index * 4, 1, 4, [int(value)], TCB_CONTROL)
        
class TCBDataRegsViaNamedRegisters(TCBDataRegs):
    def read(self, device, names):
        return device.tiny.ReadRegisters(names)
    def write(self, device, names, values):
        device.tiny.WriteRegisters(names, values)
    def read_mod_write(self, device, name, new_value, modify_mask):
        device.tiny.ReadModWriteRegister(name, new_value, modify_mask)

def get_tcbdataregs_accessor(device):
    if int(device.probe.probe_info.get('tcbdataregs', '0')):
        return TCBDataRegsViaNamedRegisters()
    else:
        return TCBDataRegsViaMemory()
        
def _get_register_type(name):
    try:
        return tcbregtypes[name]
    except KeyError:
        raise RuntimeError("Unknown register name %s" % (name,))

mdh_names = {TCBControlA : 'drseg_tcbcontrola',
             TCBControlB : 'drseg_tcbcontrolb',
             TCBControlC : 'drseg_tcbcontrolc',
             TCBControlD : 'drseg_tcbcontrold',    # Note this is a hack for now, needs replacing with the real reg
             TCBControlE : 'drseg_tcbcontrole', 
             
             TCBConfig   : 'drseg_tcbconfig',
             TCBData     : '',
             TCBwrp      : 'dbu_tf_writeptr',
             TCBrdp      : 'dbu_tf_readptr',
             'dbu_tf_control' : 'dbu_tf_control',
             TCBSys      : 'dbu_tf_stuser'

            }


def _get_mdh_name(name, device):
    if is_oci(device):
        try:
            return mdh_names[name]
        except KeyError:
            #raise RuntimeError("Unknown register %s" % (name,))
            pass
    return name
    
def _get_cm_mdh_name(name, device):
    if is_oci(device):
        if name is TCBControlB:
            return 'dbu_tf_control'
        elif name is TCBConfig:
            return 'dbu_tf_config'
        elif name is TCBControlD:
            return 'gcr_db_tcbcontrold'
        elif name is TCBSys:
            return 'dbu_tf_stuser'
    return name


def modify_names_for_device(device, names):
    if is_oci(device):
        names = [_get_mdh_name(name, device) for name in names]
    return names
        
def modify_names_for_cmdevice(device, names):
    if is_oci(device):
        names = [_get_cm_mdh_name(name, device) for name in names]
    return names

def read_tcb_register(device, name):
    return read_tcb_registers(device, [name])[0]

def _read_tcb_registers(device, names): 
    accessor = get_tcbdataregs_accessor(device)
    types = [_get_register_type(name) for name in names]
    values = accessor.read(device, names)
    return [type(val) for type, val in zip(types, values)]

def read_tcb_registers(device, names):
    names = modify_names_for_device(device, names)
    return _read_tcb_registers(device, names)

def write_tcb_registers(device, names, values):
    names = modify_names_for_device(device, names)
    accessor = get_tcbdataregs_accessor(device)
    accessor.write(device, names, values)

def mod_tcb_register(device, name, _new_value=0, _modify_mask=0, **kwargs):
    accessor = get_tcbdataregs_accessor(device)
    type = _get_register_type(name)
    _new_value, _modify_mask = _calculate_rmw_value(name, type, _new_value, _modify_mask, **kwargs)
    name = _get_mdh_name(name, device)
    #print "%s = 0x%08x" % (name, _new_value)
    accessor.read_mod_write(device, name, _new_value, _modify_mask)
    
def read_cm_tcb_register(device, name):
    cm_device = device if is_oci(device) else trace.get_trace_master(device)
    return cm_device and read_cm_tcb_registers(cm_device, [name])[0]

def read_cm_tcb_registers(device, names):
    cm_device = device if is_oci(device) else trace.get_trace_master(device)
    # Mod names for cm
    names = modify_names_for_cmdevice(device, names)
    names = modify_names_for_device(device, names)    
    return _read_tcb_registers(cm_device, names)
    
def write_cm_tcb_registers(device, names, values):
    cm_device = device if is_oci(device) else trace.get_trace_master(device)
    # Mod names for cm
    names = modify_names_for_cmdevice(device, names)
    accessor = get_tcbdataregs_accessor(device)
    accessor.write(cm_device, names, values)
    
def mod_cm_tcb_register(device, name, _new_value=0, _modify_mask=0, **kwargs):
    cm_device = device if is_oci(device) else trace.get_trace_master(device)
    # Mod names for cm
    name = _get_cm_mdh_name(name, device)
    mod_tcb_register(cm_device, name, _new_value, _modify_mask, **kwargs)
    
def get_core(device):
    if hasattr(device, 'cores'):
        if not device.cores:
            raise RuntimeError('There are no debuggable cores at present')
        return device.cores[0]
    elif hasattr(device, 'core'):
        return device.core
    else:
        return device

def iterate_vpid_tcs(device):
    info = cpuinfo(device)
    core = get_core(device)
    num_vpe = 1 if info['has_mt'] else info['num_vpe']
    num_tcs = info['num_tc']
    for vpe in range(num_vpe):
        dev = core.vpes[vpe]
        for tc in iterate_tcs(device):
            yield dev, tc
    
    
def GetGuestIDBitWidth(device, Config3):
    guestIDBitCount = 0
    VZ = 1 << 23
    if (Config3 & VZ) == VZ:
        guestCtrl = regs('cp0.10.4')
        modguest = guestCtrl | 0xff
        regs('cp0.10.4', modguest, device=device)
        modguest = regs('cp0.10.4', device=device) & 0xff
        for i in range(0, 8):
            if (modguest & (1 << i)) != 0:
                guestIDBitCount += 1
        regs('cp0.10.4', guestCtrl, device=device)
    return guestIDBitCount

cm_b_fields = ('CR', 'OfC', 'TM')

def set_tlsif(mode):
    is_one_present = mode.get_reg_field('a', 'TIM') or \
                     mode.get_reg_field('a', 'TLSM') or \
                     mode.get_reg_field('a', 'TFCR')
    mode.set_reg_field('b', 'TLSIF', int(is_one_present))

def set_pece(mode):
    mode.set_reg_field('e', 'PeCE', bool(mode.pm))
        
def tm_type(value):
    if value in ("traceto", 0):
        return 0
    elif value in ("tracefrom", 1):
        return 1
    else:
        raise RuntimeError('Unknown tracemode tm argument %s' % (value,))
        
class EnablePerfCounter(TraceModeArgument):
    def __set__(self, mode, value, type=None):
        if not hasattr(value, '__iter__'):
            value = [value]
        mode._pm = sorted(set(value))
    def __get__(self, mode, type=None):
        if mode is None: 
            return self
        return mode._pm

def check_for_idle(core):
    while read_tcb_register(core, TCBControlE).TrIDLE == 0:
        mod_tcb_register(core, TCBControlB, WE=1, EN=1)
        mod_tcb_register(core, TCBControlB, WE=1, EN=0)

#def check_for_idle_cm(core):
#    pass

def check_for_idle_cm(core):
    start = time.clock()
    while (read_cm_tcb_register(core, TCBControlB) & 0x80000) == 0:
        if is_oci(core):
            mod_cm_tcb_register(core, TCBControlB, TL=1, TO=1, WE=1, EN=1)
            mod_cm_tcb_register(core, TCBControlB, WE=1, EN=0)
        else:
            mod_cm_tcb_register(core, TCBControlB, WE=1, EN=1)
            mod_cm_tcb_register(core, TCBControlB, WE=1, EN=0)
            
        now = time.clock()
        if (now - start) > 1.0:
            break
        
   
class PDTraceMode(trace.TraceModeBase):
    renames = dict(g='asidfilter', asid='asidfilter')
   
    on = RegisterField('on', default=1, valid='1|0', fields=['a.On'], requires=[],
        doc='Turn on trace for this core')
    d = RegisterField('d', default=0, valid='1|0', fields=['a.D'], requires=[],
        doc='Enable/disable trace when the processor is in debug mode.')
    e = RegisterField('e', default=1, valid='1|0', fields=['a.E'], requires=[],
        doc='Enable/disable trace when the processor is in exception mode.')
    s = RegisterField('s', default=1, valid='1|0', fields=['a.S'], requires=[],
        doc='Enable/disable trace when the processor is in supervisor mode.')
    k = RegisterField('k', default=1, valid='1|0', fields=['a.K'], requires=[],
        doc='Enable/disable trace when the processor is in kernel mode.')
    u = RegisterField('u', default=1, valid='1|0', fields=['a.U'], requires=[],
        doc='Enable/disable trace when the processor is in user mode.')
    io = RegisterField('io', default=1, valid='1|0', fields=['a.IO'], requires=[],
        doc='Enable/disable inhibit overflow. e.g tracemode(io=0) turns it off.')
    im = RegisterField('im', default=0, valid='1|0', fields=['a.TIM'], requires=[],
        doc='Enable/disable marking of all instruction cache misses.', version=4)
    lsm = RegisterField('lsm', default=0, valid='1|0', fields=['a.TLSM'], requires=[],
        doc='Enable/disable marking of all data cache misses.', version=4)
    fcr = RegisterField('fcr', default=0, valid='1|0', fields=['a.TFCR'], requires=[],
        doc='Enable/disable marking of all function call and returns.', version=4)
    ab = RegisterField('ab', default=0, valid='1|0', fields=['a.TB'], requires=[],
        doc='Enable/disable output of pc for all branches whether needed or not.')
    ca = RegisterField('ca', default=0, valid='1|0', fields=['b.CA'], requires=[],
        doc='Enable/disable output of idle cycles.')
    offchip = RegisterField('offchip', default=0, valid='1|0', fields=['b.OfC'], requires=[],
        doc='Specify where trace data is sent when both onchip and offchip are available')
    tm = RegisterField('tm', default='traceto', type=tm_type, valid='traceto|tracefrom', fields=['b.TM'], requires=[],
        doc='Specify wrap mode, tracefrom stops when full, traceto wraps until stopped.')
    pc = RegisterField('pc', default=1, valid='1|0', fields=['c.pc'], requires=[],
        doc='Enable/disable trace of pc.', version=4)
    la = RegisterField('la', default=0, valid='1|0', fields=['c.la'], requires=[],
        doc='Enable/disable trace of load addresses.', version=4)
    sa = RegisterField('sa', default=0, valid='1|0', fields=['c.sa'], requires=[],
        doc='Enable/disable trace of store addresses.', version=4)
    ld = RegisterField('ld', default=0, valid='1|0', fields=['c.ld'], requires=[],
        doc='Enable/disable trace of loaded data.', version=4)
    sd = RegisterField('sd', default=0, valid='1|0', fields=['c.sd'], requires=[],
        doc='Enable/disable trace of stored data.', version=4)
    tc = RegisterField('tc', default=1, valid='1|0', fields=['c.MTtraceTC'], requires=[],
        doc='Specify whether a tc identifier should be output.', version=4)
    cr = RegisterField('cr', default=7, valid='0-7', fields=['b.CR'], requires=[],
        doc='Set the off chip clock ratio.')
    asidfilter = IDFilterWithValid('asidfilter', default=None, valid='None|x', fields=['!a.G', 'a.ASID', 'c.E_ASID'], requires=[],
        doc='Specify which ASID/process to trace, None means all, 0-x specify asid.')
    cpufilter = IDFilterWithValid('cpufilter', default=None, valid='None|x', fields=['c.CPUvalid', 'c.CPUid'], requires=[],
        doc='Specify which vpe to trace. None means all, 0-x specify vpe.', version=4)
    tcfilter = IDFilterWithValid('tcfilter', default=None, valid='None|x', fields=['c.TCvalid', 'c.TCnum'], requires=[],
        doc='Specify which tc to trace. None means all, 0-x specify tc.', version=4)
    syp = RegisterField('syp', default=6, valid='n', fields=['a.SyP', 'a.SyPExt'], requires=[],
        doc="Specify sync mode period (see Programmer's Guide for values).")
    fdt = RegisterField('fdt', default=0, valid='1|0', fields=['b.FDT'], requires=[],
        doc='Enable/disable filtered data trace mode.', version=6)
    pmsync = RegisterField('pmsync', default=0, valid='1|0', fields=['e.PeCSync'], requires=[],
        doc='Enable/disable performance counters trace on sync counter expiry.', version=6)
    pmbp = RegisterField('pmbp', default=0, valid='1|0', fields=['e.PeCBP'], requires=[],
        doc='Enable/disable performance counters trace on breakpoint match.', version=6)
    pmfcr = RegisterField('pmfcr', default=0, valid='1|0', fields=['e.PeCFCR'], requires=[],
        doc='Enable/disable performance counters trace on function entry or return.', version=6)
    pmovf = RegisterField('pmovf', default=0, valid='1|0', fields=['e.PeCOvf'], requires=[],
        doc='Enable/disable performance counters trace on counter overflow.', version=6)
    pm = EnablePerfCounter('pm', default=[], valid='N|[N, M, ...]', fields=[], requires=[],
        doc='Specify list of performance counters to trace. For numbering see below.', version=6)
    
    msa = RegisterField('msa', default=0, valid='1|0', fields=['e.MSA_En'], requires=[],
        doc='Enable/disable MSA load/store data trace.')
    utm = RegisterField('utm', default=1, valid='1|0', fields=['a.UTD_En'], requires=[],
        doc='Enable/disable trace of user trace data.', version=10)
    dcid = RegisterField('dcid', default=0, valid='1|0', fields=['a.CID_En'], requires=[],
        doc='Enable/disable trace of Debug Context ID.', version=10)
    mmidfilter = IDFilterWithValid('mmidfilter', default=None, valid='None|x', fields=['e.GM', 'd.MMID'], requires=[],
        doc='Specify which MMID to trace. None means all, 0-x specify MMID.', version=10)
    guestfilter = IDFilterWithValid('guestfilter', default=None, valid='None|x', fields=['e.GV', 'd.GuestID'], requires=[],
        doc='Specify which guest to trace. None means all, 0-x specify guest.')
    

    def __init__(self, a, b, c, d, e, cfg, cm_b, pm):
        self._a = a
        self._b = b
        self._c = c
        self._d = d
        self._e = e
        self._cm_b = cm_b if cm_b is not None else None
        self.pm = pm
        self.trace_version = (cfg & 7) + 3
        if self.trace_version >= 7:
            self.trace_version += 1
        
    def set_reg_field(self, regname, field, value):
        write = {field : value}
        if regname == 'b':
            write['WE'] = 1
        if field == 'OfC' and value != 0:
            reset = {'TR' : 1}
            name = '_cm_b' if self._cm_b is not None else '_b'
            setattr(self, name, getattr(self, name)._replace(**reset))
            
        if self._cm_b is not None and regname == 'b' and field in cm_b_fields:
            regname = 'cm_b'
        setattr(self, '_' + regname, getattr(self, '_' + regname)._replace(**write))
        
    def get_reg_type(self, regname):
        return type(getattr(self, '_' + regname))
            
    def get_reg_field(self, regname, field):
        if self._cm_b is not None and regname == 'b' and field in cm_b_fields:
            regname = 'cm_b'
        return getattr(getattr(self, '_' + regname), field)
        
    def write(self, device):
        set_tlsif(self)
        set_pece(self)
        core_idx = device.index
        self.set_reg_field('b', 'TWSrcVal', core_idx)
        write_tcb_registers(device, [TCBControlA, TCBControlB, TCBControlC, TCBControlD, TCBControlE], 
                                    [self._a, self._b, self._c, self._d, self._e])

        # Need to do pmc if they are supported
        if self._e.PeC:
            cnt = 0
            for vpe, tc in iterate_vpid_tcs(device):
                to_write = {}
                status = runstate(device=vpe)
                if status.status != Status.thread_offline:
                    for reg, value in zip(perf_regs, regs(perf_regs, device=vpe)):
                        value &= ~0x8000
                        if cnt not in self.pm:
                            value |= 0x8000
                        to_write[reg] = value
                        cnt += 1
                        if (value & 0x80000000) == 0:
                            break
                    if to_write:
                        regs(to_write.keys(), to_write.values(), device=vpe)
                
        if self._cm_b:
            write_cm_tcb_registers(device, [TCBControlB], [self._cm_b | 0x80000000])
            
            
    @classmethod
    def read(cls, device, read_perfs = True):
        a, b, c, d, e = read_tcb_registers(device, [TCBControlA, TCBControlB, TCBControlC, TCBControlD, TCBControlE])
        cfg = read_tcb_register(device, TCBConfig) & 0xffffffff

        pmc = set()
        if read_perfs:
            if e.PeC:
                cnt = 0
                for vpe, tc in iterate_vpid_tcs(device):
                    status = runstate(device=vpe)
                    if status.status != Status.thread_offline:
                        for value in regs(perf_regs, device=vpe):
                            if (value & 0x8000) == 0:
                                pmc.add(cnt)
                            cnt += 1
                            if (value & 0x80000000) == 0:
                                break
                    
        cm_b = read_cm_tcb_register(device, TCBControlB) if find_cm_device(device) or is_oci(device) else None
        return cls(a, b, c, d, e, cfg, cm_b, pmc)
        
    def can_trace_perfcnt(self, device):
        info = cpuinfo(device)
        return info.get('has_perf_counters') and self._e.PeC != 0
    
    def is_offchip_trace(self, device):
        return self.get_reg_field('b', 'OfC') != 0
    
    def can_fdt(self):
        fdt = self.get_reg_field('b', 'FDT')
        if fdt:
            return True
        else:
            self.set_reg_field('b', 'FDT', 1)
            can_fdt = self.get_reg_field('b', 'FDT') != 0
            self.set_reg_field('b', 'FDT', fdt)
        
    def config(self, read_perfs, device):
        cfg = ""
        this_core = get_core(device)
        for core in this_core.soc.cores:
            cfg += self.core_config(read_perfs, core)
        cm = device if is_oci(device) else find_cm_device(device)
        if cm:
            cfg += self.tm_config(device)
        return cfg
        
    def trace_enabled(self):
        return True
    
    def get_runstate(self, device):
        rstate = runstate(device=device)
        try:
            return rstate[0]
        except TypeError:
            return rstate
        
    def core_config(self, read_perfs, device):
        status = self.get_runstate(device)
        if status.status in [Status.thread_offline, Status.core_offline]:
            return ""
        try:
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
            lines.append("[section 1]" )
            if self.trace_enabled():
                if is_oci(device):
                    sdb_cfg = device.tiny.ReadRegisters(['gcr_cl_0030'])[0]
                    lines.append("VERSION=5.0")
                    lines.append("Core=%d" % (core_index,))
                    lines.append("GCR_CL_SDB_CONFIG=0x%08x" % long(sdb_cfg))
                else:
                    lines.append("VERSION=4.0")
                    lines.append("Core=%d" % (core_index,))
        
                lines.append("TCBCONTROLA=0x%08x" % (long(read_tcb_register(device, TCBControlA)) & 0xffffffff))
                lines.append("TCBCONTROLB=0x%08x" % (long(read_tcb_register(device, TCBControlB)) & 0xffffffff))
                lines.append("TCBCONTROLC=0x%08x" % (long(read_tcb_register(device, TCBControlC)) & 0xffffffff))
                lines.append("TCBCONTROLD=0x%08x" % (long(read_tcb_register(device, TCBControlD)) & 0xffffffff))
                lines.append("TCBCONTROLE=0x%08x" % (long(read_tcb_register(device, TCBControlE)) & 0xffffffff))
                tcbconfig = read_tcb_register(device, TCBConfig) & 0xffffffff
                lines.append("TCBCONFIG=0x%08x" % long(tcbconfig))
                lines.append("CONFIG=0x%08x" % long(Config))
                lines.append("CONFIG1=0x%08x" % long(Config1))
                lines.append("CONFIG3=0x%08x" % long(Config3))
                lines.append("CONFIG4=0x%08x" % long(Config4))
                lines.append("CONFIG5=0x%08x" % long(Config5))
                lines.append("CONFIG7=0x%08x" % long(Config7))
                lines.append("PRID=0x%08x" % long(PRId))
                lines.append("IFCTL=0x%08x" % 0)
                lines.append("IFCTL2=0x%08x" % 0)
                lines.append("TCBSYS=0x%08x" % read_tcb_register(device, TCBSys))
                lines.append("guestIDBitWidth=0x%08x" % GetGuestIDBitWidth(device, Config3))
        
                if read_perfs:
                    lines.append("[section 2]")
                    if self.can_trace_perfcnt(device):
                        cnt = 0
                        cnt2 = 0
                        for vpe, tc in iterate_vpid_tcs(device):
                            idx = 0
                            status = runstate(device=vpe)
                            for reg in perf_regs:
                                if status.status != Status.thread_offline:
                                    value = regs(reg, device = vpe)
                                else:
                                    value = 0    
                                str = "C%d(pm%d)%d:%d=0x%08x" % (cnt, cnt, cnt2, idx, value)
                                cnt += 1 
                                idx += 1
                                lines.append(str)
                                if (value & 0x80000000) == 0:
                                    break
                            cnt2 += 1
            else:
                if is_oci(device):
                    lines.append("VERSION=5.0")
                    lines.append("Core=%d" % (core_index,))
                    lines.append("GCR_CL_SDB_CONFIG=0x%08x" % 0)
                else:
                    lines.append("VERSION=4.0")
                    lines.append("Core=%d" % (core_index,))
        
                lines.append("TCBCONTROLA=0x%08x" % 0)
                lines.append("TCBCONTROLB=0x%08x" % 0)
                lines.append("TCBCONTROLC=0x%08x" % 0)
                lines.append("TCBCONTROLD=0x%08x" % 0)
                lines.append("TCBCONTROLE=0x%08x" % 0)
                lines.append("TCBCONFIG=0x%08x" % 0)
                lines.append("CONFIG=0x%08x" % 0)
                lines.append("CONFIG1=0x%08x" % 0)
                lines.append("CONFIG3=0x%08x" % 0)
                lines.append("CONFIG4=0x%08x" % 0)
                lines.append("CONFIG5=0x%08x" % 0)
                lines.append("CONFIG7=0x%08x" % 0)
                lines.append("PRID=0x%08x" % 0)
                lines.append("IFCTL=0x%08x" % 0)
                lines.append("IFCTL2=0x%08x" % 0)
                lines.append("TCBSYS=0x%08x" % 0)
                lines.append("guestIDBitWidth=0x%08x" % 0)
                
            lines.append('\n')
            return '\n'.join(lines)
        except:
            return ""
        
    def tm_config(self, device):
        lines = []
        version = '5.0' if is_oci(device) else '4.0'
            
        lines.append("\n[section 1]" )
        lines.append("VERSION=" + version)
        lines.append("Core=cm")
        regs_to_read = {'TCBCONTROLB' : TCBControlB,
                        'TCBCONTROLD' : TCBControlD,
                        'TCBCONTROLE' : TCBControlE,
                        'TCBCONFIG' : TCBConfig}

        keys = regs_to_read.keys()
        regnames = regs_to_read.values()
        regs = read_cm_tcb_registers(device, regnames)
        for name, value in zip(keys, regs):
            lines.append('%s=0x%08x' % (name, long(value)))

            
        if is_oci(device):
            regs_to_read = {'GCR_DB_TCBCONTROLD' : 'gcr_db_tcbcontrold', 
                            'GCR_DB_TCBCONTROLE' : 'gcr_db_tcbcontrole', 
                            'GCR_DB_TCBPERFCNTR' : 'gcr_db_tcbperfcntr',
                            'GCR_DB_PC_CTL' : 'gcr_db_pc_ctl',
                            'GCR_DB_PC_EVENT' : 'gcr_db_pc_event',
                            'GCR_DB_PC_QUAL0' : 'gcr_db_pc_qual0',
                            'GCR_DB_PC_QUAL1' : 'gcr_db_pc_qual1',
                            'GCR_SDB_CONFIG' : 'gcr_sdb_config', 
                            'GCR_CONFIG' : 'gcr_config',
                            'TFCONFIG' : 'dbu_tf_config', 
                            'TFCONTROL' : 'dbu_tf_control'}
             
            keys = regs_to_read.keys()
            regnames = regs_to_read.values()
            regs = device.tiny.ReadRegisters(regnames)
            for name, value in zip(keys, regs):
                lines.append('%s=0x%08x' % (name, value))
            

        return '\n'.join(lines)

    @classmethod
    def start_trace(cls, cores, offchip_mode = None, offchip_size = 0, imon = False, path = None):
        mode = cls.read(cores[0], False)            
        if mode.is_offchip_trace(cores[0]):
            if offchip_mode is None:
                offchip_mode = 'circular_buffer'
            caps = cores[0].probe.probe_info
            if not caps.get('has_pdtrace_connector', False):
                raise RuntimeError('Probe does not support offchip PDtrace.')            
            
            cal = config('calibrate trace')
            clk = config('trace clock')
            cr = mode.cr
            trace.validate_trace_calibrate(cal, clk, cr)
            trace.start_offchip_trace(cores[0], offchip_mode, offchip_size, path)
        elif offchip_mode or offchip_size or imon:
            msg = 'offchip_mode' if offchip_mode else 'offchip_size' if offchip_size else 'imon'
            raise  RuntimeError('%s is only valid when tracing offchip' % (msg))
        
        cm = cores[0] if is_oci(cores[0]) else find_cm_device(cores[0])
        if cm:
            mod_cm_tcb_register(cores[0], TCBControlB, WE=1, TR=1, BF=0, EN=1)
            
        for core in cores:
            #on = read_tcb_register(core, TCBControlA).On
            #mod_tcb_register(core, TCBControlA, On=1)
            on = read_tcb_register(core, TCBControlA).On
            if on:
                mod_tcb_register(core, TCBControlB, WE=1, TR=1, BF=0, EN=1)
            #mod_tcb_register(core, TCBControlA, On=1)

        
    @classmethod
    def stop_trace(cls, cores):
        for core in cores:
            on = read_tcb_register(core, TCBControlA).On
            mod_tcb_register(core, TCBControlB, WE=1, EN=0)
            if on:
                mod_tcb_register(core, TCBControlA, On=0)
            
            check_for_idle(core)
            mod_tcb_register(core, TCBControlA, On=on)
            
        cm = cores[0] if is_oci(cores[0]) else find_cm_device(cores[0])
        if cm:
            mod_cm_tcb_register(cores[0], TCBControlB, WE=1, EN=0)
            check_for_idle_cm(core)
            
        mode = cls.read(cores[0], False)
        if mode.is_offchip_trace(cores[0]):
            cores[0].tiny.ConfigureTrace('stop_trace', 'trace_only', 0, 5511)
            status, count = cores[0].tiny.PollTrace()



class PDTraceReader(trace.TraceReaderBase):
    def __init__(self, device, start_frame, num_entries, twsize):
        device = get_trace_master(device)  
        super(PDTraceReader, self).__init__(device, start_frame, num_entries, twsize)
        
    def determine_rdp(self, device):
        cm = find_cm_device(device)
        wrp, b = read_cm_tcb_registers(device, [TCBwrp, TCBControlB]) if cm else\
                            read_tcb_registers(device, [TCBwrp, TCBControlB])
        
        return wrp if b.BF else 0
        
    def init_rdp(self):
        if not is_oci(self.device):
            mod_tcb_register(self.device, TCBControlB, WE=1, RM=1)
        # Here we read the start pointer (if RM was already 1 then the above
        # will have had no effect), add in the offset and write back to the
        # read pointer
        #tcbrdp = read_tcb_registers(self.device, [TCBstp])[0]
        tcbrdp = self.determine_rdp(self.device)
        start_frame = self.start_frame
        offset = start_frame * self.twsize * 8
        tcbrdp += offset
        write_tcb_registers(self.device, [TCBrdp], [tcbrdp])
        if is_oci(self.device):
            mod_cm_tcb_register(self.device, TCBControlB, WE=1, RM=1)
            
    def endian_swap16(self, val):
        lo = val & 0xff
        hi = (val >> 8) & 0xff
        return (lo << 8) | hi
            
    def endian_swap32(self, val):
        return self.endian_swap16(val >> 16) | (self.endian_swap16(val) << 16)


    def endian_swap64(self, val):
        return self.endian_swap32(val >> 32) | (self.endian_swap32(val) << 32)

    def read(self, num_to_read):
        if not is_oci(self.device):
            return super(PDTraceReader, self).read(num_to_read)
        else:
            #return super(PDTraceReader, self).read(num_to_read)
            num_to_read = (num_to_read + 1) & ~1
            # Lock trace funnel
            
            tf_control = self.device.tiny.ReadRegisters('dbu_tf_control')[0]
            tf_control |= 0x80060000
            self.device.tiny.WriteRegisters(['dbu_tf_control'], [tf_control])

            data, imon = super(PDTraceReader, self).read(num_to_read)

            tf_control = self.device.tiny.ReadRegisters('dbu_tf_control')[0]
            tf_control &= ~0x60000
            tf_control |= 0x80020000
            self.device.tiny.WriteRegisters(['dbu_tf_control'], [tf_control])
            return data, imon

class PDTrace(trace.TraceBase):
    TraceMode = PDTraceMode
    
    def traceread(self, device, start_frame, num_entries, twsize):    
        PDTraceMode.stop_trace([device])   
        if self.is_offchip_trace(device):
            return trace.offchip_traceread(device, start_frame, num_entries, twsize)
        else:
            max_entries = self.traceentries(device, twsize)
            if not num_entries:
                num_entries =  max_entries
            num_entries = min(num_entries, max_entries)
            
            reader = PDTraceReader(device, start_frame, num_entries, twsize)
            return reader

    def read_entries(self, cm_device, device, twsize):
        # It is important to do this here as it flushes the trace buffer into
        # the trace memory. Without it entries may be lost
        #mod_tcb_register(cm_device, TCBControlA, On=0)
        cm_device = device if is_oci(device) else find_cm_device(device)
        
        if cm_device:
            mod_cm_tcb_register(device, TCBControlB, WE=1, EN=0)

        cfg, wrp, b = read_cm_tcb_registers(device, [TCBConfig, TCBwrp, TCBControlB]) if cm_device else read_tcb_registers(device, [TCBConfig, TCBwrp, TCBControlB])
        sz = 1 << (8 + cfg.SZ)
        sz = sz if b.BF else wrp
        return sz / (8 * twsize) # Entries are multiples of 64 bits dependent on target
    
    def traceentries(self, device, twsize):
        '''Discover how many trace entries are pending.'''
        if self.is_offchip_trace(device):
            return trace.offchip_traceentries(device, twsize)
        else:
            #PDTraceMode.stop_trace([device])            
            cm_device = get_trace_master(device)   
            return self.read_entries(cm_device, device, twsize)
    
    def can_disable_pctrace(self, device):
        oldmode = self.tracemode(device)
        got = self.tracemode(device, pc=0)
        self.tracemode(device, oldmode)
        return got.pc == 0
    
    def tcbrev(self, device):
        ver = read_tcb_register(device, TCBConfig).REV
        ver += 3
        if ver >= 7:
            ver += 1
            
        return ver

    def is_offchip_trace(self, device):
        mode = PDTraceMode.read(device, False)            
        return mode.get_reg_field('b', 'OfC') != 0
    
    def tracememsize(self, size, device):
        if size is None:
            cm_device = device if is_oci(device) else find_cm_device(device)
            
            cfg = read_cm_tcb_registers(device, [TCBConfig])[0] if cm_device else read_tcb_registers(device, [TCBConfig])[0]
            sz = 1 << (8 + cfg.SZ)
            return sz
        else:
            raise RuntimeError('This device has a fixed trace buffer size.')
    
class PDTraceModeCM(trace.TraceModeBase):
    wb = RegisterField('wb', default=0, valid='1|0', fields=['d.WB'], requires=[],
        doc='Turn on tracing of Coherent Writeback requests.')
    io = RegisterField('io', default=0, valid='1|0', fields=['d.IO'], requires=[],
        doc='Inhibit Overflow on CM FIFO full condition. Will stall the CM until progress can be made')
    ae = RegisterField('ae', default=0, valid='1|0', fields=['d.AE'], requires=[],
        doc='Enable address tracing for the Coherency Manager')
    tl = RegisterField('tl', default=0, valid='0-3', fields=['d.TLev'], requires=[],
        doc='See SoC documentation for values')
    en = RegisterField('en', default=0, valid='1|0', fields=['d.Core_CM_En'], requires=[],
        doc='Enable tracing for the Coherency Manager.')
    ste = RegisterField('ste', default=0, valid='1|0', fields=['d.ST_En'], requires=[],
        doc='Enable generation of system trace data.')
    stc = RegisterField('stc', default=0, valid='1|0', fields=['b.STCE'], requires=[],
        doc='Enable capture of system trace data.')
    tcbsys = RegisterField('tcbsys', default=0, valid='x', fields=['s.UsrCtl'], requires=[],
        doc='Write the value to the TCBSYS register.')
    cmp0ctl = RegisterField('cmp0ctl', default=0, valid='x', fields=['d.P0_CTL'], requires=[],
        doc='Provides control over tracing transactions on Port 0 of the CM.\n'
        '   0: Tracing enabled, no address tracing\n'
        '   1: Tracing enabled with address tracing\n'
        '   2: Reserved\n'
        '   3: Tracing disabled')
    cmp1ctl = RegisterField('cmp1ctl', default=0, valid='x', fields=['d.P1_CTL'], requires=[],
        doc='Provides control over tracing transactions on Port 1 of the CM.\n   See cmp0ctl for values')
    cmp2ctl = RegisterField('cmp2ctl', default=0, valid='x', fields=['d.P2_CTL'], requires=[],
        doc='Provides control over tracing transactions on Port 2 of the CM.\n   See cmp0ctl for values')
    cmp3ctl = RegisterField('cmp3ctl', default=0, valid='x', fields=['d.P3_CTL'], requires=[],
        doc='Provides control over tracing transactions on Port 3 of the CM.\n   See cmp0ctl for values')
    cmp4ctl = RegisterField('cmp4ctl', default=0, valid='x', fields=['d.P4_CTL'], requires=[],
        doc='Provides control over tracing transactions on Port 4 of the CM.\n   See cmp0ctl for values')
    cmp5ctl = RegisterField('cmp5ctl', default=0, valid='x', fields=['d.P5_CTL'], requires=[],
        doc='Provides control over tracing transactions on Port 5 of the CM.\n   See cmp0ctl for values')
    cmp6ctl = RegisterField('cmp6ctl', default=0, valid='x', fields=['d.P6_CTL'], requires=[],
        doc='Provides control over tracing transactions on Port 6 of the CM.\n   See cmp0ctl for values')
    cmp7ctl = RegisterField('cmp7ctl', default=0, valid='x', fields=['d.P7_CTL'], requires=[],
        doc='Provides control over tracing transactions on Port 7 of the CM.\n   See cmp0ctl for values')

    pm_delay = RegisterField('pm_delay', default=0, valid='x', fields=['p.PERFC_TC_DELAY'], requires=[],
        doc='Delay between generation of performance counter trace messages', version=10)
    pm_en   = RegisterField('pm_en', default=0, valid='1|0', fields=['p.PERFC_TC_EN'], requires=[],
        doc='Enable tracing of CM performance counters', version=10)


    def __init__(self, b, d, s, p, st, cfg):
        self._b = b
        self._d = d
        self._s = s
        self._p = p
        self._st = st
        self.trace_version = (cfg & 7) + 3
        if self.trace_version >= 7:
            self.trace_version += 1
        
    def set_reg_field(self, regname, field, value):
        write = {field : value}
        if regname == 'b':
            write['WE'] = 1
        elif self._st is not None and regname == 'd' and field == 'ST_En':
            regname = 'st'
            field = 'ST_En'
        setattr(self, '_' + regname, getattr(self, '_' + regname)._replace(**write))
        
    def get_reg_type(self, regname):
        return type(getattr(self, '_' + regname))
            
    def get_reg_field(self, regname, field):
        if self._st is not None and regname == 'd' and field == 'ST_En':
            regname = 'st'
            field = 'ST_En'
        return getattr(getattr(self, '_' + regname), field)
        
    def set_en(self):
        self.set_reg_field('d', 'TWSrcVAl', 15)
        self.set_reg_field('d', 'CM_En', 1)
        

    def write(self, device):
        self.set_en()
        tcbsys = _get_mdh_name(TCBSys, device)
        device.tiny.WriteRegisters([PMCtrl, tcbsys], [self._p, self._s])
        
        cm_device = get_trace_master(device)
        write_cm_tcb_registers(cm_device, [TCBControlB, TCBControlD], 
                                    [self._b, self._d])
        if self._st is not None:
            device.tiny.WriteRegisters([STControl], [self._st])

    @classmethod
    def read(cls, device):
        tcbsys = _get_mdh_name(TCBSys, device)
        s = read_tcb_register(device, tcbsys)
        cm_device = get_trace_master(device)
        b, d   = read_cm_tcb_registers(cm_device, [TCBControlB, TCBControlD])
        cfg = read_tcb_register(device, TCBConfig) & 0xffffffff

        p = PMCtrlValue(device.tiny.ReadRegisters([PMCtrl])[0])
        st = STControlValue(device.tiny.ReadRegisters([STControl])[0]) if is_oci(device) else None
        return cls(b, d, s, p, st, cfg)
        

class PDTraceCM(trace.TraceBase):
    TraceMode = PDTraceModeCM

