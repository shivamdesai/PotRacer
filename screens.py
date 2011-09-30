#
# screens.py
#
# Copyright (C)2011 Julian Ceipek and Patrick Varin
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

import pygame
import random
import math

from engine.screen import Screen
from engine.functions import pathJoin
from engine.background import Background

#For GameScreen:
#from engine.bar import Bar
#from gameObjects.ship import Ship, TestShip
#from gameObjects.boulder import Boulder
#from gameObjects.boulderFragment import BoulderFragment
#from backgrounds import ScrollingCodeBackground

class MenuScreen(Screen):

    def __init__(self, size, ui):
        background = Background((0,0,0))
        Screen.__init__(self, background, size, ui)
        MenuItem.textCache = Screen.textCache
        MenuItem.imageCache = Screen.imageCache
        MenuItem.resolution = Screen.resolution

        self.menuItems = []
        self.title = MenuItem('MindRush',(self.resolution[0]//2,int(self.resolution[1]/4)), scaleSize=1.5)
        self.addMenuItem(MenuItem('Play',(int(self.resolution[0]*(1/3.0)),self.resolution[1]//2,)))
        self.addMenuItem(MenuItem('Options',(int(self.resolution[0]*.5),self.resolution[1]//2)))
        self.addMenuItem(MenuItem('Exit',(int(self.resolution[0]*(2/3.0)),self.resolution[1]//2)))

        self.organizeMenuItems()

    def initializeCallbackDict(self):
        self.callbackDict = {}
        self.callbackDict['left_click'] = ('deviceString', self.leftClick)
        self.callbackDict['connectionQuality'] = ('deviceString', self.printConnectionQuality)

    def addMenuItem(self,item):
        self.menuItems.append(item)

    def draw(self, surf):
        Screen.draw(self, surf)
        self.title.draw(surf)
        for menuItem in self.menuItems:
            menuItem.draw(surf)

    def leftClick(self):
        for item in self.menuItems:
            if item.rect.collidepoint(pygame.mouse.get_pos()):
                if item.text == 'Exit':
                    pygame.event.post(pygame.event.Event(pygame.QUIT,{}))
                elif item.text == 'Play':
                    self.play()
                elif item.text == 'Options':
                    self.displayOptionsScreen()

    def organizeMenuItems(self):
        screenWidth = self.resolution[0]
        itemsLength = 0

        for item in self.menuItems:
            itemsLength += item.rect.width

        if itemsLength >= screenWidth:
            pass#FIXME, Handle this case
        else:
            itemSpace = (screenWidth-itemsLength)/(len(self.menuItems)+1)

        nextPosition = itemSpace
        for i in range(len(self.menuItems)):
            self.menuItems[i].rect.topleft = (nextPosition,self.menuItems[i].rect.topleft[1])
            nextPosition += itemSpace + self.menuItems[i].rect.width

    def play(self):
        gameScreen = GameScreen(self.resolution, self._ui)
        self._ui.addActiveScreens(gameScreen)

    def displayOptionsScreen(self):
        optionsScreen = OptionsScreen(self.resolution, self._ui)
        self._ui.addActiveScreens(optionsScreen)

    def printLook(self, event):
        print event.values

    def printConnectionQuality(self, event):
        print event.values

class MenuItem:

    def __init__(self, text, pos, scaleSize=None):
        self.text = text
        self.fontname = pathJoin(('fonts','orbitron',
            'orbitron-black.ttf'))
        self.size = int(self.resolution[1]*(1/15.0))
        if scaleSize != None:
            self.size *= scaleSize
            self.size = int(self.size)
        self.color = (255,255,255)
        self.antialias = True
        self.textSurface = self.textCache.getText(text, self.fontname,
            self.size, self.color, antialias=self.antialias)
        self.rect = self.textSurface.get_rect()
        self.rect.center = int(pos[0]), int(pos[1])

    def draw(self, surf):
        surf.blit(self.textSurface, self.rect)

class InputScreen(Screen):

    def __init__(self):
        pass

class GameScreen(Screen):

    def __init__(self, size, ui):
        Ship.imageCache = Screen.imageCache
        Boulder.imageCache = Screen.imageCache
        BoulderFragment.imageCache = Screen.imageCache
        ScrollingCodeBackground.textCache = Screen.textCache
        ScrollingCodeBackground.resolution = Screen.resolution
        Counter.textCache = Screen.textCache
        Counter.resolution = Screen.resolution

        background = ScrollingCodeBackground()
        Screen.__init__(self, background, size, ui)

        self.ships = pygame.sprite.Group()
        ship = Ship(self, pos=(size[0]/2,size[1]), screenBoundaries=(0,0)+size)
        self.ships.add(ship) #May change if we add more ships (multiplayer?)
        for ship in self.ships:
            ship.move((0,-ship.rect.height/2))
            ship.targetPosition = ship.position

        self.boulders = pygame.sprite.Group()
        self.nextBoulderTime = 0

        self.boulderFragments = pygame.sprite.Group()

        self.healthBar = Bar(100,int(size[0]*0.72),int(size[1]*0.05),fullColor=(255,0,0),emptyColor=(0,0,0), borderSize=int(size[1]*0.005), borderColor=(255,255,255))

        self.scoreDisplay = Counter(0,(self.healthBar.surface.get_rect().width,0))

        musicPath = pathJoin(('music','Music.ogg'))
        pygame.mixer.music.load(musicPath)
        pygame.mixer.music.play(-1)

    def initializeCallbackDict(self):
        self.callbackDict = {}
        self.callbackDict['look'] = ('deviceString', self.steer)
        self.callbackDict['exit'] = ('deviceString', self.exit)

    def steer(self, event):
        #move the spaceship in this method
        if hasattr(self._ui, 'getShipPosition'):
            for ship in self.ships:
                ship.targetPosition = (self._ui.getShipPosition(event.values[0]), ship.targetPosition[1])
        else:
            for ship in self.ships:
                ship.targetPosition = (event.values[0], ship.targetPosition[1])

    def exit(self):
        self._ui.clearTopScreen()
        pygame.mixer.music.stop()

    def addBoulderFragment(self, pos=(0,0), vel=(0,0), id=0):
        newBoulderFragment = BoulderFragment(self,
                               pos=pos,
                               vel=vel,
                               id=id,
                               screenBoundaries=(0,0)+self.resolution)
        self.boulderFragments.add(newBoulderFragment)

    def killBoulder(self, boulder):
        for ship in self.ships:
            ship.score += boulder.value
            self.scoreDisplay.updateValue(ship.score)
        boulder.kill()

    def draw(self, surf):
        Screen.draw(self, surf)
        self.ships.draw(surf)
        self.boulders.draw(surf)
        self.boulderFragments.draw(surf)
        self.healthBar.draw(surf,(0,0))
        self.scoreDisplay.draw(surf)

    def update(self, *args):
        gameTime, frameTime = args[:2]
        Screen.update(self, *args)
        self.ships.update(*args)
        self.boulders.update(*args)
        self.boulderFragments.update(*args)

        #For every boulder colliding with a ship,
        #kill the boulder & lose health
        for ship in self.ships:
            for boulder in ship.testMaskCollision(self.boulders):
                ship.health -= boulder.damage
                self.healthBar.updateBarWithValue(ship.health)
                boulder.kill()
                if ship.health <= 0:
                    #Kill ship, etc...
                    for ship in self.ships:
                        deadScreen = DeadScreen(self.resolution, self._ui, ship.score)
                    self._ui.clearTopScreen()
                    self._ui.addActiveScreens(deadScreen)
                    pygame.mixer.music.stop()

        if gameTime >= self.nextBoulderTime:
            boulderPos = random.randint(0,self.resolution[0]), 0
            a = (4**random.random()-1)/2
            boulderVel = (a,abs(1-a))
            self.boulders.add(Boulder(self, pos=boulderPos, vel=boulderVel, screenBoundaries=(0,0)+self.resolution))
            self.nextBoulderTime = gameTime + random.randint(200,1000)

class Counter:

    def __init__(self, value, pos, digits=8, scaleSize=None):
        self.digits = digits
        self.value = value
        self.pos = pos
        self.fontname = pathJoin(('fonts','orbitron',
            'orbitron-black.ttf'))
        self.size = int(self.resolution[1]*(1/15.0))
        if scaleSize != None:
            self.size *= scaleSize
            self.size = int(self.size)
        self.color = (255,255,255)
        self.antialias = True
        self.updateValue(self.value)

    def updateValue(self, value):
        self.textCache.clearText(self.pad(self.value), self.fontname,
            self.size, self.color, antialias=self.antialias)
        self.value = value
        self.textSurface = self.textCache.getText(self.pad(self.value),
                        self.fontname, self.size, self.color,
                        antialias=self.antialias)
        self.rect = self.textSurface.get_rect()
        self.rect.move_ip((int(self.pos[0]),int(self.pos[1])))

    def pad(self, value):
        l = len(str(value))
        if l <= self.digits:
            return '0'*(self.digits-l)+str(value)
        else:
            return '9'*(self.digits)

    def draw(self, surf):
        surf.blit(self.textSurface, self.rect)

class DeadScreen(Screen):

    def __init__(self, size, ui, score):
        background = Background((0,0,0))
        Screen.__init__(self, background, size, ui)
        MenuItem.textCache = Screen.textCache

        self.menuItems = []
        self.title = MenuItem('Game Over',(self.resolution[0]//2,int(self.resolution[1]*.15)), scaleSize=1.5)
        self.addMenuItem(MenuItem('Score: %d' % (score,),(self.resolution[0]//2, int(self.resolution[1]*.3))))
        self.addMenuItem(MenuItem('Replay',(int(self.resolution[0]*.3),self.resolution[1]//2)))
        self.addMenuItem(MenuItem('Main Menu',(int(self.resolution[0]*.7),self.resolution[1]//2)))

    def initializeCallbackDict(self):
        self.callbackDict = {}
        self.callbackDict['left_click'] = ('deviceString', self.leftClick)

    def addMenuItem(self,item):
        self.menuItems.append(item)

    def draw(self, surf):
        Screen.draw(self, surf)
        self.title.draw(surf)
        for menuItem in self.menuItems:
            menuItem.draw(surf)

    def leftClick(self):
        for item in self.menuItems:
            if item.rect.collidepoint(pygame.mouse.get_pos()):
                if item.text == 'Replay':
                    self.play()
                elif item.text == 'Main Menu':
                    self._ui.clearTopScreen()

    def play(self):
        gameScreen = GameScreen(self.resolution, self._ui)
        self._ui.addActiveScreens(gameScreen)

class OptionsScreen(Screen):

    def __init__(self, size, ui):
        background = Background((0,0,0))
        Screen.__init__(self, background, size, ui)
        MenuItem.textCache = Screen.textCache
        MenuItem.resolution = Screen.resolution

        self.title = MenuItem('Options',(self.resolution[0]//2,int(self.resolution[1]/4)), scaleSize=1.5)
        self.menuItems = []
        self.addMenuItem(MenuItem('Back',(int(self.resolution[0]*(2/3.0)),self.resolution[1]//2)))
        self.addMenuItem(MenuItem('Calibrate',(int(self.resolution[0]*(1/3.0)),self.resolution[1]//2,)))
        #self.addMenuItem(MenuItem('Input Settings',(int(self.resolution[0]*.5),self.resolution[1]//2)))

        self.organizeMenuItems()

    def initializeCallbackDict(self):
        self.callbackDict = {}
        self.callbackDict['left_click'] = ('deviceString', self.leftClick)

    def organizeMenuItems(self):
        screenWidth = self.resolution[0]
        itemsLength = 0

        for item in self.menuItems:
            itemsLength += item.rect.width

        if itemsLength >= screenWidth:
            pass#FIXME, Handle this case
        else:
            itemSpace = (screenWidth-itemsLength)/(len(self.menuItems)+1)

        nextPosition = itemSpace
        for i in range(len(self.menuItems)):
            self.menuItems[i].rect.topleft = (nextPosition,self.menuItems[i].rect.topleft[1])
            nextPosition += itemSpace + self.menuItems[i].rect.width

    def addMenuItem(self,item):
        self.menuItems.append(item)

    def draw(self, surf):
        Screen.draw(self, surf)
        self.title.draw(surf)
        for menuItem in self.menuItems:
            menuItem.draw(surf)

    def leftClick(self):
        for item in self.menuItems:
            if item.rect.collidepoint(pygame.mouse.get_pos()):
                if item.text == 'Back':
                    self._ui.clearTopScreen()
                elif item.text == 'Scores':
                    self.play(self._ui.addActiveScreens(ScoreScreen()))
                elif item.text == 'Calibrate':
                    self._ui.addActiveScreens(CalibrationScreen(self.resolution, self._ui))

class CalibrationScreen(Screen):

    def __init__(self, size, ui):
        background = Background((0,0,0))
        Screen.__init__(self, background, size, ui)
        MenuItem.textCache = Screen.textCache
        Ship.imageCache = Screen.imageCache

        self.ship = TestShip(self, pos=(size[0]/2,size[1]), screenBoundaries=(0,0)+size)
        self.ship.move((0,-self.ship.rect.height/2))

        self.menuItems = []
        self.addMenuItem(MenuItem('You are about to calibrate your eye circuit',(self.resolution[0]//2,int(self.resolution[1]*.1)),scaleSize=.75))
        self.addMenuItem(MenuItem('Follow the ship with your eyes',(self.resolution[0]//2,int(self.resolution[1]*.17)),scaleSize=.75))
        self.addMenuItem(MenuItem('Start',(self.resolution[0]//2,int(self.resolution[1]*.31)),scaleSize=.75))

        self.shipPositions = []
        self.eyePositions = []

        self.running = False

    def gatherData(self, event):
        if self.running:
            self.shipPositions.append(self.ship.position[0])
            self.eyePositions.append(event.values[0])

    def initializeCallbackDict(self):
        self.callbackDict = {}
        self.callbackDict['startCalibration'] = ('deviceString', self.start)
        self.callbackDict['left_click'] = ('deviceString', self.leftClick)
        self.callbackDict['look'] = ('deviceString', self.gatherData)

    def addMenuItem(self,item):
        self.menuItems.append(item)

    def draw(self, surf):
        Screen.draw(self, surf)
        for menuItem in self.menuItems:
            menuItem.draw(surf)
        self.ship.draw(surf)

    def update(self, *args):
        self.ship.update(*args)
        if self.ship.finished:
            self.finish()

    def leftClick(self):
        for item in self.menuItems:
            if item.rect.collidepoint(pygame.mouse.get_pos()):
                if item.text == 'Retry' or item.text == 'Start':
                    self.start()
                elif item.text == 'Continue':
                    self.close()

    def close(self):
        if len(self.eyePositions):
            eyeAve = math.fsum(self.eyePositions)/len(self.eyePositions)
            shipAve = math.fsum(self.shipPositions)/len(self.shipPositions)
            slopeTot = 0
            for eyeP, shipP in zip(self.eyePositions, self.shipPositions):
                slopeTot += (shipP-shipAve)/(eyeP-eyeAve)
            slopeAve = slopeTot/len(self.eyePositions)

            def getShipPosition(eyePosition):
                return slopeAve * (eyePosition - eyeAve) + shipAve

            self._ui.getShipPosition = getShipPosition
            print 's = %f*(e-%f)+%f' % (slopeAve, eyeAve, shipAve)

        else:
            print 'Calibration failed'
        #create the calibration function here
        self._ui.clearTopScreen()

    def finish(self):
        self.running = False

        self.menuItems = []
        self.addMenuItem(MenuItem('You have calibrated your eye circuit',(self.resolution[0]//2,int(self.resolution[1]*.1)),scaleSize=.75))


        self.addMenuItem(MenuItem('Retry',(int(self.resolution[0]*.7),int(self.resolution[1]*.31)),scaleSize=.75))
        self.addMenuItem(MenuItem('Continue',(int(self.resolution[0]*.3),int(self.resolution[1]*.31)),scaleSize=.75))


    def start(self):
        self.eyePositions = []
        self.shipPositions = []
        self.menuItems = []
        if not self.running:
            self.ship.stage = 0
            self.ship.velocity = (-0.2,0)
            self.running = True

class ScoreScreen(Screen):

    def __init__(self):
        pass

class NotificationScreen(Screen):

    def __init__(self):
        pass

class LoadingScreen(Screen):

    def __init__(self):
        pass
