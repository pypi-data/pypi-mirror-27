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

from imgtec.console.support import command, verbosity, named, auto

#  This module is a copy of the module in sw/comms, but we don't want to
# create a hard dependency from codescape at the moment, so this is cogged in.
# [[[cog
# import os, cog
# from imgbuild.SConsPaths import sw
# with open(sw('comms', 'comms', 'tdd.py')) as f:
#    contents = f.read()
# cog.out(contents[:contents.index("if __name__ == '__main__'")])
# ]]]
"""

Example
-------

Create and load a table with 2 MIPS cores and a CM::

    >>> board = Board(taps_on_chain=3, socs=[
    ...     SoC(pos_in_chain=0, ir_length=5, taps_per_soc=1, cores=
    ...        [make_core('mips_legacy')]
    ...     ),
    ...     SoC(pos_in_chain=1, ir_length=5, taps_per_soc=1, cores=
    ...        [make_core('mips_legacy')]
    ...     ),
    ...     SoC(pos_in_chain=2, ir_length=5, taps_per_soc=1, cores=
    ...        [make_core('ignore')]
    ...     ),
    ... ])
    >>> targetdata(board)                       # doctest: +SKIP

Create and load a table which instructs the probe to ignore the first of the two 2 MIPS cores::

    >>> board = Board(taps_on_chain=3, socs=[
    ...     SoC(pos_in_chain=0, ir_length=5, taps_per_soc=1, cores=
    ...        [make_core('ignore')]
    ...     ),
    ...     SoC(pos_in_chain=1, ir_length=5, taps_per_soc=1, cores=
    ...        [make_core('mips_legacy')]
    ...     ),
    ... ])
    >>> targetdata(board)                       # doctest: +SKIP

"""

from imgtec.lib.namedenum import namedenum, NamedEnumType
from collections import Sequence
from itertools import count
from operator import attrgetter
from textwrap import dedent
from xml.sax.saxutils import escape, quoteattr
from imgtec.lib import get_user_files_dir
import os

_AUTO = 0xFFFFFFFF

_Visibility = namedenum('_Visibility', 'public automatic deprecated')

MasterSlave = namedenum('MasterSlave', ('slave', 0), ('master', 1), _doc_usage='')

cs_setting_names = dict(j_img='j_img_enc', j_img_f='j_img_f_enc', j_img_m='j_img_m_enc')

def _hex_formatter(name, value):
    return '0x%02x' % value, name

CoreImgId = namedenum('CoreImgId',
    meta_legacy=          (0x00, 'IMG Legacy Core'),
    meta_atp=             (0x01, 'IMG META122 Core (ATP)'),
    meta_mtx=             (0x02, 'IMG MTX122 Core'),
    mcp=                  (0x03, 'IMG UCC Core (MCP) with Meta table layout'),
    meta_htp=             (0x04, 'IMG META HTP Core'),
    meta_mtp=             (0x05, 'IMG META MTP Core'),
    mips_legacy=          (0x06, 'MIPS Core with Meta table layout'),
    mips=                 (0x20, 'MIPS Core'),
    mips64r6 =            (0x25, 'MIPS64r6 Core'),
    mips_cm=              (0x30, 'MIPS Coherency Manager'),
    esecure=              (0x40, 'eSecure Challenge interface'),
    custom_register_block=(0xff, 'IMG Custom Register Block'),
    ignore=               (99, 'Do not debug this core'),
    _doc_usage='', _doc_values_formatter=_hex_formatter)

TapType = namedenum('TapType',
        ('legacy',         0, 'Unknown or legacy TAP'),
        ('IMG',            1, 'All IMG IP (excluding MIPS)'),
        ('legacy_s',       2, 'Legacy Encoding now unused'),
        ('legacy_i',       3, 'Legacy Encoding now unused'),
        ('legacy_mhs',     4, 'Legacy Encoding now unused'),
        ('generic_tap',    5, 'Generic tap controller with no recognisable debug logic attached'),
        ('mips_ejtag',     6, 'Classic MIPS EJTAG TAP'),
        ('mips_cm',        7, 'MIPS Coherency Manager 2 TAP'),
        ('mips_oci',       8, 'MIPS On Chip Instrumentation (DBU) TAP'),
        ('mips_mdh',       9, 'MIPS Debug Hub TAP'),
        ('arm_csight_dap', 10, 'ARM Codesight DAP JTAG-DP'),
        ('mips_ejtag_behind_mux', 11, 'MIPS EJTAG TAP behind an MDH Mux'),
        ('mips_cm_behind_mux',    12, 'MIPS CM TAP behind an MDH Mux'),
        ('img_tap_behind_mux',    13, 'IMG TAP behind an MDH Mux'),
        ('mips_oci_behind_mux',   14, 'MIPS OCI (DBU) TAP behind an MDH Mux'),
        ('generic_tap_behind_mux',15, 'Unknown TAP type behind an MDH Mux'),
        ('mips_oci_apb',          16, 'MIPS OCI (DBU) connected via APB'),
    _doc_usage='', _doc_values_formatter=_hex_formatter)
TapType.meta_tap = TapType.IMG # for backwards compatibility

MetaDebugRevision = namedenum('MetaDebugRevision',
        ('unknown',         0, 'Non IMGLib compliant JTAG'),
        ('imglib_jtag_1_1', 1, 'IMGLib JTAG 1.1 (base level)'),
        ('imglib_jtag_1_2', 2, 'IMGLib JTAG 1.2 (Adds JTAG status Instruction)'),
        ('imglib_jtag_1_3', 3, 'IMGLib JTAG 1.3 (Adds JTAG control Instruction)'),
    _doc_usage='', _doc_values_formatter=_hex_formatter)

MetaTraceVersion = namedenum('MetaTraceVersion',
    ('no_trace', 0, 'No trace support'),
    ('meta_16bit', 1, 'Meta 16-bit trace port'),
    _doc_usage='', _doc_values_formatter=_hex_formatter)

MetaThreadType = namedenum('MetaThreadType',
        ('dsp',             0x0,  'DSP Thread'),
        ('mtp_ldsp',        0x8,  'MTP LDSP Thread'),
        ('mtx',             0x9,  'MTX Thread'),
        ('mtp_ldsp_lfpu16', 0xA,  'MTP LDSP LFPU16 Thread (16 FPU Regs)'),
        ('mtp_ldsp_lfpu8',  0xB,  'MTP LDSP LFPU8 Thread (8 FPU Regs)'),
        ('gp',              0xC,  'General Purpose Thread'),
        ('mtp_lfpu16',      0xE,  'MTP LFPU16 Thread'),
        ('mtp_lfpu8',       0xF,  'MTP LFPU8 Thread'),
        ('mcp',             0x20, 'UCC Thread'),
        ('mips32',          0x80, 'MIPS32 VPE'),
        ('not_present',     0x99, 'Thread not present'),
    _doc_usage='', _doc_values_formatter=_hex_formatter)

MetaFPUType = namedenum('MetaFPUType',
        ('none',          0, 'No FPU'),
        ('double',          1, 'Double precision with Accumulator'),
        ('single_accum',    2, 'Single Precision with Accumulator'),
        ('single_no_accum', 3, 'Single Precision no Accumulator'),
    _doc_usage='', _doc_values_formatter=_hex_formatter)

MetaDSPType = namedenum('MetaDSPType',
        ('meta',         0, 'Meta dsp 16+16 DU regs, 8+8 AU regs + DPS Rams + Accumulators'),
        ('mtp',          1, 'MTP DSP : 8+8 DU regs, 4+4 AU regs (no DSP Rams or Accumulators)'),
        ('mtp_baseline', 2, 'MTP Baseline DSP : 9+9 DU regs, 4+4 AU regs (no DSP Rams or Accumulators)'),
        ('none',         99, 'No DSP'),
    _doc_usage='', _doc_values_formatter=_hex_formatter)

MetaCacheType = namedenum('MetaCacheType',
        ('l1_only_write_through', 0, 'L1 only DCache Write Through'),
        ('l1_only_write_back',    1, 'L1 only DCache Write Back'),
        ('none', 99, 'No cache'),
    _doc_usage='', _doc_values_formatter=_hex_formatter)

MetaDebugType = namedenum('MetaDebugType',
        ('normal',   0, 'Normal debug available'),
        ('mcm_only', 1, 'Debug around the core only MCM port available'),
        ('no_mcm',   2, 'Debug through the core only no MCM port'),
    _doc_usage='', _doc_values_formatter=_hex_formatter)

class _ArrayField(Sequence):
    """List like access to array fields, accesses must be within range of the array size."""
    def __init__(self, field, obj):
        self.field = field
        self.obj = obj

    def _check_bounds(self, index):
        if index >= self.field.count:
            raise IndexError("index out of range for field %s[%d], got %r" %
                    (self.field.name, self.field.count, index))

    def __getitem__(self, index):
        if isinstance(index, slice):
            start = 0                if index.start is None else index.start
            stop  = self.field.count if index.stop  is None else index.stop
            if stop < 0:
                stop += self.field.count
            step  = 1                if index.step  is None else index.step
            self._check_bounds(start)
            self._check_bounds(stop-1)
            return [self.obj.get_value(self.field.index + i) for i in range(start, stop, step)]
        else:
            self._check_bounds(index)
            return self.obj.get_value(self.field.index + index)

    def __setitem__(self, index, value):
        self._check_bounds(index)
        self.obj.set_value(self.field.index + index, self.field._check_type(value))

    def __len__(self):
        return self.field.count

    def __repr__(self):
        return _valuelist_as_hex(self.obj._values[self.field.index:self.field.end_index])
        
