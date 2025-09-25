# Source: pyboard\tutorial\assembler.rst:71
# Type: code_block
# Platform: unix


@micropython.asm_thumb
def asm_add(r0, r1):
    add(r0, r0, r1)
