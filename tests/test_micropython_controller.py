from autonome_wagen.micropython_controller import (
    DEFAULT_DRIVE,
    RobotController,
    VehicleState,
    main,
)


def test_default_drive_is_available_in_micropython_controller() -> None:
    assert DEFAULT_DRIVE == "default drive"


def test_robot_controller_uses_default_drive_mode() -> None:
    controller = RobotController()
    controller.drive_forward(0.35)

    assert controller.state.mode == "default drive"
    assert controller.state.power == 0.35


def test_main_function_is_callable() -> None:
    assert callable(main)
    assert isinstance(VehicleState(), VehicleState)
