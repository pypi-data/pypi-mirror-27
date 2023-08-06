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

import re
from imgtec.lib.netifaces import Mac
from collections import namedtuple

__all__ = ['Identifier']

_ProbeInfo = namedtuple('_ProbeInfo', 'type mac min max dns hwserial')

_probe_info = [
    _ProbeInfo('Sysprobe', Mac('00-00-00-00-00-00'), 58000, 59000, 'img-sp%05d', '02MFLS110%05d'),
    _ProbeInfo('Sysprobe', Mac('00-00-00-00-00-00'), 57000, 58000, 'img-sp%05d', '02MFLS110%05d'),
    _ProbeInfo('Sysprobe', Mac('00-19-f5-01-60-00'), 0, 0x2000, 'img-sp%05d', '02DALS320%05d'),
    _ProbeInfo('DA-net', Mac('00-19-f5-01-00-00'), 0, 0x2000, "imgda-eth%05d", '01EGNT210%05d'),
    _ProbeInfo('DA-usb', None, 0, 0x2000, None, "00XPNT410%05d"),
    _ProbeInfo('DA-trace', Mac('00-19-f5-01-20-00'), 0, 0x2000, "imgda-trace%05d", '01EHSSRB0%05d'),
    _ProbeInfo('Dash', Mac('00-50-c2-01-b0-00'), 200, 4096, 'dash-dcsu%05d', 'DCSU%05d'),
    _ProbeInfo('Dash', Mac('00-50-c2-01-b0-00'), 2, 200, 'dash-dbsu%05d', 'DBSU%05d'),
    _ProbeInfo('Dash', Mac('00-50-c2-01-b0-00'), 0, 2, 'dash-dasu%05d', 'DASU%05d'),
]

_hwserial_re = re.compile(r"(?:(D[ABC]SU)|(DA)|(?:(00XP|01EG|01EH|02DA)[a-z0-9]{5}))(\d{1,5})$", re.I)
_identifier_re = re.compile(r"(?:(dash|da-?net|da-?usb|da-?trace|da-?sim|sp|sysprobe|busblaster|virtualtap) *(\d+))$|(?:([\w\-]+) +(.*))$",
                            re.I)

_da_name_map = {
    'busblaster': 'BusBlaster',
    'dash': 'Dash',
    'dasim': 'Dash',
    'danet': 'DA-net',
    'dausb': 'DA-usb',
    'datrace': 'DA-trace',
    'simulator': 'Simulator',
    'remotesimulator': 'RemoteSimulator',
    'gdbserver': 'gdbserver',
    'daext': 'DA-ext',
    'navigator': 'Navigator',
    'remoteimperas': 'RemoteImperas',
    'sp': 'SysProbe',
    'sysprobe': 'SysProbe',
    'virtualtap': 'VirtualTap',
}


def parse(identifier):
    '''Parse a probe identifier and return (Type, Index) or (Type, Name).
    
    >>> parse('sp71')
    ('SysProbe', 71)
    >>> parse('sp58001')
    ('SysProbe', 58001)
    >>> parse('sysprobe71')
    ('SysProbe', 71)
    >>> parse('sp 192.168.152.1')
    ('SysProbe', '192.168.152.1')
    >>> parse('whatever71')
    Traceback (most recent call last):
    ...
    ValueError: Could not interpret 'whatever71' as a valid probe identifier
    '''
    m = _identifier_re.match(identifier)
    if m:
        da_type = (m.group(1) or m.group(3)).lower().replace('-', '')
        index = int(m.group(2)) if m.group(2) else m.group(4)
        return _da_name_map.get(da_type, (m.group(1) or m.group(3)).title()), index
    raise ValueError("Could not interpret %r as a valid probe identifier" % (identifier,))


