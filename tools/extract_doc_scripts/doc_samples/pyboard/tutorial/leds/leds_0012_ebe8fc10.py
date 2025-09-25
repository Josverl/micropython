# Source: pyboard\tutorial\leds.rst:12
# Type: code_block

led = pyb.LED(2)
while True:
    led.toggle()
    pyb.delay(1000)
