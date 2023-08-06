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

import wx
import itertools, math
from collections import namedtuple
from contextlib import contextmanager
from imgtec.test import *

from ..namedenum import namedenum

max_num_of_intervals = 2048

DRAW_GRAPH_EPSILON             = float(0.000000001)
DRAW_GRAPH_FLOAT_CORRECTION    = float(0.5) - DRAW_GRAPH_EPSILON

GraphAxis = namedenum("GraphAxis", "X", "Y")

def type_property(name, type_cast_fn):
    """Creates a getter/setter for the named variable which casts to the desired type."""
    def get(self):
        return getattr(self, name)
    def set(self, value):
        setattr(self, name, type_cast_fn(value))
    return property(get, set)

def float_property(name):
    """Gives you a get & set property a particular type

    Assigning to self.x will auto-cast it to a float.

    >>> class MyClass(object):
    ...     def __init__(self):
    ...         self._x = 0.0
    ...     x = float_property("_x")
    >>> c = MyClass()
    >>> c.x = "1"
    >>> c.x
    1.0
    """
    return type_property(name, float)

def int_property(name):
    """Gives you a get & set property a particular type

    Assigning to self.x will auto-cast it to a int.

    >>> class MyClass(object):
    ...     def __init__(self):
    ...         self._x = 0
    ...     x = int_property("_x")
    >>> c = MyClass()
    >>> c.x = "1"
    >>> c.x
    1
    """
    return type_property(name, int)

def get_len_of_range(start, stop, step):
    """ Translated from rangeobject.c

    >>> get_len_of_range(1, 40, 0)
    0
    >>> get_len_of_range(0, 40, 1)
    40
    >>> get_len_of_range(0, 40, 2)
    20
    >>> get_len_of_range(0, 41, 3)
    14
    >>> get_len_of_range(-50, -10, 3)
    14
    >>> get_len_of_range(40, 0, -1)
    40
    >>> get_len_of_range(39, 0, -2)
    20
    >>> get_len_of_range(41, 0, -3)
    14
    >>> get_len_of_range(-10, -50, -3)
    14
    >>> get_len_of_range(0.0, 6.0, 1.5)
    4.0
    >>> get_len_of_range(0.0, 6.0, 0.75)
    8.0
    >>> get_len_of_range(0.0, 0.5, 0.1)
    5.0
    >>> get_len_of_range(0.0, -0.5, -0.1)
    5.0
    """
    unit_offset = min(1, abs(step))
    if step > 0 and start < stop:
        return 1 + (stop - unit_offset - start) // step
    elif step < 0 and start > stop:
        return 1 + (start - unit_offset - stop) // (0 - step)
    else:
        return 0

orig_xrange = xrange

def xrange(start, stop=None, step=1):
    """xrange which is not restricted to int32 range.

    >>> ["0x%x" % x for x in xrange(0xf0000000, 0xf0000003)]
    ['0xf0000000', '0xf0000001', '0xf0000002']
    >>> ["0x%x" % x for x in xrange(0xf0000000, 0xf0000005, 2)]
    ['0xf0000000', '0xf0000002', '0xf0000004']
    """
    if step == 0:
        raise ValueError("xrange() arg 3 must not be zero")
    if stop is None:
        stop = start
        start = 0
    n = get_len_of_range(start, stop, step)
    i = 0
    while i < n:
        yield start
        start += step
        i += 1

def float_range(min_range, max_range, interval, max_intervals):
    """Returns a list of float ranges between the min & max stepped by the interval.

    >>> ["%0.1f" % f for f in float_range(0, 0.5, 0.1, 10)]
    ['0.0', '0.1', '0.2', '0.3', '0.4']

    >>> ["%0.1f" % f for f in float_range(0, 0.5, 0.1, 5)]
    ['0.0', '0.1', '0.2', '0.3', '0.4']

    >>> ["%0.1f" % f for f in float_range(0, 0.5, 0.1, 5.0)]
    ['0.0', '0.1', '0.2', '0.3', '0.4']

    >>> ["%f" % f for f in float_range(12.7, 27.6, 3.14157, 5)]
    ['12.700000', '15.841570', '18.983140', '22.124710', '25.266280']

    >>> ["%0.1f" % f for f in float_range(50, 100, 10, 5)]
    ['50.0', '60.0', '70.0', '80.0', '90.0']

    >>> ["%f" % f for f in float_range(-12.1, 13.7, 3.14157, 10)]
    ['-12.100000', '-8.958430', '-5.816860', '-2.675290', '0.466280', '3.607850', '6.749420', '9.890990']

    >>> ["%0.1f" % f for f in float_range(0, 0.5, 0.1, 4)]
    ['0.0', '0.1', '0.2', '0.3']

    >>> ["%0.1f" % f for f in float_range(0, 10, 0.0, 10)]
    Traceback (most recent call last):
    ...
    ValueError: Error float_range interval 0.000000 must be > 0.0

    >>> ["%0.1f" % f for f in float_range(0, 10, +0.0, 10)]
    Traceback (most recent call last):
    ...
    ValueError: Error float_range interval 0.000000 must be > 0.0

    >>> ["%0.1f" % f for f in float_range(0, 10, 0, 10)]
    Traceback (most recent call last):
    ...
    ValueError: Error float_range interval 0.000000 must be > 0.0

    >>> ["%0.1f" % f for f in float_range(0, 10, -0.0, 10)]
    Traceback (most recent call last):
    ...
    ValueError: Error float_range interval -0.000000 must be > 0.0

    >>> ["%0.1f" % f for f in float_range(99.4, 0.5, 0.1, 10)]
    Traceback (most recent call last):
    ...
    ValueError: Error float_range range_min 99.400000 must not be greater than range_max 0.500000

    """
    f_interval = float(interval)
    if f_interval <= 0.0:
        raise ValueError('Error float_range interval %f must be > 0.0' % (f_interval))

    f_min_range = float(min_range)
    f_max_range = float(max_range)

    if f_min_range > f_max_range:
        raise ValueError('Error float_range range_min %f must not be greater than range_max %f' % (f_min_range, f_max_range))

    return list(itertools.islice(xrange(f_min_range, f_max_range, f_interval), int(max_intervals)))

def constrain(minimum, x, maximum):
    """Returns a value of x such that minimum <= x <= maximum.

    >>> constrain(0, 1, 3)
    1
    >>> constrain(0.5, 0.25, 3.5)
    0.5
    >>> constrain(0.5, 4.25, 3.5)
    3.5
    >>> constrain(0, 0, 0)
    0
    >>> constrain(1, 0, 1)
    1
    >>> constrain(1, 2, 1)
    1
    >>> constrain(2, 1, 0)
    Traceback (most recent call last):
    ...
    ValueError: The minimum value given is greater than the maximum value
    """
    if minimum > maximum:
        raise ValueError('The minimum value given is greater than the maximum value')
    return min(maximum, max(x, minimum))

@contextmanager
def _scoped_set(getter, setter, item):
    old = getter()
    setter(item)
    try:
        yield
    finally:
        setter(old)

def set_font(dc, font):
    """Selects a font into a DC and restores it after the scope is exited.
       e.g.
        with set_font(dc, font):
            dc.DrawText(text, x, y)
    """
    return _scoped_set(dc.GetFont, dc.SetFont, font)

def _reset_clip_if_valid_rect(dc, rect):
    dc.DestroyClippingRegion()
    if rect != (0,0,0,0):
         dc.SetClippingRect(rect)

