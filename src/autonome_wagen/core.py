"""MicroPython-friendly core state for the robot.

This version intentionally avoids advanced host-only Python features such as
``dataclasses`` and ``Enum`` so the same logic can run on a Micro:Bit controller.
"""


class _DrivingModeValue(str):
    """String-like mode value that exposes a .value attribute."""

    def __new__(cls, value):
        obj = str.__new__(cls, value)
        obj.value = value
        return obj


class DrivingMode:
    """Enum-like string constants for the autonomous vehicle.

    This keeps the project MicroPython-friendly while preserving the repo's expected
    semantics, including `.value` access on each mode constant.
    """

    DEFAULT_DRIVE = _DrivingModeValue("default drive")
    AUTONOMOUS = _DrivingModeValue("default drive")
    SAFE = _DrivingModeValue("safe")


class VehicleState:
    """Current state of the vehicle."""

    def __init__(self, power=0.0, steering_angle_deg=0.0, mode=None):
        self.power = float(power)
        self.steering_angle_deg = float(steering_angle_deg)
        self.mode = mode if mode is not None else DrivingMode.SAFE


class AutonomeWagen:
    """Minimal control layer for the Autonome Wagen project."""

    def __init__(self, initial_mode=None):
        if initial_mode is None:
            initial_mode = DrivingMode.SAFE
        self.state = VehicleState(mode=initial_mode)

    def set_mode(self, mode):
        """Set the active driving mode."""
        self.state.mode = mode

    def set_speed(self, power):
        """Set the drive power as a normalized value between 0 and 1."""
        if not 0.0 <= power <= 1.0:
            raise ValueError("power must be between 0 and 1")
        self.state.power = float(power)

    def steer(self, steering_angle_deg):
        """Update the steering wheel angle in degrees."""
        self.state.steering_angle_deg = float(steering_angle_deg)

    def apply_drive_command(self, power, steering_angle_deg):
        """Apply a combined drive and steering update."""
        self.set_speed(power)
        self.steer(steering_angle_deg)
