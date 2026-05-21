# abc module runtime parity checks from notebook scenarios.

import sys
import unittest

try:
    import abc as abc_mod
except ImportError:
    abc_mod = None


class TestAbcRuntime(unittest.TestCase):
    # Basic abc helpers used in notebook should be callable.
    def test_abc_helper_functions(self):
        if abc_mod is None:
            return

        if not hasattr(abc_mod, "get_cache_token") or not hasattr(abc_mod, "update_abstractmethods"):
            # Helper API is optional in this runtime implementation.
            self.assertTrue(getattr(sys.implementation, "name", "") == "micropython")
            return

        token = abc_mod.get_cache_token()

        class C(abc_mod.ABC):
            @abc_mod.abstractmethod
            def f(self):
                ...

        cls = abc_mod.update_abstractmethods(C)
        self.assertTrue(type(token) is int)
        self.assertTrue(cls is C)

    # Abstract class pattern with concrete implementations should execute.
    def test_abstract_class_usage(self):
        if abc_mod is None:
            return

        class Shape(abc_mod.ABC):
            @abc_mod.abstractmethod
            def get_area(self):
                ...

        class Square(Shape):
            def __init__(self, side):
                self.side = side

            def get_area(self):
                return self.side * self.side

        sq = Square(5)
        self.assertEqual(sq.get_area(), 25)

    # cpydiff: metaclass=ABCMeta behavior differs between CPython and MicroPython.
    def test_abcmeta_metaclass_runtime_difference(self):
        if abc_mod is None:
            return

        code = "class MyABC(metaclass=ABCMeta):\n    pass\n"

        if getattr(sys.implementation, "name", "") == "micropython":
            with self.assertRaises(Exception):
                exec(code, {"ABCMeta": abc_mod.ABCMeta}, {})
        else:
            ns = {"ABCMeta": abc_mod.ABCMeta}
            exec(code, ns, ns)
            self.assertTrue("MyABC" in ns)


if __name__ == "__main__":
    unittest.main()
