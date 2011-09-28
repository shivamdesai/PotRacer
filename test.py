import pygame

from settings import Settings
from track import Track



if __name__ == "__main__":
    running = True

    pygame.init()
    screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
    pygame.display.set_caption("POTRacer Demo")
    clock = pygame.time.Clock()

    track = Track()

    while running:
        print "Top"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        track.addSegment()
        for r in track.getSegmentsVisibleFromCam(None):
            #print "Draw"
            pygame.draw.rect(screen, (255,255,255), r)

        pygame.display.flip()
        clock.tick(1)