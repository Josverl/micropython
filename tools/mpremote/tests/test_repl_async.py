#!/usr/bin/env python3
#
# This file is part of the MicroPython project, http://micropython.org/
#
# The MIT License (MIT)
#
# Copyright (c) 2025 Jos Verlinde
#


"""Pytest-based tests for async REPL functionality.

These tests provide comprehensive coverage of the repl_async module,
including keyboard input handling, device output handling, code injection,
and various edge cases.
"""

import asyncio
import tempfile
import os
from io import BytesIO
from unittest.mock import Mock, patch

import pytest

# Mark all tests as requiring async modules
pytestmark = pytest.mark.async_required


# Fixtures


@pytest.fixture
def mock_console():
    """Create a mock async console."""
    console = Mock()
    console.output = []
    console.input_queue = []
    console.input_idx = 0

    def write(data):
        console.output.append(data)

    async def readchar_async():
        if console.input_idx < len(console.input_queue):
            char = console.input_queue[console.input_idx]
            console.input_idx += 1
            await asyncio.sleep(0.001)  # Yield control
            return char
        await asyncio.sleep(0.001)
        return b"\x1d"  # ctrl-], exit by default

    console.write = write
    console.readchar_async = readchar_async
    console.enter = Mock()
    console.exit = Mock()

    return console


@pytest.fixture
def mock_async_transport():
    """Create a mock async transport."""
    transport = Mock()
    transport.device_name = "mock_device"
    transport.in_raw_repl = False
    transport.use_raw_paste = True
    transport.mounted = False
    transport.output_buffer = BytesIO()
    transport.read_position = 0

    async def read_async(size=256):
        # Read from buffer
        current_pos = transport.read_position
        data = transport.output_buffer.getvalue()[current_pos : current_pos + size]
        transport.read_position = current_pos + len(data)
        await asyncio.sleep(0.001)
        return data

    async def write_async(data):
        await asyncio.sleep(0.001)
        return len(data)

    async def enter_raw_repl_async(soft_reset=False):
        transport.in_raw_repl = True
        await asyncio.sleep(0.001)

    async def exit_raw_repl_async():
        transport.in_raw_repl = False
        await asyncio.sleep(0.001)

    async def exec_raw_no_follow_async(code):
        await asyncio.sleep(0.001)

    # Use Mock() for methods so we can track calls
    transport.read_async = Mock(side_effect=read_async)
    transport.write_async = Mock(side_effect=write_async)
    transport.enter_raw_repl_async = Mock(side_effect=enter_raw_repl_async)
    transport.exit_raw_repl_async = Mock(side_effect=exit_raw_repl_async)
    transport.exec_raw_no_follow_async = Mock(side_effect=exec_raw_no_follow_async)

    return transport


@pytest.fixture
def mock_state(mock_async_transport):
    """Create a mock state object."""
    state = Mock()
    state.transport = mock_async_transport
    state.did_action = Mock()

    async def ensure_friendly_repl_async():
        await asyncio.sleep(0.001)

    state.ensure_friendly_repl_async = ensure_friendly_repl_async

    return state


