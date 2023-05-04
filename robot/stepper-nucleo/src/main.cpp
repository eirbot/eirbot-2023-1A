#include "Arduino.h"
#include "control.h"
#include "odom.h"
#include "motor.h"
#include "contant.h"

Position initialPosition = {0, 0, 0};
Odometry odom = Odometry(&initialPosition);
Motor motor = Motor();
Control control = Control(&odom, &motor);


void setup() {
    Serial.begin(9600);
    pinMode(stepPinLeft, OUTPUT);
    pinMode(stepPinRight, OUTPUT);
    pinMode(dirPinLeft, OUTPUT);
    pinMode(dirPinRight, OUTPUT);
}

void loop() {
    Position targetRotate = {0, 0, PI / 2};
    Position targetTrans = {0.1, 0, 0};
    delay(2000);
    control.go_to(&targetRotate);
    delay(2000);
    control.go_to(&targetTrans);
    delay(2000);
    targetRotate = {0, 0, PI};
    control.go_to(&targetRotate);
    delay(2000);
    targetTrans = {0.1, 0, 0};
    control.go_to(&targetTrans);
}