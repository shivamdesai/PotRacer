from engine.functions import pathJoin

class MenuItem:

    def __init__(self, text, pos, scaleSize=None):
        self.text = text
        self.fontname = pathJoin(('fonts','orbitron',
            'orbitron-black.ttf'))
        self.size = int(self.resolution[1]*(1/15.0))
        if scaleSize != None:
            self.size *= scaleSize
            self.size = int(self.size)
        self.color = (255,255,255)
        self.antialias = True
        self.textSurface = self.textCache.getText(text, self.fontname,
            self.size, self.color, antialias=self.antialias)
        self.rect = self.textSurface.get_rect()
        self.rect.center = int(pos[0]), int(pos[1])

    def draw(self, surf):
        surf.blit(self.textSurface, self.rect)
