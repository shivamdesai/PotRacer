#
# window.py
#
# Copyright (C)2011 Julian Ceipek and Patrick Varin
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

import pygame
from settings import Settings

class Window:
    """
    There can only be one instance of this class.
    A window handles input from standard pygame inputs
    as well as more exotic devices like Arduinos and PICs.
    These alternative input devices must be registered with
    addInputDevice(). It also contains the game's main loop,
    the heart of the game.
    """

    def __init__(self,
        windowTitle="Powered by engine"):
        """
        active
        manager
        resolution
        displaySurface

        gameClock
        gameTime
        gameFrametime
        """
        self.active = True
        self.resolution = (Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT)
        self.fullscreen = Settings.FULLSCREEN
        self.openPygame(windowTitle)
        self.altInput = []

    def openPygame(self, windowTitle):
        pygame.init()
        pygame.display.set_caption(windowTitle)
        if self.fullscreen:
            self.displaySurface = pygame.display.set_mode(self.resolution,
                                                          pygame.FULLSCREEN)
        else:
            self.displaySurface = pygame.display.set_mode(self.resolution)
        self.gameClock = pygame.time.Clock()
        self.gameTime = 0
        self.gameFrametime = 0

    def registerManager(self, manager):
        self.manager = manager
        manager.registerEventWithCallback(pygame.QUIT, self.deactivate)
        self.manager.setupWithWindow(self)

    def addInputDevice(self, device):
        self.altInput.append(device)

    def run(self):
        """
        Initiates the game's main loop, which
        processes input, simulates the game
        logic, and tells the ui to draw itself.
        The ui is in charge of calling renderers
        as necessary, but the window will update
        the display surface every frame.
        """
        while self.active:
            for device in self.altInput:
                if device.poll():
                    for newEvent in device.getEvents():
                        pygame.event.post(newEvent)

            for event in pygame.event.get():
                self.manager.handle(event)

            self.manager.update(self.gameTime, self.gameFrametime)

            self.manager.draw(self.displaySurface)
            pygame.display.flip()

            self.gameFrametime = self.gameClock.tick(Settings.MAX_FPS)
            self.gameTime += self.gameFrametime

    def deactivate(self, event):
        self.active = False

    def cleanup(self):
        """Called when the program is closed"""
        for device in self.altInput:
            device.stop()
        print("Game Closed Successfully.")
