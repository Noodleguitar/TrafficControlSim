import copy

import pygame

from sim_utils.config import LANE_LIGHT_LOCATION, LANE_LENGTH, FACTOR_SPEED, SAFETY_DISTANCE, EMERGENCY_RED_MAX_SPEED, \
    METHOD
from sim_utils.utils import load_image, get_screen_center, get_lane_points, stopping_position, get_rotation, \
    acceleration_time


class Vehicle(pygame.sprite.Sprite):
    def __init__(self, name: str, speed: int, max_speed: int,
                 acceleration: int, braking: int, turn_rate: int, scale: tuple,
                 direction: str,  dataStorage, next_lane, id_: int = -1, time_waited: int = 0, debug=False):
        self.dataStorage = dataStorage
        pygame.sprite.Sprite.__init__(self)

        self.load_car_image(direction, name, scale)

        # Font for debugging purposes
        self.font = pygame.font.SysFont("monospace", 14)

        # Initially start the car at the start of the lane
        self.position = 0.0

        self.direction = direction
        self.next_lane = next_lane
        self.id = id_
        self.name = name
        self.scale = scale
        # TODO: better solution to determine length/width
        self.width = min(self.rect.height, self.rect.width)
        self.length = max(self.rect.height, self.rect.width)
        self.rect = pygame.Rect(-100, -100, self.rect.width, self.rect.height)
        self.speed = speed
        self.max_speed = max_speed
        self.acceleration = acceleration
        self.turn_rate = turn_rate
        self.braking = braking
        self.turning = False
        self.turning_start = None
        self.reached_destination = False
        self.ticks = 0
        self.wait_time = time_waited

        self.debug = debug
        # TODO: debug
        self.queue_length = 0

        if self.next_lane and not self.direction_change(self.next_lane, self.direction):
            # No direction change, zero turn rate
            self.turn_rate = 0

    def update_cycle(self, lane, queue_length, previous_car, intersection_blocked):
        self.ticks += 1

        # If car is stopped in queue, increase wait time
        if lane.towards and self.speed == 0:
            self.wait_time += 1

        if self.turning and self.direction_change(self.next_lane, self.direction):
            self.speed = 0

        elif (previous_car is not None and
              (stopping_position(self.position, max(self.length, self.width), self.speed, self.braking) >
               stopping_position(previous_car.position, max(previous_car.length, previous_car.width),
                                 previous_car.speed, previous_car.braking) -
               max(previous_car.length, previous_car.width) / LANE_LENGTH - SAFETY_DISTANCE)):
            # Braking now avoids a collision with the car in front
            self.speed = max(0, self.speed - self.braking)

        elif lane.checklight() == 'green':
            # Light is green; accelerate
            self.speed = min(self.speed + self.acceleration, self.max_speed)

        elif self.passed_light():
            # Already passed the light; accelerate
            self.speed = min(self.speed + self.acceleration, self.max_speed)

        elif (stopping_position(self.position, max(self.length, self.width), self.speed, self.braking) >
              LANE_LIGHT_LOCATION - SAFETY_DISTANCE):
            # Braking now stops before the light
            self.speed = max(0, self.speed - self.braking)

        else:
            # No action required, accelerate
            self.speed = min(self.speed + self.acceleration, self.max_speed)

        if (lane.towards and
            intersection_blocked and
            LANE_LIGHT_LOCATION > self.position > (LANE_LIGHT_LOCATION - 0.05)):
            # Car is about to enter intersection but emergency is crossing; brake
            self.speed = max(0, self.speed - self.braking)

        if (previous_car is not None and
            previous_car.position >LANE_LIGHT_LOCATION and
            self.direction_change(previous_car.next_lane, previous_car.direction)):
            # Car in front is turning, wait at light
            self.speed = max(0, self.speed - self.braking)

        self.position += (self.speed * FACTOR_SPEED) / LANE_LENGTH

        # TODO: debug
        self.queue_length = queue_length

        keep_car = True
        if self.position > 1.0:
            if self.next_lane:
                # Car transitions to next lane
                if self.turning:
                    if self.ticks - self.turning_start > self.turn_rate:
                        # Car is done turning, remove car, add one to next lane
                        self.turning = False
                        keep_car = False
                        self.next_lane[0].addCar(
                            Vehicle(self.name, self.speed, self.max_speed,
                                    self.acceleration, self.braking, self.turn_rate, self.scale,
                                    self.next_lane[1], self.dataStorage, None,
                                    time_waited=self.wait_time, debug=self.debug)
                        )
                else:
                    # Start turning on the intersection
                    self.turning = True
                    self.turning_start = self.ticks
            else:
                # Car has reached destination
                self.dataStorage.add_destination(self.direction, self.ticks, self.wait_time)
                keep_car = False

        if not keep_car:
            # Remove sprite from group
            self.kill()
            return False
        return True

    def update_emergency(self, lane):
        self.ticks += 1

        if self.position < (LANE_LIGHT_LOCATION - 0.15):
            # Accelerate towards max speed
            self.speed = min(self.speed + self.acceleration, self.max_speed)
        elif lane.checklight() != 'green':
            # Slow down to maximum red traversing speed
            self.speed = max(EMERGENCY_RED_MAX_SPEED, self.speed - self.braking)
        else:
            # Accelerate
            self.speed = min(self.speed + self.acceleration, self.max_speed)

        self.position += (self.speed * FACTOR_SPEED) / LANE_LENGTH

        # TODO: Below is copied from update_cycle()
        keep_car = True
        if self.position > 1.0:
            if self.next_lane:
                # Car transitions to next lane
                if self.turning:
                    if self.ticks - self.turning_start > self.turn_rate:
                        # Car is done turning, remove car, add one to next lane
                        self.turning = False
                        keep_car = False
                        self.next_lane[0].add_emerg_vehicle(
                            Vehicle(self.name, self.speed, self.max_speed,
                                    self.acceleration, self.braking, self.turn_rate, self.scale,
                                    self.next_lane[1], self.dataStorage, None, debug=self.debug)
                        )
                else:
                    # Start turning on the intersection
                    self.turning = True
                    self.turning_start = self.ticks
            else:
                # Car has reached destination
                keep_car = False

        if not keep_car:
            # Remove sprite from group
            self.kill()
            return False
        return True

    def render(self, screen, lane, prev_car, side_parked=False):
        if side_parked:
            start, end = get_lane_points(lane, get_screen_center(), order_offset=1)
        else:
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
            debug_output = 'None'
            # debug_output = str(self.id) + ', ' + str(previous_id)
            # debug_output = str(self.direction)
            # debug_output = str(self.queue_length)
            if lane.light is not None:
                debug_output = str(round(lane.light.getGreentime(), 2))
            # debug_output = str(round(acceleration_time(1.0-self.position, self.speed, self.acceleration,
            #                                            self.max_speed), 2))
            # debug_output = str(lane.emergency_active)

            text = self.font.render(debug_output, 1, (255, 255, 255), (0, 0, 0))
            screen.blit(text, self.rect.bottomright)

    def passed_light(self):
        return self.position > LANE_LIGHT_LOCATION

    def rotate_car(self, angle_start, angle_end, portion):
        current_angle = portion * (angle_end - angle_start)
        self.image = pygame.transform.rotate(self.image, current_angle)
        self.rect = self.image.get_rect()

    def load_car_image(self, direction, vehicle_name, scale):
        self.image, self.rect = load_image(vehicle_name + '.png', -1)

        # Scale original image
        new_width = int(self.rect.width * scale[0])
        new_height = int(self.rect.height * scale[1])
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

        # Rotate image according to direction
        rotation_angle = get_rotation(direction)
        self.image = pygame.transform.rotate(self.image, rotation_angle)
        self.rect = self.image.get_rect()

    @staticmethod
    def direction_change(next_lane, direction):
        if next_lane and next_lane[1] != direction:
            return True
        return False
