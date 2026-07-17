# Testing

## Local checks

Run from the repository root:

```bash
python -m pytest
python -m compileall lab1 lab2 lab3 lab_final
```

The unit tests do not require a physical Duckiebot. They cover odometry math, synthetic color detection, controller safety, stale-data handling, and the detection message contract.

## Launcher and ROS checks

Inside a Duckietown/ROS environment:

```bash
bash -n lab_final/launchers/*.sh
catkin build
roslaunch computer_vision autonomous_navigation.launch
```

## Physical smoke test

Confirm, in order: camera frames arrive; camera calibration is received; processed images are published; detections update every frame; the state machine transitions correctly; LEDs reflect state; commands stop on shutdown; and camera loss results in a safe stop.
