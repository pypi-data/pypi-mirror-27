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
from imgtec.console.results import *
from imgtec.console.regs import regs, regtype
from imgtec.lib.rst import simple_table
from imgtec.console.generic_device import cpuinfo
from imgtec.lib.namedbitfield import namedbitfield, compile_fields
from imgtec.console.commands import reset
from imgtec.console.regs import RegTypeException
from imgtec.console.breakpoints import initfromhardware
from imgtec.console.generic_device import onhaltcallback

class PerfCountException(Exception):
    pass
    
#Constant regtype so we don't have to deal with dissapearing fields between targets
PerfCtlValue = namedbitfield('PerfCtlValue', compile_fields('''\
    M     31
    TCID  29 22
    MT_EN 21 20
    VPEID 19 16
    PCTD  15
    Event 12 5
    IE    4
    U     3 
    S     2
    K     1
    EXL   0'''.splitlines()), show_raw_value=True)

class PerfCounterSettingList(list):
    def __repr__(self):
        return simple_table(
            self[0].titles if self else PerfCounterSetting.base_titles, 
            [s.get_table_row() for s in self])
    
class PerfCounterSetting(object):
    base_titles = ['Counter', 'Event', 'Interrupt Enable', 'Count User', 
                  'Count Supervisor', 'Count Kernel', 'Count EXL']
    
    def __init__(self, counter, event, interrupt_enable, count_user, count_supervisor, count_kernel, 
        count_exl, event_type, tcid, mt_en, vpeid, pctd, has_pd_trace=False, has_mt=False):
        #Aka register number
        self.counter           = counter
        #Event number
        self.event             = event
        #Enum type or None
        self.event_type        = event_type
        #Generate interrupts when half full
        self.interrupt_enable  = interrupt_enable
        #Count in various modes
        self.count_user        = count_user
        self.count_supervisor  = count_supervisor
        self.count_kernel      = count_kernel
        self.count_exl         = count_exl
        
        #Used if the target has MT ASE
        self.tcid              = tcid
        self.mt_en             = mt_en
        self.vpeid             = vpeid
        
        #Used if the target has PDTrace 
        self.pctd              = pctd
        
        #Save state for re-enabling
        self.enable_state = [('interrupt_enable', interrupt_enable),
                             ('count_user'      , count_user),
                             ('count_supervisor', count_supervisor),
                             ('count_kernel'    , count_kernel),
                             ('count_exl'       , count_exl),
                            ]
                            
        self.has_pd_trace = has_pd_trace
        self.has_mt       = has_mt
        self.titles       = self.set_titles()
                                  
    @classmethod
    def from_register(cls, counter, value, has_pd_trace, has_mt):
        '''Given a counter number and register value return a settings object if 
        any counting is enabled, otherwise return None.'''
        
        #Value will almost always have a class but we'll do this for consistency
        t = PerfCtlValue(value)
        
        if any([t.U, t.S, t.K, t.EXL]):
            #The event type we'll try to get from value's original class
            return cls(counter, t.Event, bool(t.IE), bool(t.U), bool(t.S), 
                        bool(t.K), bool(t.EXL), get_event_type(type(value)),
                        t.TCID, t.MT_EN, t.VPEID, bool(t.PCTD), has_pd_trace, 
                        has_mt)
        else:
            return None
            
    def disable(self):
        #Set all boolean fields False
        for attr, _value in self.enable_state:
            setattr(self, attr, False)
    
    def enable(self):
        #Restore from saved state
        for attr, value in self.enable_state:
            setattr(self, attr, value)
        
    def regmodify_args(self):
        return {
            'TCID'  : self.tcid,
            'MT_EN' : self.mt_en,
            'VPEID' : self.vpeid,
            'PCTD'  : self.pctd,
            'Event' : self.event,
            'IE'    : self.interrupt_enable,
            'U'     : self.count_user,
            'S'     : self.count_supervisor,
            'K'     : self.count_kernel,
            'EXL'   : self.count_exl,
        }
        
    def write_to_target(self, device):
        device.tiny.WriteRegister(control_reg_name(self.counter), 
                                  PerfCtlValue(**self.regmodify_args()))
        
    def format_event(self):
        if self.event_type is not None:
            return '%d (%s)' % (self.event, self.event_type(self.event))
        else:
            return str(self.event)
            
    def format_mt_en(self):
        return {0 : '0 (all))',
                1 : '1 (VPEs)',
                2 : '2 (TCs)',
               }.get(self.mt_en, str(self.mt_en))
            
    def get_table_row(self):
        row = [str(self.counter), self.format_event()]
        row.extend([str(item) for item in [self.interrupt_enable, self.count_user,
                    self.count_supervisor, self.count_kernel, self.count_exl]]) 
        if self.has_pd_trace:
            row.append(str(self.pctd))
        if self.has_mt:
            row.extend([str(self.tcid), str(self.vpeid), self.format_mt_en()])
        return row
        
    def set_titles(self):
        titles = self.base_titles[:]
        if self.has_pd_trace:
            titles.append('PCTD')
        if self.has_mt:
            titles.extend(['TCID', 'VPEID', 'MT_EN'])
        return titles
        
    def __repr__(self):
        return simple_table(
            self.titles,
            [self.get_table_row()],
        )
        
    def _as_tuple(self):
        return (self.counter,
                self.event,
                self.event_type,
                self.interrupt_enable,
                self.count_user,
                self.count_supervisor,
                self.count_kernel,
                self.count_exl,
                self.tcid,
                self.mt_en,
                self.vpeid,
                self.pctd,
                self.enable_state,
                self.has_pd_trace,
                self.has_mt,
                self.titles,
               )
               
    def __eq__(self, rhs):
        if isinstance(rhs, PerfCounterSetting):
            return self._as_tuple() == rhs._as_tuple()
        else:
            return False

