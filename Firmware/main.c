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
unsigned short PWM1 = 50;
unsigned short PWM2 = 50;

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
  initialize(line);
  delayMS(1000);
  sendString(TC, 3);
  
  while(1){
	/*
	  if (AS1_GetCharsInRxBuf() > 0){
	  AS1_RecvChar(&character);
	  AS2_SendChar(character);
	}
	*/
	  
	  AS1_ClearRxBuf();
		readLine(line);
		getCoordinates(line, &x, &y);
		sendString(line, 2);

		  AD1_Measure(TRUE);
		  AD1_GetValue16(&distance);
		  distance = distance >> 4;
	
		  if(x == 0){
			  if(lastX < 40){
				  Set_PWM(25, 25, 1, 0);
			  }
			  else{
				  Set_PWM(25, 35, 0, 1);
			  }
		  }
		  else{
			  if(x > 0 && x <= 80){
				  lastX = x;
			  }
			  
			  if(distance < 1100){	
				  if(x > 43){
					  Set_PWM(PWM1 * 1.45, PWM2 , 0, 0);
				  }
				  else if(x < 37){
					  // PWM1 : derecho rojo
					  // PWM2 : izquierdo verde
					  Set_PWM(PWM1, PWM2 * 1.45 , 0, 0);
				  }
				  else {
					  Set_PWM(PWM1, PWM2 , 0, 0);
				  }  
			  }
			  else if (distance > 1100 && distance < 1400){
				  Set_PWM(0, 0 , 0, 0);
			  }
			  else{
				Set_PWM(PWM1, PWM2 , 1, 1);
			  }
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
