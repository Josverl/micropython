# Source: library\machine.PWM.rst:121
# Type: code_block

pwm = PWM(Pin(13), freq=300_000, duty_u16=65536 // 2 + 255)