class PerfCounterResultList(list):
    def __repr__(self):
        return simple_table(PerfCounterResult.result_titles, [r.get_table_row() for r in self])
    
class PerfCounterResult(long):
    result_titles = ['Counter', 'Event', 'Value', 'Delta', 'Wrapped']
    
    def __new__(cls, counter, event, event_str, value, delta, wrapped):
        new = super(PerfCounterResult, cls).__new__(cls, value)
        new.counter   = counter
        new.event     = event
        #Event name as a string (not a type)
        new.event_str = event_str
        new.value     = value
        new.delta     = delta
        new.wrapped   = wrapped
        return new
        
    def get_table_row(self):
        return [str(self.counter), self.event_str, str(self.value), str(self.delta), str(self.wrapped)]
        
    def __repr__(self):
        return simple_table(PerfCounterResult.result_titles, [self.get_table_row()])

def control_reg_name(num):
    return 'PerfCtl%d' % num

def read_reg_name(num):
    return 'PerfCnt%d' % num

def get_event_type(reg_type):
    '''Given a register type try to get the 'Event' field's enum type and return
    it or None if there are no fields or no enum.'''
    try:
        for field in reg_type._fields:
            if field.name == 'Event':
                #Will throw on non enums, prevents us showing "1 (1)"
                _ = field.type._items
                return field.type
    except AttributeError:
        return None

read   = named('read')
@command(cmd=[namedstring(set), namedstring(disable), namedstring(reset), 
    namedstring(read), namedstring(enable), namedstring(initfromhardware)])
