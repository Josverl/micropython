#!/usr/bin/env python3
#
# Integration test for async transport
# This tests the full integration without requiring hardware

import asyncio

import pytest
from mpremote.async_compat import get_timeout
from mpremote.main import State
from mpremote.protocol import RawREPLProtocol

try:
    from mpremote.transport_serial_async import AsyncSerialTransport, serial_asyncio

    HAS_SERIAL_ASYNCIO = serial_asyncio is not None
except ImportError:
    HAS_SERIAL_ASYNCIO = False
    AsyncSerialTransport = None


@pytest.mark.skipif(not HAS_SERIAL_ASYNCIO, reason="pyserial-asyncio not installed")
def test_async_workflow(event_loop):
    """Test a complete async workflow (without actual hardware)."""

    async def _test():
        print("Testing async workflow integration...")

        # This tests that the API is correctly structured
        # Actual connection would fail without hardware, but we can test
        # that all the pieces fit together

        transport = AsyncSerialTransport("/dev/null", baudrate=115200, wait=0)

        # Test that all required attributes exist
        assert hasattr(transport, "device_name")
        assert hasattr(transport, "baudrate")
        assert hasattr(transport, "in_raw_repl")
        assert hasattr(transport, "use_raw_paste")

        # Test that all async methods exist and are coroutines
        async_methods = [
            "connect",
            "read_async",
            "write_async",
            "read_until_async",
            "enter_raw_repl_async",
            "exit_raw_repl_async",
            "exec_raw_no_follow_async",
            "follow_async",
            "exec_raw_async",
            "exec_async",
            "eval_async",
            "close_async",
        ]

        for method_name in async_methods:
            method = getattr(transport, method_name)
            assert asyncio.iscoroutinefunction(method), f"{method_name} should be async"

        # Test State integration
        state = State()
        assert hasattr(state, "ensure_raw_repl_async")
        assert asyncio.iscoroutinefunction(state.ensure_raw_repl_async)

        # Test protocol integration
        cmd = "print('test')"
        encoded = RawREPLProtocol.encode_command_standard(cmd)
        assert encoded == b"print('test')"

        header, cmd_bytes = RawREPLProtocol.encode_command_raw_paste(cmd)
        assert cmd_bytes == b"print('test')"
        assert len(header) == 7  # Ctrl-E A \x01 + 4 bytes length

        return True

    event_loop.run_until_complete(_test())


def test_concurrent_pattern(event_loop):
    """Test that async patterns work correctly."""

    async def _test():
        print("\nTesting async concurrent patterns...")

        # Simulate async operations
        async def operation1():
            await asyncio.sleep(0.01)
            return "op1"

        async def operation2():
            await asyncio.sleep(0.01)
            return "op2"

        async def operation3():
            await asyncio.sleep(0.01)
            return "op3"

        # Test gather pattern
        results = await asyncio.gather(operation1(), operation2(), operation3())
        assert results == ["op1", "op2", "op3"]

        # Test task pattern
        task1 = asyncio.create_task(operation1())
        task2 = asyncio.create_task(operation2())

        result1 = await task1
        result2 = await task2

        assert result1 == "op1"
        assert result2 == "op2"

        # Test timeout pattern; should not raise for short sleep
        try:
            async with get_timeout(0.1):
                await asyncio.sleep(0.01)
        except asyncio.TimeoutError:
            pytest.fail("Timeout raised unexpectedly for short operation")

    event_loop.run_until_complete(_test())


def test_error_handling():
    """Test error handling in async code."""
    print("\nTesting error handling...")

    # Test protocol error detection
    stderr = b"Traceback: error message"
    error = RawREPLProtocol.check_error(stderr)
    assert error == "Traceback: error message"

    # Test empty error
    stderr = b""
    error = RawREPLProtocol.check_error(stderr)
    assert error is None

    # Test whitespace error
    stderr = b"   \n  "
    error = RawREPLProtocol.check_error(stderr)
    assert error is None


def test_sync_async_coexistence():
    """Test that sync and async APIs can coexist."""
    print("\nTesting sync/async coexistence...")

    state = State()

    # Check both sync and async methods exist
    sync_methods = ["ensure_connected", "ensure_raw_repl", "ensure_friendly_repl"]
    async_methods = [
        "ensure_connected_async",
        "ensure_raw_repl_async",
        "ensure_friendly_repl_async",
    ]

    for method in sync_methods:
        assert hasattr(state, method), f"Missing sync method: {method}"
        assert not asyncio.iscoroutinefunction(getattr(state, method)), (
            f"{method} should not be async"
        )

    for method in async_methods:
        assert hasattr(state, method), f"Missing async method: {method}"
        assert asyncio.iscoroutinefunction(getattr(state, method)), f"{method} should be async"
