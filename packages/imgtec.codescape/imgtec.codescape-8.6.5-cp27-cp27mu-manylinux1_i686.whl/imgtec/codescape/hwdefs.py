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


"""
This module lists and describes the classes and functions used to create and manipulate the XML text
that represents a Hardware Definition of some particular hardware primarily for use in Codescape
Debugger but also for the application developer to tailor the Hardware Definition to their
requirements.

The recommended method for creating :class:`Document` objects is with the module functions:

:func:`empty_document`: for getting an initially empty :class:`Document` object.

:func:`load`: for loading and parsing an XML file and obtaining the :class:`Document` object representing
the entire Hardware Definition.

And for creating objects representing a particular class of Hardware Definition object:

:func:`loads`: for loading XML text fragments and returning an object representing the XML text fragment.

"""

from xml.dom import Node, EMPTY_NAMESPACE
from imgtec.lib.namedenum import namedenum
import os.path
import sys
from imgtec.lib.ordered_dict import OrderedDict
from collections import namedtuple
from imgtec.codescape import img_xml
    
XmlError = RuntimeError

# Note __all__ is updated at the end of this module
__all__ = [
    'HDObject',
    'factory',          # added for export visibility but not documented so not added to API documentation
    'empty_ioconfig',   # ditto
    'BSPSpacerEOL',     # ditto
] 

Size = namedenum('Size', 'uint8 uint16 uint32 uint64')
SizeBytes = {Size.uint8:1, Size.uint16:2, Size.uint32:4, Size.uint64:8}
_size_mappings = {'sb':Size.uint8, 'sw':Size.uint16, 'sl':Size.uint32, 'sd':Size.uint32, 'sq':Size.uint64}
                      
Access = namedenum('Access', 'read_only write_only read_write read_once write_once')
_access_mappings = {'ro':Access.read_only, 'wo':Access.write_only, 'rw':Access.read_write, 'roc':Access.read_once, 'woc':Access.write_once}
_memory_access_mappings = {'ro':Access.read_only, 'wo':Access.write_only, 'rw':Access.read_write}

Radix = namedenum('Radix', 'binary octal decimal hex')

_radix_mappings = {'B':Radix.binary, 'O':Radix.octal, 'D':Radix.decimal, 'H':Radix.hex}
_radix_description = "Specifies the format of the item."

MemorySetting = namedenum('MemorySetting', 'static dynamic')

_setting_mappings = {'static':MemorySetting.static, 'dynamic':MemorySetting.dynamic}


Cacheable = namedenum('Cacheable', 'no yes')
CacheableSetting = Cacheable
_cacheable_mappings = {'cacheable':True, None:False}

PropertyKind = namedenum('PropertyKind', ('text',  0,    'Arbitrary text.'),
                                         ('path',  None, 'File path.'),
                                         ('enum',  None, 'Enumerated type.'),
                                         ('hex',   None, 'Up to 32 bit hexadecimal integer.'),
                                         ('hex64', None, 'Up to 64 bit hexadecimal integer.'),
                                         ('dec',   None, 'Decimal integer.'),
                                         ('expr',  None, 'Text expression suitable for evaluation in Codescape\'s expression evaluator.')
                        )
#"""Values from this enumerated type are used to indicate the type of the data associated with a particular Hardware Definition object property."""

class PropertyInfo(namedtuple('PropertyInfo', 'title name type description')):
    """A structure comprising 4 fields:
    
    :title:         Used when showing the value of the property.
    
    :name:          The name of the property.
    
    :type:          A :class:`PropertyKind` value indicating the type of the property's value.
    
    :description:   A description of what this property means. e.g. "Number of test access ports. A positive integer."
    """
    pass

def file_line(node, filename=None):
    if hasattr(node, 'line'):
        if filename:
            filename = os.path.basename(filename)
        else:
            filename = "Text"
        return "%s(%d): tag '%s'" % (filename, node.line, node.tagName)
    return "Tag '%s'" % node.tagName

class Warnings(object):
    """The default warnings class used by the various classes and functions of the Hardware Definition library."""
    def __init__(self):
        self.messages = []
        self.edited = False
       
    def report(self, node, msg, edited):
        if edited:
            self.edited = edited
            
        try:
            self.messages.index(msg)
        except:
            self.messages.append(msg)
        
    def clear(self):
        self.messages = []
        self.edited = False
        
tag_can_be_pimpl = {}

class _ctag_order(object):
    """
        This class is a list of tags which may also contain sublists for enumerated tags.
        The order in which the items are appended determines the order in which
        input tags are validated and where tag values are to placed in the DOM
        tree when values are are added so that any output xml is properly written.
        
        See tag_order_class_tests.py
        
    """
    def __init__(self, order = None):
        self._order = {}
        self.flattened = []
        self.unflattened = []
        self._current_index = 0
           
    def __contains__(self, tag):
        return tag in self._order
    
    def __str__(self):
        return str(self.flattened)
         
    def __append_group(self, group, bump_current_index=True):
        global tag_can_be_pimpl
        if isinstance(group, list):
            for x in group:
                self.__append_group(x, False)
        else:
            if isinstance(group, tuple):
                if group[0] in self._order:
                    raise nested_tag_invisible("enum tag %s is hidden by non enum tag" % group[0])
                self._order[group[0]] = self._current_index
                self.flattened.append(group[0])
                tag_can_be_pimpl[group[0]] = group[1]
            else:
                if group in self._order:
                    raise nested_tag_invisible("enum tag %s is hidden by non enum tag" % group)
                self._order[group] = self._current_index
                self.flattened.append(group)
                tag_can_be_pimpl[group] = True
        if bump_current_index:
            self._current_index += 1

    def append(self, tag, prop_name, depth=0):
        global tag_can_be_pimpl
        if prop_name:
            if isinstance(tag, list):
                for tp in tag:
                    self.unflattened.append((prop_name, tp[0] if isinstance(tp, tuple) else tp))
            else:
                self.unflattened.append((prop_name, tag[0]))
        if isinstance(tag, list):
            for x in tag:
                if isinstance(x, list):
                    self.__append_group(x)
                else:
                    if isinstance(x, tuple):
                        if x[0] in self._order:
                            raise nested_tag_invisible("enum tag %s is hidden by non enum tag" % x[0])
                        self._order[x[0]] = self._current_index
                        self.flattened.append(x[0])
                        tag_can_be_pimpl[x[0]] = x[1]
                    else:
                        if x in self._order:
                            raise nested_tag_invisible("enum tag %s is hidden by non enum tag" % x)
                        self._order[x] = self._current_index
                        self.flattened.append(x)
                        tag_can_be_pimpl[x] = True
        elif isinstance(tag, tuple):
            if tag[0] not in self._order:
                self._order[tag[0]] = self._current_index
                self.flattened.append(tag[0])
                tag_can_be_pimpl[tag[0]] = tag[1]
        elif tag not in self._order:
            self._order[tag] = self._current_index
            self.flattened.append(tag)
            tag_can_be_pimpl[tag] = True
        self._current_index += 1
        
    def order_of(self, tag):
        try:
            return self._order[tag]
        except KeyError:
            raise ValueError("tag %s isn't valid" % tag)
        
    def validate(self, obj, all_tags):
        class ctags(list):
            def pop(self, index):
                del self[index]
                self[:] = uniqued_adjacent_items(self)
                return len(self) == 0
        
        tags = ctags(uniqued_adjacent_items(remove_unexpected_tags(all_tags, self.flattened)))
        if all_tags:
            for tag in all_tags:
                msg = "%s: tag '%s' is unsupported in the Hardware Definition Editor" % (obj.msg_hdr(), tag)
                obj.warnings.report(obj, msg, None)
            while bool(all_tags):
                all_tags.pop(0)
                
        if tags:
            for tag in self.flattened:
                while True:
                    try:
                        reduced_tag_index = tags.index(tag)
                    except:
                        break
                    if reduced_tag_index == 0:
                        if tags.pop(reduced_tag_index):
                            return
                    else:
                        reduced_tag_order = self.order_of(tag)
                        for i in xrange(reduced_tag_index):
                            if self.order_of(tags[i]) > reduced_tag_order:
                                msg = "%s: %s is in the wrong position" % (obj.msg_hdr(), tag)
                                obj.warnings.report(obj, msg, None)
                                break
                        if tags.pop(reduced_tag_index):
                            return
            
            
class nested_tag_invisible(Exception):
    pass

def flatten(children):
    """
    >>> flatten([])
    []
    >>> flatten([1, 2, 3])
    [1, 2, 3]
    >>> flatten([[1, 2], 3])
    [1, 2, 3]
    >>> flatten([[[1], 2], 3])
    [1, 2, 3]
    """
    
    flat = []
    if isinstance(children, list):
        for child in children:
            flat.extend(flatten(child))
    else:
        flat.append(children)
    return flat
                    
def remove_unexpected_tags(all_element_tags, valid_value_tags):
    element_tags = [x for x in all_element_tags if x in valid_value_tags]
    for tag in element_tags:
        while True:
            try:
                all_element_tags.pop(all_element_tags.index(tag))
            except ValueError as e:
                break
    return element_tags

def uniqued_adjacent_items(items):
    """
    >>> uniqued_adjacent_items([])
    []
    >>> uniqued_adjacent_items([1, 2, 3])
    [1, 2, 3]
    >>> uniqued_adjacent_items([1, 1, 3])
    [1, 3]
    >>> uniqued_adjacent_items([1, 2, 3, 3, 2])
    [1, 2, 3, 2]
    >>> uniqued_adjacent_items([1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 2, 2, 2])
    [1, 2, 3, 2]
    """
    
    reduced_list = []
    if items:
        for x in items:
            if reduced_list:
                if x != reduced_list[len(reduced_list) - 1]:
                    reduced_list.append(x)
            else:
                reduced_list.append(x)
    return reduced_list
    
    
def unique(iter):
    """Returns a list containing each item unique item in iter, if the item is
    in iter more than once, only the first is kept.

    >>> unique(['a', 'b', 'e'])
    ['a', 'b', 'e']
    >>> unique(['a', 'e', 'b', 'e'])
    ['a', 'e', 'b']
    >>> unique([['a', 'b'], ['a', 'c'], ['a', 'd'], ['a', 'c'], ['a', 'e'], ['a', 'b']])
    Traceback (most recent call last):
    ...
    TypeError: unhashable type: 'list'
    """
    result, seen = [], set()
    for x in iter:
        if x not in seen:
            seen.add(x)
            result.append(x)
    return result


def children_property(tag_order, children):
    child_tags = []
    for child in children:
        if isinstance(child, list):
            child_tag_group = []
            for gchild in child:
                child_tag_group.extend([(tag, gchild.can_be_pimpl()) for tag in flatten(gchild.tag_name())])
            child_tags.append(child_tag_group)
        else:
            child_tags.extend([(tag, child.can_be_pimpl()) for tag in flatten(child.tag_name())])
    tag_order.append(child_tags, None)

def key_list(d):
    return [k for k in d.iterkeys() if k is not None]

def _add_class_property_tags(cls, propname, tags):
    if isinstance(tags, tuple):
        cls.class_attributes_map[propname] = [tags[0]]
    elif isinstance(tags, list):
        cls.class_attributes_map[propname] = list(tags)
    elif isinstance(tags, dict):
        cls.class_attributes_map[propname] = [k for k in tags.iterkeys()]
    elif tags and isinstance(tags, basestring):
        cls.class_attributes_map[propname] = [tags]
    else:
        cls.class_attributes_map[propname] = [cls.tag_name()]

