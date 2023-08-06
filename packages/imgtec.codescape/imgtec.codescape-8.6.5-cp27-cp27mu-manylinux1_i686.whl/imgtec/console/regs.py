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
from imgtec.test import *
from imgtec.lib import get_user_files_dir
from imgtec.lib import rst
from imgtec.console.support import *
from imgtec.console.results import *
from imgtec.console.reginfo import Info
from imgtec.console.regdb_types  import ViewOptions
from imgtec.codescape.register_templates import parse_grid, get_template_properties, template_error_wrapper
from imgtec.codescape.register_templates import split_settings_from_template, scan_templates, expand_short_cells
from imgtec.codescape.register_templates import insert_template_from_properties, get_compatible_templates, TemplateProperties
from imgtec.lib.conversions import float_to_word
from imgtec.codescape.da_exception import Error
from imgtec.console.reg_templates import reg_templates
from imgtec.lib.namedenum import namedenum
from imgtec.lib.ordered_dict import OrderedDict
from difflib import get_close_matches

try:
    from jinja2 import Environment
    
    jinja_env = Environment()
    jinja_env.globals.update(dict(zip=zip, max=max, min=min, any=any))
    jinja_env.line_statement_prefix = '$'
except ImportError:
    print 'Module jinja2 not found. To enable support for Jinja in register templates please install using "easy_install jinja2".'
    jinja_env = None
    
class RegsException(Exception):
    pass

class TinyRegisterEvaluator(object):
    def __init__(self, device):
        self.device = device
        self.tiny = device.tiny
        self.regs = []
        self.cname_to_regname = {}
        self.regname_to_cname = {}
        self.cache = OrderedDict()
        self.float_as_int = False
        self.consecutive_errors = 0
        
    def build_cache(self, expression):
        if expression.startswith('$'):
            self.regs.append(expression[1:].lower())
        return 0
        
    def load_cache(self, view_options, suggest=False, float_as_int=False):
        self.float_as_int = float_as_int
        reg_names = list(set(item.lower() for item in self.regs))
        to_read = _comms_names(self.device, reg_names)
        self.regname_to_cname = dict((rname, cname) for rname, cname in zip(reg_names, to_read))
        self.cname_to_regname = dict((cname, rname) for cname, rname in zip(to_read, reg_names))
        
        values = []
        if suggest:
            values = read_write_reg_with_suggest(self.device, to_read, float_as_int=float_as_int) 
        else:
            values = self.tiny.ReadRegisters(to_read, float_as_int)
            
        self.cache = OrderedDict(zip(to_read, values))
        for cname in self.cache:
            self.cache[cname] = _make_reg_result(self.device, self.cname_to_regname[cname], self.cache[cname], 
                view_options, float_as_int=float_as_int)
            
    @property
    def reg_result_cache(self):
        #Like the cache but accounts for repeated registers from something like regs('at at at')
        return [(reg, self.cache[self.regname_to_cname[reg]]) for reg in self.regs]
        
    def __call__(self, expression):
        if expression.startswith('$'):
            name = expression[1:].lower()
            comms_name = self.regname_to_cname[name]
            #Try to get from cache, otherwise read normally
            try:
                val = self.cache[comms_name]
            except KeyError:
                try:
                    #Add these to the cache so the full register list is available for MultipleRegResults
                    val = read_write_reg_with_suggest(self.device, [comms_name])[0]
                    self.cache[comms_name] = val
                except Exception:
                    #Not found regs are None so that MultipleRegResults have a fixed length
                    self.cache[comms_name] = None
                    self.consecutive_errors += 1
                    
                    if self.consecutive_errors > 10:
                        raise RegsException("Stopping due to number of errors.")
                    raise
                else:
                    self.consecutive_errors = 0

            #Floating point regs need conversion even when displayed as floats
            #as we might need to shift them first
            if not self.float_as_int:
                reg_info = _get_reg_info(self.device, name)
                if reg_info.is_float:
                    val = float_to_word(val, reg_info.size)
                
            return val
        return int(expression, 0)
        
def display_registers(format, evaluator, layout_view_options=None):
    grid = template_error_wrapper(parse_grid, None, '')(format)
    
    #Apply view options in the case of a Jinja layout
    if layout_view_options is not None:
        for option in layout_view_options:
            value = layout_view_options[option]
            grid.set_view_option(option, value)
            
    #Account for possible break cells
    blocks = [[], ]
    for row in grid.rows:
        #New row
        blocks[-1].append([])
        
        for cell in row:
            if cell.is_break:
                #If the break is on the beginning of a new line the ending of the previous row
                #will have caused an empty line to be added to the end of the block so remove that.
                if not blocks[-1][-1]:
                    blocks[-1].pop(-1)
                # Start a new block
                blocks.append([[]])
            blocks[-1][-1].append(cell)
        
    final_lines = []
    
    for block in blocks:
        lines = []
        widths = [0]*max([len(row) for row in block]) if block else []
        
        #First pass renders the cells
        errors = []
        for row in block:
            cells = []
            for i, cell in enumerate(row):
                try:
                    render_str = cell.render(evaluator)
                    #Save the render (without justifying, as not all rows have been processed yet)
                    cells.append(render_str)
                except RegsException:
                    #This means we accumulated too many errors in the evaluator
                    if errors:
                        errors = sorted(set(errors))
                        print '\n'.join(errors)
                    raise
                except Exception as e:
                    errors.append(str(e))
                    render_str = 'not found'
                    cells.append(render_str)
                finally:  
                    #Check for new max length between cell's width and stored width
                    widths[i] = max(widths[i], len(render_str))
                    
            if errors:
                errors = sorted(set(errors))
                print '\n'.join(errors)
                errors = []

            #Save finished line (as a copy)
            lines.append(cells[:])
            
        #Now that all the rows have been rendered, we can do the justification
        joined_lines = []
        for row in lines:
            for i, _ in enumerate(row):
                row[i] = row[i].ljust(widths[i]+1)
            joined_lines.append(''.join(row))
        final_lines.extend(joined_lines)
        
    return '\n'.join(final_lines)
    
