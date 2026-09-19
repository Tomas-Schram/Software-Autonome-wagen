"""Motor controller abstraction for the robot chassis."""


class MotorDriver:
    """Interface for the Kitronik Compact Motor Driver Board."""

    def __init__(self) -> None:
        self.left_speed = 0.0
        self.right_speed = 0.0

    def set_left_speed(self, power: float) -> None:
        """Set the left motor power as a normalized value between 0 and 1."""
        if not 0.0 <= power <= 1.0:
            raise ValueError("power must be between 0 and 1")
        self.left_speed = float(power)

    def set_right_speed(self, power: float) -> None:
        """Set the right motor power as a normalized value between 0 and 1."""
        if not 0.0 <= power <= 1.0:
            raise ValueError("power must be between 0 and 1")
        self.right_speed = float(power)

    def stop(self) -> None:
        """Stop both motors."""
        self.left_speed = 0.0
        self.right_speed = 0.0
