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

"""
Tests for commands_async.py module.

These tests are inspired by the shell script tests in:
- test_eval_exec_run.sh
- test_filesystem.sh
- test_mount.sh
- test_resume.sh
"""

import asyncio
import hashlib
import os
import sys
import tempfile
import uuid
from io import BytesIO, StringIO
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest
from mpremote.commands_async import (
    _do_fs_mkdir_async,
    _do_fs_rmdir_async,
    _do_fs_rmfile_async,
    _do_fs_touchfile_async,
    do_eval_async,
    do_eval_sync_wrapper,
    do_exec_async,
    do_exec_sync_wrapper,
    do_filesystem_async,
    do_filesystem_cp_async,
    do_run_async,
    do_run_sync_wrapper,
    do_soft_reset_async,
)
from mpremote.transport import TransportExecError

pytestmark = pytest.mark.async_required


# ============================================================================
# Fixtures for Test Artifacts
# ============================================================================


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test artifacts."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def test_script(temp_dir):
    """Create a test Python script file (inspired by test_eval_exec_run.sh)."""
    script_path = temp_dir / "test_script.py"
    script_path.write_text("print('Hello from script')\n")
    return script_path


@pytest.fixture
def test_exec_file(temp_dir):
    """Create a test exec file with sleep (inspired by test_eval_exec_run.sh)."""
    exec_path = temp_dir / "exec_sleep.py"
    exec_path.write_text(
        "print('before sleep')\nimport time\ntime.sleep(0.1)\nprint('after sleep')\n"
    )
    return exec_path


@pytest.fixture
def test_data_file(temp_dir):
    """Create a test data file (inspired by test_filesystem.sh)."""
    data_path = temp_dir / "a.py"
    data_path.write_text("print('Hello')\nprint('World')\n")
    return data_path


@pytest.fixture
def test_package_structure(temp_dir):
    """
    Create a test package structure (inspired by test_filesystem.sh).

    Structure:
        package/
            __init__.py
            x.py
            subpackage/
                __init__.py
                y.py
    """
    package_dir = temp_dir / "package"
    package_dir.mkdir()

    subpackage_dir = package_dir / "subpackage"
    subpackage_dir.mkdir()

    # Create package files
    (package_dir / "__init__.py").write_text("from .x import x\nfrom .subpackage import y\n")
    (package_dir / "x.py").write_text("def x():\n  print('x')\n")
    (subpackage_dir / "__init__.py").write_text("from .y import y\n")
    (subpackage_dir / "y.py").write_text("def y():\n  print('y')\n")

    return package_dir


@pytest.fixture
def mock_state():
    """Create a mock state object with async transport."""
    state = Mock()
    state.did_action = Mock()
    state.ensure_raw_repl_async = AsyncMock()
    state.transport = Mock()
    return state


@pytest.fixture
def mock_args():
    """Create a mock args object."""
    args = Mock()
    return args


# ============================================================================
# Tests for do_exec_async
# ============================================================================


def test_exec_async_with_file(mock_state, test_exec_file, mock_args, event_loop):
    """Test exec command with file input (inspired by test_eval_exec_run.sh)."""

    async def _test():
        mock_args.command = str(test_exec_file)
        mock_args.follow = False

        mock_state.transport.exec_raw_no_follow_async = AsyncMock()

        await do_exec_async(mock_state, mock_args)

        # Verify state methods called
        mock_state.ensure_raw_repl_async.assert_called_once()
        mock_state.did_action.assert_called_once()

        # Verify exec was called with file contents
        assert mock_state.transport.exec_raw_no_follow_async.called
        call_args = mock_state.transport.exec_raw_no_follow_async.call_args[0]
        assert b"before sleep" in call_args[0]
        assert b"after sleep" in call_args[0]

    event_loop.run_until_complete(_test())


