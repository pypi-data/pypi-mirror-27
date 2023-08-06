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
from imgtec.lib import rst

INVALID_GUEST_ID = 0x1ff

TinyBreakpointType = namedenum('TinyBreakpointType',
    Software   = 0,
    Hardware   = 1,
    Data_Watch = 2, 
)

def bp_titles(guest):
    titles = ['ID', 'Address', 'Enabled', 'Type', 'Data', 'HW Index', 'Action']
    if guest:
        titles.append('Guest ID')
    return titles

class TinyDABreakpoint(object):
    def __init__(self, bpid, address, enabled, active, type, isa, hw_index, data,
        address_mask, access_type, access_size, watch_value, watch_value_mask, action, 
        guest_id, *extras):
        ## Generic ##
        
        # Console ID of the bkpt. (which is the TinyDA ID but -ve)
        self.bpid = bpid
        
        # The address of the breakpoint.
        self.address = address
        
        # Whether the breakpoint is currently enabled.
        self.enabled = enabled
        
        # Whether the breakpoint is currently active.
        self.active = active
        
        # type of breakpoint, see TinyBreakpointType
        self.type = TinyBreakpointType(type)
        
        # The isa of the instruction breakpointed.
        self.isa = isa
        
        ## Software only ##
        
        # The byte data for the instruction replaced by a software breakpoint (MSB first)
        self.data = data
        
        # Formatted string of the data
        self.formatted_data = self.format_watch(watch_value) if self.type == TinyBreakpointType.Data_Watch else self.format_data(data)
        
        ## Hardware only ##
        
        #The hardware resource used
        self.hw_index = hw_index
        
        # Mask applied to address when matching
        self.address_mask = address_mask
        
        ## Data watch only ##
        
        # 'read'/'write'/'both'
        self.access_type = access_type
        
        # 8,16 or 32
        self.access_size = access_size
        
        # Value to match
        self.watch_value = watch_value
        
        # Mask applied to the value (whole bytes only, e.g 0xff00ff00)
        self.watch_value_mask = watch_value_mask
        
        self.action = action
        
        self.guest_id = guest_id
        
        self.has_vz = False
        self._extras = extras
        
    @property
    def _bpid(self):
        #Use this ID when calling device.tiny methods
        return self.bpid*-1
        
    def format_data(self, data):
        if not data:
            return 'None'
        else:
            return '0x' + ''.join('%02x' % x for x in data)
        
    def format_watch(self, data):
        if not data:
            return 'None'
        else:
            return '0x' + '%x' % (data,)

    def _for_display(self):
        if self.type == TinyBreakpointType.Software:
            type_string = 'sw'
        elif self.type == TinyBreakpointType.Hardware:
            type_string = 'hw'
        elif self.type == TinyBreakpointType.Data_Watch:
            type_string = 'dw'
        else:
            type_string = '?'
            
        items = [str(self.bpid), 
                "0x%x" % self.address, 
                ['Disabled', 'Enabled'][self.enabled], 
                type_string, 
                self.formatted_data,
                str(self.hw_index),
                self.action]
                
        if self.has_vz:
            if self.type == TinyBreakpointType.Software:
                items.append("-")
            else:
                items.append("All" if self.guest_id == INVALID_GUEST_ID else str(self.guest_id))
        
        return items
                    
    def __repr__(self):
        vals = [self._for_display()]
        return rst.simple_table(bp_titles(self.has_vz), vals)
        
    def __eq__(self, rhs):
        return self._as_tuple() == rhs._as_tuple()
        
    def _as_tuple(self):
        return (self.bpid, self.address, self.enabled, self.active, self.type, 
            self.isa, self.hw_index, self.data, self.action, self._extras)
    
class BreakpointListResult(list):
    '''A list of breakpoints.  Items of this list are of type Breakpoint.'''
    def __init__(self, items, has_vz):
        for item in items:
            item.has_vz = has_vz
        list.__init__(self, items)
        self.has_vz = has_vz
    
    def __repr__(self):
        vals = [b._for_display() for b in self]
        return rst.simple_table(bp_titles(self.has_vz), vals)
        
def all_breakpoints(device):
    bpids = device.tiny.GetAllBreakpointIDs()
    bps = {}
    for bpid in bpids:
        tbp = device.tiny.GetBreakpoint(bpid)
        #IDs are +ve in TinyDashScript -ve in Console
        bpid *= -1
        bp = TinyDABreakpoint(bpid, *tbp)
        bps[bpid] = bp
    return bps
    
def get_breakpoint(bpid, device):
    #Bpid passed in is the +ve one from TinyDA, we return the -ve id for Console
    return TinyDABreakpoint(-bpid, *device.tiny.GetBreakpoint(bpid))
    
def activate(bp, device):
    if not bp.active:
        if bp.enabled:
            device.tiny.SuppressBreakpoint(bp._bpid, False)
            bp.active = True
            
def activate_all_bps(device):
    for b in all_breakpoints(device).values():
        activate(b, device) 

def suppress(bp, device):
    if bp.active:
        device.tiny.SuppressBreakpoint(bp._bpid, True)
        bp.active = False

