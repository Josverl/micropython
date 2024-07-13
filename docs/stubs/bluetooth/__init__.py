"""
This module provides an interface to a Bluetooth controller on a board.
Currently this supports Bluetooth Low Energy (BLE) in Central, Peripheral,
Broadcaster, and Observer roles, as well as GATT Server and Client and L2CAP
connection-oriented-channels. A device may operate in multiple roles
concurrently. Pairing (and bonding) is supported on some ports.

This API is intended to match the low-level Bluetooth protocol and provide
building-blocks for higher-level abstractions such as specific device types.
"""

from .ble import BLE
from .uuid import UUID