def _make_tag_info(tag_order, tag_desc, format):
    tag_s, desc = tag_desc
    tag_s = tag_s[0] if isinstance(tag_s, tuple) else tag_s
    return (tag_s, desc, tag_order, format)

def _enum_property(cls, prop_name, tags_desc, default, doc=''):
    def enum_getter(obj):
        return obj._get_enum_tag(_make_tag_info(cls._tag_order, tags_desc, None), default)
    def enum_setter(obj, value):
        obj._set_enum_tag(_make_tag_info(cls._tag_order, tags_desc, None), value, default)

    _add_class_property_tags(cls, prop_name, tags_desc[0])
    cls._tag_order.append(key_list(tags_desc[0]), prop_name)
    return property(enum_getter, enum_setter, doc=doc)

def _property(prop_name, tag_order, tag_desc, getter, setter, doc):
    if tag_desc[0]:
        tag_order.append(tag_desc[0], prop_name)
    return property(getter, setter, doc=doc)
    
def get_name(node, name_attrs):
    for name_attr in name_attrs:
        node_name = node.getAttribute(name_attr)
        if node_name:
            return node_name


def _text_property(cls, prop_name, tag_desc, default, doc=''):
    """
        tag_desc                 a pair containing the tag and its description
        default                  the tags default value when getting
    """
    def text_getter(obj):
        return obj._get_text_value(_make_tag_info(cls._tag_order, tag_desc, "%s"), default)
    def text_setter(obj, value):
        obj._set_text_value(_make_tag_info(cls._tag_order, tag_desc, "%s"), value, default)

    _add_class_property_tags(cls, prop_name, tag_desc[0])
    return _property(prop_name, cls._tag_order, tag_desc, text_getter, text_setter, doc=doc)
    
def _numeric_property(cls, prop_name, tag_desc, default, format = "0x%08x", doc='', always_output=False):
    """
        tag_desc                 a pair containing the tag and its description
        default                  the tags default value when getting
        format                   printf style formatter for rending a text representation of the value
        always_output            when true then the element will not be optimised away when it == default.
    """
    def numeric_getter(obj):
        return obj._get_numeric_value(_make_tag_info(cls._tag_order, tag_desc, format), default)
    def numeric_setter(obj, value):
        obj._set_numeric_value(_make_tag_info(cls._tag_order, tag_desc, format), value, None if always_output else default)

    _add_class_property_tags(cls, prop_name, tag_desc[0])
    return _property(prop_name, cls._tag_order, tag_desc, numeric_getter, numeric_setter, doc=doc)
    
def _address_property(cls, prop_name, tag, getter, setter, doc=''):
    """
        tag_desc                 a pair containing the tag and its description
        getter
        setter
    """
    _add_class_property_tags(cls, prop_name, tag)
    cls._tag_order.append(tag, prop_name)
    return property(getter, setter, doc=doc)    
    
def _shift_property(cls, prop_name, getter, setter, tags, doc=''):
    _add_class_property_tags(cls, prop_name, tags)
    cls._tag_order.append(tags, prop_name)
    return property(getter, setter, doc=doc)        
    
def _expression_property(cls, prop_name, tag_desc, default, format = "%s", doc=''):
    """
        tag_desc                 a pair containing the tag and its description
        default                  the tags default value when getting
    """
    def expression_getter(obj):
        return obj._get_expression_value(_make_tag_info(cls._tag_order, tag_desc, format), default)
    def expression_setter(obj, value):
        obj._set_expression_value(_make_tag_info(cls._tag_order, tag_desc, format), value, default)
    
    _add_class_property_tags(cls, prop_name, tag_desc[0])
    return _property(prop_name, cls._tag_order, tag_desc, expression_getter, expression_setter, doc=doc)
    
bsp_objects = {}
bsp_classes = []

def bsp_object(cls):
    bsp_classes.append(cls)
    tags = cls.tag_name()
    if isinstance(tags, list):
        for tag in tags:
            bsp_objects[tag] = cls
            tag_can_be_pimpl[tag] = cls.can_be_pimpl()
    else:
        bsp_objects[tags] = cls
        tag_can_be_pimpl[tags] = cls.can_be_pimpl()
    return cls

def _spacer():
    if 'imgtec.codescape.hwdefs' in sys.modules:
        module = sys.modules['imgtec.codescape.hwdefs']
        if not hasattr(module, '_spacer_'):
            setattr(module, '_spacer_', '   ')
        return getattr(module, '_spacer_')
    return '   '

def _set_spacer(s):
    if 'imgtec.codescape.hwdefs' in sys.modules:
        module = sys.modules['imgtec.codescape.hwdefs']
        setattr(module, '_spacer_', s)

def _eol():
    if 'imgtec.codescape.hwdefs' in sys.modules:
        module = sys.modules['imgtec.codescape.hwdefs']
        if not hasattr(module, '_eol_'):
            setattr(module, '_eol_', '\n')
        return getattr(module, '_eol_')
    return '\n'

def _set_eol(s):
    if 'imgtec.codescape.hwdefs' in sys.modules:
        module = sys.modules['imgtec.codescape.hwdefs']
        setattr(module, '_eol_', s)

def _have_spacer():
    return (len(_spacer()) != 0) and (len(_eol()) != 0)

def _spacing(depth):
    eol = _eol()
    spacer = _spacer()
    return eol + spacer * depth

class BSPSpacerEOL(object):
    def __init__(self, where, new_spacer, new_eol):
        self.where = where
        self.prev_spacer = _spacer()
        self.prev_eol = _eol()
        _set_spacer(new_spacer)
        _set_eol(new_eol)
        
    def __enter__(self):
        return self
        
    def __exit__(self, *args):
        _set_spacer(self.prev_spacer)
        _set_eol(self.prev_eol)


_implementation_docs='''
   Intermediate class for objects with a description:
        ObjectWithDescription -> HDObject

    BitFieldValue -> ObjectWithDescription
    BitField -> ObjectWithDescription
    Module -> ObjectWithDescription
    MemoryType -> ObjectWithDescription
    Processor -> ObjectWithDescription
    
    Intermediate class for objects with a source:
        ObjectWithSource -> HDObject
    
    DAConfiguration -> ObjectWithSource
    ProcessorLink -> ObjectWithSource
    SoCLink -> ObjectWithSource
    CoreID -> ObjectWithSource

    Intermediate class for objects based in memory:
        MemoryObject -> ObjectWithDescription
    
    SharedMemory -> MemoryObject
    MemoryBlock -> MemoryObject
    Register -> MemoryObject      
    
    Setting -> HDObject
    Settings ->HDObject
    CoreInfo -> HDObject
    SoC -> HDObject
    Board -> HDObject
    Document -> HDObject
    
    All leaf classes populate their property list in a specific order so that their private
    class member "_tag_order" is filled with the tags appropriate in a that order reflecting
    the original DTD specification for Hardware Definition files.
    
    Any attempt to instantiate a naked HDObject result in "UnknownHDObject" exception being
    raised - see factory_tests.py
    
    All objects have a "name" property and all have a "name" setter with the exception of the
    Document class which will issue a warning if an attempt is made to change the name of a
    document.
    
    For all classes the order of attribute, method/property definition is as follows:
        pseudo private and public class attributes
        public class methods
        public instance methods/properties
        pseudo private class/instance methods and properties

    All classes have two attributes which should be treated as immutable:
    
    _must_have_props: a list of tuples (pairs) of (property name, default value)
                      property name: the string name or an object property
                      default value: an initial value to assign the property
    
    _must_have_classes: a list of tuples (pairs) of
                            ((list of classes), integer count)
                        list of classes: a list of classes comprising a
                                         mutually exclusive set of choices
                        integer count:  0: zero or one
                                        1: one or more
'''

class UnknownHDObject(Exception):
    """Raised when an attempt is made to create an unrecognised HDObject type."""

