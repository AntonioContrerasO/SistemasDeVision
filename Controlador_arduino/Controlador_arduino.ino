#include <Arduino.h>
#include <Servo.h>

const int pinHallSensor = 12; // Conecta la salida del sensor Hall a este pin digital
const int pinIRSensor = 13; // Conecta la salida del sensor IR a este pin digital
const int pinLED = LED_BUILTIN; // Usar el LED incorporado en la placa
const int pinMotor = 8; // Conectar la entrada del Driver del Motor Central a este Pin digital

int pinServo1 = 3;
int pinServo2 = 5;
int pinServo3 = 6;
int pinServo4 = 9;
int pinServo5 = 10;

// Angulos Iniciales
float ANGULO1 = 90; // De 0 a 180
float ANGULO2 = 80; // De 50 a 180
float ANGULO3 = 160; // De 0 a 180
float ANGULO4 = 90; // De 0 a 180
float ANGULO5 = 180; // De 70 a 180

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;

bool waitForObject = false;

void setup() {
  Serial.begin(9600); // Inicia la comunicación serie

  // TIMSK0 = 0;
  
  pinMode(pinHallSensor, INPUT); // Configura el pin del sensor Hall como entrada
  pinMode(pinIRSensor, INPUT); // Configura el pin del sensor IR como entrada
  pinMode(pinLED, OUTPUT); // Configura el pin del LED como salida
  pinMode(pinMotor, OUTPUT); // Configura el pin del motor como salida

  servo1.attach(pinServo1);
  servo2.attach(pinServo2);
  servo3.attach(pinServo3);
  servo4.attach(pinServo4);
  servo5.attach(pinServo5);

  posicion_home();
}

void loop() {
  
  if (Serial.available()) {
    String inputString = Serial.readStringUntil('\n'); // Lee la cadena hasta encontrar un salto de línea
    if (inputString == "Motor_ON") {
      // Serial.println("Turning_Motor_ON");
      digitalWrite(pinMotor, HIGH);
      digitalWrite(pinLED, LOW);
      //motorONState = true;
      delay(1500); // Esperar a que se aleje el Iman
    }
    if (inputString == "Wait_for_Object") {
      waitForObject = true;
      Serial.println("INICIADO");
    }
    if (inputString == "ETIQUETADO") {
      delay(5000);
      Serial.println("LISTO");
    }
    if (inputString == "Recoger"){
      posicion_recoger();
    } 
    if (inputString == "Home") {
      Serial.println("Posicionando en Home");
      posicion_home();
    }
    if (inputString == "Bueno1") { // Comando brazo robot para aprobado
      Serial.println("Classificando como bueno 1");
      secuencia_bueno(1);
    }
    if (inputString == "Bueno2") { // Comando brazo robot para aprobado
      Serial.println("Classificando como bueno 2");
      secuencia_bueno(2);
    }
    if (inputString == "Malo1") { // Comando brazo robot para no aprobdo
    Serial.println("Classificando como malo 2");
      secuencia_malo(1);
    }
    if (inputString == "Malo2") { // Comando brazo robot para no aprobdo
    Serial.println("Classificando como malo 2");
      secuencia_malo(2);
    }
    
    int a = inputString.toInt();
    posicion_manual(a);
  }

  int sensorIRValue = digitalRead(pinIRSensor); // Lee el valor digital del sensor
  if (sensorIRValue == LOW & waitForObject == true) {
    delay(2000);
    Serial.println("Object_IR");
    waitForObject = false;
  }


  int sensorHallValue = digitalRead(pinHallSensor); // Lee el valor digital del sensor
  if (sensorHallValue == LOW & digitalRead(pinMotor) == HIGH) {
    digitalWrite(pinLED, HIGH);
    digitalWrite(pinMotor, LOW);
    Serial.println("Magnet_Hall_Motor_OFF");
  }

  delay(50); // Espera medio segundo antes de leer nuevamente
}

