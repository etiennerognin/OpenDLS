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


void setup() {
  Serial.begin(115200);

  // set prescale to 16
  sbi(ADCSRA, ADPS2) ; // cbi means clear bit
  cbi(ADCSRA, ADPS1) ; // sbi means set bit
  cbi(ADCSRA, ADPS0) ;
}

void loop() {
  // Read scattering values
  // ======================

  //dummy = analogRead(A0); // this is because the first point is usually of bad quality
  
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
  
  delay(10);

}
