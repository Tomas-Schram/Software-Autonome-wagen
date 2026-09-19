"""Motor controller abstraction for the robot chassis."""

from dataclasses import dataclass


@dataclass(frozen=True)
class DriverBoardConfig:
    """Logical pin mapping for the motor driver board.

    The exact GPIO numbers are intentionally left open so the hardware team can
    decide the final wiring without breaking the software contract.
    """

    left_enable_pin: int | None = None
    right_enable_pin: int | None = None
    left_direction_pin: int | None = None
    right_direction_pin: int | None = None


class MotorDriver:
    """Interface for the Kitronik Compact Motor Driver Board."""

    def __init__(
        self,
        *,
        config: DriverBoardConfig | None = None,
        left_enable_pin: int | None = None,
        right_enable_pin: int | None = None,
        left_direction_pin: int | None = None,
        right_direction_pin: int | None = None,
    ) -> None:
        self.config = config or DriverBoardConfig(
            left_enable_pin=left_enable_pin,
            right_enable_pin=right_enable_pin,
            left_direction_pin=left_direction_pin,
            right_direction_pin=right_direction_pin,
        )
        self.left_enable_pin = self.config.left_enable_pin
        self.right_enable_pin = self.config.right_enable_pin
        self.left_direction_pin = self.config.left_direction_pin
        self.right_direction_pin = self.config.right_direction_pin
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
        self.config = DriverBoardConfig(
            left_enable_pin=left_enable_pin if left_enable_pin is not None else self.left_enable_pin,
            right_enable_pin=right_enable_pin if right_enable_pin is not None else self.right_enable_pin,
            left_direction_pin=left_direction_pin if left_direction_pin is not None else self.left_direction_pin,
            right_direction_pin=right_direction_pin if right_direction_pin is not None else self.right_direction_pin,
        )
        self.left_enable_pin = self.config.left_enable_pin
        self.right_enable_pin = self.config.right_enable_pin
        self.left_direction_pin = self.config.left_direction_pin
        self.right_direction_pin = self.config.right_direction_pin

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