def suppress_all_bps(device):
    for b in all_breakpoints(device).values():
        suppress(b, device)

def get_bpid_for_address(address, bkpts):
    found = []
    for bp in bkpts.values():
        if bp.address == address:
            found.append(bp.bpid)
            
    if not found:
        raise RuntimeError("No breakpoint at address: 0x%08x" % address)
    elif len(found) > 1:
        raise RuntimeError("Found multiple breakpoints at address 0x%08x, please use a breakpoint ID instead." % address)
    else:
        #Found a single breakpoint
        return found[0]
        
def generic_bkpt_operation(address_or_bpid, isa, options, device, op, args):
    #Ends up with a bp ID and calls op(*args)
    all_bkpts = all_breakpoints(device)
    if address_or_bpid == "all":
        for bpid in all_bkpts:
            generic_bkpt_operation(bpid, isa, options, device, op, args)
    elif address_or_bpid < 0:
        #Must be an ID
        try:
            bp = all_bkpts[address_or_bpid]
            op(bp._bpid, *args)
        except KeyError:
            raise RuntimeError("No breakpoint found with ID %d" % address_or_bpid)
    else:
        generic_bkpt_operation(get_bpid_for_address(address_or_bpid, all_bkpts), 
            isa, options, device, op, args)

def bkpt_disable(address_or_bpid, isa, options, device):
    generic_bkpt_operation(address_or_bpid, isa, options, device, device.tiny.EnableBreakpoint, [False])

def bkpt_enable(address_or_bpid, isa, options, device):
    generic_bkpt_operation(address_or_bpid, isa, options, device, device.tiny.EnableBreakpoint, [True])

def bkpt_clear(address_or_bpid, isa, options, device):
    generic_bkpt_operation(address_or_bpid, isa, options, device, device.tiny.DeleteBreakpoint, [])
            
def bkpt_refresh(address_or_bpid, isa, options, device):
    generic_bkpt_operation(address_or_bpid, isa, options, device, device.tiny.RefreshBreakpoint, [])

def bkpt_sethw(address, isa, options, hw_index, device):
    bpid = device.tiny.CreateBreakpoint(address, TinyBreakpointType.Hardware, isa, options, hw_index)
    return get_breakpoint(bpid, device)

def bkpt_setsw(address, isa, options, device):
    bpid = device.tiny.CreateBreakpoint(address, TinyBreakpointType.Software, isa, options)
    return get_breakpoint(bpid, device)
    
def bkpt_setdw(address, isa, options, hw_index, device):
    bpid = device.tiny.CreateBreakpoint(address, TinyBreakpointType.Data_Watch, isa, options, hw_index)
    return get_breakpoint(bpid, device)
    
def bkpt_set(address, isa, options, device):
    try:
        return bkpt_setsw(address, isa, options, device)
    except RuntimeError:
        return bkpt_sethw(address, isa, options, -1, device)
        
def bkpt_test(address, isa, options, device):
    bkpt_setsw(address, isa, options, device)
    bkpt_clear(address, isa, options, device)
    return True
    
def bkpt_init_from_hardware(_address, _isa, _options, device):
    device.tiny.InitBreakpointsFromHardware()

setsw   = named('setsw')
sethw   = named('sethw')
setdw   = named('setdw')
clear   = named('clear')
test    = named('test')
refresh = named('refresh')
initfromhardware = named('initfromhardware')



bkpt_cmds = dict(test=bkpt_test,
            set=bkpt_set,
            setsw=bkpt_setsw,
            sethw=bkpt_sethw,
            setdw=bkpt_setdw,
            clear=bkpt_clear,
            enable=bkpt_enable,
            disable=bkpt_disable,
            refresh=bkpt_refresh,
            initfromhardware=bkpt_init_from_hardware,
            )
            
@command(cmd=[namedstring(set), namedstring(setsw), namedstring(sethw), namedstring(setdw),
        namedstring(clear), namedstring(enable), namedstring(disable), namedstring(test), 
        namedstring(refresh), namedstring(initfromhardware)],
        address=[named_all],
        isa=named_isas,
        )