class HDObject(object):
    """Abstract Base Class for all Hardware Definition object types:
                                        
    All classes define some "tables" (class attributes) which form the basis of extracting and
    setting the properties associated with an object instance of a Hardware Definition class.
    
    All objects have a 'warnings' attribute through which warnings can be issued if there is a
    problem in the underlying DOM data when reading attributes or properties, or an attempt is
    made to alter the attributes or properties of an object that does not conform with the
    expected type of data associated with the attribute or property.
    
    Additionally, all objects have a 'filename' attribute which will be the name of the file if the
    :class:`Document` was created through loading (see :func:`load`) an XML file otherwise it will be
    None.
    This attribute is used for generating warning or error messages to give a location in the XML
    text when problems arise during parsing.
    
    The warnings object must have the following methods:
    
    report(node, message, edited)
    
    Report a new warning.
    
    :DOMnode node: the DOM node containing the source of the problem.
    
    :string message: the warning message.
    
    :boolean edited: a True/False flag indicating whether an alternative was found, replacing the original XML text.
    
    clear()
    
    Clear any warnings.
    
    Any attempt to create an object of this class only will result in an :class:`UnknownHDObject`
    exception being raised.
    """

    remove_inconsistent_tags = False
    
    _properties_are_condensed = False
    '''For some objects it makes more sense to format all properties on one line,
    rather than inserting whitespace and newlines.'''
    
    @classmethod
    def _has_value_tag(cls, tag):
        return tag in cls._tag_order
    
    @classmethod
    def allowable_children(cls):
        """ Returns a list of classes of valid children for this class.

        >>> [cls.__name__ for cls in Register.allowable_children()]
        ['BitField']
        """
        try:
            return flatten(cls._valid_children)
        except AttributeError:
            return []
    
    @classmethod
    def property_info(cls):
        """Returns a list of :class:`PropertyInfo` objects."""
        pass
        
    @classmethod
    def property_names(cls):
        """Returns a list of the names of the properties on this object."""
        return [p.name for p in cls.property_info()]
        
    @property
    def properties(self):
        """An OrderedDict(property name, value) for all properties on this object."""
        return OrderedDict([(p, getattr(self, p)) for p in self.property_names()])
        
    @properties.setter
    def properties(self, newprops):
        for key, val in newprops.items():
            setattr(self, key, val)

    @classmethod
    def has_editable_name(cls):
        return True
        
    @classmethod
    def class_name(cls):
        return cls.__name__
    
    @classmethod
    def short_tag(cls):    
        '''Returns the compressed form of the tag as used in the xml.
        
        >>> Register.short_tag()
        'r'
        '''
        if isinstance(cls.tag_name(), list):
            shortest_tag = cls.tag_name()[0]
            remaining_tags = cls.tag_name()[1:]
            for tag in remaining_tags:
                if len(tag) < len(shortest_tag):
                    shortest_tag = tag
            return shortest_tag
        return cls.tag_name()
    
    def __init__(self, doc, node, warnings, filename = None):
        if self.__class__ == HDObject:
            raise UnknownHDObject
        self.doc = doc
        self.node = node
        self.warnings = warnings
        self.filename = filename
        self._preferred_name_attr = None
        self._used_tag_name = None
        self._suppress_warnings = False
        if self.__class__ != UnhandledObject:
            child_element_tags = [child.tagName for child in self._childElements]
            if child_element_tags:
                self.__class__._tag_order.validate(self, child_element_tags)
                self._validate_consistent_attributes(child_element_tags)
        
    def __eq__(self, other):
        return  (self.__class__ == other.__class__) and (self._namenc() == other._namenc()) #and (self.depth == other.depth)
    __hash__ = None
    
    def msg_hdr(self):
        if self.node:
            if hasattr(self.node, 'line'):
                if self.filename:
                    filename = os.path.basename(self.filename)
                else:
                    filename = "Text"
                path = self.path
                if path:
                    return "%s(%d): %s" % (filename, self.node.line, self.path)
                return "%s(%d):" % (filename, self.node.line)
        return self.path
    
    @property
    def name(self):
        """The name of this object from the xml node for this object.

        When changing an object name if an object with this name already exists in the parent, then
        a warning is issued and an exception is raised.
            
        .. note:: For the :class:`Document` object the :attr:`name` is ``ioconfig`` and read-only.
        """        
        name_attr = ''
        node_name = ''
        name_attrs = self._name_attrs if isinstance(self._name_attrs, list) else [self._name_attrs]
        node_names = [(name_attr, self.node.getAttribute(name_attr)) for name_attr in name_attrs if bool(self.node.getAttribute(name_attr))]
        if bool(node_names):
            name_attr, node_name = node_names[0]
        try:
            self._check_name(node_name)
            if self._preferred_name_attr is None:
                if name_attr:
                    self._preferred_name_attr = name_attr
                else:
                    self._preferred_name_attr = self._name_attrs[0] if isinstance(self._name_attrs, list) else self._name_attrs
            return node_name
        except NameError as e:
            self.warnings.report(self.node, "%s: %s" % (self.msg_hdr(), e), None)
            return ''

    @name.setter
    def name(self, new_name):
        try:
            self._check_name(new_name)
            objs = self.parent.find(self.__class__, new_name) if self.parent else None
            if not objs or (objs == self):
                if self._preferred_name_attr is None:
                    self._preferred_name_attr = self._name_attrs[0] if isinstance(self._name_attrs, list) else self._name_attrs
                self.node.setAttribute(self._preferred_name_attr, new_name)
            else:
                raise NameError("already has a %s with the name '%s'" % (self.class_name(), new_name))
        except NameError as e:
            self.warnings.report(self.node, "%s: %s" % (self.msg_hdr(), e), None)
            raise
        
    @property
    def path(self):
        """Return a path, similar to an absolute file path, consisting of the names or class names
        of the objects from the root node down to this node.
        """        
        parts = []
        item = self
        while item and item.__class__ is not Document:
            parts.append(item._namenc())
            item = item.parent
        return '/'.join(reversed(parts))
                
    @property
    def parent(self):
        """A Hardware Definition object representing the XML node that is the parent of the XML node of this Hardware Definition object."""
        
        if self.node and self.node.parentNode:
            return factory(self.doc, self.node.parentNode, self.warnings)
        return None
    
    def iterchildren(self):
        """Iterate over the children of this object."""
        for elem in self._childElements:
            obj = factory(self.doc, elem, self.warnings, self.filename, suppress_warnings=self._suppress_warnings) 
            if obj and obj.__class__ != UnhandledObject:
                yield obj
                
    @property
    def children(self):
        """A list of Hardware Definition objects of child nodes of this object."""
        return list(self.iterchildren())
    
    def node_position_list(self):
        #"""Returns a tuple (pair) containing a deep clone of the node and an "index list".
        #
        #The "index list" is a list of indices showing the position in the DOM tree of the node
        #for this object.
        #The indices begin at the root and give the position of the parent in the hierarchy for
        #the node and finally the position of node.
        #"""        
        def node_index(node):
            if node.parentNode:
                index = 0
                childNode = node.parentNode.firstChild
                while childNode:
                    #if childNode.isSameNode(node):
                    if childNode == node:
                        return index
                    index += 1
                    childNode = childNode.nextSibling
            return -1
        
        parentNode = self.node.parentNode
        indices = [node_index(self.node)]
        while parentNode:
            indices.append(node_index(parentNode))
            parentNode = parentNode.parentNode
        indices.reverse()
        if indices[0] == -1:
            indices.pop(0)
        return self.node, indices
    
    @property
    def depth(self):
        """The depth of this node relative to the root (depth 0)."""        
        node_depth = 0
        if self.node and self.node.parentNode:
            node = self.node.parentNode
            while node:
                node_depth += 1
                node = node.parentNode
        return node_depth
    
    @property
    def distance(self):
        """Returns a tuple (pair) of zero based indices containing:
            
        1. the distance of this object from the first child of this object's parent,
        2. the distance of this object from the first one within a group of children of the same class as this object.
        """        
        par = self.parent
        if par:
            children = par.children
            abs_index = children.index(self)
            for cix, child in enumerate(children):
                if child.__class__ == self.__class__:
                    return abs_index, abs_index - cix
        return 0, 0
    
    def find_by_type(self, cls):
        """Returns a list of child objects with the same type as cls (a Hardware Definition object class)."""        
        return list(self.iterchildren_by_type(cls))
        
    def iterchildren_by_type(self, cls):
        """Returns a generator of child objects with the same type as cls (a Hardware Definition object class)."""
        allowable_children = self.allowable_children()
        if cls in allowable_children:
            tagNames = flatten(cls.tag_name())
            for node in self._childElements:
                if node.tagName in tagNames:
                    yield factory(self.doc, node, self.warnings)
    
    def find_by_name(self, name):
        """Returns a list of child objects whose name is equal to the argument name."""        
        return list(self.iterchildren_by_name(name))

    def iterchildren_by_name(self, name):
        """Returns a generator of child objects whose name is equal to the argument name."""
        for child in self.iterchildren():
            if child.name == name:
                yield child
        
    def find(self, cls, name):
        """Returns the child object whose type matches 'cls' and name matches 'name'."""        
        tagNames = flatten(cls.tag_name())
        for node in self._childElements:
            if node.tagName in tagNames:
                if get_name(node, cls._name_attrs) == name:
                    return factory(self.doc, node, self.warnings)
        return None
    
    def can_insert(self, cls):
        """Returns whether it is possible to insert an object of type 'cls'.
            
            1. 'cls' must be in this class' list of 'allowable_children'.
            2. if 'cls' belongs to a group of mutually exclusive classes then there must not
               already be an instance of 'cls' or and instance of the other alternatives of the
               group.
        """        
        if cls in self.allowable_children():
            for must_have in self._must_have_classes:
                must_have_child_classes_group, must_have_child_classes_count = must_have
                if cls in must_have_child_classes_group:
                    for must_have_cls in must_have_child_classes_group:
                        if (must_have_cls != cls) and self.find_by_type(must_have_cls):
                            return False
                    children_cls = self.find_by_type(cls)
                    only_one_allowed = not bool(must_have_child_classes_count)
                    if children_cls and only_one_allowed:
                        return False
            return True
        return False
    
    def create(self, cls, name=None, **kwargs):
        """Creates and inserts a new child object (see 'can_insert' above).
        
        `cls` is one of the derived classes of :class:`HDObject`, which must be 
        a suitable child class of this object.  
        
        `name` is an optional string which will be assigned to the newly created 
        object.  If not given then a default name will be constructed from the 
        object type, for example ``Register1``.
        
        Other properties suitable for the child object can also be given as 
        keyword parameters.  For example ::
        
            reg = module.create(Register, 'reg1', start_address=0x04800000)
            
        Returns: the newly inserted child object.
        """
        return self._create(cls, name, **kwargs)
    
    def insert(self, src):
        """Insert an existing child object (see 'can_insert' above). 
        
        The existing object is deep copied, i.e. all children and properties are
        copied.
        
        Returns: the newly inserted child object.
        """
        new = self.create(type(src), **src.properties)
        for child in src.children:
            new.insert(child)
        return new
        
    def _create(self, cls, name=None, **kwargs):
        if cls in self.allowable_children():
            insertable = self.can_insert(cls)
            if insertable:
                return self._create_child(cls, name, **kwargs)
            else:
                msg = "%s, can't insert it %s" % (self.class_name(), cls.__name__)
                self.warnings.report(self.node, "%s%s%s" % (self.msg_hdr(), (': ' if self.path else ' '), msg), None)
        else:
            msg = "%s does not support inserting a %s" % (self.class_name(), cls.__name__)
            self.warnings.report(self.node, "%s%s%s" % (self.msg_hdr(), (': ' if self.path else ' '), msg), None)
            return None
        
    def _where(self, cls):
        allowable_children = self.allowable_children()
        children = []
        clsidx = int(allowable_children.index(cls) + 1)
        while clsidx < len(allowable_children):
            children = self._get_elements_by_tag_name(allowable_children[clsidx].tag_name())
            if children:
                break
            clsidx += 1
        if children:
            return children[0]
        if isinstance(self, ObjectWithDescription):
            pos = self._get_elements_by_tag_name(ObjectWithDescription._desc_info[0][0])
            if pos:
                return pos[0]
        return None
        
    def _create_child(self, cls, name, **kwargs):
        elem = self.doc.createElement(cls.tag_name()[0] if isinstance(cls.tag_name(), list) else cls.tag_name())
        name_attr = cls._name_attrs[0] if isinstance(cls._name_attrs, list) else cls._name_attrs
        new_name = self._next_name(cls) if (name is None) or not isinstance(name, basestring) else name
        elem.setAttribute(name_attr, new_name)
        self._add_element(self._where(cls), elem)
        obj = factory(self.doc, elem, self.warnings)
        obj._preferred_name_attr = name_attr
        for attr, defaultvalue in cls._must_have_props:
            setattr(obj, attr, kwargs.pop(attr, defaultvalue))
        for attr, value in kwargs.items():
            setattr(obj, attr, value)
        return obj        
        
    def remove(self, index):
        """Remove the node at 'index' from the child node list."""
        child_index = 0
        childNode = self.node.firstChild
        while childNode:
            if childNode.nodeType == Node.ELEMENT_NODE:
                if factory(self.doc, childNode, self.warnings):
                    if child_index == index:
                        removedChildNode, childNodeIndices = childNode, [child_index,]
                        obj = factory(self.doc, childNode, self.warnings)
                        if obj:
                            removedChildNode, childNodeIndices = obj.node_position_list()
                        self._remove_elem(childNode)
                        return removedChildNode, childNodeIndices
                    child_index += 1
            childNode = childNode.nextSibling

    def toxml(self):
        """Returns the XML text of the Hardware Definition objects in the document."""
        return self.doc.toxml()
    
    def save(self, filename):
        """Saves the XML text to the given file 'filename'."""
        with open(filename, "wb") as f:
            f.write(self.toxml().encode('utf8'))

    @classmethod
    def _property_info_impl(cls, name_property_desc):
        return [PropertyInfo('Name', 'name', PropertyKind.text, name_property_desc if name_property_desc else "The name of the item.")]
        
    def _check_name(self, name):
        return matches_general_id(name)
    
    def _namenc(self):
        for name_attr in self._name_attrs:
            node_name = self.node.getAttribute(name_attr)
            if node_name:
                try:
                    return self._check_name(node_name)
                except NameError, e:
                    pass
        return self.class_name()
    
    @property
    def _childElements(self):
        return [x for x in self.node.childNodes if x.nodeType == Node.ELEMENT_NODE]
        
    def _next_name(self, cls):
        all_names = [obj.name for obj in self.children]
        index = 1
        while True:
            name = "%s%d" % (cls.__name__, index)
            if name not in all_names:
                return name
            index += 1
    
    def _get_enum_tag(self, tag_info, default):
        tagnames = set([n.tagName for n in self._childElements])
        enum_tags = tag_info[0]
        for tag, value in enum_tags.items():
            if tag in tagnames:
                return int(value)
        return default

    def _get_text_value(self, tag_info, default = ''):
        tag = tag_info[0]
        if tag:
            nodes = self._get_elements_by_tag_name(tag)
            if nodes and nodes[0].firstChild:
                #data = nodes[0].firstChild.data
                #if (tag == 'd') and bool(data) and (len(data.split('\n\r')) > 1):
                #    self.warnings.report(self.node, "%s: description is multi-line" % self.msg_hdr(), None)
                return nodes[0].firstChild.data
        elif self.node.firstChild:
            try:
                return self.node.firstChild.data
            except AttributeError as e:
                pass
        return default
    
    def _get_numeric_value(self, tag_info, default_value):
        tag, desc, _, format = tag_info
        return self._get_numeric_value_simple(tag, desc, default_value)
        
    def _get_numeric_value_simple(self, tag, desc, default_value):
        nodes = self._get_elements_by_tag_name(tag)
        if nodes:
            try:
                if nodes[0].firstChild:
                    return int(nodes[0].firstChild.data, 0)
            except (TypeError, ValueError):
                self.warnings.report(self.node, "%s: %s '%s' does not convert to an integer" % (self.msg_hdr(), desc, nodes[0].firstChild.data), None)
        return default_value    
        
    def _get_expression_value(self, tag_info, default_value):
        tag, desc, _, format = tag_info
        nodes = self._get_elements_by_tag_name(tag)
        if nodes:
            if nodes[0].firstChild:
                value = nodes[0].firstChild.data
                try:
                    if value.startswith("0x"):
                        int(value, 0)
                    elif not value.startswith("$"):
                        raise ValueError
                except (TypeError, ValueError):
                    self.warnings.report(self.node, "%s: %s '%s' Could not recognise as a valid register or literal address" % (self.msg_hdr(), desc, nodes[0].firstChild.data), None)    
                return value
        return default_value
    
    def _new_text_elem(self, tag, value):
        elem = self.doc.createElement(tag)
        text_elem = self.doc.createTextNode(value)
        elem.appendChild(text_elem)
        return elem

    def _set_node_value(self, node, value):
        if value is None or len(value) == 0:
            if node.firstChild:
                node.removeChild(node.firstChild)
        elif node.firstChild:
            node.firstChild.data = value
        else:
            node.appendChild(self.doc.createTextNode(value))
            
    def _get_elements_by_tag_name(self, tag_s):
        if isinstance(tag_s, list):
            elts = []
            for n in self._childElements:
                for tag in tag_s:
                    if n.tagName == tag:
                        elts.append(n)
            return elts
        else:
            return [n for n in self._childElements if n.tagName == tag_s]
        
    def __remove_elem(self, pos):
        if pos:
            if  pos.previousSibling \
            and (pos.previousSibling.nodeType == Node.TEXT_NODE) \
            and len(pos.previousSibling.data) \
            and (pos.previousSibling.data == _spacing(self.depth)):
                self.node.removeChild(pos.previousSibling)
            self.node.removeChild(pos)
            
    def _remove_elem(self, pos):
        if isinstance(pos, list):
            for p in pos:
                self.__remove_elem(p)
        else:
            self.__remove_elem(pos)
        
    def _remove_element_by_tag_name(self, tag):
        nodes = self._get_elements_by_tag_name(tag)
        if nodes:
            self._remove_elem(nodes)

    def _prev_elem_for_tag(self, tags, tag):
        prev_elems = []
        pruned_tags = tags.copy()
        for k, v in pruned_tags.items():
            nodes = self._get_elements_by_tag_name(v)
            if nodes:
                for e in nodes:
                    prev_elems.append(e)
        return prev_elems

    def _add_element(self, pos, elem):
        had_children = self.node.hasChildNodes()
        spacing = _spacing(self.depth)
        lspacing = len(spacing)
        if not had_children:
            assert pos is None
            if lspacing != 0 and not self._properties_are_condensed:
                self.node.insertBefore(self.doc.createTextNode(spacing), pos)
            self.node.insertBefore(elem, pos)
        elif lspacing != 0  and not self._properties_are_condensed:
            if pos is None:
                self.node.insertBefore(self.doc.createTextNode(spacing), self.node.lastChild)
                self.node.insertBefore(elem, self.node.lastChild)
            else:
                spos = self.node.insertBefore(elem, pos.previousSibling)
                self.node.insertBefore(self.doc.createTextNode(spacing), spos)
        else:
            self.node.insertBefore(elem, pos)
        if not had_children and _have_spacer() and not self._properties_are_condensed:
            self.node.appendChild(self.doc.createTextNode(_spacing(self.depth - 1)))
            
    def _add_element_from_tag_order(self, elem, tag_order):
        idx = tag_order.order_of(elem.tagName)
        pos = None
        for existing_node in self._childElements:
            try:
                existing_idx = tag_order.order_of(existing_node.tagName)
            except ValueError:
                existing_idx = 0
            if existing_idx > idx:
                pos = existing_node
                break
        self._add_element(pos, elem)

    """
        _set_...
        tag_info a tuple containing
            tag           xml tag associated with the value
            description   description to be used when constructing warning message
            tag_order     see _ctag_order
            format        formatting to be used for value when setting  
    """

    def _set_enum_tag(self, tag_info, value, default):
        def invert(d):
            return dict([v, k] for k, v in d.items())   
        enum_tags, ignore_desc, tag_order, ignore_format = tag_info
        enum_tags = invert(enum_tags)
        try:
            tag = enum_tags[value]
        except KeyError:
            assert False, "enum_tags=%s tag=%s" % (enum_tags, value)
        else:
            if tag:
                self._remove_elem(self._prev_elem_for_tag(enum_tags, value))
                if value != default:
                    self._add_element_from_tag_order(self.doc.createElement(tag), tag_order)
            else:
                assert len(enum_tags) == 2, "enum_tags=%s tag=%s" % (enum_tags, value)
                self._remove_elem(self._prev_elem_for_tag(enum_tags, value))
                    
    def _set_text_value(self, tag_info, value, default=None):
        tag, ignore_desc, tag_order, ignore_format = tag_info
        self._set_text_value_simple(tag, tag_order, value, default)
        
    def _set_text_value_simple(self, tag, tag_order, value, default=None):
        if tag:
            if value is not None and value != default: # because an empty string is Falsey
                nodes = self._get_elements_by_tag_name(tag)
                if nodes:
                    self._set_node_value(nodes[0], value)
                else:
                    self._add_element_from_tag_order(self._new_text_elem(tag, value), tag_order)
            else:
                self._remove_element_by_tag_name(tag)
        else:
            self._set_node_value(self.node, value)            
    
    def _set_numeric_value(self, tag_info, value, default=None):
        tag, ignore_desc, tag_order, format = tag_info
        if value is not None and value != default:
            self._set_text_value_simple(tag, tag_order, format % value)
        else:
            self._remove_element_by_tag_name(tag)

    def _set_expression_value(self, tag_info, value, default):
        tag, desc, tag_order, format = tag_info
        if value is not None and value != default:
            try:
                if value.startswith("0x"):
                    int(value, 0)
                elif not value.startswith("$"):
                    raise ValueError
            except (TypeError, ValueError):
                self.warnings.report(self.node, "%s: %s '%s' Could not recognise as a valid register or literal address" % (self.msg_hdr(), desc, value), None)    
            self._set_text_value(tag_info, value)                
        else:
            self._remove_element_by_tag_name(tag)

    def _convert_all_unsupported_tags(self):
        self._suppress_warnings = True
        children = self.children
        for child in children:
            child._convert_all_unsupported_tags()
        self._suppress_warnings = False
        
    def _validate_consistent_attributes(self, child_element_tags):
        pass
    