void posicion_home(void){
  write_slowly(servo1, ANGULO1);
  delay(300);
  write_slowly(servo2, ANGULO2);
  delay(300);
  write_slowly(servo3, ANGULO3);
  delay(300);
  write_slowly(servo4, ANGULO4);
  delay(300);
  write_slowly(servo5, ANGULO5);
}

void posicion_recoger(void){
  write_slowly(servo3, 160);
  delay(100);
  write_slowly(servo1, 180);
  delay(100);
  write_slowly(servo4,65);
  delay(100);
  write_slowly(servo3, 70);
  delay(300);
}

void posicion_bueno1(void){
  write_slowly(servo3, 120);
  delay(100);
  write_slowly(servo4, 90);
  delay(100);
  write_slowly(servo1, 60);
  delay(100);
  servo2.write(80);
  write_slowly(servo3, 92);
  delay(100);
}

void posicion_bueno2(void){
  write_slowly(servo3, 120);
  delay(100);
  write_slowly(servo4, 90);
  delay(100);
  write_slowly(servo1, 33);
  delay(100);
  servo2.write(80);
  write_slowly(servo3, 92);
  delay(100);
}

void posicion_malo1(void){
  write_slowly(servo3, 120);
  delay(100);
  write_slowly(servo4, 90);
  delay(100);
  write_slowly(servo1, 105);
  delay(100);
  servo2.write(80);
  write_slowly(servo3, 92);
  delay(100);
}

void posicion_malo2(void){
  write_slowly(servo3, 120);
  delay(100);
  write_slowly(servo4, 90);
  delay(100);
  write_slowly(servo1, 85);
  delay(100);
  servo2.write(80);
  write_slowly(servo3, 92);
  delay(100);
}


void write_slowly(Servo servo, int angulo){
  int actual = servo.read();

  if(actual > angulo){ // Si angulo menor
    for(int i = actual; i >= angulo; i--){
      delay(20);
      servo.write(i);
    }
  } else { // Si angulo mayor
    for(int i = servo.read(); i <= angulo; i++){
      delay(10);
      servo.write(i);
    }
  }
}

void secuencia_bueno(int num){
  posicion_home();
  posicion_recoger();
  cerrar_garra();
  if(num == 1){
  posicion_bueno1();
  } 
  if(num == 2){
    posicion_bueno2();
  }
  abrir_garra();
  write_slowly(servo3, ANGULO3);
  delay(300);
  posicion_home();
}

void secuencia_malo(int num){
  posicion_home();
  posicion_recoger();
  cerrar_garra();
    if(num == 1){
  posicion_malo1();
  } 
  if(num == 2){
    posicion_malo2();
  }
  abrir_garra();
  write_slowly(servo3, ANGULO3);
  delay(300);
  posicion_home();
}

void abrir_garra(){
  delay(150);
  servo5.write(180);
  delay(150);
}

void cerrar_garra(){
  delay(150);
  servo5.write(140);
  delay(150);
}

void posicion_manual(int a){
 if(a>=1000 && a<=1180)
  { 
    servo1.write(a-1000);
    Serial.print("Posicion de S1 establecida en: ");
    Serial.println(int(a-1000));
  }
  else if(a>=2050 && a<=2180)
  {
    servo2.write(a-2000);
    Serial.print("Posicion de S2 establecida en: ");
    Serial.println(int(a-2000));
  }
  else if(a>=3000 && a<=3180)
  {
    servo3.write(a-3000);
    Serial.print("Posicion de S3 establecida en: ");
    Serial.println(int(a-3000));
  }
  else if(a>=4000 && a<=4180)
  {
    servo4.write(a-4000);
    Serial.print("Posicion de S4 establecida en: ");
    Serial.println(int(a-4000));
  }
  else if(a>=5000 && a<=5180)
  {
    servo5.write(a-5000);
    Serial.print("Posicion de S5 establecida en: ");
    Serial.println(int(a-5000));
  }
}