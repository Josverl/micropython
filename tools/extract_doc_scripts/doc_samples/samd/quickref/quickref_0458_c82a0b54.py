# Source: samd\quickref.rst:458
# Type: code_block

import time, ds18x20
from onewire import OneWire
from machine import Pin

ow = OneWire(Pin(4, Pin.OUT))
ds = ds18x20.DS18X20(ow)
roms = ds.scan()
ds.convert_temp()
time.sleep_ms(750)
for rom in roms:
    print(ds.read_temp(rom))