@contextmanager
def push_clipping_rect(dc, rect):
    """This will remember the old clip, then intersect the new clip with the existing one and then restore the original it after the scope is exited."""
    old_clip = dc.GetClippingRect()
    dc.SetClippingRect(rect)
    try:
        yield
    finally:
        _reset_clip_if_valid_rect(dc, old_clip)

def Rectx1y1(x,y,x1,y1):
    """This function will take (x y x1 y1) points and return a Rect.
    So it acts as a an alternative constructor for the Rect class (below) that
    takes (x y width height) for construction.
    """
    return Rect(x,y,int(x1)-int(x),int(y1)-int(y))

class Rect(object):
    """This is an immutable class that defines an integer rectangle.
    You can refer to the rect in either (x,y,width,height) format or (x,y,x1,y1)
    The constructor is in the format (x,y,with,height)

    There is a buddy function (above) Rectx1y1 which is derived from this and
    the only difference is it offers a (x,y,x1,y1) constructor.

    This Rect class supports negative points and negative width or height.

    Note: If you pass a floating point value as a parameter it will be rounded
    down to the nearest int.
    e.g. 10.9999 will be rounded down to 10.
    """
    def __init__(self, x=0, y=0, w =0, h =0):
        self._set_xywh(x,y,w,h)

    def _set_xywh(self, x, y, w, h):
        self._x      = int(x)
        self._y      = int(y)
        self._width  = int(w)
        self._height = int(h)

    def _get_normalised_x_and_width(self, x, width):
        """This function return a normalised x and width if width is negative.
        Otherwise it will simply return x and width.
        """
        if width < 0:
            n_width = abs(width)
            n_x     = x - n_width  # x - the abs(width)
        else:
            n_width = width
            n_x     = x
        return (n_x, n_width)

    def _get_normalised_rect(self):
        """Returns a new normalised Rect.
        A normalised rect is one that has a positive width and height.
        It is quite valid for Rect to describe a rectangle with negative width
        or height.
        The reason why we have this is that comparisons (needed for intersects
        or encloses functions) get very over complex if one rectangle has a
        positive width or height and the other does not.
        So the technique is to normalise both Rects and then compare.

        >>> rect = Rect(10,10,-10,-10)
        >>> n_rect = rect._get_normalised_rect()
        >>> n_rect.xywh
        (0, 0, 10, 10)
        >>> rect = Rect(10,10,10,10)
        >>> n_rect = rect._get_normalised_rect()
        >>> n_rect.xywh
        (10, 10, 10, 10)
        >>> rect = Rect(10,10,-20,-20)
        >>> n_rect = rect._get_normalised_rect()
        >>> n_rect.xywh
        (-10, -10, 20, 20)
        """
        (n_x, n_width) = self._get_normalised_x_and_width(self._x, self._width)
        (n_y, n_height) = self._get_normalised_x_and_width(self._y, self._height)
        return Rect(n_x, n_y, n_width, n_height)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def xywh(self):
        return (self.x, self.y, self.width, self.height)

    @property
    def xyx1y1(self):
        return (self.x, self.y, self.x1, self.y1)

    @property
    def x1(self):
        return self.x +  self.width

    @property
    def y1(self):
        return self.y +  self.height


    def offset(self, cx, cy):
        """This will return a copy of this rect offset by the specified amount.

        Paramters...
        cx : amount to offset on the x axis
        cy : amount to offset on the y axis

        Both offsets can be negative.

        >>> rect = Rect(0,0,100,100)
        >>> offset_rect = rect.offset(10,10)
        >>> offset_rect.xywh
        (10, 10, 100, 100)
        >>> offset_rect.xyx1y1
        (10, 10, 110, 110)
        >>> rect = Rect(0,0,100,100)
        >>> offset_rect = rect.offset(-10,-10)
        >>> offset_rect.xywh
        (-10, -10, 100, 100)
        >>> offset_rect.xyx1y1
        (-10, -10, 90, 90)
        """
        return Rect(self.x+cx, self.y+cy, self.width, self.height)

    def get_corner_points(self):
        """This will return a list of the corner points as (x,y) tuples.
        The rect will be normalised before returning the points. This means
        you will get the points in a fixed order.
        The order of the points in the list is...
            (x,  y)
            (x1, y)
            (x1, y1)
            (x,  y1)

        >>> rect = Rect(10,10,100,100)
        >>> rect.get_corner_points()
        [(10, 10), (110, 10), (110, 110), (10, 110)]
        >>> rect = Rect(10,10,-100,-100)
        >>> rect.get_corner_points()
        [(-90, -90), (10, -90), (10, 10), (-90, 10)]
        """
        n_rect       = self._get_normalised_rect()
        top_left     = (n_rect.x, n_rect.y)
        top_right    = (n_rect.x1, n_rect.y)
        bottom_right = (n_rect.x1, n_rect.y1)
        bottom_left  = (n_rect.x, n_rect.y1)
        return [top_left, top_right, bottom_right, bottom_left]

    def is_point_in_rect(self, point):
        """Returns True if the point is within the bounds of this rect.

        Parameters...
        point : (x,y) tuple defining a point

        >>> rect = Rect(10,10,100,100)
        >>> rect.is_point_in_rect((10,10))
        True
        >>> rect.is_point_in_rect((100,100))
        True
        >>> rect.is_point_in_rect((50,50))
        True
        >>> rect.is_point_in_rect((0,10))
        False
        >>> rect = Rect(10,10,-100,-100)
        >>> rect.is_point_in_rect((-90,-90))
        True
        >>> rect.is_point_in_rect((50,50))
        False
        """
        x = point[0]
        y = point[1]
        n_rect = self._get_normalised_rect()
        return x >= n_rect.x and x <= n_rect.x1 and y >= n_rect.y and y <= n_rect.y1

    def are_all_points_in_rect(self, point_list):
        """Returns True if all the points in the point_list are within the bounds of this rect.

        Parameters...
        point_list : a list of (x,y) tuple points

        >>> rect = Rect(10,10,100,100)
        >>> point_list = [(10,10), (10,110), (110,110), (110, 10), (50,60)]
        >>> rect.are_all_points_in_rect(point_list)
        True
        >>> point_list.append((9,9))
        >>> rect.are_all_points_in_rect(point_list)
        False
        """
        for point in point_list:
            if not self.is_point_in_rect(point):
                return False
        return True

    def are_any_points_in_rect(self, point_list):
        """Returns True if any of the points in the point_list are within the bounds of this rect.

        Parameters...
        point_list : a list of (x,y) tuple points

        >>> rect = Rect(10,10,100,100)
        >>> point_list = [(200,10), (10,210), (210,110), (210, 10), (50,60)]
        >>> rect.are_any_points_in_rect(point_list)
        True
        >>> point_list = [(200,10), (10,210), (210,110), (210, 10), (250,60)]
        >>> rect.are_any_points_in_rect(point_list)
        False
        """
        for point in point_list:
            if self.is_point_in_rect(point):
                return True
        return False

    def intersects(self, other_rect):
        """Returns True if other_rect intersects this rect.

        Parameters...
        other_rect : a Rect object to compare with.

        >>> rect = Rectx1y1(10,10,100,100)
        >>> other_rect = Rectx1y1(90,90,110,110)
        >>> rect.intersects(other_rect)
        True
        >>> another_rect = Rectx1y1(210,10,310,100)
        >>> rect.intersects(another_rect)
        False
        """
        return self.are_any_points_in_rect(other_rect.get_corner_points())

    def get_enclosing_deltas(self, inner_rect):
        """Returns the deltas between this the outer rect and the given inner rect.
        The deltas are retuned as a tuple in this format...
        (xDelta, yDelta, x1Delta, y1Delta)
        or another way of expressing this is...
        (leftDelta, topDelta, rightDelta, bottomDelta)

        Parameters...
        inner_rect : a Rect object defining the inner rect.

        >>> outer = Rect(10,10,100,100)
        >>> inner = Rect(20,20,80,80)
        >>> outer.get_enclosing_deltas(inner)
        (-10, -10, -10, -10)
        >>> inner.get_enclosing_deltas(outer)
        (10, 10, 10, 10)
        """

        n_outer_rect = self._get_normalised_rect()
        n_inner_rect = inner_rect._get_normalised_rect()
        return (n_outer_rect.x - n_inner_rect.x, n_outer_rect.y - n_inner_rect.y, n_inner_rect.x1 - n_outer_rect.x1, n_inner_rect.y1 - n_outer_rect.y1)

    def encloses(self, inner_rect):
        """Returns True if this Rect full encloses the given inner_rect.

        >>> outer = Rect(10,20,100,200)
        >>> inner = Rect(30,40,10,20)
        >>> outer.encloses(inner)
        True
        >>> inner.encloses(outer)
        False
        >>> outer = Rect(10,20,100,200)
        >>> inner = Rect(9,20,100,200)
        >>> outer.encloses(inner)
        False
        >>> outer = Rect(0,0,0,0)
        >>> inner = Rect(0,0,0,0)
        >>> outer.encloses(inner)
        True
        """
        return self.are_all_points_in_rect(inner_rect.get_corner_points())

    def expanded(self, cx, cy, cx1, cy1):
        """This will return a new Rect expanded by the given amounts.
        Parameters...
        cx  : amount to expand left
        cy  : amount to expand the top
        cx1 : amount to expand right
        cy1 : amount to expand the bottom

        >>> rect = Rectx1y1(10,10,100,100)
        >>> new_rect = rect.expanded(1,1,1,1)
        >>> new_rect.xyx1y1
        (9, 9, 101, 101)
        >>> rect = Rectx1y1(-10,-10,-100,-100)
        >>> new_rect = rect.expanded(1,1,1,1)
        >>> new_rect.xyx1y1
        (-11, -11, -99, -99)
        """
        return Rectx1y1(self.x - cx, self.y - cy, self.x1 + cx1, self.y1 + cy1)

    def shrunk(self, cx, cy, cx1, cy1):
        """This will return a new Rect shrunk by the given amounts.
        Parameters...
        cx  : amount to shrink left
        cy  : amount to shrink the top
        cx1 : amount to shrink right
        cy1 : amount to shrink the bottom

        >>> rect = Rectx1y1(10,10,100,100)
        >>> new_rect = rect.shrunk(1,1,1,1)
        >>> new_rect.xyx1y1
        (11, 11, 99, 99)
        >>> rect = Rectx1y1(-10,-10,-100,-100)
        >>> new_rect = rect.shrunk(1,1,1,1)
        >>> new_rect.xyx1y1
        (-9, -9, -101, -101)
        """
        return self.expanded(-cx, -cy, -cx1, -cy1)

