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

from imgtec.test import *
import errno
import io
import itertools
import operator
import os
import re
import sys
import traceback
from xml.etree import ElementTree as etree
from pprint import pformat
from copy import deepcopy
from imgtec.console.support import *
from imgtec.console.regdb_types import *
from imgtec.console import regdb_parse_cache
from imgtec.console.results import *
from imgtec.lib import get_user_files_dir
from imgtec.lib.namedenum import namedenum
from imgtec.lib import namedbitfield

imgns = 'http://www.mips.com/registers/1.0'

def dom_from_string(contents):
    io_contents = io.BytesIO(contents)
    xml = etree.parse(io_contents)
    root = xml.getroot()
    return root

def dom_from_file(filename):
    contents = open(filename, 'r').read()
    return dom_from_string(contents)
    
def pretty_format_xml(s):
    r'''Format some xml, try to irrelevant whitespace as far as possible.
    
    >>> pretty_format_xml('<x> <a> <b><c/></b></a></x>')
    '<?xml version="1.0" encoding="utf-8"?>\n<x>\n  <a>\n    <b>\n      <c/>\n    </b>\n  </a>\n</x>\n'
    '''
    import xml.dom.minidom as dom
    xml = dom.parseString(s)
    def removews(node):
        if node.nodeType == node.TEXT_NODE and node.data.strip() == '':
            return node # mark for removal
        to_remove = [removews(child) for child in node.childNodes]
        for x in to_remove:
            if x:
                node.removeChild(x) 
                
    pxml = xml.toprettyxml('  ', encoding='utf-8')
    pxml = '\n'.join([line for line in pxml.split('\n') if line.strip()]) + '\n'
    return pxml
    
def dom_as_string(dom, pretty_print=True):
    lines = [
        "<?xml version='1.0' encoding='utf-8'?>\n",
        '<!-- - - - - - - - - - - - - - - - - - - - - - - - - - - -->',
        '<!-- Board Support Package Config                        -->',
        '<!-- Copyright Imagination Technologies Ltd              -->',
        '<!-- - - - - - - - - - - - - - - - - - - - - - - - - - - -->',
        etree.tostring(dom)
    ]
    s = ''.join(lines)
    if pretty_print:        
        s = pretty_format_xml(s)
    return s

def dom_to_file(filename, dom, verbose=1):
    if verbose:
        print "Writing to", filename
    with open(filename, 'w+') as output_file:
        output_file.write(dom_as_string(dom, pretty_print=True))
        
def dom_to_python_file(filename, regdb_location=None):
    parse_cache = get_parse_cache(regdb_location)
    cached_attributes = ['conditions', 'templates', 'arches']
    with open(filename, 'w') as output_file:
        output_file.write('from imgtec.console.regdb_types import *\n')
        for attr in cached_attributes:
            output_file.write(attr + '=')
            output_file.write(pformat(getattr(parse_cache, attr)))
            output_file.write('\n')


def is_comment(node):
    return node.tag == etree.Comment

def _qual_name(namespace, tag):
    return '{%s}%s' % (namespace, tag)

def return_all(_node):
    return True

class TagNameIs(object):
    def __init__(self, tag_name, namespace):
        self.tag_name = _qual_name(namespace, tag_name)
    def __call__(self, node):
        return node.tag == self.tag_name
        
class TagNameIsOneOf(object):
    def __init__(self, tag_names, namespace):
        self.tags = [_qual_name(namespace, tag) for tag in tag_names]
    def __call__(self, node):
        return any([node.tag == tag for tag in self.tags])

def iterate_children(dom, predicate=return_all):
    for child in dom:
        if predicate(child):
            yield child

def iterate_children_recursive(dom, predicate=return_all):
    for child in dom:
        if predicate(child):
            yield child
        for grandchild in iterate_children_recursive(child, predicate):
            yield grandchild

def get_first_child_with_tag(dom, tag, namespace):
    for element in iterate_children(dom, TagNameIs(tag, namespace)):
        return element

def get_first_child(dom):
    for element in iterate_children(dom):
        return element

def extract_child_node_elements(parent, tag, namespace):
    return [extract_node_attributes(child) for child in iterate_children(parent, TagNameIs(tag, namespace))]


_gcr_prefixes = dict(
    GCR_GLOBAL='gcr_',
    GCR_GLOBAL_DEBUG='gcr_db_',
    GCR_CORE_LOCAL='gcr_cl_',
    CPC_GLOBAL = 'cpc_',
    CPC_LOCAL = 'cpc_cl_',
    GIC_SHARED='gic_',
    GIC_CLOCAL='gic_vl_',
)
_cpc_bindings = {
    'cpc1.0.0':'fir',
    'cpc1.25.0':'fccr',
    'cpc1.26.0':'fexr',
    'cpc1.28.0':'fenr',
    'cpc1.31.0':'fcsr',
}

def _get_comms_name(reg, default=None):
    '''Get suitable comms name from details, or `default` if the comms can't read it.

    >>> _get_comms_name({'id':'a'})
    >>> _get_comms_name({'id':'a'}, 'wobble')
    'wobble'
    >>> _get_comms_name({'id':'a', 'name':'a (view0)'}, 'wobble')
    'a'
    >>> _get_comms_name({'id':'bob', 'da_name':'ejtag_bob'})
    'ejtag_bob'
    >>> _get_comms_name({'id':'Config', 'cp_number':'0', 'cp_index':'16', 'cp_select':'0'})
    'cp0.16.0'
    >>> _get_comms_name({'id':'d16', 'cp_number':'1', 'cp_index':'16', 'cp_select':'0'})
    'd16'
    >>> _get_comms_name({'id':'f16', 'cp_number':'1', 'cp_index':'16', 'cp_select':'0'})
    'f16'
    >>> _get_comms_name({'id':'whocares', 'cp_number':'1', 'cp_index':'31', 'cp_select':'0', 'control':'true'})
    'fcsr'
    >>> _get_comms_name({'id':'r14', 'name':'zero', 'number':'14'})
    >>> _get_comms_name({'base':"GCR_GLOBAL_DEBUG", 'offset':"0x0100"})
    'gcr_db_0100'
    '''
    try:
        return reg['da_name'].lower()
    except KeyError:
        pass
    try:
        cp_number = int(reg['cp_number'])
        cp_index = int(reg['cp_index'])
        cp_select = int(reg['cp_select'])
        control = 'c' if reg.get('control', 'false').lower() == 'true' else ''
        if re.match(r'([fd]\d+)$', reg['id'], flags=re.I):
            return reg['id'].lower()
        # The underlying comms doesn't know how to read cp control registers, so
        # map them here. TODO add support in Tiny for cpC#N (0, 1 and 2)
        name = 'cp%s%d.%d.%d' % (control, cp_number, cp_index, cp_select)
        return _cpc_bindings.get(name, name)
    except KeyError:
        pass
    try:
        prefix = _gcr_prefixes[reg['base']]
        offset = int(reg.get('offset', '0'), 0)
        return '%s%04x' % (prefix, offset)
    except KeyError:
        pass
    if re.match(r'r\d+$', reg['id']):
        return None # r0-31 adds no value and results in bogus ABI name lookups 
    try:
        return reg['name'].split(None, 1)[0]
    except KeyError:
        pass
    return default


