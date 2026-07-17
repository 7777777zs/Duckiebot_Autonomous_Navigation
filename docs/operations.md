# Operations and safety

## Command ownership

Only one command-producing node may run for a vehicle at a time. The default pipeline owns `/<vehicle>/car_cmd_switch_node/cmd`; P/PD/PID and lane-following launchers are alternatives, not additions.

## Safe stop

The expected stop behavior is zero linear velocity and zero angular velocity. Nodes must publish a stop command when:

- ROS shuts down
- camera calibration or frames are unavailable
- detection data is stale
- controller state is invalid

The state machine also turns LEDs off during shutdown.

## Recovery

1. Stop the active launcher.
2. Confirm the robot is stationary.
3. Inspect camera and detection topics.
4. Restart only the required launcher.

Do not restart another controller while the previous command-producing process is still active.
