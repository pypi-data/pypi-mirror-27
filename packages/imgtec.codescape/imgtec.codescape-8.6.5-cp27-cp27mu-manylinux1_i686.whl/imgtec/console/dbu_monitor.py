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

from imgtec.console.support import *
from imgtec.lib.namedstruct import namedstruct
from imgtec.lib.namedbitfield import namedbitfield
from imgtec.console.memory import MemoryResult
from imgtec.console.debug_monitor import *
from textwrap import dedent
from imgtec.console.program_file import symbol

class DebugMonitorError(Exception):
    pass
    
MASK_32_BIT  = 0xffffffff
MASK_64_BIT  = 0xffffffffffffffff

#Sizes in bytes
COM_BUFFER_SIZE  = 8*4
COM_BUFFER_DATA_SIZE = 4*4
DATA_BUFFER_SIZE = 256*8 
DEBUG_DATA_SIZE  = 512-8-4
DEBUG_DATA_CODE_SCRATCH_SIZE = 512-(35*8)-4 #4 for the guard value
    
#Locations
DATA_BUFFER_GUARD = DATA_BUFFER + DATA_BUFFER_SIZE
DATA_BUFFER_GUARD_VALUE = 0x11ca22fe33be44ef
DEBUG_DATA_START = 0xffffffffff200008
MONITOR_VERSION = DMXSEG_BEGIN

#Command numbers
MONITOR_COMMAND_READ            = 1
MONITOR_COMMAND_WRITE           = 2
MONITOR_COMMAND_READ_IMMEDIATE  = 3
MONITOR_COMMAND_WRITE_IMMEDIATE = 4
MONITOR_COMMAND_RESUME          = 5
MONITOR_COMMAND_CACHE_OP        = 6
MONITOR_COMMAND_TLB_PROBE       = 7
MONITOR_COMMAND_FREEZE          = 8
MONITOR_COMMAND_READ_MANY       = 9
MONITOR_COMMAND_WRITE_MANY      = 10

command_types  = {1 : 'read',
                  2 : 'write',
                  3 : 'read immediate',
                  4 : 'write immediate',
                  5 : 'resume',
                  6 : 'cache op',
                  7 : 'TLB probe',
                  8 : 'Freeze',
                  9 : 'Read many',
				  10: 'Write many',
                 }
                 
command_sizes = {
    8  : 0, #Commands without size default to this
    16 : 1,
    32 : 2,
    64 : 3,
    128: 4,
    }

#Response codes
MONITOR_RESPONSE_SUCCESS         = 0
MONITOR_RESPONSE_DEBUG_REENTRY   = 1
MONITOR_RESPONSE_UNKNOWN_COMMAND = 2
MONITOR_RESPONSE_UNKNOWN_TYPE    = 3

response_codes = {0 : 'Command succeeded',
                  1 : 'Command triggered a re-entry to debug mode',
                  2 : 'Unknown command',
                  3 : 'Unknown type',
                 }

#Memory types
MDIMIPCPU      = 1
MDIMIPPC       = 2
MDIMIPTLB      = 4
MDIMIPCP0      = 10
MDIMIPCP1      = 12
MDIMIPCP1C     = 13
MDIMIPFP       = 18 
MDIMIPDFP      = 19 
MDIMIPGVIRTUAL = 25
MDIMIPMSAW     = 39
MDIMIPMSACTL   = 40
MDIMIPSHADOW   = 97
MDIMIPGTLB     = 98
MDIMIPGCP0     = 99

SKIP_REGISTER_CHECK = 0xcafebeefdeadf00d
EXPECTED_MONITOR_ID = 0x4e4f4d44
COMMAND_TIMEOUT     = 200

MonitorCommand = namedbitfield('Command', [('ready', 31), ('busy', 30), 
            ('size', 26, 24), ('type', 23, 8), ('command', 7, 0)])
            
def set_skip_register_check(device, enable=True):
    device.da.dmxsegwrite(symbol('debugEntryData'), SKIP_REGISTER_CHECK if enable else 0, 64)
    
def bank_select_addr(bank, select):
    return (bank << 5) + select
    
def get_device(device):
    return device or Command.get_device()
 
def get_command_size(size):
    try:
        return command_sizes[size]
    except KeyError:
        raise DebugMonitorError('Unknown access size %d for monitor command.' % size)
        
