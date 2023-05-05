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

void ReadSerial() {
    if (Serial.available() > 0) {
        String cmd = Serial.readStringUntil('\n'); // read the incoming command
        char *tok = strtok(&cmd[0], ":"); // parse the command using strtok()

        int i = 0;
        int cmdArguments[3] = {0, 0, 0};

        while (tok != NULL && i < 3) {
        cmdArguments[i] = atoi(tok); // convert the string token to integer
        tok = strtok(NULL, ":"); // move to the next token
        i++;
        }

        if (i == 3) {
            Position target = {(float)cmdArguments[0],(float)cmdArguments[1], (float)cmdArguments[2]}; // x y theta
            control.go_to(&target);
        }
    }
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