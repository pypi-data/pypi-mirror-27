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

from imgtec.lib.namedenum import namedenum
    
TraceTypes = namedenum ('TraceTypes',
                        'HDI_TRACETYPE_TS', 
                        'HDI_TRACETYPE_PC', 
                        'HDI_TRACETYPE_INST', 
                        'HDI_TRACETYPE_LOAD', 
                        'HDI_TRACETYPE_STORE', 
                        'HDI_TRACETYPE_ACCESS', 
                        'HDI_TRACETYPE_LOAD8', 
                        'HDI_TRACETYPE_STORE8', 
                        'HDI_TRACETYPE_LOAD16', 
                        'HDI_TRACETYPE_STORE16', 
                        'HDI_TRACETYPE_LOAD32', 
                        'HDI_TRACETYPE_STORE32', 
                        'HDI_TRACETYPE_LOAD64', 
                        'HDI_TRACETYPE_STORE64', 
                        'HDI_TRACETYPE_OVERFLOW', 
                        'HDI_TRACETYPE_TRIGGER_ABOUT', 
                        'HDI_TRACETYPE_TRIGGER_INFO', 
                        'HDI_TRACETYPE_NOTRACE_CYCLES', 
                        'HDI_TRACETYPE_BACKSTALL_CYCLES', 
                        'HDI_TRACETYPE_IDLE_CYCLES', 
                        'HDI_TRACETYPE_TCB_MESSAGE', 
                        'HDI_TRACETYPE_MODE_INIT', 
                        'HDI_TRACETYPE_MODE_CHANGE', 
                        'HDI_TRACETYPE_UTM', 
                        'HDI_TRACETYPE_INST_KILLED', 
                        'HDI_TRACETYPE_GAP', 
                        'HDI_TRACETYPE_PCV', 
                        'HDI_TRACETYPE_ERROR', 
                        'HDI_MEM_READ_ERROR', 
                        'HDI_TRACETYPE_TRIGGER_MATCH', 
                        'HDI_TRACETYPE_IPC_SYNC', 
                        'HDI_TRACETYPE_NO_INSTR_EXE', 
                        'HDI_TRACETYPE_IDLE_SLOT', 
                        'HDI_UNEXPECTED_PCDELTA', 
                        'HDI_UNRESOLVED_BRANCH', 
                        'HDI_TFMSG_OVERFLOW', 
                        'HDI_MEM_ERROR_LIMIT', 
                        'HDI_RESYNCING', 
                        'HDI_BL_INTERRUPTED', 
                        'HDI_IFLOW_3_SYNC_INFO',
                        'HDI_CID',
                        'HDI_LOAD128',
                        'HDI_STORE128',
                        HDI_IMON_DATA = 1024)
    
