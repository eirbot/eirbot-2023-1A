#include "../include/control.h"
#include "Arduino.h"

Control::Control(Odometry *odom, Motor *motor) {
    this->odom = odom;
    this->motor = motor;
}

int Control::go_to(Position *target) {
    Distance distanceAngle = position_to_distance(target);
    Step step = motor->AngleToStep(distanceAngle.angle);
    motor->ApplyStep(&step);
    delay(1000);
    step = motor->MeterToStep(&distanceAngle);
    motor->ApplyStep(&step);
    return 0;
}

Distance Control::position_to_distance(Position *target) {
    // comptue x and y distance in the actual position x and y can be negative
    float x = target->x - odom->_actual_position->x;
    float y = target->y - odom->_actual_position->y;

    // compute the angle between the actual position and the target. If the angle is superior to PI, we need to take the negative angle. Do a 2PI
    // modulo

    float targetAngle = target->theta;
    float actualAngle = odom->_actual_position->theta;
    float differenceAngle = targetAngle - actualAngle;
    if (differenceAngle > PI) {
        differenceAngle = differenceAngle - 2 * PI;
    } else if (differenceAngle < -PI) {
        differenceAngle = differenceAngle + 2 * PI;
    }
    // compute the distance
    float distance = sqrt(pow(x, 2) + pow(y, 2));
    Distance distanceAngle = {distance, differenceAngle};
    return distanceAngle;
}

Control::~Control() {
    delete odom;
    delete motor;

}
