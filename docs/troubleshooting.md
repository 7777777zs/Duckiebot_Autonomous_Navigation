# Troubleshooting

## No launcher is available

Rebuild after changing launchers:

```bash
dts devel build -f
```

Use `-L default` for the integrated pipeline. Launcher names use hyphens.

## The robot does not move

Check that `VEHICLE_NAME` is set, camera calibration is available, and the state machine is receiving fresh `LineDetection` messages. A stop under missing or stale input is expected safety behavior.

## The robot moves unexpectedly

Stop all launchers and verify that only one command-producing node is active. Do not run a diagnostic controller alongside the default pipeline.

## Detections are incorrect

Inspect processed images, confirm lighting and camera calibration, then tune HSV thresholds in the color-detection configuration. Use the color-detection diagnostic launcher before testing motion.
