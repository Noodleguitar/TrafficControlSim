WIDTH = 1600
HEIGHT = 900
FRAMERATE = 100
DEBUG = False

CAR_EVERY_FRAMES = 90
MIN_GREEN_TIME = 240
SAFETY_DISTANCE = 0.01


# Normal car
class VehicleCar:
    name = 'car'
    speed = 50
    max_speed = 90
    acceleration = 1
    braking = 2
    turning_rate = 10
# TODO: other types of vehicles

FACTOR_SPEED = 0.05

LANE_LIGHT_LOCATION = 0.95
LANE_WIDTH = 35
LANE_LENGTH = 1000
ROAD_SEPARATION_WIDTH = 2

LIGHT_COLOURS = {'red':     (255, 0, 0),
                 'yellow':  (255, 255, 0),
                 'green':   (0, 255, 0)}
