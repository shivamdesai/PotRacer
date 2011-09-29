import pymunk as phys

class Racer:
	"""
	The racer that moves along the track. It
	consists of a body and shape.
	"""
	
	def __init__(self, mass=10, points=[(0,0), (20,0), (10,33)], position=(300,300))
	    self.mass = mass
	    self.points = points
	    moment = phys.moment_for_poly(mass, points)
        self.rbody = phys.Body(mass, moment)
        self.rbody.position = position
        self.rbody.angle = 42
        self.rshape = phys.Poly(body, points)
        self.rshape.elasticity = 0.95
        self.rshape.friction = 0.5
