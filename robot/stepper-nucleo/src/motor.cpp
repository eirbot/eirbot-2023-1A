//
// Created by sedelpeuch on 10/03/23.
//
#include "../include/motor.h"
#include "Arduino.h"
#include "constant.h"

Motor::Motor() {
    this->min_speed = 600;
    this->max_speed = 400;
    this->ramp = 800;
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

void Motor::ApplyStep(Step *step) {
    float speed;

    if (step->left > 0) {
        digitalWrite(dirPinLeft, HIGH);
    } else {
        digitalWrite(dirPinLeft, LOW);
    }
    if (step->right > 0) {
        digitalWrite(dirPinRight, HIGH);
    } else {
        digitalWrite(dirPinRight, LOW);
    }

    int i = 0, j = 0;
    while (i < abs(step->left) && j < abs(step->right)) {
        while (digitalRead(stopAsserv) == HIGH) {
            delay(100);
        }
        if (i <= this->ramp || j <= this->ramp) {
            speed = (this->max_speed - this->min_speed) / this->ramp * max(i, j) + this->min_speed;
        } else {
            speed = this->max_speed;
        }

        if (i >= abs(step->left) - this->ramp || j >= abs(step->right) - this->ramp) {
            float deltaT = this->ramp;
            int t = max(i, j) - max(abs(step->left), abs(step->right)) + this->ramp;
            speed = (-this->max_speed + this->min_speed) / deltaT * t + this->max_speed;
        }

        digitalWrite(stepPinLeft, HIGH);
        digitalWrite(stepPinRight, HIGH);
        delayMicroseconds(int(speed));
        digitalWrite(stepPinLeft, LOW);
        digitalWrite(stepPinRight, LOW);
        delayMicroseconds(int(speed));
        i++;
        j++;
    }
}
