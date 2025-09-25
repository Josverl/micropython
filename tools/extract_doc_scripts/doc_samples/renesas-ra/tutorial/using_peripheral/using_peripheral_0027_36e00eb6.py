# Source: renesas-ra\tutorial\using_peripheral.rst:27
# Type: code_block

import time
from machine import Pin

led1 = Pin("LED1")
print(led1)
while True:
    led1.on()
    time.sleep(1)
    led1.off()
    time.sleep(1)
