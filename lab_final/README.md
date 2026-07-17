# Final lab — Modular autonomous navigation

This is the maintained application in the repository. It connects camera processing, typed colored-line detection, a safe state machine, wheel commands, and LED state indicators.

## Canonical pipeline

```text
camera + calibration → processing → LineDetection
    → colored-line state machine → commands + LEDs
```

## Build and run

```bash
dts devel build -f
dts devel run -R <robot-name> -L default
```

The default launcher starts only the end-to-end autonomous pipeline. Diagnostic launchers are available for camera distortion, camera processing, color detection, P/PD/PID controllers, and lane following.

## Interfaces

- Input: `/<vehicle>/camera_node/image/compressed`
- Processed image: `/<vehicle>/computer_vision/image/processed`
- Detection: `/<vehicle>/computer_vision/line_detection`
- State: `/<vehicle>/computer_vision/state`
- Motion: `/<vehicle>/car_cmd_switch_node/cmd`
- LEDs: `/<vehicle>/led_emitter_node/led_pattern`

## Safety

The state machine stops on missing or stale detection data and publishes zero velocity on shutdown. Do not run a diagnostic controller alongside the default launcher.

## Validation

Use `python -m pytest` for hardware-independent tests. Physical validation requires a calibrated Duckiebot and a clear test track; see the root `docs/operations.md` and `docs/testing.md`.
