"""Slope safety detection for the autonomous car."""


class SlopeDetector:
    """Detect whether the car is on a slope using a Micro:bit gyroscope pitch reading."""

    def __init__(self, threshold_deg: float = 8.0, tilt_sensor=None) -> None:
        self.threshold_deg = threshold_deg
        self.tilt_sensor = tilt_sensor
        self.pitch_angle_deg = 0.0
        self._pitch_offset_deg = 0.0

    def calibrate(self, pitch_angle_deg: float | None = None) -> None:
        """Set the zero-reference angle for the current test run or startup position."""
        if pitch_angle_deg is None:
            if self.tilt_sensor is None:
                raise ValueError("pitch_angle_deg is required when no tilt sensor is configured")
            self.tilt_sensor.calibrate()
            self._pitch_offset_deg = 0.0
            return

        self._pitch_offset_deg = float(pitch_angle_deg)

    def update_pitch(self, pitch_angle_deg: float | None = None) -> None:
        """Update the current pitch value relative to the calibrated baseline."""
        if pitch_angle_deg is None:
            if self.tilt_sensor is None:
                raise ValueError("pitch_angle_deg is required when no tilt sensor is configured")
            self.pitch_angle_deg = self.tilt_sensor.get_relative_pitch_degrees()
            return

        self.pitch_angle_deg = abs(float(pitch_angle_deg) - self._pitch_offset_deg)

    def is_on_slope(self) -> bool:
        """Return True when the pitch exceeds the configured slope threshold."""
        return self.pitch_angle_deg >= self.threshold_deg

    def recommended_speed_factor(self) -> float:
        """Return a lower speed factor as the slope increases, down to a minimum floor."""
        if not self.is_on_slope():
            return 1.0

        excess_deg = max(0.0, self.pitch_angle_deg - self.threshold_deg)
        factor = 1.0 / (1.0 + (excess_deg / 10.0))
        return max(0.2, factor)
