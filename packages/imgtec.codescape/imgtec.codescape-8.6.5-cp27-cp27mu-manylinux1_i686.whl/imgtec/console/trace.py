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

from imgtec.console.support import command
from imgtec.console import cpuinfo, go, dasmbytes, dasm, doubleword, byte, asid, Core, targetdata, results
from imgtec.console.cfg import config
from imgtec.console.support import *
from imgtec.console.results import *
from imgtec.console.generic_device import dasms
from imgtec.lib.format_signature import format_doc
from imgtec.console.trace_type_decode import TraceTypes, trace_type_decode

import os
import re
import select
import socket
import string
import struct
import subprocess
import sys
import tempfile
import threading
import time
import glob
from threading import Thread
from Queue import Queue, Empty
import ConfigParser
from StringIO import *
import shutil

def find_cm_device(device):
    '''Finds the CM in the cores on this SoC'''
    for core in device.probe.all_cores:
        if core.family == CoreFamily.mipscm:
            return core
    
    return None

def get_trace_master(device):
    cm = find_cm_device(device)
    return cm if cm else device

class CalibrationError(Exception): 
    pass

def validate_trace_calibrate(cal, clk, cr):
    if cal == -1:
        raise CalibrationError('Off chip trace requires calibration.')
    saved_cr = (cal >> 12) & 0xf
    saved_clock = (cal >> 16) & 0xffff
    if clk != saved_clock or saved_cr != cr:
        raise CalibrationError('Trace clock and/or clock ratio are different\n'\
                      'from values used to calibrate trace.\n'\
                      'Trace may require calibrating.')
            


class Error(Exception):
    pass

class read_thread(threading.Thread):
    def __init__(self, device, sock, config, imon_size, path):
        threading.Thread.__init__(self)
        self.device = device
        self.sock = sock
        self.config = config
        self.imon_size = imon_size
        self.path = path
        self.cont = True
      
    def read_data(self, f, timeout):  
        read, _, _ = select.select([self.sock], [], [], 2.0)
        if read:
            data = self.sock.recv(BufferSize)
            f.write(data)
        
        return read
    
    def run(self):
        try:
            if not os.path.exists(self.path):
                os.makedirs(self.path)
            filename = os.path.join(self.path, 'trace.tcf')
            with open(filename, "wb") as f:
                f.write(self.config)
            filename = os.path.join(self.path, 'trace.imon')
            # Open the file and save the data to it
            with open(filename, "wb") as f:
                status = ''
                count = 0
                f.write('IMON')
                f.write(struct.pack('>I', self.imon_size))
                while status != 'stopped' and self.cont:
                    if not self.read_data(f, 2.0):
                        status, count = self.device.tiny.PollTrace()
    
                # Check for any last data left to collect (the final stop_trace usually gathers
                # the last remaining packets
                self.read_data(f, 0.0)
        finally:
            self.sock.close()

    def stop(self):
        self.cont = False



def kill_old_thread(device):
    thr = device.probe.streaming_thread
    if thr:
        thr.stop()
        thr.join()
        device.probe.streaming_thread = None

def start_offchip_trace(device, offchip_mode, offchip_size, path = None):
    kill_old_thread(device) # Kill any previous streaming thread
    
    offchip_size = get_offchip_size(offchip_size)
    
    record_size, trace_port = device.tiny.ConfigureTrace('stop_trace', 'trace_only', 0, 5511)
    if offchip_mode == 'continuous_streaming':
        if path is None:
            raise RuntimeError('You must provide a path to a folder for streamed data')
        
        if device.probe.probe_info.get('trace_locally', 0):
            # Validate filename here
            device.tiny.ConfigureTrace('start_continuous_streaming', 'trace_only', offchip_size, 5511, 0, path)
        else:
            config = tracemode(device=device)
            cfg = config.config(True, device)
            
            #twsize = trace.determine_trace_word_size(cfg)
            # need to set up thread to read
            # Must have file parameter, to specify where to save
            connection_socket = connect_socket(device.probe.location, trace_port)
            #device.tiny.ConfigureTrace('start_download', 'trace_only', 0, trace_port)
            collector = read_thread(device, connection_socket, cfg, record_size, path)
            collector.start()
            device.probe.streaming_thread = collector
            record_size, trace_port = device.tiny.ConfigureTrace('start_' + offchip_mode, 'trace_only', offchip_size, 5511)
    else:
        record_size, trace_port = device.tiny.ConfigureTrace('start_' + offchip_mode, 'trace_only', offchip_size, 5511)
    status = None
    while status != offchip_mode:
        status, count = device.tiny.PollTrace()


def offchip_traceentries(device, twsize):
    
    imon_size, trace_port = device.tiny.ConfigureTrace('stop_trace', 'trace_only', 0, 5511)
    status, count = device.tiny.PollTrace()
    #return count
    counter = OffchipTraceCounter(device, count, trace_port, imon_size, twsize)
    return counter.count()

    
BufferSize = 65536
  
def read_trace_data_impl(sock, trace_count):
    buffer_size = BufferSize
    trace_data = ''
    amount_left = trace_count
    while amount_left != 0:
        count =  min(amount_left, buffer_size)
        read, write, _ = select.select([sock], [], [], 0.5)
        if not read:
            return trace_data
        data = sock.recv(count)
        amount_left -= len(data)
        trace_data += data
        
    return trace_data
  
def read_trace_data(sock, trace_count):
    return read_trace_data_impl(sock, trace_count)

class TraceReaderBase(object):
    def __init__(self, device, start_frame, num_entries, twsize):
        self.device = device
        self.start_frame = 0
            
        num_entries += (start_frame - self.start_frame)
        if twsize == 4:
            if (self.start_frame & 1) != 0:
                self.start_frame -= 1
                num_entries += 1
            if (num_entries & 1) != 0:
                num_entries += 1
            
        self.max_entries = num_entries
        self.twsize = twsize
        self.num_read = 0
        self.rdp = 0
        
    def reset(self):
        self.num_read = 0
            
    def read(self, num_to_read):
        
        if self.num_read == 0:
            self.init_rdp()
        num_left = self.max_entries - self.num_read
        num_to_read = min(num_left, num_to_read)
        
        data = []
        while num_to_read > 0:
            this_read = min(num_to_read, 512)
            trace = doubleword(0, count=this_read * self.twsize, type=32, device = self.device)
            data += trace
            num_to_read -= this_read
            self.num_read += this_read
        return endian_swap_words(data, self.device), []

    def length(self):
        return self.max_entries

    @property
    def end_addr(self):
        return self.start_frame + self.total_entries()
    
    def total_entries(self):
        raise NotImplementedError('total_entries not implemented in this class.')

    def init_rdp(self):
        raise NotImplementedError('total_entries not implemented in this class.')

class FileTraceReader(object):
    def determine_start_frame(self):
        with open(self.path, 'rb') as f:
            f.seek(self.start_frame * self.framesize())
            data = f.read(4)
            return struct.unpack(">I", data)[0]

    def __init__(self, path, twsize, rng = 'all'):
        self.path = path
        self.filesize = os.path.getsize(path)
        self.num_read = 0
        self.twsize = twsize
        self.start_frame, self.rng_length = determine_range('all', self.total_entries())
        self.start_frame = self.determine_start_frame()
        
    def framesize(self):
        return 4 + self.twsize * 8
        
    def reset(self):
        if self.fp:
            self.fp.close()
            self.num_read = 0
            self.frame_num = 0
            
    def read(self, num_to_read):
        if self.num_read == 0:
            self.fp = open(self.path, 'rb')
            #self.fp.seek(self.start_frame * self.framesize())
            # Here we should skip to the appropriate frame

        num_left = self.rng_length - self.num_read
        num_to_read = min(num_left, num_to_read)
        if num_to_read == 0:
            return '', []
        data = self.fp.read(num_to_read * self.framesize())
        self.num_read += len(data) / self.framesize()
        return filter_frame_num(data, self.twsize), []

    
    def total_entries(self):
        return self.filesize / self.framesize()

    def length(self):
        return self.total_entries()

    @property
    def end_addr(self):
        return self.start_frame + self.total_entries()


class OffChipFileTraceReader(object):
    hdr_size = 8

    def __init__(self, path, twsize, rng = 'all'):
        try:
            self.path = path
            self.filesize = os.path.getsize(path)
            self.fp = open(self.path, 'rb')
            # Read header to to get imon_size and other stuff
            self.num_read = 0
            hdr = self.fp.read(self.hdr_size)
            if hdr[0:4] != 'IMON':
                raise RuntimeError('File is not a valid IMON file')
            self.imon_size = struct.unpack('>I', hdr[4:])[0]
            self.twsize = twsize
            self.done = False
            self.frame_num = 0
            self.skip = - 1
            self.start_frame, self.end_frame = determine_range(rng, self.total_entries())
            self.stripper = iMonStripper(self.imon_size, self.start_frame, twsize)

            
        finally:
            if self.fp:
                self.fp.close()
                
    def reset(self):
        if self.fp:
            self.fp.close()
            self.fp = None
            
            self.num_read = 0
            self.done = False
            self.frame_num = 0
            self.skip = -1

    def read(self, num_to_read):
        if self.done:
            return []
        num_left = self.length() - self.num_read
        num_to_read = min(num_left, num_to_read)
        if num_to_read == 0:
            self.done = True
            self.reset()
            return [], []
        
        if self.num_read == 0:
            self.fp = open(self.path, 'rb')
            self.fp.seek(self.start_frame * self.imon_size + self.hdr_size)
            self.skip = -1
            
        data = self.fp.read(num_to_read * self.imon_size)
        self.num_read += num_to_read
        data, imon = self.stripper.strip(data)

        return data, imon

    def length(self):
        return self.total_entries() - self.start_frame
    
    def total_entries(self):
        return (self.filesize - self.hdr_size)/ self.imon_size
    
    @property

    def end_addr(self):
        return self.start_frame + self.total_entries()
    
    
class OffchipTraceCounter(object):
    
    def __init__(self, device, max_packets, port, imon_size, twsize):
        self.device = device
        self.max_packets = max_packets
        self.port = port
        self.imon_size = imon_size
        self.twsize = twsize
        self.num_read = 0
        self.sock = None
        
    def count(self):
        status, count = self.device.tiny.PollTrace()
        self.device.tiny.ConfigureTrace('stop_download', 'trace_only', 0, self.port)
        self.device.tiny.ConfigureTrace('start_download', 'trace_only', 0, self.port, 0)
        self.sock = connect_socket(self.device.probe.location, self.port)
        self.skip = -1

        num_frames = 0
        chunk_size = 256
        actual_num_frames = 0
        masked_num_frames = 0
        last_frames = 0
        last_mask = 0
        while self.max_packets != self.num_read:
            # We either exit when all iMon packets have been read
            # or when we have collected enough trace packets
            num_left = self.max_packets - self.num_read
            num_to_read = min(num_left, chunk_size)
            status, count = self.device.tiny.PollTrace()   
            data = read_trace_data(self.sock, num_to_read * self.imon_size)
            self.num_read += num_to_read
            skip = 0
            step = self.imon_size * 16
            if num_to_read <= chunk_size:
                step = self.imon_size
            for offset in range(0, len(data), step):
                s = data[offset : offset + imon_word_size]
                imon_hdr = struct.unpack('>Q', s)[0]                
                masked_count = (imon_hdr >> 24) & 0xff
                frame_diff = (masked_count - last_mask) & 0xff
                masked_num_frames += frame_diff
                last_mask = masked_count
            
        if self.sock:
            self.sock.close()
        return masked_num_frames / self.twsize
        
    
class OffchipTraceReader(object):
    def __init__(self, device, max_packets, count, port, imon_size, twsize, start_frame = 0):
        self.device = device
        #max_packets *= twsize
        self.max_packets = max_packets
        self.port = port
        self.imon_size = imon_size
        self.num_read = 0
        self.sock = None
        self.done = False
        self.twsize = twsize
        self.frame_num = 0
        self.skip = -1
        if start_frame < 10000:
            count += start_frame
            start_frame = 0
        else:
            count += 10000
            start_frame -= 1000
        self.start_frame =  start_frame
        self.max_entries = count
        self.stripper = iMonStripper(imon_size, start_frame, twsize)
        self.data = []
        self.imon = []
        
    def reset(self):
        self.num_read = 0
        self.done = False
        self.skip = -1
        self.frame_num = 0
        self.data = []
        self.imon = []
        self.stripper = iMonStripper(self.imon_size, self.start_frame, self.twsize)
        if self.sock:
            self.sock.close()
            self.sock = None

    def init_rdp(self):
        if self.num_read == 0:
            status, count = self.device.tiny.PollTrace()
            self.device.tiny.ConfigureTrace('stop_download', 'trace_only', 0, self.port)
            self.device.tiny.ConfigureTrace('start_download', 'trace_only', 0, self.port, 0)
            self.sock = connect_socket(self.device.probe.location, self.port)
            self.skip = -1

    def read(self, num_to_read):
        num_to_read /= self.imon_size
        if self.done:
            imon = self.imon
            self.imon = []
            return [], imon
        #num_to_read /= self.imon_size
        while True:
            # We either exit when all iMon packets have been read
            # or when we have collected enough trace packets
            num_left = self.max_packets - self.num_read
            num_to_read = min(num_left, num_to_read)
            if num_to_read == 0:
                self.done = True
                if self.sock:
                    self.sock.close()
                    self.sock = None
                
                imon = self.imon
                self.imon = []
                return [], imon
            
            self.init_rdp()
                
            status, count = self.device.tiny.PollTrace()
            data = read_trace_data(self.sock, num_to_read * self.imon_size)
            self.num_read += num_to_read
            
            new_data, new_imon = self.stripper.strip(data)
            data = self.data
            data.extend(new_data)
            imon = self.imon
            imon.extend(new_imon)
            num_frames = len(data) / self.twsize

            if num_frames:

                if self.max_entries != -1:
                    if self.frame_num + num_frames >= self.max_entries:
                        # Need to round down 
                        num_frames = self.max_entries - self.frame_num
                        
                        self.done = True
                        if self.sock:
                            self.sock.close()
                            self.sock = None
                
                self.frame_num += num_frames
                self.data = data[num_frames * self.twsize : ]
                data = data[0 : num_frames * self.twsize]
                self.imon = []
                return data, imon
            else:
                self.data = data
                self.imon = imon    
            ####
                
                
        return data, imon
    
    def length(self):
        return self.max_entries    
    
    @property
    def end_addr(self):
        return self.start_frame + self.max_entries
  
