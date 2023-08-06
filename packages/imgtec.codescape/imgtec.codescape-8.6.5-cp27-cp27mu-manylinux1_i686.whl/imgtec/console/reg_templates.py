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

template_mips_minimal = '''\
# name=MIPS Generic Console
# processor_family = mips
# version=0.1

$ if cpu_info.get('cpu_is_32bit')
$   set addrwidth = 'width=8'
$ else
$   set addrwidth = 'width=16'
$ endif

$if ABI == 'o32' or ABI == 'o64':
zero   [$zero   hex {{addrwidth}}]  at     [$at     hex {{addrwidth}}]   v0    [$v0       hex {{addrwidth}}]  v1        [$v1         hex {{addrwidth}}]
a0     [$a0     hex {{addrwidth}}]  a1     [$a1     hex {{addrwidth}}]   a2    [$a2       hex {{addrwidth}}]  a3        [$a3         hex {{addrwidth}}]
t0     [$t0     hex {{addrwidth}}]  t1     [$t1     hex {{addrwidth}}]   t2    [$t2       hex {{addrwidth}}]  t3        [$t3         hex {{addrwidth}}]
t4     [$t4     hex {{addrwidth}}]  t5     [$t5     hex {{addrwidth}}]   t6    [$t6       hex {{addrwidth}}]  t7        [$t7         hex {{addrwidth}}]
s0     [$s0     hex {{addrwidth}}]  s1     [$s1     hex {{addrwidth}}]   s2    [$s2       hex {{addrwidth}}]  s3        [$s3         hex {{addrwidth}}]
s4     [$s4     hex {{addrwidth}}]  s5     [$s5     hex {{addrwidth}}]   s6    [$s6       hex {{addrwidth}}]  s7        [$s7         hex {{addrwidth}}]
t8     [$t8     hex {{addrwidth}}]  t9     [$t9     hex {{addrwidth}}]   k0    [$k0       hex {{addrwidth}}]  k1        [$k1         hex {{addrwidth}}]
gp     [$gp     hex {{addrwidth}}]  sp     [$sp     hex {{addrwidth}}]   s8    [$s8       hex {{addrwidth}}]  ra        [$ra         hex {{addrwidth}}]
$ elif ABI == 'n32' or ABI == 'n64'
zero   = [$zero hex {{addrwidth}}]   at    = [$at  hex {{addrwidth}}]   v0  = [$v0  hex {{addrwidth}}]  v1       = [$v1   hex {{addrwidth}}]
a0     = [$a0   hex {{addrwidth}}]   a1    = [$a1  hex {{addrwidth}}]   a2  = [$a2  hex {{addrwidth}}]  a3       = [$a3   hex {{addrwidth}}]
a4     = [$a4   hex {{addrwidth}}]   a5    = [$a5  hex {{addrwidth}}]   a6  = [$a6  hex {{addrwidth}}]  a7       = [$a7   hex {{addrwidth}}]
t0     = [$t0   hex {{addrwidth}}]   t1    = [$t1  hex {{addrwidth}}]   t2  = [$t2  hex {{addrwidth}}]  t3       = [$t3   hex {{addrwidth}}]
s0     = [$s0   hex {{addrwidth}}]   s1    = [$s1  hex {{addrwidth}}]   s2  = [$s2  hex {{addrwidth}}]  s3       = [$s3   hex {{addrwidth}}]
s4     = [$s4   hex {{addrwidth}}]   s5    = [$s5  hex {{addrwidth}}]   s6  = [$s6  hex {{addrwidth}}]  s7       = [$s7   hex {{addrwidth}}]
t8     = [$t8   hex {{addrwidth}}]   t9    = [$t9  hex {{addrwidth}}]   k0  = [$k0  hex {{addrwidth}}]  k1       = [$k1   hex {{addrwidth}}]
gp     = [$gp   hex {{addrwidth}}]   sp    = [$sp  hex {{addrwidth}}]   s8  = [$s8  hex {{addrwidth}}]  ra       = [$ra   hex {{addrwidth}}]
$ elif ABI == 'p32' or ABI == 'p64'
zero   = [$zero hex {{addrwidth}}]   at    = [$at  hex {{addrwidth}}]   t4  = [$t4  hex {{addrwidth}}]  t5       = [$t5   hex {{addrwidth}}]
a0     = [$a0   hex {{addrwidth}}]   a1    = [$a1  hex {{addrwidth}}]   a2  = [$a2  hex {{addrwidth}}]  a3       = [$a3   hex {{addrwidth}}]
a4     = [$a4   hex {{addrwidth}}]   a5    = [$a5  hex {{addrwidth}}]   a6  = [$a6  hex {{addrwidth}}]  a7       = [$a7   hex {{addrwidth}}]
t0     = [$t0   hex {{addrwidth}}]   t1    = [$t1  hex {{addrwidth}}]   t2  = [$t2  hex {{addrwidth}}]  t3       = [$t3   hex {{addrwidth}}]
s0     = [$s0   hex {{addrwidth}}]   s1    = [$s1  hex {{addrwidth}}]   s2  = [$s2  hex {{addrwidth}}]  s3       = [$s3   hex {{addrwidth}}]
s4     = [$s4   hex {{addrwidth}}]   s5    = [$s5  hex {{addrwidth}}]   s6  = [$s6  hex {{addrwidth}}]  s7       = [$s7   hex {{addrwidth}}]
t8     = [$t8   hex {{addrwidth}}]   t9    = [$t9  hex {{addrwidth}}]   k0  = [$k0  hex {{addrwidth}}]  k1       = [$k1   hex {{addrwidth}}]
gp     = [$gp   hex {{addrwidth}}]   sp    = [$sp  hex {{addrwidth}}]   fp  = [$fp  hex {{addrwidth}}]  ra       = [$ra   hex {{addrwidth}}]
$ else
r0     = [$r0     hex {{addrwidth}}]   r1    = [$r1     hex {{addrwidth}}]   r2     = [$r2       hex {{addrwidth}}]  r3       = [$r3         hex {{addrwidth}}]
r4     = [$r4     hex {{addrwidth}}]   r5    = [$r5     hex {{addrwidth}}]   r6     = [$r6       hex {{addrwidth}}]  r7       = [$r7         hex {{addrwidth}}]
r8     = [$r8     hex {{addrwidth}}]   r9    = [$r9     hex {{addrwidth}}]   r10    = [$r10      hex {{addrwidth}}]  r11      = [$r11        hex {{addrwidth}}]
r12    = [$r12    hex {{addrwidth}}]   r13   = [$r13    hex {{addrwidth}}]   r14    = [$r14      hex {{addrwidth}}]  r15      = [$r15        hex {{addrwidth}}]
r16    = [$r16    hex {{addrwidth}}]   r17   = [$r17    hex {{addrwidth}}]   r18    = [$r18      hex {{addrwidth}}]  r19      = [$r19        hex {{addrwidth}}]
r20    = [$r20    hex {{addrwidth}}]   r21   = [$r21    hex {{addrwidth}}]   r22    = [$r22      hex {{addrwidth}}]  r23      = [$r23        hex {{addrwidth}}]
r24    = [$r24    hex {{addrwidth}}]   r25   = [$r25    hex {{addrwidth}}]   r26    = [$r26      hex {{addrwidth}}]  r27      = [$r27        hex {{addrwidth}}]
r28    = [$r28    hex {{addrwidth}}]   r29   = [$r29    hex {{addrwidth}}]   r30    = [$r30      hex {{addrwidth}}]  r31      = [$r31        hex {{addrwidth}}]
hi     = [$hi     hex {{addrwidth}}]   lo    = [$lo     hex {{addrwidth}}]   []       []               pc       = [$pc         hex {{addrwidth}}]
status = [$status hex {{addrwidth}}]   cause = [$cause  hex {{addrwidth}}]   epc    = [$epc      hex {{addrwidth}}]  badvaddr = [$badvaddr   hex {{addrwidth}}]
$endif
{{- "\n" -}}
Hi      [$Hi      hex width=8]  Lo        [$Lo       hex width=8]  DEPC      [$DEPC      hex {{addrwidth}}]  pc           [$pc            hex {{addrwidth}}]
Status  [$Status  hex width=8]  Cause     [$Cause    hex width=8]  EPC       [$EPC       hex {{addrwidth}}]  BadVAddr     [$BadVAddr      hex {{addrwidth}}]
Index   [$Index   hex width=8]  Random    [$Random   hex width=8]  EntryLo0  [$EntryLo0  hex width=8]        EntryLo1     [$EntryLo1      hex width=8]
Context [$Context hex width=8]  PageMask  [$PageMask hex width=8]  Wired     [$Wired     hex width=8]        Count        [$Count         hex width=8]
EntryHi [$EntryHi hex width=8]  Compare   [$Compare  hex width=8]  PRId      [$PRId      hex width=8]        ErrorEPC     [$ErrorEPC      hex {{addrwidth}}]
Config  [$Config  hex width=8]  Config1   [$Config1  hex width=8]  Config2   [$Config2   hex width=8]        Config3      [$Config3       hex width=8]
LLAddr  [$LLAddr  hex width=8]  WatchLo0  [$WatchLo0 hex width=8]  WatchHi0  [$WatchHi0  hex width=8]        Debug        [$Debug         hex width=8]
ITagLo  [$ITaglo  hex width=8]  IDataLo   [$IDataLo  hex width=8]  IDataHi   [$IDataHi   hex width=8]        PageGrain    [$PageGrain hex width=8]
DTagLo  [$DTaglo  hex width=8]  DDataLo   [$DDataLo  hex width=8]  DDataHi   [$DDataHi   hex width=8]        TraceControl [$TraceControl  hex width=8]
'''

