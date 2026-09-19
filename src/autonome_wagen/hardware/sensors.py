"""Sensor abstractions for obstacle and line detection."""

try:
    from microbit import accelerometer, button_a, button_b, compass, temperature
except ImportError:  # pragma: no cover - used when running on a normal computer
    class _MicrobitAccelerometer:
        def __init__(self) -> None:
            self._pitch = 0.0
            self._roll = 0.0

        def get_pitch(self) -> float:
            return self._pitch

        def get_roll(self) -> float:
            return self._roll

    class _MicrobitCompass:
        def __init__(self) -> None:
            self._heading = 0.0

        def heading(self) -> float:
            return self._heading

        def calibrate(self) -> None:
            self._heading = 0.0

    class _MicrobitButton:
        def __init__(self, pressed: bool = False) -> None:
            self._pressed = pressed

        def is_pressed(self) -> bool:
            return self._pressed

    accelerometer = _MicrobitAccelerometer()
    compass = _MicrobitCompass()
    button_a = _MicrobitButton(True)
    button_b = _MicrobitButton(False)
    temperature = lambda: 0.0


class UltrasonicSensor:
    """HC-SR04 style ultrasonic distance sensor."""

    def __init__(self, threshold_cm: float = 10.0) -> None:
        self.distance_cm = 0.0
        self.threshold_cm = threshold_cm

    def has_obstacle(self) -> bool:
        """Return True if an object is within detection range."""
        return self.distance_cm <= self.threshold_cm


class MicrobitMotionSensor:
    """Read Micro:bit motion data such as pitch, roll, and tilt state."""

    def __init__(self) -> None:
        self._offset_pitch = 0.0
        self._offset_roll = 0.0

    def calibrate(self) -> None:
        """Set the current motion as the reference zero position."""
        self._offset_pitch = self.get_pitch()
        self._offset_roll = self.get_roll()

    def get_pitch(self) -> float:
        getter = getattr(accelerometer, "get_pitch", None)
        if callable(getter):
            return float(getter())
        return 0.0

    def get_roll(self) -> float:
        getter = getattr(accelerometer, "get_roll", None)
        if callable(getter):
            return float(getter())
        return 0.0

    def is_tilted(self, threshold_deg: float = 10.0) -> bool:
        """Return True if either pitch or roll exceeds the tilt threshold."""
        pitch_change = abs(self.get_pitch() - self._offset_pitch)
        roll_change = abs(self.get_roll() - self._offset_roll)
        return max(pitch_change, roll_change) >= threshold_deg


class MicrobitCompassSensor:
    """Read the built-in compass from the Micro:bit."""

    def __init__(self) -> None:
        self._is_calibrated = False

    def calibrate(self) -> None:
        """Calibrate the compass if the underlying device supports it."""
        calibrator = getattr(compass, "calibrate", None)
        if callable(calibrator):
            calibrator()
        self._is_calibrated = True

    def get_heading(self) -> float:
        getter = getattr(compass, "heading", None)
        if callable(getter):
            return float(getter())
        return 0.0

    def is_ready(self) -> bool:
        """Return True if the compass is ready to provide a heading."""
        return self._is_calibrated or self.get_heading() >= 0.0


class MicrobitTemperatureSensor:
    """Read the Micro:bit temperature sensor."""

    def read_celsius(self) -> float:
        getter = getattr(temperature, "__call__", None)
        if callable(temperature):
            return float(temperature())
        if callable(getter):
            return float(temperature())
        return 0.0

    def read_fahrenheit(self) -> float:
        return (self.read_celsius() * 9.0 / 5.0) + 32.0


class MicrobitButtonSensor:
    """Wrap either Micro:bit button A or B as a simple sensor state."""

    def __init__(self, side: str) -> None:
        side = side.lower()
        if side not in {"left", "right", "a", "b"}:
            raise ValueError("side must be 'left', 'right', 'a', or 'b'")
        self.side = side

    def is_pressed(self) -> bool:
        if self.side in {"left", "a"}:
            return bool(button_a.is_pressed())
        return bool(button_b.is_pressed())


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