def _get_register_size(regtype, details):
    '''Reg size is stored in regdb in various ways, convert to a single size. 
    
    >>> _get_register_size('cop', {'cp_size':'64', 'id':'a'})
    64
    >>> _get_register_size('mm', {'datasize':'4', 'id':'a'})
    a: Ignoring datasize(4)!=accesssize(8)
    32
    >>> _get_register_size('mm', {'accesssize':'8', 'id':'a'})
    64
    >>> _get_register_size('gpr', {'at':'32', 'id':'a'})
    32
    >>> _get_register_size('gpr', {'at':'64', 'id':'a'})
    64
    >>> _get_register_size('gpr', {'id':'a'})
    32
    '''
    size = None
    if regtype == 'cop':
        size = int(details.get('cp_size', '32'), 0)
    elif regtype == 'gpr':
        # Strictly speaking for hi/lo regs this will return the wrong size because
        # they have no 'at' field and they ought to match the arch size, but
        # I'm fairly sure this isn't going to cause a problem
        size = int(details.get('at','32'), 0) 
    elif regtype == 'mm':
        size = int(details.get('datasize', '8'), 0)
        accesssize = int(details.get('accesssize', '8'), 0)
        if accesssize != size:
            print '%s: Ignoring datasize(%d)!=accesssize(%d)' % (details['id'], size, accesssize)
        size *= 8
    return size
    
# Just for reference, we ignore the following fields in the regdb xml:
_ignore_fields = '''
 unit_name  zerovalue requires ar default tooltip reg_block altname format per_tc
 do_not_rediscover mdu number
'''.split()


def _get_procs_data(register_element, register_details, templates):
    for template_tag in ['global_field_template', 'proc_field_template']:
        template_name = register_details.get(template_tag)
        if template_name:
            if template_name not in templates:
                print 'Warning, register %s references a non-existent template: %s' % (register_details['id'], template_name)
                return
            return template_name
    
    return parse_procs(register_element)
        

def parse_regdb(dom, templates):
    '''Parse the regdb and convert to a dict or arch(at->[list of registers]).'''
    tagnames=['cop_register', 'mm_register', 'gpr_register']
    arches = {'32':[], '64':[], 'any':[]}
    for register in iterate_children_recursive(dom, TagNameIsOneOf(tagnames, imgns)):
        register_details = extract_node_attributes(register)
        regtype = register.tag.replace('{' + imgns + '}', '').replace('_register', '')
        condition = _get_condition_from_details(register, register_details)
        procs_data = _get_procs_data(register, register_details, templates)
        size = _get_register_size(regtype, register_details)
        at = register_details.get('at', 'any')
        comms_name = _get_comms_name(register_details)
        name = register_details.get('name', '')
        id_ = register_details['id']
        if comms_name:
            name       = '' if name == id_ else name
            comms_name = '' if comms_name == id_ else comms_name                
            try:
                reg = Register(id_, comms_name, name, 
                    procs_data=procs_data,
                    description=register_details.get('desc', ''),
                    size=size,
                    condition=condition,
                    rwflag=register_details.get('rwflag', 'rw'),                    
                )
                arches[at].append(reg)
            except KeyError:
                print 'Unknown architecture %s for register %s' % (at, id_)
    return arches
        
def parse_registers(parse_cache, cpu_info, eval_env, verbose=0, explain=None):
    '''Get a list of valid Register instances for this cpu/arch, filter fields, 
    and check conditions.'''        
    arch = '32' if cpu_info.get('cpu_is_32bit', True) else '64'
    cpu_name = cpu_info.get('cpu_name', '')
    seen = set()
    # look in our own arch first, then the generic arch
    registers = []
    arches = parse_cache.arches
    
    for reg in itertools.chain(arches[arch], arches['any']):
        register_id = reg.id
        if register_id in seen: # already seen this (in the more specific arch)
            continue
        seen.add(register_id)
            
        procs_data = reg.procs_data
        if isinstance(procs_data, basestring):
            procs_data = parse_cache.templates[procs_data]
            
        fields = procs_data.get('', [])
        # TODO fix this dict order dependency
        for proc_patterns, proc_fields in procs_data.iteritems():
            if proc_patterns: # skip 'default' or '' as it is now known
                for proc_pattern in proc_patterns.split(','):
                    regex = re.compile(proc_pattern, flags=re.IGNORECASE)
                    if regex.match(cpu_name):
                        fields = proc_fields
                        break
        
                
        filtered_fields = []
        for field in fields:
            if field.proc:
                regex = re.compile(field.proc.replace(',','|'), flags=re.IGNORECASE)
                if not regex.match(cpu_name):
                    continue
            filtered_fields.append(field)
                
        reg = reg._replace(fields=filtered_fields, procs_data=None)
        registers.append(reg)
        eval_env.add_register(reg)
    
    #Conditions can rely on register's fields so they must be evaluated after we've gone through all the regs.
    valid = []
    explain = explain and explain.lower()
    for reg in registers:
        explain_this = explain and ((reg.id and reg.id.lower() == explain) or (reg.name and reg.name.lower() == explain))
        if explain_this: print '  condition:', repr(reg.condition)
        try:
            eval_condition = evaluate(reg.condition, eval_env)
        except RegisterUnreadable:
            # If we weren't allowed to read the register then
            # assume the register exists.
            if verbose > 1 or explain_this:
                print '%s is being treated as existing because we were told not to read any registers'
            eval_condition = True
        except RegisterPrerequisiteDoesNotExist as e:
            eval_condition  = False
            if verbose > 1 or explain_this:
                print "%s does not exist because one or more prerequisites do not exist:\n  %s" % (reg.display_name, e)
        except Exception as e:
            # Treat any other error as a failure
            eval_condition  = False
            if verbose or explain_this:
                print "Warning, failed to read a register : %s" % (e,)
        if explain_this: print '  condition->', eval_condition
            
        if eval_condition:
            valid.append(reg)
    return valid

