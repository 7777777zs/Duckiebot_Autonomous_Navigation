# Duckiebot Autonomous Navigation

Computer-vision and motion-control exercises for a Duckiebot, developed as a four-stage CMPUT 412 project. The repository keeps the learning progression visible while presenting `lab_final` as the maintained autonomous-navigation application.

## Start here

- [Getting started](docs/getting-started.md) — build and run the project.
- [Architecture](docs/architecture.md) — understand the ROS data flow.
- [Lab guide](docs/lab-guide.md) — navigate the progression from ROS basics to navigation.
- [Operations](docs/operations.md) — safety, runtime commands, and recovery.
- [Testing](docs/testing.md) — local and Duckietown validation.
- [Troubleshooting](docs/troubleshooting.md) — common setup and runtime issues.

## Quick start: final application

From the repository root, build the Duckietown development image and run the canonical pipeline:

```bash
dts devel build -f
dts devel run -R <robot-name> -L default
```

The default pipeline is:

```text
camera + calibration → image processing → typed color detection
    → colored-line state machine → wheel commands + LEDs
```

Run one diagnostic launcher at a time when inspecting a stage:

```bash
dts devel run -R <robot-name> -L camera-processing
dts devel run -R <robot-name> -L color-detection
dts devel run -R <robot-name> -L lane-following
```

Do not run multiple command-producing controllers against the same robot simultaneously.

## Project stages

| Stage | Focus | Entry point |
| --- | --- | --- |
| [lab1](lab1/README.md) | Environment and basic Python | `lab1/packages/my_package/my_script.py` |
| [lab2](lab2/exercise-2/README.md) | ROS, wheel control, and odometry | `lab2/exercise-2/packages/odometry` |
| [lab3](lab3/README.md) | Camera processing and controllers | `lab3/packages/computer_vision` |
| [lab_final](lab_final/README.md) | Modular autonomous navigation | `lab_final/packages/computer_vision` |

## Project status

The Python source is statically checked locally. Unit tests cover the hardware-independent navigation logic. Physical Duckiebot smoke tests require a configured robot, camera calibration, and a safe test track.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for code, testing, and safety conventions.
