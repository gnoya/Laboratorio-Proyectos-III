#include "AS1.h"
#include "AS2.h"
#include "Cpu.h"
#include <string.h>

// Declaraci�n de variables.

// Mantener los espacios al principio del string.
char redRange[10] = " 0 100";
char greenRange[10] = " 180 255";
char blueRange[10] = " 0 100";
char TC[40] = "TC";


// Declaraci�n de funciones.
void sendString(char string[], int choice);
void initialize();
int intToAscii(int number);
void sendBigNumber(int number);
void readLine(char *line[]);
void delayMS(int ms);