def _get_static_bsp_items(dom):
    conditions = {}
    templates = {}
    
    tags = [(_qual_name(imgns, 'condition'), conditions, parse_condition),
            (_qual_name(imgns, 'global_field_template'), templates, parse_procs),
            (_qual_name(imgns, 'proc_field_template'), templates, parse_procs)]

    for item in iterate_children_recursive(dom):   
        for tag, container, parser in tags:
            if item.tag == tag:
                id_ = item.get('id')
                if id_ in container:
                    print 'Warning, ID %s already exists'
                container[id_] = parser(item)
                
    arches = parse_regdb(dom, templates)                
    return conditions, arches, templates
    
class RegDBParseCacheBase(object):
    def __init__(self):
        self._conditions, self._arches = None, None
        
    @property
    def conditions(self):
        self.load()
        return self._conditions
        
    @property
    def arches(self):
        self.load()
        return self._arches
        
    @property
    def templates(self):
        self.load()
        return self._templates
    
    def load(self):
        if self._conditions is None or self._arches is None:
            self._conditions, self._arches, self._templates = _get_static_bsp_items(self.dom)
        
class RegDBParseCacheFromDOM(RegDBParseCacheBase):
    def __init__(self, dom):
        super(RegDBParseCacheFromDOM, self).__init__()
        self.dom = dom
    
def parse_as_list(parse_cache, cpu_info, register_reader, verbose=0, explain=None):
    env = EvaluationEnvironment(
        cpu_name = cpu_info.get('cpu_name', 'default'),
        register_reader = register_reader,
        conditions = parse_cache.conditions,
        verbose = verbose,
    )
    return parse_registers(parse_cache, cpu_info, env, verbose=verbose, explain=explain)

def unintrusive_parse(cpu_info):        
    '''Get the registers without a target, only the contents of cpu_info.'''
    registers = parse_as_list(get_parse_cache(None), cpu_info, NullRegisterReader())
    return dict([(r.id, r) for r in registers if r.comms_name.startswith('cp0.')])
    
def parse_bits(bits):
    if ':' in bits:
        start, end = bits.split(':')
        start, end = int(start), int(end)
        return Bits(start, end) if start != end else Bits(start)
    else:
        return Bits(int(bits))

def add_node_with_text(parent, name, text, **element_attributes):
    element = etree.SubElement(parent, name, **element_attributes)
    element.text = text
    return element
    
def add_description(element, thing):            
    if thing.description:
        add_node_with_text(element, 'd', format_description(thing.description))
        
