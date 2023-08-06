'''Examples that can be imported from imgtec.console.examples import 
cpc_control or installed with the installexamples command.'''

# [[[cog
# import cog, sys, os
# from os.path import join, isfile, splitext
# def encode_module(s):
#     s = s.replace('\n', '\000')
#     s = s.encode('string_escape')
#     s = s.replace('\\x00', '\n')
#     s = s.replace('[[[' 'cog', r'\[\[\[cog')
#     s = s.replace('[[' '[end]' ']]', r'\[\[\[end\]\]\]')
#     s = s.replace(']]' ']', r'\]\]\]\]')
#     return s
# 
# path = join('..', '..', "cc-examples")
# examples_names = [f[:-3] for f in os.listdir(path) if f.endswith('.py')]
# for name in examples_names:
#     with open(join(path, name + '.py'), "r") as f:
#         content = encode_module(f.read())
#     cog.outl("{0}_code = '''{1}'''\n".format(name, content))
# ]]]
cpc_control_code = '''"""Control and read the status of the Cluster Power Controller."""

from collections import OrderedDict
from imgtec.console import *
from imgtec.console import CoreFamily
from imgtec.console.support import command, on, off, verbosity
from imgtec.console.results import AllResult
from imgtec.lib.namedenum import namedenum
from textwrap import dedent
import time


modes = [
    \'D0 - Power Down\',
    \'U0 - Vdd OK\',
    \'U1 - Up Delay\',
    \'U2 - UClock Off\',
    \'U3 - Reset\',
    \'U4 - Reset Delay\',
    \'U5 - Non Coherent Execution\',
    \'U6 - Coherent Execution\',
    \'D1 - Isolate\',
    \'D3 - Clr Bus\',
    \'D2 - DClock Off\',
] # yes it does go D1,D3,D2!!

CPC = namedenum(\'CPC\',
    (\'ClockOff\', 1, dedent(\'\'\'\\
    This command causes the domain to cycle into clock-off mode. It
    disables the clock to this power domain. Only successful if
    SI_CoherenceEnable and other protocol interlocks are observed.
    If not, the command remains inactive until the protocol barriers
    subside. After that, the command is executed. Depending on the
    current sequencer state, the command either causes power-up of a
    domain, or a domain leaves active duty to become inactive. A
    power-up leads to sequencer state U2, which will require the
    execution of a subsequent Reset or PwrUp command to make this
    domain operational.\'\'\')),

    (\'PwrDown\', 2, dedent(\'\'\'\\
    Power down this domain using setup values in CPC_STAT_CONF_REG.
    Only successful if SI_CoherenceEnable inactive and all protocol
    interlocks are observed. If not, the command remains inactive
    until the protocol barriers subside. Then, the command is
    executed.\'\'\')),

    (\'PwrUp\', 3, dedent(\'\'\'\\
    Power up this domain using setup values in CPC_STAT_CONF_REG.
    Usable only for Core-Others access. It is the software
    equivalent to SI_PwrUp hardware signal.\'\'\')),

    (\'Reset\', 4, dedent(\'\'\'\\
    This domain is reset if in non-coherent mode. After the domain
    has been reset, the domain becomes operational and the command
    field reads as PwrUp.\'\'\')),
)

KSEG1 = 0xA0000000
GCR_CPC_BASE = 0x88
CPC_CL_CMD_REG = 0x2000
CPC_CL_STAT_CONF = 0x2008
CPC_CL_OTHER_REG = 0x2010
CPC_CO_CMD_REG = 0x4000
CPC_CO_STAT_CONF = 0x4008

def is_danet(device):
    return device.probe.identifier.startswith(\'DA-net\')

class CPCStatus(long):
    \'\'\'The status of the CPC, displays the current mode in text form.

    >>> CPCStatus(0x1 << 19 | 0x3)
    0x00080003 (U0 - Vdd OK)
    \'\'\'
    def __repr__(self):
        return \'0x%08x (%s)\' % (long(self), modes[(long(self) >> 19)& 0xF])

cpc_doc1 = """\\
Read the status of the CPC or send a command to the CPC.

If `core_index` is given, then instead of operating on the \'current\' core
(i.e. the one that is currently active in CodescapeConsole) instead send
the command to core number `core_index` (in this SoC) using the current
core\'s CPC register block. (i.e. using CPC_CO_).

Alternatively if `core_index` is `all` then all cores will be operated on.

`command` should be one of the below constants (as the integer value or
the name as a string), if not given, or None then the current status will
be read.
"""
cpc_doc2 = """\\

Examples:

[s0c0v0] >>> cpc(all) # get the status of all cores
s0c0: 0x00388602 (U6 - Coherent Execution)
s0c1: 0x00388404 (U6 - Coherent Execution)
[s0c0v0] >>> cpc(on, all) # send \'reset\' to all cores
[s0c0v0] >>> cpc(\'PwrDown\', 1) # send \'PwrDown\' to s0c1 FROM s0c0
[s0c0v0] >>> cpc(\'PwrDown\', 0, s0c1) # send \'PwrDown\' to s0c0 FROM s0c1
"""

@command(command=[(reset, str(CPC.Reset)), (on, str(CPC.PwrUp)), (off, str(CPC.PwrDown))],
         core_index=[(all, \'all\')],
         verbose=verbosity)
def cpc(command=None, core_index=None, verbose=True, device=None):
    # \[\[\[cog
    # import cog, sys
    # from cpc_control import *
    # from imgtec.lib import rst
    # cog.outl(\'"""\')
    # cog.outl(cpc_doc1)
    # cog.outl(rst.simple_table([\'#\', \'Name\', \'Meaning\'],
    #       [(\'%d\' % v, str(k), getattr(CPC, k).__doc__) for k, v in CPC._items()]))
    # cog.outl(cpc_doc2)
    # cog.outl(\'"""\')
    # \]\]\]\]*/
    """
    Read the status of the CPC or send a command to the CPC.

    If `core_index` is given, then instead of operating on the \'current\' core
    (i.e. the one that is currently active in CodescapeConsole) instead send
    the command to core number `core_index` (in this SoC) using the current
    core\'s CPC register block. (i.e. using CPC_CO_).

    Alternatively if `core_index` is `all` then all cores will be operated on.

    `command` should be one of the below constants (as the integer value or
    the name as a string), if not given, or None then the current status will
    be read.

    = ======== ================================================================
    # Name     Meaning
    = ======== ================================================================
    1 ClockOff This command causes the domain to cycle into clock-off mode. It 
               disables the clock to this power domain. Only successful if     
               SI_CoherenceEnable and other protocol interlocks are observed.  
               If not, the command remains inactive until the protocol barriers
               subside. After that, the command is executed. Depending on the  
               current sequencer state, the command either causes power-up of a
               domain, or a domain leaves active duty to become inactive. A    
               power-up leads to sequencer state U2, which will require the    
               execution of a subsequent Reset or PwrUp command to make this   
               domain operational.
    2 PwrDown  Power down this domain using setup values in CPC_STAT_CONF_REG. 
               Only successful if SI_CoherenceEnable inactive and all protocol 
               interlocks are observed. If not, the command remains inactive   
               until the protocol barriers subside. Then, the command is       
               executed.
    3 PwrUp    Power up this domain using setup values in CPC_STAT_CONF_REG.   
               Usable only for Core-Others access. It is the software          
               equivalent to SI_PwrUp hardware signal.
    4 Reset    This domain is reset if in non-coherent mode. After the domain  
               has been reset, the domain becomes operational and the command  
               field reads as PwrUp.
    = ======== ================================================================

    Examples:

    [s0c0v0] >>> cpc(all) # get the status of all cores
    s0c0: 0x00388602 (U6 - Coherent Execution)
    s0c1: 0x00388404 (U6 - Coherent Execution)
    [s0c0v0] >>> cpc(on, all) # send \'reset\' to all cores
    [s0c0v0] >>> cpc(\'PwrDown\', 1) # send \'PwrDown\' to s0c1 FROM s0c0
    [s0c0v0] >>> cpc(\'PwrDown\', 0, s0c1) # send \'PwrDown\' to s0c0 FROM s0c1

    """
    # //\[\[\[end\]\]\]    #
    if command is not None:
        command = CPC(command)
    if core_index == \'all\':
        res = AllResult()
        for coreno, core in enumerate(device.core.soc.cores):
            status = cpc_core(coreno, command, verbose, device=device)
            if verbose > 1:
                print \'%s: %r\' % (core.name, status)
            res.add(core.name, status)
        return res

    if core_index is None:
        core_index = device.core.index
    return cpc_core(core_index, command, verbose, device)


def cpc_core(coreno, command, verbose, device):
    if coreno == device.core.index :
        return cpc_this_core(command, verbose, device=device)
    else:
        return cpc_other_core(coreno, command, verbose, device=device)

def _wait_for_reset(device):
    time.sleep(2)
    try:
        runstate(device) #Will fail with unexpected reset (if power up or reset command is sent).
    except:
        pass


def cpc_this_core(command, verbose, device):
    if is_danet(device):
        #find where the GCRS are located.
        gcr_base= (regs(\'cmgcrbase\')<<4) + KSEG1 # requires a classic KSEG1 region and GCRS to be < 512MB.
        cpc_base= word(gcr_base+GCR_CPC_BASE)
        cpc_base_virt = (cpc_base & 0xFFFF0000) + KSEG1 # requires a classic KSEG1 region and GCRS to be < 512MB.

        #enable cpc register access
        word(gcr_base+GCR_CPC_BASE, cpc_base | 0x1)

        cpc_status = CPCStatus(word(cpc_base_virt + CPC_CL_STAT_CONF))
        if command != None:
            if verbose:
                print "Old Status: %r, Issuing Command %d" % (cpc_status, int(command))
            word(cpc_base_virt + 0x2000, command, verify=False)
            _wait_for_reset(device)

            #re-enable cpc register access (in case command was reset)
            word(gcr_base+GCR_CPC_BASE, cpc_base | 0x1)

            cpc_status = CPCStatus(word(cpc_base_virt + CPC_CL_STAT_CONF))

    else:
        #enable cpc reg access
        cpc_base = regs(\'gcr_cpc_base\')
        regs(\'gcr_cpc_base\', cpc_base | 1)

        cpc_status = CPCStatus(regs(\'cpc_cl_stat_conf_reg\'))
        if command != None:
            if verbose:
                print "Old Status: %r, Issuing Command %d" % (cpc_status, int(command))
            regs(\'cpc_cl_cmd_reg\', command)
            _wait_for_reset(device)

            #re-enable cpc register access (in case command was reset)
            regs(\'gcr_cpc_base\', cpc_base | 1)

            cpc_status = CPCStatus(regs(\'cpc_cl_stat_conf_reg\'))

    return cpc_status

class UseOtherCore(object):
    def __enter__(self):
        config("gcr core other", True) #redirect *_cl_* (core local) registers to *_co_* (core other) registers.
    def __exit__(self, type, value, traceback):
        config("gcr core other", False)


def cpc_other_core(coreno, command, verbose, device):
    """Send the CPC a Command for an \'other\' core ie not the one we are halted on currently
    Leave command empty to read status.
    """
    if is_danet(device):
        #find where the GCRS are located.
        gcr_base= (regs(\'cmgcrbase\')<<4) + KSEG1 # requires a classic KSEG1 region and GCRS to be < 512MB.
        cpc_base= word(gcr_base+GCR_CPC_BASE)
        cpc_base_virt = (cpc_base & 0xFFFF0000) + KSEG1 # requires a classic KSEG1 region and GCRS to be < 512MB.

        #enable cpc register access
        word(gcr_base+GCR_CPC_BASE, cpc_base | 0x1)

        word(cpc_base_virt + CPC_CL_OTHER_REG, (coreno & 0xFF) << 16)

        cpc_status = CPCStatus(word(cpc_base_virt + CPC_CO_STAT_CONF))
        if command != None:
            if verbose:
                print "Old Status: %r, Issuing Command %d" % (cpc_status, int(command))
            word(cpc_base_virt + CPC_CO_CMD_REG, command, verify=False)
            _wait_for_reset(device)

            #re-enable cpc register access (in case command was reset)
            word(gcr_base+GCR_CPC_BASE, cpc_base | 0x1)

            cpc_status = CPCStatus(word(cpc_base_virt + CPC_CO_STAT_CONF))

    else: #SysProbe

        #enable cpc reg access
        cpc_base = regs(\'gcr_cpc_base\')
        regs(\'gcr_cpc_base\', cpc_base | 1)
        regs(\'cpc_cl_other_reg\', (coreno & 0xFF) << 16)

        with UseOtherCore():
            cpc_status = CPCStatus(regs(\'cpc_cl_stat_conf_reg\'))
            if command != None:
                if verbose:
                    print "Old Status: %r, Issuing Command %d" % (cpc_status, int(command))

                regs(\'cpc_cl_cmd_reg\', command)
                _wait_for_reset(device)

                #re-enable cpc register access (in case command was reset)
                regs(\'gcr_cpc_base\', cpc_base | 1)

                cpc_status = CPCStatus(regs(\'cpc_cl_stat_conf_reg\'))
    return cpc_status



if __name__ == \'__main__\':
    import doctest
    doctest.testmod()
'''

diagnostic_tools_code = '''from imgtec.console.commands import command


@command()
def timed(fn, *args, **kwargs):
    """
    Runs fn(*args, **kwargs), prints the time taken, then returns the result.
    """
    import time

    start = time.time()
    result = fn(*args, **kwargs)
    print "Time taken: {0}".format((time.time() - start))
    return result


@command()
def profiled(fn, *args, **kwargs):
    """
    Runs fn(*args, **kwargs) using cProfile, prints the statistics, then returns the result.
    """
    import cProfile

    profile = cProfile.Profile()
    result = profile.runcall(fn, *args, **kwargs)
    profile.print_stats()

    return result
'''

