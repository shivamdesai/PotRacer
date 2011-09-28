import pygame
from settings import Settings

class CustomRenderer:
    def __init__(self):
        self.cameras = dict()
        self.track = None

        pygame.init()
        self.display = pygame.display.set_mode((Settings.SCREEN_WIDTH,
                                          Settings.SCREEN_HEIGHT))
        pygame.display.set_caption("POTRacer Demo")

    def setTrack(self, track):
        self.track = track

    def addCamera(self, cam):
        self.cameras[cam.uid] = cam

    def itercams(self):
        return self.cameras.itervalues()

    def render(self, clock):

        for cam in self.itercams():
            cam.screen.fill((255,0,cam.uid*255))
            for r in self.track.getSegmentsVisibleFromCam(cam):
                pygame.draw.rect(cam.screen, (255,255,255), r)
            self.display.blit(cam.screen, cam)

        pygame.display.set_caption("POTRacer Demo at fps: "+str(clock.get_fps()))

        pygame.display.flip()