"""Vehicle control logic and safety decisions."""

from autonome_wagen.core import AutonomeWagen, DrivingMode
from autonome_wagen.safety.slope import SlopeDetector


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

    def apply_slope_limit(self, base_power: float, slope_detector: SlopeDetector) -> float:
        """Reduce power inversely as the slope steepens, while preserving a minimum floor."""
        if not slope_detector.is_on_slope():
            return float(base_power)

        reduced_power = base_power * slope_detector.recommended_speed_factor()
        return max(0.0, reduced_power)

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


class AutonomousDriveLoop:
    """Continuously update the vehicle state using real sensor inputs."""

    def __init__(
        self,
        vehicle: AutonomeWagen,
        *,
        controller: VehicleController | None = None,
        slope_detector: SlopeDetector | None = None,
        normal_power: float = 0.4,
    ) -> None:
        self.vehicle = vehicle
        self.controller = controller or VehicleController(vehicle)
        self.slope_detector = slope_detector or SlopeDetector()
        self.normal_power = float(normal_power)

    def run_cycle(
        self,
        *,
        front_clear: bool,
        pitch_angle_deg: float | None = None,
        turn_direction: str = "left",
    ) -> str:
        """Evaluate the current environment and update the vehicle state."""
        if pitch_angle_deg is not None:
            self.slope_detector.calibrate(0.0)
            self.slope_detector.update_pitch(pitch_angle_deg)

        if not front_clear:
            self.controller.handle_obstacle(front_clear=False, turn_direction=turn_direction)
            return turn_direction

        self.vehicle.set_mode(DrivingMode.AUTONOMOUS)
        target_power = self.controller.apply_slope_limit(self.normal_power, self.slope_detector)
        self.controller.drive_forward(power=target_power)
        self.vehicle.steer(0.0)
        return "forward"
