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
try:
    import codescape
    running_in_codescape = True
except ImportError:
    running_in_codescape = False
    

class CodescapeMethodsHelpCtrl(object):
    def __init__(self, parent, class_name):  
        self.class_name = class_name
        self.create_ctrls(parent)
        self.layout()
        self.bind_ctrls()
        self.get_class_information()
        self.fill_methods_list_box()

    def get_sizer(self):
        return self.sizer

    def create_ctrls(self, parent):
        self.separator1      = wx.StaticLine(parent=parent)
        self.info_text       = wx.StaticText(parent=parent, label="Right click and select 'Edit Script' to see the source code.")
        self.separator2      = wx.StaticLine(parent=parent)
        self.methods_lb      = wx.ListBox( parent = parent, style= wx.LB_HSCROLL  | wx.LB_NEEDED_SB | wx.LB_SINGLE   | wx.LB_SORT) 
        self.details_txt     = wx.TextCtrl(parent = parent, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.BORDER | wx.TE_NO_VSCROLL)
        self.methods_static  = wx.StaticText(parent = parent, label=self.class_name + ' methods', style = wx.BORDER | wx.ST_NO_AUTORESIZE) 
        self.details_static  = wx.StaticText(parent = parent, label=' ', style = wx.BORDER | wx.ST_NO_AUTORESIZE) 
        self.methods_static.SetBackgroundColour(wx.LIGHT_GREY)
        self.details_static.SetBackgroundColour(wx.LIGHT_GREY)
        
    def layout(self):
        self.vsizer1 = wx.BoxSizer(wx.VERTICAL)
        self.vsizer1.Add(self.methods_static, flag=wx.EXPAND)
        self.vsizer1.Add(self.methods_lb, proportion=1, flag=wx.EXPAND)

        self.vsizer2 = wx.BoxSizer(wx.VERTICAL)
        self.vsizer2.Add(self.details_static, flag=wx.EXPAND)
        self.vsizer2.Add(self.details_txt, proportion=1, flag=wx.EXPAND)
        
        self.hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.hsizer.Add(self.vsizer1, proportion=1, flag=wx.EXPAND)
        self.hsizer.AddSpacer(10)
        self.hsizer.Add(self.vsizer2, proportion=1, flag=wx.EXPAND)
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.separator1, flag=wx.EXPAND)
        self.sizer.AddSpacer(5)        
        self.sizer.Add(self.info_text, flag=wx.EXPAND)
        self.sizer.AddSpacer(5)        
        self.sizer.Add(self.separator2, flag=wx.EXPAND)
        self.sizer.AddSpacer(10)
        self.sizer.Add(self.hsizer, proportion=1, flag=wx.EXPAND)
        
        
    def bind_ctrls(self):
        self.methods_lb.Bind(wx.EVT_LISTBOX, self.on_select_method)
        
    def get_class_information(self):    
        self.class_methods = {}
        if running_in_codescape:
            classes = [clsname for clsname in codescape.GetClasses() if clsname.startswith("codescape.") or clsname.startswith("wx.")]
            for clsname in classes:
                self.class_methods[clsname] = sorted(codescape.GetClassMethods(clsname))
        
    def fill_methods_list_box(self):    
        methods = self.class_methods.get(self.class_name, [])
        self.methods_lb.SetItems(methods)

        if self.methods_lb.GetCount():
            self.methods_lb.SetSelection(0)
            self._set_details(self.methods_lb.GetString(0))
            
    def _set_details(self, method_name):    
        if running_in_codescape:
            self.details_txt.SetValue(codescape.GetMethodInfo(self.class_name, method_name) + "\n")
            self.details_static.SetLabel(method_name + ' method...')
        
    def on_select_method(self, evt):
        self.details_txt.SetValue("")
        if evt.Selection != wx.NOT_FOUND:
            self._set_details(self.methods_lb.GetString(evt.Selection))



def bolt_on_class_methods_helper_ctrl(parent, sizer, widget_name, border_space=10):
    # We can only bolt on the Script Class Methods if we are running in Codescape
    if running_in_codescape:
        sizer.Add(CodescapeMethodsHelpCtrl(parent, widget_name).get_sizer(), proportion=1, flag=wx.EXPAND | wx.ALL, border=border_space )