def perfcnt(cmd='read', counter=None, event=None, interrupt_enable=False, 
    count_user=True, count_supervisor=True, count_kernel=True, count_exl=True, 
    pctd=False, tcid=0, vpeid=0, mt_en=0, reset_count=True, store_result=True, device=None):
    '''
    Setup and read performance counters.
    
    >>> perfcnt(set, 0, 1)
    ======= ========================== ================ ========== ================ ============ =========
    Counter Event                      Interrupt Enable Count User Count Supervisor Count Kernel Count EXL
    ======= ========================== ================ ========== ================ ============ =========
    0       1 (Instructions_completed) False            True       True             True         True
    ======= ========================== ================ ========== ================ ============ =========
    >>> go(); halt()
    Running from 0x9fc00760
    status=running
    ======= ========================== ======= ===== =======
    Counter Event                      Value   Delta Wrapped
    ======= ========================== ======= ===== =======
    0       1 (Instructions_completed) 1240046 None  False
    ======= ========================== ======= ===== =======
    status=stopped pc=0x9fc00730
    0x9fc00730 8f838058    lw        v1, -32680(gp)
    
    The value read will be cached and used to provide a delta for the next read. halt/step also read 
    counters and do the same. To prevent this and keep the currently cached value set 'store_result'
    to False or 'read_perf_counters' to False for halt/step.
    
    The command can be used in the following ways:
    
    ====================================== ======================================================================
    Syntax                                 Description
    ====================================== ======================================================================
    perfcnt(set)                           Show settings of all known counters.
    perfcnt(set, counter=x, event=y, ...)  Setup counter x to count event y with the given parameters. (settings 
                                           not supported on the target are ignored)
    perfcnt(set, counter=x, event=y, ...,  As above but do not reset the counter's value and remove the stored
        reset_count=False)                 previous value.
    perfcnt(read)                          Read the value of all counters which have been setup.
    perfcnt(read, counter=x)               Read the value of counter x.
    perfcnt(reset)                         Reset all counter values to 0 and clear previous values.
    perfcnt(reset, counter=x)              As above but for counter x only.
    perfcnt(disable)                       Disable all performance counters. (disables all counting and 
                                           interrupt generation that was enabled)
    perfcnt(disable, counter=x)            As above but for counter x only.
    perfcnt(enable)                        Enable all performance counters. Only options that were enabled before
                                           using disable will be enabled.
    perfcnt(enable, counter=x)             As above but for counter x only.
    perfcnt(initfromhardware)              Read existing performance counters and store settings for any that
                                           have counting enabled.
    perfcnt(initfromhardware,              As above but do not reset the counter after reading its settings.
        reset_count=False)
    ====================================== ======================================================================
    
    ================ ============================================================================
    Parameter        Meaning
    ================ ============================================================================
    cmd              One of set, reset, disable, enable or initfromhardware.
    counter          Number of the counter to use (0 for PerfCtl0 and so on).
    event            Number of the event to count. Please refer to your target's software user 
                     manual or use regtype with the counter's control register name. It can also 
                     be given as the string name of one of the events as shown by regtype.
    interrupt_enable Whether the counter will generate an interrupt when its top bit is set.
    count_user       Count events in user mode.
    count_supervisor Count events in supervisor mode.
    count_kernel     Count events in kernel mode.
    count_exl        Count events in exception mode.
    pctd             Disable tracing of this performance counter when performance count trace
                     is enabled for PDtrace.
    tcid             The TC from which events should be counted, if per TC counting is enabled.
    vpeid            The VPE from which events should be counted, if per VPE counting is enabled.
                     (all TCs of that VPE)
    mt_en            Which events should be counted when per VPE/TC counting is available. 
                     One of 0 (from all TCs and VPEs), 1 (the VPE given by vpeid) or 2 (the TC 
                     given in tcid).
    reset_count      Set True to reset the counter's value to 0 and clear its previous value
                     during setup or reading it back from hardware.
    store_result     Set False to not store the result of reading a counter. This means that the
                     delta for the next read will be from the previous result.
    ================ ============================================================================
    '''
    if not cpuinfo(update=True, device=device)['has_perf_counters']:
        raise PerfCountException("This target does not have any performance counters.")
        
    if counter is not None:
        num_counters = cpuinfo(update=True, device=device)['num_perf_counters']
        if counter > (num_counters-1):
            raise PerfCountException('This target only has %d performance counter(s).' % num_counters)
        
    if cmd == 'read':
        return read_counter(counter, store_result, device)
    elif cmd == 'set':
        return setup_counter(counter, event, interrupt_enable, count_user, 
            count_supervisor, count_kernel, count_exl, pctd, tcid, vpeid, mt_en, 
            reset_count, device)
    elif cmd == 'disable':
        return disable_counter(counter, device)
    elif cmd == 'reset':
        #Seperate calls because setup also uses reset_counter
        reset_counter(counter, device)
        #Don't store this result (no point showing a delta from 0)
        return read_counter(counter, False, device)
    elif cmd == 'enable':
        return enable_counter(counter, device)
    elif cmd == 'initfromhardware':
        return init_counters_from_hardware(reset_count, device)
    else:
        raise PerfCountException('Unknown perfcnt command.')
        
def check_any_counters(device):
    if not device.perfcount_settings:
        raise PerfCountException('No performance counters have been configured.')
        
def get_counter_settings(counter, device):
    try:
        return device.perfcount_settings[counter]['setting']
    except KeyError:
        raise PerfCountException('Performance counter %d has not been configured.' % counter)
        
def get_all_counter_settings(device):
    return [c['setting'] for c in device.perfcount_settings.values()]

def get_counter_numbers(counter, device):
    '''Given a number or None, check that there are some counters setup, and
    that the specific counter is setup. If counter is None return all counter
    numbers setup.'''
    check_any_counters(device)
    
    counters = []
    if counter is None:
        counters = device.perfcount_settings.keys()
    else:
        get_counter_settings(counter, device)
        counters = [counter]
        
    return counters
    
def init_counters_from_hardware(reset_count, device):
    ci = cpuinfo(update=True, device=device)
    num_counters = ci['num_perf_counters']
    has_pd_trace = ci['has_pd_trace']
    has_mt       = ci['has_mt']
    new_settings = {}
    
    for i in range(num_counters):
        ctl_reg = control_reg_name(i)
        #This uses regs because we want the register's type to get the event type
        new = PerfCounterSetting.from_register(i, regs(ctl_reg, device=device), 
                has_pd_trace, has_mt)
        if new:
            new_settings[i] = {'setting' : new}
            
    device.perfcount_settings = new_settings
    
    #Don't bother to reset if we didn't find anything
    if reset_count and device.perfcount_settings:
        reset_counter(None, device)
        
    return PerfCounterSettingList(get_all_counter_settings(device))
    
