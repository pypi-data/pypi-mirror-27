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

from .draw_graph import *
from imgtec.lib.namedenum import namedenum

TextJustify = namedenum("TextJustify", "LEFT", "CENTRE", "RIGHT")
Side = namedenum("Side", "LEFT", "TOP", "RIGHT", "BOTTOM")


def get_default_font():
    return wx.Font(7,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName = "Arial")

class _TitleText(object):
    def __init__(self, text, font, colour, horizontal, below_axis, distance_from_axis, justification):
        self._text               = text                 # text string
        self._font               = font                 # a wx.font
        self._colour             = colour               # RGB tuple
        self._horizontal         = horizontal           # text orientation
        self._below_axis         = below_axis           # draw it below the axis or above the graph
        self._distance_from_axis = distance_from_axis   #
        self._justification      = justification        #  an TextJustify  Enum : TextJustify.LEFT,   TextJustify.CENTRE, or TextJustify.RIGHT

    @property
    def text(self):
        return self._text
        
    @property
    def font(self):
        return self._font

    @property
    def colour(self):
        return self._colour
        
    @property
    def horizontal(self):
        return self._horizontal
        
    @property
    def below_axis(self):
        return self._below_axis

    @property
    def distance_from_axis(self):
        return self._distance_from_axis
        
    @property
    def justification(self):
        return self._justification       

class _LineInfo(object):
    """This is an immutable Title Text container class.
    """
    def __init__(self, coords, line_style):
        self._coords = coords     # List of GraphCoords(x,y)
        self._line   = line_style # GraphLineStyle object
        
    @property
    def coords(self):
        return self._coords

    @property
    def line(self):
        return self._line
        
class _CrossesInfo(object):        
    def __init__(self, line_graph, cross_size):
        self._line_graph = line_graph # a _LineInfo object
        self._cross_size = cross_size # size of the cross

    @property
    def line_graph(self):
        return self._line_graph
        
    @property
    def cross_size(self):
        return self._cross_size

class _BarInfo(object):
    def __init__(self, start, interval, values, bar):
        self._start    = start    # x start value
        self._interval = interval # x interval per bar
        self._values   = values   # list of y values to plot
        self._bar      = bar      # GraphBarStyle object

    @property
    def start(self):
        return self._start

    @property
    def interval(self):
        return self._interval
        
    @property
    def values(self):
        return self._values
        
    @property
    def bar(self):
        return self._bar
        


class _Marker(object):
    def __init__(self, value, text,  font, horizontal, text_colour, line_style, distance_from_axis):
        self.graph_text  = _TitleText(text, font, text_colour, horizontal, None, distance_from_axis, None)
        self.line        = line_style  # GraphLineStyle object
        self.value       = value # value where to place the marker
        

