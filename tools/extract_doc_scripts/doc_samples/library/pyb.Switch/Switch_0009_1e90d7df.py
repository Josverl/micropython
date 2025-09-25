# Source: library\pyb.Switch.rst:9
# Type: code_block

sw = pyb.Switch()  # create a switch object
sw.value()  # get state (True if pressed, False otherwise)
sw()  # shorthand notation to get the switch state
sw.callback(f)  # register a callback to be called when the
#   switch is pressed down
sw.callback(None)  # remove the callback
