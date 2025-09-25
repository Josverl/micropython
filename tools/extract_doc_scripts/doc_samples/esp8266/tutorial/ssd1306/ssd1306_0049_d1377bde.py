# Source: esp8266\tutorial\ssd1306.rst:49
# Type: code_block

display.poweroff()  # power off the display, pixels persist in memory
display.poweron()  # power on the display, pixels redrawn
display.contrast(0)  # dim
display.contrast(255)  # bright
display.invert(1)  # display inverted
display.invert(0)  # display normal
display.rotate(True)  # rotate 180 degrees
display.rotate(False)  # rotate 0 degrees
display.show()  # write the contents of the FrameBuffer to display memory
