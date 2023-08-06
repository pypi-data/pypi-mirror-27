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

#!/usr/bin/env python
from __future__ import division
import re
import socket
import select
import sys
from collections import namedtuple
from contextlib import contextmanager
from timeit import default_timer
from imgtec.lib.netifaces import Mac
from imgtec.lib import netifaces
from imgtec.lib.namedstruct import namedstruct
from imgtec.lib.namedenum import namedenum
from imgtec.codescape.probe_identifier import Identifier

__all__ = ['listen_for_broadcasts', 'find', 'discover', 'identify']

Protocol = namedenum('Protocol', 'udp tcp')
FoundProbe = namedtuple('FoundProbe', 'identifier ip protocol')

class ProbeFinder(object):
    '''ABC of the interface used by find_probe.'''

    def find(self, identifier):
        """Issue a UDP query_ip command broadcast on all interfaces on port 59.

        return None or an instance of FoundProbe.
        """
        raise NotImplementedError()

    def identify(self, ip):
        """Issue a UDP query_ip command to destination on port 59 with the 
        Mac address as a wildcard, to determine the probe identifier.

        .. note:: This is not supported in older DA-net f/w.
        
        return None or an instance of FoundProbe.
        """
        raise NotImplementedError()
        
    def verify(self, identifier, ip):
        """Issue a UDP query_ip command to destination on port 59 with the
        Mac address correctly initialised for the given identifier.

        return None or an instance of FoundProbe.
        """
        raise NotImplementedError()
        
    def dns_lookup(self, name):
        """Perform a DNS lookup of a host name, return None on failure."""
        raise NotImplementedError()
        
def _validate_ip(finder, identifier, ip):
    wrong = None
    found = finder.verify(identifier, ip)
    if not found:
        wrong = finder.identify(ip) # is someone else there?
        if wrong and wrong.identifier == identifier:
            # Probably the probe was just powering up so the verify failed but identify succeeded
            found, wrong = wrong, found
    return found, wrong
        
def find_probe(identifier, search_location, finder):
    """Defines the search algorithm used to locate SysProbes and DA-nets.
    
    finder is a concrete implementation of ProbeFinder.
    search_location may be an empty string or a hostname/ip-address on which to 
    begin the search.
    
    Returns FoundProbe or raises an exception on failure.
    """
    if identifier.index == 0 and not search_location:
        raise DeviceNotFound("Failed to find requested device : When using identifier %s a search-location must be specified" % identifier)

    if identifier.index == -1 and not search_location:
        search_location = identifier.name

    found, wrong = None, None
    search_ip = search_location and _dns_lookup(finder, search_location)
    if identifier.index != 0 and identifier.index != -1:
        if search_ip:
            found, wrong  = _validate_ip(finder, identifier, search_ip)
            if wrong:
                search_ip = None

        if not found:
            # this will succeed even if specified ip was wrong, also finds usb devices
            found = finder.find(identifier)

        if not found:
            dns_ip = _dns_lookup(finder, identifier.dns)
            if dns_ip:
                found, wrong = _validate_ip(finder, identifier, dns_ip)
                if not found and not wrong and not search_ip and identifier.is_tcp:
                    # maybe UDP is broken completely, trust the DNS if we have no reason to suspect it as invalid
                    found = FoundProbe(identifier, dns_ip, Protocol.tcp)

        if not found and not wrong and search_ip and identifier.is_tcp:
            # the user has specified a search location, and even though it failed to identify
            # we ought to try a tcp connection
            found = FoundProbe(identifier, search_ip, Protocol.tcp)

    else:
        # e.g. 'sp 1.2.3.4', 'sp localhost' or probe('sp 0', '1.2.3.4')
        if not search_ip:
            raise DeviceNotFound("Failed to find requested device : Could not resolve %s" % search_location)
        found = finder.identify(search_ip)
        if not found:
            # we don't know the identifier, but we do know the ip, only tcp can work
            found = FoundProbe(Identifier("SysProbe 0"), search_ip, Protocol.tcp)

    if not found:
        raise DeviceNotFound(notfoundmessage(identifier, search_location, wrong and wrong.identifier))
    return found        
        

