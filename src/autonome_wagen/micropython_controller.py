"""MicroPython-friendly controller for the robot when the Micro:Bit is the main controller.

This file is intentionally small and hardware-oriented so it can run on a Micro:Bit
without importing the host-only Python stack from the rest of the repo.
"""

try:
    from microbit import accelerometer, button_a, button_b, display
except ImportError:  # pragma: no cover - host-side fallback for local tests
    accelerometer = None
    button_a = None
    button_b = None

    class _DummyDisplay:
        def show(self, value):
            return value

    display = _DummyDisplay()

DEFAULT_DRIVE = "default drive"
SAFE_MODE = "safe"


class VehicleState:
    """Simple state container used by the Micro:Bit controller."""

    def __init__(self, power=0.0, steering_angle_deg=0.0, mode=DEFAULT_DRIVE):
        self.power = float(power)
        self.steering_angle_deg = float(steering_angle_deg)
        self.mode = mode


class RobotController:
    """Controller logic that runs directly on the Micro:Bit."""

    def __init__(self, state=None):
        self.state = state or VehicleState()
        self.normal_power = 0.4
        self.boost_power = 0.8
        self.slow_power = 0.2

    def drive_forward(self, power=None, *, boost_zone=False, slow_zone=False):
        """Drive forward with a default or zone-specific power level."""
        if power is not None:
            target_power = self._clamp_power(power)
        elif boost_zone:
            target_power = self.boost_power
        elif slow_zone:
            target_power = self.slow_power
        else:
            target_power = self.normal_power

        self.state.mode = DEFAULT_DRIVE
        self.state.power = float(target_power)
        self.state.steering_angle_deg = 0.0
        return target_power

    def stop(self):
        """Stop the robot and enter the safe state."""
        self.state.mode = SAFE_MODE
        self.state.power = 0.0
        self.state.steering_angle_deg = 0.0
        return self.state

    def turn(self, direction):
        """Turn left or right by updating the steering angle."""
        direction = str(direction).lower()
        if direction not in {"left", "right"}:
            direction = "left"

        self.state.mode = DEFAULT_DRIVE
        self.state.steering_angle_deg = -30.0 if direction == "left" else 30.0
        return direction

    def _clamp_power(self, power):
        power = float(power)
        if power < 0.0:
            return 0.0
        if power > 1.0:
            return 1.0
        return power

    def read_pitch(self):
        """Return the current accelerometer pitch if available."""
        if accelerometer is None:
            return 0.0
        getter = getattr(accelerometer, "get_pitch", None)
        if callable(getter):
            return float(getter())
        if hasattr(accelerometer, "pitch"):
            return float(accelerometer.pitch())
        return 0.0

    def handle_obstacle(self, front_clear=True, turn_direction="left"):
        """A simple obstacle handling routine for the Micro:Bit controller."""
        if front_clear:
            self.drive_forward()
            return "forward"

        self.stop()
        return self.turn(turn_direction)


def main():
    """Entry point for the MicroPython control loop."""
    controller = RobotController()
    controller.drive_forward()
    display.show("GO")
    return controller


if __name__ == "__main__":
    main()
