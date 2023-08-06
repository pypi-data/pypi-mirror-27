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
import itertools
from imgtec.codescape import probe_identifier

__all__ = ('DAConfig', 'DAConfigList')

class DAConfig(object):
    def __init__(self, section, index):
        self._section = section
        self._index = index
        
    def __repr__(self):
        ip = ' ip_address=%s' % (self.ip_address,) if self.use_ip_address else ''
        return '%s scan_for_it=%d%s' % (self.serial, self.scan_for_it, ip)

    @property
    def serial(self):
        return probe_identifier.from_hwserial(self._section.get_str('SerialNum%s' % (self._index)))

    @property
    def scan_for_it(self):
        return self._section.get_bool('ScanForIt%s' % (self._index), False)

    @scan_for_it.setter
    def scan_for_it(self, val):
        self._section.set_bool('ScanForIt%s' % (self._index), bool(val))
        
    @property
    def use_ip_address(self):
        return self._section.get_bool('UseIPAddress%s' % (self._index), False)

    @use_ip_address.setter
    def use_ip_address(self, val):
        return self._section.set_bool('UseIPAddress%s' % (self._index), val)

    @property
    def ip_address(self):
        return self._section.get_str('IPAddress%s' % (self._index), '')

    @ip_address.setter
    def ip_address(self, val):
        return self._section.set_str('IPAddress%s' % (self._index), val)

class DAConfigList(list):
    def __init__(self):
        super(DAConfigList, self).__init__()
        from imgtec.lib.img_settings import ImgSettings
        self._settings = ImgSettings("Nail")
        for section_name in ['DashNG', 'NetworkData', 'Others']:
            section = self._settings.section(section_name)
            for key, value in sorted(section.items):
                serial = re.match('^SerialNum(\d+)$', key)
                if serial:
                    try:
                        da = DAConfig(section, serial.group(1))
                        da.serial
                    except ValueError:
                        pass
                    else:
                        self.append(da)
                    
    def add_da(self, serial, ip='', scan_for_it=True):
        da_type, index = probe_identifier.parse(serial)
        if da_type in ('DA-usb', 'DA-trace', 'DA-net'):
            section = self._settings.section('DashNG')
        elif da_type == 'Dash':
            section = self._settings.section('NetworkData')
        else:
            raise ValueError("Can't add DA of type %s because only real DAs can be added to DAConfig" % (da_type,))
        for n in itertools.count():
            key = section.get_str('SerialNum%d' % (n,))
            if key is None:
                break
        section.set_str('SerialNum%d' % (n,), probe_identifier.make_hwserial(serial))
        newda = DAConfig(section, n)
        newda.scan_for_it = scan_for_it
        newda.ip_address = ip
        newda.use_ip_address = bool(ip)
        self.append(newda)
        return newda

    def commit(self):
        # We should reindex all of the das first in case any of them have been 
        self._settings.commit()

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    lst = DAConfigList()
    for da in lst:
        print da
    lst.add_da('danet 99')
    for da in lst:
        print da
    