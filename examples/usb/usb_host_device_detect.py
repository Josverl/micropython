# USB Host - Simple Device Detection Example
#
# This example demonstrates using machine.USBHost to detect USB devices
# connected to an ESP32-S3 (or other supported board with USB OTG).
#
# Hardware Setup:
#   - ESP32-S3 board with USB OTG port (not the USB-UART port)
#   - USB OTG adapter cable (micro-USB or USB-C OTG, depending on board)
#   - A USB device to connect (keyboard, mouse, serial adapter, etc.)
#
# Note: USB host mode and USB device mode (machine.USBDevice / CDC serial)
# are mutually exclusive. When host mode is active, the USB port cannot be
# used for REPL. Use UART REPL or run this from boot.py.

import machine
import time


def on_connect(host):
    """Called when a USB device is connected and enumerated."""
    info = host.info()
    if info:
        print("USB device connected:")
        print(f"  VID:PID = {info['vid']:#06x}:{info['pid']:#06x}")
        print(f"  Speed:  {info['speed']}")
        if info["manufacturer"]:
            print(f"  Mfr:    {info['manufacturer']}")
        if info["product"]:
            print(f"  Product:{info['product']}")

        # Read the device descriptor via a control transfer
        try:
            desc = host.control_transfer(
                0x80,  # bmRequestType: IN, Standard, Device
                0x06,  # GET_DESCRIPTOR
                0x0100,  # Device descriptor, index 0
                0x0000,  # wIndex
                18,  # wLength (device descriptor = 18 bytes)
                timeout=2000,
            )
            print(f"  Descriptor: {desc.hex()}")
        except OSError as e:
            print(f"  Control transfer failed: {e}")
    else:
        print("USB device connected (no info available)")


def on_disconnect(host):
    """Called when the USB device is disconnected."""
    print("USB device disconnected")


def main():
    print("USB Host - Device Detection Example")
    print("====================================")

    host = machine.USBHost()

    host.config(
        connect_cb=on_connect,
        disconnect_cb=on_disconnect,
    )

    print("Activating USB host mode...")
    host.active(True)
    print("USB host active. Connect a USB device.")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nDeactivating USB host...")
        host.active(False)
        print("Done.")


if __name__ == "__main__":
    main()