def get_register_width(name, reg_info):
    ''' returns register width in bytes'''
    if reg_info is not None:
        return reg_info.size
    else:
        if re.match(r'w\d+$', name): 
            return 16
        return 4
    
def make_reg_template(names, device, float_as_int):
    #Make an on-the-fly template for the given register names.
    
    regs_info = device.registers_info_by_name
    cols = 4
    row = []
    rows = [row] # So that headerless table works
    
    for name in names:
        info = regs_info.get(name)
        width_bytes = get_register_width(name, info)
        is_float = False if not info else info.is_float
        
        if len(row) >= cols*2:
            row = []
            rows.append(row)
            
        row.append(name)
        
        #Use hex cells for showing floats as int, makes reading the value easier
        if is_float and not float_as_int:
            row.append('[$%s floating_point width_bytes=%d as_hex=%s]' % 
                (name, width_bytes, 'True' if float_as_int else 'False'))
        else:
            #Width in chars here
            row.append('[$%s hex width=%d]' % (name,width_bytes*2))

    return rst.headerless_table(rows)
    
class RegModifyException(RuntimeError):
    pass
    
def _get_field_value(field, field_value):
    '''Ensure that field_value is a valid integer value for field, converting 
    from enum names if approriate.
    
    >>> from imgtec.lib.namedbitfield import Field
    >>> f = Field('f', 15, 8, type=namedenum('e', a=1, b=2, c=3, B=7))
    >>> _get_field_value(f, 'c')
    3
    >>> _get_field_value(f, 'C')
    3
    >>> _get_field_value(f, 'B')
    7
    >>> _get_field_value(f, 'B')
    7
    >>> _get_field_value(f, 0)
    0
    >>> _get_field_value(f, 255)
    255
    >>> _get_field_value(f, 256)
    Traceback (most recent call last):
    ...
    ValueError: Value 0x00000100 is out of range for field f which has mask 0x000000ff
    >>> _get_field_value(f, -1)
    255
    >>> _get_field_value(f, -255)
    1
    '''
    if not isinstance(field_value, basestring):
        if field_value < 0:
            field_value = field_value + field.mask + 1
        if (field_value & field.mask) != field_value:
            raise ValueError("Value 0x%08x is out of range for field %s which has mask 0x%08x" % (field_value, field.name, field.mask))
        return field_value
    #Try to find a matching enum value
    try:
        enum_items = dict(field.type._items())
        ienum_items = dict((k.lower(),v) for k, v in enum_items.iteritems())
    except AttributeError:
        raise RegModifyException("Got string value '%s' for field '%s' which has no enum type." % (field_value, field.name))

    try:
        return enum_items[field_value]
    except KeyError:
        pass
        
    # try case insensitively:
    try:
        return ienum_items[field_value.lower()]
    except KeyError:
        raise RegModifyException("Got unknown value '%s' for field '%s'" % (field_value, field.name))
        
        
def _calculate_rmw_value(name, reg_type, _new_value=0, _modify_mask=0, **kwargs):
    if kwargs:
        try:
            fields = dict((field.name.lower(), field) for field in reg_type._fields)
        except AttributeError:
            raise RegModifyException("Register '%s' does not have a rich type associated with it." % name)

        #Search kwargs for things that look like field names
        unknown = []
        for field_name, field_value in kwargs.iteritems():
            try:
                field = fields[field_name.lower()]
            except KeyError:
                unknown.append(field_name)
            else:
                field_value = _get_field_value(field, field_value)
                _modify_mask |= (field.mask << field.shift)
                _new_value |= ((field_value & field.mask) << field.shift)
        if unknown:
            raise RegModifyException('Got unexpected field names: %r' % (unknown,))
    return _new_value, _modify_mask

    
@command()
def regmodify(name, _new_value=0, _modify_mask=0, device=None, **kwargs):
    '''
    Read/modify write a register where the keyword arguments are new field values.
    This command only applies to registers which have type information. Field values
    can be integers or strings, where the string is one of the field's enum values
    (see regtype).

    >>> regmodify('index', Index=0xe)
    Field Name  Old Value  New Value
    <raw value> 0x80000004 0x8000000e
    P           P.No_match P.No_match
    Reserved    0x0        0x0
    Index       0x4        0xe   

    >>> regmodify('index', Index='Match')
    Field Name  Old Value  New Value
    <raw value> 0x8000000e 0x0000000e
    P           P.No_match P.Match
    Reserved    0x0        0x0
    Index       0x4        0xe
    
    Alternatively a new_value and modify_mask may be set explicitly (the param
    names are listed with prefixed underscores so they don't clash with the 
    keyword arguments representing field names of the register) :
    
    >>> regmodify('index', 0x4, 0xf)
    Field Name  Old Value  New Value
    <raw value> 0x0000000e 0x00000004
    P           P.Match    P.Match
    Reserved    0x0        0x0
    Index       0xe        0x4
    
    Or both can be combined:

    >>> regmodify('index', 0x2, 0xf, P='No_match')
    Field Name  Old Value  New Value
    <raw value> 0x00000004 0x80000002
    P           P.Match    P.No_match
    Reserved    0x0        0x0
    Index       0x4        0x2
    
    '''
    try:
        reg_type = regtype(name)
    except RegTypeException:
        # Some registers aren't in the RegisterInfo e.g. 'r1' with o32 ABI
        reg_type = long
    
    _new_value, _modify_mask = _calculate_rmw_value(name, reg_type, _new_value, _modify_mask, **kwargs)

    if reg_type in (int, long):
        #TODO should be size somehow.  ideally regtype would do that for us, a
        # and it would cope with floats, using, say the guts of _make_reg_result.
        # but _make_reg_result doesn't seem to do reg size properly anyway
        reg_type = IntResult  
    
    try:
        name = _comms_names(device, [name])[0]
        old, new = device.tiny.ReadModWriteRegister(name, _new_value, _modify_mask, '=,old_values,new_values')
        old, new = reg_type(old), reg_type(new)
    except AttributeError:
        old = regs(name)
        value = (old & ~_modify_mask) | (_new_value & _modify_mask)
        new = regs(name, value)
    return NamedBitfieldDiff(old, new)
    
