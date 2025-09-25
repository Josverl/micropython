# Source: library\machine.UART.rst:28
# Type: code_block

uart.read(10)  # read 10 characters, returns a bytes object
uart.read()  # read all available characters
uart.readline()  # read a line
uart.readinto(buf)  # read and store into the given buffer
uart.write("abc")  # write the 3 characters
