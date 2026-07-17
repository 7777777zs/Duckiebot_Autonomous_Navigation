# Architecture

## Final pipeline

```text
camera_node/image/compressed + camera_info
        ↓
camera_processing_node
        ↓ sensor_msgs/Image
computer_vision/image/processed
        ↓
color_detection_node
        ↓ computer_vision/LineDetection
computer_vision/line_detection
        ↓
state_machine_node
        ↓
car_cmd_switch_node/cmd + led_emitter_node/led_pattern
```

`camera_processing_node` owns calibration-aware undistortion, resizing, and blur. `color_detection_node` publishes one typed detection message per processed frame, including an explicit no-detection result. `state_machine_node` is the only motion-command publisher in the default launch.

## Diagnostic controllers

P, PD, PID, and lane-following nodes are educational alternatives. They consume processed camera data and publish vehicle commands only when launched individually. They are not started by `default.sh`.

## Safety boundary

Motion nodes stop on shutdown, missing detections, stale inputs, and invalid controller state. The runtime documentation treats topic ownership and command-node exclusivity as safety requirements.