LOOPBACK  = '127.0.0.1'
BROADCAST = '255.255.255.255'
ConfigPacketImpl = namedstruct('NailConfigImpl', [
        'H ident',
        'H type',
        "6s mac=''",
        "4s ip=''",
    ],
    prefix='!',
)
class ConfigPacket(ConfigPacketImpl):
    r'''The packet used to send and receive nail commands over UDP.

    >>> ConfigPacket(0x1234, 1, '\x00\x19\xf5\x01`\x16', '\x00\x00\x00\x00')
    ConfigPacket(0x1234, 0x0001 (query_ip), 00-19-f5-01-60-16, '0.0.0.0')
    >>> ConfigPacket(0xc0c0, 1, '\x00\x19\xf5\x01`\x16', '\x00\x00\x00\x00')
    ConfigPacket(0xc0c0 (config), 0x0001 (query_ip), 00-19-f5-01-60-16, '0.0.0.0')
    '''
    def __repr__(self):
        enums = []
        for value, type in [(self.ident, Ident), (self.type, Config)]:
            try:
                enums.append('0x%04x (%s)' % (value, type(value)))
            except ValueError:
                enums.append('0x%04x' % (value, ))
        mac = Mac(self.mac)
        ip = '.'.join('%d' % ord(x) for x in self.ip)
        return '%s(%s, %s, %r, %r)' % (self.__class__.__name__, enums[0], enums[1], mac, ip)

Ident = namedenum('Ident', command=0xdada, config=0xc0c0)
Config = namedenum('Config', query_ip=1,
                             force_ip=2,
                             dhcp_on=3,
                             dhcp_off=4,
                             tcp_enabled=5)
Command= namedenum('Command', connect=1,
                              allowed=2,
                              refused=3,
                              disconnect=4,
                              disconnected=5,
                              command=6,
                              reply=7,
                              forced_disconnect=8)
        

def _wait_for_readable_socket(sockets, timeout=None):
    start = default_timer()
    remaining = timeout
    while timeout is None or remaining >= 0:
        args = () if timeout is None else (remaining,)
        ready, _, _ = select.select(sockets, [], [], *args)
        now = default_timer()
        for s in ready:
            yield s, (now - start)
        if timeout is not None:
            remaining = timeout - (now - start)


_SocketInfo = namedtuple('_SocketInfo', 'address port broadcast')
_socket_cache = {}
'''A dict of _SocketInfo->socket.'''

@contextmanager
def _open_sockets(addresses, port, broadcast):
    sockets = []
    infos = []
    for address in addresses:
        info = _SocketInfo(address, port, broadcast)
        try:
            s = _socket_cache.pop(info)
        except KeyError:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            if broadcast:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 0x9000)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 0x9000)
            s.bind((address, port))
        infos.append(info)
        sockets.append(s)
    try:
        yield sockets
    finally:
        # don't close the sockets, because on windows the close can take
        # up to 20s.  stick them in a socket cache for reuse
        #for s in sockets:
        #    s.close()
        _socket_cache.update(zip(infos, sockets))

def listen_for_broadcasts(addresses, identifier):
    '''Listen indefinitely for UDP broadcasts searching for the given probe.'''
    identifier = Identifier(identifier)

    # you'd think that we could bind to a particular interface but it doesn't
    # work on linux. So instead we bind to all interfaces and reply with our ip
    # as 0.0.0.0 both nail and this module use the actual address that the
    # packet came from in that case
    with _open_sockets([''], 59, broadcast=False) as sockets:
        mymac = identifier.mac
        for socket, response_time in _wait_for_readable_socket(sockets):
            data, fromaddr = socket.recvfrom(ConfigPacket._size)
            data = ConfigPacket._unpack(data)
            if data.ident == Ident.config and data.type==Config.query_ip:
                gotmac = Mac(data.mac)
                if gotmac in (Mac(), mymac):
                    if gotmac == Mac():
                        print 'Received request for all probes from %s.' % (fromaddr,)
                    else:
                        print 'Received request for this probe from %s.' % (fromaddr,)
                    p = ConfigPacket(ident=Ident.config, type=Config.query_ip,
                                    mac=mymac, ip='\x00\x00\x00\x00')
                    socket.sendto(p._pack(), fromaddr)
                else:
                    try:
                        id = Identifier.from_mac(gotmac)
                    except ValueError:
                        id = repr(gotmac)
                    print 'Ignored request for', id