class RegTypeException(Exception):
    pass
    
def _get_reg_info_doc(info):
    return (info.name,
    '%d-bit' % (info.size*8),
    ''.join(['(', ', '.join(alias for alias in info.aliases), ')']) if info.aliases else '',
    'float' if info.is_float else '')


class RegTypeListResult(OrderedDict):
    def __init__(self, results):
        #Results is a list of [name, info, type]
        self._info = [info for info, type in results]
        super(RegTypeListResult, self).__init__([(info.name.lower(), type) for info, type in results])
        
    def __getitem__(self, key):
        if isinstance(key, (int, long, slice)):
            return self.values().__getitem__(key)
        elif isinstance(key, basestring):
            return super(RegTypeListResult, self).__getitem__(key.lower())
        else:
            raise TypeError('Incorrect key type.')
            
    def __contains__(self, key):
        if isinstance(key, basestring):
            key = key.lower()
        return super(RegTypeListResult, self).__contains__(key)
        
    def __repr__(self):
        rows = [_get_reg_info_doc(info) for info in self._info]
        return rst.headerless_table(rows)
        
def _search_reg_name(search_name, info):
    '''
    Perform a case insensitive match of a search term against a reginfo.Info
    object, searching in both name and it's aliases. Also search for close 
    matches by looking for the term within the register name or within each of 
    it's aliases.
    
    >>> _search_reg_name('foo', Info('Food', 4, 4, 0, []))
    True
    >>> _search_reg_name('cafe', Info('Food', 4, 4, 0, ['caFEfood']))
    True
    >>> _search_reg_name('cad', Info('Food', 4, 4, 0, ['caFEfood']))
    False
    '''
    names = [alias.lower() for alias in info.aliases] + [info.name.lower()]    
    return any([search_name in name for name in names])
    
def _MultiLineException(cls, *lines):
    lines = [x for x in lines if x]
    return cls('\n'.ljust(len(cls.__name__)+3).join(lines))
def _RegTypeException(*lines):
    return _MultiLineException(RegTypeException, *lines)
        
@command()
def regtype(name='', view=None, exact=True, show_vertical=True, show_raw_value=True, 
    show_bit_position=False, device=None):
    """Get the type of a register by name.
    
    Find a register with a name or alias matching `name` - the comparison is 
    case-insensitive - and return it's type which will be one of 
    namedbitfield, long or float and is equivalent to ``type(regs('regname'))`` 
    but without reading the register. 
    
    If the register is not found then an exception is raised.
    
    For the parameters `view`, `show_vertical`, and `show_raw_value` see 
    :func:`regs`.   
    
    Note that floating point registers may also have bitfield information.
    
    For backwards compatability, if name is an empty string, or exact is False
    then this command is equivalent to :func:`regsearch`.
    """
    if not name or not exact:
        return regsearch(name, view, show_vertical, show_raw_value, device=device)
        
    viewopts = ViewOptions(True, show_vertical, show_raw_value, show_bit_position, view)
    reg_info = device.registers_info_by_name.get(name.lower())
    if not reg_info:
        raise _RegTypeException("No register found with name '%s'." % name,
                                get_register_suggestion_msg(device, name),
                                "(use regsearch to search for names containing '%s')" % name)
    return _make_reg_type(device, reg_info, viewopts)
    
@command()
def regsearch(name='', view=None, show_vertical=True, show_raw_value=True, show_bit_position=False, 
    device=None):
    '''Search for registers by name.
    
    If name is given then only registers with a name or alias matching that
    name are shown (the comparison is case-insensitive), otherwise all registers
    are returned. Note that not all registers are necessarily valid on the 
    current probe or device.
    
    If exact is False then a OrderedDict of types is returned even if only one
    match is found.  The OrderedDict is keyed on the register name in lower case
    to the type.
    '''
    viewopts = ViewOptions(True, show_vertical, show_raw_value, show_bit_position, view)
    
    regs = device.registers_info
    if name:
        name = name.lower()
        regs = [r for r in regs if _search_reg_name(name, r)]
    if not regs:
        raise _RegTypeException("No registers found with name containing '%s'." % name,
                                get_register_suggestion_msg(device, name))

    types = [(r, _make_reg_type(device, r, viewopts)) for r in regs]
    return RegTypeListResult(types)    
        
def get_register_suggestion_msg(device, name):
    matches = get_close_matches(name, device.registers_info_by_name)
    err_parts = []
    
    if matches:
        err_parts.append("Did you mean ")
        if len(matches) == 1:
            err_parts.append("'%s'" % matches[-1])
        else:
            err_parts.append(', '.join(["'%s'" % m for m in matches[:-1]]))
            err_parts.append(" or '%s'" % matches[-1])
        err_parts.append('?')
        
    return ''.join(err_parts)

REGION_VERSION = 1.4
USER_TEMPLATE_DIR = get_user_files_dir('register_templates')

def get_jinja_args(device):
    processor_family = str(device.family)
    cpu_info = dict(device.da.CpuInfo())
    core_id = cpu_info.get('prid', 0x0)
    
    new_registers_info = device.registers_info_by_name   
    kwargs =  {'cpu_info' : cpu_info,
               'REGION_VERSION' : REGION_VERSION,
               'CORE_ID' : hex(core_id),
               'registers' : sorted(new_registers_info.keys()),
               'ABI' : device.abi,
               'PROCESSOR_FAMILY' : processor_family,
              }
              
    return (processor_family, cpu_info, core_id, kwargs, new_registers_info)
    
