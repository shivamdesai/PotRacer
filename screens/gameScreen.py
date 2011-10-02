import pymunk as phys

from engine.screen import Screen
from engine.background import Background
from settings import Settings

from renderer import CustomRenderer
from gameObjects.track import Track
from gameObjects.camera import Camera
from gameObjects.racer import Racer

class GameScreen(Screen):

    def __init__(self, size, ui):
        Screen.__init__(self, None, size, ui)
        self.setup()

    def setup(self):
        self.physSpace = self.generatePhysSpace()
        self.track = self.generateNewTrack()
        self.racers = self.generateRacers(2)
        self.cameras = self.generateCameras(2)
        self.renderer = CustomRenderer(imageCache = Screen.imageCache)
        self.renderer.setTrack(self.track)
        self.renderer.addRacers(self.racers)
        self.renderer.addCameras(self.cameras)

    def generatePhysSpace(self):
        space = phys.Space()
        space.gravity = (0.0, 0.0)
        return space

    def generateNewTrack(self):
        track = Track()
        for t in xrange(50):
            track.addSegment(space=self.physSpace)
        return track
    
    def generateRacers(self, count):
        racers = []
        for r in xrange(count):
            start = Settings.SCREEN_WIDTH/2 - Settings.MIN_TRACK_WIDTH
            offset = (Settings.MIN_TRACK_WIDTH*2)/(count+1)
            position = ((1+r)*offset+start, 30)
            racer = Racer(position, space=self.physSpace)
            racers.append(racer)
        return racers
    
    def generateCameras(self, count):
        cameras = []
        if count == 1:
            camP1 = Camera((0,0),
                      (0,0,Settings.SCREEN_WIDTH,Settings.SCREEN_HEIGHT))
            cameras.append(camP1)
        elif count == 2:
            camP1 = Camera((0,0),
                      (0,0,
                      Settings.SCREEN_WIDTH/2,Settings.SCREEN_HEIGHT))
            camP2 = Camera((0,0),
                      (Settings.SCREEN_WIDTH/2,0,
                      Settings.SCREEN_WIDTH/2,Settings.SCREEN_HEIGHT))
            cameras.append(camP1)
            cameras.append(camP2)
        return cameras

    def initializeCallbackDict(self):
        self.callbackDict = {}
        #self.callbackDict['look'] = ('deviceString', self.steer)
        self.callbackDict['exit'] = ('deviceString', self.exit)
        self.callbackDict['p1boost'] = ('deviceString', self.boost)
        self.callbackDict['p2boost'] = ('deviceString', self.boost2)
        self.callbackDict['p1control'] = ('deviceString', self.steer)
        self.callbackDict['p2control'] = ('deviceString', self.steer2)


    def steerLeft(self):
        self.racers[0].steerLeft()
        
    def steerRight(self):
        self.racers[0].steerRight()

    def steer(self, event):
        loc = event.values[0] - 127.5
        self.racers[0].steer(loc)

    def steer2(self, event):
        loc = event.values[0] - 127.5
        self.racers[1].steer(loc)
    
    def boost(self):
        self.racers[0].boost()

    def boost2(self):
        self.racers[1].boost()

    def exit(self):
        self._ui.clearTopScreen()
        #pygame.mixer.music.stop()

    def draw(self, surf):
        #Bypasses traditional draw method with renderer
        self.renderer.render()

    def update(self, *args):
        gameTime, frameTime = args[:2]
        for cam, racer in zip(self.cameras,self.racers):
            cam.centerOnPt(racer.getPos())
        dt = 1.0/(Settings.MAX_FPS*20)
        for x in range(10):
            self.physSpace.step(dt)

