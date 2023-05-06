//
// Created by sedelpeuch on 10/03/23.
//
#include "../include/motor.h"
#include "Arduino.h"

Motor::Motor() = default;

void Motor::MeterToStep(Distance *distance, Step *step) {
    // take the distance and convert it to step using the constant
    float distanceMeter = distance->distance;
    auto step_inc = float(distanceMeter * stepsPerRevolution / stepperResolution);
    step->left = step_inc;
    step->right = step_inc;
}

void Motor::AngleToStep(float angle, Step *step) {
    // take the angle and convert it to step using the constant
    auto step_inc = float((abs(angle) * stepsPerRevolution * interAxis) / (2 * PI * wheelRadius));
    if (angle > 0) {
        step->left = step_inc;
        step->right = -step_inc;
    } else {
        step->left = -step_inc;
        step->right = step_inc;
    }
}

void Motor::ApplyStep(Step *step) {
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
    while (i < abs(step->left) && j < abs(step->right) && digitalRead(stopAsserv) != HIGH) {
        Serial.println("step");
        digitalWrite(stepPinLeft, HIGH);
        digitalWrite(stepPinRight, HIGH);
        delayMicroseconds(100);
        digitalWrite(stepPinLeft, LOW);
        digitalWrite(stepPinRight, LOW);
        delayMicroseconds(100);
        i++;
        j++;
    }

    if (i < step->left) {
        while (i < step->left && digitalRead(stopAsserv) != HIGH) {
            Serial.println("step");
            digitalWrite(stepPinLeft, HIGH);
            delayMicroseconds(100);
            digitalWrite(stepPinLeft, LOW);
            delayMicroseconds(100);
            i++;
        }
    }
    if (j < step->right) {
        while (j < step->right && digitalRead(stopAsserv) != HIGH) {
            Serial.println("step");
            digitalWrite(stepPinRight, HIGH);
            delayMicroseconds(100);
            digitalWrite(stepPinRight, LOW);
            delayMicroseconds(100);
            j++;
        }
    }
}
