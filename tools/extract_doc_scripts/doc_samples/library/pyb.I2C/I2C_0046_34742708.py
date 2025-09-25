# Source: library\pyb.I2C.rst:46
# Type: code_block

i2c.is_ready(0x42)  # check if peripheral 0x42 is ready
i2c.scan()  # scan for peripherals on the bus, returning
#   a list of valid addresses
i2c.mem_read(3, 0x42, 2)  # read 3 bytes from memory of peripheral 0x42,
#   starting at address 2 in the peripheral
i2c.mem_write("abc", 0x42, 2, timeout=1000)  # write 'abc' (3 bytes) to memory of peripheral 0x42
# starting at address 2 in the peripheral, timeout after 1 second
