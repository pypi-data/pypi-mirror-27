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

import os.path, re
from imgtec.lib.img_settings.config import ConfigError

# based on IMG.program_settings

import_regex = re.compile("\s*#import\s+(.+)\s*")
comment_regex = re.compile("\s*(?:#(?!import)|;).*")

def is_comment(line) :
    """Determines if the given line is a comment

    >>> is_comment("#this is a comment")
    True
    >>> is_comment("this isn't")
    False
    >>> is_comment("#import this isn't either")
    False
    """
    return comment_regex.match(line) is not None

def is_section(line) :
    """Determines if the given line is a section
    i.e. of the form [section_name]"""
    
    line = line.strip()
    return len(line) != 0 and line[0] == '[' and line[len(line) - 1] == ']'

def extract_section(line) :
    "Extracts the section name"
    
    line = line.strip()
    return line[1 : len(line) - 1]

def extract_key(line) :
    """Extracts the key and value from a line of the form:
    key = value"""
    
    line = line.strip()
    idx = line.find('=')
    key = ""
    value = ""
    if idx != -1 :
        key = line[0 : idx]
        value = line[idx + 1 :]
    else :
        key = line
        value = ""

    return (key.strip(), value.strip())

def is_import(line) :
    """Determines if the current line is of the form:
    #import filename"""
    return import_regex.match(line) is not None

def extract_import(line) :
    "Extracts the filename from an import directive"
    
    match = import_regex.match(line)
    return match.group(1)

def expand_macros_impl(str, mapping) :
    """replace all occcurrences of %macro% with mapping['macro'].
    
    >>> expand_macros_impl('jake', {})
    'jake'
    >>> expand_macros_impl('%jake%', {'jake' : 'elwood'})
    'elwood'
    >>> expand_macros_impl('%jake% %jake', {'jake' : 'elwood'})
    'elwood %jake'
    >>> expand_macros_impl('%jake% %jake%', {'jake' : '%blues%', 'blues' : 'brothers'})
    'brothers brothers'
    """
    regexp = re.compile('(?:%([^%]+)%)')
    prev_str = None
    while prev_str != str :
        prev_str = str
        str = regexp.sub(lambda m : mapping[m.group(1)], str)
    return str

true_values = ("true", "yes", "y", "1", "0x1")
false_values = ("false", "no", "n", "0", "0x0")

class MemoryConfig(object):
    def __init__(self):
        self.sections = {}
        self.imported = []

    def make_section_parents(self, section_path):
        for i in xrange(1, len(section_path)):
            section_name = "/".join(section_path[:i])
            if section_name not in self.sections:
                self.sections[section_name] = {}

    def set_section(self, section_name, section):
        self.make_section_parents(section_name.split("/"))
        self.sections[section_name] = section

    def get_section(self, section_path):
        section_name = "/".join(section_path)
        section = self.sections.get(section_name)
        if section is None:
            section = {}
            self.set_section(section_name, section)
        return section

    def get_section_if_exists(self, section_path):
        return self.sections.get("/".join(section_path))

    def set_value(self, section_path, key, value):
        self.get_section(section_path)[key] = value
        
    def set_str(self, section_path, key, value):
        self.get_section(section_path)[key] = str(value)

    def set_bool(self, section_path, key, value):
        self.get_section(section_path)[key] = bool(value)

    def set_int(self, section_path, key, value):
        self.get_section(section_path)[key] = int(value)

    def get_str(self, section_path, key, default=None):
        section = self.get_section_if_exists(section_path)
        if section is None:
            return default
        return section.get(key, default)

    def get_value(self, section_path, key, default=None):
        value = self.get_str(section_path, key, default)
        if value is default:
            return default
        try:
            return int(value, 0)
        except (ValueError, TypeError):
            return value

    def get_int(self, section_path, key, default=None):
        value = self.get_value(section_path, key, default)
        if value is default or type(value) not in (int, long):
            return default
        return value

    def get_bool(self, section_path, key, default=None):
        value = self.get_str(section_path, key, default)
        if value is default:
            return default
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, long)):
            return value != 0
        if value.lower() in true_values:
            return True
        if value.lower() in false_values:
            return False
        return default

    def remove_key(self, section_path, key):
        section = self.get_section_if_exists(section_path)
        if section is not None and key in section:
            del section[key]

    def remove_all_keys(self, section_path):
        section = self.get_section_if_exists(section_path)
        if section is not None:
            self.sections["/".join(section_path)].clear()

    def remove_section(self, section_path):
        section_prefix = "/".join(section_path)
        if section_prefix in self.sections:
            del self.sections[section_prefix]
        if section_prefix:
            section_prefix += "/"
        for section_name in self.sections.keys():
            if section_name.startswith(section_prefix):
                del self.sections[section_name]

    def iter_sections(self, section_path):
        section_prefix = "/".join(section_path)
        if section_prefix:
            section_prefix += "/"
        count = len(section_path)
        for section_name in self.sections:
            if section_name and section_name.startswith(section_prefix) and section_name.count("/") == count:
                yield section_name[len(section_prefix):]

    def iter_keys(self, section_path):
        section = self.get_section_if_exists(section_path)
        if section is not None:
            return section.iteritems()
        else:
            return iter(())

    def commit(self):
        pass

def _read_settings(memconfig, filename):
    """ reads the settings from the file and stores as a dictionary
    of sections that are themselves dictionaries of keys and values"""
    try:
        with open(filename) as f:
            lines = f.readlines()
    except EnvironmentError as e:
        raise ConfigError(*e.args)
    _read_settings_from_lines(memconfig, lines, os.path.dirname(os.path.realpath(filename)))

def _read_settings_from_lines(config, lines, import_path):
    """reads the settings from the array of lines and applies them to a config."""
    current = ""
    section = config.sections.get(current, {})
    for line in lines:
        line = line.strip()
        if line and not is_comment(line):
            if is_section(line):
                config.set_section(current, section)
                current = extract_section(line)
                section = config.sections.get(current, {})
            elif is_import(line):
                config.set_section(current, section)
                import_filename = os.path.join(import_path, extract_import(line))
                config.imported.append(import_filename)
                _read_settings(config, import_filename)
            else:
                key, value = extract_key(line)
                section[key] = value
    if section:
        config.set_section(current, section)
        
def _write_settings(config, filename):
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    with open(filename, 'w') as out:
        for section_name, section in sorted(config.sections.items()):
            if section_name:
                out.write("[%s]\n" % (section_name,))
            for key, value in section.items():
                out.write("%s=%s\n" % (key, value))
            out.write("\n")
            
        

class IniConfig(MemoryConfig):
    def __init__(self, filename):
        super(IniConfig, self).__init__()
        try:
            _read_settings(self, filename)
        except ConfigError:
            pass
        self._filename = filename
        
    def commit(self):
        _write_settings(self, self._filename)
        
