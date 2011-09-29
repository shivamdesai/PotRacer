import pygame
from settings import Settings

class CustomRenderer:
    def __init__(self):
        self.cameras = dict()
        self.track = None
        self.testBalls = dict()

        pygame.init()
        self.display = pygame.display.set_mode((Settings.SCREEN_WIDTH,
                                          Settings.SCREEN_HEIGHT))
        pygame.display.set_caption("POTRacer Demo")

    def addTestBall(self, ball):
        self.testBalls[id(ball)] = ball
        
        
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
            cam.screen.fill((255,0,cam.uid*255))
            for r in self.track.getSegmentsVisibleFromCam(cam):
                pygame.draw.rect(cam.screen, (0,255,0), r,1)
            for r in self.track.getPhysSegmentsVisibleFromCam(cam):
                for s in r:
                    pygame.draw.line(cam.screen, (255,255,255), conv(s.a, cam.anchorPt), conv(s.b, cam.anchorPt))
            for r in self.track.getPointsVisibleFromCam(cam):
                for p in r:
                    pygame.draw.circle(cam.screen, (0,255,0), (int(p[0]),int(p[1])), 3)    
            
            for ball in self.testBalls.itervalues():
                pygame.draw.circle(cam.screen, (0,255,0), conv(ball.position, cam.anchorPt), 10, 2)
        
            self.display.blit(cam.screen, cam.displayRect)
            

        pygame.display.set_caption("POTRacer Demo at fps: "+str(clock.get_fps()))

        pygame.display.flip()
