#
# altInput.py
#
# Copyright (C)2011 Julian Ceipek and Patrick Varin
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

import pygame

class AltInput:
    """
    This is a class template for using alternative input devices with engine.
    Most of these functions need to be present and overriden
    """
    def __init__(self, *args):
        #Set up input devices here
        pass #OVERRIDE

    def poll(self):
        #Use this to check if there is an event available
        return False #OVERRIDE

    def getEvents(self):
        #get the next event(s), or wait until one is available
        pass #OVERRIDE, using makeEvent

    def stop(self):
        #cleanly close the input devices
        pass #OVERRIDE

    def makeEvent(self, identifier, value, discrete):
        #Make a pygame event with a consistent format
        #DOES NOT NEED TO BE OVERRIDEN
        eventDict = {}
        eventDict['identifier'] = identifier
        eventDict['value'] = value
        eventDict['discrete'] = discrete
        return pygame.event.Event(pygame.USEREVENT, eventDict)