def test_exec_async_with_stdin(mock_state, mock_args, monkeypatch, event_loop):
    """Test exec command with stdin input (inspired by test_eval_exec_run.sh)."""

    async def _test():
        mock_args.command = "-"
        mock_args.follow = False

        # Mock stdin
        stdin_data = b"print('from stdin')\n"
        stdin_mock = Mock()
        stdin_mock.buffer = BytesIO(stdin_data)
        monkeypatch.setattr("sys.stdin", stdin_mock)

        mock_state.transport.exec_raw_no_follow_async = AsyncMock()

        await do_exec_async(mock_state, mock_args)

        # Verify exec was called with stdin contents
        call_args = mock_state.transport.exec_raw_no_follow_async.call_args[0]
        assert call_args[0] == stdin_data

    event_loop.run_until_complete(_test())


def test_exec_async_with_follow(mock_state, test_exec_file, mock_args, event_loop):
    """Test exec command with follow option (inspired by test_eval_exec_run.sh)."""

    async def _test():
        mock_args.command = str(test_exec_file)
        mock_args.follow = True

        mock_state.transport.exec_raw_no_follow_async = AsyncMock()
        mock_state.transport.follow_async = AsyncMock(return_value=(b"output", None))

        await do_exec_async(mock_state, mock_args)

        # Verify follow was called
        mock_state.transport.follow_async.assert_called_once()

    event_loop.run_until_complete(_test())


def test_exec_async_with_follow_error(mock_state, test_exec_file, mock_args, event_loop):
    """Test exec command with follow and error output."""

    async def _test():
        mock_args.command = str(test_exec_file)
        mock_args.follow = True

        mock_state.transport.exec_raw_no_follow_async = AsyncMock()
        mock_state.transport.follow_async = AsyncMock(return_value=(b"output", b"Error occurred"))

        with pytest.raises(TransportExecError) as exc_info:
            await do_exec_async(mock_state, mock_args)

        # TransportExecError contains the error bytes
        assert (
            b"Error occurred" in str(exc_info.value.args).encode()
            or exc_info.value.args[1] == b"Error occurred"
        )

    event_loop.run_until_complete(_test())


# ============================================================================
# Tests for do_eval_async
# ============================================================================


def test_eval_async_simple_expression(mock_state, mock_args, event_loop):
    """Test eval command with simple expression (inspired by test_eval_exec_run.sh)."""

    async def _test():
        mock_args.expression = "1+2"

        # Mock exec_raw_no_follow_async and follow_async (eval now uses exec path)
        mock_state.transport.exec_raw_no_follow_async = AsyncMock()
        mock_state.transport.follow_async = AsyncMock(return_value=(b"3\n", None))

        await do_eval_async(mock_state, mock_args)

        # Verify state methods called
        mock_state.ensure_raw_repl_async.assert_called_once()
        mock_state.did_action.assert_called_once()

        # Verify exec was called with print(expression)
        mock_state.transport.exec_raw_no_follow_async.assert_called_once_with("print(1+2)")

        # Verify follow was called
        mock_state.transport.follow_async.assert_called_once()

    event_loop.run_until_complete(_test())


def test_eval_async_complex_expression(mock_state, mock_args, event_loop):
    """Test eval command with complex expression (inspired by test_eval_exec_run.sh)."""

    async def _test():
        mock_args.expression = "[{'a': 'b'}, (1,2,3,), True]"

        mock_state.transport.exec_raw_no_follow_async = AsyncMock()
        mock_state.transport.follow_async = AsyncMock(
            return_value=(b"[{'a': 'b'}, (1, 2, 3), True]\n", None)
        )

        await do_eval_async(mock_state, mock_args)

        # Verify exec was called with print(expression)
        expected_cmd = "print([{'a': 'b'}, (1,2,3,), True])"
        mock_state.transport.exec_raw_no_follow_async.assert_called_once_with(expected_cmd)

        # Verify follow was called
        mock_state.transport.follow_async.assert_called_once()

    event_loop.run_until_complete(_test())


# ============================================================================
# Tests for do_run_async
# ============================================================================


def test_run_async_script(mock_state, test_script, mock_args, event_loop):
    """Test run command with script file (inspired by test_eval_exec_run.sh)."""

    async def _test():
        mock_args.script = str(test_script)

        mock_state.transport.exec_raw_async = AsyncMock(return_value=(b"output", None))

        await do_run_async(mock_state, mock_args)

        # Verify state methods called
        mock_state.ensure_raw_repl_async.assert_called_once()
        mock_state.did_action.assert_called_once()

        # Verify exec was called with script contents
        assert mock_state.transport.exec_raw_async.called
        call_args = mock_state.transport.exec_raw_async.call_args[0]
        assert b"Hello from script" in call_args[0]

    event_loop.run_until_complete(_test())


