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

import os
import itertools
import shutil
import struct
import sys
import subprocess
from imgtec.console.support import command, named_isas, verifies, updates, verbosity
from imgtec.console.memory import *
from imgtec.codescape.disassembly import Disassembly
from imgtec.codescape.program_file import load_program, Section, NotAnELF, ProgramFileError
from imgtec.lib import filesystem
from textwrap import dedent

branches = "bal beq bge bgt ble blt bne bpo b16 jal jr bt bc1 bc2 bovc bnvc jic jialc".split()

gcc_ases = {
    'mips16' :     '-mips16',
    'mips16e2' :   '--mips16 -mmips16e2',
    'micromips' :  '-mips32r2 -mmicromips -meva',
    'micromips64': '-mips64r2 -mmicromips -meva',
    'micromipsr6': '-mips32r6 -mmicromips -meva',
    'micromips64r6': '-mips64r6 -mmicromips -meva',
    'mips32':      '-mips32r2 -meva',
    'mips32r6':    '-mips32r6 -meva',
    'mips64':      '-mips64r2 -meva',
    'mips64r6':    '-mips64r6 -meva',
    'smart':       '-msmartmips',
    'dsp':         '-mdspr2',
    'mt':          '-mmt',
    'msa':         '-mmsa',
    '3d':          '-mips3d',
    'macro':       '-march=interaptiv-mr2',
    'copy':        '-march=interaptiv-mr2',
}

# This is here for nanoMIPS, names subject to change
gcc_nanomips_ases = {
    'dsp':         '-mdspr3',
    'mt':          '-mmt',
    'nanomips':    '',
    'nms':         '-march=m7000'
}


def isjump(opcode):
    """
    >>> isjump('B')
    True
    >>> isjump('BGEZAL')
    True
    >>> isjump('addui')
    False
    >>> isjump('bitswap')
    False
    >>> isjump('bovc')
    True
    >>> isjump('bnvc')
    True
    >>> isjump('jic')
    True
    >>> isjump('jialc')
    True
    >>> isjump('break')
    False
    >>> isjump('bc')
    True
    """
    op = opcode.lower()
    return op in ('b', 'j', 'bc') or any(op.startswith(x) for x in branches)
    
def is_16bit_isa(isa):
    return not (isa.startswith('mips32') or isa.startswith('mips64'))
    
def is_r6_isa(isa):
    return isa.startswith('mips32r6') or isa.startswith('mips64r6') or \
           isa.startswith('micromipsr6') or isa.startswith('micromips64r6')
    
