from pygame import Rect

class Camera(Rect):
    """
    Cameras have a unique id, gameworld
    position, and viewport size.
    """
    nextUID = 0

    def __init__(self):
        self.uid = Camera.nextUID
        Camera._incrementUID()

    @classmethod
    def _incrementUID(cls):
        Camera.nextUID += 1
