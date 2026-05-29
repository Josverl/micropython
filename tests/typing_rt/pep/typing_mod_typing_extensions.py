# Python 3.5
# module typing_extensions
# https://typing-extensions.readthedocs.io/

try:
    # typing_extensions MUST exist when typing is available
    import typing_extensions
except ImportError:
    print("SKIP")
    raise SystemExit

import unittest

# Do not test for all the individual names, just that the module exists
# as the different CPython versions have different subsets of names


class TestTypingExtensionsSpecialPrimitives(unittest.TestCase):
    # Module-level import of typing_extensions should succeed.
    def test_typing_extensions_module_imported(self):
        self.assertTrue(typing_extensions is not None)

    # Star-import from typing_extensions should succeed at runtime.
    def test_typing_extensions_star_import(self):
        ns = {}
        exec("from typing_extensions import *", {}, ns)
        self.assertTrue(len(ns) >= 1)


if __name__ == "__main__":
    unittest.main()