abis = dict(
# [[[cog
# import sys, os, re
# sys.path.insert(0, os.path.normpath(os.path.join(os.getcwd(), "..", "..")))
# try:
#     import path_config
# except ImportError:
#     pass
# from imgtec.console import asmbytes, dasmbytes
# sys.path.insert(0, os.path.normpath(os.path.join(os.getcwd(), "..", "..", "..", "comms", "comms")))
# import mips_registers
# for abi in ['o32', 'n32', 'n64', 'p32']:
#       cog.outl('%s={' % (abi,))
#       n = 0
#       for r in mips_registers.registers:
#           if r.index < 32 and abi == 'p32': continue
#           name = r.abi_name(abi) or r.alias
#           asmname = r.name
#           asmname = re.sub(r'r(\d+)', r'$\1', asmname)
#           asmname = re.sub(r'cp0\.(\d+)\.(\d+)', r'$\1, 0x\2', asmname)
#           if name and r.name != asmname:
#               cog.out(("'%s':'%s'," % (name.lower(), asmname)).ljust(25))
#               n += 1
#               if (n % 4) == 0:
#                   cog.outl()
#       cog.outl('},')
#
# ]]]
o32={
'zero':'$0',             'at':'$1',               'v0':'$2',               'v1':'$3',               
'a0':'$4',               'a1':'$5',               'a2':'$6',               'a3':'$7',               
't0':'$8',               't1':'$9',               't2':'$10',              't3':'$11',              
't4':'$12',              't5':'$13',              't6':'$14',              't7':'$15',              
's0':'$16',              's1':'$17',              's2':'$18',              's3':'$19',              
's4':'$20',              's5':'$21',              's6':'$22',              's7':'$23',              
't8':'$24',              't9':'$25',              'k0':'$26',              'k1':'$27',              
'gp':'$28',              'sp':'$29',              's8':'$30',              'ra':'$31',              
'index':'$0, 0x0',       'random':'$1, 0x0',      'entrylo0':'$2, 0x0',    'entrylo1':'$3, 0x0',    
'context':'$4, 0x0',     'pagemask':'$5, 0x0',    'wired':'$6, 0x0',       'hwrena':'$7, 0x0',      
'badvaddr':'$8, 0x0',    'count':'$9, 0x0',       'entryhi':'$10, 0x0',    'compare':'$11, 0x0',    
'status':'$12, 0x0',     'cause':'$13, 0x0',      'epc':'$14, 0x0',        'prid':'$15, 0x0',       
'config':'$16, 0x0',     'lladdr':'$17, 0x0',     'watchlo0':'$18, 0x0',   'watchhi0':'$19, 0x0',   
'xcontext':'$20, 0x0',   'debug':'$23, 0x0',      'depc':'$24, 0x0',       'perfctl0':'$25, 0x0',   
'errctl':'$26, 0x0',     'cacheerr':'$27, 0x0',   'itaglo':'$28, 0x0',     'itaghi':'$29, 0x0',     
'errorepc':'$30, 0x0',   'desave':'$31, 0x0',     'mvpcontrol':'$0, 0x1',  'vpecontrol':'$1, 0x1',  
'tcstatus':'$2, 0x1',    'globalnumber':'$3, 0x1','contextconfig':'$4, 0x1','pagegrain':'$5, 0x1',   
'srsconf0':'$6, 0x1',    'badinstr':'$8, 0x1',    'intctl':'$12, 0x1',     'ebase':'$15, 0x1',      
'config1':'$16, 0x1',    'maar':'$17, 0x1',       'watchlo1':'$18, 0x1',   'watchhi1':'$19, 0x1',   
'tracecontrol':'$23, 0x1','perfcnt0':'$25, 0x1',   'ierrctl':'$26, 0x1',    'idatalo':'$28, 0x1',    
'idatahi':'$29, 0x1',    'mvpconf0':'$0, 0x2',    'vpeconf0':'$1, 0x2',    'tcbind':'$2, 0x2',      
'userlocal':'$4, 0x2',   'segctl0':'$5, 0x2',     'srsconf1':'$6, 0x2',    'badinstrp':'$8, 0x2',   
'srsctl':'$12, 0x2',     'cdmmbase':'$15, 0x2',   'config2':'$16, 0x2',    'maari':'$17, 0x2',      
'watchlo2':'$18, 0x2',   'watchhi2':'$19, 0x2',   'tracecontrol2':'$23, 0x2','tracecontrol3':'$24, 0x2',
'perfctl1':'$25, 0x2',   'dtaglo':'$28, 0x2',     'dtaghi':'$29, 0x2',     'kscratch1':'$31, 0x2',  
'mvpconf1':'$0, 0x3',    'vpeconf1':'$1, 0x3',    'tcrestart':'$2, 0x3',   'xcontextconfig':'$4, 0x3',
'segctl1':'$5, 0x3',     'srsconf2':'$6, 0x3',    'srsmap':'$12, 0x3',     'cmgcrbase':'$15, 0x3',  
'config3':'$16, 0x3',    'watchlo3':'$18, 0x3',   'watchhi3':'$19, 0x3',   'usertracedata1':'$23, 0x3',
'usertracedata2':'$24, 0x3','perfcnt1':'$25, 0x3',   'ddatalo':'$28, 0x3',    'ddatahi':'$29, 0x3',    
'kscratch2':'$31, 0x3',  'yqmask':'$1, 0x4',      'tchalt':'$2, 0x4',      'debugcontextid':'$4, 0x4',
'segctl2':'$5, 0x4',     'srsconf3':'$6, 0x4',    'guestctl1':'$10, 0x4',  'view_ipl':'$12, 0x4',   
'view_ripl':'$13, 0x4',  'config4':'$16, 0x4',    'watchlo4':'$18, 0x4',   'watchhi4':'$19, 0x4',   
'traceibpc':'$23, 0x4',  'perfctl2':'$25, 0x4',   'l23taglo':'$28, 0x4',   'kscratch3':'$31, 0x4',  
'vpeschedule':'$1, 0x5', 'tccontext':'$2, 0x5',   'mmid':'$4, 0x5',        'srsconf4':'$6, 0x5',    
'srsmap2':'$12, 0x5',    'config5':'$16, 0x5',    'watchlo5':'$18, 0x5',   'watchhi5':'$19, 0x5',   
'tracedbpc':'$23, 0x5',  'perfcnt2':'$25, 0x5',   'l23datalo':'$28, 0x5',  'l23datahi':'$29, 0x5',  
'kscratch4':'$31, 0x5',  'vpeschefback':'$1, 0x6','tcschedule':'$2, 0x6',  'guestctl0':'$12, 0x6',  
'config6':'$16, 0x6',    'watchlo6':'$18, 0x6',   'watchhi6':'$19, 0x6',   'debug2':'$23, 0x6',     
'perfctl3':'$25, 0x6',   'kscratch5':'$31, 0x6',  'vpeopt':'$1, 0x7',      'tcschefback':'$2, 0x7', 
'tcopt':'$3, 0x7',       'config7':'$16, 0x7',    'watchlo7':'$18, 0x7',   'watchhi7':'$19, 0x7',   
'perfcnt3':'$25, 0x7',   'kscratch6':'$31, 0x7',  'guest_index':'guest_$0, 0x0','guest_random':'guest_$1, 0x0',
'guest_entrylo0':'guest_$2, 0x0','guest_entrylo1':'guest_$3, 0x0','guest_context':'guest_$4, 0x0','guest_pagemask':'guest_$5, 0x0',
'guest_wired':'guest_$6, 0x0','guest_hwrena':'guest_$7, 0x0','guest_badvaddr':'guest_$8, 0x0','guest_count':'guest_$9, 0x0',
'guest_entryhi':'guest_$10, 0x0','guest_compare':'guest_$11, 0x0','guest_status':'guest_$12, 0x0','guest_cause':'guest_$13, 0x0',
'guest_epc':'guest_$14, 0x0','guest_prid':'guest_$15, 0x0','guest_config':'guest_$16, 0x0','guest_lladdr':'guest_$17, 0x0',
'guest_watchlo0':'guest_$18, 0x0','guest_watchhi0':'guest_$19, 0x0','guest_xcontext':'guest_$20, 0x0','guest_debug':'guest_$23, 0x0',
'guest_depc':'guest_$24, 0x0','guest_perfctl0':'guest_$25, 0x0','guest_errctl':'guest_$26, 0x0','guest_cacheerr':'guest_$27, 0x0',
'guest_itaglo':'guest_$28, 0x0','guest_itaghi':'guest_$29, 0x0','guest_errorepc':'guest_$30, 0x0','guest_desave':'guest_$31, 0x0',
'guest_mvpcontrol':'guest_$0, 0x1','guest_vpecontrol':'guest_$1, 0x1','guest_tcstatus':'guest_$2, 0x1','guest_globalnumber':'guest_$3, 0x1',
'guest_contextconfig':'guest_$4, 0x1','guest_pagegrain':'guest_$5, 0x1','guest_srsconf0':'guest_$6, 0x1','guest_badinstr':'guest_$8, 0x1',
'guest_intctl':'guest_$12, 0x1','guest_ebase':'guest_$15, 0x1','guest_config1':'guest_$16, 0x1','guest_maar':'guest_$17, 0x1',
'guest_watchlo1':'guest_$18, 0x1','guest_watchhi1':'guest_$19, 0x1','guest_tracecontrol':'guest_$23, 0x1','guest_perfcnt0':'guest_$25, 0x1',
'guest_ierrctl':'guest_$26, 0x1','guest_idatalo':'guest_$28, 0x1','guest_idatahi':'guest_$29, 0x1','guest_mvpconf0':'guest_$0, 0x2',
'guest_vpeconf0':'guest_$1, 0x2','guest_tcbind':'guest_$2, 0x2','guest_userlocal':'guest_$4, 0x2','guest_segctl0':'guest_$5, 0x2',
'guest_srsconf1':'guest_$6, 0x2','guest_badinstrp':'guest_$8, 0x2','guest_srsctl':'guest_$12, 0x2','guest_cdmmbase':'guest_$15, 0x2',
'guest_config2':'guest_$16, 0x2','guest_maari':'guest_$17, 0x2','guest_watchlo2':'guest_$18, 0x2','guest_watchhi2':'guest_$19, 0x2',
'guest_tracecontrol2':'guest_$23, 0x2','guest_tracecontrol3':'guest_$24, 0x2','guest_perfctl1':'guest_$25, 0x2','guest_dtaglo':'guest_$28, 0x2',
'guest_dtaghi':'guest_$29, 0x2','guest_kscratch1':'guest_$31, 0x2','guest_mvpconf1':'guest_$0, 0x3','guest_vpeconf1':'guest_$1, 0x3',
'guest_tcrestart':'guest_$2, 0x3','guest_xcontextconfig':'guest_$4, 0x3','guest_segctl1':'guest_$5, 0x3','guest_srsconf2':'guest_$6, 0x3',
'guest_srsmap':'guest_$12, 0x3','guest_cmgcrbase':'guest_$15, 0x3','guest_config3':'guest_$16, 0x3','guest_watchlo3':'guest_$18, 0x3',
'guest_watchhi3':'guest_$19, 0x3','guest_usertracedata1':'guest_$23, 0x3','guest_usertracedata2':'guest_$24, 0x3','guest_perfcnt1':'guest_$25, 0x3',
'guest_ddatalo':'guest_$28, 0x3','guest_ddatahi':'guest_$29, 0x3','guest_kscratch2':'guest_$31, 0x3','guest_yqmask':'guest_$1, 0x4',
'guest_tchalt':'guest_$2, 0x4','guest_debugcontextid':'guest_$4, 0x4','guest_segctl2':'guest_$5, 0x4','guest_srsconf3':'guest_$6, 0x4',
'guest_guestctl1':'guest_$10, 0x4','guest_view_ipl':'guest_$12, 0x4','guest_view_ripl':'guest_$13, 0x4','guest_config4':'guest_$16, 0x4',
'guest_watchlo4':'guest_$18, 0x4','guest_watchhi4':'guest_$19, 0x4','guest_traceibpc':'guest_$23, 0x4','guest_perfctl2':'guest_$25, 0x4',
'guest_l23taglo':'guest_$28, 0x4','guest_kscratch3':'guest_$31, 0x4','guest_vpeschedule':'guest_$1, 0x5','guest_tccontext':'guest_$2, 0x5',
'guest_mmid':'guest_$4, 0x5','guest_srsconf4':'guest_$6, 0x5','guest_srsmap2':'guest_$12, 0x5','guest_config5':'guest_$16, 0x5',
'guest_watchlo5':'guest_$18, 0x5','guest_watchhi5':'guest_$19, 0x5','guest_tracedbpc':'guest_$23, 0x5','guest_perfcnt2':'guest_$25, 0x5',
'guest_l23datalo':'guest_$28, 0x5','guest_l23datahi':'guest_$29, 0x5','guest_kscratch4':'guest_$31, 0x5','guest_vpeschefback':'guest_$1, 0x6',
'guest_tcschedule':'guest_$2, 0x6','guest_guestctl0':'guest_$12, 0x6','guest_config6':'guest_$16, 0x6','guest_watchlo6':'guest_$18, 0x6',
'guest_watchhi6':'guest_$19, 0x6','guest_debug2':'guest_$23, 0x6','guest_perfctl3':'guest_$25, 0x6','guest_kscratch5':'guest_$31, 0x6',
'guest_vpeopt':'guest_$1, 0x7','guest_tcschefback':'guest_$2, 0x7','guest_tcopt':'guest_$3, 0x7','guest_config7':'guest_$16, 0x7',
'guest_watchlo7':'guest_$18, 0x7','guest_watchhi7':'guest_$19, 0x7','guest_perfcnt3':'guest_$25, 0x7','guest_kscratch6':'guest_$31, 0x7',
'zero.0':'$0.0',         'at.0':'$1.0',           'v0.0':'$2.0',           'v1.0':'$3.0',           
'a0.0':'$4.0',           'a1.0':'$5.0',           'a2.0':'$6.0',           'a3.0':'$7.0',           
't0.0':'$8.0',           't1.0':'$9.0',           't2.0':'$10.0',          't3.0':'$11.0',          
't4.0':'$12.0',          't5.0':'$13.0',          't6.0':'$14.0',          't7.0':'$15.0',          
's0.0':'$16.0',          's1.0':'$17.0',          's2.0':'$18.0',          's3.0':'$19.0',          
's4.0':'$20.0',          's5.0':'$21.0',          's6.0':'$22.0',          's7.0':'$23.0',          
't8.0':'$24.0',          't9.0':'$25.0',          'k0.0':'$26.0',          'k1.0':'$27.0',          
'gp.0':'$28.0',          'sp.0':'$29.0',          's8.0':'$30.0',          'ra.0':'$31.0',          
'zero.1':'$0.1',         'at.1':'$1.1',           'v0.1':'$2.1',           'v1.1':'$3.1',           
'a0.1':'$4.1',           'a1.1':'$5.1',           'a2.1':'$6.1',           'a3.1':'$7.1',           
't0.1':'$8.1',           't1.1':'$9.1',           't2.1':'$10.1',          't3.1':'$11.1',          
't4.1':'$12.1',          't5.1':'$13.1',          't6.1':'$14.1',          't7.1':'$15.1',          
's0.1':'$16.1',          's1.1':'$17.1',          's2.1':'$18.1',          's3.1':'$19.1',          
's4.1':'$20.1',          's5.1':'$21.1',          's6.1':'$22.1',          's7.1':'$23.1',          
't8.1':'$24.1',          't9.1':'$25.1',          'k0.1':'$26.1',          'k1.1':'$27.1',          
'gp.1':'$28.1',          'sp.1':'$29.1',          's8.1':'$30.1',          'ra.1':'$31.1',          
'zero.2':'$0.2',         'at.2':'$1.2',           'v0.2':'$2.2',           'v1.2':'$3.2',           
'a0.2':'$4.2',           'a1.2':'$5.2',           'a2.2':'$6.2',           'a3.2':'$7.2',           
't0.2':'$8.2',           't1.2':'$9.2',           't2.2':'$10.2',          't3.2':'$11.2',          
't4.2':'$12.2',          't5.2':'$13.2',          't6.2':'$14.2',          't7.2':'$15.2',          
's0.2':'$16.2',          's1.2':'$17.2',          's2.2':'$18.2',          's3.2':'$19.2',          
's4.2':'$20.2',          's5.2':'$21.2',          's6.2':'$22.2',          's7.2':'$23.2',          
't8.2':'$24.2',          't9.2':'$25.2',          'k0.2':'$26.2',          'k1.2':'$27.2',          
'gp.2':'$28.2',          'sp.2':'$29.2',          's8.2':'$30.2',          'ra.2':'$31.2',          
'zero.3':'$0.3',         'at.3':'$1.3',           'v0.3':'$2.3',           'v1.3':'$3.3',           
'a0.3':'$4.3',           'a1.3':'$5.3',           'a2.3':'$6.3',           'a3.3':'$7.3',           
't0.3':'$8.3',           't1.3':'$9.3',           't2.3':'$10.3',          't3.3':'$11.3',          
't4.3':'$12.3',          't5.3':'$13.3',          't6.3':'$14.3',          't7.3':'$15.3',          
's0.3':'$16.3',          's1.3':'$17.3',          's2.3':'$18.3',          's3.3':'$19.3',          
's4.3':'$20.3',          's5.3':'$21.3',          's6.3':'$22.3',          's7.3':'$23.3',          
't8.3':'$24.3',          't9.3':'$25.3',          'k0.3':'$26.3',          'k1.3':'$27.3',          
'gp.3':'$28.3',          'sp.3':'$29.3',          's8.3':'$30.3',          'ra.3':'$31.3',          
'zero.4':'$0.4',         'at.4':'$1.4',           'v0.4':'$2.4',           'v1.4':'$3.4',           
'a0.4':'$4.4',           'a1.4':'$5.4',           'a2.4':'$6.4',           'a3.4':'$7.4',           
't0.4':'$8.4',           't1.4':'$9.4',           't2.4':'$10.4',          't3.4':'$11.4',          
't4.4':'$12.4',          't5.4':'$13.4',          't6.4':'$14.4',          't7.4':'$15.4',          
's0.4':'$16.4',          's1.4':'$17.4',          's2.4':'$18.4',          's3.4':'$19.4',          
's4.4':'$20.4',          's5.4':'$21.4',          's6.4':'$22.4',          's7.4':'$23.4',          
't8.4':'$24.4',          't9.4':'$25.4',          'k0.4':'$26.4',          'k1.4':'$27.4',          
'gp.4':'$28.4',          'sp.4':'$29.4',          's8.4':'$30.4',          'ra.4':'$31.4',          
'zero.5':'$0.5',         'at.5':'$1.5',           'v0.5':'$2.5',           'v1.5':'$3.5',           
'a0.5':'$4.5',           'a1.5':'$5.5',           'a2.5':'$6.5',           'a3.5':'$7.5',           
't0.5':'$8.5',           't1.5':'$9.5',           't2.5':'$10.5',          't3.5':'$11.5',          
't4.5':'$12.5',          't5.5':'$13.5',          't6.5':'$14.5',          't7.5':'$15.5',          
's0.5':'$16.5',          's1.5':'$17.5',          's2.5':'$18.5',          's3.5':'$19.5',          
's4.5':'$20.5',          's5.5':'$21.5',          's6.5':'$22.5',          's7.5':'$23.5',          
't8.5':'$24.5',          't9.5':'$25.5',          'k0.5':'$26.5',          'k1.5':'$27.5',          
'gp.5':'$28.5',          'sp.5':'$29.5',          's8.5':'$30.5',          'ra.5':'$31.5',          
'zero.6':'$0.6',         'at.6':'$1.6',           'v0.6':'$2.6',           'v1.6':'$3.6',           
'a0.6':'$4.6',           'a1.6':'$5.6',           'a2.6':'$6.6',           'a3.6':'$7.6',           
't0.6':'$8.6',           't1.6':'$9.6',           't2.6':'$10.6',          't3.6':'$11.6',          
't4.6':'$12.6',          't5.6':'$13.6',          't6.6':'$14.6',          't7.6':'$15.6',          
's0.6':'$16.6',          's1.6':'$17.6',          's2.6':'$18.6',          's3.6':'$19.6',          
's4.6':'$20.6',          's5.6':'$21.6',          's6.6':'$22.6',          's7.6':'$23.6',          
't8.6':'$24.6',          't9.6':'$25.6',          'k0.6':'$26.6',          'k1.6':'$27.6',          
'gp.6':'$28.6',          'sp.6':'$29.6',          's8.6':'$30.6',          'ra.6':'$31.6',          
'zero.7':'$0.7',         'at.7':'$1.7',           'v0.7':'$2.7',           'v1.7':'$3.7',           
'a0.7':'$4.7',           'a1.7':'$5.7',           'a2.7':'$6.7',           'a3.7':'$7.7',           
't0.7':'$8.7',           't1.7':'$9.7',           't2.7':'$10.7',          't3.7':'$11.7',          
't4.7':'$12.7',          't5.7':'$13.7',          't6.7':'$14.7',          't7.7':'$15.7',          
's0.7':'$16.7',          's1.7':'$17.7',          's2.7':'$18.7',          's3.7':'$19.7',          
's4.7':'$20.7',          's5.7':'$21.7',          's6.7':'$22.7',          's7.7':'$23.7',          
't8.7':'$24.7',          't9.7':'$25.7',          'k0.7':'$26.7',          'k1.7':'$27.7',          
'gp.7':'$28.7',          'sp.7':'$29.7',          's8.7':'$30.7',          'ra.7':'$31.7',          
'zero.8':'$0.8',         'at.8':'$1.8',           'v0.8':'$2.8',           'v1.8':'$3.8',           
'a0.8':'$4.8',           'a1.8':'$5.8',           'a2.8':'$6.8',           'a3.8':'$7.8',           
't0.8':'$8.8',           't1.8':'$9.8',           't2.8':'$10.8',          't3.8':'$11.8',          
't4.8':'$12.8',          't5.8':'$13.8',          't6.8':'$14.8',          't7.8':'$15.8',          
's0.8':'$16.8',          's1.8':'$17.8',          's2.8':'$18.8',          's3.8':'$19.8',          
's4.8':'$20.8',          's5.8':'$21.8',          's6.8':'$22.8',          's7.8':'$23.8',          
't8.8':'$24.8',          't9.8':'$25.8',          'k0.8':'$26.8',          'k1.8':'$27.8',          
'gp.8':'$28.8',          'sp.8':'$29.8',          's8.8':'$30.8',          'ra.8':'$31.8',          
'zero.9':'$0.9',         'at.9':'$1.9',           'v0.9':'$2.9',           'v1.9':'$3.9',           
'a0.9':'$4.9',           'a1.9':'$5.9',           'a2.9':'$6.9',           'a3.9':'$7.9',           
't0.9':'$8.9',           't1.9':'$9.9',           't2.9':'$10.9',          't3.9':'$11.9',          
't4.9':'$12.9',          't5.9':'$13.9',          't6.9':'$14.9',          't7.9':'$15.9',          
's0.9':'$16.9',          's1.9':'$17.9',          's2.9':'$18.9',          's3.9':'$19.9',          
's4.9':'$20.9',          's5.9':'$21.9',          's6.9':'$22.9',          's7.9':'$23.9',          
't8.9':'$24.9',          't9.9':'$25.9',          'k0.9':'$26.9',          'k1.9':'$27.9',          
'gp.9':'$28.9',          'sp.9':'$29.9',          's8.9':'$30.9',          'ra.9':'$31.9',          
'zero.10':'$0.10',       'at.10':'$1.10',         'v0.10':'$2.10',         'v1.10':'$3.10',         
'a0.10':'$4.10',         'a1.10':'$5.10',         'a2.10':'$6.10',         'a3.10':'$7.10',         
't0.10':'$8.10',         't1.10':'$9.10',         't2.10':'$10.10',        't3.10':'$11.10',        
't4.10':'$12.10',        't5.10':'$13.10',        't6.10':'$14.10',        't7.10':'$15.10',        
's0.10':'$16.10',        's1.10':'$17.10',        's2.10':'$18.10',        's3.10':'$19.10',        
's4.10':'$20.10',        's5.10':'$21.10',        's6.10':'$22.10',        's7.10':'$23.10',        
't8.10':'$24.10',        't9.10':'$25.10',        'k0.10':'$26.10',        'k1.10':'$27.10',        
'gp.10':'$28.10',        'sp.10':'$29.10',        's8.10':'$30.10',        'ra.10':'$31.10',        
'zero.11':'$0.11',       'at.11':'$1.11',         'v0.11':'$2.11',         'v1.11':'$3.11',         
'a0.11':'$4.11',         'a1.11':'$5.11',         'a2.11':'$6.11',         'a3.11':'$7.11',         
't0.11':'$8.11',         't1.11':'$9.11',         't2.11':'$10.11',        't3.11':'$11.11',        
't4.11':'$12.11',        't5.11':'$13.11',        't6.11':'$14.11',        't7.11':'$15.11',        
's0.11':'$16.11',        's1.11':'$17.11',        's2.11':'$18.11',        's3.11':'$19.11',        
's4.11':'$20.11',        's5.11':'$21.11',        's6.11':'$22.11',        's7.11':'$23.11',        
't8.11':'$24.11',        't9.11':'$25.11',        'k0.11':'$26.11',        'k1.11':'$27.11',        
'gp.11':'$28.11',        'sp.11':'$29.11',        's8.11':'$30.11',        'ra.11':'$31.11',        
'zero.12':'$0.12',       'at.12':'$1.12',         'v0.12':'$2.12',         'v1.12':'$3.12',         
'a0.12':'$4.12',         'a1.12':'$5.12',         'a2.12':'$6.12',         'a3.12':'$7.12',         
't0.12':'$8.12',         't1.12':'$9.12',         't2.12':'$10.12',        't3.12':'$11.12',        
't4.12':'$12.12',        't5.12':'$13.12',        't6.12':'$14.12',        't7.12':'$15.12',        
's0.12':'$16.12',        's1.12':'$17.12',        's2.12':'$18.12',        's3.12':'$19.12',        
's4.12':'$20.12',        's5.12':'$21.12',        's6.12':'$22.12',        's7.12':'$23.12',        
't8.12':'$24.12',        't9.12':'$25.12',        'k0.12':'$26.12',        'k1.12':'$27.12',        
'gp.12':'$28.12',        'sp.12':'$29.12',        's8.12':'$30.12',        'ra.12':'$31.12',        
'zero.13':'$0.13',       'at.13':'$1.13',         'v0.13':'$2.13',         'v1.13':'$3.13',         
'a0.13':'$4.13',         'a1.13':'$5.13',         'a2.13':'$6.13',         'a3.13':'$7.13',         
't0.13':'$8.13',         't1.13':'$9.13',         't2.13':'$10.13',        't3.13':'$11.13',        
't4.13':'$12.13',        't5.13':'$13.13',        't6.13':'$14.13',        't7.13':'$15.13',        
's0.13':'$16.13',        's1.13':'$17.13',        's2.13':'$18.13',        's3.13':'$19.13',        
's4.13':'$20.13',        's5.13':'$21.13',        's6.13':'$22.13',        's7.13':'$23.13',        
't8.13':'$24.13',        't9.13':'$25.13',        'k0.13':'$26.13',        'k1.13':'$27.13',        
'gp.13':'$28.13',        'sp.13':'$29.13',        's8.13':'$30.13',        'ra.13':'$31.13',        
'zero.14':'$0.14',       'at.14':'$1.14',         'v0.14':'$2.14',         'v1.14':'$3.14',         
'a0.14':'$4.14',         'a1.14':'$5.14',         'a2.14':'$6.14',         'a3.14':'$7.14',         
't0.14':'$8.14',         't1.14':'$9.14',         't2.14':'$10.14',        't3.14':'$11.14',        
't4.14':'$12.14',        't5.14':'$13.14',        't6.14':'$14.14',        't7.14':'$15.14',        
's0.14':'$16.14',        's1.14':'$17.14',        's2.14':'$18.14',        's3.14':'$19.14',        
's4.14':'$20.14',        's5.14':'$21.14',        's6.14':'$22.14',        's7.14':'$23.14',        
't8.14':'$24.14',        't9.14':'$25.14',        'k0.14':'$26.14',        'k1.14':'$27.14',        
'gp.14':'$28.14',        'sp.14':'$29.14',        's8.14':'$30.14',        'ra.14':'$31.14',        
'zero.15':'$0.15',       'at.15':'$1.15',         'v0.15':'$2.15',         'v1.15':'$3.15',         
'a0.15':'$4.15',         'a1.15':'$5.15',         'a2.15':'$6.15',         'a3.15':'$7.15',         
't0.15':'$8.15',         't1.15':'$9.15',         't2.15':'$10.15',        't3.15':'$11.15',        
't4.15':'$12.15',        't5.15':'$13.15',        't6.15':'$14.15',        't7.15':'$15.15',        
's0.15':'$16.15',        's1.15':'$17.15',        's2.15':'$18.15',        's3.15':'$19.15',        
's4.15':'$20.15',        's5.15':'$21.15',        's6.15':'$22.15',        's7.15':'$23.15',        
't8.15':'$24.15',        't9.15':'$25.15',        'k0.15':'$26.15',        'k1.15':'$27.15',        
'gp.15':'$28.15',        'sp.15':'$29.15',        's8.15':'$30.15',        'ra.15':'$31.15',        
},
n32={
'zero':'$0',             'at':'$1',               'v0':'$2',               'v1':'$3',               
'a0':'$4',               'a1':'$5',               'a2':'$6',               'a3':'$7',               
'a4':'$8',               'a5':'$9',               'a6':'$10',              'a7':'$11',              
't0':'$12',              't1':'$13',              't2':'$14',              't3':'$15',              
's0':'$16',              's1':'$17',              's2':'$18',              's3':'$19',              
's4':'$20',              's5':'$21',              's6':'$22',              's7':'$23',              
't8':'$24',              't9':'$25',              'k0':'$26',              'k1':'$27',              
'gp':'$28',              'sp':'$29',              's8':'$30',              'ra':'$31',              
'index':'$0, 0x0',       'random':'$1, 0x0',      'entrylo0':'$2, 0x0',    'entrylo1':'$3, 0x0',    
'context':'$4, 0x0',     'pagemask':'$5, 0x0',    'wired':'$6, 0x0',       'hwrena':'$7, 0x0',      
'badvaddr':'$8, 0x0',    'count':'$9, 0x0',       'entryhi':'$10, 0x0',    'compare':'$11, 0x0',    
'status':'$12, 0x0',     'cause':'$13, 0x0',      'epc':'$14, 0x0',        'prid':'$15, 0x0',       
'config':'$16, 0x0',     'lladdr':'$17, 0x0',     'watchlo0':'$18, 0x0',   'watchhi0':'$19, 0x0',   
'xcontext':'$20, 0x0',   'debug':'$23, 0x0',      'depc':'$24, 0x0',       'perfctl0':'$25, 0x0',   
'errctl':'$26, 0x0',     'cacheerr':'$27, 0x0',   'itaglo':'$28, 0x0',     'itaghi':'$29, 0x0',     
'errorepc':'$30, 0x0',   'desave':'$31, 0x0',     'mvpcontrol':'$0, 0x1',  'vpecontrol':'$1, 0x1',  
'tcstatus':'$2, 0x1',    'globalnumber':'$3, 0x1','contextconfig':'$4, 0x1','pagegrain':'$5, 0x1',   
'srsconf0':'$6, 0x1',    'badinstr':'$8, 0x1',    'intctl':'$12, 0x1',     'ebase':'$15, 0x1',      
'config1':'$16, 0x1',    'maar':'$17, 0x1',       'watchlo1':'$18, 0x1',   'watchhi1':'$19, 0x1',   
'tracecontrol':'$23, 0x1','perfcnt0':'$25, 0x1',   'ierrctl':'$26, 0x1',    'idatalo':'$28, 0x1',    
'idatahi':'$29, 0x1',    'mvpconf0':'$0, 0x2',    'vpeconf0':'$1, 0x2',    'tcbind':'$2, 0x2',      
'userlocal':'$4, 0x2',   'segctl0':'$5, 0x2',     'srsconf1':'$6, 0x2',    'badinstrp':'$8, 0x2',   
'srsctl':'$12, 0x2',     'cdmmbase':'$15, 0x2',   'config2':'$16, 0x2',    'maari':'$17, 0x2',      
'watchlo2':'$18, 0x2',   'watchhi2':'$19, 0x2',   'tracecontrol2':'$23, 0x2','tracecontrol3':'$24, 0x2',
'perfctl1':'$25, 0x2',   'dtaglo':'$28, 0x2',     'dtaghi':'$29, 0x2',     'kscratch1':'$31, 0x2',  
'mvpconf1':'$0, 0x3',    'vpeconf1':'$1, 0x3',    'tcrestart':'$2, 0x3',   'xcontextconfig':'$4, 0x3',
'segctl1':'$5, 0x3',     'srsconf2':'$6, 0x3',    'srsmap':'$12, 0x3',     'cmgcrbase':'$15, 0x3',  
'config3':'$16, 0x3',    'watchlo3':'$18, 0x3',   'watchhi3':'$19, 0x3',   'usertracedata1':'$23, 0x3',
'usertracedata2':'$24, 0x3','perfcnt1':'$25, 0x3',   'ddatalo':'$28, 0x3',    'ddatahi':'$29, 0x3',    
'kscratch2':'$31, 0x3',  'yqmask':'$1, 0x4',      'tchalt':'$2, 0x4',      'debugcontextid':'$4, 0x4',
'segctl2':'$5, 0x4',     'srsconf3':'$6, 0x4',    'guestctl1':'$10, 0x4',  'view_ipl':'$12, 0x4',   
'view_ripl':'$13, 0x4',  'config4':'$16, 0x4',    'watchlo4':'$18, 0x4',   'watchhi4':'$19, 0x4',   
'traceibpc':'$23, 0x4',  'perfctl2':'$25, 0x4',   'l23taglo':'$28, 0x4',   'kscratch3':'$31, 0x4',  
'vpeschedule':'$1, 0x5', 'tccontext':'$2, 0x5',   'mmid':'$4, 0x5',        'srsconf4':'$6, 0x5',    
'srsmap2':'$12, 0x5',    'config5':'$16, 0x5',    'watchlo5':'$18, 0x5',   'watchhi5':'$19, 0x5',   
'tracedbpc':'$23, 0x5',  'perfcnt2':'$25, 0x5',   'l23datalo':'$28, 0x5',  'l23datahi':'$29, 0x5',  
'kscratch4':'$31, 0x5',  'vpeschefback':'$1, 0x6','tcschedule':'$2, 0x6',  'guestctl0':'$12, 0x6',  
'config6':'$16, 0x6',    'watchlo6':'$18, 0x6',   'watchhi6':'$19, 0x6',   'debug2':'$23, 0x6',     
'perfctl3':'$25, 0x6',   'kscratch5':'$31, 0x6',  'vpeopt':'$1, 0x7',      'tcschefback':'$2, 0x7', 
'tcopt':'$3, 0x7',       'config7':'$16, 0x7',    'watchlo7':'$18, 0x7',   'watchhi7':'$19, 0x7',   
'perfcnt3':'$25, 0x7',   'kscratch6':'$31, 0x7',  'guest_index':'guest_$0, 0x0','guest_random':'guest_$1, 0x0',
'guest_entrylo0':'guest_$2, 0x0','guest_entrylo1':'guest_$3, 0x0','guest_context':'guest_$4, 0x0','guest_pagemask':'guest_$5, 0x0',
'guest_wired':'guest_$6, 0x0','guest_hwrena':'guest_$7, 0x0','guest_badvaddr':'guest_$8, 0x0','guest_count':'guest_$9, 0x0',
'guest_entryhi':'guest_$10, 0x0','guest_compare':'guest_$11, 0x0','guest_status':'guest_$12, 0x0','guest_cause':'guest_$13, 0x0',
'guest_epc':'guest_$14, 0x0','guest_prid':'guest_$15, 0x0','guest_config':'guest_$16, 0x0','guest_lladdr':'guest_$17, 0x0',
'guest_watchlo0':'guest_$18, 0x0','guest_watchhi0':'guest_$19, 0x0','guest_xcontext':'guest_$20, 0x0','guest_debug':'guest_$23, 0x0',
'guest_depc':'guest_$24, 0x0','guest_perfctl0':'guest_$25, 0x0','guest_errctl':'guest_$26, 0x0','guest_cacheerr':'guest_$27, 0x0',
'guest_itaglo':'guest_$28, 0x0','guest_itaghi':'guest_$29, 0x0','guest_errorepc':'guest_$30, 0x0','guest_desave':'guest_$31, 0x0',
'guest_mvpcontrol':'guest_$0, 0x1','guest_vpecontrol':'guest_$1, 0x1','guest_tcstatus':'guest_$2, 0x1','guest_globalnumber':'guest_$3, 0x1',
'guest_contextconfig':'guest_$4, 0x1','guest_pagegrain':'guest_$5, 0x1','guest_srsconf0':'guest_$6, 0x1','guest_badinstr':'guest_$8, 0x1',
'guest_intctl':'guest_$12, 0x1','guest_ebase':'guest_$15, 0x1','guest_config1':'guest_$16, 0x1','guest_maar':'guest_$17, 0x1',
'guest_watchlo1':'guest_$18, 0x1','guest_watchhi1':'guest_$19, 0x1','guest_tracecontrol':'guest_$23, 0x1','guest_perfcnt0':'guest_$25, 0x1',
'guest_ierrctl':'guest_$26, 0x1','guest_idatalo':'guest_$28, 0x1','guest_idatahi':'guest_$29, 0x1','guest_mvpconf0':'guest_$0, 0x2',
'guest_vpeconf0':'guest_$1, 0x2','guest_tcbind':'guest_$2, 0x2','guest_userlocal':'guest_$4, 0x2','guest_segctl0':'guest_$5, 0x2',
'guest_srsconf1':'guest_$6, 0x2','guest_badinstrp':'guest_$8, 0x2','guest_srsctl':'guest_$12, 0x2','guest_cdmmbase':'guest_$15, 0x2',
'guest_config2':'guest_$16, 0x2','guest_maari':'guest_$17, 0x2','guest_watchlo2':'guest_$18, 0x2','guest_watchhi2':'guest_$19, 0x2',
'guest_tracecontrol2':'guest_$23, 0x2','guest_tracecontrol3':'guest_$24, 0x2','guest_perfctl1':'guest_$25, 0x2','guest_dtaglo':'guest_$28, 0x2',
'guest_dtaghi':'guest_$29, 0x2','guest_kscratch1':'guest_$31, 0x2','guest_mvpconf1':'guest_$0, 0x3','guest_vpeconf1':'guest_$1, 0x3',
'guest_tcrestart':'guest_$2, 0x3','guest_xcontextconfig':'guest_$4, 0x3','guest_segctl1':'guest_$5, 0x3','guest_srsconf2':'guest_$6, 0x3',
'guest_srsmap':'guest_$12, 0x3','guest_cmgcrbase':'guest_$15, 0x3','guest_config3':'guest_$16, 0x3','guest_watchlo3':'guest_$18, 0x3',
'guest_watchhi3':'guest_$19, 0x3','guest_usertracedata1':'guest_$23, 0x3','guest_usertracedata2':'guest_$24, 0x3','guest_perfcnt1':'guest_$25, 0x3',
'guest_ddatalo':'guest_$28, 0x3','guest_ddatahi':'guest_$29, 0x3','guest_kscratch2':'guest_$31, 0x3','guest_yqmask':'guest_$1, 0x4',
'guest_tchalt':'guest_$2, 0x4','guest_debugcontextid':'guest_$4, 0x4','guest_segctl2':'guest_$5, 0x4','guest_srsconf3':'guest_$6, 0x4',
'guest_guestctl1':'guest_$10, 0x4','guest_view_ipl':'guest_$12, 0x4','guest_view_ripl':'guest_$13, 0x4','guest_config4':'guest_$16, 0x4',
'guest_watchlo4':'guest_$18, 0x4','guest_watchhi4':'guest_$19, 0x4','guest_traceibpc':'guest_$23, 0x4','guest_perfctl2':'guest_$25, 0x4',
'guest_l23taglo':'guest_$28, 0x4','guest_kscratch3':'guest_$31, 0x4','guest_vpeschedule':'guest_$1, 0x5','guest_tccontext':'guest_$2, 0x5',
'guest_mmid':'guest_$4, 0x5','guest_srsconf4':'guest_$6, 0x5','guest_srsmap2':'guest_$12, 0x5','guest_config5':'guest_$16, 0x5',
'guest_watchlo5':'guest_$18, 0x5','guest_watchhi5':'guest_$19, 0x5','guest_tracedbpc':'guest_$23, 0x5','guest_perfcnt2':'guest_$25, 0x5',
'guest_l23datalo':'guest_$28, 0x5','guest_l23datahi':'guest_$29, 0x5','guest_kscratch4':'guest_$31, 0x5','guest_vpeschefback':'guest_$1, 0x6',
'guest_tcschedule':'guest_$2, 0x6','guest_guestctl0':'guest_$12, 0x6','guest_config6':'guest_$16, 0x6','guest_watchlo6':'guest_$18, 0x6',
'guest_watchhi6':'guest_$19, 0x6','guest_debug2':'guest_$23, 0x6','guest_perfctl3':'guest_$25, 0x6','guest_kscratch5':'guest_$31, 0x6',
'guest_vpeopt':'guest_$1, 0x7','guest_tcschefback':'guest_$2, 0x7','guest_tcopt':'guest_$3, 0x7','guest_config7':'guest_$16, 0x7',
'guest_watchlo7':'guest_$18, 0x7','guest_watchhi7':'guest_$19, 0x7','guest_perfcnt3':'guest_$25, 0x7','guest_kscratch6':'guest_$31, 0x7',
'zero.0':'$0.0',         'at.0':'$1.0',           'v0.0':'$2.0',           'v1.0':'$3.0',           
'a0.0':'$4.0',           'a1.0':'$5.0',           'a2.0':'$6.0',           'a3.0':'$7.0',           
'a4.0':'$8.0',           'a5.0':'$9.0',           'a6.0':'$10.0',          'a7.0':'$11.0',          
't0.0':'$12.0',          't1.0':'$13.0',          't2.0':'$14.0',          't3.0':'$15.0',          
's0.0':'$16.0',          's1.0':'$17.0',          's2.0':'$18.0',          's3.0':'$19.0',          
's4.0':'$20.0',          's5.0':'$21.0',          's6.0':'$22.0',          's7.0':'$23.0',          
't8.0':'$24.0',          't9.0':'$25.0',          'k0.0':'$26.0',          'k1.0':'$27.0',          
'gp.0':'$28.0',          'sp.0':'$29.0',          's8.0':'$30.0',          'ra.0':'$31.0',          
'zero.1':'$0.1',         'at.1':'$1.1',           'v0.1':'$2.1',           'v1.1':'$3.1',           
'a0.1':'$4.1',           'a1.1':'$5.1',           'a2.1':'$6.1',           'a3.1':'$7.1',           
'a4.1':'$8.1',           'a5.1':'$9.1',           'a6.1':'$10.1',          'a7.1':'$11.1',          
't0.1':'$12.1',          't1.1':'$13.1',          't2.1':'$14.1',          't3.1':'$15.1',          
's0.1':'$16.1',          's1.1':'$17.1',          's2.1':'$18.1',          's3.1':'$19.1',          
's4.1':'$20.1',          's5.1':'$21.1',          's6.1':'$22.1',          's7.1':'$23.1',          
't8.1':'$24.1',          't9.1':'$25.1',          'k0.1':'$26.1',          'k1.1':'$27.1',          
'gp.1':'$28.1',          'sp.1':'$29.1',          's8.1':'$30.1',          'ra.1':'$31.1',          
'zero.2':'$0.2',         'at.2':'$1.2',           'v0.2':'$2.2',           'v1.2':'$3.2',           
'a0.2':'$4.2',           'a1.2':'$5.2',           'a2.2':'$6.2',           'a3.2':'$7.2',           
'a4.2':'$8.2',           'a5.2':'$9.2',           'a6.2':'$10.2',          'a7.2':'$11.2',          
't0.2':'$12.2',          't1.2':'$13.2',          't2.2':'$14.2',          't3.2':'$15.2',          
's0.2':'$16.2',          's1.2':'$17.2',          's2.2':'$18.2',          's3.2':'$19.2',          
's4.2':'$20.2',          's5.2':'$21.2',          's6.2':'$22.2',          's7.2':'$23.2',          
't8.2':'$24.2',          't9.2':'$25.2',          'k0.2':'$26.2',          'k1.2':'$27.2',          
'gp.2':'$28.2',          'sp.2':'$29.2',          's8.2':'$30.2',          'ra.2':'$31.2',          
'zero.3':'$0.3',         'at.3':'$1.3',           'v0.3':'$2.3',           'v1.3':'$3.3',           
'a0.3':'$4.3',           'a1.3':'$5.3',           'a2.3':'$6.3',           'a3.3':'$7.3',           
'a4.3':'$8.3',           'a5.3':'$9.3',           'a6.3':'$10.3',          'a7.3':'$11.3',          
't0.3':'$12.3',          't1.3':'$13.3',          't2.3':'$14.3',          't3.3':'$15.3',          
's0.3':'$16.3',          's1.3':'$17.3',          's2.3':'$18.3',          's3.3':'$19.3',          
's4.3':'$20.3',          's5.3':'$21.3',          's6.3':'$22.3',          's7.3':'$23.3',          
't8.3':'$24.3',          't9.3':'$25.3',          'k0.3':'$26.3',          'k1.3':'$27.3',          
'gp.3':'$28.3',          'sp.3':'$29.3',          's8.3':'$30.3',          'ra.3':'$31.3',          
'zero.4':'$0.4',         'at.4':'$1.4',           'v0.4':'$2.4',           'v1.4':'$3.4',           
'a0.4':'$4.4',           'a1.4':'$5.4',           'a2.4':'$6.4',           'a3.4':'$7.4',           
'a4.4':'$8.4',           'a5.4':'$9.4',           'a6.4':'$10.4',          'a7.4':'$11.4',          
't0.4':'$12.4',          't1.4':'$13.4',          't2.4':'$14.4',          't3.4':'$15.4',          
's0.4':'$16.4',          's1.4':'$17.4',          's2.4':'$18.4',          's3.4':'$19.4',          
's4.4':'$20.4',          's5.4':'$21.4',          's6.4':'$22.4',          's7.4':'$23.4',          
't8.4':'$24.4',          't9.4':'$25.4',          'k0.4':'$26.4',          'k1.4':'$27.4',          
'gp.4':'$28.4',          'sp.4':'$29.4',          's8.4':'$30.4',          'ra.4':'$31.4',          
'zero.5':'$0.5',         'at.5':'$1.5',           'v0.5':'$2.5',           'v1.5':'$3.5',           
'a0.5':'$4.5',           'a1.5':'$5.5',           'a2.5':'$6.5',           'a3.5':'$7.5',           
'a4.5':'$8.5',           'a5.5':'$9.5',           'a6.5':'$10.5',          'a7.5':'$11.5',          
't0.5':'$12.5',          't1.5':'$13.5',          't2.5':'$14.5',          't3.5':'$15.5',          
's0.5':'$16.5',          's1.5':'$17.5',          's2.5':'$18.5',          's3.5':'$19.5',          
's4.5':'$20.5',          's5.5':'$21.5',          's6.5':'$22.5',          's7.5':'$23.5',          
't8.5':'$24.5',          't9.5':'$25.5',          'k0.5':'$26.5',          'k1.5':'$27.5',          
'gp.5':'$28.5',          'sp.5':'$29.5',          's8.5':'$30.5',          'ra.5':'$31.5',          
'zero.6':'$0.6',         'at.6':'$1.6',           'v0.6':'$2.6',           'v1.6':'$3.6',           
'a0.6':'$4.6',           'a1.6':'$5.6',           'a2.6':'$6.6',           'a3.6':'$7.6',           
'a4.6':'$8.6',           'a5.6':'$9.6',           'a6.6':'$10.6',          'a7.6':'$11.6',          
't0.6':'$12.6',          't1.6':'$13.6',          't2.6':'$14.6',          't3.6':'$15.6',          
's0.6':'$16.6',          's1.6':'$17.6',          's2.6':'$18.6',          's3.6':'$19.6',          
's4.6':'$20.6',          's5.6':'$21.6',          's6.6':'$22.6',          's7.6':'$23.6',          
't8.6':'$24.6',          't9.6':'$25.6',          'k0.6':'$26.6',          'k1.6':'$27.6',          
'gp.6':'$28.6',          'sp.6':'$29.6',          's8.6':'$30.6',          'ra.6':'$31.6',          
'zero.7':'$0.7',         'at.7':'$1.7',           'v0.7':'$2.7',           'v1.7':'$3.7',           
'a0.7':'$4.7',           'a1.7':'$5.7',           'a2.7':'$6.7',           'a3.7':'$7.7',           
'a4.7':'$8.7',           'a5.7':'$9.7',           'a6.7':'$10.7',          'a7.7':'$11.7',          
't0.7':'$12.7',          't1.7':'$13.7',          't2.7':'$14.7',          't3.7':'$15.7',          
's0.7':'$16.7',          's1.7':'$17.7',          's2.7':'$18.7',          's3.7':'$19.7',          
's4.7':'$20.7',          's5.7':'$21.7',          's6.7':'$22.7',          's7.7':'$23.7',          
't8.7':'$24.7',          't9.7':'$25.7',          'k0.7':'$26.7',          'k1.7':'$27.7',          
'gp.7':'$28.7',          'sp.7':'$29.7',          's8.7':'$30.7',          'ra.7':'$31.7',          
'zero.8':'$0.8',         'at.8':'$1.8',           'v0.8':'$2.8',           'v1.8':'$3.8',           
'a0.8':'$4.8',           'a1.8':'$5.8',           'a2.8':'$6.8',           'a3.8':'$7.8',           
'a4.8':'$8.8',           'a5.8':'$9.8',           'a6.8':'$10.8',          'a7.8':'$11.8',          
't0.8':'$12.8',          't1.8':'$13.8',          't2.8':'$14.8',          't3.8':'$15.8',          
's0.8':'$16.8',          's1.8':'$17.8',          's2.8':'$18.8',          's3.8':'$19.8',          
's4.8':'$20.8',          's5.8':'$21.8',          's6.8':'$22.8',          's7.8':'$23.8',          
't8.8':'$24.8',          't9.8':'$25.8',          'k0.8':'$26.8',          'k1.8':'$27.8',          
'gp.8':'$28.8',          'sp.8':'$29.8',          's8.8':'$30.8',          'ra.8':'$31.8',          
'zero.9':'$0.9',         'at.9':'$1.9',           'v0.9':'$2.9',           'v1.9':'$3.9',           
'a0.9':'$4.9',           'a1.9':'$5.9',           'a2.9':'$6.9',           'a3.9':'$7.9',           
'a4.9':'$8.9',           'a5.9':'$9.9',           'a6.9':'$10.9',          'a7.9':'$11.9',          
't0.9':'$12.9',          't1.9':'$13.9',          't2.9':'$14.9',          't3.9':'$15.9',          
's0.9':'$16.9',          's1.9':'$17.9',          's2.9':'$18.9',          's3.9':'$19.9',          
's4.9':'$20.9',          's5.9':'$21.9',          's6.9':'$22.9',          's7.9':'$23.9',          
't8.9':'$24.9',          't9.9':'$25.9',          'k0.9':'$26.9',          'k1.9':'$27.9',          
'gp.9':'$28.9',          'sp.9':'$29.9',          's8.9':'$30.9',          'ra.9':'$31.9',          
'zero.10':'$0.10',       'at.10':'$1.10',         'v0.10':'$2.10',         'v1.10':'$3.10',         
'a0.10':'$4.10',         'a1.10':'$5.10',         'a2.10':'$6.10',         'a3.10':'$7.10',         
'a4.10':'$8.10',         'a5.10':'$9.10',         'a6.10':'$10.10',        'a7.10':'$11.10',        
't0.10':'$12.10',        't1.10':'$13.10',        't2.10':'$14.10',        't3.10':'$15.10',        
's0.10':'$16.10',        's1.10':'$17.10',        's2.10':'$18.10',        's3.10':'$19.10',        
's4.10':'$20.10',        's5.10':'$21.10',        's6.10':'$22.10',        's7.10':'$23.10',        
't8.10':'$24.10',        't9.10':'$25.10',        'k0.10':'$26.10',        'k1.10':'$27.10',        
'gp.10':'$28.10',        'sp.10':'$29.10',        's8.10':'$30.10',        'ra.10':'$31.10',        
'zero.11':'$0.11',       'at.11':'$1.11',         'v0.11':'$2.11',         'v1.11':'$3.11',         
'a0.11':'$4.11',         'a1.11':'$5.11',         'a2.11':'$6.11',         'a3.11':'$7.11',         
'a4.11':'$8.11',         'a5.11':'$9.11',         'a6.11':'$10.11',        'a7.11':'$11.11',        
't0.11':'$12.11',        't1.11':'$13.11',        't2.11':'$14.11',        't3.11':'$15.11',        
's0.11':'$16.11',        's1.11':'$17.11',        's2.11':'$18.11',        's3.11':'$19.11',        
's4.11':'$20.11',        's5.11':'$21.11',        's6.11':'$22.11',        's7.11':'$23.11',        
't8.11':'$24.11',        't9.11':'$25.11',        'k0.11':'$26.11',        'k1.11':'$27.11',        
'gp.11':'$28.11',        'sp.11':'$29.11',        's8.11':'$30.11',        'ra.11':'$31.11',        
'zero.12':'$0.12',       'at.12':'$1.12',         'v0.12':'$2.12',         'v1.12':'$3.12',         
'a0.12':'$4.12',         'a1.12':'$5.12',         'a2.12':'$6.12',         'a3.12':'$7.12',         
'a4.12':'$8.12',         'a5.12':'$9.12',         'a6.12':'$10.12',        'a7.12':'$11.12',        
't0.12':'$12.12',        't1.12':'$13.12',        't2.12':'$14.12',        't3.12':'$15.12',        
's0.12':'$16.12',        's1.12':'$17.12',        's2.12':'$18.12',        's3.12':'$19.12',        
's4.12':'$20.12',        's5.12':'$21.12',        's6.12':'$22.12',        's7.12':'$23.12',        
't8.12':'$24.12',        't9.12':'$25.12',        'k0.12':'$26.12',        'k1.12':'$27.12',        
'gp.12':'$28.12',        'sp.12':'$29.12',        's8.12':'$30.12',        'ra.12':'$31.12',        
'zero.13':'$0.13',       'at.13':'$1.13',         'v0.13':'$2.13',         'v1.13':'$3.13',         
'a0.13':'$4.13',         'a1.13':'$5.13',         'a2.13':'$6.13',         'a3.13':'$7.13',         
'a4.13':'$8.13',         'a5.13':'$9.13',         'a6.13':'$10.13',        'a7.13':'$11.13',        
't0.13':'$12.13',        't1.13':'$13.13',        't2.13':'$14.13',        't3.13':'$15.13',        
's0.13':'$16.13',        's1.13':'$17.13',        's2.13':'$18.13',        's3.13':'$19.13',        
's4.13':'$20.13',        's5.13':'$21.13',        's6.13':'$22.13',        's7.13':'$23.13',        
't8.13':'$24.13',        't9.13':'$25.13',        'k0.13':'$26.13',        'k1.13':'$27.13',        
'gp.13':'$28.13',        'sp.13':'$29.13',        's8.13':'$30.13',        'ra.13':'$31.13',        
'zero.14':'$0.14',       'at.14':'$1.14',         'v0.14':'$2.14',         'v1.14':'$3.14',         
'a0.14':'$4.14',         'a1.14':'$5.14',         'a2.14':'$6.14',         'a3.14':'$7.14',         
'a4.14':'$8.14',         'a5.14':'$9.14',         'a6.14':'$10.14',        'a7.14':'$11.14',        
't0.14':'$12.14',        't1.14':'$13.14',        't2.14':'$14.14',        't3.14':'$15.14',        
's0.14':'$16.14',        's1.14':'$17.14',        's2.14':'$18.14',        's3.14':'$19.14',        
's4.14':'$20.14',        's5.14':'$21.14',        's6.14':'$22.14',        's7.14':'$23.14',        
't8.14':'$24.14',        't9.14':'$25.14',        'k0.14':'$26.14',        'k1.14':'$27.14',        
'gp.14':'$28.14',        'sp.14':'$29.14',        's8.14':'$30.14',        'ra.14':'$31.14',        
'zero.15':'$0.15',       'at.15':'$1.15',         'v0.15':'$2.15',         'v1.15':'$3.15',         
'a0.15':'$4.15',         'a1.15':'$5.15',         'a2.15':'$6.15',         'a3.15':'$7.15',         
'a4.15':'$8.15',         'a5.15':'$9.15',         'a6.15':'$10.15',        'a7.15':'$11.15',        
't0.15':'$12.15',        't1.15':'$13.15',        't2.15':'$14.15',        't3.15':'$15.15',        
's0.15':'$16.15',        's1.15':'$17.15',        's2.15':'$18.15',        's3.15':'$19.15',        
's4.15':'$20.15',        's5.15':'$21.15',        's6.15':'$22.15',        's7.15':'$23.15',        
't8.15':'$24.15',        't9.15':'$25.15',        'k0.15':'$26.15',        'k1.15':'$27.15',        
'gp.15':'$28.15',        'sp.15':'$29.15',        's8.15':'$30.15',        'ra.15':'$31.15',        
},
n64={
'zero':'$0',             'at':'$1',               'v0':'$2',               'v1':'$3',               
'a0':'$4',               'a1':'$5',               'a2':'$6',               'a3':'$7',               
'a4':'$8',               'a5':'$9',               'a6':'$10',              'a7':'$11',              
't0':'$12',              't1':'$13',              't2':'$14',              't3':'$15',              
's0':'$16',              's1':'$17',              's2':'$18',              's3':'$19',              
's4':'$20',              's5':'$21',              's6':'$22',              's7':'$23',              
't8':'$24',              't9':'$25',              'k0':'$26',              'k1':'$27',              
'gp':'$28',              'sp':'$29',              's8':'$30',              'ra':'$31',              
'index':'$0, 0x0',       'random':'$1, 0x0',      'entrylo0':'$2, 0x0',    'entrylo1':'$3, 0x0',    
'context':'$4, 0x0',     'pagemask':'$5, 0x0',    'wired':'$6, 0x0',       'hwrena':'$7, 0x0',      
'badvaddr':'$8, 0x0',    'count':'$9, 0x0',       'entryhi':'$10, 0x0',    'compare':'$11, 0x0',    
'status':'$12, 0x0',     'cause':'$13, 0x0',      'epc':'$14, 0x0',        'prid':'$15, 0x0',       
'config':'$16, 0x0',     'lladdr':'$17, 0x0',     'watchlo0':'$18, 0x0',   'watchhi0':'$19, 0x0',   
'xcontext':'$20, 0x0',   'debug':'$23, 0x0',      'depc':'$24, 0x0',       'perfctl0':'$25, 0x0',   
'errctl':'$26, 0x0',     'cacheerr':'$27, 0x0',   'itaglo':'$28, 0x0',     'itaghi':'$29, 0x0',     
'errorepc':'$30, 0x0',   'desave':'$31, 0x0',     'mvpcontrol':'$0, 0x1',  'vpecontrol':'$1, 0x1',  
'tcstatus':'$2, 0x1',    'globalnumber':'$3, 0x1','contextconfig':'$4, 0x1','pagegrain':'$5, 0x1',   
'srsconf0':'$6, 0x1',    'badinstr':'$8, 0x1',    'intctl':'$12, 0x1',     'ebase':'$15, 0x1',      
'config1':'$16, 0x1',    'maar':'$17, 0x1',       'watchlo1':'$18, 0x1',   'watchhi1':'$19, 0x1',   
'tracecontrol':'$23, 0x1','perfcnt0':'$25, 0x1',   'ierrctl':'$26, 0x1',    'idatalo':'$28, 0x1',    
'idatahi':'$29, 0x1',    'mvpconf0':'$0, 0x2',    'vpeconf0':'$1, 0x2',    'tcbind':'$2, 0x2',      
'userlocal':'$4, 0x2',   'segctl0':'$5, 0x2',     'srsconf1':'$6, 0x2',    'badinstrp':'$8, 0x2',   
'srsctl':'$12, 0x2',     'cdmmbase':'$15, 0x2',   'config2':'$16, 0x2',    'maari':'$17, 0x2',      
'watchlo2':'$18, 0x2',   'watchhi2':'$19, 0x2',   'tracecontrol2':'$23, 0x2','tracecontrol3':'$24, 0x2',
'perfctl1':'$25, 0x2',   'dtaglo':'$28, 0x2',     'dtaghi':'$29, 0x2',     'kscratch1':'$31, 0x2',  
'mvpconf1':'$0, 0x3',    'vpeconf1':'$1, 0x3',    'tcrestart':'$2, 0x3',   'xcontextconfig':'$4, 0x3',
'segctl1':'$5, 0x3',     'srsconf2':'$6, 0x3',    'srsmap':'$12, 0x3',     'cmgcrbase':'$15, 0x3',  
'config3':'$16, 0x3',    'watchlo3':'$18, 0x3',   'watchhi3':'$19, 0x3',   'usertracedata1':'$23, 0x3',
'usertracedata2':'$24, 0x3','perfcnt1':'$25, 0x3',   'ddatalo':'$28, 0x3',    'ddatahi':'$29, 0x3',    
'kscratch2':'$31, 0x3',  'yqmask':'$1, 0x4',      'tchalt':'$2, 0x4',      'debugcontextid':'$4, 0x4',
'segctl2':'$5, 0x4',     'srsconf3':'$6, 0x4',    'guestctl1':'$10, 0x4',  'view_ipl':'$12, 0x4',   
'view_ripl':'$13, 0x4',  'config4':'$16, 0x4',    'watchlo4':'$18, 0x4',   'watchhi4':'$19, 0x4',   
'traceibpc':'$23, 0x4',  'perfctl2':'$25, 0x4',   'l23taglo':'$28, 0x4',   'kscratch3':'$31, 0x4',  
'vpeschedule':'$1, 0x5', 'tccontext':'$2, 0x5',   'mmid':'$4, 0x5',        'srsconf4':'$6, 0x5',    
'srsmap2':'$12, 0x5',    'config5':'$16, 0x5',    'watchlo5':'$18, 0x5',   'watchhi5':'$19, 0x5',   
'tracedbpc':'$23, 0x5',  'perfcnt2':'$25, 0x5',   'l23datalo':'$28, 0x5',  'l23datahi':'$29, 0x5',  
'kscratch4':'$31, 0x5',  'vpeschefback':'$1, 0x6','tcschedule':'$2, 0x6',  'guestctl0':'$12, 0x6',  
'config6':'$16, 0x6',    'watchlo6':'$18, 0x6',   'watchhi6':'$19, 0x6',   'debug2':'$23, 0x6',     
'perfctl3':'$25, 0x6',   'kscratch5':'$31, 0x6',  'vpeopt':'$1, 0x7',      'tcschefback':'$2, 0x7', 
'tcopt':'$3, 0x7',       'config7':'$16, 0x7',    'watchlo7':'$18, 0x7',   'watchhi7':'$19, 0x7',   
'perfcnt3':'$25, 0x7',   'kscratch6':'$31, 0x7',  'guest_index':'guest_$0, 0x0','guest_random':'guest_$1, 0x0',
'guest_entrylo0':'guest_$2, 0x0','guest_entrylo1':'guest_$3, 0x0','guest_context':'guest_$4, 0x0','guest_pagemask':'guest_$5, 0x0',
'guest_wired':'guest_$6, 0x0','guest_hwrena':'guest_$7, 0x0','guest_badvaddr':'guest_$8, 0x0','guest_count':'guest_$9, 0x0',
'guest_entryhi':'guest_$10, 0x0','guest_compare':'guest_$11, 0x0','guest_status':'guest_$12, 0x0','guest_cause':'guest_$13, 0x0',
'guest_epc':'guest_$14, 0x0','guest_prid':'guest_$15, 0x0','guest_config':'guest_$16, 0x0','guest_lladdr':'guest_$17, 0x0',
'guest_watchlo0':'guest_$18, 0x0','guest_watchhi0':'guest_$19, 0x0','guest_xcontext':'guest_$20, 0x0','guest_debug':'guest_$23, 0x0',
'guest_depc':'guest_$24, 0x0','guest_perfctl0':'guest_$25, 0x0','guest_errctl':'guest_$26, 0x0','guest_cacheerr':'guest_$27, 0x0',
'guest_itaglo':'guest_$28, 0x0','guest_itaghi':'guest_$29, 0x0','guest_errorepc':'guest_$30, 0x0','guest_desave':'guest_$31, 0x0',
'guest_mvpcontrol':'guest_$0, 0x1','guest_vpecontrol':'guest_$1, 0x1','guest_tcstatus':'guest_$2, 0x1','guest_globalnumber':'guest_$3, 0x1',
'guest_contextconfig':'guest_$4, 0x1','guest_pagegrain':'guest_$5, 0x1','guest_srsconf0':'guest_$6, 0x1','guest_badinstr':'guest_$8, 0x1',
'guest_intctl':'guest_$12, 0x1','guest_ebase':'guest_$15, 0x1','guest_config1':'guest_$16, 0x1','guest_maar':'guest_$17, 0x1',
'guest_watchlo1':'guest_$18, 0x1','guest_watchhi1':'guest_$19, 0x1','guest_tracecontrol':'guest_$23, 0x1','guest_perfcnt0':'guest_$25, 0x1',
'guest_ierrctl':'guest_$26, 0x1','guest_idatalo':'guest_$28, 0x1','guest_idatahi':'guest_$29, 0x1','guest_mvpconf0':'guest_$0, 0x2',
'guest_vpeconf0':'guest_$1, 0x2','guest_tcbind':'guest_$2, 0x2','guest_userlocal':'guest_$4, 0x2','guest_segctl0':'guest_$5, 0x2',
'guest_srsconf1':'guest_$6, 0x2','guest_badinstrp':'guest_$8, 0x2','guest_srsctl':'guest_$12, 0x2','guest_cdmmbase':'guest_$15, 0x2',
'guest_config2':'guest_$16, 0x2','guest_maari':'guest_$17, 0x2','guest_watchlo2':'guest_$18, 0x2','guest_watchhi2':'guest_$19, 0x2',
'guest_tracecontrol2':'guest_$23, 0x2','guest_tracecontrol3':'guest_$24, 0x2','guest_perfctl1':'guest_$25, 0x2','guest_dtaglo':'guest_$28, 0x2',
'guest_dtaghi':'guest_$29, 0x2','guest_kscratch1':'guest_$31, 0x2','guest_mvpconf1':'guest_$0, 0x3','guest_vpeconf1':'guest_$1, 0x3',
'guest_tcrestart':'guest_$2, 0x3','guest_xcontextconfig':'guest_$4, 0x3','guest_segctl1':'guest_$5, 0x3','guest_srsconf2':'guest_$6, 0x3',
'guest_srsmap':'guest_$12, 0x3','guest_cmgcrbase':'guest_$15, 0x3','guest_config3':'guest_$16, 0x3','guest_watchlo3':'guest_$18, 0x3',
'guest_watchhi3':'guest_$19, 0x3','guest_usertracedata1':'guest_$23, 0x3','guest_usertracedata2':'guest_$24, 0x3','guest_perfcnt1':'guest_$25, 0x3',
'guest_ddatalo':'guest_$28, 0x3','guest_ddatahi':'guest_$29, 0x3','guest_kscratch2':'guest_$31, 0x3','guest_yqmask':'guest_$1, 0x4',
'guest_tchalt':'guest_$2, 0x4','guest_debugcontextid':'guest_$4, 0x4','guest_segctl2':'guest_$5, 0x4','guest_srsconf3':'guest_$6, 0x4',
'guest_guestctl1':'guest_$10, 0x4','guest_view_ipl':'guest_$12, 0x4','guest_view_ripl':'guest_$13, 0x4','guest_config4':'guest_$16, 0x4',
'guest_watchlo4':'guest_$18, 0x4','guest_watchhi4':'guest_$19, 0x4','guest_traceibpc':'guest_$23, 0x4','guest_perfctl2':'guest_$25, 0x4',
'guest_l23taglo':'guest_$28, 0x4','guest_kscratch3':'guest_$31, 0x4','guest_vpeschedule':'guest_$1, 0x5','guest_tccontext':'guest_$2, 0x5',
'guest_mmid':'guest_$4, 0x5','guest_srsconf4':'guest_$6, 0x5','guest_srsmap2':'guest_$12, 0x5','guest_config5':'guest_$16, 0x5',
'guest_watchlo5':'guest_$18, 0x5','guest_watchhi5':'guest_$19, 0x5','guest_tracedbpc':'guest_$23, 0x5','guest_perfcnt2':'guest_$25, 0x5',
'guest_l23datalo':'guest_$28, 0x5','guest_l23datahi':'guest_$29, 0x5','guest_kscratch4':'guest_$31, 0x5','guest_vpeschefback':'guest_$1, 0x6',
'guest_tcschedule':'guest_$2, 0x6','guest_guestctl0':'guest_$12, 0x6','guest_config6':'guest_$16, 0x6','guest_watchlo6':'guest_$18, 0x6',
'guest_watchhi6':'guest_$19, 0x6','guest_debug2':'guest_$23, 0x6','guest_perfctl3':'guest_$25, 0x6','guest_kscratch5':'guest_$31, 0x6',
'guest_vpeopt':'guest_$1, 0x7','guest_tcschefback':'guest_$2, 0x7','guest_tcopt':'guest_$3, 0x7','guest_config7':'guest_$16, 0x7',
'guest_watchlo7':'guest_$18, 0x7','guest_watchhi7':'guest_$19, 0x7','guest_perfcnt3':'guest_$25, 0x7','guest_kscratch6':'guest_$31, 0x7',
'zero.0':'$0.0',         'at.0':'$1.0',           'v0.0':'$2.0',           'v1.0':'$3.0',           
'a0.0':'$4.0',           'a1.0':'$5.0',           'a2.0':'$6.0',           'a3.0':'$7.0',           
'a4.0':'$8.0',           'a5.0':'$9.0',           'a6.0':'$10.0',          'a7.0':'$11.0',          
't0.0':'$12.0',          't1.0':'$13.0',          't2.0':'$14.0',          't3.0':'$15.0',          
's0.0':'$16.0',          's1.0':'$17.0',          's2.0':'$18.0',          's3.0':'$19.0',          
's4.0':'$20.0',          's5.0':'$21.0',          's6.0':'$22.0',          's7.0':'$23.0',          
't8.0':'$24.0',          't9.0':'$25.0',          'k0.0':'$26.0',          'k1.0':'$27.0',          
'gp.0':'$28.0',          'sp.0':'$29.0',          's8.0':'$30.0',          'ra.0':'$31.0',          
'zero.1':'$0.1',         'at.1':'$1.1',           'v0.1':'$2.1',           'v1.1':'$3.1',           
'a0.1':'$4.1',           'a1.1':'$5.1',           'a2.1':'$6.1',           'a3.1':'$7.1',           
'a4.1':'$8.1',           'a5.1':'$9.1',           'a6.1':'$10.1',          'a7.1':'$11.1',          
't0.1':'$12.1',          't1.1':'$13.1',          't2.1':'$14.1',          't3.1':'$15.1',          
's0.1':'$16.1',          's1.1':'$17.1',          's2.1':'$18.1',          's3.1':'$19.1',          
's4.1':'$20.1',          's5.1':'$21.1',          's6.1':'$22.1',          's7.1':'$23.1',          
't8.1':'$24.1',          't9.1':'$25.1',          'k0.1':'$26.1',          'k1.1':'$27.1',          
'gp.1':'$28.1',          'sp.1':'$29.1',          's8.1':'$30.1',          'ra.1':'$31.1',          
'zero.2':'$0.2',         'at.2':'$1.2',           'v0.2':'$2.2',           'v1.2':'$3.2',           
'a0.2':'$4.2',           'a1.2':'$5.2',           'a2.2':'$6.2',           'a3.2':'$7.2',           
'a4.2':'$8.2',           'a5.2':'$9.2',           'a6.2':'$10.2',          'a7.2':'$11.2',          
't0.2':'$12.2',          't1.2':'$13.2',          't2.2':'$14.2',          't3.2':'$15.2',          
's0.2':'$16.2',          's1.2':'$17.2',          's2.2':'$18.2',          's3.2':'$19.2',          
's4.2':'$20.2',          's5.2':'$21.2',          's6.2':'$22.2',          's7.2':'$23.2',          
't8.2':'$24.2',          't9.2':'$25.2',          'k0.2':'$26.2',          'k1.2':'$27.2',          
'gp.2':'$28.2',          'sp.2':'$29.2',          's8.2':'$30.2',          'ra.2':'$31.2',          
'zero.3':'$0.3',         'at.3':'$1.3',           'v0.3':'$2.3',           'v1.3':'$3.3',           
'a0.3':'$4.3',           'a1.3':'$5.3',           'a2.3':'$6.3',           'a3.3':'$7.3',           
'a4.3':'$8.3',           'a5.3':'$9.3',           'a6.3':'$10.3',          'a7.3':'$11.3',          
't0.3':'$12.3',          't1.3':'$13.3',          't2.3':'$14.3',          't3.3':'$15.3',          
's0.3':'$16.3',          's1.3':'$17.3',          's2.3':'$18.3',          's3.3':'$19.3',          
's4.3':'$20.3',          's5.3':'$21.3',          's6.3':'$22.3',          's7.3':'$23.3',          
't8.3':'$24.3',          't9.3':'$25.3',          'k0.3':'$26.3',          'k1.3':'$27.3',          
'gp.3':'$28.3',          'sp.3':'$29.3',          's8.3':'$30.3',          'ra.3':'$31.3',          
'zero.4':'$0.4',         'at.4':'$1.4',           'v0.4':'$2.4',           'v1.4':'$3.4',           
'a0.4':'$4.4',           'a1.4':'$5.4',           'a2.4':'$6.4',           'a3.4':'$7.4',           
'a4.4':'$8.4',           'a5.4':'$9.4',           'a6.4':'$10.4',          'a7.4':'$11.4',          
't0.4':'$12.4',          't1.4':'$13.4',          't2.4':'$14.4',          't3.4':'$15.4',          
's0.4':'$16.4',          's1.4':'$17.4',          's2.4':'$18.4',          's3.4':'$19.4',          
's4.4':'$20.4',          's5.4':'$21.4',          's6.4':'$22.4',          's7.4':'$23.4',          
't8.4':'$24.4',          't9.4':'$25.4',          'k0.4':'$26.4',          'k1.4':'$27.4',          
'gp.4':'$28.4',          'sp.4':'$29.4',          's8.4':'$30.4',          'ra.4':'$31.4',          
'zero.5':'$0.5',         'at.5':'$1.5',           'v0.5':'$2.5',           'v1.5':'$3.5',           
'a0.5':'$4.5',           'a1.5':'$5.5',           'a2.5':'$6.5',           'a3.5':'$7.5',           
'a4.5':'$8.5',           'a5.5':'$9.5',           'a6.5':'$10.5',          'a7.5':'$11.5',          
't0.5':'$12.5',          't1.5':'$13.5',          't2.5':'$14.5',          't3.5':'$15.5',          
's0.5':'$16.5',          's1.5':'$17.5',          's2.5':'$18.5',          's3.5':'$19.5',          
's4.5':'$20.5',          's5.5':'$21.5',          's6.5':'$22.5',          's7.5':'$23.5',          
't8.5':'$24.5',          't9.5':'$25.5',          'k0.5':'$26.5',          'k1.5':'$27.5',          
'gp.5':'$28.5',          'sp.5':'$29.5',          's8.5':'$30.5',          'ra.5':'$31.5',          
'zero.6':'$0.6',         'at.6':'$1.6',           'v0.6':'$2.6',           'v1.6':'$3.6',           
'a0.6':'$4.6',           'a1.6':'$5.6',           'a2.6':'$6.6',           'a3.6':'$7.6',           
'a4.6':'$8.6',           'a5.6':'$9.6',           'a6.6':'$10.6',          'a7.6':'$11.6',          
't0.6':'$12.6',          't1.6':'$13.6',          't2.6':'$14.6',          't3.6':'$15.6',          
's0.6':'$16.6',          's1.6':'$17.6',          's2.6':'$18.6',          's3.6':'$19.6',          
's4.6':'$20.6',          's5.6':'$21.6',          's6.6':'$22.6',          's7.6':'$23.6',          
't8.6':'$24.6',          't9.6':'$25.6',          'k0.6':'$26.6',          'k1.6':'$27.6',          
'gp.6':'$28.6',          'sp.6':'$29.6',          's8.6':'$30.6',          'ra.6':'$31.6',          
'zero.7':'$0.7',         'at.7':'$1.7',           'v0.7':'$2.7',           'v1.7':'$3.7',           
'a0.7':'$4.7',           'a1.7':'$5.7',           'a2.7':'$6.7',           'a3.7':'$7.7',           
'a4.7':'$8.7',           'a5.7':'$9.7',           'a6.7':'$10.7',          'a7.7':'$11.7',          
't0.7':'$12.7',          't1.7':'$13.7',          't2.7':'$14.7',          't3.7':'$15.7',          
's0.7':'$16.7',          's1.7':'$17.7',          's2.7':'$18.7',          's3.7':'$19.7',          
's4.7':'$20.7',          's5.7':'$21.7',          's6.7':'$22.7',          's7.7':'$23.7',          
't8.7':'$24.7',          't9.7':'$25.7',          'k0.7':'$26.7',          'k1.7':'$27.7',          
'gp.7':'$28.7',          'sp.7':'$29.7',          's8.7':'$30.7',          'ra.7':'$31.7',          
'zero.8':'$0.8',         'at.8':'$1.8',           'v0.8':'$2.8',           'v1.8':'$3.8',           
'a0.8':'$4.8',           'a1.8':'$5.8',           'a2.8':'$6.8',           'a3.8':'$7.8',           
'a4.8':'$8.8',           'a5.8':'$9.8',           'a6.8':'$10.8',          'a7.8':'$11.8',          
't0.8':'$12.8',          't1.8':'$13.8',          't2.8':'$14.8',          't3.8':'$15.8',          
's0.8':'$16.8',          's1.8':'$17.8',          's2.8':'$18.8',          's3.8':'$19.8',          
's4.8':'$20.8',          's5.8':'$21.8',          's6.8':'$22.8',          's7.8':'$23.8',          
't8.8':'$24.8',          't9.8':'$25.8',          'k0.8':'$26.8',          'k1.8':'$27.8',          
'gp.8':'$28.8',          'sp.8':'$29.8',          's8.8':'$30.8',          'ra.8':'$31.8',          
'zero.9':'$0.9',         'at.9':'$1.9',           'v0.9':'$2.9',           'v1.9':'$3.9',           
'a0.9':'$4.9',           'a1.9':'$5.9',           'a2.9':'$6.9',           'a3.9':'$7.9',           
'a4.9':'$8.9',           'a5.9':'$9.9',           'a6.9':'$10.9',          'a7.9':'$11.9',          
't0.9':'$12.9',          't1.9':'$13.9',          't2.9':'$14.9',          't3.9':'$15.9',          
's0.9':'$16.9',          's1.9':'$17.9',          's2.9':'$18.9',          's3.9':'$19.9',          
's4.9':'$20.9',          's5.9':'$21.9',          's6.9':'$22.9',          's7.9':'$23.9',          
't8.9':'$24.9',          't9.9':'$25.9',          'k0.9':'$26.9',          'k1.9':'$27.9',          
'gp.9':'$28.9',          'sp.9':'$29.9',          's8.9':'$30.9',          'ra.9':'$31.9',          
'zero.10':'$0.10',       'at.10':'$1.10',         'v0.10':'$2.10',         'v1.10':'$3.10',         
'a0.10':'$4.10',         'a1.10':'$5.10',         'a2.10':'$6.10',         'a3.10':'$7.10',         
'a4.10':'$8.10',         'a5.10':'$9.10',         'a6.10':'$10.10',        'a7.10':'$11.10',        
't0.10':'$12.10',        't1.10':'$13.10',        't2.10':'$14.10',        't3.10':'$15.10',        
's0.10':'$16.10',        's1.10':'$17.10',        's2.10':'$18.10',        's3.10':'$19.10',        
's4.10':'$20.10',        's5.10':'$21.10',        's6.10':'$22.10',        's7.10':'$23.10',        
't8.10':'$24.10',        't9.10':'$25.10',        'k0.10':'$26.10',        'k1.10':'$27.10',        
'gp.10':'$28.10',        'sp.10':'$29.10',        's8.10':'$30.10',        'ra.10':'$31.10',        
'zero.11':'$0.11',       'at.11':'$1.11',         'v0.11':'$2.11',         'v1.11':'$3.11',         
'a0.11':'$4.11',         'a1.11':'$5.11',         'a2.11':'$6.11',         'a3.11':'$7.11',         
'a4.11':'$8.11',         'a5.11':'$9.11',         'a6.11':'$10.11',        'a7.11':'$11.11',        
't0.11':'$12.11',        't1.11':'$13.11',        't2.11':'$14.11',        't3.11':'$15.11',        
's0.11':'$16.11',        's1.11':'$17.11',        's2.11':'$18.11',        's3.11':'$19.11',        
's4.11':'$20.11',        's5.11':'$21.11',        's6.11':'$22.11',        's7.11':'$23.11',        
't8.11':'$24.11',        't9.11':'$25.11',        'k0.11':'$26.11',        'k1.11':'$27.11',        
'gp.11':'$28.11',        'sp.11':'$29.11',        's8.11':'$30.11',        'ra.11':'$31.11',        
'zero.12':'$0.12',       'at.12':'$1.12',         'v0.12':'$2.12',         'v1.12':'$3.12',         
'a0.12':'$4.12',         'a1.12':'$5.12',         'a2.12':'$6.12',         'a3.12':'$7.12',         
'a4.12':'$8.12',         'a5.12':'$9.12',         'a6.12':'$10.12',        'a7.12':'$11.12',        
't0.12':'$12.12',        't1.12':'$13.12',        't2.12':'$14.12',        't3.12':'$15.12',        
's0.12':'$16.12',        's1.12':'$17.12',        's2.12':'$18.12',        's3.12':'$19.12',        
's4.12':'$20.12',        's5.12':'$21.12',        's6.12':'$22.12',        's7.12':'$23.12',        
't8.12':'$24.12',        't9.12':'$25.12',        'k0.12':'$26.12',        'k1.12':'$27.12',        
'gp.12':'$28.12',        'sp.12':'$29.12',        's8.12':'$30.12',        'ra.12':'$31.12',        
'zero.13':'$0.13',       'at.13':'$1.13',         'v0.13':'$2.13',         'v1.13':'$3.13',         
'a0.13':'$4.13',         'a1.13':'$5.13',         'a2.13':'$6.13',         'a3.13':'$7.13',         
'a4.13':'$8.13',         'a5.13':'$9.13',         'a6.13':'$10.13',        'a7.13':'$11.13',        
't0.13':'$12.13',        't1.13':'$13.13',        't2.13':'$14.13',        't3.13':'$15.13',        
's0.13':'$16.13',        's1.13':'$17.13',        's2.13':'$18.13',        's3.13':'$19.13',        
's4.13':'$20.13',        's5.13':'$21.13',        's6.13':'$22.13',        's7.13':'$23.13',        
't8.13':'$24.13',        't9.13':'$25.13',        'k0.13':'$26.13',        'k1.13':'$27.13',        
'gp.13':'$28.13',        'sp.13':'$29.13',        's8.13':'$30.13',        'ra.13':'$31.13',        
'zero.14':'$0.14',       'at.14':'$1.14',         'v0.14':'$2.14',         'v1.14':'$3.14',         
'a0.14':'$4.14',         'a1.14':'$5.14',         'a2.14':'$6.14',         'a3.14':'$7.14',         
'a4.14':'$8.14',         'a5.14':'$9.14',         'a6.14':'$10.14',        'a7.14':'$11.14',        
't0.14':'$12.14',        't1.14':'$13.14',        't2.14':'$14.14',        't3.14':'$15.14',        
's0.14':'$16.14',        's1.14':'$17.14',        's2.14':'$18.14',        's3.14':'$19.14',        
's4.14':'$20.14',        's5.14':'$21.14',        's6.14':'$22.14',        's7.14':'$23.14',        
't8.14':'$24.14',        't9.14':'$25.14',        'k0.14':'$26.14',        'k1.14':'$27.14',        
'gp.14':'$28.14',        'sp.14':'$29.14',        's8.14':'$30.14',        'ra.14':'$31.14',        
'zero.15':'$0.15',       'at.15':'$1.15',         'v0.15':'$2.15',         'v1.15':'$3.15',         
'a0.15':'$4.15',         'a1.15':'$5.15',         'a2.15':'$6.15',         'a3.15':'$7.15',         
'a4.15':'$8.15',         'a5.15':'$9.15',         'a6.15':'$10.15',        'a7.15':'$11.15',        
't0.15':'$12.15',        't1.15':'$13.15',        't2.15':'$14.15',        't3.15':'$15.15',        
's0.15':'$16.15',        's1.15':'$17.15',        's2.15':'$18.15',        's3.15':'$19.15',        
's4.15':'$20.15',        's5.15':'$21.15',        's6.15':'$22.15',        's7.15':'$23.15',        
't8.15':'$24.15',        't9.15':'$25.15',        'k0.15':'$26.15',        'k1.15':'$27.15',        
'gp.15':'$28.15',        'sp.15':'$29.15',        's8.15':'$30.15',        'ra.15':'$31.15',        
},
p32={
'index':'$0, 0x0',       'random':'$1, 0x0',      'entrylo0':'$2, 0x0',    'entrylo1':'$3, 0x0',    
'context':'$4, 0x0',     'pagemask':'$5, 0x0',    'wired':'$6, 0x0',       'hwrena':'$7, 0x0',      
'badvaddr':'$8, 0x0',    'count':'$9, 0x0',       'entryhi':'$10, 0x0',    'compare':'$11, 0x0',    
'status':'$12, 0x0',     'cause':'$13, 0x0',      'epc':'$14, 0x0',        'prid':'$15, 0x0',       
'config':'$16, 0x0',     'lladdr':'$17, 0x0',     'watchlo0':'$18, 0x0',   'watchhi0':'$19, 0x0',   
'xcontext':'$20, 0x0',   'debug':'$23, 0x0',      'depc':'$24, 0x0',       'perfctl0':'$25, 0x0',   
'errctl':'$26, 0x0',     'cacheerr':'$27, 0x0',   'itaglo':'$28, 0x0',     'itaghi':'$29, 0x0',     
'errorepc':'$30, 0x0',   'desave':'$31, 0x0',     'mvpcontrol':'$0, 0x1',  'vpecontrol':'$1, 0x1',  
'tcstatus':'$2, 0x1',    'globalnumber':'$3, 0x1','contextconfig':'$4, 0x1','pagegrain':'$5, 0x1',   
'srsconf0':'$6, 0x1',    'badinstr':'$8, 0x1',    'intctl':'$12, 0x1',     'ebase':'$15, 0x1',      
'config1':'$16, 0x1',    'maar':'$17, 0x1',       'watchlo1':'$18, 0x1',   'watchhi1':'$19, 0x1',   
'tracecontrol':'$23, 0x1','perfcnt0':'$25, 0x1',   'ierrctl':'$26, 0x1',    'idatalo':'$28, 0x1',    
'idatahi':'$29, 0x1',    'mvpconf0':'$0, 0x2',    'vpeconf0':'$1, 0x2',    'tcbind':'$2, 0x2',      
'userlocal':'$4, 0x2',   'segctl0':'$5, 0x2',     'srsconf1':'$6, 0x2',    'badinstrp':'$8, 0x2',   
'srsctl':'$12, 0x2',     'cdmmbase':'$15, 0x2',   'config2':'$16, 0x2',    'maari':'$17, 0x2',      
'watchlo2':'$18, 0x2',   'watchhi2':'$19, 0x2',   'tracecontrol2':'$23, 0x2','tracecontrol3':'$24, 0x2',
'perfctl1':'$25, 0x2',   'dtaglo':'$28, 0x2',     'dtaghi':'$29, 0x2',     'kscratch1':'$31, 0x2',  
'mvpconf1':'$0, 0x3',    'vpeconf1':'$1, 0x3',    'tcrestart':'$2, 0x3',   'xcontextconfig':'$4, 0x3',
'segctl1':'$5, 0x3',     'srsconf2':'$6, 0x3',    'srsmap':'$12, 0x3',     'cmgcrbase':'$15, 0x3',  
'config3':'$16, 0x3',    'watchlo3':'$18, 0x3',   'watchhi3':'$19, 0x3',   'usertracedata1':'$23, 0x3',
'usertracedata2':'$24, 0x3','perfcnt1':'$25, 0x3',   'ddatalo':'$28, 0x3',    'ddatahi':'$29, 0x3',    
'kscratch2':'$31, 0x3',  'yqmask':'$1, 0x4',      'tchalt':'$2, 0x4',      'debugcontextid':'$4, 0x4',
'segctl2':'$5, 0x4',     'srsconf3':'$6, 0x4',    'guestctl1':'$10, 0x4',  'view_ipl':'$12, 0x4',   
'view_ripl':'$13, 0x4',  'config4':'$16, 0x4',    'watchlo4':'$18, 0x4',   'watchhi4':'$19, 0x4',   
'traceibpc':'$23, 0x4',  'perfctl2':'$25, 0x4',   'l23taglo':'$28, 0x4',   'kscratch3':'$31, 0x4',  
'vpeschedule':'$1, 0x5', 'tccontext':'$2, 0x5',   'mmid':'$4, 0x5',        'srsconf4':'$6, 0x5',    
'srsmap2':'$12, 0x5',    'config5':'$16, 0x5',    'watchlo5':'$18, 0x5',   'watchhi5':'$19, 0x5',   
'tracedbpc':'$23, 0x5',  'perfcnt2':'$25, 0x5',   'l23datalo':'$28, 0x5',  'l23datahi':'$29, 0x5',  
'kscratch4':'$31, 0x5',  'vpeschefback':'$1, 0x6','tcschedule':'$2, 0x6',  'guestctl0':'$12, 0x6',  
'config6':'$16, 0x6',    'watchlo6':'$18, 0x6',   'watchhi6':'$19, 0x6',   'debug2':'$23, 0x6',     
'perfctl3':'$25, 0x6',   'kscratch5':'$31, 0x6',  'vpeopt':'$1, 0x7',      'tcschefback':'$2, 0x7', 
'tcopt':'$3, 0x7',       'config7':'$16, 0x7',    'watchlo7':'$18, 0x7',   'watchhi7':'$19, 0x7',   
'perfcnt3':'$25, 0x7',   'kscratch6':'$31, 0x7',  'guest_index':'guest_$0, 0x0','guest_random':'guest_$1, 0x0',
'guest_entrylo0':'guest_$2, 0x0','guest_entrylo1':'guest_$3, 0x0','guest_context':'guest_$4, 0x0','guest_pagemask':'guest_$5, 0x0',
'guest_wired':'guest_$6, 0x0','guest_hwrena':'guest_$7, 0x0','guest_badvaddr':'guest_$8, 0x0','guest_count':'guest_$9, 0x0',
'guest_entryhi':'guest_$10, 0x0','guest_compare':'guest_$11, 0x0','guest_status':'guest_$12, 0x0','guest_cause':'guest_$13, 0x0',
'guest_epc':'guest_$14, 0x0','guest_prid':'guest_$15, 0x0','guest_config':'guest_$16, 0x0','guest_lladdr':'guest_$17, 0x0',
'guest_watchlo0':'guest_$18, 0x0','guest_watchhi0':'guest_$19, 0x0','guest_xcontext':'guest_$20, 0x0','guest_debug':'guest_$23, 0x0',
'guest_depc':'guest_$24, 0x0','guest_perfctl0':'guest_$25, 0x0','guest_errctl':'guest_$26, 0x0','guest_cacheerr':'guest_$27, 0x0',
'guest_itaglo':'guest_$28, 0x0','guest_itaghi':'guest_$29, 0x0','guest_errorepc':'guest_$30, 0x0','guest_desave':'guest_$31, 0x0',
'guest_mvpcontrol':'guest_$0, 0x1','guest_vpecontrol':'guest_$1, 0x1','guest_tcstatus':'guest_$2, 0x1','guest_globalnumber':'guest_$3, 0x1',
'guest_contextconfig':'guest_$4, 0x1','guest_pagegrain':'guest_$5, 0x1','guest_srsconf0':'guest_$6, 0x1','guest_badinstr':'guest_$8, 0x1',
'guest_intctl':'guest_$12, 0x1','guest_ebase':'guest_$15, 0x1','guest_config1':'guest_$16, 0x1','guest_maar':'guest_$17, 0x1',
'guest_watchlo1':'guest_$18, 0x1','guest_watchhi1':'guest_$19, 0x1','guest_tracecontrol':'guest_$23, 0x1','guest_perfcnt0':'guest_$25, 0x1',
'guest_ierrctl':'guest_$26, 0x1','guest_idatalo':'guest_$28, 0x1','guest_idatahi':'guest_$29, 0x1','guest_mvpconf0':'guest_$0, 0x2',
'guest_vpeconf0':'guest_$1, 0x2','guest_tcbind':'guest_$2, 0x2','guest_userlocal':'guest_$4, 0x2','guest_segctl0':'guest_$5, 0x2',
'guest_srsconf1':'guest_$6, 0x2','guest_badinstrp':'guest_$8, 0x2','guest_srsctl':'guest_$12, 0x2','guest_cdmmbase':'guest_$15, 0x2',
'guest_config2':'guest_$16, 0x2','guest_maari':'guest_$17, 0x2','guest_watchlo2':'guest_$18, 0x2','guest_watchhi2':'guest_$19, 0x2',
'guest_tracecontrol2':'guest_$23, 0x2','guest_tracecontrol3':'guest_$24, 0x2','guest_perfctl1':'guest_$25, 0x2','guest_dtaglo':'guest_$28, 0x2',
'guest_dtaghi':'guest_$29, 0x2','guest_kscratch1':'guest_$31, 0x2','guest_mvpconf1':'guest_$0, 0x3','guest_vpeconf1':'guest_$1, 0x3',
'guest_tcrestart':'guest_$2, 0x3','guest_xcontextconfig':'guest_$4, 0x3','guest_segctl1':'guest_$5, 0x3','guest_srsconf2':'guest_$6, 0x3',
'guest_srsmap':'guest_$12, 0x3','guest_cmgcrbase':'guest_$15, 0x3','guest_config3':'guest_$16, 0x3','guest_watchlo3':'guest_$18, 0x3',
'guest_watchhi3':'guest_$19, 0x3','guest_usertracedata1':'guest_$23, 0x3','guest_usertracedata2':'guest_$24, 0x3','guest_perfcnt1':'guest_$25, 0x3',
'guest_ddatalo':'guest_$28, 0x3','guest_ddatahi':'guest_$29, 0x3','guest_kscratch2':'guest_$31, 0x3','guest_yqmask':'guest_$1, 0x4',
'guest_tchalt':'guest_$2, 0x4','guest_debugcontextid':'guest_$4, 0x4','guest_segctl2':'guest_$5, 0x4','guest_srsconf3':'guest_$6, 0x4',
'guest_guestctl1':'guest_$10, 0x4','guest_view_ipl':'guest_$12, 0x4','guest_view_ripl':'guest_$13, 0x4','guest_config4':'guest_$16, 0x4',
'guest_watchlo4':'guest_$18, 0x4','guest_watchhi4':'guest_$19, 0x4','guest_traceibpc':'guest_$23, 0x4','guest_perfctl2':'guest_$25, 0x4',
'guest_l23taglo':'guest_$28, 0x4','guest_kscratch3':'guest_$31, 0x4','guest_vpeschedule':'guest_$1, 0x5','guest_tccontext':'guest_$2, 0x5',
'guest_mmid':'guest_$4, 0x5','guest_srsconf4':'guest_$6, 0x5','guest_srsmap2':'guest_$12, 0x5','guest_config5':'guest_$16, 0x5',
'guest_watchlo5':'guest_$18, 0x5','guest_watchhi5':'guest_$19, 0x5','guest_tracedbpc':'guest_$23, 0x5','guest_perfcnt2':'guest_$25, 0x5',
'guest_l23datalo':'guest_$28, 0x5','guest_l23datahi':'guest_$29, 0x5','guest_kscratch4':'guest_$31, 0x5','guest_vpeschefback':'guest_$1, 0x6',
'guest_tcschedule':'guest_$2, 0x6','guest_guestctl0':'guest_$12, 0x6','guest_config6':'guest_$16, 0x6','guest_watchlo6':'guest_$18, 0x6',
'guest_watchhi6':'guest_$19, 0x6','guest_debug2':'guest_$23, 0x6','guest_perfctl3':'guest_$25, 0x6','guest_kscratch5':'guest_$31, 0x6',
'guest_vpeopt':'guest_$1, 0x7','guest_tcschefback':'guest_$2, 0x7','guest_tcopt':'guest_$3, 0x7','guest_config7':'guest_$16, 0x7',
'guest_watchlo7':'guest_$18, 0x7','guest_watchhi7':'guest_$19, 0x7','guest_perfcnt3':'guest_$25, 0x7','guest_kscratch6':'guest_$31, 0x7',
'zero.0':'$0.0',         'at.0':'$1.0',           't4.0':'$2.0',           't5.0':'$3.0',           
'a0.0':'$4.0',           'a1.0':'$5.0',           'a2.0':'$6.0',           'a3.0':'$7.0',           
'a4.0':'$8.0',           'a5.0':'$9.0',           'a6.0':'$10.0',          'a7.0':'$11.0',          
't0.0':'$12.0',          't1.0':'$13.0',          't2.0':'$14.0',          't3.0':'$15.0',          
's0.0':'$16.0',          's1.0':'$17.0',          's2.0':'$18.0',          's3.0':'$19.0',          
's4.0':'$20.0',          's5.0':'$21.0',          's6.0':'$22.0',          's7.0':'$23.0',          
't8.0':'$24.0',          't9.0':'$25.0',          'k0.0':'$26.0',          'k1.0':'$27.0',          
'gp.0':'$28.0',          'sp.0':'$29.0',          'fp.0':'$30.0',          'ra.0':'$31.0',          
'zero.1':'$0.1',         'at.1':'$1.1',           't4.1':'$2.1',           't5.1':'$3.1',           
'a0.1':'$4.1',           'a1.1':'$5.1',           'a2.1':'$6.1',           'a3.1':'$7.1',           
'a4.1':'$8.1',           'a5.1':'$9.1',           'a6.1':'$10.1',          'a7.1':'$11.1',          
't0.1':'$12.1',          't1.1':'$13.1',          't2.1':'$14.1',          't3.1':'$15.1',          
's0.1':'$16.1',          's1.1':'$17.1',          's2.1':'$18.1',          's3.1':'$19.1',          
's4.1':'$20.1',          's5.1':'$21.1',          's6.1':'$22.1',          's7.1':'$23.1',          
't8.1':'$24.1',          't9.1':'$25.1',          'k0.1':'$26.1',          'k1.1':'$27.1',          
'gp.1':'$28.1',          'sp.1':'$29.1',          'fp.1':'$30.1',          'ra.1':'$31.1',          
'zero.2':'$0.2',         'at.2':'$1.2',           't4.2':'$2.2',           't5.2':'$3.2',           
'a0.2':'$4.2',           'a1.2':'$5.2',           'a2.2':'$6.2',           'a3.2':'$7.2',           
'a4.2':'$8.2',           'a5.2':'$9.2',           'a6.2':'$10.2',          'a7.2':'$11.2',          
't0.2':'$12.2',          't1.2':'$13.2',          't2.2':'$14.2',          't3.2':'$15.2',          
's0.2':'$16.2',          's1.2':'$17.2',          's2.2':'$18.2',          's3.2':'$19.2',          
's4.2':'$20.2',          's5.2':'$21.2',          's6.2':'$22.2',          's7.2':'$23.2',          
't8.2':'$24.2',          't9.2':'$25.2',          'k0.2':'$26.2',          'k1.2':'$27.2',          
'gp.2':'$28.2',          'sp.2':'$29.2',          'fp.2':'$30.2',          'ra.2':'$31.2',          
'zero.3':'$0.3',         'at.3':'$1.3',           't4.3':'$2.3',           't5.3':'$3.3',           
'a0.3':'$4.3',           'a1.3':'$5.3',           'a2.3':'$6.3',           'a3.3':'$7.3',           
'a4.3':'$8.3',           'a5.3':'$9.3',           'a6.3':'$10.3',          'a7.3':'$11.3',          
't0.3':'$12.3',          't1.3':'$13.3',          't2.3':'$14.3',          't3.3':'$15.3',          
's0.3':'$16.3',          's1.3':'$17.3',          's2.3':'$18.3',          's3.3':'$19.3',          
's4.3':'$20.3',          's5.3':'$21.3',          's6.3':'$22.3',          's7.3':'$23.3',          
't8.3':'$24.3',          't9.3':'$25.3',          'k0.3':'$26.3',          'k1.3':'$27.3',          
'gp.3':'$28.3',          'sp.3':'$29.3',          'fp.3':'$30.3',          'ra.3':'$31.3',          
'zero.4':'$0.4',         'at.4':'$1.4',           't4.4':'$2.4',           't5.4':'$3.4',           
'a0.4':'$4.4',           'a1.4':'$5.4',           'a2.4':'$6.4',           'a3.4':'$7.4',           
'a4.4':'$8.4',           'a5.4':'$9.4',           'a6.4':'$10.4',          'a7.4':'$11.4',          
't0.4':'$12.4',          't1.4':'$13.4',          't2.4':'$14.4',          't3.4':'$15.4',          
's0.4':'$16.4',          's1.4':'$17.4',          's2.4':'$18.4',          's3.4':'$19.4',          
's4.4':'$20.4',          's5.4':'$21.4',          's6.4':'$22.4',          's7.4':'$23.4',          
't8.4':'$24.4',          't9.4':'$25.4',          'k0.4':'$26.4',          'k1.4':'$27.4',          
'gp.4':'$28.4',          'sp.4':'$29.4',          'fp.4':'$30.4',          'ra.4':'$31.4',          
'zero.5':'$0.5',         'at.5':'$1.5',           't4.5':'$2.5',           't5.5':'$3.5',           
'a0.5':'$4.5',           'a1.5':'$5.5',           'a2.5':'$6.5',           'a3.5':'$7.5',           
'a4.5':'$8.5',           'a5.5':'$9.5',           'a6.5':'$10.5',          'a7.5':'$11.5',          
't0.5':'$12.5',          't1.5':'$13.5',          't2.5':'$14.5',          't3.5':'$15.5',          
's0.5':'$16.5',          's1.5':'$17.5',          's2.5':'$18.5',          's3.5':'$19.5',          
's4.5':'$20.5',          's5.5':'$21.5',          's6.5':'$22.5',          's7.5':'$23.5',          
't8.5':'$24.5',          't9.5':'$25.5',          'k0.5':'$26.5',          'k1.5':'$27.5',          
'gp.5':'$28.5',          'sp.5':'$29.5',          'fp.5':'$30.5',          'ra.5':'$31.5',          
'zero.6':'$0.6',         'at.6':'$1.6',           't4.6':'$2.6',           't5.6':'$3.6',           
'a0.6':'$4.6',           'a1.6':'$5.6',           'a2.6':'$6.6',           'a3.6':'$7.6',           
'a4.6':'$8.6',           'a5.6':'$9.6',           'a6.6':'$10.6',          'a7.6':'$11.6',          
't0.6':'$12.6',          't1.6':'$13.6',          't2.6':'$14.6',          't3.6':'$15.6',          
's0.6':'$16.6',          's1.6':'$17.6',          's2.6':'$18.6',          's3.6':'$19.6',          
's4.6':'$20.6',          's5.6':'$21.6',          's6.6':'$22.6',          's7.6':'$23.6',          
't8.6':'$24.6',          't9.6':'$25.6',          'k0.6':'$26.6',          'k1.6':'$27.6',          
'gp.6':'$28.6',          'sp.6':'$29.6',          'fp.6':'$30.6',          'ra.6':'$31.6',          
'zero.7':'$0.7',         'at.7':'$1.7',           't4.7':'$2.7',           't5.7':'$3.7',           
'a0.7':'$4.7',           'a1.7':'$5.7',           'a2.7':'$6.7',           'a3.7':'$7.7',           
'a4.7':'$8.7',           'a5.7':'$9.7',           'a6.7':'$10.7',          'a7.7':'$11.7',          
't0.7':'$12.7',          't1.7':'$13.7',          't2.7':'$14.7',          't3.7':'$15.7',          
's0.7':'$16.7',          's1.7':'$17.7',          's2.7':'$18.7',          's3.7':'$19.7',          
's4.7':'$20.7',          's5.7':'$21.7',          's6.7':'$22.7',          's7.7':'$23.7',          
't8.7':'$24.7',          't9.7':'$25.7',          'k0.7':'$26.7',          'k1.7':'$27.7',          
'gp.7':'$28.7',          'sp.7':'$29.7',          'fp.7':'$30.7',          'ra.7':'$31.7',          
'zero.8':'$0.8',         'at.8':'$1.8',           't4.8':'$2.8',           't5.8':'$3.8',           
'a0.8':'$4.8',           'a1.8':'$5.8',           'a2.8':'$6.8',           'a3.8':'$7.8',           
'a4.8':'$8.8',           'a5.8':'$9.8',           'a6.8':'$10.8',          'a7.8':'$11.8',          
't0.8':'$12.8',          't1.8':'$13.8',          't2.8':'$14.8',          't3.8':'$15.8',          
's0.8':'$16.8',          's1.8':'$17.8',          's2.8':'$18.8',          's3.8':'$19.8',          
's4.8':'$20.8',          's5.8':'$21.8',          's6.8':'$22.8',          's7.8':'$23.8',          
't8.8':'$24.8',          't9.8':'$25.8',          'k0.8':'$26.8',          'k1.8':'$27.8',          
'gp.8':'$28.8',          'sp.8':'$29.8',          'fp.8':'$30.8',          'ra.8':'$31.8',          
'zero.9':'$0.9',         'at.9':'$1.9',           't4.9':'$2.9',           't5.9':'$3.9',           
'a0.9':'$4.9',           'a1.9':'$5.9',           'a2.9':'$6.9',           'a3.9':'$7.9',           
'a4.9':'$8.9',           'a5.9':'$9.9',           'a6.9':'$10.9',          'a7.9':'$11.9',          
't0.9':'$12.9',          't1.9':'$13.9',          't2.9':'$14.9',          't3.9':'$15.9',          
's0.9':'$16.9',          's1.9':'$17.9',          's2.9':'$18.9',          's3.9':'$19.9',          
's4.9':'$20.9',          's5.9':'$21.9',          's6.9':'$22.9',          's7.9':'$23.9',          
't8.9':'$24.9',          't9.9':'$25.9',          'k0.9':'$26.9',          'k1.9':'$27.9',          
'gp.9':'$28.9',          'sp.9':'$29.9',          'fp.9':'$30.9',          'ra.9':'$31.9',          
'zero.10':'$0.10',       'at.10':'$1.10',         't4.10':'$2.10',         't5.10':'$3.10',         
'a0.10':'$4.10',         'a1.10':'$5.10',         'a2.10':'$6.10',         'a3.10':'$7.10',         
'a4.10':'$8.10',         'a5.10':'$9.10',         'a6.10':'$10.10',        'a7.10':'$11.10',        
't0.10':'$12.10',        't1.10':'$13.10',        't2.10':'$14.10',        't3.10':'$15.10',        
's0.10':'$16.10',        's1.10':'$17.10',        's2.10':'$18.10',        's3.10':'$19.10',        
's4.10':'$20.10',        's5.10':'$21.10',        's6.10':'$22.10',        's7.10':'$23.10',        
't8.10':'$24.10',        't9.10':'$25.10',        'k0.10':'$26.10',        'k1.10':'$27.10',        
'gp.10':'$28.10',        'sp.10':'$29.10',        'fp.10':'$30.10',        'ra.10':'$31.10',        
'zero.11':'$0.11',       'at.11':'$1.11',         't4.11':'$2.11',         't5.11':'$3.11',         
'a0.11':'$4.11',         'a1.11':'$5.11',         'a2.11':'$6.11',         'a3.11':'$7.11',         
'a4.11':'$8.11',         'a5.11':'$9.11',         'a6.11':'$10.11',        'a7.11':'$11.11',        
't0.11':'$12.11',        't1.11':'$13.11',        't2.11':'$14.11',        't3.11':'$15.11',        
's0.11':'$16.11',        's1.11':'$17.11',        's2.11':'$18.11',        's3.11':'$19.11',        
's4.11':'$20.11',        's5.11':'$21.11',        's6.11':'$22.11',        's7.11':'$23.11',        
't8.11':'$24.11',        't9.11':'$25.11',        'k0.11':'$26.11',        'k1.11':'$27.11',        
'gp.11':'$28.11',        'sp.11':'$29.11',        'fp.11':'$30.11',        'ra.11':'$31.11',        
'zero.12':'$0.12',       'at.12':'$1.12',         't4.12':'$2.12',         't5.12':'$3.12',         
'a0.12':'$4.12',         'a1.12':'$5.12',         'a2.12':'$6.12',         'a3.12':'$7.12',         
'a4.12':'$8.12',         'a5.12':'$9.12',         'a6.12':'$10.12',        'a7.12':'$11.12',        
't0.12':'$12.12',        't1.12':'$13.12',        't2.12':'$14.12',        't3.12':'$15.12',        
's0.12':'$16.12',        's1.12':'$17.12',        's2.12':'$18.12',        's3.12':'$19.12',        
's4.12':'$20.12',        's5.12':'$21.12',        's6.12':'$22.12',        's7.12':'$23.12',        
't8.12':'$24.12',        't9.12':'$25.12',        'k0.12':'$26.12',        'k1.12':'$27.12',        
'gp.12':'$28.12',        'sp.12':'$29.12',        'fp.12':'$30.12',        'ra.12':'$31.12',        
'zero.13':'$0.13',       'at.13':'$1.13',         't4.13':'$2.13',         't5.13':'$3.13',         
'a0.13':'$4.13',         'a1.13':'$5.13',         'a2.13':'$6.13',         'a3.13':'$7.13',         
'a4.13':'$8.13',         'a5.13':'$9.13',         'a6.13':'$10.13',        'a7.13':'$11.13',        
't0.13':'$12.13',        't1.13':'$13.13',        't2.13':'$14.13',        't3.13':'$15.13',        
's0.13':'$16.13',        's1.13':'$17.13',        's2.13':'$18.13',        's3.13':'$19.13',        
's4.13':'$20.13',        's5.13':'$21.13',        's6.13':'$22.13',        's7.13':'$23.13',        
't8.13':'$24.13',        't9.13':'$25.13',        'k0.13':'$26.13',        'k1.13':'$27.13',        
'gp.13':'$28.13',        'sp.13':'$29.13',        'fp.13':'$30.13',        'ra.13':'$31.13',        
'zero.14':'$0.14',       'at.14':'$1.14',         't4.14':'$2.14',         't5.14':'$3.14',         
'a0.14':'$4.14',         'a1.14':'$5.14',         'a2.14':'$6.14',         'a3.14':'$7.14',         
'a4.14':'$8.14',         'a5.14':'$9.14',         'a6.14':'$10.14',        'a7.14':'$11.14',        
't0.14':'$12.14',        't1.14':'$13.14',        't2.14':'$14.14',        't3.14':'$15.14',        
's0.14':'$16.14',        's1.14':'$17.14',        's2.14':'$18.14',        's3.14':'$19.14',        
's4.14':'$20.14',        's5.14':'$21.14',        's6.14':'$22.14',        's7.14':'$23.14',        
't8.14':'$24.14',        't9.14':'$25.14',        'k0.14':'$26.14',        'k1.14':'$27.14',        
'gp.14':'$28.14',        'sp.14':'$29.14',        'fp.14':'$30.14',        'ra.14':'$31.14',        
'zero.15':'$0.15',       'at.15':'$1.15',         't4.15':'$2.15',         't5.15':'$3.15',         
'a0.15':'$4.15',         'a1.15':'$5.15',         'a2.15':'$6.15',         'a3.15':'$7.15',         
'a4.15':'$8.15',         'a5.15':'$9.15',         'a6.15':'$10.15',        'a7.15':'$11.15',        
't0.15':'$12.15',        't1.15':'$13.15',        't2.15':'$14.15',        't3.15':'$15.15',        
's0.15':'$16.15',        's1.15':'$17.15',        's2.15':'$18.15',        's3.15':'$19.15',        
's4.15':'$20.15',        's5.15':'$21.15',        's6.15':'$22.15',        's7.15':'$23.15',        
't8.15':'$24.15',        't9.15':'$25.15',        'k0.15':'$26.15',        'k1.15':'$27.15',        
'gp.15':'$28.15',        'sp.15':'$29.15',        'fp.15':'$30.15',        'ra.15':'$31.15',        
},
# [[[end]]]
)
    
