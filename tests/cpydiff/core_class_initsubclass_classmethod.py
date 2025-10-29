"""
categories: Core,Classes
description: __init_subclass__ does not support explicit @classmethod decorator
cause: PEP 487 specifies that __init_subclass__ is implicitly a classmethod. MicroPython's optimized implementation does not support the explicit @classmethod decorator (which is redundant per PEP 487).
workaround: Do not use @classmethod decorator on __init_subclass__. It is implicitly a classmethod and does not need the decorator.
"""

# This works in CPython but not in MicroPython
try:
    class Base:
        @classmethod
        def __init_subclass__(cls):
            cls.marker = True
    
    class Derived(Base):
        pass
    
    print(f"Derived.marker = {Derived.marker}")
except TypeError:
    print("TypeError: @classmethod decorator not supported on __init_subclass__")
