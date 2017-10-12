#! /usr/bin/env python

import time

import pygame
import random

from carlogic import Vehicle
from intersection import Intersection, TrafficLight
from sim_utils.config import WIDTH, HEIGHT, FRAMERATE, CAR_EVERY_FRAMES, DEBUG
from sim_utils.utils import Coord
from traffic_controller import Controller


class SimMain:
    def __init__(self):
        """Initialize"""
        """Initialize PyGame"""
        pygame.init()
        """Set the window Size"""
        self.width = WIDTH
        self.height = HEIGHT
        """Create the Screen"""
        self.screen = pygame.display.set_mode((
            self.width, self.height))
        pygame.display.set_caption('Traffic Control Simulation')

        self.intersection = Intersection(center=Coord(x=WIDTH * 0.5, y=HEIGHT * 0.5))
        # Add traffic light
        traffic_lightWE = TrafficLight(green=True, strategy='classic', id_=0)
        traffic_lightEW = TrafficLight(green=False, strategy='classic', id_=1)
        traffic_lightSN = TrafficLight(green=False, strategy='classic', id_=2)
        traffic_lightNS = TrafficLight(green=False, strategy='classic', id_=3)
        # Add a few dummy lanes
        self.intersection.add_lane(direction=Coord(1, 0), towards=False, order=0)
        self.intersection.add_lane(direction=Coord(1, 0), towards=True, order=0, light=traffic_lightWE)
        self.intersection.add_lane(direction=Coord(-1, 0), towards=True, order=0, light=traffic_lightEW)
        self.intersection.add_lane(direction=Coord(-1, 0), towards=False, order=0)
        self.intersection.add_lane(direction=Coord(0, -1), towards=False, order=0)
        self.intersection.add_lane(direction=Coord(0, -1), towards=True, order=0, light=traffic_lightSN)
        self.intersection.add_lane(direction=Coord(0, 1), towards=False, order=0)
        self.intersection.add_lane(direction=Coord(0, 1), towards=True, order=0, light=traffic_lightNS)

        self.controller = Controller(self.intersection.get_lanes())

        self.carframecounter = 0

    def MainLoop(self):
        """Create the background"""
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))

        running = True
        while running:
            """Do the Drawing"""
            self.screen.blit(self.background, (0, 0))

            # Update traffic light and car
            self.intersection.lanes[1].light.frameUpdate()
            # self.intersection.lanes[1].updateCars(self.screen)
            self.intersection.lanes[2].light.frameUpdate()
            # self.intersection.lanes[2].updateCars(self.screen)
            self.intersection.lanes[5].light.frameUpdate()
            # self.intersection.lanes[5].updateCars(self.screen)
            self.intersection.lanes[7].light.frameUpdate()
            # self.intersection.lanes[7].updateCars(self.screen)
            self.maybe_add_car()

            self.controller.update()

            self.intersection.render(self.screen)
            self.intersection.update_lanes(self.screen)

            pygame.display.flip()

            # Handle events
            running = self.handle_events()

            time.sleep(1.0 / FRAMERATE)

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Key press
                if event.key == pygame.K_ESCAPE:
                    return False
        return True

    def maybe_add_car(self):
        if self.carframecounter == 0:
            rand = random.randint(0, 3)
            if rand == 0:
                self.intersection.lanes[1].addCar(
                    Vehicle('car', 80, 140, 2, 3, 'E', debug=DEBUG)
                )
            if rand == 1:
                self.intersection.lanes[2].addCar(
                    Vehicle('car', 80, 140, 2, 3, 'W', debug=DEBUG)
                )
            if rand == 2:
                self.intersection.lanes[7].addCar(
                    Vehicle('car', 80, 140, 2, 3, 'S', debug=DEBUG)
                )
            if rand == 3:
                self.intersection.lanes[5].addCar(
                    Vehicle('car', 80, 140, 2, 3, 'N', debug=DEBUG)
                )
        self.carframecounter += 1
        if self.carframecounter == CAR_EVERY_FRAMES:
            self.carframecounter = 0


if __name__ == "__main__":
    MainWindow = SimMain()
    MainWindow.MainLoop()
