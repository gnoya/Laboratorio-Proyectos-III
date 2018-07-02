import requests
import threading
import serial
import time
import numpy as np
import math

# Define the IP address and Port of the Server.

#serialPort = serial.Serial('COM3', 9600)
ip_address = "127.0.0.1"
port = "8000"
loopTime = 0.025 # Intervalo de loop en segundos.

myFrontColor = 'YELLOW'
myBackColor = 'BLUE'
enemyFrontColor = 0
enemyBackColor = 0
targetBallColor = 'RED'
enemyBallColor = 0

class Ball:
  def __init__(self, x, y, radius, color):
    self.x = x
    self.y = y
    self.radius = radius
    self.color = color

class Robot:
  def __init__(self, frontBall, backBall):
    self.frontBall = frontBall
    self.backBall = backBall
    self.x = (frontBall.x + backBall.x) / 2
    self.y = (frontBall.y + backBall.y) / 2
    self.angle = 0
  
  def updateCoordinates(self):
    self.x = (self.frontBall.x + self.backBall.x) / 2
    self.y = (self.frontBall.y + self.backBall.y) / 2

  def updateAngle(self):
    self.angle = math.atan2(self.frontBall.y - self.backBall.y, self.frontBall.x - self.backBall.x) * 180 / math.pi
    if(self.angle < 0):
      self.angle += 360

  def calculateAngle(self, ball):
    angleRobotBall = math.atan2(ball.y - self.y, ball.x - self.x) * 180 / math.pi
    
    if(angleRobotBall < 0):
      angleRobotBall += 360
    # print("Angulo robot-bola", angleRobotBall)
    angleBetween = angleRobotBall - self.angle
    return angleBetween

  def calculateDistance(self, ball):
    distance = math.sqrt(math.pow((self.x - ball.x)) + math.pow((self.y - ball.y)))
    return distance

def createBall(response):
  x = response[0][0]
  y = response[0][1]
  radius = response[1]
  color = response[2]
  return Ball(x, y, radius, color)

def classifyBall(ball, targetBalls, enemyBalls):
  if ball.color == targetBallColor:
    targetBalls.append(ball)
  elif ball.color == enemyBallColor:
    enemyBalls.append(ball)
  elif ball.color == myFrontColor:
    myRobot.frontBall = ball
  elif ball.color == myBackColor:
    myRobot.backBall = ball
  elif ball.color == enemyFrontColor:
    enemyRobot.frontBall = ball
  elif ball.color == enemyBackColor:
    enemyRobot.backBall = ball
  else:
    pass

def leftMotor(pwm, direction):
  # FKLMNA : F: encabezado; K: 0 motor izquierdo, 1 motor derecho; L: 0 hacia atras, 1 hacia adelante; MN % de PWM; A fin de la trama.
  # command = "F0xxxA"

  command = "F0"
  command += str(direction)
  command += str(int(pwm / 10))
  command += str(int(pwm % 10))
  command += 'A'
  serialPort.write(command.encode())

def rightMotor(pwm, direction):
  # FKLMNA : F: encabezado; K: 0 motor izquierdo, 1 motor derecho; L: 0 hacia atras, 1 hacia adelante; MN % de PWM; A fin de la trama.
  command = "F1"
  command += str(direction)
  command += str(int(pwm / 10))
  command += str(int(pwm % 10))
  command += 'A'
  serialPort.write(command.encode())

def stop():
  leftMotor(0, 1)
  rightMotor(0, 1)

def setMotors(leftPwm, rightPwm, leftDirection, rightDirection):
  leftMotor(leftPwm, leftDirection)
  rightMotor(rightPwm, rightDirection)

def loop(): 
  r = requests.get("http://" + ip_address + ":" + port)
  responses = r.json()
  targetBalls = []
  enemyBalls = []

  for response in responses:
    ball = createBall(response)
    classifyBall(ball, targetBalls, enemyBalls)

  myRobot.updateCoordinates()
  myRobot.updateAngle()

  # Calcular la bola mas cercana: nearestBall
  nearestBall = targetBalls[0]
  distance = myRobot.calculateDistance(nearestBall)
  differenceAngle = myRobot.calculateAngle(nearestBall) # Si el angulo es positivo hay que girar a la izquierda.
  print("Distancia:", distance)
  print("Diferencia de angulo:", differenceAngle)
  if(differenceAngle > 7.5):
    setMotors(25, 25, 0, 1)
  elif(differenceAngle < -7.5):
    setMotors(25, 25, 1, 0)
  else:
    setMotors(0, 0, 1, 1)
  serialPort.read(1)

myRobot = Robot(Ball(45, 45, 0, 0), Ball(0, 0, 0, 0))
ball = Ball(0, 90, None, None)

myRobot.updateCoordinates()
myRobot.updateAngle()
differenceAngle = myRobot.calculateAngle(ball) # Si el angulo es positivo hay que girar a la izquierda.

print(differenceAngle)

# while(1){
#   loop()
# }



























# asd = "F1111A"
# das = "X2341A"
# port.write(asd.encode())
# port.write(das.encode())
# data = port.read(6)
# print(data)
# data = port.read(6)
# print(data)


# balls = len(responses)
# print("Enviando")
# serialPort.write(str(balls).encode())
# print("Recibido:")
# data = serialPort.read(1)
# print(data)

# def test():
#   setMotors(30, 80, 0, 1)
#   # leftMotor(0, 1)
#   print("Esperando")
#   data = serialPort.read(6)
#   print(data)

# test()

# def testRobot():
#   myRobot.updateAngle()
#   print(myRobot.angle)

# testRobot()