def _generate_field_doc(field):
    r'''
    
    >>> print _generate_field_doc(_Field(0, 'fname', doc='Hello'))
    *type:* uint32  *default:* 0xffffffff
    <BLANKLINE>
    Hello
    >>> print _generate_field_doc(_Field(0, 'fname', doc='Hello', type=TapType))
    *type:* :class:`~imgtec.console.tdd.TapType`  *default:* 0xffffffff
    <BLANKLINE>
    Hello
    >>> print _generate_field_doc(_Field(0, 'fname', doc='Hello', array_size=8))
    *type:* uint32[8]  *default:* 0xffffffff
    <BLANKLINE>
    Hello
    >>> print _generate_field_doc(_Field(0, 'fname', doc='Hello', array_size=8, type=TapType))
    *type:* :class:`~imgtec.console.tdd.TapType`\[8]  *default:* 0xffffffff
    <BLANKLINE>
    Hello
    >>> print _generate_field_doc(_Field(0, 'fname', docname='Docname'))
    *type:* uint32  *default:* 0xffffffff
    <BLANKLINE>
    Docname
    '''
    lines = []
    
    array = '[%d]' % field.array_size if field.is_array else ''
    default = _value_as_expression(field.default, field, force_display=True)
    type = 'uint32'
    if issubclass(field.type, NamedEnumType):
        type = ':class:`~imgtec.console.tdd.%s`' % (field.type.__name__,)
        if field.is_array:
            type += '\\'
    elif field.type == bool:
        type = 'bool'
    lines = ['*type:* %s%s  *default:* %s' % (type, array, default)]
        
    if field.visibility == _Visibility.automatic:
        lines.append('This field is automatically updated.')
    if field.doc:
        lines.append(field.doc)
    return '\n\n'.join(lines)
        
class _Field(object):
    def __init__(self, index, name, default=_AUTO, docname="", doc="", type=int, allow_auto=True, visibility=_Visibility.public,
                    category='Core Information', array_size=None, show_in_cores=all):
        self.name = name
        if not allow_auto and default == _AUTO:
            raise SyntaxError("Bad default for field %s" % (name,))
        self.default = default
        self.docname = docname
        self.doc = dedent(doc)
        self.type = type
        self.allow_auto = allow_auto
        self.visibility = visibility
        self.category = category 
        self.array_size = array_size
        self.index = index
        self.show_in_cores = show_in_cores.split() if isinstance(show_in_cores, basestring) else show_in_cores
        self.doc = self.doc or self.docname
        if not self.doc:
            raise SyntaxError("Missing doc for field %s" % (name,))
        self.__doc__ = _generate_field_doc(self)

    @property
    def count(self):
        return self.array_size if self.is_array else 1

    @property
    def is_array(self):
        return self.array_size is not None

    @property
    def end_index(self):
        return self.index + self.count

    def __repr__(self):
        return self.name

    def _replace(self, **updates):
        kwargs = dict(
            name=self.name,
            default=self.default,
            docname=self.docname,
            doc=self.doc,
            type=self.type,
            allow_auto=self.allow_auto,
            visibility=self.visibility,
            category=self.category,
            array_size=self.array_size,
            index=self.index,
            show_in_cores=self.show_in_cores,
            )
        kwargs.update(updates)
        return _Field(**kwargs)

    def _check_array_type(self, value):
        if not isinstance(value, Sequence):
            raise TypeError("Expected sequence for field %s[%d], got %r" %
                            (self.name, self.count, value))
        if len(value) > self.count:
            raise ValueError("Too many values for field %s[%d], got %r" %
                (self.name, self.count, value))
        return [self._check_type(v) for v in value]

    # descriptor support, allows _Field to be used as a property directly
    def __get__(self, obj, objtype=None):
        if obj is None:  # allow Table.core_img_id to give the _Field object (may be a bad idea)
            return self
        if self.is_array:
            return _ArrayField(self, obj)
        return obj.get_value(self.index)
    def __set__(self, obj, value):
        if self.is_array:
            value = self._check_array_type(value)
            for index, v in enumerate(value, self.index):
                obj.set_value(index, v)
        else:
            obj.set_value(self.index, self._check_type(value))

    def _check_type(self, value):
        if self.type != bool and isinstance(value, basestring):
            value = self.type(value)
        return int(value)


class _Container(object):
    def __init__(self, name, doc):
        self.name = name
        self.__doc__ = dedent(doc)
    def __get__(self, obj, objtype=None):
        if obj is None:  # allow Table.core_img_id to give the _Field object
            return self
        try:
            return getattr(obj, '_' + self.name)
        except AttributeError:
            setattr(obj, '_' + self.name, [])
            return getattr(obj, '_' + self.name)
    def __set__(self, obj, value):
        raise AttributeError("Cannot set readonly attribute %s" % (self.name,))

def get_core_class(core_img_id):
    """Find the subclass of :class:`Core` matching the core_img_id, in the known list
    of core types. If not found :class:`Core` is returned.

    >>> get_core_class(0xfe).__name__
    'Core'
    >>> get_core_class(5).__name__
    'MetaCore'
    >>> get_core_class('meta_mtp').__name__
    'MetaCore'
    >>> get_core_class(CoreImgId.mcp).__name__
    'MCPCore'
    """
    core_img_ids = {
        CoreImgId.meta_atp    : MetaCore,
        CoreImgId.meta_mtx    : MetaCore,
        CoreImgId.mcp         : MCPCore,
        CoreImgId.meta_htp    : MetaCore,
        CoreImgId.meta_mtp    : MetaCore,
        CoreImgId.mips_legacy : MipsLegacyCore,
        CoreImgId.mips        : MipsCore,
        CoreImgId.mips64r6    : MipsCore,
        CoreImgId.mips_cm     : MipsCMCore,
    }
    if isinstance(core_img_id, basestring):
        core_img_id = CoreImgId(core_img_id)
    return core_img_ids.get(core_img_id, Core)
    

def make_core(core_img_id, **kwargs):
    """Create an instance of the correct subclass of :class:`Core` for the `core_img_id`.

    See :class:`CoreImgId` for valid values for core_img_id.

        >>> make_core('mips').core_img_id
        32
        >>> make_core('mips')
        tdd.MipsCore(
          core_img_id=tdd.CoreImgId.mips,
        )

    """
    return get_core_class(core_img_id)(core_img_id=core_img_id, **kwargs)    

def _expand_arrays_and_format(name, value, formatter):
    if isinstance(value, Sequence):
        return [formatter('%s[%d]' % (name, n), v) for n, v in zip(count(), value)]
    else:
        return [formatter(name, value)]

def _rstrip_values(sequence, value):
    '''Remove any consecutive trailing values.
    
    >>> _rstrip_values([1, 2, 3], 3)
    [1, 2]
    >>> _rstrip_values([3, 3, 3], 3)
    []
    >>> _rstrip_values([1, 3, 1], 3)
    [1, 3, 1]
    >>> _rstrip_values([1, 1, 1], 3)
    [1, 1, 1]
    >>> _rstrip_values([3, 1, 1], 3)
    [3, 1, 1]
    '''
    remove = 0
    for idx in xrange(len(sequence) - 1, -1, -1):
        if sequence[idx] != value:
            remove = idx + 1
            break
    return sequence[:remove]

def _value_as_expression(value, field, force_display=False, include_doc=False):
    '''Format a table entry into something evaluatable.  Try to be reasonably
    terse.  Returns None if the entry should be discarded because it is the same
    as the field's default value.

    If force_display is True then the formatted value will be returned even if
    it is == default.
    
    If include_doc is True then a (display, comment) pair will be returned, 
    where comment is the raw value and value documentation if appropriate (or
    an empty string if not).

    >>> _value_as_expression([1, 2, 3], _Field(1, 'name', default=3, doc='c'), '')
    '[0x00000001, 0x00000002]'
    >>> _value_as_expression([3, 3, 3], _Field(1, 'name', default=3, doc='c'), '')
    >>> _value_as_expression(3, _Field(1, 'name', default=3, doc='c'), '')
    >>> _value_as_expression(1, _Field(1, 'name', default=0, doc='c', type=bool))
    'True'
    >>> _value_as_expression(0, _Field(1, 'name', default=0, doc='c', type=bool), '')
    >>> Bob = namedenum('Bob', 'the builder')
    >>> _value_as_expression(1, _Field(1, 'name', type=Bob, doc='c'))
    'tdd.Bob.builder'
    >>> _value_as_expression(2, _Field(1, 'name', type=Bob, doc='c'))
    '0x00000002'
    >>> _value_as_expression(0x77, SoC.tap_type, include_doc=True)
    ('0x00000077', '')
    >>> _value_as_expression(0, SoC.tap_type, force_display=True, include_doc=True)
    ('tdd.TapType.legacy', '0x00000000 - Unknown or legacy TAP')
    >>> _value_as_expression(0x77, MetaCore.thread_type, include_doc=True)
    ('0x00000077', '')
    >>> _value_as_expression(0, MetaCore.thread_type, include_doc=True)
    ('tdd.MetaThreadType.dsp', '0x00000000 - DSP Thread')
    '''
    if isinstance(value, Sequence):
        value = _rstrip_values(value, field.default)
        if value:
            return '[' + ', '.join(_value_as_expression(x, field, True) for x in value) + ']'

    elif value != field.default or force_display:
        display, doc = '0x%08x' % value, ''
        if field.type == bool:
            return repr(bool(value))
        elif issubclass(field.type, NamedEnumType):
            try:
                found = field.type(value)                
                display = 'tdd.%r' % (found,)
                if include_doc and found.__doc__:
                    doc = '0x%08x - %s' % (value, found.__doc__)
            except ValueError:
                pass
        return (display, doc) if include_doc else display


