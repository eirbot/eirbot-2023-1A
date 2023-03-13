#include "Arduino.h"
#include "control.h"
#include "odom.h"
#include "motor.h"

void setup() {
    Position initialPosition = {0, 0, 0};
    Odometry odom = Odometry(&initialPosition);
    Motor motor = Motor();
    Control control = Control(&odom, &motor);

    Position targetTranslate = {1, 0, 0};
    Position targetRotate = {0, 0, PI / 2};

    control.go_to(&targetTranslate);
    delay(1000);
    control.go_to(&targetRotate);
}

void loop() {

}