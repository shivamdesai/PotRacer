import pymunk as phys
from settings import Settings
class Racer:
    """
    The racer that moves along the track. It
    consists of a body and shape.
    """
    
    def __init__(self, position, mass=10, points=None, space=None):
        if points == None:
            self.points = [(-10,15), (0,-18), (10,15), (-10,15)]
        else:
            self.points = points
        self.mass = mass
        moment = phys.moment_for_poly(self.mass, self.points)
        self.body = phys.Body(self.mass, moment)
        self.body.position = phys.Vec2d(position[0], 
                                        -position[1]+Settings.SCREEN_HEIGHT)
        self.shape = phys.Poly(self.body, self.points)
        self.shape.elasticity = 0.95
        self.shape.friction = 5
        if space:
            self.setPhysicsSpace(space) 
        
    def setPhysicsSpace(self, space):
        space.add(self.body, self.shape)
        
    def getPos(self):
        return (self.body.position[0], 
                -self.body.position[1]+Settings.SCREEN_HEIGHT)
    
    def getPhysPoints(self):
        return self.shape.get_points()
        
    def steer(self, value):
        curr = self.body.rotation_vector.angle
        print curr
        des = value
        self.body.angular_velocity = 0.25*(des-curr)
        #self.body.torque = value
        
    def boost(self):
        print self.body.rotation_vector.perpendicular()
        self.body.apply_impulse(-self.body.rotation_vector.perpendicular()*10000)
