# Source: wipy\quickref.rst:120
# Type: code_block

from machine import I2C

# configure the I2C bus
i2c = I2C(baudrate=100000)
i2c.scan()  # returns list of peripheral addresses
i2c.writeto(0x42, "hello")  # send 5 bytes to peripheral with address 0x42
i2c.readfrom(0x42, 5)  # receive 5 bytes from peripheral
i2c.readfrom_mem(0x42, 0x10, 2)  # read 2 bytes from peripheral 0x42, peripheral memory 0x10
i2c.writeto_mem(0x42, 0x10, "xy")  # write 2 bytes to peripheral 0x42, peripheral memory 0x10
