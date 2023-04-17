//libraries of modules
#include <Keypad.h>
#include <Stepper.h>

//Params of dc motor
#define STEPS 96
#define SPEED 100

//Motor configuration
Stepper stepper(STEPS, 14, 15, 16, 17);

//HSR04  module params
const int Trigger = 2;
const int Echo = 3;
double time;
double distance = 0.00;  //distance

//highs on centimeters
const double H1 = 10;  //15.53
const double H2 = 20;
const double H3 = 38;  //42.43
double errorPercentage = 2.0;


//Matricial keyboar configs
byte rows[4] = { 13, 12, 11, 10 };
byte columns[4] = { 9, 8, 7, 6 };
char opciones[4][4] = {
  { '1', '2', '3', 'A' },
  { '4', '5', '6', 'B' },
  { '7', '8', '9', 'C' },
  { '*', '0', '#', 'D' }
};
Keypad teclado = Keypad(makeKeymap(opciones), rows, columns, 4, 4);
char boton;

void setup() {
  //Config of serial port
  Serial.begin(9600);
  //HSR04 module pins
  pinMode(Trigger, OUTPUT);
  pinMode(Echo, INPUT);
  digitalWrite(Trigger, LOW);
  //Motor speed
  stepper.setSpeed(SPEED);
}

void loop() {
  //Calcular la distancia de la plataforma
  calcDistance();Serial.println(distance);
  //Obtener el valor del boton del teclado
  boton = teclado.getKey();
  //stepper.step(-12);
  switch (boton) {
    case '1':
      Serial.println(distance);
      to15Degrees(((distance < H1) ? 1 : -1));
      boton = " ";
      break;
    case '2':
      to25Degrees(((distance < H2) ? 1 : -1));
      boton = " ";
      break;
    case '3':
      to45Degrees(((distance < H3) ? 1 : -1));
      boton = " ";
      break;
  }
}

void calcDistance() {
  digitalWrite(Trigger, HIGH);
  delayMicroseconds(10);  //Enviamos un pulso de 10us
  digitalWrite(Trigger, LOW);

  time = pulseIn(Echo, HIGH);  //obtenemos el ancho del pulso (tiempo)
  distance = time / 59;        //Obtenemos distancia en cm
}

void to15Degrees(int dir) {  //dir = 1/-1 => rotate direction
  toDegrees(dir, H1);
}

void to25Degrees(int dir) {
  toDegrees(dir, H2);
}

void to45Degrees(int dir) {
  toDegrees(dir, H3);
}

//It is ok, but you are going to change from
//  sign, because if the current high is
//  	- more than the needed - izq (negative numbers-bajar)
//  	- less than needed - der (positive numbers-subir)
//  It will be applied to the multiplier of the motor

void toDegrees(int dir, double high) {  //dir = 1/-1
  calcDistance();
  if (dir == -1) {
    //Baja la plataforma
    Serial.println("Baja plataforma");
    Serial.println(high);
    while (!isWithinError(high, distance, errorPercentage)) {
      stepper.step(-12);
      calcDistance();
      Serial.println(distance);
      
    }
  } else {
    //Sube la platarforma
    Serial.println("Sube plataforma");
    Serial.println(high);
    while (!isWithinError(high, distance, errorPercentage)) {
      stepper.step(12);
      calcDistance();
      Serial.println(distance);
      
    }
  }
}

bool isWithinError(double val1, double val2, double errorPercentage) {
  double diff = fabs(val1 - val2);
  double avg = (fabs(val1) + fabs(val2)) / 2.0;
  double error = avg * (errorPercentage / 100.0);
  return diff <= error;
}