def get_asm_contents(address, text, isa, abi='o32'):
    r"""Generate the contents of an .s file for as.  
    
    Returns (syms, contents, start_address) where syms is a dictionary of symbol to address
    for the linker, and address is the start_address of the generated sequence.  
    `start_address` may be different from address if a padding sdbbp was required on an 'odd'
    address 16-bit isa.
    
    >>> syms, contents, address = get_asm_contents(0x80000004, 'b 0x80000000', 'mips32')
    >>> [(s, '0x%08x' % x) for s, x in syms.items()]
    [('GNUASM0', '0x80000000')]
    >>> contents
    '.text\n.set noat\n.set noreorder\n_start:\nb GNUASM0\n'
    >>> '0x%08x' % (address,)
    '0x80000004'
    >>> get_asm_contents(0x80000004, 'lui 0x80000000, $0', 'mips32',)[1]
    '.text\n.set noat\n.set noreorder\n_start:\nlui 0x80000000, $0\n'
    >>> '0x%08x' % get_asm_contents(0x80000004, 'lui 0x80000000, $0', 'mips32',)[2]
    '0x80000004'
    >>> get_asm_contents(0x80000002, 'lui 0x80000000, $0', 'mips16')[1]
    '.text\n.set noat\n.set noreorder\nsdbbp\n_start:\nlui 0x80000000, $0\n'
    >>> get_asm_contents(0x80000002, 'lui 0x80000000, $at', 'mips16')[1]
    '.text\n.set noat\n.set noreorder\nsdbbp\n_start:\nlui 0x80000000, $at\n'
    >>> get_asm_contents(0x80000002, 'lui 0x80000000, AT', 'mips16')[1]
    '.text\n.set noat\n.set noreorder\nsdbbp\n_start:\nlui 0x80000000, $1\n'
    >>> get_asm_contents(0x80000002, 'lui 0x80000000, at', 'mips16')[1]
    '.text\n.set noat\n.set noreorder\nsdbbp\n_start:\nlui 0x80000000, $1\n'
    >>> '0x%08x' % get_asm_contents(0x80000002, 'lui 0x80000000, $0', 'mips16')[2]
    '0x80000000'
    >>> input = '''\
    ...     addu $2, $3, $4
    ... Add:
    ...     nop
    ...     b 0x80000000
    ...     addu $2, $3, $4
    ...     b Add
    ...     nop
    ...     b 0xDEADBEEF
    ...     nop'''
    >>> f = get_asm_contents(0x80000000, input, 'mips32')
    >>> sorted([(s[0], '0x%08x' % s[1]) for s in f[0].iteritems()])
    [('GNUASM0', '0x80000000'), ('GNUASM1', '0xdeadbeef')]
    >>> for line in f[1].splitlines():
    ...    print line
    .text
    .set noat
    .set noreorder
    _start:
    addu $2, $3, $4
    Add: 
    nop 
    b GNUASM0
    addu $2, $3, $4
    b Add
    nop 
    b GNUASM1
    nop 
    """
    lines = [".text", ".set noat", ".set noreorder"]
    syms = {}
    arg_num = 0

    # If micromips/mips16 on an odd halfword boundary, pad with a
    # preceding sdbbp and adjust address down by 2.  Sdbbp will be stripped
    # later.
    if is_16bit_isa(isa) and address & 2:
        address -= 2
        lines.append("sdbbp")
    lines.append('_start:')

    for text in text.splitlines():        
        # Replace each numeric constant branches with an internal constant
        # and then specify the constant in the ld command line.  This
        # is necessary to get branch addresses resolved correctly.
        text = text.strip()
        
        if not text:
            continue
        
        if ' ' in text or '\t' in text:
            opcode, args = text.split(None, 1)
            regs = abis.get(abi, {})
            def replace(m, regs=regs):
                return regs.get(m.group(1).lower(), m.group(1))
            args = re.sub(r'(?<!\$)\b([a-zA-Z][\w\.]+)\b', replace, args)
        else:
            opcode, args = text, ''
        
        if isjump(opcode):
            args = args.split(',')
            if args:
                arg = args[-1]
                arg = arg.strip()
                try:
                    sym = "GNUASM%d" % (arg_num,)
                    syms[sym] = int(arg, 0)
                    arg = sym
                    #Increment after the probable exception point
                    args[-1] = arg
                    arg_num += 1
                except ValueError:
                    pass
        else:
            args = [arg.strip() for arg in args.split(',')]
        lines.append(opcode + ' ' + ', '.join(args))
    return syms, ''.join(x + '\n' for x in lines), address

