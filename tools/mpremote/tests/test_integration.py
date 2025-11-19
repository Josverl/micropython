#!/usr/bin/env python3
#
# Integration test for async transport
# This tests the full integration without requiring hardware

import sys
import os
import asyncio

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from mpremote.transport_serial_async import AsyncSerialTransport
from mpremote.main import State
from mpremote.protocol import RawREPLProtocol


async def test_async_workflow():
    """Test a complete async workflow (without actual hardware)."""
    print("Testing async workflow integration...")
    
    # This tests that the API is correctly structured
    # Actual connection would fail without hardware, but we can test
    # that all the pieces fit together
    
    transport = AsyncSerialTransport("/dev/null", baudrate=115200, wait=0)
    
    # Test that all required attributes exist
    assert hasattr(transport, 'device_name')
    assert hasattr(transport, 'baudrate')
    assert hasattr(transport, 'in_raw_repl')
    assert hasattr(transport, 'use_raw_paste')
    
    # Test that all async methods exist and are coroutines
    async_methods = [
        'connect', 'read_async', 'write_async', 'read_until_async',
        'enter_raw_repl_async', 'exit_raw_repl_async',
        'exec_raw_no_follow_async', 'follow_async', 'exec_raw_async',
        'exec_async', 'eval_async', 'close_async'
    ]
    
    for method_name in async_methods:
        method = getattr(transport, method_name)
        assert asyncio.iscoroutinefunction(method), f"{method_name} should be async"
    
    print("  ✓ All async methods are present and are coroutines")
    
    # Test State integration
    state = State()
    assert hasattr(state, 'ensure_raw_repl_async')
    assert asyncio.iscoroutinefunction(state.ensure_raw_repl_async)
    
    print("  ✓ State class has async methods")
    
    # Test protocol integration
    cmd = "print('test')"
    encoded = RawREPLProtocol.encode_command_standard(cmd)
    assert encoded == b"print('test')"
    
    header, cmd_bytes = RawREPLProtocol.encode_command_raw_paste(cmd)
    assert cmd_bytes == b"print('test')"
    assert len(header) == 7  # Ctrl-E A \x01 + 4 bytes length
    
    print("  ✓ Protocol encoding works correctly")
    
    print("\n✅ Integration test passed!")
    return True


async def test_concurrent_pattern():
    """Test that async patterns work correctly."""
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
    
    print("  ✓ asyncio.gather works correctly")
    
    # Test task pattern
    task1 = asyncio.create_task(operation1())
    task2 = asyncio.create_task(operation2())
    
    result1 = await task1
    result2 = await task2
    
    assert result1 == "op1"
    assert result2 == "op2"
    
    print("  ✓ asyncio.create_task works correctly")
    
    # Test timeout pattern
    try:
        async with asyncio.timeout(0.1):
            await asyncio.sleep(0.01)
        print("  ✓ asyncio.timeout works correctly")
    except asyncio.TimeoutError:
        print("  ✗ Timeout occurred unexpectedly")
        return False
    
    print("\n✅ Concurrent pattern test passed!")
    return True


def test_error_handling():
    """Test error handling in async code."""
    print("\nTesting error handling...")
    
    # Test protocol error detection
    stderr = b"Traceback: error message"
    error = RawREPLProtocol.check_error(stderr)
    assert error == "Traceback: error message"
    print("  ✓ Error detection works")
    
    # Test empty error
    stderr = b""
    error = RawREPLProtocol.check_error(stderr)
    assert error is None
    print("  ✓ Empty error handling works")
    
    # Test whitespace error
    stderr = b"   \n  "
    error = RawREPLProtocol.check_error(stderr)
    assert error is None
    print("  ✓ Whitespace error handling works")
    
    print("\n✅ Error handling test passed!")
    return True


def test_sync_async_coexistence():
    """Test that sync and async APIs can coexist."""
    print("\nTesting sync/async coexistence...")
    
    state = State()
    
    # Check both sync and async methods exist
    sync_methods = ['ensure_connected', 'ensure_raw_repl', 'ensure_friendly_repl']
    async_methods = ['ensure_connected_async', 'ensure_raw_repl_async', 'ensure_friendly_repl_async']
    
    for method in sync_methods:
        assert hasattr(state, method), f"Missing sync method: {method}"
        assert not asyncio.iscoroutinefunction(getattr(state, method)), f"{method} should not be async"
    
    print("  ✓ All sync methods present and not async")
    
    for method in async_methods:
        assert hasattr(state, method), f"Missing async method: {method}"
        assert asyncio.iscoroutinefunction(getattr(state, method)), f"{method} should be async"
    
    print("  ✓ All async methods present and are async")
    
    print("\n✅ Sync/async coexistence test passed!")
    return True


def main():
    """Run all integration tests."""
    print("=" * 70)
    print("INTEGRATION TESTS")
    print("=" * 70)
    
    results = []
    
    # Run async tests
    print("\nRunning async integration tests...")
    try:
        result = asyncio.run(test_async_workflow())
        results.append(("Async Workflow", result))
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        results.append(("Async Workflow", False))
    
    try:
        result = asyncio.run(test_concurrent_pattern())
        results.append(("Concurrent Patterns", result))
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        results.append(("Concurrent Patterns", False))
    
    # Run sync tests
    try:
        result = test_error_handling()
        results.append(("Error Handling", result))
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        results.append(("Error Handling", False))
    
    try:
        result = test_sync_async_coexistence()
        results.append(("Sync/Async Coexistence", result))
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        results.append(("Sync/Async Coexistence", False))
    
    # Summary
    print("\n" + "=" * 70)
    print("INTEGRATION TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} {name}")
    
    print("=" * 70)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 70)
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
