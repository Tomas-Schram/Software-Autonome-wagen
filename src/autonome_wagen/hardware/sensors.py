"""Sensor abstractions for obstacle and line detection."""


class UltrasonicSensor:
    """HC-SR04 style ultrasonic distance sensor."""

    def __init__(self, threshold_cm: float = 20.0) -> None:
        self.distance_cm = 0.0
        self.threshold_cm = threshold_cm

    def has_obstacle(self) -> bool:
        """Return True if an object is within detection range."""
        return self.distance_cm <= self.threshold_cm


class LineSensor:
    """Simple line detection sensor abstraction."""

    def __init__(self, threshold: float = 0.5) -> None:
        self.threshold = threshold
        self.values = {"left": False, "center": False, "right": False}

    @property
    def left(self) -> bool:
        return bool(self.values.get("left", False))

    @property
    def center(self) -> bool:
        return bool(self.values.get("center", False))

    @property
    def right(self) -> bool:
        return bool(self.values.get("right", False))

    def is_on_line(self) -> bool:
        """Return True if any sensor detects a line."""
        return any(self.values.values())

    def set_threshold(self, threshold: float) -> None:
        """Set the detection threshold and reject invalid values."""
        if threshold < 0:
            raise ValueError("threshold must be non-negative")
        self.threshold = float(threshold)
