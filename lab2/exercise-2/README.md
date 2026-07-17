# Lab 2 — ROS and odometry

This stage introduces ROS publishers and subscribers, camera conversion, wheel commands, encoder data, differential-drive odometry, and trajectory plotting.

## Main package

The code is in `packages/odometry/src/`. The most important entry points are:

- `camera_reader_node.py` — converts and annotates camera images.
- `wheel_control_node.py` — drives forward and backward for a measured duration.
- `wheel_encoder_reader_node.py` — logs left and right encoder ticks.
- `move.py` — traces the D-shaped exercise path and records odometry.
- `plot.py` — reads the odometry bag and creates a trajectory plot.

## Build and run

```bash
dts devel build -f
dts devel run -R <robot-name> -L wheel-control
dts devel run -R <robot-name> -L wheel-encoder-reader
dts devel run -R <robot-name> -L move
```

Run only one wheel-command launcher at a time. Use `plot` after a bag has been recorded.

## Expected behavior

Wheel commands stop on completion and shutdown. The odometry exercise records the integrated pose and the plotter reads the resulting `odometry_<vehicle>.bag` file.

## Limitations

Time-based wheel commands are approximate and require calibration. Floor friction, wheel slip, encoder direction, and camera geometry affect the measured result.
