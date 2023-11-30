const int pinHallSensor = 2; // Conecta la salida del sensor Hall a este pin digital
const int pinIRSensor = 3; // Conecta la salida del sensor IR a este pin digital
const int pinLED = LED_BUILTIN; // Usar el LED incorporado en la placa
const int pinMotor = 8; // Conectar la entrada del Driver del Motor Central a este Pin digital

bool waitForObject = false;

void setup() {
  Serial.begin(9600); // Inicia la comunicación serie
  pinMode(pinHallSensor, INPUT); // Configura el pin del sensor Hall como entrada
  pinMode(pinIRSensor, INPUT); // Configura el pin del sensor IR como entrada
  pinMode(pinLED, OUTPUT); // Configura el pin del LED como salida
  pinMode(pinMotor, OUTPUT); // Configura el pin del motor como salida
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
    if (inputString == "CLASIFICADOR") {
      delay(5000);
      Serial.println("LISTO");
    }
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