class Identifier(str):
    '''Represents a probe identifier.

    >>> Identifier('sp 123')
    'SysProbe 123'
    >>> Identifier('SysProbe 123').index
    123
    >>> Identifier('SysProbe localhost').index
    -1
    >>> Identifier('SysProbe localhost').name
    'localhost'
    >>> Identifier('SysProbe localhost').is_tcp
    True
    >>> Identifier('DA-net 123').is_tcp
    False
    '''

    def __new__(cls, s):
        type, name = parse(s)
        x = str.__new__(cls, "%s %s" % (type, name))
        x.type = type
        x.name = name
        return x

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def _get_name(self):
        try:
            return int(self.name)
        except ValueError:
            return self.name

    def short_id(self):
        res = "Sp" if self.type == 'SysProbe' else "Da"
        return res + str(self.name)

    def __eq__(self, other):
        try:
            return (self.type, self._get_name()) == (other.type, other._get_name())
        except AttributeError:
            try:
                other = Identifier(other)
                return self == other
            except (ValueError, TypeError):
                return False

    def __lt__(self, other):
        try:
            if other is None:
                return False
            return (self.type, self._get_name()) < (other.type, other._get_name())
        except AttributeError:
            try:
                other = Identifier(other)
                return self < other
            except (ValueError, TypeError):
                return type(self) < type(other)

    def __le__(self, other):
        try:
            if other is None:
                return False
            return (self.type, self._get_name()) <= (other.type, other._get_name())
        except AttributeError:
            try:
                other = Identifier(other)
                return self <= other
            except (ValueError, TypeError):
                return type(self) <= type(other)

    @property
    def is_tcp(self):
        return self.type == 'SysProbe'

    @property
    def index(self):
        if isinstance(self.name, (int, long)):
            return self.name
        return -1

    @property
    def dns(self):
        '''Get the DNS name for this probe identifier.'''
        return make_dns(self)

    @property
    def mac(self):
        '''Get the Mac address of this probe identifier.'''
        return make_mac(self)

    @property
    def hwserial(self):
        '''Create the hardware serial number of this probe identifier.'''
        return make_hwserial(self)

    @classmethod
    def from_mac(cls, mac):
        r'''Determine a probe identifier based on a mac address.

        >>> Identifier.from_mac(Mac('\x00\x19\xf5\x01\x00\x23'))
        'DA-net 35'
        >>> Identifier.from_mac(Mac('00-50-c2-01-b1-c0'))
        'Dash 448'
        >>> Identifier.from_mac(Mac('\x01\x19\xf5\x01\x00\x23'))
        Traceback (most recent call last):
        ...
        ValueError: Could not determine probe identifier from mac address 01-19-f5-01-00-23
        '''
        for info in _probe_info:
            if info.mac:
                try:
                    min = _make_mac(info, info.min)
                except TypeError:
                    return repr((info, info.mac))

                max = _make_mac(info, info.max - 1)
                if min.as_int() <= mac.as_int() <= max.as_int():
                    return cls('%s %d' % (info.type, mac.as_int() - min.as_int() + info.min))
        raise ValueError('Could not determine probe identifier from mac address %r' % (mac,))

    @classmethod
    def from_hwserial(cls, serial):
        r'''Create a probe identifier from a hardware serial number.

        >>> Identifier.from_hwserial('01EGNT21000035')
        'DA-net 35'
        >>> Identifier.from_hwserial('01EGyyyyy00035')
        'DA-net 35'
        >>> Identifier.from_hwserial('12333214324233')
        Traceback (most recent call last):
        ...
        ValueError: Could not determine probe identifier from hardware serial '12333214324233'
        '''
        m = _hwserial_re.match(serial)
        if m:
            leading = m.group(1) or m.group(2) or m.group(3)
            index = int(m.group(4))
            for info in _probe_info:
                if info.hwserial.lower().startswith(leading.lower()):
                    return cls('%s %d' % (info.type, index))
        raise ValueError('Could not determine probe identifier from hardware serial %r' % (serial,))

    @classmethod
    def from_dns(cls, hostname):
        '''Convert a dns name to a probe identifier.

        >>> Identifier.from_dns('imgda-eth00035.le.imgtec.org')
        'DA-net 35'
        >>> Identifier.from_dns('imgda-eth00035')
        'DA-net 35'
        >>> Identifier.from_dns('wubble')
        Traceback (most recent call last):
        ...
        ValueError: 'wubble' is not a known probe DNS name.
        '''
        for info in _probe_info:
            if info.dns:
                expr = re.sub('%\0?\d+d', r'(\d+)', info.dns) + r'(\..*)?'
                m = re.match(expr, hostname, flags=re.I)
                if m:
                    return cls(info.type + ' ' + m.group(1))
        raise ValueError('%r is not a known probe DNS name.' % (hostname,))


