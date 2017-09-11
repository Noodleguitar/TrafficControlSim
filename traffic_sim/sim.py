#! /usr/bin/env python

import pygame
import time
from helpers import load_image

if not pygame.font:
    print 'Warning, fonts disabled'
if not pygame.mixer:
    print 'Warning, sound disabled'

WIDTH = 640
HEIGHT = 480
FRAMERATE = 60


class PyManMain:
    """The Main PyMan Class - This class handles the main
    initialization and creating of the Game."""

    def __init__(self, width=WIDTH, height=HEIGHT):
        """Initialize"""
        """Initialize PyGame"""
        pygame.init()
        """Set the window Size"""
        self.width = width
        self.height = height
        """Create the Screen"""
        self.screen = pygame.display.set_mode((
            self.width, self.height))

    def MainLoop(self):
        """This is the Main Loop of the Game"""

        """Load All of our Sprites"""
        self.LoadSprites()
        """tell pygame to keep sending up keystrokes when they are
        held down"""
        pygame.key.set_repeat(500, 30)

        """Create the background"""
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))

        while 1:
            self.car.move()

            """Do the Drawging"""
            self.screen.blit(self.background, (0, 0))

            self.car_sprites.draw(self.screen)
            pygame.display.flip()
            time.sleep(1.0 / FRAMERATE)

    def LoadSprites(self):
        """Load the sprites that we need"""
        self.car = Car()
        self.car_sprites = pygame.sprite.RenderPlain((self.car))


class Car(pygame.sprite.Sprite):
    """This is our car that will move around the screen"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('car.png', -1)
        """Set the number of Pixels to move each time"""
        self.x_dist = 5
        self.y_dist = 5

    def move(self):
        """Move your self in one of the 4 directions according to key"""
        """Key is the pyGame define for either up,down,left, or right key
        we will adjust outselfs in that direction"""
        xMove = 0
        yMove = 0

        xMove = self.x_dist
        self.rect.move_ip(xMove, yMove)


if __name__ == "__main__":
    MainWindow = PyManMain()
    MainWindow.MainLoop()