# [[[cog
# from imgbuild.SConsPaths import sw
# import os
# templates = [
#   ('template_mcp' , 'mcp.txt',        False),
#   ('template_meta', 'meta.txt',       False),
#   ('template_mips', 'mips_basic.txt', True),
# ]
# regtemplates_path =  sw('codescape', 'register_templates/')
# var_str = "reg_templates = [template_mips_minimal"
# for py_name, file_name, has_cog in templates:
#   cog.outl('%s = \'\'\'\\' % py_name)
#   with open(os.path.join(regtemplates_path, file_name)) as f:
#       if not has_cog:
#           cog.out(f.read())
#       else:
#           #Get around mips_basic containing cog itself
#           lines = f.readlines()
#           in_cog = False
#           for line in lines:
#               if line.startswith('{#'):
#                   in_cog = True
#               if not in_cog:
#                   cog.out(line)
#               if line.strip().endswith('#}'):
#                   in_cog = False
#       cog.outl("\'\'\'")
#       cog.outl()
#       var_str += ', ' + py_name
# var_str += ']'
# cog.outl(var_str)
# ]]]
template_mcp = '''\
# name=MCP Generic
# core_ids=0x00
# processor_family = mcp
# version=1.4
$ set num_vus = cpu_info.get('number_of_vu_units', 0)
# view_option= Show default per-thread registers:ShowDefaultPerThread:True
# view_option= Show control registers:ShowControl:True
$ if num_vus > 1
#   view_option= Show pseudo registers:ShowPseudo:False
$ endif
# view_option= ---
# view_option= Show fixed point registers as hex:ShowFixedPointAsHex:True
# view_option= Show fixed point registers as complex:ShowFixedPointAsComplex:False
# view_option= Show 6-bit registers as left aligned hex:ShowNoneFixedPointRegistersLeftAligned:True
$ if num_vus > 1
#   view_option= ---
#   view_option=Default|{% for n in range(num_vus) %}Vu {{n}}{%if not loop.last %}|{% endif %}{% endfor %}|{% for n in range(num_vus) %}Copro Vu {{n}}{%if not loop.last %}|{% endif %}{% endfor %}:Vu:0:True:True
#   view_option= ---
$ endif
# view_option= Show Layout Vertically:Vertical:False
$ set h6="hex width=6"
$ set h6ro="hex width=6 read_only=True"
$ set fpc="fixed_point_complex width_m=0 width_n=27 left_align=True"
$ set fpro="fixed_point width_m=0 width_n=27 read_only=True left_align=True"
$ set fpcro="fixed_point_complex width_m=0 width_n=27 read_only=True left_align=True"
$ set ds = "hex width=2 left_align=True bit_start=0 bit_end=5"
$ set norm="hex width=2 read_only=True left_align=True bit_start=26 bit_end=31"
$ set max_banks = num_vus * 2
$ if Vu is not defined or Vu == 0 or Vu > max_banks
$  set vu="  "
$  set cp=""
$ elif Vu > num_vus
$  set vu=".%d" % (Vu-1-num_vus, )
$  set cp="CP_"
$ else
$  set vu=".%d" % (Vu-1, )
$  set cp=""
$ endif
$- if Vertical
    $- if ShowDefaultPerThread
        DP0{{vu}}        = [${{cp}}DP0{{vu}}  {{fpc}}] [${{cp}}DP1{{vu}}  {{fpc}}] [${{cp}}DP2{{vu}}  {{fpc}}] [${{cp}}DP3{{vu}}  {{fpc}}]                       {% if ShowControl %}MOD{{vu}}   = [${{cp}}MOD{{vu}} {{h6}}]{% endif %}
        DP4{{vu}}        = [${{cp}}DP4{{vu}}  {{fpc}}] [${{cp}}DP5{{vu}}  {{fpc}}] [${{cp}}DP6{{vu}}  {{fpc}}] [${{cp}}DP7{{vu}}  {{fpc}}]                       {% if ShowControl %}L1R{{vu}}   = [${{cp}}L1R{{vu}} {{h6}}]{% endif %}
        DP8{{vu}}        = [${{cp}}DP8{{vu}}  {{fpc}}] [${{cp}}DP9{{vu}}  {{fpc}}] [${{cp}}DP10{{vu}} {{fpc}}] [${{cp}}DP11{{vu}} {{fpc}}]                       {% if ShowControl %}L2R{{vu}}   = [${{cp}}L2R{{vu}} {{h6}}]{% endif %}
        DP12{{vu}}       = [${{cp}}DP12{{vu}} {{fpc}}] [${{cp}}DP13{{vu}} {{fpc}}] [${{cp}}DP14{{vu}} {{fpc}}] [${{cp}}DP15{{vu}} {{fpc}}]                       {% if ShowControl %}L3R{{vu}}   = [${{cp}}L3R{{vu}} {{h6}}]{% endif %}
        []             []              []              []              []                                                            {% if ShowControl and not cp %}L1{{vu}}    = [${{cp}}L1{{vu}}  {{h6ro}}]{% endif %}
        DM0{{vu}}        = [${{cp}}DM0{{vu}}  {{fpc}}] [${{cp}}DM1{{vu}}  {{fpc}}] [${{cp}}DM2{{vu}}  {{fpc}}] [${{cp}}DM3{{vu}}  {{fpc}}]                   {% if ShowControl and not cp %}L2{{vu}}    = [${{cp}}L2{{vu}}  {{h6ro}}]{% endif %}
        DM4{{vu}}        = [${{cp}}DM4{{vu}}  {{fpc}}] [${{cp}}DM5{{vu}}  {{fpc}}] [${{cp}}DM6{{vu}}  {{fpc}}] [${{cp}}DM7{{vu}}  {{fpc}}]                   {% if ShowControl and not cp %}L3{{vu}}    = [${{cp}}L3{{vu}}  {{h6ro}}]{% endif %}
        DM8{{vu}}        = [${{cp}}DM8{{vu}}  {{fpc}}] [${{cp}}DM9{{vu}}  {{fpc}}] [${{cp}}DM10{{vu}} {{fpc}}] [${{cp}}DM11{{vu}} {{fpc}}]                   {% if ShowControl and not cp %}L1RTN   = [${{cp}}L1RTN {{h6ro}}]{% endif %}
        DM12{{vu}}       = [${{cp}}DM12{{vu}} {{fpc}}] [${{cp}}DM13{{vu}} {{fpc}}] [${{cp}}DM14{{vu}} {{fpc}}] [${{cp}}DM15{{vu}} {{fpc}}]                   {% if ShowControl and not cp %}L2RTN   = [${{cp}}L2RTN {{h6ro}}]{% endif %}
        []             []              []              []              []                                                            {% if ShowControl and not cp %}L3RTN   = [${{cp}}L3RTN {{h6ro}}]{% endif %}
        DS0{{vu}}        = [${{cp}}DS0{{vu}} {{ds}}]   [${{cp}}DS1{{vu}} {{ds}}]   [${{cp}}DS2{{vu}} {{ds}}]   [${{cp}}DS3{{vu}} {{ds}}]                     {% if ShowControl %}SHO{{vu}}   = [${{cp}}SHO{{vu}} {{h6}}]{% endif %}
        []             []              []              []              []                                                            {% if ShowControl %}MHO{{vu}}   = [${{cp}}MHO{{vu}} {{h6}}]{% endif %}
        OPADD0{{vu}}     = [${{cp}}OPADD0{{vu}} {{fpcro}}] [${{cp}}OPADD1{{vu}} {{fpcro}}] [${{cp}}OPADD2{{vu}} {{fpcro}}] [${{cp}}OPADD3{{vu}} {{fpcro}}]   {% if ShowControl %}SWP     = [${{cp}}SWP {{h6}}]{% endif %}
        OPADD4{{vu}}     = [${{cp}}OPADD4{{vu}} {{fpcro}}] [${{cp}}OPADD5{{vu}} {{fpcro}}] [${{cp}}OPADD6{{vu}} {{fpcro}}] [${{cp}}OPADD7{{vu}} {{fpcro}}]   {% if ShowControl %}PC      = [${{cp}}PC {{h6}}]{% endif %}

        OMUL0r{{vu}}     = [${{cp}}OMUL0r{{vu}} {{fpro}}] [${{cp}}OMUL1r{{vu}} {{fpro}}] [${{cp}}OMUL2r{{vu}} {{fpro}}] [${{cp}}OMUL3r{{vu}} {{fpro}}]
        OMUL0i{{vu}}     = [${{cp}}OMUL0i{{vu}} {{fpro}}] [${{cp}}OMUL1i{{vu}} {{fpro}}] [${{cp}}OMUL2i{{vu}} {{fpro}}] [${{cp}}OMUL3i{{vu}} {{fpro}}]
        OMUL4r{{vu}}     = [${{cp}}OMUL4r{{vu}} {{fpro}}] [${{cp}}OMUL5r{{vu}} {{fpro}}] [${{cp}}OMUL6r{{vu}} {{fpro}}] [${{cp}}OMUL7r{{vu}} {{fpro}}]
        OMUL4i{{vu}}     = [${{cp}}OMUL4i{{vu}} {{fpro}}] [${{cp}}OMUL5i{{vu}} {{fpro}}] [${{cp}}OMUL6i{{vu}} {{fpro}}] [${{cp}}OMUL7i{{vu}} {{fpro}}]

        OACC0r{{vu}}     = [${{cp}}OACC0r{{vu}} {{fpro}}] [${{cp}}OACC1r{{vu}} {{fpro}}] [${{cp}}OACC2r{{vu}} {{fpro}}] [${{cp}}OACC3r{{vu}} {{fpro}}]
        OACC0i{{vu}}     = [${{cp}}OACC0i{{vu}} {{fpro}}] [${{cp}}OACC1i{{vu}} {{fpro}}] [${{cp}}OACC2i{{vu}} {{fpro}}] [${{cp}}OACC3i{{vu}} {{fpro}}]
        OACC4r{{vu}}     = [${{cp}}OACC4r{{vu}} {{fpro}}] [${{cp}}OACC5r{{vu}} {{fpro}}] [${{cp}}OACC6r{{vu}} {{fpro}}] [${{cp}}OACC7r{{vu}} {{fpro}}]
        OACC4i{{vu}}     = [${{cp}}OACC4i{{vu}} {{fpro}}] [${{cp}}OACC5i{{vu}} {{fpro}}] [${{cp}}OACC6i{{vu}} {{fpro}}] [${{cp}}OACC7i{{vu}} {{fpro}}]

        OCOMB0r{{vu}}    = [${{cp}}OCOMB0r{{vu}} {{fpro}}] [${{cp}}OCOMB1r{{vu}} {{fpro}}] [${{cp}}OCOMB2r{{vu}} {{fpro}}] [${{cp}}OCOMB3r{{vu}} {{fpro}}]
        OCOMB0i{{vu}}    = [${{cp}}OCOMB0i{{vu}} {{fpro}}] [${{cp}}OCOMB1i{{vu}} {{fpro}}] [${{cp}}OCOMB2i{{vu}} {{fpro}}] [${{cp}}OCOMB3i{{vu}} {{fpro}}]
        OCOMBNORM0{{vu}} = [${{cp}}OCOMBNORM0{{vu}} {{norm}}] [${{cp}}OCOMBNORM1{{vu}} {{norm}}] [${{cp}}OCOMBNORM2{{vu}} {{norm}}] [${{cp}}OCOMBNORM3{{vu}} {{norm}}]

        OFNS0{{vu}}      = [${{cp}}OFNS0{{vu}} {{fpcro}}]    [${{cp}}OFNS1{{vu}} {{fpcro}}]     [${{cp}}OFNS2{{vu}} {{fpcro}}]    [${{cp}}OFNS3{{vu}} {{fpcro}}]
        OFNSNORM0{{vu}}  = [${{cp}}OFNSNORM0{{vu}} {{norm}}] [${{cp}}OFNSNORM1{{vu}} {{norm}}]  [${{cp}}OFNSNORM2{{vu}} {{norm}}] [${{cp}}OFNSNORM3{{vu}} {{norm}}]

        OSCALE0{{vu}}    = [${{cp}}OSCALE0{{vu}} {{fpcro}}] [${{cp}}OSCALE1{{vu}} {{fpcro}}] [${{cp}}OSCALE2{{vu}} {{fpcro}}] [${{cp}}OSCALE3{{vu}} {{fpcro}}]

        AP0{{vu}}        = [${{cp}}AP0{{vu}} {{h6}}] [${{cp}}AP1{{vu}} {{h6}}] [${{cp}}AP2{{vu}} {{h6}}] [${{cp}}AP3{{vu}} {{h6}}]
        AP4{{vu}}        = [${{cp}}AP4{{vu}} {{h6}}] [${{cp}}AP5{{vu}} {{h6}}] [${{cp}}AP6{{vu}} {{h6}}] [${{cp}}AP7{{vu}} {{h6}}]

        AO0{{vu}}        = [${{cp}}AO0{{vu}} {{h6}}] [${{cp}}AO1{{vu}} {{h6}}] [${{cp}}AO2{{vu}} {{h6}}] [${{cp}}AO3{{vu}} {{h6}}]
        AO4{{vu}}        = [${{cp}}AO4{{vu}} {{h6}}] [${{cp}}AO5{{vu}} {{h6}}] [${{cp}}AO6{{vu}} {{h6}}] [${{cp}}AO7 {{h6}}]

        AI0{{vu}}        = [${{cp}}AI0{{vu}} {{h6}}] [${{cp}}AI1{{vu}} {{h6}}] [${{cp}}AI2{{vu}} {{h6}}] [${{cp}}AI3{{vu}} {{h6}}]

        AM0{{vu}}        = [${{cp}}AM0{{vu}} {{h6}}] [${{cp}}AM1{{vu}} {{h6}}] [${{cp}}AM2{{vu}} {{h6}}] [${{cp}}AM3{{vu}} {{h6}}]
    $- endif
$- else    
    $- if ShowDefaultPerThread
        DP0{{vu}}     = [${{cp}}DP0{{vu}}  {{fpc}}]       [${{cp}}DP1{{vu}} {{fpc}}]       [${{cp}}DP2{{vu}} {{fpc}}]       [${{cp}}DP3{{vu}} {{fpc}}]         DM0{{vu}}        = [${{cp}}DM0{{vu}} {{fpc}}]  [${{cp}}DM1{{vu}} {{fpc}}]  [${{cp}}DM2{{vu}} {{fpc}}]  [${{cp}}DM3{{vu}} {{fpc}}]                               {% if ShowControl %}MOD{{vu}}   = [${{cp}}MOD{{vu}} {{h6}}]{% endif %}
        DP4{{vu}}     = [${{cp}}DP4{{vu}}  {{fpc}}]       [${{cp}}DP5{{vu}} {{fpc}}]       [${{cp}}DP6{{vu}} {{fpc}}]       [${{cp}}DP7{{vu}} {{fpc}}]         DM4{{vu}}        = [${{cp}}DM4{{vu}} {{fpc}}]  [${{cp}}DM5{{vu}} {{fpc}}]  [${{cp}}DM6{{vu}} {{fpc}}]  [${{cp}}DM7{{vu}} {{fpc}}]                               {% if ShowControl %}L1R{{vu}}   = [${{cp}}L1R{{vu}} {{h6}}]{% endif %}
        DP8{{vu}}     = [${{cp}}DP8{{vu}}  {{fpc}}]       [${{cp}}DP9{{vu}} {{fpc}}]       [${{cp}}DP10{{vu}} {{fpc}}]      [${{cp}}DP11{{vu}} {{fpc}}]        DM8{{vu}}        = [${{cp}}DM8{{vu}} {{fpc}}]  [${{cp}}DM9{{vu}} {{fpc}}]  [${{cp}}DM10{{vu}} {{fpc}}] [${{cp}}DM11{{vu}} {{fpc}}]                              {% if ShowControl %}L2R{{vu}}   = [${{cp}}L2R{{vu}} {{h6}}]{% endif %}
        DP12{{vu}}    = [${{cp}}DP12{{vu}} {{fpc}}]       [${{cp}}DP13{{vu}} {{fpc}}]      [${{cp}}DP14{{vu}} {{fpc}}]      [${{cp}}DP15{{vu}} {{fpc}}]        DM12{{vu}}       = [${{cp}}DM12{{vu}} {{fpc}}] [${{cp}}DM13{{vu}} {{fpc}}] [${{cp}}DM14{{vu}} {{fpc}}] [${{cp}}DM15{{vu}} {{fpc}}]                              {% if ShowControl %}L3R{{vu}}   = [${{cp}}L3R{{vu}} {{h6}}]{% endif %}
        []          []                    []                   []                   []                     []             []              []              []              []                                                                                                   {% if ShowControl and not cp  %}L1{{vu}}    = [${{cp}}L1{{vu}}  {{h6ro}}]{% endif %}
        OPADD0{{vu}}  = [${{cp}}OPADD0{{vu}} {{fpcro}}]   [${{cp}}OPADD1{{vu}} {{fpcro}}]  [${{cp}}OPADD2{{vu}} {{fpcro}}]  [${{cp}}OPADD3{{vu}} {{fpcro}}]    OPADD4{{vu}}     = [${{cp}}OPADD4{{vu}} {{fpcro}}] [${{cp}}OPADD5{{vu}} {{fpcro}}] [${{cp}}OPADD6{{vu}} {{fpcro}}] [${{cp}}OPADD7{{vu}} {{fpcro}}]              {% if ShowControl and not cp  %}L2{{vu}}    = [${{cp}}L2{{vu}}  {{h6ro}}]{% endif %}
        []          []                    []                   []                   []                     []             []              []              []              []                                                                                                   {% if ShowControl and not cp  %}L3{{vu}}    = [${{cp}}L3{{vu}}  {{h6ro}}]{% endif %}
        OMUL0r{{vu}}  = [${{cp}}OMUL0r{{vu}} {{fpro}}]    [${{cp}}OMUL1r{{vu}} {{fpro}}]   [${{cp}}OMUL2r{{vu}} {{fpro}}]   [${{cp}}OMUL3r{{vu}} {{fpro}}]     OMUL4r{{vu}}     = [${{cp}}OMUL4r{{vu}} {{fpro}}]  [${{cp}}OMUL5r{{vu}} {{fpro}}]  [${{cp}}OMUL6r{{vu}} {{fpro}}]  [${{cp}}OMUL7r{{vu}} {{fpro}}]               {% if ShowControl and not cp  %}L1RTN   = [${{cp}}L1RTN {{h6ro}}]{% endif %}
        OMUL0i{{vu}}  = [${{cp}}OMUL0i{{vu}} {{fpro}}]    [${{cp}}OMUL1i{{vu}} {{fpro}}]   [${{cp}}OMUL2i{{vu}} {{fpro}}]   [${{cp}}OMUL3i{{vu}} {{fpro}}]     OMUL4i{{vu}}     = [${{cp}}OMUL4i{{vu}} {{fpro}}]  [${{cp}}OMUL5i{{vu}} {{fpro}}]  [${{cp}}OMUL6i{{vu}} {{fpro}}]  [${{cp}}OMUL7i{{vu}} {{fpro}}]               {% if ShowControl and not cp  %}L2RTN   = [${{cp}}L2RTN {{h6ro}}]{% endif %}
        OACC0r{{vu}}  = [${{cp}}OACC0r{{vu}} {{fpro}}]    [${{cp}}OACC1r{{vu}} {{fpro}}]   [${{cp}}OACC2r{{vu}} {{fpro}}]   [${{cp}}OACC3r{{vu}} {{fpro}}]     OACC4r{{vu}}     = [${{cp}}OACC4r{{vu}} {{fpro}}]  [${{cp}}OACC5r{{vu}} {{fpro}}]  [${{cp}}OACC6r{{vu}} {{fpro}}]  [${{cp}}OACC7r{{vu}} {{fpro}}]               {% if ShowControl and not cp  %}L3RTN   = [${{cp}}L3RTN {{h6ro}}]{% endif %}
        OACC0i{{vu}}  = [${{cp}}OACC0i{{vu}} {{fpro}}]    [${{cp}}OACC1i{{vu}} {{fpro}}]   [${{cp}}OACC2i{{vu}} {{fpro}}]   [${{cp}}OACC3i{{vu}} {{fpro}}]     OACC4i{{vu}}     = [${{cp}}OACC4i{{vu}} {{fpro}}]  [${{cp}}OACC5i{{vu}} {{fpro}}]  [${{cp}}OACC6i{{vu}} {{fpro}}]  [${{cp}}OACC7i{{vu}} {{fpro}}]               {% if ShowControl %}SHO{{vu}}   = [${{cp}}SHO{{vu}} {{h6}}]{% endif %}
        []          []                    []                   []                   []                     []             []              []              []              []                                                                                                   {% if ShowControl %}MHO{{vu}}   = [${{cp}}MHO{{vu}} {{h6}}]{% endif %}
        OCOMB0r{{vu}} = [${{cp}}OCOMB0r{{vu}} {{fpro}}]   [${{cp}}OCOMB1r{{vu}} {{fpro}}]  [${{cp}}OCOMB2r{{vu}} {{fpro}}]  [${{cp}}OCOMB3r{{vu}} {{fpro}}]    OCOMBNORM0{{vu}} = [${{cp}}OCOMBNORM0{{vu}} {{norm}}] [${{cp}}OCOMBNORM1{{vu}} {{norm}}] [${{cp}}OCOMBNORM2{{vu}} {{norm}}] [${{cp}}OCOMBNORM3{{vu}} {{norm}}]  {% if ShowControl %}SWP     = [${{cp}}SWP {{h6}}]{% endif %}
        OCOMB0i{{vu}} = [${{cp}}OCOMB0i{{vu}} {{fpro}}]   [${{cp}}OCOMB1i{{vu}} {{fpro}}]  [${{cp}}OCOMB2i{{vu}} {{fpro}}]  [${{cp}}OCOMB3i{{vu}} {{fpro}}]    []             []                     []                     []                     []                                                  {% if ShowControl %}PC      = [${{cp}}PC {{h6}}]{% endif %}

        OFNS0{{vu}}   = [${{cp}}OFNS0{{vu}} {{fpcro}}]    [${{cp}}OFNS1{{vu}} {{fpcro}}]   [${{cp}}OFNS2{{vu}} {{fpcro}}]   [${{cp}}OFNS3{{vu}} {{fpcro}}]     OFNSNORM0{{vu}}  = [${{cp}}OFNSNORM0{{vu}} {{norm}}] [${{cp}}OFNSNORM1{{vu}} {{norm}}]  [${{cp}}OFNSNORM2{{vu}} {{norm}}] [${{cp}}OFNSNORM3{{vu}} {{norm}}]

        OSCALE0{{vu}} = [${{cp}}OSCALE0{{vu}} {{fpcro}}]  [${{cp}}OSCALE1{{vu}} {{fpcro}}] [${{cp}}OSCALE2{{vu}} {{fpcro}}] [${{cp}}OSCALE3{{vu}} {{fpcro}}]   DS0{{vu}}        = [${{cp}}DS0{{vu}} {{ds}}]  [${{cp}}DS1{{vu}} {{ds}}]  [${{cp}}DS2{{vu}} {{ds}}]  [${{cp}}DS3{{vu}} {{ds}}]

        AP0{{vu}}     = [${{cp}}AP0{{vu}} {{h6}}]         [${{cp}}AP1{{vu}} {{h6}}]        [${{cp}}AP2{{vu}} {{h6}}]        [${{cp}}AP3{{vu}} {{h6}}]          AP4{{vu}}        = [${{cp}}AP4{{vu}} {{h6}}] [${{cp}}AP5{{vu}} {{h6}}] [${{cp}}AP6{{vu}} {{h6}}] [${{cp}}AP7{{vu}} {{h6}}]
        AO0{{vu}}     = [${{cp}}AO0{{vu}} {{h6}}]         [${{cp}}AO1{{vu}} {{h6}}]        [${{cp}}AO2{{vu}} {{h6}}]        [${{cp}}AO3{{vu}} {{h6}}]          AO4{{vu}}        = [${{cp}}AO4{{vu}} {{h6}}] [${{cp}}AO5{{vu}} {{h6}}] [${{cp}}AO6{{vu}} {{h6}}] [${{cp}}AO7{{vu}} {{h6}}]
        AI0{{vu}}     = [${{cp}}AI0{{vu}} {{h6}}]         [${{cp}}AI1{{vu}} {{h6}}]        [${{cp}}AI2{{vu}} {{h6}}]        [${{cp}}AI3{{vu}} {{h6}}]          AM0{{vu}}        = [${{cp}}AM0{{vu}} {{h6}}] [${{cp}}AM1{{vu}} {{h6}}] [${{cp}}AM2{{vu}} {{h6}}] [${{cp}}AM3{{vu}} {{h6}}]
    $- endif
$- endif
$- if ShowControl and not ShowDefaultPerThread
    L1R{{vu}}   = [${{cp}}L1R{{vu}} {{h6}}]      L2R{{vu}}   = [${{cp}}L2R {{h6}}]           L3R{{vu}}   = [${{cp}}L3R {{h6}}]
    $ if not cp
        L1{{vu}}    = [${{cp}}L1{{vu}}  {{h6ro}}]    L2{{vu}}    = [${{cp}}L2{{vu}}  {{h6ro}}]   L3{{vu}}    = [${{cp}}L3{{vu}}  {{h6ro}}]
        L1RTN   =     [${{cp}}L1RTN {{h6ro}}]        L2RTN   =     [${{cp}}L2RTN {{h6ro}}]       L3RTN   =     [${{cp}}L3RTN {{h6ro}}]
    $- endif
    SHO{{vu}}   = [${{cp}}SHO{{vu}} {{h6}}]      MHO{{vu}}   = [${{cp}}MHO{{vu}} {{h6}}]     SWP     =     [${{cp}}SWP {{h6}}]
    {% if not cp  %}PC      =      [${{cp}}PC {{h6}}] {% endif %}
$- endif
$- if num_vus > 1 and ShowPseudo
    {{"\n"}} 
    AP0BASE = [$AP0BASE]  AP1BASE = [$AP1BASE] AP2BASE = [$AP2BASE] AP3BASE = [$AP3BASE]
    AP4BASE = [$AP4BASE]  AP5BASE = [$AP5BASE] AP6BASE = [$AP6BASE] AP7BASE = [$AP7BASE]
    AP0LOOP = [$AP0LOOP]  AP1LOOP = [$AP1LOOP] AP2LOOP = [$AP2LOOP] AP3LOOP = [$AP3LOOP]
    AP4LOOP = [$AP4LOOP]  AP5LOOP = [$AP5LOOP] AP6LOOP = [$AP6LOOP] AP7LOOP = [$AP7LOOP]
    AP0MULT = [$AP0MULT]  AP1MULT = [$AP1MULT] AP2MULT = [$AP2MULT] AP3MULT = [$AP3MULT]
    AP4MULT = [$AP4MULT]  AP5MULT = [$AP5MULT] AP6MULT = [$AP6MULT] AP7MULT = [$AP7MULT]
    L1RLength = [$L1RLength]  L2RLength = [$L2RLength] L3RLength = [$L3RLength]
    L1ROffset = [$L1ROffset]  L2ROffset = [$L2ROffset] L3ROffset = [$L3ROffset]
    FracOffsetQ1516 = [$FracOffsetQ1516]  FracIncQ1516 = [$FracIncQ1516] FracAddrLoopSel = [$FracAddrLoopSel]
    L1SubOverride = [$L1SubOverride]  L2SubOverride = [$L2SubOverride] L3SubOverride = [$L3SubOverride]
    L1SubUsed = [$L1SubUsed]  L2SubUsed = [$L2SubUsed] L3SubUsed = [$L3SubUsed]
    MemProtEnable = [$MemProtEnable]  MemProtLowAddress = [$MemProtLowAddress] MemProtHighAddress = [$MemProtHighAddress]
    OCOMBSUM0r = [$OCOMBSUM0r]  OCOMBSUM1r = [$OCOMBSUM1r] UpdateCombSum = [$UpdateCombSum]
    OCOMBSUM0i = [$OCOMBSUM0i]  OCOMBSUM1i = [$OCOMBSUM1i]
    MinMaxPos = [$MinMaxPos]  MinMaxValue = [$MinMaxValue] MinMaxCtrl = [$MinMaxCtrl]
    MinMaxPosOverall = [$MinMaxPosOverall]  MinMaxValueOverall = [$MinMaxValueOverall] UpdateMinMax = [$UpdateMinMax]
$- endif

'''

