from settings import Settings
from pygame import Rect, Surface
from pymunk import Vec2d

class Camera():
    """
    Cameras have a unique id, gameworld
    position, and viewport size.
    """
    nextUID = 0

    def __init__(self, anchorPt, dispRect):
        self.anchorPt = Vec2d(anchorPt)
        self.uid = Camera._incrementUID()
        self.displayRect = Rect(dispRect)
        self.screen = Surface((self.displayRect.width,
                               self.displayRect.height))

    def centerOnPhysPt(self, vec):
        self.anchorPt.x = (-vec[0] + self.displayRect.width/2)
        self.anchorPt.y = vec[1] - Settings.SCREEN_HEIGHT + self.displayRect.height/2

    @classmethod
    def _incrementUID(cls):
        curr = Camera.nextUID
        Camera.nextUID += 1
        return curr