def _add_registers_to_hd_tree(module_element, registers, filter, excludes):
    sorted_registers = sorted(registers, key=operator.attrgetter('display_name'))
    filter = re.compile(filter)
    
    for reg in sorted_registers:
        # HACK: Ignore FPU - These are 64bit values and we fall over
        #TODO do ejtag/DRSEG/GCR registers, the problem is that simulators don't have them
        if reg.comms_name is None or not filter.match(reg.comms_name) or reg.comms_name in excludes:
            continue
        
        register_element = etree.SubElement(module_element, 'r', N=make_cpp_variable_name(reg.display_name))
        add_node_with_text(register_element, 's', '$' + reg.comms_name)
            
        quad = reg.size > 32
        if quad:
            etree.SubElement(register_element, 'sq')
        
        rw = getattr(reg, 'rwflag', 'rw')
            
        if rw not in ('r', 'rw'):
            raise Exception('Unknown read/write flag: %s' % rw)
        if rw == 'r':
            etree.SubElement(register_element, 'ro')

        field_names = set()
        fields = sorted(reg.fields, key=operator.attrgetter('bits'), reverse=True)
        for field in fields:
            variable_name = make_cpp_variable_name(field.name, field_names)
            field_names.add(variable_name)
            field_element = etree.SubElement(register_element, 'f', N=variable_name)

            add_node_with_text(field_element, 'fm', '0x%x' % (field.bits.mask,))
            if field.bits.end != 0:
                add_node_with_text(field_element, 'rs', str(field.bits.end))

            value_format = '0x%0' + ('%d' % ((field.bits.num_bits+3)//4,)) + 'x'
            previous_names = []
            for value in field.values:
                name = make_cpp_variable_name(value.name, previous_names)
                previous_names.append(name)
                value_element = etree.SubElement(field_element, 'v', N=name)                
                etree.SubElement(value_element, 'x').text = value_format % (value.value,)
                add_description(value_element, value)
            add_description(field_element, field)
        add_description(register_element, reg)
    
def build_img_bsp_xml(registers, cpu_info, probe_type, include_memory_types_and_ranges):
    root = etree.Element('ioconfig')
    
    p = etree.SubElement(root, 'p', N='/.*/i')
    
    module_info = [
        ('COP_REGISTERS', r'cp0\..*', []),
    ]
    
    if probe_type.lower() == 'sysprobe':
        module_info.append((
            'GCR_REGISTERS',
            r'gcr_.*',
            []
        ))
        
        # other_excludes = [
            # 'ejtag_dcr', 

            # 'a0', 'a1', 'a2', 'a3', 'gp', 'k0', 'k1', 'ra', 's0', 's1', 's2', 's3', 
            # 's4', 's5', 's6', 's7', 's8', 'sp', 't0', 't1', 't2', 't3', 't4', 't5', 
            # 't6', 't7', 't8', 't9', 'v0', 'v1',
            
            # 'fp',
            
            # 'fccr', 'fcsr', 'fenr', 'fexr', 'fir',
        # ]
        # other_excludes.extend(['f%d' % i for i in range(32)])
        # other_excludes.extend(['d%d' % i for i in range(32)])
        # other_excludes.extend(['r%d' % i for i in range(32)])
        
        # module_info.append((
            # 'OTHER_REGISTERS',
            # r'^(?!(cp0\.)|(gcr_.*)).*',
            # other_excludes
        # ))
    
    for N, filter, excludes in module_info:
        m = etree.Element('m', N=N)
        _add_registers_to_hd_tree(m, registers, filter, excludes)

        if len(m): # specifically using len here
            p.append(m)

            if cpu_info['has_vze'] and N == 'COP_REGISTERS':
                m = deepcopy(m)
                m.set('N', 'GUEST_' + m.get('N'))

                for reg in m:
                    reg.set('N', 'guest_' + reg.get('N'))
                    reg.getchildren()[0].text = reg.getchildren()[0].text.replace('$', '$guest_')
                    
                p.append(m)
            
    if include_memory_types_and_ranges:
        mt = etree.SubElement(p, 'mt', N='cp')
        add_node_with_text(mt, 'mtv', '0x3')

        mt = etree.SubElement(p, 'mt', N='Ram')
        add_node_with_text(mt, 'mtv', '0x0')
        etree.SubElement(mt, 'static')

        is_64bit_cpu = not cpu_info.get('cpu_is_32bit', True)

        def add_mb(parent, name, start, end, description, cacheable=False):
            mb = etree.SubElement(parent, 'mb', N=name)
            to_hex = '0x%016x' if is_64bit_cpu else'0x%08x'
            add_node_with_text(mb, 's', to_hex % (start,))
            add_node_with_text(mb, 'en', to_hex % (end,))
            etree.SubElement(mb, 'sd')
            if cacheable:
                etree.SubElement(mb, 'cacheable')
            add_node_with_text(mb, 'd', description)

        se = sign_extend_32_to_64 if is_64bit_cpu else lambda x: x
        add_mb(mt, 'useg',  se(0x00000000), se(0x7fffffff), 'User Mapped Segment', cacheable=True)
        if is_64bit_cpu:
            add_mb(mt, 'xuseg',  0x80000000, 0xffffffff7fffffff, 'User Mapped Segment', cacheable=True)
        add_mb(mt, 'kseg0', se(0x80000000), se(0x9fffffff), 'Kernel Unmapped Segment', cacheable=True)
        add_mb(mt, 'kseg1', se(0xa0000000), se(0xbfffffff), 'Kernel Unmapped Uncached Segment')
        add_mb(mt, 'kseg2', se(0xc0000000), se(0xdfffffff), 'Supervisor Mapped Segment')
        add_mb(mt, 'kseg3', se(0xe0000000), se(0xffffffff), 'Kernel Mapped Segment')
    
    return root
    
def _read_core_id(reader):
    return reader.get_register_value('cp0.15.0') & 0x00ffff00
    
def build_core_id_tree(reader, core_name, xml_filename):
    core_id = _read_core_id(reader)
    root = etree.Element('ioconfig')    
    core_id_node = etree.SubElement(root, 'CoreID', N='MIPS:%s' % core_name)
    add_node_with_text(core_id_node, 'CoreIDValue', '0x%08x' % core_id)
    add_node_with_text(core_id_node, 'src', xml_filename)
    return root
    
def extract_node_attributes(node):
    return dict((key, node.get(key)) for key in node.keys())

class EvaluationEnvironment(object):
    def __init__(self, cpu_name='', conditions=None, register_reader=None, verbose=False):
        self.conditions = {} if conditions is None else conditions
        self.register_reader = register_reader or RegisterReaderPrecalculatedRegisters()
        self.cpu_name = cpu_name
        self.constants = {}
        self.register_field_aliases = {} # not used at present, remove in a future refactor
        self.registers = {}
        self.verbose = verbose
        self._printed = set()

    def add_constant(self, constant, value):
        self.constants[constant] = value
        
    def add_register(self, register):
        self.registers[register.id.lower()] = register
        
    def read_register(self, register, field):
        try:
            what = (register.display_name + '.' + field.name) if field else register.display_name
            val =  self.register_reader.get_register_value(register.comms_name)
            if self.verbose > 1 and what not in self._printed:
                if field:
                    print "Read %s for field %s(0x%x) == 0x%08x(%s==0x%x)" % (
                        register.display_name, field.name, field.bits.mask, val, field.name, val & field.bits.mask)
                else:
                    print "Read %s == 0x%08x" % (register.display_name, val)
                self._printed.add(what)
            return val
        except RegisterUnreadable as e:
            raise
        except Exception as e:
            if verbose:
                if field:       
                    print "Failed to read %s for field %s : %s" % (register.display_name, field.name, e)
                else:
                    print "Failed to read %s : %s" % (register.display_name, e)
            raise

    def get_register_and_field(self, register_and_field):
        try:
            try:
                regid, fieldname = register_and_field.split('::')
            except ValueError:
                regid, fieldname = register_and_field, ''
            reg = self.registers[regid.lower()]
        except KeyError:
            raise RegisterAccessError('Register %s is not defined' % regid)

        if self and not evaluate(reg.condition, self):
            raise RegisterPrerequisiteDoesNotExist('%s condition %r evaluated as False' % (register_and_field, reg.condition))

        if fieldname:
            fields = [f for f in reg.fields if f.name.lower() == fieldname.lower()]
            if not fields:
                raise RegisterPrerequisiteDoesNotExist('%s has no field %s' % (regid, fieldname))
            if len(fields) > 1:
                raise RegisterAccessError('Register with ID %s field %s is ambiguous' % (regid, fieldname))
            field = fields[0]
        else:
            field = None
        return reg, field
        

class ParseError(Exception):
    pass

def parse_condition_value(value):
    """
    >>> parse_condition_value('')
    Traceback (most recent call last):
    ...
    ParseError: Cannot parse ""
    >>> parse_condition_value('% 5 == 2')
    Traceback (most recent call last):
    ...
    ParseError: Cannot parse "% 5 == 2"
    >>> parse_condition_value('true')
    ('==', True)
    >>> parse_condition_value('set')
    ('==', True)
    >>> parse_condition_value('false')
    ('==', False)
    >>> parse_condition_value('==1')
    ('==', 1)
    >>> parse_condition_value(' == 1')
    ('==', 1)
    >>> parse_condition_value('gt 1')
    ('gt', 1)
    >>> parse_condition_value('gte 1')
    ('gte', 1)
    >>> parse_condition_value('lt 8')
    ('lt', 8)
    >>> parse_condition_value('lte 1')
    ('lte', 1)
    >>> parse_condition_value('and 0x8000')
    ('and', 32768)
    >>> parse_condition_value(' != 0x1234')
    ('!=', 4660)
    >>> parse_condition_value('lt RegEditTest::K')
    ('lt', Reg('RegEditTest::K'))

    """
    regex = r'\s*(?P<op>and|!=|==|gt|gte|lte|lt)?\s*(?P<value_str>true|false|set|\d+|0x[\da-fA-F]+|[A-Za-z\:]+)\s*$'
    match = re.match(regex, value)
    if match:
        value = match.group('value_str').lower()
        if value in ('true', 'set'):
            value = True
        elif value == 'false':
            value = False
        else:
            try:
                value = int(match.group('value_str'), 0)
            except ValueError:
                value = Reg(match.group('value_str'))
        return (match.group('op') or '=='), value
    raise ParseError('Cannot parse "%s"' % value)

def _parse_condition_value(value):
    if value == '=0': # TODO: Hack. This may be corrupt data in the XML file
        value = '==0'
    return parse_condition_value(value)

def _parse_check(checking_if):
    conditions = extract_node_attributes(checking_if)
    if 'cpu_name_matches' in conditions:
        return CPUNameMatches(conditions['cpu_name_matches'])
    if 'is' in conditions:
        op, value = _parse_condition_value(conditions['is'])
        if 'value_of' in conditions:
            return Op(op, Reg(conditions['value_of']), value)
        if 'condition' in conditions:
            return Op(op, Condition(conditions['condition']), value)
    if 'write_enabled' in conditions:
        return False
    raise ParseError('Unable to parse %s' % conditions)

def _build_expression(node):
    is_and = TagNameIs('and', imgns)
    is_or = TagNameIs('or', imgns)
    is_not = TagNameIs('not', imgns)
    is_checking = TagNameIs('checking_if', imgns)

    if node is None:
        return True
    elif is_comment(node):
        return
    elif is_checking(node):
        return _parse_check(node)
    else:
        result = [_build_expression(x) for x in iterate_children(node)]
        result = [x for x in result if x is not None]
        if is_and(node):
            return And(*result)
        elif is_or(node):
            return Or(*result)
        elif is_not(node):
            return Not(*result)

    raise ParseError('Unable to parse %s' % node)

def parse_condition(condition):
    details = extract_node_attributes(condition)
    return _get_condition_from_details(condition, details)
    
def _get_condition_from_details(condition, details):
    conditions = []
    try:
        conditions.append(CPUNameMatches(details['proc']))
    except KeyError:
        pass
    try:
        conditions.append(Condition(details['discover_using']))
    except KeyError:
        pass
    discover_by = get_first_child_with_tag(condition, 'discover_by', imgns)
    if discover_by is not None:
        conditions.append(_build_expression(get_first_child(discover_by)))
        
    if not conditions:
        return True
    elif len(conditions) == 1:
        return conditions[0]
    else:
        return And(*conditions)
   
def parse_value(value):
    '''Convert a value dict from regdb into a Value namedtuple, no name 
    disambiguation is done at this point.

    >>> values = [dict(id='val0', value='0', desc='v0'), dict(id='val11', value='0x11', desc='v11')]
    >>> parse_value(values[0])
    Value('val0', 0, 'v0')
    >>> parse_value(values[1])
    Value('val11', 17, 'v11')
    >>> parse_value(values[1])
    Value('val11', 17, 'v11')
    >>> parse_value({'id':'id', 'value':'1', 'reserved':'true'})
    Value('id', 1, '', True)
    '''
    name  = value['id']
    val = int(value['value'], 0)
    reserved = value.get('reserved', 'false') in ('true', '1')
    return Value(name, val, value.get('desc', ''), reserved)
            
def parse_field(details, values):
    '''Convert a field dict from regdb into a Field namedtuple.'''
    bits = parse_bits(details.get('bits', '0'))
    try:
        xlt_bits = parse_bits(details['xlt_bits'])
    except KeyError:
        xlt_bits = None
    values = [parse_value(value) for value in values]
    return Field(details['id'], bits, details.get('desc', ''),
                 values, xlt_bits, details.get('proc'))

def parse_fields(parent):
    fields = []
    for field in iterate_children(parent, TagNameIs('field', imgns)):
        field_data = extract_node_attributes(field)
        values = extract_child_node_elements(field, 'field_value', imgns)
        fields.append(parse_field(field_data, values))
    return fields
    
def parse_procs(parent):
    procs = {}
    allprocs = list(iterate_children(parent, TagNameIs('proc', imgns)))
    
    if allprocs:
        for proc in allprocs:
            proc_names = [x.strip() for x in proc.get('list').split(',')]
            parsed = parse_fields(proc)
            if 'default' in proc_names:  # so it is findable in the dict easily
                procs[''] = parsed
            nondefaults = ','.join(x for x in proc_names if x != 'default')
            if nondefaults:
                procs[nondefaults] = parsed
    else:
        fields = parse_fields(parent)
        if fields:
            procs[''] = fields 
    return procs

class RegisterReaderPrecalculatedRegisters(object):
    def __init__(self, register_values=None):
        if register_values is None:
            register_values = {}
        from imgtec.console.reginfo import normalise_name
        self.register_values = dict([(normalise_name('o32', k),v)for k,v in register_values.items()])

    def get_register_value(self, register):
        try:
            from imgtec.console.reginfo import normalise_name
            return self.register_values[normalise_name('o32', register)]
        except KeyError:
            #print 'Failed to find %s(%s) in %r' % (register, normalise_name('o32', register), self.register_values)
            raise
        
def core_name_from_simulator_name(simulator_name):
    '''Extract the root core name, ignoring groups and endian.
    
    >>> core_name_from_simulator_name('Simulator RPUSim')
    >>> core_name_from_simulator_name('Simulator IAsim-M5100_M5100-BE')
    'M5100'
    '''
    pattern = 'Simulator IAsim-((?=[^ _]+_)([^ _]*_)|())(?P<name>[^ ]+)[ -](?P<endian>[BL]E)'
    match = re.match(pattern, simulator_name)
    return match and match.group('name')
        
        
def write_register_values(cores, identifier_names, regdb_location=None):
    from imgtec.console.reginfo import normalise_name
    from imgtec.console.generic_device import device
    seen_prids = {}
    parse_cache = get_parse_cache(regdb_location)
    for identifier, core in identifier_names:
        print 'Reading registers from %s (core name == %s)' %(identifier, core)
        try:
            from imgtec.console import probe, cpuinfo
            probe(identifier)
            reader = RegisterReaderCodescapeConsole(device())
            if not core:
                core = cpuinfo()['cpu_name']
                print '..using core name', core
            convert_to_hd_dom(parse_cache, cpuinfo(), reader)
            _read_core_id(reader)
        except Exception:
            traceback.print_exc()
        else:
            regs = reader.cache
            prid = regs['cp0.15.0']
            try:
                print 'Skipping %s as it shares prid 0x%08x with %s' % (core, prid, seen_prids[prid])
            except KeyError:
                seen_prids[prid] = core
                cores[core] = {normalise_name(device().abi, name):value for name, value in regs.items()}

def get_unique_simulators():
    from imgtec.console import simulators
    seen, sims = set(), []
    for sim in sorted(simulators()):
        name = core_name_from_simulator_name(sim)
        if name and name not in seen and not name.startswith('M14K'):
            sims.append((sim, name))
            seen.add(name)
    return sims        

def convert_to_hd_dom(parse_cache, cpu_info, reader, probe_type='', include_memory_types_and_ranges=True, verbose=False, explain=None):
    regs = parse_as_list(parse_cache, cpu_info, reader, verbose=verbose, explain=explain)
    return build_img_bsp_xml(regs, cpu_info, probe_type, include_memory_types_and_ranges)

def build_dom(regdb_location):
    print 'reading', regdb_location
    xml_paths = []

    for location, folders, files in os.walk(regdb_location):
        if not os.path.split(location)[1] == 'Test':
            xml_files = [filename for filename in files if os.path.splitext(filename)[1].lower() == '.xml']
            new_files = [os.path.join(location, file) for file in xml_files]
            xml_paths += new_files
        
    grand_dom = etree.Element('BIG_DOM')
    for filename in xml_paths:
        dom = dom_from_file(filename)
        for child in dom:
            grand_dom.insert(0, child)
    return grand_dom
        
def get_parse_cache(regdb_location):
    regdb_location = regdb_location or os.environ.get('MIPS_REGDB_LOCATION', None)
    if regdb_location:
        dom = build_dom(regdb_location)
        return RegDBParseCacheFromDOM(dom)
    else:
        return regdb_parse_cache
    


def is_cpu_in_list(cpu_name, cpu_list):
    """
    >>> is_cpu_in_list('1004Kc', '1004K.*')
    True
    >>> is_cpu_in_list('proaptiv', '1004K.*')
    False
    >>> is_cpu_in_list('1004Kc', '1004K.*,proaptiv.*')
    True
    >>> is_cpu_in_list('proaptiv', '1004K.*,proaptiv.*')
    True
    >>> is_cpu_in_list('ProAptiv', '1004K,proaptiv')
    True
    >>> is_cpu_in_list('interaptiv', '1004K.*,proaptiv.*')
    False
    """
    pattern = re.compile(cpu_list.replace(',', '|'), flags=re.IGNORECASE)
    return bool(pattern.match(cpu_name))

def create_hd_with_reader(output_dir, cpu_info, outname, reader, regdb_location=None, verbose=False, explain=None):
    parse_cache = get_parse_cache(regdb_location)
    img_tree = convert_to_hd_dom(parse_cache, cpu_info, reader, verbose=verbose, explain=explain)
    outname = outname or cpu_info['cpu_name']
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    src_path = os.path.join(output_dir, outname + '.xml')
    dom_to_file(src_path, img_tree)
    core_id_tree = build_core_id_tree(reader, cpu_info['cpu_name'], os.path.basename(src_path))
    core_id_path = os.path.join(output_dir, outname + '.core_id')
    dom_to_file(core_id_path, core_id_tree)
    
def create_hd_from_reg_values(output_dir, cpu_name, outname, regs, regdb_location=None, verbose=False, explain=None):
    reader = RegisterReaderPrecalculatedRegisters(regs)
    config = regs['Config']
    CP0_CONFIG3_HAS_VZE_MASK = 0x00800000
    cpu_info = dict(cpu_name=cpu_name, 
                    cpu_is_32bit=(config & 0x00006000) == 0,
                    has_vze=(regs['Config3'] & CP0_CONFIG3_HAS_VZE_MASK) != 0,
    )
    create_hd_with_reader(output_dir, cpu_info, outname, reader, regdb_location=regdb_location, verbose=verbose, explain=explain)
    
def make_cpp_variable_name(name, different_from=None):
    """
    >>> make_cpp_variable_name('')
    'anonymous'
    >>> make_cpp_variable_name('anonymous')
    'anonymous'
    >>> make_cpp_variable_name('fred')
    'fred'
    >>> make_cpp_variable_name('3fred')
    '_3fred'
    >>> make_cpp_variable_name('fred-west')
    'fred_west'
    >>> make_cpp_variable_name('fred.west')
    'fred_west'
    >>> make_cpp_variable_name('3fred-west')
    '_3fred_west'
    >>> make_cpp_variable_name('3$some[_&messed+up name')
    '_3_some_messed_up_name'
    >>> make_cpp_variable_name('3$messed+!"$%^&*()up')
    '_3_messed_up'
    >>> make_cpp_variable_name('$')
    '_'
    >>> make_cpp_variable_name('fred.west', set(['fred_west']))
    'fred_west0'
    """
    if different_from is None:
        different_from = set()
    name = re.sub('[^A-Za-z0-9]+', '_', name)
    name = re.sub('^([0-9])', '_\\1', name)
    name = name if name else 'anonymous'

    salt = 0
    unique_name = name
    while unique_name in different_from:
        unique_name = name + str(salt)
        salt += 1

    return unique_name
    
class NullRegisterReader(object):
    def get_register_value(self, name):
        raise RegisterUnreadable('Cannot read %s because read_registers is False' % (name,))
    
class RegisterReaderFromTargetData(object):
    '''
    >>> class Table(object):
    ...      config = range(0x80000000, 0x80000008)
    ...      dcr = 0x1234
    >>> t = Table()
    >>> reader = RegisterReaderFromTargetData(Table())
    >>> reader.get_register_value('other')
    Traceback (most recent call last):
    ...
    RegisterUnreadable: Cannot read other because read_registers is False
    >>> '%x' % reader.get_register_value('cp0.16.0')
    '80000000'
    >>> '%x' % reader.get_register_value('cp0.16.7')
    '80000007'
    >>> '%x' % reader.get_register_value('ejtag_dcr')
    '1234'
    '''
    def __init__(self, coretable, underlying=None):
        self.coretable = coretable
        self.underlying = underlying or NullRegisterReader()
    def get_register_value(self, name):
        regs = dict([('cp0.16.%d' % x, ('config', x)) for x in range(8)])
        regs['ejtag_dcr'] = ('dcr', None)
        regs['ejtag_ibs'] = ('ibs', None)
        regs['ejtag_dbs'] = ('dbs', None)
        regs['ejtag_cbtc'] = ('cbtc', None)
        regs['cp0.15.0'] = ('prid', None)
        regs['cp0.0.2'] = ('mvp_conf0', None)
        try:
            attr, index = regs[name]
            x = getattr(self.coretable, attr)
            return x if index is None else x[index]
        except KeyError:
            pass
        return self.underlying.get_register_value(name)
    
class RegisterReaderCodescapeConsole(object):
    def __init__(self, device):
        self.device = device
        self.cache = {}
        
    def get_register_value(self, name):
        try:
            return self.cache[name]
        except KeyError:
            self.cache[name] = value = self.device.tiny.ReadRegister(name)
            return value
            
class MakeCoreHDResult(object):
    def __init__(self, hd_path, core_path=None):
        self.core_path = core_path
        self.hd_path = hd_path
        
    def __repr__(self):
        return '\n'.join(["Wrote to %s" % f for f in [self.core_path, self.hd_path] if f])
   
@command(verbose=verbosity)
def makecorehd(output_dir=None, output_name=None, create_coreid=False, verbose=0, device=None):
    '''Generate an hardware definition file for current core. 
    
    This command will read CP0 registers to determine the presence of core
    features and determine which CP0 registers are available.
    
    If `create_coreid` is True, then a core_id file will also be written.
    
    If `output_name` is not given then the default cpu_name as given by
    cpuinfo() will be used.
    
    If `output_dir` is not given, the file(s) will be output to the user 
    hardware definition files directory, which is usually ~/imgtec/hwdefs. This 
    directory will be created if necessary.
    '''
    if output_dir is None:
        output_dir = get_user_files_dir('hwdefs')
    try:
        os.makedirs(output_dir)
    except EnvironmentError as e:
        if e.errno != errno.EEXIST:
            raise
    
    if device.core.family != CoreFamily.mips:
        pass
    else:
        cpu_info = dict(device.da.CpuInfo())
        output_name = output_name or cpu_info.get('cpu_name')
        
        reader = RegisterReaderCodescapeConsole(device)
        reader = RegisterReaderFromTargetData(device.core.targetdata, reader)
        
        from imgtec.console.generic_device import probe
        probe_type = probe().identifier.split()[0]
        img_tree = convert_to_hd_dom(get_parse_cache(None), cpu_info, reader, probe_type=probe_type, include_memory_types_and_ranges=False)
        #Place to put file, default to console dir
        src_path = os.path.join(output_dir, output_name + '.xml')
        file_paths = [src_path]
        
        dom_to_file(src_path, img_tree, verbose)
        if create_coreid:
            core_id_tree = build_core_id_tree(reader, output_name, os.path.basename(src_path))
            core_id_path = os.path.join(output_dir, output_name + '.core_id')
            dom_to_file(core_id_path, core_id_tree, verbose)
            file_paths.append(core_id_path)
            
        return MakeCoreHDResult(*file_paths)
           
@command(verbose=verbosity)
def scanregisters(read_registers=True, verbose=0, explain=None, device=None):
    '''Discover which registers and register fields the target has. 
    
    Note that unless read_registers is False, this command will read CP0 
    registers to determine the presence of core features and determine which 
    CP0 registers are available.
    
    if read_registers is False, then it will be assumed that all possible 
    registers exist.
    
    `explain` can be the name of a register and causes more diagnostics to be 
    output explaining why the given register is determined to exist or not.
    '''
    from imgtec.console.generic_device import _regdb_callbacks
    cpu_info = dict(device.da.CpuInfo())
    
    parse_cache = get_parse_cache(None)
    
    reader = NullRegisterReader()
    core = getattr(device, 'core', device)
    if read_registers:
        reader = RegisterReaderCodescapeConsole(device)
    reader = RegisterReaderFromTargetData(core.targetdata, reader)
    env = EvaluationEnvironment(
        cpu_name = cpu_info.get('cpu_name', 'default'),
        register_reader = reader,
        conditions = parse_cache.conditions,
        verbose = verbose,
    )
    
    if device.family == CoreFamily.mips:
        try:
            device.regdb = _make_regdb(reader, cpu_info, read_registers, env, parse_cache, verbose, explain)
        except KeyError:  # TODO why do we quash this exception?
            pass
    elif verbose:
        print "Skipping non MIPS device %s" % device
        
    for cb in _regdb_callbacks:
        try:
            thread = device.vpes[0]
        except AttributeError:
            thread = device
        try:
            cb(thread)
        except Exception:
            print 'user scanregisters callback failed on %s:' % (thread.name,)
            traceback.print_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2].tb_next)
            
    if explain == '*':
        conds = OrderedDictResult()        
        for n, c in sorted(parse_cache.conditions.items()):
            try:
                conds[n] = evaluate(c, env) 
            except RegisterPrerequisiteDoesNotExist:
                conds[n] = False
            except RegisterAccessError:
                conds[n] = False
        return conds
        
    
    
