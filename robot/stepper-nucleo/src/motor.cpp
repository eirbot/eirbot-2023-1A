//
// Created by sedelpeuch on 10/03/23.
//
#include "../include/motor.h"
#include "Arduino.h"
#include "constant.h"

Motor::Motor() {
    this->stepperLeft = AccelStepper(AccelStepper::DRIVER, stepPinLeft, dirPinLeft);
    this->stepperRight = AccelStepper(AccelStepper::DRIVER, stepPinRight, dirPinRight);
    this->stepperLeft.setMaxSpeed(5 * stepsPerRevolution);
    this->stepperRight.setMaxSpeed(5 * stepsPerRevolution);
    this->stepperLeft.setAcceleration(3 * stepsPerRevolution);
    this->stepperRight.setAcceleration(3 * stepsPerRevolution);
    this->stepperLeft.setSpeed(500000);
    this->stepperRight.setSpeed(500000);

    this->steppers = MultiStepper();
    this->steppers.addStepper(stepperLeft);
    this->steppers.addStepper(stepperRight);
}

void Motor::MeterToStep(Distance *distance, Step *step) {
    // take the distance and convert it to step using the constant
    float distanceMeter = distance->distance;
    auto step_inc = float(distanceMeter * stepsPerRevolution) / (2 * PI * wheelRadius);
    step->left = step_inc;
    step->right = step_inc;
}

void Motor::AngleToStep(float angle, Step *step) {
    // take the angle and convert it to step using the constant
    auto step_inc = float((abs(angle) * stepsPerRevolution * interAxis * 0.5) / (2 * PI * wheelRadius));
    if (angle > 0) {
        step->left = step_inc;
        step->right = -step_inc;
    } else {
        step->left = -step_inc;
        step->right = step_inc;
    }
}

void Motor::ApplyStep(Step *step, float RevPerSec) {
    this->stepperLeft.move(step->left);
    this->stepperRight.move(step->right);
    this->stepperLeft.setSpeed(RevPerSec * stepsPerRevolution);
    this->stepperRight.setSpeed(RevPerSec * stepsPerRevolution);
    boolean arrivedLeft = true;
    boolean arrivedRight = true;
    while (arrivedLeft && arrivedRight) {
        if (digitalRead(stopAsserv) == HIGH) {
            this->stepperLeft.stop();
            this->stepperRight.stop();
            return;
        }
        arrivedLeft = this->stepperLeft.run();
        arrivedRight = this->stepperRight.run();
    }
}
