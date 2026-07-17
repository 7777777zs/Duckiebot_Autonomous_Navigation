#!/bin/bash

source /environment.sh
dt-launchfile-init

rosrun computer_vision state_machine_node.py

dt-launchfile-join
