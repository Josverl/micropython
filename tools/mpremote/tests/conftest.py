#!/usr/bin/env python3
#
# This file is part of the MicroPython project, http://micropython.org/
#
# The MIT License (MIT)
#
# Copyright (c) 2025 Jos Verlinde
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""Pytest configuration and shared fixtures for mpremote async tests."""

import sys
import os
import asyncio
import pytest
from pathlib import Path

# Add mpremote to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


# Check for async module availability
try:
    from mpremote.transport_async import AsyncTransport
    from mpremote.transport_serial_async import AsyncSerialTransport
    from mpremote.protocol import RawREPLProtocol
    from mpremote.console_async import AsyncConsole
    from mpremote.commands_async import do_exec_async, do_eval_async

    HAS_ASYNC = True
    ASYNC_IMPORT_ERROR = None
except ImportError as e:
    HAS_ASYNC = False
    ASYNC_IMPORT_ERROR = str(e)

# Check for serial module availability
try:
    import serial.tools.list_ports

    HAS_SERIAL = True
except ImportError:
    HAS_SERIAL = False


# Platform detection
IS_WINDOWS = sys.platform == "win32"
IS_POSIX = not IS_WINDOWS

# Check for termios (POSIX terminal control)
try:
    import termios

    HAS_TERMIOS = True
except ImportError:
    HAS_TERMIOS = False


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "asyncio: mark test as async (using pytest-asyncio)")
    config.addinivalue_line("markers", "async_required: mark test as requiring async modules")
    config.addinivalue_line("markers", "serial_required: mark test as requiring pyserial-asyncio")
    config.addinivalue_line("markers", "windows_only: mark test as Windows-only")
    config.addinivalue_line("markers", "posix_only: mark test as POSIX-only")
    config.addinivalue_line("markers", "hardware_required: mark test as requiring hardware device")
    config.addinivalue_line(
        "markers", "micropython_unix: mark test as requiring MicroPython unix port"
    )
    config.addinivalue_line("markers", "slow: mark test as slow-running")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to handle platform-specific and conditional tests."""
    for item in items:
        # Skip tests that require async modules if not available
        if "async_required" in item.keywords and not HAS_ASYNC:
            item.add_marker(
                pytest.mark.skip(reason=f"Async modules not available: {ASYNC_IMPORT_ERROR}")
            )

        # Skip tests that require pyserial-asyncio if not available
        if "serial_required" in item.keywords:
            # Try to import to check if it's available
            try:
                import serial_asyncio

                pass  # It's available
            except ImportError:
                item.add_marker(pytest.mark.skip(reason="pyserial-asyncio not installed"))

        # Skip Windows-only tests on non-Windows
        if "windows_only" in item.keywords and not IS_WINDOWS:
            item.add_marker(pytest.mark.skip(reason="Test requires Windows platform"))

        # Skip POSIX-only tests on Windows
        if "posix_only" in item.keywords and not IS_POSIX:
            item.add_marker(pytest.mark.skip(reason="Test requires POSIX platform"))

        # Skip POSIX tests that require termios
        if "posix_only" in item.keywords and IS_POSIX and not HAS_TERMIOS:
            item.add_marker(pytest.mark.skip(reason="Test requires termios module"))


# ============================================================================
# Platform Fixtures
# ============================================================================


@pytest.fixture
def platform_info():
    """Provide platform information."""
    return {
        "is_windows": IS_WINDOWS,
        "is_posix": IS_POSIX,
        "has_termios": HAS_TERMIOS,
        "platform": sys.platform,
    }


# ============================================================================
# Async Module Fixtures
# ============================================================================


@pytest.fixture
def async_modules():
    """Provide async module imports if available."""
    if not HAS_ASYNC:
        pytest.skip(f"Async modules not available: {ASYNC_IMPORT_ERROR}")

    return {
        "AsyncTransport": AsyncTransport,
        "AsyncSerialTransport": AsyncSerialTransport,
        "RawREPLProtocol": RawREPLProtocol,
        "AsyncConsole": AsyncConsole,
        "do_exec_async": do_exec_async,
        "do_eval_async": do_eval_async,
    }


# ============================================================================
# Event Loop Fixtures
# ============================================================================


@pytest.fixture
def event_loop():
    """Create and clean up event loop for async tests."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    try:
        # Clean up pending tasks
        pending = asyncio.all_tasks(loop)
        for task in pending:
            task.cancel()
        if pending:
            loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
    finally:
        loop.close()


# ============================================================================
# Hardware Device Fixtures
# ============================================================================


def find_micropython_device():
    """Find the first available MicroPython device."""
    if not HAS_SERIAL:
        return None

    try:
        import serial.tools.list_ports

        ports = serial.tools.list_ports.comports()
        if not ports:
            return None

        # Look for common MicroPython device identifiers
        micropython_keywords = [
            "USB Serial",
            "USB-SERIAL",
            "CH340",
            "CH343",
            "CP210",
            "FT232",
            "Arduino",
            "Pico",
            "ESP32",
            "STM32",
        ]

        for port in ports:
            description = port.description.upper()
            for keyword in micropython_keywords:
                if keyword.upper() in description:
                    return port.device

        # If no specific match, return first available
        return ports[0].device
    except Exception:
        return None


@pytest.fixture(scope="session")
def test_device_port(request):
    """
    Get test device port from command line or auto-detect.

    Usage: pytest --device=COM20 or pytest --device=/dev/ttyUSB0
    """
    device = request.config.getoption("--device", default=None)
    if device:
        return device

    # Try to auto-detect
    device = find_micropython_device()
    if device:
        return device

    return None


@pytest.fixture
def hardware_device(test_device_port):
    """Provide hardware device port or skip test if not available."""
    if test_device_port is None:
        pytest.skip("No MicroPython device available")
    return test_device_port


@pytest.fixture
async def connected_transport(hardware_device, async_modules):
    """
    Create and connect an async transport to hardware device.

    Automatically cleans up connection after test.
    """
    AsyncSerialTransport = async_modules["AsyncSerialTransport"]

    transport = AsyncSerialTransport(hardware_device, baudrate=115200)
    await asyncio.wait_for(transport.connect(), timeout=5.0)

    yield transport

    # Cleanup
    try:
        await transport.close_async()
    except Exception:
        pass


# ============================================================================
# MicroPython Unix Port Fixtures
# ============================================================================


@pytest.fixture(scope="session")
def micropython_unix_binary():
    """Find MicroPython unix port binary."""
    possible_paths = [
        Path(__file__).parent.parent.parent.parent
        / "ports"
        / "unix"
        / "build-standard"
        / "micropython",
        Path(__file__).parent.parent.parent.parent / "ports" / "unix" / "build" / "micropython",
        Path("/usr/local/bin/micropython"),
        Path("/usr/bin/micropython"),
    ]

    for path in possible_paths:
        if path.exists() and path.is_file():
            return str(path)

    return None


# ============================================================================
# Command Line Options
# ============================================================================


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--device",
        action="store",
        default=None,
        help="Serial port for hardware tests (e.g., COM20 or /dev/ttyUSB0)",
    )
    parser.addoption(
        "--run-hardware",
        action="store_true",
        default=False,
        help="Run hardware integration tests",
    )
