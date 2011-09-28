import pygame

from renderer import CustomRenderer
from settings import Settings
from track import Track
from camera import Camera


if __name__ == "__main__":
    running = True

    pygame.init()
    screen = pygame.display.set_mode((Settings.SCREEN_WIDTH,
                                      Settings.SCREEN_HEIGHT))
    pygame.display.set_caption("POTRacer Demo")
    clock = pygame.time.Clock()

    track = Track()
    renderer = CustomRenderer()

    camP1 = Camera()
    #camP2 = Camera()

    renderer.addTrack(track)
    renderer.addCamera(camP1)

    timeDelta = clock.tick(Settings.MAX_FPS)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        track.addSegment()
        for r in track.getSegmentsVisibleFromCam(None):
            pygame.draw.rect(screen, (255,255,255), r)

        pygame.display.flip()
        timeDelta = clock.tick(Settings.MAX_FPS)