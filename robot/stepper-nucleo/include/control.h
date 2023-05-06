#ifndef STEPPER_NUCLEO_CONTROL_H
#define STEPPER_NUCLEO_CONTROL_H

#include "motor.h"
#include "constant.h"

class Control {

private:
    Motor *motor;

public:
    explicit Control(Motor *motor);

    int go_to(Position *target);

    static Distance position_to_distance(Position *target);

    ~Control();
};

#endif //STEPPER_NUCLEO_CONTROL_H
