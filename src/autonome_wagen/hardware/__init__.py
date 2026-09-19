"""Hardware interfaces for the Autonomous Wagen robot."""

from .microbit import MicrobitMotorDriver, MicrobitSoundPlayer, MicrobitTiltSensor
from .motors import DriverBoardConfig, MotorDriver
from .sensors import (
    LineSensor,
    MicrobitButtonSensor,
    MicrobitCompassSensor,
    MicrobitMotionSensor,
    MicrobitTemperatureSensor,
    UltrasonicSensor,
)

__all__ = [
    "MotorDriver",
    "DriverBoardConfig",
    "LineSensor",
    "UltrasonicSensor",
    "MicrobitMotionSensor",
    "MicrobitCompassSensor",
    "MicrobitTemperatureSensor",
    "MicrobitButtonSensor",
    "MicrobitMotorDriver",
    "MicrobitSoundPlayer",
    "MicrobitTiltSensor",
]
