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

import sys
import re

"""
interface ConfigImpl
    key : str
    section : [str]

    set_value(section, key, value)
    set_str(section, key, value)
    set_int(section, key, value)
    set_bool(section, key, value)
    get_value(section, key, default=None) -> (int | bool | str)
    get_str(section, key, default=None) -> value
    get_int(section, key, default=None) -> value
    get_bool(section, key, default=None) -> value
    remove_key(section, key)
    remove_all_keys(section)
    remove_section(section)
    iter_sections(section)
    iter_keys(section)
    commit()
"""

class ConfigError(Exception):
    pass

valid_chars = r"0-9A-Za-z !\"#$%&'()*+,-.:;<=>?@\[\]^_`{|}~"
key_re = re.compile(r"^[%s]+$" % valid_chars)
section_re = re.compile(r"^[%s]+(/[%s]+)*$" % (valid_chars, valid_chars))

def check_key_name(key):
    if not key_re.match(key):
        raise ConfigError("Invalid key name: '%s'" % key)

def check_section_name(section_name):
    if not section_re.match(section_name):
        raise ConfigError("Invalid section name: '%s'" % section_name)

class ConfigSection(object):
    def __init__(self, conf, section=()):
        self.__conf = conf
        self.__section = section

    def __repr__(self):
        return "ConfigSection(%r, %r)" % (self.__conf, self.__section)

    def name(self):
        return self.__section[-1] if self.__section else ""
    name = property(name)

    def get(self, key, default=None):
        check_key_name(key)
        return self.__conf.get_value(self.__section, key, default)

    def set(self, key, value):
        check_key_name(key)
        self.__conf.set_value(self.__section, key, value)

    def remove(self, key):
        check_key_name(key)
        self.__conf.remove_key(self.__section, key)

    def remove_all_keys(self):
        self.__conf.remove_all_keys(self.__section)

    def section(self, section):
        check_section_name(section)
        return ConfigSection(self.__conf, self.__section + tuple(section.split("/")))

    def remove_section(self, section=""):
        section_path = ()
        if section:
            check_section_name(section)
            section_path = tuple(section.split("/"))
        self.__conf.remove_section(self.__section + section_path)

    def keys(self):
        for key, value in self.__conf.iter_keys(self.__section):
            yield key
    keys = property(keys)

    def items(self):
        return self.__conf.iter_keys(self.__section)
    items = property(items)

    def sections(self):
        return (self.section(x) for x in self.__conf.iter_sections(self.__section))
    sections = property(sections)

    def get_list(self, fmt="%d", first=0):
        values = []
        i = first
        while True:
            value = self.get(fmt % i)
            if value is None:
                break
            values.append(value)
            i += 1
        return values

    def set_list(self, values, fmt="%d", first=0):
        self.remove_all_keys()
        for i, value in enumerate(values):
            self.set(fmt % (i+first), value)

    def get_str(self, key, default=None):
        check_key_name(key)
        return self.__conf.get_str(self.__section, key, default)

    def set_str(self, key, value):
        check_key_name(key)
        self.__conf.set_str(self.__section, key, value)

    def get_int(self, key, default=None):
        check_key_name(key)
        return self.__conf.get_int(self.__section, key, default)

    def set_int(self, key, value):
        check_key_name(key)
        self.__conf.set_int(self.__section, key, value)

    def get_bool(self, key, default=None):
        check_key_name(key)
        return self.__conf.get_bool(self.__section, key, default)

    def set_bool(self, key, value):
        check_key_name(key)
        self.__conf.set_bool(self.__section, key, value)
        
    def commit(self):
        self.__conf.commit()
