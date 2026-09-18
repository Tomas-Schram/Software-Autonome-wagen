"""Slope safety detection for the autonomous car."""


class SlopeDetector:
    """Detect whether the car is on a slope and reduce speed accordingly."""

    def __init__(self, threshold_deg: float = 8.0) -> None:
        self.threshold_deg = threshold_deg
        self.pitch_angle_deg = 0.0

    def is_on_slope(self) -> bool:
        """Return True when the pitch exceeds the configured slope threshold."""
        return self.pitch_angle_deg >= self.threshold_deg

    def recommended_speed_factor(self) -> float:
        """Return a reduced speed factor when on a slope."""
        return 0.5 if self.is_on_slope() else 1.0