ipconfig_code = '''\'\'\'Codescape console commands that allow configuring of DHCP and a static IP
address.\'\'\'
# TODO ::
#  1. we should warn (and prevent without an override) the user when the probe
#     is not currently in the same subnet as broadcast will not work.
#  2. Update probe_finder.find_probe to return the current dhcp state

from imgtec.codescape.probe_identifier import Identifier, Mac
from imgtec.lib import netifaces
from imgtec.console import command, enable, disable, probe
from imgtec.console.support import verbosity, named
from collections import namedtuple
import random
import socket
import time

from imgtec.codescape.probe_finder import Ident, Config, Command, Protocol, BROADCAST, ConfigPacket, RealProbeFinder, find_probe, CallLogger
from imgtec.codescape.probe_finder import _open_sockets, _wait_for_readable_socket, _query_ip

NULL_IP = \'\
\
\
\
\'
MAGIC_DHCP_STRING = \'<DHCP>\'
NUM_RETRIES = 10
DEFAULT_TIMEOUT = 10.0
SETTING_CHANGE_RETRIES = 10

class FoundProbeWithDHCP(namedtuple(\'FoundProbeWithDHCP\', \'identifier ip protocol dhcp\')):
    def __repr__(self):
        return \'{0} @ {1}[{2}], DHCP is {3}\'.format(self.identifier, self.ip,
             self.protocol, [\'disabled\', \'enabled\'][self.dhcp])

class RealProbeFinderWithDHCP(RealProbeFinder):
    \'\'\'Extends the existing probe finder with one that also captures the DHCP
    status.
    \'\'\'
    def find(self, identifier):
        for found in self._query_ip2(self.interface_addresses, identifier, BROADCAST):
            return found
    def identify(self, ip):
        for found in self._query_ip2([\'\'], None, ip):
            return found
    def verify(self, identifier, ip):
        for found in self._query_ip2([\'\'], identifier, ip):
            return found

    def _query_ip2(self, interface_addresses, identifier, address):
        \'\'\'This is very similar to probe_finder._query_ip except that it returns
        FoundProbeWithDHCP instead of FoundProbe.\'\'\'
        mac = identifier.mac if identifier else Mac()
        p = ConfigPacket(Ident.config, Config.query_ip, mac)
        for fromaddr, response in self._send_config_command(interface_addresses, p, address):
            found_mac = Mac(response.mac)
            if found_mac == Mac():
                if self.verbose:
                    print \'  ignoring wildcard mac\'
                continue

            try:
                found = Identifier.from_mac(found_mac)
                dhcp = False
            except ValueError as e:
                if str(found_mac) != MAGIC_DHCP_STRING:
                    if self.verbose:
                        print \'  could not interpret: %r(%s) as a probe mac address\' % (found_mac,str(found_mac))
                    continue # bad mac, or unknown type
                dhcp = True
            protocol = Protocol.tcp if response.type == Config.tcp_enabled else Protocol.udp
            probe_address = \'.\'.join(\'%d\' % ord(x) for x in response.ip)
            if probe_address == \'0.0.0.0\':
                probe_address  = fromaddr
            yield FoundProbeWithDHCP(identifier, fromaddr, protocol, dhcp)

    def _send_config_command(self, interface_addresses, packet, address):
        with _open_sockets(interface_addresses, 0, broadcast=address==BROADCAST) as sockets:
            seen = set()
            for retry in range(NUM_RETRIES):
                for s in sockets:
                    if self.verbose:
                        print \'  sending %r to %s:%s on if %s\' % (packet, address, 59, s.getsockname()[0])
                    s.sendto(packet._pack(), (address, 59))
                for s, response_time in _wait_for_readable_socket(sockets, self.timeout/NUM_RETRIES):
                    if self.verbose:
                        print \'  received socket readable event on %s\' % (s.getsockname()[0],)
                    try:
                        data, (addr, port) = s.recvfrom(1400)
                    except socket.error as e:
                        if self.verbose:
                            print \' \', e
                        continue

                    data = ConfigPacket._unpack_from(data)
                    if self.verbose:
                        print \'  %.6fs received %r from %s:%d\' % (response_time, data, addr, port)
                    yield (addr, data)


    def ipconfig(self, identifier, dhcp_or_address):
        """Configure the IP/DHCP settings of the probe.

        `dhcp_or_address` may be \'dhcp\' or a dotted IPv4 address.
        """
        if dhcp_or_address == \'dhcp\':
            cmd, address = Config.dhcp_on, \'0.0.0.0\'
        else:
            cmd, address = Config.dhcp_off, dhcp_or_address
        p = ConfigPacket(Ident.config, cmd, identifier.mac, socket.inet_aton(address))
        for fromaddr, response in self._send_config_command(self.interface_addresses, p, BROADCAST):
            return

def _make_finder(timeout, verbose):
    # probe_finder.make_finder should take a cls argument
    finder = RealProbeFinderWithDHCP(timeout, max(verbose-1, 0))
    if verbose:
        finder = CallLogger(finder)
    return finder

def _parse_new_setting(address, _random=random.randrange):
    \'\'\'

    >>> _parse_new_setting(\'DHCP\')
    \'dhcp\'
    >>> pseudo = lambda b, e, numbers=[33, 66]:numbers.pop(0)
    >>> _parse_new_setting(\'linklocal\', pseudo)
    \'169.254.33.66\'
    >>> _parse_new_setting(\'192.2.4.5\')
    \'192.2.4.5\'
    >>> _parse_new_setting(\'192.2.4.5.7\')
    Traceback (most recent call last):
    ...
    ValueError: Badly formatted IPv4 address : \'192.2.4.5.7\'
    >>> _parse_new_setting(\'192.2.4.5wtf\')
    Traceback (most recent call last):
    ...
    ValueError: Badly formatted IPv4 address : \'192.2.4.5wtf\'
    \'\'\'
    if address.lower() == \'dhcp\':
        return \'dhcp\'
    elif address.lower() == \'linklocal\':
        (a, b) = _random(1, 254), _random(1, 254)
        return \'169.254.{0}.{1}\'.format(a, b)
    else:
        try:
            socket.inet_aton(address)
            return address
        except socket.error:
            raise ValueError(\'Badly formatted IPv4 address : {0!r}\'.format(address))


dhcp      = named(\'dhcp\')
linklocal = named(\'linklocal\')

def _retry_find_probe(identifier, search_location, finder):
    for n in range(SETTING_CHANGE_RETRIES):
        if n != 0:
            time.sleep(1.0)
        yield find_probe(identifier, search_location, finder)

@command(verbose=verbosity, newsetting=[(dhcp, \'dhcp\'), (linklocal, \'linklocal\')])
def probeipconfig(newsetting=None, identifier=None, search_location=\'\', timeout=DEFAULT_TIMEOUT, verbose=True):
    \'\'\'Determine or configure current IP configuration of a probe.

    When called with no arguments the current settings are returned.

    When called with `dhcp`, DHCP will be enabled and the probe will attempt
    to obtain an IP address.

    When called with `linklocal`, a static IP address will be configured in the
    link-local address range (169.254.0.0/16).  Note that the DA-net does not
    implement the auto-ip specification, but it will successfully defend it\'s
    assigned IP address using ARP so it ought to work in most ad hoc
    environments and is the recommended way of setting up a small network
    (for example a cross over cable).

    When called with a specific IP address, that IP address will be assigned
    to the probe. This will only be allowed if the IP address is in the current
    subnet, (this check can be disabled using ``force=True``).

    If `identifier` is given then the specified probe is used instead of the
    current Codescape Console probe, if there is no current probe, then
    `identifier` must be given. `identifier` should take the form \'danet1234\'
    or \'sp1234\' like the :func:`~imgtec.console.probe` command.

    \'\'\'
    identifier = Identifier(identifier or probe().identifier)
    finder = _make_finder(timeout, max(verbose-1, 0))
    found = find_probe(identifier, search_location, finder)
    if newsetting is  None:
        return found
    dhcp_or_address = _parse_new_setting(newsetting)
    finder.ipconfig(identifier, dhcp_or_address)
    if dhcp_or_address == \'dhcp\':
        # search_location = identifier.dns - Whilst this might possibly be a
        # good idea, on 8.4 it exposes a bug in probe_finder
        for n, found in enumerate(_retry_find_probe(identifier, search_location, finder)):
            if found.dhcp and found.ip != \'0.0.0.0\':
                return found
            if verbose: print \'Waiting for DHCP IP to be acquired (retry {0})\'.format(n+1)
        if found.dhcp and found.ip == \'0.0.0.0\':
            timeout_msg = \'Probe failed to acquire an IP address from the DHCP server\'
        else:
            timeout_msg = \'Probe did not enable DHCP\'
    else:
        # search_location = dhcp_or_address - Whilst this might possibly be a
        # good idea, on 8.4 it exposes a bug in probe_finder
        for n, found in enumerate(_retry_find_probe(identifier, search_location, finder)):
            if not found.dhcp and found.ip == dhcp_or_address:
                return found
            if verbose: print \'Waiting for static IP to be applied (retry {0})\'.format(n+1)
        timeout_msg = \'Probe did not accept static IP\'
    raise RuntimeError(\'{0} after {1} seconds\'.format(timeout_msg, SETTING_CHANGE_RETRIES))

if __name__ == \'__main__\':
    import doctest, sys
    if doctest.testmod()[0]:
        sys.exit(1)
'''

