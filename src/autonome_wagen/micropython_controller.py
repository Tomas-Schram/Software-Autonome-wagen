"""Full MicroPython controller for the Micro:Bit robot runtime.

This file is intended to be flashed directly to the Micro:Bit as the robot's
controller. It is fully self-contained and does not depend on the host Python
package in this repository.
"""

from microbit import accelerometer, button_a, button_b, display, sleep, uart

DEFAULT_DRIVE = "default drive"
SAFE_MODE = "safe"


class VehicleState:
    def __init__(self, power=0.0, steering_angle_deg=0.0, mode=DEFAULT_DRIVE):
        self.power = float(power)
        self.steering_angle_deg = float(steering_angle_deg)
        self.mode = mode


class RobotController:
    def __init__(self, state=None):
        self.state = state or VehicleState()
        self.normal_power = 0.4
        self.boost_power = 0.8
        self.slow_power = 0.2

    def clamp_power(self, power):
        power = float(power)
        if power < 0.0:
            return 0.0
        if power > 1.0:
            return 1.0
        return power

    def drive_forward(self, power=None, boost_zone=False, slow_zone=False):
        if power is not None:
            target_power = self.clamp_power(power)
        elif boost_zone:
            target_power = self.boost_power
        elif slow_zone:
            target_power = self.slow_power
        else:
            target_power = self.normal_power

        self.state.mode = DEFAULT_DRIVE
        self.state.power = float(target_power)
        self.state.steering_angle_deg = 0.0
        return target_power

    def stop(self):
        self.state.mode = SAFE_MODE
        self.state.power = 0.0
        self.state.steering_angle_deg = 0.0
        return self.state

    def turn(self, direction):
        direction = str(direction).lower()
        if direction not in {"left", "right"}:
            direction = "left"

        self.state.mode = DEFAULT_DRIVE
        self.state.steering_angle_deg = -30.0 if direction == "left" else 30.0
        return direction

    def read_pitch(self):
        try:
            return float(accelerometer.get_pitch())
        except Exception:
            return 0.0

    def handle_obstacle(self, front_clear=True, turn_direction="left"):
        if front_clear:
            self.drive_forward()
            return "forward"

        self.stop()
        return self.turn(turn_direction)


controller = RobotController()


try:
    uart.init(baudrate=115200)
except Exception:
    pass


def send_status():
    try:
        uart.write(
            "mode="
            + str(controller.state.mode)
            + ";power="
            + str(controller.state.power)
            + ";steering="
            + str(controller.state.steering_angle_deg)
            + ";pitch="
            + str(controller.read_pitch())
            + "\n"
        )
    except Exception:
        pass


def main():
    display.show("M")
    controller.drive_forward(0.4)
    send_status()

    while True:
        if button_a.is_pressed() and button_b.is_pressed():
            controller.stop()
            display.show("S")
        elif button_a.is_pressed():
            controller.drive_forward(0.6)
            display.show("F")
        elif button_b.is_pressed():
            controller.turn("left")
            display.show("<")
        else:
            controller.drive_forward(0.3)
            display.show("D")

        send_status()
        sleep(200)


main()
