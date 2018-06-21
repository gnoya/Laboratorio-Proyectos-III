import requests
import threading
import serial
import time
import numpy as np
import math

# Define the IP address and Port of the Server.

serialPort = serial.Serial('COM3', 9600)
ip_address = "127.0.0.1"
port = "8000"
loopTime = 2 # Intervalo de loop en segundos.

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
    self.x = (frontBall.x + backBall.x ) / 2
    self.y = (frontBall.y + backBall.y ) / 2
    self.angle = 0
  
  def updateAngle(self):
    self.angle = math.atan(frontBall.y - backBall.y, frontBall.x - backBall.x) * 180 / math.pi

  def calculateAngle(self, ball):
    angleCenterBall = math.atan(ball.y - self.y, ball.x - self.x)
    angleBetween = angleFromOrigin - self.angle
    return angleBetween * 180 / math.pi


def createBall(response):
  x = response[0][0]
  y = response[0][1]
  radius = response[1]
  color = response[2]
  return Ball(x, y, radius, color)

def classifyBall(ball):
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
  command = "F0xxxA"
  command[2] = str(direction)
  command[3] = str(int(pwm / 10))
  commnad[4] = str(int(pwm % 10))
  serialPort.write(command.encode())

def rightMotor(pwm, direction):
  # FKLMNA : F: encabezado; K: 0 motor izquierdo, 1 motor derecho; L: 0 hacia atras, 1 hacia adelante; MN % de PWM; A fin de la trama.
  command = "F1xxxA"
  command[2] = str(direction)
  command[3] = str(int(pwm / 10))
  commnad[4] = str(int(pwm % 10))
  serialPort.write(command.encode())

def stop():
  leftMotor(0, 0)
  rightMotor(0, 0)

def setMotors(leftPwm, rightPwm, leftDirection, rightDirection):
  leftMotor(leftPwm, leftDirection)
  rightMotor(rightPwm, rightDirection)

def loop(): 
  threading.Timer(loopTime, loop).start()
  r = requests.get("http://" + ip_address + ":" + port)
  responses = r.json()

  targetBalls = []
  enemyBalls = []

  for response in responses:
    ball = createBall(response)
    classifyBall(ball)
  
  myRobot.updateAngle()
  # Calcular la bola mas cercana: nearestBall
  nearestBall = targetBalls[0]
  differenceAngle = myRobot.calculateAngle(nearestBall) # Si el angulo es positivo hay que girar a la izquierda.
  if(differenceAngle > 5):
    setMotors(35, 65, 1, 1)
  elif(differenceAngle < 5):
    setMotors(65, 35, 1, 1)
  else:
    setMotors(60, 60, 1, 1)



loop()












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