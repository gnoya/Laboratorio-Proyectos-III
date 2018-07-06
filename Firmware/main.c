/* ###################################################################
**     Filename    : main.c
**     Project     : Proyectos3
**     Processor   : MCF51QE128CLK
**     Version     : Driver 01.00
**     Compiler    : CodeWarrior ColdFireV1 C Compiler
**     Date/Time   : 2018-04-30, 17:58, # CodeGen: 0
**     Abstract    :
**         Main module.
**         This module contains user's application code.
**     Settings    :
**     Contents    :
**         No public methods
**
** ###################################################################*/
/*!
** @file main.c
** @version 01.00
** @brief
**         Main module.
**         This module contains user's application code.
*/         
/*!
**  @addtogroup main_module main module documentation
**  @{
*/         
/* MODULE main */


/* Including needed modules to compile this module/procedure */
#include "Cpu.h"
#include "Events.h"
#include "AS1.h"
#include "AS2.h"
#include "AD1.h"
#include "Bit1.h"
#include "Bit2.h"
#include "PWM1.h"
#include "PWM2.h"
#include <string.h>
/* Include shared modules, which are used for whole project */
#include "PE_Types.h"
#include "PE_Error.h"
#include "PE_Const.h"
#include "IO_Map.h"
#include "functions.h"

/* User includes (#include below this line is not maintained by Processor Expert) */
int estado = 1;
unsigned char character;
char line[50] = {0};
int x = 0;
int y = 0;
unsigned int lastX = 0;

unsigned short distance = 0;
unsigned short rightPWM = 0;
unsigned short leftPWM = 0;
unsigned short leftDirection = 1;
unsigned short rightDirection = 1;
void main(void){
/* Write your local variable definition here */

/*** Processor Expert internal initialization. DON'T REMOVE THIS CODE!!! ***/
PE_low_level_init();
/*** End of Processor Expert internal initialization.                    ***/

/* Write your code here */
/* For example: for(;;) { } */
/***********************************************************
 * */
//AD1_Start();
//initialize(line);
//delayMS(1000);
//sendString(TC, 3);
//sendString("GM",3);

while(1){
	
	if (AS2_GetCharsInRxBuf() > 0){
		readLine2(line);
		//sendString2(line, 2);
		getMotorData(line, &leftPWM, &rightPWM, &leftDirection, &rightDirection);
		setPWM(leftPWM, rightPWM, leftDirection, rightDirection);
		AS2_SendChar('A');
		
	}
}






  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  /*** Don't write any code pass this line, or it will be deleted during code generation. ***/
  /*** Processor Expert end of main routine. DON'T MODIFY THIS CODE!!! ***/
  for(;;){}
  /*** Processor Expert end of main routine. DON'T WRITE CODE BELOW!!! ***/
} /*** End of main routine. DO NOT MODIFY THIS TEXT!!! ***/

/* END main */
/*!
** @}
*/
/*
** ###################################################################
**
**     This file was created by Processor Expert 10.3 [05.09]
**     for the Freescale ColdFireV1 series of microcontrollers.
**
** ###################################################################
*/
