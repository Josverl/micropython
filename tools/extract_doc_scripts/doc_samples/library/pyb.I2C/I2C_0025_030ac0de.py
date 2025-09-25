# Source: library\pyb.I2C.rst:25
# Type: code_block

i2c.send("abc")  # send 3 bytes
i2c.send(0x42)  # send a single byte, given by the number
data = i2c.recv(3)  # receive 3 bytes
