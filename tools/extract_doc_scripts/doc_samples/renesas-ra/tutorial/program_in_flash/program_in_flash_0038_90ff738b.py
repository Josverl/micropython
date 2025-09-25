# Source: renesas-ra\tutorial\program_in_flash.rst:38
# Type: code_block

import os

os.getcwd()
f = open("main.py", "rw+")
print(f.read())
f.write("import time\n")
f.write("from machine import Pin\n")
f.write("led1 = Pin(Pin.cpu.P106)\n")
f.write("while True:\n")
f.write("    led1.on()\n")
f.write("    time.sleep(1)\n")
f.write("    led1.off()\n")
f.write("    time.sleep(1)\n")
f.close()
f = open("main.py", "r")
print(f.read())
f.close()
