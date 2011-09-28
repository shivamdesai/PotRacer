import pygame
import random

class Settings:
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600

    MIN_TRACK_WIDTH = 80

class Camera:
    """
    Cameras have a unique id, gameworld
    position, and viewport size.
    """
    nextID = 0

    def __init__(self):
        self.id = Camera.nextID
        Camera._incrementID()

    @classmethod
    def _incrementID(cls):
        Camera.nextID += 1

class Track:
    """
    The track along which racers move. It consists
    of TrackSegments and includes methods to optimize
    rendering by associating each camera with one of the
    segments it saw during the last update.
    """
    def __init__(self):
        self.cameras = dict()
        self.trackStart = None
        self.trackEnd = None

    def attachCamera(self, cam):
        self.cameras[cam.id] = cam

    def detachCamera(self, cam):
        del self.cameras[cam.id]

    def addSegment(self):
        if self.trackStart == None:
            print "AddFirst"
            left = (Settings.SCREEN_WIDTH/2 - Settings.MIN_TRACK_WIDTH, 0)
            right = (Settings.SCREEN_WIDTH/2 + Settings.MIN_TRACK_WIDTH, 0)
            newSeg = TrackSegment(left, right, prev=None, next=None)
            self.trackStart = newSeg
            self.trackEnd = newSeg
            print right[0] - left[0]
        else:
            print "AddNew"
            vert = random.randint(Settings.MIN_TRACK_WIDTH,
                                Settings.MIN_TRACK_WIDTH) + self.trackEnd.left[1]
            horizShift = random.randint(-Settings.MIN_TRACK_WIDTH/2,
                                         Settings.MIN_TRACK_WIDTH/2)
            horizL = self.trackEnd.left[0] + horizShift
            horizR = random.randint(horizL + Settings.MIN_TRACK_WIDTH,
                                    horizL + Settings.MIN_TRACK_WIDTH * 2)
            left = horizL, vert
            right = horizR, vert
            newSeg = TrackSegment(left, right, prev=self.trackEnd, next=None)
            self.trackEnd.next = newSeg
            self.trackEnd = newSeg
            print right[0] - left[0]

    def getSegmentsVisibleFromCam(self, cam):
        #FIXME
        ptr = self.trackStart #should actually use cam pos as ref
        while ptr:
            if ptr.prev:
                #print (ptr.prev.left[0],ptr.prev.left[1], ptr.right[0],ptr.right[1])
                #print ptr.prev.right[0] - ptr.prev.left[0]
                yield (ptr.prev.left[0],ptr.prev.left[1], ptr.prev.right[0]-ptr.prev.left[0],ptr.right[1]-ptr.prev.left[1])
            ptr = ptr.next


class TrackSegment:
    """
    A TrackSegment is a node in a bi-directional
    linked list that knows the coordinates of its left and right points.
    """
    def __init__(self, l, r, prev=None, next=None):
        self.prev = prev
        self.next = next
        self.left = l
        self.right = r

class CustomRenderer:
    def __init__(self, screen):
        pass

    def render(self):
        pass

if __name__ == "__main__":
    running = True

    pygame.init()
    screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
    pygame.display.set_caption("POTRacer Demo")
    clock = pygame.time.Clock()

    track = Track()

    while running:
        print "Top"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        track.addSegment()
        for r in track.getSegmentsVisibleFromCam(None):
            #print "Draw"
            pygame.draw.rect(screen, (255,255,255), r)

        pygame.display.flip()
        clock.tick(1)