# Source: pyboard\tutorial\lcd_skin.rst:34
# Type: code_block

import pyb

lcd = pyb.LCD("X")
lcd.light(True)
for x in range(-80, 128):
    lcd.fill(0)
    lcd.text("Hello uPy!", x, 10, 1)
    lcd.show()
    pyb.delay(25)
