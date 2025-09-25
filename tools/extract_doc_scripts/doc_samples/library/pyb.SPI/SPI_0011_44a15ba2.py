# Source: library\pyb.SPI.rst:11
# Type: code_block

from pyb import SPI

spi = SPI(1, SPI.CONTROLLER, baudrate=600000, polarity=1, phase=0, crc=0x7)