def test_run_async_with_error(mock_state, test_script, mock_args, event_loop):
    """Test run command with error output."""

    async def _test():
        mock_args.script = str(test_script)

        mock_state.transport.exec_raw_async = AsyncMock(return_value=(b"output", b"RuntimeError"))

        with pytest.raises(TransportExecError) as exc_info:
            await do_run_async(mock_state, mock_args)

        # TransportExecError contains the error bytes
        assert (
            b"RuntimeError" in str(exc_info.value.args).encode()
            or exc_info.value.args[1] == b"RuntimeError"
        )

    event_loop.run_until_complete(_test())


# ============================================================================
# Tests for do_filesystem_cp_async - Local to Remote
# ============================================================================


def test_filesystem_cp_local_to_remote(mock_state, test_data_file, event_loop):
    """Test copying local file to remote (inspired by test_filesystem.sh)."""

    async def _test():
        src = str(test_data_file)
        dest = ":remote_file.py"

        mock_state.transport.fs_exists_async = AsyncMock(return_value=False)
        mock_state.transport.fs_isdir_async = AsyncMock(return_value=False)
        mock_state.transport.fs_writefile_async = AsyncMock()

        await do_filesystem_cp_async(mock_state, src, dest, False)

        # Verify state methods called
        mock_state.ensure_raw_repl_async.assert_called_once()

        # Verify writefile was called
        assert mock_state.transport.fs_writefile_async.called
        call_args = mock_state.transport.fs_writefile_async.call_args[0]
        assert call_args[0] == "remote_file.py"
        assert b"Hello" in call_args[1]
        assert b"World" in call_args[1]

    event_loop.run_until_complete(_test())


def test_filesystem_cp_local_to_remote_with_hash(mock_state, test_data_file, event_loop):
    """Test copying with hash check (inspired by test_filesystem.sh sha256sum)."""

    async def _test():
        src = str(test_data_file)
        dest = ":remote_file.py"

        # Read file to compute hash
        with open(test_data_file, "rb") as f:
            data = f.read()
        source_hash = hashlib.sha256(data).digest()

        # Mock same hash on remote (file is up to date)
        mock_state.transport.fs_exists_async = AsyncMock(return_value=False)
        mock_state.transport.fs_isdir_async = AsyncMock(return_value=False)
        mock_state.transport.fs_hashfile_async = AsyncMock(return_value=source_hash)
        mock_state.transport.fs_writefile_async = AsyncMock()

        await do_filesystem_cp_async(mock_state, src, dest, False, check_hash=True)

        # Verify writefile was NOT called because hash matched
        mock_state.transport.fs_writefile_async.assert_not_called()

    event_loop.run_until_complete(_test())


def test_filesystem_cp_local_to_remote_hash_mismatch(mock_state, test_data_file, event_loop):
    """Test copying with hash mismatch (inspired by test_filesystem.sh)."""

    async def _test():
        src = str(test_data_file)
        dest = ":remote_file.py"

        # Mock different hash on remote (file needs update)
        mock_state.transport.fs_exists_async = AsyncMock(return_value=False)
        mock_state.transport.fs_isdir_async = AsyncMock(return_value=False)
        mock_state.transport.fs_hashfile_async = AsyncMock(return_value=b"different_hash")
        mock_state.transport.fs_writefile_async = AsyncMock()

        await do_filesystem_cp_async(mock_state, src, dest, False, check_hash=True)

        # Verify writefile WAS called because hash didn't match
        mock_state.transport.fs_writefile_async.assert_called_once()

    event_loop.run_until_complete(_test())


