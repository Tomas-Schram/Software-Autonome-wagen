import pytest

from autonome_wagen.core import AutonomeWagen, DrivingMode
from autonome_wagen.control.controller import VehicleController
from autonome_wagen.hardware.motors import MotorDriver
from autonome_wagen.hardware.sensors import LineSensor, UltrasonicSensor
from autonome_wagen.hardware.microbit import MicrobitMotorDriver, MicrobitSoundPlayer
from autonome_wagen.navigation.maze import MazeNavigator
from autonome_wagen.navigation.open_space import OpenSpaceNavigator
from autonome_wagen.safety.barrier import BarrierController, SoundController
from autonome_wagen.safety.slope import SlopeDetector


def test_default_state_is_safe_and_stopped() -> None:
    car = AutonomeWagen()

    assert car.state.power == 0.0
    assert car.state.steering_angle_deg == 0.0
    assert car.state.mode == DrivingMode.SAFE


def test_set_speed_validates_power_percentage_range() -> None:
    car = AutonomeWagen()

    car.set_speed(0.75)
    assert car.state.power == 0.75

    with pytest.raises(ValueError, match="between 0 and 1"):
        car.set_speed(-0.1)

    with pytest.raises(ValueError, match="between 0 and 1"):
        car.set_speed(1.5)


def test_motor_driver_tracks_left_and_right_speed() -> None:
    motor_driver = MotorDriver()

    motor_driver.set_left_speed(0.6)
    motor_driver.set_right_speed(0.4)

    assert motor_driver.left_speed == 0.6
    assert motor_driver.right_speed == 0.4


def test_motor_driver_pin_configuration_is_changeable() -> None:
    motor_driver = MotorDriver()

    motor_driver.configure_pins(
        left_enable_pin=9,
        right_enable_pin=10,
        left_direction_pin=11,
        right_direction_pin=12,
    )

    assert motor_driver.left_enable_pin == 9
    assert motor_driver.right_enable_pin == 10
    assert motor_driver.left_direction_pin == 11
    assert motor_driver.right_direction_pin == 12


def test_ultrasonic_sensor_reads_distance_and_detects_obstacle() -> None:
    sensor = UltrasonicSensor(threshold_cm=20)
    sensor.distance_cm = 15

    assert sensor.distance_cm == 15
    assert sensor.has_obstacle() is True


def test_vehicle_controller_stops_when_obstacle_detected() -> None:
    car = AutonomeWagen(initial_mode=DrivingMode.AUTONOMOUS)
    controller = VehicleController(car)

    controller.drive_forward(0.25)
    result = controller.handle_obstacle(front_clear=False, turn_direction="left")

    assert result == "left"
    assert car.state.mode == DrivingMode.SAFE
    assert car.state.power == 0.0
    assert car.state.steering_angle_deg < 0.0


def test_vehicle_controller_uses_standard_driving_power_and_zone_variants() -> None:
    car = AutonomeWagen(initial_mode=DrivingMode.AUTONOMOUS)
    controller = VehicleController(car)

    controller.drive_forward()
    assert car.state.power == 0.4

    controller.drive_forward(boost_zone=True)
    assert car.state.power == 0.8

    controller.drive_forward(slow_zone=True)
    assert car.state.power == 0.2


def test_maze_navigator_decides_turn_from_sensor_readings() -> None:
    navigator = MazeNavigator()

    assert navigator.decide_turn(left=True, center=False, right=False) == "left"
    assert navigator.decide_turn(left=False, center=True, right=False) == "forward"
    assert navigator.decide_turn(left=False, center=False, right=True) == "right"


def test_line_sensor_reports_binary_reading() -> None:
    sensor = LineSensor()
    sensor.values = {"left": True, "center": False, "right": True}

    assert sensor.is_on_line() is True
    assert sensor.left is True
    assert sensor.right is True

    with pytest.raises(ValueError, match="non-negative"):
        sensor.set_threshold(-5)


def test_slope_detector_identifies_decline_and_reduces_speed() -> None:
    detector = SlopeDetector(threshold_deg=8.0)
    detector.pitch_angle_deg = 12.0

    assert detector.is_on_slope() is True
    assert detector.recommended_speed_factor() == 0.5


def test_barrier_controller_stops_and_plays_sound_on_slagboom() -> None:
    sound_controller = SoundController()
    barrier = BarrierController(sound_controller)

    result = barrier.handle_slagboom()

    assert result["state"] == "stopped"
    assert result["sound"] == "beep"
    assert sound_controller.last_sound == "beep"


def test_open_space_navigator_chooses_open_path_without_line() -> None:
    navigator = OpenSpaceNavigator()

    assert navigator.choose_direction(front_clear=True, left_clear=False, right_clear=False) == "forward"
    assert navigator.choose_direction(front_clear=False, left_clear=True, right_clear=False) == "left"
    assert navigator.choose_direction(front_clear=False, left_clear=False, right_clear=True) == "right"


def test_microbit_motor_driver_wraps_hardware_commands() -> None:
    adapter = MicrobitMotorDriver()

    adapter.set_left_speed(0.8)
    adapter.set_right_speed(0.3)

    assert adapter.left_speed == 0.8
    assert adapter.right_speed == 0.3


def test_microbit_sound_player_calls_beep_method() -> None:
    player = MicrobitSoundPlayer()

    player.play("beep")

    assert player.last_sound == "beep"
