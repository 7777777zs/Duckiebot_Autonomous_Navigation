# Lab 1 — Environment basics

This introductory exercise verifies that project code can execute inside the Duckietown environment and read the active robot name.

## Entry point

```text
packages/my_package/my_script.py
```

The script reads the `VEHICLE_NAME` environment variable and prints a greeting. It does not publish ROS messages or move the robot.

## Run

```bash
python3 packages/my_package/my_script.py
```

The output includes the configured vehicle name. If `VEHICLE_NAME` is missing, configure the environment before running the exercise.