def test_filesystem_cp_local_to_remote_hash_not_exists(mock_state, test_data_file, event_loop):
    """Test copying when remote file doesn't exist (inspired by test_filesystem.sh)."""

    async def _test():
        src = str(test_data_file)
        dest = ":remote_file.py"

        # Mock fs_hashfile raising OSError (file doesn't exist)
        mock_state.transport.fs_exists_async = AsyncMock(return_value=False)
        mock_state.transport.fs_isdir_async = AsyncMock(return_value=False)
        mock_state.transport.fs_hashfile_async = AsyncMock(side_effect=OSError("File not found"))
        mock_state.transport.fs_writefile_async = AsyncMock()

        await do_filesystem_cp_async(mock_state, src, dest, False, check_hash=True)

        # Verify writefile WAS called because file doesn't exist
        mock_state.transport.fs_writefile_async.assert_called_once()

    event_loop.run_until_complete(_test())


# ============================================================================
# Tests for do_filesystem_cp_async - Remote to Local
# ============================================================================


def test_filesystem_cp_remote_to_local(mock_state, temp_dir, event_loop):
    """Test copying remote file to local (inspired by test_filesystem.sh)."""

    async def _test():
        src = ":remote_file.py"
        dest = str(temp_dir / "local_copy.py")

        remote_data = b"print('Remote data')\n"
        mock_state.transport.fs_readfile_async = AsyncMock(return_value=remote_data)

        await do_filesystem_cp_async(mock_state, src, dest, False)

        # Verify state methods called
        mock_state.ensure_raw_repl_async.assert_called_once()

        # Verify readfile was called
        mock_state.transport.fs_readfile_async.assert_called_once()

        # Verify local file was written
        local_file = Path(dest)
        assert local_file.exists()
        assert local_file.read_bytes() == remote_data

    event_loop.run_until_complete(_test())


# ============================================================================
# Tests for do_filesystem_cp_async - Remote to Remote
# ============================================================================


def test_filesystem_cp_remote_to_remote(mock_state, event_loop):
    """Test copying between remote locations (inspired by test_filesystem.sh)."""

    async def _test():
        src = ":source.py"
        dest = ":destination.py"

        remote_data = b"print('Copy on device')\n"
        mock_state.transport.fs_exists_async = AsyncMock(return_value=False)
        mock_state.transport.fs_isdir_async = AsyncMock(return_value=False)
        mock_state.transport.fs_readfile_async = AsyncMock(return_value=remote_data)
        mock_state.transport.fs_writefile_async = AsyncMock()

        await do_filesystem_cp_async(mock_state, src, dest, False)

        # Verify read from source (check just the path, not the callback)
        assert mock_state.transport.fs_readfile_async.called
        call_args = mock_state.transport.fs_readfile_async.call_args[0]
        assert call_args[0] == "source.py"

        # Verify write to destination
        mock_state.transport.fs_writefile_async.assert_called_once()
        call_args = mock_state.transport.fs_writefile_async.call_args[0]
        assert call_args[0] == "destination.py"
        assert call_args[1] == remote_data

    event_loop.run_until_complete(_test())


# ============================================================================
# Tests for do_filesystem_cp_async - Local to Local
# ============================================================================


def test_filesystem_cp_local_to_local(mock_state, test_data_file, temp_dir, event_loop):
    """Test copying between local locations (edge case)."""

    async def _test():
        src = str(test_data_file)
        dest = str(temp_dir / "local_copy.py")

        await do_filesystem_cp_async(mock_state, src, dest, False)

        # Verify state methods called
        mock_state.ensure_raw_repl_async.assert_called_once()

        # Verify local file was written
        local_file = Path(dest)
        assert local_file.exists()
        assert local_file.read_text() == test_data_file.read_text()

    event_loop.run_until_complete(_test())


# ============================================================================
# Tests for Sync Wrappers
# ============================================================================


def test_exec_sync_wrapper(mock_state, test_exec_file, mock_args):
    """Test sync wrapper for exec command."""
    mock_args.command = str(test_exec_file)
    mock_args.follow = False

    mock_state.transport.exec_raw_no_follow_async = AsyncMock()

    # Call sync wrapper
    do_exec_sync_wrapper(mock_state, mock_args)

    # Verify it was executed
    mock_state.ensure_raw_repl_async.assert_called_once()