template_meta = '''\
# name=Meta Generic
# processor_family=meta
# version=0.1
# view_option=Show default per-thread registers:ShowDefaultPerThread:True
# view_option=Show control registers:ShowControl:True
{%- set local_data = cpu_info.get('local_data_registers', 0) %}
{%- set local_addr = cpu_info.get('local_address_registers', 0) %}
{%- set glob_data = cpu_info.get('global_data_registers', 0) %}
{%- set glob_addr = cpu_info.get('global_address_registers', 0) %}
{%- if glob_data or glob_addr %}
# view_option=Show global registers:ShowGlobal:False
{%- endif %}
{%- if glob_data > 8 or glob_addr > 4 %}
# view_option=Show extended per-thread registers:ShowExtendedPerThread:False
{%- endif %}
{%- if cpu_info.get('has_dsp') %}
# view_option=Show DSP extension registers:ShowDSPExtension:False
# view_option=Show DSP accumulator registers:ShowDSPAccumulator:False
{%- endif %}
{%- if cpu_info.get('has_fpu') %}
# view_option=Show float registers:ShowFloatingPoint:False
# view_option=---
# view_option=Show Floating Point Registers as Hex:ShowFloatingPointAsHex:True
{% endif %}
{%- if ShowDefaultPerThread %}
    D0Re0 = [$D0Re0 hex] D1Re0 = [$D1Re0 hex] A0StP    = [$A0StP hex]   A1GbP     = [$A1GbP hex]
    D0Ar6 = [$D0Ar6 hex] D1Ar5 = [$D1Ar5 hex] A0FrP    = [$A0FrP hex]   A1LbP     = [$A1LbP hex]
    D0Ar4 = [$D0Ar4 hex] D1Ar3 = [$D1Ar3 hex] A0.2     = [$A0.2 hex]    A1.2      = [$A1.2 hex]
    D0Ar2 = [$D0Ar2 hex] D1Ar1 = [$D1Ar1 hex] A0.3     = [$A0.3 hex]    A1.3      = [$A1.3 hex]
    D0FrT = [$D0FrT hex] D1RtP = [$D1RtP hex]
    D0.5  = [$D0.5 hex]  D1.5  = [$D1.5 hex]  TXRPT    = [$TXRPT hex]   {%-if 'txbpobits' in registers%}TXBPOBITS = [$TXBPOBITS hex]{%-endif%}
    D0.6  = [$D0.6 hex]  D1.6  = [$D1.6 hex]  TXTIMER  = [$TXTIMER hex] TXTIMERI  = [$TXTIMERI hex]
    D0.7  = [$D0.7 hex]  D1.7  = [$D1.7 hex]
{%- endif %}
{%- if ShowExtendedPerThread and local_data > 8 %}
    D0.8  = [$D0.8 hex]  D1.8  = [$D1.8 hex]  A0.4 = [$A0.4 hex] A1.4 = [$A1.4 hex]
    D0.9  = [$D0.9 hex]  D1.9  = [$D1.9 hex]  A0.5 = [$A0.5 hex] A1.5 = [$A1.5 hex]
    D0.10 = [$D0.10 hex] D1.10 = [$D1.10 hex] A0.6 = [$A0.6 hex] A1.6 = [$A1.6 hex]
    D0.11 = [$D0.11 hex] D1.11 = [$D1.11 hex] A0.7 = [$A0.7 hex] A1.7 = [$A1.7 hex]
    D0.12 = [$D0.12 hex] D1.12 = [$D1.12 hex]
    D0.13 = [$D0.13 hex] D1.13 = [$D1.13 hex]
    D0.14 = [$D0.14 hex] D1.14 = [$D1.14 hex]
    D0.15 = [$D0.15 hex] D1.15 = [$D1.15 hex]
{%- endif %}
{%- if ShowGlobal %}
    {%- for n in range(glob_data) %}
        {%- set d0 = 'D0.%d' % (local_data+n) %}
        {%- set d1 = 'D1.%d' % (local_data+n) %}
        {%- set a0 = 'A0.%d' % (local_addr+n) %}
        {%- set a1 = 'A1.%d' % (local_addr+n) %}
        {{d0}} = [${{d0}} hex] {{d1}} = [${{d1}} hex]  {% if n < glob_addr %}{{a0}} = [${{a0}} hex]  {{a1}} = [${{a1}} hex]{% endif %}
    {%- endfor %}
{%- endif %}
{%- if ShowDefaultPerThread %}
    [] [] [] [] TXENABLE = [$TXENABLE hex]
    PC    = [$PC hex] PCX   = [$PCX hex] TXSTATUS = [$TXSTATUS hex] [$TXSTATUS bits bits=znocZNOC]
{% endif %}
{%- if ShowControl %}

    {%- if cpu_info.get('is_mtx') %}
        TXSTAT    = [$TXSTAT hex]  TXMASK    = [$TXMASK hex]    TXPOLL    = [$TXPOLL hex]   TXGPIOI   = [$TXGPIOI hex]
        TXSTATI   = [$TXSTATI hex] TXMASKI   = [$TXMASKI hex]   TXPOLLI   = [$TXPOLLI hex]  TXGPIOO   = [$TXGPIOO hex]
        
        TXMODE    = [$TXMODE hex]  TXTACTCYC = [$TXTACTCYC hex] TXIDLECYC = [$TXIDLECYC hex]
    {%- else %}
        TXSTAT    = [$TXSTAT hex]  TXMASK    = [$TXMASK hex]    TXPOLL    = [$TXPOLL hex]
        TXSTATI   = [$TXSTATI hex] TXMASKI   = [$TXMASKI hex]   TXPOLLI   = [$TXPOLLI hex]

        TXCATCH0  = [$TXCATCH0 hex] TXAMAREG0 = [$TXAMAREG0 hex] TXCLKCTRL = [$TXCLKCTRL hex]  TXDEFR    = [$TXDEFR hex]
        TXCATCH1  = [$TXCATCH1 hex] TXAMAREG1 = [$TXAMAREG1 hex] TXDIVTIME = [$TXDIVTIME hex]  TXPRIVEXT = [$TXPRIVEXT hex]
        TXCATCH2  = [$TXCATCH2 hex] TXAMAREG2 = [$TXAMAREG2 hex] TXTACTCYC = [$TXTACTCYC hex]
        TXCATCH3  = [$TXCATCH3 hex] TXAMAREG3 = [$TXAMAREG3 hex] TXIDLECYC = [$TXIDLECYC hex]
    {%- endif %}
{%- endif %}
{%- if (ShowDSPAccumulator or ShowDSPExtension) and cpu_info.get('has_dsp')%}

    TXMODE    = [$TXMODE hex]
{%- endif %}
{%- if ShowDSPAccumulator and cpu_info.get('has_dsp')%}

    AC0.0     = [$AC0.0 hex width=10] AC0.1     = [$AC0.1 hex width=10] AC0.2    = [$AC0.2 hex width=10] AC0.3    = [$AC0.3 hex width=10]
    AC1.0     = [$AC1.0 hex width=10] AC1.1     = [$AC1.1 hex width=10] AC1.2    = [$AC1.2 hex width=10] AC1.3    = [$AC1.3 hex width=10]
{%- endif %}
{%- if ShowDSPExtension and cpu_info.get('has_dsp') %}

    D0AR.0    = [$D0AR.0 hex] D0AR.1    = [$D0AR.1 hex] D0AW.0   = [$D0AW.0 hex] D0AW.1   = [$D0AW.1 hex]
    D1AR.0    = [$D1AR.0 hex] D1AR.1    = [$D1AR.1 hex] D1AW.0   = [$D1AW.0 hex] D1AW.1   = [$D1AW.1 hex]
    D0BR.0    = [$D0BR.0 hex] D0BR.1    = [$D0BR.1 hex] D0BW.0   = [$D0BW.0 hex] D0BW.1   = [$D0BW.1 hex]
    D1BR.0    = [$D1BR.0 hex] D1BR.1    = [$D1BR.1 hex] D1BW.0   = [$D1BW.0 hex] D1BW.1   = [$D1BW.1 hex]

    D0ARI.0   = [$D0ARI.0 hex] D0ARI.1   = [$D0ARI.1 hex] D0AWI.0  = [$D0AWI.0 hex] D0AWI.1  = [$D0AWI.1 hex]
    D1ARI.0   = [$D1ARI.0 hex] D1ARI.1   = [$D1ARI.1 hex] D1AWI.0  = [$D1AWI.0 hex] D1AWI.1  = [$D1AWI.1 hex]
    D0BRI.0   = [$D0BRI.0 hex] D0BRI.1   = [$D0BRI.1 hex] D0BWI.0  = [$D0BWI.0 hex] D0BWI.1  = [$D0BWI.1 hex]
    D1BRI.0   = [$D1BRI.0 hex] D1BRI.1   = [$D1BRI.1 hex] D1BWI.0  = [$D1BWI.0 hex] D1BWI.1  = [$D1BWI.1 hex]

    T0        = [$T0 hex] T1        = [$T1 hex] T2       = [$T2 hex] T3       = [$T3 hex]
    T4        = [$T4 hex] T5        = [$T5 hex] T6       = [$T6 hex] T7       = [$T7 hex]
    T8        = [$T8 hex] T9        = [$T9 hex] TA       = [$TA hex] TB       = [$TB hex]
    TC        = [$TC hex] TD        = [$TD hex] TE       = [$TE hex] TF       = [$TF hex]
{%- endif %}
{%- if (ShowDSPAccumulator or ShowDSPExtension) and cpu_info.get('has_dsp') %}

    TXL1START = [$TXL1START hex] TXL2START = [$TXL2START hex] TXDRCTRL = [$TXDRCTRL hex] TXDRSIZE = [$TXDRSIZE hex]
    TXL1END   = [$TXL1END hex] TXL2END   = [$TXL2END hex] TXMRSIZE = [$TXMRSIZE hex]
    TXL1COUNT = [$TXL1COUNT hex] TXL2COUNT = [$TXL2COUNT hex]
{%- endif %}
{%- if ShowFloatingPoint and cpu_info.get('has_fpu') %}

    {% if cpu_info.get('float_registers') %}
        {%- for regs in range(cpu_info.get('float_registers')) | batch(4) %}
            {%- for n in regs %}FX.{{n}} = [$FX.{{n}} floating_point width_bytes=4]{% endfor %}
        {% endfor %}
    {%- endif %}    
    {% if cpu_info.get('double_registers') %}
        {%- for regs in range(0, cpu_info.get('double_registers') * 2, 2) | batch(4) %}
            {%- for n in regs %}FX.{{n}}:FX.{{n+1}} = [$FX.{{n}}:FX.{{n+1}} floating_point width_bytes=8]{% endfor %}
        {% endfor %}
    {%- endif %}
{%- endif %}
'''

