import pygame
from settings import Settings

class CustomRenderer:
    def __init__(self):
        self.cameras = dict()
        self.track = None
        self.Racers = dict()

        pygame.init()
        self.display = pygame.display.set_mode((Settings.SCREEN_WIDTH,
                                          Settings.SCREEN_HEIGHT))
        pygame.display.set_caption("POTRacer Demo")

    def addRacer(self, racer):
        self.Racers[id(racer)] = racer

    def setTrack(self, track):
        self.track = track

    def addCamera(self, cam):
        self.cameras[cam.uid] = cam

    def itercams(self):
        return self.cameras.itervalues()

    def render(self, clock):
        def conv(vec, anchor):
            return (int(vec[0]+anchor.x), int(-vec[1]+Settings.SCREEN_HEIGHT+anchor.y))
        for cam in self.itercams():
            cam.screen.fill((0,0,0))
            for r in self.track.iterSegmentsVisibleFromCam(cam):
                pygame.draw.rect(cam.screen, (255,255,255), r)
            #for r in self.track.getPhysSegments():
            #    for s in r:
            #        pygame.draw.line(cam.screen, (255,255,255), conv(s.a, cam.anchorPt), conv(s.b, cam.anchorPt))
            for r in self.track.iterPointsVisibleFromCam(cam):
                for p in r:
                    pygame.draw.circle(cam.screen, (0,255,0), (int(p[0]),int(p[1])), 3)

            for racer in self.Racers.itervalues():
                p = [conv(r, cam.anchorPt) for r in racer.get_points()]
                pygame.draw.lines(cam.screen, (0,0,255) , False, p, 1)
           
            self.display.blit(cam.screen, cam.displayRect)
            pygame.draw.rect(self.display, (0,0,50), cam.displayRect, 1)


        pygame.display.set_caption("POTRacer Demo at fps: "+str(clock.get_fps()))

        pygame.display.flip()