class UnhandledObject(HDObject):
    """ For tags that are not recognised but are retained in the DOM model of xml."""
    pass 

class ObjectWithDescription(HDObject):
    """Intermediate class for objects with a description."""
    _desc_str = "A description of the item which will appear in the Peripheral Region in Codescape Debugger."
    _desc_prop_info = PropertyInfo('Description', 'description', PropertyKind.text, _desc_str)
    _desc_info = ('d', False)
    
    @classmethod
    def _property_info_impl(cls, name_property_desc = None, extras = []):
        return HDObject._property_info_impl(name_property_desc) + extras + [ObjectWithDescription._desc_prop_info]

class ObjectWithSource(HDObject):
    """Intermediate class for objects with a source."""
    _source_str = "The path to a file for the xml configuration file for this object. This can be an absolute path, or a path relative to the main prconfig.xml file."
    _source_prop_info = PropertyInfo('Source', 'source', PropertyKind.path, _source_str)
    _source_info = ('src', False)
    
    @classmethod
    def property_info(cls):
        return HDObject._property_info_impl(None) + [ObjectWithSource._source_prop_info]

    def __str__(self):
        return "%s %s" % (self.__class__.__name__, self.source)
    
@bsp_object
class DAConfiguration(ObjectWithSource):
    """
    Defines a DA Configuration.
    """
    
    _name_attrs = ["N", "Name"]
    _tag_order = _ctag_order()
    _must_have_props = [('source', '')]
    _must_have_classes = []
    class_attributes_map = {}    
    
    @classmethod
    def tag_name(cls):
        return 'DAConfiguration'
    
    @classmethod
    def can_be_pimpl(cls):
        return False


_DAConfiguration_source_doc = "The path to an XML file describing the configuration."
DAConfiguration.source = _text_property(DAConfiguration, 'source', ObjectWithSource._source_info, '', doc=_DAConfiguration_source_doc)

@bsp_object
class SoCLink(ObjectWithSource):
    """
    Defines a SoC Link.
    """
    
    _name_attrs = ["N", "Name"]
    _tag_order = _ctag_order()
    _must_have_props = [('source', '')]
    _must_have_classes = []
    class_attributes_map = {}    
    
    @classmethod
    def tag_name(cls):
        return 'SoCLink'
        
    @classmethod
    def can_be_pimpl(cls):
        return False
    
    def _check_name(self, name):
        return allow_anything_apart_from_bad_slashed_regex(name)
    
_SoCLink_source_doc = "The path to an XML file describing the System on Chip."
SoCLink.source = _text_property(SoCLink, 'source', ObjectWithSource._source_info, '', doc=_SoCLink_source_doc)

