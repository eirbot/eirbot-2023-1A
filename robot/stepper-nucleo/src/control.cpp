#include "../include/control.h"
#include "Arduino.h"

Control::Control(Motor *motor) {
    this->motor = motor;
}

int Control::go_to(Position *target) {
    // First apply angle beetwen the actual position and the target
    float alpha = float(atan2(target->y, target->x));
    float final_theta = target->theta;
    target->theta = alpha;
    Distance distanceAngle = position_to_distance(target);
    Step step{};

    Motor::AngleToStep(distanceAngle.angle, &step);
    if (step.left != 0 && step.right != 0) {
        motor->ApplyStep(&step);
        delay(500);
    }
    Motor::MeterToStep(&distanceAngle, &step);
    if (step.left != 0 && step.right != 0) {
        motor->ApplyStep(&step);
        delay(500);
    }
    Motor::AngleToStep(final_theta, &step);
    if (step.left != 0 && step.right != 0) {
        motor->ApplyStep(&step);
        delay(500);
    }
    return 0;
}

Distance Control::position_to_distance(Position *target) {
    // comptue x and y distance in the actual position x and y can be negative

    float targetAngle = target->theta;
    if (targetAngle > float(PI)) {
        targetAngle = targetAngle - float(2 * PI);
    } else if (targetAngle < float(-PI)) {
        targetAngle = targetAngle + float(2 * PI);
    }
    auto distance = float(sqrt(pow(target->x, 2) + pow(target->y, 2)));
    Distance distanceAngle = {distance, targetAngle};
    return distanceAngle;
}

Control::~Control() {
    delete motor;

}