def offchip_traceread(device, start_frame, num_entries, twsize):
    imon_size, trace_port = device.tiny.ConfigureTrace('stop_trace', 'trace_only', 0, 5511)
    status, max_packets = device.tiny.PollTrace()
    trace_per_packet = imon_size / 8 - 1
    max_entries = max_packets
    max_entries *= trace_per_packet
    max_entries /= twsize
    if not num_entries:
        num_entries =  max_entries - start_frame
    num_entries = min(num_entries, max_entries)
    return OffchipTraceReader(device, max_packets, num_entries, trace_port, imon_size, twsize, start_frame)
    
class UnableToStartJava(Exception):
    pass

class InvalidJavaVersion(Exception):
    pass

class SrcValAllocator(object):
    
    def __init__(self, src_width, sys_trace):
        self.ids = [n for n in range(1 << src_width)]

        if sys_trace < 0 or sys_trace >= (1 << src_width):
            raise RuntimeError('Out of range value for system trace')
            
        self.ids.remove(sys_trace)
        
    def allocate(self):
        if len(self.ids):
            src_val = self.ids[0]
            self.ids.remove(src_val)
        else:
            raise RuntimeError('Too many trace sources')
            
        

def is_16bit_isa(isa):
    isa = isa.lower()
    return isa == 'mips16' or isa == 'micromips' or isa == 'nanomips'

def can_trace_history(target):
    # return true if all cores on target SoC are not tracing
    return False

def is_trace_historying(target):
    #return true if any target on the current core is trace historying
    # Nobody else can trace if so
    return False

class TargetInfo(object):
    
    def __init__(self, cfg, core_index = None):
        config = find_config_for_core(cfg, core_index) if core_index is not None else cfg
        fp = StringIO(config)
        self.is_r6,\
        self.is_micromips,\
        self.is_nanomips,\
        self.mr2,\
        self.isa_extras,\
        self.endian,\
        self.show_markers,\
        self.show_im,\
        self.show_lsm,\
        self.show_fcr,\
        self.core_details = self.determine_isa_stuff(fp)
        self.is_fdt,\
        self.iflow3, \
        self.is_flow = self.determine_fdt(StringIO(config))
        self.tracePC,\
        self.traceLA,\
        self.traceSA,\
        self.traceLD,\
        self.traceSD = self.determine_ldstinfo(StringIO(config))
        
        self.twsize = determine_trace_word_size(config)
        self.is_74k = is_74k(config) 
        self.is_1074k = is_1074k(config) 
        self.has_vze,\
        self.has_vpid,\
        self.trace_rev,\
        self.is_samurai = self.determine_extras(StringIO(config))
        self.read_registers(StringIO(config))
        
    def has_r6(self):
        return not self.is_nanomips and self.is_r6
        
    def tracerev(self):
        if self.is_flow:
            return self.trace_rev + 2
        else:
            ver = (self.trace_rev & 0xf) + 3
            if ver > 7:
                ver += 1
            return ver
        
    def no_upper_data(self):
        return (self.tcbcontrole & (1 << 25)) != 0
        
    def is_daimyo(self, company, prid):
        return company == 1 and (prid == 0xb0 or prid == 0xa9)
    
    def determine_extras(self, fp):
        parser = ConfigParser.ConfigParser()
        try:
            parser.readfp(fp)
            config3 = int(parser.get('section 1', 'config3'), 16)
            has_vz_mask = 0x00800000
            has_vz = (config3 & has_vz_mask) == has_vz_mask
            prid = int(parser.get('section 1', 'PRID'), 16)
            c = (prid >> 16) & 0xff
            p = (prid >> 8) & 0xff
            has_vpid = self.is_daimyo(c, p)
            is_samurai = has_vpid
            if self.is_flow:
                tcbver = (int(parser.get('section 1', 'ifctl'), 16) >> 16) & 0x3
            else:
                tcbver = int(parser.get('section 1', 'tcbconfig'), 16) & 0xf
            
            return has_vz, has_vpid, tcbver, is_samurai
        
        except ConfigParser.Error:
            return False, False, False, False

    def read_registers(self, fp):
        parser = ConfigParser.ConfigParser()
        try:
            parser.readfp(fp)
            self.tcbcontrola = int(parser.get('section 1', 'tcbcontrola'), 16)
            self.tcbcontrolb = int(parser.get('section 1', 'tcbcontrolb'), 16)
            self.tcbcontrolc = int(parser.get('section 1', 'tcbcontrolc'), 16)
            self.tcbcontrold = int(parser.get('section 1', 'tcbcontrold'), 16)
            self.tcbcontrole = int(parser.get('section 1', 'tcbcontrole'), 16)
            
        except ConfigParser.Error:
            self.tcbcontrola = 0
            self.tcbcontrolb = 0
            self.tcbcontrolc = 0
            self.tcbcontrold = 0
            self.tcbcontrole = 0

        
    def determine_isa_extras(self, parser):
        try:
            extras = ""
            config1 = int(parser.get('section 1', 'config1'), 16)
            config3 = int(parser.get('section 1', 'config3'), 16)
            config7 = int(parser.get('section 1', 'config7'), 16)
            if config3 & 2:
                extras += '+smart'
            if config3 & 4:
                extras += '+mt'
            if config3 & 0x400:
                extras += '+dsp'
            if config3 & 0x10000000:
                extras += '+msa' 
            if config7 & (1 << 22):
                extras += '+copy'
            if config7 & (1 << 23):
                extras += '+macro'
            return extras
        
        except ConfigParser.Error:
            return extras

    def get_mr2(self, parser):
        try:
            config5 = int(parser.get('section 1', 'CONFIG5'), 16)
            return (config5 & (1 << 14)) != 0
        except:
            return 0
        
    def determine_isa_stuff(self, fp):
        parser = ConfigParser.ConfigParser()
        try:
            parser.readfp(fp)
            config = int(parser.get('section 1', 'CONFIG'), 16)
            r6 = ((config >> 10) & 7) == 2
            config3 = int(parser.get('section 1', 'CONFIG3'), 16)
            micromips = (config3 & 0x0000c000) != 0
            micromips_only = (config3 & 0x00004000) != 0
            mm_rev = (config3 & 0x001C0000)
            nanomips = r6 and micromips_only and mm_rev >= 0x000C0000
            endian = (config & 0x00008000) != 0
            tcb_b = int(parser.get('section 1', 'TCBCONTROLB'), 16)
            show_markers = (tcb_b & (1 << 11)) != 0
            has_mt = (config3 & 4) != 0
            multicore = is_multicore(parser)
            is_32bit = (config & 0x6000) == 0
            mr2 = self.get_mr2(parser)
            core_details = (is_32bit << 2) + (multicore << 1) + has_mt
            tcb_a = int(parser.get('section 1', 'TCBCONTROLA'), 16)
            show_im = (tcb_a & (1 << 1)) != 0
            show_lsm = (tcb_a & (1 << 2)) != 0
            show_fcr = (tcb_a & (1 << 3)) != 0
            return r6, micromips, nanomips, mr2, self.determine_isa_extras(parser), endian, show_markers, show_im, show_lsm, show_fcr, core_details
        
        except ConfigParser.Error:
            return False, False, False, False, "", False, False, False, False, False, 0
    
    
    def determine_fdt(self, fp):    
        parser = ConfigParser.ConfigParser()
        try:
            parser.readfp(fp)
            cfg3 = int(parser.get('section 1', 'CONFIG3'), 16)
            is_flow = False
            if self.is_bit_set(cfg3, 8):
                is_flow = True
                ifctl = int(parser.get('section 1', 'IFCTL'), 16)
                is_fdt = self.is_bit_set(ifctl, 13)
                iflow3 = ((ifctl >> 16) & 3) > 0
            else:
                tcbcontrolB = int(parser.get('section 1', 'TCBControlB'), 16)
                is_fdt = self.is_bit_set(tcbcontrolB, 17)
                iflow3 = 0
            return is_fdt, iflow3, is_flow
        
        except ConfigParser.Error:
            return False, False, False    

    def is_bit_set(self, value, bitpos):
        return (value & (1 << bitpos)) != 0

    def field_is(self, value, bitpos, mask, match):
        return match == ((value >> bitpos) & mask)
        
    def determine_ldstinfo(self, fp):
        parser = ConfigParser.ConfigParser()
        try:
            VMODES = 24
            VMODES_MASK = 3
            LDST_AD = 2
            TRACE_MODE = 23
            parser.readfp(fp)
            tcbcontrola = int(parser.get('section 1', 'TCBControlA'), 16)
            tcbcontrolc = int(parser.get('section 1', 'TCBControlC'), 16)
            tracePC = self.is_bit_set(tcbcontrolc, TRACE_MODE)
            traceLA = self.is_bit_set(tcbcontrolc, TRACE_MODE + 1)
            traceSA = self.is_bit_set(tcbcontrolc, TRACE_MODE + 1)
            traceLD = self.field_is(tcbcontrola, VMODES, VMODES_MASK, LDST_AD) and self.is_bit_set(tcbcontrolc, TRACE_MODE + 3)
            traceSD = self.field_is(tcbcontrola, VMODES, VMODES_MASK, LDST_AD) and self.is_bit_set(tcbcontrolc, TRACE_MODE + 4)
            return tracePC, traceLA, traceSA, traceLD, traceSD
        
        
        except ConfigParser.Error:
            return False, False, False, False, False  

    def is_multicore(self):
        return (self.core_details & 2) != 0
    
    def is_32bit(self):
        return (self.core_details & 4) != 0

class TraceFrame(object):   
    tc_isa = {}  
    tc_asid = {} 
    
    frmnum_regexp = re.compile(r"^(\s*\d+.\d+)(.*)")
    addr_regexp = re.compile(r"pc\s+(0x[a-fA-F0-9]+:)?(0x[a-fA-F0-9]+)")
    isa_regexp = re.compile(r"isa=(\w+)")
    cpu_tc_regexp = re.compile(r"\s(\d+) (\d+)(\s.*)") 
    tc_regexp = re.compile(r"^\s*(\d+)(\s.*)")
    asid_regexp = re.compile(r"asid=(\w+)")
    
    def extract_framenum(self, text):
        m = TraceFrame.frmnum_regexp.search(text)
        return (m.group(1), m.group(2)) if m else (None, None)
    
    def extract_frameaddr(self, text):
        m = TraceFrame.addr_regexp.search(text)
        return (m.group(2)) if m else None

    def extract_isa(self, text, isa):
        m = TraceFrame.isa_regexp.search(text)
        return m.group(1).lower() if m else isa.lower()

    def extract_asid(self, text, asid):
        m = TraceFrame.asid_regexp.search(text)
        return int(m.group(1), 16) if m else asid
        

    def extract_tc(self, text):
        m = TraceFrame.cpu_tc_regexp.search(text)
        if m:
            return (int(m.group(1)), int(m.group(2)), m.group(3))
        m = TraceFrame.tc_regexp.search(text)
        return (None, int(m.group(1)), m.group(2)) if m else (None, None, text)
        
    def get_tc_isa(self, tc):
        if tc is None:
            tc = 0
        try:
            return TraceFrame.tc_isa[tc]
        except KeyError, e:
            TraceFrame.tc_isa[tc]="mips32"
            return TraceFrame.tc_isa[tc]        

    def get_tc_asid(self, tc):
        if tc is None:
            tc = 0
        try:
            return TraceFrame.tc_asid[tc]
        except KeyError, e:
            TraceFrame.tc_asid[tc]= 0
            return TraceFrame.tc_asid[tc]        

        
    def __init__(self, buffer, is_r6):
        text = buffer
        self.frame_number, self.text = self.extract_framenum(text)
        if self.frame_number is not None:
            self.cpu, self.tc, self.text = self.extract_tc(self.text)
            
            self.address = self.extract_frameaddr(self.text)
            self.isa = self.extract_isa(self.text, self.get_tc_isa(self.tc))
            self.asid = self.extract_asid(self.text, self.get_tc_asid(self.tc))
            TraceFrame.tc_isa[self.tc if self.tc else 0] = self.isa
            TraceFrame.tc_asid[self.tc if self.tc else 0] = self.asid
            self.is_r6 = is_r6
            self.mem_available = 'Code memory unavailable' not in self.text
        
        else:
            self.text = buffer
            self.address = None

    def __str__(self):
        if self.frame_number is None:
            return self.text
        
        if self.cpu is not None:
            if self.tc is None:
                tc = 0
            return "%s %d %d %s" % (self.frame_number, self.cpu, self.tc, self.text)
        elif self.tc is None:
            return "%s %s" % (self.frame_number, self.text)
        else:
            return "%s  %d %s" % (self.frame_number, self.tc, self.text)

   
    def format(self, disasm, mem_map, decoder, info, use_asid, device):
        return str(self)

def connect_socket(location, port):
    start = time.time()
    while 1:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((location, port))
            return sock
        except Exception:
            if (time.time() - start) > 10:
                raise
            time.sleep(0.1) 
            
            
def run_process(cmd_args, cwd, show_window = False, env=None):
    if 0:
        print ' '.join(cmd_args)
        print env
    return subprocess.Popen(cmd_args, cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)