template_mips = '''\
# name=MIPS Generic with n64
# processor_family = mips
# version=1.3
# view_option=Show general purpose registers:ShowDefaultPerThread:True
$ if cpu_info.get('has_dsp1')
# view_option=Show DSP accumulator registers:ShowDSPAccumulator:True:{{cpu_info.get('dsp_enabled')}}
$ endif
$ if cpu_info.get('has_fpu')
# view_option=Show floating point registers:ShowFloatingPoint:True:{{cpu_info.get('fpu_enabled')}}
$ endif
# view_option=Show CP0 registers:ShowCP0:False
$ set msa_available = cpu_info.get('has_msa') and 'msair' in registers
$ if msa_available
# view_option=Show MSA registers:ShowMSA:True:{{cpu_info.get('msa_enabled')}}
# view_option=Show MSA control registers:ShowMSAControl:True:{{cpu_info.get('msa_enabled')}}
$ endif
# view_option=---
$ if msa_available
$ set enable_formatting = cpu_info.get('msa_enabled') and ShowMSA
# view_option=>>>:MSA Formatting
# view_option=Show MSA registers as 8 bit integers|Show MSA registers as 16 bit integers|Show MSA registers as 32 bit integers|Show MSA registers as 64 bit integers|Show MSA registers as 128 bit integers|Show MSA registers as 16 bit fixed points|Show MSA registers as 32 bit fixed points|Show MSA registers as 32 bit floating points|Show MSA registers as 64 bit floating points:MSAFormat:3:{{enable_formatting}}:False
# view_option=<<<
# view_option=Show fixed point registers as hex:ShowFixedPointAsHex:False
$ endif
$ if (cpu_info.get('has_fpu') and cpu_info.get('fpu_enabled')) or msa_available
# view_option=Show floating point registers as hex:ShowFloatingPointAsHex:False
$ endif
$ set is_gdbserver = cpu_info.get('is_gdbserver', False)
$ if is_gdbserver
$   set supported_cp0_regs = cpu_info.get('supported_cp0_regs', '').lower().split()
$   set epc_supported = not supported_cp0_regs or "epc" in supported_cp0_regs 
$ else
$   set supported_cp0_regs = []
$   set epc_supported = True
$ endif
$ set is32 = cpu_info.get('cpu_is_32bit')
$ if is32
$   set addrwidth = 'width=8'
$ else
$   set addrwidth = 'width=16'
$ endif
$ set extra_fpu_regs = cpu_info.get('extra_fpu_regs', 'fccr fenr fexr').lower().split()
$ set has_fccr = (is32 and "fccr" in extra_fpu_regs)
$ set has_fenr = "fenr" in extra_fpu_regs
$ set has_fexr = "fexr" in extra_fpu_regs
$ if ShowDefaultPerThread
$ if ABI == 'o32' or ABI == 'o64'
zero   = [$zero hex {{addrwidth}}]   at    = [$at  hex {{addrwidth}}]   v0  = [$v0  hex {{addrwidth}}]  v1       = [$v1   hex {{addrwidth}}]
a0     = [$a0   hex {{addrwidth}}]   a1    = [$a1  hex {{addrwidth}}]   a2  = [$a2  hex {{addrwidth}}]  a3       = [$a3   hex {{addrwidth}}]
t0     = [$t0   hex {{addrwidth}}]   t1    = [$t1  hex {{addrwidth}}]   t2  = [$t2  hex {{addrwidth}}]  t3       = [$t3   hex {{addrwidth}}]
t4     = [$t4   hex {{addrwidth}}]   t5    = [$t5  hex {{addrwidth}}]   t6  = [$t6  hex {{addrwidth}}]  t7       = [$t7   hex {{addrwidth}}]
s0     = [$s0   hex {{addrwidth}}]   s1    = [$s1  hex {{addrwidth}}]   s2  = [$s2  hex {{addrwidth}}]  s3       = [$s3   hex {{addrwidth}}]
s4     = [$s4   hex {{addrwidth}}]   s5    = [$s5  hex {{addrwidth}}]   s6  = [$s6  hex {{addrwidth}}]  s7       = [$s7   hex {{addrwidth}}]
t8     = [$t8   hex {{addrwidth}}]   t9    = [$t9  hex {{addrwidth}}]   k0  = [$k0  hex {{addrwidth}}]  k1       = [$k1   hex {{addrwidth}}]
gp     = [$gp   hex {{addrwidth}}]   sp    = [$sp  hex {{addrwidth}}]   s8  = [$s8  hex {{addrwidth}}]  ra       = [$ra   hex {{addrwidth}}]
$ elif ABI == 'n32' or ABI == 'n64'
zero   = [$zero hex {{addrwidth}}]   at    = [$at  hex {{addrwidth}}]   v0  = [$v0  hex {{addrwidth}}]  v1       = [$v1   hex {{addrwidth}}]
a0     = [$a0   hex {{addrwidth}}]   a1    = [$a1  hex {{addrwidth}}]   a2  = [$a2  hex {{addrwidth}}]  a3       = [$a3   hex {{addrwidth}}]
a4     = [$a4   hex {{addrwidth}}]   a5    = [$a5  hex {{addrwidth}}]   a6  = [$a6  hex {{addrwidth}}]  a7       = [$a7   hex {{addrwidth}}]
t0     = [$t0   hex {{addrwidth}}]   t1    = [$t1  hex {{addrwidth}}]   t2  = [$t2  hex {{addrwidth}}]  t3       = [$t3   hex {{addrwidth}}]
s0     = [$s0   hex {{addrwidth}}]   s1    = [$s1  hex {{addrwidth}}]   s2  = [$s2  hex {{addrwidth}}]  s3       = [$s3   hex {{addrwidth}}]
s4     = [$s4   hex {{addrwidth}}]   s5    = [$s5  hex {{addrwidth}}]   s6  = [$s6  hex {{addrwidth}}]  s7       = [$s7   hex {{addrwidth}}]
t8     = [$t8   hex {{addrwidth}}]   t9    = [$t9  hex {{addrwidth}}]   k0  = [$k0  hex {{addrwidth}}]  k1       = [$k1   hex {{addrwidth}}]
gp     = [$gp   hex {{addrwidth}}]   sp    = [$sp  hex {{addrwidth}}]   s8  = [$s8  hex {{addrwidth}}]  ra       = [$ra   hex {{addrwidth}}]
$ elif ABI == 'p32' or ABI == 'p64'
zero   = [$zero hex {{addrwidth}}]   at    = [$at  hex {{addrwidth}}]   t4  = [$t4  hex {{addrwidth}}]  t5       = [$t5   hex {{addrwidth}}]
a0     = [$a0   hex {{addrwidth}}]   a1    = [$a1  hex {{addrwidth}}]   a2  = [$a2  hex {{addrwidth}}]  a3       = [$a3   hex {{addrwidth}}]
a4     = [$a4   hex {{addrwidth}}]   a5    = [$a5  hex {{addrwidth}}]   a6  = [$a6  hex {{addrwidth}}]  a7       = [$a7   hex {{addrwidth}}]
t0     = [$t0   hex {{addrwidth}}]   t1    = [$t1  hex {{addrwidth}}]   t2  = [$t2  hex {{addrwidth}}]  t3       = [$t3   hex {{addrwidth}}]
s0     = [$s0   hex {{addrwidth}}]   s1    = [$s1  hex {{addrwidth}}]   s2  = [$s2  hex {{addrwidth}}]  s3       = [$s3   hex {{addrwidth}}]
s4     = [$s4   hex {{addrwidth}}]   s5    = [$s5  hex {{addrwidth}}]   s6  = [$s6  hex {{addrwidth}}]  s7       = [$s7   hex {{addrwidth}}]
t8     = [$t8   hex {{addrwidth}}]   t9    = [$t9  hex {{addrwidth}}]   k0  = [$k0  hex {{addrwidth}}]  k1       = [$k1   hex {{addrwidth}}]
gp     = [$gp   hex {{addrwidth}}]   sp    = [$sp  hex {{addrwidth}}]   fp  = [$fp  hex {{addrwidth}}]  ra       = [$ra   hex {{addrwidth}}]
$ else
r0     = [$r0   hex {{addrwidth}}]   r1    = [$r1  hex {{addrwidth}}]   r2  = [$r2  hex {{addrwidth}}]  r3       = [$r3   hex {{addrwidth}}]
r4     = [$r4   hex {{addrwidth}}]   r5    = [$r5  hex {{addrwidth}}]   r6  = [$r6  hex {{addrwidth}}]  r7       = [$r7   hex {{addrwidth}}]
r8     = [$r8   hex {{addrwidth}}]   r9    = [$r9  hex {{addrwidth}}]   r10 = [$r10 hex {{addrwidth}}]  r11      = [$r11  hex {{addrwidth}}]
r12    = [$r12  hex {{addrwidth}}]   r13   = [$r13 hex {{addrwidth}}]   r14 = [$r14 hex {{addrwidth}}]  r15      = [$r15  hex {{addrwidth}}]
r16    = [$r16  hex {{addrwidth}}]   r17   = [$r17 hex {{addrwidth}}]   r18 = [$r18 hex {{addrwidth}}]  r19      = [$r19  hex {{addrwidth}}]
r20    = [$r20  hex {{addrwidth}}]   r21   = [$r21 hex {{addrwidth}}]   r22 = [$r22 hex {{addrwidth}}]  r23      = [$r23  hex {{addrwidth}}]
r24    = [$r24  hex {{addrwidth}}]   r25   = [$r25 hex {{addrwidth}}]   r26 = [$r26 hex {{addrwidth}}]  r27      = [$r27  hex {{addrwidth}}]
r28    = [$r28  hex {{addrwidth}}]   r29   = [$r29 hex {{addrwidth}}]   r30 = [$r30 hex {{addrwidth}}]  r31      = [$r31  hex {{addrwidth}}]
$endif
$ if not (cpu_info.get('has_r6_instruction_set') or cpu_info.get('has_nano_mips')) or cpu_info.get('has_dsp3')
hi     = [$hi hex {{addrwidth}}]     lo    = [$lo hex {{addrwidth}}]    []    []                        pc       = [$pc   hex {{addrwidth}}]
$ else
[]       []                          []      []                         []    []                        pc       = [$pc   hex {{addrwidth}}]
$ endif
status = [$status hex] cause = [$cause hex] {%if epc_supported%}epc = [$epc hex  {{addrwidth}}]{%else%}[] []{%endif%}  badvaddr = [$badvaddr hex  {{addrwidth}}]
$ endif

$ if ShowDSPAccumulator and cpu_info.get('has_dsp1') and cpu_info.get('dsp_enabled')
    {{- "\n" -}}
    hi1 = [$hi1 hex] lo1 = [$lo1 hex] hi2        = [$hi2        hex] lo2 = [$lo2 hex]
    hi3 = [$hi3 hex] lo3 = [$lo3 hex] dspcontrol = [$dspcontrol hex]
$ endif

$ if ShowFloatingPoint and cpu_info.get('has_fpu') and cpu_info.get('fpu_enabled')
     {{ " " }}
    $ if cpu_info.get('fpu_max_register_size', 32) == 64
        $ if cpu_info.get('fpu_split_64bit_mode')
            [$ text text="d0   =" is_break=True] [$d0  floating_point width_bytes=8] d2   = [$d2  floating_point width_bytes=8] d4   = [$d4  floating_point width_bytes=8] d6   = [$d6  floating_point width_bytes=8]
            d8   =                               [$d8  floating_point width_bytes=8] d10  = [$d10 floating_point width_bytes=8] d12  = [$d12 floating_point width_bytes=8] d14  = [$d14 floating_point width_bytes=8]
            d16  =                               [$d16 floating_point width_bytes=8] d18  = [$d18 floating_point width_bytes=8] d20  = [$d20 floating_point width_bytes=8] d22  = [$d22 floating_point width_bytes=8]
            d24  =                               [$d24 floating_point width_bytes=8] d26  = [$d26 floating_point width_bytes=8] d28  = [$d28 floating_point width_bytes=8] d30  = [$d30 floating_point width_bytes=8]
        $ else
            [$ text text="d0   =" is_break=True] [$d0  floating_point width_bytes=8] d1   = [$d1  floating_point width_bytes=8] d2   = [$d2  floating_point width_bytes=8] d3   = [$d3  floating_point width_bytes=8] 
            d4   =                               [$d4  floating_point width_bytes=8] d5   = [$d5  floating_point width_bytes=8] d6   = [$d6  floating_point width_bytes=8] d7   = [$d7  floating_point width_bytes=8]
            d8   =                               [$d8  floating_point width_bytes=8] d9   = [$d9  floating_point width_bytes=8] d10  = [$d10 floating_point width_bytes=8] d11  = [$d11 floating_point width_bytes=8]
            d12  =                               [$d12 floating_point width_bytes=8] d13  = [$d13 floating_point width_bytes=8] d14  = [$d14 floating_point width_bytes=8] d15  = [$d15 floating_point width_bytes=8]
            d16  =                               [$d16 floating_point width_bytes=8] d17  = [$d17 floating_point width_bytes=8] d18  = [$d18 floating_point width_bytes=8] d19  = [$d19 floating_point width_bytes=8]
            d20  =                               [$d20 floating_point width_bytes=8] d21  = [$d21 floating_point width_bytes=8] d22  = [$d22 floating_point width_bytes=8] d23  = [$d23 floating_point width_bytes=8]
            d24  =                               [$d24 floating_point width_bytes=8] d25  = [$d25 floating_point width_bytes=8] d26  = [$d26 floating_point width_bytes=8] d27  = [$d27 floating_point width_bytes=8]
            d28  =                               [$d28 floating_point width_bytes=8] d29  = [$d29 floating_point width_bytes=8] d30  = [$d30 floating_point width_bytes=8] d31  = [$d31 floating_point width_bytes=8]
        $ endif
    $endif
    f0   = [$f0  floating_point width_bytes=4] f1   = [$f1  floating_point width_bytes=4] f2   = [$f2  floating_point width_bytes=4] f3   = [$f3  floating_point width_bytes=4]
    f4   = [$f4  floating_point width_bytes=4] f5   = [$f5  floating_point width_bytes=4] f6   = [$f6  floating_point width_bytes=4] f7   = [$f7  floating_point width_bytes=4]
    f8   = [$f8  floating_point width_bytes=4] f9   = [$f9  floating_point width_bytes=4] f10  = [$f10 floating_point width_bytes=4] f11  = [$f11 floating_point width_bytes=4]
    f12  = [$f12 floating_point width_bytes=4] f13  = [$f13 floating_point width_bytes=4] f14  = [$f14 floating_point width_bytes=4] f15  = [$f15 floating_point width_bytes=4]
    f16  = [$f16 floating_point width_bytes=4] f17  = [$f17 floating_point width_bytes=4] f18  = [$f18 floating_point width_bytes=4] f19  = [$f19 floating_point width_bytes=4]
    f20  = [$f20 floating_point width_bytes=4] f21  = [$f21 floating_point width_bytes=4] f22  = [$f22 floating_point width_bytes=4] f23  = [$f23 floating_point width_bytes=4]
    f24  = [$f24 floating_point width_bytes=4] f25  = [$f25 floating_point width_bytes=4] f26  = [$f26 floating_point width_bytes=4] f27  = [$f27 floating_point width_bytes=4]
    f28  = [$f28 floating_point width_bytes=4] f29  = [$f29 floating_point width_bytes=4] f30  = [$f30 floating_point width_bytes=4] f31  = [$f31 floating_point width_bytes=4]
    {{ " " }}
    [$ text text="fir  =" is_break=True] [$fir hex width=8] {%if has_fccr%}fccr = [$fccr hex width=8]{%endif%} {%if has_fenr%}fenr = [$fenr hex width=8]{%endif%} {%if has_fexr%}fexr = [$fexr hex width=8]{%endif%} {%if is32%}{{"\n"}}{%endif%}fcsr = [$fcsr hex width=8]
$ endif

$ if msa_available and cpu_info.get('msa_enabled')
    $if ShowMSA
        $ set element_sizes = [8, 16, 32, 64, 128, 16, 32, 32, 64]
        {# MSAFormat will not be set if the template is being loaded for the first time #}
        $ set MSAFormat = MSAFormat if MSAFormat is defined else 4
        $ set elements = 128//(element_sizes[MSAFormat])
        $ set element_size = element_sizes[MSAFormat]
        $ if MSAFormat is defined
            $ if 0 <= MSAFormat < 5
                $ for w in range(0, 32)
                    $ set is_break = not w
                    [$ text text="w{{w}} = " is_break={{is_break}}] {% for element in range(elements, 0, -1) %}[$w{{w}} hex width={{element_size//4}} bit_start={{(element-1)*element_size}} bit_end={{(element*element_size)-1}}]{% endfor %} 
                $ endfor
            $ elif 5 <= MSAFormat < 7
                $ if MSAFormat == 5
                    $ set width_n = 15
                $ else
                    $ set width_n = 31
                $ endif
                
                $ for w in range(0, 32)
                    $ set is_break = not w
                    [$ text text="w{{w}} = " is_break={{is_break}}] {% for element in range(elements, 0, -1) %}[$w{{w}} fixed_point width_m=0 width_n={{width_n}} bit_start={{(element-1)*element_size}}]{% endfor %} 
                $ endfor 
            $ elif MSAFormat >= 7
                $ set width_bytes = element_size//8
                $ for w in range(0, 32)
                    $ set is_break = not w
                    [$ text text="w{{w}} = " is_break={{is_break}}] {% for element in range(elements, 0, -1) %}[$w{{w}} floating_point width_bytes={{width_bytes}} bit_start={{(element-1)*element_size}}]{% endfor %} 
                $ endfor 
            $ endif
        $ endif
    $ endif
    
    $ if ShowMSAControl
        {{- "\n" -}}
        [$ text text="msair     =" is_break=True] [$msair     hex] msacsr     = [$msacsr     hex]
        msaaccess =                               [$msaaccess hex] msasave    = [$msasave    hex]
        msamodify =                               [$msamodify hex] msarequest = [$msarequest hex]
        msamap    =                               [$msamap    hex] msaunmap   = [$msaunmap   hex]
    $ endif    
$ endif
{%- if ShowCP0 -%}
$- macro cp0_cell(name, name_width)
    {{name.ljust(name_width)}} [${{name}} hex width={%if not is32 and name in cp0_64bit_names%}16{%else%}8{%endif%} ]
$- endmacro
$- macro all_cp0_cells(all_names, name_width)
$-  if supported_cp0_regs
$-      set supported_names = []
$-      for name in all_names
$-          if name|lower in supported_cp0_regs
$-              set _want_side_effect = supported_names.append(name)
$-          endif
$-      endfor
$-  else
$-      set supported_names = all_names
$-  endif
$-  for row in supported_names | batch(4)
$-      for reg in row
            {{ cp0_cell(reg, name_width) }}
$-      endfor
        {{-"\n"-}}
$-  endfor
$- endmacro
$ set all_cp0_names = [
    "Index", "MVPControl", "MVPConf0", "MVPConf1", "cp0.0.4", "cp0.0.5", "cp0.0.6", "cp0.0.7", "Random", "VPEControl", "VPEConf0", "VPEConf1", "YQMask", "VPESchedule", "VPEScheFBack", "VPEOpt",
    "EntryLo0", "TCStatus", "TCBind", "TCRestart", "TCHalt", "TCContext", "TCSchedule", "TCScheFBack", "EntryLo1", "GlobalNumber", "cp0.3.2", "cp0.3.3", "cp0.3.4", "cp0.3.5", "cp0.3.6", "TCOpt",
    "Context", "ContextConfig", "UserLocal", "XContextConfig", "DebugContextID", "MMID", "cp0.4.6", "cp0.4.7", "PageMask", "PageGrain", "SegCtl0", "SegCtl1", "SegCtl2", "cp0.5.5", "cp0.5.6",
    "cp0.5.7", "Wired", "SRSConf0", "SRSConf1", "SRSConf2", "SRSConf3", "SRSConf4", "cp0.6.6", "cp0.6.7", "HWREna", "cp0.7.1", "cp0.7.2", "cp0.7.3", "cp0.7.4", "cp0.7.5", "cp0.7.6", "cp0.7.7",
    "BadVAddr", "BadInstr", "BadInstrP", "cp0.8.3", "cp0.8.4", "cp0.8.5", "cp0.8.6", "cp0.8.7", "Count", "cp0.9.1", "cp0.9.2", "cp0.9.3", "cp0.9.4", "cp0.9.5", "cp0.9.6", "cp0.9.7", "EntryHi",
    "cp0.10.1", "cp0.10.2", "cp0.10.3", "GuestCtl1", "cp0.10.5", "cp0.10.6", "cp0.10.7", "Compare", "cp0.11.1", "cp0.11.2", "cp0.11.3", "cp0.11.4", "cp0.11.5", "cp0.11.6", "cp0.11.7", "Status",
    "IntCtl", "SRSCtl", "SRSMap", "View_IPL", "SRSMap2", "GuestCtl0", "cp0.12.7", "Cause", "cp0.13.1", "cp0.13.2", "cp0.13.3", "View_RIPL", "cp0.13.5", "cp0.13.6", "cp0.13.7", "EPC", "cp0.14.1",
    "cp0.14.2", "cp0.14.3", "cp0.14.4", "cp0.14.5", "cp0.14.6", "cp0.14.7", "PRId", "EBase", "CDMMBase", "CMGCRBase", "cp0.15.4", "cp0.15.5", "cp0.15.6", "cp0.15.7", "Config", "Config1", "Config2",
    "Config3", "Config4", "Config5", "Config6", "Config7", "LLAddr", "MAAR", "MAARI", "cp0.17.3", "cp0.17.4", "cp0.17.5", "cp0.17.6", "cp0.17.7", "WatchLo0", "WatchLo1", "WatchLo2", "WatchLo3",
    "WatchLo4", "WatchLo5", "WatchLo6", "WatchLo7", "WatchHi0", "WatchHi1", "WatchHi2", "WatchHi3", "WatchHi4", "WatchHi5", "WatchHi6", "WatchHi7", "XContext", "cp0.20.1", "cp0.20.2", "cp0.20.3",
    "cp0.20.4", "cp0.20.5", "cp0.20.6", "cp0.20.7", "cp0.21.0", "cp0.21.1", "cp0.21.2", "cp0.21.3", "cp0.21.4", "cp0.21.5", "cp0.21.6", "cp0.21.7", "cp0.22.0", "cp0.22.1", "cp0.22.2", "cp0.22.3",
    "cp0.22.4", "cp0.22.5", "cp0.22.6", "cp0.22.7", "Debug", "TraceControl", "TraceControl2", "UserTraceData1", "TraceIBPC", "TraceDBPC", "Debug2", "cp0.23.7", "DEPC", "cp0.24.1", "TraceControl3",
    "UserTraceData2", "cp0.24.4", "cp0.24.5", "cp0.24.6", "cp0.24.7", "PerfCtl0", "PerfCnt0", "PerfCtl1", "PerfCnt1", "PerfCtl2", "PerfCnt2", "PerfCtl3", "PerfCnt3", "ErrCtl", "IErrCtl", "cp0.26.2",
    "cp0.26.3", "cp0.26.4", "cp0.26.5", "cp0.26.6", "cp0.26.7", "CacheErr", "cp0.27.1", "cp0.27.2", "cp0.27.3", "cp0.27.4", "cp0.27.5", "cp0.27.6", "cp0.27.7", "ITagLo", "IDataLo", "DTagLo",
    "DDataLo", "L23TagLo", "L23DataLo", "cp0.28.6", "cp0.28.7", "ITagHi", "IDataHi", "DTagHi", "DDataHi", "cp0.29.4", "L23DataHi", "cp0.29.6", "cp0.29.7", "ErrorEPC", "cp0.30.1", "cp0.30.2",
    "cp0.30.3", "cp0.30.4", "cp0.30.5", "cp0.30.6", "cp0.30.7", "DESAVE", "cp0.31.1", "KScratch1", "KScratch2", "KScratch3", "KScratch4", "KScratch5", "KScratch6"
]
$ set cp0_64bit_names = [
    "EntryLo0", "EntryLo1", "Context", "PageMask", "BadVAddr", "EntryHi", "Status", "Cause", "EPC", "LLAddr", "WatchLo0", "XContext", "cp0.21.0", "cp0.22.0", "DEPC", "PerfCtl0", "ErrCtl", "CacheErr",
    "ITagLo", "ITagHi", "ErrorEPC", "DESAVE", "MVPControl", "VPEControl", "TCStatus", "GlobalNumber", "SRSConf0", "cp0.7.1", "cp0.9.1", "cp0.10.1", "cp0.11.1", "cp0.13.1", "cp0.14.1", "MAAR",
    "WatchLo1", "cp0.20.1", "cp0.21.1", "cp0.22.1", "TraceControl", "cp0.24.1", "PerfCnt0", "IErrCtl", "cp0.27.1", "IDataLo", "IDataHi", "cp0.30.1", "cp0.31.1", "MVPConf0", "VPEConf0", "TCBind",
    "cp0.3.2", "UserLocal", "SegCtl0", "SRSConf1", "cp0.7.2", "cp0.9.2", "cp0.10.2", "cp0.11.2", "cp0.13.2", "cp0.14.2", "CDMMBase", "MAARI", "WatchLo2", "cp0.20.2", "cp0.21.2", "cp0.22.2",
    "TraceControl2", "TraceControl3", "PerfCtl1", "cp0.26.2", "cp0.27.2", "DTagLo", "DTagHi", "cp0.30.2", "KScratch1", "MVPConf1", "VPEConf1", "TCRestart", "cp0.3.3", "XContextConfig", "SegCtl1",
    "SRSConf2", "cp0.7.3", "cp0.8.3", "cp0.9.3", "cp0.10.3", "cp0.11.3", "cp0.13.3", "cp0.14.3", "CMGCRBase", "cp0.17.3", "WatchLo3", "cp0.20.3", "cp0.21.3", "cp0.22.3", "UserTraceData1",
    "UserTraceData2", "PerfCnt1", "cp0.26.3", "cp0.27.3", "DDataLo", "DDataHi", "cp0.30.3", "KScratch2", "cp0.0.4", "YQMask", "TCHalt", "cp0.3.4", "DebugContextID", "SegCtl2", "SRSConf3", "cp0.7.4",
    "cp0.8.4", "cp0.9.4", "GuestCtl1", "cp0.11.4", "View_IPL", "View_RIPL", "cp0.14.4", "cp0.17.4", "WatchLo4", "cp0.20.4", "cp0.21.4", "cp0.22.4", "TraceIBPC", "cp0.24.4", "PerfCtl2", "cp0.26.4",
    "cp0.27.4", "L23TagLo", "cp0.29.4", "cp0.30.4", "KScratch3", "cp0.0.5", "VPESchedule", "TCContext", "cp0.3.5", "MMID", "cp0.5.5", "SRSConf4", "cp0.7.5", "cp0.8.5", "cp0.9.5", "cp0.10.5",
    "cp0.11.5", "SRSMap2", "cp0.14.5", "cp0.15.5", "cp0.17.5", "WatchLo5", "cp0.20.5", "cp0.21.5", "cp0.22.5", "TraceDBPC", "cp0.24.5", "PerfCnt2", "cp0.26.5", "cp0.27.5", "L23DataLo", "L23DataHi",
    "cp0.30.5", "KScratch4", "cp0.0.6", "VPEScheFBack", "TCSchedule", "cp0.3.6", "cp0.4.6", "cp0.5.6", "cp0.7.6", "cp0.8.6", "cp0.9.6", "cp0.10.6", "cp0.11.6", "GuestCtl0", "cp0.13.6", "cp0.14.6",
    "cp0.15.6", "Config6", "cp0.17.6", "WatchLo6", "cp0.20.6", "cp0.21.6", "cp0.22.6", "Debug2", "cp0.24.6", "PerfCtl3", "cp0.26.6", "cp0.27.6", "cp0.28.6", "cp0.29.6", "cp0.30.6", "KScratch5",
    "cp0.0.7", "VPEOpt", "TCScheFBack", "TCOpt", "cp0.4.7", "cp0.5.7", "cp0.6.7", "cp0.7.7", "cp0.8.7", "cp0.9.7", "cp0.10.7", "cp0.11.7", "cp0.12.7", "cp0.13.7", "cp0.14.7", "cp0.15.7", "Config7",
    "cp0.17.7", "WatchLo7", "cp0.20.7", "cp0.21.7", "cp0.22.7", "cp0.23.7", "cp0.24.7", "PerfCnt3", "cp0.26.7", "cp0.27.7", "cp0.28.7", "cp0.29.7", "cp0.30.7", "KScratch6"
]
{{all_cp0_cells(all_cp0_names, 14)}}
{% endif %}
'''

reg_templates = [template_mips_minimal, template_mcp, template_meta, template_mips]
# [[[end]]]