@bsp_object
class CoreID(ObjectWithSource):
    """
    Defines a CoreID specification for automatic loading based on CoreID or PRId.
    
    If no board file has been specified for a probe then Codescape Debugger 
    searches the Hardware Definition search paths for files with the extension 
    .core_id, and compares the CoreID in each file against the Core ID or PRId
    for each core.  If the values match then the file indicated in :attr:`source`
    is used for the peripheral data on that core.

    Note that for MIPS Cores the core's CoreID is AND\'ed with ``0xffffff00``
    before comparing to :attr:`value`.

    """
    
    _name_attrs = ["N", "Name"]
    _cidv_tag = 'CoreIDValue'; _cidv_desc = 'Core ID Value'
    _tag_order = _ctag_order()
    _must_have_props = [('value', 0), ('source', '')]
    _must_have_classes = []
    class_attributes_map = {}    

    _cdiv_prop_info = PropertyInfo('Core ID Value', 'value', PropertyKind.hex, "The core ids.")
    _cidv_info = (_cidv_tag, False)
    
    @classmethod
    def tag_name(cls):
        return 'CoreID'
        
    @classmethod
    def can_be_pimpl(cls):
        return False
    
    @classmethod
    def property_info(cls):
        return HDObject._property_info_impl(None) + [CoreID._cdiv_prop_info, ObjectWithSource._source_prop_info]
    
    def __str__(self):
        return "CoreID 0x%04x %s" % (self.value, self.source)
    
    def _check_name(self, name):
        return allow_anything_apart_from_bad_slashed_regex(name)
    
    def _validate_consistent_attributes(self, child_element_tags):
        dont_care = self.value


_CoreID_value_doc = '''\
The value used to match against the core ID. The value should be in hexadecimal
and with a leading ``0x``.
'''
CoreID.value = _numeric_property(CoreID, 'value', CoreID._cidv_info, 0, "0x%08x", doc=_CoreID_value_doc)

_CoreID_source_doc = "The path to an XML file describing the peripheral registers for the given core."
CoreID.source = _text_property(CoreID, 'source', ObjectWithSource._source_info, '', doc=_CoreID_source_doc)

@bsp_object
class BitFieldValue(ObjectWithDescription):
    """
    Defines a Bit Field Value.
    
    BitField Values are like enumerated types for a bitfield in a register.
    
    After the mask and shift have been applied to the register value it is 
    compared against the :attr:`value` property of each the BitFieldValue in the 
    Bitfield.  Codescape Debugger will display the matching BitFieldValue name.
    """
    
    _name_attrs = ['N', 'Name']
    _bfv_tag = 'x'; _bfv_desc = 'Bit Field Value'
    _tag_order = _ctag_order()
    _must_have_props = []
    _must_have_classes = []
    class_attributes_map = {}    

    @classmethod
    def tag_name(cls):
        return 'v'
    
    @classmethod
    def can_be_pimpl(cls):
        return True
    
    @classmethod
    def property_info(cls):
        return ObjectWithDescription._property_info_impl(None, [PropertyInfo('Value', 'value', PropertyKind.hex64, "A hex value whose width in bits is not greater than the number of bits in the BitField mask to which this value belongs.")]) 
    
    def __str__(self):
        return "BitFieldValue"
    
    def _check_name(self, name):
        return matches_cidentifier(name)
    
    def _validate_consistent_attributes(self, child_element_tags):
        dont_care = self.name
        dont_care = self.value

_BitFieldValue_value_doc = "A hex value whose width in bits is not greater than the number of bits in the BitField mask to which this value belongs."
BitFieldValue.value = _numeric_property(BitFieldValue, 'value', ((BitFieldValue._bfv_tag, False), BitFieldValue._bfv_desc), 0,"0x%016x", doc=_BitFieldValue_value_doc)
BitFieldValue.description = _text_property(BitFieldValue, 'description', ObjectWithDescription._desc_info, '', doc=ObjectWithDescription._desc_str)

@bsp_object
class BitField(ObjectWithDescription):
    """
    Defines a Bit Field within a :class:`Register`.
    
    An AND mask and shift is applied to extract the relevant bits.
    
    BitField objects can contain :class:`BitFieldValue` objects.
    """
    
    _name_attrs = ['N', 'Name']
    _default_tag = 'dv';    _default_desc = 'Default'
    _mask_tag = 'fm';       _mask_desc = 'A mask to be AND\'ed with the value of the :class:`Register` that owns this bit field.'
    _ls_tag = 'ls';         _ls_desc = 'Left Shift'    
    _rs_tag = 'rs';         _rs_desc = 'Right Shift'
    _tag_order = _ctag_order() 
    _valid_children = [BitFieldValue]
    _must_have_props = []
    _must_have_classes = []
    class_attributes_map = {}    
    _name_property_desc = "The name of the Bitfield that is displayed in the Peripheral Region in Codescape."

    @classmethod
    def tag_name(cls):
        return 'f'
    
    @classmethod
    def can_be_pimpl(cls):
        return False
    
    @classmethod
    def property_info(cls):
        return ObjectWithDescription._property_info_impl(BitField._name_property_desc, \
                                                   [PropertyInfo('Default', 'default', PropertyKind.hex, "Default bit field value in hex."), \
                                                    PropertyInfo('AND Mask', 'mask', PropertyKind.hex, "Mask used to extract the required bits of the field."), \
                                                    PropertyInfo('Shift', 'shift', PropertyKind.dec, "The shift to be applied to the bits after masking. Positive for a left shift, negative for a right shift."), \
                                                    PropertyInfo('Radix', 'radix', PropertyKind.enum, _radix_description)])

    def __str__(self):
        return "BitField"
    
    def _check_name(self, name):
        return matches_cidentifier(name)

    def _get_shift(self):
        current_shift = self._get_numeric_value_simple(BitField._rs_tag, BitField._rs_desc, None)
        if not current_shift:
            current_shift = self._get_numeric_value_simple(BitField._ls_tag, BitField._ls_desc, None)
            if current_shift:
                current_shift = -current_shift
            else:
                current_shift = 0
        return current_shift
    
    def _set_shift(self, value):
        if isinstance(value, basestring):
            if value.lower() == 'none':
                value = 0
            else:
                m = re.match(r'(l(?:eft)?|r(?:ight)?)?\s*(-?\d+)$', value, flags=re.I)
                if not m:
                    raise ValueError("%s: badly formed shift expression: %s" % (self.msg_hdr(), value))
                value = int(m.group(2), 0)
                if m.group(1) and m.group(1).lower().startswith('l'):
                    value = -value
        self._remove_element_by_tag_name(BitField._ls_tag)
        self._remove_element_by_tag_name(BitField._rs_tag)
        if value < 0:
            self._set_text_value_simple(BitField._ls_tag, BitField._tag_order, "%d" % -value)
        else:
            self._set_text_value_simple(BitField._rs_tag, BitField._tag_order, "%d" % value)
        
    def _validate_consistent_attributes(self, child_element_tags):
        dont_care = self.name
        dont_care = self.mask
        dont_care = self.shift
        dont_care = self.radix

_BitField_default_doc = 'The value to displayed if none of the values match the bitfield values after the mask and shift have been applied.'
BitField.default = _numeric_property(BitField, 'default', ((BitField._default_tag, None), BitField._default_desc), 0, doc=_BitField_default_doc)

_BitField_mask_doc = 'A mask (default zero) to be AND\'ed with the register value.'
BitField.mask = _numeric_property(BitField, 'mask', ((BitField._mask_tag, False), BitField._mask_desc), 0, doc=_BitField_mask_doc)

_BitField_shift_doc = 'The right shift (default zero) to be applied after AND\'ing the register value with the mask.'
BitField.shift = _shift_property(BitField, 'shift', BitField._get_shift, BitField._set_shift, [BitField._rs_tag, BitField._ls_tag], doc=_BitField_shift_doc)

_BitField_radix_doc = _radix_description
BitField.radix = _enum_property(BitField, 'radix', (_radix_mappings, "Radix"), Radix.hex, doc=_BitField_radix_doc)
BitField._children_ = children_property(BitField._tag_order, BitField._valid_children)
BitField.description = _text_property(BitField, 'description', ObjectWithDescription._desc_info, '', doc=ObjectWithDescription._desc_str)

class MemoryObject(ObjectWithDescription):
    _sa_doc = "The start address this %s in hex.\n\nThis must align to the element size of %s."
    _sa_tag = 's'
    _sa_info = PropertyInfo('Start Address', 'start_address', PropertyKind.hex, "The start address in the memory area of this block in hex which must align on a boundary according to the size of an addressable element in this memory block.")
    
    @property
    def byte_size(self):
        byte_size = 4
        try:
            byte_size = SizeBytes[self.size]
        except AttributeError, e:
            parent = self.parent
            if parent:
                try:
                    byte_size = SizeBytes[parent.size]
                except AttributeError, e:
                    pass
        return byte_size

    def _get_start_address(self):
        saddr = self._get_numeric_value(_make_tag_info(self._tag_order, (self._sa_tag, self._sa_info[0]), "0x%08x"), 0)
        if saddr % self.byte_size != 0:
            self.warnings.report(self.node, "%s: start address 0x%08x does not align on a %d byte boundary" % (self.msg_hdr(), saddr, self.byte_size), None)
        return saddr
    
    def _set_start_address(self, value):
        if value % self.byte_size != 0:
            self.warnings.report(self.node, "%s: start address 0x%08x does not align on a %d byte boundary" % (self.msg_hdr(), value, self.byte_size), None)
        self._set_numeric_value(_make_tag_info(self._tag_order, (self._sa_tag, self._sa_info[0]), "0x%08x"), value)
       
@bsp_object
class SharedMemory(MemoryObject):
    """
    Defines an area of shared memory.
    """    

    _name_attrs = 'N'
    _tag_order = _ctag_order()
    _must_have_props = [('start_address', 0)]
    _must_have_classes = []
    class_attributes_map = {}    

    @classmethod
    def tag_name(cls):
        return 'shared'
    
    @classmethod
    def can_be_pimpl(cls):
        return False
    
    @classmethod
    def property_info(cls):
        return ObjectWithDescription._property_info_impl(None, [MemoryObject._sa_info])
    
    def __str__(self):
        return "SharedMemory start=%08x" % self.start_address

    def _validate_consistent_attributes(self, child_element_tags):
        dont_care = self.name
        dont_care = self.start_address
        
_SharedMemory_start_address_doc = MemoryObject._sa_doc % ('shared area', 'the memory block to which this shared area belongs')
SharedMemory.start_address = _address_property(SharedMemory, 'start_address', MemoryObject._sa_tag, MemoryObject._get_start_address, MemoryObject._set_start_address, doc=_SharedMemory_start_address_doc)
SharedMemory.description = _text_property(SharedMemory, 'description', ObjectWithDescription._desc_info, '', doc=ObjectWithDescription._desc_str)
   

