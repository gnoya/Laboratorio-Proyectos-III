#include "AS1.h"
#include "AS2.h"
#include "Cpu.h"
#include "Bit1.h"
#include "Bit2.h"
#include "PWM1.h"
#include "PWM2.h"
#include <string.h>

// Declaraci�n de variables.

// Mantener los espacios al principio del string.
char redRange[10] = " 138 160";
char greenRange[10] = " 12 30";
char blueRange[10] = " 16 43";
char TC[40] = "TC";


// Declaraci�n de funciones.
void sendString(char string[], int choice);
void sendString2(char string[], int choice);
void initialize(char line[]);
int intToAscii(int number);
void sendBigNumber(int number);
void readLine(char line[]);
void readLine2(char line[]);
void delayMS(int ms);
void getMassCenter(char line[]);
void getCoordinates(char line[], int *x, int *y);
int asciiToInt(char ascii);
void setRightPWM(unsigned short porcentaje, bool dir);
void setLeftPWM(unsigned short porcentaje, bool dir);
void Set_PWM(unsigned short porcentaje1, unsigned short porcentaje2, bool dir1, bool dir2);
void setPWM(unsigned short leftPWM, unsigned short rightPWM, unsigned short leftDir, unsigned short rightDir);
int getMotorData(char line[], unsigned short *leftPWM, unsigned short *rightPWM, unsigned short *leftDir, unsigned short *rightDir);
