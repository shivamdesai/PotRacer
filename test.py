import pygame
import pymunk as phys
from renderer import CustomRenderer
from settings import Settings
from track import Track
from camera import Camera


if __name__ == "__main__":
    running = True

    renderer = CustomRenderer()

    clock = pygame.time.Clock()

    space = phys.Space()
    space.gravity = (0.0, -900.0)

    ball = phys.Body(10, 100)
    ball.position = phys.Vec2d(Settings.SCREEN_WIDTH/2, Settings.SCREEN_HEIGHT-30)
    shape = phys.Circle(ball, 10, (0,0))
    shape.friction = 0.5
    shape.collision_type = 2
    space.add(ball, shape)


    track = Track()
    for t in xrange(100):
        track.addSegment(space=space)

    camP1 = Camera( (0,0), (0,                      0,Settings.SCREEN_WIDTH/2,Settings.SCREEN_HEIGHT/2))
    #camP1 = Camera( (0,0), (0,                      0,Settings.SCREEN_WIDTH,Settings.SCREEN_HEIGHT))
    camP2 = Camera( (0,0), (Settings.SCREEN_WIDTH/2,0,Settings.SCREEN_WIDTH/2,Settings.SCREEN_HEIGHT))

    camP3 = Camera( (0,0), (0,                      Settings.SCREEN_HEIGHT/2,Settings.SCREEN_WIDTH/2,Settings.SCREEN_HEIGHT/2))

    camP1.anchorPt.x -= 300

    renderer.setTrack(track)
    renderer.addCamera(camP1)
    renderer.addCamera(camP2)
    renderer.addCamera(camP3)
    renderer.addTestBall(ball)

    timeDelta = clock.tick(Settings.MAX_FPS)

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        #camP2.anchorPt.y -= timeDelta*0.5

        #camP1.anchorPt.y -= timeDelta * 0.15



        dt = 1.0/600.0
        for x in range(10):
            space.step(dt)

        camP1.centerOnPhysPt(ball.position)
        camP2.centerOnPhysPt(ball.position)
        camP3.centerOnPhysPt(ball.position)

        renderer.render(clock)
        timeDelta = clock.tick(Settings.MAX_FPS)
