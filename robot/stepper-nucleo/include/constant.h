#ifndef STEPPER_NUCLEO_CONSTANT_H
#define STEPPER_NUCLEO_CONSTANT_H

#define dirPinLeft 2
#define dirPinRight 5
#define stepPinLeft 8
#define stepPinRight 4
#define stepsPerRevolution 1600
#define wheelRadius 0.037
#define interAxis 0.270
#define stopAsserv 9

struct Position {
    float x;
    float y;
    float theta; // angle in radian
};

struct Distance {
    float distance;
    float angle;
};

struct Step {
    float left;
    float right;
};

#endif //STEPPER_NUCLEO_CONSTANT_H
