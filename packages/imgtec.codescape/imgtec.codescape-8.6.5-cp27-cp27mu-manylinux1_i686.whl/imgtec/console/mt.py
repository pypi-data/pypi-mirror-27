from imgtec.console.support import *
from imgtec.console.results import *
from imgtec.console import *
from imgtec.console.generic_device import update_prompt
from imgtec.lib import rst

__all__ = ['tclist', 'tcactive']

rnst_states = [ "running", "blocked on wait", "blocked on yield", "blocked on gating store" ]
activated_states = ['', 'activated']
halted_states = ['', 'halted']
current_states = ['', 'current']

class TcStatus(object):
    def __init__(self, core, n, tcbind, tchalt, tcstatus, vpeconf0, runstate=None, current=False):
        self.core = core
        self.n = n
        self.tcbind = tcbind
        self.tchalt = tchalt
        self.tcstatus = tcstatus
        self.vpeconf0 = vpeconf0
        self.runstate = runstate
        self.current = current

    columns = ['Core', 'TC#', 'Running State', 'Activated', 'Halted', 'VPE', 'VPE Status', 'Runstate', 'PC', 'Current']

    @property
    def status(self):
        return (self.core, '%d' % self.n,
                rnst_states[self.tcstatus.RNST],
                activated_states[self.tcstatus.A],
                halted_states[self.tchalt.H],
                '%d' % (self.tcbind & 0xF),
                'active' if (self.vpeconf0 & 0x1) else 'inactive',
                str(self.runstate.status),
                '%08x' % (self.runstate.pc,) if not self.runstate.is_running else '',
                current_states[self.current])

    def __repr__(self):
        return rst.table(TcStatus.columns, [self.status])

class TcStatusList(list):
    def __repr__(self):
        return rst.table(TcStatus.columns, [x.status for x in self])

@command()
def tcactive(active=None, device=None):
    '''Set the active TC for the current VPE.'''
    old = device.tiny.GetActiveTC()
    if active is not None:
        def set_tc(newtc):
            device.tiny.SetActiveTC(newtc)
            update_prompt()
        set_tc(active)
        return NoneGuard(set_tc, old)
    return old
    
    
def iterate_tcs(device=None):
    '''Iterate over all TCs in the current Core.
    
    Ensures that the yielded tc is 'active' and that 
    the original tc is restored on exit.
    '''
    info = cpuinfo(device)
    with tcactive(0, device=device):
        for tc in range(0, info.get('num_tc', 1)):
            if tc:
                tcactive(tc, device=device)
            yield tc

def _applyregtypes(names, values, device):
    return [regtype(name, device=device)(value) for name, value in zip(names, values)]

_regnames = 'tcbind tcstatus tchalt vpeconf0'.split()

def _sysprobe_tclist(core):
    ret = []
    _mvpcontrol, tcs = core.tiny.GetTCStatus()
    
    for tcn, tc in enumerate(tcs):
        tcbind, tcstatus, tchalt, vpeconf0 = _applyregtypes(_regnames, tc[:4], device=core.vpes[0])
        is_last_halted = tc[5]

        v = min(tcbind.CurVPE, len(core.vpes)-1)
        vpe = core.vpes[v]
        try:
            oldtcn = vpe.tiny.GetActiveTC()
            vpe.tiny.SetActiveTC(tcn)
            run = runstate(vpe)
        finally:
            vpe.tiny.SetActiveTC(oldtcn)
        ret.append(TcStatus(core.name, tcn, tcbind, tchalt, tcstatus, vpeconf0, run, is_last_halted))
    return ret

def _danet_tclist(core):
    ret = []
    count = cpuinfo(core).get('num_tc', 0)
    currenttcs = []
    for v in core.vpes:
        with tcactive(-1, device=core.vpes[0]):
            try:
                currenttcs.append(v.tiny.GetTCs()[0])
            except Exception:
                currenttcs.append(-1)

    for tc in range(count):
        with tcactive(tc, device=core.vpes[0]):
            tcbind, tcstatus, tchalt, vpeconf0 = regs(_regnames, core.vpes[0])
            v = min(tcbind.CurVPE, len(core.vpes)-1)
            vpe = core.vpes[v]
            with tcactive(tc, device=vpe):
                run = runstate(vpe)
                ret.append(TcStatus(core.name, tc, tcbind, tchalt, tcstatus, vpeconf0, run, currenttcs[v] == tc))
    return ret

@command()
def tclist(device=None):
    '''Print status of all TCs on the current core or given core or SoC.'''
    ret = TcStatusList()
    cores = []
    if hasattr(device, 'cores'):
        cores = device.cores
        device = cores[0].vpes[0]
    elif hasattr(device, 'vpes'):
        cores = [device]
    else:
        cores = [device.core]


    getter = _sysprobe_tclist if int(device.probe.probe_info.get('get_tc_status', '0')) else _danet_tclist
    ret = TcStatusList()
    for core in cores:
        if cpuinfo(core.vpes[0]).get('has_mt'):
            ret.extend(getter(core))
    return ret

if __name__ == '__main__':
    test.main()
    