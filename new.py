from settings import Settings
from engine.window import Window
from engine.manager import Manager
from engine.ui import UI

from screens import MenuScreen

window = Window(windowTitle="POTRacer")

manager = Manager()
window.registerManager(manager)

userInterface = UI(manager)
#screens must be initialized after the manager and the ui
mainScreen = MenuScreen((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT),
                        userInterface)
userInterface.addActiveScreens(mainScreen)

window.run()
window.cleanup()

"""
if __name__ == "__main__":
    running = True

    renderer = CustomRenderer()

    clock = pygame.time.Clock()

    track = Track()
    for t in xrange(50):
        track.addSegment()

    camP1 = Camera( (0,0),
    (0,0,Settings.SCREEN_WIDTH/2,Settings.SCREEN_HEIGHT))
    camP2 = Camera( (0,0),
    (Settings.SCREEN_WIDTH/2,0,Settings.SCREEN_WIDTH/2,Settings.SCREEN_HEIGHT))

    camP2.anchorPt.x -= 200

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

        camP2.anchorPt.y -= timeDelta*0.5
        camP1.anchorPt.x -= timeDelta*0.05

        renderer.render(clock)
        timeDelta = clock.tick(Settings.MAX_FPS)
"""