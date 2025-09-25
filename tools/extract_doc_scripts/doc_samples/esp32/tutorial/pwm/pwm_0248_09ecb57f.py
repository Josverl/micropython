# Source: esp32\tutorial\pwm.rst:248
# Type: code_block

pwm = PWM(Pin(5), freq=1000, duty=512)
pwm.init(freq=500, duty=256)
