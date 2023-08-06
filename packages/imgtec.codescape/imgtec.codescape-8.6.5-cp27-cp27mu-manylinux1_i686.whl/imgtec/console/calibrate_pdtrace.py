#!/usr/bin/python

import os, sys, time
from imgtec.console import *
from imgtec.console.support import CoreFamily
from imgtec.console.scan import TCBControlBValue, TCBControlAValue
from imgtec.console import trace
from imgtec.console.pdtrace import is_oci, TCBConfigValue, TF_ControlValue, TF_ConfigValue

from imgtec.console.support import Command, command

import struct

USE_OVERSAMPLE = 0
USE_PLLS = 1
AUTO = 2

ejtag_regnames = {tcbcontrola : 'ejtag_tcbcontrola',
                  tcbcontrolb : 'ejtag_tcbcontrolb'}
                  
mdh_regnames =  {tcbcontrola : 'drseg_tcbcontrola',
                  tcbcontrolb : 'drseg_tcbcontrolb'}

regtypes = {'ejtag_tcbcontrola' : TCBControlAValue,
            'ejtag_tcbcontrolb' : TCBControlBValue,
            'drseg_tcbcontrola' : TCBControlAValue,
            'drseg_tcbcontrolb' : TCBControlBValue,
            'dbu_tf_control' : TF_ControlValue,
            'dbt_tf_config' : TF_ConfigValue}


def mod_reg(reg_name, device, **kwargs):
    value = device.tiny.ReadRegisters([reg_name])[0]
    type = regtypes[reg_name]
    val = type(value)
    val = val._replace(**kwargs)
    device.tiny.WriteRegisters([reg_name], [val])
    
def modtapreg(reg, device, **kwargs):
    if is_oci(device):
        reg_name = mdh_regnames[reg]
    else:
        reg_name = ejtag_regnames[reg]
        
    mod_reg(reg_name, device, **kwargs)


def determines_quads(device):
    if is_oci(device):
        val = TF_ConfigValue(device.tiny.ReadRegisters(['dbu_tf_config'])[0])
    else:
        val = TCBConfigValue(device.tiny.ReadRegisters(['ejtag_tcbconfig'])[0])
    return 2 ** val.PW

def mod_cm_controlreg(device, **kwargs):
    if is_oci(device):
        reg_name = 'dbu_tf_control'
    else:
        reg_name = 'ejtag_tcbcontrolb'
    
    mod_reg(reg_name, device, **kwargs)
        
def split_byte_cmp(byte_val) :
    temp1 = ord(byte_val) & 0xf
    temp2 = ord(byte_val) >> 4
    if temp1 != temp2 :
        #print "FAILED: 4-bit values don't match, High %d : Low %d" % (temp2, temp1)
        return 1
    return 0

def try_to_lock(tr_records, num_quad_bits) :
    cal_data = [0, 15, 0, 5, 10, 8, 4, 2, 1, 14, 13, 11, 7]
    bit4_0 = ord(tr_records[0]) & 0xf
    bit4_1 = ord(tr_records[0]) >> 4
    bit4_2 = ord(tr_records[1]) & 0xf
    bit4_3 = ord(tr_records[1]) >> 4
    if num_quad_bits == 2 :
        if bit4_0 != bit4_1 or bit4_2 != bit4_3 :
            return [0, 0]
    if num_quad_bits == 4 :
        if bit4_0 != bit4_1 or bit4_0 != bit4_2 or bit4_0 != bit4_3 :
            return [0, 0]
    if bit4_0 != cal_data[0] :
        for index, val in enumerate(cal_data) :
            if val == bit4_0 :
                #print "0:Locked at %d with val %d" %(index, val)
                return [0, index]
    elif bit4_1 != cal_data[0] and num_quad_bits == 1 :
        for index, val in enumerate(cal_data) :
            if val == bit4_1 :
                #print "1:Locked at %d with val %d" %(index, val)
                return [1, index]
    elif bit4_2 != cal_data[0] and num_quad_bits == 2 :
        for index, val in enumerate(cal_data) :
            if val == bit4_2 :
                #print "1:Locked at %d with val %d" %(index, val)
                return [1, index]
    return [0, 0]

class traceIO(object):
    def __init__(self, data):
        self.data = data
        self.offset = 0
        
    def read(self, count):
        if self.offset + count > len(self.data):
            count = len(self.data) - self.offset
        
        data = self.data[self.offset : self.offset + count]
        self.offset += count
        return data
    
    def close(self):
        self.offset = 0
        
offsets = [3, 1, 7, 5]
def determine_offset(idx):
    return offsets[idx & 3]