class _Formatter(object):
    children_open = []
    children_close = []
    child_sep = ''
    fields_indent = ''
    children_indent = ''
    
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
            
    def open_close(self, _table):
        return ([], [])
            
    def format_fields(self, table, indent):
        settings = []
        for field in table._known_fields(hide_automatic=True):
            settings.extend(self.format_field(table, field))
        return [self.fields_indent + indent + s for s in settings]

    def format_children(self, table, indent):
        lines = []
        for container in table._containers():
            children = getattr(table, container)
            if children:
                macros = dict(container=container)
                lines.extend([indent + l % macros for l in self.children_open])
                for child in children:
                    child = self.format_table(child, self.children_indent + indent)
                    lines.append(child + self.child_sep)
                lines.extend([indent + l % macros for l in self.children_close])
        return lines

    def format_table(self, table, indent=''):
        settings = self.format_fields(table, indent)
        childrenlines = self.format_children(table, indent)
        open, close = self.open_close(table)
        return '\n'.join([indent + line for line in open] +
                settings + childrenlines +
                [indent + line for line in close])

class _TextFormatter(_Formatter):
    children_indent = '  '
    fields_indent = ''

    def format_field(self, table, field):
        def formatter(name, value):
            display, doc = _value_as_expression(value, field, force_display=True, include_doc=True)
            if doc: doc = ' (' + doc + ')'
            return '{0:17} = {1}{2}'.format(name, display, doc)
        value = getattr(table, field.name)
        if isinstance(value, Sequence):
            value = _rstrip_values(value, field.default)
        return _expand_arrays_and_format(field.name, value, formatter)
        
    def format_fields(self, table, indent):
        settings = []
        for field in table._known_fields(hide_automatic=True, hide_irrelevant=True):
            settings.extend(self.format_field(table, field))
        return [self.fields_indent + indent + s for s in settings]
        
    def format_children(self, table, indent):
        lines = []
        for container in table._containers():
            for n, child in enumerate(getattr(table, container)):
                lines.append('%s%s[%d]' % (indent, container, n))
                lines.append(self.format_table(child, self.children_indent + indent))
        return lines
            
            
class _XmlFormatter(_Formatter):
    fields_indent = '  '
    children_indent = '  '
    
    def format_field(self, table, field):
        name = cs_setting_names.get(field.name, field.name)
        value = getattr(table, field.name)
        formatter = '<setting N="{0}">0x{1:x}</setting>'.format
        return _expand_arrays_and_format(name, value, formatter)
        
    def open_close(self, table):
        macros = dict(name=quoteattr(table.name),
                      hd_filename=escape(getattr(table, 'hd_filename', '')))
        if isinstance(table, Board):
            return ([u'<?xml version="1.0" encoding="utf-8" ?>',
                     u'<ioconfig>',
                     u'<Board Name=%(name)s>' % macros],
                    [u'</Board>',
                     u'</ioconfig>'])
        elif isinstance(table, SoC):
            return ([u'<SoC Name=%(name)s>' % macros],
                    [u'</SoC>'])
        else:
            return ([u'<CoreInfo Name=%(name)s>' % macros],
                    [u'  <ProcessorLink N="/.*/">',
                     u'    <src>%(hd_filename)s</src>'% macros,
                     u'  </ProcessorLink>',
                     u'</CoreInfo>'])
    
class _ExpressionFormatter(_Formatter):
    children_open = ['  %(container)s=[']
    children_close = ['  ],']
    child_sep = ','
    fields_indent = '  '
    children_indent = '    '

    def format_field(self, table, field):
        value = _value_as_expression(getattr(table, field.name), field)
        if value:
            return ['%s=%s,' % (field, value)]
        return []

    def open_close(self, table):
        extras = [(f, d, getattr(table, f)) for f, d in table._extra_fields()]
        extras = ' '.join(['%s=%r,' % (f, v) for f, d, v in extras if d != v])
        return (['tdd.{0}({1}'.format(table.__class__.__name__, extras)], [')'])

_formatters = dict(
    text=_TextFormatter(), 
    xml=_XmlFormatter(),
    expression=_ExpressionFormatter(),
    repr=_ExpressionFormatter(),
)

def _valuelist_as_hex(values):
    return '[' + ", ".join(['0x{0:08x}'.format(v) for v in values]) + ']'
    
class _ValuesResult(list):
    def __repr__(self):
        return _valuelist_as_hex(self)

