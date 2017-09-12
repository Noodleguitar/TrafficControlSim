# class Signal:
#     def __init__(self):
#         # State of traffic light, 0 = green, 1 = yellow, 2 = red
#         self.state = 0


# from collections import defaultdict

import pygame

from .sim_utils.utils import Coord


LANE_WIDTH = 15
LANE_LENGTH = 200
ROAD_SEPARATION_WIDTH = 2


class Lane:
    def __init__(self, direction: Coord, towards: bool, order: int):
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


class Intersection:
    def __init__(self, center: Coord):
        self.center = center
        self.lanes = list()
        # self.signals = list()

    def add_lane(self, direction, towards, order):
        self.lanes.append(Lane(direction, towards, order))

    def render(self, surface):
        for lane in self.lanes:
            start, end = self.get_lane_points(lane)
            pygame.draw.line(surface, (255, 255, 255), (start.x, start.y), (end.x, end.y))


def get_lane_points(lane: Lane, center: Coord):
    if abs(lane.direction.x) > 0:
        # Horizontal lane
        if lane.direction.x > 0:
            # East direction
            start_y = center.y + ROAD_SEPARATION_WIDTH + (lane.order + 1) * LANE_WIDTH
            if lane.towards:
                start = Coord(x=center.x - LANE_LENGTH,
                              y=start_y)
            else:
                start = Coord(x=center.x,
                              y=start_y)
        else:
            # West direction
            start_y = center.y - ROAD_SEPARATION_WIDTH - (lane.order + 1) * LANE_WIDTH
            if lane.towards:
                start = Coord(x=center.x + LANE_LENGTH,
                              y=start_y)
            else:
                start = Coord(x=center.x,
                              y=start_y)
    else:
        # Vertical lane
        # TODO
        pass

    # placeholder
    # TODO: add direction * length to start coordinate
    end = Coord(x=0, y=0)

    return start, end