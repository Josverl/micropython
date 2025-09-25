# Source: esp8266\quickref.rst:178
# Type: code_block

import os, machine

uart = machine.UART(0, 115200)
os.dupterm(uart, 1)