_regdb_cache = {}
def _make_regdb(reader, cpu_info, read_registers, env, parse_cache, verbose=0, explain=None):
    regdb = None
    if not read_registers:
        key = tuple(sorted(cpu_info.items()))
        regdb = _regdb_cache.get(key)
        
    if not regdb:
        registers = parse_registers(parse_cache, cpu_info, env, verbose=verbose, explain=explain)
        regdb = RegDB(registers)
        if not read_registers:
            _regdb_cache[key] = regdb
    return regdb
    
class RegDBError(Exception):
    pass
    
def format_description(s):
    r'''Format description, converting ${p} etc and fixing up whitespace issues.
    
    >>> format_description('this   is   a${p}new paragraph')
    'this is a\n\nnew paragraph'
    >>> format_description('this   is   a${nl}${tab}new indented line')
    'this is a\n    new indented line'
    >>> format_description(r'this   is   a\n${tab}new indented line')
    'this is a\n    new indented line'
    >>> format_description('this.   is   a new sentence')
    'this.  is a new sentence'
    >>> format_description('3.1 this is not')
    '3.1 this is not'
    '''
    repls = dict(p='\n\n', nl='\n', tab='    ')
    def _convert_formatters(match):
        return repls.get(match.group(1), match.group(0))

    # find all excessive whitespaces (but take care after a full stop)
    s = re.sub(r'(?<!\.)\s\s+', ' ', s) 
    # sometimes newlines are encoded with \\n
    s = s.replace('\\n', '\n')
    return re.sub(r'\${([^{]+)}', _convert_formatters, s)
        
        
