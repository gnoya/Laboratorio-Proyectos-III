import numpy as np
import math
import sys

# Potencial.
celdas = 11
dim = 1.0
disceldas = dim/celdas
error = 0
vPre = 5 * np.ones((celdas,celdas))
vNow = 5 * np.ones((celdas,celdas))
columpos, filapos=[], []
limitError = 1
dicangle = [135, 112.5, 90, 67.5, 45, 137.5, 135, 90, 45, 22.5, 180, 180, 999, 0, 0, 202.5, 225, 270, 315, 337.5, 225, 247.5, 270, 292.5, 315]
targetBallPotential = 1000
enemyBallPotential = -200

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

def matrizPotencial(error,vPre,vNow, filapos, columpos):
  while error>limitError:
    for z in range(1,celdas-1):
      for j in range(1,celdas-1):
        if not checkBall(z,j, filapos, columpos):
          vNow[z][j]= round((vNow[z-1][j]+vNow[z+1][j]+vNow[z][j-1]+vNow[z][j+1])/4, 0)

    error=np.max(np.absolute(vNow)-np.absolute(vPre))
    vPre=np.copy(vNow)
  return None

def matrizPotencial2(error,vPre,vNow, filapos, columpos):
  while error>limitError:
    for z in range(1,celdas-1):
      for j in range(1,celdas-1):
        if not checkBall(z,j, filapos, columpos):
          vNow[z][j]=round((vNow[z-1][j] + vNow[z+1][j] + vNow[z][j-1] + vNow[z][j+1] + vNow[z+1][j+1] + vNow[z-1][j-1] + vNow[z+1][j-1] + vNow[z-1][j+1])/8, 0)

    error=np.max(np.absolute(vNow)-np.absolute(vPre))
    vPre=np.copy(vNow)
  return None

def getCell(disfila,discolum):
  celdacolum=(int)(discolum/disceldas)
  if(celdacolum >= 10):
      celdacolum=9
  celdafila=(celdas-1)-(int)(disfila/disceldas)
  return celdafila,celdacolum 


vPre = 5 * np.zeros((celdas, celdas))
vNow = 5 * np.zeros((celdas, celdas))
columpos, filapos = [], []
setBall(0.5, 0.5, targetBallPotential, vNow, filapos, columpos)
error = np.max(np.absolute(vNow) - np.absolute(vPre))
matrizPotencial(error, vPre, vNow, filapos, columpos)

print(vNow)

vPre = 5 * np.zeros((celdas, celdas))
vNow = 5 * np.zeros((celdas, celdas))
columpos, filapos = [], []
setBall(0.5, 0.5, targetBallPotential, vNow, filapos, columpos)
error = np.max(np.absolute(vNow) - np.absolute(vPre))
matrizPotencial2(error, vPre, vNow, filapos, columpos)
print("8 vecinos:")
print(vNow)