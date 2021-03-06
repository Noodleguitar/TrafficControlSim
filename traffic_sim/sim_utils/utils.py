from collections import namedtuple
import os
import math

import numpy as np
import pygame
from pygame.locals import RLEACCEL

from .config import LANE_LENGTH, LANE_WIDTH, ROAD_SEPARATION_WIDTH, WIDTH, HEIGHT, FACTOR_SPEED

Coord = namedtuple('Coord', ['x', 'y'])


def get_screen_center():
    return Coord(x=WIDTH * 0.5, y=HEIGHT * 0.5)


def get_rotation(direction: str):
    if direction == 'E':
        return 0
    if direction == 'W':
        return 180
    if direction == 'N':
        return 90
    if direction == 'S':
        return 270


def acceleration_time(distance, speed, acceleration, max_speed):
    distance = (distance * LANE_LENGTH) / FACTOR_SPEED
    speed_diff = max_speed - speed
    max_speed_time = speed_diff / acceleration
    # s = v_0*t + 0.5*a*t^2  --->
    # 0.5*a*t^2 + v_0*t - s = 0
    # Solve quadratic function and use positive solution
    distance_time = max(np.polynomial.polynomial.polyroots([-distance, speed, 0.5*acceleration]))
    if distance_time > max_speed_time:
        # Max speed is reached before the distance is travelled
        distance_max_speed = travel_time(speed, max_speed, acceleration)
        distance_left = distance - distance_max_speed
        time_left = distance_left / max_speed
        return max_speed_time + time_left
    else:
        return distance_time


def travel_time(speed_start, speed_end, acceleration):
    frames = (speed_end - speed_start) / acceleration
    return speed_start * frames + 0.5 * acceleration * frames**2


def stopping_distance(speed, braking):
    frames = speed / braking
    # s = 0.5 * a * t^2
    distance = 0.5 * braking * frames**2 + frames
    return (distance * FACTOR_SPEED) / LANE_LENGTH


def stopping_position(position, length, speed, braking):
    return position + stopping_distance(speed, braking) + (length * 0.5) / LANE_LENGTH


# TODO: this should be in intersection, without circularly referencing carlogic and intersection
def get_lane_points(lane, center: Coord, order_offset=0, center_line=False):
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

    if center_line:
        # Shift line to center of the lane
        side_direction = perpendicular(lane.direction)
        start = Coord(start.x + side_direction.x * LANE_WIDTH * 0.5,
                      start.y + side_direction.y * LANE_WIDTH * 0.5)
        end = Coord(end.x + side_direction.x * LANE_WIDTH * 0.5,
                    end.y + side_direction.y * LANE_WIDTH * 0.5)

    return start, end


def perpendicular(direction: Coord):
    return Coord(-direction.y, direction.x)


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


def chance(probability):
    value = np.random.rand(1)[0]
    if value < probability:
        return True
    return False