class GraphAxisInfo(object):
    """
    Axis info contains information to describe and axis.
    
    This is used by the following objects
        * :class:`~imgtec.lib.wx_extensions.DrawGraphController`
        * :class:`~imgtec.lib.wx_extensions.GraphControl`
    
    """
    
    def __init__(self, axis_type, calculate_factors_fn):
        self.axis_type                    = axis_type
        self._range_min                   = 0.0
        self._range_max                   = 0.0
        self._calculate_factors_fn        = calculate_factors_fn
        self.title_text                   = None  # _TitleText object
        self.axis_line                    = None  # GraphLineStyle object
        self.force_axis_to_edge           = False
        self.tick_line                    = None  # GraphLineStyle object
        self.tick_line_len                = None
        self.tick_text_horizontal         = None
        self.tick_text_colour             = None
        self.tick_text_distance_from_axis = None
        self.tick_text_font               = None 
        self.grid_line                    = None  # GraphLineStyle object
            
        # Auto        
        self.grid_interval                = None
        self.tick_interval                = None
        self.tick_text_interval           = None
        self.tick_text_format             = None
        
        #Manual
        # Note: the tick_text_list is a list of tuples of (value, text) and the other lists are just values.
        # However the graphing library will accept a list of tuples for grid_values & tick values - as long as the first entry in the tuple is the value.
        # This enables you to create one list of (value,text) tuples and set that to any of the lists below.
        self.tick_text_value_list         = None  # list of tuples (value, text)
        self.grid_value_list              = None  # list of values to graw a grid
        self.tick_value_list              = None  # list of values to draw a tick
        self.marker_list                  = []    # list of markers to add the the graph or lollypops if you wish to get technical
        
    @property
    def min(self):
        return self._range_min

    @property
    def max(self):
        return self._range_max
                
    @property
    def range(self):
        return self._range_max - self._range_min
        
    def set_range(self, min, max):
        """Set the min and max range for what the axis represents.
        
        :param min: Minimum value of what the axis represents
        :param max: Maximum value of what the axis represents
        
        :return: None
        
        The values can be any floating point number.
        
        """
        self._range_min = float(min)
        self._range_max = float(max)
        if(self._range_min > self._range_max):
            self._range_min, self._range_max = self._range_max, self._range_min    
        self._calculate_factors_fn()


    def set_draw_line(self, line_style = GraphLineStyle(), force_axis_to_edge = False):
        """set_draw_line([line_style = GraphLineStyle()] , [force_axis_to_edge = False])
        
        This function is a request to draw an axis line in the specified line style.
        
        :param line_style:           This is a :class:`~imgtec.lib.wx_extensions.GraphLineStyle` object.  Default is GraphLineStyle().
        :param force_axis_to_bottom: By default if zero on an axis is shown 
                                     within the graph then the axis line will
                                     draw at the zero point. If you wish to 
                                     always display the axis at the bottom or 
                                     right then set this to True.
                                     
                                     Default is False.
                                    
        :return: None                                     
        """
        self.axis_line = line_style
        self.force_axis_to_edge = force_axis_to_edge

    def set_draw_tick(self, interval, line_style = GraphLineStyle(), tick_line_len = 4):
        """set_draw_tick(interval, [line_style = GraphLineStyle()], [, tick_line_len = 4])
        
        This defines the 'tick' along the specified axis.
        The 'tick' refers to the markers along the axis.::
        
            e.g. |---|---|---|---|---|---|
        
        The tick positions will be drawn at every interval starting from the min
        value in the axis range.
        
        :param interval:      This is the regular interval to draw the tick. 
        
                              .. note:: This is a value of what the axis represents
                                        and not pixels.
                                        
        :param line_style:    This is a :class:`~imgtec.lib.wx_extensions.GraphLineStyle` object. Default is GraphLineStyle().
        :param tick_line_len: The pixel length of each tick. Default is 4.
        
        :return: None
        """
        self.tick_line     = line_style
        self.tick_interval = interval
        self.tick_line_len = tick_line_len
        
    def set_draw_tick_manual(self, value_list, line_style = GraphLineStyle(), tick_line_len = 4):
        """set_draw_tick_manual(value_list, [line_style = GraphLineStyle()] , [tick_line_len = 4])
        
        This defines the 'tick' along the specified axis.
        The 'tick' refers to the markers along the axis.::
        
            e.g. |---|---|---|---|---|---|
        
        The tick positions will be drawn at every value specified in the value_list. 
        The values specified in the value list can be in any order.
        
        
        :param value_list:    This is a list of values where to draw ticks.
        
                              .. note:: These are values of what the axis represents
                                        and not pixels.
                              
                              .. note:: Also note that this function will accept a tuple list as
                                  long as the value is the first entry in the tuple. This
                                  is useful if you have one list of (values,text) tuples
                                  that can be passed to the following functions.
                                  
                                  * :meth:`set_draw_tick_manual`                        
                                  * :meth:`set_draw_grid_manual`
                                  * :meth:`set_draw_tick_text_manual`
                                  
        :param line_style:    This is a :class:`~imgtec.lib.wx_extensions.GraphLineStyle` object. Default is GraphLineStyle().
        :param tick_line_len: The pixel length of each tick. Default is 4.

        :return: None
        """
        self.tick_line       = line_style
        self.tick_value_list = value_list
        self.tick_line_len   = tick_line_len
            
    def set_draw_grid(self, interval, line_style = GraphLineStyle()):
        """set_draw_grid(interval, [line_style = GraphLineStyle()])
        
        This will draw a regular grid line perpendicular to the specified axis.
        The grid lines will be drawn the full len/width of the graph area, using
        the line style.

        :param interval:   This is the regular interval to draw the grid lines.
        
                           .. note:: This is a value of what the axis represents and
                                     not pixels.

        :param line_style: This is a :class:`~imgtec.lib.wx_extensions.GraphLineStyle` object. Default is GraphLineStyle().
        :return: None
        """
        self.grid_line     = line_style
        self.grid_interval = interval

    def set_draw_grid_manual(self, value_list, line_style = GraphLineStyle()):
        """set_draw_grid_manual(value_list, [line_style = GraphLineStyle()])
        
        This will draw a regular grid line perpendicular to the specified axis.
        The grid lines will be drawn at every value specified in the value_list. 
        The values specified in the value list can be in any order.

        :param value_list: This is a list of values where to grid lines. 
        
                           .. note:: These are values of what the axis represents
                               and not pixels.
                              
                               Also note that this function will accept a tuple list as
                               long as the value is the first entry in the tuple. This
                               is useful if you have one list of (values,text) tuples
                               that can be passed to the following functions.
                              
                               * :meth:`set_draw_tick_manual`                        
                               * :meth:`set_draw_grid_manual`
                               * :meth:`set_draw_tick_text_manual`

        :param line_style: This is a :class:`~imgtec.lib.wx_extensions.GraphLineStyle` object. Default is GraphLineStyle().
        :return: None
        """
        self.grid_line       = line_style
        self.grid_value_list = value_list

    def set_draw_tick_text(self, interval, format, font=None, horizontal_text = True, colour = (0,0,0), distance_from_axis = 5):
        """set_draw_tick_text(interval, format, [font = Font(7, faceName="Arial")], [horizontal_text = True], [colour = (0,0,0)] , [distance_from_axis = 5])
        
        This will draw text of what the axis represents at regular intervals.
        The text will be drawn at every interval starting from the min value in
        the specified format, font, orientation, colour and distance from the axis.
        
        :param interval:           This is the regular interval to draw the text. 
        
                                   .. note:: This is a value of what the axis 
                                             represents and not pixels.
        :param format:             This is regular python format string. e.g. 
            
                                   "-%0.02f Deg"
                                    
        :param font:               A :class:`~imgtec.lib.wx_extensions.Font` object. Default is Font(7, faceName="Arial")
        :param horizontal_text:    True = horizontal orientation, 
                                   False = vertical orientation
                                   Default is True.
        :param colour:             A (Red, Green, Blue) tuple. Default is (0,0,0).
        :param distance_from_axis: This is the distance in pixels from the 
                                   specified axis to draw the text. Default is 5.
        :return: None
        """
        self.tick_text_interval           = interval
        self.tick_text_format             = format
        self.tick_text_font               = font or get_default_font()
        self.tick_text_horizontal         = horizontal_text
        self.tick_text_colour             = colour
        self.tick_text_distance_from_axis = distance_from_axis

    def set_draw_tick_text_manual(self, value_text_tuple_list, font=None, horizontal_text = True, colour = (0,0,0), distance_from_axis = 5):
        """set_draw_tick_text_manual(value_text_tuple_list, [font = Font(7, faceName="Arial")], [horizontal_text = True], [colour = (0,0,0)] , [distance_from_axis = 5])
        
        This will draw text of what the axis represents at specified positions.
        The text in the value_text_tuple_list will be drawn at it accompanying
        value in the specified font, orientation, colour and distance from the axis.
        
        :param value_text_tuple_list: This is a list of (value,text) tuples.
        
                                      .. note:: The values are what the axis 
                                                represents and not pixels.
                                
        :param font:                  A :class:`~imgtec.lib.wx_extensions.Font` object. Default = Font(7, faceName="Arial").
        :param horizontal_text:       True = horizontal orientation, 
                                      False = vertical orientation. Default is True.
        :param colour:                A (Red, Green, Blue) tuple. Default is (0,0,0)
        :param distance_from_axis:    This is the distance in pixels from the 
                                      specified axis to draw the text. Default is 5
        :return: None
        """
        self.tick_text_value_list         = value_text_tuple_list
        self.tick_text_font               = font or get_default_font()
        self.tick_text_horizontal         = horizontal_text
        self.tick_text_colour             = colour
        self.tick_text_distance_from_axis = distance_from_axis

    def set_title(self, text, font=None, colour = (0,0,0), distance_from_axis = 20, justification = TextJustify.CENTRE):     
        """set_title(text, font = Font(7, faceName="Arial"), colour = (0,0,0), [distance_from_axis = 20], [justification = TextJustify.CENTRE])
        
        This will set a title for the specified axis.
        The title will be displayed below the axis in the style and position specified.
        
        :param text:               This is the text string to display
        :param font:               A :class:`~imgtec.lib.wx_extensions.Font` object. Default is Font(7, faceName="Arial")
        :param colour:             A (Red, Green, Blue) tuple. Default is (0,0,0)
        :param distance_from_axis: This is the distance in pixels from the 
                                   specified axis to draw the title. Default = 20
        :param justification:      TextJustify.LEFT, TextJustify.CENTRE, TextJustify.RIGHT. Default = TextJustify.CENTRE.
        :return: None
        """
        self.title_text = _TitleText(text, font or get_default_font(), colour, self.axis_type == GraphAxis.X, True, distance_from_axis, justification)

    def add_marker(self, value, text, font=None, horizontal_text = True, text_colour = (0,0,0), line_style = GraphLineStyle(), distance_from_axis = 30):
        """add_marker(value, text, font = Font(7, faceName="Arial"), [horizontal_text = True], [text_colour = (0,0,0)], [line_style = GraphLineStyle()] , [distance_from_axis = 30])
        
        This will add a marker at the specified position.
        A marker consists of a line that spans the full width or height and then
        beyond the graph area to some text.
        The line will be drawn in the specified line style and the text in the
        specified font, orientation and colour
        
        :param value:              The axis value where to display the marker.
        
                                   .. note:: This is a value of what the axis 
                                             represents and not pixels.
        :param text:               This is the text string to display
        :param font:               A :class:`~imgtec.lib.wx_extensions.Font` object. Default is Font(7, faceName="Arial").
        :param horizontal_text:    True = horizontal orientation, 
                                   False = vertical orientation. Default is True.
        :param text_colour:        A (Red, Green, Blue) tuple. Default is (0,0,0).
        :param line_style:         This is a :class:`~imgtec.lib.wx_extensions.GraphLineStyle` object. Default is GraphLineStyle().
        :param distance_from_axis: This is the distance in pixels from the 
                                   specified axis to draw the text. Default = 30
        :return: None
        """
        self.marker_list.append(_Marker(value, text, font or get_default_font(), horizontal_text, text_colour, line_style, distance_from_axis))
    
    def clear_markers(self):
        """clear_markers()
        
        This function will clear the marker list.
        
        :return: None
        """
        self.marker_list = []  


