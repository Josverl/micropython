# Source: library\network.WIZNET5K.rst:50
# Type: code_block
# Platform: esp32
import network

nic = network.WIZNET5K(pyb.SPI(1), pyb.Pin.board.X5, pyb.Pin.board.X4)