def get_tool(location, prefix, name, _platform=sys.platform):
    r"""Return path to a gcc tool, e.g. 'as'.
    
    >>> get_tool(r'c:\path\to\toolkit', 'mips-mti-elf-', 'as', _platform='win32')
    'c:\\path\\to\\toolkit\\mips-mti-elf-as.exe'
    >>> get_tool(r'/path/to/toolkit', 'mips-sde-elf-', 'as', _platform='linux2')
    '/path/to/toolkit/mips-sde-elf-as'
    >>> get_tool(r'/path/to/toolkit', 'mips-img-elf-', 'as', _platform='linux2')
    '/path/to/toolkit/mips-img-elf-as'
    """
    ext = '.exe' if _platform == 'win32' else ''
    slash = dict(win32='\\').get(_platform, '/')
    location = '' if location == '' else location + slash
    return os.path.expandvars('%s%s%s%s' % (location, prefix, name, ext))

def get_gcc_arch(isa):
    """Convert our isa spec into a list of gcc -m arch flags.
    
    >>> get_gcc_arch('mips16')
    ['-mips16']
    >>> get_gcc_arch('mips32')
    ['-mips32r2', '-meva']
    >>> get_gcc_arch('mips64')
    ['-mips64r2', '-meva']
    >>> get_gcc_arch('micromips')
    ['-mips32r2', '-mmicromips', '-meva']
    >>> get_gcc_arch('micromips64')
    ['-mips64r2', '-mmicromips', '-meva']
    >>> get_gcc_arch('micromipsr6')
    ['-mips32r6', '-mmicromips', '-meva']
    >>> get_gcc_arch('micromips64r6')
    ['-mips64r6', '-mmicromips', '-meva']
    >>> get_gcc_arch('mips64+smart')
    ['-mips64r2', '-meva', '-msmartmips']
    >>> get_gcc_arch('mips64+mt')
    ['-mips64r2', '-meva', '-mmt']
    >>> get_gcc_arch('mips64+msa')
    ['-mips64r2', '-meva', '-mmsa']
    >>> get_gcc_arch('nanomips+nms')
    ['-march=m7000']
    >>> get_gcc_arch('nanomips')
    ['-march=i7200']
    >>> get_gcc_arch('wtf+msa')
    Traceback (most recent call last):
    ...
    ValueError: Unknown isa 'wtf'
    """
    try:
        if isa.startswith('nanomips'):
            result = [gcc_nanomips_ases[ase].split() for ase in isa.split('+')]
            result = list(itertools.chain.from_iterable(result))
            if '-march=m7000' not in result:
                result.append('-march=32r6s')
        else:
            result = [gcc_ases[ase].split() for ase in isa.split('+')]
            result = list(itertools.chain.from_iterable(result))
        return result
    except KeyError as e:
        raise ValueError("Unknown isa %s" % str(e))

