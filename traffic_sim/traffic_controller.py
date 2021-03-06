import operator

from sim_utils.config import MIN_GREEN_TIME, METHOD

# TODO: find out which traffic lights conflict with each other to potentially allow double green lights


class Controller:
    def __init__(self, lanes: list):
        self.lanes = lanes

        # Collect lanes with a traffic light attached to them
        self.light_lanes = self.gather_light_lanes(lanes)

    def update(self):
        # Sort lanes with traffic lights by queue time, descending
        self.light_lanes = sorted(self.light_lanes, key=operator.attrgetter('queue_length'), reverse=True)
        for i, l in enumerate(self.light_lanes):
            if l.checklight() == 'yellow':
                # Yellow light on one of the lanes, no action taken
                return
            if l.checklight() == 'green':
                if METHOD == "Laemmer":
                    if l.light.get_current_light_time() > l.light.getGreentime():
                        # The current set green time has expired, set state to yellow
                        l.light.set_state('yellow')
                    return
                else:
                    if i > 0 and l.light.get_current_light_time() > MIN_GREEN_TIME:
                        # Lane is not the highest priority at this moment and minimum green time expired,
                        # light can be switched to yellow.
                        l.light.set_state('yellow')
                    return

        # All lights are red, set longest queue to green
        self.light_lanes[0].light.set_state('green')

    @staticmethod
    def gather_light_lanes(lanes):
        lane_lights = list()
        for l in lanes:
            if l.light is not None:
                lane_lights.append(l)
        return lane_lights
