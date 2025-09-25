# Source: samd\quickref.rst:383
# Type: code_block

from machine import SPI

spi = SPI()  # Use the default device and default baudrate
spi = SPI(baudrate=12_000_000)  # Use the default device and change the baudrate
