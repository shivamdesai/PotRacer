#
# ui.py
#
# Copyright (C)2011 Julian Ceipek and Patrick Varin
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

from classMethod import ClassMethod

class UI:

    def __init__(self, manager):
        self._manager = manager
        UI.resolution = manager.resolution
        self._manager.registerUI(self)
        self.activeScreens = []

    def addActiveScreens(self, screens):
        """
        Adds an ordered list of screens to the view
        Supports lists, tuples and singletons
        """
        if type(screens) != list and type(screens) != tuple:
            screens = [screens]

        self.activeScreens.append(*screens)
        self._manager.setScreenInputDict(self.activeScreens[-1].getCallbackDict())

    def clearActiveScreens(self):
        """
        Removes all of the screens from view
        """
        self.activeScreens = []
        self._manager.setScreenInputDict({})

    def clearTopScreen(self):
        """
        Removes the top screen from view and returns it
        """
        if len(self.activeScreens)>1:
            self._manager.setScreenInputDict(self.activeScreens[-2].getCallbackDict())
        else:
            self._manager.setScreenInputDict({})
        return self.activeScreens.pop()

    def draw(self, surf):

        for screen in self.activeScreens:
            screen.draw(surf)

    def update(self, *args):

        for screen in self.activeScreens:
            screen.update(*args)

    def setCaches(textCache=None, imageCache=None):
        """
        Called by the manager to let the ui make images, text, etc.
        """
        if textCache != None:
            UI.textCache = textCache
        if imageCache != None:
            UI.imageCache = imageCache

    setCaches = ClassMethod(setCaches)
