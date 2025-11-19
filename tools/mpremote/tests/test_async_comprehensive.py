#!/usr/bin/env python3
#
# Comprehensive tests for async transport implementation

import sys
import os
import asyncio

# Add mpremote to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from mpremote.transport_async import AsyncTransport
from mpremote.transport_serial_async import AsyncSerialTransport
from mpremote.protocol import RawREPLProtocol
from mpremote.console_async import AsyncConsole, AsyncConsolePosix, AsyncConsoleWindows
from mpremote.commands_async import do_exec_async, do_eval_async


def test_import_all_modules():
    """Test that all async modules can be imported."""
    print("Testing module imports...")
    
    try:
        import mpremote.transport_async
        import mpremote.transport_serial_async
        import mpremote.protocol
        import mpremote.console_async
        import mpremote.repl_async
        import mpremote.commands_async
        return True
    except ImportError as e:
        print(f"  FAIL: Import error - {e}")
        return False


def test_async_transport_inheritance():
    """Test that AsyncSerialTransport properly inherits from AsyncTransport."""
    print("\nTesting class inheritance...")
    
    try:
        # Check inheritance
        assert issubclass(AsyncSerialTransport, AsyncTransport)
        
        # Check that all abstract methods are implemented
        abstract_methods = [
            'read_async',
            'write_async',
            'read_until_async',
            'enter_raw_repl_async',
            'exit_raw_repl_async',
            'exec_raw_no_follow_async',
            'follow_async',
            'exec_raw_async',
            'exec_async',
            'eval_async',
            'close_async',
        ]
        
        for method in abstract_methods:
            assert hasattr(AsyncSerialTransport, method), f"Missing method: {method}"
            # Check it's a coroutine function
            method_obj = getattr(AsyncSerialTransport, method)
            if asyncio.iscoroutinefunction(method_obj):
                print(f"  ✓ {method} is async")
            else:
                print(f"  ✗ WARNING: {method} is not async")
        
        return True
    except AssertionError as e:
        print(f"  FAIL: {e}")
        return False


def test_protocol_methods():
    """Test all protocol methods."""
    print("\nTesting protocol methods...")
    
    try:
        # Test is_raw_paste_supported
        assert RawREPLProtocol.is_raw_paste_supported(b'OK') == True
        assert RawREPLProtocol.is_raw_paste_supported(b'raw REPL') == True
        assert RawREPLProtocol.is_raw_paste_supported(b'error') == False
        
        # Test encode_command_standard
        cmd = "x = 42"
        encoded = RawREPLProtocol.encode_command_standard(cmd)
        assert encoded == b"x = 42"
        
        # Test encode_command_raw_paste
        header, cmd_bytes = RawREPLProtocol.encode_command_raw_paste(cmd)
        assert header.startswith(b'\x05A\x01')
        assert len(header) == 7  # \x05A\x01 + 4 bytes length
        assert cmd_bytes == b"x = 42"
        
        # Test decode_response variations
        stdout, stderr = RawREPLProtocol.decode_response(b"hello\x04world\x04")
        assert stdout == b"hello"
        assert stderr == b"world"
        
        stdout, stderr = RawREPLProtocol.decode_response(b"output\x04")
        assert stdout == b"output"
        assert stderr == b""
        
        # Test check_error
        assert RawREPLProtocol.check_error(b"") is None
        assert RawREPLProtocol.check_error(b"   ") is None
        assert RawREPLProtocol.check_error(b"error message") == "error message"
        assert RawREPLProtocol.check_error(b"  error  \n") == "error"
        
        return True
    except AssertionError as e:
        print(f"  FAIL: {e}")
        return False


def test_console_factory():
    """Test console factory function."""
    print("\nTesting console factory...")
    
    try:
        console = AsyncConsole()
        
        # Check it returns the right type based on platform
        import sys
        if sys.platform == "win32":
            assert isinstance(console, AsyncConsoleWindows)
        else:
            try:
                import termios
                assert isinstance(console, AsyncConsolePosix)
            except ImportError:
                pass  # termios not available, skip platform check
        
        # Check console has required methods
        assert hasattr(console, 'enter')
        assert hasattr(console, 'exit')
        assert hasattr(console, 'readchar_async')
        assert hasattr(console, 'write')
        
        return True
    except AssertionError as e:
        print(f"  FAIL: {e}")
        return False


def test_async_transport_attributes():
    """Test AsyncSerialTransport attributes and initialization."""
    print("\nTesting transport attributes...")
    
    try:
        transport = AsyncSerialTransport(
            device="/dev/null",
            baudrate=115200,
            wait=0,
            exclusive=True,
            timeout=10.0
        )
        
        # Check all attributes exist
        assert transport.device_name == "/dev/null"
        assert transport.baudrate == 115200
        assert transport.wait == 0
        assert transport.exclusive == True
        assert transport.timeout == 10.0
        assert transport.in_raw_repl == False
        assert transport.use_raw_paste == True
        assert transport.mounted == False
        
        # Check stream attributes are initialized to None
        assert transport.reader is None
        assert transport.writer is None
        assert transport._transport is None
        
        return True
    except Exception as e:
        print(f"  FAIL: {e}")
        return False