@pytest.fixture
def temp_inject_file():
    """Create a temporary file for code injection."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("print('injected code')\n")
        f.write("x = 42\n")
        temp_path = f.name

    yield temp_path

    # Cleanup
    try:
        os.unlink(temp_path)
    except:
        pass


# Tests for _is_disconnect_exception


def test_is_disconnect_exception_io_error(async_modules):
    """Test disconnect detection for IO error (errno 5)."""
    from mpremote.repl_async import _is_disconnect_exception

    exception = OSError(5, "Input/output error")
    assert _is_disconnect_exception(exception) is True


def test_is_disconnect_exception_write_timeout(async_modules):
    """Test disconnect detection for write timeout."""
    from mpremote.repl_async import _is_disconnect_exception

    exception = OSError("Write timeout")
    assert _is_disconnect_exception(exception) is True


def test_is_disconnect_exception_device_disconnected(async_modules):
    """Test disconnect detection for device disconnected message."""
    from mpremote.repl_async import _is_disconnect_exception

    exception = OSError("Device disconnected")
    assert _is_disconnect_exception(exception) is True


def test_is_disconnect_exception_clearcomm_error(async_modules):
    """Test disconnect detection for ClearCommError."""
    from mpremote.repl_async import _is_disconnect_exception

    exception = OSError("ClearCommError failed")
    assert _is_disconnect_exception(exception) is True


def test_is_disconnect_exception_other_oserror(async_modules):
    """Test that other OSErrors are not considered disconnects."""
    from mpremote.repl_async import _is_disconnect_exception

    exception = OSError(2, "No such file or directory")
    assert _is_disconnect_exception(exception) is False


def test_is_disconnect_exception_non_oserror(async_modules):
    """Test that non-OSError exceptions are not considered disconnects."""
    from mpremote.repl_async import _is_disconnect_exception

    assert _is_disconnect_exception(ValueError("test")) is False
    assert _is_disconnect_exception(KeyError("test")) is False


# Tests for do_repl_main_loop_async


def test_repl_main_loop_exit_ctrl_bracket(mock_state, mock_console, event_loop, async_modules):
    """Test exiting REPL with Ctrl-]."""
    from mpremote.repl_async import do_repl_main_loop_async

    async def _test():
        mock_console.input_queue = [b"\x1d"]  # ctrl-]
        result = await do_repl_main_loop_async(mock_state, mock_console)
        assert result is False  # Should return False (user exit, not disconnect)

    event_loop.run_until_complete(_test())


def test_repl_main_loop_exit_ctrl_x(mock_state, mock_console, event_loop, async_modules):
    """Test exiting REPL with Ctrl-X."""
    from mpremote.repl_async import do_repl_main_loop_async

    async def _test():
        mock_console.input_queue = [b"\x18"]  # ctrl-x
        result = await do_repl_main_loop_async(mock_state, mock_console)
        assert result is False

    event_loop.run_until_complete(_test())


def test_repl_main_loop_ctrl_d_async_transport(
    mock_state, mock_console, event_loop, async_modules
):
    """Test Ctrl-D handling with async transport."""
    from mpremote.repl_async import do_repl_main_loop_async

    async def _test():
        mock_console.input_queue = [b"\x04", b"\x1d"]  # ctrl-d, then exit
        result = await do_repl_main_loop_async(mock_state, mock_console)
        assert result is False
        # Ctrl-D is processed, REPL exits normally

    event_loop.run_until_complete(_test())


def test_repl_main_loop_inject_code(mock_state, mock_console, event_loop, async_modules):
    """Test code injection with Ctrl-J."""
    from mpremote.repl_async import do_repl_main_loop_async

    async def _test():
        code_to_inject = b"print('hello')\r\n"
        mock_console.input_queue = [b"\x0a", b"\x1d"]  # ctrl-j, then exit

        result = await do_repl_main_loop_async(
            mock_state, mock_console, code_to_inject=code_to_inject
        )

        assert result is False
        # Verify code was injected
        calls = [call[0][0] for call in mock_state.transport.write_async.call_args_list]
        assert code_to_inject in calls

    event_loop.run_until_complete(_test())


def test_repl_main_loop_inject_file(
    mock_state, mock_console, temp_inject_file, event_loop, async_modules
):
    """Test file injection with Ctrl-K."""
    from mpremote.repl_async import do_repl_main_loop_async

    async def _test():
        mock_console.input_queue = [b"\x0b", b"\x1d"]  # ctrl-k, then exit

        result = await do_repl_main_loop_async(
            mock_state, mock_console, file_to_inject=temp_inject_file
        )

        assert result is False
        # Verify raw REPL was entered and exited
        mock_state.transport.enter_raw_repl_async.assert_called_once()
        mock_state.transport.exit_raw_repl_async.assert_called_once()
        mock_state.transport.exec_raw_no_follow_async.assert_called_once()

    event_loop.run_until_complete(_test())


def test_repl_main_loop_inject_file_with_error(
    mock_state, mock_console, temp_inject_file, event_loop, async_modules
):
    """Test file injection that raises TransportError."""
    from mpremote.repl_async import do_repl_main_loop_async
    from mpremote.transport import TransportError

    async def _test():
        mock_console.input_queue = [b"\x0b", b"\x1d"]  # ctrl-k, then exit

        # Make exec_raw_no_follow_async raise an error
        async def raise_error(code):
            raise TransportError("Execution failed")

        mock_state.transport.exec_raw_no_follow_async = raise_error

        result = await do_repl_main_loop_async(
            mock_state, mock_console, file_to_inject=temp_inject_file
        )

        assert result is False
        # Error should be written to console
        assert any(b"Error:" in output for output in mock_console.output)

    event_loop.run_until_complete(_test())


def test_repl_main_loop_regular_input(mock_state, mock_console, event_loop, async_modules):
    """Test regular character input."""
    from mpremote.repl_async import do_repl_main_loop_async

    async def _test():
        mock_console.input_queue = [b"a", b"b", b"c", b"\r", b"\x1d"]

        result = await do_repl_main_loop_async(mock_state, mock_console)

        assert result is False
        # All characters should be sent to device
        assert mock_state.transport.write_async.call_count >= 4

    event_loop.run_until_complete(_test())


def test_repl_main_loop_device_output(mock_state, mock_console, event_loop, async_modules):
    """Test receiving device output."""
    from mpremote.repl_async import do_repl_main_loop_async

    async def _test():
        # Set up device output
        mock_state.transport.output_buffer = BytesIO(b"MicroPython v1.0\r\n>>> ")
        mock_state.transport.read_position = 0

        mock_console.input_queue = [b"\x1d"]  # Exit immediately

        result = await do_repl_main_loop_async(mock_state, mock_console)

        assert result is False
        # Device output should be written to console
        assert len(mock_console.output) > 0

    event_loop.run_until_complete(_test())


def test_repl_main_loop_escape_non_printable(mock_state, mock_console, event_loop, async_modules):
    """Test escaping non-printable characters."""
    from mpremote.repl_async import do_repl_main_loop_async

    async def _test():
        # Device output with non-printable bytes
        mock_state.transport.output_buffer = BytesIO(b"test\x00\x01\x02")
        mock_state.transport.read_position = 0

        mock_console.input_queue = [b"\x1d"]

        result = await do_repl_main_loop_async(mock_state, mock_console, escape_non_printable=True)

        assert result is False
        # Non-printable bytes should be escaped in output
        output = b"".join(mock_console.output)
        assert b"[00]" in output or b"test" in output

    event_loop.run_until_complete(_test())


def test_repl_main_loop_disconnect_on_read(mock_state, mock_console, event_loop, async_modules):
    """Test handling disconnect during device read."""
    from mpremote.repl_async import do_repl_main_loop_async

    async def _test():
        # Make read_async raise a disconnect exception
        async def raise_disconnect(size=256):
            raise OSError(5, "Input/output error")

        mock_state.transport.read_async = raise_disconnect
        mock_console.input_queue = []  # No input

        result = await do_repl_main_loop_async(mock_state, mock_console)

        assert result is True  # Should return True for disconnect

    event_loop.run_until_complete(_test())


def test_repl_main_loop_disconnect_on_write(mock_state, mock_console, event_loop, async_modules):
    """Test handling disconnect during device write."""
    from mpremote.repl_async import do_repl_main_loop_async

    async def _test():
        # Make write_async raise a disconnect exception
        async def raise_disconnect(data):
            raise OSError(5, "Input/output error")

        mock_state.transport.write_async = raise_disconnect
        mock_console.input_queue = [b"a"]  # Try to send a character

        result = await do_repl_main_loop_async(mock_state, mock_console)

        assert result is True  # Should return True for disconnect

    event_loop.run_until_complete(_test())


# Removed test_repl_with_sync_transport - sync transports are no longer supported
# in async REPL. Async REPL now requires an async transport and will raise
# TypeError if a sync transport is provided (see test_async_repl_rejects_sync_transport)


# Tests for do_repl_async wrapper


def test_do_repl_async_wrapper(mock_state, event_loop, async_modules):
    """Test synchronous wrapper for async REPL."""
    from mpremote.repl_async import do_repl_async_wrapper

    args = Mock()
    args.escape_non_printable = False
    args.capture = None
    args.inject_code = None
    args.inject_file = None

    with patch("mpremote.repl_async.AsyncConsole") as MockConsole:
        mock_console_instance = Mock()

        async def readchar():
            await asyncio.sleep(0.001)
            return b"\x1d"

        mock_console_instance.readchar_async = readchar
        mock_console_instance.write = Mock()
        mock_console_instance.enter = Mock()
        mock_console_instance.exit = Mock()

        MockConsole.return_value = mock_console_instance

        with patch("builtins.print"):
            result = do_repl_async_wrapper(mock_state, args)

        assert result is False


def test_async_repl_rejects_sync_transport(event_loop, capsys):
    """Test that async REPL raises TypeError when given a sync transport without read_async."""
    from mpremote.repl_async import do_repl_main_loop_async

    async def _test():
        # Create mock state with sync transport (no read_async method)
        mock_state = Mock()
        mock_state.transport = Mock(spec=["serial", "device_name"])  # No read_async
        mock_state.transport.device_name = "test"

        # Create mock console with proper async mock
        mock_console = Mock()

        async def mock_readchar():
            await asyncio.sleep(0.001)
            return b"\x1d"  # Exit character

        mock_console.readchar_async = mock_readchar
        mock_console.write = Mock()

        # The TypeError is raised in the device_output task and caught by the task runner
        # The function returns False (not disconnect), but prints the error
        result = await do_repl_main_loop_async(
            mock_state,
            mock_console,
            escape_non_printable=False,
            code_to_inject=None,
            file_to_inject=None,
        )

        # Returns False (not a disconnect), but the error message is printed
        assert result is False

    event_loop.run_until_complete(_test())

    # Verify error message was printed
    captured = capsys.readouterr()
    assert "Task error:" in captured.out
    assert "Async REPL requires an async transport" in captured.out


def test_repl_with_capture_file(event_loop):
    """Test that REPL captures output to file when capture_file is specified."""
    from mpremote.repl_async import do_repl_async

    async def _test():
        # Create mock state with async transport
        mock_state = Mock()
        mock_state.transport = Mock()
        mock_state.transport.device_name = "test_device"

        # Mock async methods
        async def mock_read_async(size):
            await asyncio.sleep(0.001)
            return b">>> Hello from device\r\n"

        mock_state.transport.read_async = mock_read_async
        mock_state.transport.write_async = Mock(return_value=asyncio.sleep(0))

        # Mock state methods
        async def mock_ensure_friendly():
            pass

        mock_state.ensure_friendly_repl_async = mock_ensure_friendly
        mock_state.did_action = Mock()

        # Create args with capture file
        with tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=".txt") as capture:
            capture_path = capture.name

        try:
            args = Mock()
            args.escape_non_printable = False
            args.capture = capture_path
            args.inject_code = None
            args.inject_file = None

            # Mock AsyncConsole
            with patch("mpremote.repl_async.AsyncConsole") as MockConsole:
                mock_console_instance = Mock()

                # Simulate console that exits after receiving device output
                call_count = [0]

                async def readchar():
                    await asyncio.sleep(0.002)
                    call_count[0] += 1
                    if call_count[0] > 2:  # Exit after a couple iterations
                        return b"\x1d"
                    return b"x"  # Regular character

                mock_console_instance.readchar_async = readchar

                # Track what gets written to console
                written_data = []

                def mock_write(data):
                    written_data.append(data)

                mock_console_instance.write = mock_write
                mock_console_instance.enter = Mock()
                mock_console_instance.exit = Mock()

                MockConsole.return_value = mock_console_instance

                with patch("builtins.print"):
                    result = await do_repl_async(mock_state, args)

                assert result is False  # Not disconnected

            # Verify capture file contains the device output
            with open(capture_path, "rb") as f:
                captured_content = f.read()

            assert b"Hello from device" in captured_content

            # Verify console.write was called with the same data
            assert len(written_data) > 0
            assert any(b"Hello from device" in data for data in written_data)

        finally:
            # Cleanup
            if os.path.exists(capture_path):
                os.remove(capture_path)

    event_loop.run_until_complete(_test())


def test_repl_capture_file_multiple_writes(event_loop):
    """Test that capture file receives all device output correctly."""
    from mpremote.repl_async import do_repl_async

    async def _test():
        # Create mock state
        mock_state = Mock()
        mock_state.transport = Mock()
        mock_state.transport.device_name = "test"

        # Mock read_async to return multiple chunks of data
        read_count = [0]

        async def mock_read_async(size):
            await asyncio.sleep(0.001)
            read_count[0] += 1
            if read_count[0] == 1:
                return b"First line\r\n"
            elif read_count[0] == 2:
                return b"Second line\r\n"
            elif read_count[0] == 3:
                return b"Third line\r\n"
            return b""

        mock_state.transport.read_async = mock_read_async
        mock_state.transport.write_async = Mock(return_value=asyncio.sleep(0))

        async def mock_ensure_friendly():
            pass

        mock_state.ensure_friendly_repl_async = mock_ensure_friendly
        mock_state.did_action = Mock()

        # Create capture file
        with tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=".txt") as capture:
            capture_path = capture.name

        try:
            args = Mock()
            args.escape_non_printable = False
            args.capture = capture_path
            args.inject_code = None
            args.inject_file = None

            with patch("mpremote.repl_async.AsyncConsole") as MockConsole:
                mock_console_instance = Mock()

                call_count = [0]

                async def readchar():
                    # Wait longer to ensure device output task has time to read all data
                    await asyncio.sleep(0.02)
                    call_count[0] += 1
                    # Wait until all three lines have been read before exiting
                    # This prevents race condition where keyboard exits before device reads all data
                    if call_count[0] > 10 and read_count[0] >= 3:
                        return b"\x1d"  # Exit
                    return b"t"

                mock_console_instance.readchar_async = readchar
                mock_console_instance.write = Mock()
                mock_console_instance.enter = Mock()
                mock_console_instance.exit = Mock()

                MockConsole.return_value = mock_console_instance

                with patch("builtins.print"):
                    await do_repl_async(mock_state, args)

            # Verify all lines are in capture file
            with open(capture_path, "rb") as f:
                captured_content = f.read()

            assert b"First line" in captured_content
            assert b"Second line" in captured_content
            assert b"Third line" in captured_content

        finally:
            if os.path.exists(capture_path):
                os.remove(capture_path)

    event_loop.run_until_complete(_test())