def get_gcc_abi(abi):
    """Convert our abi spec into a gcc -mabi compatible flag.
    
    >>> get_gcc_abi('o32')
    ['-mabi=32']
    >>> get_gcc_abi('n32')
    ['-mabi=n32']
    >>> get_gcc_abi('n64')
    ['-mabi=64']
    >>> get_gcc_abi('p32')
    ['-m32']
    >>> get_gcc_abi('numeric')
    []
    """
    if abi == 'numeric': 
        return []
    elif abi == 'p32':
        return ['-m32']
    elif abi == 'o32': 
        abi = '32'
    elif abi == 'n64': 
        abi = '64'
    return ['-mabi=' + abi]
    
def _get_toolkit_prefix(toolkit, setting, isa):
    r'''Try to guess the tookit prefix,.
    
    >>> _get_toolkit_prefix(r'C:\PROGRA~1\IMAGIN~1\TOOLCH~1\mips-img-elf\2015.06-05/bin', '', 'mips32')
    'mips-img-elf-'
    >>> _get_toolkit_prefix(r'/opt/imgtec/toolkits/mips-wibble-elf/2015.06-05/bin', '', 'mips32')
    'mips-wibble-elf-'
    >>> _get_toolkit_prefix(r'/opt/imgtec/toolkits/mips-wibble-elf/2015.06-05/bin', '', 'nanomips')
    'nanomips-elf-'
    >>> _get_toolkit_prefix(r'/opt/imgtec/toolkits/mips-img-elf/2015.06-05/bin', 'wobble-', 'mips16')
    'wobble-'
    >>> _get_toolkit_prefix(r'/nomatch', '', 'mips32')
    'mips-mti-elf-'
    >>> _get_toolkit_prefix(r'/nomatch', '', 'mips32r6')
    'mips-img-elf-'
    >>> _get_toolkit_prefix(r'/nomatch', '', 'micromipsr6')
    'mips-img-elf-'
    '''
    if setting:
        return setting
    if isa == 'nanomips':
        return 'nanomips-elf-'
    m = re.search(r'[\\/](mips-[a-z]+-elf)[\\/]', toolkit)
    if m:
        return m.group(1) + '-'
    return 'mips-img-elf-' if is_r6_isa(isa) else 'mips-mti-elf-'

