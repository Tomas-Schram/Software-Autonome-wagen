"""Vehicle control logic and safety decisions."""

from autonome_wagen.core import AutonomeWagen, DrivingMode


class VehicleController:
    """High-level controller for the robot vehicle."""

    def __init__(self, vehicle: AutonomeWagen) -> None:
        self.vehicle = vehicle

    def drive_forward(self, speed_kmh: float) -> None:
        """Drive forward at the given speed."""
        self.vehicle.set_mode(DrivingMode.AUTONOMOUS)
        self.vehicle.set_speed(speed_kmh)

    def handle_obstacle(self) -> None:
        """Apply safety stop when an obstacle is detected."""
        self.vehicle.set_mode(DrivingMode.SAFE)
        self.vehicle.set_speed(0.0)