class trace_type_decode(object):
    mode_string = ["kernel (exl=0 erl=0)",
                    "kernel (exl=1 erl=0)",
                    "kernel (erl=1)",
                    "debug",
                    "supervisor",
                    "user",
                    "unknown6",
                    "unknown7"]
    
    mode_string_IFLOW = ["kernel",
                        "kernel",
                        "kernel",
                        "debug",
                        "supervisor",
                        "user",
                        "unknown6",
                        "unknown7"]    
    isa_string = ["MIPS32", "MIPS64", "MIPS16", "unknown3"]    
    
    msa_info = {8 : ('b', 0xff,               '0x%02X ',  '0x-- '),
                16 :('h', 0xffff,             '0x%04X ',  '0x---- '),
                32 :('w', 0xffffffff,         '0x%08X ',  '0x-------- '),
                64 :('d', 0xffffffffffffffff, '0x%016X ', '0x---------------- '),
                128 :('d', 0xfffffffffffffff, '0x%032X ', '0x-------------------------------- ')
                }
    
    def __init__(self, show_asid, target_info):
        self.type_handlers = {TraceTypes.HDI_TRACETYPE_TS : self.tt_ts, 
                              TraceTypes.HDI_TRACETYPE_PC  : self.tt_pc, 
                            TraceTypes.HDI_TRACETYPE_INST : self.tt_inst, 
                            TraceTypes.HDI_TRACETYPE_LOAD : self.tt_load, 
                            TraceTypes.HDI_TRACETYPE_STORE : self.tt_store, 
                            TraceTypes.HDI_TRACETYPE_ACCESS : self.tt_access, 
                            TraceTypes.HDI_TRACETYPE_LOAD8 : self.tt_load8, 
                            TraceTypes.HDI_TRACETYPE_STORE8 : self.tt_store8, 
                            TraceTypes.HDI_TRACETYPE_LOAD16 : self.tt_load16, 
                            TraceTypes.HDI_TRACETYPE_STORE16 : self.tt_store16, 
                            TraceTypes.HDI_TRACETYPE_LOAD32 : self.tt_load32, 
                            TraceTypes.HDI_TRACETYPE_STORE32 : self.tt_store32, 
                            TraceTypes.HDI_TRACETYPE_LOAD64 : self.tt_load64, 
                            TraceTypes.HDI_TRACETYPE_STORE64 : self.tt_store64, 
                            TraceTypes.HDI_TRACETYPE_OVERFLOW : self.tt_overflow, 
                            TraceTypes.HDI_TRACETYPE_TRIGGER_ABOUT : self.tt_trigger_about, 
                            TraceTypes.HDI_TRACETYPE_TRIGGER_INFO : self.tt_trigger_info, 
                            TraceTypes.HDI_TRACETYPE_NOTRACE_CYCLES : self.tt_notrace_cycles, 
                            TraceTypes.HDI_TRACETYPE_BACKSTALL_CYCLES : self.tt_backstall_cycles, 
                            TraceTypes.HDI_TRACETYPE_IDLE_CYCLES : self.tt_idle_cycles, 
                            TraceTypes.HDI_TRACETYPE_TCB_MESSAGE : self.tt_tcb_msg, 
                            TraceTypes.HDI_TRACETYPE_MODE_INIT : self.tt_mode_init,
                            TraceTypes.HDI_TRACETYPE_MODE_CHANGE :  self.tt_mode_init,
                            TraceTypes.HDI_TRACETYPE_UTM : self.tt_utm, 
                            TraceTypes.HDI_TRACETYPE_INST_KILLED : self.tt_inst_killed, 
                            TraceTypes.HDI_TRACETYPE_GAP : self.tt_gap, 
                            TraceTypes.HDI_TRACETYPE_PCV : self.tt_pcv, 
                            TraceTypes.HDI_TRACETYPE_ERROR : self.tt_error, 
                            TraceTypes.HDI_MEM_READ_ERROR : self.tt_mem_read_error,
                            TraceTypes.HDI_TRACETYPE_TRIGGER_MATCH : self.tt_trigger_match, 
                            TraceTypes.HDI_TRACETYPE_IPC_SYNC : self.tt_ipc_sync, 
                            TraceTypes.HDI_TRACETYPE_NO_INSTR_EXE : self.tt_no_instr_exe, 
                            TraceTypes.HDI_TRACETYPE_IDLE_SLOT : self.tt_idle_slot,
                            TraceTypes.HDI_UNEXPECTED_PCDELTA : self.tt_unexpected_pc_delta, 
                            TraceTypes.HDI_UNRESOLVED_BRANCH : self.tt_unresolved_branch, 
                            TraceTypes.HDI_TFMSG_OVERFLOW : self.tt_tfmsg_overflow, 
                            TraceTypes.HDI_MEM_ERROR_LIMIT : self.tt_mem_error_limit, 
                            TraceTypes.HDI_RESYNCING : self.tt_resyncing, 
                            TraceTypes.HDI_BL_INTERRUPTED : self.tt_bl_interrupted, 
                            TraceTypes.HDI_IFLOW_3_SYNC_INFO : self.tt_iflow_sync_info,
                            TraceTypes.HDI_CID : self.tt_cid,
                            TraceTypes.HDI_LOAD128 : self.tt_load128,
                            TraceTypes.HDI_STORE128 : self.tt_store128,
                            
                            TraceTypes.HDI_IMON_DATA : self.tt_imon_data }
        # TODO - is_flow needs initialising
        self.show_asid = show_asid
        self.show_markers = target_info.show_markers
        self.is_flow = False #target_info.is_flow
        self.core_details = target_info.core_details
        self.is_fdt = target_info.is_fdt
        self.is_iflow3 = target_info.iflow3
        self.is_32bit = target_info.is_32bit()
        self.show_im = target_info.show_im
        self.show_lsm = target_info.show_lsm
        self.show_fcr = target_info.show_fcr
        self.target_info = target_info
        
    def is_multicore(self):
        return (self.core_details & 2) != 0    

    def has_mt(self):
        return (self.core_details & 1) != 0
     
    def tt_ts(self, tr, addr):
        delta = tr.value/1000.0
        return "TimeStamp %f us (dT=N/A us)" % (delta,)
    
    def report_slot_info(self):
        return self.target_info.is_74k or self.target_info.is_1074k
    
    def tt_pc(self, tr, addr):
        if tr.value != 0xffffffffffffffff and self.report_slot_info():
            return "S" + str(tr.value) + " pc " + addr
        else:
            return "pc    " + addr
    
    def tt_inst(self, tr, addr):
        return "inst  " + addr + " 0x%08X" % (tr.value,)

    def get_data_fmt(self, tr):
        return ' 0x%016X' if tr.value > 0xffffffff else' 0x%08X'
        
    def tt_load(self, tr, addr):
        fmt = self.get_data_fmt(tr)
        sVal = fmt % (tr.value,) if self.target_info.traceLD or self.is_fdt else ""
        return "ld    " + addr + sVal
      
    def tt_store(self, tr, addr):
        fmt = self.get_data_fmt(tr)
        sVal = fmt % (tr.value,) if self.target_info.traceSD or self.is_fdt else ""
        return "st    " + addr + sVal
          
    def tt_access(self, tr, addr):
        return "ac    " + addr
        
    def determine_value_mask(self, bits, prefix, is_msa):
        if is_msa:
            return 0xffffffffffffffff
        if (prefix == 'ld'):
            if bits <= 32:
                return 0xffffffff
        elif bits == 8:
            return 0xff
        elif bits == 16:
            return 0xffff
        elif bits == 32:
            return 0xffffffff
        return -1
    
    def determine_masked_value(self, tr, value_mask):
        if tr.meta_data3 != -1:
            value = tr.value + (tr.meta_data << 64) + (tr.meta_data2 << 96)
        else:
            value = tr.value
        
        return value & value_mask 

    def format_msa(self, value, bits, no_upper):    
        s = ''
        size, mask, fmt, no_upr = self.msa_info[bits]
        for n in range (128, 0, -bits):
            bitpos = n - bits
            if bitpos < 64 or not no_upper:
                data = (value >> bitpos) & mask
                s += fmt % (data)
            else:
                s += no_upr
        return s
        
    def outputTcb6MsaData(self, inst, tr, addr, bits) :
        if tr.meta_data3 != -1:
            if bits == 128:
                bits = tr.nbytes()
            value = tr.value + (tr.meta_data << 64) + (tr.meta_data2 << 96)
            data_str = self.format_msa(value, bits, tr.isUPR128())
            return inst + " " + addr + "   " + data_str
        else:
            return inst + " " + addr + "   <msa data capture disabled>"
        
        
    def ldst_fmt(self, prefix, bits, addr, tr):
        if tr.isMsa():
            size, mask, fmt, no_upr = self.msa_info[bits]
            inst = '%s.%s' % (prefix, size)
        else:
            inst = '%s%d' %(prefix, bits)
        if bits == 8:
            inst += '  '
        elif bits != 128:
            inst += ' '
            
        value_mask = self.determine_value_mask(bits, prefix, tr.isMsa())
        masked_value = self.determine_masked_value(tr, value_mask)
            
        if tr.isOverflow():
            if bits > 32:
                return inst + " " + "0x****************   0x****************    overflow"
            else:
                return inst + " " + "0x********   0x********    overflow"
        
        if tr.isMsa():
            return self.outputTcb6MsaData(inst, tr, addr, bits)
        
        if bits > 32:
            if (masked_value & 0xffffffffffffffff) == 0xffffffffffffffff:
                if self.target_info.no_upper_data():
                    result =  inst + " " + addr + "   0x----------------"
                else:
                    result = inst+  " " + addr
            else:
                result = inst + " " + addr + "   0x%016X" % (masked_value,)
            return result
        fmt = "   0x%08X" if self.is_32bit else "   0x--------%08X"  
        if bits == 32:
            fmt = "   0x%08X" if self.is_32bit else "   0x--------%08X"
            mask = 0xffffffff
        elif bits == 16:
            fmt = "   0x----%04X" if self.is_32bit else "   0x------------%04X"
            mask = 0xffff
        elif bits == 8:
            fmt = "   0x------%02X" if self.is_32bit else "   0x--------------%02X"
            mask = 0xff
            
        result = inst + " " + addr + fmt % (masked_value & mask,)
            
        return result

    def tt_ldst_fmt(self, prefix, addr, fmt, value):
        return prefix + addr + fmt % (value,)
            
    def tt_load8(self, tr, addr):
        return self.ldst_fmt('ld', 8, addr, tr)

    def tt_store8(self, tr, addr):
        return self.ldst_fmt('st', 8, addr, tr)
        
    def tt_load16(self, tr, addr):
        return self.ldst_fmt('ld', 16, addr, tr)
        
    def tt_store16(self, tr, addr):
        return self.ldst_fmt('st', 16, addr, tr)
    
    def tt_load32(self, tr, addr):
        return self.ldst_fmt('ld', 32, addr, tr)
        
    def tt_store32(self, tr, addr):
        return self.ldst_fmt('st', 32, addr, tr)
    
    def tt_load64(self, tr, addr):
        return self.ldst_fmt('ld', 64, addr, tr)

    def tt_store64(self, tr, addr):
        return self.ldst_fmt('st', 64, addr, tr)
    
    def tt_load128(self, tr, addr):
        return self.ldst_fmt('ld', 128, addr, tr)
    
    def tt_store128(self, tr, addr):
        return self.ldst_fmt('st', 128, addr, tr)
    
    
    def tt_overflow(self, tr, addr):
        return "overflow"

    def tt_trigger_about(self, tr, addr):
        return "trigger about 0x%02X" % (tr.value,)
      
    def tt_trigger_info(self, tr, addr):
        code = tr.addr
        tcbInfo = tr.value

        if (code & 0x9) != 0:
            inst_data = "data-bkpt" if (tcbInfo & 0x001) != 0 else "inst-bkpt"
            trc_start_stop = "start" if (tcbInfo & 0x02) != 0 else "stop"
            bkptNum = (tcbInfo >> 2) & 0x0F
            return "trace " + trc_start_stop + "  " + inst_data + "  " + str(bkptNum)
        else:
            return "trigger info 0x%02X" % (tr.value,)
        
    def tt_notrace_cycles(self, tr, addr):
        return "no trace cycles %d" % (tr.value,)
        
    def tt_backstall_cycles(self, tr, addr):
        return "backstall cycles %d" % (tr.value,)
       
    def tt_idle_cycles(self, tr, addr):
        # TODO - May need to check dq_hwinfo
        if self.is_flow:
            s = "cycles %d"
        else:
            s = "idle cycles %d"
        return  s % (tr.value,)
    
    def tt_tcb_msg(self, tr, addr):
        return "tcb message code=0x%x info=0x%x" % (tr.addr, tr.value)
        
    def tt_mode_init(self, tr, addr):
        ISA_mode = tr.isa
        modes_list = self.mode_string #self.mode_string_IFLOW if self.is_flow else self.mode_string
        
        result = "mode " + modes_list[(tr.value >> 8) & 7]
        result += ", isa=" + ISA_mode       
        asid_str = self.get_asid_str(tr)
        result += asid_str
        
        if self.target_info.has_vpid:
            vpstr = ", VP%d" % (tr.tc)
            result += vpstr
            
        if self.target_info.has_vze and self.target_info.tracerev() >= 10:
            gid = tr.meta_data2
            gidstr = ', Root' if gid == 0 else ', G%d' % (gid,)
            result += gidstr
        if tr.value & 0x80000000:
            cid = tr.meta_data3 & 0xffffffff
            cidstr = ', cid 0x%X' % (cid,)
            result += cidstr
            
        return result
    
    def tt_cid(self, tr, addr):
        cid = tr.meta_data3 & 0xffffffff
        cidstr = 'cid   0x%08X' % (cid,)
        return cidstr
    
    def tt_utm(self, tr, addr):
        fmt = "0x%08X" if self.is_32bit else "0x%016X"
        val = fmt % (tr.value,)
        return ("utm%d" % (tr.addr,)) + " value=" + val
          
    def tt_inst_killed(self, tr, addr):
        return "previous instruction killed"
    
    def tt_gap(self, tr, addr):
        return "gap"
        
    def tt_pcv(self, tr, addr):
        # TODO - performance counter value
        prev = tr.addr & 0xffffffff
        curr = tr.value & 0xffffffff
        
        counter_num = tr.meta_data
        if counter_num == 0xffffffff:
            counter_str = '??    '
        elif counter_num == 0xfffffffe:
            counter_str = 'Cks   '
            curr *= tr.meta_data2
            prev *= tr.meta_data2
        else:
            counter_str = 'C%d (%d)' % (counter_num, tr.meta_data2)
        val_str = str(curr)
        result = "%s %s %-12s" % ('perf counter value', counter_str, val_str)
        
        if prev != 0xffffffff:
            delta = 0
            if prev > curr:
                delta = 0x100000000 + curr - prev
            else:
                delta = curr - prev
                
            result = result + " : d=" + str(delta)
            
        return result
    
    def tt_error(self, tr, addr):
        return "generic trace errror"
        
    def tt_mem_read_error(self, tr, addr):
        return "pc    " + addr + "   Code memory unavailable"
        
    def tt_trigger_match(self, tr, addr):
        trigger_type = "data" if (tr.value & 1) != 0 else "inst"
        return "bkpt/trigger match: %s-bkpt %d" % (trigger_type, (tr.value >> 2) & 0x0F)
    
    def tt_ipc_sync(self, tr, addr):
        ISA_mode = tr.isa
        modes_list = self.mode_string #self.mode_string_IFLOW if self.is_flow is True else self.mode_string
        mode = modes_list[(tr.value >> 8) & 7]
        return "Sync: pc=" + addr + "  mode " + mode + ", isa=" + ISA_mode + (", asid=0x%02X" % (tr.value & 0xFF,))
        
    def tt_no_instr_exe(self, tr, addr):
        return "No Instructions Executed"
        
    def tt_idle_slot(self, tr, addr):
        return "S%d idle slot " % (tr.value,)
           
    def tt_unexpected_pc_delta(self, tr, addr):
        return "Unexpected PC Delta:  " + addr + " ---> " + (" 0x%08X" % (tr.value,))
        
    def tt_unresolved_branch(self, tr, addr):
        return "**** Unresolved Branch: ******"
 
    def tt_tfmsg_overflow(self, tr, addr):
        return "**** Trace Message buffer limit reached *****"
    
    def tt_mem_error_limit(self, tr, addr):
        return "**** Code Memory Read Error Limit Reached, DQer process stopped *****"
          
    def tt_resyncing(self, tr, addr):
        return "**** ReSyncing to trace Sync Point *****"

    def tt_bl_interrupted(self, tr, addr):
        return " ??? " + addr
        
    def tt_iflow_sync_info(self, tr, addr): 
        isa_mode = tr.isa
        idx = tr.meta_data
        
        POMode = self.mode_string[idx] if self.is_iflow3 else self.mode_string_IFLOW[idx]
        guest_str = ""
        if self.target_info.tracerev() > 2:
            if self.target_info.has_vze:
                if tr.meta_data3 == 0:
                    guest_str = "Root"
                elif tr.meta_data3 > 0:
                    guest_str = "Guest=" + str(tr.meta_data3)
            else:
                guest_str = 'Root'
        else:
            guest_str = ''
            
        asid_str = ", asid=0x%02X  " % (tr.meta_data2 & 0xff,)
        
        return "mode " + POMode + ", isa=" + isa_mode + asid_str + guest_str
    
    def tt_imon_data(self, tr, add):
        return 'IMON timestamp'
    
    def is_ldst(self, trace_type):
        return trace_type in [  TraceTypes.HDI_TRACETYPE_LOAD8,
                                TraceTypes.HDI_TRACETYPE_STORE8,
                                TraceTypes.HDI_TRACETYPE_LOAD16,
                                TraceTypes.HDI_TRACETYPE_STORE16,
                                TraceTypes.HDI_TRACETYPE_LOAD32,
                                TraceTypes.HDI_TRACETYPE_STORE32,
                                TraceTypes.HDI_TRACETYPE_LOAD64, 
                                TraceTypes.HDI_TRACETYPE_STORE64,
                              ]
    
    def decode_trace_type(self, tr, is_flow):
        # TODO fix th
        addr_fmt = "0x%08X" if self.is_32bit else "0x%016X"
        addr = addr_fmt % (tr.addr,)
        if self.is_fdt and self.is_ldst(tr.type):
            addr = "0x------%02X" % (tr.addr & 0xff, )
            
        if self.show_asid:
            asid_str = "%s:" % (self.get_asid_value_str(tr,))
            addr = asid_str + addr
        try:
            self.is_flow = is_flow
            markers = self.get_markers(tr) if self.show_markers else ""
            return markers + "  " + self.type_handlers[tr.type](tr, addr)
        
        except KeyError:
            if tr.type == 0xffffffff:
                return "No Trace Data Available..."
            elif tr.type == 0xfffffffe:
                return "Decoding trace data..."
            elif tr.type == 0xfffffffd:
                return "No trace data of selected types..."
            elif tr.type == 0xfffffffc:
                return "Collecting trace data..."
            elif tr.type == 0xfffffffb:
                return ""
            else:
                return "Unrecognised trace type"
            
    def get_markers(self, tr):
        markerF = "FCR" if tr.isFCR() and self.show_fcr else "   "
        markerI = "IM" if tr.isIM() and self.show_im else "  "
        markerL = "LSM" if tr.isLSM() and self.show_lsm else "   "
        
        if tr.type == TraceTypes.HDI_TRACETYPE_MODE_CHANGE:
            markerL = "   "   
        if tr.type != TraceTypes.HDI_TRACETYPE_PC:
            markerI = "  "
            markerF = "   "
        return markerF + " " + markerI + " " + markerL    
    
    def get_asid_value_str(self, tr):
        asid_fmt = "0x%04X" if self.target_info.tracerev() >=6 else "0x%02X"
        asid_value = tr.asid
        asid_str = (asid_fmt % (asid_value,))
        return asid_str

    def get_asid_str(self, tr):
        return ', asid=' + self.get_asid_value_str(tr)
    