manageprobes_code = '''"""Probe Management Utility.

A script to manage many probes and assist with firmware upgrades.  It maintains
a list of probes in $(PWD)/probes.txt.  This list can be modified using the
add/remove/discover commands.

Once a list of probes has been configured a status report can be generated with 
the status command, and firmware upgrades can be performed on many probes at 
once using the upgrade command.
"""
script_help = __doc__

import argparse
from imgtec.console.generic_device import probe, closeprobe, discoverprobes
from imgtec.console.firmware import firmwarelist, firmwareupgrade
from imgtec.codescape.probe_identifier import Identifier
from imgtec.lib.rst import simple_table
import logging
import re
import sys

PROBES_FILE = "probes.txt"

manageable_probes = (\'DA-net\', \'SysProbe\')

class NoFileException(Exception):
    pass

def status(_):
    probes = _read_probes()
    if not probes:
        raise ValueError("{0} contains no probes. Please use \'discover\' "
                         "first or use \'add\' to add new targets to the pool.".format(PROBES_FILE))
    titles = ["Identifier", "Status", "Firmware version", "Can be upgraded?"]
    result = [_get_status(id) for id in probes]
    print simple_table(titles, result)

def _in_use(e):
    \'\'\'Return owner if `e` is an error/message for in use or else None.
    
    >>> _in_use(\'Some other error\')
    >>> _in_use(\'ssds Connection Refused.  In use by acquirer@le\')
    \'acquirer@le\'
    \'\'\'
    if isinstance(e, Exception):
        e = str(e)
    m = re.search(\'Connection Refused.  In use by ([\\S]+)\', e)
    return m and m.group(1)

def _get_status(id):
    can_be_updated, fwversion = False, \'\'
    try:
        p = probe(id)
        can_be_updated = _can_be_updated(p)
        status, fwversion = \'Online\', p.firmware_version
    except Exception as e:
        status = \'In use\' if _in_use(e) else \'Offline\'
    finally:
        closeprobe()
    return str(id), status, fwversion, (\'Yes\' if can_be_updated else \'No\')

def discover(_):
    probes = _get_probes()
    nr_of_actual = len(probes)
    probes += discoverprobes()
    probes = list(set(probes))
    probes = [p for p in probes if p.type in manageable_probes]

    nr_of_new_probes = len(probes) - nr_of_actual
    if nr_of_new_probes:
        old_probes = _get_probes()
        new_probes = ", ".join(p for p in probes if p not in old_probes)
        print "Discovered {0} new probes: {1}".format(nr_of_new_probes, new_probes)

    _save_probes(probes)

def add(args):
    id = Identifier(args.identifier)
    probes = _get_probes()
    if id in probes:
        raise ValueError("{0} is already in the list of probes.".format(id))
    probes.append(id)
    _save_probes(probes)

def _save_probes(probes):
    with open(PROBES_FILE, "w") as f:
        f.write("\\n".join(p for p in probes if p))

def remove(args):
    id = Identifier(args.identifier)
    probes = _read_probes()
    try:
        probes.remove(id)
        _save_probes(probes)
    except ValueError:
        raise ValueError("{0} is not in the list of probes.".format(id))

def upgrade(args):
    target, version = args.target.lower(), args.version
    probes = _read_probes()
    if target == "all":
        if version:
            raise ValueError("You cannot specify a version if you want to upgrade all probes.\\nThey must be upgraded to the latest version.")
    elif target in ["danet", "da-net"]:
        probes = [p for p in probes if p.type == "DA-net"]
    elif target in (\'sp\', "sysprobe"):
        probes = [p for p in probes if p.type == "SysProbe"]
    else:
        probes = [p for p in probes if p == Identifier(target)]

    for p in probes:
        _upgrade(p, version)


def _upgrade(id, version):
    try:
        p = probe(id)
        if version or _can_be_updated(p):
            if version.count(".") == 3 and version.endswith(".0"):
                version = version[:-2]
            print "Upgrading {0}...".format(id)
            firmwareupgrade(version=version)  # RuntimeError
        elif not version:
            print "{0}\'s firmware is up to date.".format(id)
    except Exception as e:
        if not _in_use(e):
            raise
        print \'{0} cannot be upgraded because it is in use by {1}\'.format(
                id, _in_use(e))
    finally:
        closeprobe()


def __can_be_updated(firmware_version, latest_version):
    \'\'\'
    >>> __can_be_updated(\'1.2.1\', \'1.2.1.0\')
    False
    >>> __can_be_updated(\'1.2.1.0\', \'1.2.1\')
    False
    >>> __can_be_updated(\'1.2.3.4\', \'1.2.4\')
    True
    >>> __can_be_updated(\'1.2.1\', \'1.2.10\')
    True
    >>> __can_be_updated(\'2.1.0\', \'1.2.10\')
    False
    >>> __can_be_updated(\'1.2.10\', \'2.1.0\')
    True
    >>> __can_be_updated(\'1.2.2\', \'1.2.10\')
    True
    \'\'\'
    def get_ver(version):
        version = [int(v) for v in version.split(".")]
        while not version[-1]:
            version = version[:-1]
        return version
    return get_ver(firmware_version) < get_ver(latest_version)


def _can_be_updated(probe):
    return __can_be_updated(probe.firmware_version, firmwarelist()[0].version)


def _get_probes():
    \'\'\'Get configured probes, return empty list if file not present.\'\'\'
    try:
        return _read_probes()
    except NoFileException:
        return []


def _read_probes():
    \'\'\'Read configured probes, fail if file not present.\'\'\'
    try:
        with open(PROBES_FILE) as f:
            return [Identifier(p) for p in f.read().splitlines()]
    except IOError:
        raise NoFileException("{0} not found. Please use \'discover\' first or use \'add\' "
                              "to add new targets to the list of probes.".format(PROBES_FILE))


def parse_arguments(args):
    title, help = script_help.split(\'\\n\', 1)
    argparser = argparse.ArgumentParser(description=title,  epilog=script_help.strip(),
                               formatter_class=argparse.RawDescriptionHelpFormatter)
    argparser.add_argument(\'--debug\', action=\'store_true\', default=False)
    subparsers = argparser.add_subparsers()

    status_pars = subparsers.add_parser("status", help=
      "Display a table of all the configured probes, including fw version, and whether they can be upgraded.")
    status_pars.set_defaults(func=status)

    discover_pars = subparsers.add_parser("discover", help=
      "Get a list of probes in the local subnet and connected via USB and add them to the list of probes")
    discover_pars.set_defaults(func=discover)

    acq_pars = subparsers.add_parser("add", help=
      "Add to the list of probes.")
    acq_pars.set_defaults(func=add)
    acq_pars.add_argument(\'identifier\', type=str, help=
      "Probe identifier ie. sp123")

    acq_pars = subparsers.add_parser("remove", help=
      "Remove from the list of probes.")
    acq_pars.set_defaults(func=remove)
    acq_pars.add_argument(\'identifier\', type=str, help=
      "Probe identifier ie. sp123")

    acq_pars = subparsers.add_parser("upgrade", help=
      \'Upgrade all probes that match `target`\')
    acq_pars.set_defaults(func=upgrade)
    acq_pars.add_argument(\'target\', type=str, help=
      "One of all/danet/sysprobe/danet 123/sysprobe 123")
    acq_pars.add_argument(\'version\', type=str, help="Custom version, otherwise will upgrade to the newest one.")

    args = argparser.parse_args(args)

    return args


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "upgrade":
        sys.argv.append("")
    args = parse_arguments(sys.argv[1:])
    if not args.debug:
        l = logging.getLogger(\'comms\')
        l.disabled = True
    try:
        args.func(args)
    except Exception as e:
        if args.debug:
            raise
        print str(e)

if __name__ == \'__main__\':
    import doctest
    if len(sys.argv) == 1:
        if doctest.testmod()[0]:
            sys.exit(1)
    main()'''

