/*Example sketch to control a stepper motor with A4988 stepper motor driver and Arduino without a library. More info: https://www.makerguides.com */

// Define stepper motor connections and steps per revolution:
#define dirPin 2
#define stepPin 3
#define dirPin1 4
#define stepPin1 5
#define stepsPerRevolution 100

void setup() {
  // Declare pins as output:
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(stepPin1, OUTPUT);
  pinMode(dirPin1, OUTPUT);
}

void loop() {


  // Set the spinning direction counterclockwise:
  digitalWrite(dirPin, HIGH);
  digitalWrite(dirPin1, HIGH);

  //Spin the stepper motor 5 revolutions fast:
  for (int i = 0; i < 5 * stepsPerRevolution; i++) {
    // These four lines result in 1 step:
    digitalWrite(stepPin, HIGH);
    digitalWrite(stepPin1, HIGH);
    delayMicroseconds(2000);
    digitalWrite(stepPin, LOW);
    digitalWrite(stepPin1, LOW);
    delayMicroseconds(2000);
  }
  delay(1000);

  //   // Set the spinning direction counterclockwise:
  // digitalWrite(dirPin, LOW);
  // digitalWrite(dirPin1, LOW);


  // //Spin the stepper motor 5 revolutions fast:
  // for (int i = 0; i < 5 * stepsPerRevolution; i++) {
  //   // These four lines result in 1 step:
  //   digitalWrite(stepPin, HIGH);
  //   digitalWrite(stepPin1, HIGH);
  //   delayMicroseconds(2000);
  //   digitalWrite(stepPin, LOW);
  //   digitalWrite(stepPin1, LOW);
  //   delayMicroseconds(2000);
  // }
  // delay(1000);

  //     // Set the spinning direction counterclockwise:
  // digitalWrite(dirPin, HIGH);
  // digitalWrite(dirPin1, LOW);


  // //Spin the stepper motor 5 revolutions fast:
  // for (int i = 0; i < 5 * stepsPerRevolution; i++) {
  //   // These four lines result in 1 step:
  //   digitalWrite(stepPin, HIGH);
  //   digitalWrite(stepPin1, HIGH);
  //   delayMicroseconds(2000);
  //   digitalWrite(stepPin, LOW);
  //   digitalWrite(stepPin1, LOW);
  //   delayMicroseconds(2000);
  // }
  // delay(1000);

  //     // Set the spinning direction counterclockwise:
  // digitalWrite(dirPin, LOW);
  // digitalWrite(dirPin1, HIGH);


  // //Spin the stepper motor 5 revolutions fast:
  // for (int i = 0; i < 5 * stepsPerRevolution; i++) {
  //   // These four lines result in 1 step:
  //   digitalWrite(stepPin, HIGH);
  //   digitalWrite(stepPin1, HIGH);
  //   delayMicroseconds(2000);
  //   digitalWrite(stepPin, LOW);
  //   digitalWrite(stepPin1, LOW);
  //   delayMicroseconds(2000);
  // }
  // delay(1000);

}