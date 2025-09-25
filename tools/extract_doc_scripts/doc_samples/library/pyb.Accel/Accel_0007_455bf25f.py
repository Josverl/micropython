# Source: library\pyb.Accel.rst:7
# Type: code_block

accel = pyb.Accel()
for i in range(10):
    print(accel.x(), accel.y(), accel.z())
