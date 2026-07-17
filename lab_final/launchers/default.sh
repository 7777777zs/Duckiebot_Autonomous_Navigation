#!/bin/bash

source /environment.sh
dt-launchfile-init

roslaunch computer_vision autonomous_navigation.launch

dt-launchfile-join
