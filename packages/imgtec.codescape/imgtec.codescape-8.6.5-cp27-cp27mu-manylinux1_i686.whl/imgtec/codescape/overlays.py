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

class OverlayArea(object):

    def __init__(self, context, area):
        self.__context = context
        self.__area = area

    def __str__(self):
        return self.description

    def _GetCurrentIndex(self):
        return self.__context.GetCurrentOverlay(self.__area)

    def _GetActiveIndex(self):
        return self.__context.GetActiveOverlay(self.__area)

    def GetDescription(self):
        """ Get the string describing this overlay area """
        return self.__context.GetOverlayAreaString(self.__area)

    def GetOverlayByIndex(self, index):
        return Overlay(self.__context, self, self.__area, index)

    def GetOverlays(self):
        """ Return a collection of overlays in this overlay area """
        overlay_count = self.__context.GetOverlayCount(self.__area)
        return [self.GetOverlayByIndex(index) for index in range(overlay_count)]

    def GetActiveOverlay(self):
        """ Return the overlay that is currently active in this overlay area """
        return self.GetOverlayByIndex(self._GetActiveIndex())

    def GetCurrentOverlay(self):
        """ Return the current overlay in this overlay area """
        index = self._GetCurrentIndex()

        if index == -1:
            return NullOverlay(self)

        return self.GetOverlayByIndex(index)

    def SetNoCurrentOverlay(self):
        no_overlay = -1
        return self.__context.SetCurrentOverlay(self.__area, no_overlay)

    active_overlay = property(GetActiveOverlay)
    current_overlay = property(GetCurrentOverlay)
    description = property(GetDescription)
    overlays = property(GetOverlays)

class NullOverlay(object):

    def __init__(self, overlay_area):
        self.__overlay_area = overlay_area

    def __str__(self):
        return self.description

    def GetDescription(self):
        return ''

    def MakeCurrent(self):
        pass

    def GetIsCurrent(self):
        return self.overlay_area._GetCurrentIndex() == -1

    def GetIsActive(self):
        return False

    def GetOverlayArea(self):
        return self.__overlay_area

    description = property(GetDescription)
    is_active = property(GetIsActive)
    is_current = property(GetIsCurrent)
    overlay_area = property(GetOverlayArea)

class Overlay(object):

    def __init__(self, da, overlay_area, overlay_area_index, index):
        self.__context = da
        self.__overlay_area_index = overlay_area_index
        self.__overlay_area = overlay_area
        self.__index = index

    def __str__(self):
        return self.description

    def GetDescription(self):
        """ Get a string describing this overlay """
        return self.__context.GetOverlayString(self.__overlay_area_index, self.__index)

    def MakeCurrent(self):
        """ Set this overlay as the current overlay in its overlay area """
        return self.__context.SetCurrentOverlay(self.__overlay_area_index, self.__index)

    def GetIsCurrent(self):
        """ Returns True if this is the current overlay in its overlay area, False otherwise """
        return self.__index == self.overlay_area._GetCurrentIndex()

    def GetIsActive(self):
        """ Returns True if this is the active overlay in its overlay area, False otherwise """
        return self.__index == self.overlay_area._GetActiveIndex() 

    def GetOverlayArea(self):
        """ Return the overlay area to which this overlay belongs """
        return self.__overlay_area

    description = property(GetDescription)
    is_active = property(GetIsActive)
    is_current = property(GetIsCurrent)
    overlay_area = property(GetOverlayArea)
