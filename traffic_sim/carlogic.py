class Vehicle:

 	def __init__(self, length: int, width: int, vehicleType: str, speed: int, turn: int, lane: str, maxSpeed: int, acceleration: int, id: int):
    	self.length = length
    	self.width = width
	    self.vehicleType = vehicleType
	    self.speed = speed
	    self.brakeSpeed = brakeSpeed
	    self.turn = turn
	    self.id = id
	    self.lane = lane
	    self.maxSpeed = maxSpeed
	    self.acceleration = acceleration

  def frameUpdate(self):
      if (not lane.checkLight):
          speed = max(speed - brakeSpeed,0)
      if(lane.checkLight):
          speed = min(speed + acceleration ,maxSpeed)

      return(speed)


class TrafficLight:

  def __init__(self,green: bool, strategy: str, id: int):
      self.green = green
      self.id = id
      self.strategy = strategy
      self.framerateCount = 0

  if (self.strategy = classic):
      self.changeRate = 180


  def frameUpdate(self):
      self.framerateCount += 1
      if (changerate=<framerateCount)
          framerateCount = 0
          self.changeLight()

  def changeLight(self):
    self.green = not green