mz_flash_code = '''from imgtec.console import *
from imgtec.lib.namedbitfield import namedbitfield
from contextlib import contextmanager
from imgtec.test import *
from textwrap import dedent
import time
class FlashMemoryError(Exception):
    pass
class FlashSettings(object):
    def __init__(self):
        self.prog_address        = 0x9d000000
        self.prog_size           = 0x200000
        self.boot_address        = 0xbfc00000
        self.boot_size           = 0x74000
        self.device_timeout      = 5
        self.block_write_timeout = 5
        self.erase_timeout       = 15
        self.block_size          = 0x00004000 # protect block size...
        self.multi_cnt           = 512
    
    def __repr__(self): 
        return dedent(\'\'\'\\
            Program Base Address : 0x%08x
                    Program Size : 0x%08x
               Boot Base Address : 0x%08x
                       Boot Size : 0x%08x
                      Block Size : 0x%08x
                      Multi Cnt  : 0x%08x
                  Device Timeout : %ds
             Block Write Timeout : %ds
                   Erase Timeout : %ds\'\'\' %
                  (self.prog_address, self.prog_size, self.boot_address, self.boot_size,
                    self.block_size, self.multi_cnt,
                    self.device_timeout, self.block_write_timeout, self.erase_timeout))
        
flash_settings = FlashSettings()
print "The current Flash Memory settings are:"
print repr(flash_settings)
print "If these are not correct please change them using the \'flashsettings\' command."
# FLASH Registers
NVMCON          = 0xBF800600
NVMCONCLR       = 0xBF800604
NVMCONSET       = 0xBF800608
NVMCONINV       = 0xBF80060C
NVMKEY          = 0xBF800610
NVMADDR         = 0xBF800620
NVMADDRCLR      = 0xBF800624
NVMADDRSET      = 0xBF800628
NVMADDRINV      = 0xBF80062C
NVMDATA0        = 0xBF800630
NVMDATA1        = 0xBF800640
NVMDATA2        = 0xBF800650
NVMDATA3        = 0xBF800660
NVMSRCADDR      = 0xBF800670
NVMPWP          = 0xBF800680
NVMBWP          = 0xBF800690
COPYADDR        = 0xA0000000
DEVCFG0         = 0xBFC0FFCC
CFGCON          = 0xBF800000
CFGSPACESTART   = 0xBFC0FF40
CFGSPACEEND     = 0xBFC10000
# flash Operations
RESET           = 0x4000
PROGRAM         = 0x4001
QPROGRAM        = 0x4002
MPROGRAM        = 0x4003
SECTORERASE     = 0x4004
CHIPERASE       = 0x4007
NVMCON_WR       = 0x8000
NVMCON_WREN     = 0x4000

#The usual register
Status = namedbitfield(\'NVMCON\', 
    [(\'wr\', 15), (\'wren\', 14), (\'wrerr\', 13), (\'lvderr\', 12), (\'swap\', 7), 
        (\'nvmop\', 3,0)])

cfg_space_contents = []

@command()
def flashsettings(prog_address=None, prog_size=None, boot_address=None, boot_size=None,
    device_timeout=None, block_write_timeout=None, erase_timeout=None, block_size=None,
    multi_cnt=None):
    \'\'\'
    Change the or view the current flash memory settings.
    
    =================== ================================================================================
    Parameter           Meaning
    =================== ================================================================================
    prog_address        Start address of the program flash memory.
    prog_size           Size of program flash memory.
    boot_address        Start address of the boot flash memory.
    boot_size           Size of the program flash memory.
    device_timeout      Amount of time to wait for the flash devices to be ready for general operations.
    block_write_timeout Amount of time to wait for a block write to complete.
    erase_timeout       Amount of time to wait for a full device erase to complete.
    block_size          Flash memory block size in 
    multi_cnt           Size of row programming blocks
    =================== ================================================================================
    \'\'\'
    
    if prog_address is not None:
        flash_settings.prog_address = prog_address
    if prog_size is not None:
        flash_settings.prog_size = prog_size
    if boot_address is not None:
        flash_settings.boot_address = boot_address
    if boot_size is not None:
        flash_settings.boot_size = boot_size
    if device_timeout is not None:
        flash_settings.device_timeout = device_timeout
    if block_write_timeout is not None:
        flash_settings.block_write_timeout = block_write_timeout
    if erase_timeout is not None:
        flash_settings.erase_timeout = erase_timeout
    if block_size is not None:
        flash_settings.block_size = block_size
    if multi_cnt is not None:
        flash_settings.multi_cnt = multi_cnt
    return flash_settings

def flashcheckstatus(device):
    status = Status(word(NVMCON, device))        
    if status.lvderr:
        raise FlashMemoryError(\'Operation failed with a low voltage error.\')
    if status.wrerr:
        raise FlashMemoryError(\'Write or Erase Operation failed.\')

def flashwaitfordevice(device, timeout=None):
    if timeout is None:
        timeout = flash_settings.device_timeout
        
    start = time.time()
    while True:
        status = Status(word(NVMCON, device))
        if not status.wr:
            break
            
        if (time.time() - start) > timeout:
            raise FlashMemoryError(\'Timed out waiting for a flash device to be ready.\')

    flashcheckstatus(device)

def flashwriteaddress(address, device):
    # Address written must be a physical address.
    word(NVMADDR, (address & 0x1fffffff), verify=False, device=device)

def flashunlock(device):
    word(NVMKEY, 0, verify=False, device=device)
    word(NVMKEY, 0xAA996655, verify=False, device=device)
    word(NVMKEY, 0x556699AA, verify=False, device=device)
    
def flashoperation(op, device=device()):
    try:
        word(NVMCON, op, verify=False, device=device)
        flashunlock(device)
        word(NVMCONSET, NVMCON_WR, verify=False, device=device)
        flashwaitfordevice(device)
    finally:
        word(NVMCONCLR, NVMCON_WREN, verify=False, device=device)

@command()
def flasheraseprogramflash(device=None,verify=False):
    \'\'\'
    Erase the entire program flash.
    \'\'\'
    flashcheckstatus(device)
    flashwriteaddress(0x1D000000, device)
    flashoperation(CHIPERASE,device)
    
    if verify == True:
        for x in range(0, flash_settings.prog_size, flash_settings.block_size/4):
            if word(0xbd000000+x,device) != 0xFFFFFFFF:
                raise FlashMemoryError(\'Program flash not erased. Check protection and try again.\')
                
    print "Devices erased successfully."

@command()
def flasheraseblock(address, device=None, verify=False):
    \'\'\'
    Erase this block/sector of boot or program flash that contains the address.
    \'\'\'
    flashcheckstatus(device)
    if address != None and not( (flash_settings.prog_address <= address < (flash_settings.prog_address + flash_settings.prog_size)) or (flash_settings.boot_address <= address < (flash_settings.boot_address + flash_settings.boot_size))):
        raise FlashMemoryError(\'address must be in boot flash or program flash address range.\')
    flashwriteaddress(address, device)
    flashoperation(SECTORERASE,device)
    
    if verify == True:
        for x in range(0, flash_settings.block_size, 64) :
            if word(address+x,device) != 0xFFFFFFFF:
                raise FlashMemoryError("Block not erased. Address 0x%x failed to erase. Check protection and try again." % (address+x))
                
    print "Erased block at 0x%x" % (address)
def split_values_for_block_write(address, values):
    \'\'\'
    Given a list of values to be written starting at address, split those values
    into multi_cnt blocks, quad blocks or a single word block.
    Returns a list of tuples of (address, [values]).
    
    Note: doesn\'t handle addresses that aren\'t 32 bit aligned, may cause issues.

    Return {size, address, [values]}
    \'\'\'
    write_chunks = []
    temp_addr    = address
    temp_count = len(values)
    temp_chunk   = []
    chunk_addr   = address
    first_block = True
    for value in values:
        if first_block or block_size == len(temp_chunk):
            if not first_block:
                write_chunks.append((block_size, chunk_addr, temp_chunk))
                chunk_addr = temp_addr
                temp_chunk = []
                
            first_block = False
            block_size = 1
            if ( temp_count >= flash_settings.multi_cnt and (temp_addr % (flash_settings.multi_cnt * 4) == 0) ) :
                block_size = flash_settings.multi_cnt
            elif ( temp_count >= 4 and (temp_addr % 16 == 0) ) :
                block_size = 4
                
        temp_chunk.append(value)
        temp_addr += 4
        temp_count -= 1

    if( len(temp_chunk) == 0):
        raise FlashMemoryError(\'Length is zero!\')

    write_chunks.append((block_size, chunk_addr, temp_chunk))

    return write_chunks
    
def flash_write_block(address, size, values, device, verbose=False):
    if( size == flash_settings.multi_cnt ):
        flash_write_multi(address, values, device, verbose)
    elif ( size == 4 ) :
        flash_write_quad(address, values, device, verbose)
    else :
        flash_write_word(address, values, device, verbose)

def flash_write_multi(address, values, device, verbose=False):
    if verbose:
        print "Writing 0x%x bytes at address 0x%x with multi" % (flash_settings.multi_cnt*4,address)
    
    save_contents = word(COPYADDR,None,count=flash_settings.multi_cnt,device=device)
    flashcheckstatus(device)

    try:
        word(COPYADDR, values, verify=True,device=device)
        flashwriteaddress(address, device)
        word(NVMSRCADDR, 0, verify=False, device=device)
        flashoperation(MPROGRAM,device)
    finally:
        word(COPYADDR, save_contents, verify=False, device=device)
    

def flash_write_quad(address, values, device, verbose=False):
    if verbose:
        print "Writing 0x%x bytes at address 0x%x with quad" % (16,address)
        
    flashcheckstatus(device)
    flashwriteaddress(address, device)
    word(NVMDATA0, values[0], verify=False, device=device)
    word(NVMDATA1, values[1], verify=False, device=device)
    word(NVMDATA2, values[2], verify=False, device=device)
    word(NVMDATA3, values[3], verify=False, device=device)
    flashoperation(QPROGRAM,device)

def flash_write_word(address, values, device, verbose=False):
    global cfg_space_contents
    global cfg_space_in_use
    flashcheckstatus(device)
    
    if (CFGSPACESTART <= address < CFGSPACEEND):
        # save all writes to config space until we process the whole load file
        # then write them as quads.  This way we only write the data once.
        cfg_idx = (((address - CFGSPACESTART) & 0xff)/4)
        cfg_space_contents[cfg_idx] = values[0]
        cfg_space_in_use = True
    else:
        # Is the ECC bit on?
        if ((word(CFGCON, device) & 0x30) == 0):
            # yes, so we can\'t do single word writes must use quads
            quad_idx = ((address & 0xf)/4)
            qualAddress = (address & 0xfffffff0)
            quad_contents = []
            for x in range(0,    4):
                quad_contents.append(word(qualAddress+(x*4),device))
                
            quad_contents[quad_idx] = values[0]
            flash_write_quad(qualAddress, quad_contents, device, verbose=verbose)
        else:
            # normal single word flash write
            if verbose:
                print "Writing 0x%x bytes at address 0x%x with word" % (4,address)
                
            flashwriteaddress(address, device)
            word(NVMDATA0, values[0], verify=False, device=device)
            flashoperation(PROGRAM,device)

@command()
def flashwriteblock(address, values, device=None, verbose=False):
    \'\'\'
    Write a list of 32 bit values starting at address
    Script will select largest writeable size; word, quad, or row until list is empty.
    \'\'\'
    write_blocks = split_values_for_block_write(address, values)
    [flash_write_block(addr, size, vals, device, verbose) for size, addr, vals in write_blocks]

@command()
def flashloadfile(path, verify=True, verbose=True, base_address=None, device=None):
    \'\'\'
    Write a file to flash memory.
    Flash must be erased prior to executing this command.
    For a binary file supply a base address, for other types confirm that the file\'s
    addresses are in the flash range before loading.
    \'\'\'
    global cfg_space_contents
    global cfg_space_in_use

    if base_address != None and not( (flash_settings.prog_address <= base_address < (flash_settings.prog_address + flash_settings.prog_size)) or (flash_settings.boot_address <= base_address < (flash_settings.boot_address + flash_settings.boot_size))):
        raise FlashMemoryError(\'base_address must be in prog or boot flash address range.\')
    for x in range(CFGSPACESTART, CFGSPACEEND, 4):
        cfg_space_contents.append(0xFFFFFFFF)
    cfg_space_in_use = False
    #Replace current device.da with our proxy object
    flash_device = FlashMemoryDA(device, verbose=verbose)
    #Load command can function normally via the proxy
    if verify == True:
        load(path, setpc=False, verify=False, verbose=verbose, base_addr=base_address, device=flash_device, load_symbols=False)
    else:
        load(path, setpc=False, verify=verify, verbose=verbose, base_addr=base_address, device=flash_device)
      
    if cfg_space_in_use == True:
        if verbose:
            print "Writing CONFIG SPACE Memory" 
        
        for x in range(CFGSPACESTART, CFGSPACEEND, 16):
            indexAddrStart = (x - CFGSPACESTART) / 4
            indexAddrEnd = ((x+16) - CFGSPACESTART) / 4
            flash_write_quad(x, cfg_space_contents[indexAddrStart:indexAddrEnd], device=device, verbose=verbose)
            
    if verify == True:
        load(path, setpc=False, verify=True, verbose=False, base_addr=base_address, device=device, load_symbols=True)
    
@command()
def flashclearstatus(device=None):
    \'\'\'
    Reset the status register. Do this after an error to reset the device.
    \'\'\'
    flashoperation(RESET,device)

def flashdodataflashprotection(address,device,protecting):
    protectInfo = [ (0x1FC00000, 0x8000, 0x0100),
                    (0x1FC04000, 0x8000, 0x0200),
                    (0x1FC08000, 0x8000, 0x0400),
                    (0x1FC0C000, 0x8000, 0x0800),
                    (0x1FC10000, 0x8000, 0x1000),
                    (0x1FC20000, 0x0080, 0x0001),
                    (0x1FC24000, 0x0080, 0x0002),
                    (0x1FC28000, 0x0080, 0x0004),
                    (0x1FC2C000, 0x0080, 0x0008),
                    (0x1FC30000, 0x0080, 0x0010)]
    retProtect = word(NVMBWP,device)
    
    for addr, check, protect in protectInfo:
        if addr <= (address & 0x1fffffff) <= (addr + 0x4000 - 1):
            if (retProtect & check) == 0:
                raise FlashMemoryError(\'Protect Operation failed: Data flash protection for this block can not be modified.\')
            if( protecting ):
                retProtect = retProtect | protect
            else:
                # is there an easier way to do a one\'s complement?
                retProtect = retProtect & (protect ^ 0xffffffff)
            flashunlock(device)
            word(NVMBWP,retProtect,verify=False,device=device)
            
    if retProtect != word(NVMBWP,device):
        raise FlashMemoryError(\'Protect Operation failed: Data flash protection for this block failed. expect: 0x%08x; actual: 0x%08x \' %(retProtect,word(NVMBWP,device)) )

@command()
def flashsetprotection(address, device=None):
    \'\'\'
    Turn on protection for a flash region.
    Set protection on the boot flash block that starts at the given address.
    Set protection on the program flash from the start of program
    flash through the full page of the given address.
    !!!There is an errata for revs A3 and A4 that makes protecting only a portion of program flash impossible. Errata 40.
    \'\'\'
    if (address & 0x1F000000) == (flash_settings.prog_address & 0x1f000000):
        # program flash
        if (address & 0x7fffffff) > 0x1d1fffff:
            raise FlashMemoryError(\'Protect Operation failed: Address out of range.\')
        protect = word(NVMPWP,device)
        
        if (protect & 0x80000000) == 0:
            raise FlashMemoryError(\'Protect Operation failed: Program flash protection can not be modified.\')
            
        protect = (address & 0x00ffc000) | 0x80000000
        flashunlock(device)
        word(NVMPWP,protect,verify=False,device=device)
        
        if protect != word(NVMPWP,device):
            raise FlashMemoryError(\'Protect Operation failed: Program flash protection for this address failed.\')
    else:
        if (address-flash_settings.boot_address) % flash_settings.block_size:
            raise FlashMemoryError(\'Address must be the beginning of a protection block.\')
        flashdodataflashprotection(address,device,True)
@command()
def flashclearprotection(address, device=None):
    \'\'\'
    Turn off protection for a flash region.
    Clear protection on the boot flash block that starts at the given address.
    Clear protection on the program flash entire range from the address to the end of 
    flash. The region from the start of program flash to the address - 1 is protected.
    To clear protection on the entire program flash use the starting address of the flash.
    !!!There is an errata for revs A3 and A4 that make protecting only a portion of program flash impossible. Errata 40.
    \'\'\'
    if (address & 0x5F000000) == 0x1d000000:
        if (address & 0x7fffffff) > 0x1d1fffff:
            raise FlashMemoryError(\'Clear Protection Operation Failed: Address out of range.\')
            
        protect = word(NVMPWP,device)
        if (protect & 0x80000000) == 0:
            raise FlashMemoryError(\'Clear Protection Operation Failed: Program flash protection can not be modified.\')
        protect = (address & 0x00ffc000) | 0x80000000
        flashunlock(device)
        word(NVMPWP,protect,verify=False,device=device)
        if protect != word(NVMPWP,device):
            raise FlashMemoryError(\'Clear Protection Operation failed: Program flash protection for this address failed.\')
    else:
        if (address-flash_settings.boot_address) % flash_settings.block_size:
            raise FlashMemoryError(\'Address must be the beginning of a protection block.\')
        flashdodataflashprotection(address,device,False)

class FlashDevice(object):
    def __init__(self, man_code, dev_code, prim_vend_code, size, max_multi_words, 
        num_erase_blocks):
        self.man_code         = man_code
        self.dev_code         = dev_code
        self.prim_vend_code   = prim_vend_code
        self.size             = size
        self.max_multi_words  = max_multi_words
        self.num_erase_blocks = num_erase_blocks
        
    def __repr__(self):
        return dedent(\'\'\'\\
              Manufacturer ID : 0x%x
                    Device ID : 0x%x
          Primary Vendor Code : 0x%x
                         Size : %dM bytes
        Max Multi Byte Write  : %d bytes
        Number of erase blocks: %d\'\'\') % (
            self.man_code, self.dev_code, self.prim_vend_code, 
            self.size//(1024**2), self.max_multi_words, 
            self.num_erase_blocks)

class FlashDeviceList(list):
    def __repr__(self):
        return \'\\n\'.join([repr(item) for item in self])

class FlashMemoryDA(object):
    def __init__(self, device, verbose=False):
        #The \'real\' device, which has the real DA
        self.device = device
        #Redirect device.da calls to this object (only catching what load uses)
        self.da = self
        self.verbose = verbose
          
    def CpuInfo(self):
        return self.device.da.CpuInfo()
         
    def GetEndian(self):
        return self.device.da.GetEndian()
         
    def WriteMemoryBlock(self, address, count, elem_size, data):
        #Note that the command will exit reflash mode, so subsequent reads
        #(for verify) will read normally.
        flashwriteblock(address, data[:count], device=self.device, verbose=self.verbose)
         
    def ReadMemoryBlock(self, address, count, elem_size):
        #This can always be done normally
        return self.device.da.ReadMemoryBlock(address, count, elem_size)
         
    def __getattr__(self, name):
        try:
            return getattr(self.device, name)
        except AttributeError:
            return getattr(self.device.da, name)
            '''