named_enum_cache = {}
def get_named_enum(field_name, enum_types):
    global named_enum_cache
    
    key = (field_name, tuple(enum_types))
    if not named_enum_cache.get(key):
        named_enum_cache[key] = namedenum(field_name, *enum_types)
        
    return named_enum_cache[key]
    

def make_enum_value(value, previous_names):
    '''Convert names in a Value to be suitable for use in a namedenum.
    Unicode chars in description are removed.
    
    >>> values = [Value('None', 0, u'\xdfv0'), Value('_wibble', 0x11, u'\xaev11')]
    >>> previous_names = []
    >>> make_enum_value(values[0], previous_names)
    ('e_None', 0, 'v0')
    >>> make_enum_value(values[1], previous_names)
    ('e_wibble', 17, 'v11')
    >>> make_enum_value(values[1], previous_names)
    ('e_wibble0', 17, 'v11')
    '''
    #Disambiguate/make valid field names
    name = make_cpp_variable_name(value.name, previous_names)
    previous_names.append(name)
    #Config's 'MMU type' can be 'None', which Python doesn't like, and namedenum
    # doesn't like leading underscores.
    if name == 'None':
        name = '_None'
    if name.startswith('_'):
        name = 'e' + name
    return (name, value.value, value.description.encode('ascii', 'ignore'))
        
