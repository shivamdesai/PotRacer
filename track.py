import random

from settings import Settings

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
        self.cameras[cam.uid] = cam

    def detachCamera(self, cam):
        del self.cameras[cam.uid]

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