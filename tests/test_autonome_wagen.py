import pytest

from autonome_wagen.core import AutonomeWagen, DrivingMode
from autonome_wagen.control.controller import AutonomousDriveLoop, VehicleController
from autonome_wagen.hardware import (
    DriverBoardConfig,
    MicrobitButtonSensor,
    MicrobitCompassSensor,
    MicrobitMotionSensor,
    MicrobitTemperatureSensor,
    MicrobitTiltSensor as ExportedMicrobitTiltSensor,
)
from autonome_wagen.hardware.motors import MotorDriver
from autonome_wagen.hardware.sensors import LineSensor, UltrasonicSensor
from autonome_wagen.hardware.microbit import MicrobitMotorDriver, MicrobitSoundPlayer, MicrobitTiltSensor
from autonome_wagen.navigation.maze import MazeNavigator
from autonome_wagen.navigation.open_space import OpenSpaceNavigator
from autonome_wagen.safety.barrier import BarrierController, SoundController
from autonome_wagen.safety.slope import SlopeDetector


def test_default_state_is_safe_and_stopped() -> None:
    car = AutonomeWagen()

    assert car.state.power == 0.0
    assert car.state.steering_angle_deg == 0.0
    assert car.state.mode == DrivingMode.SAFE
    assert hasattr(DrivingMode, "AUTONOMOUS")
    assert not hasattr(DrivingMode, "MANUAL")


def test_default_drive_mode_is_named_default_drive() -> None:
    assert DrivingMode.DEFAULT_DRIVE.value == "default drive"
    assert DrivingMode.AUTONOMOUS.value == "default drive"


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


def test_driver_board_config_can_be_used_as_a_single_hardware_contract() -> None:
    config = DriverBoardConfig(
        left_enable_pin=17,
        right_enable_pin=18,
        left_direction_pin=19,
        right_direction_pin=20,
    )

    motor_driver = MotorDriver(config=config)

    assert motor_driver.config == config
    assert motor_driver.left_enable_pin == 17
    assert motor_driver.right_enable_pin == 18
    assert motor_driver.left_direction_pin == 19
    assert motor_driver.right_direction_pin == 20


def test_microbit_sensor_adapters_use_hardware_calls_when_available(monkeypatch) -> None:
    import autonome_wagen.hardware.sensors as sensors

    class FakeAccelerometer:
        def __init__(self):
            self._pitch = 0.0
            self._roll = 0.0

        def get_pitch(self):
            return self._pitch

        def get_roll(self):
            return self._roll

        def set_state(self, pitch, roll):
            self._pitch = pitch
            self._roll = roll

    class FakeCompass:
        def heading(self):
            return 90.0

        def calibrate(self):
            return "calibrated"

    class FakeButton:
        def __init__(self, pressed):
            self._pressed = pressed

        def is_pressed(self):
            return self._pressed

    fake_accelerometer = FakeAccelerometer()
    monkeypatch.setattr(sensors, "accelerometer", fake_accelerometer)
    monkeypatch.setattr(sensors, "compass", FakeCompass())
    monkeypatch.setattr(sensors, "button_a", FakeButton(True))
    monkeypatch.setattr(sensors, "button_b", FakeButton(False))
    monkeypatch.setattr(sensors, "temperature", lambda: 21)

    fake_accelerometer.set_state(0.0, 0.0)
    motion = MicrobitMotionSensor()
    motion.calibrate()

    fake_accelerometer.set_state(18.0, 12.0)

    assert motion.get_pitch() == pytest.approx(18.0)
    assert motion.get_roll() == pytest.approx(12.0)
    assert motion.is_tilted(threshold_deg=10) is True

    compass = MicrobitCompassSensor()
    assert compass.get_heading() == pytest.approx(90.0)
    assert compass.is_ready() is True

    temp = MicrobitTemperatureSensor()
    assert temp.read_celsius() == 21
    assert temp.read_fahrenheit() == pytest.approx(69.8)

    left_button = MicrobitButtonSensor("left")
    right_button = MicrobitButtonSensor("right")
    assert left_button.is_pressed() is True
    assert right_button.is_pressed() is False


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
    detector.calibrate(0.0)
    detector.update_pitch(18.0)

    assert detector.is_on_slope() is True
    assert detector.recommended_speed_factor() == pytest.approx(0.5)


def test_vehicle_controller_reduces_power_on_slope() -> None:
    car = AutonomeWagen(initial_mode=DrivingMode.AUTONOMOUS)
    controller = VehicleController(car)
    detector = SlopeDetector(threshold_deg=8.0)
    detector.calibrate(0.0)
    detector.update_pitch(18.0)

    assert controller.apply_slope_limit(0.8, detector) == pytest.approx(0.4)


def test_slope_detector_calibrates_on_startup() -> None:
    detector = SlopeDetector(threshold_deg=8.0)
    detector.calibrate(5.0)
    detector.update_pitch(12.0)

    assert detector.pitch_angle_deg == 7.0
    assert detector.is_on_slope() is False

    detector.update_pitch(18.0)
    assert detector.is_on_slope() is True


def test_slope_detector_uses_microbit_tilt_sensor_when_provided(monkeypatch) -> None:
    class FakeAccelerometer:
        def __init__(self, values):
            self._values = values
            self._index = 0

        def get_pitch(self):
            value = self._values[self._index]
            self._index = min(self._index + 1, len(self._values) - 1)
            return value

    sensor = MicrobitTiltSensor()
    detector = SlopeDetector(threshold_deg=8.0, tilt_sensor=sensor)

    from autonome_wagen.hardware import microbit

    monkeypatch.setattr(microbit, "accelerometer", FakeAccelerometer([0.0, 18.0]))

    detector.calibrate()
    detector.update_pitch()

    assert detector.pitch_angle_deg == pytest.approx(18.0)
    assert detector.is_on_slope() is True


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


def test_autonomous_drive_loop_runs_safe_slope_aware_cycle() -> None:
    car = AutonomeWagen(initial_mode=DrivingMode.AUTONOMOUS)
    controller = VehicleController(car)
    detector = SlopeDetector(threshold_deg=8.0)
    detector.calibrate(0.0)
    loop = AutonomousDriveLoop(car, controller=controller, slope_detector=detector)

    result = loop.run_cycle(front_clear=True, pitch_angle_deg=18.0)

    assert result == "forward"
    assert car.state.mode == DrivingMode.AUTONOMOUS
    assert car.state.power == pytest.approx(0.2)
    assert car.state.steering_angle_deg == 0.0

    detector.calibrate(0.0)
    result = loop.run_cycle(front_clear=False, turn_direction="right")

    assert result == "right"
    assert car.state.mode == DrivingMode.SAFE
    assert car.state.power == 0.0


def test_microbit_tilt_sensor_is_exposed_through_package_exports() -> None:
    assert ExportedMicrobitTiltSensor is MicrobitTiltSensor

    import autonome_wagen

    assert hasattr(autonome_wagen, "MicrobitTiltSensor")
    assert autonome_wagen.MicrobitTiltSensor is MicrobitTiltSensor