def get_dqer_path():
    DQER_NAME = 'CSDQer.jar'
    path = config(console, 'dqer_path')
    if path:
        if os.path.isfile(path):
            return path
        else:
            return os.path.join(path, DQER_NAME)
    
    # If not explicitly set, then look for a min dqer in the imgtec.codescape dir
    from imgtec.codescape import _get_default_dqer_directory
    path = os.path.join(_get_default_dqer_directory(), DQER_NAME)
    if os.path.isfile(path):
        return path

def get_line_from_process(process, pipe):
    return pipe.get_line() if pipe else process.stdout.readline()
    
def get_line_from_process_stdout(process, pipe):
    line = get_line_from_process(process, pipe)
    start = time.time()
    while line == '' and (time.time() - start) < 10 :
        line = get_line_from_process(process, pipe)
        
    return line
    
    
def run_dequeuer(configpath, port0, respect_asid, options, outputbin):
    java_path = config(console, 'java_path')
    dqer = get_dqer_path()
    if not dqer:
        raise RuntimeError('Invalid DQer path, please configure using config(console, "dqer_path", "Path to folder containing DQer")')
    
    dequeuer_path, dqer_name = os.path.split(dqer)
    
    core_index = 'cm' if options['cm'] else str(options['core_index'])
    
    core_cmd = 'src' if core_index == 'cm' else 'core'

    cmd_args =[java_path,
               "-jar",
               dqer_name,
               configpath,
               "-port",
               str(port0),
               core_cmd, 
               core_index, # TODO - Needs core index here
               "-df2",
               "-mfh",
               ]
    if options.get('rng', False):
        cmd_args.append('-fr')
        cmd_args.append(options['rng'])

    if respect_asid:
        cmd_args.append('-respasid')
    if options['show_asid']:
        cmd_args.append('-showasid')
        
    if options['save_decoded']:
        cmd_args.append('-outbinfile')
        cmd_args.append('mdi')
    elif outputbin:
        cmd_args.append('-outbin')
    elif options['mode'] == 'show_stdout' and options['dasm'] == True:
        cmd_args.append('dasm')
        
    #rng = options['range']
    #if rng == 'all':
        # Here we look at whether we stop when buffer full or
        # or not set either first or last 50000 frames
    #    cmd_args.append(rng)
    #elif '..' in rng:
    #    cmd_args.append('fr')
    #    cmd_args.append(rng)
    #else:
    #    rng = rng.split()
    #    cmd_args.extend(rng)
    cmd_args.append('all')
    if options['mode'] == 'tm':
        cmd_args.append('tm')
    elif options['mode'] == 'raw':
        cmd_args.append('raw')
    env = None
    if 'CODESCAPE_NATIVE_LIBRARY' not in os.environ:
        from imgtec.codescape import _DAscript
        env = dict(os.environ, CODESCAPE_NATIVE_LIBRARY=_DAscript.__file__)
    process = run_process(cmd_args, cwd=dequeuer_path, env=env, show_window = False)
    #time.sleep(0.5) # warm up time (!)
    if process.poll() is not None:
        raise RuntimeError('Process has closed with errorcode %d' % (process.returncode,))

    line = get_line_from_process_stdout(process, None)
    ports = re.match(r'(\d+),(\d+)$', line)
    if not ports:
        output = line + process.stdout.read()
        raise RuntimeError('Unable to determine ports for communications:\n  DQer output: {}'.format(output))
        
    port0, port1 = int(ports.group(1)), int(ports.group(2))
    path = None
    if options['save_decoded']:
        path = get_line_from_process_stdout(process, None)
        path = path.strip()
        if path == '':
            raise RuntimeError('Unable to determine trace output file.')
        
    return process, port0, port1, path

class TraceData(object):
    def __init__(self, process, is_r6, isa, for_list):
        
        self.process = process
        self.isa = isa
        self.is_r6 = is_r6
        self.dequeued = []
        self.queue = Queue()
        self.for_list = for_list
    
        self.t = Thread(target=self.enqueue_output, )
        self.t.daemon = True
        self.t.start()

    def enqueue_output(self):
        for line in iter(self.process.stdout.readline, ''):
            self.queue.put(line)
        return

    def join(self):
        self.t.join(2.0)

    def build_frames(self, line):
        frames = []
        if not line.startswith("End of"):
            frame = TraceFrame(line, self.is_r6)
            if self.for_list:
                frames.append(str(frame))
            else:
                print str(frame)
            
        return frames

    def get_line(self):
        while 1:            
            try:
                return self.queue.get_nowait()
            except Empty:
                return ''

    def handle(self):
        while 1:
            line = self.get_line().rstrip() #self.queue.get_nowait() #  self.process.stdout.read()
            if line == '':
                return
            new_frames = self.build_frames(line)
            self.dequeued.extend(new_frames)
            
    def close(self):
        pass
    
from imgtec.lib.namedstruct import namedstruct

dequeued_data = namedstruct(
'dequeued_data',
(
    'Q frame_num = 0',
    'Q addr = 0',
    'Q value = 0',
    'I type = 0',
    'I fields = 0',
    'I meta_data = 0',
    'I meta_data2 = 0',
    'i meta_data3 = 0'
),
'>'
)


class TraceFrame2(object):   
    isa_strings = trace_type_decode.isa_string #["mips32", "mips64", "mips16", "mips32"]
    isa_16bits = ["mips16", "micromips"]
        
    
    
    IS_FCR  = 1
    IS_LSM  = 2
    IS_IM   = 4 
    UPR128 = 8
    MISALIGNED = 16
    MSA = 32
    OVERFLOW = 64
    
    sync_frame_types = [int(TraceTypes.HDI_TRACETYPE_MODE_INIT),
                        int(TraceTypes.HDI_TRACETYPE_MODE_CHANGE),
                   int(TraceTypes.HDI_TRACETYPE_IPC_SYNC),
                   int(TraceTypes.HDI_IFLOW_3_SYNC_INFO)]    
    
    tc_isa = {}
    tc_asid = {} 
    isas = ['mips32', 'mips64', 'mips16', 'micromips', 'nanomips']
    dequeued = dequeued_data()
    TRACE_DATA_LENGTH = dequeued._size
    TRACE_FRAME_LENGTH = TRACE_DATA_LENGTH + 12
    
    def get_tc_isa(self, tc):
        if tc is None:
            tc = 0
        try:
            return TraceFrame2.tc_isa[tc]
        except KeyError, e:
            TraceFrame2.tc_isa[tc]="mips32"
            return TraceFrame2.tc_isa[tc]        
        
        
    def get_tc_asid(self, tc):
        if tc is None:
            tc = 0
        try:
            return TraceFrame2.tc_asid[tc]
        except KeyError, e:
            TraceFrame2.tc_asid[tc]= 0
            return TraceFrame2.tc_asid[tc]        

    def extract_isa(self, is_micromips, is_nanomips, tc):
        if self.type in TraceFrame2.sync_frame_types:
            isa = (self.value >> 11) & 3
            isa_str = self.isa_strings[isa]
            if isa == 2 and is_micromips:
                isa_str = "microMIPS"
              
            if is_nanomips:
                isa_str = "nanoMIPS"
            TraceFrame2.tc_isa[tc] = isa_str
            # Need to determine if microMips and add in r6
            # store in TraceFrame.tc_isa
        else:
            isa_str = self.get_tc_isa(tc)
        
        return isa_str
        
    def __init__(self, buffer, offset, target_info, frm_num = None, value = None):
        if buffer:
            self.dequeued_data = dequeued_data._unpack_from(buffer, offset)
            self.tc = (self.fields >> 16) & 0xff
            if self.tc == 0xff:
                self.tc = 0
            self.core = (self.fields >> 24) & 0xff
            if self.core == 0xff:
                self.core = 0
            self.isa = self.extract_isa(target_info.is_micromips, target_info.is_nanomips, self.tc)
    
            self.asid = self.extract_asid(self.tc)
            TraceFrame2.tc_isa[self.tc] = self.isa
            self.mem = b'\xff\xff\xff\xff'
            self.target_info = target_info
        else:
            self.dequeued_data = dequeued_data(frame_num = frm_num, value = value, type = TraceTypes.HDI_IMON_DATA)
            self.tc = 0
            self.core = 0
            self.isa = self.extract_isa(False, False, self.tc)
            self.asid = self.extract_asid(self.tc)
            TraceFrame2.tc_isa[self.tc if self.tc else 0] = self.isa
            self.mem = b'\xff\xff\xff\xff'
            
    @property
    def frame_number(self):
        return self.dequeued_data.frame_num
    
    @property
    def addr(self):
        return self.dequeued_data.addr
    
    @property
    def value(self):
        return self.dequeued_data.value
    
    @property
    def type(self):
        return self.dequeued_data.type
    
    @property
    def fields(self):
        return self.dequeued_data.fields
    
    @property
    def meta_data(self):
        return self.dequeued_data.meta_data
    
    @property
    def meta_data2(self):
        return self.dequeued_data.meta_data2
    
    @property
    def meta_data3(self):
        return self.dequeued_data.meta_data3
    
    def find_isa_index(self, isa):
        try:
            return TraceFrame2.isas.index(isa.lower())
        except ValueError as e:
            return 0
    
    def save_frame(self, fp):
        data = self.dequeued_data._pack()
        fp.write(data)
        data = struct.pack('>I', self.find_isa_index(self.isa))
        fp.write(data)
        data = struct.pack('>I', self.asid)
        fp.write(data)
        fp.write(self.mem)
        
    
    @classmethod
    def load_frame(cls, fp, target_info):
        size = TraceFrame2.TRACE_DATA_LENGTH + 12
        frm = fp.read(size)
        if frm and len(frm) == size:
            trace_frame = TraceFrame2(frm, 0, target_info)
            isa_index = struct.unpack_from('>I', frm, trace_frame.dequeued_data._size)[0]
            trace_frame.asid = struct.unpack_from('>I', frm, trace_frame.dequeued_data._size + 4)[0]
            trace_frame.mem = frm[trace_frame.dequeued_data._size + 8:]
            trace_frame.isa = TraceFrame2.isas[isa_index]
            return trace_frame
            
        else:
            raise RuntimeError('Unknown file format')
            

    def get_asid(self):
        return self.asid

    def extract_asid(self, tc):
        try:
            asid =  TraceFrame2.tc_asid[self.tc]
        except KeyError:
            asid = 0
        if self.type == TraceTypes.HDI_TRACETYPE_MODE_INIT or\
                self.type == TraceTypes.HDI_TRACETYPE_MODE_CHANGE:
            asid = self.meta_data
            if asid == 0:
                asid = self.value & 0xff
            TraceFrame2.tc_asid[self.tc] = asid
                
        elif self.type == TraceTypes.HDI_TRACETYPE_IPC_SYNC:
            asid = self.value & 0xff
            TraceFrame2.tc_asid[self.tc] = asid
        elif self.type == TraceTypes.HDI_IFLOW_3_SYNC_INFO:
            asid = self.meta_data2 & 0xff
            TraceFrame2.tc_asid[self.tc] = asid
        return asid

    def getcontextid(self):
        if self.type == TraceTypes.HDI_TRACETYPE_PCV or self.type == TraceTypes.HDI_TRACETYPE_TRIGGER_INFO:
            return 'X'
        else:
            return str(self.tc)

    def get_core_tc(self, decoder):
        if decoder.target_info.has_vpid:
            return "%d %s 0" % (self.core, self.getcontextid())
        elif decoder.is_multicore() and decoder.has_mt():
            return "%d %s" % (self.core, self.getcontextid())
        elif decoder.is_multicore():
            return "%d" % (self.core)
        elif decoder.has_mt():
            return "%s" % (self.getcontextid())
        else:
            return ""
            

    def as_str(self, decoder):
        # May need to change this for MC
        return "%s %s %s" % (self.get_frame_num(), self.get_core_tc(decoder), self.get_trace_data(decoder))

    def calculate_frame_num(self, twsize):
        divisor = 100.0 if twsize == 1 else 1000.0
        return self.frame_number / divisor
    
    def create_frame_num(self, num, twsize):
        multiplier = 100.0 if twsize == 1 else 1000.0
        return num * multiplier
    
    
    def get_frame_num(self):
        twsize = self.target_info.twsize
        divisor = 100.0 if twsize == 1 else 1000.0
        fmt = "%9.2f" if twsize == 1 else "%9.3f"
        return fmt % (self.calculate_frame_num(twsize))
    
    
    def get_trace_data(self, decoder):
        markers = False
        is_flow = False
        return decoder.decode_trace_type(self, is_flow = is_flow)


    def get_dasm(self, disasm, mem_map, mr2, isa_extras, endian, use_asid, device):
        dasm_str = ""
        if disasm and self.type == TraceTypes.HDI_TRACETYPE_PC:  #and self.mem_available:
            data = self.mem #self.extract_data(endian, mem_map, use_asid)
            isa = self.isa.lower()
            if mr2 and isa == 'mips16':
                isa = isa + 'e2'
            isa = (isa + 'r6') if self.target_info.has_r6() else isa
            isa = isa + isa_extras
            if data:
                disasm_ops =  dasmbytes(self.addr, data, isa = isa, device = device)[0]
            elif len(mem_map) == 0:
                disasm_ops =  dasm(self.addr, isa = isa, device=device)[0]
            else:
                return str(self)
            filler = ' ' * (8 - disasm_ops.size*2)
            op = disasm_ops.ops[0]
            opcode = disasm_ops.opcode
            dasm_str = "   %s%s%2s%r" % (opcode, filler, '', op)
        return dasm_str

    def format(self, disasm, mem_map, decoder, info, use_asid, device):
        return self.as_str(decoder) + self.get_dasm(disasm, mem_map, info.mr2, info.isa_extras, info.endian, use_asid, None)

    
   
    def is_ipc_sync(self):
        return self.type == TraceTypes.HDI_TRACETYPE_IPC_SYNC

    def is_exec_frame_type(self):
        return self.type == TraceTypes.HDI_TRACETYPE_PC or self.type == TraceTypes.HDI_TRACETYPE_INST \
                or self.type == TraceTypes.HDI_TRACETYPE_IDLE_SLOT
      
    def isIM(self):
        return (self.fields & self.IS_IM) != 0
    
    def isLSM(self):
        return (self.fields & self.IS_LSM) != 0
    
    def isFCR(self):
        return (self.fields & self.IS_FCR) != 0 
      
    def isOverflow(self):
        return (self.fields & self.OVERFLOW) != 0 
    
    def isMsa(self):
        return (self.fields & self.MSA) != 0 
                 
    def isUPR128(self):
        return (self.fields & self.UPR128) != 0 
         
    def nbytes(self):
        nb = (self.fields & 0xff00) >> 8 
        return nb
        
    def is_exec_frame(self):
        return self.is_exec_frame_type() and not self.isIM() and \
                not self.isLSM() and not self.isFCR()
    
    def is_info_frame(self):
        return self.type == TraceTypes.HDI_TRACETYPE_MODE_INIT or self.type == TraceTypes.HDI_TRACETYPE_MODE_CHANGE

    def is_idle_frame(self):
        return self.type == TraceTypes.HDI_TRACETYPE_IDLE_CYCLES or \
                self.type == TraceTypes.HDI_TRACETYPE_BACKSTALL_CYCLES or \
                self.type == TraceTypes.HDI_TRACETYPE_GAP
                
    def is_no_instr_exe(self):
        return self.type == TraceTypes.HDI_TRACETYPE_NO_INSTR_EXE
              
    def is_timestamp_frame(self):
        return self.type == TraceTypes.HDI_TRACETYPE_TS
    
    def is_user_msg(self, msg):
        return self.type == TraceTypes.HDI_TRACETYPE_UTM and self.addr == msg
    
    def get_disasm(self):
        return self.disasm

    def set_disasm(self, disasm):
        self.disasm = disasm
        
    def set_src(self, src):
        self.src = src.lstrip()

    def set_src_loc(self, loc):
        self.src_loc = loc
        
    def get_src(self):
        if self.src is None:
            if self.type == TraceTypes.HDI_TRACETYPE_PC or self.type == TraceTypes.HDI_BL_INTERRUPTED:
                self.src = ""
            else:
                self.src = ""
        return self.src
    
    def get_srcloc(self):
        if self.src is None:
            if self.type == TraceTypes.HDI_TRACETYPE_PC or self.type == TraceTypes.HDI_BL_INTERRUPTED:
                self.src_loc = ''
            else:
                self.src_loc = ""
        return self.src_loc


