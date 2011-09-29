import pygame
from pygame.locals import *
from pygame.color import *
import pymunk as phys
import math, sys, random
from os.path import join as joinPath

def to_pygame(p):
    """Small hack to convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y+600)

def flipy(y):
    """Small hack to convert chipmunk physics to pygame coordinates"""
    return -y+600

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("car in Box")
clock = pygame.time.Clock()
running = True

### Physics
space = phys.Space()
space.gravity = (0.0, -900.0)

## Cars
cars = []

### Walls
static_body = phys.Body(phys.inf, phys.inf)
static_lines = [phys.Segment(static_body, phys.Vec2d(150.0, 150.0), phys.Vec2d(450.0, 150.0), 1.0),
                phys.Segment(static_body, phys.Vec2d(450.0, 150.0), phys.Vec2d(450.0, 450.0), 1.0),
                phys.Segment(static_body, phys.Vec2d(450.0, 450.0), phys.Vec2d(150.0, 450.0), 1.0),
                phys.Segment(static_body, phys.Vec2d(150.0, 450.0), phys.Vec2d(150.0, 150.0), 1.0)]
for line in static_lines:
    line.elasticity = 0.95
space.add_static(static_lines)

## Car Image
if pygame.image.get_extended():
    img = pygame.image.load(joinPath("images","beta.png"))
else:
    img = pygame.image.load(joinPath("images","beta.bmp"))

index = 0

while running:

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False

    if index <= 0:
        index += 1
        mass = 10
        points = [(0,0), (20,0), (10,33)]
        moment = phys.moment_for_poly(mass, points)
        body = phys.Body(mass, moment)
        body.position = 300, 300
        body.angle = 42
        car = phys.Poly(body, points)
        car.elasticity = 0.95
        car.friction = 0.5
        space.add(body, car)
        cars.append(car)

    if index == 1:
        index += 1
        for car in cars:
            car.body.apply_impulse(phys.Vec2d(1000,1000))

    ### Clear screen
    screen.fill(THECOLORS["white"])

    for car in cars:
        p = car.body.position


        #pygame.draw.circle(screen, THECOLORS["blue"], p, int(car.radius), 2)
        ps = car.get_points()
        ps = [(p.x, flipy(p.y)) for p in ps]
        ps += [ps[0]]
        pygame.draw.lines(screen, THECOLORS["red"], False, ps, 1)


        # Rotate 180 degrees because of the y coordinate flip
        angle_degrees = math.degrees(car.body.angle) + 180
        rotated_logo_img = pygame.transform.rotate(img, angle_degrees)

        offset = phys.Vec2d(rotated_logo_img.get_size()) / 2.
        p = phys.Vec2d(p.x, flipy(p.y))
        p = p - offset

        screen.blit(rotated_logo_img, p)



     # Wall Physics
    for line in static_lines:
        line.elasticity = 0.95
        line.friction = 0.95
        body = line.body
        pv1 = body.position + line.a.rotated(body.angle)
        pv2 = body.position + line.b.rotated(body.angle)
        p1 = to_pygame(pv1)
        p2 = to_pygame(pv2)
        pygame.draw.lines(screen, THECOLORS["red"], False, [p1,p2])

    ### Update physics
    dt = 1.0/60.0
    for x in range(1):
        space.step(dt)

    ### Flip screen
    pygame.display.flip()
    clock.tick(50)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))
