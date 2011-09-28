class CustomRenderer:
    def __init__(self, screen):
        self.cameras = dict()

    def addTrack(self, track):
        pass

    def addCamera(self, cam):
        self.cameras[cam.uid] = cam

    def render(self):
        pass