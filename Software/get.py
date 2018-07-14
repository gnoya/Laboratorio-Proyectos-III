import requests
import threading
import serial
import time
import numpy as np
import math
import sys

# Define the IP address and Port of the Server.

serialPort = serial.Serial('COM3', 9600, timeout=5)
ip_address = "127.0.0.1"
port = "8000"

myFrontColor = "BLACK"
myFrontColor2 = "CYAN"
myBackColor = "BLUE"
enemyFrontColor = 0
enemyBackColor = 0
targetBallColor = 'RED'
enemyBallColor = 'YELLOW'

# Potencial.
celdas = 12
dim = 1.0
disceldas = dim/celdas
error = 0
vPre = 5 * np.ones((celdas,celdas))
vNow = 5 * np.ones((celdas,celdas))
columpos, filapos=[], []
limitError = 1
dicangle = [135, 112.5, 90, 67.5, 45, 137.5, 135, 90, 45, 22.5, 180, 180, 999, 0, 0, 202.5, 225, 270, 315, 337.5, 225, 247.5, 270, 292.5, 315]
targetBallPotential = 4000
enemyBallPotential = -10

# Controladores.

# Rotacional
angleOffset = 5
lastRotationalError = 0
minRotatingPWM = 25
angleIntegrative = 0

# Lateral
forward = False
forwardMaxAngle = 25
longitudalPWM = 45
maxLongitudinalPD = 15
lastLongitudinalError = 0
longitudinalIntegrative = 0

targetDistance = 0.13
targetReached = False

goalX = 0.78
goalY = 0.5

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
    distance = math.sqrt(math.pow((self.x - ball.x), 2) + math.pow((self.y - ball.y), 2))
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
  elif ball.color == myFrontColor or ball.color == myFrontColor2:
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
  pwm *= 0.85
  command = "F0"
  command += str(direction)
  command += str(int(pwm / 10))
  command += str(int(pwm % 10))
  command += 'A'
  serialPort.write(command.encode())

def rightMotor(pwm, direction):
  # FKLMNA : F: encabezado; K: 0 motor izquierdo, 1 motor derecho; L: 0 hacia atras, 1 hacia adelante; MN % de PWM; A fin de la trama.
  pwm *= 1.10
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

def getCell(disfila,discolum):
  celdacolum=(int)(discolum/disceldas)
  if(celdacolum >= 10):
      celdacolum=9
  celdafila=(celdas-1)-(int)(disfila/disceldas)
  return celdafila,celdacolum 

def setBall(x,y,V, vNow, filapos, columpos):
  fila,colum=getCell(y,x)
  vNow[fila][colum]=V
  columpos.append(colum)
  filapos.append(fila)
  return None

def Indexes(value, array):
  return [i for (y,i) in zip (array, range(len(array))) if value==y]

def checkBall(fila,colum, filapos, columpos):
  A=Indexes(colum,columpos)
  for i in range(len(A)):
    if filapos[A[i]]==fila:
        return True
    else:
      return False

def matrizPotencial(error, vPre, vNow, filapos, columpos):
  while error>limitError:
    for z in range(1,celdas-2):
      for j in range(1,celdas-2):
        if not checkBall(z,j, filapos, columpos):
          vNow[z][j]=(vNow[z-1][j] + vNow[z+1][j] + vNow[z][j-1] + vNow[z][j+1] + vNow[z+1][j+1] + vNow[z-1][j-1] + vNow[z+1][j-1] + vNow[z-1][j+1])/8

    error=np.max(np.absolute(vNow)-np.absolute(vPre))
    vPre=np.copy(vNow)
  return None

def getAngle(matriz,xcar,ycar,anglecar):
  filacar,columcar=getCell(ycar,xcar)
  #print(filacar, columcar)
  aux=matriz[filacar-2:filacar+3,columcar-2:columcar+3]
  
  print(aux)
  # if(np.argmax(aux) == 5):
  dif = dicangle[np.argmax(aux)]-anglecar

  if dif > 180:
    dif -= 360
  elif dif < -180:
    dif += 360
  return dif

