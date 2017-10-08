import pygame

from sim_utils.config import WIDTH, HEIGHT, LANE_LIGHT_LOCATION, LANE_LENGTH, FACTOR_SPEED
from sim_utils.utils import load_image, get_screen_center, get_lane_points


class Vehicle(pygame.sprite.Sprite):

    def __init__(self, length: int, width: int, name: str, speed: int, maxSpeed: int,
                 acceleration: int, turnPoint: int, start, direction, finish):
        pygame.sprite.Sprite.__init__(self)
        if direction == 'E':
            self.image, self.rect = load_image('car_small_right.png', -1)
        if direction == 'W':
            self.image, self.rect = load_image('car_small_left.png', -1)
        if direction == 'N':
            self.image, self.rect = load_image('car_small_up.png', -1)
        if direction == 'S':
            self.image, self.rect = load_image('car_small_down.png', -1)

        # Initially start the car at the start of the lane
        self.position = 0.0

        self.name = name
        # self.start = start
        # self.finish = finish
        self.length = length
        self.width = width
        # self.rect = pygame.Rect(self.start[0], self.start[1], self.length, self.width)
        self.rect = pygame.Rect(0, 0, self.length, self.width)
        self.speed = speed
        self.maxSpeed = maxSpeed
        self.acceleration = acceleration
        # self.turnPoint = turnPoint
        self.direction = direction
        # self.hasTurned = False
        self.inQ = False

    def update_cycle(self, lane, queue_length):
        # TODO: prevent crashes by predicting stopping distance
        if lane.checklight() == 'green':
            self.inQ = False
            self.speed = min(self.speed + self.acceleration, self.maxSpeed)
        elif self.passed_light():
            self.inQ = False
            self.speed = min(self.speed + self.acceleration, self.maxSpeed)
        elif self.before_queue(queue_length):
            self.speed = min(self.speed + self.acceleration, self.maxSpeed)
        else:
            self.inQ = True
            self.speed = 0

        self.position += (self.speed * FACTOR_SPEED) / LANE_LENGTH

        if self.position > 1.0:
            self.kill()

    def render(self, lane):
        start, end = get_lane_points(lane, get_screen_center(), center_line=True)

        if self.direction == 'E':
            self.rect.center = (start.x + self.position * LANE_LENGTH,
                                start.y)
        if self.direction == 'W':
            self.rect.center = (start.x - self.position * LANE_LENGTH,
                                start.y)
        # TODO: rotate car sprite and fix x-direction off-sets
        if self.direction == 'N':
            self.rect.center = (start.x + self.rect.width * 0.25,
                                start.y - self.position * LANE_LENGTH)
        if self.direction == 'S':
            self.rect.center = (start.x + self.rect.width * 0.25,
                                start.y + self.position * LANE_LENGTH)

    def frameUpdate(self, light, qlength, prevCar):
        if light == 'green':
            self.inQ = False
            self.speed = min(self.speed + self.acceleration, self.maxSpeed)
        elif self.isPassedLight():
            self.inQ = False
            self.speed = min(self.speed + self.acceleration, self.maxSpeed)
        elif self.beforeQ(qlength):
            self.speed = min(self.speed + self.acceleration, self.maxSpeed)
        else:
            self.inQ = True
            self.speed = 0
        self.move()

    def move(self):
        loc = self.rect.topleft
        if self.direction == 'E':
            if loc[0] > self.finish:
                self.kill()
            else:
                self.rect.move_ip(self.speed * 0.05, 0)
        if self.direction == 'W':
            if loc[0] < self.finish:
                self.kill()
            else:
                self.rect.move_ip(self.speed * -0.05, 0)
        if self.direction == 'N':
            if loc[1] > self.finish:
                self.kill()
            else:
                self.rect.move_ip(0, -self.speed * 0.05)
        if self.direction == 'S':
            if loc[1] < self.finish:
                self.kill()
            else:
                self.rect.move_ip(0, self.speed * 0.05)

    def passed_light(self):
        return self.position > LANE_LIGHT_LOCATION

    def before_queue(self, qlength):
        # TODO
        if self.position < 0.8:
            return True
        return False

    def isPassedLight(self):
        loc = self.rect.topleft
        if self.direction == 'E':
            if loc[0] > self.turnPoint:
                return True

        if self.direction == 'W':
            if loc[0] < self.turnPoint:
                return True

        if self.direction == 'N':
            if loc[1] < self.turnPoint:
                return True

        if self.direction == 'S':
            if loc[1] > self.turnPoint:
                return True
        return False

    def beforeQ(self, qlength):
        loc = self.rect.topleft
        if self.direction == 'E' and (loc[0] < (self.turnPoint - qlength)):
            return True
        if self.direction == 'W' and (loc[0] > (self.turnPoint + qlength)):
            return True
        if self.direction == 'N' and (loc[1] > (self.turnPoint + qlength)):
            return True
        if self.direction == 'S' and (loc[1] < (self.turnPoint - qlength)):
            return True
        return False
