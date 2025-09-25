# Source: wipy\tutorial\timer.rst:11
# Type: code_block

from machine import Timer
from machine import Pin

led = Pin("GP16", mode=Pin.OUT)  # enable GP16 as output to drive the LED
tim = Timer(3)  # create a timer object using timer 3
tim.init(mode=Timer.PERIODIC)  # initialize it in periodic mode
tim_ch = tim.channel(Timer.A, freq=5)  # configure channel A at a frequency of 5Hz
tim_ch.irq(
    handler=lambda t: led.toggle(), trigger=Timer.TIMEOUT
)  # toggle a LED on every cycle of the timer
