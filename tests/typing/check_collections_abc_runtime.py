# collections.abc runtime parity checks from notebook scenarios.

import unittest

try:
    import collections.abc as cabc
except ImportError:
    cabc = None

try:
    import typing as typing_mod
except ImportError:
    typing_mod = None


class TestCollectionsAbcRuntime(unittest.TestCase):
    # Mapping and Sequence annotation signatures should execute.
    def test_mapping_sequence_annotations(self):
        if cabc is None:
            return

        class Employee:
            pass

        def notify_by_email(employees: cabc.Sequence[Employee], overrides: cabc.Mapping[str, str]) -> None:
            self.assertTrue(type(overrides) is dict)
            self.assertTrue(type(employees) is list)

        notify_by_email([Employee()], {"a": "b"})

    # Callable and Awaitable annotations should be usable in async callback signatures.
    def test_callable_awaitable_annotations(self):
        if cabc is None:
            return

        async def on_update(value: str) -> None:
            return None

        callback: cabc.Callable[[str], cabc.Awaitable[None]] = on_update
        self.assertTrue(callback is on_update)

    # Iterable and Protocol callback pattern should execute.
    def test_iterable_protocol_callback_path(self):
        if cabc is None or not hasattr(typing_mod, "Protocol"):
            return

        class Combiner(typing_mod.Protocol):
            def __call__(self, *vals: bytes, maxlen=None):
                ...

        def batch_proc(data: cabc.Iterable[bytes], cb_results: Combiner) -> bytes:
            for item in data:
                _ = item
            out = cb_results(b"a", b"b")
            return out[0]

        def good_cb(*vals: bytes, maxlen=None):
            return list(vals)

        result = batch_proc([b"x", b"y"], good_cb)
        self.assertEqual(result, b"a")


if __name__ == "__main__":
    unittest.main()
