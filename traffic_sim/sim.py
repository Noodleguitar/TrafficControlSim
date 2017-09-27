#! /usr/bin/env python

import pygame
import time

from intersection import Intersection, TrafficLight
from carlogic import Vehicle
from helpers import load_image
from sim_utils.utils import Coord

if not pygame.font:
    print('Warning, fonts disabled')
if not pygame.mixer:
    print('Warning, sound disabled')

WIDTH = 1200
HEIGHT = 800
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
        pygame.display.set_caption('Traffic Control Simulation')

        self.intersection = Intersection(center=Coord(x=WIDTH*0.5, y=HEIGHT*0.5))
        # Add traffic light
        traffic_light = TrafficLight(green=True, strategy='classic', id_=0)
        traffic_light2 = TrafficLight(green=False, strategy='classic', id_=1)
        # Add a few dummy lanes
        self.intersection.add_lane(direction=Coord(1, 0), towards=False, order=0)
        self.intersection.add_lane(direction=Coord(1, 0), towards=True, order=0, light=traffic_light)
        self.intersection.add_lane(direction=Coord(-1, 0), towards=True, order=0)
        self.intersection.add_lane(direction=Coord(-1, 0), towards=False, order=0)
        self.intersection.add_lane(direction=Coord(0, -1), towards=False, order=0)
        self.intersection.add_lane(direction=Coord(0, -1), towards=True, order=0, light=traffic_light2)
        self.intersection.add_lane(direction=Coord(0, 1), towards=False, order=0)
        self.intersection.add_lane(direction=Coord(0, 1), towards=True, order=0)

        # Add car (and link it to the 2nd lane which has a traffic light attached)
        self.vehicle = Vehicle(300, 150, 'car', 80, 3, self.intersection.lanes[1], 140, 2, 3, id_=0)

        self.carframecounter = 0

    def MainLoop(self):
        self.cars_sprites = pygame.sprite.Group()

        """Create the background"""
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))

        running = True
        while running:
            # Update traffic light and car
            self.intersection.lanes[1].light.frameUpdate()
            self.intersection.lanes[5].light.frameUpdate()
            self.vehicle.frameUpdate()
            # self.car.move()
            self.maybe_add_car()
            for car in self.cars_sprites:
                car.move(self.vehicle.speed)

            """Do the Drawing"""
            self.screen.blit(self.background, (0, 0))
            self.intersection.render(self.screen)

            self.cars_sprites.draw(self.screen)
            pygame.display.flip()

            # Handle events
            running = self.handle_events_()

            # Clamp to maximum frame rate
            time.sleep(1.0 / FRAMERATE)

    def handle_events_(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Key press
                if event.key == pygame.K_ESCAPE:
                    return False
        # print(events)
        return True

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

    def move(self, speed):
        yMove = 0
        xMove = speed * 0.05

        loc = self.rect.topleft
        if loc[0] > WIDTH:
            self.kill()
        else:
            self.rect.move_ip(xMove, yMove)


if __name__ == "__main__":
    MainWindow = SimMain()
    MainWindow.MainLoop()
