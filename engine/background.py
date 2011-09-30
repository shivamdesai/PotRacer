#
# background.py
#
# Copyright (C)2011 Julian Ceipek and Patrick Varin
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

class Background:
    """
    A sprite group or solid color that is displayed on a screen.
    """
    def __init__(self, bg):
        self.bg = bg
        self.isAnimated = hasattr(bg,'update')


    def draw(self, surf):
        if type(self.bg) == tuple:
            surf.fill(self.bg)
        else:
            surf.fill((0,0,0))
            self.bg.draw(surf)

    def update(self, *args):
        if self.isAnimated:
            self.bg.update(*args) #FIXME
