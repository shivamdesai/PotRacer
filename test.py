import pygame

from renderer import CustomRenderer
from settings import Settings
from track import Track
from camera import Camera


if __name__ == "__main__":
    running = True

    renderer = CustomRenderer()

    clock = pygame.time.Clock()

    track = Track()
    for t in xrange(1000):
        track.addSegment()

    camP1 = Camera((20,20,300,300))
    #camP2 = Camera()

    renderer.setTrack(track)
    renderer.addCamera(camP1)

    timeDelta = clock.tick(Settings.MAX_FPS)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        renderer.render(clock)
        timeDelta = clock.tick(Settings.MAX_FPS)