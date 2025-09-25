# Source: library\pyb.I2C.rst:31
# Type: code_block

data = bytearray(3)  # create a buffer
i2c.recv(data)  # receive 3 bytes, writing them into data