class GraphRange(object):
    """This is an immutable range container class.
    This simply stores an min, max range definition.
    The class guarantees the range values are floats and max >= min.
    """
    def __init__(self, min = 0.0, max = 0.0):
        self._min = float(min)
        self._max = float(max)
        if(self._min > self._max):
            self._min, self._max = self._max, self._min    

    @property
    def min(self):
        return self._min
        
    @property
    def max(self):
        return self._max
        
    @property
    def range(self):
        return self._max - self._min

class GraphLineStyle(object):
    """
    .. method:: __init__([line_colour = (0,0,0)], [line_width = 1], [style = SOLID])
    
    This immutable class defines a line style.
    
    Line styles are used by :class:`~imgtec.lib.wx_extensions.GraphControl`, 
    :class:`~imgtec.lib.wx_extensions.GraphAxisInfo`, 
    :class:`~imgtec.lib.wx_extensions.DrawGraphController` and
    :class:`~imgtec.lib.wx_extensions.GraphBarStyle`.
    
    :param line_colour: This is an RGB tuple. This is defaulted to (0,0,0) black
    :param line_width:  This is the width of the line. Default is 1.
    
                        .. note:: Some styles will only draw a 1 width line regardless of this value.

    :param style:       This is the style of the line which can be one of the following values.
                                
                            ====================  ===========================
                            **SOLID**             Solid style.
                            **TRANSPARENT**       No pen is used.
                            **DOT**               Dotted style.
                            **LONG_DASH**         Long dashed style.
                            **SHORT_DASH**        Short dashed style.
                            **DOT_DASH**          Dot and dash style.
                            **STIPPLE**           Use the stipple bitmap.
                            **BDIAGONAL_HATCH**   Backward diagonal hatch.
                            **CROSSDIAG_HATCH**   Cross-diagonal hatch.
                            **FDIAGONAL_HATCH**   Forward diagonal hatch.
                            **CROSS_HATCH**       Cross hatch.
                            **HORIZONTAL_HATCH**  Horizontal hatch.
                            **VERTICAL_HATCH**    Vertical hatch.
                            ====================  ===========================
                            
                        Default is SOLID.    
    """
    def __init__(self, line_colour = (0,0,0), line_width = 1, style = wx.SOLID):         
        self._line_colour = line_colour    # This is an RGB tuple
        self._line_width  = int(line_width) # Note some pen styles ignore this value and can only do a width of 1  
        self._pen_style   = style    # A wx pen style e.g. wx.SOLID,  wx.DOT,  wx.DOT_DASH           
        
    @property
    def line_colour(self):
        return self._line_colour

    @property
    def line_width(self):
        return self._line_width
        
    @property
    def pen_style(self):
        return self._pen_style
        
class GraphBarStyle(object):
    """
    .. method:: __init__([bar_colour=(0,0,255)], [bar_style=SOLID], [draw_solid_bar=True], [x_orientation=True], [draw_outline=True], [line_style=None])

    This immutable class defines a bar style.

    The Bar style is used by the following classes:
    
        * :class:`~imgtec.lib.wx_extensions.DrawGraphController`
        * :class:`~imgtec.lib.wx_extensions.GraphControl`
    
    :param bar_colour:      This is a (Red, Green, Blue) tuple. Default is (0,0,255) blue.
    :param bar_style:       This is the style of the brush used to fill the bar which can be one of the following values.
                            
                                ====================   ===========================
                                **TRANSPARENT**        Transparent (no fill).
                                **SOLID**              Solid.
                                **STIPPLE**            Uses a bitmap as a stipple.
                                **BDIAGONAL_HATCH**    Backward diagonal hatch.
                                **CROSSDIAG_HATCH**    Cross-diagonal hatch.
                                **FDIAGONAL_HATCH**    Forward diagonal hatch.
                                **CROSS_HATCH**        Cross hatch.
                                **HORIZONTAL_HATCH**   Horizontal hatch.
                                **VERTICAL_HATCH**     Vertical hatch.
                                ====================   ===========================
                                    
                                Default is SOLID.
                                
    :param draw_solid_bar:  When True this will fill the bar with the specified colour and brush style. Default is True.
    :param x_orientation:   When True is will draw an X orientated Bar Graph else it will be Y orientated. Default is True.
    :param draw_outline:    When True this will draw an outline around each rectangle using the pen specified by the line object below. Default is True.
    :param line:            This is a :class:`~imgtec.lib.wx_extensions.GraphLineStyle` object. Default is GraphLineStyle().
    """
    def __init__(self, bar_colour = (0,0,255), bar_style = wx.SOLID, draw_solid_bar = True, x_orientation = True, draw_outline = True, line_style = GraphLineStyle()):
        self._bar_colour         = bar_colour
        self._wx_bar_brush_style = bar_style
        self._line               = line_style
        self._draw_outline       = draw_outline
        self._draw_solid_bar     = draw_solid_bar
        self.x_orientation       = x_orientation
 
    @property
    def bar_colour(self):
        return self._bar_colour

    @property
    def wx_bar_brush_style(self):
        return self._wx_bar_brush_style

    @property
    def line(self):
        return self._line

    @property
    def draw_outline(self):
        return self._draw_outline

    @property
    def draw_solid_bar(self):
        return self._draw_solid_bar


