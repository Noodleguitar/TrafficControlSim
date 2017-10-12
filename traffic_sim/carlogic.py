import pygame

from sim_utils.config import LANE_LIGHT_LOCATION, LANE_LENGTH, FACTOR_SPEED, SAFETY_DISTANCE
from sim_utils.utils import load_image, get_screen_center, get_lane_points, stopping_position


class Vehicle(pygame.sprite.Sprite):
    def __init__(self, name: str, speed: int, max_speed: int,
                 acceleration: int, braking: int, direction,  dataStorage, id_: int = -1, debug=False):
        self.dataStorage = dataStorage
        pygame.sprite.Sprite.__init__(self)
        if direction == 'E':
            self.image, self.rect = load_image('car_small_right.png', -1)
        if direction == 'W':
            self.image, self.rect = load_image('car_small_left.png', -1)
        if direction == 'N':
            self.image, self.rect = load_image('car_small_up.png', -1)
        if direction == 'S':
            self.image, self.rect = load_image('car_small_down.png', -1)

        # Font for debugging purposes
        self.font = pygame.font.SysFont("monospace", 14)

        # Initially start the car at the start of the lane
        self.position = 0.0

        self.id = id_
        self.name = name
        self.width = self.rect.width
        self.length = self.rect.height
        self.rect = pygame.Rect(-100, -100, self.rect.width, self.rect.height)
        self.speed = speed
        self.max_speed = max_speed
        self.acceleration = acceleration
        self.braking = braking
        self.direction = direction
        self.inQ = False

        self.debug = debug

    def update_cycle(self, lane, queue_length, previous_car):
        print(str(self.dataStorage.getTotal()))
        if lane.checklight() == 'green':
            # Light is green, accelerate
            self.inQ = False
            self.speed = min(self.speed + self.acceleration, self.max_speed)
        elif self.passed_light():
            # Already passed the light, accelerate
            self.inQ = False
            self.speed = min(self.speed + self.acceleration, self.max_speed)
        elif (stopping_position(self.position, max(self.length, self.width), self.speed, self.braking) >
              LANE_LIGHT_LOCATION - SAFETY_DISTANCE):
            # Braking now stops before the light
            self.inQ = True
            self.speed = max(0, self.speed - self.braking)
        elif (previous_car is not None and
              (stopping_position(self.position, max(self.length, self.width), self.speed, self.braking) >
               stopping_position(previous_car.position, max(previous_car.length, previous_car.width),
                                 previous_car.speed, previous_car.braking) -
               max(previous_car.length, previous_car.width) / LANE_LENGTH - SAFETY_DISTANCE)):
            # Braking now avoids a collision with the car in front
            self.speed = max(0, self.speed - self.braking)
        else:
            # No action required, accelerate
            self.inQ = False
            self.speed = min(self.speed + self.acceleration, self.max_speed)

        self.position += (self.speed * FACTOR_SPEED) / LANE_LENGTH

        # if self.position > 1.0:
        #     self.kill()

    def render(self, screen, lane, prev_car):
        start, end = get_lane_points(lane, get_screen_center(), center_line=True)

        if self.direction == 'E':
            self.rect.center = (start.x + self.position * LANE_LENGTH,
                                start.y)
        if self.direction == 'W':
            self.rect.center = (start.x - self.position * LANE_LENGTH,
                                start.y)
        if self.direction == 'N':
            self.rect.center = (start.x,
                                start.y - self.position * LANE_LENGTH)
        if self.direction == 'S':
            self.rect.center = (start.x,
                                start.y + self.position * LANE_LENGTH)
        if self.debug:
            # debug_output = str(round(self.position, 2))
            previous_id = -1
            if prev_car is not None:
                previous_id = prev_car.id
            debug_output = str(self.id) + ', ' + str(previous_id)

            text = self.font.render(debug_output, 1, (255, 255, 255), (0, 0, 0))
            screen.blit(text, self.rect.bottomright)

    def frameUpdate(self, light, qlength, prevCar):
        if light == 'green':
            self.inQ = False
            self.speed = min(self.speed + self.acceleration, self.max_speed)
        elif self.isPassedLight():
            self.inQ = False
            self.speed = min(self.speed + self.acceleration, self.max_speed)
        elif self.beforeQ(qlength):
            self.speed = min(self.speed + self.acceleration, self.max_speed)
        else:
            self.inQ = True
            self.speed = 0
        self.move()

    def move(self):
        loc = self.rect.topleft
        if self.direction == 'E':
            if self.position > 1.0:
                self.dataStorage.addEast()
                self.kill()
            else:
                self.rect.move_ip(self.speed * 0.05, 0)
        if self.direction == 'W':
            if self.position < 1.0:
                self.dataStorage.addWest()
                self.kill()
            else:
                self.rect.move_ip(self.speed * -0.05, 0)
        if self.direction == 'N':
            if self.position > 1.0:
                self.dataStorage.addNorth()
                self.kill()
            else:
                self.rect.move_ip(0, -self.speed * 0.05)
        if self.direction == 'S':
            if self.position < 1.0:
                self.dataStorage.addSouth()
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
