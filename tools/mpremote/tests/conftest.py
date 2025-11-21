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

import ast
import asyncio
import os
import sys
import tempfile
from collections.abc import Callable, Generator
from pathlib import Path
from textwrap import dedent
from typing import Any

import pytest

TESTS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TESTS_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# Check for async module availability
AsyncConsole = None
AsyncTransport = None
AsyncSerialTransport = None
RawREPLProtocol = None
do_exec_async = None
do_eval_async = None
try:
    from mpremote.commands_async import do_eval_async, do_exec_async
    from mpremote.console_async import AsyncConsole
    from mpremote.protocol import RawREPLProtocol
    from mpremote.transport_async import AsyncTransport
    from mpremote.transport_serial_async import AsyncSerialTransport

    HAS_ASYNC = True
    ASYNC_IMPORT_ERROR = None
except ImportError as e:
    HAS_ASYNC = False
    ASYNC_IMPORT_ERROR = str(e)

# Check for serial module availability
serial_list_ports = None
try:
    from serial.tools import list_ports as serial_list_ports

    HAS_SERIAL = True
except ImportError:
    HAS_SERIAL = False

# Check for serial_asyncio availability
try:
    import serial_asyncio

    HAS_SERIAL_ASYNCIO = True
except ImportError:
    HAS_SERIAL_ASYNCIO = False
    serial_asyncio = None


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
        if "serial_required" in item.keywords and not HAS_SERIAL_ASYNCIO:
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
def platform_info() -> dict[str, Any]:
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
def async_modules() -> dict[str, Any]:
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
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
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

_TARGET_INFO_SCRIPT = dedent(
    """
    import sys
    _impl = getattr(sys, 'implementation', None)
    info = {
        'platform': getattr(sys, 'platform', ''),
        'version': getattr(sys, 'version', ''),
        'implementation_name': getattr(_impl, 'name', '') if _impl else '',
        'implementation_version': tuple(getattr(_impl, 'version', ())) if _impl else (),
        'implementation_mpy': getattr(_impl, '_mpy', None) if _impl else None,
        'implementation_build': getattr(_impl, '_build', '') if _impl else '',
        'implementation_machine': getattr(_impl, '_machine', '') if _impl else '',
        'implementation_thread': getattr(_impl, '_thread', '') if _impl else '',
    }
    if hasattr(sys, 'machine'):
        info['machine'] = getattr(sys, 'machine')
    else:
        info['machine'] = info['implementation_machine']
    print(repr(info))
    """
)


def _parse_target_info(payload: str) -> dict:
    """Parse the target info payload emitted by the device."""

    payload = payload.strip()
    if not payload:
        return {}

    try:
        result = ast.literal_eval(payload)
    except (ValueError, SyntaxError) as exc:  # pragma: no cover
        raise RuntimeError(f"Unable to parse target metadata: {payload}") from exc

    if not isinstance(result, dict):  # pragma: no cover - sanity check
        raise RuntimeError(f"Unexpected metadata payload: {payload}")

    return result


def find_micropython_device() -> str | None:
    """Find the first available MicroPython device."""
    if not HAS_SERIAL or serial_list_ports is None:
        return None

    try:
        ports = serial_list_ports.comports()
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
def test_device_port(request) -> str | None:
    """
    Get test device port from command line, environment, or auto-detect.

    Priority order:
    1. Command line: pytest --device=COM20 or pytest --device=/dev/ttyUSB0
    2. Environment: MICROPYTHON_DEVICE=COM20 pytest ...
    3. Auto-detect: First available serial port (cross-platform)

    Returns None if no device is found, causing hardware tests to be skipped.
    """
    # 1. Check command line argument
    device = request.config.getoption("--device", default=None)
    if device:
        return device

    # 2. Check environment variable
    device = os.environ.get("MICROPYTHON_DEVICE")
    if device:
        return device

    # 3. Try to auto-detect first available serial port
    device = find_micropython_device()
    if device:
        return device

    return None