SHRT_MIN = -32768        # minimum (signed) short value 
SHRT_MAX = 32767         # maximum (signed) short value 

def _validate_coord(x):
    """make sure the coord is an int and within range of a draw context.
    
    Parameters...
    x : a screen pixel position
    
    >>> _validate_coord(0)
    0
    >>> _validate_coord(10)
    10
    >>> _validate_coord(-10)
    -10
    >>> _validate_coord(10.9)
    10
    >>> _validate_coord(-10.2)
    -10
    >>> _validate_coord(32767)
    32767
    >>> _validate_coord(32768)
    32767
    >>> _validate_coord(-32768)
    -32768
    >>> _validate_coord(-32769)
    -32768
    """
    return constrain(SHRT_MIN, int(x),SHRT_MAX)

def _calculate_factor(range, width):
    """This will calculate an axis factor
    The axis factor describes the relationship between the screen coordinates
    and the graphs coordinates.

    Parameters...
    range : The range of what the graph axis represents.
    width : The width of axis on screen
    
    >>> _calculate_factor(100, 1000)
    10.0
    >>> _calculate_factor(1000, 100)
    0.1
    >>> _calculate_factor(0, 1000)
    0.0
    >>> _calculate_factor(1000, 0)
    0.0
    """
    return float(width) / range if(range != 0) else 0.0
    
def _scaler(value, factor):
    """Given a value and the axis factor this will return an integer screen position within the graph.
    
    Parameters...
    value  : A value within what the axis represents.
    factor : The factor between the what the axis represents and the width on screen.

    >>> _scaler(100, 0.10000000000000001)
    10
    >>> _scaler(100, 10.0)
    1000
    >>> _scaler(100.5, 1)
    100
    >>> _scaler(100.5 + DRAW_GRAPH_EPSILON, 1)
    101
    """
    return int((factor * value) + DRAW_GRAPH_FLOAT_CORRECTION)

def _un_scaler(x, factor):
    """Returns the value from the screen position within the graph and the axis factor
    
    Parameters...
    x      : A screen position along the axis.
    factor : The factor between the what the axis represents and the width on screen.
    
    >>> _un_scaler(10, 0.1)
    100.0
    >>> _un_scaler(10, 1)
    10.0
    >>> _un_scaler(10, 10)
    1.0
    >>> _un_scaler(10, 0)
    0.0
    >>> _un_scaler(0.0, 10)
    0.0
    """
    return float(x) / factor if(factor > 0 or factor < 0) else 0.0

