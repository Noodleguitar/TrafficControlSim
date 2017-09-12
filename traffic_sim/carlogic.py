class Vehicle:

  def __init__(self, length, width, vehicleType, speed, turn, lane, maxSpeed, acceleration, id):
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
      if (lane.checkLight):
          speed = max(speed - brakeSpeed,0)
      if(not lane.checkLight):
          speed = min(speed + acceleration ,maxSpeed)

      return(speed)


class TrafficLight:

  def __init__(self,color, strategy, id):
      self.Green = color
      self.id = id
      self.strategy =strategy
      self.framerateCount = 0

  if (self.strategy = classic):
      self.changeRate = 180


  def frameUpdate(self):
      self.framerateCount += 1
      if (changerate=<framerateCount)
          framerateCount = 0
          self.changeLight()
  def checkLight(self):



  def changeLight(self):
    self.color = not color





