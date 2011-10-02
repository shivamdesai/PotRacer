import pygame
import math
import pymunk as phys

from settings import Settings
from engine.functions import pathJoin

class CustomRenderer:
    
    def __init__(self, imageCache=None):
        self.cameras = dict()
        self.track = None
        self.racers = dict()
        CustomRenderer.imageCache = imageCache
        pygame.init()
        self.display = pygame.display.set_mode((Settings.SCREEN_WIDTH,
                                          Settings.SCREEN_HEIGHT))
        pygame.display.set_caption("POTRacer Demo")

    def addRacer(self, racer):
        self.racers[id(racer)] = racer

    def addRacers(self, racers):
        if type(racers) == dict:
            for racer in racers.itervalues():
                self.racers[id(racer)] = racer
        elif type(racers) == list or type(racers) == tuple:
            for racer in racers:
                racerPath0 = pathJoin(('images','beta.png'))
                racerPath1 = pathJoin(('images','alpha.png'))
                if not racerPath0 in self.racers:
                    self.racers[racerPath0] = racer
                else:
                    self.racers[racerPath1] = racer

    def addCameras(self, cameras):
        if type(cameras) == dict:
            for camera in cameras.itervalues():
                self.cameras[id(camera)] = camera
        elif type(cameras) == list or type(cameras) == tuple:
            for camera in cameras:
                self.cameras[id(camera)] = camera

    def setTrack(self, track):
        self.track = track

    def addCamera(self, cam):
        self.cameras[cam.uid] = cam

    def itercams(self):
        return self.cameras.itervalues()
        
    def iterracers(self):
        return self.racers.itervalues()
        
    def render(self, clock=None):
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

            for racerImagePath,racer in self.racers.iteritems():
                #p = [conv(r, cam.anchorPt) for r in racer.getPhysPoints()]
                #pygame.draw.lines(cam.screen, (0,0,255) , False, p, 1)
                racerImage = self.imageCache.getImage(racerImagePath, colorkey='alpha', mask=False)
                degrees = math.degrees(racer.body.angle)
                rotatedImage = pygame.transform.rotate(racerImage, degrees)
                offset = phys.Vec2d(rotatedImage.get_size()) / 2.
                cam.screen.blit(rotatedImage, rotatedImage.get_rect().move(racer.getPos()+cam.anchorPt-offset))

            self.display.blit(cam.screen, cam.displayRect)
            pygame.draw.rect(self.display, (0,0,50), cam.displayRect, 1)

        if clock:
            pygame.display.set_caption("POTRacer Demo at fps: "+str(clock.get_fps()))

        pygame.display.flip()