def _fix_up_line_nums(stderr, extra_lines=4):
    r'''Adjust err messages from the assembler to adjust for lines we added implicitly.
    
    >>> _fix_up_line_nums('something\n{standard input}:5:some error')
    'something\n{standard input}:1:some error'
    >>> _fix_up_line_nums('{standard input}: Assembler messages:\n{standard input}:5:some error')
    '{standard input}:1:some error'
    '''
    stderr = stderr.replace('{standard input}: Assembler messages:\n', '')
    def adjuster(m):
        return r'{{standard input}}:{0}:'.format(int(m.group(1))-extra_lines)
    return re.sub(r'^{standard input}:(\d+):', adjuster, stderr, flags=re.M)

def _exec(toolkit, prefix, tool, args, contents, verbose=0):
    cmd = [""]
    try:
        cmd = [get_tool(toolkit, prefix, tool)] + args
        if verbose and contents:
            print ' '.join(cmd), " <<< '" + contents + "'"
        elif verbose:
            print ' '.join(cmd)
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except EnvironmentError as e:
        toolkit_expanded = os.path.expandvars(toolkit)
        prefix_expanded = os.path.expandvars(prefix)
        mips_elf_root = os.environ.get('MIPS_ELF_ROOT', 'Not Set')
        raise RuntimeError("Inline assembler failed\n"
                           "Failed to execute '%s' :\n     %s\n"
                           "MIPS_ELF_ROOT=%s\n"
                           "Using toolkit=%r (%r)\n"
                           "Using toolkit_prefix=%r (%r)\n"
                           "Please specify the toolkit using config(console, 'toolkit', '/path/to')\n"
                           "Please specify the toolkit prefix using config(console, 'toolkit_prefix', 'mips-img-elf-')" %
                            (cmd[0], e, mips_elf_root, toolkit, toolkit_expanded, prefix, prefix_expanded))
    else:
        stdout, stderr = p.communicate(contents)
        stderr = stderr.replace('\r', '')
        if p.returncode:
            num_lines = 4 + (3*['--section-start' in a for a in args].count(True))
            raise RuntimeError(_fix_up_line_nums(stderr, extra_lines=num_lines))
        elif verbose:
            print 'STDERR',stderr
            print 'STDOUT',repr(stdout)
        return stdout

