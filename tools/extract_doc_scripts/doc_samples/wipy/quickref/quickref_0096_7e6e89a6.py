# Source: wipy\quickref.rst:96
# Type: code_block

from machine import UART

uart = UART(0, baudrate=9600)
uart.write("hello")
uart.read(5)  # read up to 5 bytes
