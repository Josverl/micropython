# Source: library\pyb.ADC.rst:164
# Type: code_block

adcall = pyb.ADCAll(12, 0x70000)  # 12 bit resolution, internal channels
temp = adcall.read_core_temp()