def bkpt(cmd=None, address=None, isa='auto', options=None, hw_index = -1, device=None):
    """Manage breakpoints.

    This command adds, modifies, or deletes breakpoints from the active 
    breakpoint list.
    
    Some commands can be given an ID instead of an address and this is required when there
    are multiple breakpoints on the same address. For example:
    
    == ========== ======= ==== ==== ========
    ID Address    Enabled Type Data HW Index
    == ========== ======= ==== ==== ========
    -1 0xbfc00014 Enabled hw   None 0
    == ========== ======= ==== ==== ========
    
    The breakpoint above could be disabled by using bkpt(disable, 0xbfc00014) or bkpt(disable, -1).
    
    Valid options are:

    ========================== ======================================================================
    Syntax                     Description
    ========================== ======================================================================
    bkpt(set, addr)            Add breakpoint. Try to set a software breakpoint first and if that 
                               fails use a hardware breakpoint.
    bkpt(sethw, addr)          Add a hardware breakpoint at addr.
    bkpt(setsw, addr)          Add a software breakpoint at addr.
    bkpt(setdw, addr)          Add a data watch breakpoint for addr.
    bkpt(clear, addr or id)    Remove breakpoint at addr or with an ID of id.
    bkpt(clear, all)           Remove all breakpoints.
    bkpt(enable, addr or id)   Enable breakpoint at addr or with an ID of id.
    bkpt(enable, all)          Enable all breakpoints.
    bkpt(disable, addr)        Disable breakpoint at addr or with an ID of id.
    bkpt(disable, all)         Disable all breakpoints.
    bkpt(test, addr)           Test that the address can accept a software breakpoint.
    bkpt(refresh, addr or id)  Rewrite breakpoint at addr or with an ID of id, applying the current
                               settings to the target.
    bkpt(refresh, all)         Refresh all breakpoints.
    bkpt(initfromhardware)     Removes all existing non software breakpoint settings and replaces
                               them with any hardware or data watch breakpoints which are enabled 
                               on the target. Features not supported by Codescape Console are
                               removed (see the options table below).
    ========================== ======================================================================
    
    The return value depends on the command. For set, sethw, setsw, and setdw then the created
    breakpoint is returned.  For all other commands a list of all breakpoints is returned.

    Specify the isa using the named parameters below to override the auto detected isa.

    * MIPS32 instructions are always on word boundaries (0, 4, 8, etc.).

    * MIPS16 and microMIPS instructions can be one or two halfwords and are therefore on
      halfword boundaries (0, 2, 4, etc.).

    * When setting a breakpoint, use mips16|mips32|micromips to determine the type. Once
      set, MIPS16 and microMIPS breakpoints are shown with the least significant bit (bit 0)
      set ("1") to differentiate it from MIPS32 breakpoints (LSB is "0").
      
    * 'options' can be set to a dictionary of breakpoint attributes as defined by the table below.
    
    ================= ======================= ======================================================
    Option            Breakpoint Type         Description
    ================= ======================= ======================================================
    address_mask      hardware and data watch Mask applied to the address when matching. Set a bit 
                                              to 1 to not compare it.
    access_size       data watch              Size of access to break on. One of 8,16 or 32.
    access_type       data watch              Type of data access to break on. One of 'read', 
                                              'write' or 'both'. 
    watch_value       data watch              Value to break on.
    watch_value_mask  data watch              Mask applied to the value, which must consist of whole 
                                              bytes. For example 0x00ff is valid, 0x000f is not.
    action            hardware and data watch Action to perform when breakpoint is triggered.
    guest_id          hardware and data watch Guest ID to match. The breakpoint will match any Guest
                                              ID in the case that this is not set, or is set with a 
                                              value of 0x1ff.
    ================= ======================= ======================================================

    Valid actions are:
    
    ================== =======================================================================
    Action             Description
    ================== =======================================================================
    breakpoint         Behave as regular breakpoint, i.e. halt or enter debug mode (default).
    triggerpoint       Set triggered status bit, do not halt/enter debug mode.
    trace_start        Cause trace to start.
    trace_stop         Cause trace to stop.
    trace_start_pm     Start trace and dump performance counters.
    trace_stop_pm      Stop trace and dump performance counters.
    trace_start_all    Start trace on both this core and on components of the coherent system.
    trace_stop_all     Stop trace on both this core and on components of the coherent system.
    trace_start_all_pm Start trace on both this core and on components of the coherent system 
                       and dump performance counters.
    trace_stop_all     Stop trace on both this core and on components of the coherent system 
                       and dump performance counters.
    ================== =======================================================================
            
    For example:
        
        >>> bkpt(setdw, 0x80000000, options={'access_type':'read', 'access_size':32})

    """
    from imgtec.console.generic_device import cpuinfo
    has_vz = cpuinfo(device)['has_vze']
    
    if options is None:
        options = {}
    result = None
    if cmd is not None:
        try:
            fn = bkpt_cmds[cmd]
        except KeyError:
            name = getattr(cmd, '__name__', '') or str(cmd)
            raise RuntimeError('Unknown breakpoint command %s' % (cmd,))
        else:
            if address is None:
                name = getattr(cmd, '__name__', '') or str(cmd)
                if name != 'initfromhardware':
                    raise TypeError("bpkt(%s) address or ID argument is required." % (name,))
            elif isinstance(address, TinyDABreakpoint):
                address = address.bpid
            elif address != 'all':
                address = eval_address(device, address)
            if fn == bkpt_sethw or fn == bkpt_setdw:
                result = fn(address, isa, options, hw_index, device)
            elif hw_index != -1:
                raise RuntimeError("Hardware index is only valid when creating hardware breakpoints. %d", (hw_index,))
            else:
                result = fn(address, isa, options, device)
    if result is not None:
        try:
            result.has_vz = has_vz
        except AttributeError:
            pass
        return result
    return BreakpointListResult([value for _addr, value in sorted(all_breakpoints(device).items())], has_vz)