def _query_ip(interface_addresses, identifier, address, timeout=1.0, verbose=False):
    '''Perform a query ip command.

    If `identifier` is given then a specific broadcast for that probe
    is issued. If `Identifier` is None then a broadcast for all probes using the
    wildcard mac is issued.

    In either case (identifier, address) pairs will be yielded as they are
    found,  and after a maximum `timeout` seconds the generator will stop
    yielding items.
    '''
    mac = identifier.mac if identifier else Mac()
    p = ConfigPacket(ident=Ident.config, type=Config.query_ip, mac=mac)
    with _open_sockets(interface_addresses, 0, broadcast=address==BROADCAST) as sockets:
        seen = set()
        NUM_RETRIES = 3
        for retry in range(NUM_RETRIES):
            for s in sockets:
                if verbose:
                    print '  sending %r to %s:%s on if %s' % (p, address, 59, s.getsockname()[0])
                s.sendto(p._pack(), (address, 59))
            for s, response_time in _wait_for_readable_socket(sockets, timeout/NUM_RETRIES):
                if verbose:
                    print '  received socket readable event on %s' % (s.getsockname()[0],)
                try:
                    data, (addr, port) = s.recvfrom(1400)
                except socket.error as e:
                    if verbose:
                        print ' ', e
                    continue

                data = ConfigPacket._unpack_from(data)
                if verbose:
                    print '  %.6fs received %r from %s:%d' % (response_time, data, addr, port)
                found_mac = Mac(data.mac)
                if found_mac == Mac():
                    if verbose:
                        print '  ignoring wildcard mac'
                    continue

                try:
                    found = Identifier.from_mac(found_mac)
                except ValueError as e:
                    if str(found_mac) == '<DHCP>' and identifier:
                        found = identifier
                        if verbose:
                            print '  received mac address of <DHCP> so assuming %r' % (identifier,)
                    else:
                        if verbose:
                            print '  could not interpret: %r(%s) as a probe mac address' % (found_mac,str(found_mac))
                        continue # bad mac, or unknown type

                if found in seen:
                    if verbose:
                        print "Ignoring %r because we've seen it before" % (found,)
                    continue
                seen.add(found)

                protocol = Protocol.tcp if data.type == Config.tcp_enabled else Protocol.udp
                probe_address = '.'.join('%d' % ord(x) for x in data.ip)
                if probe_address == '0.0.0.0':
                    probe_address  = addr
                yield FoundProbe(found, probe_address, protocol)

def discover(interface_addresses, timeout=1.0, verbose=False):
    '''Discover probes via UDP broadcast.

    A broadcast for all probes is issued, and a list of (identifier, address)
    pairs will be yielded as they are found.

    A maximum of `timeout` seconds will be waited for responses.
    '''
    for found in _query_ip(interface_addresses, None, BROADCAST, timeout, verbose):
        yield (found.identifier, found.ip)        

class CallLogger(object):
    def __init__(self, underlying):
        self.underlying = underlying
        
    def __getattr__(self, name):
        f = getattr(self.underlying, name)
        def wrapper(*args, **kwargs):
            allargs = [repr(x) for x in args] + ['%s=%r' % x for x in kwargs.items()]
            msg = '%s(%s)' % (name, ', '.join(allargs))
            print msg, '->'
            try:
                res = f(*args, **kwargs)
                print ' ' * len(msg), '->', repr(res)
                return res
            except Exception as e:
                print ' ' * len(msg), '->', repr(e)
                raise
        return wrapper

class RealProbeFinder(ProbeFinder):
    def __init__(self, timeout=1.0, verbose=False):
        self.interface_addresses = netifaces.addresses(netifaces.interfaces())
        self.timeout = timeout
        self.verbose = verbose

    def find(self, identifier):
        for found in _query_ip(self.interface_addresses, identifier, BROADCAST, self.timeout, self.verbose):
            return found
    def identify(self, ip):
        for found in _query_ip([''], None, ip, self.timeout, self.verbose):
            return found
    def verify(self, identifier, ip):
        for found in _query_ip([''], identifier, ip, self.timeout, self.verbose):
            return found
    def dns_lookup(self, name):
        try:
            return socket.gethostbyname(name)
        except socket.gaierror:
            return None
            
class TCPOpener(object):
    def tcp_connect(self, ip, port):
        tcp = socket.create_connection((ip, port), timeout=2)
        tcp.close()
        return True
        
def make_finder(timeout, verbose):
    finder = RealProbeFinder(timeout, verbose>1)
    if verbose:
        finder = CallLogger(finder)
    return finder
    
