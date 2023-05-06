#ifndef STEPPER_NUCLEO_MOTOR_H
#define STEPPER_NUCLEO_MOTOR_H

#include "constant.h"

class Motor {
public:
    Motor();

    /**
     * Convert distance to step
     * @param distance distance in meter
     * @return step
     */
    Step MeterToStep(Distance *distance);

    /**
     * Convert angle to step
     * @param angle distance in meter
     * @return step
     */
    Step AngleToStep(float angle);

    /**
     * Apply step to motor
     * @param step step
     * @param time time
     */
    void ApplyStep(Step *step);

};

#endif //STEPPER_NUCLEO_MOTOR_H