def rotationalPDController(error, lastError, integrativeError):
  Kp = 0.15
  Kd = 0.5
  Ki = 0
  integrativeError += lastError
  direction = True
  if error < 0: 
    direction = False
  return Kp * error + Kd * (error - lastError) + Ki * integrativeError, direction

def longitudinalPDController(error, lastError, integrativeError):
  Kp = 0.93
  Kd = 1
  Ki = 0
  integrativeError += lastError
  return Kp * error + Kd * (error - lastError) + Ki * integrativeError

def loop(): 
  global forward
  global lastRotationalError
  global angleIntegrative
  global lastLongitudinalError
  global targetDistance
  global targetReached

  r = requests.get("http://" + ip_address + ":" + port)
  responses = r.json()
  targetBalls = []
  enemyBalls = []

  for response in responses:
    ball = createBall(response)
    classifyBall(ball, targetBalls, enemyBalls)

  myRobot.updateCoordinates()
  myRobot.updateAngle()

  if(len(targetBalls) > 0 or len(enemyBallColor) > 0):
    # Calcular la bola mas cercana: nearestBall

    # Potencial
    vPre = 5 * np.ones((celdas, celdas))
    vNow = 5 * np.ones((celdas, celdas))
    columpos, filapos = [], []

    for ball in enemyBalls:
      setBall(ball.x, ball.y, enemyBallPotential, vNow, filapos, columpos)
      setBall(ball.x + disceldas, ball.y, enemyBallPotential, vNow, filapos, columpos)
      setBall(ball.x, ball.y + disceldas, enemyBallPotential, vNow, filapos, columpos)
      setBall(ball.x - disceldas, ball.y, enemyBallPotential, vNow, filapos, columpos)
      setBall(ball.x, ball.y - disceldas, enemyBallPotential, vNow, filapos, columpos)

      # setBall(ball.x + 2*disceldas, ball.y, enemyBallPotential, vNow, filapos, columpos)
      # setBall(ball.x, ball.y + 2*disceldas, enemyBallPotential, vNow, filapos, columpos)
      # setBall(ball.x - 2*disceldas, ball.y, enemyBallPotential, vNow, filapos, columpos)
      # setBall(ball.x, ball.y - 2*disceldas, enemyBallPotential, vNow, filapos, columpos)

    distances = []

    for ball in targetBalls:
      temporalDistance = myRobot.calculateDistance(ball)
      if(temporalDistance > 0.075):
        distances.append(temporalDistance)

    nearest = np.argmin(distances)
    nearestBall = targetBalls[nearest]
    setBall(nearestBall.x, nearestBall.y, targetBallPotential, vNow, filapos, columpos)
    print("Going to:", nearestBall.x, nearestBall.y)
    print(" ")
    error = np.max(np.absolute(vNow) - np.absolute(vPre))
    matrizPotencial(error, vPre, vNow, filapos, columpos)
    
    for ball in enemyBalls:
      row, column = getCell(ball.y, ball.x)
      # for i in range(1, 3):7
      i = 1
      vNow[row - i, column - i] = enemyBallPotential
      vNow[row - i, column] = enemyBallPotential
      vNow[row - i, column + i] = enemyBallPotential
      vNow[row, column - i] = enemyBallPotential
      vNow[row, column + i] = enemyBallPotential
      vNow[row + i, column - i] = enemyBallPotential
      vNow[row + i, column] = enemyBallPotential
      vNow[row + i, column + i] = enemyBallPotential

    # row, column = getCell(nearestBall.y, nearestBall.x)
    # vNow[row, column] = targetBallPotential
    # Controladores.

    #print("OMW")
    #print(vNow, myRobot.x, myRobot.y, myRobot.angle)
    angleError = getAngle(vNow, myRobot.x, myRobot.y, myRobot.angle)
    if(len(targetBalls) > 0):
      #nearestBall = targetBalls[0]
      if(myRobot.calculateDistance(nearestBall) <= targetDistance):
        targetReached = True     

    if(abs(angleError) < angleOffset):
      forward = True

    if((not forward) and (not targetReached)):
      PD, direction = rotationalPDController(angleError, lastRotationalError, angleIntegrative)
      # Se toma el valor absoluto para tomar en cuenta los ángulos negativos.
      PD = abs(PD)
      if(PD > minRotatingPWM):
        PD = minRotatingPWM
      PWM = minRotatingPWM + PD
      setMotors(PWM, PWM, int(not direction), int(direction)) # direction: 1 antihorario. 0 horario.
      lastRotationalError = angleError
      serialPort.read(2)
    elif(not targetReached):
      if(abs(angleError) > forwardMaxAngle):
        forward = False
      PD = longitudinalPDController(angleError, lastLongitudinalError, longitudinalIntegrative)
      PD = abs(PD)
      if(PD > maxLongitudinalPD):
        PD = maxLongitudinalPD
      if(angleError >= 0):
        setMotors(longitudalPWM, longitudalPWM + PD, 1, 1)
      else:
        setMotors(longitudalPWM + PD, longitudalPWM, 1, 1)
      lastLongitudinalError = angleError
      serialPort.read(2)
    else:
      stop()
      serialPort.read(2)
      

