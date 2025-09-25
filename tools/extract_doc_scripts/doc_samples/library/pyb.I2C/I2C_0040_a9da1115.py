# Source: library\pyb.I2C.rst:40
# Type: code_block

i2c.init(I2C.CONTROLLER)
i2c.send("123", 0x42)  # send 3 bytes to peripheral with address 0x42
i2c.send(b"456", addr=0x42)  # keyword for address
