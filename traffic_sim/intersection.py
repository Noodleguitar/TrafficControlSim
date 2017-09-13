import pygame

from sim_utils.utils import Coord


LANE_WIDTH = 35
LANE_LENGTH = 500
ROAD_SEPARATION_WIDTH = 1


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

    def checklight(self):
        return self.light.green


class Intersection:
    def __init__(self, center: Coord):
        self.center = center
        self.lanes = list()
        # self.signals = list()

    def add_lane(self, direction, towards, order, light=None):
        self.lanes.append(Lane(direction, towards, order, light=light))

    def render(self, surface):
        for lane in self.lanes:
            start, end = get_lane_points(lane, self.center)
            pygame.draw.line(surface, (255, 255, 255), (start.x, start.y), (end.x, end.y))
            start, end = get_lane_points(lane, self.center, order_offset=1)
            pygame.draw.line(surface, (255, 255, 255), (start.x, start.y), (end.x, end.y))


def get_lane_points(lane: Lane, center: Coord, order_offset=0):
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

    # placeholder
    end = Coord(start.x + lane.direction.x * LANE_LENGTH,
                start.y + lane.direction.y * LANE_LENGTH)

    return start, end
