.. currentmodule:: machine
.. _machine.TouchPad:

class TouchPad  -- capacitive touch sensor
==========================================

The ``TouchPad`` class provides access to the capacitive touch sensor 
hardware on the ESP32, ESP32-S2 and ESP32-S3.
Example::

    from machine import TouchPad, Pin

    t = TouchPad(Pin(14))
    t.read()              # Returns a smaller or larger number when touched


Constructors
------------

.. class:: TouchPad(pin)

   Create a new TouchPad object associated with the given pin. The pin must be one of the touch-capable pins on the ESP32.

   Availability: esp32

Methods
-------

.. method:: TouchPad.config(value)

   Configure the touchpad sensitivity. The *value* parameter is hardware-specific.

   Availability: esp32

.. method:: TouchPad.read()

   Read the current value of the touch sensor. Returns an integer representing the touch sensor reading.

    The value is proportional to the capacitance between the pin and the board's Ground connection. 
    On ESP32 the number becomes smaller when the pin (or connected touch pad) is touched, on ESP32-S2 
    and ESP32-S3 the number becomes larger when the pin is touched.

    In all cases, a touch causes a significant change in the return value. Note the
    returned values are *relative* and can vary depending on the board and
    surrounding environment so some calibration (i.e. comparison to a baseline or
    rolling average) may be required.

    Availability: esp32