class Table(object):
    """Base class for all tables.

    Field access methods, and meta data about the available fields can be
    retrieved through the following methods:
    """
    def __init__(self, **kwargs):
        """Create an instance from named keywords."""
        fields = self.__class__._known_fields()
        object.__setattr__(self, 'default_format', kwargs.pop('default_format', 'expression'))
        
        for extra, default in self.__class__._extra_fields():
            value = kwargs.pop(extra, default)
            object.__setattr__(self, extra, value)
                        
        self._values = []
        for f in fields:
            if not f.is_array:
                self._values.append(f._check_type(kwargs.pop(f.name, f.default)))
            else:
                value = kwargs.pop(f.name, [f.default] * f.count)
                value = f._check_array_type(value)
                self._values.extend(list(value) + [f.default] * (f.count - len(value)))
        for container in self._containers():
            getattr(self, container).extend(kwargs.pop(container, []))
        if kwargs:
            s  = 's' if len(kwargs) > 1 else ''
            an = ''  if len(kwargs) > 1 else ' an'
            unexpected = ', '.join(repr(x) for x in sorted(kwargs.keys()))
            raise TypeError("%s() got%s unexpected keyword argument%s %s" %
                            (self.__class__.__name__, an, s, unexpected))

    @classmethod
    def from_values(cls, values):
        """Construct a table from a 32-bit value stream.

        If `values` is given then the total size (in bytes) of the entry is
        taken from the first word, and fields are read from the remaining
        words.

        If size//4 is smaller than the known fields then missing entries are
        filled with the field defaults.  If size//4 of the entry is larger
        than the known fields then extra values are accessible through
        :meth:`get_value` or :meth:`as_values`.  This flexibility allows tables
        to be configured for fields unknown to this version of Codescape Console.

        If `values` is given then keyword parameters are ignored.

            >>> board2 = Board.from_values([8, 2])
            >>> board2  # note that num_of_socs is taken from the defaults
            tdd.Board(
              taps_on_chain=0x00000002,
            )

        Note that contained tables are not processed, use :func:`board_from_values`
        to parse a full configuration table into a Board.
        """
        x = cls()
        size = values[0] if values else 0
        x._values = values[:size//4]
        for f in cls._known_fields():
            missing = max(0, f.end_index - len(x._values))
            x._values.extend([f.default] * missing)
        return x

    def get_value(self, index):
        """Get a value from the table by index, if missing the default is returned."""
        try:
            return self._values[index]
        except IndexError:
            return _AUTO

    def set_value(self, index, value):
        """Set a value in the table by index.

        The index may be greater than the current length of the table, in this case
        defaults will be inserted.

        >>> b = Board()
        >>> b.as_values()
        [0x0000000c, 0x00000001, 0x00000000]
        >>> b.set_value(4, 0x1234)
        >>> b.as_values()
        [0x00000014, 0x00000001, 0x00000000, 0xffffffff, 0x00001234]

        This allows setting of fields not supported by this version of Codescape
        Console. Of course the probe firmware must support it.
        """
        try:
            value + 1
        except TypeError:
            raise TypeError("Table values must be an integer, given %r" % (value,))
        try:
            self._values[index] = value
        except IndexError:
            missing = index - len(self._values)
            self._values.extend([_AUTO] * missing + [value])

    @classmethod
    def _containers(cls):
        x = []
        for c in cls.__mro__:
            x += [x.name for x in c.__dict__.values() if isinstance(x, _Container)]
        return x

    @classmethod
    def known_fields(cls):
        """List of field names in this table in order of index."""
        return [x.name for x in cls._known_fields()]

    @classmethod
    def _known_fields(cls, hide_automatic=False, hide_irrelevant=False):
        fields = []
        for c in cls.__mro__:
            fields += [x for x in c.__dict__.values() if isinstance(x, _Field)]
        if hide_automatic:
            fields = [f for f in fields if f.visibility != _Visibility.automatic]
        if hide_irrelevant:
            fields = [f for f in fields if cls._show_in_core(f)]
        return sorted(fields, key=attrgetter('index'))

    @classmethod
    def known_length(cls):
        """The number of values in known fields in this table.

        This includes the length of any expanded array fields, so it
        is not equal to the length of known_fields:

        >>> len(MetaCore.known_fields())
        37
        >>> MetaCore.known_length()
        54
        """
        return sum(f.count for f in cls._known_fields())

    def as_values(self):
        """The data from this table as a series of 32-bit values.

        Returns a copy of the values with the values updated with corrected
        values for size and the num_of_socs/num_of_cores fields.

        Note that the values for contained tables are not included, use
        :func:`board_as_values` to extract the full table configuration data.
        """
        x = self._values[:]
        cls = self.__class__
        x[cls.size.index] = len(x)*4
        for container in cls._containers():
            x[getattr(cls, 'num_of_' + container).index] = len(getattr(self, container))
        return _ValuesResult(x)

    @classmethod
    def _show_in_core(cls, field):
        return field.show_in_cores == all or cls.__name__ in field.show_in_cores

    @classmethod
    def _extra_fields(cls):
        return [('name', '')]
        
    @classmethod   
    def _size(cls):
        return sum(f.count for f in cls._known_fields())
        
    def __setattr__(self, name, value):
        if not name.startswith('_'):
            getattr(self, name)
        super(Table, self).__setattr__(name, value)
            
    def __repr__(self):
        return format(self, self.default_format)
        
    def __format__(self, format):
        try:
            formatter = _formatters[format]
        except KeyError:
            raise ValueError('Invalid conversion specification: ' + repr(format))
        return formatter.format_table(self, '')

class Board(Table):
    """A table entry for a Board.

    Valid keywords are any of the fields in Board and `socs` :- a list of
    :class:`SoC` instances ::

        >>> board = Board(taps_on_chain=2, socs=[SoC(cores=[MipsCore(dcr=1)])])
        >>> board
        tdd.Board(
          taps_on_chain=0x00000002,
          socs=[
            tdd.SoC(
              cores=[
                tdd.MipsCore(
                  dcr=0x00000001,
                ),
              ],
            ),
          ],
        )
        >>> del board.socs[0]
        >>> board
        tdd.Board(
          taps_on_chain=0x00000002,
        )

    A Board contains the following fields:

    """
    size = _Field(0, "size", 12, docname="Size", category='Board Information', visibility=_Visibility.automatic,
        doc="Size of the board data table in bytes.")

    taps_on_chain = _Field(1, "taps_on_chain", 1, docname="Taps on JTAG Chain", allow_auto=False, category='Board Information',
        doc="The total number of devices connected in the JTAG chain.")

    num_of_socs = _Field(2, "num_of_socs",  1, docname="Number of Debuggable SoCs", category='Board Information', allow_auto=False,
        visibility=_Visibility.automatic,
        doc="The total number of devices on the JTAG chain containing debuggable IMG IP.")

    socs = _Container('socs', r'List of :class:`SoC`\s contained in this board')
                    
    def to_xml(self):
        '''Return this board as a Codescape HSP board file in xml.'''
        return self._as_xml()


class SoC(Table):
    """A table entry for an SoC.

    Valid keywords are any of the fields in SoC and `cores` :- a list of
    :class:`Core` instances.  ::

        >>> soc = SoC(pos_in_chain=3, ir_length=6, jtag_id=0x1234, cores=[make_core(CoreImgId.meta_htp)])
        >>> del soc.cores[0]
        >>> soc
        tdd.SoC(
          pos_in_chain=0x00000003,
          ir_length=0x00000006,
          jtag_id=0x00001234,
        )

    An SoC contains the following fields:

    """
    size = _Field(0, "size", 40, docname="SoC` Data Size", category='SoC Information', visibility=_Visibility.automatic,
        doc="Size of the per SoC data table in bytes.")

    pos_in_chain = _Field(1, "pos_in_chain",  1, docname="Position in JTAG chain", allow_auto=False, category='SoC Information',
        doc="The position of the SoC relative to the Probe's TDO on the JTAG chain")

    ir_length = _Field(2, "ir_length", 4, docname="IR length", allow_auto=False, category='SoC Information',
        doc="Size of the JTAG Instruction Register")

    jtag_id = _Field(3, "jtag_id", 0, docname="JTAG ID", allow_auto=False, category='SoC Information',
        doc="Value of the JTAG ID register (optional).")

    j_img_attn = _Field(4, "j_img_attn", 0, docname="J_IMG_ATTEN instruction encoding", allow_auto=False,
        category='SoC Information',
        doc="The value used to encode the IMG proprietary JTAG Attention instruction.")

    tap_type = _Field(5, "tap_type", 0, docname="TAP Type", allow_auto=False,
        category='SoC Information',doc="""\
        A number indicating the type of IMG wrapper used around the standard JTAG TAP,
        this is an enumerated value of the type TapType.

        (Use on FPGA design with large skew on JTAG nets - delays driving of TMS/TDO
        until falling edge of TCK. nb TCK must be 10MHz or less).""", type=TapType)

    num_of_cores = _Field(6, "num_of_cores", default=1, docname="Number of Debuggable Cores", visibility=_Visibility.automatic,
        category='SoC Information',
        doc="Number of IMG Cores within the SoC which are debuggable using a Probe.")

    j_img_status = _Field(7, "j_img_status", default=0, docname="J_IMG_STATUS instruction encoding", allow_auto=False,
        category='SoC Information',
        doc="The value used to encode the IMG proprietary JTAG Status instruction.")

    j_img_control = _Field(8, "j_img_control", default=0, docname="J_IMG_CONTROL instruction encoding", allow_auto=False,
        category='SoC Information',
        doc="The value used to encode the IMG proprietary JTAG Control instruction.")

    taps_per_soc = _Field(9, "taps_per_soc", default=1, docname="Number of taps per SoC", allow_auto=False,
        category='SoC Information',
        doc="The number of taps per soc.")

    cores = _Container('cores', r'List of :class:`Core`\s contained in this SoC')

class Core(Table):
    """Fields common to all Core table types, it is a base class of
    :class:`MetaCore` and :class:`MipsCore`.

        >>> core = Core(core_img_id='ignore')
        >>> core.core_img_id
        99

    Normally only subclasses of Core should be instantiated, you can use :func:`make_core`
    to make a core based on its core_img_id ::

        >>> core = make_core('ignore')
        >>> core.core_img_id
        99

    """
    size =     _Field(0, "size", 0, docname="Core Data Size", visibility=_Visibility.automatic,
        doc="Size of the per Core data table in bytes.",
        category='Core Information')

    core_img_id = _Field(1, "core_img_id", 0, docname="Core IMG ID Type", allow_auto=False, doc="""\
        Identifies the type of IMG IP for this Core.""",
        type=CoreImgId, category='Core Information')

    @classmethod
    def _extra_fields(cls):
        return [('name', ''), ('hd_filename', '')]
    


class MetaCore(Core):
    """A table entry for a Meta core.

    Valid keywords are any of the fields shown below, or in the :class:`Core`.
    Array fields may be initialised with lists, and enum fields may be initialised
    with numbers, strings for the field names, or enum instances ::

        >>> core = MetaCore(core_img_id='meta_mtp', debug_type=2, thread_type=['dsp', 'gp'])
        >>> core.thread_type
        [0x00000000, 0x0000000c, 0xffffffff, 0xffffffff]
        >>> core
        tdd.MetaCore(
          core_img_id=tdd.CoreImgId.meta_mtp,
          thread_type=[tdd.MetaThreadType.dsp, tdd.MetaThreadType.gp],
          debug_type=tdd.MetaDebugType.no_mcm,
        )
        >>> core.thread_type = [0x42, 'dsp', MetaThreadType.gp]
        >>> core.thread_type
        [0x00000042, 0x00000000, 0x0000000c, 0xffffffff]

    """
    debug_rev = _Field(2, "debug_rev", 1, docname="Debug Revision", allow_auto=False,
        doc="Debug interface revision, this tracks the version of the IMG JTAG wrapper",
        type=MetaDebugRevision, category='Core Information')

    j_img = _Field(3, "j_img", 0, docname="J_IMG JTAG instruction encoding", allow_auto=False,
        doc="The value used to encode the IMG proprietary JTAG debug instruction.",
        category='Core Information')

    j_img_f = _Field(4, "j_img_f", 0, docname="J_IMG_F JTAG instruction encoding", allow_auto=False,
        doc="The value used to encode the IMG proprietary fast JTAG debug instruction.",
        category='Core Information')

    j_img_m = _Field(5, "j_img_m", 0, docname="J_IMG_M JTAG instruction encoding", allow_auto=False,
        doc="The value used to encode the IMG proprietary JTAG mode instruction.",
        category='Core Information')

    extra_shifts = _Field(6, "extra_shifts", 0, docname="Extra Shift Registers", visibility=_Visibility.deprecated, doc="""\
         The number of additional registers added to the scan chain path between the
         TAP and Core (these are often added to improve timing).""",
         category='Core Options')

    extra_poll_on_read = _Field(7, "extra_poll_on_read", 1, docname="Extra Poll on Read", allow_auto=False, doc="""\
        On reading from certain targets an extra poll on the status register is required
        before shifting data out.  This option is ignored unless **Debug Revision** is `Legacy`.""",
          type=bool, category='Core Options')

    reset_master = _Field(8, "reset_master", 1, docname="Reset Master/Slave", doc="""\
        When the Probe is the slave it cannot reset the target directly and/or another core host in the
        system may reset this core without warning.

        When the Probe is a master it can reset the target directly and the target can only be reset by
        an external event (ie push button/power cycle) or this core issuing a warm reset.""",
        type=MasterSlave, category='Core Options')

    debug_master = _Field(9, "debug_master", 1, docname="Debug Master/Slave", doc="""\
        When the Probe is configured as a debug slave it shares the debug port with another host system and
        must arbitrate for access and/or this core is a slave to another host in the system using a
        different interface eg SPI/SDIO/ etc and the Probe must arbitrate for shared resource and obtain
        locks for operations which must be atomic.

        When configured as debug master it is the sole user of the debug port and there are no other host
        systems.""", type=MasterSlave, category='Core Options')

    corereg_interlock = _Field(10, "corereg_interlock", 0, docname="Core Registers - Interlock Accesses", allow_auto=False,
        doc="Obtain a lock before using the register port.", type=bool, category='Core Options', show_in_cores='MetaCore')

    corereg_arbitrate = _Field(11, "corereg_arbitrate", 0, docname="Core Registers - Arbitrate for Port", allow_auto=False, doc="""\
        Arbitrate for use of the register port, needed on Meta cores when code running on a thread
        wishes to examine another threads registers in so using the same port which the Probe uses, hence
        arbitration is required.""", type=bool, category='Core Options', show_in_cores='MetaCore')

    icache_size = _Field(12, "icache_size", docname="Instruction Cache Size", category='Cache',
        doc="Size of the Instruction Cache of the given Core in Kb, 0 if no cache available.", show_in_cores='MetaCore')

    dcache_size = _Field(13, "dcache_size", docname="Data Cache Size", category='Cache',
        doc="Size of the Data Cache of the given Core in Kb, 0 if no cache available.", show_in_cores='MetaCore')

    cache_ways = _Field(14, "cache_ways", docname="Cache Ways", category='Cache',
        doc="Number of ways (count of how many places a single address may reside within the cache).",
        show_in_cores='MetaCore')

    cache_line_size = _Field(15, "cache_line_size", docname="Cache Line Size", category='Cache',
        doc="Size of a cache line in bytes", show_in_cores='MetaCore')

    data_watch_fix = _Field(16, "data_watch_fix", 0, docname="Data Watchpoint Fix", category='Core Options',
        allow_auto=False,
        doc="""\
        Enable fix for SoCs with faulty Data Watchpoint hardware. This value is only used
        on Meta 1.2.x cores, and should be 0 otherwise.""",
        type=bool, show_in_cores='MetaCore')

    cache_contexts = _Field(17, "cache_contexts", 1, docname="Cache Contexts", visibility=_Visibility.deprecated, doc="""\
        Cache last read values from a context, so on a write, if cache matches the value to be
        written the write is ignored.  This is used to minimize core accesses.""", type=bool,
        category='Cache')

    trace_version = _Field(18, "trace_version", 0, docname="Trace Version", allow_auto=False, category='Core Options',
        doc="Version of extended trace interface supported by the core.",
        type=MetaTraceVersion, show_in_cores='MetaCore')

    meta_core_base = _Field(19, "meta_core_base", 0, docname="Base Address of Core Registers", visibility=_Visibility.deprecated,
        doc="32-bit Address of the location of Core Registers.", category='Core Options', show_in_cores='MetaCore')

    core_code_mem_size = _Field(20, "core_code_mem_size", docname="Core Code Memory Size",
        doc="Size of the Core Code Memory blocks on Meta cores in Kb, 0 if not present.",
        category='Memory', array_size=8, show_in_cores='MetaCore')

    core_data_mem_size = _Field(28, "core_data_mem_size", array_size=8, docname="Core Data Memory Size",
        doc="Size of the Core Data Memory blocks on Meta cores in Kb, 0 if not present.",
        category='Memory', show_in_cores='MetaCore')

    thread_type = _Field(36, "thread_type", array_size=4, docname="Thread Type", category='Threads',
        doc="""\
        Type of Thread for multithreaded cores, if core is not multithread thread0_type indicates core type,
        threads 1-3 should be set to "Thread not present".""", type=MetaThreadType)

    hw_break_controllers = _Field(40, "hw_break_controllers", docname="Hardware Break Controllers",
        doc="Number of available break controllers.", category='Resources', show_in_cores='MetaCore')

    hw_watch_controllers = _Field(41, "hw_watch_controllers", docname="Hardware Watch Controllers",
        doc="Number of available hardware watch points.", category='Resources', show_in_cores='MetaCore')

    global_address_registers = _Field(42, "global_address_registers", docname="Global Address Registers",
        doc="Number of global address registers.", category='Resources', show_in_cores='MetaCore')

    global_data_registers = _Field(43, "global_data_registers", docname="Global Data Registers",
        doc="Number of global data registers.", category='Resources', show_in_cores='MetaCore')

    global_accumulators = _Field(44, "global_accumulators", docname="Global Accumulators",
        doc="Number of global accumulators.", category='Resources', show_in_cores='MetaCore')

    fpu_type = _Field(45, "fpu_type", docname="FPU Type", category='Resources',
        doc="Presence and type of Floating Point Unit.", type=MetaFPUType, show_in_cores='MetaCore')

    dsp_type = _Field(46, "dsp_type", docname="DSP Type", category='Resources', type=MetaDSPType, show_in_cores='MetaCore')

    cache_type = _Field(47, "cache_type", docname="Cache Type",  category='Cache', type=MetaCacheType, show_in_cores='MetaCore')

    debug_type = _Field(48, "debug_type", docname="Debug Type", category='Core Information', type=MetaDebugType, show_in_cores='MetaCore')

    txenable0 = _Field(49, 'txenable0', docname='TXENABLE register of first thread', category='Core Information',  show_in_cores='MetaCore')

    metac_id = _Field(50, 'metac_id', docname='METAC_ID register', category='Core Information',  show_in_cores='MetaCore')

    core_id_reg = _Field(51, 'core_id_reg', docname='CORE_ID register', category='Core Information')

    core_config2 = _Field(52, 'core_config2', docname='CORE_CONFIG2 register', category='Core Information')

    core_config3 = _Field(53, 'core_config3', docname='CORE_CONFIG3 register', category='Core Information',  show_in_cores='MetaCore')


class MCPCore(MetaCore):
    pass

class MipsLegacyCore(MetaCore):
    """
    This is a :class:`MetaCore` table for use with MIPS cores on old DA-net 
    firmware.  The DA-net firmware before 5.4 did not have a separate table 
    layout for MIPS cores so a MipsLegacyCore with a ``core_img_id`` of 
    ``'mips_legacy'`` should be used.

    >>> core = MipsLegacyCore(core_img_id='mips_legacy')

    All fields are ignored by the Probe.
    """

class MipsCMCore(Core):
    """A table entry for a MIPS Coherency Manager.

    >>> core = MipsCMCore(core_img_id='mips_cm')

    All fields are ignored by the Probe.
    """

class MipsCore(Core):
    """A table entry for a MIPS core.

    Valid keywords are any of the fields in :class:`Core` :

        >>> core = MipsCore(core_img_id='mips')
        >>> '0x%x' % (core.core_img_id,)
        '0x20'

    """
    dcr = _Field(2, 'dcr', docname="Debug Control Register", category='Core Information',
        doc='Value of the Debug Control DRSEG register.')
    prid = _Field(3, 'prid', docname="PRId Register", category='Core Information',
        doc='Value of the PRId cp0 register.')
    config = _Field(4, 'config', array_size=8, docname="Config Registers", category='Core Information',
        doc='Values of the Config and Config1-7 cp0 registers for those that exist, 0 for those that don\'t.')
    mvp_conf0 = _Field(12, 'mvp_conf0', docname="MVPConf0 Register", category='Core Information',
        doc='Value of the MVPConfig0 register if MT is enabled, 0 if not.')
    num_vcs = _Field(13, 'num_vcs', docname="Number of VPs for OCI/DBU cores", category='Core Information',
        doc='Number of VPs in OCI/DBU cores, or 0 for EJTAG cores.')
    bev_overlay_base = _Field(14, 'bev_overlay_base', docname='BEV Overlay Base Address', category='Core Information',
        doc='Begin address for the BEV Overlay, this field is auto(0xffffffff) when no BEV overlay is in use.')
    bev_overlay_size = _Field(15, 'bev_overlay_size', docname='BEV Overlay Size', category='Core Information',
        doc='Length of the BEV Overlay in bytes, this field is auto(0xffffffff) when no BEV overlay is in use.')
    gcr_config = _Field(16, 'gcr_config', docname='GCR_CONFIG Register', category='Core Information',
        doc='Contents of the Global Config Register found in CPS systems.')
    ibs = _Field(17, 'ibs', docname='Instruction Breakpoint Status Register', category='Core Information',
        doc='Contains information about the number and capability of hardware code breakpoints.')
    dbs = _Field(18, 'dbs', docname='Data Breakpoint Status Register', category='Core Information',
        doc='Contains information about the number and capability of hardware data breakpoints.')
    cbtc = _Field(19, 'cbtc', docname='Complex Break and Trigger Control register', category='Core Information',
        doc='Contents of the Complex Break and Trigger Control register, if CBT is supported, otherwise 0.')
    trace_word_length = _Field(20, 'trace_word_length', docname='Trace Word Length', category='Core Information',
        doc='Size of one PDtrace word in bits, if tracing logic is implemented, otherwise 0.')
    bev_base_phys = _Field(21, 'bev_base_phys', docname='BEV Overlay Base (Physical)', category='Core Information',
        doc='The physical address of the BEV overlay, this field is auto(0xffffffff) when no BEV overlay is in use.')
    perfctl_count = _Field(22, 'perfctl_count', docname='Performance Register Count',  category='Core Information',
        doc='This is a count of how many perfctl+perfcount register pairs the core supports.')
    watch_count = _Field(23, 'watch_count', docname='WatchPoint Register Count', category = 'Core information',
        doc='This is a count of many watch hi+lo pairs the core supports.')
    srsctl = _Field(24, 'srsctl', docname = 'srsctl register', category = 'Core Information',
        doc='Value of the srsctl register used to determine the number of shadow register sets')
    vpeconf0 = _Field(25, 'vpeconf0',docname = 'vpeconf0 register', category = 'Core Information',
        doc='Value of the vpeconf0 register if MT is enabled, 0 if not.')
    vpeconf1 = _Field(26, 'vpeconf1',docname = 'vpeconf1 register', category = 'Core Information',
        doc='Value of the vpeconf0 register if MT is enabled, 0 if not.')
    tcbconfig = _Field(27, 'tcbconfig',docname = 'tcbconfig register', category = 'Core Information',
        doc='Value of the TCBConfig register if PDTrace hardware is supported else 0')    


def board_from_values(values, format='expression'):
    """Convert a list of 32-bit values read from the probe into a Board."""
    board = Board.from_values(values)
    offset = board.size // 4
    for _soc_count in range(board.num_of_socs):
        soc = SoC.from_values(values[offset:])
        board.socs.append(soc)
        offset += soc.size // 4
        for _core_count in range(soc.num_of_cores):
            core = Core.from_values(values[offset:])
            core_type = get_core_class(core.core_img_id)
            core = core_type.from_values(values[offset:])
            offset += core.size // 4
            soc.cores.append(core)
    board.default_format = format
    return board

def board_as_values(board):
    """Convert a Board into a list of 32-bit values for writing to the Probe."""
    values = board.as_values()
    for soc in board.socs:
        values.extend(soc.as_values())
        for core in soc.cores:
            values.extend(core.as_values())
    return values

# [[[end]]]

from imgtec.codescape import hwdefs
from imgtec.console.support import parse_memory_descriptor, AddressRangeType, sign_extend_32_to_64, require_device
import difflib, re

def check_mode(device):
    if device.probe.mode not in ('table', 'autodetected'):
        raise RuntimeError('The probe must not be in %s mode. Please use the autodetect command.' % (device.probe.mode,))

@command(device_required=False)
def targetdata(new_board=None, format='expression', write=None, device=None):
    """Display, update, or load a target detection data table.

    When called with no arguments then the detection data from the probe is read 
    and returned.

    If `new_board` is specified and it is a tdd.Board instance (from a prior call
    to targetdata(), or by directly constructing a table using the tdd module).
    The board will then be written to the probe.
    
    If `new_board` is specified and it is a string, then it is treated as the 
    name or path of a board file to be loaded. If it is an absolute path then 
    the board file will be loaded from there. If just a name is given then the 
    usual Hardware Definition directories will be searched for a board file.  If
    no extension is given then ``.board`` will be assumed.
    
    If the load is successful and write is not explicitly False, then the target 
    data will then be written to the probe.
    
    For example, to read the current table from the probe ::

        >>> board = targetdata()

    Read the table from a board file and write it to the probe ::

        >>> targetdata('boardname')

    Read, then modify, and then write a board from/to the probe ::

        >>> board = targetdata()                         # doctest: +SKIP
        >>> board.socs[0].cores[0].dcr |= 0x80000000     # doctest: +SKIP
        >>> targetdata(board)                            # doctest: +SKIP

    Load a board from a file, but *do not* write it to the probe ::

        >>> board = targetdata('filename.board', write=False)   # doctest: +SKIP

    To save board files, please see the :func:`makehd` command.

    Some fields are array fields, for example config[0-7], these can be
    retrieved/modified using the normal python syntax for a sequence ::

        >>> board.socs[0].cores[0].config[1] = 0x80000000       # doctest: +SKIP
        >>> board.socs[0].cores[0].config= [0x80000000] + [0]*6 # doctest: +SKIP
        >>> board.socs[0].cores[0].config                       # doctest: +SKIP
        [0x800000000, 0, 0, 0, 0, 0, 0, 0xffffffff]             # doctest: +SKIP

    The return type is always a tdd.Board object.  By default this will display
    using a format that is copy pasteable into a python script which contains
    ``from imgtec.console import tdd``. 

    `format` may be one of 'expression' (the default), 'text', or 'xml', and if
    given this will change the default display format of the returned board.  
    'expression' is a python evaluatable expression for using in scripts.  
    'text' is a slightly more human readable representation and 
    'xml' is suitable for use in Codescape Debugger board files.  

    See :ref:`tdd-intro` for more information on target detection data
    """
    if new_board is None or write is not False:
        require_device(device)
    if new_board is None:
        check_mode(device)
    if isinstance(new_board, basestring):
        path = _find_board_file_by_name(new_board, get_all_hsp_paths2())
        new_board = _xml_as_board(hwdefs.load(path))
                    
    if new_board:    
        if write is False:
            return new_board        
        device.tiny.WriteDAConfigurationData(board_as_values(new_board))
        device.probe.scan_devices()
    return board_from_values(device.tiny.ReadDAConfigurationData(), format=format)
    
def _from_xml_name(name):
    if isinstance(name, str): return name
    try:
        return name.encode('ascii')
    except UnicodeEncodeError:
        return name
    
def _xml_to_table(elem, identifier, cls):
    settings = dict([(s.name, int(s.value, 0)) for s in elem.find_by_type(hwdefs.Setting)])
    if cls is Core:
        cls = get_core_class(settings.get('core_img_id', 0))
    obj = cls(name=_from_xml_name(elem.name))
    valid, invalid = 0, 0
    for name, value in settings.items():
        m = re.match(r'(\w+)(?:\[(\d+)])?', name)
        name, index = m.group(1, 2)
        try:
            if index:
                l = getattr(obj, name)
                l[int(index, 0)] = value
            else:
                setattr(obj, name, value)
            valid += 1
        except AttributeError:
            print 'Unknown setting %s for object %s' % (name, type(obj).__name__)
            invalid += 1
    if valid == 0:
        raise RuntimeError('%s does not contain any target data' % (identifier, ))
    return obj
    
def _xml_as_board(doc):
    board_elems = doc.find_by_type(hwdefs.Board)
    if not board_elems:
        raise RuntimeError('%s does not contain a board' % (doc.filename,))
    board = Board(name=_from_xml_name(board_elems[0].name))
    soc_elems = board_elems[0].find_by_type(hwdefs.SoC)
    if not soc_elems:
        raise RuntimeError('%s does not contain any SoCs' % (doc.filename,))
    for socn, soc_elem in enumerate(soc_elems):
        soc = _xml_to_table(soc_elem, 'soc%d' % (socn,), SoC)
        core_elems = soc_elem.find_by_type(hwdefs.CoreInfo)
        if not core_elems:
            raise RuntimeError('%s:soc%d does not contain any cores' % (doc.filename,socn))
        for coren, core_elem in enumerate(core_elems):
            soc.cores.append(_xml_to_table(core_elem, 's%dc%d' % (socn,coren), Core))
        board.socs.append(soc)
    return board
    
def _did_you_mean(needle, haystack):
    possibles = difflib.get_close_matches(needle, haystack, 5)
    
    if possibles:
        one_of = '' if len(possibles) == 1 else ' one of'
        return 'Did you mean%s: %s' % (one_of, ' '.join(possibles))
    else:
        return 'No possible matches were found'

def _find_board_file_by_name(name, search_paths, os=os):
    if os.path.isabs(name):
        if os.path.exists(name):
            return name
        raise RuntimeError("%s does not exist" % (name,))
    possibles = set()
    path = name
    if not os.path.splitext(path)[1]:
        path += '.board'
    ext = os.path.splitext(path)[1]
    for d in search_paths:
        # only consider things that end with the same extension as possibles
        possibles.update([f for f in os.listdir(d) if f.endswith(ext)])
        tryit = os.path.join(d, path)
        if os.path.exists(tryit):
            return tryit
    possibles = _did_you_mean(name, possibles)
    raise RuntimeError("%s not found, search paths were:\n  %s\n%s"
                % (path,'\n  '.join(search_paths), possibles))
                
leave = named('leave')
bf_named = [(auto, 'auto'), (leave, 'leave')]
@command(memory=bf_named, registers=bf_named, targetdata=bf_named, verbose=verbosity)
def boardfile(name=None, path=None, memory='leave', registers='leave', 
            targetdata='leave', verbose=1, overwrite=False, device=None):
    '''Create or update a board file for this target.
    
    A board file configures Codescape Debugger and the probe with:
    
     * valid memory - to prevent system hangs due to debugger memory accesses.
     * registers - for the peripheral region.
     * target data - to prevent probe auto detection.     
    
    To update a Ci40 board file with the given memory layout::
   
     >>> boardfile('Ci40', memory='4K@0xbfc00000@boot')
           
    Update the Ci40 board file with redetected peripheral registers,
    (in this case the core files will be overrwritten)::

     >>> boardfile('Ci40', registers=auto)
    
    Load the Ci40 board file and replace the current targetdata with that found
    on the probe::

     >>> boardfile('Ci40', targetdata=auto)
     
    These can be combined to update memory, targetdata, and registers::
    
     >>> boardfile('Ci40', memory='4K@0xbfc00000@boot',
     ...                   targetdata=auto,
     ...                   registers=auto)
     
    If the board file does not already exist then 'auto' will be assumed for 
    each option that is 'leave'. So to create a board file with the best 
    available data this is sufficient::
    
     >>> boardfile('Ci40')
     
    targetdata, memory and registers can also be False, meaning remove them. 
    For example this removes linked register xml files::
    
     >>> boardfile('Ci40', registers=False)
    
    Note that this does not delete the register xml file, only the link to it in
    the .board file.
    
    ========== =================== ==========================================================================
    Parameter  Values              Meaning
    ========== =================== ==========================================================================
    name       string              The file name to use for the board file generated. This is required unless
                                   path is given, in which case path should be the full path of the board file.
    path       string              Location to write files to. If this is not given then the user hardware
                                   definition files directory will be used, which is usually ~/imgtec/hwdefs.
    memory     memory descriptor,  Specify memory blocks for each type of core. This can either be a single 
               auto,               string or a dictionary of strings keyed on core ID. Multiple memory ranges
               leave,              can be separated by a comma or newline.
               False        
                                   For example, the following will add a single memory range to all MIPS 
                                   cores found. (excluding coherency managers)
                                   
                                    '4K@0xbfc00000@boot,1K@0x80000000@stack'
                                   
                                   To apply that memory only to specific type of core, the key
                                   can be either a core ID (i.e. PRId) or a name which will
                                   be matched case insensitively to the start of the core's
                                   display_name (as returned from :func:`cpuinfo`):
                                   
                                    >>> dict(interAptiv='8K@0xbfc00000@boot,1K@0x80000000@stack',
                                        microAptiv='4K@0xbfc00000@boot,1K@0x80000000@stack')
                                   
                                   If memory ranges are not given for a MIPS core, default memory will be 
                                   provided, equivalent to: (address sign extended for 64 bit cores)
                                   
                                       '32K@0xbfc00000@boot vector'
                                   
                                   Each memory block string has the syntax:
                                     
                                       <block size>@<address>@<name>
                                       
                                   <block size> indicates the size of the memory block and must be an
                                   integer or an abbreviation using 'K' or 'M' for kilobyte and megabyte
                                   respectivley.
                                     
                                   <address> start address of the block
                                     
                                   <name> the name of the block
                                     
                                   If memory ranges are not given for a non-MIPS core, no memory
                                   will be created.
                          
    registers   auto,              If True, xml files will be generated for each core in addition to the 
                leave,              main hardware definition file. Otherwise installed hardware support files 
                False              will be searched to find a matching file which will be linked to by the 
                                   generated file which defines the target as a whole.
    targetdata  auto,              If True include the probes targetdata will be written to the hardware 
                leave,             definition file.
                False
    ========== =================== ==========================================================================
    
    '''
    if name is None:
        if path is None:
            raise RuntimeError("Board name is required if path is not given.")
        board_path = path
    else:
        path = path or get_user_files_dir('hwdefs')
        board_path = os.path.join(path, name + '.board')
        
    check_mode(device)
    
    expected = ['auto', 'leave', False]
    if targetdata not in expected:
        raise RuntimeError("targetdata must be one of %r" % expected)
    if registers not in expected:
        raise RuntimeError("registers must be one of %r" % expected)
    
    doc = generatehd(device.probe, board_path, memory, registers, targetdata, verbose, overwrite)
    doc.save(board_path)
    return board_path
    
@command(verbose=verbosity)
def makehd(name=None, output_dir=None, memory_ranges=None, generate_core=True, targetdata=True, verbose=1, device=None):
    '''
    Create a board file for this target, including table and register data.

    A board file for a target configures the probe, the registers on each core,
    and the accessible memory on each core.
    
    >>> makehd('Ci40', './hsps/', {0x12345678:'4K@0xbfc00000@boot'})
    Writing to ./hsps/interAptivMP-SoC0-Core0.xml
    Writing to ./hsps/interAptivMP-SoC0-Core1.xml
    ./hsps/Ci40.board
    
    >>> makehd('MyBoard', './hsps/', '4K@0xbfc00000@boot', generate_core=False)
    ./hsps/MyBoard.board
    
    =============== ==========================================================================
    Parameter       Meaning
    =============== ==========================================================================
    name            The file name to use for the board file generated. This is required.
    output_dir      Location to write files to. If this is not given then the user hardware
                    definition files directory will be used, which is usually ~/imgtec/hwdefs.
    memory_ranges   Specify memory blocks for each type of core. This can either be a single 
                    string or a dictionary of strings keyed on core ID. Multiple memory ranges
                    can be separated by a comma or newline.
    
                    For example, the following will add a single memory range to all MIPS 
                    cores found. (excluding coherency managers)
                    
                    '4K@0xbfc00000@boot,1K@0x80000000@stack'
                    
                    To apply that memory only to specific type of core:
                    
                    dict(0x12345678='4K@0xbfc00000@boot,1K@0x80000000@stack')
                    
                    If memory ranges are not given for a core, default memory will be 
                    provided, equivalent to: (address sign extended for 64 bit cores)
                    
                        '32K@0xbfc00000@boot vector'
                    
                    Each memory block string has the syntax:
                      
                        <block size>@<address>@<name>
                        
                      <block size> indicates the size of the memory block and must be an
                      integer or an abbreviation using 'K' or 'M' for kilobyte and megabyte
                      respectivley.
                      
                      <address> start address of the block
                      
                      <name> the name of the block
                    
    generate_core   If True, xml files will be generated for each core in addition to the 
                    main hardware definition file. Otherwise installed hardware support files 
                    will be searched to find a matching file which will be linked to by the 
                    generated file which defines the target as a whole.
    targetdata      If True include the SoC/core's targetdata in the hardware definition file.
    =============== ==========================================================================
    
    '''
        
    return boardfile(name=name, 
        path=output_dir, 
        memory='leave' if memory_ranges is None else memory_ranges, 
        registers='auto' if generate_core else False, 
        targetdata='auto' if targetdata else False, 
        verbose=verbose, 
        overwrite=True, 
        device=device)
    
def get_user_hwdefs_dir():
    return get_user_files_dir('hwdefs')
    
def get_default_hwdefs_dirs():
    import platform
    from imgtec.lib.img_settings import ImgSettings

    order = "Path", "Path_64"
    if platform.architecture(0)[0] == "64bit":
        order = order[1], order[0]

    core_defs = ImgSettings("HSP").section("CoreDefs")
    order = [core_defs.get(x, core_defs.get(x.lower())) for x in order]
    return [x for x in order if x and os.path.isdir(x)]
    
def get_all_hsp_paths2():
    return [ get_user_hwdefs_dir()] + get_default_hwdefs_dirs()
    
def all_hsp_files(extension=None):
    for d in get_all_hsp_paths2():
        try:
            for f in sorted(os.listdir(d)):
                if extension is None or f.endswith(extension):
                    yield os.path.join(d, f)
        except OSError:
            pass
    
def find_core_id_file_by_core_id(core_id):
    for path in all_hsp_files('.core_id'):
        doc = hwdefs.load(path)
        if doc and doc.children and isinstance(doc.children[0], hwdefs.CoreID):
            coreid_file = doc.children[0]
            if coreid_file.value == core_id:
                return path
    return None
    
def disambiguate_name(name, previous):
    '''
    >>> disambiguate_name('foo', [])
    'foo'
    >>> disambiguate_name('foo', ['foo'])
    'foo-1'
    >>> disambiguate_name('foo', ['foo', 'foo-1'])
    'foo-2'
    '''
    base_name = name
    count = 1
    while name in previous:
        name = ''.join([base_name, '-%d' % count])
        count += 1
    return name

def add_targetdata(obj, targetdata):
    for setting in targetdata.known_fields():
        if setting != 'size':
            value = getattr(targetdata, setting)
            if hasattr(value, '__len__'):
                for i, item in enumerate(value):
                    f = obj.create(hwdefs.Setting)
                    f.name = "%s[%d]" % (setting, i)
                    f.value = '0x%0x' % item
            else:
                f = obj.create(hwdefs.Setting)
                f.name = setting
                f.value = '0x%0x' % value
                
def remove_children(obj, to_remove):
    while list(obj.iterchildren_by_type(to_remove)):
        for i, child in enumerate(obj.children):
            if isinstance(child, to_remove):
                obj.remove(i)
                #Need to go from the beginning each time because indexes change
                break
        
def get_default_mem(cpu_info):
    start = 0xbfc00000
    start = start if cpu_info['cpu_is_32bit'] else sign_extend_32_to_64(start)
    return [(AddressRangeType(start, start+0x8000, name='boot vector'), 0)]
    
def core_id_from_cpuinfo(cpu_info):
    if 'prid' in cpu_info:
        return cpu_info['prid'] & 0xFFFFFF00
    elif 'core_id' in cpu_info:
        return cpu_info['core_id'] & 0x000000FF
    else:
        return None
        
def get_core_id_mask(cpu_info):
    if 'prid' in cpu_info:
        return 0xFFFFFF00
    elif 'core_id' in cpu_info:
        return 0x000000FF
        
def get_core_ranges(core, cpu_info, memory_ranges):
    from imgtec.console.regdb import CoreFamily
    core_id = core_id_from_cpuinfo(cpu_info)
    core_mem_ranges = []

    if core_id and core.family == CoreFamily.mips:
        for id in memory_ranges:
            #Either hex no. matches or name is in the display name
            if id != 'all' and (
                (isinstance(id, str) and id.lower() in cpu_info['display_name'].lower()) or
                (not isinstance(id, str) and id & get_core_id_mask(cpu_info)) == core_id):
                core_mem_ranges = memory_ranges[id]
                break
        else:
            if 'all' in memory_ranges:
                core_mem_ranges = memory_ranges['all']
            else:
                core_mem_ranges = get_default_mem(cpu_info)
    
    return core_mem_ranges
    
def validate_board_file(board_path, overwrite):
    exists = os.path.isfile(board_path)
    
    if not overwrite and exists:
        raise RuntimeError("'{}' already exists, set overwrite=True to overwrite it.".format(board_path))
            
    if exists:
        try:
            doc = hwdefs.load(board_path)
        except Exception as e:
            exists = False
            print "Warning: existing file isn't a valid board file - %s" % (str(e))
        else:
            if not doc.children or not isinstance(doc.children[0], hwdefs.Board):
                raise RuntimeError('Existing file is not a valid board file.')
            board = doc.children[0]
    
    name = os.path.splitext(os.path.basename(board_path))[0]
    # Note that exists may have changed by this point. This is to differentiate
    # there being a valid board file which we can load vs a file with that name
    # that isn't a board file. (mainly for testing)
    if not exists:
        doc = hwdefs.empty_document()
        board = doc.create(hwdefs.Board)
        board.name = name
        
    return exists, board_path, doc, board, name
    
def normalise_memory_ranges(memory_ranges, exists):
    if memory_ranges == 'leave' and not exists:
        memory_ranges = 'auto'
        
    if memory_ranges is None or memory_ranges == 'auto':
        memory_ranges = {}
    elif isinstance(memory_ranges, str) and memory_ranges not in ['auto', 'leave']:
        memory_ranges = {'all' : [parse_memory_descriptor(f) for f in memory_ranges.split(',')]}
    elif memory_ranges not in ['leave', 'auto', False]:
        for core_id in memory_ranges:
            memory_ranges[core_id] = [parse_memory_descriptor(f) for f in memory_ranges[core_id].split(',')]
            
    return memory_ranges
    
def generatehd(probe, board_path, memory_ranges, generate_core, targetdata, verbose, overwrite):
    from imgtec.console.regdb import makecorehd
    
    exists, board_path, doc, board, name = validate_board_file(board_path, overwrite)
    memory_ranges = normalise_memory_ranges(memory_ranges, exists)
    
    if targetdata == 'leave' and not exists:
        targetdata = 'auto'
    
    if exists:
        socs_in_board = len(list(board.iterchildren_by_type(hwdefs.SoC)))
        socs_on_probe = len(probe.socs)
        if socs_in_board != socs_on_probe:
            raise RuntimeError('Existing board file has %d SoC(s) but the target has %d SoC(s).' % (socs_in_board, socs_on_probe))
            
        for socnum, socs in enumerate(zip(probe.socs, board.iterchildren_by_type(hwdefs.SoC))):
            probe_soc, board_soc = socs
            
            if targetdata != 'leave':
                remove_children(board_soc, hwdefs.Setting)
                
                if targetdata:
                    add_targetdata(board_soc, probe_soc.targetdata)
            
            board_cores_in_soc = len(list(board_soc.iterchildren_by_type(hwdefs.CoreInfo)))
            probe_cores_in_soc = len(probe_soc.cores)
            
            if board_cores_in_soc != probe_cores_in_soc:
                raise RuntimeError('Existing SoC %d has %d core(s) but the target has %d core(s).' % (socnum, board_cores_in_soc, probe_cores_in_soc))
            
            for probe_core, board_core in zip(probe_soc.cores, board_soc.iterchildren_by_type(hwdefs.CoreInfo)):
                cpu_info = dict(probe_core.tiny.CpuInfo())
                if memory_ranges != 'leave':
                    #Remove existing 
                    remove_children(board_core, hwdefs.MemoryType)
                    
                    if memory_ranges == 'auto':
                        #Put in bfc default
                        add_memory_ranges(board_core, get_default_mem(cpu_info))
                    elif memory_ranges != False:
                        #Must be valid descriptors (note that this might return the defaults too)
                        add_memory_ranges(board_core, get_core_ranges(probe_core, cpu_info, memory_ranges))
                        
                if generate_core != 'leave':
                    remove_children(board_core, hwdefs.ProcessorLink)
                        
                    if generate_core:
                        f = makecorehd(output_dir=os.path.dirname(board_path), 
                                output_name=core_xml_filename(name, cpu_info['display_name'], probe_core), 
                                verbose=verbose, 
                                device=probe_core.vpes[0])
                        if f:
                            pl = board_core.create(hwdefs.ProcessorLink)
                            pl.name = board_core.name
                            pl.source = os.path.basename(f.hd_path)
                            
                if targetdata != 'leave':
                    remove_children(board_core, hwdefs.Setting)
                    
                    if targetdata:
                        add_targetdata(board_core, probe_core.targetdata)
    else:
        make_new_board_file(name, board_path, board, probe, generate_core, 
            memory_ranges, targetdata, verbose)
                
    return doc
    
def core_xml_filename(board_name, core_name, core):
    return '%s-%s-SoC%d-Core%d' % (board_name, core_name, core.soc.index, core.index)
    
def make_new_board_file(name, board_path, board, probe, registers, memory, targetdata, verbose):
    for soc in probe.socs:
        new_soc = board.create(hwdefs.SoC)
        new_soc.name = soc.name
        
        opts = dict(auto=True, leave=False)
        if opts.get(targetdata, targetdata):
            add_targetdata(new_soc, soc.targetdata)
        
        try:
            if memory in opts:
                memory = {}
        except TypeError: 
            #Unhashable (dict)
            pass
        
        core_names = set()        
        for core in soc.cores:
            core_names.add(
                make_core_file(new_soc, core, name, registers, 
                    os.path.dirname(board_path), verbose, memory, core_names, targetdata))
    
def make_core_file(soc_obj, core, board_name, generate_core, path, verbose, memory_ranges, core_names, targetdata):
    from imgtec.console.regdb import makecorehd
    cpu_info = dict(core.tiny.CpuInfo())
    core_name = cpu_info['display_name']
    core_id = core_id_from_cpuinfo(cpu_info)
    
    #Try to generate an hd file
    outname = core_xml_filename(board_name, core_name, core)
    file_path = None
    if generate_core:
        f = makecorehd(output_dir=path, output_name=outname, verbose=verbose, device=core.vpes[0])
        if f:
            #Use file name here as a relative path, but files found by searching need the full path.
            file_path = os.path.split(f.hd_path)[1]
            
    core_mem_ranges = get_core_ranges(core, cpu_info, memory_ranges)
                            
    if not file_path:
        #Look for a file
        file_path = find_core_id_file_by_core_id(core_id)
        
        if file_path:
            print '  %s: Matched core_id 0x%08x to %s' % (core_name, core_id, str(file_path))
           
    core_name = disambiguate_name(core_name, core_names)
    create_core(soc_obj, core_name, file_path, core.targetdata if targetdata else None, core_mem_ranges)
    return core_name
    
def create_core(nsoc, name, file_path, targetdata, memory_ranges):
    ncore = nsoc.create(hwdefs.CoreInfo)
    ncore.name = name
        
    if file_path:
        npl = ncore.create(hwdefs.ProcessorLink)
        npl.name = name
        npl.source = file_path
    
    if targetdata:
        add_targetdata(ncore, targetdata)
    
    if memory_ranges:
        add_memory_ranges(ncore, memory_ranges)
            
def add_memory_ranges(core, ranges):
    mem_type = core.create(hwdefs.MemoryType)
    mem_type.name = 'default'
    range_no = 0
    names = set()
    unnamed_ranges = []

    #Named ranges first
    for rng in ranges:
        rng = rng[0] #Ignore memory type

        if not rng.name:
            unnamed_ranges.append(rng)
            continue

        if rng.name in names:
            raise RuntimeError("Memory range names must be unique (\"%s\")" % rng.name)

        names.add(rng.name)
        add_mem_range_to_type(rng, mem_type)

    #Then go back and make up names
    for rng in unnamed_ranges:
        while True:
            name = "memory_range_%d" % range_no
            if name in names:
                range_no += 1
            else:
                break

        names.add(name)
        rng.name = name
        add_mem_range_to_type(rng, mem_type)

def add_mem_range_to_type(rng, mem_type):
    r = mem_type.create(hwdefs.MemoryBlock)
    r.name = rng.name
    r.start_address = rng.begin
    r.end_address = rng.end-1
    r.cacheable = True

target_data = targetdata

if __name__ == '__main__':
    import doctest
    doctest.testmod()
