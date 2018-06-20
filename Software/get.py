import requests
import threading
import serial
import time

serialPort = serial.Serial('COM3', 9600)

# asd = "F1111A"
# das = "X2341A"
# port.write(asd.encode())
# port.write(das.encode())
# data = port.read(6)
# print(data)
# data = port.read(6)
# print(data)

class Ball:
  def __init__(self, x, y, radius, color):
    self.x = x
    self.y = y
    self.radius = radius
    self.color = color

  def example(self):
    pass

class Robot:
  def __init__(self, frontBall, backBall):
    self.frontBall = frontBall
    self.backBall = backBall


# Define the IP address and Port of the Server.
ip_address = "127.0.0.1"
port = "8000"

myFrontColor = 'CYAN'
myBackColor = 0
enemyFrontColor = 0
enemyBackColor = 0
targetBallColor = 0
enemyBallColor = 0

targetBalls = []
enemyBalls = []

myRobot = Robot(0, 0)
enemyRobot = Robot(0, 0)


def loop(): 
  threading.Timer(2, loop).start()
  r = requests.get("http://" + ip_address + ":" + port)
  responses = r.json()
  balls = len(responses)
  
  print("Enviando")
  serialPort.write(str(balls).encode())
  print("Recibido:")
  data = serialPort.read(1)
  print(data)








  # targetBalls = []
  # enemyBalls = []

  # for response in responses:
  #   x = response[0][0]
  #   y = response[0][1]
  #   radius = response[1]
  #   color = response[2]
  #   ball = Ball(x, y, radius, color)
    
  #   if ball.color == targetBallColor:
  #     targetBalls.append(ball)
  #   elif ball.color == enemyBallColor:
  #     enemyBalls.append(ball)
  #   elif ball.color == myFrontColor:
  #     myRobot.frontBall = ball
  #   elif ball.color == myBackColor:
  #     myRobot.backBall = ball
  #   elif ball.color == enemyFrontColor:
  #     enemyRobot.frontBall = ball
  #   elif ball.color == enemyBackColor:
  #     enemyRobot.backBall = ball
  #   else:
  #     pass
    
loop()
