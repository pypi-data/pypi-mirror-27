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

#Exceptions
import sys
# [[[cog
# import cog
# from imgbuild.SConsPaths import sys_path_append_sw
# sys_path_append_sw('tiny_scripting', 'tiny_scripting')
# import exception_types
# for exc in exception_types.base_first():
#    base = exception_types.get_base(exc)
#    cog.outl("class %s(%s):" % (exc, base or 'RuntimeError'))
#    cog.outl('    """%s"""\n' % (exception_types.get_doc(exc) or ''))
# ]]]
class Error(RuntimeError):
    """"""

class BreakpointError(Error):
    """Raised when a breakpoint could not be created or modified."""

class CommsBaseError(Error):
    """Base class for comms errors"""

class ExecutionStateError(Error):
    """When a function that requires the target to be halted is called
    and the target is running."""

class InvalidArgError(Error):
    """"""

class LicenseError(Error):
    """FLEX-related exception."""

class NotAnELF(Error):
    """"""

class OperationCancelled(Error):
    """The operation has been cancelled."""

class ProfilerError(Error):
    """"""

class ProgramFileError(Error):
    """"""

class TargetError(Error):
    """"""

class ThreadInvalidError(Error):
    """DAscript or DAtinyscript was called from the wrong system thread.
    
    This exception will only be called when thread checking has been enabled.
    """

class ArgumentNotSuppliedError(InvalidArgError):
    """"""

class AssertionFailed(TargetError):
    """"""

class CallBackError(InvalidArgError):
    """"""

class CommsError(CommsBaseError):
    """Errors reported by the comms layer, related to comms failure states"""

class CommsProbeError(CommsBaseError):
    """Errors reported by the probe, related to probe failure states"""

class CommsTargetError(CommsBaseError):
    """Errors reported by the probe, related to target failure states"""

class CoreDisabled(TargetError):
    """The core has been disabled."""

class CoreOffline(TargetError):
    """The core is offline."""

class ExpressionEvaluationError(InvalidArgError):
    """Raised when an invalid expression has been given."""

class InvalidConversion(InvalidArgError):
    """"""

class LicenseCheckoutError(LicenseError):
    """Failed to check out a license."""

class LicenseConsistencyError(LicenseError):
    """An inconsistency has been detected in the license manager. e.g.
    *    Bad initialisation of the flex handling code.
    *    A supposedly checked-out license is no longer checked out.
    *    A request for info has failed.
    """

class LoadProgramFileError(TargetError):
    """"""

class ResetOccurred(TargetError):
    """The target has reset unexpectedly, and AcknowledgeReset has not yet
    been called."""

class TargetAlreadyConnected(TargetError):
    """The target is already connected, an earlier ConnectThread call was not 
    matched with a corresponding DisconnectThread.
    """

class TargetDisconnected(TargetError):
    """The target is not connected."""

class TargetInvalid(TargetError):
    """Invalid target identifier."""

class TargetNotFound(TargetError):
    """Unable to find the probe.   Raised by ConnectProbe."""

class UnrecoverableMemoryFault(TargetError):
    """An unrecoverable memory fault has been detected.
    
    The target will be soft reset to allow inspection of the postmortem state.
    """

class CommsBadChannelNumberError(CommsError):
    """The requested channel number is invalid"""

class CommsDeviceInUseError(CommsError):
    """The device is already in use"""

class CommsDeviceNotFoundError(CommsError):
    """Failed to find requested device"""

class CommsNoTransportFoundError(CommsError):
    """No transport was found which supports the given serial number"""

class CommsPayloadMissingError(CommsError):
    """No payload was received from the probe, when one was expected"""

class CommsPayloadShortError(CommsError):
    """The payload received was shorter than expected"""

class CommsProbeConnectionRefusedError(CommsProbeError):
    """DA is in use, currently sent on TCP only in response to connect command."""

class CommsProbeFatalError(CommsProbeError):
    """Command fatal error"""

class CommsProbeFlashDataBadError(CommsProbeError):
    """A bad application binary has been passed for flashing."""

class CommsProbeFlashEraseError(CommsProbeError):
    """Failed flash erase"""

class CommsProbeFlashImageCorruptError(CommsProbeError):
    """Flash image is corrupt"""

class CommsProbeFlashWriteError(CommsProbeError):
    """Failed flash program"""

class CommsProbeTimeoutError(CommsProbeError):
    """Command timed out"""

class CommsRegisterInvalidDataSizeError(CommsError):
    """Invalid data size for the requested registers"""

class CommsSimInUseError(CommsError):
    """The DA-sim could not connect to the simulator because the simulator is in use"""