pic32_flash_support_code = '''from imgtec.console import *

LOWER_BOOT = 0xBFC00000
UPPER_BOOT = 0xBFC20000
BOOT_FLASH_1 = 0xBFC40000
BOOT_FLASH_2 = 0xBFC60000
PROGRAM_FLASH = 0xBD000000
PROGRAM_FLASH_CACHED = 0x9D000000

#Helper for known pic32 devices
@command()
def pic32mz2048_register_flash_regions(device=None):
    \'\'\' Sets up the flash region of a pic32 device\'\'\'
    flashconfig("lower boot alias",LOWER_BOOT,0x14000,\'type:pic32mz\',device)
    flashconfig("upper boot alias",UPPER_BOOT,0x14000,\'type:pic32mz\',device)
    flashconfig("boot flash 1",BOOT_FLASH_1,0x14000,\'type:pic32mz\',device)
    flashconfig("boot flash 2",BOOT_FLASH_2,0x14000,\'type:pic32mz\',device)
    flashconfig("program flash",PROGRAM_FLASH,0x200000,\'type:pic32mz\',device)
    flashconfig("program flash cached",PROGRAM_FLASH_CACHED,0x200000,\'type:pic32mz\',device)
    print flashconfig()

@command()
def pic32mz1024_register_flash_regions(device=None):
    \'\'\' Sets up the flash region of a pic32 device\'\'\'
    flashconfig("lower boot alias",LOWER_BOOT,0x14000,\'type:pic32mz\',device)
    flashconfig("upper boot alias",UPPER_BOOT,0x14000,\'type:pic32mz\',device)
    flashconfig("boot flash 1",BOOT_FLASH_1,0x14000,\'type:pic32mz\',device)
    flashconfig("boot flash 2",BOOT_FLASH_2,0x14000,\'type:pic32mz\',device)
    flashconfig("program flash",PROGRAM_FLASH,0x100000,\'type:pic32mz\',device)
    flashconfig("program flash cached",PROGRAM_FLASH_CACHED,0x100000,\'type:pic32mz\',device)
    print flashconfig()

@command()
def pic32mz512_register_flash_regions(device=None):
    \'\'\' Sets up the flash region of a pic32 device\'\'\'
    flashconfig("lower boot alias",LOWER_BOOT,0x14000,\'type:pic32mz\',device)
    flashconfig("upper boot alias",UPPER_BOOT,0x14000,\'type:pic32mz\',device)
    flashconfig("boot flash 1",BOOT_FLASH_1,0x14000,\'type:pic32mz\',device)
    flashconfig("boot flash 2",BOOT_FLASH_2,0x14000,\'type:pic32mz\',device)
    flashconfig("program flash",PROGRAM_FLASH,0x80000,\'type:pic32mz\',device)
    flashconfig("program flash cached",PROGRAM_FLASH_CACHED,0x80000,\'type:pic32mz\',device)
    print flashconfig()

#MX Parts:
@command()
def pic32mx1xx_064_register_flash_regions(device=None):
    \'\'\' Sets up the flash region of a pic32 device\'\'\'
    flashconfig("boot flash",LOWER_BOOT,0xC00,\'type:pic32mx,pagesize:1024\',device)
    flashconfig("program flash",PROGRAM_FLASH,0x10000,\'type:pic32mx,pagesize:1024\',device)
    flashconfig("program flash cached",PROGRAM_FLASH_CACHED,0x10000,\'type:pic32mx,pagesize:1024\',device)
    print flashconfig()
    
@command()
def pic32mx2xx_064_register_flash_regions(device=None):
    \'\'\' Sets up the flash region of a pic32 device\'\'\'
    flashconfig("boot flash",LOWER_BOOT,0xC00,\'type:pic32mx,pagesize:1024\',device)
    flashconfig("program flash",PROGRAM_FLASH,0x10000,\'type:pic32mx,pagesize:1024\',device)
    flashconfig("program flash cached",PROGRAM_FLASH_CACHED,0x10000,\'type:pic32mx,pagesize:1024\',device)
    print flashconfig()
    
@command()
def pic32mx5x0_064_register_flash_regions(device=None):
    \'\'\' Sets up the flash region of a pic32 device\'\'\'
    flashconfig("boot flash",LOWER_BOOT,0xC00,\'type:pic32mx,pagesize:1024\',device)
    flashconfig("program flash",PROGRAM_FLASH,0x10000,\'type:pic32mx,pagesize:1024\',device)
    flashconfig("program flash cached",PROGRAM_FLASH_CACHED,0x10000,\'type:pic32mx,pagesize:1024\',device)
    print flashconfig()
    
@command()
def pic32mx1xx_128_register_flash_regions(device=None):
    \'\'\' Sets up the flash region of a pic32 device\'\'\'
    flashconfig("boot flash",LOWER_BOOT,0xC00,\'type:pic32mx,pagesize:1024\',device)
    flashconfig("program flash",PROGRAM_FLASH,0x20000,\'type:pic32mx,pagesize:1024\',device)
    flashconfig("program flash cached",PROGRAM_FLASH_CACHED,0x20000,\'type:pic32mx,pagesize:1024\',device)
    print flashconfig()
    
@command()
def pic32mx2xx_128_register_flash_regions(device=None):
    \'\'\' Sets up the flash region of a pic32 device\'\'\'
    flashconfig("boot flash",LOWER_BOOT,0xC00,\'type:pic32mx,pagesize:1024\',device)
    flashconfig("program flash",PROGRAM_FLASH,0x20000,\'type:pic32mx,pagesize:1024\',device)
    flashconfig("program flash cached",PROGRAM_FLASH_CACHED,0x20000,\'type:pic32mx,pagesize:1024\',device)
    print flashconf()
    
@command()
def pic32mx5x0_128_register_flash_regions(device=None):
    \'\'\' Sets up the flash region of a pic32 device\'\'\'
    flashconfig("boot flash",LOWER_BOOT,0xC00,\'type:pic32mx,pagesize:1024\',device)
    flashconfig("program flash",PROGRAM_FLASH,0x20000,\'type:pic32mx,pagesize:1024\',device)
    flashconfig("program flash cached",PROGRAM_FLASH_CACHED,0x20000,\'type:pic32mx,pagesize:1024\',device)
    print flashconf()
    
@command()
def pic32mx1xx_256_register_flash_regions(device=None):
    \'\'\' Sets up the flash region of a pic32 device\'\'\'
    flashconfig("boot flash",LOWER_BOOT,0xC00,\'type:pic32mx,pagesize:1024\',device)
    flashconfig("program flash",PROGRAM_FLASH,0x40000,\'type:pic32mx,pagesize:1024\',device)
    flashconfig("program flash cached",PROGRAM_FLASH_CACHED,0x40000,\'type:pic32mx,pagesize:1024\',device)
    print flashconf()
    
@command()
def pic32mx2xx_256_register_flash_regions(device=None):
    \'\'\' Sets up the flash region of a pic32 device\'\'\'
    flashconfig("boot flash",LOWER_BOOT,0xC00,\'type:pic32mx,pagesize:1024\',device)
    flashconfig("program flash",PROGRAM_FLASH,0x40000,\'type:pic32mx,pagesize:1024\',device)
    flashconfig("program flash cached",PROGRAM_FLASH_CACHED,0x40000,\'type:pic32mx,pagesize:1024\',device)
    print flashconf()
    
@command()
def pic32mx5x0_256_register_flash_regions(device=None):
    \'\'\' Sets up the flash region of a pic32 device\'\'\'
    flashconfig("boot flash",LOWER_BOOT,0xC00,\'type:pic32mx,pagesize:1024\',device)
    flashconfig("program flash",PROGRAM_FLASH,0x40000,\'type:pic32mx,pagesize:1024\',device)
    flashconfig("program flash cached",PROGRAM_FLASH_CACHED,0x40000,\'type:pic32mx,pagesize:1024\',device)
    print flashconf()
    
@command()
def pic32mx1xx_512_register_flash_regions(device=None):
    \'\'\' Sets up the flash region of a pic32 device\'\'\'
    flashconfig("boot flash",LOWER_BOOT,0xC00,\'type:pic32mx,pagesize:1024\',device)
    flashconfig("program flash",PROGRAM_FLASH,0x80000,\'type:pic32mx,pagesize:1024\',device)
    flashconfig("program flash cached",PROGRAM_FLASH_CACHED,0x80000,\'type:pic32mx,pagesize:1024\',device)
    print flashconf()
    
@command()
def pic32mx2xx_512_register_flash_regions(device=None):
    \'\'\' Sets up the flash region of a pic32 device\'\'\'
    flashconfig("boot flash",LOWER_BOOT,0xC00,\'type:pic32mx,pagesize:1024\',device)
    flashconfig("program flash",PROGRAM_FLASH,0x80000,\'type:pic32mx,pagesize:1024\',device)
    flashconfig("program flash cached",PROGRAM_FLASH_CACHED,0x80000,\'type:pic32mx,pagesize:1024\',device)
    print flashconf()
    
@command()
def pic32mx5x0_512_register_flash_regions(device=None):
    \'\'\' Sets up the flash region of a pic32 device\'\'\'
    flashconfig("boot flash",LOWER_BOOT,0xC00,\'type:pic32mx,pagesize:1024\',device)
    flashconfig("program flash",PROGRAM_FLASH,0x80000,\'type:pic32mx,pagesize:1024\',device)
    flashconfig("program flash cached",PROGRAM_FLASH_CACHED,0x80000,\'type:pic32mx,pagesize:1024\',device)
    print flashconf()
    
def pic32_64_12(device=None):
    flashconfig("boot flash",LOWER_BOOT,0x3000,\'type:pic32mx\',device)
    flashconfig("program flash",PROGRAM_FLASH,0x10000,\'type:pic32mx\',device)
    flashconfig("program flash cached",PROGRAM_FLASH_CACHED,0x10000,\'type:pic32mx\',device)
    print flashconfig()
    
def pic32_128_12(device=None):
    flashconfig("boot flash",LOWER_BOOT,0x3000,\'type:pic32mx\',device)
    flashconfig("program flash",PROGRAM_FLASH,0x20000,\'type:pic32mx\',device)
    flashconfig("program flash cached",PROGRAM_FLASH_CACHED,0x20000,\'type:pic32mx\',device)
    print flashconfig()
    
def pic32_256_12(device=None):
    flashconfig("boot flash",LOWER_BOOT,0x3000,\'type:pic32mx\',device)
    flashconfig("program flash",PROGRAM_FLASH,0x40000,\'type:pic32mx\',device)
    flashconfig("program flash cached",PROGRAM_FLASH_CACHED,0x40000,\'type:pic32mx\',device)
    print flashconfig()
    
def pic32_512_12(device=None):
    flashconfig("boot flash",LOWER_BOOT,0x3000,\'type:pic32mx\',device)
    flashconfig("program flash",PROGRAM_FLASH,0x80000,\'type:pic32mx\',device)
    flashconfig("program flash cached",PROGRAM_FLASH_CACHED,0x80000,\'type:pic32mx\',device)
    print flashconfig()
    
@command()
def pic32mx3xx_064_register_flash_regions(device=None):
    \'\'\' Sets up the flash region of a pic32 device\'\'\'
    pic32_64_12(device)
    
@command()
def pic32mx4xx_064_register_flash_regions(device=None):
    \'\'\' Sets up the flash region of a pic32 device\'\'\'
    pic32_64_12(device)
    
@command()
def pic32mx5xx_064_register_flash_regions(device=None):
    \'\'\' Sets up the flash region of a pic32 device\'\'\'
    pic32_64_12(device)
    
@command()
def pic32mx6xx_064_register_flash_regions(device=None):
    \'\'\' Sets up the flash region of a pic32 device\'\'\'
    pic32_64_12(device)
    
@command()
def pic32mx7xx_064_register_flash_regions(device=None):
    \'\'\' Sets up the flash region of a pic32 device\'\'\'
    pic32_64_12(device)


@command()
def pic32mx3xx_128_register_flash_regions(device=None):
    \'\'\' Sets up the flash region of a pic32 device\'\'\'
    pic32_128_12(device)
    
@command()
def pic32mx4xx_128_register_flash_regions(device=None):
    \'\'\' Sets up the flash region of a pic32 device\'\'\'
    pic32_128_12(device)
    
@command()
def pic32mx5xx_128_register_flash_regions(device=None):
    \'\'\' Sets up the flash region of a pic32 device\'\'\'
    pic32_128_12(device)
    
@command()
def pic32mx6xx_128_register_flash_regions(device=None):
    \'\'\' Sets up the flash region of a pic32 device\'\'\'
    pic32_128_12(device)
    
@command()
def pic32mx7xx_128_register_flash_regions(device=None):
    \'\'\' Sets up the flash region of a pic32 device\'\'\'
    pic32_128_12(device)


@command()
def pic32mx3xx_256_register_flash_regions(device=None):
    \'\'\' Sets up the flash region of a pic32 device\'\'\'
    pic32_256_12(device)
    
@command()
def pic32mx4xx_256_register_flash_regions(device=None):
    \'\'\' Sets up the flash region of a pic32 device\'\'\'
    pic32_256_12(device)
    
@command()
def pic32mx5xx_256_register_flash_regions(device=None):
    \'\'\' Sets up the flash region of a pic32 device\'\'\'
    pic32_256_12(device)
    
@command()
def pic32mx6xx_256_register_flash_regions(device=None):
    \'\'\' Sets up the flash region of a pic32 device\'\'\'
    pic32_256_12(device)
    
@command()
def pic32mx7xx_256_register_flash_regions(device=None):
    \'\'\' Sets up the flash region of a pic32 device\'\'\'
    pic32_256_12(device)


@command()
def pic32mx3xx_512_register_flash_regions(device=None):
    \'\'\' Sets up the flash region of a pic32 device\'\'\'
    pic32_512_12(device)
    
@command()
def pic32mx4xx_512_register_flash_regions(device=None):
    \'\'\' Sets up the flash region of a pic32 device\'\'\'
    pic32_512_12(device)
    
@command()
def pic32mx5xx_512_register_flash_regions(device=None):
    \'\'\' Sets up the flash region of a pic32 device\'\'\'
    pic32_512_12(device)
    
@command()
def pic32mx6xx_512_register_flash_regions(device=None):
    \'\'\' Sets up the flash region of a pic32 device\'\'\'
    pic32_512_12(device)
    
@command()
def pic32mx7xx_512_register_flash_regions(device=None):
    \'\'\' Sets up the flash region of a pic32 device\'\'\'
    pic32_512_12(device)
'''

