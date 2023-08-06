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

import sys
import os
from imgtec.lib.img_settings.config import ConfigSection
from config_ini import IniConfig

def _get_ini_filename(appname):
    user = os.path.expanduser("~/.com.imgtec/%s_config" % (appname.lower(),))
    glob = "/etc/imgtec/%s_config" % (appname.lower(),)
    if os.path.isfile(user):
        return user
    if os.path.isfile(glob):
        return glob
    return user

def RegSettings(appname):
    import _winreg as winreg
    from config_reg import RegConfig
    conf = RegConfig(winreg.HKEY_CURRENT_USER, "Software\\Imagination Technologies\\%s" % appname)
    return ConfigSection(conf)

def IniSettings(appname):
    conf = IniConfig(_get_ini_filename(appname))
    return ConfigSection(conf)

if sys.platform == "win32":
    ImgSettings = RegSettings
else:
    ImgSettings = IniSettings

