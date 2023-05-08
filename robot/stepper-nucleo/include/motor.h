#ifndef STEPPER_NUCLEO_MOTOR_H
#define STEPPER_NUCLEO_MOTOR_H

#include "constant.h"
#include "AccelStepper.h"
#include "MultiStepper.h"

class Motor {
private:
    AccelStepper stepperLeft;
    AccelStepper stepperRight;
    MultiStepper steppers;
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
    void ApplyStep(Step *step, float RevPerSec = 0.5);

};

#endif //STEPPER_NUCLEO_MOTOR_H
