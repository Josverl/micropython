# Source: zephyr\tutorial\pins.rst:9
# Type: code_block
from machine import Pin

LED = Pin(("GPIO_1", 22), Pin.OUT)
