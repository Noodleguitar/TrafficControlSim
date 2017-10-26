import numpy as np
import pygame

from carlogic import Vehicle
from sim_utils.config import LANE_LIGHT_LOCATION, LIGHT_COLOURS, LANE_WIDTH, LANE_LENGTH, METHOD
from sim_utils.utils import Coord, get_lane_points


class Intersection:
    def __init__(self, center: Coord):
        self.center = center
        self.lanes = list()
        self.blocked = False
        # self.signals = list()

    def get_lanes(self):
        return self.lanes

    def add_lane(self, direction, towards, order, light=None):
        self.lanes.append(Lane(direction, towards, order, light=light))

    def update_lanes(self, screen):
        emergency_lanes = [lane.emergency_near_intersection() for lane in self.lanes]
        self.blocked = np.any(emergency_lanes)

        for lane in self.lanes:
            lane.update_lane(screen, self.blocked)
        self.blocked = False

    def render(self, surface):
        for lane in self.lanes:
            # Draw first line (closest to center)
            start, end = get_lane_points(lane, self.center)
            pygame.draw.line(surface, (255, 255, 255), (start.x, start.y), (end.x, end.y))
            # Draw second line
            start_off, end_off = get_lane_points(lane, self.center, order_offset=1)
            pygame.draw.line(surface, (255, 255, 255), (start_off.x, start_off.y), (end_off.x, end_off.y))
            # Render the traffic light on this lane if applicable
            render_light_(surface, lane, start, end)


class TrafficLight:
    def __init__(self, strategy: str, id_: int):
        self.id = id_
        self.state = 'red'
        self.strategy = strategy
        self.framerateCount = 0
        self.framesInRotation = 1200
        self.greenTime = self.framesInRotation / 6
        self.yellow_time = 130
        self.green_set = False

    def get_current_light_time(self):
        return self.framerateCount

    def set_state(self, state):
        if state == 'green':
            self.green_set = True
        else:
            self.green_set = False
        self.state = state
        self.framerateCount = 0

    def frameUpdate(self):
        self.framerateCount += 1
        if self.state == 'yellow' and self.framerateCount >= self.yellow_time:
            # Change to red
            self.set_state('red')

    def setGreentime(self, greentime: int):
        self.greenTime = greentime

    def getGreentime(self):
        return self.greenTime

    def is_green_set(self):
        return self.green_set


class Lane:
    def __init__(self, direction: Coord, towards: bool, order: int, light=None):
        """
        Create a lane going towards or from the intersection.
        :param direction: (Coord) Unit vector of direction of lane.
        :param towards: (bool) Whether the lane is going towards or away from the intersection.
        :param order: (int) Order from center of road of the lane indexed by zero, in case multiple lanes exist
        with the same direction.
        """
        self.direction = direction
        self.towards = towards
        self.order = order
        self.light = light
        self.car_sprites = pygame.sprite.Group()
        self.cars = list()
        self.emerg_vehicles = list()
        self.queue_length = 0
        self.delay = 15
        self.emergency_active = False
        self.greenTime = 0

        if (light is not None) and (not towards):
            raise ValueError('[Lane.__init__] Attempting to add a traffic light to a lane going away from the '
                             'intersection.')

    def addCar(self, v: Vehicle):
        self.cars.append(v)
        self.cars[-1].id = len(self.cars) - 1
        self.car_sprites.add(v)

    def add_emerg_vehicle(self, v: Vehicle):
        self.emerg_vehicles.append(v)
        self.car_sprites.add(v)
        self.emergency_active = True

    def update_lane(self, screen, intersection_blocked):
        # Update traffic light assigned to this lane (if any)
        if self.light is not None:
            self.light.frameUpdate()

        # Determine current queue_length
        self.queue_length = self.determine_queue(method=METHOD)
        # Update vehicles
        self.update_cars(screen, intersection_blocked)
        self.update_emerg_vehicles(screen)
        # TODO: move drawing somewhere else
        self.car_sprites.draw(screen)

    def update_cars(self, screen, intersection_blocked):
        removed_idcs = list()
        prev_car = None
        for i, car in enumerate(self.cars):
            if prev_car is not None:
                assert prev_car is not car

            # Apply motion of the car
            if not car.update_cycle(self, self.queue_length, prev_car, self.emergency_active, intersection_blocked):
                # Car should be deleted
                removed_idcs.append(i)
            car.render(screen, self, prev_car, self.emergency_active)
            prev_car = car

        # Remove deleted cars from list
        for index in sorted(removed_idcs, reverse=True):
            del self.cars[index]

    def update_emerg_vehicles(self, screen):
        removed_idcs = list()
        for i, veh in enumerate(self.emerg_vehicles):
            # Apply motion of the car
            if not veh.update_emergency(self):
                # Car should be deleted
                removed_idcs.append(i)
            veh.render(screen, self, None, False)

        # Remove deleted cars from list
        for index in sorted(removed_idcs, reverse=True):
            del self.emerg_vehicles[index]

        if len(self.emerg_vehicles) == 0:
            self.emergency_active = False

    def emergency_near_intersection(self):
        if not self.towards:
            return False

        for em in self.emerg_vehicles:
            if em.position > (LANE_LIGHT_LOCATION - 0.15) or em.position > LANE_LIGHT_LOCATION:
                # Emergency vehicle is close to intersection
                return True
        return False

    def determine_queue(self, method='Laemmer'):
        if method == 'default':
            return self.queue_default_(self.cars)
        if method == 'Laemmer':
            return self.queue_laemmer_(self.cars)

    @staticmethod
    def queue_default_(cars):
        queue_length = 0
        for car in cars:
            if car.speed == 0:
                # Car is stopped in the lane
                queue_length += 1
        return queue_length

    def queue_laemmer_(self, cars):
        time_to_clear_q = 0
        for car in cars:
            time_to_clear_q += car.length / car.max_speed
            time_to_clear_q += (car.max_speed - car.speed) / car.acceleration
            time_to_clear_q += car.turn_rate

        # Set light green time if it has not been set already
        if self.light is not None and not self.light.is_green_set():
            self.light.setGreentime(time_to_clear_q)

        # The (esitmated) time to clear the lane determines the queue length
        return time_to_clear_q

    def checklight(self):
        # TODO: handle None light exception differently
        if self.light is None:
            return 'green'
        return self.light.state


def render_light_(surface, lane: Lane, start: Coord, end: Coord):
    if lane.light is None:
        # No light to render
        return

    line_start = Coord(x=start.x + (end.x - start.x) * LANE_LIGHT_LOCATION,
                       y=start.y + (end.y - start.y) * LANE_LIGHT_LOCATION)
    # Traffic light line should be normal to the lane direction
    line_end = Coord(x=line_start.x - lane.direction.y * LANE_WIDTH,
                     y=line_start.y + lane.direction.x * LANE_WIDTH)

    line_colour = LIGHT_COLOURS[lane.checklight()]
    pygame.draw.line(surface, line_colour, (line_start.x, line_start.y), (line_end.x, line_end.y), 2)
