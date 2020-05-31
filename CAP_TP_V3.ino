//this code was created bye ENSEM students
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x3F,20,4);
int capt_temp = 1  ; // lm35 relié au port A1 
int capt_pression = 2 ; //caapteur de pression relié à A2
int capt_debit = 3 ; //capteur de débit relié à A3

void setup() {
 Serial.begin(9600);
 lcd.init();
 pinMode(capt_temp,INPUT);
 pinMode(capt_pression,INPUT);
 pinMode(capt_debit,INPUT);
 
}

void loop() {
// put your main code here, to run repeatedly:
int val_temp = analogRead(capt_temp); //lecture de la temperature
int val_press = analogRead(capt_pression);//lecture de la pression
int val_debit = analogRead(capt_debit);//lecture du débit 
float temp = val_temp*(5.0/1023.0)/0.1;//Vout=10mV/°C
float pression = val_press*(5.0/1023.0);
float debit = val_debit*(5.0/1023.0);
senddata(temp,pression,debit);
lcd.backlight();
lcd.setCursor(0,0);
lcd.print("Temperature =");
//float t=(temp)/0.1;
lcd.setCursor(10,1);
lcd.print(temp);
delay(1999);

}
void senddata(float TEMP,float PRES,float debit){
  Serial.println(String(TEMP)+" "+String(PRES)+" "+String(debit));
}