def convert_field_shift_and_mask(field):
    '''Convert a field, details, and values into a namedbitfield.Field object.
    Unicode characters are removed from all descriptions.

    >>> convert_field_shift_and_mask(Field('f', bits=Bits(7, 4), description='D'))
    f bit_start:7 bit_end:4 mask:0xf0
        D
        
    >>> values = [Value('val0', 0, u'\xaev0'), Value('None', 11, 'v11')]
    >>> convert_field_shift_and_mask(Field('f', bits=Bits(7,4), description=u'D\xae', values=values))
    f bit_start:7 bit_end:4 mask:0xf0
        D
            ===== ====== ===========
            Value Name   Description
            ===== ====== ===========
            0     val0   v0
            11    e_None v11
            ===== ====== ===========
    
    '''
    name = make_cpp_variable_name(field.name)

    field_type = long
    if field.values:
        previous_names = []
        values = [make_enum_value(value, previous_names) for value in field.values]
        field_type = get_named_enum(name, values)

    #Ignore unprintable chars
    field_desc = field.description.encode('ascii', 'ignore')
    #Remove excess whitespace
    field_desc = re.sub(r'\s{2,}', ' ', field_desc)
    #Substitute ${x} formatting markers for their meanings
    field_desc = format_description(field_desc)
    return namedbitfield.Field(name, field.bits.start, field.bits.end, field_desc, type=field_type)

