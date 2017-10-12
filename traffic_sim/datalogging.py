class DataLogging:
    def __init__(self):
        self.westCount = 0
        self.eastCount = 0
        self.northCount = 0
        self.southCount = 0


    def addWest(self):
        self.westCount += 1
    def addEast(self):
        self.EastCount += 1
    def addNorth(self):
        self.northCount += 1
    def addSouth(self):
        self.southCount += 1
    def getTotal(self):
        return (self.westCount + self.eastCount + self.northCount + self.southCount)
