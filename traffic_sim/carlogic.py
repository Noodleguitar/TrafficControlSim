from intersection import Lane


class Vehicle:

    def __init__(self, length: int, width: int, vehicleType: str, speed: int, turn: int, lane: Lane, maxSpeed: int,
                 acceleration: int, brakeSpeed: int, id_: int):
        self.length = length
        self.width = width
        self.vehicleType = vehicleType
        self.speed = speed
        self.brakeSpeed = brakeSpeed
        self.turn = turn
        self.id = id_
        self.lane = lane
        self.maxSpeed = maxSpeed
        self.acceleration = acceleration

    def frameUpdate(self):
        if (not self.lane.checklight()):
            self.speed = max(self.speed - self.brakeSpeed, 0)
        else:
            self.speed = min(self.speed + self.acceleration, self.maxSpeed)


class TrafficLight:

    def __init__(self, green: bool, strategy: str, id_: int):
        self.green = green
        self.id = id_
        self.strategy = strategy
        self.framerateCount = 0
        self.changeRate = 100

        if (self.strategy == 'classic'):
            self.changeRate = 180

    def frameUpdate(self):
        self.framerateCount += 1
        if (self.changeRate <= self.framerateCount):
            self.framerateCount = 0
            self.changeLight()

    def changeLight(self):
        self.green = not self.green
