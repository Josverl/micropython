# This doesn't quite test everything but just serves to verify that basic syntax works,
# which for MicroPython means everything typing-related should be ignored.

try:
    import typing
except ImportError:
    print("SKIP")
    raise SystemExit

import unittest

from typing import List, Tuple, Iterable, NewType, TypeVar, Union, Generic
from typing import Any

# Available with MICROPY_PY_TYPING_EXTRA_MODULES.
try:
    import typing_extensions
except ImportError:
    typing_extensions = None

# Available with MICROPY_PY_TYPING_EXTRA_MODULES and MICROPY_MODULE_BUILTIN_SUBPACKAGES.
try:
    import collections.abc

    collections.abc.Sequence
except ImportError:
    pass

import sys


class TestTypingSyntax(unittest.TestCase):
    # typing_extensions and __future__ access should work when available.
    def test_typing_extensions_and_future(self):
        # If this is available verify it works, and try the other modules as well.
        if typing_extensions is not None:
            import __future__
            from abc import abstractmethod

            getattr(__future__, "annotations")

    # FIXME: MicroPython should reject attribute assignment / subscription on typing/List.
    # if "micropython" in sys.implementation.name:
    #     # Verify assignment is not possible.
    #     try:
    #         typing.a = None
    #         raise Exception()
    #     except AttributeError:
    #         pass
    #     try:
    #         typing[0] = None
    #         raise Exception()
    #     except TypeError:
    #         pass
    #     try:
    #         List.a = None
    #         raise Exception()
    #     except AttributeError:
    #         pass

    # Module-level annotations and function with annotations should parse and run.
    def test_module_level_annotations_and_function(self):
        MyAlias = str
        Vector: typing.List[float]
        UserId = NewType("UserId", int)
        T = TypeVar("T", int, float, complex)

        hintedGlobal: Any = None

        def func_with_hints(c: int, b: MyAlias, a: Union[int, None], lst: List[float] = [0.0]) -> Any:
            pass

        func_with_hints(1, "alias", None)


if __name__ == "__main__":
    unittest.main()
