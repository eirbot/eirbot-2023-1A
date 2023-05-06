#include "Arduino.h"
#include "control.h"
#include "motor.h"
#include "constant.h"

Position initialPosition = {0, 0, 0};
Position targetPosition = {0, 0, 0};
Motor motor = Motor();
Control control = Control(&motor);

int currentArg = 0;
float target[3] = {0., 0., 0.};

void setup() {
    Serial.begin(9600);
    pinMode(stepPinLeft, OUTPUT);
    pinMode(stepPinRight, OUTPUT);
    pinMode(dirPinLeft, OUTPUT);
    pinMode(dirPinRight, OUTPUT);
}

void ReadCommandFromSerial() {
    //convert Serial.read() to int
    if (Serial.available()) {
        target[currentArg] = Serial.parseFloat();
        currentArg++;

        if (currentArg == 4) {
            for (int i = 0; i < (float) target[0]; i++) {
                digitalWrite(LED_BUILTIN, HIGH);
                delay(1000);
                digitalWrite(LED_BUILTIN, LOW);
                delay(1000);
            }
            for (int i = 0; i < (float) target[1]; i++) {
                digitalWrite(LED_BUILTIN, HIGH);
                delay(1000);
                digitalWrite(LED_BUILTIN, LOW);
                delay(1000);
            }

            for (int i = 0; i < (float) target[2]; i++) {
                digitalWrite(LED_BUILTIN, HIGH);
                delay(1000);
                digitalWrite(LED_BUILTIN, LOW);
                delay(1000);
            }

            //float angle = target[2];

            targetPosition = {target[0], target[1], target[2]};
            control.go_to(&targetPosition);

            currentArg = 0;
        }

    }
}


void loop() {
//    Position targetRotate = {0, 0, PI / 2};
    Position targetTrans = {0.0, 0.2, 0};
//    delay(2000);
//    control.go_to(&targetRotate);
//    delay(2000);
    control.go_to(&targetTrans);
    delay(2000);
//    targetRotate = {0, 0, PI};
//    control.go_to(&targetRotate);
//    delay(2000);
//    targetTrans = {0.2, 0, 0};
//    control.go_to(&targetTrans);
//   ReadCommandFromSerial();
    //test();
}