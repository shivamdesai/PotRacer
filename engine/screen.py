#
# screen.py
#
# Copyright (C)2011 Julian Ceipek and Patrick Varin
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

import pygame

from classMethod import ClassMethod

class Screen(pygame.Surface):

    def __init__(self, background, size, ui):
        pygame.Surface.__init__(self, size)
        if not hasattr(self,'textCache'):
            Screen.setCaches(textCache=ui.textCache)
        if not hasattr(self,'imageCache'):
            Screen.setCaches(imageCache=ui.imageCache)
        if not hasattr(self,'resolution'):
            Screen.resolution = ui.resolution
        self.background = background
        self.size = size #Should default to screen size if not specified
        self.shouldUpdate = True
        self.initializeCallbackDict()
        self._ui = ui

    def initializeCallbackDict(self):
        self.callbackDict = {}

    def draw(self, surf):
        """
        Draws the screen's background to the surface
        Note: May be changed later to add foreground/override
        """
        if self.background:
            self.background.draw(surf)

    def setCaches(textCache=None, imageCache=None):
        """
        Called in the init method to let screens make images, text, etc.
        """
        if textCache != None:
            Screen.textCache = textCache
        if imageCache != None:
            Screen.imageCache = imageCache

    def update(self, *args):
        if self.background:
            self.background.update(self, *args)

    def getCallbackDict(self):
        """
        Used to pass callbacks to the manager.
        The dictionary maps
            configString : (deviceString, callback)
        """
        return self.callbackDict

    setCaches = ClassMethod(setCaches)
