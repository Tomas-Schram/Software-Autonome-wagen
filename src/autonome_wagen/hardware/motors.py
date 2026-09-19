"""Motor controller abstraction for the robot chassis."""


class MotorDriver:
    """Interface for the Kitronik Compact Motor Driver Board."""

    def __init__(
        self,
        *,
        left_enable_pin: int | None = None,
        right_enable_pin: int | None = None,
        left_direction_pin: int | None = None,
        right_direction_pin: int | None = None,
    ) -> None:
        self.left_enable_pin = left_enable_pin
        self.right_enable_pin = right_enable_pin
        self.left_direction_pin = left_direction_pin
        self.right_direction_pin = right_direction_pin
        self.left_speed = 0.0
        self.right_speed = 0.0

    def configure_pins(
        self,
        *,
        left_enable_pin: int | None = None,
        right_enable_pin: int | None = None,
        left_direction_pin: int | None = None,
        right_direction_pin: int | None = None,
    ) -> None:
        """Update the board pin mapping without changing the rest of the driver behavior."""
        if left_enable_pin is not None:
            self.left_enable_pin = left_enable_pin
        if right_enable_pin is not None:
            self.right_enable_pin = right_enable_pin
        if left_direction_pin is not None:
            self.left_direction_pin = left_direction_pin
        if right_direction_pin is not None:
            self.right_direction_pin = right_direction_pin

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
