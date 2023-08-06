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

__all__ = 'Breakpoint'

import sys

import da_types
from da_exception import BreakpointError
import functools

def _get_breakpoint_info(da):
    table = da.GetBreakpointsRaw()
    return [dict(zip(table[0], values)) for values in table[1:]]

def _find_breakpoint_info(da, bpid):
    for bpinfo in _get_breakpoint_info(da):
        if bpinfo["bpid"] == bpid:
            return bpinfo
            

def _check_is_breakpoint_type(breakpoint, bptype, fnname):
    if breakpoint.GetType() == da_types.BreakpointType.Code:
        raise BreakpointError('%s: Invalid call for a %s breakpoint' % (fnname,str(bptype).lower()))

def code_breakpoint_method(f):
    @functools.wraps(f)
    def code_breakpoint_method_wrapper(breakpoint, *args, **kargs):
        _check_is_breakpoint_type(breakpoint, da_types.BreakpointType.Code, f.__name__)
        return f(breakpoint, *args, **kargs)
    code_breakpoint_method_wrapper.__doc__ = f.__doc__
    return code_breakpoint_method_wrapper

def data_breakpoint_method(f):
    @functools.wraps(f)
    def data_breakpoint_method_wrapper(breakpoint, *args, **kargs):
        _check_is_breakpoint_type(breakpoint, da_types.BreakpointType.Data, f.__name__)
        return f(breakpoint, *args, **kargs)
    data_breakpoint_method_wrapper.__doc__ = f.__doc__
    return data_breakpoint_method_wrapper

# These properties are here because we have previously advertised these
# types/values to be members of breakpoint.XXX
AnyWatchAccessSize = da_types.WatchAccessSize.Any
SingleShot = da_types.SingleShot
WatchAccessTypes = da_types.WatchAccessTypes
Mechanisms = da_types.Mechanisms
Conditions = da_types.Conditions
Log = da_types.Log



class BreakpointList(list):
    """A list like object holding a set of breakpoints.
    
    Also contains methods that operate on all of the breakpoints in the list.
    """

    def __init__(self, context, breakpoints):
        self.__context = context
        self.extend(breakpoints)

    def EnableAll(self, enabled=True):
        """Enable all breakpoints in this list."""
        for breakpoint in self:
            breakpoint.enabled = enabled

    def DisableAll(self):
        """Disable all breakpoints in this list."""
        self.EnableAll(False)

    def DestroyAll(self):
        """Destroy all breakpoints in this list."""
        for breakpoint in self:
            breakpoint.Destroy()
            
    def ResetAll(self):
        """Reset counters in all breakpoints in this list."""
        for breakpoint in self:
            breakpoint.Reset()

    def GetCodeBreakpoints(self):
        """Return a BreakpointList with only the code breakpoints in this list."""
        return BreakpointList(self.__context, (breakpoint for breakpoint in self if breakpoint.is_code))

    def GetDataBreakpoints(self):
        """Return a BreakpointList with only the data breakpoints in this list."""
        return BreakpointList(self.__context, (breakpoint for breakpoint in self if breakpoint.is_data))

    code_breakpoints = property(GetCodeBreakpoints)
    data_breakpoints = property(GetDataBreakpoints)

_type_mechanism_map = {
    da_types.BreakpointType.Code:         Mechanisms.AnyAvailable,
    da_types.BreakpointType.CodeHardware: Mechanisms.Hardware,
    da_types.BreakpointType.CodeSoftware: Mechanisms.Software,
    da_types.BreakpointType.Data:         Mechanisms.AnyAvailable,
}

_mechanism_type_map = {
    Mechanisms.AnyAvailable: da_types.BreakpointType.Code,
    Mechanisms.Hardware:     da_types.BreakpointType.CodeHardware,
    Mechanisms.Software:     da_types.BreakpointType.CodeSoftware,
}

