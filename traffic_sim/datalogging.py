class DataLogging:
    def __init__(self):
        self.westCount = 0
        self.eastCount = 0
        self.northCount = 0
        self.southCount = 0

    def add_destination(self, direction):
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

    def getTotal(self):
        return (self.westCount + self.eastCount + self.northCount + self.southCount)