def test_eval_sync_wrapper(mock_state, mock_args):
    """Test sync wrapper for eval command."""
    mock_args.expression = "1+2"

    # Mock the exec methods used by do_eval_async
    mock_state.transport.exec_raw_no_follow_async = AsyncMock()
    mock_state.transport.follow_async = AsyncMock(return_value=(b"3\n", None))

    # Call sync wrapper
    do_eval_sync_wrapper(mock_state, mock_args)

    # Verify it was executed
    mock_state.ensure_raw_repl_async.assert_called_once()
    mock_state.transport.exec_raw_no_follow_async.assert_called_once_with("print(1+2)")


def test_run_sync_wrapper(mock_state, test_script, mock_args):
    """Test sync wrapper for run command."""
    mock_args.script = str(test_script)

    mock_state.transport.exec_raw_async = AsyncMock(return_value=(b"output", None))

    # Call sync wrapper
    do_run_sync_wrapper(mock_state, mock_args)

    # Verify it was executed
    mock_state.ensure_raw_repl_async.assert_called_once()


def test_soft_reset_async(mock_state, event_loop):
    """Test async soft_reset command."""
    # Call async function
    event_loop.run_until_complete(do_soft_reset_async(mock_state))

    # Verify ensure_raw_repl_async was called with soft_reset=True
    mock_state.ensure_raw_repl_async.assert_called_once_with(soft_reset=True)
    mock_state.did_action.assert_called_once()


# ============================================================================
# Edge Cases and Error Handling
# ============================================================================


def test_exec_async_file_not_found(mock_state, mock_args, event_loop):
    """Test exec with non-existent file."""

    async def _test():
        mock_args.command = "/nonexistent/file.py"
        mock_args.follow = False

        with pytest.raises(FileNotFoundError):
            await do_exec_async(mock_state, mock_args)

    event_loop.run_until_complete(_test())


def test_run_async_file_not_found(mock_state, mock_args, event_loop):
    """Test run with non-existent file."""

    async def _test():
        mock_args.script = "/nonexistent/script.py"

        with pytest.raises(FileNotFoundError):
            await do_run_async(mock_state, mock_args)

    event_loop.run_until_complete(_test())


def test_filesystem_cp_local_file_not_found(mock_state, event_loop):
    """Test filesystem cp with non-existent local file."""

    async def _test():
        src = "/nonexistent/file.py"
        dest = ":remote.py"

        mock_state.transport.fs_exists_async = AsyncMock(return_value=False)
        mock_state.transport.fs_isdir_async = AsyncMock(return_value=False)

        with pytest.raises(FileNotFoundError):
            await do_filesystem_cp_async(mock_state, src, dest, False)

    event_loop.run_until_complete(_test())


def test_filesystem_cp_empty_file(mock_state, temp_dir, event_loop):
    """Test copying empty file (edge case from test_filesystem.sh touch)."""

    async def _test():
        empty_file = temp_dir / "empty.py"
        empty_file.write_text("")

        src = str(empty_file)
        dest = ":remote_empty.py"

        mock_state.transport.fs_exists_async = AsyncMock(return_value=False)
        mock_state.transport.fs_isdir_async = AsyncMock(return_value=False)
        mock_state.transport.fs_writefile_async = AsyncMock()

        await do_filesystem_cp_async(mock_state, src, dest, False)

        # Verify empty file was handled
        call_args = mock_state.transport.fs_writefile_async.call_args[0]
        assert call_args[1] == b""

    event_loop.run_until_complete(_test())


# ============================================================================
# Tests for New Async Filesystem Commands
# ============================================================================


def _create_transport_state(transport):
    class TransportState:
        def __init__(self, transport):
            self.transport = transport
            self._did_action_called = False

        def did_action(self):
            self._did_action_called = True

        async def ensure_raw_repl_async(self):
            # Transport fixture already enters raw REPL.
            return None

    return TransportState(transport)


def _unique_remote_dir(writable_path, prefix):
    base = writable_path.rstrip("/")
    name = f"{prefix}_{uuid.uuid4().hex[:8]}"
    return f"/{name}" if not base else f"{base}/{name}"


async def _cleanup_remote_artifacts(transport, dir_path, file_paths=None):
    file_paths = file_paths or []
    for file_path in file_paths:
        if not file_path:
            continue
        try:
            await transport.fs_rmfile_async(file_path)
        except (OSError, TransportExecError):
            pass

    if dir_path:
        try:
            await transport.fs_rmdir_async(dir_path)
        except (OSError, TransportExecError):
            pass