def _calc_text_point_from_justify(x, x1, text_width, justify):
    if justify == TextJustify.RIGHT:
        return x1 - text_width
    elif justify == TextJustify.CENTRE:    
        total_width = x1 - x
        return x + (total_width / 2) - (text_width / 2)
    else:
        return x

def _get_text_points(axis_y, text_height, below_axis, distance_from_axis):
    if below_axis:
        y = axis_y + distance_from_axis
        y1 = y + text_height
    else:
        y1 = axis_y - distance_from_axis
        y = y1 - text_height
    return (y,y1)

def _get_text_points_horz(axis_y, text_height, below_axis, distance_from_axis):
    return _get_text_points(axis_y, text_height, below_axis, distance_from_axis)

def _get_text_points_vert(axis_x, text_height, below_axis, distance_from_axis):
    return _get_text_points(axis_x, text_height, not below_axis, distance_from_axis)

def _get_text_rect(dc, graph_rect, side, horizontal, font, below_axis, distance_from_axis, justification, text):
    with set_font(dc, font):
        (text_width, text_height) = dc.GetTextExtent(text)
        if side == Side.LEFT or side == Side.RIGHT:
            if horizontal:
                (text_width, text_height) = (text_height, text_width)
            (x, x1) = _get_text_points_vert(graph_rect.x if side == Side.LEFT else graph_rect.x1, text_height, below_axis, distance_from_axis)
            y = _calc_text_point_from_justify(graph_rect.y, graph_rect.y1, text_width, justification)
            y1 = y + text_width
        else:
            if not horizontal:
                (text_width, text_height) = (text_height, text_width)
            (y, y1) = _get_text_points_horz(graph_rect.y if side == Side.TOP else graph_rect.y1, text_height, below_axis, distance_from_axis)
            x = _calc_text_point_from_justify(graph_rect.x, graph_rect.x1, text_width, justification)
            x1 = x + text_width
        return Rectx1y1(x,y,x1,y1)    
    return Rect()
    

