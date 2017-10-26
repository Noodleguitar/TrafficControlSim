WIDTH = 1778
HEIGHT = 1000
FRAMERATE = 300
DEBUG = False
# Duration of data collection period given as number of frames
RUN_TIME = 54000
# Run identifier for results exporting
TEST_RUN_NUMBER = 0

CAR_EVERY_FRAMES = 88
MIN_GREEN_TIME = 240
EMERGENCY_RED_MAX_SPEED = 25
SAFETY_DISTANCE = 0.01
# Maximum distance between light and car in which communication is possible
COMMUNICATION_DISTANCE = 0.7

FACTOR_SPEED = 0.05

LANE_LIGHT_LOCATION = 0.95
LANE_WIDTH = 35
LANE_LENGTH = 1000
ROAD_SEPARATION_WIDTH = 2
# Method to apply to traffic control, 'default' or 'Laemmer'
METHOD = "Laemmer"

LIGHT_COLOURS = {'red':     (255, 0, 0),
                 'yellow':  (255, 255, 0),
                 'green':   (0, 255, 0)}


# Normal car
class VehicleCar:
    name = 'car'
    speed = 50
    max_speed = 90
    acceleration = 1
    braking = 2
    turning_rate = 10
    scale = (0.9, 0.9)
    spawn_rate = 0.9


# Truck
class VehicleTruck:
    name = 'truck'
    speed = 50
    max_speed = 60
    acceleration = 1
    braking = 1
    turning_rate = 90
    scale = (0.45, 0.45)
    spawn_rate = 0.1


# Police vehicle
class VehicleEmergency:
    name = 'police'
    speed = 70
    max_speed = 120
    acceleration = 2
    braking = 3
    turning_rate = 5
    scale = (0.9, 0.9)
    spawn_rate = 0.01
