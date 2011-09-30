#
# imageCache.py
#
# Copyright (C)2011 Julian Ceipek and Patrick Varin
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

import pygame

class ImageCache:
    """
    A repository that stores images and associated masks for reuse.
    It abstracts the process of handling font rendering so that
    the game logic does not have to worry about loading fonts
    """
    def __init__(self):
        self.images = {}

    def getImageContainer(self, imagepath, id=None, colorkey=None, mask=False):

        if not (imagepath, id) in self.images:
            image = pygame.image.load(imagepath)
            if mask == True:
                mask = pygame.mask.from_surface(image)
            elif mask == False:
                mask = None

            if colorkey == 'alpha':
                image = image.convert_alpha()
            elif colorkey:
                image.set_colorkey(colorkey)
            self.images[(imagepath, id)] = ImageContainer(image, mask)

        return self.images[(imagepath, id)]

    def getImage(self, imagepath, id=None, colorkey=None, mask=False):
        """
        Used to create/get images from the image cache

        mask: setting this to True will allow the image to generate its own mask
        id: used for images that might be duplicated
        """
        container = self.getImageContainer(imagepath, id=id,
                                            colorkey=colorkey, mask=mask)
        return container.getImage()

    def getMask(self, imagepath, id=None, colorkey=None, mask=False):
        container = self.getImageContainer(imagepath, id=id,
                                            colorkey=colorkey, mask=mask)
        return container.getMask()

    def getRect(self, imagepath, id=None, colorkey=None, mask=False):
        container = self.getImageContainer(imagepath, id=id,
                                            colorkey=colorkey, mask=mask)
        return container.getRect()

    def clearImage(self, imagepath, id=None):
        """
        Removes a image object from the cache to save memory.
        Keep in mind that making new image objects requires disk access,
        which is relatively slow.

        Unless your game has many images, this needs to be called
        very infrequently.
        """
        if (imagepath, id) in self.images:
            del self.images[(imagepath, id)]

class ImageContainer:
    def __init__(self, image, mask):
        self.image = image
        self.rect = image.get_rect()
        self.mask = mask

    def getImage(self):
        return self.image

    def getMask(self):
        return self.mask

    def getRect(self):
        return self.rect

