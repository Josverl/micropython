"""
functions related to the hardware. See: https://docs.micropython.org/en/latest/library/machine.html

The ``machine`` module contains specific functions related to the hardware
on a particular board. Most functions in this module allow to achieve direct
and unrestricted access to and control of hardware blocks on a system
(like CPU, timers, buses, etc.). Used incorrectly, this can lead to
malfunction, lockups, crashes of your board, and in extreme cases, hardware
damage.
"""

# source version: latest
# origin module:: /home/jimmo/src/github.com/micropython/micropython3/docs/library/machine.rst
# + module: machine.Pin.rst
# + module: machine.Signal.rst
# + module: machine.ADC.rst
# + module: machine.ADCBlock.rst
# + module: machine.PWM.rst
# + module: machine.UART.rst
# + module: machine.SPI.rst
# + module: machine.I2C.rst
# + module: machine.I2S.rst
# + module: machine.RTC.rst
# + module: machine.Timer.rst
# + module: machine.WDT.rst
# + module: machine.SD.rst
# + module: machine.SDCard.rst
from typing import Any, Callable, List, NoReturn, Optional, Tuple, Union

mem8: Any = ...
"""Read/write 8 bits of memory."""
mem16: Any = ...
"""Read/write 16 bits of memory."""
mem32: int = 1
"""\
Read/write 32 bits of memory.

Use subscript notation ``[...]`` to index these objects with the address of
interest. Note that the address is the byte address, regardless of the size of
memory being accessed.

Example use (registers are specific to an stm32 microcontroller):
"""
IDLE: Any = ...
"""IRQ wake values."""
SLEEP: Any = ...
"""IRQ wake values."""
DEEPSLEEP: Any = ...
"""IRQ wake values."""
PWRON_RESET: Any = ...
"""Reset causes."""
HARD_RESET: Any = ...
"""Reset causes."""
WDT_RESET: Any = ...
"""Reset causes."""
DEEPSLEEP_RESET: Any = ...
"""Reset causes."""
SOFT_RESET: Any = ...
"""Reset causes."""
WLAN_WAKE: Any = ...
"""Wake-up reasons."""
PIN_WAKE: Any = ...
"""Wake-up reasons."""
RTC_WAKE: Any = ...
"""Wake-up reasons."""

from .pin import Pin
from .signal import Signal
from .adc import ADC, ADCBlock
from .pwm import PWM
from .uart import UART
from .spi import SPI, SoftSPI
from .i2c import I2C, SoftI2C
from .i2s import I2S
from .rtc import RTC
from .timer import Timer
from .wdt import WDT
from .sdcard import SD, SDCard

def reset() -> NoReturn:
    """
    Resets the device in a manner similar to pushing the external RESET
    button.
    """
    ...

def soft_reset() -> NoReturn:
    """
    Performs a soft reset of the interpreter, deleting all Python objects and
    resetting the Python heap.  It tries to retain the method by which the user
    is connected to the MicroPython REPL (eg serial, USB, Wifi).
    """
    ...

def reset_cause() -> int:
    """
    Get the reset cause. See :ref:`constants <machine_constants>` for the possible return values.
    """
    ...

def bootloader(value: Optional[Any] = None) -> None:
    """
    Reset the device and enter its bootloader.  This is typically used to put the
    device into a state where it can be programmed with new firmware.

    Some ports support passing in an optional *value* argument which can control
    which bootloader to enter, what to pass to it, or other things.
    """
    ...

def disable_irq() -> Any:
    """
    Disable interrupt requests.
    Returns the previous IRQ state which should be considered an opaque value.
    This return value should be passed to the `enable_irq()` function to restore
    interrupts to their original state, before `disable_irq()` was called.
    """
    ...

def enable_irq(state) -> Any:
    """
    Re-enable interrupt requests.
    The *state* parameter should be the value that was returned from the most
    recent call to the `disable_irq()` function.
    """
    ...

def freq(hz: Optional[Any] = None) -> Any:
    """
    Returns the CPU frequency in hertz.

    On some ports this can also be used to set the CPU frequency by passing in *hz*.
    """
    ...

def idle() -> Any:
    """
    Gates the clock to the CPU, useful to reduce power consumption at any time during
    short or long periods. Peripherals continue working and execution resumes as soon
    as any interrupt is triggered (on many ports this includes system timer
    interrupt occurring at regular intervals on the order of millisecond).
    """
    ...

def sleep() -> Any:
    """
    ``Note:`` This function is deprecated, use `lightsleep()` instead with no arguments.
    """
    ...