cal_data =  [0, 0x0f, 0, 0x05, 0x0a, 0x08, 0x04, 0x02, 0x01, 0x0e, 0x0d, 0x0b, 0x07]
cal_data2 = [0, 0xff, 0, 0x55, 0xaa, 0x88, 0x44, 0x22, 0x11, 0xee, 0xdd, 0xbb, 0x77]
# Should add PDtrace data lines dependencies 4, 8, 16
def check_calibration_data(trace_per_record, num_quad_bits, total_records, trace_data, num_64bit_tr_words):
    if num_quad_bits not in [1, 2, 4] :
        raise RuntimeError('Incorrect number of PDtrace data lines. Should be 1, 2 or 4 corresponding to 4, 8 or 16 data lines')

    fr = traceIO(trace_data)
    trace_record = fr.read(8) #Imon and Timestamp
    num_records = 0
    locked = 0
    pat = 0
    offset = 0
    count = 0
    while len(trace_record) and num_records < total_records - num_64bit_tr_words :
        align = 4 * (num_64bit_tr_words - (num_records % num_64bit_tr_words))
        for i in range(trace_per_record*4):
            offset = determine_offset(i)
            if (i % 4) == 0 :
                swapped_buf = fr.read(8)
            trace_record = ''.join([swapped_buf[offset], swapped_buf[offset-1]])
            if not locked :
                ret = try_to_lock(trace_record, num_quad_bits)
                if ret[1] != 0 :
                    pat = ret[1] - ret[0]
                    locked = 1
                else :
                    return 0
            if ((i + align) % (4*num_64bit_tr_words)) == 0 and cal_data[pat] == 0 :
                pat += 1		# FPGA removes zeros from the start of TraceWords
            if num_quad_bits == 1 :
                for j in range(2) :
                    bit4_0 = ord(trace_record[j]) & 0xf
                    bit4_1 = ord(trace_record[j]) >> 4
                    if bit4_0 != cal_data[pat] :
                        return 0
                    pat = (pat + 1) % 13
                    if bit4_1 != cal_data[pat] :
                        return 0
                    pat = (pat + 1) % 13
            elif num_quad_bits == 2 :
                if ord(trace_record[0]) != cal_data2[pat]:
                    return 0
                if ord(trace_record[1]) != cal_data2[(pat + 1) % 13]:
                    return 0
                pat = (pat + 2) % 13
                
            elif num_quad_bits == 4 :
                if ord(trace_record[0]) != cal_data2[pat] or ord(trace_record[1]) != cal_data2[pat]:
                    #print 'count = %d, pat = %d' % (count, pat) 
                    #print ord(trace_record[0]), ord(trace_record[1]), cal_data2[pat]
                    return 0
                pat = (pat + 1) % 13
            count += 1
        trace_record = fr.read(8) #Imon and Timestamp
        num_records += 1
        if len(trace_record) != 8 :
            #print 'finishing on %d with %d num_records'%(num_records,len(trace_record))
            break
    fr.close()
    #print "PASSED"
    return 1

def check_cal_data(trace_per_record, num_quad_bits, total_records, trace_data):
    if total_records < 1000:
        return 0
    num_64bit_tr_words = targetdata(device()).socs[0].cores[0].trace_word_length / 64
    return check_calibration_data(trace_per_record, num_quad_bits, total_records, trace_data, num_64bit_tr_words)
        
def read_trace(port, device, count):
    status, _ = device.tiny.PollTrace()
    imon_size, _ = device.tiny.ConfigureTrace('start_download', 'trace_only', 0, port)
    sock = trace.connect_socket(device.probe.location, port)
    data = trace.read_trace_data(sock, count * imon_size)
    sock.close()
    time.sleep(1)
    return data
    

