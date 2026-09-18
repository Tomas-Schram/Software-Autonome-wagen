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

    speed_kmh: float = 0.0
    steering_angle_deg: float = 0.0
    mode: DrivingMode = DrivingMode.SAFE


class AutonomeWagen:
    """Minimal control layer for the Autonome Wagen project."""

    def __init__(self, initial_mode: DrivingMode = DrivingMode.SAFE) -> None:
        self.state = VehicleState(mode=initial_mode)

    def set_mode(self, mode: DrivingMode) -> None:
        """Set the active driving mode."""
        self.state.mode = mode

    def set_speed(self, speed_kmh: float) -> None:
        """Update the current vehicle speed in km/h."""
        if speed_kmh < 0:
            raise ValueError("speed_kmh must be non-negative")
        self.state.speed_kmh = float(speed_kmh)

    def steer(self, steering_angle_deg: float) -> None:
        """Update the steering wheel angle in degrees."""
        self.state.steering_angle_deg = float(steering_angle_deg)

    def apply_drive_command(self, speed_kmh: float, steering_angle_deg: float) -> None:
        """Apply a combined drive and steering update."""
        self.set_speed(speed_kmh)
        self.steer(steering_angle_deg)