def reset_counter(counter, device):
    for _counter in get_counter_numbers(counter, device):
        #Remove cache
        device.perfcount_settings[_counter]['results'] = []
        #Clear the count register
        device.tiny.WriteRegister(read_reg_name(_counter), 0)
        
def enable_counter(counter, device):
    for _counter in get_counter_numbers(counter, device):
        setting = get_counter_settings(_counter, device)
        setting.enable()
        setting.write_to_target(device)
        device.perfcount_settings[_counter]['setting'] = setting
        
    if counter is None:
        return PerfCounterSettingList(get_all_counter_settings(device))
    else:
        return get_counter_settings(counter, device)
        
def disable_counter(counter, device):
    for _counter in get_counter_numbers(counter, device):
        setting = get_counter_settings(_counter, device)
        setting.disable()
        setting.write_to_target(device)
        device.perfcount_settings[_counter]['setting'] = setting
        
    if counter is None:
        return PerfCounterSettingList(get_all_counter_settings(device))
    else:
        return get_counter_settings(counter, device)
        
def _get_event(event, reg_type, ctl_reg):
    if event is None:
        raise PerfCountException('Event number required for setup.')
    elif isinstance(event, basestring):
        #Try to find it in the reg info
        if reg_type is not None:
            try:
                fields = reg_type._fields
            except AttributeError:
                raise PerfCountException("%s does not have a rich type associated with it. Please specify a number for the event." % ctl_reg)
            else:
                for field in fields:
                    if field.name == 'Event':
                        try:
                            return dict(field.type._items())[event]
                        except (AttributeError, KeyError):
                            err_str = "Event '%s' is not valid for this counter. To see a list of events use regtype(\"%s\")."
                            raise PerfCountException(err_str % (event, ctl_reg))
    else:
        if event > 127:
            raise PerfCountException("Invalid event number.")
    
    return event
        
def setup_counter(counter, event, interrupt_enable, count_user, count_supervisor, 
    count_kernel, count_exl, pctd, tcid, vpeid, mt_en, reset_count, device):
    
    #Show all current settings
    if counter is None:
        return PerfCounterSettingList(get_all_counter_settings(device))
    
    ctl_reg = control_reg_name(counter)
    try:
        reg_type = regtype(ctl_reg, device=device)
    except RegTypeException:
        reg_type = None
    
    event = _get_event(event, reg_type, ctl_reg)
            
    if not 0 <= tcid <= 255:
        raise PerfCountException("Invalid TCID (should be 0-255).")
    if not 0 <= vpeid <= 15:
        raise PerfCountException("Invalid VPEID (should be 0-15).")
    if not 0 <= mt_en <= 3:
        raise PerfCountException("Invalid MT_EN (should be 0-3).")

    #Get possible events from the RegDB
    event_type = None
    if reg_type is not None:
        event_type = get_event_type(reg_type)
        
    ci = cpuinfo(device=device)
    new_setting = PerfCounterSetting(counter, event, interrupt_enable,
                    count_user, count_supervisor, count_kernel, count_exl, 
                    event_type, tcid, mt_en, vpeid, pctd, ci['has_pd_trace'], ci['has_mt'])
    new_setting.write_to_target(device)
    
    #Store on the VPE
    device.perfcount_settings[counter] = {'setting' : new_setting, 'results' : []}
    
    if reset_count:
        reset_counter(counter, device)
        
    return new_setting
    
def read_counter(counter, store_result, device):
    check_any_counters(device)
    
    if counter is None:
        #Get all that have been setup
        results = [get_counter_value(setting, store_result, device) for setting in get_all_counter_settings(device)]
        return PerfCounterResultList(results)
    else:
        #Specific counter
        return get_counter_value(get_counter_settings(counter, device), store_result, device)
            
def get_counter_value(setting, store_result, device):
    value = device.tiny.ReadRegister(read_reg_name(setting.counter))
    prev = device.perfcount_settings[setting.counter]['results']
    if prev:
        #There is a previious result
        previous_value = prev[0].value
        delta = value - previous_value
        wrapped = value < previous_value
    else:
        delta = None
        wrapped = False
        
    res = PerfCounterResult(setting.counter, setting.event, setting.format_event(), 
            value, delta, wrapped)
            
    if store_result:
        #Just store the last result for deltas
        device.perfcount_settings[setting.counter]['results'] = [res]
        
    return res


@onhaltcallback('perfcnt')
def read_perfcounters(device):
    if device.perfcount_settings:
        return perfcnt('read', device=device)