def calibrate_trace(trace_clock, cr, num_packets, num_steps, device):
    num = num_steps					#Currently FPGA has 32 time slots
    trace_master = trace.get_trace_master(device)
    modtapreg(tcbcontrola, device=device, SyPExt = 0, SyP = 0, TB = 0, IO = 1, D = 0, E = 1, S = 1, K = 1, U = 1, ASID = 0, G = 1, TFCR = 0, TLSM = 0, TIM = 0, On = 0)
    modtapreg(tcbcontrolb, device=device, WE = 1, TM = 0, FDT = 0, CR = cr, CA = 0, OfC = 1, EN = 0)
    quads = determines_quads(device)
    mod_cm_controlreg(device = trace_master, WE = 1, TM = 0, OfC = 1, TR = 1, EN = 1, CR = cr, Cal = 0)
    samples = []
    config('Trace Clock', trace_clock)
    for i in range(num) :
        config('calibrate trace', (trace_clock << 16) | (cr << 12) | i, device=device)
        device.tiny.ConfigureTrace('stop_trace', 'trace_only')
        device.tiny.ConfigureTrace('start_one_shot', 'trace_only')
        mod_cm_controlreg(device=trace_master, WE = 1, TM = 0, OfC = 1, TR = 1, EN = 1, CR = cr, Cal = 1)
        time.sleep(0.1)
        mod_cm_controlreg(device=trace_master, WE = 1, TM = 0, OfC = 1, TR = 1, EN = 1, CR = cr, Cal = 0)
        imon_size, port = device.tiny.ConfigureTrace('stop_trace', 'trace_only')
        status, count = device.tiny.PollTrace()
        if count > num_packets:
            count = num_packets
        sample = 0
        if count:
            data = read_trace(port, device, count)
            if count > 1000:
                sample = check_cal_data(15, quads, count, data)
        #print status,count, sample            
        #print sample
        if Command._interactive:
            sys.stdout.write('.')# if sample else 'F')
            sys.stdout.flush()        

        samples.append(sample)
    start = 0
    counter = 0
    group_of_ones = [0, 0]
    # Rotate the array to group the ones together
    #print samples
    while samples[0] == 1 and start < num:
        samples = samples[1:] + samples[:1]
        start += 1
    if start == num :
        start = 0           #When PDtrace clock is slow the sample_data_delay can take any value
    for i in range(num) :
        if samples[i] == 1 :
            if counter == 0 :
                start_of_ones = i
            counter += 1
            if counter > group_of_ones[1] :
                group_of_ones[0] = start_of_ones
                group_of_ones[1] = counter
        else :
            counter = 0
    if group_of_ones[1] == 0 :
        config('calibrate trace', -1, device=device)        
        raise RuntimeError('Trace calibration failed, check values for trace clock and clock ratio.')
    end_passed = ((group_of_ones[0] + group_of_ones[1])) == num and (num == 32)
    tc = config('Trace Clock')
    if 0 < tc <= 35 and end_passed:
        inc_idelay = num - 1
    else:
        inc_idelay = (start + group_of_ones[0] + group_of_ones[1]/2) % num
    config('calibrate trace', (trace_clock << 16) | (cr << 12) | inc_idelay, device=device)
    return inc_idelay

def determine_num_steps(clock):
    clock = clock * 16
    num_steps = 1000 / clock
    return num_steps
    
@command()
def tracecalibrate(trace_clock=None, cr=None, device=None):
    ''' Calibrate the probe for reading of offchip pdtrace data.

    ============ ====================================================================
    Parameter    Meaning
    ============ ====================================================================
    cr           Off chip clock ratio to set. After calibration codescapeconsole will
                 validate that offchip trace is configured with this clock ratio
    ============ ====================================================================

    '''

    if not trace.is_pd_trace(device):
        raise RuntimeError('Device does not support PDtrace.')
    caps = device.probe.probe_info
    if not caps.get('has_pdtrace_connector', False):
        raise RuntimeError('Probe does not support offchip PDtrace.')
        
    if trace_clock is None:
        trace_clock =     config('Trace Clock')
    if cr is None:
        mode = tracemode()
        cr = mode.cr
         
    method = config('trace plls')
    num_steps = 32
    if method == AUTO:
        method = USE_OVERSAMPLE if trace_clock < 20 else USE_PLLS

    if method == USE_OVERSAMPLE:
        if trace_clock < 30:
            num_steps = determine_num_steps(trace_clock)
            #config('calibrate trace', (trace_clock << 16) | (cr << 12) | num_steps / 2, device=device)
            #if Command._interactive:
            #    print
            
            #return
            
        else:
           raise RuntimeError("Over sampling mode can only be used when the trace clock is less than 30MHz.")
    
    elif method == USE_PLLS:
        num_steps = 32
    else:
        raise RuntimeError("Invalid value for config('trace plls'). Valid values are:\n"\
                            " 0 - Use over sample mode\n"\
                            " 1 - Use trace PLLs\n"\
                            " 2 - Automatically determine which method to use based on trace clock.")
         
    if Command._interactive:
        print 'Calibrating trace. This may take a while.'

    delay = calibrate_trace(trace_clock, cr, 50000, num_steps, device)
    if Command._interactive:
        print
    

if __name__ == "__main__":
    probe('sp58011')
    reset(probe)
    autodetect()
    
    device(probe().socs[0].cores[0].vpes[0])    
    results3000 = []
    
    tracecalibrate(12,4)
    
    for i in range(10):
        now = time.time()
        idelay = calibrate_trace(12, 4, 20000, device())
        results3000.append(idelay)
        print "Time taken = %f, value = %d" % (time.time() - now, idelay)
    print results3000

    results40000 = []
    for i in range(10):
        now = time.time()
        results40000.append(calibrate_trace(0, 7, 50000, device()))
        print "Time taken = ", time.time() - now
        
    print results40000
