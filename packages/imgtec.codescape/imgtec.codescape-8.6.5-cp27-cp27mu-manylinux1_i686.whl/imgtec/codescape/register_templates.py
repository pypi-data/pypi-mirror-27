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

import sys, os, re, traceback
if __name__ == "__main__":
    sys.path.insert(0, "../../..")

from jinja2 import Environment, TemplateSyntaxError, TemplateError
from copy import copy
from textwrap import dedent

from imgtec.lib.complex_helpers import calculate_Q_format_width_and_precision, extract_bits
from imgtec.lib.complex_helpers import complex_separator, nibble_align_shift_offset, sign_extend
from imgtec.lib.conversions import word_to_float, word_to_fixed, float_to_word, wrap_value, fixed_to_word, word_to_signed

jinja_env = Environment()
jinja_env.globals.update(dict(zip=zip, max=max, min=min, any=any))
jinja_env.line_statement_prefix = '$'

class FormatException(Exception):
    pass
    
class TemplateSettingsException(FormatException):
    pass
    
class WrappedTemplateException(Exception):
    '''
    This is used to wrap lower level exceptions with some extra info when they
    are going to propagate up to the error wrapper. At that point the original 
    exception will be re-raised and the extra info used to determine the correct
    error message.
    '''
    def __init__(self, e, layout, line_number=None):
        self.e = e
        self.layout = layout
        self.line_number = line_number
    
    def __str__(self):
        return self.e.__str__()
    
