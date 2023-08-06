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

'''A portable mechanism to enumerate the available network interfaces.'''
#!/usr/bin/env python
from collections import namedtuple
import itertools
import re
import sys

__all__ = ('Address', 'Interface', 'Mac', 'interfaces', 'addresses')

class Address(namedtuple('Address', 'address mask')):
    """An address and mask pair.
    
.. py:attribute:: address

    The ipv4 address as a dotted string.

.. py:attribute:: mask

    The ipv4 subnet mask as a dotted string.

"""
    
class Interface(namedtuple('Interface', 'name mac addresses')):
    """An address and mask pair.

.. py:attribute:: name

    The name of the interface. On linux/OSX this is typically something like
    'en1', on windows this is usually the name of the device driver.

.. py:attribute:: mac

    The MAC address of interface.  See :class:`Mac`.
    
.. py:attribute:: addresses

    List of :class:`Address`\s associated with this interface. This list will 
    always contain at least one item.

"""

class Mac(str):
    r'''Extends string to format mac addresses nicely.

    A Mac can be created from a 6-byte binary, or hyphenated hex pairs.

    >>> Mac()
    00-00-00-00-00-00
    >>> Mac('\x01\x19\xf5\x01\x00\x23')
    01-19-f5-01-00-23
    >>> Mac('01-19-F5-01-00-23')
    01-19-f5-01-00-23
    >>> Mac('\x01\x19\xf5\x01\x00')
    Traceback (most recent call last):
    ...
    ValueError: Badly formatted Mac address '\x01\x19\xf5\x01\x00'.
    '''

    def __new__(cls, s=''):
        if not s:
            return str.__new__(cls, '\x00' * 6)
        if len(s) == 6:
            return str.__new__(cls, s)
        if not re.match(r'([0-9a-f]{1,2}-){5}[0-9a-f]{1,2}', s, flags=re.I):
            raise ValueError('Badly formatted Mac address %r.' % (s,))
        return str.__new__(cls, ''.join([chr(int(byte, 16)) for byte in s.split('-')]))

    def __repr__(self):
        return '-'.join('%02x' % ord(x) for x in self)

    def as_int(self):
        r"""Return the mac address as an integer.

        >>> '%012x' % Mac('01-19-f5-01-00-23').as_int()
        '0119f5010023'
        """
        return int(''.join('%02x' % ord(x) for x in self), 16)


def _win32():
    import ctypes.wintypes

    MAX_ADAPTER_ADDRESS_LENGTH = 8
    MAX_ADAPTER_NAME_LENGTH = 256
    MAX_ADAPTER_DESCRIPTION_LENGTH = 128
    ERROR_BUFFER_OVERFLOW = 111
    DWORD = ctypes.wintypes.DWORD
    UINT = ctypes.wintypes.UINT
    BOOL = ctypes.wintypes.BOOL

    class IP_ADDR_STRING(ctypes.Structure):
        pass
    PIP_ADDR_STRING = ctypes.POINTER(IP_ADDR_STRING)
    TIME_T=ctypes.c_int64 if ctypes.sizeof(PIP_ADDR_STRING) == 8 else ctypes.c_int32
    IP_ADDR_STRING._fields_ = [
        ("Next", PIP_ADDR_STRING),
        ("IpAddress", ctypes.c_char * 16),
        ("IpMask", ctypes.c_char * 16),
        ("Context", DWORD)]

    class IP_ADAPTER_INFO(ctypes.Structure):
            pass
            
    PIP_ADAPTER_INFO = ctypes.POINTER(IP_ADAPTER_INFO)
    IP_ADAPTER_INFO._fields_ = [('Next', PIP_ADAPTER_INFO),
            ('ComboIndex', DWORD),
            ('AdapterName', ctypes.c_char * (MAX_ADAPTER_NAME_LENGTH + 4)),
            ('Description', ctypes.c_char * (MAX_ADAPTER_DESCRIPTION_LENGTH + 4)),
            ('AddressLength', UINT),
            ('Address', ctypes.c_ubyte * MAX_ADAPTER_ADDRESS_LENGTH),
            ('Index', DWORD),
            ('Type', UINT),
            ('DhcpEnabled', UINT),
            ('CurrentIpAddress', PIP_ADDR_STRING),
            ('IpAddressList', IP_ADDR_STRING),
            ('GatewayList', IP_ADDR_STRING),
            ('DhcpServer', IP_ADDR_STRING),
            ('HaveWins', BOOL),
            ('PrimaryWinsServer', IP_ADDR_STRING),
            ('SecondaryWinsServer', IP_ADDR_STRING),
            ('LeaseObtained', TIME_T),
            ('LeaseExpires', TIME_T)]

    GetAdaptersInfo = ctypes.WINFUNCTYPE(DWORD, PIP_ADAPTER_INFO, ctypes.POINTER(ctypes.c_ulong))(('GetAdaptersInfo', ctypes.windll.iphlpapi))

    adapters = (IP_ADAPTER_INFO * 1)()
    buflen = ctypes.c_ulong(ctypes.sizeof(IP_ADAPTER_INFO))
    res = GetAdaptersInfo(adapters, ctypes.byref(buflen))
    if res == ERROR_BUFFER_OVERFLOW:
        ctypes.resize(adapters, buflen.value)
        res = GetAdaptersInfo(adapters, ctypes.byref(buflen))
        if res:
            print 'Warning, failed to read adapter info, error code %d' % (res,)
            buflen.value = 0
    ifaces = []
    if buflen.value >= ctypes.sizeof(IP_ADAPTER_INFO):
        adapter = adapters[0]
        while adapter:
            adNode = adapter.IpAddressList
            ips = []
            while adNode:
                ipAddr = adNode.IpAddress
                if ipAddr:
                    ips.append(Address(ipAddr, adNode.IpMask))
                adNode = adNode.Next and adNode.Next.contents
            address = ''.join(chr(part) for part in adapter.Address[:6])
            ifaces.append(Interface(adapter.Description, Mac(address), ips))
            adapter = adapter.Next and adapter.Next.contents
    return ifaces

