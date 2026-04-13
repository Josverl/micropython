.. currentmodule:: machine
.. _machine.USBHost:

class USBHost -- USB Host driver
================================

.. note:: ``machine.USBHost`` is currently only supported on the esp32 port
          (ESP32-S3, ESP32-S2, ESP32-P4 with USB OTG support).

USBHost provides a low-level Python API for USB host mode functionality.
When active, the USB OTG peripheral operates as a host controller, allowing
the microcontroller to communicate with connected USB devices such as
keyboards, serial adapters, and mass storage devices.

.. warning:: This is a low-level API that assumes familiarity with the USB
   standard. Higher-level class drivers (HID, CDC, MSC) will be provided in
   `micropython-lib`_ as installable packages that use this API.

.. warning:: USB host mode and USB device mode are mutually exclusive on
   hardware with a single USB OTG peripheral. Activating ``USBHost`` while
   ``USBDevice`` is active (or vice versa) will raise an error.

Terminology
-----------

- **Host mode**: The microcontroller acts as the USB host, providing power
  (VBUS) and initiating all communication with connected USB devices.

- **Device mode**: The microcontroller acts as a USB peripheral, responding
  to requests from an external USB host (e.g., a PC). This is the mode used
  by ``machine.USBDevice``.

- **OTG (On-The-Go)**: A USB specification that allows a single port to
  switch between host and device roles. The ESP32-S3 supports USB OTG with
  full-speed (12 Mbit/s) and low-speed (1.5 Mbit/s) data rates.

Constructors
------------

.. class:: USBHost()

   Construct a USBHost object.

   .. note:: This object is a singleton, each call to this constructor
             returns the same object reference.

Methods
-------

.. method:: USBHost.config(*, connect_cb=None, disconnect_cb=None, xfer_cb=None)

    Configures the ``USBHost`` singleton with callback functions:

    - ``connect_cb`` - Called when a USB device is connected and enumerated.
      The callback takes a single argument: the ``USBHost`` object.

      ::

          def on_connect(host):
              info = host.info()
              print("Connected:", info["product"])

    - ``disconnect_cb`` - Called when a USB device is disconnected. Takes a
      single argument: the ``USBHost`` object.

    - ``xfer_cb`` - Called when an asynchronous transfer (submitted via
      :func:`USBHost.submit_xfer`) completes. Takes a single argument: a
      3-tuple of ``(ep_addr, result, xferred_bytes)`` where ``result`` is
      ``True`` on success and ``False`` on error.

    Callbacks can be updated at any time by calling ``config()`` again with
    the new callback(s). Only the specified keyword arguments are updated;
    unspecified callbacks are left unchanged.

.. method:: USBHost.active([value])

    Returns the current active state of the USB host as a boolean.

    If the optional ``value`` argument is set to a truthy value, the USB host
    controller is activated. This initialises the USB PHY in host mode, starts
    VBUS power (if supported by the board), and begins listening for device
    connections.

    If the optional ``value`` argument is set to a falsey value, the USB host
    controller is deactivated and all resources are released.

    Raises ``OSError(ENODEV)`` if the hardware does not support USB host mode.

.. method:: USBHost.info()

    Returns a dictionary with information about the currently connected USB
    device, or ``None`` if no device is connected.

    The dictionary contains:

    - ``vid`` - USB Vendor ID (integer)
    - ``pid`` - USB Product ID (integer)
    - ``speed`` - Connection speed: ``"LS"`` (low-speed) or ``"FS"`` (full-speed)
    - ``manufacturer`` - Manufacturer string (may be empty)
    - ``product`` - Product string (may be empty)

    Raises ``OSError(EINVAL)`` if the USB host is not active.

.. method:: USBHost.control_transfer(bmRequestType, bRequest, wValue, wIndex, data_or_length, *, timeout=5000)

    Perform a blocking USB control transfer.

    - ``bmRequestType`` - Request type bitmap (direction, type, recipient)
    - ``bRequest`` - Request code
    - ``wValue`` - Value field
    - ``wIndex`` - Index field
    - ``data_or_length`` - For IN transfers (device-to-host), an integer
      specifying the maximum number of bytes to read. For OUT transfers
      (host-to-device), a bytes-like object containing data to send.
    - ``timeout`` - Timeout in milliseconds (default 5000)

    Returns ``bytes`` for IN transfers, or the number of bytes transferred
    for OUT transfers.

    Raises ``OSError(EIO)`` if the transfer fails.
    Raises ``OSError(EINVAL)`` if the USB host is not active.

.. method:: USBHost.open_endpoint(ep_addr, ep_type, max_pkt_size)

    Open a USB endpoint for data transfers.

    - ``ep_addr`` - Endpoint address (bit 7 set for IN endpoints)
    - ``ep_type`` - Endpoint transfer type: ``USBHost.XFER_CONTROL``,
      ``USBHost.XFER_ISOCHRONOUS``, ``USBHost.XFER_BULK``, or
      ``USBHost.XFER_INTERRUPT``
    - ``max_pkt_size`` - Maximum packet size for the endpoint

    Raises ``OSError(EINVAL)`` if the USB host is not active.

.. method:: USBHost.close_endpoint(ep_addr)

    Close a previously opened endpoint.

    - ``ep_addr`` - Endpoint address to close

    Raises ``OSError(EINVAL)`` if the USB host is not active.

.. method:: USBHost.submit_xfer(ep_addr, buffer)

    Submit an asynchronous transfer on the specified endpoint.

    - ``ep_addr`` - Endpoint address. For IN endpoints (bit 7 set),
      ``buffer`` must be writable. For OUT endpoints, ``buffer`` must be
      readable.
    - ``buffer`` - Buffer for the transfer data.

    Returns ``True`` if the transfer was successfully queued.

    When the transfer completes, the ``xfer_cb`` callback (set via
    :func:`USBHost.config`) is invoked.

    Raises ``OSError(EINVAL)`` if the USB host is not active.

Constants
---------

.. data:: USBHost.XFER_CONTROL
.. data:: USBHost.XFER_ISOCHRONOUS
.. data:: USBHost.XFER_BULK
.. data:: USBHost.XFER_INTERRUPT

    USB endpoint transfer type constants, used with :func:`USBHost.open_endpoint`.

Example
-------

Basic device detection::

    import machine

    host = machine.USBHost()

    def on_connect(host):
        info = host.info()
        if info:
            print(f"Connected: VID={info['vid']:#06x} PID={info['pid']:#06x}")
            print(f"  Speed: {info['speed']}")

    def on_disconnect(host):
        print("Device disconnected")

    host.config(connect_cb=on_connect, disconnect_cb=on_disconnect)
    host.active(True)

Control transfer to read a device descriptor::

    import machine

    host = machine.USBHost()
    host.active(True)

    # Standard GET_DESCRIPTOR request for device descriptor
    desc = host.control_transfer(
        0x80,   # bmRequestType: Device-to-host, Standard, Device
        0x06,   # bRequest: GET_DESCRIPTOR
        0x0100, # wValue: Descriptor type (Device) and index
        0x0000, # wIndex: Zero
        18,     # wLength: Device descriptor is 18 bytes
        timeout=5000
    )
    print("Device descriptor:", desc)

.. _micropython-lib: https://github.com/micropython/micropython-lib/tree/master/micropython/usb#readme