class TraceCollector(object):
    
    def __init__(self, sock, imon, num_frames, target_info, mem_map, use_asid, options):
        # The socket will likely be passed in as it will be the same used to send the data
        self.sock = sock
        self.dequeued = []
        self.isa = 0
        self.remaining = ''
        self.num_frames = num_frames
        self.target_info = target_info
        self.mem_map = mem_map
        self.use_asid = use_asid
        self.decoder = trace_type_decode(options['show_asid'], target_info)
        self.fp = None
        self.imon = imon
        self.dasm = options['dasm']
        self.for_list = options['for_list']
        self.twsize = target_info.twsize

    def close(self):
        if self.fp:
            self.fp.close()
            self.fp = None
            
    def fileno(self):
        return self.sock.fileno()

    def have_a_full_frame(self, chunk, offset):
        chunklen = len(chunk)
        return offset + TraceFrame2.TRACE_DATA_LENGTH <= chunklen
    
    def frame_length(self, chunk, offset):
        return TraceFrame2.TRACE_DATA_LENGTH
    
    def display_frame(self, frame, frames):
        if self.fp:
            frame.save_frame(self.fp)
        else:
            s = frame.format(self.dasm, None, self.decoder, self.target_info, self.use_asid, None)
            if self.for_list:
                frames.append(s)
            else:
                print s

    def build_frames(self, chunk):
        frames = []
        offset = 0
        while self.have_a_full_frame(chunk, offset):
            frame = TraceFrame2(chunk, offset, self.target_info)
            offset += TraceFrame2.TRACE_DATA_LENGTH #self.frame_length(chunk, offset)
            if frame.type == TraceTypes.HDI_TRACETYPE_PC:
                asid = frame.asid if self.use_asid else 0xffff
                mem = extract_bytes(frame.addr, frame.isa, self.target_info.endian, self.mem_map, asid)
                if mem:
                    frame.mem = mem
            
            elif frame.type == 0xffffffff:
                data = struct.pack('!I', 0xffffffff)
                self.sock.send(data)
                break
            
            if self.imon:
                frame_num, imon_data = self.imon[0]
                fr = int(frame.calculate_frame_num(self.twsize))
                while frame_num < fr:
                    del self.imon[0]
                    if not self.imon:
                        break
                    frame_num, imon_data = self.imon[0]
                    
                if frame_num == int(frame.calculate_frame_num(self.twsize)):
                    imon_frame = TraceFrame2(None, None, None, frm_num = frame.create_frame_num(frame_num, self.twsize), value = imon_data)
                    del self.imon[0]
                    # For now omit imon display until we have a fix and know exactly how to display it
                    #self.display_frame(imon_frame, frames)
                
            self.display_frame(frame, frames)

        return frames, chunk[offset:] # frames,   chunk[offset:]
        
    def handle(self):
        try:
            chunk = self.sock.recv(8192)
            if chunk == '':
                return
            #print "Chunk length = ", len(chunk)
            new_frames, self.remaining = self.build_frames(self.remaining + chunk)
            self.dequeued.extend(new_frames)
        
        except Exception, e:
            new_frames, self.remaining = self.build_frames(self.remaining)
            self.sock.close()    
            self.dequeued.extend(new_frames)
            print e
            raise
        
    def amount_done(self):        
        if self.dequeued:
            last_frame = self.dequeued[-1].frame_number / 100
            return 100 * last_frame / self.num_frames
        return 0

def find_asid_memory(mem_map, core_id, guest_id, pom, asid):
    try:
        core_mem = mem_map[core_id]
        guest_mem = core_mem[guest_id]
        virtual_mem = guest_mem[pom]
        return virtual_mem[asid]
    except KeyError, e:
        if asid == 0xffff:
            return {}
        else:
            return find_asid_memory(mem_map, core_id, guest_id, pom, 0xffff)


def build_asid_memory(mem_map, core_id, guest_id, pom, asid):
    try:
        core_mem = mem_map[core_id]
    except KeyError, e:
        core_mem = {}
        mem_map[core_id] = core_mem

    try:
        guest_mem = core_mem[guest_id]
    except KeyError, e:
        guest_mem = {}
        core_mem[guest_id] = guest_mem
        
    try:
        virtual_mem = guest_mem[pom]
    except KeyError, e:
        virtual_mem = {}
        guest_mem[pom] = virtual_mem
        
    try:
        # If mmu off, asid = 0
        asid_mem = virtual_mem[asid]
    except KeyError, e:
        asid_mem = {}
        virtual_mem[asid] = asid_mem
        
    return asid_mem

class TraceMemReadException(Exception):
    pass

class TraceMemoryReader(object):
    def __init__(self, device, port, save_files, path, save_decoded, is_32bit):
        #self.socket = socket.create_connection(('localhost', port))
        
        self.socket = connect_socket('localhost', port)
        self._device = device
        self.save_files = save_files and not save_decoded
        self.path = path
        self.mem_map = {}
        self.load_mem_files(save_files, path)
        self.is_32bit = is_32bit
        
    def find_asid_mem(self, core_id, guest_id, pom, asid):
        return build_asid_memory(self.mem_map, core_id, guest_id, pom, asid)

    def load_mem_files(self, save_files, path):
        self.mem_loaded = False
        if not save_files and path:
            filename = 'trace*.mem'
            files = glob.glob(os.path.join(path, filename))
            for file in files:
                core_id, guest_id, pom, asid, addr, data = self.read_chunk(file)
                asid_mem = self.find_asid_mem(core_id, guest_id, pom, asid)
                asid_mem[addr] = data
                
            self.mem_loaded = True        
      
    def read_chunk(self, pathname):
        with open(pathname, "rb") as f:
            address = f.read(4)
            address, = struct.unpack('>I', address)
            if (address & 0xff) != 0xff:
                data = f.read()
                return 0xffff, 0xffff, 0xffff, 0, address, data
            else:
                header = f.read(16)
                core_id, guest_id, pom, asid, addr = struct.unpack(">HHHHQ", header)
                data = f.read()
                return core_id, guest_id, pom, asid, addr, data            
                
     
    def save_asid_mem(self, core_id, guest_id, pom, asid, asid_mem, count):
        addr = 0
        data = ""
        compress = {}
        for key in sorted(asid_mem.keys()):
            length = len(data)
            if (addr + length) == key:
                data += asid_mem[key]
            else:
                if length:
                    compress[addr] = data
                addr = key
                data = asid_mem[key]
             
        if len(data):
            compress[addr] = data
            
        for key in compress.keys():
            try:
                self.save_chunk(self.path, key, compress[key], core_id, guest_id, pom, asid, count)
                count += 1
            except Exception, e:
                print e
     
        return count
      
    def save_mem_files(self):
        if self.save_files and self.path:
            count = 0
            for core_id in self.mem_map.keys():
                core_mem = self.mem_map[core_id]
                for guest_id in core_mem.keys():
                    guest_mem = core_mem[guest_id]
                    for pom in guest_mem.keys():
                        pom_mem = guest_mem[pom]
                        for asid in pom_mem.keys():
                            asid_mem = pom_mem[asid]
                            
                            count = self.save_asid_mem(core_id, guest_id, pom, asid, asid_mem, count)
            
    # def save_mem_filesold(self):
        # if self.save_files and self.path:
            # for key in sorted(self.mem_map.keys()):
                # length = len(data)
                # if (addr + length) == key:
                    # data += self.mem_map[key]
                # else:
                    # if length:
                        # compress[addr] = data
                    # addr = key
                    # data = self.mem_map[key]
                 
            # if len(data):
                # compress[addr] = data
                
            # count = 0
            # for key in compress.keys():
                # try:
                    # self.save_chunk(self.path, key, compress[key], count)
                    # count += 1
                # except Exception, e:
                    # print e
            
    def save_chunk_old(self, path, addr, data, count):
        filename = "trace%d.mem" % (count,)
        pathname = os.path.join(path, filename)
        with open(pathname, "wb") as f:
            address = struct.pack('>I', addr)
            f.write(address)
            f.write(data)
      
    def save_chunk(self, path, addr, data, core_id, guest_id, pom, asid, count):
        filename = "trace%d.mem" % (count,)
        pathname = os.path.join(path, filename)
        with open(pathname, "wb") as f:
            version = struct.pack('>I', 0x010000ff)
            f.write(version)
            f.write(struct.pack('>H', core_id))
            f.write(struct.pack('>H', guest_id))
            f.write(struct.pack('>H', pom))
            f.write(struct.pack('>H', asid))
            address = struct.pack('>Q', addr)
            f.write(address)
            f.write(data)

    
    def fileno(self):
        return self.socket.fileno()

    def read_uint16(self):
        data = self.socket.recv(2)
        return -1 if len(data) != 2 else struct.unpack('!H', data)[0]
        
    def read_uint32(self):
        data = self.socket.recv(4)
        return -1 if len(data) != 4 else struct.unpack('!I', data)[0]
        
    def read_uint64(self):
        data = self.socket.recv(8)
        return -1 if len(data) != 8 else struct.unpack('!Q', data)[0]

    def write_uint32(self, value):
        data = struct.pack('!I', value)
        self.socket.send(data)
    
    def determine_device(self, core_index):
        if core_index == 0xffff:
            return self._device
        
        #TODO - Find device from core index
        return self._device
    

    
    def read_memory_from_target(self, core_index, guest_id, pom, tasid, address, size):
        last_asid = asid()
        asid(-1 if tasid == 0xffff else tasid)
        device = self.determine_device(core_index)
        try:
            data = byte(address, count=size, device=device)
            data = struct_pack(data, 1, False)
        except Exception, e:
            data = "" 
         
        asid_mem = self.find_asid_mem(core_index, guest_id, pom, tasid)
        asid_mem[address] = data
        asid(last_asid)
        return data
    
    def read_memory_from_map(self, core_index, guest_id, pom, asid, address, size):
        asid_mem = self.find_asid_mem(core_index, guest_id, pom, asid)
        for k, v in asid_mem.items():
            if k <= address < k + len(v):
                offset = address - k
                if offset + size <= len(v):
                    return v[offset:offset + size]
                else:
                    return v[offset:]
        if asid != 0xffff:
            return self.read_memory_from_map(core_index, guest_id, pom, 0xffff, address, size)
        return "\0" * size 
                
    def read_memory(self):
        asid = self.read_uint32()
        address = self.read_uint64()
        address &= 0xffffffff
        size = self.read_uint32()
        if self.mem_loaded:
            data = self.read_memory_from_map(0xffff, 0xffff, 0xffff, asid, address, size)
        else:
            data = self.read_memory_from_target(0xffff, 0xffff, 0xffff, asid, address, size)
        
        self.write_uint32(self.memory_read)
        self.write_uint32(len(data))
        self.socket.send(data)
    
    def read_memory_v1(self):
        core_index = self.read_uint16()
        guest_id = self.read_uint16()
        pom = self.read_uint16()
        asid = self.read_uint16()
        address = self.read_uint64()
        size = self.read_uint32()
        if self.mem_loaded:
            data = self.read_memory_from_map(core_index, guest_id, pom, asid, address, size)
        else:
            if self.is_32bit and address >= 0x100000000:
                address &= 0xffffffff
            data = self.read_memory_from_target(core_index, guest_id, pom, asid, address, size)
        
        self.write_uint32(self.memory_read_v1)
        self.write_uint32(len(data))
        self.socket.send(data)
    memory_read = 1
    memory_read_v1 = 2
    
    def handle(self):
        try:
            cmd = self.read_uint32()
            if cmd == self.memory_read:
                try:
                    self.read_memory()
                except Exception, e:
                    print e
            elif cmd == self.memory_read_v1:
                try:
                    self.read_memory_v1()
                except Exception, e:
                    print e
            elif cmd == -1:
                raise TraceMemReadException('Trace completed')
            else:
                raise RuntimeError('Unknown memory command.')
        except socket.timeout:
            print 'timeout'
            

       
