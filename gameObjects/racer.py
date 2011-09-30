import pymunk as phys
from settings import Settings
class Racer:
    """
    The racer that moves along the track. It
    consists of a body and shape.
    """
    
    def __init__(self, position, mass=10, points=None):
        if points == None:
            self.points = [(-10,15), (0,-18), (10,15), (-10,15)]
        else:
            self.points = points
        self.mass = mass
        moment = phys.moment_for_poly(self.mass, self.points)
        self.body = phys.Body(self.mass, moment)
        self.body.position = position
        self.shape = phys.Poly(self.body, self.points)
        self.shape.elasticity = 0.95
        self.shape.friction = 0.5
    
    def setPhysicsSpace(self, space):
        space.add(self.body, self.shape)
        
    def getPos(self):
        return (self.body.position[0], 
                -self.body.position[1]+Settings.SCREEN_HEIGHT)
