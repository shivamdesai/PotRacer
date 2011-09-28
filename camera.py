from pygame import Rect, Surface

class Camera(Rect):
    """
    Cameras have a unique id, gameworld
    position, and viewport size.
    """
    nextUID = 0

    def __init__(self, *rect):
        Rect.__init__(self, *rect)
        self.uid = Camera._incrementUID()
        self.screen = Surface((self.width, self.height))

    @classmethod
    def _incrementUID(cls):
        curr = Camera.nextUID
        Camera.nextUID += 1
        return curr
