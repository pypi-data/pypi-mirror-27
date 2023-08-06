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

import itertools
from .breakpoint import BreakpointList
from .core import Core

def _target_info_attrgetter(attrname):
    def _target_info_attrgetter(x):
        return getattr(x.target_info, attrname)
    return _target_info_attrgetter

def _create_children(parent, descendent_contexts, cls, target_info_attr):
    children = []
    idxgetter = _target_info_attrgetter(target_info_attr)
    for idx, contexts in itertools.groupby(descendent_contexts, idxgetter):
        children.append(cls(idx, parent, list(contexts)))
    return children

class SoC(object):
    """Representation of System-On-a-Chip. Only needed when multiple SoCs are connected to a probe."""

    def __init__(self, index, probe, descendent_contexts):
        self.__index = index
        self.__probe = probe
        self.__context = descendent_contexts[0]
        self.__cores = _create_children(self, descendent_contexts, Core, 'core_index')
        
    @property
    def index(self):
        '''Return the zero based index of this soc in the probe object.'''
        return self.__index

    def GetName(self):
        """Name of the SoC."""
        return self.__context.target_info.soc_name

    def GetProbe(self):
        """Parent :class:`Probe <imgtec.codescape.Probe>` of this SoC."""
        return self.__probe
    GetDA = GetProbe

    def GetCores(self):
        """List of :class:`Cores <imgtec.codescape.Core>` on this SoC."""
        return self.__cores

    def GetHardwareThreads(self):
        """List of hardware :class:`Threads <imgtec.codescape.Thread>` on this SoC."""
        return list(itertools.chain.from_iterable(core.hwthreads for core in self.__cores))

    def GetBreakpoints(self):
        """
        Return a :class:`~imgtec.codescape.BreakpointList` containing all
        breakpoints on this SoC.
        """
        target_breakpoints = list(itertools.chain.from_iterable(child.breakpoints for child in self.cores))
        return BreakpointList(self.__context, target_breakpoints)
    
    def __repr__(self):
        name = self.name or ('soc%d' % (self.index,))
        return 'SoC(%s, probe=%s)' % (name,self.probe.name)
        
    def GetDASettingList(self):
        """Returns list of DA settings names."""
        return self.__context.GetDASettingList()

    def GetDASettingValue(self, name):
        """
        Return the DA setting value associated with the setting name given.
        Raises a Error if the name given is not in the list returned by GetEnvList.

        This only returns the value; previously this method returned the type of the
        value as a enum type although I cannot see where this is used. Am I correct in
        removing the value type.
        """
        value, type = self.__context.ReadDASetting(name)
        return value

    def SetDASettingValue(self, name, value):
        """
        Set the DA setting value associated with the setting name given.
        Raises :class:`~imgtec.codescape.Error` if the name given is not in the list returned by GetDASettingList.
        """
        self.__context.WriteDASetting(name, value)        

    breakpoints = property(GetBreakpoints)
    cores       = property(GetCores)
    da          = property(GetDA)
    hwthreads   = property(GetHardwareThreads)
    name        = property(GetName)
    probe       = property(GetProbe)
