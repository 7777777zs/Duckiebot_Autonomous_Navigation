# Getting started

## Requirements

- Docker and the Duckietown Shell (`dts`)
- A Duckiebot name reachable from the development environment
- A calibrated Duckiebot camera for physical runs
- A Duckietown-compatible ROS environment for package builds

## Build

Run from the repository root:

```bash
dts devel build -f
```

## Run the final pipeline

```bash
dts devel run -R <robot-name> -L default
```

The default launcher starts image processing, color detection, and the colored-line state machine. It is the only launcher intended to command the complete autonomous behavior.

## Run diagnostics

Diagnostics are deliberately independent. Stop the default pipeline before starting a controller diagnostic.

```bash
dts devel run -R <robot-name> -L camera-distortion
dts devel run -R <robot-name> -L camera-processing
dts devel run -R <robot-name> -L color-detection
dts devel run -R <robot-name> -L p-controller
dts devel run -R <robot-name> -L pd-controller
dts devel run -R <robot-name> -L pid-controller
dts devel run -R <robot-name> -L lane-following
```

## Before moving the robot

Verify the robot is on a clear test surface, the wheels are free, the camera stream is live, and an emergency stop is available. Start at low speed and keep the robot within reach.