def _make_register_type(reg, viewopts):
    if reg.fields or reg.description:
        fields = [convert_field_shift_and_mask(f) for f in reg.fields]
        return namedbitfield.namedbitfield(reg.display_name, fields, reg.size,
                                 description=reg.description,
                                 show_vertical=viewopts.show_vertical,
                                 show_raw_value=viewopts.show_raw_value,
                                 show_bit_position=viewopts.show_bit_position)
                                 
class RegDB(object):
    def __init__(self, registers):
        lookup = {}
        for reg in registers:
            views = lookup.setdefault(reg.comms_name.lower(), [])
            views.append(reg)
            lookup[reg.display_name_no_view.lower()] = views
            lookup[reg.display_name.lower()] = views # make all full view names lookupable
        self._registers = lookup
        '''Dict of (comms names, display names and view names).lower()->[Registers].
        This is a list because there may be multiple views for a register.
        '''
        
        self._reg_type_cache = {}
        '''Cache of namedbitfields keyed on some key.'''
        
    def get_register_type(self, name, device, viewopts=ViewOptions()):
        '''Return a namedbitfield for the given register or None if no rich type info is found.'''
        if name.startswith('guest_'):
            name = name.split('guest_', 1)[1]
        
        name = device._normalise_regname(name)
        try:
            reg = self.get_register(name, viewopts.view)
        except RegDBError as e:
            if 'no view' in str(e):
                raise
        else:
            cpu_info = dict(device.da.CpuInfo())
            prid = cpu_info.get('prid', 0x0)
            # TODO, should this cache on fields as well?
            key = (device.family, prid, reg.display_name, viewopts)
            try:
                return self._reg_type_cache[key]
            except KeyError:
                pass                
            if reg.fields or reg.description:
                t = self._reg_type_cache[key] = _make_register_type(reg, viewopts)
                return t
        return None
            
    def comms_name(self, name):
        '''Return the name that the underlying comms expects for the given register.'''
        try:
            return self.get_register(name).comms_name
        except RegDBError:
            return name.lower()
            
    def does_register_exist(self, name):
        try:
            self.get_register(name)
            return True
        except RegDBError:
            return False
    
    def get_register(self, name, view=None):
        try:
            views = all_views = self._registers[name.lower()] 
            reg = views[0]
        except KeyError:
            raise RegDBError("Register named '%s' cannot be found" % (name,))
        if view:
            views = [v for v in views if v.view_name.lower() == view.lower()]
            if not views:
                valid = ', '.join(v.view_name for v in all_views)
                name = reg.display_name_no_view
                raise RegDBError("Register %s has no view named '%s', valid views are %s" % (name, view, valid))
        elif len(views) > 1 and name.lower() not in (reg.display_name_no_view.lower(), reg.comms_name):
            # where name == full view name, e.g. regname_viewname, note that
            # regs.py prevents this because it incorrectly filters names through
            # regsinfo first.
            views = [v for v in views if v.display_name.lower() == name.lower()]
        return views[0]
        
        
if __name__ == '__main__':
    import doctest
    doctest.testmod()
    unintrusive_parse({})
