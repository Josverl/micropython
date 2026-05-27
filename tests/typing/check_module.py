# probe module availability
# import only

import collections
import sys
import unittest


try:
    from typing import TYPE_CHECKING
except Exception:
    print("SKIP")
    raise SystemExit

class TestModuleIncluded(unittest.TestCase):

    def test_typing(self):
        import typing
        self.assertIsNotNone(typing)

    def test_typing_extensions(self):
        try:
            import typing_extensions
            self.assertIsNotNone(typing_extensions)
        except ImportError:
            unittest.skip("module not available")

    def test_future(self):
        try:
            import __future__
            self.assertIsNotNone(__future__)
        except ImportError:
            unittest.skip("module not available")

    def test_collections(self):
        try:
            import collections
            self.assertIsNotNone(collections)
        except ImportError:
            unittest.skip("module not available")

    def test_collections_abc(self):
        import collections.abc
        self.assertIsNotNone(collections.abc)


if __name__ == "__main__":
    unittest.main()
