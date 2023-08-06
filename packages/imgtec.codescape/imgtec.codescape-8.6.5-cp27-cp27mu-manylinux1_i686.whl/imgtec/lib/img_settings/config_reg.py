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

from __future__ import with_statement
import _winreg as winreg
from imgtec.lib.img_settings.config import ConfigError
from config_ini import MemoryConfig

def is_int(x):
    return isinstance(x, (int, long))

class RegAccess(object):
    def __init__(self, rootkey, root):
        self.rootkey = rootkey
        self.root = root

    def open_key(self, section, sam=winreg.KEY_READ):
        return winreg.OpenKey(self.rootkey, "\\".join((self.root,) + section), 0, sam)

    def create_key(self, section):
        return winreg.CreateKey(self.rootkey, "\\".join((self.root,) + section))

    def set_value(self, section, key, value):
        if type(value) in (int, long, bool) and 0 <= value <= 0xFFFFFFFF:
            valtype = winreg.REG_DWORD
        elif type(value) == str and "\0" in value:
            valtype = winreg.REG_BINARY
        else:
            valtype = winreg.REG_SZ
        try:
            with self.create_key(section) as hkey:
                winreg.SetValueEx(hkey, key, 0, valtype, value)
        except WindowError, e:
            raise ConfigError(*e.args)

    def set_str(self, section, key, value):
        self.set_value(section, key, str(value))

    def set_bool(self, section, key, value):
        self.set_value(section, key, bool(value))

    set_int = set_value
    
    def _get_value_conversion(self, value, valtype):
        if valtype == winreg.REG_DWORD:
            return int(value)
        elif valtype == winreg.REG_BINARY:
            return value
        elif valtype == winreg.REG_SZ:
            return value
        return value
        
    def get_value(self, section, key, default=None):
        try:
            with self.open_key(section) as hkey:
                value, valtype = winreg.QueryValueEx(hkey, key)
            return self._get_value_conversion(value, valtype)
        except WindowsError:
            return default

    def get_str(self, section, key, default=None):
        value = self.get_value(section, key, default)
        if value is default:
            return default
        return str(value)

    def get_int(self, section, key, default=None):
        value = self.get_value(section, key, default)
        if value is default:
            return default
        return value if is_int(value) else default

    def get_bool(self, section, key, default=None):
        value = self.get_value(section, key, default)
        if value is default:
            return default
        return bool(value) if is_int(value) else default

    def remove_key(self, section, key):
        try:
            with self.open_key(section, winreg.KEY_WRITE) as hkey:
                winreg.DeleteValue(hkey, key)
        except WindowsError:
            pass

    def remove_all_keys(self, section):
        keys = [k for k, v in self.iter_keys(section)]
        [self.remove_key(section, key) for key in keys]

    def remove_section(self, section):
        # _winreg doesn't have DeleteTree() ...
        self.remove_all_sections(section)
        self.remove_all_keys(section)
        parent = section[:-1]
        with self.open_key(parent, winreg.KEY_WRITE) as hparent:
            winreg.DeleteKey(hparent, section[-1])
                
    def remove_all_sections(self, section):
        subsections = list(self.iter_sections(section))
        for subsection in subsections:
            self.remove_section(section + (subsection,))

    def iter_sections(self, section):
        try:
            with self.open_key(section) as hkey:
                num = winreg.QueryInfoKey(hkey)[0]
                for i in xrange(num):
                    yield winreg.EnumKey(hkey, i)
        except WindowsError:
            pass

    def iter_keys(self, section):
        try:
            with self.open_key(section) as hkey:
                num = winreg.QueryInfoKey(hkey)[1]
                for i in xrange(num):
                    key, value, valtype = winreg.EnumValue(hkey, i)
                    if key:
                        yield key, self._get_value_conversion(value, valtype)
        except WindowsError:
            pass

    def commit(self):
        pass
        
def __read_registry(reg, config, sections):
    current = ''
    for key, value in reg.iter_keys(sections):
        config.set_value(sections, key, value)
    for section in reg.iter_sections(sections):
        __read_registry(reg, config, sections + (section,))

def _read_registry(config, rootkey, root):
    reg = RegAccess(rootkey, root)
    __read_registry(reg, config, tuple())
    
def _calculate_removes_and_writes(olddict, newdict):
    """Return a set of operations that will convert olddict into newdict.
    
    Specifically it returns (removes, writes) where removes is a list of keys 
    in olddict not in newdict, and writes is a dict of key->value for values 
    that are in newdict but not in old dict OR newdict[key] != olddict[key].
    
    Or to put it another way ::
        
    >>> olddict = dict(a=1, b=2, c=None)
    >>> newdict = dict(     b=2, c=4, d=5, e=None)
    >>> removes, writes = _calculate_removes_and_writes(olddict, newdict)
    >>> for k in removes:
    ...    del olddict[k]
    >>> olddict.update(writes)
    >>> olddict == newdict
    True
    >>> list(removes)
    ['a']
    >>> sorted(writes.items())
    [('c', 4), ('d', 5), ('e', None)]
    """
    r = frozenset(olddict) - frozenset(newdict)
    get = olddict.get
    w = dict((k, v) for k, v in newdict.iteritems() if get(k, Ellipsis) != v)
    return r, w
    
def __write_registry(reg, config, sections):
    current = ''
    reg_keys = dict(reg.iter_keys(sections))
    cfg_keys = dict(config.iter_keys(sections))
    
    removes, writes = _calculate_removes_and_writes(reg_keys, cfg_keys)
    
    for k in removes:
        reg.remove_key(sections, k)
    for k, v in writes.iteritems():
        reg.set_value(sections, k, v)
        
    newsections = set(config.iter_sections(sections))
    regsections = set(reg.iter_sections(sections))
    sections_to_remove = regsections - newsections
    for s in sections_to_remove:
        reg.remove_section(sections + (s,))
    for s in newsections:
        __write_registry(reg, config, sections + (s,))

def _write_registry(config, rootkey, root):
    reg = RegAccess(rootkey, root)
    __write_registry(reg, config, tuple())
        
                
class RegConfig(MemoryConfig):
    def __init__(self, rootkey, root):
        super(RegConfig, self).__init__()
        _read_registry(self, rootkey, root)
        self._rootkey = rootkey
        self._root = root
        
    def commit(self):
        _write_registry(self, self._rootkey, self._root)
        
