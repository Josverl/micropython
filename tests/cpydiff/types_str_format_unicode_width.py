"""
categories: Types,str
description: String formatting does not account for Unicode character display width
cause: MicroPython treats all Unicode characters as having display width 1, while CPython accounts for East Asian Width properties where some characters (Wide and Fullwidth) occupy 2 terminal columns.
workaround: No direct workaround available. Applications that need proper terminal alignment with CJK and other wide characters should calculate display width separately using external logic.
"""

# Common emoji (takes 2 columns in terminal)
print("[{:5c}]".format(0x2764))  # ❤ heart - CPython: [    ❤] (3 spaces), MicroPython: [  ❤] (4 spaces)

# Japanese character (takes 2 columns)
print("[{:6c}]".format(0x3042))  # あ hiragana A - CPython: [     あ] (4 spaces), MicroPython: [   あ] (5 spaces)

# Chinese character (takes 2 columns)  
print("[{:6c}]".format(0x4E2D))  # 中 "middle/China" - CPython: [     中] (4 spaces), MicroPython: [   中] (5 spaces)

# Latin with diacritics - shows MicroPython counts UTF-8 bytes instead of characters
print("[{:10}]".format("Frühstück"))  # 9 chars, 11 bytes - CPython: [Frühstück ] (1 space), MicroPython: [Frühstück] (no space)

# Regular ASCII character for comparison
print("[{:5c}]".format(ord('A')))  # Both: [    A] (4 spaces)
