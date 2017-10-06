from collections import namedtuple
import os
import pygame
from pygame.locals import RLEACCEL

from .config import LANE_LENGTH, LANE_WIDTH, ROAD_SEPARATION_WIDTH, WIDTH, HEIGHT

Coord = namedtuple('Coord', ['x', 'y'])


def get_screen_center():
    return Coord(x=WIDTH * 0.5, y=HEIGHT * 0.5)


# TODO: this should be in intersection, without circularly referencing carlogic and intersection
def get_lane_points(lane, center: Coord, order_offset=0):
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


def load_image(name, colorkey=None):
    fullname = os.path.join('data', 'images')
    fullname = os.path.join(fullname, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', fullname)
        raise Exception(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()
