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
        if self.lane.checklight() == 'yellow' or self.lane.checklight() == 'red':
            self.speed = max(self.speed - self.brakeSpeed, 0)
        else:
            self.speed = min(self.speed + self.acceleration, self.maxSpeed)