def get_compatible_templates_for_device(jinja_args, use_user=True):
    processor_family, _cpu_info, core_id, kwargs, _register_info = jinja_args
    #Get template properties
    template_props = [get_template_properties(temp, kwargs) for temp in reg_templates]
    
    for temp, prop in zip(reg_templates, template_props):
        #As these aren't file based we use .layout to store a copy of the unmodified layout
        prop.layout = temp
        
    # Build structure
    mapping = {}
    
    if use_user:
        #User template folder
        class FakeRegmodel(object):
            def __init__(self):
                self.template_keyword_args = kwargs
            
        mapping = scan_templates([USER_TEMPLATE_DIR], FakeRegmodel(), REGION_VERSION, mapping=mapping)
    
    #Update with built in templates
    for prop in template_props:
        insert_template_from_properties(mapping, prop, REGION_VERSION)
    
    return get_compatible_templates(mapping, processor_family, core_id, insert_null=False)
    
class RegTemplateList(list):
    def __repr__(self):
        s = []
        for template in self:
            name = None
            if template.name is not None:
                name = template.name
            else:
                #Otherwise say nothing and the user will see the file path
                name = 'Unknown'
                    
            temp = [name]
            if template.file_path:
                temp.append('(%s)' % template.file_path)
            s.append(' '.join(temp))
        return '\n'.join(s)
    
@command(vpe_required=True)
def regtemplates(device=None):
    '''
    Returns a list of register templates compatible with this device. 
    These can be selected by passing their name to the regs command as 'template_name'.
    
    Calling 'get_options' on one of these items will return a dictionary of the 
    template's options. This can then be modified and passed to the regs command.
    
    >>> regtemplates()
    MIPS Generic Console
    MIPS Generic with n64
    >>> opts = regtemplates()[1].get_options()
    {ShowFloatingPoint: True, ShowDefaultPerThread: True, ShowDSPAccumulator: True, ShowCP0: False}
    >>> opts['ShowFloatingPoint'] = False
    >>> regs(template_name='with n64', view_options=opts)
    ...
    
    '''
    jinja_args = get_jinja_args(device)
    templates = get_compatible_templates_for_device(jinja_args)
    
    if templates:
        return RegTemplateList(templates)
    else:
        raise RegsException('No compatible register templates found.')
    
def _get_reg_info(device, name):
    try:
        return device.registers_info_by_name[name.lower()]
    except KeyError:
        return Info(name, 4, 4, False, [])
        
def _make_fallback_reg_type(reg_info, float_as_int):
    if reg_info.is_float and not float_as_int:
        return float # TODO We need a FloatResultType that stores float/hex

    doc = ' '.join(_get_reg_info_doc(reg_info)).strip()
    return IntResultType(size=reg_info.size, doc=doc)
    
def _make_reg_type(device, reg_info, viewopts, float_as_int=False):
    #Get possible special type from the regdb
    name = reg_info.name.lower()
    if viewopts.show_fields:
        try:
            reg_type = device.user_regdb[name]
        except KeyError:
            reg_type = device.regdb and device.regdb.get_register_type(name, device, viewopts)

        if reg_type is not None:
            return reg_type

    # In the event that there is no RegDB or the reg isn't in it use the data 
    # from reginfo to make an appropriately sized type.
    return _make_fallback_reg_type(reg_info, float_as_int)
    
def _make_reg_result(device, name, reg_value, viewopts, float_as_int=False):
    reg_info = _get_reg_info(device, name)
    
    if reg_info.is_float and not float_as_int:
        reg_type = float
    else:
        reg_type = _make_reg_type(device, reg_info, viewopts, float_as_int=float_as_int)
        
    if viewopts.show_fields:
        if reg_info.is_float and not issubclass(reg_type, float) and not float_as_int:
            #When showing fields for floats we need the real hex value
            reg_value = float_to_word(reg_value, reg_info.size)
    
    return reg_type(reg_value)
        
class MultipleRegResult(ListDict):
    def __init__(self, render, cache):
        self._render = render
        super(MultipleRegResult, self).__init__(cache)
        
    def __getitem__(self, key):
        if isinstance(key, basestring):
            val = super(MultipleRegResult, self).__getitem__(key)
            if val is None:
                raise KeyError("Register '%s' failed to read." % key)
            else:
                return val
        else:
            return super(MultipleRegResult, self).__getitem__(key)
            
    def __repr__(self):
        return self._render
    
    def get(self, name, default=None):
        try:
            return self[name]
        except KeyError:
            return default
        
    def diff(self, other):
        if not isinstance(other, MultipleRegResult):
            raise TypeError('Can only diff against another MultipleRegResult.')
            
        titles = ['Name', 'First result', 'Second Result']
        rows = []
        
        reg_names = set(self.keys() + other.keys())
        for reg_name in reg_names:
            lhs = self.get(reg_name)
            rhs = other.get(reg_name)
                
            if lhs == rhs:
                continue
                
            new_row = [reg_name]
            for v in lhs, rhs:
                if v is None:
                    new_row.append("N/A")
                else:
                    new_row.append("0x%016x" % v)
                    
            rows.append(new_row)
            
        return rst.simple_table(titles, rows)


def _comms_names(device, names):
    if device.regdb:
        names = [device.regdb.comms_name(name) for name in names]
        
    # This mapping is so that aliases work in comms (probably test comms) that
    # don't cope with the aliases configured in regsinfo.
    # TODO fix the underlying test devices
    return [device._normalise_regname(n) for n in names]
    
def _parse_reg_not_found(message):
    r'''Extract the register name from a No register found with name message.
    
    >>> _parse_reg_not_found("No register found with name 'name' in abi <ABI>")
    'name'
    >>> _parse_reg_not_found(r"No register found with name '<n'ame>' in abi <ABI>")
    "<n'ame>"
    >>> _parse_reg_not_found(r"No register found with name '<n\'ame>' in abi <ABI>")
    "<n\\'ame>"
    >>> _parse_reg_not_found(r"No register found with oops not formatted correctly")
    ''
    '''
    #Note that unescaped quotes and spaces can end up in the register name 
    try:
        return re.search(r"with name '(.*)' in abi", message).group(1)
    except AttributeError:      
        return ''