def _draw_text(dc, text_rect, horizontal, font, colour, graph_text):
    if graph_text != "": # This is necessary because there is a bug in wxPythonGTK where DrawRotatedText will error if you give it an empty string.
        with set_font(dc, font):
            with wx.DCTextColourChanger(dc, colour):
                if horizontal:
                    dc.DrawText(graph_text, text_rect.x, text_rect.y)   
                else:
                    (text_width, text_height) = dc.GetTextExtent(graph_text)
                    dc.DrawRotatedText(graph_text, text_rect.x , text_rect.y + text_width , 90 ) # adjust x & y for the rotation


def get_side_from_title_text(title_text):
    if title_text.horizontal:
        if title_text.below_axis:
            side = Side.BOTTOM
        else:
            side = Side.TOP
    else:        
        if title_text.below_axis:
            side = Side.LEFT
        else:
            side = Side.RIGHT
    return side

def _draw_text_off_axis(dc, graph_rect, side, title_text):# horizontal_text, font, colour, below_axis, distance_from_axis, justification, text):
    _draw_text(dc, _get_text_rect(dc, graph_rect, side, title_text.horizontal, title_text.font, title_text.below_axis, title_text.distance_from_axis, title_text.justification, title_text.text), title_text.horizontal, title_text.font, title_text.colour, title_text.text)