class CommsSimNotFoundError(CommsError):
    """The DA-sim could not start the simulator"""

class CommsTargetAddressError(CommsTargetError):
    """Bad address parameter"""

class CommsTargetChannelBufferEmptyError(CommsTargetError):
    """Channel buffer empty"""

class CommsTargetChannelBufferFullError(CommsTargetError):
    """Channel buffer full"""

class CommsTargetCheckInquiryError(CommsTargetError):
    """Unspecified problem, check 'inquiry'"""

class CommsTargetCommandNotAvailableError(CommsTargetError):
    """Command not available"""

class CommsTargetCommandUnknownError(CommsTargetError):
    """Command unknown"""

class CommsTargetCountError(CommsTargetError):
    """Bad count parameter"""

class CommsTargetFatalError(CommsTargetError):
    """Command fatal error"""

class CommsTargetJtagIncompatibleError(CommsTargetError):
    """The target has an incompatible version of IMGlib JTAG, the DA requires a firmware upgrade"""

class CommsTargetMmuAddressNotMappedError(CommsTargetError):
    """The address is not mapped in the MMU"""

class CommsTargetMtxMemoryFaultError(CommsTargetError):
    """MTX memory fault, chip lockup"""

class CommsTargetParameterError(CommsTargetError):
    """Bad command parameter"""

class CommsTargetRejectedBusyError(CommsTargetError):
    """Command rejected due to being busy"""

class CommsTargetThread0BusError(CommsTargetError):
    """Meta thread 0 bus lock error"""

class CommsTargetThread0JtagError(CommsTargetError):
    """Meta thread 0 jtag failure"""

class CommsTargetThread1BusError(CommsTargetError):
    """Meta thread 1 bus lock error"""

class CommsTargetThread1JtagError(CommsTargetError):
    """Meta thread 1 jtag failure"""

class CommsTargetThread2BusError(CommsTargetError):
    """Meta thread 2 bus lock error"""

class CommsTargetThread2JtagError(CommsTargetError):
    """Meta thread 2 jtag failure"""

class CommsTargetThread3BusError(CommsTargetError):
    """Meta thread 3 bus lock error"""

class CommsTargetThread3JtagError(CommsTargetError):
    """Meta thread 3 jtag failure"""

class CommsTimeoutError(CommsError):
    """Command timed out"""

class CommsUnsupportedError(CommsError):
    """This transport does not support this operation."""

class CommsUserAbortError(CommsError):
    """The user aborted the operation"""

class LicensePlatformError(LicenseCheckoutError):
    """No license for the requested platform."""

class LoadProgramFileNonFatalError(LoadProgramFileError):
    """A serious problem was detected in the debug info.
    
    Thrown when a serious warning occurs during the load of the debug info of an
    elf.  The binary has successfully loaded (if requested), but some or all of the
    debug info may not be available due to corrupt or invalid debug information.
    """

# [[[end]]]

class OverlayError(Error):
    """Overlay error."""

class DiagnosticError(TargetError):
    """Diagnostic error."""

class FrameError(Error):
    """Frame access error."""

class FileServerError(Error):
    """File server error."""