def comeback():
  global forward
  global lastRotationalError
  global angleIntegrative
  global lastLongitudinalError
  global targetDistance
  global targetReached

  r = requests.get("http://" + ip_address + ":" + port)
  responses = r.json()
  targetBalls = []
  enemyBalls = []
  for response in responses:
    ball = createBall(response)
    classifyBall(ball, targetBalls, enemyBalls)

  myRobot.updateCoordinates()
  myRobot.updateAngle()

  vPre = 5 * np.ones((celdas, celdas))
  vNow = 5 * np.ones((celdas, celdas))
  columpos, filapos = [], []

  setBall(goal.x, goal.y, targetBallPotential, vNow, filapos, columpos)

  error = np.max(np.absolute(vNow) - np.absolute(vPre))
  matrizPotencial(error, vPre, vNow, filapos, columpos)

  for ball in enemyBalls:
    row, column = getCell(ball.y, ball.x)
    i = 1
    vNow[row - i, column - i] = enemyBallPotential
    vNow[row - i, column] = enemyBallPotential
    vNow[row - i, column + i] = enemyBallPotential
    vNow[row, column - i] = enemyBallPotential
    vNow[row, column + i] = enemyBallPotential
    vNow[row + i, column - i] = enemyBallPotential
    vNow[row + i, column] = enemyBallPotential
    vNow[row + i, column + i] = enemyBallPotential

  print("Volviendo")
  angleError = getAngle(vNow, myRobot.x, myRobot.y, myRobot.angle)

  if(abs(angleError) < angleOffset):
    forward = True

  if(myRobot.calculateDistance(goal) < targetDistance):
    pass
    #xD
  
  if(not forward):
    PD, direction = rotationalPDController(angleError, lastRotationalError, angleIntegrative)
    # Se toma el valor absoluto para tomar en cuenta los ángulos negativos.
    PD = abs(PD)
    if(PD > minRotatingPWM):
      PD = minRotatingPWM
    PWM = minRotatingPWM + PD
    setMotors(PWM, PWM, int(not direction), int(direction)) # direction: 1 antihorario. 0 horario.
    lastRotationalError = angleError
    serialPort.read(2)
  else:
    if(abs(angleError) > forwardMaxAngle):
      forward = False
    PD = longitudinalPDController(angleError, lastLongitudinalError, longitudinalIntegrative)
    PD = abs(PD)
    if(PD > maxLongitudinalPD):
      PD = maxLongitudinalPD
    if(angleError >= 0):
      setMotors(longitudalPWM, longitudalPWM + PD, 1, 1)
    else:
      setMotors(longitudalPWM + PD, longitudalPWM, 1, 1)
    lastLongitudinalError = angleError
    serialPort.read(2)

myRobot = Robot(Ball(45, 45, 0, 0), Ball(0, 0, 0, 0))
goal = Ball(goalX, goalY, None, None)

while(1):
  try:
    if(not targetReached):
      loop()
    else:
      comeback()
      # setMotors(30, 60, 1, 1)
      # serialPort.read(2)
  except KeyboardInterrupt:
    stop()
    print("Detener")
    sys.exit()
  except:
    stop()




# def test():
#   setMotors(40, 40, 1, 1)
#   # leftMotor(0, 1)
#   print("Esperando")
#   data = serialPort.read(1)
#   print(data)

# test()