def read_write_reg_with_suggest(device, names, values=None, float_as_int=False):
    comms_names = _comms_names(device, names)
    try:
        if values is None:
            return device.tiny.ReadRegisters(comms_names, float_as_int)
        else:
            device.tiny.WriteRegisters(comms_names, values, float_as_int)
    #Error from da_exceptions is TinyDashScript, RuntimeError from the test device
    except (Error, RuntimeError) as e:
        name = _parse_reg_not_found(str(e))
        if name:
            raise RuntimeError(str(e) + '. ' + get_register_suggestion_msg(device, name))
        else:
            raise
        
vertical   = named('vertical')
horizontal = named('horizontal')
rawvalue   = named('rawvalue')
norawvalue = named('norawvalue')

@command(
    show_vertical=[(vertical, True), (horizontal, False)],
    show_raw_value=[(rawvalue, True), (norawvalue, False)],
    vpe_required=True,
)
def regs(name=None, value=None, view=None, template=None, template_path=None, 
         template_name=None, use_user=True, view_options=None, show_fields=True, 
         show_vertical=True, show_raw_value=True, show_bit_position=False, 
         float_as_int=False, device=None):
    """Dumps common registers, or gets and sets registers by name.
    
    To read or write a single register:

    >>> regs('pc')
    0xbfc00000
    >>> regs('pc', 0x80000000)
    0x80000000

    For multiple registers 'name' can be a whitespace seperated string of names, 
    or a list of names. With values as a list.

    >>> regs('pc config')
    pc BFC00000 config 80240482
    >>> regs(['pc', 'config'])
    pc BFC00000 config 80240482
    >>> regs('pc config', [0x80000000, 0x1])
    pc 80000000 config 80240481

    In this case the return type is a type that is like a list and a dictionary. 
    You can index it to get values but also lookup by register name.

    >>> regs('pc config')['pc']
    0xbfc00000
    >>> regs('pc config')[0]
    0xbfc00000

    Note that when giving register names as a list or string, the first failure
    will be raise an Exception. Whereas a register template will read as many
    registers as possible. In that case registers that fail to read are 
    given the value None in the return value.

    >>> regs('pc at foo')
    Error: No register found with name 'foo' in abi o32
    >>> template = 'pc [$pc hex] at [$at hex] foo [$foo hex]'
    >>> f = regs(template=template)
    >>> f
    pc bfc00000 at cafef00d foo not found
    >>> list(f)
    [0xbfc00000, 0xcafef00d, None]
    >>> f['pc']
    0xbfc00000
    >>> f['foo']
    Traceback (most recent call last):
    ...
    KeyError: "Register 'foo' failed to read."

    The return value of a multi register read can be written back to the target by
    passing is as 'value' with 'name' as None:

    >>> f= regs('pc config')
    >>> f
    pc 80000000 config 80240481
    >>> regs('pc', 0xbfc00000)
    0xbfc00000
    >>> regs(value=f)
    pc 80000000 config 80240481

    Where possible the return value includes field information:

    >>> regs('config')
    <raw value> 0x80240481
    M           0x1
    <...>
    K0          0x1
    >>> regs('pc config')[1]
    <raw value> 0x80240481
    M           0x1
    <...>
    K0          0x1
    >>> regs('config').K0
    0x1

    Field information can be disabled with show_fields=False, and the format changed
    by setting show_vertical and/or show_raw_value.

    >>> regs('config', show_fields=False)
    0x80240481
    >>> regs('config', show_vertical=False)
    <raw>    M K23 KU ISP DSP UDI SB MDU MM BM BE AT AR MT K0
    80240481 1 0   0  0   0   0   1  0   1  0  0  0  1  1  1
    >>> regs('config', show_vertical=False, show_raw_value=False)
    M K23 KU ISP DSP UDI SB MDU MM BM BE AT AR MT K0
    1 0   0  0   0   0   1  0   1  0  0  0  1  1  1

    If no name or value is given then a register template is used. These come from one
    of the following locations:

      - a template as a string ('template' arg)
      - a template file path ('template_path' arg)
      - a template found from a Codescape Debugger install, or user template 
        folder (default is ~/imgtec/register_templates)

    For more detail on the register template format see Codescape Debugger's help.
    
    ================= =========================================================================
    Parameter         Meaning
    ================= =========================================================================
    name              Register name, or list/whitespace separated string of names.
    value             Value, list of values or MultipleRegResult to write to the register(s).
    view              For registers which can be viewed in different ways set this to show that
                      view. For example 'ITagLo_0_0'.
    template          A register template as a string.
    template_path     The file path of a register template file.
    template_name     The name of the template you wish to use, to get a list of these names
                      use the regtemplates command. Templates with exactly the same name are
                      looked for first, followed by lower case exact and then names containing
                      the lower case name.
    use_user          If True templates from the user/Codescape/register_templates folder may 
                      be used when all regs are shown.
    view_options      A dictionary containing view options for the template used.
    show_fields       Show known fields when reading a single register. In the case of 
                      floating point registers, if this is False they will be shown as their 
                      floating point value instead of hex fields. (default True)
    show_vertical     When reading a single register for which fields are known, show them 
                      vertically instead of horizontally. (default True)
    show_raw_value    When reading a single register for which fields are known show the raw 
                      value of the register along with its fields. For floating point 
                      registers this value will still be in hex format (see show_fields). 
                      (default True)
    show_bit_position When showing register fields also show the bit position of those fields.
    ================= =========================================================================
    
    """
    if view_options is None:
        view_options = {}
    
    processor_family = None
    kwargs   = {}
    viewopts = ViewOptions(show_fields, show_vertical, show_raw_value, show_bit_position, view)
    
    # Set when reading a specific list of registers so that one failure raises,
    # whereas a general template can have some registers fail.
    raise_on_first_failure = False
        
    if template_path:
        try:
            with open(template_path, 'r') as f:
                template = f.read()
            processor_family, _cpu_info, _core_id, kwargs, register_info = get_jinja_args(device)
        except IOError:
            print "Warning: unable to open %s, using defaults" % template_path
    
    
    if template is None:
        if name is not None:
            names = name.split() if isinstance(name, basestring) else name
            
            if value is not None:
                if len(names) == 1:
                    read_write_reg_with_suggest(device, [names[0]], values=[value], float_as_int=float_as_int)
                else:
                    #Writing multiple registers (going to assume values is a list type)
                    try:
                        if len(names) == len(value):
                            read_write_reg_with_suggest(device, names, value)
                        else:
                            raise TypeError()
                    except TypeError:
                        raise TypeError('Number of registers does not match the number of values.')
                
            if len(names) == 1:
                return _make_reg_result(device, names[0], read_write_reg_with_suggest(
                    device, names, float_as_int=float_as_int)[0],
                    viewopts, float_as_int=float_as_int)
                
            # for more than one register, use the advanced display
            template = make_reg_template(names, device, float_as_int)
            raise_on_first_failure = True
        else:
            if value is not None:
                if isinstance(value, MultipleRegResult):
                    read_write_reg_with_suggest(device, value.keys(), value)
                    template = make_reg_template(value.keys(), device, float_as_int)
                else:
                    raise TypeError('Value must be a MultipleRegResult when name is None.')
            else:
                #Lookup a template using proc family and core ID
                jinja_args = get_jinja_args(device)
                templates = get_compatible_templates_for_device(jinja_args, use_user=use_user)
                processor_family, _cpu_info, _core_id, kwargs, register_info = jinja_args  
                template = _search_compatible_templates(templates, template_name)
                
                #Might be many matches, otherwise it's just one template, exceptions if none found
                if isinstance(template, RegTemplateList):
                    #Found multiple, tell user that
                    print "Multiple templates found for the name '%s'" % template_name
                    return template
    else:
        #Template given directly
        processor_family, _cpu_info, _core_id, kwargs, register_info = get_jinja_args(device)
            
    layout_view_options = None
        
    #If jinja couldn't be found the env is None, if proc family is not set then we are dealing with a non Jinja template
    if jinja_env is not None and processor_family is not None:
        template, layout_view_options = _render_jinja_template(template, kwargs, register_info, view_options)

    eval = TinyRegisterEvaluator(device)
    #First pass gets the register names
    display_registers(template, eval.build_cache, layout_view_options)
    
    try:
        #No point suggesting names if we're going to try to read individually
        eval.load_cache(viewopts, suggest=raise_on_first_failure, float_as_int=float_as_int)
    except Exception as e:
        if raise_on_first_failure:
            raise
        else:
            print "Warning : Failed to read registers as a block : %s\nReading registers individually." % (str(e),)
    
    return MultipleRegResult(display_registers(template, eval, layout_view_options), eval.reg_result_cache)
    
