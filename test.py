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
    for t in xrange(10):
        track.addSegment()

    camP1 = Camera((0,0,Settings.SCREEN_WIDTH/2,Settings.SCREEN_HEIGHT))
    camP2 = Camera((Settings.SCREEN_WIDTH/2,0,Settings.SCREEN_WIDTH/2,Settings.SCREEN_HEIGHT))

    renderer.setTrack(track)
    renderer.addCamera(camP1)
    renderer.addCamera(camP2)

    timeDelta = clock.tick(Settings.MAX_FPS)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        renderer.render(clock)
        timeDelta = clock.tick(Settings.MAX_FPS)