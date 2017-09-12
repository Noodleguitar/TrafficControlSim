#! /usr/bin/env python

import pygame
import time
from .helpers import load_image

if not pygame.font:
    print('Warning, fonts disabled')
if not pygame.mixer:
    print('Warning, sound disabled')

WIDTH = 640
HEIGHT = 480
FRAMERATE = 60
CAR_EVERY_FRAMES = 60


class SimMain:
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

        self.carframecounter = 0

    def MainLoop(self):
        self.cars_sprites = pygame.sprite.Group()

        """Create the background"""
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))

        while 1:

            # speed = vehicle.frameUpdate()
            self.car.move()
            self.maybe_add_car()
            for car in self.cars_sprites:
                car.move()


            """Do the Drawing"""
            self.screen.blit(self.background, (0, 0))

            self.cars_sprites.draw(self.screen)
            pygame.display.flip()
            time.sleep(1.0 / FRAMERATE)

    def maybe_add_car(self):
        if self.carframecounter == 0:
            self.cars_sprites.add(Car(pygame.Rect(0, HEIGHT / 2, 64, 64)))
        self.carframecounter += 1
        if self.carframecounter == CAR_EVERY_FRAMES:
            self.carframecounter = 0


class Car(pygame.sprite.Sprite):
    """This is our car that will move around the screen"""

    def __init__(self, rect=None):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('car_small.png', -1)
        if rect is not None:
            self.rect = rect
        """Set the number of Pixels to move each time"""
        self.x_dist = 5
        self.y_dist = 5

    def move(self):
        xMove = 0
        yMove = 0

        xMove = self.x_dist

        loc = self.rect.topleft
        if loc[0] > WIDTH:
            self.kill()
        else:
            self.rect.move_ip(xMove, yMove)


if __name__ == "__main__":
    MainWindow = SimMain()
    MainWindow.MainLoop()
