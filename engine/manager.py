#
# manager.py
#
# Copyright (C)2011 Julian Ceipek and Patrick Varin
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

import pygame

from textCache import TextCache
from imageCache import ImageCache
from continuousEvent import ContinuousEvent

class Manager:

    def __init__(self):
        self.inputDict = {}
        self.screenInputDict = {}

        self.readEventConfig()
        self.initializeCaches()

        #register continuous events
        self.registerEventWithCallback(pygame.MOUSEMOTION,
                                       self.handleContinuous)
        self.registerEventWithCallback(pygame.JOYBALLMOTION,
                                       self.handleContinuous)
        self.registerEventWithCallback(pygame.JOYAXISMOTION,
                                       self.handleContinuous)
        self.registerEventWithCallback(pygame.JOYHATMOTION,
                                       self.handleContinuous)

        #register discrete events
        self.registerEventWithCallback(pygame.MOUSEBUTTONUP,
                                       self.handleDiscrete)
        self.registerEventWithCallback(pygame.MOUSEBUTTONDOWN,
                                       self.handleDiscrete)
        self.registerEventWithCallback(pygame.KEYUP,
                                       self.handleDiscrete)
        self.registerEventWithCallback(pygame.KEYDOWN,
                                       self.handleDiscrete)
        self.registerEventWithCallback(pygame.JOYBUTTONUP,
                                       self.handleDiscrete)
        self.registerEventWithCallback(pygame.JOYBUTTONDOWN,
                                       self.handleDiscrete)

    def readEventConfig(self):
        """
        This reads from the config file and constructs the
        eventTypeToString dictionary
        """

        self.eventTypeToString = {}

        try:
            inputFile = open("input.config")

            for line in inputFile:
                #Strip extra whitespace
                line = line.strip()
                line = line.replace(" ","")
                line = line.replace("\t","")

                #ignore comments
                line = line.split('#')[0]
                if len(line)>0:
                    self.eventTypeToString[line.split(':')[1]] = line.split(':')[0]
                self.eventTypeToString['UserEvent'] = 'UserEvent'
        except:
            raise Exception('Unable to open input configuration file')

    def getEventString(self, event):
        if hasattr(event, 'identifier'):
            eventName = event.identifier
        else:
            eventName = pygame.event.event_name(event.type)

        return self.eventTypeToString.get(eventName,None)

    def initializeCaches(self):
        Manager.textCache = TextCache()
        Manager.imageCache = ImageCache()

    def registerUI(self, ui):
        self._ui = ui
        self._ui.setCaches(textCache=self.textCache,
                           imageCache=self.imageCache)

    def setScreenInputDict(self, dict):
        """
        Associates event types to devices and callbacks
        """
        self.screenInputDict = dict

    def registerEventWithCallback(self, eventType, callback):
        """
        Will associate an event type with a callback.
        """
        self.inputDict[eventType] = callback

    def setupWithWindow(self, window):
        """
        Give the manager various window properties needed by game objects
        """
        self.resolution = window.resolution

    def update(self, gameTime, gameFrametime):
        try:
            self._ui.update(gameTime, gameFrametime)
        except Exception as e:
            if not hasattr(self, '_ui'):
                print("================================================")
                print("                     ERROR:                     ")
                print("------------------------------------------------")
                print("The ui has not been registered with the Manager!")
                print("Do this using userInterface = UI(manager)")
                print("================================================")
            raise e

    def draw(self, surf):
        self._ui.draw(surf)

    def handle(self, event):
        """
        Will execute the function associated with the type of the pygame event passed in.
        """

        if event.type in self.inputDict:
            self.inputDict[event.type](event)
        elif event.type == pygame.USEREVENT:
            if event.discrete:
                self.handleDiscrete(event)
            else:
                self.handleContinuous(event)

    def handleDiscrete(self, event):
        """
        Handles discrete events, e.g. mouse clicks and button presses
        """
        eventName = pygame.event.event_name(event.type)

        #catch events associated with only the types
        if eventName in self.eventTypeToString:
            string = self.eventTypeToString[eventName]
            if string in self.screenInputDict:
                self.screenInputDict[string][1]()

        #extensible beyond KEYUP and KEYDOWN events to user defined events
        if hasattr(event,'key'):
            keyName = pygame.key.name(event.key)

            #differentiate between key up and key down events
            if event.type == pygame.KEYDOWN:
                keyName += '_down'
            elif event.type == pygame.KEYUP:
                keyName += '_up'

            if keyName in self.eventTypeToString:
                string = self.eventTypeToString[keyName]
                if string in self.screenInputDict:
                    self.screenInputDict[string][1]()

        #extensible beyond MOUSEBUTTONUP, MOUSEBUTTONDOWN, JOYBUTTONUP and
        #JOYBUTTONDOWN to user defined events
        if hasattr(event,'button'):
            buttonName = '%s_%d' % (eventName,event.button)
            if buttonName in self.eventTypeToString:
                string = self.eventTypeToString[buttonName]
                if string in self.screenInputDict:
                    self.screenInputDict[string][1]()


    def handleContinuous(self, event):
        """
        Handles absolute motion events, e.g. MOUSEMOTION
        """
        eventString = self.getEventString(event)
        if eventString != None:
            if eventString in self.screenInputDict:
                if hasattr(event,'rel'):
                    self.screenInputDict[eventString][1](ContinuousEvent(event.rel,relative = True))
                if hasattr(event,'pos'):
                    self.screenInputDict[eventString][1](ContinuousEvent(event.pos))

                if hasattr(event,'value'):
                    self.screenInputDict[eventString][1](ContinuousEvent(event.value))


    def post(self, event):
        pygame.event.post(Event)