def _search_compatible_templates(templates, template_name):
    if not templates:
        raise RegsException("No compatible register templates found")
    else:
        if template_name is not None:
            #Search for the name
            template = None
            #Exact equal, lower equal then lower partial
            comparison_funcs = [lambda x: x.name == template_name,
                                lambda x: x.name.lower() == template_name.lower(),
                                lambda x: template_name.lower() in x.name.lower(),
                               ]
                               
            for comparison_func in comparison_funcs:
                results = filter(comparison_func, templates)

                if len(results) == 1:
                    template = results[0]
                elif len(results) > 1:
                    template = RegTemplateList(results)
                    
                if template:
                    #Either a single template or a list of them
                    return template

            if not template:
                raise RegsException("No templates found with a name containing '%s'" % template_name)
            
        else:
            return templates[0]
    
def _render_jinja_template(template, kwargs, register_info, view_options):
    #If the template is passed in directly
    if isinstance(template, TemplateProperties):
        #We've already got the settings
        temp_properties = template
        
        #If it came from a file then it will have a file path
        if temp_properties.file_path:
            print "Using template at %s" % temp_properties.file_path
            template = temp_properties.get_layout_content()
        else:
            template = temp_properties.layout
    else:
        #Expand cells like [$pc]
        template = expand_short_cells(template, register_info)
        
        #Otherwise render once to get the settings
        f = template_error_wrapper(get_template_properties, None, '')
        temp_properties = f(template, kwargs)

    #Second pass uses the default values for the settings
    kwargs.update(temp_properties._get_view_options_dict())
    #Apply any non default options
    kwargs.update(view_options)
    
    #Store a copy of all these view options so they can be given to the grid later
    layout_view_options = temp_properties._get_view_options_dict()
    layout_view_options.update(view_options)
    
    #Do the final render
    template = jinja_env.from_string(template)
    layout = template.render(**kwargs)
    
    #Remove the setting lines
    layout = split_settings_from_template(layout)
    layout = layout.lstrip()
    template = layout
    
    return (template, layout_view_options)
    
class FPUException(Exception):
    pass
        
