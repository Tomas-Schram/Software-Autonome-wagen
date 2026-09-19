"""Vehicle control logic and safety decisions."""

from autonome_wagen.core import AutonomeWagen, DrivingMode


class VehicleController:
    """High-level controller for the robot vehicle."""

    def __init__(self, vehicle: AutonomeWagen) -> None:
        self.vehicle = vehicle
        self.normal_power = 0.4
        self.boost_power = 0.8
        self.slow_power = 0.2

    def drive_forward(self, power: float | None = None, *, boost_zone: bool = False, slow_zone: bool = False) -> None:
        """Drive forward using a normalized motor power fraction, with a default cruising speed and special zones."""
        self.vehicle.set_mode(DrivingMode.AUTONOMOUS)

        if power is not None:
            target_power = power
        elif boost_zone:
            target_power = self.boost_power
        elif slow_zone:
            target_power = self.slow_power
        else:
            target_power = self.normal_power

        self.vehicle.set_speed(target_power)

    def handle_obstacle(self, *, front_clear: bool, turn_direction: str = "left") -> str:
        """Brake immediately on a front obstacle and turn in the preferred direction."""
        self.vehicle.set_mode(DrivingMode.SAFE)
        self.vehicle.set_speed(0.0)

        if front_clear:
            self.vehicle.steer(0.0)
            return "forward"

        direction = turn_direction if turn_direction in {"left", "right"} else "left"

        if direction == "left":
            self.vehicle.steer(-30.0)
        else:
            self.vehicle.steer(30.0)

        return direction
