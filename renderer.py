import pygame
from settings import Settings

class CustomRenderer:
    def __init__(self):
        self.cameras = dict()
        self.track = None

        pygame.init()
        self.screen = pygame.display.set_mode((Settings.SCREEN_WIDTH,
                                          Settings.SCREEN_HEIGHT))
        pygame.display.set_caption("POTRacer Demo")

    def setTrack(self, track):
        self.track = track

    def addCamera(self, cam):
        self.cameras[cam.uid] = cam

    def render(self, clock):
        for r in self.track.getSegmentsVisibleFromCam(None):
            pygame.draw.rect(self.screen, (255,255,255), r)

        pygame.display.set_caption("POTRacer Demo at fps: "+str(clock.get_fps()))

        pygame.display.flip()