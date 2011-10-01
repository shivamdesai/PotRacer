from settings import Settings
from engine.window import Window
from engine.manager import Manager
from engine.ui import UI

from screens.mainMenu import MenuScreen

window = Window(windowTitle="POTRacer")

manager = Manager()
window.registerManager(manager)

from dualPBInputDevice import DualPBDevice
PICInput = DualPBDevice(0x6666, 0x0003)
window.addInputDevice(PICInput)

userInterface = UI(manager)
#screens must be initialized after the manager and the ui
mainScreen = MenuScreen((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT),
                        userInterface)
userInterface.addActiveScreens(mainScreen)

window.run()
window.cleanup()
