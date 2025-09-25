# Source: pyboard\tutorial\leds.rst:66
# Type: code_block

led = pyb.LED(4)
intensity = 0
while True:
    intensity = (intensity + 1) % 255
    led.intensity(intensity)
    pyb.delay(20)
