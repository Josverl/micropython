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

MyAlias: TypeAlias = str


class TestTypingSyntax(unittest.TestCase):
    # Module-level annotations and function with annotations should parse and run.
    def test_module_level_annotations_and_function(self):
        Vector: List[float]
        UserId = NewType("UserId", int)
        T = TypeVar("T", int, float, complex)

        hintedGlobal: Any = None

        def func_with_hints(
            c: int, b: MyAlias, a: Union[int, None], lst: List[float] = [0.0]
        ) -> Any:
            pass

        func_with_hints(1, "alias", None)


if __name__ == "__main__":
    unittest.main()