@bsp_object
class MemoryBlock(MemoryObject):
    """
    Defines a block of memory.
   
    MemoryBlock objects can contain :class:`SharedMemory` objects.
    """
 
    _properties_are_condensed = True
    _name_attrs = 'N'
    _ea_tag = 'en'
    _ea_info = (('en', False), 'End Address')
    _tag_order = _ctag_order()
    _valid_children = [SharedMemory]
    _must_have_props = [('start_address', 0), ('end_address', 0xffffffff)]
    _must_have_classes = []
    _cacheable_desc = "Indicates if the debugger (Codescape or DAScript) can cache this memory block." \
                      " In the XML text 'cacheable' should be present for memory which can be cached by the debugger, e.g. general RAM areas, and not areas describing registers or ports."
    class_attributes_map = {}    
    
    @classmethod
    def tag_name(cls):
        return 'mb'
    
    @classmethod
    def can_be_pimpl(cls):
        return False
    
    @classmethod
    def property_info(cls):
        return ObjectWithDescription._property_info_impl(None, [MemoryObject._sa_info, \
                PropertyInfo('End Address', 'end_address', PropertyKind.hex, "The end address within the memory area of this block in hex such that the end address + 1 aligns on a boundary according to the size of an addressable element in this memory block."), \
                PropertyInfo('Element Size', 'size', PropertyKind.enum, "The size in bytes of a individual memory element."), \
                PropertyInfo('Access', 'access', PropertyKind.enum, "Describes how the memory item can be accessed."), \
                PropertyInfo('Cacheable', 'cacheable', PropertyKind.enum, MemoryBlock._cacheable_desc)])

    def __str__(self):
        return "MemoryBlock start=%08x end=%08x size=%d" % (self.start_address, self.end_address, int(self.size))
    
    def _check_name(self, name):
        return matches_general_id(name)

    def _get_end_address(self):
        eaddr = self._get_numeric_value(_make_tag_info(self._tag_order, self._ea_info, "0x%08x"), 0xffffffff)
        bs = self.byte_size
        if (eaddr + 1) % bs != 0:
            self.warnings.report(self.node, "%s: end address(0x%08x) + 1 does not align on a %d byte boundary" % (self.msg_hdr(), eaddr, bs), None)
        return eaddr
    
    def _set_end_address(self, value):
        bs = self.byte_size
        if (value + 1) % bs != 0:
            self.warnings.report(self.node, "%s: end address(0x%08x) + 1 does not align on a %d byte boundary" % (self.msg_hdr(), value, bs), None)
        self._set_numeric_value(_make_tag_info(self._tag_order, self._ea_info, "0x%08x"), value)
    
    def _validate_consistent_attributes(self, child_element_tags):
        dont_care = self.name
        dont_care = self.start_address
        dont_care = self.end_address
        dont_care = self.size
        dont_care = self.access
        dont_care = self.cacheable
            
_MemoryBlock_start_address_doc = MemoryObject._sa_doc % ('memory block', 'this memory block')
MemoryBlock.start_address = _address_property(MemoryBlock, 'start_address', MemoryObject._sa_tag, MemoryObject._get_start_address, MemoryObject._set_start_address, doc=_MemoryBlock_start_address_doc)

_MemoryBlock_end_address_doc = "The end address within the memory area of this block in hex. (end address + 1) must align to the element size of this memory block."
MemoryBlock.end_address = _address_property(MemoryBlock, 'end_address', MemoryBlock._ea_tag, MemoryBlock._get_end_address, MemoryBlock._set_end_address, doc=_MemoryBlock_end_address_doc)

_MemoryBlock_size_doc ="The size in bytes of a individual memory element described by one of the values in the enumeration Size."
MemoryBlock.size = _enum_property(MemoryBlock, 'size', (_size_mappings, "Size"), Size.uint32, doc=_MemoryBlock_size_doc)

_MemoryBlockr_access_doc = "Describes how the memory can be accessed by one of the values in the enumeration Access."
MemoryBlock.access = _enum_property(MemoryBlock, 'access', (_memory_access_mappings, "Access"), Access.read_write, doc=_MemoryBlockr_access_doc)

_MemoryBlock_cacheable_doc = MemoryBlock._cacheable_desc
MemoryBlock.cacheable = _enum_property(MemoryBlock, 'cacheable', (_cacheable_mappings, "Cacheable"), Cacheable.no, doc=_MemoryBlock_cacheable_doc)

MemoryBlock._children_ = children_property(MemoryBlock._tag_order, MemoryBlock._valid_children)
MemoryBlock.description = _text_property(MemoryBlock, 'description', ObjectWithDescription._desc_info, '', doc=ObjectWithDescription._desc_str)
        
@bsp_object
class MemoryType(ObjectWithDescription):
    """
    Defines a class of memory storage.

    The Memory Types are used to identify the Codescape memory types that should be used for memory
    spaces in a processor. There may be a single memory space for code, data, and memory mapped
    registers, or on some platforms separate memory spaces. For example, the Ensigma RPU has
    separate memory spaces for code, data and memory mapped registers, whilst MIPS cores use a
    single address space. 
    
    The value of a Memory Type is an internal constant used between the debugger and the probe to
    identify the memory space, so users do not normally need to change these settings.  The Memory
    Type value of 0, usually with the Memory Type name of "Ram" is appropriate for normally
    addressable memory.
    
    A Memory Type may be implicitly dynamic, meaning that Codescape knows the size and accessibility
    of address ranges within the address space; or it may be explicitly static using the <static/>
    tag, which means that the memory type element should contain Memory Block elements describing
    those address ranges that are readable, writable and cacheable by the debugger.
    
    A Memory Block may also configure the access size using the <sb/>, <sw/>, <sd/>, or <sq/> tags
    (for 8-, 16-, 32-, and 64-bit access sizes respectively), but in practice the probe ignores
    these accesses and performs the best access size for the comms and target type.  In general the
    <sd/> should be used.
    """
    
    _name_attrs = 'N'
    _mtv_tag = 'mtv'
    _tag_order = _ctag_order()
    _valid_children = [MemoryBlock]
    _must_have_props = [('memory_type', 0)]
    _must_have_classes = []
    class_attributes_map = {}
    _name_property_desc = "The name of the Memory Type. This is used in Registers to identify the Memory Type for the Register."

    @classmethod
    def tag_name(cls):
        return 'mt'
    
    @classmethod
    def can_be_pimpl(cls):
        return False
    
    @classmethod
    def property_info(cls):
        return ObjectWithDescription._property_info_impl(MemoryType._name_property_desc, \
                                                        [PropertyInfo('Memory Type Value', 'memory_type', PropertyKind.hex, "A hex number read by Codescape to identify the Memory Type. This value should not be altered without consultation with Codescape Technical Support"), \
                                                         PropertyInfo('Memory Settings', 'setting', PropertyKind.enum, "Specifies whether the memory is static or dynamic.")])
    
    def __str__(self):
        return "MemoryType"
    
    def _validate_consistent_attributes(self, child_element_tags):
        dont_care = self.name
        dont_care = self.memory_type
        dont_care = self.setting
        
MemoryType.memory_type = _numeric_property(MemoryType, 'memory_type', ((MemoryType._mtv_tag, False), 'Memory Type Value'), 0, "0x%02x", always_output=True)
MemoryType.setting = _enum_property(MemoryType, 'setting', (_setting_mappings, "Memory Settings"), True)
MemoryType._children_ = children_property(MemoryType._tag_order, MemoryType._valid_children)
MemoryType.description = _text_property(MemoryType, 'description', ObjectWithDescription._desc_info, '', doc=ObjectWithDescription._desc_str)

@bsp_object
class ProcessorLink(ObjectWithSource):
    """
    Defines a Processor Link.
    """
    
    _name_attrs = ["N", "Name"]
    _tag_order = _ctag_order()
    _valid_children = []
    _must_have_props = [('source', '')]
    _must_have_classes = []
    class_attributes_map = {}    
    
    @classmethod
    def tag_name(cls):
        return ['pl', 'ProcessorLink']
        
    @classmethod
    def can_be_pimpl(cls):
        return False
    
    def _check_name(self, name):
        return allow_anything_apart_from_bad_slashed_regex(name)
    
_ProcessorLink_source_doc = "The path to an XML file describing the processor."
ProcessorLink.source = _text_property(ProcessorLink, 'source', ObjectWithSource._source_info, '', doc=_ProcessorLink_source_doc)
ProcessorLink._children_ = children_property(ProcessorLink._tag_order, ProcessorLink._valid_children)

@bsp_object
class Register(MemoryObject):
    """
    Defines a processor, co-processor or memory mapped register.
   
    Register objects can contain :class:`BitField` objects.
    """
 
    _name_attrs = ['N', 'Name']
    _mtn_tag = 'mtn';   _mtn_info = ((_mtn_tag, False), 'Memory Type')
    _rm_tag = 'rm';     _rm_info = ((_rm_tag, False), 'Read Mask')
    _wam_tag = 'wam';   _wam_info = ((_wam_tag, False), 'Write AND Mask')
    _wom_tag = 'wom';   _wom_info = ((_wom_tag, False), 'Write OR Mask')
    
    _tag_order = _ctag_order()
    _valid_children = [BitField]
    _must_have_props = []
    _must_have_classes = []
    class_attributes_map = {}    
    _name_property_desc = "The name of the register that is displayed in the Peripheral Region in Codescape."
    
    @classmethod
    def tag_name(cls):
        return 'r'
    
    @classmethod
    def can_be_pimpl(cls):
        return True
    
    @classmethod    
    def property_info(cls):
        return ObjectWithDescription._property_info_impl(Register._name_property_desc, \
                                                   [PropertyInfo('Memory Type', 'memory_type', PropertyKind.text,"The memory type (class) to which this register belongs."), \
                                                    PropertyInfo('Start Address', 'start_address', PropertyKind.expr, "The start address within the memory type of this register."), \
                                                    PropertyInfo('Size', 'size',PropertyKind.enum, "The size of the register."), \
                                                    PropertyInfo('Access', 'access', PropertyKind.enum, "Describes how the register can be accessed."), \
                                                    PropertyInfo('Read AND Mask', 'read_mask', PropertyKind.hex, "Specifies a mask in hex to bitwise AND against the register value before the value is displayed. (Default: 0xFFFFFFFF) "), \
                                                    PropertyInfo('Write AND Mask', 'write_and_mask', PropertyKind.hex, "Specifies a mask in hex to bitwise AND against the register value before the value is written. (Default: 0xFFFFFFFF) "), \
                                                    PropertyInfo('Write OR Mask', 'write_or_mask', PropertyKind.hex, "Specifies a mask in hex to bitwise OR against the register value before the value is written. (Default: 0) "), \
                                                    PropertyInfo('Radix', 'radix', PropertyKind.enum, _radix_description)])
    
    
    def __str__(self):
        return "Register start=%s size=%d radix=%s" % (self.start_address, SizeBytes[self.size], str(self.radix))
    
    def _check_name(self, name):
        return matches_cidentifier(name)
    
    def _validate_tag_info(self, child_element_tags, tag_info, format, inconsistent_tags):
        tag, desc = tag_info
        if child_element_tags.count(tag):
            inconsistent_tags.append(tag)
            self.warnings.report(self, format % (self.msg_hdr(), desc), self.remove_inconsistent_tags)
            return True
        return False

    def _validate_consistent_attributes(self, child_element_tags):
        dont_care = self.name
        dont_care = self.memory_type
        dont_care = self.start_address
        dont_care = self.size
        dont_care = self.radix
        access = self.access
        inconsistent_tags = []
        if (access == Access.read_only) or (access == Access.read_once):
            format = "%s: one or more \"%s\" found in read only or read once Register"
            if self._validate_tag_info(child_element_tags, self._wam_info, format, inconsistent_tags):
                inconsistent_tags.extend(['ro', 'roc'])
            if self._validate_tag_info(child_element_tags, self._wom_info, format, inconsistent_tags):
                inconsistent_tags.extend(['ro', 'roc'])
                
        elif (access == Access.write_only) or (access == Access.write_once):
            if self._validate_tag_info(child_element_tags, self._rm_info, "%s: one or more \"%s\" found in write only or write once Register", inconsistent_tags):
                inconsistent_tags.extend(['wo', 'woc'])
        
        if bool(inconsistent_tags) and self.remove_inconsistent_tags:
            inconsistent_tags = unique(inconsistent_tags)
            for tag in inconsistent_tags:
                self._remove_element_by_tag_name(tag)

