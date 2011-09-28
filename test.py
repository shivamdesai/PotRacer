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

    camP1 = Camera()
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

        track.addSegment()

        renderer.render()
        timeDelta = clock.tick(Settings.MAX_FPS)