async def test_async_state_methods():
    """Test State class async methods."""
    print("\nTesting State class async methods...")
    
    try:
        # Import here to avoid issues if not available
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
        from mpremote.main import State
        
        state = State()
        
        # Check async methods exist
        assert hasattr(state, 'ensure_connected_async')
        assert hasattr(state, 'ensure_raw_repl_async')
        assert hasattr(state, 'ensure_friendly_repl_async')
        
        # Check they are coroutine functions
        assert asyncio.iscoroutinefunction(state.ensure_connected_async)
        assert asyncio.iscoroutinefunction(state.ensure_raw_repl_async)
        assert asyncio.iscoroutinefunction(state.ensure_friendly_repl_async)
        
        return True
    except Exception as e:
        print(f"  FAIL: {e}")
        return False


def test_command_async_functions():
    """Test async command functions."""
    print("\nTesting async command functions...")
    
    try:
        # Check that async command functions exist
        assert callable(do_exec_async)
        assert callable(do_eval_async)
        
        # Check they are coroutine functions
        assert asyncio.iscoroutinefunction(do_exec_async)
        assert asyncio.iscoroutinefunction(do_eval_async)
        
        return True
    except Exception as e:
        print(f"  FAIL: {e}")
        return False


def test_sync_wrappers_exist():
    """Test that sync wrappers exist for backward compatibility."""
    print("\nTesting sync wrapper functions...")
    
    try:
        from mpremote.commands_async import (
            do_exec_sync_wrapper,
            do_eval_sync_wrapper,
            do_run_sync_wrapper
        )
        from mpremote.repl_async import do_repl_async_wrapper
        
        # Check they exist and are callable
        assert callable(do_exec_sync_wrapper)
        assert callable(do_eval_sync_wrapper)
        assert callable(do_run_sync_wrapper)
        assert callable(do_repl_async_wrapper)
        
        # Check they are NOT coroutine functions (they're sync wrappers)
        assert not asyncio.iscoroutinefunction(do_exec_sync_wrapper)
        assert not asyncio.iscoroutinefunction(do_eval_sync_wrapper)
        assert not asyncio.iscoroutinefunction(do_run_sync_wrapper)
        assert not asyncio.iscoroutinefunction(do_repl_async_wrapper)
        
        return True
    except Exception as e:
        print(f"  FAIL: {e}")
        return False


def test_protocol_edge_cases():
    """Test protocol edge cases and error handling."""
    print("\nTesting protocol edge cases...")
    
    try:
        # Test empty response
        stdout, stderr = RawREPLProtocol.decode_response(b"")
        assert stdout == b""
        assert stderr == b""
        
        # Test response with no separators
        stdout, stderr = RawREPLProtocol.decode_response(b"no separator")
        assert stdout == b"no separator"
        assert stderr == b""
        
        # Test response with multiple separators
        stdout, stderr = RawREPLProtocol.decode_response(b"out1\x04err1\x04extra\x04")
        assert stdout == b"out1"
        assert stderr == b"err1"
        
        # Test encode with unicode
        cmd = "print('ñ')"
        encoded = RawREPLProtocol.encode_command_standard(cmd)
        assert isinstance(encoded, bytes)
        assert b'print' in encoded
        
        return True
    except Exception as e:
        print(f"  FAIL: {e}")
        return False


def test_async_console_methods():
    """Test async console has all required methods."""
    print("\nTesting async console methods...")
    
    try:
        console = AsyncConsole()
        
        # Check all required methods exist
        required_methods = ['enter', 'exit', 'readchar_async', 'write']
        for method in required_methods:
            assert hasattr(console, method), f"Missing method: {method}"
        
        # Check readchar_async is async
        assert asyncio.iscoroutinefunction(console.readchar_async)
        
        # Check enter/exit are not async (they're setup/teardown)
        assert not asyncio.iscoroutinefunction(console.enter)
        assert not asyncio.iscoroutinefunction(console.exit)
        
        return True
    except Exception as e:
        print(f"  FAIL: {e}")
        return False


def run_all_tests():
    """Run all comprehensive tests."""
    print("=" * 70)
    print("COMPREHENSIVE ASYNC TRANSPORT TESTS")
    print("=" * 70)
    
    results = []
    
    # Synchronous tests
    results.append(("Module Imports", test_import_all_modules()))
    results.append(("Class Inheritance", test_async_transport_inheritance()))
    results.append(("Protocol Methods", test_protocol_methods()))
    results.append(("Console Factory", test_console_factory()))
    results.append(("Transport Attributes", test_async_transport_attributes()))
    results.append(("Command Functions", test_command_async_functions()))
    results.append(("Sync Wrappers", test_sync_wrappers_exist()))
    results.append(("Protocol Edge Cases", test_protocol_edge_cases()))
    results.append(("Console Methods", test_async_console_methods()))
    
    # Async tests
    print("\nRunning async tests...")
    try:
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(test_async_state_methods())
        results.append(("State Async Methods", result))
    except Exception as e:
        print(f"  FAIL: Error running async test - {e}")
        results.append(("State Async Methods", False))
    
    # Summary
    print("\n" + "=" * 70)
    
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
    success = run_all_tests()
    sys.exit(0 if success else 1)
