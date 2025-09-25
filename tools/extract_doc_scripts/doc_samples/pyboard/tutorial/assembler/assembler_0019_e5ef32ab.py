# Source: pyboard\tutorial\assembler.rst:19
# Type: code_block
# Platform: unix
import micropython


@micropython.asm_thumb
def fun():
    movw(r0, 42)
