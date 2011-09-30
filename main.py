import pygame
import pymunk as phys
import math, sys, random

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Joints. Just wait and the L will tip over")
clock = pygame.time.Clock()
running = True

MAX_FPS = 60
MAX_FRAME_TIME = 0.25

dt = 0.01  # Logic delta time

t = 0.0    # Current simulation time
accumulator = 0.0 # Keeps track of "unsimulated" time after a frame
currentTime = clock.tick(MAX_FPS)


while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False

    frameTime = clock.tick(MAX_FPS)

    if ( frameTime > MAX_FRAME_TIME )
        frameTime = MAX_FRAME_TIME   # avoid spiral of death

    accumulator += frameTime;

    while ( accumulator >= dt )
        #SIMULATE:
        #previousState = currentState;
        #integrate( currentState, t, dt );
        t += dt
        accumulator -= dt

    alpha = accumulator / dt # Interpolation constant

    #INTERPOLATE:
    #State state = currentState*alpha + previousState * ( 1.0 - alpha );

    #RENDER:
    #render( state );


    ### Update physics
    dt = 1.0/50.0/10.0
    for x in range(10):
        space.step(dt)

    ### Flip screen
    pygame.display.flip()
    clock.tick(50)

if __name__ == '__main__':
    sys.exit(main())