def test_filesystem_async_operations_integrated(connected_transport, event_loop):
    """Integration test for filesystem async operations."""
    transport, writable_path = connected_transport

    async def _test():
        state = _create_transport_state(transport)

        test_dir = _unique_remote_dir(writable_path, "async_test_dir")
        test_file = f"{test_dir}/test.txt"

        await _cleanup_remote_artifacts(transport, test_dir, [test_file])

        try:
            # Test mkdir
            await _do_fs_mkdir_async(state, test_dir)

            # Verify directory exists
            stat = await transport.fs_stat_async(test_dir)
            assert stat[0] & 0x4000  # Is directory

            # Test touch
            await _do_fs_touchfile_async(state, test_file)

            # Verify file exists
            stat = await transport.fs_stat_async(test_file)
            assert not (stat[0] & 0x4000)  # Is not directory

            # Test rm
            await _do_fs_rmfile_async(state, test_file)

            # Verify file removed
            with pytest.raises(TransportExecError):
                await transport.fs_stat_async(test_file)

            # Test rmdir
            await _do_fs_rmdir_async(state, test_dir)

            # Verify directory removed
            with pytest.raises(TransportExecError):
                await transport.fs_stat_async(test_dir)
        finally:
            await _cleanup_remote_artifacts(transport, test_dir, [test_file])

    event_loop.run_until_complete(_test())


def test_filesystem_async_mkdir_creates_directory(connected_transport, event_loop):
    transport, writable_path = connected_transport

    async def _test():
        state = _create_transport_state(transport)
        test_dir = _unique_remote_dir(writable_path, "mkdir_dir")

        await _cleanup_remote_artifacts(transport, test_dir)
        try:
            await _do_fs_mkdir_async(state, test_dir)
            stat = await transport.fs_stat_async(test_dir)
            assert stat[0] & 0x4000
        finally:
            await _cleanup_remote_artifacts(transport, test_dir)

    event_loop.run_until_complete(_test())


def test_filesystem_async_touchfile_creates_file(connected_transport, event_loop):
    transport, writable_path = connected_transport

    async def _test():
        state = _create_transport_state(transport)
        test_dir = _unique_remote_dir(writable_path, "touch_dir")
        test_file = f"{test_dir}/touch.txt"

        await _cleanup_remote_artifacts(transport, test_dir, [test_file])
        try:
            await _do_fs_mkdir_async(state, test_dir)
            await _do_fs_touchfile_async(state, test_file)
            stat = await transport.fs_stat_async(test_file)
            assert not (stat[0] & 0x4000)
        finally:
            await _cleanup_remote_artifacts(transport, test_dir, [test_file])

    event_loop.run_until_complete(_test())


def test_filesystem_async_rmfile_removes_file(connected_transport, event_loop):
    transport, writable_path = connected_transport

    async def _test():
        state = _create_transport_state(transport)
        test_dir = _unique_remote_dir(writable_path, "rmfile_dir")
        test_file = f"{test_dir}/remove.txt"

        await _cleanup_remote_artifacts(transport, test_dir, [test_file])
        try:
            await _do_fs_mkdir_async(state, test_dir)
            await _do_fs_touchfile_async(state, test_file)
            await _do_fs_rmfile_async(state, test_file)
            with pytest.raises(TransportExecError):
                await transport.fs_stat_async(test_file)
        finally:
            await _cleanup_remote_artifacts(transport, test_dir, [test_file])

    event_loop.run_until_complete(_test())


def test_filesystem_async_rmdir_removes_directory(connected_transport, event_loop):
    transport, writable_path = connected_transport

    async def _test():
        state = _create_transport_state(transport)
        test_dir = _unique_remote_dir(writable_path, "rmdir_dir")

        await _cleanup_remote_artifacts(transport, test_dir)
        try:
            await _do_fs_mkdir_async(state, test_dir)
            await _do_fs_rmdir_async(state, test_dir)
            with pytest.raises(TransportExecError):
                await transport.fs_stat_async(test_dir)
        finally:
            await _cleanup_remote_artifacts(transport, test_dir)

    event_loop.run_until_complete(_test())