class Breakpoint(object):

    # These properties are here because we have previously advertised these 
    # types/values to be members of Breakpoint.XXX and BreakpointEnums.XXX
    AnyWatchAccessSize = da_types.WatchAccessSize.Any
    WatchAccessSize = da_types.WatchAccessSize
    SingleShot = da_types.SingleShot
    WatchAccessTypes = da_types.WatchAccessTypes
    Mechanisms = da_types.Mechanisms
    Conditions = da_types.Conditions
    Log = da_types.Log

    def __init__(self, context, thread, bpid, info=None):
        self.__context = context
        self.__thread = thread
        self.__bpid = bpid
        self.__dead = False

        if not info:
            info = _find_breakpoint_info(self.__context, self.__bpid)
        if not info:
            raise BreakpointError("Invalid breakpoint: %r" % self.__bpid)

        self._set_info(info)

    def __eq__(self, other):
        return self.__bpid == other.__bpid
        
    def __hash__(self):
        return hash(self.__bpid)

    def _set_dead(self):
        self.__dead = True

    def _set_info(self, info):
        self.__address = int(info["address"])
        self.__enabled = info["enabled"]
        self.__type = info["type"]
        self.__is_source = info["is_source"]
        self.__location_expression = info["location_expression"]
        self.__location_mask = info["location_mask"]
        self.__overlay_area = info["overlay_area"]
        self.__overlay = info["overlay"]
        self.__breakpoint_condition = info["breakpoint_condition"]
        self.__condition_expression = info["condition_expression"]
        self.__trigger = info["trigger"]
        self.__count = info["count"]
        self.__data_mask = info["data_mask"]
        self.__include_data_condition = info["include_data_condition"]
        self.__data_expression = info["data_expression"]
        self.__access_type = info["access_type"]
        self.__access_size = info["access_size"]
        self.__halt_execution = info["halt_execution"]
        self.__message_box = info["message_box"]
        self.__run_script = info["run_script"]
        self.__script_file = info["script_file"]
        self.__script_arguments = info["script_arguments"]
        self.__prompt_for_script_arguments = info["prompt_for_script_arguments"]
        self.__single_shot = info["single_shot"]
        self.__log = info["log"]
        self.__log_expression = info["log_expression"]

    def _check_exists(self):
        if self.__dead:
            raise BreakpointError("Breakpoint does not exist: %r" % self.__bpid)

    def _refresh(self):
        self.__thread._refresh_breakpoints()

    def GetId(self):
        """Returns a unique identifier for this breakpoint."""
        return self.__bpid

    def GetIsDead(self):
        """True if breakpoint has been deleted."""
        return self.__dead

    def GetEnabled(self):
        """True if the breakpoint is currently enabled."""
        self._check_exists()
        return self.__enabled

    def SetEnabled(self, enabled=True):
        """Set the breakpoint to be enabled or disabled."""
        self._check_exists()
        self.__context.EnableBreakpoint(self.__bpid, enabled)
        self._refresh()
        
    def Enable(self):
        """Equivalent to ``SetEnabled(True)``."""
        self.SetEnabled(True)

    def Disable(self):
        """Equivalent to ``SetEnabled(False)``."""
        self.SetEnabled(False)

    def GetAddress(self):
        """Get location address of this breakpoint."""
        self._check_exists()
        return self.__address

    def GetType(self):
        """The :class:`BreakpointType <imgtec.codescape.BreakpointType>` of this breakpoint."""
        return self.__type

    def GetIsCode(self):
        """True if this breakpoint is a code breakpoint."""
        self._check_exists()
        return self.__type != da_types.BreakpointType.Data

    def GetIsData(self):
        """True if this breakpoint is a data breakpoint."""
        self._check_exists()
        return not self.is_code

    def GetLocationExpression(self):
        """The location expression of this breakpoint.
        This value was evaluated to determine the location address of this breakpoint."""
        self._check_exists()
        return self.__location_expression

    def SetLocationExpression(self, location_expression):
        """Changes the location expression of this breakpoint.
        
        This value is evaluated to determine the location address of this breakpoint."""
        self._check_exists()
        self.__context.RecreateBreakpoint(self.__bpid, location_expression, self.GetMechanism())
        self._refresh()

    SetAddress = SetLocationExpression

    @data_breakpoint_method
    def GetDataMask(self):
        """Returns the data mask applied to the :meth:`GetDataExpression <imgtec.codescape.Breakpoint.GetDataExpression>`
        before making the data comparison."""
        self._check_exists()
        return self.__context.GetBreakpointDataMask(self.__bpid)

    @data_breakpoint_method
    def SetDataMask(self, mask):
        """Sets a data mask applied to the :meth:`GetDataExpression <imgtec.codescape.Breakpoint.GetDataExpression>`
        before making the data comparison."""
        self._check_exists()
        self.__context.SetBreakpointDataMask(self.__bpid, mask)
        self._refresh()

    def GetOverlay(self):
        """:class:`OverlayArea <imgtec.codescape.OverlayArea>` of this breakpoint."""
        # TODO: This should return an Overlay object
        self._check_exists()
        raise NotImplementedError
        #return (self.__overlay, self.__overlay_area)

    def SetOverlay(self, overlay):
        """Set :class:`OverlayArea <imgtec.codescape.OverlayArea>`."""
        # TODO: This should accept an Overlay object
        self._check_exists()
        raise NotImplementedError

    def GetLocationMask(self):
        """Returns the location mask of the breakpoints location."""
        self._check_exists()
        return '0x%08x' % int(self.__location_mask, 16)

    def SetLocationMask(self, mask):
        """Gets the location mask of the breakpoints location."""
        self._check_exists()
        self.__context.SetBreakpointLocationMaskEx(self.__bpid, mask)
        self._refresh()

    @data_breakpoint_method
    def GetDataExpression(self):
        """Returns the data expression used in the data comparison on this data watch breakpoint.

        For this option to be enabled the breakpoint is required to have
        :meth:`include data condition <imgtec.codescape.Breakpoint.GetIncludeDataCondition>` enabled.

        A :meth:`data mask <imgtec.codescape.Breakpoint.SetDataMask>`
        may also be used to mask out bits when making the data comparison. """
        self._check_exists()
        return self.__data_expression

    @data_breakpoint_method
    def SetDataExpression(self, data_expression):
        """Sets the data expression used in the data comparison on this data watch breakpoint.
        This expression will be evaluated to determine the data value to be used in the data comparison.

        For this option to be enabled the breakpoint is required to have 
        :meth:`include data condition <imgtec.codescape.Breakpoint.GetIncludeDataCondition>` enabled.

        A :meth:`data mask <imgtec.codescape.Breakpoint.SetDataMask>`
        may also be used to mask out bits when making the data comparison.
        """
        self._check_exists()
        watch_parameters = self.__context.GetWatchBreakpointParameters(self.__bpid)
        expression_type = watch_parameters[2]
        self.__context.SetWatchBreakpointParameters(self.__bpid, self.__include_data_condition, data_expression, expression_type, self.__access_size, self.__access_type)
        self._refresh()

    def GetMechanism(self):
        """Returns the :class:`Mechanism <imgtec.codescape.Mechanism>` of this breakpoint."""
        self._check_exists()
        return _type_mechanism_map[self.__type]

    @code_breakpoint_method
    def SetMechanism(self, mechanism):
        """Changes the :class:`Mechanism <imgtec.codescape.Mechanism>` of this breakpoint."""
        self._check_exists()
        self.__context.RecreateBreakpoint(self.__bpid, self.__location_expression, mechanism)
        self._refresh()

    @data_breakpoint_method
    def GetIncludeDataCondition(self):
        """Returns True if this breakpoint is using a data condition.
        
        To configure the watch parameters, see :meth:`SetWatchParameters <imgtec.codescape.Breakpoint.SetWatchParameters>`.
        """
        self._check_exists()
        return self.__include_data_condition

    @data_breakpoint_method
    def GetAccessSize(self):
        """Returns the data access size when the data at this location is accessed.
        
        To configure the watch parameters, see :meth:`SetWatchParameters <imgtec.codescape.Breakpoint.SetWatchParameters>`.
        """
        self._check_exists()
        return self.__access_size

    @data_breakpoint_method
    def GetAccessType(self):
        """Returns the data access type when the data at this location is accessed.
        
        To configure the watch parameters, see :meth:`SetWatchParameters <imgtec.codescape.Breakpoint.SetWatchParameters>`.
        """
        self._check_exists()
        return self.__access_type

    @data_breakpoint_method
    def SetWatchParameters(self, include_data_condition, access_type, access_size):
        """Set the data breakpoint conditions required for breakpoint to match."""
        self._check_exists()
        watch_parameters = self.__context.GetWatchBreakpointParameters(self.__bpid)
        expression_type = watch_parameters[2]
        self.__context.SetWatchBreakpointParameters(self.__bpid, include_data_condition, self.__data_expression, expression_type, access_size, access_type)
        self._refresh()

    def GetTriggerCount(self):
        """Returns the number of times this breakpoint is hit before a break will occur.
        
        The current hit count can be found by calling :meth:`GetHitCount <imgtec.codescape.Breakpoint.GetHitCount>`.

        The hit count is only compared to the trigger count if a suitable condition option is set in
        :meth:`SetConditionType <imgtec.codescape.Breakpoint.SetConditionType>`.
        """
        self._check_exists()
        condition_type, expression, trigger_count, hit_count = self.__context.GetBreakpointConditionEx(self.__bpid)
        return trigger_count

    def SetTriggerCount(self, trigger_count):
        """Sets the number of times this breakpoint is hit before a break will occur.
        
        The current hit count can be found by calling :meth:`GetHitCount <imgtec.codescape.Breakpoint.GetHitCount>`.

        The hit count is only compared to the trigger count if a suitable condition option is set in
        :meth:`SetConditionType <imgtec.codescape.Breakpoint.SetConditionType>`."""
        self._check_exists()
        self.__context.SetBreakpointConditionEx(self.__bpid, self.GetConditionType(), self.GetConditionExpression(), trigger_count, self.GetHitCount())
        self._refresh()

    def GetHitCount(self):
        """Returns the number of times this breakpoint has been currently hit.
        
        This count will be compared to the trigger count to determine when this breakpoint will break.

        The hit count is only compared to the trigger count if a suitable condition option is set in
        :meth:`SetConditionType <imgtec.codescape.Breakpoint.SetConditionType>`.
        """
        condition_type, expression, trigger_count, hit_count = self.__context.GetBreakpointConditionEx(self.__bpid)
        return hit_count

    def SetHitCount(self, hit_count):
        """Change the number of times this breakpoint has been currently hit. 
        
        This count will be compared to the trigger count to determine when this breakpoint will break.

        The hit count is only compared to the trigger count if a suitable condition option is set in
        :meth:`SetConditionType <imgtec.codescape.Breakpoint.SetConditionType>`.
        """
        self._check_exists()
        self.__context.SetBreakpointConditionEx(self.__bpid, self.GetConditionType(), self.GetConditionExpression(), self.GetTriggerCount(), hit_count)
        self._refresh()

    def GetConditionExpression(self):
        """Returns the condition expression evaluated when the breakpoint is hit.
        
        The breakpoint will break if this expression evaluates to true.
        """
        self._check_exists()
        condition_type, expression, trigger_count, hit_count = self.__context.GetBreakpointConditionEx(self.__bpid)
        return expression

    def SetConditionExpression(self, expression):
        """Sets the condition expression evaluated when the breakpoint is hit.
        
        The breakpoint will break if this expression evaluates to true.

        This condition is only evaluated if a suitable condition option is set in
        :meth:`SetConditionType <imgtec.codescape.Breakpoint.SetConditionType>`.
        """
        self._check_exists()
        self.__context.SetBreakpointConditionEx(self.__bpid, self.GetConditionType(), expression, self.GetTriggerCount(), self.GetHitCount())
        self._refresh()

    def GetConditionType(self):
        """Get the :class:`BreakpointType <imgtec.codescape.Condition>` of this breakpoint."""
        self._check_exists()
        condition_type, expression, trigger_count, hit_count = self.__context.GetBreakpointConditionEx(self.__bpid)
        return Conditions(condition_type)

    def SetConditionType(self, condition_type):
        """Set the :class:`BreakpointType <imgtec.codescape.Condition>` of this breakpoint.

        To configure the trigger count, see :meth:`SetTriggerCount <imgtec.codescape.Breakpoint.SetTriggerCount>`.

        To configure the configure expression, see :meth:`SetConditionExpression <imgtec.codescape.Breakpoint.SetConditionExpression>`.
        """
        self._check_exists()
        if condition_type not in list(Conditions._values()):
            raise BreakpointError('Invalid condition type: Refer to Conditions')

        self.__context.SetBreakpointConditionEx(self.__bpid, condition_type, self.GetConditionExpression(), self.GetTriggerCount(), self.GetHitCount())
        self._refresh()

    def GetHaltExecution(self):
        """Should this breakpoint break when hit.

        The breakpoint must be configured to break when hit for certain actions to be executed, such as
        :meth:`run scripts <imgtec.codescape.Breakpoint.GetScriptFile>` and
        :meth:`displaying a message box <imgtec.codescape.Breakpoint.GetShowMessageBox>`.
        """
        self._check_exists()
        return self.__halt_execution

    def SetHaltExecution(self, halt_execution=True):
        """Set this breakpoint to break when hit, or if to continue execution."""
        self._check_exists()
        self.__context.SetBreakpointActionEx(self.__bpid, halt_execution, self.__single_shot, self.__message_box, self.__run_script, self.__script_file, self.__script_arguments, self.__prompt_for_script_arguments, self.__log, self.__log_expression)
        self._refresh()

    def GetShowMessageBox(self):
        """Should a message box to be displayed when this breakpoint is hit.
        
        For this option to be enabled the breakpoint is required to be set to break when hit.
        See :meth:`SetHaltExecution <imgtec.codescape.Breakpoint.SetHaltExecution>`.
        """
        self._check_exists()
        return self.__message_box

    def SetShowMessageBox(self, show_message_box):
        """Set a message box to be displayed when this breakpoint is hit.
        
        For this option to be enabled the breakpoint is required to be set to break when hit.
        See :meth:`SetHaltExecution <imgtec.codescape.Breakpoint.SetHaltExecution>`.
        """
        self._check_exists()
        self.__context.SetBreakpointActionEx(self.__bpid, self.__halt_execution, self.__single_shot, show_message_box, self.__run_script, self.__script_file, self.__script_arguments, self.__prompt_for_script_arguments, self.__log, self.__log_expression)
        self._refresh()

    def GetSingleShot(self):
        """Get the :class:`BreakpointType <imgtec.codescape.SingleShot>` of this breakpoint."""
        self._check_exists()
        return self.__single_shot

    def SetSingleShot(self, single_shot):
        """Set the :class:`BreakpointType <imgtec.codescape.SingleShot>` of this breakpoint."""
        self._check_exists()
        self.__context.SetBreakpointActionEx(self.__bpid, self.__halt_execution, single_shot, self.__message_box, self.__run_script, self.__script_file, self.__script_arguments, self.__prompt_for_script_arguments, self.__log, self.__log_expression)
        self._refresh()

    def GetLogType(self):
        """Get the :class:`Logging Type <imgtec.codescape.Log>` of this breakpoint."""
        self._check_exists()
        return Log(self.__log)

    def SetLogType(self, log):
        """Set the :class:`Logging Type <imgtec.codescape.Log>` of this breakpoint.
        
        The log expression can be defined by calling 
        :meth:`SetLogExpression <imgtec.codescape.Breakpoint.SetLogExpression>`.
        """
        self._check_exists()
        self.__context.SetBreakpointActionEx(self.__bpid, self.__halt_execution, self.__single_shot, self.__message_box, self.__run_script, self.__script_file, self.__script_arguments, self.__prompt_for_script_arguments, log, self.__log_expression)
        self._refresh()

    GetLog = GetLogType
    SetLog = SetLogType

    def GetLogExpression(self):
        """Returns the log expression that is printed when this breakpoint is hit."""
        self._check_exists()
        return self.__log_expression

    def SetLogExpression(self, log_expression):
        """Sets the log expression that should be printed when this breakpoint is hit.
        
        To control when this expression is logged see 
        :meth:`SetLogType <imgtec.codescape.Breakpoint.SetLogType>`.
        """
        self._check_exists()
        self.__context.SetBreakpointActionEx(self.__bpid, self.__halt_execution, self.__single_shot, self.__message_box, self.__run_script, self.__script_file, self.__script_arguments, self.__prompt_for_script_arguments, self.__log, log_expression)
        self._refresh()

    def GetRunScript(self):
        """True if a script should be run when the breakpoint is hit.
        
        For a script to be executed, this breakpoint is required to be set to break when hit.
        See :meth:`SetHaltExecution <imgtec.codescape.Breakpoint.SetHaltExecution>`.
        """
        self._check_exists()
        return self.__run_script

    def SetRunScript(self, run_script=True):
        """True if a script should be run when the breakpoint is hit.
        
        For this option to be enabled the breakpoint is required to be set to break when hit.
        The script to be run is defined by calling :meth:`SetScriptFile <imgtec.codescape.Breakpoint.SetScriptFile>`.
        
        For a script to be executed, this breakpoint is required to be set to break when hit.
        See :meth:`SetHaltExecution <imgtec.codescape.Breakpoint.SetHaltExecution>`.
        """
        self._check_exists()
        self.__context.SetBreakpointActionEx(self.__bpid, self.__halt_execution, self.__single_shot, self.__message_box, run_script, self.__script_file, self.__script_arguments, self.__prompt_for_script_arguments, self.__log, self.__log_expression)
        self._refresh()

    def GetScriptFile(self):
        """The path of the script that will be run when the breakpoint is hit if
        :meth:`GetRunScript <imgtec.codescape.Breakpoint.GetRunScript>` is enabled.
        
        For a script to be executed, this breakpoint is required to be set to break when hit.
        See :meth:`SetHaltExecution <imgtec.codescape.Breakpoint.SetHaltExecution>`.
        """
        self._check_exists()
        return self.__script_file

    def SetScriptFile(self, script_file):
        """Set the path of the script that will be run when the breakpoint is hit if
        :meth:`GetRunScript <imgtec.codescape.Breakpoint.GetRunScript>` is enabled.
        
        For a script to be executed, this breakpoint is required to be set to break when hit.
        See :meth:`SetHaltExecution <imgtec.codescape.Breakpoint.SetHaltExecution>`.
        """
        self._check_exists()
        self.__context.SetBreakpointActionEx(self.__bpid, self.__halt_execution, self.__single_shot, self.__message_box, self.__run_script, script_file, self.__script_arguments, self.__prompt_for_script_arguments, self.__log, self.__log_expression)
        self._refresh()

    def GetScriptArguments(self):
        """Returns the parameters passed to the configured script file to be run when this breakpoint is hit.
        
        The script to be run is defined by calling :meth:`SetScriptFile <imgtec.codescape.Breakpoint.SetScriptFile>`.
        """
        self._check_exists()
        return self.__script_arguments

    def SetScriptArguments(self, script_arguments):
        """Sets the parameters passed to the configured script file to be run when this breakpoint is hit.
        
        The script to be run is defined by calling :meth:`SetScriptFile <imgtec.codescape.Breakpoint.SetScriptFile>`.
        """
        self._check_exists()
        self.__context.SetBreakpointActionEx(self.__bpid, self.__halt_execution, self.__single_shot, self.__message_box, self.__run_script, self.__script_file, script_arguments, self.__prompt_for_script_arguments, self.__log, self.__log_expression)
        self._refresh()

    def Reset(self):
        """Reset any counters on this breakpoints."""
        self.__context.ResetBreakpoint(self.__bpid)
            
    def Destroy(self):
        """Destroy this breakpoint and remove it from the target thread."""
        self._check_exists()
        self.__context.ClearBreakpoint(self.__bpid)
        self._refresh()
        
    def __repr__(self):
        return '%s(address=%s (%s), enabled=%s)' % (da_types.BreakpointType(self.GetType()),
                    self.address, self.location_expression, self.enabled)

    enabled = property(GetEnabled, SetEnabled)
    address = property(GetAddress, SetAddress)
    location_expression = property(GetLocationExpression, SetLocationExpression)
    is_dead = property(GetIsDead)
    is_code = property(GetIsCode)
    is_data = property(GetIsData)
    
BreakpointEnums = Breakpoint
