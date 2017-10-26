import numpy as np

class DataLogging:
    def __init__(self):
        self.westCount = 0
        self.eastCount = 0
        self.northCount = 0
        self.southCount = 0
        self.travel_times = list()
        self.wait_times = list()

    def add_destination(self, direction, travel_time, wait_time):
        if direction == 'W':
            self.westCount += 1
        elif direction == 'E':
            self.eastCount += 1
        elif direction == 'N':
            self.northCount += 1
        elif direction == 'S':
            self.southCount += 1
        else:
            raise ValueError('[Datalogging.add_destination] Given direction was unknown')
        self.travel_times.append(travel_time)
        self.wait_times.append(wait_time)

    def getTotal(self):
        return (self.westCount + self.eastCount + self.northCount + self.southCount)

    def get_results(self, aggregate_function=np.median):
        return dict(
            west_count=self.westCount,
            east_count=self.eastCount,
            north_count=self.northCount,
            south_count=self.southCount,
            total_wait=self.wait_times,
            total_travel=self.travel_times,
            travel_time=aggregate_function(self.travel_times),
            wait_time=aggregate_function(self.wait_times),
            travel_variance=np.var(self.travel_times),
            wait_variance=np.var(self.wait_times)
        )
