#!/usr/bin/env python3
#
# Comprehensive tests for async transport implementation

import asyncio
import pytest


pytestmark = pytest.mark.async_required


def test_import_all_async_modules(async_modules):
    """Test that all async modules can be imported."""
    import mpremote.transport_async
    import mpremote.transport_serial_async
    import mpremote.protocol
    import mpremote.console_async
    import mpremote.repl_async
    import mpremote.commands_async

    assert mpremote.transport_async is not None
    assert mpremote.transport_serial_async is not None
    assert mpremote.protocol is not None
    assert mpremote.console_async is not None
    assert mpremote.repl_async is not None
    assert mpremote.commands_async is not None


def test_async_transport_inheritance(async_modules):
    """Test that AsyncSerialTransport properly inherits from AsyncTransport."""
    AsyncTransport = async_modules["AsyncTransport"]
    AsyncSerialTransport = async_modules["AsyncSerialTransport"]

    assert issubclass(AsyncSerialTransport, AsyncTransport)

    abstract_methods = [
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

    for method in abstract_methods:
        assert hasattr(AsyncSerialTransport, method), f"Missing method: {method}"
        method_obj = getattr(AsyncSerialTransport, method)
        assert asyncio.iscoroutinefunction(method_obj), f"{method} should be async"


def test_protocol_methods(async_modules):
    """Test all protocol methods."""
    RawREPLProtocol = async_modules["RawREPLProtocol"]

    # Test is_raw_paste_supported
    assert RawREPLProtocol.is_raw_paste_supported(b"OK") is True
    assert RawREPLProtocol.is_raw_paste_supported(b"raw REPL") is True
    assert RawREPLProtocol.is_raw_paste_supported(b"error") is False

    # Test encode_command_standard
    cmd = "x = 42"
    encoded = RawREPLProtocol.encode_command_standard(cmd)
    assert encoded == b"x = 42"

    # Test encode_command_raw_paste
    header, cmd_bytes = RawREPLProtocol.encode_command_raw_paste(cmd)
    assert header.startswith(b"\x05A\x01")
    assert len(header) == 7
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


def test_console_factory(async_modules, platform_info):
    """Test console factory function."""
    AsyncConsole = async_modules["AsyncConsole"]
    from mpremote.console_async import AsyncConsolePosix, AsyncConsoleWindows

    console = AsyncConsole()

    # Check it returns the right type based on platform
    if platform_info["is_windows"]:
        assert isinstance(console, AsyncConsoleWindows)
    else:
        if platform_info["has_termios"]:
            assert isinstance(console, AsyncConsolePosix)

    # Check console has required methods
    assert hasattr(console, "enter")
    assert hasattr(console, "exit")
    assert hasattr(console, "readchar_async")
    assert hasattr(console, "write")


@pytest.mark.serial_required
def test_async_transport_attributes(async_modules):
    """Test AsyncSerialTransport attributes and initialization."""
    AsyncSerialTransport = async_modules["AsyncSerialTransport"]

    transport = AsyncSerialTransport(
        device="/dev/null", baudrate=115200, wait=0, exclusive=True, timeout=10.0
    )

    assert transport.device_name == "/dev/null"
    assert transport.baudrate == 115200
    assert transport.wait == 0
    assert transport.exclusive is True
    assert transport.timeout == 10.0
    assert transport.in_raw_repl is False
    assert transport.use_raw_paste is True
    assert transport.mounted is False
    assert transport.reader is None
    assert transport.writer is None
    assert transport._transport is None


def test_async_state_methods(async_modules, event_loop):
    """Test State class async methods."""
    from mpremote.main import State

    state = State()

    assert hasattr(state, "ensure_connected_async")
    assert hasattr(state, "ensure_raw_repl_async")
    assert hasattr(state, "ensure_friendly_repl_async")

    assert asyncio.iscoroutinefunction(state.ensure_connected_async)
    assert asyncio.iscoroutinefunction(state.ensure_raw_repl_async)
    assert asyncio.iscoroutinefunction(state.ensure_friendly_repl_async)


def test_command_async_functions(async_modules):
    """Test async command functions."""
    do_exec_async = async_modules["do_exec_async"]
    do_eval_async = async_modules["do_eval_async"]

    assert callable(do_exec_async)
    assert callable(do_eval_async)

    assert asyncio.iscoroutinefunction(do_exec_async)
    assert asyncio.iscoroutinefunction(do_eval_async)


def test_sync_wrappers_exist(async_modules):
    """Test that sync wrappers exist for backward compatibility."""
    from mpremote.commands_async import (
        do_exec_sync_wrapper,
        do_eval_sync_wrapper,
        do_run_sync_wrapper,
    )
    from mpremote.repl_async import do_repl_async_wrapper

    assert callable(do_exec_sync_wrapper)
    assert callable(do_eval_sync_wrapper)
    assert callable(do_run_sync_wrapper)
    assert callable(do_repl_async_wrapper)

    # Check they are NOT coroutine functions (they're sync wrappers)
    assert not asyncio.iscoroutinefunction(do_exec_sync_wrapper)
    assert not asyncio.iscoroutinefunction(do_eval_sync_wrapper)
    assert not asyncio.iscoroutinefunction(do_run_sync_wrapper)
    assert not asyncio.iscoroutinefunction(do_repl_async_wrapper)


def test_protocol_edge_cases(async_modules):
    """Test protocol edge cases and error handling."""
    RawREPLProtocol = async_modules["RawREPLProtocol"]

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
    assert b"print" in encoded


def test_async_console_methods(async_modules):
    """Test async console has all required methods."""
    AsyncConsole = async_modules["AsyncConsole"]

    console = AsyncConsole()

    required_methods = ["enter", "exit", "readchar_async", "write"]
    for method in required_methods:
        assert hasattr(console, method), f"Missing method: {method}"

    assert asyncio.iscoroutinefunction(console.readchar_async)
    assert not asyncio.iscoroutinefunction(console.enter)
    assert not asyncio.iscoroutinefunction(console.exit)