normalise = Identifier
from_dns = Identifier.from_dns
from_mac = Identifier.from_mac
from_hwserial = Identifier.from_hwserial


def _get_probe_info(type, index, _for=''):
    possibles = [info for info in _probe_info if info.type.lower() == type.lower()]
    if not possibles:
        if _for and type.lower() not in _da_name_map:
            _for = ''
        raise ValueError("Invalid probe type %r%s." % (type, _for))
    try:
        index = int(index, 10)
    except TypeError:
        pass

    inrange = [info for info in possibles if index >= info.min and index < info.max]
    if not inrange:
        possibles.sort(key=lambda x:x.min)
        ranges = ', '.join('%d-%d' % (info.min, info.max-1) for info in possibles)
        raise ValueError("Invalid index %d, valid indicies for %s are %s." % (index, type, ranges))
    return inrange[0], index

def make_dns(identifier):
    '''Get the DNS name for the given probe identifier.

    >>> make_dns('DAnet 35')
    'imgda-eth00035'
    >>> make_dns('DAnet 8191')
    'imgda-eth08191'
    >>> make_dns('Wubble 8192')
    Traceback (most recent call last):
    ...
    ValueError: Invalid probe type 'Wubble'.

    '''
    type, index = parse(identifier)
    info, index = _get_probe_info(type, index, ' for a DNS name')
    return info.dns % (index,)


def make_mac(identifier):
    '''Get the mac address for the given probe identifier.

    >>> make_mac('DAnet 35')
    00-19-f5-01-00-23
    >>> make_mac('DAnet 8191')
    00-19-f5-01-1f-ff
    >>> make_mac('Dash 448')
    00-50-c2-01-b1-c0
    >>> make_mac('Dash 148')
    00-50-c2-01-b0-94
    >>> make_mac('Dash 1')
    00-50-c2-01-b0-01
    >>> make_mac('SysProbe 58011')
    00-00-00-00-e2-9b
    >>> make_mac('SysProbe 56999')
    Traceback (most recent call last):
    ...
    ValueError: Invalid index 56999, valid indicies for SysProbe are 0-8191, 57000-57999, 58000-58999.
    >>> make_mac('DAnet 8192')
    Traceback (most recent call last):
    ...
    ValueError: Invalid index 8192, valid indicies for DA-net are 0-8191.
    >>> make_mac('Simulator 8192')
    Traceback (most recent call last):
    ...
    ValueError: Invalid probe type 'Simulator' for a mac address.
    '''
    type, index = parse(identifier)
    info, index = _get_probe_info(type, index, ' for a mac address')
    return _make_mac(info, index)


def _make_mac(info, index):
    index_bytes = [((index >> (byte * 8)) & 0xff) for byte in range(len(info.mac) - 1, -1, -1)]
    mac = [ord(base) | x for base, x in zip(info.mac, index_bytes)]
    return Mac(''.join(chr(x) for x in mac))


def make_hwserial(da_name):
    r'''Create the hardware serial number from a probe identifier.

    >>> make_hwserial('danet35')
    '01EGNT21000035'
    >>> make_hwserial('sp71')
    '02DALS32000071'
    '''
    type, index = parse(da_name)
    info, index = _get_probe_info(type, index, ' for a hardware serial number')
    return info.hwserial % index


if __name__ == '__main__':
    import doctest, sys

    if doctest.testmod()[0]:
        sys.exit(1)