def asm_to_elf(toolkit, prefix, isa, abi, gcc_flags, asmcontents, address, syms, elfname, verbose):
    '''The contents of this file are made into words to be written to memory and
    that process assumes big endian order. Target endian is handled later.'''
    dummy_name = '.dummy_'
    extra = dedent('''\
        .section %s%s, ""
        %s:
        nop
        ''')
    extra = ''.join([extra % (dummy_name, name, name) for name, val in syms.items()])
    asmcontents = extra + asmcontents

    args = get_gcc_arch(isa) + get_gcc_abi(abi)
    args += ['-pipe', '-nostartfiles', '-nostdlib', '-nodefaultlibs', '-g', '-EB', '-mhard-float']
    args += ['-xassembler', '-'] # input from stdin
    args += ['-o', elfname] # output to elfname
    if verbose > 1: # tell gcc to be verbose too
        args += ['-v']
    ldargs = ['-Ttext', '0x%08x' % address, '-e', '0']
    ldargs += ['--section-start=%s%s=0x%08x' % (dummy_name, i, val) for i, val in syms.items()]
    args += ['-Wl,' + x for x in ldargs]
    args += gcc_flags
    return _exec(toolkit, prefix, 'gcc', args, asmcontents, verbose=verbose)

def read_elf_contents(name, address):
    try:
        progfile = load_program(name)
        sections = progfile.sections()
        for section in sections:
            if (section.kind() == Section.Standard) and (section.virtual_address() == address):
                return str(section.contents())
        did_find = [s.virtual_address() for s in sections if s.kind() == Section.Standard]
        did_find = ', '.join('0x%08x' % x for x in did_find)
        raise RuntimeError("Could not find an elf section matching the start address(0x%08x). Candidates were:\n%s"
                        % (address, did_find))
    except NotAnELF as e:
        raise RuntimeError(str(e))
    except ProgramFileError as e:
        raise