class _ExceptionMapper(object):
    def __init__(self, srcmodule):
        self.__srcmodule = srcmodule
        if srcmodule:
            self.__exception_map = [
                # [[[cog
                # import cog
                # import sys
                # sys.path.append(r'../../../../debugger/library/tiny_scripting/tiny_scripting')
                # import exception_types
                # for exc in exception_types.derived_first():
                #    cog.outl("('%s', %s)," % (exc, exc))
                # ]]]
                ('CommsBadChannelNumberError', CommsBadChannelNumberError),
                ('CommsDeviceInUseError', CommsDeviceInUseError),
                ('CommsDeviceNotFoundError', CommsDeviceNotFoundError),
                ('CommsNoTransportFoundError', CommsNoTransportFoundError),
                ('CommsPayloadMissingError', CommsPayloadMissingError),
                ('CommsPayloadShortError', CommsPayloadShortError),
                ('CommsProbeConnectionRefusedError', CommsProbeConnectionRefusedError),
                ('CommsProbeFatalError', CommsProbeFatalError),
                ('CommsProbeFlashDataBadError', CommsProbeFlashDataBadError),
                ('CommsProbeFlashEraseError', CommsProbeFlashEraseError),
                ('CommsProbeFlashImageCorruptError', CommsProbeFlashImageCorruptError),
                ('CommsProbeFlashWriteError', CommsProbeFlashWriteError),
                ('CommsProbeTimeoutError', CommsProbeTimeoutError),
                ('CommsRegisterInvalidDataSizeError', CommsRegisterInvalidDataSizeError),
                ('CommsSimInUseError', CommsSimInUseError),
                ('CommsSimNotFoundError', CommsSimNotFoundError),
                ('CommsTargetAddressError', CommsTargetAddressError),
                ('CommsTargetChannelBufferEmptyError', CommsTargetChannelBufferEmptyError),
                ('CommsTargetChannelBufferFullError', CommsTargetChannelBufferFullError),
                ('CommsTargetCheckInquiryError', CommsTargetCheckInquiryError),
                ('CommsTargetCommandNotAvailableError', CommsTargetCommandNotAvailableError),
                ('CommsTargetCommandUnknownError', CommsTargetCommandUnknownError),
                ('CommsTargetCountError', CommsTargetCountError),
                ('CommsTargetFatalError', CommsTargetFatalError),
                ('CommsTargetJtagIncompatibleError', CommsTargetJtagIncompatibleError),
                ('CommsTargetMmuAddressNotMappedError', CommsTargetMmuAddressNotMappedError),
                ('CommsTargetMtxMemoryFaultError', CommsTargetMtxMemoryFaultError),
                ('CommsTargetParameterError', CommsTargetParameterError),
                ('CommsTargetRejectedBusyError', CommsTargetRejectedBusyError),
                ('CommsTargetThread0BusError', CommsTargetThread0BusError),
                ('CommsTargetThread0JtagError', CommsTargetThread0JtagError),
                ('CommsTargetThread1BusError', CommsTargetThread1BusError),
                ('CommsTargetThread1JtagError', CommsTargetThread1JtagError),
                ('CommsTargetThread2BusError', CommsTargetThread2BusError),
                ('CommsTargetThread2JtagError', CommsTargetThread2JtagError),
                ('CommsTargetThread3BusError', CommsTargetThread3BusError),
                ('CommsTargetThread3JtagError', CommsTargetThread3JtagError),
                ('CommsTimeoutError', CommsTimeoutError),
                ('CommsUnsupportedError', CommsUnsupportedError),
                ('CommsUserAbortError', CommsUserAbortError),
                ('LicensePlatformError', LicensePlatformError),
                ('LoadProgramFileNonFatalError', LoadProgramFileNonFatalError),
                ('ArgumentNotSuppliedError', ArgumentNotSuppliedError),
                ('AssertionFailed', AssertionFailed),
                ('CallBackError', CallBackError),
                ('CommsError', CommsError),
                ('CommsProbeError', CommsProbeError),
                ('CommsTargetError', CommsTargetError),
                ('CoreDisabled', CoreDisabled),
                ('CoreOffline', CoreOffline),
                ('ExpressionEvaluationError', ExpressionEvaluationError),
                ('InvalidConversion', InvalidConversion),
                ('LicenseCheckoutError', LicenseCheckoutError),
                ('LicenseConsistencyError', LicenseConsistencyError),
                ('LoadProgramFileError', LoadProgramFileError),
                ('ResetOccurred', ResetOccurred),
                ('TargetAlreadyConnected', TargetAlreadyConnected),
                ('TargetDisconnected', TargetDisconnected),
                ('TargetInvalid', TargetInvalid),
                ('TargetNotFound', TargetNotFound),
                ('UnrecoverableMemoryFault', UnrecoverableMemoryFault),
                ('BreakpointError', BreakpointError),
                ('CommsBaseError', CommsBaseError),
                ('ExecutionStateError', ExecutionStateError),
                ('InvalidArgError', InvalidArgError),
                ('LicenseError', LicenseError),
                ('NotAnELF', NotAnELF),
                ('OperationCancelled', OperationCancelled),
                ('ProfilerError', ProfilerError),
                ('ProgramFileError', ProgramFileError),
                ('TargetError', TargetError),
                ('ThreadInvalidError', ThreadInvalidError),
                ('Error', Error),
                # [[[end]]]
            ]
            
    def map_exception(self, e):
        if self.__srcmodule:
            for cexc_name, pyexc in self.__exception_map:
                cexc = getattr(self.__srcmodule, cexc_name, None)
                if cexc and isinstance(e, cexc):
                    return pyexc
        return Error

    def wrap(self, wrappee):
        if self.__srcmodule:
            def f(*args, **kwargs):
                try:
                    return wrappee(*args, **kwargs)
                except self.__srcmodule.Error as e:
                    tb = sys.exc_info()[2]
                    exc = self.map_exception(e)
                    raise exc, str(e), tb
            f.__name__ == wrappee.__name__
        else:
            f = wrappee
        return f
