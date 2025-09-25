# Source: library\pyb.UART.rst:25
# Type: code_block

from machine import UART

uart = UART(1, 9600)
buf = bytearray(100)

uart.read(10)  # read 10 characters, returns a bytes object
uart.read()  # read all available characters
uart.readline()  # read a line
uart.readinto(buf)  # read and store into the given buffer
uart.write("abc")  # write the 3 characters