fpu_template = '''
$ if cpu_info.get('fpu_max_register_size', 32) == 64
    $set is_64 = True
    $ if not cpu_info.get('fpu_split_64bit_mode')
        $set not_split_64 = True
    $ endif
$ endif
[]   as single (.s)                                  [][]                                 [] {% if is_64 %}       []                   as double(.d){% endif %}
f0 : [$f0  floating_point width_bytes=4 as_hex=True] ( [$f0  floating_point width_bytes=4] ) {% if is_64 %}       [$ text text="d0 :"] [$d0  floating_point width_bytes=8 as_hex=True] ( [$d0  floating_point width_bytes=8] ){% endif %}
f1 : [$f1  floating_point width_bytes=4 as_hex=True] ( [$f1  floating_point width_bytes=4] ) {% if not_split_64%} [$ text text="d1 :"] [$d1  floating_point width_bytes=8 as_hex=True] ( [$d1  floating_point width_bytes=8] ){% endif %}
f2 : [$f2  floating_point width_bytes=4 as_hex=True] ( [$f2  floating_point width_bytes=4] ) {% if is_64 %}       [$ text text="d2 :"] [$d2  floating_point width_bytes=8 as_hex=True] ( [$d2  floating_point width_bytes=8] ){% endif %}
f3 : [$f3  floating_point width_bytes=4 as_hex=True] ( [$f3  floating_point width_bytes=4] ) {% if not_split_64%} [$ text text="d3 :"] [$d3  floating_point width_bytes=8 as_hex=True] ( [$d3  floating_point width_bytes=8] ){% endif %}
f4 : [$f4  floating_point width_bytes=4 as_hex=True] ( [$f4  floating_point width_bytes=4] ) {% if is_64 %}       [$ text text="d4 :"] [$d4  floating_point width_bytes=8 as_hex=True] ( [$d4  floating_point width_bytes=8] ){% endif %}
f5 : [$f5  floating_point width_bytes=4 as_hex=True] ( [$f5  floating_point width_bytes=4] ) {% if not_split_64%} [$ text text="d5 :"] [$d5  floating_point width_bytes=8 as_hex=True] ( [$d5  floating_point width_bytes=8] ){% endif %}
f6 : [$f6  floating_point width_bytes=4 as_hex=True] ( [$f6  floating_point width_bytes=4] ) {% if is_64 %}       [$ text text="d6 :"] [$d6  floating_point width_bytes=8 as_hex=True] ( [$d6  floating_point width_bytes=8] ){% endif %}
f7 : [$f7  floating_point width_bytes=4 as_hex=True] ( [$f7  floating_point width_bytes=4] ) {% if not_split_64%} [$ text text="d7 :"] [$d7  floating_point width_bytes=8 as_hex=True] ( [$d7  floating_point width_bytes=8] ){% endif %}
f8 : [$f8  floating_point width_bytes=4 as_hex=True] ( [$f8  floating_point width_bytes=4] ) {% if is_64 %}       [$ text text="d8 :"] [$d8  floating_point width_bytes=8 as_hex=True] ( [$d8  floating_point width_bytes=8] ){% endif %}
f9 : [$f9  floating_point width_bytes=4 as_hex=True] ( [$f9  floating_point width_bytes=4] ) {% if not_split_64%} [$ text text="d9 :"] [$d9  floating_point width_bytes=8 as_hex=True] ( [$d9  floating_point width_bytes=8] ){% endif %}
f10: [$f10 floating_point width_bytes=4 as_hex=True] ( [$f10 floating_point width_bytes=4] ) {% if is_64 %}       [$ text text="d10:"] [$d10 floating_point width_bytes=8 as_hex=True] ( [$d10 floating_point width_bytes=8] ){% endif %}
f11: [$f11 floating_point width_bytes=4 as_hex=True] ( [$f11 floating_point width_bytes=4] ) {% if not_split_64%} [$ text text="d11:"] [$d11 floating_point width_bytes=8 as_hex=True] ( [$d11 floating_point width_bytes=8] ){% endif %}
f12: [$f12 floating_point width_bytes=4 as_hex=True] ( [$f12 floating_point width_bytes=4] ) {% if is_64 %}       [$ text text="d12:"] [$d12 floating_point width_bytes=8 as_hex=True] ( [$d12 floating_point width_bytes=8] ){% endif %}
f13: [$f13 floating_point width_bytes=4 as_hex=True] ( [$f13 floating_point width_bytes=4] ) {% if not_split_64%} [$ text text="d13:"] [$d13 floating_point width_bytes=8 as_hex=True] ( [$d13 floating_point width_bytes=8] ){% endif %}
f14: [$f14 floating_point width_bytes=4 as_hex=True] ( [$f14 floating_point width_bytes=4] ) {% if is_64 %}       [$ text text="d14:"] [$d14 floating_point width_bytes=8 as_hex=True] ( [$d14 floating_point width_bytes=8] ){% endif %}
f15: [$f15 floating_point width_bytes=4 as_hex=True] ( [$f15 floating_point width_bytes=4] ) {% if not_split_64%} [$ text text="d15:"] [$d15 floating_point width_bytes=8 as_hex=True] ( [$d15 floating_point width_bytes=8] ){% endif %}
f16: [$f16 floating_point width_bytes=4 as_hex=True] ( [$f16 floating_point width_bytes=4] ) {% if is_64 %}       [$ text text="d16:"] [$d16 floating_point width_bytes=8 as_hex=True] ( [$d16 floating_point width_bytes=8] ){% endif %}
f17: [$f17 floating_point width_bytes=4 as_hex=True] ( [$f17 floating_point width_bytes=4] ) {% if not_split_64%} [$ text text="d17:"] [$d17 floating_point width_bytes=8 as_hex=True] ( [$d17 floating_point width_bytes=8] ){% endif %}
f18: [$f18 floating_point width_bytes=4 as_hex=True] ( [$f18 floating_point width_bytes=4] ) {% if is_64 %}       [$ text text="d18:"] [$d18 floating_point width_bytes=8 as_hex=True] ( [$d18 floating_point width_bytes=8] ){% endif %}
f19: [$f19 floating_point width_bytes=4 as_hex=True] ( [$f19 floating_point width_bytes=4] ) {% if not_split_64%} [$ text text="d19:"] [$d19 floating_point width_bytes=8 as_hex=True] ( [$d19 floating_point width_bytes=8] ){% endif %}
f20: [$f20 floating_point width_bytes=4 as_hex=True] ( [$f20 floating_point width_bytes=4] ) {% if is_64 %}       [$ text text="d20:"] [$d20 floating_point width_bytes=8 as_hex=True] ( [$d20 floating_point width_bytes=8] ){% endif %}
f21: [$f21 floating_point width_bytes=4 as_hex=True] ( [$f21 floating_point width_bytes=4] ) {% if not_split_64%} [$ text text="d21:"] [$d21 floating_point width_bytes=8 as_hex=True] ( [$d21 floating_point width_bytes=8] ){% endif %}
f22: [$f22 floating_point width_bytes=4 as_hex=True] ( [$f22 floating_point width_bytes=4] ) {% if is_64 %}       [$ text text="d22:"] [$d22 floating_point width_bytes=8 as_hex=True] ( [$d22 floating_point width_bytes=8] ){% endif %}
f23: [$f23 floating_point width_bytes=4 as_hex=True] ( [$f23 floating_point width_bytes=4] ) {% if not_split_64%} [$ text text="d23:"] [$d23 floating_point width_bytes=8 as_hex=True] ( [$d23 floating_point width_bytes=8] ){% endif %}
f24: [$f24 floating_point width_bytes=4 as_hex=True] ( [$f24 floating_point width_bytes=4] ) {% if is_64 %}       [$ text text="d24:"] [$d24 floating_point width_bytes=8 as_hex=True] ( [$d24 floating_point width_bytes=8] ){% endif %}
f25: [$f25 floating_point width_bytes=4 as_hex=True] ( [$f25 floating_point width_bytes=4] ) {% if not_split_64%} [$ text text="d25:"] [$d25 floating_point width_bytes=8 as_hex=True] ( [$d25 floating_point width_bytes=8] ){% endif %}
f26: [$f26 floating_point width_bytes=4 as_hex=True] ( [$f26 floating_point width_bytes=4] ) {% if is_64 %}       [$ text text="d26:"] [$d26 floating_point width_bytes=8 as_hex=True] ( [$d26 floating_point width_bytes=8] ){% endif %}
f27: [$f27 floating_point width_bytes=4 as_hex=True] ( [$f27 floating_point width_bytes=4] ) {% if not_split_64%} [$ text text="d27:"] [$d27 floating_point width_bytes=8 as_hex=True] ( [$d27 floating_point width_bytes=8] ){% endif %}
f28: [$f28 floating_point width_bytes=4 as_hex=True] ( [$f28 floating_point width_bytes=4] ) {% if is_64 %}       [$ text text="d28:"] [$d28 floating_point width_bytes=8 as_hex=True] ( [$d28 floating_point width_bytes=8] ){% endif %}
f29: [$f29 floating_point width_bytes=4 as_hex=True] ( [$f29 floating_point width_bytes=4] ) {% if not_split_64%} [$ text text="d29:"] [$d29 floating_point width_bytes=8 as_hex=True] ( [$d29 floating_point width_bytes=8] ){% endif %}
f30: [$f30 floating_point width_bytes=4 as_hex=True] ( [$f30 floating_point width_bytes=4] ) {% if is_64 %}       [$ text text="d30:"] [$d30 floating_point width_bytes=8 as_hex=True] ( [$d30 floating_point width_bytes=8] ){% endif %}
f31: [$f31 floating_point width_bytes=4 as_hex=True] ( [$f31 floating_point width_bytes=4] ) {% if not_split_64%} [$ text text="d31:"] [$d31 floating_point width_bytes=8 as_hex=True] ( [$d31 floating_point width_bytes=8] ){% endif %}

$ if cpu_info.get('cpu_name') != "I6400"
FCCR: [$FCCR hex width=8]
$ endif
FCSR: [$FCSR hex width=8]
FENR: [$FENR hex width=8]
FEXR: [$FEXR hex width=8]
FIR : [$FIR  hex width=8]
'''

