# Source: library\pyb.rst:64
# Type: code_block

start = pyb.micros()
while pyb.elapsed_micros(start) < 1000:
    # Perform some operation
    pass
