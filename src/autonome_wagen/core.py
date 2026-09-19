from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class DrivingMode(str, Enum):
    """Supported driving modes for the autonomous vehicle."""

    MANUAL = "manual"
    AUTONOMOUS = "autonomous"
    SAFE = "safe"


@dataclass
class VehicleState:
    """Current state of the vehicle."""

    power: float = 0.0
    steering_angle_deg: float = 0.0
    mode: DrivingMode = DrivingMode.SAFE


class AutonomeWagen:
    """Minimal control layer for the Autonome Wagen project."""

    def __init__(self, initial_mode: DrivingMode = DrivingMode.SAFE) -> None:
        self.state = VehicleState(mode=initial_mode)

    def set_mode(self, mode: DrivingMode) -> None:
        """Set the active driving mode."""
        self.state.mode = mode

    def set_speed(self, power: float) -> None:
        """Set the drive power as a normalized value between 0 and 1."""
        if not 0.0 <= power <= 1.0:
            raise ValueError("power must be between 0 and 1")
        self.state.power = float(power)

    def steer(self, steering_angle_deg: float) -> None:
        """Update the steering wheel angle in degrees."""
        self.state.steering_angle_deg = float(steering_angle_deg)

    def apply_drive_command(self, power: float, steering_angle_deg: float) -> None:
        """Apply a combined drive and steering update."""
        self.set_speed(power)
        self.steer(steering_angle_deg)
