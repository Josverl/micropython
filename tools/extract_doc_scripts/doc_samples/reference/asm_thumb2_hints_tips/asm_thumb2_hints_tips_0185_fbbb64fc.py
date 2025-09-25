# Source: reference\asm_thumb2_hints_tips.rst:185
# Type: code_block
# Platform: unix
import micropython


class foo:
    @staticmethod
    @micropython.asm_thumb
    def bar(r0):
        add(r0, r0, r0)