def template_error_wrapper(function, notifier, filename):
    def inner(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        #Has extra info we can use
        except TemplateSyntaxError as e:
            if notifier:
                notifier.signal(e.message + ' on line ' + str(e.lineno) + ' in template: ' + filename)
            raise e
        #Anything less specific
        except TemplateError as e:
            if notifier:
                notifier.signal(e.message + ' in template: ' + filename)
            raise e
        except TemplateSettingsException as e:
            if notifier:
                notifier.signal("Settings error in template %s: %s" % (filename, str(e)), layout=None)
            raise e
        except WrappedTemplateException as e:
            if notifier:
                err = "Error parsing template %s" % filename
                if e.line_number is not None:
                    err += " at line %d" % e.line_number
                err += " : %s" % str(e)
                notifier.signal(err, layout=e.layout, line_number=e.line_number)
            #This raises the original exception
            raise e.e
        except Exception as e:
            if notifier:
                notifier.signal("Error parsing template %s: %s" % (filename, str(e)), layout=None)
            raise e
    return inner
    
def get_compatible_templates(id_to_file, processor_family, core_id, insert_null=True):
    family = id_to_file.get(processor_family, {})
    
    #Find the templates that apply to the given family AND core ID
    templates = copy(family.get(core_id, []))
    
    #Add any generic family templates (copy so you don't end up putting the 
    #generic template everywhere when you search)
    templates.extend(copy(family.get('any', [])))
    
    #Remove disabled templates
    templates = [template for template in templates if template.enabled]

    if insert_null:
        templates.append(NullTemplateProperties())
        
    return templates
    
def remove_templates(mapping, file_paths):
    #Remove any templates which have the given file paths
    #To solve the problem of a user editing a template, deleting the copy, then
    #re-editing the template and getting two entries in the menu, which reference
    #the same file.
    
    if not file_paths:
        return
    
    #Visit every entry in case the edit had its family/Core ID changed
    for family in mapping:
        for core_id in mapping[family]:
            templates = mapping[family][core_id]
            templates = [temp for temp in templates if temp.file_path not in file_paths]
            mapping[family][core_id] = templates
            
def insert_template_from_properties(mapping, template, version):
    #Insert a template using the given properties object, no rendering required.

    #If template is compatible
    if template.is_compatible(version):
        #Must at least have a family
        if template.processor_family is None:
            return
        
        #If the template has no core IDs it can be used for any of that family
        if len(template.core_ids) == 0:
            template.core_ids.append('any')
            
        family = template.processor_family
        core_ids = template.core_ids
        
        #If the family is new
        if mapping.get(family) is None:
            #Make an empty dict for it
            mapping[family] = {}
            
        for core_id in core_ids:
            #Create a list if one isn't there already
            if mapping[family].get(core_id) is None:
                mapping[family][core_id] = [template]
            else:
                mapping[family][core_id].append(template)
    
def insert_template(mapping, contents, dir, filename, version, regmodel, notifier=None):
    #Add a template to the mapping structure in the correct place
    template = template_error_wrapper(get_template_properties, notifier, filename)
    try:
        template = template(contents, kwargs=regmodel.template_keyword_args)
    except:
        return
        
    template.file_path = os.path.join(dir, filename)
    insert_template_from_properties(mapping, template, version)
                
def scan_templates(dirs, regmodel, version, notifier=None, mapping=None):
    #Returns a dictionary of the form:
    # {
    #  'family_name' : {
    #    core_id : [template_one, template_two],
    #    ...
    #  },
    #  'other_family' : {
    #    ...
    #  },
    # }
    
    id_to_file = mapping if mapping else {}
    
    for dir in dirs:
        #Get all .txt files in the directory
        try:
            files = [file for file in os.listdir(dir) if os.path.isfile(os.path.join(dir, file))]
            files = [file for file in files if os.path.splitext(file)[1] == '.txt']
        except OSError:
            files = []

        for file in files:
            full_path = os.path.join(dir, file)
            with open(full_path) as f:
                insert_template(id_to_file, f.read(), dir, full_path, version, regmodel, notifier)
                
    return id_to_file
    
def change_template_setting(content, setting, new_value):
    #Find and change the given setting line to a new value
    #not going to render for the time being so assume the line could be anywhere
    #Replaces all instances, intended for use with things like name and version
    return re.sub(template_settings_pattern(setting), ''.join(['# ', setting, '=', new_value]), content)
    
class TemplateProperties(object):
    def __init__(self, core_ids=None, coding=None, version=None, name=None, 
        file_path=None, processor_family=None, view_options=None, layout='',
        enabled = True):
        self.core_ids  = core_ids or []
        self.coding    = coding
        self.name      = name
        self.file_path = file_path
        self.view_options = view_options or []
        self.version = version
        self.processor_family = processor_family
        self.layout = layout
        self.enabled = enabled

    def _as_tuple(self):
        return (self.core_ids, self.coding, self.name, self.file_path, 
                self.version, self.processor_family, self.view_options, 
                self.layout, self.enabled)
        
    def __cmp__(self, other):
        return cmp(self._as_tuple(), other._as_tuple())
        
    def __repr__(self):
        core_ids = ['Core IDs:']
        core_ids.extend(['0x%x,' % core_id if core_id != 'any' else core_id for core_id in self.core_ids])
        return '<TemplateProperties %s at %s>' % (''.join(core_ids), str(self.file_path))
        
    def is_compatible(self, version):
        #Return true if template is compatible with the given region version
        if version is not None and self.version is not None:
            return float(version) >= float(self.version)
        else:
            return False
            
    def get_layout_content(self):
        #Returns the contents of the template file
        #Override to make a template based on some other source
        if self.file_path:
            with open(self.file_path, 'r') as f:
                return f.read()
        else:
            return ''
            
    def _get_view_options_dict(self):
        return dict((op.name, op.value) for op in self.view_options)
        
    def get_options(self):
        '''
        Get a dictionary of name->default value pairs for every user accessible option.
        Any option which is not an open/close menu or a separator.
        '''
        return dict((op.name, op.value) for op in self.view_options if op.is_user_option)
        
    def get_region_options(self):
        '''
        Get a list of options which are to be shown in the region itself
        in addition to the menus.
        '''
        return [opt for opt in self.view_options if opt.show_in_region]
            
class NullTemplateProperties(TemplateProperties):
    def get_layout_content(self):
        return dedent('''\
            No compatible layout found.
            
            Expected Template Version: [$ text text="{{ REGION_VERSION }}"]
            Target: [$ text text="{{ TARGET_NAME }}"]
            Core ID: [$ text text="{{ CORE_ID }}"]
            Processor Family: [$ text text="{{ PROCESSOR_FAMILY }}"]
            ABI: [$ text text="{{ ABI }}"]
            CPU Info:
            {%- for key, value in cpu_info.iteritems() %}
            [] {{key}} = {{value}}
            {%- endfor %}
            Registers:
            {% for regs in registers|batch(10) -%}
            [] {% for reg in regs %}{{reg}}{% if not loop.last %}, {% endif %}{% endfor %}
            {% endfor %}
            ''')
            
def jinja_line_number_from_exception(tb):
    pattern = pattern = r'\s*File "<template>", line (?P<lineno>\d+),'
    m = re.search(pattern, tb)
    if m:
        return int(m.group('lineno'))
    else:
        return None
 
def get_template_properties(layout, kwargs={}):
    #Contents of file is passed in, including the settings lines
    #kwargs are target properties, such as whether an FPU is present
    setting_lines = []
    
    #Render here so that jinja blocks can be used to filter settings too
    try:
        layout = jinja_env.from_string(layout)
        layout = layout.render(**kwargs)
    except Exception as e:
        tb = traceback.format_exc()
        line_number = jinja_line_number_from_exception(tb)
        raise WrappedTemplateException(e, None, line_number=line_number)

    #Settings begin with '#'
    for line in layout.splitlines():
        #Settings finish at the first line without '#'
        if not line.startswith('#'):
            break
        
        setting_lines.append(line)
    
    settings = parse_template_settings(setting_lines)
    
    valid_settings = {
    'name'            : lambda x:x,
    'core_ids'        : line_to_int_list,
    'processor_family': lambda x:x,
    'coding'          : lambda x:x,
    'version'         : lambda x:float(x),
    'view_option'     : line_to_options_list,
    'enabled'         : lambda x:to_bool(x),
    }
    
    settings_obj = TemplateProperties()
    settings_obj.layout = layout
    
    for setting in settings:
        if setting in valid_settings:
            #Call conversion function for that setting
            name  = setting
            value = valid_settings[name](settings[name])
            #View options are one per line but many lines
            if setting in ['view_option']:
                name += 's'
            setattr(settings_obj, name, value)
        else:
            raise TemplateSettingsException('Unknown template setting "%s".' % setting)

    return settings_obj
    
VIEW_OPT_MENU_SEPARATOR = '---'
VIEW_OPT_MENU_OPEN      = '>>>'
VIEW_OPT_MENU_CLOSE     = '<<<'
    
class TemplateViewOption(object):
    def __init__(self, display_string, variable_name, value, enable, show_in_region):
        #The string shown on the menu item
        self.string = display_string
        #Internal name, used in the template
        self.name   = variable_name
        #The default value for this option
        self.value  = value
        #Whether the option is enabled in the menu
        self.enable = enable
        #Whether the option is shown in the region itself
        self.show_in_region = show_in_region
        
        self.is_radio       = '|' in self.string
        self.is_separator   = self.string == VIEW_OPT_MENU_SEPARATOR
        self.is_open_menu   = self.string == VIEW_OPT_MENU_OPEN
        self.is_close_menu  = self.string == VIEW_OPT_MENU_CLOSE
        #Any option that a user can click on
        self.is_user_option = not any([self.is_separator, self.is_open_menu, self.is_close_menu])
        
        if self.is_radio:
            self.radio_options = [x.strip() for x in self.string.split('|')]
        else:
            self.radio_options = []
        
    def menu_items(self, prefix):
        """Returns list of (display, action, value) tuples.
        
        For normal options this is a list of length 1, but radio
        options return 1 per option.
        
        The returned action is prefix + option.name, and if it is a radio
        option then the current index is used as well.
        """
        if self.is_radio:
            return [(opt, '%s%s%d' % (prefix, self.name, n), n) for n, opt in enumerate(self.radio_options)]
        return [(self.string, prefix + self.name, None)]
                
    def _as_tuple(self):
        return (self.string, self.name, self.value, self.enable, self.show_in_region)
        
    def __cmp__(self, other):
        return cmp(self._as_tuple(), other._as_tuple())
        
    def __repr__(self):
        return "TemplateViewOption(%s, %s, %s %s)" % (self.string, self.name, self.value, self.enable)

def line_to_options_list(line):
    '''
    Take a line in the form...
    display name : variable name : default value, repeated
    E.g. Show floating point registers : SHOW_FPU_REG : False
    and return a list of view option objects
    '''
    options = []
    
    #Split line by commas
    lines = line.split(',')
    
    for option in lines:
        #Split into properties
        prop = [item.strip() for item in option.split(':')]
        
        #If it is a menu separator or end of a nested menu
        if len(prop) == 1 and prop[0] in [VIEW_OPT_MENU_SEPARATOR, VIEW_OPT_MENU_CLOSE]:
            #Add fake values and process normally
            prop.extend([prop[0], False])
            
        #Start of a nested menu, must have a name also
        if len(prop) == 2 and prop[0] == VIEW_OPT_MENU_OPEN and prop[1]:
            prop.append(False)
            
        if len(prop) != 5:
            #Doesn't have enable or show in region
            if len(prop) == 3:
                #Enabled by default
                prop.append(True)
                
            if len(prop) == 4:
                #Not shown in the region by default
                prop.append(False)
                
            if len(prop) != 5:
                #Ignore malformed options
                continue
        
        display_string, variable_name, default_value, enable, show_in_region = prop
        try:
            default_value = to_int(default_value)
        except ValueError:
            default_value = to_bool(default_value)
        enable = to_bool(enable)
        show_in_region = to_bool(show_in_region)
        options.append(TemplateViewOption(display_string, variable_name, 
            default_value, enable, show_in_region))
        
    return options
    
def line_to_int_list(line):
    #Convert comma separated string to a list of integers
    if not line:
        return []
    int_list = line.split(',')
    ints = []
    
    for item in int_list:
        try:
            ints.append(int(item, 0))
        except ValueError:
            pass

    return ints
    
def template_settings_pattern(setting=None):
    #Return pattern to match a specific setting, or any line that looks like a
    #setting with the name in group 1 and value in group 2.
    
    if not setting:
        #Match any setting
        setting = '\w+'
        
    return ''.join(['#',              # Line starts with #
                    '\s*'             # possible spaces
                    '(', setting, ')' # name of the setting
                    '\s*',            # possible spaces
                    '[:=]',           # Either symbol
                    '\s*',            # more space
                    '(.+)',           # value of the setting
                    ])
    
def parse_template_settings(lines):
    #Returns a dictionary with pairs setting_name:line
    #both are strings at this point, no conversion is done.
    settings = {}
    for line in lines:
        match = re.match(template_settings_pattern(), line)
        
        if match:
            name, value = match.groups()
            
            #Multi line settings get an exception
            multi_line = ['view_option', 'core_ids']
            if name in multi_line and settings.get(name, None):
                settings[name] = ','.join([settings[name], value])
            else:
                #Single line settings override each other if they appear more than once
                settings[name] = value
            
    return settings
    
def split_settings_from_template(layout):
    #Remove settings lines and return the register layout only
    lines = layout.splitlines()
    while lines:
        if not lines[0] or lines[0][0] != '#':
            break
        else:
            lines.pop(0)
    
    return '\n'.join(lines)

def format_fixed(value, fixed_widths, field_length):
    # check for negative values (top bit set), if so we would need to sign extend.
    if (value & 1 << sum(fixed_widths)) and value > 0:
        # create the negative by moving the value down the number range (masking method does not work
        # in python as the numbers just get bigger and don't wrap into a negative value)
        max_range = 1 << (sum(fixed_widths) + 1)
        if value >= max_range:
            print "warning: fixed point number greater than valid range"
        value = value - max_range        
    #The fixed widths are the number of bits either side of the decimal point, field length is the chars
    return "%*.*f" % (field_length[0], field_length[1], word_to_fixed(value, fixed_widths[0]))

class ModelRegisterEvaluator(object):
    def __init__(self, model):
        self.model = model
        
    def __call__(self, expression):
        if expression.startswith('$'):
            name = self.model.make_reg_name(expression[1:])
            return self.model.regvals.get(name.lower(), None)
        elif expression.startswith('#'):
            return self.model.symvals.get(expression, None)
  
class BaseCell(object):
    def __init__(self, expression, read_only=False, show_grey=False, editor_prefix='', editor_postfix='',
        can_overtype=False, left_align=False, bit_start=0, bit_end=32, is_break=False):
        
        #The first render after the most recent stop, used to compare current with to show changes
        self.first_render = None
        #The most recent render, compared with first_render and used to set first_render
        self.last_render = None
        #Of the form '$foo' (case sensitive, as it is used to read symbols also)
        self.expression = expression
        #E.g. if expression = '$foo' then the name is 'foo'
        self.name = self.expression[1:].lower() if self.expression else None
        #Can the cell be modified
        self._read_only = to_bool(read_only)
        self.editor_prefix = editor_prefix
        #The string which appears before the value in a popup editor, e.g. '0x'
        #The string which appears after the value, e.g. '_f'
        self.editor_postfix = editor_postfix
        #Whether the cell can be typed on to modify it
        self.can_overtype = to_bool(can_overtype)
        #Does the cell contain content that could change
        self.should_refresh = True
        self.show_grey = to_bool(show_grey)
        self.left_align = to_bool(left_align)
        #The actual width of the source register, None if not known
        self.real_width_bytes = None
        #Whether this cell starts a new section for alignment purposes
        self.is_break = to_bool(is_break)
        
        self.is_memory_mapped = self.expression.startswith('#') if self.expression else False
        
        self.bit_start = to_int(bit_start)
        self.bit_end   = to_int(bit_end)
        self.num_bits = self.bit_end-self.bit_start+1
        self.width_bytes = self.num_bits//8
        
        #Display options, every cell has them to simplify setting them from the grid.
        self._show_floating_point_as_hex = False
        self._show_fixed_point_as_hex = False
        self._show_fixed_point_as_complex = False
        self._show_6bit_as_left_aligned_hex = False
        
    def __repr__(self):
        return "BaseCell('%s')" % self.expression

    @property
    def direct_edit(self):
        #Can this cell be popup edited without modifications?
        return True
        
    @property
    def is_full_register(self):
        if self.real_width_bytes is not None:
            #Use num_bits to get an exact match
            return self.num_bits == (self.real_width_bytes*8)
        else:
            return False
        
    @property
    def read_only(self):
        return self._read_only
        
    @read_only.setter
    def read_only(self, read_only):
        self._read_only = read_only
        
    @property
    def can_inplace_edit(self):
        #Can the cell be edited using the popup editor
        return not self.read_only
    
    @property    
    def is_left_aligned_register(self):
        return self.left_align
        
    @property
    def is_bit_cell(self):
        return False
        
    @property
    def is_float_register(self):
        return False
        
    @property
    def is_double_register(self):
        return False
        
    @property
    def is_floatingpoint_register(self):
        return False
        
    @property
    def is_split_complex_fixedpoint_register(self):
        return False
        
    @property
    def is_complex_fixedpoint_register(self):
        return False
        
    @property
    def is_fixedpoint_register(self):
        return False
        
    def render(self, evaluator):
        if self.should_refresh:
            #Cell has an expression so get real value, or None if the reg is invalid
            value = evaluator(self.expression)
        else:
            #Something that doesn't rely on a register, so the value is irrelevant, but must be not None
            value = 0x0

        if value is not None:        
            #Cells with a valid expression, or that do not depend on one are rendered normally
            render = self._render(value)
        else:
            #Invalid expressions show an error message
            render = "not found"
            
        #Usual history saving always happens
        if not self.first_render:
            self.first_render = render
            
        '''
        first_render is compared to the latest render to do difference highlighting
        last_render is a saved copy of the latest render, which may be used to 
        set first_render, instead of having to re-render everything (e.g. when target steps)
        '''
        self.last_render = render
        return render
    
    def _render(self, value):
        return "%i" % value
        
    def create_nibble_modify_fn(self, mask, nibble):
        #Default, assuming a whole integer register beginning at bit 0
        return lambda x: ((x & mask) | (nibble & ~mask))
        
    def create_adjust_func(self, delta):
        #Used when incrementing/decrementing a register
        return lambda x: x + delta
        
    def create_hex_adjust_function(self, delta):
        #Generic adjust function for hex format cells that are not a whole register
        def adjust(value):
                #Get relevant bits
                field = extract_bits(value, self.bit_start, self.bit_end + 1, False)
                #Apply the adjustment
                field += delta
                #Check for wrap
                field = wrap_value(field, self.num_bits)
                #Mask for the section we're modifying
                mask = ((2**self.num_bits)-1) << self.bit_start
                # Zero the old section
                value &= ~mask
                #Or in the new section value
                value |= (field << self.bit_start)
                return value
                
        return adjust
        
    def create_nibble_edit_shift_and_mask(self, char_index):
        shift = (((self.num_bits//4) - char_index - 1) * 4) + self.bit_start
        mask  = 0xf << shift
        return (shift, ~mask)
        
    def mask_editor_change_hex(self, original, new):
        #Mask and shift the new value based on the cell's properties.
        new = wrap_value(new, self.num_bits)
        mask = ((2**self.num_bits)-1) << self.bit_start
        #Clear the section in the original value
        original &= ~mask
        #Add in new value
        original |= (new << self.bit_start)
        return original
        
    def get_tooltip_string(self, evaluator):
        value = evaluator(self.expression)
        
        #If it is a valid register
        if value is not None:
            return unicode('0x%x : %d : %d' % (value, value, word_to_signed(value, self.width_bytes)))
        else:
            return unicode("'%s' is not present or cannot be read at this time." % self.name)
        
class FloatingPointCell(BaseCell):
    def __init__(self, expression, format='%g', width_bytes=4, read_only=False,
        show_grey=False, as_hex=False, bit_start=0, is_break=False):
        bit_end = to_int(bit_start) + ((to_int(width_bytes)*8)-1)
        BaseCell.__init__(self, expression, read_only, show_grey, bit_start=bit_start, bit_end=bit_end, is_break=is_break)
        self.ShowFloatingPointAsHex = to_bool(as_hex)
        self.format = format
    
    def __repr__(self):
        return "FloatingPointCell(%r, width_bytes='%i')" % (self.expression, self.width_bytes)
        
    @property
    def is_float_register(self):
        return True
        
    @property
    def is_double_register(self):
        return True
        
    @property
    def is_floatingpoint_register(self):
        return True
        
    @property
    def direct_edit(self):
        return self.is_full_register
        
    @property
    def ShowFloatingPointAsHex(self):
        return self._show_floating_point_as_hex
        
    @ShowFloatingPointAsHex.setter
    def ShowFloatingPointAsHex(self, as_hex):
        self._show_floating_point_as_hex = as_hex
        self.editor_prefix = '0x' if as_hex else ''
        if as_hex:
            self.editor_postfix = '_d' if self.width_bytes==8 else '_f'
        else:
            self.editor_prefix = ''
        self.can_overtype = as_hex
     
    def _render(self, value):
        #bit_end is 0 indexed
        value = extract_bits(value, self.bit_start, self.bit_end+1, False)
        
        if self.ShowFloatingPointAsHex:
            format = "%0" + str(self.width_bytes*2) + "X"
            return format % value
        else:
            return self.format % word_to_float(value, self.width_bytes)
            
    def create_adjust_func(self, delta):
        if self.is_full_register:
            return super(FloatingPointCell, self).create_adjust_func(delta)
        elif self.ShowFloatingPointAsHex:
            return self.create_hex_adjust_function(delta)
        else:
            def adjust(value):
                #Value is the value of the whole register
                #Get the part we want
                to_modify = extract_bits(value, self.bit_start, self.bit_end+1)
                #Convert to a float
                to_modify = word_to_float(to_modify, self.width_bytes)
                #Apply delta (to the float value)
                to_modify += delta
                #Convert back to a word
                to_modify = float_to_word(to_modify, self.width_bytes)
                
                #Remove the old section
                mask = ((2**self.num_bits)-1) << self.bit_start
                value &= ~mask
                #Add the new one
                value |= (to_modify << self.bit_start)
                
                return value
            return adjust
        
class FixedPointComplexCell(BaseCell):
    def __init__(self, expression, width_m=16, width_n=16, as_hex=False, 
        read_only=False, show_grey=False, as_complex=False, left_align=False, is_break=False):
        self.width_m = to_int(width_m)
        self.width_n = to_int(width_n)
        #Bit start assumed always 0 for the time being
        bit_end = self.width_m+self.width_n+1
        BaseCell.__init__(self, expression, read_only, show_grey, left_align=left_align, 
            bit_start=0, bit_end=bit_end, is_break=is_break)
        self.ShowFixedPointAsComplex = to_bool(as_complex)
        self.ShowFixedPointAsHex = to_bool(as_hex)
        
    def __repr__(self):
        return "FixedPointComplexCell('%s', width_m=%d, width_n=%d)" % (self.expression, self.width_m, self.width_n)
        
    @property
    def can_inplace_edit(self):
        #Can the cell be edited using the popup editor
        return not self.read_only and not self.ShowFixedPointAsComplex
        
    @property
    def is_split_complex_fixedpoint_register(self):
        return True
        
    @property
    def is_complex_fixedpoint_register(self):
        return True
        
    @property
    def is_fixedpoint_register(self):
        return True
        
    @property
    def ShowFixedPointAsHex(self):
        return self._show_fixed_point_as_hex
    
    @ShowFixedPointAsHex.setter
    def ShowFixedPointAsHex(self, as_hex):
        self._show_fixed_point_as_hex = as_hex
        #'0x' is only needed when the display is a single hex, not a split value
        self.editor_prefix = '0x' if (as_hex and not self.ShowFixedPointAsComplex) else ''
        #Overtyping should be possible in any hex mode
        self.can_overtype = as_hex
        
    @property
    def ShowFixedPointAsComplex(self):
        return self._show_fixed_point_as_complex
        
    @ShowFixedPointAsComplex.setter
    def ShowFixedPointAsComplex(self, as_complex):
        self._show_fixed_point_as_complex = as_complex
        #Also set here because the order in which the two attributes are set isn't always the same 
        self.editor_prefix = '0x' if (self.ShowFixedPointAsHex and not self.ShowFixedPointAsComplex) else ''
        
    def create_nibble_edit_shift_and_mask(self, char_index):
        if self.ShowFixedPointAsComplex:
            #The end of the first hex chunk
            half_cell_char_width = self.calculate_half_hex_split_width()
            start_second_half = half_cell_char_width + len(complex_separator())
            
            if char_index >= half_cell_char_width and char_index < start_second_half:
                # on the complex separator, do nothing
                return (0, ~0)                     
            else:
                fixed_widths, split_pos = self.get_complex_split_pos_info()
                nibble_offset = nibble_align_shift_offset(0, split_pos, self.is_left_aligned_register)
                if char_index < half_cell_char_width:
                    shift = split_pos + (half_cell_char_width - char_index - 1) * 4 - nibble_offset
                    mask = 0xf if shift >= (nibble_offset + split_pos) else (0xf >> nibble_offset) << nibble_offset
                else:            
                    shift = (start_second_half + half_cell_char_width - char_index - 1) * 4 - nibble_offset
                    mask = 0xf if shift >= nibble_offset else (0xf >> nibble_offset) << nibble_offset
                    
            mask = mask << shift if shift >= 0 else mask >> -shift
            
            return (shift, ~mask)
        else:
            return super(FixedPointComplexCell, self).create_nibble_edit_shift_and_mask(char_index)
        
    def calculate_half_hex_split_width(self):
        width = (self.width_m+self.width_n+1) // 8
        #Divide by two as we're finding the middle point
        fixed_widths = (self.width_m >> 1, self.width_n >> 1)
        # do we need to add 1 to account for a half nibble
        if (sum(fixed_widths) + 1) % 4: 
            width = width + 1
        return width
        
    def get_complex_split_pos_info(self):
        fixed_widths = (self.width_m, self.width_n)
        split_pos = (sum(fixed_widths) + 1) // 2
        return (fixed_widths, split_pos)
        
    def _render(self, value):
        #Complex number as 2 hex numbers
        if self.ShowFixedPointAsHex and self.ShowFixedPointAsComplex:
            
            fixed_width = (self.width_m, self.width_n)
            split_pos = (fixed_width[0] + fixed_width[1] + 1) //2
            split_values = (extract_bits(value, split_pos, split_pos * 2, self.left_align), extract_bits(value, 0, split_pos, self.left_align))
            
            width = 8 //2 #Assuming 8 chars per register
            if (sum(fixed_width) + 1) % 4:
                width += 1
            half_cell_char_width = width
            
            return "%0*X" % (half_cell_char_width, split_values[0]) + complex_separator() + "%0*X" % (half_cell_char_width, split_values[1])
         
        #Single hex number
        elif self.ShowFixedPointAsHex:
            #Assume not left align for the time being
            num_bits  = (self.width_n + self.width_m + 1)
            hex_value = extract_bits(value, 0, num_bits, False)
            num_chars = num_bits//4
            return "%0*X" % (num_chars, hex_value)
        
        #Complex number as two fixed points
        elif self.ShowFixedPointAsComplex:            
            split_pos = (self.width_m + self.width_n + 1) //2
            left_aligned = False #Never left align
            split_values = (extract_bits(value, split_pos, split_pos * 2, left_aligned), extract_bits(value, 0, split_pos, left_aligned))

            #For the next part shift down and order m,n as this is what calculate_q... expects
            fixed_width = (self.width_n >> 1, self.width_m >> 1)
            half_cell_char_width = calculate_Q_format_width_and_precision(fixed_width)
            return format_fixed(split_values[0], 
                                fixed_width, 
                                half_cell_char_width) + complex_separator() + format_fixed(split_values[1], 
                                fixed_width, 
                                half_cell_char_width)
        
        #Actual fixed point
        else:
            fixed_width = (self.width_n, self.width_m)
            display_width = calculate_Q_format_width_and_precision(fixed_width)
            return format_fixed(value, fixed_width, display_width)
        
class FixedPointCell(BaseCell):
    def __init__(self, expression, width_m=0, width_n=0, read_only=False, 
        as_hex=False, show_grey=False, left_align=False, bit_start=0, is_break=False):
        self.width_n             = to_int(width_n)
        self.width_m             = to_int(width_m)
        bit_end = to_int(bit_start)+self.width_m+self.width_n
        BaseCell.__init__(self, expression, read_only, show_grey, 
            left_align=left_align, bit_start=bit_start, bit_end=bit_end, is_break=is_break)
        self.ShowFixedPointAsHex = to_bool(as_hex)
        
    def __repr__(self):
        return "FixPointCell('%s', width_m=%d, width_n=%d)" % (self.expression, self.width_m, self.width_n)
        
    @property
    def direct_edit(self):
        return self.is_full_register

    @property
    def is_complex_fixedpoint_register(self):
        return True
        
    @property
    def is_fixedpoint_register(self):
        return True
        
    @property
    def ShowFixedPointAsHex(self):
        return self._show_fixed_point_as_hex
            
    def create_adjust_func(self, delta):
        return self.create_hex_adjust_function(delta)
            
    @ShowFixedPointAsHex.setter
    def ShowFixedPointAsHex(self, as_hex):
        self._show_fixed_point_as_hex = as_hex
        self.editor_prefix = '0x' if as_hex else ''
        self.can_overtype = as_hex
        
    def _render(self, value):
        fixed_width = (self.width_m, self.width_n)
        value = extract_bits(value, self.bit_start, self.bit_start + self.num_bits, False)
        
        if self.ShowFixedPointAsHex:
            #Assume not left align for the time being
            num_chars = self.num_bits//4
            return "%0*X" % (num_chars, value)
        else:
            fixed_width = (self.width_n, self.width_m)
            display_width = calculate_Q_format_width_and_precision(fixed_width)
            return format_fixed(value, fixed_width, display_width)

class NumberCell(BaseCell):
    def __init__(self, expression, base='X', fill_char='0', width=8, editor_prefix='',
        read_only=False, show_grey=False, can_overtype=False, left_align=False, 
        bit_start=0, bit_end=0, is_break=False):
        #The bit_start and end args are for hex cell to pass down to the base, number cells won't use them
        
        #If not hex or int, always read only
        _read_only = False if base in ('X', 'x', 'd') and not read_only else True
        self.width = to_int(width)
        
        BaseCell.__init__(self, expression, read_only=_read_only, show_grey=show_grey, 
            editor_prefix=editor_prefix, can_overtype=can_overtype, 
            left_align=left_align, bit_start=bit_start, bit_end=bit_end, is_break=is_break)
            
        self.base = base
        self.fill_char = fill_char
        
    def __repr__(self):
        return "NumberCell('%r', %r)" % (self.expression, self.base)
        
    def _render(self, value):
        return format(value, self.base).rjust(self.width, self.fill_char)
        
class HexCell(NumberCell):
    def __init__(self, expression, width=8, read_only=False, show_grey=False, 
        can_overtype=True, left_align=False, bit_start=0, bit_end=None, is_break=False):
        width = to_int(width)
        if bit_end is None:
            bit_end = (width * 4) - 1 + bit_start
        else:
            bit_end = to_int(bit_end)
        
        NumberCell.__init__(self, expression, base='X', width=width, 
                editor_prefix='0x', read_only=read_only, 
                can_overtype=can_overtype, show_grey=show_grey, left_align=left_align, 
                bit_start=bit_start, bit_end=bit_end, is_break=is_break)
                
    def __repr__(self):
        return "HexCell('%s', width=%d)" % (self.expression, self.width)
        
    @property
    def direct_edit(self):
        return self.is_full_register
        
    def create_adjust_func(self, delta):
        #All hex cells use a custom adjust because even cells starting at bit 0
        #might not be the whole register
        return self.create_hex_adjust_function(delta)
            
    @property
    def ShowNoneFixedPointRegistersLeftAligned(self):
        return self._show_6bit_as_left_aligned_hex
        
    @ShowNoneFixedPointRegistersLeftAligned.setter
    def ShowNoneFixedPointRegistersLeftAligned(self, as_hex):
        self._show_6bit_as_left_aligned_hex = as_hex
        self.editor_prefix = '0x' if as_hex or not self.left_align else ''
        
    def _render(self, value):
        if not self.ShowNoneFixedPointRegistersLeftAligned and self.left_align:
            return "%d" % sign_extend(
                extract_bits(value, 
                             self.bit_start, 
                             self.bit_end + 1, 
                             False), 
                self.bit_end - self.bit_start + 1)
        else:
            bits = extract_bits(value, self.bit_start, self.bit_end + 1, self.left_align)
            return NumberCell._render(self, bits)
            
class DecimalCell(NumberCell):
    def __init__(self, expression, width=1, read_only=False, show_grey=False, is_break=False):
        NumberCell.__init__(self, expression, base='d', width=to_int(width), 
        read_only=read_only, show_grey=show_grey, is_break=is_break)
        
    def __repr__(self):
        return "DecimalCell('%s', width=%d)" % (self.expression, self.width)
    
class FormatCell(BaseCell):
    def __init__(self, expression, format, read_only=False, show_grey=False, can_overtype=True,
        is_break=False):
        BaseCell.__init__(self, expression, read_only, show_grey, can_overtype=can_overtype, is_break=is_break)
        self.format = format
        
    def __repr__(self):
        return "FormatCell('%s', %r)" % (self.expression, self.format)
        
    def _render(self, value):
        """
        >>> FormatCell('$foo', '%i').render(lambda x:10)
        '10'
        >>> FormatCell('$foo', '%X').render(lambda x:10)
        'A'
        >>> FormatCell('$foo', '%08X').render(lambda x:0xABCD)
        '0000ABCD'
        """
        
        return self.format % value
        
class BitsCell(BaseCell):
    def __init__(self, expression, bits, bit_start=0, read_only=False, show_grey=False,
        is_break=False):
        BaseCell.__init__(self, expression, read_only, show_grey, can_overtype=False,
            is_break=is_break)
        
        self.bits = bits
        self.bit_start = to_int(bit_start)
        
    @property
    def is_bit_cell(self):
        return True
        
    @property
    def can_inplace_edit(self):
        return False
        
    def _render(self, value):
        """
        >>> BitsCell('$regname', bits='abcdABCD').render(lambda x:5)
        'aBcD'
        >>> BitsCell('$regname', bits='abcdABCD', bit_start='1').render(lambda x:10)
        'aBcD'
        """
        value >>= self.bit_start
        
        w = len(self)
        bits = []
        for n in range(w):
            offset = w if (value & 1) != 0 else 0
            bits.append(self.bits[len(self) - n - 1 + offset])
            value >>= 1
            
        bits.reverse()
        return ''.join(bits)
        
    def __repr__(self):
        start = (", bit_start=%d" % self.bit_start) if self.bit_start else ''
        return "BitCell('%s', bits=%r%s)" % (self.expression, self.bits, start)
        
    def __len__(self):
        return len(self.bits)//2
        
class DefaultTextCell(BaseCell):
    #This is the type of cell generated when an unbroken string is found in the template.
    #E.g. '     The quick brown fox {$foo hex width="8"}'
    #Generates a DefaultTextCell 'The quick brown fox' and a hex cell with reg 'foo'.
    
    def __init__(self, text, read_only=False, show_grey=False, is_break=False):
        #Read only is False here so that the text is not italic
        #Editing will not be possible anyway because the cell can't be selected
        BaseCell.__init__(self, None, read_only, show_grey, is_break=is_break)
        self.text = text
        self.should_refresh = False
        
    @property
    def can_inplace_edit(self):
        return False
        
    def _render(self, value):
        """
        >>> DefaultTextCell("Hello world!").render(None)
        'Hello world!'
        """
        
        return self.text
        
    def __repr__(self):
        return "TextCell('%s')" % self.text
        
class TextCell(DefaultTextCell):
    #The same as a DefaultTextCell except that it must be intentionally created.
    #E.g. '{$ text text="    hello world"}'
    #The difference being that this cell will preserve whitespace in the 'text' parameter.
    
    def __init__(self, expression, text='', read_only=False, show_grey=False, is_break=False):
        DefaultTextCell.__init__(self, text, read_only=read_only, show_grey=show_grey, is_break=is_break)
 
def _quoted(delim):
    """Makes a reg expression that will match a string delimited by delim, possibly
    with escaped delims inside (using \\).
    """
    return delim + r"([^" + delim + r"\\]*(?:\\.[^" + delim + r"\\]*)*)" + delim
    
def to_int(s):
    """Convert a string to a int.

    If the parameter is already an int/long then it is not converted.
    Standard prefixes such as 0x and 0 are supported.

    Raises ValueError if the conversion fails.

    >>> [to_int(x) for x in ['42', '0x42', '042']]
    [42, 66, 34]
    >>> [to_int(x) for x in [42, 0x42, 042]]
    [42, 66, 34]
    >>> to_int('10u')
    Traceback (most recent call last):
    ...
    ValueError: Cannot convert '10u' to an integer
    """
    if isinstance(s, (int, long)):
        return s
    try:
        return int(s, 0)
    except ValueError:
        raise ValueError("Cannot convert %r to an integer" % s)

def to_bool(s):
    """Convert a string to a bool.

    If the parameter is already a bool then it is not converted.
    The values 'true' and 'false' are acceptable string values and
    the test is case-insensitive.  The integer value 0 converts to
    False and all other integer types convert to True.

    Raises ValueError if the conversion fails.

    >>> [to_bool(x) for x in ['true', 'True', 'faLSE', 'False', '1', '0', 'None']]
    [True, True, False, False, True, False, False]
    >>> [to_bool(x) for x in [True, False, 42, 0, 1]]
    [True, False, True, False, True]
    >>> to_bool('tre')
    Traceback (most recent call last):
    ...
    ValueError: Cannot convert 'tre' to a bool
    """
    if isinstance(s, bool):
        return s
    try:
        return to_int(s) != 0
    except ValueError:
        try:
            return dict(true=True, false=False, none=False)[s.lower()]
        except KeyError:
            raise ValueError("Cannot convert %r to a bool" % s)
        
cident = r"[a-zA-Z0-9_]+"
arg_re = re.compile(r"\s*(?:(" + cident + ")=)?(?:([^'\"][^'\" \t]*)|" + _quoted("'") + "|" + _quoted('"') + r")\s*""")
        
def parse_arguments(s):
    args = []
    kwargs = {}
    for arg in matchiter(arg_re, s):
        if not arg:
            raise SyntaxError('Error parsing argument list in "%s"' % s)
        value = arg.group(2) or arg.group(3) or arg.group(4) or ''
        if arg.group(1):
            kwargs[arg.group(1)] = value
        else:
            if kwargs:
                raise SyntaxError('Positional argument following keyword argument in "%s"' % s)
            args.append(value)
    return args, kwargs
    
def matchiter(pattern, s, *args):
    """This is to re.finditer what re.match is to re.search.  It will return a
    None if at any point there is a failure to match a non-overlapping
    expression."""
    if isinstance(pattern, basestring):
        pattern = re.compile(pattern, *args)
    pos = 0
    while pos != len(s):
        m = pattern.match(s, pos)
        pos = m.end() if m else len(s)
        yield m
        
def parse_cell(s):
    """
    >>> parse_cell('')
    TextCell('')
    >>> parse_cell('$regname format format="%08x"')
    FormatCell('$regname', '%08x')
    >>> parse_cell('$regname bits bits=abcdABCD')
    BitCell('$regname', bits='abcdABCD')
    >>> parse_cell('$regname bits bits=abcdABCD bit_start=1')
    BitCell('$regname', bits='abcdABCD', bit_start=1)
    >>> parse_cell('"abcdef gh" other')
    TextCell('abcdef gh')
    """

    args, kwargs = parse_arguments(s)
    return cell(*args, **kwargs)
    
def cell(expression='', type='', **kwargs):
    cell_types = {
    'bits'               : BitsCell,
    'fixed_point'        : FixedPointCell,
    'fixed_point_complex': FixedPointComplexCell,
    'floating_point'     : FloatingPointCell,     
    'format'             : FormatCell,
    'hex'                : HexCell,
    'decimal'            : DecimalCell,
    'number'             : NumberCell,
    'text'               : TextCell,
    }
    
    if not expression[:1] in ['$', '#'] and type in cell_types:
        raise FormatException("Expression '%s' for cell type '%s' does not begin with '$' or '#'" % (expression, type))
    
    #Default to a DefaultTextCell
    try:
        return cell_types.get(type, DefaultTextCell)(expression, **kwargs)
    except TypeError as e:
        arg = str(e).rsplit(' ', 1)[1][1:-1]
        raise FormatException('Unexpected argument "%s" for cell type "%s" with expression "%s"' % (arg, type, expression))

class Grid(object):
    def __init__(self, rows):
        self.rows = rows
        self.max_columns = self.get_max_column()
        self.max_rows = len(self.rows)
        self.regs = [cell.name for cell in self if cell.name and cell.should_refresh]
        self.memory_mapped_regs = [cell.expression for cell in self if cell.name and cell.is_memory_mapped]
        
    def __iter__(self):
        for row in self.rows:
            for cell in row:
                yield cell
        
    def get_cell_by_pos(self, position):
        try:
            return self.rows[position[0]][position[1]]
        except IndexError:
            return None
               
    def get_max_column(self):
        if self.rows:
            return max([len(row) for row in self.rows])
        else: 
            return 0
        
    def get_col_widths(self, evaluator):
        cols = []
        
        for i in range(self.max_columns):
            col_width = 0
            for j in range(self.max_rows):
                cell = self.get_cell_by_pos((j, i))
                if cell:
                    col_width = max(len(cell.render(evaluator))+1, col_width)
            cols.append(col_width)
            
        return cols
        
    def clear_history(self):
        self.set_attr('first_render', None)
        
    def set_view_option(self, option, value):
        valid = ['ShowFloatingPointAsHex',
                 'ShowFixedPointAsHex',
                 'ShowFixedPointAsComplex',
                 'ShowNoneFixedPointRegistersLeftAligned',
                ]
        if option in valid:
            self.set_attr(option, value)
            
    def set_attr(self, method, value):
        for cell in self:
            setattr(cell, method, value)
                    
    def render_all(self, evaluator):
        for cell in self:
            cell.render(evaluator)
            
    def set_all_first_render(self):
        for cell in self:
            cell.first_render = cell.last_render
    
def parse_line(line):
    """
    >>> parse_line("cell 1 [$cell] cell 3 [$cell bits bits=4] []")
    [TextCell('cell 1'), TextCell('$cell'), TextCell('cell 3'), BitCell('$cell', bits='4'), TextCell('')]
    """
    pattern = re.compile(r"""
    \s*     # Any amount of whitespace
    (?:     # Non capturing group, so we can remove '[' and ']'
    ([^[]+) # At least one char that isn't '['. Captures runs of plain text.
    |       # or
    \[      # opening [
    ([^]]*) # Any number of chars, as '[]' is a valid cell. Captures the inside of cells.
    \]      # Closing ]
    )       # End non capture group
    """,
    re.VERBOSE)
    
    cells = []
    for m in matchiter(pattern, line):
        if not m:
            continue
        if m.group(1):
            cells.append(cell(m.group(1).strip()))
        else:
            cells.append(parse_cell(m.group(2)))
    return cells
    
def parse_grid(format):
    try:
        return Grid([parse_line(l) for l in format.splitlines()])
    except Exception as e:
        raise WrappedTemplateException(e, format)
    
def expand_short_cells(layout, registers_info):
    
    def insert_hex_cell(match):
        expr = match.groupdict()['expr']
        
        #Width in bytes
        info = registers_info.get(expr)
        if info is not None:
            width = info.size
        else:
            width = 4
        
        return "[$%s hex width=%d]" % (expr, width*2)
    
    pattern = r"""
    \[              # Opening [
    [^\S\r\n]*?     # Any whitespace which may be there
    \$              # Beginning of expression
    (?P<expr>       # Group to contain expression
    [^\n\r\[\]\s]+? # The expression itself, no end of lines, no [] or spaces
    )               # Close expression group
    [^\S\r\n]*?     # More whitespace if present
    \]              # Closing ]
    """
    
    pattern = re.compile(pattern, re.VERBOSE)
    return re.sub(pattern, insert_hex_cell, layout)