class Uploader(object):
    def __init__(self, port, frames):
        self.sock = socket.create_connection(('localhost', port))
        self.frames = struct.pack('<%dQ' % len(frames), *frames)
        self.offset = 0

    def fileno(self):
        return self.sock.fileno()

    def send_header(self, sock, length):
        try:
            hdr = struct.pack(">i", length)
            sock.send(hdr)
        except Exception, e:
            pass

    def handle(self):
        chunk_size = 4096
        length = len(self.frames)
        remaining = length - self.offset
        if  remaining > 0:
            amount = chunk_size if remaining > chunk_size else remaining

            self.send_header(self.sock, amount)
            s = self.frames[self.offset:self.offset + amount]
            self.sock.send(s)
            self.offset += amount
            if self.done():
                try:
                    self.send_header(self.sock, 0)
                    
                except Exception, e:
                    pass
                
    def amount_done(self):
        return 100 * self.offset / len(self.frames)
    
    def done(self):
        return self.offset == len(self.frames)
    
    def upload_all(self):
        while not self.done():
            self.handle()


class Uploader2(object):
    def __init__(self, port, frames):
        self.sock = socket.create_connection(('localhost', port))
        #self.frames = struct.pack('<%dQ' % len(frames), *frames)
        self.frames = frames
        self.all_sent = False
        self.sent = 0
        self.frame_sent = 0
        self.uploaded = 0
        self.imon = []
        
    def fileno(self):
        return self.sock.fileno()

    def send_header(self, sock, length):
        try:
            if self.sent == 0:
                hdr = struct.pack(">i", -1) #, self.frames.end_addr)
                sock.send(hdr)
                hdr = struct.pack(">i", self.frames.start_frame)
                sock.send(hdr)
            hdr = struct.pack(">i", length)
            sock.send(hdr)
        except Exception, e:
            pass

    def handle(self):
        if self.all_sent:
            return
        chunk_size = 32768
        frames, imon_data = self.frames.read(chunk_size)
        if len(frames) == 0:
            try:
                self.send_header(self.sock, 0)
                
            except Exception, e:
                pass
            self.all_sent = True
            return
        
        frames = struct.pack('<%dQ' % len(frames), *frames)
        
        amount = len(frames)
        self.uploaded += amount

        self.send_header(self.sock, amount)
        self.sock.send(frames)
        self.sent += chunk_size
        self.frame_sent += amount/8
        self.imon.extend(imon_data)
                
    def amount_done(self):
        return 100 * 0 / len(self.frames)
    
    def done(self):
        return self.all_sent
    
    def upload_all(self):
        while not self.done():
            self.handle()



    
def is_micromips(device):
    info = cpuinfo(device)
    return "has_micromips" in info and info["has_micromips"]

from contextlib import contextmanager
@contextmanager
def NullDevice():
    yield
   
def find_core(lines, core_index):
    for line in lines:
        if line.lower().startswith('core='):
            try:
                if int(line[5:]) == core_index:
                    return True
            except ValueError:
                pass
            
    return False
   
def find_config_for_core(config, core_index):
    lines = config.splitlines()
    for line in range(0, len(lines)):
        if lines[line].lower().startswith('[section 1]'):
            for next in range(line + 1, len(lines)):
                if lines[next].lower().startswith('[section 1]'):
                    if find_core(lines[line:next], core_index):
                        return '\n'.join(lines[line:next])
            
            if find_core(lines[line:], core_index):
                return '\n'.join(lines[line:])
    
    return ""
   
    
def upload_and_collect(dev_config, frames, respect_asid, options, device=None):
    # save_decoded overrides show_stdout
    if options['save_decoded'] and options['mode'] == 'show_stdout':
        options['mode'] = 'mdi'
    outputbin = not options['cm'] and options['mode'] == 'mdi'
    with device or NullDevice():
        with tempfile.NamedTemporaryFile(suffix = ".tcf", delete = False) as f:
            f.write(dev_config + '\n')
        try:
            if options['save_decoded'] and options['path']:
                save_trace_config(options['path'], find_config_for_core(dev_config, options['core_index']) )
                
            target_info = TargetInfo(dev_config, options['core_index'])
            process, port0, port1, path = run_dequeuer(f.name, 0, respect_asid, options, outputbin)
            try:
                uploader = Uploader2(port0, frames)
                memory = TraceMemoryReader(device, port1, options['save_files'], options['path'], options['save_decoded'], target_info.is_32bit())
                if outputbin:
                    collector = TraceCollector(uploader.sock, uploader.imon, frames.length(), target_info, memory.mem_map, respect_asid, options)
                else:
                    collector = TraceData(process, target_info.is_r6, "mips32", options['for_list'])
                try:
                    readers = [collector] if outputbin else []
                    readers.append(memory)
                    while 1:
                        read, write, _ = select.select(readers, [] if uploader.done() else [uploader], [], 0.1)
                        for handler in write + read:
                            handler.handle()
                        if not outputbin:                            
                            collector.handle()
                except select.error, e:
                    pass
                except socket.error, e:
                    pass    
                except TraceMemReadException, e:
                    pass
                uploader.sock.close()
                memory.socket.close()
                if not outputbin:
                    collector.handle()
                    collector.join()
                memory.save_mem_files()
                dequeued = collector.dequeued
                collector.close()
                while process.poll() is None:
                    line = process.stdout.readline()
                    
                if options['save_decoded']:
                    filename = os.path.join(options['path'], "trace.dqd")
                    shutil.copyfile(path, filename)
                    os.remove(path)
                    
                return dequeued, memory.mem_map

            except socket.error as e:
                raise RuntimeError('Unable to connect to Trace DQ\'er\nCheck firewall and port settings: ' + str(e))

        finally:
            os.remove(f.name)   

class TraceResults(list):
    def __repr__(self):
        return '' #'\n'.join(self) if self.show_repr else ''

def get_tracer(device):
    info = cpuinfo(device)
    from imgtec.console import iftrace, pdtrace
    if is_iflow_trace(device):
        return iftrace.IFTrace()
    elif is_pd_trace(device):
        return pdtrace.PDTrace()
    else:
        raise RuntimeError('No trace mechanism available')

def is_iflow_trace(device):
    info = cpuinfo(device)
    return "has_iflow_trace" in info and info["has_iflow_trace"]
    
def is_pd_trace(device):
    info = cpuinfo(device)
    return "has_pd_trace" in info and info["has_pd_trace"]
    
   
def save_trace_config(path, config, delete_old_files = True):  
    if not os.path.exists(path):
        os.makedirs(path)
    
    if delete_old_files:
        delete_trace_files(path)
    pathname = path
    tcfname = os.path.join(pathname, "trace.tcf")
    with open(tcfname, "w") as f:
        f.write(config)          
    
    return True
    
def save_dequeued_data(path, config, frames):
    save_trace_config(path, config, False)
    pathname = path
    filename = os.path.join(pathname, "trace.dqd")
    
    with open(filename, "wb") as f:
        f.write('MIPB')
        version = struct.pack('>I', 2)
        f.write(version)
        for frm in frames:
            frm.save_frame(f)

def seek_to_start(file, offset):
    offset *= TraceFrame2.TRACE_FRAME_LENGTH
    file.seek(offset, 1)

def load_dequeued_data(path, rng, dasm, target_info, decoder, for_list):
    frames = []
    hdr_size = 8
    length = os.path.getsize(path) - 8
    max_entries = length / TraceFrame2.TRACE_FRAME_LENGTH
    start, num_entries = determine_range(rng, max_entries)
    with open(path, "rb") as f:
        id = f.read(4)
        v = f.read(4)
        version = struct.unpack(">I", v)[0]
        if id == 'MIPB' and version == 2:
            seek_to_start(f, start)
            for n in range(0, num_entries):
                try:
                    frm = TraceFrame2.load_frame(f, target_info)
                    s = frm.format(dasm, None, decoder, target_info, False, None)
                    if for_list:
                        frames.append(s)
                    else:
                        print s
                except Exception as e:
                    return frames
        else:
            raise RuntimeError('Unknown file format')
    
    return frames
    
def save_trace_files(path, config, frames, twsize):
    save_trace_config(path, config)
    pathname = path
    filename = os.path.join(pathname, "trace.rtd")
    with open(filename, "wb") as f:
        write_trace_data(f, frames, twsize)

    
    return True    
    
def read_config(read_perfs, device):    
    with device:
        config = tracemode(device=device)
        return config.config(read_perfs, device)

def write_frame_num(file, num):
    s = struct.pack(">I", num)
    file.write(s)

def skip_frames(frames, to_skip):
    max_read = 1024
    while to_skip:
        cnt = min(to_skip, max_read)
        frames.read(cnt)
        to_skip -= cnt
        

def write_trace_data(file, frames, twsize, frame_start = 0, skip = 0, length = None):
    if frame_start < frames.start_frame:
        frame_start = frames.start_frame
    skip = frame_start - frames.start_frame
    
    skip_frames(frames, skip)
    skip = 0
    if length is not None:
        length *= twsize
    frame_num = 0
    while True:
        raw_frames, imon_data = frames.read(1024)
        frames_read = len(raw_frames) / twsize
        if frames_read == 0 :
            break
        
        #if skip:
        #    n = min(skip, frames_read)
        #    skip -= n
        #    raw_frames = raw_frames[n * twsize:]

        frames_left = len(raw_frames) / twsize
        if length is not None:
            if length == 0:
                break
            num_frames = min(frames_left, length) * twsize
            length -= num_frames
        else:
            num_frames = len(raw_frames)

        for n in range(0, num_frames, twsize):
            write_frame_num(file, frame_start + n / twsize)
            for i in range(0, twsize):
                # Swap word order for big endian 
                offset = twsize - (i + 1)
                s = struct.pack(">Q", raw_frames[n + offset]) 
                file.write(s)       
        
        frame_start += frames_read
        
    frames.reset()

def build_trace_data(frames, twsize, frame_start = 0, skip = 0, length = None):
    file = StringIO()
    write_trace_data(file, frames, twsize, frame_start, skip, length)
    return file.getvalue()

        
def filter_frame_num(raw_frames, twsize):
    file = StringIO()
    frame_size = 8 * twsize
    tot_frame_size = frame_size + 4
    num_frames = len(raw_frames) / tot_frame_size   
    result = []
    for n in range(0, num_frames):
        for tw in range(0, twsize):
            # Swap to word order to little endian
            offset = 8 * (twsize - (tw + 1))
            offset += tot_frame_size * n + 4
            frame = struct.unpack(">Q", raw_frames[offset:offset + 8])
            result.append(frame[0])
    
    return result    
    
def WaitExit(process):
    while process.poll() is None:
        pass

version_regexp = re.compile(r"^.*\"(\d+).(\d+).*\".*")
    
def ReadJavaOutput(process):
    while 1:
        line = process.stdout.readline()
        if line == '':
            return False
        m = version_regexp.search(line)
        if m:
            hi = int(m.group(1))
            lo = int(m.group(2))
            
            if hi > 1 or (hi == 1 and lo >= 7):
                return
            break
        
    raise InvalidJavaVersion("DQ'er requires Java version 1.7 or higher.\nPlease upgrade Java to minimum required version.")

def CheckJava():
    java_path = config(console, 'java_path')
    cmd_args =[java_path,
               "-version",]
    
    try:
        process = run_process(cmd_args, cwd = '.', show_window = False)
        if process:
            ReadJavaOutput(process)
        else:
            raise UnableToStartJava("Unable to start Java\nCheck Java Path")
    except Exception as e:
        raise UnableToStartJava("Unable to start Java: %s\nCheck Java Path" % (str(e),))
        
    WaitExit(process)

proclist = [(0x01, 0xb0, 4),    # Daimyo - 256 bit trace words
            (0x01, 0xa9, 4),    # Samurai - 256 bit trace words
            (0x01, 0xa4, 2)     # Knight - 128 bits trace words
            ]

multicore_list = [(0x01, 0x99),  #"1004K"
                  (0x01, 0x9a),  #"1074K"
                  (0x01, 0xA0),  #"interAptivUP"
                  (0x01, 0xA1),  #"interAptivMP"
                  (0x01, 0xA2),  #"proAptivUP"
                  (0x01, 0xA3),  #"proAptivMP"
                  (0x01, 0xA4),  #"P6600",
                  (0x01, 0xA8),  #"P5600",
                  (0x01, 0xb0),  #"I6500"
                  ]

def check_core_type(config, company, proc_id):
    parser = ConfigParser.ConfigParser()
    fp = StringIO(config)
    try:
        parser.readfp(fp)
        prid = int(parser.get('section 1', 'PRID'), 16)
        c = (prid >> 16) & 0xff
        p = (prid >> 8) & 0xff
        
        return company == c and proc_id == p
    except ConfigParser.Error:
        return False

def is_74k(config):
    return check_core_type(config, 1, 0x97)
    
def is_1074k(config):
    return check_core_type(config, 1, 0x9a)

def find_trace_word_size(prid):
    company = (prid >> 16) & 0xff
    proc = (prid >> 8) & 0xff
    
    for c, p, w in proclist:
        if company == c and proc == p:
            return w
        
    return 1

def determine_trace_word_size(config):
    ''' Returns the size of a trace data packet in doublewords'''
    parser = ConfigParser.ConfigParser()
    fp = StringIO(config)
    try:
        parser.readfp(fp)
        prid = int(parser.get('section 1', 'PRID'), 16)
        return find_trace_word_size(prid)
    except ConfigParser.Error:
        return 1
        
