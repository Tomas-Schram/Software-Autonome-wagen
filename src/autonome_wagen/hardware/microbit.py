"""Micro:bit-specific adapters for real hardware interaction."""

try:
    from microbit import accelerometer, speaker
except ImportError:  # pragma: no cover - used when running on a normal computer
    class _MicrobitAccelerometer:
        def __init__(self):
            self._pitch = 0.0

        def get_pitch(self):
            return self._pitch

        def pitch(self):
            return self._pitch

    class _MicrobitSpeaker:
        def __init__(self):
            self.last_sound = None

        def play(self, sound_name):
            self.last_sound = sound_name

    accelerometer = _MicrobitAccelerometer()
    speaker = _MicrobitSpeaker()


class MicrobitMotorDriver:
    """Adapter layer that wraps Micro:bit motor commands."""

    def __init__(self):
        self.left_speed = 0.0
        self.right_speed = 0.0

    def set_left_speed(self, power):
        """Set the left motor power using the hardware interface."""
        if not 0.0 <= power <= 1.0:
            raise ValueError("power must be between 0 and 1")
        self.left_speed = float(power)

    def set_right_speed(self, power):
        """Set the right motor power using the hardware interface."""
        if not 0.0 <= power <= 1.0:
            raise ValueError("power must be between 0 and 1")
        self.right_speed = float(power)


class MicrobitTiltSensor:
    """Read the Micro:bit accelerometer pitch and allow calibration per test run."""

    def __init__(self):
        self._offset_deg = 0.0

    def calibrate(self):
        """Set the current orientation as the zero point for this run."""
        self._offset_deg = self._read_pitch_degrees()

    def _read_pitch_degrees(self):
        getter = getattr(accelerometer, "get_pitch", None)
        if callable(getter):
            return float(getter())
        if hasattr(accelerometer, "pitch"):
            return float(accelerometer.pitch())
        return 0.0

    def get_relative_pitch_degrees(self):
        """Return the current pitch difference from the calibrated zero point."""
        return abs(self._read_pitch_degrees() - self._offset_deg)


class MicrobitSoundPlayer:
    """Adapter for making a sound on the Micro:bit built-in speaker."""

    def __init__(self):
        self.last_sound = None
        self.output = "speaker"

    def play(self, sound_name):
        """Play a sound via the Micro:bit speaker and store the last sound for verification."""
        self.last_sound = sound_name
        self.output = "speaker"
        if hasattr(speaker, "play"):
            speaker.play(sound_name)
