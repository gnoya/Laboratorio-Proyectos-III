#include "AS1.h"
#include "AS2.h"
#include "Cpu.h"
#include "Bit1.h"
#include "Bit2.h"
#include "PWM1.h"
#include "PWM2.h"
#include <string.h>
#include <Math.h>

extern char redRange[10];
extern char greenRange[10];
extern char blueRange[10];
extern char TC[40];

int motor;
int direction;
int pwm;
	
void delayMS(int ms){
	Cpu_Delay100US(10*ms);
}

void sendString(char string[], int choice){
	int i;
	//char carry = 0x0D;
	//string[5] = (char) 13;
	
	for(i = 0; i < strlen(string); i++){
		if(choice == 1){
		  AS1_SendChar(string[i]);
		}
		else if (choice == 2){
		  AS2_SendChar(string[i]);
		}
		else{
		  AS1_SendChar(string[i]);
		  AS2_SendChar(string[i]);
		}
	}
	
	delayMS(20);
	if(choice == 1){
		AS1_SendChar(13); // \r.
	}
	else if(choice == 2){
		AS2_SendChar(13); // \r.
	}
	else if(choice == 3){
		AS1_SendChar(13); // \r.
		AS2_SendChar(13); // \r.
	}
	else{
	}
}

void sendString2(char string[], int choice){
	int i;
	//char carry = 0x0D;
	//string[5] = (char) 13;
	
	for(i = 0; i < strlen(string); i++){
		if(choice == 1){
		  AS1_SendChar(string[i]);
		}
		else if (choice == 2){
		  AS2_SendChar(string[i]);
		}
		else{
		  AS1_SendChar(string[i]);
		  AS2_SendChar(string[i]);
		}
	}
	//AS2_SendChar(13); // \r.
}

int asciiToInt(char ascii){
	return ascii - '0';
}

void getCoordinates(char line[], int *x, int *y){
	int i = 0;
	int j = 2;
	*x = 0;
	*y = 0;
	
	while(line[j] != ' '){
		j++;
	}
	j--;
	
	i = j;
	while(line[i] != ' '){
		*x += asciiToInt(line[i]) * pow(10, j - i);
		i--;
	}
	
	
	j += 2;
	
	while(line[j] != ' '){
		j++;
	}
	j--;
	
	i = j;
	while(line[i] != ' '){
		*y += asciiToInt(line[i]) * pow(10, j - i);
		i--;
	}
}


int intToAscii(int number){
	unsigned char ascii = number + '0';
	return ascii;
}

void sendBigNumber(int number){
	int i;
	int L;
	int digit;
	int digits[40] = {0};
	char string[40];
	i = 0;
	while (number > 0) {
		digit = number % 10;
		digits[i] = digit;
		number = number / 10;
		i++;
	}
	L = i;
	
	for(i = 0; i < L; i++){
		string[L - i - 1] = intToAscii(digits[i]);
	}
	sendString(string, 2);
}

void sendSerial(char ascii){
	AS1_SendChar(ascii);
	AS2_SendChar(ascii);
}

void readLine(char line[]){
  unsigned char charact;
  int i = 0;
  int carryReturn = 13;

  for(i = 0; i < 50; i++){
	  line[i] = 0;
  }
  i = 0;
  
  while(1){
	//AS2_SendChar('w');
    if(AS1_RecvChar(&charact) != ERR_RXEMPTY){
      if((int)charact == carryReturn) {
    	  AS2_SendChar(charact);
    	  break;
      }
      AS2_SendChar(charact);
      line[i] = charact;
      i++;
      //AS2_SendChar(charact);
    }
  }
}

void readLine2(char line[]){
  unsigned char charact;
  int i = 0;

  for(i = 0; i < 50; i++){
	  line[i] = 0;
  }
  i = 0;
  
  while(1){
    if(AS2_RecvChar(&charact) != ERR_RXEMPTY){
      if((int)charact == 65) { // A
    	  line[i] = charact;
    	  break;
      }
      line[i] = charact;
      i++;
    }
  }
}

void initialize(char line[]){
	// Asi se hace el reset.
	AS1_ClearRxBuf();
	AS1_SendChar(13); // \r.
	sendString("RS", 3);
	delayMS(100);
	
	//AS1_ClearRxBuf();
	strcat(TC, redRange);
	strcat(TC, greenRange);
	strcat(TC, blueRange);
}

void getMassCenter(char line[]){
  AS1_ClearRxBuf();
  sendString(TC, 3);
  //readLine(line); // ACK
  //readLine(line); // Paquete M.
  delayMS(100);
  AS1_SendChar(13); // Detenemos el envio de la camara
  //readLine(line); // :
}




// Definicion
void setRightPWM(unsigned short porcentaje, bool dir){
	unsigned short parametro;
	parametro = 65535*(porcentaje)/100;
	PWM1_SetRatio16(parametro);
	Bit1_PutVal(dir);
}

void setLeftPWM(unsigned short porcentaje, bool dir){
	unsigned short parametro;
	parametro = (65535*(porcentaje)/100);
	PWM2_SetRatio16(parametro);
	Bit2_PutVal(dir);
}
void Set_PWM(unsigned short porcentaje1, unsigned short porcentaje2, bool dir1, bool dir2){
	
	if(dir1){
		setRightPWM(100 - porcentaje1, dir1);
	} 
	else{
		setRightPWM(porcentaje1, dir1);
	}
	
	if(dir2){
		setLeftPWM(100 - porcentaje2, dir2);
	}
	else{
		setLeftPWM(porcentaje2, dir2);
	}
	
}

void setPWM(unsigned short leftPWM, unsigned short rightPWM, unsigned short leftDir, unsigned short rightDir){
	if(leftDir == 1){
		setLeftPWM(leftPWM, 0);
	} else {
		setLeftPWM(100 - leftPWM, 1);
	}
	
	if(rightDir == 1){
		setRightPWM(rightPWM, 0);
	} else {
		setRightPWM(100 - rightPWM, 1);
	}
}

int getMotorData(char line[], unsigned short *leftPWM, unsigned short *rightPWM, unsigned short *leftDir, unsigned short *rightDir){
	if((int)line[0] != 70) return 0;
	
	motor = asciiToInt(line[1]);
	direction = asciiToInt(line[2]);
	pwm = asciiToInt(line[3])*10 + asciiToInt(line[4]);
	
	if(motor == 0){
		*leftDir = direction;
		*leftPWM = pwm;
	}
	else if (motor == 1){
		*rightDir = direction;
		*rightPWM = pwm;
	}
	return 1;
}