@pytest.fixture(scope="session")
def hardware_target_info(test_device_port: str | None) -> dict[str, Any]:
    """Collect sys.platform/sys.implementation metadata for the connected device."""

    if test_device_port is None:
        pytest.skip("No MicroPython device available")

    if not HAS_ASYNC:
        pytest.skip(f"Async modules not available: {ASYNC_IMPORT_ERROR}")

    transport = AsyncSerialTransport(test_device_port, baudrate=115200)  # type: ignore
    loop = asyncio.new_event_loop()

    async def _probe():
        try:
            await asyncio.wait_for(transport.connect(), timeout=5.0)
            await transport.enter_raw_repl_async()
            stdout, _ = await transport.exec_raw_async(_TARGET_INFO_SCRIPT)
            return stdout.decode(errors="ignore")
        finally:
            try:
                await transport.close_async()
            except Exception:
                pass

    try:
        payload = loop.run_until_complete(_probe())
    finally:
        loop.close()

    info = _parse_target_info(payload)
    info.setdefault("device", test_device_port)
    return info


@pytest.fixture
def require_dut(
    hardware_target_info: dict[str, Any],
    request: pytest.FixtureRequest,
) -> Callable[..., dict[str, Any]]:
    """
    Skip tests when the connected device (DUT, device under test) does not match the requested platform.

    This fixture provides a callable that checks if the connected MicroPython device
    meets the specified requirements for platform, implementation, and machine type.
    If the requirements are not met, the test is skipped with an appropriate message.

    Args:
        hardware_target_info: Dictionary containing information about the connected device,
            including 'platform', 'implementation_name', and 'implementation_machine'.

    Returns:
        A callable that accepts the following keyword arguments:
            platform: str | list[str] | None
                The required MicroPython platform(s) (sys.platform). Can be a single string
                or a list of acceptable platforms.
            implementation: str | None
                The required MicroPython implementation name (e.g., 'micropython', 'circuitpython').
            machine_substring: str | None
                A substring that must be present in the machine description.
        The callable returns the hardware_target_info dictionary if all requirements are met,
        otherwise it skips the test.

    Example:
        def test_esp32_specific_feature(require_dut):
            # Skip this test if the device is not an ESP32
            require_dut(platform="esp32")
            # Test code here will only run on ESP32 devices
            assert True

        def test_unix_or_rp2_feature(require_dut):
            # Skip if device is neither unix nor rp2
            require_dut(platform=["unix", "rp2"])
            # Test code here runs on unix or rp2 platforms
            assert True

        def test_pico_board(require_dut):
            # Skip if not running on a Raspberry Pi Pico variant
            require_dut(
                platform="rp2",
                machine_substring="Pico"
            )
            # Test code specific to Pico boards
            assert True

        def test_micropython_implementation(require_dut):
            # Skip if not running official MicroPython implementation
            info = require_dut(implementation="micropython")
            # Use returned info if needed
            assert info["implementation_name"] == "micropython"
    """

    test_id = request.node.nodeid

    def _skip(reason: str) -> None:
        pytest.skip(f"{test_id}: {reason}")

    def _require(
        *,
        platform: str | list[str] | None = None,
        implementation: str | None = None,
        machine_substring: str | None = None,
    ) -> dict[str, Any]:
        actual_platform = str(hardware_target_info.get("platform", "")).lower()
        actual_impl = str(hardware_target_info.get("implementation_name", "")).lower()
        actual_machine = str(hardware_target_info.get("implementation_machine", "")).lower()

        if platform is not None:
            expected = (
                {platform.lower()} if isinstance(platform, str) else {p.lower() for p in platform}
            )
            if actual_platform not in expected:
                _skip(
                    f"requires platform {expected}, device reports platform '{actual_platform or 'unknown'}'"
                )

        if implementation is not None and actual_impl != implementation.lower():
            _skip(
                f"requires implementation '{implementation}', device reports '{actual_impl or 'unknown'}'"
            )

        if machine_substring is not None and machine_substring.lower() not in actual_machine:
            _skip(
                f"requires machine containing '{machine_substring}', device reports '{actual_machine or 'unknown'}'"
            )

        return hardware_target_info

    return _require


@pytest.fixture
def hardware_device(test_device_port: str | None) -> str:
    """Provide hardware device port or skip test if not available."""
    if test_device_port is None:
        pytest.skip("No MicroPython device available")
    return test_device_port