scanmeta_code = '''###############################################################################
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
"""Meta Debug access using Jtag scan operations.
"""

import collections
import textwrap
from imgtec.console.results import IntResult, IntListResult
from imgtec.console.support import command, verifies
from imgtec.console.scan import devtapi, devtapd, tap
from imgtec.codescape.da_types import Status
from imgtec.codescape.tiny import State

TapSettings = collections.namedtuple(\'CoreSettings\', \'j_img_attn j_img_status j_img_control\')
"""Settings for the Tap/SoC required to initialise a :class:`ImgCore` instance."""

CoreSettings = collections.namedtuple(\'CoreSettings\', \'j_img j_img_f j_img_m\')
"""Core jtag settings required per core with :class:`ImgCore` instance."""

MDBGDATAX = 0x00
MDBGDATAT = 0x01
MDBGCTRL0 = 0x02
MDBGCTRL1 = 0x03
MDBGREAD  = 0x30
MDBGWRITE = 0x20

ADDRESS_WRITE      = 0x0
ADDRESS_READ       = 0x1
ADDRESS_INC        = 0x2
ADDRESS_WRITE_INC  = ADDRESS_WRITE | ADDRESS_INC
ADDRESS_READ_INC   = ADDRESS_READ | ADDRESS_INC

class Error(StandardError):
    """All exceptions derive from this class."""

def _load_address(address, read_write_increment):
    """Calculate load address for MDBGCTRL0 using an ADDRESS_? constant."""
    return (address & 0xFFFFFFFC) | read_write_increment

class ImgTap(object):
    """Low-level access to the Meta Debug port as JTAG scans.  There should
    only be one of these created per DA.  Multiple cores should share a ImgTap
    instance.
    """

    def __init__(self, underlying_device, tap_index, tap_settings):
        self.underlying_device = underlying_device
        self.tap_index = tap_index
        self.last_ir_register = 0
        self.tap_settings = tap_settings

    def _IRScan(self, type, settings, value=0):
        if type == 0:      #load J_IMG
            if settings.j_img == 0:
                raise Error("ImgTap._IRScan - J_IMG instruction value is set to 0")
            data_in = settings.j_img

        elif type == 1:     #Load J_IMG_F
            raise Error("ImgTap._IRScan - We Cannot Support FAST Mode Accesses as non JTAG Compliant")

        elif type == 2:     #Load J_IMG_M
            if settings.j_img_m == 0:
                raise Error("ImgTap._IRScan - J_IMG_M instruction value is set to 0")
            data_in = settings.j_img_m

        elif type == 4:     #Load BYPASS
            data_in = 0xFF

        elif type == 5:     # Load IDCODE
            data_in = 0x01

        elif type == 6:     #Generic Scan - value passed in
            if value == 0:
                raise Error("ImgTap._IRScan - trying to load IR register with 0, this is a bad thing as it puts SoC into Boundary Scan Mode!!!")
            data_in = value

        elif type == 7:    # Load J_IMG_C
            if self.tap_settings.j_img_control == 0:
                raise Error("ImgTap._IRScan - J_Ctrl instruction value is set to 0")
            data_in = self.tap_settings.j_img_control

        else:
            raise Error("ImgTap._IRScan - unknown IR Scan type (%d) requested" % (type,))
        tap(self.tap_index, device=self.underlying_device)
        data_out = devtapi(None, data_in, device=self.underlying_device)
        self.last_ir_register = data_in
        return data_out

    def _DRData(self, data):
        """Perform a 32-bit DRScan.  `data` is interpreted as a 32-bit word.
        The return from the scan is also interpreted as a 32-bit word."""
        tap(self.tap_index, device=self.underlying_device)
        return devtapd(32, data, device=self.underlying_device)

    def _DRControl(self, value, length=6):
        """Perform a 6-bit DRScan.  `value` is interpreted as a byte.
        Returns the 6-bit result."""
        tap(self.tap_index, device=self.underlying_device)
        return devtapd(length, value, device=self.underlying_device)

    def CheckIR(self, settings, force=False):
        if self.last_ir_register != settings.j_img or force:
            self._IRScan(0, settings)

    def _IsDebugPortReady(self):
        return self._DRControl(0) & 0x7 == 0x7

    def _CheckStatus(self):
        """Wait for the debug port to be ready."""
        timeout = 0
        while not self._IsDebugPortReady():
            if timeout == 20:
                raise Error("Timeout waiting on Debug Port Ready")
            timeout += 1

    def ReadDebugRegister(self, address):
        """Read from a debug register, `address` should be one of the MDBG
        constants.  Assumes that CheckIR has been called already.
        """
        self._CheckStatus()
        self._DRControl(MDBGREAD | (address & 0xF))
        self._CheckStatus()
        return self._DRData(0)

    def WriteDebugRegister(self, address, data):
        """Write to a debug register, `address` should be one of the MDBG
        constants. Assumes that CheckIR has been called already.
        """
        self._CheckStatus()
        self._DRControl(MDBGWRITE | (address & 0xF))
        self._DRData(data)
        
    def Reset(self):
        if self.tap_settings.j_img_control ==0:
            raise Error( "No J_Ctrl instruction : cannot reset target via JTAG")
        else:
            self._IR_Scan(7, None)
            self._DRControl(0x02, 4)
            self._DRControl(0x00, 4)

TXUXXRXDT     = [0x0480FFF0, 0x048000F8]
TXUXXRXRQ      = [0x0480FFF8, 0x048000FC]
TXUXXRXRQ_DREADY_BIT = 0x80000000
TXUXXRXRQ_RDnWR_BIT  = 0x00010000
MMCU_DCACHE_CTRL = 0x04830018
MMCU_ICACHE_CTRL = 0x04830020

NumOfTXRegRWPollsBeforeQuit = 10
HWSTATMETA = 0x04820000
CT_BASE, CT_REG_STRIDE, CT_THR_STRIDE = 0x04800000, 0x00000008, 0x00001000

_register_values  = dict(
 D0_0=0x001,  D0_1=0x011,  D0_2=0x021,  D0_3=0x031,  D0_4=0x041,  D0_5=0x051,  D0_6=0x061,  D0_7=0x071,
 D0_8=0x081,  D0_9=0x091, D0_10=0x0a1, D0_11=0x0b1, D0_12=0x0c1, D0_13=0x0d1, D0_14=0x0e1, D0_15=0x0f1,
D0_16=0x101, D0_17=0x111, D0_18=0x121, D0_19=0x131, D0_20=0x141, D0_21=0x151, D0_22=0x161, D0_23=0x171,
D0_24=0x181, D0_25=0x191, D0_26=0x1a1, D0_27=0x1b1, D0_28=0x1c1, D0_29=0x1d1, D0_30=0x1e1, D0_31=0x1f1,
 D1_0=0x002,  D1_1=0x012,  D1_2=0x022,  D1_3=0x032,  D1_4=0x042,  D1_5=0x052,  D1_6=0x062,  D1_7=0x072,
 D1_8=0x082,  D1_9=0x092, D1_10=0x0a2, D1_11=0x0b2, D1_12=0x0c2, D1_13=0x0d2, D1_14=0x0e2, D1_15=0x0f2,
D1_16=0x102, D1_17=0x112, D1_18=0x122, D1_19=0x132, D1_20=0x142, D1_21=0x152, D1_22=0x162, D1_23=0x172,
D1_24=0x182, D1_25=0x192, D1_26=0x1a2, D1_27=0x1b2, D1_28=0x1c2, D1_29=0x1d2, D1_30=0x1e2, D1_31=0x1f2,
 A0_0=0x003,  A0_1=0x013,  A0_2=0x023,  A0_3=0x033,  A0_4=0x043,  A0_5=0x053,  A0_6=0x063,  A0_7=0x073,
 A0_8=0x083,  A0_9=0x093, A0_10=0x0a3, A0_11=0x0b3, A0_12=0x0c3, A0_13=0x0d3, A0_14=0x0e3, A0_15=0x0f3,
 A1_0=0x004,  A1_1=0x014,  A1_2=0x024,  A1_3=0x034,  A1_4=0x044,  A1_5=0x054,  A1_6=0x064,  A1_7=0x074,
 A1_8=0x084,  A1_9=0x094, A1_10=0x0a4, A1_11=0x0b4, A1_12=0x0c4, A1_13=0x0d4, A1_14=0x0e4, A1_15=0x0f4,
   PC=0x005,   PCX=0x015,
 TR_0=0x007,  TR_1=0x017,  TR_2=0x027,  TR_3=0x037,  TR_4=0x047,  TR_5=0x057,  TR_6=0x067,  TR_7=0x077,
 FX_0=0x009,  FX_1=0x019,  FX_2=0x029,  FX_3=0x039,  FX_4=0x049,  FX_5=0x059,  FX_6=0x069,  FX_7=0x079,
 FX_8=0x089,  FX_9=0x099, FX_10=0x0a9, FX_11=0x0b9, FX_12=0x0c9, FX_13=0x0d9, FX_14=0x0e9, FX_15=0x0f9,
)
_register_values = dict([(k.replace(\'_\', \'.\'), v) for k, v in _register_values.items()])

_ct_registers = dict(
 TXENABLE=0,  TXSTATUS=2,  TXRPT=3,      TXTIMER=4, TXBPOBITS=11, TXTIMERI=13,
 TXCATCH0=16, TXCATCH1=17, TXCATCH2=18,  TXCATCH3=19,
 TXDEFR=20,  TXDIVTIME=28, TXPRIVEXT=29, TXTACTCYC=30, TXIDLECYC=31,
)

_register_aliases =  dict(D0Re0="D0.0",D0Ar6="D0.1",D0Ar4="D0.2",D0Ar2="D0.3",D0FrT="D0.4",
                          D1Re0="D1.0",D1Ar5="D1.1",D1Ar3="D1.2",D1Ar1="D1.3",D1RtP="D1.4",
                          A0StP="A0.0", A0FrP="A0.1",
                          A1GbP="A1.0",A1LbP="A1.1")
"""Aliases for some registers."""

def _encode_txuxx(reg, thread):
    """Return the TXUXXRXRQ value required to read or write the given register."""
    reg = _register_aliases.get(reg, reg)
    try:
        reg = _register_values[reg.upper()]
    except KeyError:
        allregs = _ct_registers.keys() + _register_values.keys() + _register_aliases.keys()
        valid = \', \'.join(sorted(allregs))
        valid = \'\\n  \'.join(textwrap.wrap(valid, 78))
        raise ValueError("Unknown register %r. Supported registers are:\\n  %s" % (reg,valid))
    return reg | thread << 12

def _poll_for_txuxx_ready(core, is_mtx):
    for i in range(NumOfTXRegRWPollsBeforeQuit):
        if core.Read32(TXUXXRXRQ[is_mtx]) & TXUXXRXRQ_DREADY_BIT:
            return
    raise Error("Timeout on TXRegRW(%08x) poll for ready - %08x : Tried %d times " % (TXUXXRXRQ[is_mtx], TXUXXRXRQ_DREADY_BIT, NumOfTXRegRWPollsBeforeQuit))

def _ct_address(reg, thread):
    """Get the address of a CT register by name

    >>> \'0x%08x\' % _ct_address(0, 0)
    \'0x04800000\'
    >>> \'0x%08x\' % _ct_address(2, 3)
    \'0x04803010\'
    """
    try:
        n = _ct_registers[reg.upper()]
        return CT_BASE + CT_REG_STRIDE * n + CT_THR_STRIDE * thread
    except KeyError:
        return None

def _read_txuxx_register(core, thread, reg, is_mtx):
    reg = _encode_txuxx(reg, thread)
    reg |= TXUXXRXRQ_RDnWR_BIT
    _poll_for_txuxx_ready(core, is_mtx)
    core.Write32(TXUXXRXRQ[is_mtx], reg)
    _poll_for_txuxx_ready(core, is_mtx)
    val =  core.Read32(TXUXXRXDT[is_mtx])
    return val

def _write_txuxx_register(core, thread, reg, value, is_mtx):
    reg = _encode_txuxx(reg, thread)
    _poll_for_txuxx_ready(core, is_mtx)
    core.Write32(TXUXXRXDT[is_mtx], value)
    core.Write32(TXUXXRXRQ[is_mtx], reg)
    _poll_for_txuxx_ready(core, is_mtx)

def _hwstatmeta_is_halted(stat, thread):
    return (stat >> (thread * 4)) & 0x7 != 0

def _runstatus(core):
    """Determine current run status of the current thread."""
    TXENABLE_TSTOPPED               = 4
    TXSTATUS_FREASON                = 0x00300000
    TXSTATUS_FREASON_NOERROR\t\t= 0x00000000
    TXSTATUS_FREASON_GENERAL\t\t= 0x00100000
    TXSTATUS_FREASON_PAGE\t\t\t= 0x00200000
    TXSTATUS_FREASON_PROTECTION\t\t= 0x00300000

    TXSTATUS_HREASON                = 0x000c0000
    TXSTATUS_HREASON_SWITCH\t\t\t= 0x00000000
    TXSTATUS_HREASON_UNKNOWN_INST\t= 0x00040000
    TXSTATUS_HREASON_PRIVILEGE\t\t= 0x00080000
    TXSTATUS_HREASON_MEM_FAULT\t\t= 0x000C0000
    
    # not using HWSTATMETA at the moment, but we should probably expose it
    def _is_thread_halted(core, thread):
        """Return True if the current thread is stopped"""
        return (core.ReadRegister(\'TXENABLE\') & 1) == 0
        return _hwstatmeta_is_halted(core.Read32(HWSTATMETA), thread)

    ct0 = core.ReadRegister(\'TXENABLE\')
    if ct0 & 1:
        return Status.running
         
    if ct0 & TXENABLE_TSTOPPED:
        return Status.stopped

    ct2 = core.ReadRegister(\'TXSTATUS\')
    hreason = ct2 & TXSTATUS_HREASON
    freason = ct2 & TXSTATUS_FREASON
    if hreason == TXSTATUS_HREASON_MEM_FAULT:
        return Status.memory_fault

    # Don\'t do this check as we don\'t know whether or not we single stepped so it would be a lie.
    #~ # nope, some exception state, or maybe a single step
    #~ pc = core.ReadRegister(\'PC\')
    #~ pc_at_switch = is_instruction_switch_opcode(thread, pc)
    #~ if did_single_step_[thread] && !pc_at_switch && (freason != CT2_FREASON_PROTECTION):
        #~ return Status.single_stepped

    if hreason == TXSTATUS_HREASON_SWITCH:
        return Status.sw_break

    if hreason == TXSTATUS_HREASON_UNKNOWN_INST and \\
        freason == TXSTATUS_FREASON_PROTECTION:
        return Status.hw_break

    return Status.exception

class ImgCore(object):
    """Low-level access to a Meta Core Debug port as JTAG scans."""
    def __init__(self, img_tap, core_settings):
        self.img_tap = img_tap
        self.core_settings = core_settings
        self.img_tap.CheckIR(core_settings, force=True)
        self._thread = 0
        
    def Read32(self, address):
        """Read a 32-bit value from `address`."""
        self.img_tap.CheckIR(self.core_settings)
        self.img_tap.WriteDebugRegister(MDBGCTRL0, _load_address(address, ADDRESS_READ))
        return self.img_tap.ReadDebugRegister(MDBGDATAX)

    def BlockRead32(self, address, count):
        """Read `count` 32-bit values starting from `address`."""
        self.img_tap.CheckIR(self.core_settings)
        self.img_tap.WriteDebugRegister(MDBGCTRL0, _load_address(address, ADDRESS_READ_INC))
        data = []
        for i in range(count - 1):
            data.append(self.img_tap.ReadDebugRegister(MDBGDATAT))
        # now do final word
        data.append(self.img_tap.ReadDebugRegister(MDBGDATAX))
        return data

    def Write32(self, address, data):
        """Write the 32-bit value `data` to `address`."""
        self.img_tap.CheckIR(self.core_settings)
        self.img_tap.WriteDebugRegister(MDBGCTRL0, _load_address(address, ADDRESS_WRITE))
        self.img_tap.WriteDebugRegister(MDBGDATAT, data)

    def BlockWrite32(self, address, data):
        """Write len(data) 32-bit values to `address`."""
        self.img_tap.CheckIR(self.core_settings)
        self.img_tap.WriteDebugRegister(MDBGCTRL0, _load_address(address, ADDRESS_WRITE_INC))
        for x in data:
            self.img_tap.WriteDebugRegister(MDBGDATAT, x)
            
    def ReadRegister(self, reg):
        ct_addr =  _ct_address(reg, self._thread)
        if ct_addr is not None:
            return self.Read32(ct_addr)
        is_mtx = False #self._cores[self._core]._cpu_info.get(\'is_mtx\', False)
        return _read_txuxx_register(self, self._thread, reg, is_mtx)

    def WriteRegister(self, reg, value):
        ct_addr = _ct_address(reg, self._thread)
        if ct_addr is not None:
            return self.Write32(ct_addr, value)
        is_mtx = False #self._cores[self._core]._cpu_info.get(\'is_mtx\', False)
        return _write_txuxx_register(self, self._thread, reg, value, is_mtx)

    def GetThread(self):
        return self._thread

    def SetThread(self, thread):
        """Set the current thread."""
        if self._thread != thread:
            self._thread = thread
            self.img_tap.CheckIR(self.core_settings)
            temp = self.img_tap.ReadDebugRegister(MDBGCTRL1)
            #nb bits 8, 12 and 13 are write 1 to clear - these need preserving so clears these bits in the write back value.
            temp = (temp & 0xFFFFCECF ) | ((thread & 0x3) << 4)
            self.img_tap.WriteDebugRegister(MDBGCTRL1, temp)
    
    def Reset(self):
        return self.img_tap.Reset()
        
def _get_j_img(device, j_img):
    if j_img is None:
        if not hasattr(device, \'j_img\'):
            raise RuntimeError(\'First usage of tapmeta commands must specify a j_img value.\\n\'
                               \'This can usually be determined from IMG PnP data with the tapinfo command.\')
        j_img = device.j_img
    else:
        device.j_img = j_img
    return j_img
    
def _get_core(device, j_img=None):
    tap_index = 0 if device.probe.tap_index == -1 else device.probe.tap_index
    tap_settings = TapSettings(0, 0, 0)
    core = CoreSettings(j_img=_get_j_img(device, j_img), j_img_f=0, j_img_m=0)
    img_tap = ImgTap(device, device.probe.tap_index, tap_settings)
    return ImgCore(img_tap, core)
    
@command(verify=verifies)
def tapmetaword(address, value=None, j_img=None, verify=True, count=None, device=None):
    """Read/write a word on a Meta device using low level JTAG operations.
    
    If `count` is given or `value` is a list, then the autoincrement feature is 
    used to read/write one or more addresses at once.
    
    If `verify` is True then on a write the result is read back.
    
    """
    core = _get_core(device, j_img)
    #core.SetThread(thread)
    if value is not None:
        if isinstance(value, (list, tuple)):
            if count is not None:
                value = value[:count]
            count = len(value)
            core.BlockWrite32(address, value)            
        else:
            core.Write32(address, value)
    if value is None or verify:
        if count is not None:
            return IntListResult(core.BlockRead32(address, count), size=4)
        else:
            return IntResult(core.Read32(address), size=4)
            
@command(verify=verifies)
def tapmetareg(name, value=None, j_img=None, thread=0, verify=True, device=None):
    """Read/write a register on a Meta device using low level JTAG operations.
    """
    core = _get_core(device, j_img)
    core.SetThread(thread)
    if value is not None:
        core.WriteRegister(name, value)
    if value is None or verify:
        return IntResult(core.ReadRegister(name), size=4)
    
@command(verify=verifies)
def tapmetarunstate(j_img=None, thread=0, verify=True, device=None):
    """Return the run status of a Meta device using low level JTAG operations.
    """
    core = _get_core(device, j_img)
    core.SetThread(thread)
    status  = _runstatus(core)
    pc = 0
    if status != Status.running:
        pc = core.ReadRegister(\'PC\')
    return State(status, pc, 0)

'''

