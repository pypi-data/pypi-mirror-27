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

#!/usr/bin/env python

version='8.6.5.1513346799'

import support
from assembler import *
from breakpoints import *
from cache import *
from cfg import *
from commands import *
from firmware import *
from scan import *
from dbudriver import *
from program_file import *
from regs import *
from tlb import *
from tdd import targetdata, target_data, makehd, boardfile, leave
from memory import *
from support import namedstring, require_device
from spram import *
from teams import *
import main
import textfile
from regdb import *
from perfcount import *
from generic_device import *
from sysdumps import *
from sysrestores import *
from trace import *
from calibrate_pdtrace import *
from mt import *
from flash import *
from main import parse_startup_args, init_console
import tdd
from pc_sample import *
from secure_debug import *

__all__ = support.Command.get_globals() + [
    'command', 'namedstring', 'require_device',
    
    # modules that we want to be visible without an import
    'tdd',
    
    # imgtec.console.main things:
    'parse_startup_args', 'init_console',
    
    # legacy name changes
    'asm_bytes', 'dasm_bytes',    
    'configure_tap', 'enter_debug', 'tap_info',
    'tap_ecr', 'tap_data', 'tap_address', 'tap_reg', 'tap_boot',
    
    'list_devices', 'list_vpes',
    'target_data',
    
    'ExecutionState', 'Runstate',
]


if __name__ == "__main__":
    main.main()