_Register_memory_type_doc = "This is the 'memory_type' value of a MemoryType object."
Register.memory_type = _text_property(Register, 'memory_type', Register._mtn_info, '', doc=_Register_memory_type_doc)

_Register_start_address_doc = "The address of the register in the memory area in which it is defined.\n\nThis can be a hexadecimal address or an expression such as $cp0.1."
Register.start_address = _expression_property(Register, 'start_address', ((MemoryObject._sa_tag, False), MemoryObject._sa_info[0]), "0x0", doc=_Register_start_address_doc)        

_Register_size_doc = "The size of the register described by one of the values in the enumeration Size."
Register.size = _enum_property(Register, 'size', (_size_mappings, "Size"), Size.uint32, doc=_Register_size_doc)

_Register_access_doc = "Describes how the register can be accessed by one of the values in the enumeration Access."
Register.access = _enum_property(Register, 'access', (_access_mappings, "Access"), Access.read_write, doc=_Register_access_doc)

_Register_read_mask_doc = "Specifies a mask in hex to bitwise AND against the register value before the value is displayed."
Register.read_mask = _numeric_property(Register, 'read_mask', Register._rm_info, 0xffffffffffffffff, doc=_Register_read_mask_doc)

_Register_write_and_mask_doc = "Specifies a mask in hex to bitwise AND against the register value before the value is written."
Register.write_and_mask = _numeric_property(Register, 'write_and_mask', Register._wam_info, 0xffffffffffffffff, doc=_Register_write_and_mask_doc)

_Register_write_or_mask_doc = "Specifies a mask in hex to bitwise OR against the register value before the value is written."
Register.write_or_mask = _numeric_property(Register, 'write_or_mask', Register._wom_info, 0, doc=_Register_write_or_mask_doc)

_Register_radix_doc = "Specifies the format of the item described by one of the values in the enumeration Radix."
Register.radix = _enum_property(Register, 'radix', (_radix_mappings, "Radix"), Radix.hex, doc=_Register_radix_doc)

Register._children_ = children_property(Register._tag_order, Register._valid_children)
Register.description = _text_property(Register, 'description', ObjectWithDescription._desc_info, '', doc=ObjectWithDescription._desc_str)
    
@bsp_object
class Module(ObjectWithDescription):
    """
    Defines a Module.

    A Module is used for associating information about one or more devices, for example, a Bus State
    Controller (BSC).
    
    Module objects can contain :class:`Register` and :class:`Module` objects.
    """
    
    _name_attrs = ['N', 'Name']
    _tag_order = _ctag_order()
    _valid_children = [Register]
    _must_have_props = []
    _must_have_classes = []
    class_attributes_map = {}
    _name_property_desc = "The name of the Module that is displayed in the Peripheral Region in Codescape."
            
    @classmethod
    def tag_name(cls):
        return ['m', 'Module']
    
    @classmethod
    def property_info(cls):
        return HDObject._property_info_impl(Module._name_property_desc)
        
    @classmethod
    def can_be_pimpl(cls):
        return True
    
    def __str__(self):
        return "Module"

    def _check_name(self, name):
        return matches_cidentifier(name)
    
Module._valid_children.insert(0, Module)
Module._children_ = children_property(Module._tag_order, Module._valid_children)
Module.description = _text_property(Module, 'description', ObjectWithDescription._desc_info, '', doc=ObjectWithDescription._desc_str)
   
@bsp_object
class Setting(HDObject):
    """
    Defines a single Setting.
    
    These are single-value string items not directly related to the physical configuration of targets.
    """
    
    _name_attrs = 'N'
    _value_info = (None, ('value', 'Value'))
    _tag_order = _ctag_order()
    _must_have_props = []
    _must_have_classes = []
    class_attributes_map = {}    

    @classmethod
    def tag_name(cls):
        return 'setting'

    @classmethod
    def can_be_pimpl(cls):
        return True
    
    @classmethod
    def property_info(cls):
        return HDObject._property_info_impl(None) + [PropertyInfo('Value', 'value', PropertyKind.text, "The value of this setting.")]

    def __str__(self):
        return "Setting %s" % self.value
    
    def _validate_consistent_attributes(self, child_element_tags):
        dont_care = self.name
        dont_care = self.value
        
_Setting_value_doc = 'The value of the setting.'
Setting.value = _text_property(Setting, 'value', Setting._value_info, '', doc=_Setting_value_doc)

@bsp_object
class Settings(HDObject):
    """
    Defines a collection of Setting or Settings objects.
    """
    
    _name_attrs = 'N'
    _tag_order = _ctag_order()
    _valid_children = [Setting]
    _must_have_props = []
    _must_have_classes = []
    class_attributes_map = {}

    @classmethod
    def tag_name(cls):
        return 'settings'
    
    @classmethod
    def property_info(cls):
        return HDObject._property_info_impl(None)
    
    @classmethod
    def can_be_pimpl(cls):
        return True
    
    def __str__(self):
        return "Settings"
        
    def _check_name(self, name):
        return optional_matches_identifier(name)
    
Settings._valid_children.append(Settings)
Settings._children_ = children_property(Settings._tag_order, Settings._valid_children)
    
@bsp_object
class Processor(ObjectWithDescription):
    """
    Defines a Processor.
    
    Processor objects can contain :class:`MemoryType`, :class:`Module` and :class:`Settings` objects.
    """
    
    _name_attrs = ['N', 'Name']
    _tag_order = _ctag_order()
    _valid_children = [[MemoryType, Module], Settings]
    _must_have_props = []
    _must_have_classes = []
    class_attributes_map = {}    
    _name_property_desc = "The name of the processor that is displayed in the Peripheral Region in Codescape. This must match the name of the processor as displayed in Codescape."
    
    @classmethod
    def tag_name(cls):
        return ['p', 'Processor']
    
    @classmethod
    def property_info(cls):
        return ObjectWithDescription._property_info_impl(Processor._name_property_desc)

    @classmethod
    def can_be_pimpl(cls):
        return True
       
    def __str__(self):
        return "Processor"
        
    def _check_name(self, name):
        return allow_anything_apart_from_bad_slashed_regex(name)
    
Processor._children_ = children_property(Processor._tag_order, Processor._valid_children)
Processor.description = _text_property(Processor, 'description', ObjectWithDescription._desc_info, '', doc=ObjectWithDescription._desc_str)
    
@bsp_object
class CoreInfo(HDObject):
    """
    Defines a Core.
    
    CoreInfo objects can contain :class:`DAConfiguration`, :class:`Processor`, :class:`ProcessorLink`,
    :class:`MemoryType`, :class:`Settings` and :class:`Setting` objects.
    
    There can be at most one :class:`DAConfiguration` and either one of :class:`Processor` or :class:`ProcessorLink`
    but not both.
    """
    
    _name_attrs = ["N", "Name"]
    _tag_order = _ctag_order()
    _valid_children = [DAConfiguration, Processor, ProcessorLink, MemoryType, Settings, Setting]
    _must_have_props = []
    _must_have_classes = [((Processor, ProcessorLink), 0), ((DAConfiguration,), 0)]
    class_attributes_map = {}    
    
    @classmethod
    def tag_name(cls):
        return 'CoreInfo'
    
    @classmethod
    def property_info(cls):
        return HDObject._property_info_impl(None)
    
    @classmethod
    def can_be_pimpl(cls):
        return True
    
    def _check_name(self, name):
        return allow_anything_apart_from_bad_slashed_regex(name)

    def __str__(self):
        return "CoreInfo"

    _children_ = children_property(_tag_order, _valid_children)
            
class _SoCStrs:
    _jtagpos_tag = 'JTagPosition';  _jtagpos_desc = 'Position of this item on the JTAG scan chain.';        _jtagpos_ldesc = _jtagpos_desc
    _irlen_tag = 'IRLength';        _irlen_desc = 'The length of the TAP Instruction Register in bits.';    _irlen_ldesc = _irlen_desc
    _jtagid_tag = 'JtagID';         _jtagid_desc = 'JTAG ID in hexadecimal.';                               _jtagid_ldesc = _jtagid_desc
    _jtattn_tag = 'J_IMG_ATTEN';    _jtattn_desc = 'JTAG Attention Instruction in hexadecimal.';            _jtattn_ldesc = _jtattn_desc
    _jtstatus_tag = 'J_IMG_STATUS'; _jtstatus_desc = 'JTAG Status Instruction in hexadecimal.';             _jtstatus_ldesc = _jtstatus_desc
    _jtctrl_tag = 'J_IMG_CONTROL';  _jtctrl_desc = 'JTAG Control Instruction in hexadecimal.';              _jtctrl_ldesc = _jtctrl_desc
    _taptype_tag = 'TapType';       _taptype_desc = 'Tap Type in hexadecimal.';                             _taptype_ldesc = _taptype_desc

@bsp_object
class SoC(HDObject):
    """
    Defines a System on Chip.
    
    All the properties except Name are relevant to META processors only.
    
    SoC objects can contain :class:`CoreInfo`, :class:`Setting` and :class:`Settings` objects.
    
    There must be at least one :class:`CoreInfo` object.
    """
    
    _name_attrs = ["N", "Name"]
    _tag_name = 'SoC'
    _tag_order = _ctag_order()
    _valid_children = [CoreInfo, Settings, Setting]
    #_must_have = [('jtagpos', 0), ('irlength', 0), ('jtagid', 0), ('jtag_attn', 0), ('tap_type', 0), (CoreInfo, None)]
    _must_have_props = []
    _must_have_classes = [((CoreInfo,), 1)]
    class_attributes_map = {}    
        
    def _check_name(self, name):
        return allow_anything_apart_from_bad_slashed_regex(name)

    @classmethod
    def tag_name(cls):
        return 'SoC'
    
    @classmethod
    def can_be_pimpl(cls):
        return False
    
    @classmethod
    def property_info(cls):
        return HDObject._property_info_impl(None) + [PropertyInfo(_SoCStrs._jtagpos_desc, 'jtagpos', PropertyKind.dec, _SoCStrs._jtagpos_ldesc), \
                                                      PropertyInfo(_SoCStrs._irlen_desc, 'irlength', PropertyKind.dec, _SoCStrs._irlen_ldesc), \
                                                      PropertyInfo(_SoCStrs._jtagid_desc, 'jtagid', PropertyKind.dec, _SoCStrs._jtagid_ldesc), \
                                                      PropertyInfo(_SoCStrs._jtattn_desc, 'jtag_attn', PropertyKind.dec, _SoCStrs._jtattn_ldesc), \
                                                      PropertyInfo(_SoCStrs._taptype_desc, 'tap_type', PropertyKind.dec, _SoCStrs._taptype_ldesc), \
                                                      PropertyInfo(_SoCStrs._jtstatus_desc, 'jtag_status', PropertyKind.dec, _SoCStrs._jtstatus_ldesc), \
                                                      PropertyInfo(_SoCStrs._jtctrl_desc, 'jtag_ctrl', PropertyKind.dec, _SoCStrs._jtctrl_ldesc)]
        
    def __str__(self):
        return "SoC"
    
    def _validate_consistent_attributes(self, child_element_tags):
        dont_care = self.name
        dont_care = self.jtagpos
        dont_care = self.irlength
        dont_care = self.jtagid
        dont_care = self.jtag_attn
        dont_care = self.tap_type
        dont_care = self.jtag_status
        dont_care = self.jtag_ctrl

