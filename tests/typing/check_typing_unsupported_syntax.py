# Unsupported syntax/runtime parity checks from notebook scenarios.

import sys
import unittest


class TestTypingUnsupportedSyntax(unittest.TestCase):
    # Python 3.12 type statement support differs by runtime.
    def test_type_statement_runtime_difference(self):
        code = "type Point = tuple[float, float]\n"
        is_mpy = getattr(sys.implementation, "name", "") == "micropython"

        if is_mpy:
            with self.assertRaises(SyntaxError):
                exec(code, {}, {})
        else:
            ns = {}
            exec(code, ns, ns)
            self.assertTrue("Point" in ns)

    # Python 3.12 generic function syntax support differs by runtime.
    def test_type_parameter_syntax_runtime_difference(self):
        code = (
            "from collections.abc import Sequence\n"
            "def first[T](l: Sequence[T]) -> T:\n"
            "    return l[0]\n"
        )
        is_mpy = getattr(sys.implementation, "name", "") == "micropython"

        if is_mpy:
            with self.assertRaises(SyntaxError):
                exec(code, {}, {})
        else:
            ns = {}
            exec(code, ns, ns)
            self.assertEqual(ns["first"]([1, 2, 3]), 1)


if __name__ == "__main__":
    unittest.main()
