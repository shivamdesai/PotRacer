from pygame import Rect, Surface

class Camera(Rect):
    """
    Cameras have a unique id, gameworld
    position, and viewport size.
    """
    nextUID = 0

    def __init__(self, anchorRect, dispRect):
        Rect.__init__(self, anchorRect)
        self.uid = Camera._incrementUID()
        self.screen = Surface((self.width, self.height))
        self.displayRect = Rect(dispRect)

    @classmethod
    def _incrementUID(cls):
        curr = Camera.nextUID
        Camera.nextUID += 1
        return curr