def is_multicore(parser):
    try:
        prid = int(parser.get('section 1', 'PRID'), 16)
        company = (prid >> 16) & 0xff
        proc = (prid >> 8) & 0xff
        
        for c, p in multicore_list:
            if company == c and proc == p:
                return True
            
        return False
    except ConfigParser.Error:
        return False
    
def get_bytes(core_id, guest_id, pom, asid, address, mem_map, isa, endian_fmt, size_fmt):
    asid_mem = find_asid_memory(mem_map, core_id, guest_id, pom, asid)
    for addr in asid_mem:
        data = asid_mem[addr]
        size = 4 if size_fmt == 'I' else 2
        if addr <= address <= addr + len(data) - size:
            offset = address - addr
            val = struct.unpack(endian_fmt + size_fmt, data[offset:offset + size])
            data = struct.pack(">"  + size_fmt, val[0])
            return data
    if asid != 0xffff:
        return get_bytes(core_id, guest_id, pom, 0xffff, address, mem_map, isa, endian_fmt, size_fmt)
    return None

def determine_bytes(address, mem_map, isa, endian_fmt, size_fmt, asid):
    core_id = 0xffff
    guest_id = 0xffff
    pom = 0xffff
    #address = int(address, 16)
    if size_fmt == 'I':
        return get_bytes(core_id, guest_id, pom, asid, address, mem_map, isa, endian_fmt, size_fmt)
    else:
        first = get_bytes(core_id, guest_id, pom, asid, address, mem_map, isa, endian_fmt, size_fmt)
        second = get_bytes(core_id, guest_id, pom, asid, address + 2, mem_map, isa, endian_fmt, size_fmt)
        if first and second:
            return first + second
        else:
            return first 

def extract_bytes(addr, isa, endian, mem_map, asid):
    endian_fmt = ">" if endian else "<"
    size_fmt = "H" if is_16bit_isa(isa) else "I"
    return determine_bytes(addr, mem_map, isa, endian_fmt, size_fmt, asid)
    
       
def insert_memory(traced_data, mem_map, endian, use_asid):
    for frm in traced_data:
        if frm.type == TraceTypes.HDI_TRACETYPE_PC:
            asid = frm.asid if use_asid else 0xffff
            mem = extract_bytes(frm.addr, frm.isa, endian, mem_map, asid)
            if mem:
                frm.mem = mem
        
@command(device_required=False,
        dasm=dasms,
        range=[named_all],
        )
def traceprint(range="all", dasm=False, mode='mdi', save_files=False, path=None, respect_asid = True, show_asid=False, cm = None, device=None):
    '''Show trace data, this can be in raw form, tm packets or instruction trace.
    
    ============ ===================================================================
    Parameter    Meaning
    ============ ===================================================================
    range        Which trace frames to show. Values:
                 'all' - Show all frames
                 'xx..yy' - Show from frame xx to frame yy inclusive
    dasm         If true disassemble instruction at address in instruction trace
    mode         Change mode of display. Values:
                 'mdi' - Default, show instruction trace
                 'tm'  - Show tm mode
                 'raw' - Show raw trace data
    save_files   If True and path is valid save the trace files in path
                 else If False and path is valid load trace files found in path
                 else do not load or save files
    path         Path to load files from or save files to
    respect_asid Respect the asid value in memory reads
    show_asid    Show asid in addresses
    cm           If True show Coherency Manager trace
    ============ ===================================================================
    
    Example usage::
    
    >>> traceprint(dasm=True, save_files = True, path='/usr/tmp')
    '''
    return tracedecode(range, dasm, mode, save_files, path, respect_asid, show_asid, False, cm=cm, device=device)

@command(device_required=False,
        dasm=dasms,
        range=[named_all],
        )
def tracelist(range="all", dasm=False, mode='mdi', save_files=False, path=None, respect_asid = True, show_asid=False, cm=None, device=None):
    '''Return decoded trace data, this can be in raw form, tm packets or instruction trace.
    
    ============ ===================================================================
    Parameter    Meaning
    ============ ===================================================================
    range        Which trace frames to show. Values:
                 'all' - Show all frames
                 'xx..yy' - Show from frame xx to frame yy inclusive
    dasm         If true disassemble instruction at address in instruction trace
    mode         Change mode of display. Values:
                 'mdi' - Default, show instruction trace
                 'tm'  - Show tm mode
                 'raw' - Show raw trace data
    save_files   If True and path is valid save the trace files in path
                 else If False and path is valid load trace files found in path
                 else do not load or save files
    path         Path to load files from or save files to
    respect_asid Respect the asid value in memory reads
    show_asid    Show asid in addresses
    cm           If True show Coherency Manager trace
    ============ ===================================================================
    
    Example usage::
    
    >>> frames = tracelist(dasm=True)
    >>> for frame in frames:
    >>>   do_something_with(frm)
    '''
    return tracedecode(range, dasm, mode, save_files, path, respect_asid, show_asid, True, False, cm=cm, device=device)

    
@command(device_required=False,
        dasm=dasms,
        range=[named_all],
        )
def tracetofile(path, range="all", respect_asid = True, device=None):
    '''Save decoded trace data to a file, this can be in raw form, tm packets or instruction trace.
    
    ============ ===================================================================
    Parameter    Meaning
    ============ ===================================================================
    range        Which trace frames to show. Values:
                 'all' - Show all frames
                 'xx..yy' - Show from frame xx to frame yy inclusive
    path         Path to load files from or save files to
    respect_asid Respect the asid value in memory reads
    ============ ===================================================================
    
    Example usage::
    
    >>> tracetofile('/usr/tmp', range = '0..100')
    '''
    return tracedecode(range, False, 'mdi', True, path, respect_asid, False, False, True, device=device)    
    
def tracedecode(rng="all", dasm=False, mode='mdi', save_files=False, path=None, respect_asid = True, show_asid=False, for_list = False, save_decoded = False, cm = None, device=None):
    
    CheckJava()
    tracestop()
    # Determine range (a -ve start means from end
    # Need to then validate range
    is_offchip = False
    if not path or save_files:
        require_device(device)
        tracestop(device)
    if path and not save_files:
        device = None
        dqdname = os.path.join(path, "trace.dqd")
        tcfname = os.path.join(path, "trace.tcf")
        with open(tcfname, "r") as f:
            tconfig = f.read()
        if (mode == 'mdi' or mode == 'show_stdout') and os.path.exists(dqdname):
            target_info = TargetInfo(tconfig)
            decoder = trace_type_decode(show_asid, target_info)
            traced_data = load_dequeued_data(dqdname, rng, dasm, target_info, decoder, for_list)
            return TraceResults(traced_data) #results
            
        imon_name = os.path.join(path, "trace.imon")
        twsize = determine_trace_word_size(tconfig)
        if os.path.exists(imon_name):
            data = OffChipFileTraceReader(imon_name, twsize, rng)
            is_offchip = True
        else:
            filename = os.path.join(path, "trace.rtd")
            data = FileTraceReader(filename, twsize, rng)
    else:
        require_device(device)
        tconfig = read_config(True, device)
        twsize = determine_trace_word_size(tconfig)
        trace = get_tracer(device)
        is_offchip = trace.is_offchip_trace(device)
        if is_offchip:
            imon_size, trace_port = device.tiny.ConfigureTrace('stop_trace', 'trace_only', 0, 5511)
            status, count = device.tiny.PollTrace()
            trace_per_packet = imon_size / 8 - 1
            num_entries = count
            num_entries *= trace_per_packet
            num_entries /= twsize
        else:
            num_entries = traceentries(device)
        start_frame, length = determine_range(rng, num_entries)       
        data = tracereader(twsize = twsize, start_frame = start_frame, num_entries = length, device=device)
    if not save_decoded and save_files and path:
        save_trace_files(path, tconfig, data, twsize)
        data = tracereader(twsize = twsize, start_frame = start_frame, num_entries = length, device=device)
    if data:
        options = {'save_files' : save_files,
                    'path' : path, 
                    'show_asid' : show_asid, 
                    'range' : rng,
                    'mode' : mode,
                    'dasm' : dasm, 
                    'for_list' : for_list,
                    'save_decoded' : save_decoded,
                    'core_index' : device.core.index if device else 0,
                    'cm' : cm}
        #if not is_offchip:
        rng = '%d..%d' % (start_frame, start_frame + length + 1)
        options['rng'] = rng
        traced_data, mem_map = upload_and_collect(tconfig, data, respect_asid, options, device=device)
        target_info = TargetInfo(tconfig, device.core.index if device else None)

        decoder = trace_type_decode(show_asid, target_info)
        return TraceResults(traced_data) #results
    return TraceResults(["No data collected."])

def trace_word_size(size, device):
    if size is None:
        #config = tracemode(device)
        core = device if isinstance(device, Core) else device.core
        core_index = core.index
        targdata = targetdata(device=device)
        table = targdata.socs[core.soc.index].cores[core_index]
        prid = table.prid
        size = find_trace_word_size(prid)
    return size

def tracereader(num_entries=0, twsize = None, start_frame = 0, device=None):
    '''Return an object that can read the trace records.'''
    tracestop()
    trace = get_tracer(device)
    word_size = trace_word_size(twsize, device)
    return trace.traceread(device, start_frame, num_entries, word_size)
 

@command()
def traceread(num_entries=0, twsize = None, start_frame = 0, device=None):
    '''Read and display the trace data.'''
    word_size = trace_word_size(twsize, device)
    fmt = '0x%016X ' * word_size
    reader = tracereader(num_entries, word_size, start_frame, device)
    if Command._interactive:
        chunk_size=512
        data = reader.read(chunk_size)[0]
        while data != []:
            for n in range(0, len(data), word_size):
                slice = data[n : n + word_size]
                to_print = tuple(slice)
                print fmt % to_print
            data = reader.read(chunk_size)[0]
    return None

@command(verbose=verbosity)
def tracego(verbose=True, devices=[], offchip_mode = None, offchip_size = 0, path = None):
    '''Enables trace generation on all of the given cores and starts them running.
    
    This is roughly equivalent to ::
    
       foreach core in devices:
          tracestart(core)
       go(*devices)
    
    Multiple cores may be specified, for example::
    
      tracego()            # start tracing and run the current core
      tracego(s0c0, s0c1)  # start tracing and run the cores s0c0 and s0c1
      tracego(soc0)        # start tracing and all the cores in soc0
    
    '''
    trace = get_tracer(devices[0])
    return trace.got(devices, verbose, offchip_mode, offchip_size, path)

@command()
def tracestop(devices=[]):
    '''Stop generating trace data on the given cores.
    
    Multiple cores may be specified, for example::

      tracestop()            # stop tracing on the current core
      tracestop(s0c0, s0c1)  # stop tracing on cores s0c0 and s0c1
      tracestop(soc0)        # stop tracing on all cores in soc0

    '''
    trace = get_tracer(devices[0])
    return trace.stop(devices)
    
@command()
def tracestart(devices=[], offchip_mode = None, offchip_size = 0, imon = False, path = None):
    '''Start generating trace data on the given cores.

    Multiple cores may be specified, for example::

      tracestart()            # start tracing on the current core
      tracestart(s0c0, s0c1)  # start tracing on cores s0c0 and s0c1
      tracestart(soc0)        # start tracing on all cores in soc0

    '''   
    trace = get_tracer(devices[0])
    return trace.start(devices, offchip_mode, offchip_size, imon, path)

@command()
def traceentries(device=None):
    '''Discover how many trace entries are pending.'''
    trace = get_tracer(device)
    return trace.traceentries(device, trace_word_size(None, device))
    
def can_disable_pctrace(device=None):    
    '''Detects whether pc tracing can be disabled.'''
    trace = get_tracer(device)
    return trace.can_disable_pctrace(device)
    
@command()
def tracerev(device=None):
    '''Returns version of the trace hardware.'''
    trace = get_tracer(device)
    return trace.tcbrev(device)

default = named('default')

@command(cmd=[namedstring(default), namedstring(on), namedstring(off)])
def tracemode(cmd=None, devices=[], **kwargs):
    '''Get or configure the trace system.
    
    ========================= ======================================================
    Syntax                    Description
    ========================= ======================================================
    tracemode(default)        Put the trace system into a known state. Enables 
                              tracing in all modes except debug, enables PC trace
                              only, turns off all filtering.
    tracemode(on)             Turn on trace for this core.
    tracemode(off)            Turn off trace initially for this core.
    ========================= ======================================================
    
    Other settings can be specified using key=value syntax and combined with 
    the above commands. For example::
    
       tracemode(default, asidfilter=3) # use default settings but specify an asid
       filter
       
    Multiple cores may be specified, for example::

      tracemode()              # display tracing mode for the current core
      tracemode(s0c0, s0c1)    # display tracing mode for the cores s0c0 and s0c1
      tracemode(default, soc0) # set trace mode to default for all cores on soc0
      tracemode(soc0, pc=[0])  # enable PC tracing on all cores of soc0
    
    
    The return value of tracemode can be saved and passed back to tracemode to 
    restore settings, and it can be manipulated using attribute assignment::
    
        tm = tracemode(default)
        tm.en = 1
        tracemode(tm)
        
    $tracemodedocs
    
    Performance Counter Numbering on MT cores:    
    
    Performance counters are implemented per-TC but are not restricted to 
    collect data from their own TC so are best viewed as a global resource.
    
    Consequently performance counters are numbered logically, for example a core 
    that has 2 performance counters implemented per TC and has 4 TCs then the 
    counters are numbered as follows:
    
    ========= ==== ==========================
    Counter#  TC#  CP0 Configuration Register 
    ========= ==== ==========================
    pm=[0]    0    perfctl0
    pm=[1]    0    perfctl1
    pm=[2]    1    perfctl0
    pm=[3]    1    perfctl1
    pm=[4]    2    perfctl0
    pm=[5]    2    perfctl1
    pm=[6]    3    perfctl0
    pm=[7]    3    perfctl1
    ========= ==== ==========================
    
    To enable tracing of multiple performance counters specify them as a list, 
    e.g. to enable tracing of perfctl0/TC0 and perfctl1/TC2 for the above core
    then use ``pm=[0,7]``.
    '''
    cores = get_cores(devices)
    def tm(device, *args, **kwargs):
        return get_tracer(device).tracemode(device, *args, **kwargs)
    res = results.AllResult()
    res.call(tm, cores, cmd, **kwargs)
    return res.get_result_maybe_just_one(tracemode, cmd, **kwargs)
    