def _fcntl():
    import array, socket, struct, fcntl, platform
    SIOCGIFCONF = 0x8912
    SIOCGIFHWADDR = 0x8927

    def get_mac_address(sock, ifname):
        info = fcntl.ioctl(sock.fileno(), SIOCGIFHWADDR, struct.pack("256s", ifname[:15]))
        return Mac("-".join("%02X" % ord(x) for x in info[18:24]))

    bufsize = 4096
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = array.array("B", "\0" * bufsize)
    size = struct.unpack("iP", fcntl.ioctl(sock.fileno(), SIOCGIFCONF,
                struct.pack("iP", bufsize, data.buffer_info()[0])))[0]
    interfaces = []
    for i in xrange(0, size, 32 if platform.architecture()[0] != "64bit" else 40):
        name = data[i:i+16].tostring().split("\0", 1)[0]
        addr = data[i+20:i+24]
        mac = get_mac_address(sock, name)
        addresses = [Address('.'.join('%d' % x for x in addr), '')]
        interfaces.append(Interface(name, mac, addresses))
    return interfaces
    
test_ifconfig = '''\
lo0: flags=8049<UP,LOOPBACK,RUNNING,MULTICAST> mtu 16384
        options=3<RXCSUM,TXCSUM>
        inet6 ::1 prefixlen 128
        inet 127.0.0.1 netmask 0xff000000
        inet6 fe80::1%lo0 prefixlen 64 scopeid 0x1
        nd6 options=1<PERFORMNUD>
en0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
        options=10b<RXCSUM,TXCSUM,VLAN_HWTAGGING,AV>
        ether 3c:07:54:43:8a:b6
        inet6 fe80::3e07:54ff:fe43:8ab6%en0 prefixlen 64 scopeid 0x4
        inet 192.168.152.88 netmask 0xffffff00 broadcast 192.168.152.255
        nd6 options=1<PERFORMNUD>
        media: autoselect (1000baseT <full-duplex,flow-control>)
        status: active
en1: flags=8823<UP,BROADCAST,SMART,SIMPLEX,MULTICAST> mtu 1500
        ether 60:c5:47:22:67:c7
        nd6 options=1<PERFORMNUD>
        media: autoselect (<unknown type>)
        status: inactive
'''

def _parse_ifconfig(lines):
    '''Parse the output of parse_ifconfig.

    `lines` is an iterable of lines in the output.

    >>> _parse_ifconfig(test_ifconfig.splitlines())
    [Interface(name='en0', mac=3c-07-54-43-8a-b6, addresses=[Address(address='192.168.152.88', mask='255.255.255.0')])]
    '''
    r_interface_line = re.compile(r"^(\w+):.*$")
    r_mac_address = re.compile(r"^\s+ether\s+([0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5})\s*$")
    r_inet = re.compile('^\s*inet\s+((?:\d{1,3}\.){3}\d{1,3})\s+netmask\s+0x([0-9a-f]{8})\s+broadcast\s+((?:\d{1,3}\.){3}\d{1,3})')
    name, mac, addr = None, None, None
    interfaces = []
    for line in lines:
        m_interface = r_interface_line.match(line)
        if m_interface:
            name, mac, addr = m_interface.group(1), None, None
            continue
        m_mac_address = r_mac_address.match(line)
        if m_mac_address:
            mac_address = m_mac_address.group(1)
            mac = Mac(mac_address.replace(":", "-").upper())
        m_inet = r_inet.match(line)
        if m_inet:
            addr, mask = m_inet.group(1, 2) # broadcast?
            mask = '.'.join('%d' % int(mask[n:n+2], 16) for n in range(0, 8, 2))
            addr = Address(addr, mask)
        if name and mac and addr:
            interfaces.append(Interface(name, mac, [addr]))
            name, mac, addr = None, None, None
    return interfaces

def _ifconfig():
    import subprocess
    process = subprocess.Popen(["ifconfig"], stdout=subprocess.PIPE)
    return parse_ifconfig(process.stdout)

def interfaces():
    '''Detect the network interfaces available.
    
    Return a list of :class:`Interface`\s
    '''
    if sys.platform == "win32":
        return _win32()
    elif sys.platform[:5] == "linux":
        return _fcntl()
    else: # probably *nix of some sort which probably has ifconfig
        return _ifconfig()

def addresses(interfaces):
    '''Return all of the ip addresses found in the given list of Interfaces.'''
    all =  [a.address for a in itertools.chain.from_iterable(i.addresses for i in interfaces)]
    return [addr.address for addr in itertools.chain.from_iterable(a.addresses for a in interfaces)]


if __name__ == '__main__':
    import doctest
    if doctest.testmod()[0]:
        sys.exit(1)
    found = interfaces()
    longest = max(len(interface.name) for interface in found) if found else 0
    for i in found:
        print '%s %s %r' % (i.name.ljust(longest), i.addresses[0].address, i.mac)
        for other in i.addresses[1:]:
            print '%s %s' % (''.ljust(longest), other.address,)