spramsetup_code = '''from imgtec.console import *
import time

ISPRAM_BASE_PHYSICAL_ADDRESS=0x04000000
\'\'\'The base physical address where the ISPRAM should be configured.

This address should match precisely the address used by the boot ROM.
\'\'\'

DSPRAM_BASE_PHYSICAL_ADDRESS=0x05000000
\'\'\'The base physical address where the DSPRAM should be configured.

This address should match precisely the address used by the boot ROM.
\'\'\'

HALT_TARGET_IF_RUNNING = False
\'\'\'If the target is running when this script runs and this option is True
then halt the target to perform SPRAM initialisation.  The target will be 
resumed after SPRAM initialisation is complete.\'\'\'

POST_RESET_DELAY = 5
\'\'\'If HALT_TARGET_IF_RUNNING is True then this configures how long (in 
seconds) the boot ROM should be left running before SPRAM initialisation 
is done.\'\'\'

def initialise_sprams():
    \'\'\'Initialise the SPRAMS if not already enabled and request the probe
    to detect the current SPRAM settings.
    
    Note:  If this script is run in the middle of boot ROM SPRAM setup 
           then this existing state of the SPRAMs may have been affected.
           
           In this case it is probably sufficient to re-run this script
           after the boot ROM\'s SPRAM initialisation is complete.
           
           Alternatively you could use Codescape Console 
    \'\'\'
    # do not do anything if the target is still running post reset
    print \'initialise_sprams\'.center(80, \'-\')
    if not runstate().is_running:
        config("Use ISPRAM",0)
        if not ispram().enabled or not dspram().enabled:
            print \'Enabling ISPRAMs\'        
            print ispram(enable=True,base_addr_phys=ISPRAM_BASE_PHYSICAL_ADDRESS)
            print \'Enabling DSPRAMs\'        
            print dspram(enable=True,base_addr_phys=DSPRAM_BASE_PHYSICAL_ADDRESS)
            print \'Enabling probe support for SPRAMs\'
        # This forces the probe to redetect SPRAM setup
        config("Use ISPRAM",1)
    elif not HALT_TARGET_IF_RUNNING:
        print \'SPRAMs were not initialised because the target was running.\'
        print \'You should rerun this script when the target halts.\'
    else:
        print \'Target is running post-reset, waiting 5 seconds for the boot rom\'
        print \'to ensure that SPRAM setup is complete...\'
        time.sleep(POST_RESET_DELAY)
        halt()
        try:
            initialise_sprams()
        finally:
            go()


def reset_script():
    initialise_sprams()

def connect_script():
    initialise_sprams()

if __name__ == \'__main__\':
    with probe(args=parse_startup_args()) as p:
        if p.environment == \'codescape\':
            reset_script()
        else:
            connect_script()
'''

virtualtap_adapter_code = '''import argparse
from contextlib import closing
import socket
import struct
import traceback
from imgtec.lib.namedenum import namedenum
from imgtec.codescape.probe_identifier import Identifier
from imgtec.codescape.tiny import ConnectProbe
from imgtec.console import command


MessageId = namedenum(\'MessageId\',
    ir              = 0,
    dr              = 1,
    set_signal      = 2,
    get_signal      = 3,
    ir_and_dr       = 4,
    apb_read        = 6,
    apb_write       = 7,
)

Signal = namedenum(\'Signal\',
    ntrst    = 0x00,
    nhardreset = 0x01,
    dint   = 0x03,
)

SignalValue = namedenum(\'SignalValue\',
    off  = 0,
    low  = 2,
    high = 3,
)

Status = namedenum(\'Status\',
    ok = 0,
    unknown_command = 1,
    bad_size = 2,
    unsupported_command=3,
)

from imgtec.lib.bits import bits_to_words, words_to_bits

def bytes_to_bits(bytes, num_bits):
    r\'\'\'

    >>> bytes_to_bits([0x45, 0x23, 0x01], 20)
    \'00010010001101000101\'

    \'\'\'
    bytes = reversed(bytes)
    widths = [8] * (num_bits/8)
    if num_bits%8:
        widths += [num_bits%8]
    widths = reversed(widths)
    return words_to_bits(bytes, widths)

def _bits_to_bytes(res):
    r\'\'\'

    >>> [\'%02x\' % x for x in _bits_to_bytes(\'0001\'\'00100011\'\'01000101\')]
    [\'45\', \'23\', \'01\']

    \'\'\'
    num_bits = len(res)
    widths = [8] * (num_bits/8)
    if num_bits%8:
        widths += [num_bits%8]
    widths = list(reversed(widths))
    bytes = []
    count = 0
    for w in widths:
        bytes.append(int(res[count:count+w], 2))
        count += w
    bytes.reverse()
    return bytes

def bits_to_bytes(res):
    return \'\'.join([chr(x) for x in _bits_to_bytes(res)])

handlers = {}

def recvall(s, sz):
    input = \'\'
    while len(input) < sz:
        x = s.recv(sz - len(input))
        if not x:
            raise RuntimeError("Connection closed")
        input += x
    if 0: print \'..................... recvall(%d) -> %s\' % (sz, \' \'.join(\'%02x\' % ord(x) for x in input))
    return input

def handler(header):
    cls = struct.Struct(\'!\' + header)
    def _handler(f):
        def __handler(probe, s):
            input = recvall(s, cls.size)
            args = cls.unpack(input)
            res, data = f(probe, s, *args)
            return Status.ok, res, data
        handlers[MessageId(f.__name__)] = __handler
        return __handler
    return _handler

def read_bits(s, num_bits):
    num_bytes = (num_bits + 7) / 8
    data = recvall(s, num_bytes)
    return bytes_to_bits(bytearray(data), num_bits)

@handler(\'I\')
def ir(probe, s, num_bits):
    bits = read_bits(s, num_bits)
    if 0: print \'  IR TDI:\', bits
    res = probe.Scan(bits, \'\')
    if 0: print \'  IR TDO:\', res
    return [num_bits], bits_to_bytes(res)

@handler(\'I\')
def dr(probe, s, num_bits):
    bits = read_bits(s, num_bits)
    if 0: print \'  DR TDI:\', bits
    res = probe.Scan(\'\', bits)
    if 0: print \'  DR TDO:\', res
    return [num_bits], bits_to_bytes(res)

@handler(\'II\')
def ir_and_dr(probe, s, num_bits_ir, num_bits_dr):
    ir = read_bits(s, num_bits_ir)
    if 0: print \'  IR TDI:\', ir
    dr = read_bits(s, num_bits_dr)
    if 0: print \'  DR TDI:\', dr
    res = probe.Scan(ir, dr)
    if 0: print \'     TDO:\', res
    return [num_bits_ir, num_bits_dr], bits_to_bytes(ir) + bits_to_bytes(res)

signals = {
    Signal.ntrst: \'assert ntrst\',
    Signal.nhardreset: \'assert nhardreset\',
    Signal.dint: \'assert dint\',
}

@handler(\'II\')
def set_signal(probe, s, signal, value):
    try:
        probe.WriteDASetting(signals[Signal(signal)], 1 if value == SignalValue.high else 0)
        if 0: print \'set\', signals[Signal(signal)], 1 if value == SignalValue.high else 0
    except Exception as e:
        print e
    return [], \'\'

@handler(\'I\')
def get_signal(probe, s, signal):
    try:
        val, type = probe.ReadDASetting(\'assert \' + str(signal))
        val = SignalValue.high if val else SignalValue.low
        if 0: print \'get\', signals[Signal(signal)], 1 if val == SignalValue.high else 0
    except Exception as e:
        val = 0
    return [int(val)], \'\'

def connection(s, probe):
    if probe.GetDAMode() not in (\'scanonly\', \'uncommitted\'):
        probe.DAReset()
    while 1:
        input = recvall(s, 4)
        res, status, data = [], Status.ok, \'\'
        msg, = struct.unpack(\'!L\', input)
        try:
            handler = handlers[MessageId(msg)]
        except KeyError:
            status = Status.unsupported_command
        except ValueError:
            status = Status.unknown_command
        else:
            status, res, data = handler(probe, s)
        if 0: print \'.....................             -> %r %r %s\' % (status, res, \' \'.join(\'%02x\' % ord(x) for x in data))
        s.send(struct.pack(\'!I\' + \'I\' * len(res), status, *res) + data)




@command()
def virtualtaplisten(port=44445, device=None):
    \'\'\'Listen for VirtualTap connections and forward to the current SysProbe.\'\'\'
    listening = socket.socket()
    listening.bind((\'\', port))
    print \'Listening on\',  port
    listening.listen(1)
    p = device.probe
    from imgtec.console import scanonly
    scanonly()
    while 1:
        print \'connected to\', p.identifier
        accepted, address = listening.accept()
        try:
            with closing(accepted):
                print \'Accepted\', address
                connection(accepted, p.tiny)
        except Exception as e:
            traceback.print_exc()


def main(args):
    from imgtec.console import probe
    with probe(args.identifier) as p:
        virtualtap_adapter(args.port)

if __name__ == \'__main__\':
    import sys
    import doctest
    if doctest.testmod()[0]:
        sys.exit()
    parser = argparse.ArgumentParser(description=\'Listen for VirtualTap connections and forward IR/DR/Signal commands to a SysProbe/DAnet\')
    parser.add_argument(\'identifier\', type=Identifier, help=\'Identifier of sysprobe/danet to forward to\')
    parser.add_argument(\'--port\', type=int, default=44445, help=\'port num to listen to, defaults to 44445\')
    sys.argv = [\'\', \'sp157\']  # you can hardcode a sp num here if you want to avoid command line args
    #if sys.argv[1:] == []:
    #    from imgtec.console.socket_sim_driver import SocketDriver
    #    driver = SocketDriver(44445)
    #    print driver.Scan(\'11111\', \'0000111111111\')
    #
    #
    #else:
    main(parser.parse_args())
'''

