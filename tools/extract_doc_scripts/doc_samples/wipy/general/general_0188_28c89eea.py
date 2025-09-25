# Source: wipy\general.rst:188
# Type: code_block
# Platform: esp32

from machine import Pin

g = Pin("GP9", mode=Pin.OUT, pull=None, drive=Pin.MED_POWER, alt=-1)
