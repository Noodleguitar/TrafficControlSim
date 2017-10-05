import pygame
from sim_utils.utils import Coord
from carlogic import Vehicle


LANE_WIDTH = 35
LANE_LENGTH = 1000
ROAD_SEPARATION_WIDTH = 2
LIGHT_COLOURS = {'red':     (255, 0, 0),
                 'yellow':  (255, 255, 0),
                 'green':   (0, 255, 255)}


class Intersection:
    def __init__(self, center: Coord):
        self.center = center
        self.lanes = list()
        # self.signals = list()

    def get_lanes(self):
        return self.lanes

    def add_lane(self, direction, towards, order, light=None):
        self.lanes.append(Lane(direction, towards, order, light=light))

    def render(self, surface):
        for lane in self.lanes:
            # Draw first line (closest to center)
            start, end = get_lane_points_(lane, self.center)
            pygame.draw.line(surface, (255, 255, 255), (start.x, start.y), (end.x, end.y))
            # Draw second line
            start_off, end_off = get_lane_points_(lane, self.center, order_offset=1)
            pygame.draw.line(surface, (255, 255, 255), (start_off.x, start_off.y), (end_off.x, end_off.y))
            # Render the traffic light on this lane if applicable
            render_light_(surface, lane, start, end)


class TrafficLight:
    def __init__(self, green: bool, strategy: str, id_: int):
        if green:
            self.state = 'green'
        else:
            self.state = 'red'
        self.id = id_
        self.strategy = strategy
        self.framerateCount = 0
        self.framesInRotation = 1200
        self.greentime = self.framesInRotation / 6
        self.yellow_time = 130

    def get_current_light_time(self):
        return self.framerateCount

    def set_state(self, state):
        self.state = state
        self.framerateCount = 0

    def frameUpdate(self):
        self.framerateCount += 1
        if self.state == 'yellow' and self.framerateCount >= self.yellow_time:
            # Change to red
            self.set_state('red')


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
        self.cars_sprites = pygame.sprite.Group()
        self.queue_length = 0

        if (light is not None) and (not towards):
            raise ValueError('[Lane.__init__] Attempting to add a traffic light to a lane going away from the '
                             'intersection')

    def addCar(self, v: Vehicle):
        self.cars_sprites.add(v)

    def updateCars(self, screen):
        # Clear queue if light is green
        if self.checklight() == 'green':
            self.queue_length = 0

        qlength = 50
        for car in self.cars_sprites:
            if car.inQ:
                qlength += car.length + 5
        prevCar = None
        for car in self.cars_sprites:
            car.frameUpdate(self.checklight(), qlength, prevCar)
            prevCar = car
        self.queue_length = qlength
        self.cars_sprites.draw(screen)

    def checklight(self):
        return self.light.state


def render_light_(surface, lane: Lane, start: Coord, end: Coord):
    if lane.light is None:
        # No light to render
        return

    line_start = Coord(x=start.x + (end.x - start.x) * 0.95,
                       y=start.y + (end.y - start.y) * 0.95)
    # Traffic light line should be normal to the lane direction
    line_end = Coord(x=line_start.x - lane.direction.y * LANE_WIDTH,
                     y=line_start.y + lane.direction.x * LANE_WIDTH)

    line_colour = LIGHT_COLOURS[lane.checklight()]
    pygame.draw.line(surface, line_colour, (line_start.x, line_start.y), (line_end.x, line_end.y), 2)


def get_lane_points_(lane: Lane, center: Coord, order_offset=0):
    if abs(lane.direction.x) > 0:
        # Horizontal lane
        if lane.direction.x > 0:
            # East direction
            start_y = center.y + ROAD_SEPARATION_WIDTH + (lane.order + order_offset) * LANE_WIDTH
            if lane.towards:
                start = Coord(x=center.x - LANE_LENGTH,
                              y=start_y)
            else:
                start = Coord(x=center.x,
                              y=start_y)
        else:
            # West direction
            start_y = center.y - ROAD_SEPARATION_WIDTH - (lane.order + order_offset) * LANE_WIDTH
            if lane.towards:
                start = Coord(x=center.x + LANE_LENGTH,
                              y=start_y)
            else:
                start = Coord(x=center.x,
                              y=start_y)
    else:
        # Vertical lane
        if lane.direction.y > 0:
            # South direction
            start_x = center.x - ROAD_SEPARATION_WIDTH - (lane.order + order_offset) * LANE_WIDTH
            if lane.towards:
                start = Coord(x=start_x,
                              y=center.y - LANE_LENGTH)
            else:
                start = Coord(x=start_x,
                              y=center.y)
        else:
            # North direction
            start_x = center.x + ROAD_SEPARATION_WIDTH + (lane.order + order_offset) * LANE_WIDTH
            if lane.towards:
                start = Coord(x=start_x,
                              y=center.y + LANE_LENGTH)
            else:
                start = Coord(x=start_x,
                              y=center.y)

    end = Coord(start.x + lane.direction.x * LANE_LENGTH,
                start.y + lane.direction.y * LANE_LENGTH)

    return start, end