def find(identifier, search_location='', timeout=1.0, verbose=False):
    '''Find the address of a probe using DNS and UDP broadcast.'''
    identifier = Identifier(identifier)
    finder = make_finder(timeout, verbose)
    found = find_probe(identifier, search_location, finder)
    # For TCP probes, check that it does actually have something listening there
    # because find_probe will return probes that have not been verified or 
    # identified in case UDP is broken
    if found.protocol == Protocol.tcp:
        opener = TCPOpener()
        if verbose:
            opener = CallLogger(opener)
        try:        
            opener.tcp_connect(found.ip, 9999)
        except socket.error:
            found = None
    if not found:
        raise DeviceNotFound(notfoundmessage(identifier, search_location))
    return found.ip
        
def identify(ip_address, timeout=2.0, verbose=False):
    '''Determine the probe identifier of a probe at the given ip address.'''
    finder = make_finder(timeout, verbose)
    found = finder.identify(ip_address)
    if found:
        return found.identifier
    raise RuntimeError("The device at %s does not appear to be a probe" % (ip_address,))

def _dns_lookup(finder, name):
    '''Catch dns lookups of dotted ip addresses, to avoid bothering ProbeFinder
    with simple requests.
    '''
    if re.match('(?:\\d{1,3}\\.){3}\\d{1,3}$', name):
        return name
    return finder.dns_lookup(name)

class DeviceNotFound(RuntimeError):
    pass
    
def notfoundmessage(identifier, search_location='', wrong=None):
    if wrong:
        msg = ("Failed to find requested device : The probe at %s is %s but %s was requested, all other search mechanisms failed"
                                    % (search_location, wrong, identifier))
    else:
        what = identifier
        if identifier.index == 0 and identifier.index != -1:
            what = "a " + identifier.type
        at = search_location and (" at " + search_location)
        msg = "Failed to find requested device : All search mechanisms failed for %s%s" % (what, at)
    return msg

def _find(args):
    ip = find(args.probe, args.search_location, args.timeout, args.verbose)
    print 'Found %s at %s' % (args.probe, ip) 

def _identify(args):
    identifier = identify(args.ip, args.timeout, args.verbose)
    print 'Found %s at %s' % (identifier, args.ip)

def _listen(args):
    interface_addresses = netifaces.addresses(netifaces.interfaces())
    listen_for_broadcasts(interface_addresses, args.probe)

def _discover(args):
    interface_addresses = netifaces.addresses(netifaces.interfaces())
    for identifier, ip in discover(interface_addresses, args.timeout, args.verbose):
        #mode = '(failsafe)' if found.identifier.startswith('SysProbe') and found.protocol == Protocol.udp else ''
        print 'Found', identifier, 'at', ip
    print 'Search complete'

def _interfaces(args):
    interfaces = netifaces.interfaces()
    longest = max(len(interface.name) for interface in interfaces)
    for interface in interfaces:
        print '%s %s %r' % (interface.name.ljust(longest), interface.addresses[0].address, interface.mac)
        

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action='count', help='Be more verbose, add multiple times for more verbosity')
    subparsers = parser.add_subparsers()
    listen_parser = subparsers.add_parser('listen', help='Listen for discovery broadcasts')
    listen_parser.add_argument('probe', type=Identifier, help='Probe identifier to listen for')
    listen_parser.set_defaults(func=_listen)
    discover_parser = subparsers.add_parser('discover', help='Discover probes in the vicinity')
    discover_parser.add_argument('--timeout', default=1.0, type=float, help='Number of seconds to wait for responses (default 1s)')
    discover_parser.set_defaults(func=_discover)
    find_parser = subparsers.add_parser('find', help='Find a probe')
    find_parser.add_argument('probe', type=Identifier, help='Probe identifier to find')
    find_parser.add_argument('search_location', default='', nargs='?', type=str, help='Optional IP address/hostname to start search at')
    find_parser.add_argument('--timeout', default=1.0, type=float, help='Number of seconds to wait for responses (default 1s)')
    find_parser.set_defaults(func=_find)
    identify_parser = subparsers.add_parser('identify', help='Identify a probe based on ip address')
    identify_parser.add_argument('ip', type=str, help='IP address to identify')
    identify_parser.add_argument('--timeout', default=1.0, type=float, help='Number of seconds to wait for responses (default 1s)')
    identify_parser.set_defaults(func=_identify)

        
    args = parser.parse_args()
    #args = parser.parse_args(['find', 'sp58011', '192.168.152.44'])
    #args = parser.parse_args(['discover'])
    if not args.verbose:
        import doctest
        if doctest.testmod()[0]:
            sys.exit(1)
    try:
        sys.exit(args.func(args))
    except Exception as e:
        sys.exit(str(e))
    
    
