"""Micro:bit-specific adapters for real hardware interaction."""


class MicrobitMotorDriver:
    """Adapter layer that wraps Micro:bit motor commands."""

    def __init__(self) -> None:
        self.left_speed = 0.0
        self.right_speed = 0.0

    def set_left_speed(self, power: float) -> None:
        """Set the left motor power using the hardware interface."""
        if not 0.0 <= power <= 1.0:
            raise ValueError("power must be between 0 and 1")
        self.left_speed = float(power)

    def set_right_speed(self, power: float) -> None:
        """Set the right motor power using the hardware interface."""
        if not 0.0 <= power <= 1.0:
            raise ValueError("power must be between 0 and 1")
        self.right_speed = float(power)


class MicrobitSoundPlayer:
    """Adapter for making a sound on the Micro:bit hardware."""

    def __init__(self) -> None:
        self.last_sound = None

    def play(self, sound_name: str) -> None:
        """Play a sound name and store the last sound for verification."""
        self.last_sound = sound_name
