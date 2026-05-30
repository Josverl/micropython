# Additional typing spec coverage for runtime behavior and known unsupported parts.
# Spec index: https://typing.python.org/en/latest/spec/

try:
    import typing
except ImportError:
    print("SKIP")
    raise SystemExit

import sys
import unittest



class TestTypingUnsupportedRuntime(unittest.TestCase):
    # typing spec features that are intentionally not implemented in this runtime variant.
    def test_missing_advanced_spec_symbols(self):
        unsupported = (
            "ParamSpec",
            "TypeVarTuple",
            "TypeAlias",
            "runtime_checkable",
            "final",
            "Never",
            "TypeGuard",
            "TypeIs",
            "Required",
            "Unpack",
            "reveal_type",
        )

        for name in unsupported:
            with self.subTest(name=name):
                self.assertFalse(hasattr(typing, name), "unexpected symbol: {}".format(name))

    # typing runtime gap: Generic parameterized base does not yield a real class object.
    def test_generic_parameterized_base_is_not_a_real_class(self):
        if getattr(sys.implementation, "name", "") != "micropython":
            return

        code = (
            "from typing import Generic, TypeVar\n"
            "T = TypeVar('T')\n"
            "class Foo(Generic[T]):\n"
            "    pass\n"
            "class Bar(Foo[int]):\n"
            "    pass\n"
        )

        ns = {}
        exec(code, {}, ns)
        self.assertFalse(type(ns["Bar"]) is type)

    # cpydiff: NamedTuple factory behavior differs between CPython and MicroPython.
    def test_namedtuple_factory_runtime_difference(self):
        if not hasattr(typing, "NamedTuple"):
            return

        if getattr(sys.implementation, "name", "") == "micropython":
            with self.assertRaises(TypeError):
                typing.NamedTuple("Movie", [("name", str), ("year", int)])
            return

        movie_t = typing.NamedTuple("Movie", [("name", str), ("year", int)])
        item = movie_t("Blade Runner", 1982)
        self.assertEqual(item.name, "Blade Runner")
        self.assertEqual(item.year, 1982)

    # cpydiff: NewType has class-like runtime behavior in MicroPython vs callable object in CPython.
    def test_newtype_class_semantics_runtime_difference(self):
        user_id = typing.NewType("UserId", int)
        value = user_id(7)

        if getattr(sys.implementation, "name", "") == "micropython":
            self.assertTrue(user_id is int)
            self.assertTrue(isinstance(value, user_id))
            return

        self.assertFalse(type(user_id) is type)
        with self.assertRaises(TypeError):
            isinstance(value, user_id)


if __name__ == "__main__":
    unittest.main()
