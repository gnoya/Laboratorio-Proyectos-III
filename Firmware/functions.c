#include "AS1.h"
#include "AS2.h"
#include "Cpu.h"
#include <string.h>

extern char redRange[10];
extern char greenRange[10];
extern char blueRange[10];
extern char TC[40];




void sendString(char string[]){
	int i;
	for(i = 0; i < strlen(string); i++){
		AS1_SendChar(string[i]);
		AS2_SendChar(string[i]);
	}
	AS1_SendChar(13); // \r.
	AS2_SendChar(13);
}

void initialize(){
	sendString("RS");
	strcat(TC, redRange);
	strcat(TC, greenRange);
	strcat(TC, blueRange);
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
	sendString(string);
}

void sendSerial(char ascii){
	AS1_SendChar(ascii);
	AS2_SendChar(ascii);
}

void delayMS(int ms){
	Cpu_Delay100US(10*ms);
}
