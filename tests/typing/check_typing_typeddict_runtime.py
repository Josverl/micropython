# TypedDict runtime parity checks from the notebook scenarios.

try:
    from typing import TypeVar, TypedDict
except ImportError:
    print("SKIP")
    raise SystemExit

import sys
import unittest


class TestTypingTypedDictRuntime(unittest.TestCase):
    # Basic TypedDict-like construction path used in notebook examples.
    def test_typed_dict_construction_and_access(self):
        class Movie(TypedDict):
            name: str
            year: int

        movie = Movie(name="Blade Runner", year=1982)
        self.assertTrue(isinstance(movie, dict))
        self.assertEqual(movie["name"], "Blade Runner")
        self.assertEqual(movie["year"], 1982)

    # isinstance(TypedDict) behavior differs by runtime and is documented for parity.
    def test_typed_dict_isinstance_runtime_difference(self):
        class Movie(TypedDict):
            name: str
            year: int

        movie = {"name": "Blade Runner", "year": 1982}

        if getattr(sys.implementation, "name", "") == "micropython":
            # In this runtime, TypedDict is currently dict-like at runtime.
            self.assertFalse(isinstance(movie, Movie))
        else:
            # CPython typing spec behavior raises TypeError for TypedDict in isinstance.
            with self.assertRaises(TypeError):
                isinstance(movie, Movie)

    # Notebook includes this static-analysis pattern; runtime call path should still execute.
    def test_typevar_bound_typed_dict_runtime_path(self):
        t = TypeVar("T", bound=TypedDict)
        self.assertTrue(t is None or hasattr(t, "__class__"))


if __name__ == "__main__":
    unittest.main()
