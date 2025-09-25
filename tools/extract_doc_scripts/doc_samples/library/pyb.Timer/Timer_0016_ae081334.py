# Source: library\pyb.Timer.rst:16
# Type: code_block

tim = pyb.Timer(4)  # create a timer object using timer 4
tim.init(freq=2)  # trigger at 2Hz
tim.callback(lambda t: pyb.LED(1).toggle())
