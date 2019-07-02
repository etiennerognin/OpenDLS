
// This test code counts values and send them via serial port all in one go.
const unsigned int numReadings = 800;
unsigned int analogVals[numReadings];
long t, t0;

// Speed of the ADC
// defines for setting and clearing register bits
#ifndef cbi
#define cbi(sfr, bit) (_SFR_BYTE(sfr) &= ~_BV(bit))
#endif
#ifndef sbi
#define sbi(sfr, bit) (_SFR_BYTE(sfr) |= _BV(bit))
#endif

/*
// Temperature sensor
#include "TM1637.h"
#define CLK 10//pins definitions for TM1637 and can be changed to other ports
#define DIO 11
TM1637 tm1637(CLK,DIO);
*/


void setup() {
  Serial.begin(115200);

  // set prescale to 16
  cbi(ADCSRA, ADPS2) ; // cbi means clear bit
  sbi(ADCSRA, ADPS1) ; // sbi means set bit
  sbi(ADCSRA, ADPS0) ;

  // Display
  /*tm1637.init();
  tm1637.set(BRIGHT_TYPICAL);//BRIGHT_TYPICAL = 2,BRIGHT_DARKEST = 0,BRIGHTEST = 7;
  */
}

void loop() {
  // Read scattering values
  // ======================
  
  t0 = micros();
  
  // Construct the array
  for (int i=0; i < numReadings ; i++)
  {
    analogVals[i] = analogRead(A0);
  }
  t = micros()-t0;  // calculate elapsed time

  
  // Send to computer
  for (int i=0; i < numReadings ; i++)
  {
    Serial.print(analogVals[i]);
    Serial.print(',');
  }
  Serial.println(t);

  // Do other things
  // ===============
  /*tm1637.clearDisplay();
  int temperature = 20;
  tm1637.display(temperature);
  */
  
  delay(100);

}
