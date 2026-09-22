# Autonome Wagen

This project is the software for an autonomous robot car. The current design treats the Micro:Bit as the robot controller, while this repository remains the host-side development and testing codebase.

## Architecture

The Micro:Bit is the controller of the robot, not a passive peripheral.

That means:
- the board runs a small MicroPython control loop
- this repository is used for design, validation, and higher-level logic
- the full repo is not flashed to the Micro:Bit as-is
- the board firmware is a compact controller script, not the desktop Python project

## Repository layout

- `src/autonome_wagen/core.py`  
  Core vehicle state and drive modes.

- `src/autonome_wagen/control/controller.py`  
  Control logic for driving and safety decisions.

- `src/autonome_wagen/hardware/`  
  Hardware abstractions for motors and Micro:Bit sensors.

- `src/autonome_wagen/navigation/`  
  Navigation logic for open-space and line-based decisions.

- `src/autonome_wagen/safety/`  
  Safety logic for slope checks and barrier behavior.

- `src/autonome_wagen/micropython_controller.py`  
  MicroPython-friendly controller entry point for the Micro:Bit.

- `tests/`  
  Regression tests for the project logic.

## Default drive mode

The default autonomous driving mode is named:

- `default drive`

This is the normal operating state when the robot is moving without a special safety or obstacle override.

## Validation

Run the Python test suite locally:

```bash
python -m pytest -q
```

The repo is validated through these tests before hardware changes are made.

## Flashing the Micro:Bit

Do not flash the entire repo onto the Micro:Bit.

Instead, flash a small MicroPython controller script that contains only the robot control logic. That script should:
- read inputs from sensors or buttons
- decide movement
- update the vehicle mode
- control drive outputs or motor commands
- optionally show status on the display

## Recommended workflow

1. Update the design logic in this repository
2. Validate it with pytest
3. Extract the relevant control behavior into a MicroPython script
4. Flash that script to the Micro:Bit
5. Test the robot on hardware
6. Iterate and reflash as needed

## Summary

This repo supports an embedded-controller approach:
- host machine: development, prototyping, and tests
- Micro:Bit: onboard robot controller