_SoC_jtagpos_doc = _SoCStrs._jtagpos_ldesc
SoC.jtagpos = _numeric_property(SoC, 'jtagpos', ((_SoCStrs._jtagpos_tag, False), _SoCStrs._jtagpos_desc), 0, doc=_SoC_jtagpos_doc)

_SoC_irlength_doc = _SoCStrs._irlen_ldesc
SoC.irlength = _numeric_property(SoC, 'irlength', ((_SoCStrs._irlen_tag, False), _SoCStrs._irlen_desc), 0, doc=_SoC_irlength_doc)

_SoC_jtagid_doc = _SoCStrs._jtagid_ldesc
SoC.jtagid = _numeric_property(SoC, 'jtagid', ((_SoCStrs._jtagid_tag, False), _SoCStrs._jtagid_desc), 0, doc=_SoC_jtagid_doc)

_SoC_jtag_attn_doc = _SoCStrs._jtattn_ldesc
SoC.jtag_attn = _numeric_property(SoC, 'jtag_attn', ((_SoCStrs._jtattn_tag, False), _SoCStrs._jtattn_desc), 0, doc=_SoC_jtag_attn_doc)

_SoC_tap_type_doc = _SoCStrs._taptype_ldesc
SoC.tap_type = _numeric_property(SoC, 'tap_type', ((_SoCStrs._taptype_tag, False), _SoCStrs._taptype_desc), 0, doc=_SoC_tap_type_doc)

_SoC_jtag_status_doc = _SoCStrs._jtstatus_ldesc
SoC.jtag_status = _numeric_property(SoC, 'jtag_status', ((_SoCStrs._jtstatus_tag, False), _SoCStrs._jtstatus_desc), 0, doc=_SoC_jtag_status_doc)

_SoC_jtag_ctrl_doc = _SoCStrs._jtctrl_ldesc
SoC.jtag_ctrl = _numeric_property(SoC, 'jtag_ctrl', ((_SoCStrs._jtctrl_tag, False), _SoCStrs._jtctrl_desc), 0, doc=_SoC_jtag_ctrl_doc)
SoC._children_ = children_property(SoC._tag_order, SoC._valid_children)

@bsp_object
class Board(HDObject):
    """
    Defines a Board.
    
    Board objects can contain :class:`SoC`, :class:`SoCLink`, :class:`Settings` and :class:`Setting` objects.

    There can be either one of :class:`SoC` or :class:`SoCLink` but not both.
    """
    
    _name_attrs = ["N", "Name"]
    _tap_tag = 'Taps'
    _tag_order = _ctag_order()
    _valid_children = [SoC, SoCLink, Settings, Setting]
    _must_have_props = []
    _must_have_classes = [((SoC, SoCLink), 1)]
    class_attributes_map = {}    

    @classmethod
    def tag_name(cls):
        return 'Board'
            
    @classmethod
    def can_be_pimpl(cls):
        return False
    
    @classmethod
    def property_info(cls):
        return HDObject._property_info_impl(None) + [PropertyInfo('Number of Taps', 'tap_count', PropertyKind.dec, "Number of test access ports. A positive integer.")]
    
    def __str__(self):
        return "Board"
    
    def _check_name(self, name):
        return name_non_empty_string(name)
    
    def _validate_consistent_attributes(self, child_element_tags):
        dont_care = self.name
        dont_care = self.tap_count

_Board_tap_count_doc = "Number of test access ports. A positive integer."
Board.tap_count = _numeric_property(Board, 'tap_count', ((Board._tap_tag, False), 'Number of Taps'), 0, doc=_Board_tap_count_doc)
Board._children_ = children_property(Board._tag_order, Board._valid_children)

@bsp_object
class Document(HDObject):
    """The root element of the Hardware Definition XML data. All objects must have this element as
    the outermost enclosing object.
    
    Document objects can contain :class:`Board`, :class:`Processor`, :class:`ProcessorLink`,
    :class:`SoC`, :class:`SoCLink` and :class:`CoreID` objects.
    """
    
    _tag_order = _ctag_order()
    _valid_children = [Board, Processor, ProcessorLink, SoC, SoCLink, CoreID]
    _must_have_props = []
    _must_have_classes = []
    class_attributes_map = {}    
            
    @classmethod
    def tag_name(cls):
        return 'ioconfig'
    
    @classmethod
    def can_be_pimpl(cls):
        return True
    
    @classmethod
    def property_info(cls):
        return HDObject._property_info_impl(None)
    
    @classmethod
    def has_editable_name(cls):
        return False
    
    def __str__(self):
        return "Document"
    
    @property
    def document_element(self):
        return self.node
    
    @property
    def name(self):
        return self.node.tagName
    
    @name.setter
    def name(self, n):
        self.warnings.report(self.node, "Cannot change Document name", None)
        
    def search(self, results):
        pass

    def convert_all_unsupported_tags(self):
        self._convert_all_unsupported_tags()
    
Document._children_ = children_property(Document._tag_order, Document._valid_children)

def factory(doc, node, warnings, filename = None, suppress_warnings=False):
    if node.nodeType != Node.DOCUMENT_NODE:
        try:
            obj = bsp_objects[node.tagName](doc, node, warnings, filename)
            return obj
        except KeyError:
            for cls in bsp_objects.itervalues():
                if cls._has_value_tag(node.tagName):
                    return None
            msg = "%s is unsupported in the Hardware Definition Editor" % file_line(node, filename)
            if not suppress_warnings and msg:
                warnings.report(None, msg, False)
            return UnhandledObject(doc, node, warnings)
    return None

# end of library code

def empty_ioconfig(cls):
    domimpl = img_xml.getDOMImplementation(None)
    tag_names = cls.tag_name()
    return domimpl.createDocument(EMPTY_NAMESPACE, tag_names[0] if isinstance(tag_names, list) else tag_names, None)

def empty_document(warnings=None):
    """Returns an empty :class:`Document` object.
    
    :optional warnings: a warnings object described in :class:`HDObject`.
    """
    doc = empty_ioconfig(Document)
    return factory(doc, doc.documentElement, warnings or Warnings())
        
def load(filename, warnings=None, suppress_warnings=False):
    """Loads and parses a file given the filename returning a Hardware Definition object of the root element in the XML file.
    
    :string filename: the name of an XML file describing some Hardware Definition system.
    
    :optional warnings: a warnings object described in :class:`HDObject`.
    
    :optional boolean suppress_warnings: do not issue warnings through the warnings object.
    """
    doc = img_xml.parse(filename)
    return factory(doc, doc.documentElement, warnings or Warnings(), filename=filename, suppress_warnings=suppress_warnings)

def load_string(text, warnings=None, filename = None):
    warnings = warnings or Warnings()
    try:
        warnings.clear()
        doc = img_xml.parseString(text)
        return factory(doc, doc.documentElement, warnings, filename), None
    except XmlError as err:
        obj = empty_document(warnings)
        msg = str(err)
        if hasattr(err, 'lineno') and hasattr(err, 'offset'):
            msg = "%d[%d]" % (err.lineno, err.offset)
        warnings.report(None, "XML error %s" % (msg,), False)
        return obj, msg

def loads(text, warnings=None, filename = None):
    """Loads and parses the given string 'text' returning a Hardware Definition
    object of the root element in the XML string and a string warning or None.

    :string text: the XML text fragment.
    
    :optional warnings: a warnings object described in :class:`HDObject`.
    
    :optional string filename: a filename associated with the XML text fragment.
    
    For example:
    
    >>> obj = loads('<f N="Bitfield1"><fm>0xf0f0f0f0</fm><rs>3</rs></f>')
    >>> obj.name
    'Bitfield1'
    
    >>> print "0x%08x" % obj.mask
    0xf0f0f0f0
    
    >>> print obj.shift
    3
    """
    return load_string(text, warnings, filename)[0]


import re

class NameError(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)
        
class _ErrorEmpty(NameError):
    def __init__(self):
        NameError.__init__(self, 'name should not be empty')

class _ErrorReMatch(NameError):
    def __init__(self, *args):
        NameError.__init__(self, "\"%s\" %s (regular expression %s)" %  args)

class _ErrorReOption(NameError):
    def __init__(self, *args):
        NameError.__init__(self, "\"%s\" unrecognised regular expression option flag(s) : \"%s\"" % args)

class _ErrorReInvalid(NameError):
    def __init__(self, *args):
        NameError.__init__(self, "the name \"%s\" is not a valid regular expression : %s" % args)

_crex     = re.compile(r"^[a-zA-Z_][a-zA-Z_0-9]*$", 0), "must be a C identifier"
_xml_safe = re.compile(r"""^[^&<>"']+$""",          0), """cannot contain any of: & < > " '"""
_xml_safe_id = _xml_safe[0], """must be non-empty and """ + _xml_safe[1]

def _matches_id(name, rex_thing):
    rex, desc = rex_thing
    if len(name) != 0:
        if not rex.match(name, 0):
            raise _ErrorReMatch, (name, desc, rex.pattern)
        return name
    raise _ErrorEmpty
    
def _optional_matches(text, rex_thing):
    if (len(text) != 0):
        return _matches_id(text, rex_thing)
    return text

def optional_matches_identifier(name):
    return _optional_matches(name, _crex)
    
def optional_xml_safe(text):
    return _optional_matches(text, _xml_safe)

def xml_safe(text):
    return _matches_id(text, _xml_safe)

def matches_general_id(name):
    return _matches_id(name, _xml_safe_id)
            
def matches_cidentifier(name):
    return _matches_id(name, _crex)
            
def name_non_empty_string(name):
    if name:
        return name
    raise _ErrorEmpty
            
def allow_anything_apart_from_bad_slashed_regex(name):
    org_name = name
    syntax_option = 0;
    if len(name) != 0:
        if name[0] == '/':
            name = name[1:]
            flags = ""
            pos = name.rfind('/')
            if pos != -1:
                flags = name[pos + 1:]
                name = name[0:pos]
            if flags == "i":
                syntax_option = re.IGNORECASE;
            elif len(flags) != 0:
                raise _ErrorReOption(org_name, flags)
            try:
                re.compile(name, syntax_option)
            except re.error as what:
                raise _ErrorReInvalid(org_name, what)
        return org_name
    raise _ErrorEmpty
        

__all__ += sorted(x.__name__ for x in bsp_classes)
__all__.extend([UnknownHDObject.__name__, UnhandledObject.__name__, Warnings.__name__, PropertyKind.__name__, PropertyInfo.__name__])
__all__.extend([Size.__name__, Access.__name__, Radix.__name__, MemorySetting.__name__, Cacheable.__name__])
__all__.extend([empty_document.__name__, load.__name__, load_string.__name__, loads.__name__])
            
if __name__ == "__main__":
    import doctest
    doctest.testmod()
    
