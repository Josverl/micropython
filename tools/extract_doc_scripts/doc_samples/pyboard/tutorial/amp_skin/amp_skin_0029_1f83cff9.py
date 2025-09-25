# Source: pyboard\tutorial\amp_skin.rst:29
# Type: code_block

import pyb


def volume(val):
    pyb.I2C(1, pyb.I2C.CONTROLLER).mem_write(val, 46, 0)