@pytest.fixture
def connected_transport(
    hardware_device: str,
    hardware_target_info: dict[str, Any],
    async_modules: dict[str, Any],
    event_loop: asyncio.AbstractEventLoop,
) -> Generator[tuple[Any, str], None, None]:
    """
    Create and connect an async transport to hardware device.

    Automatically cleans up connection after test.
    Returns a tuple of (transport, writable_path) and adds a `target_info`
    attribute to the transport containing sys.platform/sys.implementation metadata.
    """
    AsyncSerialTransport = async_modules["AsyncSerialTransport"]

    async def _get_transport():
        transport = AsyncSerialTransport(hardware_device, baudrate=115200)
        await asyncio.wait_for(transport.connect(), timeout=5.0)
        await transport.enter_raw_repl_async()

        # Detect writable path
        code = dedent(
            """
            import os
            writable_path = None
            test_paths = ['/', '/flash', '/sd']
            for path in test_paths:
                try:
                    items = os.listdir(path)
                    test_file = path + '/.test_write'
                    with open(test_file, 'w') as f:
                        f.write('test')
                    os.remove(test_file)
                    writable_path = path
                    break
                except (OSError, AttributeError):
                    continue
            print(writable_path if writable_path else 'NONE')
            """
        )
        stdout, _ = await transport.exec_raw_async(code)
        result = stdout.strip().decode()
        writable_path = None if result == "NONE" else result

        if writable_path is None:
            pytest.skip("No writable filesystem available on device")

        transport.target_info = dict(hardware_target_info)
        return transport, writable_path

    # Run async setup
    transport, writable_path = event_loop.run_until_complete(_get_transport())

    yield (transport, writable_path)

    # Cleanup
    async def _cleanup():
        try:
            await transport.close_async()
        except Exception:
            pass

    event_loop.run_until_complete(_cleanup())


@pytest.fixture
def get_writable_path() -> Callable[[Any], Any]:
    """
    Return a helper function that detects writable filesystem path on device.

    Usage:
        writable_path = await get_writable_path(transport)
        if writable_path is None:
            pytest.skip("No writable filesystem available")
    """

    async def _get_writable_path(transport: Any) -> str | None:
        """Detect and return writable path on device, or None if none available."""
        code = dedent(
            """
            import os
            writable_path = None
            test_paths = ['/', '/flash', '/sd']
            for path in test_paths:
                try:
                    items = os.listdir(path)
                    test_file = path + '/.test_write'
                    with open(test_file, 'w') as f:
                        f.write('test')
                    os.remove(test_file)
                    writable_path = path
                    break
                except (OSError, AttributeError):
                    continue
            print(writable_path if writable_path else 'NONE')
            """
        )
        stdout = await transport.exec_async(code)
        result = stdout.strip().decode()
        return None if result == "NONE" else result

    return _get_writable_path


# ============================================================================
# MicroPython Unix Port Fixtures
# ============================================================================


@pytest.fixture(scope="session")
def micropython_unix_binary() -> str | None:
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
# CLI Fixtures
# ============================================================================


_ASYNC_TEST_FLAG = os.environ.get("MPREMOTE_TEST_ENABLE_ASYNC", "").lower() in {
    "1",
    "true",
    "yes",
    "on",
}


@pytest.fixture(params=["sync", "async"])
def cli_mode(request: pytest.FixtureRequest) -> str:
    """Yield desired CLI mode, skipping async unless explicitly enabled."""
    mode = request.param
    if mode == "async" and not _ASYNC_TEST_FLAG:
        pytest.skip("async CLI temporarily disabled (set MPREMOTE_TEST_ENABLE_ASYNC=1 to enable)")
    return mode


@pytest.fixture
def mpremote_cmd(cli_mode: str) -> list[str]:
    """Get mpremote command with appropriate mode flag."""
    mpremote = os.environ.get("MPREMOTE", "mpremote")
    if cli_mode == "async":
        return [mpremote, "--async"]
    else:
        return [mpremote]


@pytest.fixture
def temp_script() -> Generator[str, None, None]:
    """Create temporary script file."""
    fd, path = tempfile.mkstemp(suffix=".py", prefix="mpremote_test_")
    os.close(fd)
    yield path
    try:
        os.unlink(path)
    except:
        pass


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