def is_valid_range(lo, hi):
    return hi == -1 or lo <= hi

def to_int(val):
    val = val.strip()
    val = val.lower()
    radix = 16 if val.startswith("0x") else 10
    return int(val, radix)
    
def determine_range(range, max):
    if range == all or range == 'all':
        return 0, max
    else:
        vals = range.split(' ')
        if len(vals) == 2:
            if vals[0] == 'first':
                start = 0
                end = to_int(vals[1])
            elif vals[0] == 'last':
                start = max - to_int(vals[1])
                end = max - start
            else:
                raise RuntimeError("Invalid range")
            #if is_valid_range(start, end):
            return start, end
        else:
            vals = range.split("..")
            if (len(vals) == 1): 
                start = to_int(vals[0])
                if is_valid_range(start, max):
                    return start, max - start
            elif len(vals) == 2:
                start = to_int(vals[0])
                end = to_int(vals[1])
                if start < max:
                    if is_valid_range(start, end):
                        return start, min(end, max) - start
        
    raise RuntimeError("Invalid range")
            
    
def make_filename(file, extension):
    return file + ('' if extension.startswith('.') else '.') + extension
    
def skip_data(amount, twize, trace_data):
    max_skip = 1024 
    amount *= twize
    while amount:
        to_skip = min(max_skip, amount)
        trace_data.read(to_skip)
        amount -= to_skip
         
trace_extensions = ['rtd', 'tcf', 'mem']     
        
def has_file_extension(name, extensions):
    for ext in extensions:
        if name.endswith(ext):
            return True
    return False

def list_files_with_extensions(path, extensions):
    files = []
    if os.path.exists(path):
        for name in os.listdir(path):
            if not os.path.isdir(name):
                if has_file_extension(name, extensions):
                    files.append(name)
                
    return files

def delete_trace_files(path):
    for file in list_files_with_extensions(path, trace_extensions):
        try:
            os.remove(os.path.join(path, file))
        except Exception:
            # just eat any exception for nwo
            pass

def trace_files_exist(path):
    return  len(list_files_with_extensions(path, trace_extensions)) != 0             
         
@command()
def tracesave(path, trace=all, mem = None, tasid = -1, memtype = None, delete_existing = False, device = None):
    '''Save trace data, config, and memory for later use.
    
    =============== ================================================================
    Parameter       Meaning
    =============== ================================================================
    path            Folder where the trace files will be saved. If trace files 
                    already exist in the folder they will be deleted if 
                    delete_existing is True else and error will be raised.
    trace           Which range of trace frames to save. Values:
                    'all' - Save all frames
                    'xx..yy' - Save from frame xx to frame yy inclusive
                    Default value = all
    mem             Range of memory to save:
                    'xx..yy' - Save memory from xx to yy inclusive
                    Default value = None 
    memtype         Memory type to save
                    'kernel' = eva kernel mode
                    'user' = eva user mode
                    'physical' = physical (ERL=1)
                    None = Read memory using the current state of the machine
                    Default value = None
    tasid           asid to use for memory read (-1 means use current)
                    Default value = -1
    delete_existing If the file already exists it will be deleted if delete_existing
                    is True otherwise an error will be raised.
                    Default value = False
                 
    =============== ================================================================
    '''
    if trace_files_exist(path):
        if delete_existing:
            delete_trace_files(path)
        else:
            raise RuntimeError('Trace files already exist in path.')
    
    file = os.path.join(path, 'trace')
    
    if trace:
        num_entries = traceentries()
        config = tracemode(device)
        config = config.config(True, device)
        twsize = determine_trace_word_size(config)
        tracer = get_tracer(device)
        is_offchip = tracer.is_offchip_trace(device)
        
        if is_offchip:
            imon_size, trace_port = device.tiny.ConfigureTrace('stop_trace', 'trace_only', 0, 5511)
            trace_per_packet = imon_size / 8 - 1
            num_entries *= trace_per_packet
        
        #### TODO
        start, length = determine_range(trace, num_entries)
        trace_data = tracereader(twsize = twsize, start_frame = start, device=device)

        skip = start - trace_data.start_frame
        pathname = os.path.dirname(file)
        if not os.path.exists(pathname):
            os.makedirs(pathname)
        if length:
            begin = start * twsize
            end = start + length * twsize
            
            #trace_data = build_trace_data(trace_data[begin : end], twsize, frame_start = start)
            rtd_name = make_filename(file, "rtd") 
            with open(rtd_name, "wb") as f:
                write_trace_data(f, trace_data, twsize, start, skip, length)
            
        cfg_name = make_filename(file, "tcf") 
        with open(cfg_name, "wb") as f:
            f.write(config + '\n')
    if mem:
        tracesavemem(file, mem, tasid, memtype, delete_existing, device = device)
     
@command()
def tracesavemem(file, mem, tasid = -1, memtype = None, delete_existing = False, device = None):
    '''Save trace data, config, and memory for later use.
    
    =============== ================================================================
    Parameter       Meaning
    =============== ================================================================
    file            Filename: e.g d:\\savetrace\\trace.mem. If the file does not
                    have the extension .mem it will be appended. 
    mem             Address range of memory to save. Values:
                    'xx..yy' - Save from frame xx to frame yy inclusive
    memtype         Memory type to save
                    'kernel' = eva kernel mode
                    'user' = eva user mode
                    'physical' = physical (ERL=1)
                    None = Read memory using the current state of the machine
                    Default value = None
    tasid           asid to use for memory read (-1 means use current)
                    Default value = -1
    delete_existing If the file already exists it will be deleted if delete_existing
                    is True otherwise an error will be raised.
    ================ ===============================================================
    '''
    
    if not file.endswith('.mem'):
        file = file + '.mem'
    
    if os.path.exists(file):
        if delete_existing:
            os.remove(file)
        else:
            raise RuntimeError('File (%s) already exists.' % (file,))
        
    with asid(tasid if tasid else -1):
        info = cpuinfo(device=device)
        limit = 0xffffffff if info['cpu_is_32bit'] else 0xffffffffffffffff
        start, length = determine_range(mem, limit)
        pathname = os.path.dirname(file)
        if not os.path.exists(pathname):
            os.makedirs(pathname)
        if memtype == 'kernel':
            type = 4
            mem_mode = 0
        elif memtype == 'user':
            type = 5
            mem_mode = 1
        elif memtype == 'physical':
            type = 4    # TODO - fix for new memory type
            mem_mode = 2
        elif memtype is None:
            type = 0
            mem_mode = 0xffff
        else:
            raise ValueError("Unrecognised memory type: %s" % (memtype,))
            
            
        data = byte(start, count=length, type = type, device=device)
        data = struct_pack(data, 1, False)
        tasid = tasid if tasid != -1 else 0xffff            
        with open(file, "wb") as f:
            version = struct.pack('>I', 0x010000ff)
            f.write(version)
            f.write(struct.pack('>H', 0xffff))
            f.write(struct.pack('>H', 0xffff))
            f.write(struct.pack('>H', 0xffff))
            f.write(struct.pack('>H', tasid))
            address = struct.pack('>Q', start)
            f.write(address)
            f.write(data)

def _assign_regfields(argname, mode, value, *regfieldnames):
    original = value
    max = 0
    for regfieldname in regfieldnames:
        regname, fieldname = regfieldname.split('.')
        field = mode.get_reg_type(regname)._find_field(fieldname)
        mode.set_reg_field(regname, fieldname, value & field.mask)
        value = value >> field.size
        max += field.size
    if value:
        raise ValueError("Value 0x%x is out of range for %s (max = 0x%x)" % (original, argname, (1 << max) -1))

def _extract_regfields(mode, *regfieldnames):
    value = 0
    prevshift = 0
    for regfieldname in reversed(regfieldnames):
        regname, fieldname = regfieldname.split('.')
        regtype = mode.get_reg_type(regname)
        shift = regtype._find_field(fieldname).size
        value = (value << shift) | mode.get_reg_field(regname, fieldname)
    return value        

class TraceModeArgument(object):
    def __init__(self, name='', default=0, type=None, valid='', fields=[], requires=[], doc='', version = 0):
        _TraceModeMetaClass.add_argument(self)
        self.name = name
        self.default = default
        self.valid = valid
        self.fields = fields
        self.__doc__ = self.doc = doc
        self.type = type
        self.requires = requires
        self.version = version

    def __repr__(self):
        extras = []
        if self.requires:
            extras.append('requires=%r' % (self.requires,))
        if self.type:
            extras.append('type=%s' % (self.type.__name__,))
        return ('%s(%r, default=%r, valid=%r, fields=%r,%s\n'
                '    doc=%r)') % (self.__class__.__name__, self.name, 
                self.default, self.valid, self.fields, ', '.join(extras), self.doc)

class RegisterField(TraceModeArgument):
    def __set__(self, mode, value, type=None):
        if self.type:
            value = self.type(value)
        _assign_regfields(self.name, mode, value, *self.fields)
        
    def __get__(self, mode, type=None):
        if mode is None: return self
        return _extract_regfields(mode, *self.fields)
        
class IDFilterWithValid(TraceModeArgument):
    def __set__(self, mode, value, type=None):
        validr, validf = self.fields[0].split('.')
        valid = value is not None
        if validr.startswith('!'):
            validr = validr[1:]
            valid = not valid
        mode.set_reg_field(validr, validf, valid)
        if value is not None:
            _assign_regfields(self.name, mode, value, *self.fields[1:])
            
    def __get__(self, mode, type=None):
        if mode is None: return self
        value = None
        validr, validf = self.fields[0].split('.')
        if validr.startswith('!'):
            validr = validr[1:]
            valid = not mode.get_reg_field(validr, validf)
        else:
            valid = mode.get_reg_field(validr, validf)
        if valid:
            value = _extract_regfields(mode, *self.fields[1:])
        return value
        
def endian_swap_words(data, device):
    swapped = []
    for d in data:
        top = d >> 32
        bot = d & 0xffffffff

        d = top | (bot << 32)
        swapped.append(d)

    return swapped                
    
def get_cores(devices):
    cores = []
    for device in devices:
        if hasattr(device, 'cores'):
            if not device.cores:
                raise RuntimeError('There are no debuggable cores at present')
            cores.extend([c for c in device.cores if c.family != CoreFamily.mipscm])
        elif hasattr(device, 'core'):
            cores.append(device.core)
        else:
            cores.append(device)
    # now remove duplicates and sort 
    cores = dict([((c.soc.index, c.index), c) for c in cores])
    return [c for index, c in sorted(cores.items())]
        
class _TraceModeMetaClass(type):
    '''Metaclass that allows us to get the tm args in the order they are 
    defined, whereas dir(mcs) returns them in dict order.'''
    __tmargs = []
    def __new__(mcs, name, bases, attributes):        
        attributes['arguments'] = _TraceModeMetaClass.__tmargs
        _TraceModeMetaClass.__tmargs = []
        return type.__new__(mcs, name, bases, attributes)
        
    @classmethod
    def add_argument(mcs, arg):
        mcs.__tmargs.append(arg)
      
@command()
def tracebuffersize(size = None, device = None):
    '''Set the size of the shared trace memory.
    
    =============== ================================================================
    Parameter       Meaning
    =============== ================================================================
    size            Optional, if provided specifies amount of memory to reserve for 
                    trace data collection. The size must be a power of two.
                    You can specify the size using a convenient string such as:
                    "32K" specify a size of 32768 bytes.
                    "1M" specify a size of 1 Megabyte (1048576 bytes).
                    If the trace buffer size is fixed and a size specified or the 
                    target does not support on chip trace an exception will be 
                    raised.
                    If size is omitted, the current size of the onc chip trace 
                    buffer is returned.
    =============== ================================================================
    
    Returns the size of the trace buffer. 
    '''
    trace = get_tracer(device)
    return trace.tracememsize(size, device)
    
class TraceModeBase(object):
    __metaclass__ = _TraceModeMetaClass
    renames = {}
    _byname = {}
        
    @classmethod
    def defaults(cls):
        return dict([(a.name, a.default) for a in cls.arguments])
       
    @classmethod
    def _find_argument(cls, name):
        if not cls._byname:
            cls._byname = dict([(a.name,a) for a in cls.arguments])
        try:
            return cls._byname[name]
        except KeyError:
            try:
                use = ' (use %s)' % cls.renames[name]
            except KeyError:
                use = ''
            raise KeyError('Unknown tracemode argument %s%s' % (name,use))
        
    def _requirement_met(self, requirement):
        return bool(self.get_reg_field(*requirement.split('.')))
        
    def __repr__(self):
        result = OrderedDict()
        for tmarg in self.arguments:
            if all(self._requirement_met(req) for req in tmarg.requires):
                if tmarg.version <= self.trace_version:
                    result[tmarg.name] = getattr(self, tmarg.name)
        return results.column_table(['%s=%s' % x for x in result.items()])
        
    def get_config(self, name, default):
        try:
            return config(name)
        except ValueError:
            return default
        
    def apply(self, cmd, **kwargs):
        cls = self.__class__
        if cmd == 'default':
            defaults = cls.defaults()
            try:
                cr = defaults['cr']
                # Here we check if trace has been calibrated and if so use the cr from there
                cal = self.get_config('calibrate trace', -1)
                if cal != -1:
                    cr = (cal >> 12) & 0x0f
                    if cr != 0xf:
                        defaults['cr'] = cr
            except KeyError:
                pass
            kwargs = dict(defaults, **kwargs)
        elif cmd == 'on':
            self.on = 1
        elif cmd == 'off':
            self.on = 0
        for k in kwargs.keys():
            cls._find_argument(k)
        for k, v in kwargs.items():
            setattr(self, k, v)

