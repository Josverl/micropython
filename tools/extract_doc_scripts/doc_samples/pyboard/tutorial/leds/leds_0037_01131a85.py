# Source: pyboard\tutorial\leds.rst:37
# Type: code_block

n = 0
while True:
    n = (n + 1) % 4
    leds[n].toggle()
    pyb.delay(50)
