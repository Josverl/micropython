# typing_extensions runtime parity checks from notebook scenarios.

import sys
import unittest

try:
    import typing_extensions as te
except ImportError:
    te = None


class TestTypingExtensionsRuntime(unittest.TestCase):
    # TYPE_CHECKING should be present and boolean.
    def test_type_checking_bool(self):
        if te is None:
            return

        self.assertTrue(hasattr(te, "TYPE_CHECKING"))
        self.assertTrue(type(te.TYPE_CHECKING) is bool)

    # Self annotation path should execute and return self.
    def test_self_annotation_runtime_path(self):
        if te is None:
            return

        if not hasattr(te, "Self"):
            return

        class Foo:
            def return_self(self) -> te.Self:
                return self

        foo = Foo()
        self.assertTrue(foo.return_self() is foo)

    # Generator annotation path should execute and produce expected first value.
    def test_generator_annotation_runtime_path(self):
        if te is None:
            return

        if not hasattr(te, "Generator"):
            return

        def echo_round() -> te.Generator[int, float, str]:
            sent = yield 0
            while sent >= 0:
                sent = yield round(sent)
            return "Done"

        g = echo_round()
        self.assertEqual(next(g), 0)

    # reveal_type should be callable if provided.
    def test_reveal_type_runtime_path(self):
        if te is None:
            return

        if not hasattr(te, "reveal_type"):
            return

        value = 42
        revealed = te.reveal_type(value)
        self.assertEqual(revealed, value)

    # TypeVarTuple and Unpack are optional in this runtime setup.
    def test_typevar_tuple_symbols_optional(self):
        if te is None:
            return

        if hasattr(te, "TypeVarTuple"):
            ts = te.TypeVarTuple("Ts")
            self.assertTrue(ts is not None)
        elif getattr(sys.implementation, "name", "") == "micropython":
            self.assertFalse(hasattr(te, "TypeVarTuple"))

        if hasattr(te, "Unpack"):
            self.assertTrue(te.Unpack is not None)
        elif getattr(sys.implementation, "name", "") == "micropython":
            self.assertFalse(hasattr(te, "Unpack"))

    # TypeVar should be importable from typing_extensions in this runtime setup.
    def test_typevar_runtime_path(self):
        if te is None or not hasattr(te, "TypeVar"):
            return

        t = te.TypeVar("T")
        if getattr(sys.implementation, "name", "") == "micropython":
            self.assertTrue(t is None)
        else:
            self.assertTrue(t is not None)

    # reveal_type may be absent on MicroPython and is tracked explicitly.
    def test_reveal_type_runtime_difference(self):
        if te is None:
            return

        if getattr(sys.implementation, "name", "") == "micropython":
            self.assertFalse(hasattr(te, "reveal_type"))
            return

        self.assertTrue(hasattr(te, "reveal_type"))


if __name__ == "__main__":
    unittest.main()
