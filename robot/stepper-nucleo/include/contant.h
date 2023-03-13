#ifndef STEPPER_NUCLEO_CONTANT_H
#define STEPPER_NUCLEO_CONTANT_H

#define dirPinLeft 13
#define dirPinRight 2
#define stepPinLeft 12
#define stepPinRight 4
#define stepsPerRevolution 200
#define stepperResolution 0.032
#define button A0
#define led A1
#define wheelRadius 0.039
#define interAxis 0.123

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