def get_core(device):
    if hasattr(device, 'core'):
        return device.core
    else:
        return device

def get_trace_mode(device):
    return None #getattr(get_core(device), 'trace_mode', None)
    
def set_trace_mode(device, mode):
    get_core(device).trace_mode = mode

def get_offchip_size(size):
    valid_sizes = [i * 512 for i in range(17)]
    try:
        return valid_sizes.index(size)
    except:
        raise RuntimeError('Invalid offchip size. Must a multiple of 512 no greater than 8192.')

class TraceBase(object):
    TraceMode = TraceModeBase
    def tracemode(self, device, cmd_or_tm=None, **kwargs):
        cls = self.__class__
        if isinstance(cmd_or_tm, TraceModeBase):
            mode = cmd_or_tm
        else:
            mode = cls.TraceMode.read(device)
            if cmd_or_tm is None and not kwargs:
                return mode                
            mode.apply(cmd_or_tm, **kwargs)
        mode.write(device=device)
        mode = cls.TraceMode.read(device)
        set_trace_mode(device,  mode)
        return mode

    def got(self, devices, verbose, offchip_mode = None, offchip_size = 0, path = None):
        self.__class__.TraceMode.start_trace(get_cores(devices), offchip_mode, offchip_size, path)
        go(verbose=verbose, devices=devices)

    def stop(self, devices):
        self.__class__.TraceMode.stop_trace(get_cores(devices))

    def start(self, devices, offchip_mode = None, offchip_size = 0, imon = False, path = None):
        self.__class__.TraceMode.start_trace(get_cores(devices), offchip_mode, offchip_size, path)

def gendocs(indent='    '):
    from imgtec.lib import rst
    from imgtec.console import pdtrace, iftrace
    pdt = [(arg.name, arg.valid, arg.doc) for arg in pdtrace.PDTraceMode.arguments]
    ift = [(arg.name, arg.valid, arg.doc) for arg in iftrace.IFTraceMode.arguments]
    common = list(set(pdt) & set(ift))
    common.sort(key=lambda x:pdt.index(x))
    
    lines = []
    for section, opts in [('', common), ('PDTrace only', pdt), ('iFlowtrace only', ift)]:
        if section:
            lines.append('{}:'.format(section))
        lines.append('')
        rows = []
        for name, valid, doc in opts:
            if not section or (name, valid, doc) not in common:
                rows.append(['%s=%s' % (name, valid), doc])
        lines.extend(rst.simple_table(['Parameter', 'Description'], rows).split('\n'))
        lines.append('')
    return ('\n' + indent).join(lines)

def gencmdocs(indent='    '):
    from imgtec.lib import rst
    from imgtec.console import pdtrace
    pdt = [(arg.name, arg.valid, arg.doc) for arg in pdtrace.PDTraceModeCM.arguments]
    common = list(set(pdt))
    common.sort(key=lambda x:pdt.index(x))
    
    lines = []
    for section, opts in [('', common)]:
        if section:
            lines.append('{}:'.format(section))
        lines.append('')
        rows = []
        for name, valid, doc in opts:
            if not section or (name, valid, doc) not in common:
                rows.append(['%s=%s' % (name, valid), doc])
        lines.extend(rst.simple_table(['Parameter', 'Description'], rows).split('\n'))
        lines.append('')
    return ('\n' + indent).join(lines)


def word_swap(data):
    top = (data >> 32) & 0xffffffff
    bot = data & 0xffffffff
    return (bot << 32) + top            
        
imon_word_size = 8 # All imon data comes in 64 bit chunks (or at least it does at the moment)

def extract_trace_data(num_trace_packets, data, offset):
    fmt = ">" + "Q" * num_trace_packets
    trace_data = struct.unpack(fmt, data[offset : offset + imon_word_size * num_trace_packets])
    return [word_swap(data) for data in trace_data]
                
def extract_number_of_trace_words(imon_hdr):
    return (imon_hdr >> 32) & 0xf

class iMonStripper(object):
    
    def __init__(self, imon_size, frames_to_skip, twsize):
        self.init = True
        self.imon_size = imon_size
        self.imon_frame = frames_to_skip
        self.frames_to_skip = frames_to_skip * twsize
        self.reset_frames_to_skip = self.frames_to_skip
        self.twsize = twsize
        self.data = ''
        
    def reset(self):
        self.frames_to_skip = self.reset_frames_to_skip
        self.init = True
        self.data = ''
        
    def adjust_start(self, imon_hdr):
        if self.init:
            num_trace_packets = extract_number_of_trace_words(imon_hdr)
            mask = self.twsize - 1
            tcount = ((imon_hdr >> 24) & 0xff) - num_trace_packets
            frames_to_skip = (self.twsize - tcount) & mask
            frames_to_skip += self.frames_to_skip
        else:
            frames_to_skip = self.frames_to_skip
        
        self.init = False
        return frames_to_skip
    
    
    def strip(self, data):
        if self.data:
            self.data += data
        results = []
        imon_data = []
        
        offset = 0
        if len(data) < self.imon_size:
            return [], []
        while offset <= len(data) - self.imon_size:
            s = data[offset : offset + imon_word_size]
            imon_hdr = struct.unpack('>Q', s)[0]
            self.frames_to_skip = self.adjust_start(imon_hdr)
            num_trace_packets = extract_number_of_trace_words(imon_hdr)
            if num_trace_packets > (self.imon_size / imon_word_size - 1):
                raise Error('Corrupt/Invalid trace data')
            
            if self.frames_to_skip >= num_trace_packets:
                self.frames_to_skip -= num_trace_packets
            else:
                num_trace_packets -= self.frames_to_skip
                trace_data = extract_trace_data(num_trace_packets, data, offset + (self.frames_to_skip + 1) * imon_word_size)
                self.frames_to_skip = 0
                results.extend(trace_data)
                imon_frame = self.imon_frame + len(results) / self.twsize
                imon_data.append((imon_frame, imon_hdr))

            offset += self.imon_size
        
        self.imon_frame += len(results) / self.twsize

        return results, imon_data
            

    
@command(cmd=[namedstring(default)])
def tracecm(cmd=None, device=None, **kwargs):
    '''Get or configure the Coherency Manager trace.
    
    ========================= ======================================================
    Syntax                    Description
    ========================= ======================================================
    tracecm(default)          Put the trace system into a known state. 
    ========================= ======================================================
    
    Other settings can be specified using key=value syntax and combined with 
    the above commands. For example::
    
       tracecm(default, wb=1) # use default settings but specify trace write backs
       
    The return value of tracecm can be saved and passed back to tracecm to 
    restore settings, and it can be manipulated using attribute assignment::
    
        tm = tracecm(default)
        tm.en = 1
        tracecm(tm)
        
    $tracemodecmdocs
    
    '''
    from imgtec.console import pdtrace
    info = cpuinfo(device)
    if is_pd_trace(device):
        tracer = pdtrace.PDTraceCM()
    else:
        raise RuntimeError('No Coherency Manager trace mechanism available')

    cm = device if pdtrace.is_oci(device) else find_cm_device(device)
    if cm is None:
        raise RuntimeError('No Coherency Manager found.')
    

    
    return tracer.tracemode(device, cmd, **kwargs)

# [[[cog
# import cog 
# from imgtec.console import trace
# cog.outl('_tracemodecmdocs = """' + trace.gencmdocs() + '"""')
# ]]]
_tracemodecmdocs = """
    ========== ========================================================================================
    Parameter  Description
    ========== ========================================================================================
    wb=1|0     Turn on tracing of Coherent Writeback requests.
    io=1|0     Inhibit Overflow on CM FIFO full condition. Will stall the CM until progress can be made
    ae=1|0     Enable address tracing for the Coherency Manager
    tl=0-3     See SoC documentation for values
    en=1|0     Enable tracing for the Coherency Manager.
    ste=1|0    Enable generation of system trace data.
    stc=1|0    Enable capture of system trace data.
    tcbsys=x   Write the value to the TCBSYS register.
    cmp0ctl=x  Provides control over tracing transactions on Port 0 of the CM.                         
                  0: Tracing enabled, no address tracing                                               
                  1: Tracing enabled with address tracing                                              
                  2: Reserved                                                                          
                  3: Tracing disabled
    cmp1ctl=x  Provides control over tracing transactions on Port 1 of the CM.                         
                  See cmp0ctl for values
    cmp2ctl=x  Provides control over tracing transactions on Port 2 of the CM.                         
                  See cmp0ctl for values
    cmp3ctl=x  Provides control over tracing transactions on Port 3 of the CM.                         
                  See cmp0ctl for values
    cmp4ctl=x  Provides control over tracing transactions on Port 4 of the CM.                         
                  See cmp0ctl for values
    cmp5ctl=x  Provides control over tracing transactions on Port 5 of the CM.                         
                  See cmp0ctl for values
    cmp6ctl=x  Provides control over tracing transactions on Port 6 of the CM.                         
                  See cmp0ctl for values
    cmp7ctl=x  Provides control over tracing transactions on Port 7 of the CM.                         
                  See cmp0ctl for values
    pm_delay=x Delay between generation of performance counter trace messages
    pm_en=1|0  Enable tracing of CM performance counters
    ========== ========================================================================================
    """
# [[[end]]]
tracecm._doc = format_doc(string.Template(tracecm._f.__doc__).substitute(tracemodecmdocs=_tracemodecmdocs))

    
# [[[cog
# import cog 
# from imgtec.console import trace
# cog.outl('_tracemodedocs = """' + trace.gendocs() + '"""')
# ]]]
_tracemodedocs = """
    ================= ======================================================================
    Parameter         Description
    ================= ======================================================================
    on=1|0            Turn on trace for this core
    cr=0-7            Set the off chip clock ratio.
    asidfilter=None|x Specify which ASID/process to trace, None means all, 0-x specify asid.
    syp=n             Specify sync mode period (see Programmer's Guide for values).
    ================= ======================================================================
    
    PDTrace only:
    
    ==================== ===========================================================================
    Parameter            Description
    ==================== ===========================================================================
    d=1|0                Enable/disable trace when the processor is in debug mode.
    e=1|0                Enable/disable trace when the processor is in exception mode.
    s=1|0                Enable/disable trace when the processor is in supervisor mode.
    k=1|0                Enable/disable trace when the processor is in kernel mode.
    u=1|0                Enable/disable trace when the processor is in user mode.
    io=1|0               Enable/disable inhibit overflow. e.g tracemode(io=0) turns it off.
    im=1|0               Enable/disable marking of all instruction cache misses.
    lsm=1|0              Enable/disable marking of all data cache misses.
    fcr=1|0              Enable/disable marking of all function call and returns.
    ab=1|0               Enable/disable output of pc for all branches whether needed or not.
    ca=1|0               Enable/disable output of idle cycles.
    offchip=1|0          Specify where trace data is sent when both onchip and offchip are available
    tm=traceto|tracefrom Specify wrap mode, tracefrom stops when full, traceto wraps until stopped.
    pc=1|0               Enable/disable trace of pc.
    la=1|0               Enable/disable trace of load addresses.
    sa=1|0               Enable/disable trace of store addresses.
    ld=1|0               Enable/disable trace of loaded data.
    sd=1|0               Enable/disable trace of stored data.
    tc=1|0               Specify whether a tc identifier should be output.
    cpufilter=None|x     Specify which vpe to trace. None means all, 0-x specify vpe.
    tcfilter=None|x      Specify which tc to trace. None means all, 0-x specify tc.
    fdt=1|0              Enable/disable filtered data trace mode.
    pmsync=1|0           Enable/disable performance counters trace on sync counter expiry.
    pmbp=1|0             Enable/disable performance counters trace on breakpoint match.
    pmfcr=1|0            Enable/disable performance counters trace on function entry or return.
    pmovf=1|0            Enable/disable performance counters trace on counter overflow.
    pm=N|[N, M, ...]     Specify list of performance counters to trace. For numbering see below.
    msa=1|0              Enable/disable MSA load/store data trace.
    utm=1|0              Enable/disable trace of user trace data.
    dcid=1|0             Enable/disable trace of Debug Context ID.
    mmidfilter=None|x    Specify which MMID to trace. None means all, 0-x specify MMID.
    guestfilter=None|x   Specify which guest to trace. None means all, 0-x specify guest.
    ==================== ===========================================================================
    
    iFlowtrace only:
    
    ================== ============================================================================
    Parameter          Description
    ================== ============================================================================
    io=1|0             Enable/disable inhibit overflow e.g tracemode(io=0) turns it off.
    fcr=1|0            Enable/disable tracing of all function call and returns, requires est=1.
    offchip=1|0        Specify where trace data is sent when both onchip and offchip are available.
    est=1|0            Enable/disable special trace modes.
    dc=1|0             Enable/disable tracing of delta cycles, requires est=1.
    fdt=1|0            Enable/disable filtered data trace mode, requires est=1.
    bm=1|0             Enable/disable breakpoint match mode.
    ecr=1|0            Enable/disable tracing of exceptions and returns, requires est=1.
    efdt=1|0           Enable/disable extended filtered data trace mode, requires est=1.
    utm=1|0            Enable/disable trace of user trace messages.
    guestfilter=None|x Specify which guestid to trace. None means all, 0-x specify guest id.
    dc_divide=x        Set the value of the delta cycle divider (if available).
    ================== ============================================================================
    """
# [[[end]]]

tracemode._doc = format_doc(string.Template(tracemode._f.__doc__).substitute(tracemodedocs=_tracemodedocs))




if __name__ == '__main__':
    print gendocs()
    
