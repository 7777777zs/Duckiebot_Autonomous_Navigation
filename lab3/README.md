# Lab 3 — Vision and controllers

This stage explores the computer-vision building blocks used by the final application: camera calibration, preprocessing, colored-line detection, P/PD/PID control, lane following, and state transitions.

## Package contents

The ROS package is `packages/computer_vision`. Its nodes are independently launchable for comparison and tuning. The final modular pipeline is documented in `lab_final`; this lab remains the intermediate exercise snapshot.

## Build and run

```bash
dts devel build -f
dts devel run -R <robot-name> -L camera-processing
dts devel run -R <robot-name> -L color-detection
dts devel run -R <robot-name> -L p-controller
dts devel run -R <robot-name> -L pd-controller
dts devel run -R <robot-name> -L pid-controller
dts devel run -R <robot-name> -L lane-following
```

Run only one command-producing controller at a time. Use the state-machine launcher only when testing that behavior in isolation.

## Expected behavior

Vision nodes publish diagnostic images and controllers publish bounded `Twist2DStamped` commands only while valid detections are available. All motion nodes stop on shutdown or stale input.
