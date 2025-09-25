# Source: esp32\tutorial\pwm.rst:14
# Type: code_block

from time import sleep
from machine import Pin, PWM

try:
    F = 10000  # Hz
    D = 65536 // 16  # 6.25%
    pins = (2, 4, 12, 13, 14, 15, 16, 18, 19, 22, 23, 25, 26, 27, 32, 33)
    pwms = []
    for i, pin in enumerate(pins):
        f = F * (i // 2 + 1)
        d = min(65535, D * (i + 1))
        pwms.append(PWM(pin, freq=f, duty_u16=d))
        sleep(2 / f)
        print(pwms[i])
finally:
    for pwm in pwms:
        try:
            pwm.deinit()
        except:
            pass
