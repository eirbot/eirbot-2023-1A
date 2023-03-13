#ifndef STEPPER_NUCLEO_CONTROL_H
#define STEPPER_NUCLEO_CONTROL_H

#include "odom.h"
#include "motor.h"
#include "contant.h"

class Control {

private:
    Odometry *odom;
    Motor *motor;

public:
    Control(Odometry *odom, Motor *motor);

    int go_to(Position *target);

    Distance position_to_distance(Position *target);

    ~Control();
};

#endif //STEPPER_NUCLEO_CONTROL_H