def read_buffer(address, count, size, device):
    return [device.da.dmxsegread(address+(i*(size//8)), size) for i in range(count)]
    
def write_buffer(address, values, size, device):
    for i, item in enumerate(values):
        device.da.dmxsegwrite(address+(i*(size//8)), item, size)
        
def load_monitor(device=None):
    '''
    Load the debug monitor into dmxseg.
    '''
    device = get_device(device)
    for item, offset in zip(monitor_contents, itertools.count()):
        device.da.dmxsegwrite(DMXSEG_BEGIN+(offset*8), item, 64)
        
    #This is no longer included in the ELF as the buffer size can change.
    #We just use a fixed size for this wrapper though.
    device.da.dmxsegwrite(DATA_BUFFER_GUARD, DATA_BUFFER_GUARD_VALUE, 64)
    
def write_monitor_command(command=None, type=None, size=8, device=None, ready=1, 
    busy=0, check_idle=True):
    com = read_monitor_command(device=device)
    if check_idle:
        if com.ready != 0 or com.busy != 0:
            acknowledge_monitor_command(device=device)
            print "Warning: DBU monitor was not in the Idle state (ready=%d busy=%d)" \
                % (com.ready, com.busy)
                    
    new_com = MonitorCommand(ready=ready, busy=busy,
                size    = get_command_size(size) if size is not None else com.size,
                command = command if command is not None else com.command,
                type    = type if type is not None else com.type)
    device.da.dmxsegwrite(COM_BUFFER, new_com, 32)
    
def write_monitor_command_address(address, device):
    device.da.dmxsegwrite(COM_BUFFER_ADDR, address, 64)
    
def write_monitor_command_count(count, device):
    device.da.dmxsegwrite(COM_BUFFER_COUNT, count, 32)
    
def wait_for_command_completion(device, verbose=False):
    #When a command has finished Ready = 0, Busy = 1
    for _tries in range(COMMAND_TIMEOUT):
        com   = read_monitor_command(device=device)
        ready = com.ready
        busy  = com.busy
        
        if verbose:
            print "Ready = %d Busy = %d" % (ready, busy)
            
        if not ready:
            break
    else:
        acknowledge_monitor_command(device=device)
        raise DebugMonitorError(
                "Timed out waiting for command (0x%x, %s) to complete." 
                % (com.command, command_types.get(com.command, 'unknown')))
        
    #Check the response code
    response_code = read_monitor_command(device=device).command
    exc_code = response_code >> 3
    response_code = response_code & 0x7
    
    if response_code != MONITOR_RESPONSE_SUCCESS:
        #Clears flags only
        acknowledge_monitor_command(device=device)
        raise DebugMonitorError("Command failed with response code %d - %s (DExcCode %d)" % 
                (response_code, response_codes.get(response_code, 'Unknown'), exc_code))
                    
def reset_monitor_entry_level(device=None):
    '''
    Reset the monitor's stored debug entry level. Used when the target is reset
    during debug mode, so that on the next entry to debug mode it does not think
    that it is a re-entry.
    '''
    device = get_device(device)
    device.da.dmxsegwrite(DEBUG_DATA_ENTRY_LEVEL, 0x0, 64)

def acknowledge_monitor_command(device=None):
    '''
    Clear the flags to tell the monitor we have read the results of the last 
    command. Also to set the monitor back to idle when a command fails.
    '''
    device = get_device(device)
    #Command number and type are preserved
    write_monitor_command(size=None, device=device, ready=0, busy=0, check_idle=False)
    
def reset_monitor_changes(device=None):
    '''
    Reset all variable parts of the monitor. Debug data, command buffer and data 
    buffer.
    '''
    device = get_device(device)
    write_buffer(COM_BUFFER,        [0x0]*8,                    32, device)
    write_buffer(DEBUG_DATA,        [0x0]*(DEBUG_DATA_SIZE/4),  32, device)
    write_buffer(DATA_BUFFER,       [0x0]*(DATA_BUFFER_SIZE/8), 64, device)
    
def reset_monitor_command(device=None):
    '''
    Reset the first word of the command buffer, clearing command number, type
    and flags.
    '''
    device = get_device(device)
    acknowledge_monitor_command(device=device)
    
def read_monitor_command(device=None):
    '''
    Read the first word of the command buffer, showing the command number, type
    and flags.
    '''
    device = get_device(device)
    return MonitorCommand(device.da.dmxsegread(COM_BUFFER, 32))
    
def read_monitor_command_buffer(device=None):
    '''
    Read the whole command buffer. (8 words)
    '''
    device = get_device(device)
    return read_buffer(COM_BUFFER, COM_BUFFER_SIZE/4, 32, device)
    
class MonitorVersion(object):
    def __init__(self, major, minor, v_2, v_3, identifier):
        self.major      = major
        self.minor      = minor
        self.v_2        = v_2
        self.v_3        = v_3
        self.identifier = identifier
        self.version    = "%d.%d.%d.%d" % (self.major, self.minor, self.v_2, self.v_3)
        
    def __repr__(self):
        return self.version
    
def check_monitor_version(expected_version, device=None):
    '''
    Check the monitor's identifier is correct and that the version number matches
    expected_version. Where expected_version is a string of the form 'w.x.y.z'.
    '''
    device = get_device(device)
    id, version = read_buffer(MONITOR_VERSION, 2, 32, device)
    
    if id != EXPECTED_MONITOR_ID:
        raise DebugMonitorError(
            'Debug monitor identifier is incorrect (0x%08x), monitor may invalid or not loaded. ' % id)
    
    version_parts = [(version >> shift) & 0xFF for shift in [0, 8, 16, 24]] + [id]
    ver = MonitorVersion(*version_parts)
    
    if ver.version != expected_version:
        raise DebugMonitorError(
            'Debug monitor version is incorrect. Found %s expected %s.' % (ver.version, expected_version))
    
    return ver
    
def check_monitor_instruction_buff_guard(device=None):
    '''
    Check that the constant value at the end of the instruction buffer is still
    in place.
    '''
    device = get_device(device)
    
    guard = read_buffer(DEBUG_DATA_INSTR_GUARD, 1, 32, device)[0]
    if guard != 0xcafef00d:
        raise DebugMonitorError('Instruction buffer guard is invalid (0x%08x), therefore monitor is invalid.' % guard)
        
def check_monitor_data_buff_guard(device=None):
    '''
    Check that the constant value at the end of the data buffer is still in place.
    '''
    device = get_device(device)
    
    guard = read_buffer(DATA_BUFFER_GUARD, 1, 64, device)[0]
    if guard != DATA_BUFFER_GUARD_VALUE:
        raise DebugMonitorError('Data buffer guard is invalid (0x%016x), therefore monitor is invalid.' % guard)
    
class MonitorDebugContext(object):
    def __init__(self, scratch, debug_entry_level, pc, registers, code_scratch):
        self.scratch           = scratch
        self.pc                = pc
        self.debug_entry_level = debug_entry_level
        self.registers         = registers
        self.code_scratch      = code_scratch
        
    def __repr__(self):
        lines = [dedent('''\
                      Scratch: 0x%x
            Debug Entry Level: 0x%x
                           PC: 0x%016x
                   -Registers-''') %  (self.scratch, self.debug_entry_level, self.pc)]
                   
        #Start with r1, r0 not saved
        for reg, n in zip(self.registers, itertools.count(1)):
            lines.append("             r%02d : 0x%x" % (n, reg))
        return '\n'.join(lines)
        
def read_monitor_entry_level(device=None):
    '''
    Read the debug entry level from the saved context.
    '''
    device = get_device(device)
    return read_buffer(DEBUG_DATA + (2*8), 1, 64, device)[0]
    
def read_monitor_debug_data(device=None):
    '''
    Read the monitor's saved context. Contains the current PC, registers, debug 
    entry level and temporary code space. R1 is fetched from DESAVE. 
    Note: due to reading DESAVE the first sequence in the code scratch with always
    be a dmfc0.
    '''
    device = get_device(device)
    
    read_size = 1 + 1 + 1 + 31 #scratch, PC, entry level, registers
    data = read_buffer(DEBUG_DATA, read_size, 64, device)

    scratch, pc, debug_entry_level = data[:3]
    registers = data[3:]
    code_scratch = read_buffer(DEBUG_DATA_CODE_SCRATCH, 
                        DEBUG_DATA_CODE_SCRATCH_SIZE//4, 32, device)
    
    #Bypass DESAVE redirect to get r1
    set_skip_register_check(device)
    registers[0] = monitor_read_cp0_register(31, 0, 1, device=device)[0]
    set_skip_register_check(device, enable=False)
    
    return MonitorDebugContext(scratch, debug_entry_level, pc, registers, code_scratch)
    
def save_monitor_debug_data(device=None):
    '''
    Return the monitor's saved context as a list of words. (doesn't account for values stashed in DESAVE)
    '''
    device = get_device(device)
    
    return read_buffer(DEBUG_DATA_START, DATA_BUFFER_SIZE/8, 64, device)
    
def restore_monitor_debug_data(data, device=None):
    '''
    Write a previously saved context to the monitor's debug data. Intended for use
    when loading the debug monitor in debug mode.
    '''
    device = get_device(device)
    write_buffer(DEBUG_DATA_START, data, 64, device)
    
def read_monitor_code_scratch(device=None):
    '''
    Read the monitor's code scratch space. Use this instead of 
    read_monitor_debug_data to prevent overwriting the scratch space when reading 
    r1.
    '''
    return read_buffer(DEBUG_DATA_CODE_SCRATCH, DEBUG_DATA_CODE_SCRATCH_SIZE//4, 32, device)
    
def read_monitor_data_buffer(read_size=32, device=None):
    '''
    Read contents of data buffer.
    '''
    device = get_device(device)
    read_size_bytes = read_size//8
    num_words = DATA_BUFFER_SIZE//read_size_bytes
    result = read_buffer(DATA_BUFFER, num_words, read_size, device)
    return MemoryResult(result, address=DATA_BUFFER, size=read_size_bytes, bytes_per_line=24)
    
def read_monitor_context_register(index, device=None):
    '''
    Read a GP register directly from the monitor's saved context (r1 onwards). 
    For any register that is not r1 this will not require the monitor to be running,
    however r1 must be fetched from DESAVE.
    '''
    device = get_device(device)
    if index < 1:
        raise DebugMonitorError("Register r0 is not stored in the saved context.")
    elif index != 1:
        # Would normally be plus 3 for scratch, pc and entry level, but as zero is 
        # not stored r1 is the first register.
        return device.da.dmxsegread(DEBUG_DATA+((index+2)*8), 64)
    else:
        #Get r1 from DESAVE
        set_skip_register_check(device)
        r1 = monitor_read_cp0_register(31, 0, 1, device=device)[0]
        set_skip_register_check(device, enable=False)
        return r1
    
def write_monitor_context_register(index, value, device=None):
    '''
    Write a GP register directly using the monitor's saved context (r1 onwards).
    '''
    device = get_device(device)
    if index < 1:
        raise DebugMonitorError("Register r0 is not stored in the saved context.")
    elif index != 1:
        device.da.dmxsegwrite(DEBUG_DATA+((index+2)*8), value, 64)
    else:
        #Write to DESAVE (cached r1)
        set_skip_register_check(device)
        monitor_write_cp0_register(31, 0, [value], device=device)
        set_skip_register_check(device, enable=False)
        
def monitor_freeze(core, vc, device=None):
    '''
    Send a freeze command to the monitor which will cause the current active VC
    to restore all GP regs bar r1 which will be stored in DESAVE and throttle itself.
    This allows another VC to execute in debug mode.
    '''
    device = get_device(device)
    write_monitor_command(MONITOR_COMMAND_FREEZE, 0, device=device)
    wait_for_command_completion(device)
    acknowledge_monitor_command(device=device)
    
    for _tries in range(COMMAND_TIMEOUT):
        #Assume first core and VC as we're just testing freeze for now
        lt = device.da.read_vc_control1(core, vc)
        
        if lt == 0:
            break
    else:
        acknowledge_monitor_command(device=device)
        raise DebugMonitorError("Timed out waiting for freeze command to clear local throttle.")
        
def monitor_unfreeze(core, vc, device=None):
    '''
    Release the given thread's local throttle allowing it to return from a frozen
    state.
    '''
    device = get_device(device)
    device.da.write_vc_control1(core, vc, 1)
    
def monitor_read_generic(address, count, type, size, device, immediate=False):
    if immediate and (count*size > 128):
        raise RuntimeError("Immediate read size exceeds 128 bits.")
        
    write_monitor_command_address(address, device)
    device.da.dmxsegwrite(COM_BUFFER_COUNT, count, 32)
    
    command = MONITOR_COMMAND_READ_IMMEDIATE if immediate else MONITOR_COMMAND_READ
    write_monitor_command(command, type, size=size, device=device)
    wait_for_command_completion(device)
    
    result_address = COM_BUFFER_DATA if immediate else DATA_BUFFER
    result = read_buffer(result_address, count, size, device)
    acknowledge_monitor_command(device=device)
    
    return result
    
def monitor_write_generic(address, values, type, size, device, immediate=False):
    count = len(values)
    if immediate and (count*size > 128):
        raise RuntimeError("Immediate write size exceeds 128 bits.")
    
    write_monitor_command_address(address, device)
    device.da.dmxsegwrite(COM_BUFFER_COUNT, count, 32)
    
    values_addr = COM_BUFFER_DATA if immediate else DATA_BUFFER
    write_buffer(values_addr, values, size, device)
    
    command = MONITOR_COMMAND_WRITE_IMMEDIATE if immediate else MONITOR_COMMAND_WRITE
    write_monitor_command(command, type, size=size, device=device)
    
    wait_for_command_completion(device)
    acknowledge_monitor_command(device=device)
    
def monitor_read_memory(address, type=MDIMIPGVIRTUAL, count=1, size=32, immediate=False, device=None):
    '''
    Read memory using the data buffer for the results. Operations larger than the 
    buffer will be split into multiple commands but still return a single result.
    '''
    device = get_device(device)
    
    #Large operations need to be split into data buffer sized chunks
    size_bytes = size//8
    buffer_size = COM_BUFFER_DATA_SIZE if immediate else DATA_BUFFER_SIZE
    section_elements = buffer_size // size_bytes
    results = []
    
    for remaining in range(count, 0, -section_elements):
        results.extend(
            monitor_read_generic(
                address, 
                section_elements if remaining > section_elements else remaining, 
                type, size, device, immediate=immediate)
            )
        address += section_elements*size_bytes
        
    return results
    
def monitor_write_memory(address, values, type=MDIMIPGVIRTUAL, count=1, size=32, immediate=False, device=None):
    '''
    Write memory using the data buffer for input. Operations larger than the 
    data buffer will be split into multiple commands. 
    '''
    device = get_device(device)
    
    #Split large writes into data buffer sized chunks
    size_bytes = size//8
    buffer_size = COM_BUFFER_DATA_SIZE if immediate else DATA_BUFFER_SIZE
    section_elements = buffer_size // size_bytes
    
    for remaining in range(count, 0, -section_elements):
        monitor_write_generic(
            address, 
            values[:section_elements] if remaining > section_elements else values,
            type, size, device, immediate=immediate)
        address += section_elements*size_bytes
        values = values[section_elements:]
    
def monitor_read_gp_register(index, count=1, immediate=False, device=None):
    '''
    Read some number of GP registers starting from index.
    '''
    device = get_device(device)
    return monitor_read_generic(index, count, MDIMIPCPU, 64, device, immediate=immediate)
    
def monitor_write_gp_register(index, values, immediate=False, device=None):
    '''
    Write some number of GP registers starting from index. 
    '''
    device = get_device(device)
    monitor_write_generic(index, values, MDIMIPCPU, 64, device, immediate=immediate)

def monitor_read_shadow_gp_register(set, index, count, immediate=False, device=None):
    '''
    Read some number of shadow registers from the given set, starting at the given index.
    '''
    device = get_device(device)
    return monitor_read_generic(bank_select_addr(set, index), count, MDIMIPSHADOW, 
        64, device, immediate=immediate)

def monitor_write_shadow_gp_register(set, index, values, immediate=False, device=None):
    '''
    Write some number of shadow registers from the given set, starting at the given index.
    '''
    device = get_device(device)
    monitor_write_generic(bank_select_addr(set, index), values, 
        MDIMIPSHADOW, 64, device, immediate=immediate)
    
def monitor_read_cp0_register(bank, select, count, immediate=False, device=None):
    '''
    Read some number of CP0 registers starting at (bank, select) incrementing bank. 
    '''
    device = get_device(device)
    return monitor_read_generic(bank_select_addr(bank, select), count, 
        MDIMIPCP0, 64, device, immediate=immediate)
        
def monitor_read_many_cp0_registers(bank_selects, device=None):
    '''
    Read a list of CP0 registers where bank_selects is a list of tuples (bank, select).
    '''
    device = get_device(device)
    
    #Indexes go in the data buffer (64 bit values for convenience)
    data = [bank_select_addr(b, s) for b, s in bank_selects]
    write_buffer(DATA_BUFFER, data, 64, device)
    device.da.dmxsegwrite(COM_BUFFER_COUNT, len(bank_selects), 32)
        
    write_monitor_command(MONITOR_COMMAND_READ_MANY, MDIMIPCP0, size=64, device=device)
    wait_for_command_completion(device)
    
    #Results are in the data buffer, overwriting the indexes
    res = read_buffer(DATA_BUFFER, len(bank_selects), 64, device)
    acknowledge_monitor_command(device)
    return res
    
def monitor_write_many_cp0_registers(bank_selects, values, device=None):
    '''
    Write a list of CP0 registers where bank_selects is a list of tuples (bank, select)
    and values is a list of the same size.
    '''
    device = get_device(device)
    
    data = []
    for bank_select, value in zip(bank_selects, values):
        bank, select = bank_select
        data.extend([bank_select_addr(bank, select), value])
    write_buffer(DATA_BUFFER, data, 64, device)
        
    device.da.dmxsegwrite(COM_BUFFER_COUNT, len(bank_selects), 32)
    
    write_monitor_command(MONITOR_COMMAND_WRITE_MANY, MDIMIPCP0, size=64, device=device)
    wait_for_command_completion(device)
    acknowledge_monitor_command(device)

def monitor_write_cp0_register(bank, select, values, immediate=False, device=None):
    '''
    Write some number of CP0 registers starting at (bank, select) incrementing 
    bank.
    '''
    device = get_device(device)
    monitor_write_generic(bank_select_addr(bank, select), values, 
        MDIMIPCP0, 64, device, immediate=immediate)

def monitor_read_cp1_register(index, count, immediate=False, device=None):
    '''
    Read some number of CP1 registers, starting from index. 
    '''
    device = get_device(device)
    return monitor_read_generic(index, count, MDIMIPCP1, 64, device, immediate=immediate)
    
def monitor_write_cp1_register(index, values, immediate=False, device=None):
    '''
    Write some number of CP1 registers, starting at index. 
    '''
    device = get_device(device)
    monitor_write_generic(index, values,  MDIMIPCP1, 64, device, immediate=immediate)
    
def monitor_read_cp1c_register(index, count, immediate=False, device=None):
    '''
    Read some number of CP1C registers, starting at index. 
    '''
    device = get_device(device)
    return monitor_read_generic(index, count, MDIMIPCP1C, 32, device, immediate=immediate)
    
def monitor_write_cp1c_register(index, values, immediate=False, device=None):
    '''
    Write some number of CP1C registers, starting at index. 
    '''
    device = get_device(device)
    monitor_write_generic(index, values, MDIMIPCP1C, 32, device, immediate=immediate)
    
def monitor_read_msa_control_register(index, count, immediate=False, device=None):
    '''
    Read some number of MSA control registers starting from index. 
    '''
    device = get_device(device)
    return monitor_read_generic(index, count, MDIMIPMSACTL, 32, device, immediate=immediate)
    
def monitor_write_msa_control_register(index, values, device=None):
    '''
    Write some number of MSA control registers, using the command buffer for input. 
    '''
    device = get_device(device)
    return monitor_write_generic(index, values, MDIMIPMSACTL, 32, device)
    
def monitor_read_msa_register(index, count, device=None):
    '''
    Read some number of MSA W registers starting at index. 
    '''
    device = get_device(device)
    return monitor_read_generic(index, count, MDIMIPMSAW, 128, device)
    
def monitor_write_msa_register(index, values, device=None):
    '''
    Write some number of MSA W registers starting at index. 
    '''
    device = get_device(device)
    return monitor_write_generic(index, values, MDIMIPMSAW, 128, device)
    
def monitor_read_fpu_single_register(index, count, device=None):
    '''
    Read some number of 32 bit FPU registers, starting at index.
    '''
    device = get_device(device)
    return monitor_read_generic(index, count, MDIMIPFP, 32, device)
    
def monitor_write_fpu_single_register(index, values, device=None):
    '''
    Write some number of 32 bit FPU registers starting at index. 
    '''
    device = get_device(device)
    return monitor_write_generic(index, values, MDIMIPFP, 32, device) 
    
def monitor_read_fpu_double_register(index, count, device=None):
    '''
    Read some number of 64 bit FPU registers, starting at index.
    '''
    device = get_device(device)
    return monitor_read_generic(index, count, MDIMIPDFP, 64, device)
    
def monitor_write_fpu_double_register(index, values, device=None):
    '''
    Write some number of 64 bit FPU registers starting at index. 
    '''
    device = get_device(device)
    return monitor_write_generic(index, values, MDIMIPDFP, 64, device)
    
def monitor_read_guest_cp0_register(bank, select, count, device=None):
    '''
    Read some number of guest CP0 registers starting at (bank, select), 
    incrementing bank. 
    '''
    device = get_device(device)
    return monitor_read_generic(bank_select_addr(bank, select), count, 
        MDIMIPGCP0, 64, device)

def monitor_write_guest_cp0_register(bank, select, values, device=None):
    '''
    Write some number of guest CP0 registers starting at (bank, select), 
    incrementing bank. 
    '''
    device = get_device(device)
    return monitor_write_generic(bank_select_addr(bank, select), values, 
        MDIMIPGCP0, 64, device)
    
def monitor_read_pc(device=None):
    '''
    Read the current PC. Note that all DEPC operations are redirected to the PC 
    in the saved context as DEPC may be modified further by exceptions in debug mode. 
    '''
    device = get_device(device)
    return monitor_read_generic(0, 1, MDIMIPPC, 64, device, immediate=True)[0]
    
def monitor_write_pc(value, device=None):
    '''
    Write the PC. 
    '''
    device = get_device(device)
    monitor_write_generic(0, [value], MDIMIPPC, 64, device, immediate=True)
    
def monitor_resume(core, vpe, device=None):
    '''
    Exit debug mode. This process involves restoring applying any changes to the 
    saved registers/PC and handling pending exceptions if present. 
    '''
    device = get_device(device)
    
    write_monitor_command(MONITOR_COMMAND_RESUME, 0, device=device)
    wait_for_command_completion(device)
    acknowledge_monitor_command(device=device)

    vc_control = 1
    while vc_control != 0:
        vc_control = device.da.read_vc_control1(core, vpe)

    device.da.set_global_throttle(True)
    device.da.write_vc_control1(core, vpe, 1)

    from imgtec.console.dbudriver import dbustep, RBHeader
    num_steps = 0
    deret_executed = False
    while num_steps < 20:
        hdr = RBHeader(device.tiny.rbheader())

        if ((hdr.dest_id == 0x25) and 
            (hdr.core_id == core) and 
            (hdr.vpe_id == vpe) and
            (hdr.mcmd == 2)):
            dbustep(verbose=False)
            num_steps += 1

            if hdr.addr == DERET_ADDR:
                deret_executed = True
                break

    if not deret_executed:
        raise RuntimeError("Resume did not reach deret within the expected number of steps.")

    device.da.write_ejtag_brk_mask(0x0)

    #Even if it re-entered it will have stopped as GT=1
    #If this were the probe we would...
    #device.da.write_vc_control1(core, vpe, 0)
    #but that's all manual for this wrapper.

    #Then remove GT so it'll run again if it did DINT
    device.da.set_global_throttle(False)
    
cache_op_params = namedstruct('cache_op_params', 
        ('I command=0', 'Q address=0', 'I count=0', 'I pad=0', 
         'I line_size=0', 'I op=0', 'I flags=0'), 
        prefix='<', 
        expected_size = 32)
    
def monitor_cache_op(address, line_size, op, count, flags, device=None):
    '''
    Perform a cache operation. See CSUtils.DAtiny.CacheOperation.
    '''
    device = get_device(device)
    com_buffer = cache_op_params(address=address,
                                 count=count,
                                 line_size=line_size,
                                 op=op, #cache type is already ored in here
                                 flags=flags)
    
    #Make this into bytes
    data = com_buffer._pack()
    #Unpack as 32 bit words, ignore command
    data = struct_unpack(data, 4, False)[1:]
    
    #Write everything but command
    write_buffer(COM_BUFFER_ADDR, data, 32, device)
        
    #Write the command, sets flags
    write_monitor_command(MONITOR_COMMAND_CACHE_OP, 0, device=device)
    wait_for_command_completion(device)
    acknowledge_monitor_command(device)
    
def monitor_tlb_probe(entryhi, guestctl1=0, guest=False, device=None):
    '''
    Look for a TLB entry containing entryhi and if one is found return the rest
    of the entry. Optionally match against guestctl1 also, and use guest TLB if
    guest is set.
    '''
    device = get_device(device)
    
    #Order in data buffer is entrylo0, entrylo1, entryhi, pagemask, guestctl1
    
    #EntryHi and guestctl1 are inputs, the rest are outputs of the search
    device.da.dmxsegwrite(DATA_BUFFER+16, entryhi, 64, device)
    device.da.dmxsegwrite(DATA_BUFFER+32, guestctl1, 32, device)
    
    #Set type to differentiate from guest/normal
    write_monitor_command(MONITOR_COMMAND_TLB_PROBE, 
                          MDIMIPGTLB if guest else MDIMIPTLB, 
                          device=device)
    wait_for_command_completion(device)
    
    #Read index back from end of command buffer
    index = device.da.dmxsegread(COM_BUFFER+28, 32)
    
    #If the top bit is set then an entry was found
    if index & 0x80000000:
        #Mask out actual index
        index = index & 0x1F
        #We already know entryhi and guestctl1
        entrylo0, entrylo1, _, pagemask = read_buffer(DATA_BUFFER, 4, 64, device)
        mmid = read_buffer(DATA_BUFFER+TLB_Entry._size-4, 1, 32, device)
        #Pagemask is only 32 bit
        pagemask &= MASK_32_BIT
        acknowledge_monitor_command(device=device)
        return (index, entrylo0, entrylo1, entryhi, pagemask, guestctl1, mmid)
    else:
        acknowledge_monitor_command(device=device)
        raise DebugMonitorError("No TLB entry found for EntryHi 0x%x (GuestCtl1 0x%0x)" % (entryhi, guestctl1))
       
TLB_Entry = namedstruct('TLBEntry', 
                        ('Q entrylo0=0', 'Q entrylo1=0', 'Q entryhi=0', 'Q pagemask=0', 'L guestctl1=0', 'L mmid=0'), 
        prefix='<', 
        expected_size = 40)
       
def monitor_read_tlb(index, count, guest=False, device=None):
    '''
    Read a number of tlb entries starting at the given index. Returns a list of 
    entries as named structures giving access to the register values of each 
    entry. Uses guest tlb if 'guest' is True.
    '''
    device = get_device(device)
    
    #Can't use the generic method because of a count->size mismatch
    write_monitor_command_address(index, device)
    write_monitor_command_count(count, device)
    
    access_type = MDIMIPGTLB if guest else MDIMIPTLB
    write_monitor_command(MONITOR_COMMAND_READ, access_type, device=device)
    wait_for_command_completion(device)
    
    result = [read_buffer(DATA_BUFFER+(i*TLB_Entry._size), TLB_Entry._size//4, 32, device) for i in range(count)]
    acknowledge_monitor_command(device=device)
    
    #Pack as 32 bit words, then unpack into 'TLB_Entry's
    return [TLB_Entry._unpack(struct_pack(res, 4, False)) for res in result]
    
def monitor_write_tlb(index, entries, guest=False, device=None):
    '''
    Write TLB entries starting at the given index. Where entries is a list of 
    lists, each inner list containing the 5 register values that make up one entry.
    (leave guestctl1 empty for non vz systems)
    [[EntryLo0, EntryLo1, EntryHi, PageMask, Guestctl1], [...], [etc],]
    Uses guest tlb if 'guest' is True.
    '''
    device = get_device(device)
    count = len(entries)
    
    write_monitor_command_address(index, device)
    write_monitor_command_count(count, device)
    
    #Convert to TLB entries, pack into bytes, unpack as 32 bit words
    entries_as_words = []
    for entry in entries:
        #Convert to a TLB entry
        t = TLB_Entry(*entry)
        #Pack into a struct
        t = t._pack()
        #Unpack it as 32 bit words and add it to the end of the list
        entries_as_words.extend(struct_unpack(t, 4, False))
    
    #Write entries into the data buffer
    write_buffer(DATA_BUFFER, entries_as_words, 32, device)
    
    access_type = MDIMIPGTLB if guest else MDIMIPTLB
    write_monitor_command(MONITOR_COMMAND_WRITE, access_type, device=device)
    wait_for_command_completion(device)
    acknowledge_monitor_command(device=device)
    
