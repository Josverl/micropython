# Source: library\machine.SD.rst:20
# Type: code_block

from machine import SD
import vfs

# clk cmd and dat0 pins must be passed along with
# their respective alternate functions
sd = machine.SD(pins=("GP10", "GP11", "GP15"))
vfs.mount(sd, "/sd")
# do normal file operations
