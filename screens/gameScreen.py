from engine.screen import Screen
from engine.background import Background
from settings import Settings

from renderer import CustomRenderer
from gameObjects.track import Track
from gameObjects.camera import Camera

class GameScreen(Screen):

    def __init__(self, size, ui):
        Screen.__init__(self, None, size, ui)
        self.setup()

    def setup(self):
        self.renderer = CustomRenderer()
        self.track = self.generateNewTrack()
        self.renderer.setTrack(self.track)
        self.cameras = {}
        self.setPlayerCount(2)
        for cam in self.cameras.itervalues():
            self.renderer.addCamera(cam)

    def generateNewTrack(self):
        track = Track()
        for t in xrange(50):
            track.addSegment()
        return track

    def setPlayerCount(self, count):
        if count == 1:
            camP1 = Camera((0,0),
                      (0,0,Settings.SCREEN_WIDTH,Settings.SCREEN_HEIGHT))
            self.cameras[id(camP1)] = camP1
        elif count == 2:
            camP1 = Camera((0,0),
                      (0,0,
                      Settings.SCREEN_WIDTH/2,Settings.SCREEN_HEIGHT))
            camP2 = Camera((0,0),
                      (Settings.SCREEN_WIDTH/2,0,
                      Settings.SCREEN_WIDTH,Settings.SCREEN_HEIGHT))
            self.cameras[id(camP1)] = camP1
            self.cameras[id(camP2)] = camP2

    def initializeCallbackDict(self):
        self.callbackDict = {}
        #self.callbackDict['look'] = ('deviceString', self.steer)
        self.callbackDict['exit'] = ('deviceString', self.exit)

    def steer(self, event):
        #move the appropriate racer in this method
        """
        if hasattr(self._ui, 'getShipPosition'):
            for ship in self.ships:
                ship.targetPosition = (self._ui.getShipPosition(event.values[0]), ship.targetPosition[1])
        else:
            for ship in self.ships:
                ship.targetPosition = (event.values[0], ship.targetPosition[1])"""
        pass

    def exit(self):
        self._ui.clearTopScreen()
        #pygame.mixer.music.stop()

    def draw(self, surf):
        #Bypasses traditional draw method with renderer
        self.renderer.render()

    def update(self, *args):
        gameTime, frameTime = args[:2]
        #Screen.update(self, *args)
        #self.ships.update(*args)
        #self.boulders.update(*args)
        #self.boulderFragments.update(*args)
