Stepper myStepper(stepsPerRevolution, 8, 9, 10, 11);

void setup() {
  myStepper.setSpeed(100);
  Serial.begin(9600);
}

void loop() {
  // 1 rotation clockwise: 
  Serial.println("clockwise");
  myStepper.step(stepsPerRevolution);
  delay(2000);

  // 1 rotation counterclockwise:
  Serial.println("counterclockwise");
  myStepper.step(-stepsPerRevolution);
  delay(2000);
}