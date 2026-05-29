# Python 3.3+
# module collections.abc
# https://peps.python.org/pep-3119/
# https://docs.python.org/3/library/collections.abc.html#module-collections.abc
#
# Note: the current runtime typing implementation does not yet implement
# collections.abc, so the imports below are marked as expected failures.

from math import e

try:
    import collections.abc
except ImportError:
    print("SKIP")
    raise SystemExit

import unittest

# Note: ``import collections.abc`` itself may fail on this runtime typing
# implementation; individual import tests below capture per-symbol behavior.


class TestCollectionsAbcImports(unittest.TestCase):
    # collections.abc top-level container ABCs.
    def test_container_imports(self):
        from collections.abc import Container
        from collections.abc import Hashable
        from collections.abc import Iterable
        from collections.abc import Reversible
        from collections.abc import Generator
        from collections.abc import Sized
        from collections.abc import Callable
        from collections.abc import Collection

    # collections.abc sequence ABCs.
    def test_sequence_imports(self):
        from collections.abc import Sequence
        from collections.abc import MutableSequence
        # from collections.abc import ByteString # Deprecated since version 3.12,

    # collections.abc set and mapping ABCs.
    def test_set_and_mapping_imports(self):
        from collections.abc import Set
        from collections.abc import MutableSet
        from collections.abc import Mapping
        from collections.abc import MutableMapping
        from collections.abc import MappingView
        from collections.abc import KeysView
        from collections.abc import ItemsView
        from collections.abc import ValuesView

    # collections.abc async/awaitable ABCs.
    def test_async_imports(self):
        from collections.abc import Awaitable
        from collections.abc import Coroutine
        from collections.abc import AsyncIterable
        from collections.abc import AsyncIterator
        from collections.abc import AsyncGenerator

    # collections.abc Buffer ABC (Python 3.12+).
    def test_buffer_import(self):
        from collections.abc import Buffer


if __name__ == "__main__":
    unittest.main()