class DrawGraph(object):
    def __init__(self):
        self._graph_rect            = Rect()     #  This is the rect of the graph the user would like. This used to calculate scale etc.
        self._draw_rect             = Rect()     #  This is the rect of what the user is given. This can change from the rect above due to rounding errors once scaling has been calculated. This rect is the scaled positions of the min and max ranges of both axis.
        self._x_range               = GraphRange()      
        self._y_range               = GraphRange()
        self._tick_height           = 4
        self._cross_width           = 4               # Sets the size of the 'X' to draw with the draw_crosses function. 
        self._x_zero                = 0
        self._y_zero                = 0
        self._x_factor              = 0
        self._y_factor              = 0
        self._draw_graph_min_size   = 1

    #properties
    tick_height             = int_property("_tick_height")
    cross_width             = int_property("_cross_width")
    x_zero                  = int_property("_x_zero")
    y_zero                  = int_property("_y_zero")
    x_factor                = float_property("_x_factor")
    y_factor                = float_property("_y_factor")
    draw_graph_min_size     = int_property("_draw_graph_min_size")
    
    @property
    def graph_rect(self):
        return self._graph_rect
        
    @graph_rect.setter
    def graph_rect(self, rect):
        self._graph_rect = rect
        self._calculate_x_factors()
        self._calculate_y_factors()
        self._set_draw_rect()

    @property
    def x_range(self):
        return self._x_range
        
    @x_range.setter
    def x_range(self, range):
        self._x_range = range
        signal_x_range_change()        
                
    @property
    def y_range(self):
        return self._y_range
        
    @y_range.setter
    def y_range(self, range):
        self._y_range = range
        signal_y_range_change()        
            
    def _set_draw_rect(self):
        self._draw_rect = Rectx1y1(self.value_to_screen_x(self.x_range.min), self.value_to_screen_y(self.y_range.max), self.value_to_screen_x(self.x_range.max), self.value_to_screen_y(self.y_range.min))
        
    def _calculate_x_factor(self):
        return _calculate_factor(self.x_range.range, self.graph_rect.width)
        
    def _calculate_y_factor(self):
        return _calculate_factor(self.y_range.range, self.graph_rect.height)
        
    def _calculate_zero(self, x, min, factor):
        return x + _scaler(-min, factor)

    def _calculate_x_zero(self, XFactor):
        return self._calculate_zero(self.graph_rect.x, self.x_range.min, XFactor)    

    def _calculate_y_zero(self, YFactor):
        return self._calculate_zero(self.graph_rect.y1, -self.y_range.min, YFactor)

    def _calculate_x_factors(self):
        self.x_factor = self._calculate_x_factor()        
        self.x_zero = self._calculate_x_zero(self.x_factor)
    
    def _calculate_y_factors(self):
        self.y_factor = self._calculate_y_factor()        
        self.y_zero = self._calculate_y_zero(self.y_factor)

    def _is_x_axis_at_bottom(self):
        return (self.y_range.min > 0 and self.y_range.max < 0) or (self.y_range.min == 0)

    def _is_y_axis_at_side(self):
        return (self.x_range.min > 0 and self.x_range.max < 0) or (self.x_range.min == 0)

    def _scale_coord(self, CoOrd):
        return wx.Point(self.value_to_screen_x(CoOrd[0]), self.value_to_screen_y(CoOrd[1]))
        
    def _is_it_a_valid_draw(self):
        return (self._draw_rect.width > self.draw_graph_min_size and self._draw_rect.height > self.draw_graph_min_size)

    def _draw_axis(self, dc, x, line, draw_line_fn):
        with wx.DCPenChanger(dc, wx.Pen(line.line_colour, line.line_width, line.pen_style)):
            draw_line_fn(dc, x)
                  
    def _is_it_a_valid_interval(self, interval):
        return interval > 0.0 and (not math.isnan(interval)) and (not math.isinf(interval)) 

    def _round_to_the_nearest_interval(self, min, interval):
        """Given the min value & interval it will return the first interval point that would be on-screen
        
        >>> graph = DrawGraph()
        >>> graph._round_to_the_nearest_interval(2.5, 1.0)
        3.0
        >>> graph._round_to_the_nearest_interval(0.25, 0.1)
        0.30000000000000004
        >>> graph._round_to_the_nearest_interval(-0.25, 0.1)
        -0.2
        >>> graph._round_to_the_nearest_interval(2.5, -1.0) is None
        True
        """
        val = None
        if self._is_it_a_valid_interval(interval):
            val = float(int(min / interval)) * interval
            if val < min:
                val += interval
        return val    

    def _get_list_of_intervals(self, graphrange, interval):
        """Returns a list of intervals starting from min to and including the max of the range.
        
        >>> graph = DrawGraph()
        >>> range = GraphRange(0,10)
        >>> graph._get_list_of_intervals(range, 1)
        [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
        >>> range = GraphRange(0.5,10.5)
        >>> graph._get_list_of_intervals(range, 1.0)
        [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
        >>> range = GraphRange(-1.75, 1.66)
        >>> graph._get_list_of_intervals(range, 1.25)
        [-1.25, 0.0, 1.25]
        >>> range = GraphRange(-1.75, 1.25)
        >>> graph._get_list_of_intervals(range, 1.25)
        [-1.25, 0.0, 1.25]

        >>> graph._get_list_of_intervals(GraphRange(0,0), 0)
        []

        >>> len(graph._get_list_of_intervals(GraphRange(0,0xFFFFFFFF), 0.1)) == max_num_of_intervals
        True

        """
        list = []
        start = self._round_to_the_nearest_interval(graphrange.min, interval)
        if start != None:
            # We need to create a range from start up to and including max
            # To do this a float_range is created one interval past the max
            # If the last entry is past the max then we discard it.
            # This is easier than checking whether the graphrange.max is exactly divisable by the interval
            # as this is floating point division and there is no guaranteed exact divide.
            list = float_range(start, graphrange.max + interval, interval, max_num_of_intervals)
            list_len = len(list)
            if list_len > 0:
                LastVal = list[list_len -1]
                if(LastVal > graphrange.max): # if we have gone past graphrange.max remove last entry
                    list.pop()
 
        return list    

    def _draw_grid_manual(self, dc, value_list, line, to_screen_fn, draw_line_fn):
        with wx.DCPenChanger(dc, wx.Pen(line.line_colour, line.line_width, line.pen_style)):
            for xval in value_list:
                try:
                    x = xval[0]     #  is it a tuple ?
                except TypeError:
                    x = xval        # else is it a single value
                draw_line_fn(dc,to_screen_fn(x))

    def _draw_grid(self, dc, val_range, interval, line, to_screen_fn, draw_line_fn):
        interval = float(interval)
        value_list = self._get_list_of_intervals(val_range, interval)
        self._draw_grid_manual(dc, value_list, line, to_screen_fn, draw_line_fn)

    def _draw_grid_x_line(self, dc, x):
        dc.DrawLine(x,self._draw_rect.y, x, self._draw_rect.y1 +1)

    def _draw_grid_y_line(self, dc, y):
        dc.DrawLine(self._draw_rect.x,y, self._draw_rect.x1 + 1,y)
        
    def _draw_tick_x_line(self, dc, x):
        dc.DrawLine(x,self._draw_rect.y1 + self.tick_height, x, self._draw_rect.y1)

    def _draw_tick_y_line(self, dc, y):
        dc.DrawLine(self._draw_rect.x - self.tick_height,y, self._draw_rect.x,y)

    def _draw_line_from_coords(self, dc, coords, line, draw_fn):
        if self._is_it_a_valid_draw():
            with wx.DCPenChanger(dc, wx.Pen(line.line_colour, line.line_width, line.pen_style)):
                screen_coords = self.create_screen_coords_from_value_coords(coords)
                draw_fn(dc, screen_coords)

    def _draw_line_graph_from_coords(self, dc, coord_list):
       with push_clipping_rect(dc, self._draw_rect.expanded(0,0,1,1).xywh):
            dc.DrawLines(coord_list)
                    
    def _draw_cross(self, dc, coord):
        x = coord.x - self.cross_width
        x1 = coord.x + self.cross_width
        y = coord.y - self.cross_width
        y1 = coord.y + self.cross_width
        dc.DrawLine(x, y, x1+1, y1+1) # draw 1 past as Draw line does not draw the last pixel
        dc.DrawLine(x1, y, x-1, y1+1)
        
    def _draw_crosses_at_coords(self, dc, coord_list):
        clip_rect = self._draw_rect.expanded(self.cross_width, self.cross_width, self.cross_width+1, self.cross_width+1)
        with push_clipping_rect(dc, clip_rect.xywh):
            for coord in coord_list:
                self._draw_cross(dc, coord)
            
    def _create_x_bar_rect(self, x, y_value, x_interval):
        return Rectx1y1(self.value_to_screen_x(x), self.value_to_screen_y(y_value), self.value_to_screen_x(x + x_interval), self.y_zero)
        
    def _create_y_bar_rect(self, y, x_value, y_interval):
        return Rectx1y1(self.x_zero, self.value_to_screen_y(y), self.value_to_screen_x(x_value), self.value_to_screen_y(y + y_interval))
        
    def _create_bar_graph_rect_list(self, start_x, x_interval, values, create_rect_function):
        rect_list = []
        if self._is_it_a_valid_draw() and self._is_it_a_valid_interval(x_interval):
            x = float(start_x)
            for value in values:
                rect_list.append(create_rect_function(x, value, x_interval))
                x+=x_interval
        return rect_list

    def _draw_bar_graph(self, dc, start_x, x_interval, values, bar, create_rect_function):
        with push_clipping_rect(dc, self._draw_rect.expanded(0,0,1,1).xywh):
            with wx.DCPenChanger(dc, wx.Pen(bar.line.line_colour, bar.line.line_width, bar.line.pen_style) if bar.draw_outline else wx.TRANSPARENT_PEN):
                with wx.DCBrushChanger(dc, wx.Brush(bar.bar_colour, bar.wx_bar_brush_style) if bar.draw_solid_bar else wx.TRANSPARENT_BRUSH):                   
                    rect_list = self._create_bar_graph_rect_list(start_x, x_interval, values, create_rect_function)
                    for rect in rect_list:
                        dc.DrawRectangle(rect.x,rect.y, rect.width, rect.height)

    def _get_x_text_rect(self, dc, text, text_width, text_height, value, horizontal, tick_length):
        if horizontal:
            w = text_width
            h = text_height
        else:
            w = text_height            
            h = text_width
        x = self.value_to_screen_x(value) - (w/2)
        y = self._draw_rect.y1 + tick_length
        return Rect(x,y,w,h)

    def _get_y_text_rect(self, dc, text, text_width, text_height, value, horizontal, tick_length):
        if horizontal:
            w = text_width
            h = text_height
        else:
            w = text_height            
            h = text_width
        x = self._draw_rect.x - tick_length - w
        y = self.value_to_screen_y(value) - (h/2)
        return Rect(x,y,w,h)
    
    def _create_text_out_list(self, dc, value_and_text_list, font, horizontal, tick_length, get_text_rect_function):
        list = []
        with set_font(dc, font):
            for value_and_text in value_and_text_list:
                (value,text) = value_and_text
                (width, height) = dc.GetTextExtent(text)
                rect = get_text_rect_function(dc, text, width, height, value, horizontal, tick_length)            
                rotation = 0 if horizontal else 90
                list.append((rect, text, rotation))
        return list            

    def _create_val_text_tuple(self, value, format):
        return (value, format % (value,))

    def _draw_manual_text_on_axis(self, dc, value_and_text_list, font, horizontal, text_colour, tick_length, get_text_rect_function):
        rect_text_rot_list = self._create_text_out_list(dc, value_and_text_list, font, horizontal, tick_length, get_text_rect_function)
        with set_font(dc, font):
            with wx.DCTextColourChanger(dc, text_colour):
                for rect_text_rot in rect_text_rot_list:
                    (rect,text,rotation) = rect_text_rot
                    if text != "": # This is necessary because there is a bug in wxPythonGTK where DrawRotatedText will error if you give it an empty string.
                        y = rect.y if rotation == 0 else rect.y + rect.height
                        dc.DrawRotatedText(text,rect.x,y, rotation)  
                
    def _draw_text_on_axis(self, dc, range, interval, format, font, horizontal, text_colour, tick_length, get_text_rect_function):
        value_and_text_list = self.create_value_text_tuple_list(range, interval, format)
        self._draw_manual_text_on_axis(dc, value_and_text_list, font, horizontal, text_colour, tick_length, get_text_rect_function)

    def draw_axis(self, dc, axis, line_style, force_axis_to_bottom = False):
        """Draws the x axis using the given GraphLineStyle.
        In the event of x axis being drawn mid display (at zero) you can specify
        to draw it at the bottom by setting force_x_axis_to_bottom
        
        'line_style' is a GraphLineStyle() which consists of...
        line_colour : (r,g,b)
        pen_width   : Note: that with some wx_pensytles the pen will always be 1 regardless of what you set.
        wx_penstyle : wx.SOLID, wx.DOT, wx.DOT_DASH etc..
        
        example of use...
        graph = DrawGraph()
        graph._draw_rect = rect
        graph.x_range = GraphRange(xmin, xmax)
        line_colour = (r,g,b)
        line_width = 1
        line_style = wx.SOLID
        axis_line = GraphLineStyle(line_colour, line_width, line_style)
        graph.draw_axis(dc, GraphAxis.X, axis_line)
        """
        if axis == GraphAxis.X:
            self._draw_axis(dc, self._draw_rect.y1 if force_axis_to_bottom or self._is_x_axis_at_bottom() else self.y_zero, line_style, self._draw_grid_y_line)
        else:
            self._draw_axis(dc, self._draw_rect.x if force_axis_to_bottom or self._is_y_axis_at_side() else self.x_zero, line_style, self._draw_grid_x_line)
                        
 
    def draw_grid(self, dc, axis, interval, line_style):
        """Draws a regular grid along the x axis using the given GraphLineStyle.
        The grid will be drawn at regular intervals of x_interval.
        
        'line_style' is a GraphLineStyle() which consists of...
        line_colour : (r,g,b)
        pen_width   : Note: that with some wx_pensytles the pen will always be 1 regardless of what you set.
        wx_penstyle : wx.SOLID, wx.DOT, wx.DOT_DASH etc..
        
        example of use...
        graph = DrawGraph()
        graph._draw_rect = rect
        graph.x_range = GraphRange(xmin, xmax)
        line_colour = (r,g,b)
        line_width = 1
        line_style = wx.SOLID
        grid_line = GraphLineStyle(line_colour, line_width, line_style)
        graph.draw_grid(dc, GraphAxis.X, interval, grid_line)
        """
        if axis == GraphAxis.X:
            self._draw_grid(dc, self.x_range, interval, line_style, self.value_to_screen_x, self._draw_grid_x_line)
        else:
            self._draw_grid(dc, self.y_range, interval, line_style, self.value_to_screen_y, self._draw_grid_y_line)


    def draw_grid_manual(self, dc, axis, value_list, line_style):
        """Draws a grid the x axis using the given GraphLineStyle.
        The grid will be drawn at the given intervals defined in the value_list.

        The value_list can be a straight list of values or it can be a list of 
        tuples where the first value of each tuple is the value.
        This is useful if you have a tuple list like this...
        value_list = [(1.0, "start"), (2.0, "mid"), (3.0, "end")]
        This means you can pass the same list to...
            draw_grid_x_manual
            draw_grid_y_manual
            draw_tick_x_manual
            draw_tick_y_manual
            draw_tick_x_text_manual
            draw_tick_y_text_manual

        'line_style' is a GraphLineStyle() which consists of...
        line_colour : (r,g,b)
        pen_width   : Note: that with some wx_pensytles the pen will always be 1 regardless of what you set.
        wx_penstyle : wx.SOLID, wx.DOT, wx.DOT_DASH etc..

        example of use...
        graph = DrawGraph()
        graph._draw_rect = rect
        graph.x_range = GraphRange(xmin, xmax)
        line_colour = (r,g,b)
        line_width = 1
        line_style = wx.SOLID
        grid_line = GraphLineStyle(line_colour, line_width, line_style)
        interval_list = [3.1, 4.6, 7.9]
        graph.draw_grid_manual(dc, GraphAxis.X, interval_list, grid_line)
        """
        if axis == GraphAxis.X:
            self._draw_grid_manual(dc, value_list, line_style, self.value_to_screen_x, self._draw_grid_x_line)
        else:
            self._draw_grid_manual(dc, value_list, line_style, self.value_to_screen_y, self._draw_grid_y_line)
        
        
    def draw_tick(self, dc, axis, interval, line_style, tick_length = 4):
        """Draws a regular tick along the x axis using the given GraphLineStyle.
        The grid will be drawn at regular intervals of x_interval with a length
        of tick_length.
        
        'line_style' is a GraphLineStyle() which consists of...
        line_colour : (r,g,b)
        pen_width   : Note: that with some wx_pensytles the pen will always be 1 regardless of what you set.
        wx_penstyle : wx.SOLID, wx.DOT, wx.DOT_DASH etc..
                
        example of use...
        graph = DrawGraph()
        graph._draw_rect = rect
        graph.x_range = GraphRange(xmin, xmax)
        line_colour = (r,g,b)
        line_width = 1
        line_style = wx.SOLID
        tick_line = GraphLineStyle(line_colour, line_width, line_style)
        graph.draw_tick(dc, GraphAxis.X, interval, tick_line, line_length)
        """
        self.tick_height = tick_length
        if axis == GraphAxis.X:
            self._draw_grid(dc, self.x_range, interval, line_style, self.value_to_screen_x, self._draw_tick_x_line)
        else:
            self._draw_grid(dc, self.y_range, interval, line_style, self.value_to_screen_y, self._draw_tick_y_line)


    def draw_tick_manual(self, dc, axis, value_list, line_style, tick_length = 4):
        """Draws a tick along the x axis using the given GraphLineStyle.
        The grid will be drawn at the given intervals defined in the value_list
        with a length of tick_length.
        
        The value_list can be a straight list of values or it can be a list of 
        tuples where the first value of each tuple is the value.
        This is useful if you have a tuple list like this...
        value_list = [(1.0, "start"), (2.0, "mid"), (3.0, "end")]
        This means you can pass the same list to...
            draw_grid_x_manual
            draw_grid_y_manual
            draw_tick_x_manual
            draw_tick_y_manual
            draw_tick_x_text_manual
            draw_tick_y_text_manual
        
        'line_style' is a GraphLineStyle() which consists of...
        line_colour : (r,g,b)
        pen_width   : Note: that with some wx_pensytles the pen will always be 1 regardless of what you set.
        wx_penstyle : wx.SOLID, wx.DOT, wx.DOT_DASH etc..

        example of use...
        graph = DrawGraph()
        graph._draw_rect = rect
        graph.x_range = GraphRange(xmin, xmax)
        line_colour = (r,g,b)
        line_width = 1
        line_style = wx.SOLID
        tick_line = GraphLineStyle(line_colour, line_width, line_style)
        graph.draw_tick_manual(dc, GraphAxis.X, interval, tick_line, line_length)
        """
        self.tick_height = tick_length
        if axis == GraphAxis.X:
            self._draw_grid_manual(dc, value_list, line_style, self.value_to_screen_x, self._draw_tick_x_line)
        else:
            self._draw_grid_manual(dc, value_list, line_style, self.value_to_screen_y, self._draw_tick_y_line)
        
        
        
    def draw_tick_text(self, dc, axis, interval, format, font, horizontal, text_colour = wx.BLACK, tick_length = 4):
        """Draws values represented on the x axis in the given text format\font\colour.
        The text will be drawn centralised to the regular interval specified by x_interval.
        The text can be drawn horizontal or vertical.
        If you have drawn ticks then please specify the tick length so the text 
        can be place at the correct distance from the axis.
        
        example of use...
        graph = DrawGraph()
        graph._draw_rect = rect
        graph.x_range = GraphRange(xmin, xmax)
        font = wx.Font(7, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial")
        text_colour = (r,g,b)
        horizontal = True
        graph.draw_tick_text(dc, interval, "%+02.2f", font, horizontal, text_colour, tick_line_length)
        """
        text_rect_fn = self._get_x_text_rect if axis == GraphAxis.X else self._get_y_text_rect
        axis_range = self.x_range if axis == GraphAxis.X else self.y_range
        self._draw_text_on_axis(dc, axis_range, interval, format, font, horizontal, text_colour, tick_length, text_rect_fn)


    def draw_tick_text_manual(self, dc, axis, value_and_text_list, font, horizontal, text_colour = wx.BLACK, tick_length = 4):
        """Draws text along the x axis in the given text format\font\colour.
        The values and text accociated with those values are passed in as a list
        of (value, text) tuples.
        e.g
        value_and_text_list = [(1.0, "start"), (2.0, "mid"), (3.0, "end")]
        
        The text will be drawn centralised to the regular interval specified by x_interval.
        The text can be drawn horizontal or vertical.
        If you have drawn ticks then please specify the tick length so the text 
        can be place at the correct distance from the axis.
                
        example of use...
        graph = DrawGraph()
        graph._draw_rect = rect
        graph.x_range = GraphRange(xmin, xmax)
        font = wx.Font(7, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial")
        text_colour = (r,g,b)
        horizontal = True
        graph.draw_tick_text_manual(dc, GraphAxis.X, value_and_text_list, font, horizontal, text_colour, tick_line_length)
        """
        text_rect_fn = self._get_x_text_rect if axis == GraphAxis.X else self._get_y_text_rect
        self._draw_manual_text_on_axis(dc, value_and_text_list, font, horizontal, text_colour, tick_length, text_rect_fn)

        
    def draw_line_graph(self, dc, coords, line_style = GraphLineStyle()):
        """Draws a line graph from the given coords using the specified line.
        The coordinates are a list of GraphCoOrd's in the format (x,y).
        
        'line_style' is a GraphLineStyle() which consists of...
        line_colour : (r,g,b)
        pen_width   : Note: that with some wx_pensytles the pen will always be 1 regardless of what you set.
        wx_penstyle : wx.SOLID, wx.DOT, wx.DOT_DASH etc..
        
        example of use...
        graph = DrawGraph()
        graph._draw_rect = rect
        graph.x_range = GraphRange(-360, 360)
        graph.y_range = GraphRange(-1.0, 1.0)        
        number_of_points = 100
        XTickInterval = graph.x_range.range / number_of_points
        x = graph.x_range.min
        coords = []
        y = math.sin(math.radians(x))
        for i in range(number_of_points):
            coords.append(GraphCoOrd(x,y)) 
            x+= XTickInterval
            y= math.sin(math.radians(x))
        coords.append(GraphCoOrd(x,y))    
        line = GraphLineStyle((255,0,0))
        graph.draw_line_graph(dc, coords, line)        
        """
        self._draw_line_from_coords(dc, coords, line_style, self._draw_line_graph_from_coords)

    def draw_crosses(self, dc, coords, line_style = GraphLineStyle(), width = 4):  
        """Draws a cross 'X' at the specified coordinates using the line style.
        The size of the X is defined by the width.
        A line is drawn from x-width, y-width to x+width y+width and from
        x+width, y-width to x-width y+width.
        
        'line_style' is a GraphLineStyle() which consists of...
        line_colour : (r,g,b)
        pen_width   : Note: that with some wx_pensytles the pen will always be 1 regardless of what you set.
        wx_penstyle : wx.SOLID, wx.DOT, wx.DOT_DASH etc..
        
        example of use...
        graph = DrawGraph()
        graph._draw_rect = rect
        graph.x_range = GraphRange(-360, 360)
        graph.y_range = GraphRange(-1.0, 1.0)        
        number_of_points = 100
        XTickInterval = graph.x_range.range / number_of_points
        x = graph.x_range.min
        coords = []
        y = math.sin(math.radians(x))
        for i in range(number_of_points):
            coords.append(GraphCoOrd(x,y)) 
            x+= XTickInterval
            y= math.sin(math.radians(x))
        coords.append(GraphCoOrd(x,y))    
        line = GraphLineStyle((255,0,0))
        graph.draw_crosses(dc, coords, line, 5)
        """
        self.cross_width = width    
        self._draw_line_from_coords(dc, coords, line_style, self._draw_crosses_at_coords)

    def draw_bar_graph(self, dc, start, interval, value_list, bar_style = GraphBarStyle()):
        """Draws a bar graph from the given points in the given bar sytle .        
        The value_list is a straight list of values (not coords).
        It will draw a bar for each value entry in the list.
        The bars will be drawn from a start value and the bar width is determined
        by the regular interval.
        
        The bar_sytle consists of...
        bar_colour          : rgb colour
        wx_bar_brush_style  : wx.SOLID, wx.CROSSDIAG_HATCH etc.
        line_style          : GraphLineStyle()
        draw_outline        : set True to draw an outline rect
        draw_solid_bar      : set True to draw a solid bar
        
        'line_style' is a GraphLineStyle() which consists of...
        line_colour : (r,g,b)
        pen_width   : Note: that with some wx_pensytles the pen will always be 1 regardless of what you set.
        wx_penstyle : wx.SOLID, wx.DOT, wx.DOT_DASH etc..

        Note: You can draw a solid bar with an outline, just the bar or just the outline.

        graph = DrawGraph()
        graph._draw_rect = rect
        graph.y_range = GraphRange(0, 100)
        graph.x_range = GraphRange(0, 10)
        draw_solid_bar = True
        draw_x_orientated_graph = True
        draw_outline = True
        bar = GraphBarStyle((0,0,255), wx.CROSSDIAG_HATCH, draw_solid_bar, draw_x_orientated_graph, draw_outline, GraphLineStyle((255,255,0)))
        value_list = range(10,110,10)
        graph.draw_bar_graph(dc, GraphAxis.X, 0, 1, value_list, bar)
        """
        self._draw_bar_graph(dc, start, interval, value_list, bar_style, self._create_x_bar_rect if bar_style.x_orientation else self._create_y_bar_rect)
     
    def value_to_screen_x(self, value):
        """Converts an x axis value to a screen position on the graph.
        This is the opposite operation of screen_to_value_x.
        This purposely does not do any range checking as it is perfectly valid to
        draw to a point beyond the graph even though the draw area is clipped.
        e.g. plotting math.tan(90).
        """
        return _validate_coord(self.x_zero + _scaler(float(value), self.x_factor))
            
    def value_to_screen_y(self, value):
        """Converts an y axis value to a screen position on the graph.
        This is the opposite operation of screen_to_value_y.        
        This purposely does not do any range checking as it is perfectly valid to
        draw to a point beyond the graph even though the draw area is clipped.
        e.g. plotting math.tan(90).
        """
        return _validate_coord(self.y_zero - _scaler(float(value), self.y_factor))
            
    def screen_to_value_x(self, x):
        """Converts screen position on the graph to an x axis value.
        This is the opposite operation of value_to_screen_x.
        If the x is out of the graphs rect then a ValueError exception is raised.
        """
        x = int(x)
        if x >= self._draw_rect.x and x <= self._draw_rect.x1:
            return _un_scaler(x, self.x_factor)
        else:
            raise ValueError("x coord %d is out of the drawing area %d to %d" % (x, self._draw_rect.x, self._draw_rect.x1 ))
            
    def screen_to_value_y(self, y):
        """Converts screen position on the graph to a y axis value.
        This is the opposite operation of value_to_screen_y.
        If the y is out of the graphs rect then a ValueError exception is raised.
        """
        y = int(y)
        if y >= self._draw_rect.y and y <= self._draw_rect.y1:
            return _un_scaler(y, self.y_factor)
        else:
            raise ValueError("y coord %d is out of the drawing area %d to %d" % (y, self._draw_rect.y, self._draw_rect.y1 ))
        
    def create_value_text_tuple_list(self, range, interval, format):
        """Returns a list of tuples of (values, text) given a range.
        The values are calculated by stepping by an interval through a range.
        The text is the value formatted into a string using the expression::
        
         ticks = [format % (v,) for v in xrange(range[0], range[1], interval)]
         
        .. note :: Whilst the fragment here shows xrange, in fact a different 
                   function is used which is more friendly to float.
        """
        interval_list = self._get_list_of_intervals(range, interval)
        return [self._create_val_text_tuple(value, format) for value in interval_list]
    
    def create_x_text_out_list(self, dc, value_and_text_list, font, horizontal, tick_length):
        """Given a value_text tuple list this will produce a rect_text_rotaion tuple list
        Pass in a list of (x_Values, Text) tuples along with the font,
        text orientation and tick_length and for each entry the function will 
        generate a tuple containing the (texts occupying rect, the text, 
        rotation in degrees).
        The tick_length in this case is the distance the text is from the axis.
        """
        return self._create_text_out_list(dc, value_and_text_list, font, horizontal, tick_length, self._get_x_text_rect)

    def create_y_text_out_list(self, dc, value_and_text_list, font, horizontal, tick_length):
        """Given a value_text tuple list this will produce a rect_text_rotaion tuple list
        Pass in a list of (y_Values,Text) tuples along with the font,
        text orientation and tick_length and for each entry the function will 
        generate a tuple containing the (texts occupying rect, the text, 
        rotation in degrees).
        The tick_length in this case is the distance the text is from the axis.
        """
        return self._create_text_out_list(dc, value_and_text_list, font, horizontal, tick_length, self._get_y_text_rect)
    
    def create_screen_coords_from_value_coords(self, value_coords):
        """This will take a list of GraphCoord(x_value,y_value) and return a list of screen wx.Point(x,y) coords.
        """
        return [self._scale_coord(value_coord) for value_coord in value_coords]

    def create_x_bar_graph_rect_list(self, start_x, x_interval, values):
        """This will take a list of GraphCoord(x_value,y_value) and return a list of screen wx.Point(x,y) coords.
        """
        return self._create_bar_graph_rect_list(start_x, x_interval, values, self._create_x_bar_rect)    

    def create_y_bar_graph_rect_list(self, start_y, y_interval, values):
        """This will take a list of GraphCoord(x_value,y_value) and return a list of screen wx.Point(x,y) coords.
        """
        return self._create_bar_graph_rect_list(start_y, y_interval, values, self._create_y_bar_rect)
                
    def plugin_xrange_object(self, range_obj):
        """This enables you to plugin your own x range object.
        If you plugin in your own range object then when the range is modified
        you must manually call the signal_x_range_change() function.
        
        Parameters...
        range_obj : Can be any object that has the following properties...
                    @property
                    def min(self):
                        return self._range_min

                    @property
                    def max(self):
                        return self._range_max
                                
                    @property
                    def range(self):
                        return self._range_max - self._range_min
        
        e.g. of use from the draw_graph_controller object...
        self.graph  = DrawGraph()
        # The GraphAxisInfo object has the required property signature and you will
        # see The signal_x_range_change function is passed into this object so
        # when the range is modified then the graph object can be signalled. 
        self.x_axis = GraphAxisInfo(GraphAxis.X, self.graph.signal_x_range_change) 
        self.y_axis = GraphAxisInfo(GraphAxis.Y, self.graph.signal_y_range_change)
        self.graph.plugin_xrange_object(self.x_axis)
        self.graph.plugin_yrange_object(self.y_axis)
        """
        self._x_range = range_obj
        
    def plugin_yrange_object(self, range_obj):
        """This enables you to plugin your own y range object.
        If you plugin in your own range object then when the range is modified
        you must manually call the signal_y_range_change() function.
        
        Parameters...
        range_obj : Can be any object that has the following properties...
                    @property
                    def min(self):
                        return self._range_min

                    @property
                    def max(self):
                        return self._range_max
                                
                    @property
                    def range(self):
                        return self._range_max - self._range_min
        
        e.g. of use from the draw_graph_controller object...
        self.graph  = DrawGraph()
        # The GraphAxisInfo object has the required property signature and you will
        # see The signal_y_range_change function is passed into this object so
        # when the range is modified then the graph object can be signalled. 
        self.x_axis = GraphAxisInfo(GraphAxis.X, self.graph.signal_x_range_change) 
        self.y_axis = GraphAxisInfo(GraphAxis.Y, self.graph.signal_y_range_change)
        self.graph.plugin_xrange_object(self.x_axis)
        self.graph.plugin_yrange_object(self.y_axis)
        """
        self._y_range = range_obj

    def signal_x_range_change(self):
        """This signals to the DrawGraph object that the x range has been 
        externally modified.
        
        This is for use with the plugin_xrange_object() function.
        """
        self._calculate_x_factors()
        self._set_draw_rect()
        
    def signal_y_range_change(self):
        """This signals to the DrawGraph object that the y range has been 
        externally modified.

        This is for use with the plugin_xrange_object() function.
        """
        self._calculate_y_factors()
        self._set_draw_rect()

if __name__ == "__main__":
    test.main()
