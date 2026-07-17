# Contributing

## Project structure

The repository contains four intentionally separate learning stages. Keep lab-specific examples in their original lab unless a change fixes a shared safety or packaging problem. The maintained autonomous-navigation implementation lives in `lab_final`.

## Development workflow

1. Read the relevant lab README before changing code.
2. Add or update a hardware-independent test before changing behavior.
3. Keep ROS callbacks thin and put reusable calculations in pure Python modules.
4. Run the local validation commands in `docs/testing.md`.
5. Update the relevant README or troubleshooting note when behavior or launch commands change.

## Safety requirements

Any node that publishes motion commands must stop on shutdown, missing input, stale vision data, and invalid detections. Do not run more than one command-producing behavior against the same vehicle at a time.

## Style

- Use Python 3, four spaces, and descriptive snake_case names.
- Prefer small functions with explicit inputs and outputs.
- Keep topic names and message types documented beside the node that owns them.
- Do not commit bags, generated plots, camera samples, build outputs, or editor files.

