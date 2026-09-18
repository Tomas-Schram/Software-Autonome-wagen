"""Motor controller abstraction for the robot chassis."""


class MotorDriver:
    """Interface for the Kitronik Compact Motor Driver Board."""

    def __init__(self) -> None:
        self.left_speed = 0
        self.right_speed = 0

    def set_left_speed(self, speed: int) -> None:
        """Set the speed of the left motor."""
        self.left_speed = int(speed)

    def set_right_speed(self, speed: int) -> None:
        """Set the speed of the right motor."""
        self.right_speed = int(speed)

    def stop(self) -> None:
        """Stop both motors."""
        self.left_speed = 0
        self.right_speed = 0
