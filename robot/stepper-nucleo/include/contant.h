#ifndef STEPPER_NUCLEO_CONTANT_H
#define STEPPER_NUCLEO_CONTANT_H

#define dirPinLeft 2
#define dirPinRight 5
#define stepPinLeft 8
#define stepPinRight 4
#define stepsPerRevolution 100
#define stepperResolution 0.1
#define button A0
#define led A1
#define wheelRadius 0.037
#define interAxis 0.270

struct Position {
    float x;
    float y;
    float theta;
};

struct Distance {
    float distance;
    float angle;
};

struct Step {
    float left;
    float right;
};

#endif //STEPPER_NUCLEO_CONTANT_H
