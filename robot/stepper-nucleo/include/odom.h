#ifndef STEPPER_NUCLEO_ODOM_H
#define STEPPER_NUCLEO_ODOM_H

#include "contant.h"

class Odometry {
public:
    Position *_actual_position;

    explicit Odometry(Position *actual_position);

    Position set_position(Position *position);
};

#endif //STEPPER_NUCLEO_ODOM_H
