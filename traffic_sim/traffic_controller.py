import operator

# TODO: find out which traffic lights conflict with each other


class Controller:
    def __init__(self, lanes: list):
        self.lanes = lanes

        # Collect lanes with a traffic light attached to them
        self.light_lanes = self.gather_light_lanes(lanes)

    def update(self):
        # TODO: sort lanes by queue length, find lane that has green, check green time; switch if possible (if yellow).
        pass

    @staticmethod
    def gather_light_lanes(lanes):
        lane_lights = list()
        for l in lanes:
            if l.light is not None:
                lane_lights.append(l)
        return lane_lights