@command(vpe_required=True)
def fpu(device=None):
    '''Display CP1/fpu registers if an FPU is present.'''
    if not dict(device.tiny.CpuInfo())['has_fpu']:
        raise FPUException('No FPU found')
    return regs(template=fpu_template)

def is_64_bit(device):
    return not dict(device.da.CpuInfo())['cpu_is_32bit']
    
def generate_template_with_existing_regs(registers, cols, include_all_registers, device, guest, reg_names_64=None):
    if reg_names_64 is None:
        reg_names_64 = []

    #If there's a regdb we can narrow down the list
    if device.regdb and not include_all_registers:
        _regs = [reg for reg in registers if device.regdb.does_register_exist(reg)]
    else:
        _regs = registers
        
    #Check number of cols (0 or -ve not allowed)
    if cols <= 0:
        raise ValueError("Invalid number of columns (%d)" % cols) 
    
    #Split names into chucks of cols length
    rows = [_regs[n:n+cols] for n in range(0, len(_regs), cols)]
        
    # name [$name hex width=x]
    base_string = "%s [$%s hex width=%d]"
    ret_str = []
    
    is64 = is_64_bit(device)
    for row in rows:
        row_str = []
        for name in row:
            if guest:
                name = 'guest_' + name
            width = 16 if name in reg_names_64 and is64 else 8
            row_str.append(base_string % (name, name, width))
        ret_str.append(' '.join(row_str))
        
    return '\n'.join(ret_str)
    
@command(vpe_required=True, show_all=[(all, True)])
def cp0(show_all=False, guest=False, device=None):
    '''Display all CP0 registers.
    
    If register information is available only registers which are present
    on the target will be shown. To show all registers set show_all to True,
    to show guest registers set guest to True.'''
    cp0_names = ['cp0.%d.%d' % (index, sel) for index in range(32) for sel in range(8)] 
    cp0_regs = [device.registers_info_by_name[n] for n in cp0_names]

    cp0_64bit_names = []
    for r in cp0_regs:
        if r.size64 == 8:
            if r.aliases:
                cp0_64bit_names.extend(r.aliases)
            cp0_64bit_names.append(r.name)

    return regs(template=generate_template_with_existing_regs(
                    [r.name for r in cp0_regs], 
                    4, 
                    show_all, 
                    device, 
                    guest,
                    reg_names_64=cp0_64bit_names)
                )

if __name__ == "__main__":
    import doctest
    doctest.testmod()
