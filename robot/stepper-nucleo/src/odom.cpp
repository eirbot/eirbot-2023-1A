//
// Created by sedelpeuch on 10/03/23.
//
#include "../include/odom.h"

Odometry::Odometry(Position *actual_position) {
    this->_actual_position = actual_position;
}

Position Odometry::set_position(Position *position) {
    this->_actual_position = position;
}


