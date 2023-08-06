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

__all__ = 'Core'

import itertools

import da_types
from breakpoint import BreakpointList
from da_thread import Thread

def _get_core_threads(core, descendent_contexts):
    threads= []
    for idx, context in enumerate(descendent_contexts):
        threads.append(Thread(idx, core, context))
    return threads

class Core(object):

    """Representation of a hardware core. Cores will have one or more hardware threads."""
    
    def __init__(self, index, soc, descendent_contexts):
        self.__index = index
        self.__context = descendent_contexts[0]
        self.__soc = soc
        self.__core_index = self.__context.target_info.core_index
        self.__name = self.__context.target_info.core_type
        self.__hwthreads = _get_core_threads(self, descendent_contexts)
        
    @property
    def index(self):
        '''Return the zero based index of this core in it's SoC object.'''
        return self.__index

    def __str__(self):
        return self.__name

    def __repr__(self):
        soc_id = self.soc.name or ('soc%d' % (self.soc.index,))
        return 'Core(%s, soc=%s)' % (self.__name, soc_id)

    def HardReset(self):
        """Perform a hard reset of this core."""
        self.__context.HardReset()
        
    def SoftReset(self):
        """Perform a soft reset of this core.
        
        .. note:: This is not implemented on many cores, so will not have any 
                  effect.    
        """
        self.__context.SoftReset()

    def GetHardwareThreads(self):
        """List of hardware :class:`~imgtec.codescape.Thread`\s on this core."""
        return self.__hwthreads

    def GetProbe(self):
        """Parent :class:`~imgtec.codescape.Probe`\s of this core."""
        return self.__soc.probe
    GetDA = GetProbe

    def GetSoC(self):
        """Parent :class:`~imgtec.codescape.SoC` of this core."""
        return self.__soc

    def GetName(self):
        """Name of this core."""
        return self.__name

    def GetDescription(self):
        """Description of this core."""
        return self.name

    def RunAll(self, only_loaded=True):
        """Run all threads on this core."""
        self.__context.RunAllThreads(only_loaded)

    def StopAll(self, only_loaded=True):
        """Stop all threads on this core."""
        self.__context.StopAllThreads(only_loaded)

    def GetEnabled(self):
        """Return boolean value representing the enabled state of the core.
        
        A core that is not disabled does not necessarily mean that the core has 
        been powered down, but rather that debugging of this core has been
        disabled.  This improves the performance of other cores slightly when
        working with very slow targets such as emulators.
        """
        return self.__context.IsCoreEnabled()

    def SetEnabled(self, enabled):
        """Enable or disable the core. See :meth:`GetEnabled`."""
        self.__context.EnableCore(enabled)
        
    def Enable(self):
        """Equivalent to SetEnabled(True)."""
        self.SetEnabled(True)

    def Disable(self):
        """Equivalent to SetEnabled(False)."""
        self.SetEnabled(False)
        
    def GetBreakpoints(self):
        """
        Return a :class:`~imgtec.codescape.BreakpointList` containing all
        breakpoints on this core.
        """
        target_breakpoints = list(itertools.chain.from_iterable(child.breakpoints for child in self.hwthreads))
        return BreakpointList(self.__context, target_breakpoints)

    def GetHSPSettings(self):
        """
        Return the current HSP path or None if no HSP has been set.
        """
        return self.probe.GetHSPSettings()

    def SetHSPSettings(self, hsp_path):
        """
        Load a HSP specified by path, or None to disable HSP.
        """
        self.probe.SetHSPSettings(hsp_path)

    def LoadScript(self, filename, hard_reset=True, load_type=da_types.LoadType.binary_and_symbols, progress=False):
        """
        Initialize the thread with a load script file.

        :param filename:   File name of the load script file.
        :param hard_reset: Hard reset the thread? (True by default).
        :param load_type:  :class:`~imgtec.codescape.LoadType` specifying how to load the program file.
        :param progress:   Show progress? (False by default).
        """
        return self.__hwthreads[0].LoadScript(filename, hard_reset, load_type, progress)

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
        
    def GetStartupOptions(self):
        '''Returns a list of supported startup options.
        
        Each entry is a tuple of (name, load flag, allows command line args).
        
        For example, on MIPS cores the options returned are : 
        
        ======================================= ========= =============================
        Name                                    Load Flag Allows Command Line Arguments
        ======================================= ========= =============================
        UHI command line boot (Status.BEV = 1)  0x1000000 True
        None                                    0         False
        ======================================= ========= =============================
        
        The Load Flag can be OR'd in with other options in the `load_type` 
        parameter of :meth:`LoadScript` or 
        :meth:`~imgtec.codescape.Thread.LoadProgramFile`.
        '''
        return self.__context.GetStartupOptions()

    breakpoints = property(GetBreakpoints)
    da          = property(GetDA)
    description = property(GetDescription)
    enabled     = property(GetEnabled, SetEnabled)
    hwthreads   = property(GetHardwareThreads)
    name        = property(GetName)
    probe       = property(GetProbe)
    soc         = property(GetSoC)
    startup_options = property(GetStartupOptions)