def lightsleep(time_ms: Optional[Any] = None) -> Any:
    """
    Stops execution in an attempt to enter a low power state.

    If *time_ms* is specified then this will be the maximum time in milliseconds that
    the sleep will last for.  Otherwise the sleep can last indefinitely.

    With or without a timeout, execution may resume at any time if there are events
    that require processing.  Such events, or wake sources, should be configured before
    sleeping, like `Pin` change or `RTC` timeout.

    The precise behaviour and power-saving capabilities of lightsleep and deepsleep is
    highly dependent on the underlying hardware, but the general properties are:

    * A lightsleep has full RAM and state retention.  Upon wake execution is resumed
      from the point where the sleep was requested, with all subsystems operational.

    * A deepsleep may not retain RAM or any other state of the system (for example
      peripherals or network interfaces).  Upon wake execution is resumed from the main
      script, similar to a hard or power-on reset. The `reset_cause()` function will
      return `machine.DEEPSLEEP` and this can be used to distinguish a deepsleep wake
      from other resets.
    """
    ...

def deepsleep(time_ms: Optional[Any] = None) -> NoReturn:
    """
    Stops execution in an attempt to enter a low power state.

    If *time_ms* is specified then this will be the maximum time in milliseconds that
    the sleep will last for.  Otherwise the sleep can last indefinitely.

    With or without a timeout, execution may resume at any time if there are events
    that require processing.  Such events, or wake sources, should be configured before
    sleeping, like `Pin` change or `RTC` timeout.

    The precise behaviour and power-saving capabilities of lightsleep and deepsleep is
    highly dependent on the underlying hardware, but the general properties are:

    * A lightsleep has full RAM and state retention.  Upon wake execution is resumed
      from the point where the sleep was requested, with all subsystems operational.

    * A deepsleep may not retain RAM or any other state of the system (for example
      peripherals or network interfaces).  Upon wake execution is resumed from the main
      script, similar to a hard or power-on reset. The `reset_cause()` function will
      return `machine.DEEPSLEEP` and this can be used to distinguish a deepsleep wake
      from other resets.
    """
    ...

def wake_reason() -> Any:
    """
    Get the wake reason. See :ref:`constants <machine_constants>` for the possible return values.

    Availability: ESP32, WiPy.
    """
    ...

def unique_id() -> bytes:
    """
    Returns a byte string with a unique identifier of a board/SoC. It will vary
    from a board/SoC instance to another, if underlying hardware allows. Length
    varies by hardware (so use substring of a full value if you expect a short
    ID). In some MicroPython ports, ID corresponds to the network MAC address.
    """
    ...

def time_pulse_us(pin, pulse_level, timeout_us=1000000, /) -> int:
    """
    Time a pulse on the given *pin*, and return the duration of the pulse in
    microseconds.  The *pulse_level* argument should be 0 to time a low pulse
    or 1 to time a high pulse.

    If the current input value of the pin is different to *pulse_level*,
    the function first (*) waits until the pin input becomes equal to *pulse_level*,
    then (**) times the duration that the pin is equal to *pulse_level*.
    If the pin is already equal to *pulse_level* then timing starts straight away.

    The function will return -2 if there was timeout waiting for condition marked
    (*) above, and -1 if there was timeout during the main measurement, marked (**)
    above. The timeout is the same for both cases and given by *timeout_us* (which
    is in microseconds).
    """
    ...

def bitstream(pin, encoding, timing, data, /) -> Any:
    """
    Transmits *data* by bit-banging the specified *pin*. The *encoding* argument
    specifies how the bits are encoded, and *timing* is an encoding-specific timing
    specification.

    The supported encodings are:

      - ``0`` for "high low" pulse duration modulation. This will transmit 0 and
        1 bits as timed pulses, starting with the most significant bit.
        The *timing* must be a four-tuple of nanoseconds in the format
        ``(high_time_0, low_time_0, high_time_1, low_time_1)``. For example,
        ``(400, 850, 800, 450)`` is the timing specification for WS2812 RGB LEDs
        at 800kHz.

    The accuracy of the timing varies between ports. On Cortex M0 at 48MHz, it is
    at best +/- 120ns, however on faster MCUs (ESP8266, ESP32, STM32, Pyboard), it
    will be closer to +/-30ns.

    ``Note:`` For controlling WS2812 / NeoPixel strips, see the :mod:`neopixel`
       module for a higher-level API.
    """
    ...

def rng() -> int:
    """
    Return a 24-bit software generated random number.

    Availability: WiPy.
    """
    ...
