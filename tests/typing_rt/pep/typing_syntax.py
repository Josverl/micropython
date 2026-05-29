# This doesn't quite test everything but just serves to verify that basic syntax works,
# which for MicroPython means everything typing-related should be ignored.

try:
    from typing import TYPE_CHECKING
except ImportError:
    print("SKIP")
    raise SystemExit

import unittest

from typing import List, NewType, TypeAlias, TypeVar, Union, Any
import typing
import sys

MyAlias :TypeAlias = str

class TestTypingSyntax(unittest.TestCase):

    @unittest.expectedFailure
    # FIXME: MicroPython should reject attribute assignment / subscription on typing/List.
    def test_typing_assigment_rejected(self):
        if "micropython" not in sys.implementation.name:
            self.skipTest("MicroPython-specific behaviour")
        with self.assertRaises(AttributeError):
            typing.a = None
        with self.assertRaises(TypeError):
            typing[0] = None
        with self.assertRaises(AttributeError):
            List.a = None

    # Module-level annotations and function with annotations should parse and run.
    def test_module_level_annotations_and_function(self):
        Vector: List[float]
        UserId = NewType("UserId", int)
        T = TypeVar("T", int, float, complex)

        hintedGlobal: Any = None

        def func_with_hints(c: int, b: MyAlias, a: Union[int, None], lst: List[float] = [0.0]) -> Any:
            pass

        func_with_hints(1, "alias", None)


if __name__ == "__main__":
    unittest.main()
