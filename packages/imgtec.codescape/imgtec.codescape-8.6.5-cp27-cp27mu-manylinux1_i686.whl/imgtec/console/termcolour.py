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


enabled = False

ansi_fore = 30
ansi_back = 40
ansi_colours = dict(
    black = 0,
    blue = 4,
    green = 2,
    cyan = 6,
    red = 1,
    magenta =5,
    yellow =3,
    light_grey = 7,
)

ansi_bold_colours = dict(
    dark_grey      = ansi_colours['black'],
    bright_blue    = ansi_colours['blue'] ,
    bright_green   = ansi_colours['green'] ,
    bright_cyan    = ansi_colours['cyan'] ,
    bright_red     = ansi_colours['red'] ,
    bright_magenta = ansi_colours['magenta'] ,
    bright_yellow  = ansi_colours['yellow'] ,
    white          = ansi_colours['light_grey'],
)

def ansi_colourizer(s, fore=None, back=None):
    pre = ''
    if fore is not None:
        try :
            pre += "\033[0;%dm" % (ansi_colours[fore] + ansi_fore,)
        except KeyError :
            pre += "\033[1;%dm" % (ansi_bold_colours[fore] + ansi_fore,)
    if back is not None:
        try :
            pre += "\033[%dm" % (ansi_colours[back] + ansi_back,)
        except KeyError :
            pre += "\033[%dm" % (ansi_bold_colours[back] + ansi_back,)
    if pre:
        return pre + s + '\033[0m'
    return s

def null_colourizer(s, fore=None, back=None): # pylint: disable=unused-argument
    return s

def colourizer(s, fore=None, back=None):
    c = ansi_colourizer if enabled else null_colourizer
    return c(s, fore, back)

def test():
    colours = ansi_colours.keys() + ansi_bold_colours.keys()
    displays = [''.join(x[0] for x in c.split('_')) for c in colours]
    colours = [None] + colours
    displays = ['0'] + displays
    rows = []
    for fore, fdisplay in zip(colours, displays):
        row = []
        for back, bdisplay in zip(colours, displays):
            row.append(colourizer(("%s/%s" % (fdisplay, bdisplay)).ljust(6), fore, back))
        rows.append(' '.join(row))
    return '\n' + '\n'.join(rows) + '\n'
