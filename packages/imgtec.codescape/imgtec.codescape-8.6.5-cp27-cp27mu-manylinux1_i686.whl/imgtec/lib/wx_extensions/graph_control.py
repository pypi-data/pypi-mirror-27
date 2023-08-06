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
from .draw_graph_controller import *

class GraphControl(wx.Window, DrawGraphController):
    """
    Use a GraphControl to plot your data as a graph.
    
     .. image:: examples/SinCosExample.png
        
    This control uses the :class:`~imgtec.lib.wx_extensions.DrawGraphController` helper class to draw
    a graph.
    
    Please read :class:`~imgtec.lib.wx_extensions.DrawGraphController`.
    
    The difference between using this control and using the
    :class:`~imgtec.lib.wx_extensions.DrawGraphController` directly, is that this control is an actual
    widget window which will be a child window of the script region, it has a
    background colour and can be moved and resized. Whereas the 
    :class:`~imgtec.lib.wx_extensions.DrawGraphController` helper class is just a list of methods for
    drawing a graph and when used it will draw a graph directly on the script
    region.
        
    .. note:: If you use the wx layout method, where you create controls as zero
              size and then use wx sizers to size and layout your controls, 
              then you will need to call the :func:`set_internal_borders` 
              function after it has been laid out. This is because the default
              internal borders will have also been set to zero when the control
              was initially created with zero size.    
        
    Here is the code for the DrawGraph example (shown above)
    
    .. literalinclude:: examples/SinCosGraphControlExample.py
    
    The same example but using the DrawGraphController directly (for comparison)
    
    :doc:`examples/SinCosDrawGraphControllerExample`
    
    .. method:: __init__([parent=None], [id=ID_ANY], [pos=DefaultPosition], [size=DefaultSize], [style=0])
    
        :param parent: Pointer to a parent window. Default is None. There is no 
                       need to set this for the script region.
        :param id:     Window identifier. If set to ID_ANY, will automatically 
                       create an identifier. Default = ID_ANY.
                       You only need to set the ID if you are going to use the
                       ID to identify which control generated an event rather
                       than using the bind method.
        :param pos:    (x, y) tuple specifying the controls' position. 
                       DefaultPosition (-1,-1) indicates that wxWidgets should 
                       generate a default position for the window. 
                       Default is DefaultPosition.
        :param size:   (width, height) tuple specifying the controls' size. 
                       DefaultSize (-1,-1) indicates the graph control will be
                       created using a default size. Default is DefaultSize.
        :param style:  Window style. There are no specific GraphControl Styles.
                       For generic window styles, please see wxWindow.
    
    """
    def __init__(self, parent, *args, **kwargs):
        wx.Window.__init__(self, parent, *args, **kwargs)
        size = self.GetClientSizeTuple()
        DrawGraphController.__init__(self, (0,0), size)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_PAINT, self._on_paint)
        self.background_colour = (255,255,255) # default white

    def set_background_colour(self, colour):
        """This function will set the background colour of the DrawGraph control.
        
        :param colour: This is a (Red, Green, Blue) tuple.
        :return: None
        """
        self.background_colour = colour
        self.Refresh()
        
    def _draw_control(self, dc):    
        dc.SetBackground(wx.Brush(self.background_colour, wx.SOLID))
        dc.Clear()
        size = self.GetClientSizeTuple()
        self.set_rect(0,0, *size)
        self.draw(dc)

    def _on_paint(self, evt):
        dc = wx.AutoBufferedPaintDC(self)
        dc.BeginDrawing()
        self._draw_control(dc)
        dc.EndDrawing()
        
    def redraw(self):
        """This will cause an immediate redraw of the graph."""
        self.Refresh()
        self.Update()
