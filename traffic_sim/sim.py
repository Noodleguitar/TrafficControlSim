#! /usr/bin/env python

import pygame
import random
import datetime as dt
import time
from datalogging import DataLogging

from carlogic import Vehicle
from intersection import Intersection, TrafficLight
from sim_utils.config import WIDTH, HEIGHT, FRAMERATE, CAR_EVERY_FRAMES, DEBUG
from sim_utils.utils import Coord
from traffic_controller import Controller


class SimMain:
    def __init__(self):
        """Initialize"""
        self.dataStorage = DataLogging()
        """Initialize PyGame"""
        pygame.init()
        """Set the window Size"""
        self.width = WIDTH
        self.height = HEIGHT
        """Create the Screen"""
        self.screen = pygame.display.set_mode((
            self.width, self.height))
        pygame.display.set_caption('Traffic Control Simulation')
        # Initialize font
        self.font = pygame.font.SysFont('monospace', 14)

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

        self.frame_timing = pygame.time.Clock()
        self.carframecounter = 0

    def MainLoop(self):
        """Create the background"""
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))

        running = True
        while running:
            frame_start = dt.datetime.now()

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

            # Handle events
            running = self.handle_events()

            self.display_fps()

            pygame.display.flip()

            frame_time = (dt.datetime.now() - frame_start).total_seconds()
            # pygame.time.delay(int(max(0, (1.0 / FRAMERATE) - frame_time) * 1000))
            time.sleep(max(0, (1.0 / FRAMERATE) - frame_time))
            self.frame_timing.tick()

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Key press
                if event.key == pygame.K_ESCAPE:
                    return False
        return True

    def display_fps(self):
        fps = round(self.frame_timing.get_fps())
        fps_text = self.font.render('FPS: ' + str(fps), 0, (255, 255, 255))
        self.screen.blit(fps_text, (0, 0))

    def maybe_add_car(self):
        # TODO: check destination lanes
        routes = [
            (1, 0, 'E', 'E'),
            (1, 4, 'E', 'N'),
            (1, 6, 'E', 'S'),
            (2, 3, 'W', 'W'),
            (2, 4, 'W', 'N'),
            (2, 6, 'W', 'S'),
            (5, 0, 'N', 'N'),
            (5, 3, 'N', 'W'),
            (5, 6, 'N', 'E'),
            (7, 0, 'S', 'S'),
            (7, 3, 'S', 'W'),
            (7, 4, 'S', 'E'),
        ]
        if self.carframecounter == 0:
            route = routes[random.randint(0, len(routes) - 1)]
            next_lane = (self.intersection.lanes[route[1]], route[3])
            self.intersection.lanes[route[0]].addCar(
                Vehicle(
                    'car', 80, 140, 2, 3, route[2], self.dataStorage,
                    next_lane, debug=DEBUG)
            )

        self.carframecounter += 1
        if self.carframecounter == CAR_EVERY_FRAMES:
            self.carframecounter = 0


if __name__ == "__main__":
    MainWindow = SimMain()
    MainWindow.MainLoop()