def _draw_border(dc, rect, line_style):
    with wx.DCPenChanger(dc, wx.Pen(line_style.line_colour, line_style.line_width, line_style.pen_style)):
        with wx.DCBrushChanger(dc, wx.TRANSPARENT_BRUSH):
            dc.DrawRectangle(*(rect.xywh))



class DrawGraphController(object):
    """
    This is the helper class that :class:`~imgtec.lib.wx_extensions.GraphControl` uses to draw the graph.
    DrawGraphController can be used stand alone but we recommend using the 
    GraphControl.

    The DrawGraphController is a helper class to which allows you to describe a 
    graph and then draw it all with a single :func:`draw` function.

    The DrawGraphController has 2 rectangles; the outer rect and 
    the inner rect. The inner rect is always within the bounds of the 
    outer rect.
    
    You cannot draw beyond the specified outer rect.
    
    Graph data will not draw beyond the inner rect.
    
    The gaps between the outer rect and the inner rect contain the axis
    scales, markers and titles
    
        .. image:: examples/SimpleSineGraphRects.png
         
    The gaps between the outer rect and the inner rect are defined using
    the :func:`set_internal_borders` function.
    The default borders are (40, 30, 20, 40) - left, top, right, bottom respectively.
 
    The outer rect is initially set by the constructor but can be modified
    using the :func:`set_rect` function. 
    Modifying the outer rect will automatically apply the specified 
    borders and resize the inner rect.
 
    DrawGraphController allows you to add multiple lines, bars, crosses.

    There is a single function :func:`draw` which will draw
    the whole graph (including all the data) in one function.
    
    The DrawGraphController is designed so you only have to setup your graph once.
    You can then subsequently add data to plot, then clear that data and then add 
    new data (i.e. your data has changed).

    To clear the current data set in this controller use the :func:`clear_data`
    
    The DrawGraphController has two properties. . .
    
        * :attr:`x_axis`
        * :attr:`y_axis`
        
    These properties store the information about each axis. 
    See the example code below for how to use these properties.
    
    Here is the code for the sine wave graph (shown above)
    
    .. literalinclude:: examples/SimpleGraphControllerExample.py
    
    More examples. . .
    
    :doc:`examples/SimpleBarGraphControllerExample`
    
    :doc:`examples/SimpleYBarGraphControllerExample`
    
    
    Also see. . .
    
        * :class:`~imgtec.lib.wx_extensions.GraphControl`
    
    
    .. method:: __init__(pos, size)

        :param pos:    (x, y) tuple which defines the top left corner of the 
                       controller (in pixels).
        :param size:   (width, height) tuple which defines the width and height 
                       of the controller (in pixels).    
    """
    def __init__(self, pos, size): # using pos and size tuples to be easily interchangeable with the GraphControl constructor.
        self.graph               = DrawGraph()
        self._max_rect           = Rect(*(pos + size))
        self.set_internal_borders(40,30,20,40)
        self._x_axis             = GraphAxisInfo(GraphAxis.X, self.graph.signal_x_range_change) # pass in the signal_x_range_change so when the range changes in our external object we inform the DrawGraph object
        self._y_axis             = GraphAxisInfo(GraphAxis.Y, self.graph.signal_y_range_change) # pass in the signal_y_range_change so when the range changes in our external object we inform the DrawGraph object
        self._title_text         = None 
        self.draw_border_line    = None
        self.clear_data()
        self.graph.plugin_xrange_object(self.x_axis) # Plugin our own range object which in this case is the GraphAxisInfo object
        self.graph.plugin_yrange_object(self.y_axis) # Plugin our own range object which in this case is the GraphAxisInfo object

    @property
    def x_axis(self):
        """This is an instance of :class:`wx.GraphAxisInfo` representing the graph's X axis."""
        return self._x_axis
        
    @property
    def y_axis(self):
        """This is an instance of :class:`wx.GraphAxisInfo` representing the graph's Y axis."""
        return self._y_axis
        
    def _draw_axis_pre(self, dc, axis_info):                
        # Draw Grid
        if axis_info.grid_value_list != None:
            self.graph.draw_grid_manual(dc, axis_info.axis_type, axis_info.grid_value_list, axis_info.grid_line)
        elif axis_info.grid_line != None:
            self.graph.draw_grid(dc, axis_info.axis_type, axis_info.grid_interval, axis_info.grid_line)
                  
        # Draw ticks
        if axis_info.tick_value_list != None:            
            self.graph.draw_tick_manual(dc, axis_info.axis_type, axis_info.tick_value_list, axis_info.tick_line, axis_info.tick_line_len)
        elif axis_info.tick_line != None:
            self.graph.draw_tick(dc, axis_info.axis_type, axis_info.tick_interval, axis_info.tick_line, axis_info.tick_line_len)
        
        # Draw tick text
        if axis_info.tick_text_value_list != None:
            self.graph.draw_tick_text_manual(dc, axis_info.axis_type, axis_info.tick_text_value_list, axis_info.tick_text_font, axis_info.tick_text_horizontal, axis_info.tick_text_colour, axis_info.tick_text_distance_from_axis)
        elif axis_info.tick_text_format != None:
            self.graph.draw_tick_text(dc, axis_info.axis_type, axis_info.tick_text_interval, axis_info.tick_text_format, axis_info.tick_text_font, axis_info.tick_text_horizontal, axis_info.tick_text_colour, axis_info.tick_text_distance_from_axis)
        
        # Draw axis title
        if axis_info.title_text != None: 
            _draw_text_off_axis(dc, self.graph.graph_rect, get_side_from_title_text(axis_info.title_text), axis_info.title_text)            

    def _draw_marker(self, dc, axis_type, graph_marker):
        value_text_tuple_list = [(graph_marker.value, graph_marker.graph_text.text)]
        if graph_marker.line != None:
            self.graph.draw_grid_manual(dc, axis_type, value_text_tuple_list, graph_marker.line)
            self.graph.draw_tick_manual(dc, axis_type, value_text_tuple_list, graph_marker.line, graph_marker.graph_text.distance_from_axis -1)
        if graph_marker.graph_text.text != "":
            self.graph.draw_tick_text_manual(dc, axis_type, value_text_tuple_list, graph_marker.graph_text.font, graph_marker.graph_text.horizontal, graph_marker.graph_text.colour, graph_marker.graph_text.distance_from_axis)


    def _draw_axis_post(self, dc, axis_info):
        # Draw axis lines
        if axis_info.axis_line != None:
            self.graph.draw_axis(dc, axis_info.axis_type, axis_info.axis_line, axis_info.force_axis_to_edge)            
        # Draw markers    
        for graph_marker in axis_info.marker_list:
            self._draw_marker(dc, axis_info.axis_type, graph_marker)


    def clear_data(self):
        """clear_data()
        
        Clears all the drawing data.
        
        .. note:: This only clears the line, bar and crosses lists not any
                  of the graph setup.
                  
        :return: None
        """
        self._line_list          = []
        self._bar_list           = []
        self._crosses_list       = []

    def get_rect(self):
        """get_rect(self) -> Rect object
        
        Returns the maximum rect of the graph drawing control"""
        return self._max_rect.xywh

    def set_rect(self, x, y, width, height):
        """set_rect(x, y, width, height)
        
        This will set the maximum rect of the graph drawing control.

        This will automatically resize the inner graph area applying the internal borders.
        
        .. note:: Nothing will draw out of this area.

        :param x:      The screen x position of the graph in pixels. (x,y) defines the top left position
        :param y:      The screen y position of the graph in pixels. (x,y) defines the top left position
        :param width:  The width of the graph in pixels.
        :param height: The height of the graph in pixels.
        
        :return: None
        """
        new_rect = Rect(x, y, width, height)
        Deltas = self._max_rect.get_enclosing_deltas(self.graph.graph_rect)
        self._max_rect = new_rect
        self.graph.graph_rect = self._max_rect.expanded(*Deltas)

    def set_internal_borders(self, left_border, top_border, right_border, bottom_border):
        """set_internal_borders(left_border, top_border, right_border, bottom_border)
        
        This function will set the size of the borders between the graph control
        rect and the inner graph rect.
        
        The inner graph rect is where the actual graph is drawn.
        
        .. note:: The graph data will not draw out of this area.

        The scales and titles are drawn in the borders.
        
        The parameters define the distance from the outer graph control rect to 
        the inner graph rect.
        
        If this function is not called then the control will default to internal borders of (40, 30, 20, 40) - left, top, right, bottom respectively.
        
        :param left_border:   The left hand gap between the outer and the inner rect in pixels. 
        :param top_border:    The gap at the top between the outer and the inner rect in pixels. 
        :param right_border:  The right hand gap between the outer and the inner rect in pixels. 
        :param bottom_border: The gap at the bottom between the outer and the inner rect in pixels. 
        
        :return: None
        """
        # shrink the graph rect to be the max_rect - the borders
        new_rect = self._max_rect.shrunk(abs(left_border), abs(top_border), abs(right_border), abs(bottom_border))        
        # Make sure the _graph_rect is no bigger than the max - This can occur when the sum of the borders is actually bigger than the max_rect
        if self._max_rect.encloses(new_rect):
            self.graph.graph_rect = new_rect       
        else:    
            self.graph.graph_rect = Rect(*self._max_rect.xywh)
        
    def set_draw_border_line(self, line_style = GraphLineStyle()):
        """set_draw_border_line([line_style = GraphLineStyle()])
        
        This function will draw a border line around the Graph Control using the given line style.
        
        :param line_style: This is a :class:`~imgtec.lib.wx_extensions.GraphLineStyle` object. Default is GraphLineStyle().
        :return: None
        """
        self.draw_border_line = line_style

    def set_title(self, text, font=None, colour = (0,0,0), distance_from_graph = 5, justification = TextJustify.CENTRE):
        """set_title(text, [font = Font(7, faceName="Arial")], [colour = (0,0,0)], [distance_from_graph = 5], [justification = TextJustify.CENTRE])
        
        This will set a title for the whole graph.
        
        The title will be displayed above the graph in the style and position specified.
        
        :param text:                This is the text string to display
        :param font:                A :class:`~imgtec.lib.wx_extensions.Font` object. Default is Font(7, faceName="Arial").
        :param colour:              A (Red, Green, Blue) tuple. Default is (0,0,0)
        :param distance_from_graph: This is the vertical distance in pixels from the graph to draw the title. Default is 20
        :param justification:       TextJustify.LEFT, TextJustify.CENTRE, TextJustify.RIGHT. Default is TextJustify.CENTRE.
        :return: None
        """
        self._title_text = _TitleText(text, font or get_default_font(), colour, True, False, distance_from_graph, justification)

    def add_crosses(self, coords, line_style = GraphLineStyle(), cross_size = 4):
        """add_crosses(coords, [line_style = GraphLineStyle()], [cross_size = 4])
        
        This will draw crosses at the specified coordinates.
        
        The cross will drawn in the specified line style.
        
        You can call this function multiple times to draw multiple sets of crosses.
        
        Each set of crosses will be drawn in the order they are added i.e. first in first drawn.
        
        :param coords:     A list of (x,y) coordinate tuples.
        :param line_style: This is a :class:`~imgtec.lib.wx_extensions.GraphLineStyle` object. Default is GraphLineStyle().
        :param cross_size: The size of the cross is the horizontal distance from
                           the centre of the cross to the edge of the crosses 
                           containing rectangle.
                           
                           i.e. the cross is drawn from        
                           
                           (x - cross_size, y - cross_size) to  (x + cross_size, y + cross_size)
                        
                           and from
                            
                           (x - cross_size, y + cross_size) to  (x + cross_size, y - cross_size)
                           
                           Default is 4.

        :return: None
        """
        self._crosses_list.append(_CrossesInfo(_LineInfo(coords, line_style), cross_size))

    def add_line(self, coords, line_style = GraphLineStyle()):
        """add_line(coords, [line_style = GraphLineStyle()])
        
        This is a request to draw a line graph from the given coordinated.
        
        .. note:: The coordinate values are what the axis represent and not pixels.
        
        The line will be drawn using the given line style.
        
        You can call this function multiple times to draw multiple line graphs.
        
        Each line will be drawn in the order they are added i.e. first in first drawn.

        :param coords:     A list of (x,y) coordinate tuples. 
        :param line_style: This is a :class:`~imgtec.lib.wx_extensions.GraphLineStyle` object. Default is GraphLineStyle().
        :return: None
        """
        self._line_list.append(_LineInfo(coords, line_style))
        
    def add_bar(self, start, interval, value_list, bar_style = GraphBarStyle()):
        """add_bar(start, interval, value_list, [bar_style = GraphBarStyle()])
        
        This is a request to draw a bar graph using the given value list.
        
        .. note:: The values are what the axis represent and not pixels.
        
        The bar graph will begin the draw at the specified start and will draw
        a bar of width 'interval' for each entry in the value_list.
        
        The bar will be drawn using the bar style 
        
        You can call this function multiple times to draw multiple bar graphs.
        
        Each bar will be drawn in the order they are added i.e. first in first drawn.
        Subsequent draws will overwrite the previously drawn data.

        :param start:      A value that specifies where to start drawing the bar graph.
                           This is a graph value not a pixel.
        :param interval:   This is the regular interval to draw the bars. So this
                           equates to the bar width. This is graph value not a pixel
                           width.
        :param value_list: A list of values : i.e. the height of each bar in graph values (not pixels).
        :param bar_style:  This is a :class:`~imgtec.lib.wx_extensions.GraphBarStyle` object. Default is GraphBarStyle()
        :return: None
        """
        self._bar_list.append(_BarInfo(start, interval, value_list, bar_style))

    def draw(self, dc):
        """draw(dc)
        
        This is the single function that will draw the whole graph from the data
        you have setup in this controller.
        
        :param dc: The draw context to draw the graph on. see :class:`~imgtec.lib.wx_extensions.DC`.
        :return: None
        """
        
        #Please note the order that elements of the graph are drawn in are  important, so please do not change the order.
        with push_clipping_rect(dc, self._max_rect.xywh):
        
            # Draw axis specific stuff
            self._draw_axis_pre(dc,self.x_axis)
            self._draw_axis_pre(dc,self.y_axis)
        
            # Draw the graphs title
            if self._title_text != None: 
                _draw_text_off_axis(dc, self.graph.graph_rect, get_side_from_title_text(self._title_text), self._title_text)            

            # Draw bar graphs
            for bar_graph in self._bar_list:
                self.graph.draw_bar_graph(dc, bar_graph.start, bar_graph.interval, bar_graph.values, bar_graph.bar)
                
            # Draw line graphs    
            for line_graph in self._line_list:
                self.graph.draw_line_graph(dc, line_graph.coords, line_graph.line)

            # Draw axis specific stuff that needs drawing after the graphs have been drawn
            self._draw_axis_post(dc, self.x_axis)
            self._draw_axis_post(dc, self.y_axis)
        
            # Draw crosses
            for crosses in self._crosses_list:
                self.graph.draw_crosses(dc, crosses.line_graph.coords, crosses.line_graph.line, crosses.cross_size)
        
            # Draw a border around the whole graph
            if self.draw_border_line != None:
                _draw_border(dc, self._max_rect, self.draw_border_line)
