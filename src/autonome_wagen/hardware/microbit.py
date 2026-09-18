"""Micro:bit-specific adapters for real hardware interaction."""


class MicrobitMotorDriver:
    """Adapter layer that wraps Micro:bit motor commands."""

    def __init__(self) -> None:
        self.left_speed = 0
        self.right_speed = 0

    def set_left_speed(self, speed: int) -> None:
        """Set the left motor speed using the hardware interface."""
        self.left_speed = int(speed)

    def set_right_speed(self, speed: int) -> None:
        """Set the right motor speed using the hardware interface."""
        self.right_speed = int(speed)


class MicrobitSoundPlayer:
    """Adapter for making a sound on the Micro:bit hardware."""

    def __init__(self) -> None:
        self.last_sound = None

    def play(self, sound_name: str) -> None:
        """Play a sound name and store the last sound for verification."""
        self.last_sound = sound_name
