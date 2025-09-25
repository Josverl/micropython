# Source: renesas-ra\tutorial\using_peripheral.rst:51
# Type: code_block
from machine import Pin

Pin(Pin.cpu.P106, mode=Pin.OUT, pull=Pin.PULL_NONE, drive=Pin.LOW_POWER)
