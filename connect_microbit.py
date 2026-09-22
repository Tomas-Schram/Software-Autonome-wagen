#!/usr/bin/env python3
"""Attempt to connect to a Micro:Bit on a specific I2C bus/device."""

from __future__ import annotations

import sys

try:
    import smbus2 as smbus
except ImportError:  # pragma: no cover
    try:
        import smbus  # type: ignore
    except ImportError:  # pragma: no cover
        smbus = None


def probe_i2c(bus_num: int = 1, device_addr: int = 3) -> None:
    """Read a byte from a device on the given I2C bus.

    Micro:Bit boards are not always exposed as an I2C device at the same address,
    so this script is helpful for probing the configured bus/device.
    """
    if smbus is None:
        raise RuntimeError(
            "No I2C Python module is installed. Install smbus2 or smbus first."
        )

    bus = smbus.SMBus(bus_num)
    try:
        value = bus.read_byte(device_addr)
        print(f"Connected successfully to bus {bus_num}, device {device_addr}.")
        print(f"Byte read: {value}")
    except Exception as exc:  # pragma: no cover
        print(f"Connection failed on bus {bus_num}, device {device_addr}: {exc}")
        raise
    finally:
        bus.close()


if __name__ == "__main__":
    bus_num = 1
    device_addr = 3

    print(f"Probing Micro:Bit on I2C bus {bus_num}, device {device_addr}...")
    try:
        probe_i2c(bus_num, device_addr)
        sys.exit(0)
    except Exception as exc:  # pragma: no cover
        print(f"Unable to connect: {exc}")
        sys.exit(1)