@command(isa=named_isas, 
         update=updates,
         verbose=verbosity,
         device_required=False)
def asmbytes(address, text, isa='auto', abi='auto', update=True, toolkit=None, prefix=None, _extra_gcc_flags='', verbose=0, _save_temp=None, device=None):
    r"""Assemble `text` at `address` with the given isa.
    
    Returns an instance of imgtec.codescape.disassembly.Disassembly or 
    imgtec.codescape.disassembly.DisassemblyList which can be queried for the 
    size and opcode ::
    
        >>> asmbytes(0x80000002, 'b 0x80000000', 'micromips', 'o32')
        0x80000002 9400fffd    b         0x80000000
        >>> x = asmbytes(0x80000002, 'b 0x80000000', 'micromips', 'o32')
        >>> x.size, x.opcode
        (4, '9400fffd')
        >>> '0x%08x' % (int(x.opcode, 16),)
        '0x9400fffd'
        >>> asmbytes(0x80000002, '''b 0x80000000
        ...     nop
        ...     ''', 'micromips', 'o32')
        0x80000002 9400fffd    b         0x80000000
        0x80000006 0c00     DS nop
        
    If there is a current device then `isa` and `abi` may be 'auto' in which
    case the current ISA of the cpu, and the currently configured abi is used.

    If there is no current device then `isa` must be specified, valid values
    are listed in the help for :func:`isa` and :func:`abi`. If `abi` is not
    specified then 'o32' is used for MIPS targets.  The ISA can also be
    explicitly specified using the named parameters below::
        
        >>> asmbytes(0x80000000, 'subu $v0, $v0, $v1', mips32, 'o32')
        0x80000000 00431023    subu      v0, v0, v1
        >>> asmbytes(0x80000000, 'subu $v0, $v0, $v1', mips64, 'n32')
        0x80000000 00431023    subu      v0, v0, v1
        >>> asmbytes(0x80000000, 'subu $2, $2, $3', 'mips32', 'o32')
        0x80000000 00431023    subu      v0, v0, v1
        
    Using numeric abi changes the disassembly format, but o32 register 
    names are still permitted::
        
        >>> asmbytes(0x80000000, 'subu $v0, $v0, $v1', 'mips32', 'numeric')
        0x80000000 00431023    subu      $2, $2, $3
        
    :func:`asm` and asmbytes keep a static address as the default if address is 
    None. If `update` is True (i.e. noupdate is not specified) then the asm 
    address is updated to the address after the final instruction after each 
    command so that the next instruction can be assembled without entering 
    another address::

        >>> asmbytes(0x80000000, 'subu $v0, $v0, $v1', 'mips32')
        0x80000000 00431023    subu      $2, $2, $3
        >>> asmbytes(None, 'nop', 'mips32', noupdate)
        0x80000004 00000000    nop
        >>> asmbytes(None, 'nop\nnop')
        0x80000004 00000000    nop
        0x80000008 00000000    nop
        >>> asmbytes(None, 'nop')
        0x8000000c 00000000    nop

    The GCC assembler is used for the assemble operation, it is located by
    default in ``${MIPS_ELF_ROOT}/bin`` with the default prefix.
    The path and prefix can be overridden using::

      config(console, 'toolkit', '/path/to/toolkit')
      config(console, 'toolkit_prefix', 'mips-img-elf-')
      
    .. note:: The default prefix is 'mips-img-elf-' for R6 ISAs or 
              'mips-mti-elf-' otherwise.

    """
    from imgtec.console.cfg import console_config
    from imgtec.codescape import tiny
    if address is None:
        address = asmbytes.default_address or 'pc'
    if isinstance(address, basestring):
        if not device:
            raise RuntimeError('No probe is configured, please provide an address, not a register name')
        address = eval_address(device, address)
        
    #For a single line input only deal with the first op code produced
    single_line = False
    if len([line for line in text.splitlines() if line]) == 1:
        single_line = True
        
    isa, abi = get_isa_and_abi(isa, abi, address, device=device)
    if ('64' not in isa) and (address > 0xffffffff):
        raise RuntimeError('Cannot assemble at a 64 bit address with a 32 bit isa.')
        
    if toolkit is None:
        toolkit = os.path.expandvars(console_config.toolkit)
    if prefix is None:
        prefix = _get_toolkit_prefix(toolkit, console_config.toolkit_prefix, isa)
        
    syms, contents, start_address = get_asm_contents(address, text, isa, abi)
    
    with filesystem.named_temp(prefix='console.asm.', suffix='.elf') as elf:
        elf.close()
        asm_to_elf(toolkit, prefix, isa, abi, _extra_gcc_flags, contents,
                                    start_address, syms, elf.name, verbose=verbose)
        
        if _save_temp:
            shutil.copyfile(elf.name, _save_temp)
        data = read_elf_contents(elf.name, start_address)
        data = data[address - start_address:] # offset any padding instruction
        
        if single_line:
            i = tiny.DisassembleBytes(address, None, isa, abi, data)
            if update:
                asmbytes.default_address = i.address + i.size
        else:
            i = tiny.DisassembleBytes(address, -1, isa, abi, data)
            if update:
                asmbytes.default_address = i[-1].address + i[-1].size
        return i
asmbytes.default_address = None
asm_bytes = asmbytes

def _write_words(ops, isa, word, halfword, verify=True, device=None):
    for op in ops:
        wordsize = 2 if is_16bit_isa(isa) else 4
        vals = [int(op.opcode[n*2:n*2+wordsize*2],16) for n in range(0, op.size, wordsize)]
        fn = word if wordsize == 4 else halfword
        fn(op.address, vals, verify=False, device=device)
        if verify:
            got = fn(op.address, count=len(vals), device=device)
            if got != vals:
                bytes = struct.pack('>%dL' % len(vals), *got) if wordsize == 4 else struct.pack('>%dH' % len(vals), *got)
                actual = dasmbytes(op.address, bytes)
                raise RuntimeError('Failed to write instruction(s), wrote\n%r ; but read back\n%r' % (op, actual))

@command(isa=named_isas, verify=verifies, update=updates, verbose=verbosity)
def asm(address, text, isa='auto', abi='auto', verify=True, update=True, toolkit=None, prefix=None, _extra_gcc_flags='', verbose=0, device=None):
    r"""Assemble `text` at `address` and write it to the target.

    Returns an instance of imgtec.codescape.disassembly.Disassembly or 
    imgtec.codescape.disassembly.DisassemblyList in the case that the input 
    has multiple instructions. This can be queried for the size and opcode 
    that was written::

        >>> dasm(0x80000000, count=1)
        0x80000000 00000000    nop
        >>> asm(0x80000000, 'subu $v0, $v0, $v1')
        0x80000000 00431023    subu      v0, v0, v1
        >>> dasm(0x80000000, count=1)
        0x80000000 00431023    subu      v0, v0, v1

    `isa` and `abi` may be 'auto' in which case the current ISA of the cpu, 
    and the currently configured abi is used.  Valid values are listed in 
    the help for :func:`isa` and :func:`abi`.  The ISA can also be explicitly 
    specified using the named parameters below.

    asm and :func:`asmbytes` keep a static address as the default if address is
    None, if `update` is True (i.e. noupdate is not specified) then the asm
    address is updated to the address after the final instruction after each
    command so that the next instruction can be assembled without entering
    another address::

        >>> asm(0x80000000, 'subu $v0, $v0, $v1', 'mips32')
        0x80000000 00431023    subu      $2, $2, $3
        >>> asm(None, 'nop', 'mips32', noupdate)
        0x80000004 00000000    nop
        >>> asm(None, 'b 0x80000004', 'mips32', noupdate)
        0x80000004 10000000    b         0x80000004
        
    The GCC assembler is used for the assemble operation, it is located by 
    default in ``${MIPS_ELF_ROOT}/bin``, with the tool prefix 'mips-mti-elf-',
    these can be overridden using::

      config(console, 'toolkit', '/path/to/toolkit')
      config(console, 'toolkit_prefix', 'mips-img-elf-')

    """
    address = eval_address(device, address)
    i = asmbytes(address, text, isa, abi, update=update, toolkit=toolkit, 
            prefix=prefix, _extra_gcc_flags=_extra_gcc_flags, verbose=verbose, 
            device=device)
    
    isa, abi = get_isa_and_abi(isa, abi, address, device=device)

    #asmbytes will return a DisassemblyList for multi line input
    if isinstance(i, Disassembly):
        ops = [i]
    else:
        ops = i
    _write_words(ops, isa, word, halfword, verify, device)
    return i    

if __name__ == "__main__":
    import doctest
    doctest.testmod()