wifire_code = '''\'\'\'Enable the eJTAG on a Digilent WiFire device.\'\'\'
from imgtec.console import *

@command(desiredmode=[(autodetect, \'autodetect\'), (scanonly, \'scanonly\')])
def enablejtag(desiredmode=\'autodetect\', device=None):
    \'\'\'Enable the eJTAG on a Digilent WiFire device.
    
    The Digilent WiFire device by default has a non-MIPS TAP controller 
    selected.  A special sequence needs to be scanned into TDI whilst nReset is 
    held low to select the MIPS TAP controller.
    
    Note that this will cause a system reset, and should be run whenever power
    has been removed from the device.
    \'\'\'
    reset(probe)
    config(\'Assert nHardReset\', 0)
    tapi(\'8 0x2f\')
    config(\'Assert nHardReset\', 1)
    if desiredmode == \'autodetect\':
        autodetect()
    elif desiredmode == \'scanonly\':
        scanonly()
'''

wpj344_code = '''\'\'\'wpj344 boot commands.

This is a collection of commands that can help initialise a Compex WPJ344 board
after reset.  

It can be used directly or it can be used as a reference example to create a 
boot script for other MIPS cores.

To use, 

1. Copy this file to ~/imgtec/console_scripts.  
2. Start Codescape Console and connect to your board

 [s0c0v0] >>> import wpj344
 [s0c0v0] >>> bootwpj344()
 Initializing TLBs
 Initializing Caches
 Initializing L1I: 2048 sets, 32 lines
 Initializing L1D: 1024 sets, 32 lines 
    
You can then load an elf, srec or binary using the built-in load command:

 [s0c0v0] >>> load(\'demo_threadx_be_74k.elf\')
 [s0c0v0] >>> go()
 Running from 0x8010be40 (__start)
 status=running
 [s0c0v0] >>> halt()
 status=stopped pc=0x801094d4 (_tx_queue_send)
 0x801094d4 0062102b    sltu      v0, v1, v0
 
Alternatively you can use the initregs, inittlbs, initmemory, initcaches 
commands directly.

\'\'\'
from imgtec.codescape import da_types
from imgtec.console import command
from imgtec.console import *
from imgtec.console.cache import INDEX_STORE_TAG
import time, sys, os

@command()
def bootwpj344(device=None):
    \'\'\'Reset the board and perform post reset initialisation.\'\'\'
    reset(ejtagboot)
    initregs()
    initmemory()
    inittlbs()
    initcaches()
    
@command()
def initregs():
    \'\'\'Initialise registers\'\'\'
    regmodify(\'Config\', K0=3)
    regs(\'cause\',    0)
    regs(\'status\',   0)
    regs(\'watchhi0\', 7)
    regs(\'watchlo0\', 0)
    regs(\'watchhi1\', 7)
    regs(\'watchlo1\', 0)
    regs(\'watchhi2\', 7)
    regs(\'watchlo2\', 0)
    regs(\'watchhi3\', 7)
    regs(\'watchlo3\', 0)
    regs(\'compare\',  0)
    regs(\'a0\',       0)
    regs(\'a1\',       0)
    regs(\'a2\',       0)
    regs(\'a3\',       0)    

@command()
def initmemory(device=None):
    \'\'\'Setup memory controller\'\'\'
    word(0xB806001C, 0xE6CEFFFF)
    word(0xB8050008, 0x0130801C)
    word(0xB8050000, 0x40021380)
    word(0xB8050004, 0x40815800)
    word(0xB8050044, 0x78180200)
    word(0xB8050048, 0x00C00000)
    word(0xB8050000, 0x00021380)
    word(0xB8050004, 0x00815800)
    word(0xB8050008, 0x01308000)
    word(0xB8050024, 0x00000570)
    word(0xB8000000, 0xC7D48CD0)
    word(0xB8000004, 0x9DD0E6A8)
    word(0xB80000b8, 0x00000E59)
    word(0xB8000010, 0x00000008)
    word(0xB8000008, 0x133)
    word(0xB8000010, 0x1)
    word(0xB800000C, 0x382)
    word(0xB8000010, 0x2)
    word(0xB800000C, 0x402)
    word(0xB8000010, 0x2)
    word(0xB8000008, 0x33)
    word(0xB8000010, 0x1)
    word(0xB8000014, 0x4270)
    word(0xB800001C, 0x10012)
    word(0xB8000020, 0x10012)
    word(0xB8000024, 0x10012)
    word(0xB8000028, 0x10012)
    word(0xB8000018, 0xff)
    word(0xB80000c4, 0x74444444)
    word(0xB80000c8, 0x222)
    word(0xB80000cc, 0xfffff)
    word(0xB8000108, 0x0)

@command()
def inittlbs(device=None):
    \'\'\'Initialise the TLBs, e.g. after a reset.\'\'\'
    tlb_type = get_TLB_type()
    if tlb_type == 0:  # if no TLB
        print \'No TLB\'
        return

    cop_configs = get_available_COP_configs()
    if not does_config_exist(cop_configs, 1): # if no COP Config registers
        print \'COP Config registers not found\'
        return

    print \'Initializing TLBs\'
    num_of_mmu_entries = get_num_of_MMU_entries(tlb_type, cop_configs)
    make_all_TLB_available()
    invalidatetlb(num_of_mmu_entries)
    
@command()
def invalidatetlb(num_of_mmu_entries, device=None):
    \'\'\'Invalidate the TLBs to a system wide unique value\'\'\'
    cpu_num = get_native_core_number()
    addr = 0x80000000 | (cpu_num << 20)
    for index in range(0, num_of_mmu_entries + 1):
        tlb(index, [0, 0, addr + (index * 0x2000) + 0x40, 0])
    

@command()
def initcaches(device=None):
    \'\'\'Detect and initialise the caches, e.g. after a reset.\'\'\'
    cop_configs = get_available_COP_configs()
    if not does_config_exist(cop_configs, 1): # if no COP Config registers
        print \'COP Config registers not found\'
        return

    print \'Initializing Caches\'
    reset_L1_ICache()
    reset_L1_DCache()

    # On the first core only
    if get_native_core_number() == 0 and does_config_exist(cop_configs, 2):
        at_least_L2_exists = get_L2_cache_line_size()
        if at_least_L2_exists:
            enable_L2_3_cache(cop_configs, False)
            reset_L2_cache()
            reset_L3_cache()
            enable_L2_3_cache(cop_configs, True)
        
def get_native_core_number():
    return regs(\'EBase\').CPUNum

def get_TLB_type():
    return regs(\'Config\').MT

def get_available_COP_configs():
    MAX_COP_CONFIGS = 8
    result_set = set()
    for i in range(MAX_COP_CONFIGS):
        result_set.add(i)
        another_cfg_exists = regs(\'Config%s\' % (str(i) if i > 0 else \'\')).M
        if not another_cfg_exists:
            break
    return result_set
   
def does_config_exist(cop_configs, config_num):
    return config_num in cop_configs

def get_the_traditional_MMU_entry_size():
    return regs(\'Config1\').MMUSize

def get_num_of_MMU_entries(tlb_type, cop_configs):
    # Get the traditional MMU size
    entries = get_the_traditional_MMU_entry_size()

    # Cores with C0_CONFIG4 change the interpretation of this MMU size
    if does_config_exist(cop_configs, 4):
        ext_def = regs(\'Config4\').MMUExtDef
        if ext_def:
            # No FTLBs - C0_CONFIG4:ExtVTLBs extends C0_CONFIG1:MMUSize
            entries |= (long(regs(\'Config4\')) & 0x7f) << 6
        elif (tlb_type == 3) and (ext_def == 3):
            # FTLBs - defined by C0_CONFIG4:FTLB_*, above VTLBs
            ways = regs(\'Config4\').FTLB_Ways
            sets = regs(\'Config4\').FTLB_Sets
            entries += ways * sets
    return entries

def make_all_TLB_available():
    regs(\'Wired\', 0)

def enable_L2_3_cache(cop_configs, enable):
    if does_config_exist(cop_configs, 3):
        GCR_BASE = 0xbfbf8008
        try:
            # Enable / Disable CCA in GCR_Base
            wordmodify(GCR_BASE, 0 if enable else 0x50, 0xff)
        except RuntimeError:
            pass

def twotopowerof(value):
    return 2 << value if value else 0
    
def get_L1_Icache_line_size():
    return twotopowerof(regs(\'Config1\').IL)

def get_L1_Dcache_line_size():
    return twotopowerof(regs(\'Config1\').DL)

def get_L2_cache_line_size():
    return twotopowerof(regs(\'Config2\').SL)

def get_L3_cache_line_size():
    return twotopowerof(regs(\'Config2\').TL)

def reset_L1_ICache():
    L1_I_line_size = get_L1_Icache_line_size()
    if L1_I_line_size:
        regs(\'ITagLo\', 0)
        regs(\'ITagHi\', 0)
        config1 = regs(\'Config1\')
        i_lines = (64 << config1.IS) * (config1.IA + 1)
        print \'Initializing L1I: \' + str(i_lines) + \' sets, \' + str(L1_I_line_size) + \' byte line size\'
        cacheop(\'instr\', 0x80000000, L1_I_line_size, INDEX_STORE_TAG, count=i_lines)
    else:
        print \'No L1 I Cache\'

def reset_L1_DCache():
    L1_D_line_size = get_L1_Dcache_line_size()
    if L1_D_line_size:
        regs(\'DTagLo\', 0)
        regs(\'DTagHi\', 0)
        config1 = regs(\'Config1\')
        d_lines = (64 << config1.DS) * (config1.DA + 1)
        print \'Initializing L1D: \' + str(d_lines) + \' sets, \' + str(L1_D_line_size) + \' byte line size\'
        cacheop(\'data\', 0x80000000, L1_D_line_size, INDEX_STORE_TAG, count=d_lines)
    else:
        print \'No L1 D Cache\'

def reset_L2_cache():
    l2_line_size = get_L2_cache_line_size()
    if l2_line_size: # do we have an L2 Cache
        regs(\'L23TagLo\', 0)
        # cp0.29.4 is L23TAGHI, currently this has no name because no known mips 
        # cores implement it.  This write here is just belt and braces in case a 
        # core comes along with this register.
        regs(\'cp0.29.4\', 0)
        config2 = regs(\'Config2\')
        l2_lines = (64 << config2.SS) * (config2.SA + 1)
        print \'Initializing L2: \' + str(l2_lines) + \' sets, \' + str(l2_line_size) + \' byte line size\'
        cacheop(\'secondary\', 0x80000000, l2_line_size, INDEX_STORE_TAG, count=l2_lines)
    else:
        print \'No L2 Cache\'

def reset_L3_cache():
    l3_line_size = get_L3_cache_line_size()
    if l3_line_size: # do we have an L3 Cache
        config2 = regs(\'Config2\')
        l3_lines = (64 << config2.TS) * (config2.TA + 1)
        print \'Initializing L3: \' + str(l3_lines) + \' sets, \' + str(l3_line_size) + \' byte line size\'
        cacheop(\'tertiary\', 0x80000000, l3_line_size, INDEX_STORE_TAG, count=l3_lines)
    else:
        print \'No L3 Cache\'

if __name__ == \'__main__\':
    from imgtec.console.main import interact
    args=parse_startup_args()
    with probe(args=args):
        initregs()
        initmemory()
        inittlbs()
        initcaches()
        if sys.stdin.isatty():
            interact(args)

'''

# [[[end]]]

def import_code(code, name):
    import imp
    module = imp.new_module(name)
    exec code in module.__dict__
    return module

# [[[cog
# for module in examples_names:
#     if module != "mz_flash":
#         cog.outl("{0} = import_code({0}_code, '{0}')".format(module))
# ]]]
cpc_control = import_code(cpc_control_code, 'cpc_control')
diagnostic_tools = import_code(diagnostic_tools_code, 'diagnostic_tools')
ipconfig = import_code(ipconfig_code, 'ipconfig')
manageprobes = import_code(manageprobes_code, 'manageprobes')
pic32_flash_support = import_code(pic32_flash_support_code, 'pic32_flash_support')
scanmeta = import_code(scanmeta_code, 'scanmeta')
spramsetup = import_code(spramsetup_code, 'spramsetup')
virtualtap_adapter = import_code(virtualtap_adapter_code, 'virtualtap_adapter')
wifire = import_code(wifire_code, 'wifire')
wpj344 = import_code(wpj344_code, 'wpj344')
# [[[end]]]

# [[[cog
# cog.outl("examples = {")
# cog.out("".join('    "{0}": {0}_code,\n'.format(e) for e in examples_names))
# cog.out("}\n")
# ]]]
examples = {
    "cpc_control": cpc_control_code,
    "diagnostic_tools": diagnostic_tools_code,
    "ipconfig": ipconfig_code,
    "manageprobes": manageprobes_code,
    "mz_flash": mz_flash_code,
    "pic32_flash_support": pic32_flash_support_code,
    "scanmeta": scanmeta_code,
    "spramsetup": spramsetup_code,
    "virtualtap_adapter": virtualtap_adapter_code,
    "wifire": wifire_code,
    "wpj344": wpj344_code,
}
# [[[end]]]
