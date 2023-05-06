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
    static void MeterToStep(Distance *distance, Step *step);

    /**
     * Convert angle to step
     * @param angle distance in meter
     * @return step
     */
    static void AngleToStep(float angle, Step *step);

    /**
     * Apply step to motor
     * @param step step
     * @param time time
     */
    static void ApplyStep(Step *step);

};

#endif //STEPPER_NUCLEO_MOTOR_H
