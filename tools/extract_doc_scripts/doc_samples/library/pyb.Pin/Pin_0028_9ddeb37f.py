# Source: library\pyb.Pin.rst:28
# Type: code_block

MyMapperDict = {"LeftMotorDir": pyb.Pin.cpu.C12}
pyb.Pin.dict(MyMapperDict)
g = pyb.Pin("LeftMotorDir", pyb.Pin.OUT_OD)
