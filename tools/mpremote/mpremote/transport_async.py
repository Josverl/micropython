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

import ast
from .transport import Transport, stdout_write_bytes


class AsyncTransport(Transport):
    """Abstract base class for async transport implementations.

    This class defines the async interface for communicating with MicroPython devices.
    Concrete implementations should override the async methods for specific transport
    types (serial, WebSocket, Bluetooth, etc.).
    """

    async def read_async(self, size: int = 1) -> bytes:
        """Read up to size bytes from transport.

        Args:
            size: Maximum number of bytes to read

        Returns:
            bytes: Data read from transport
        """
        raise NotImplementedError

    async def write_async(self, data: bytes) -> int:
        """Write data to transport.

        Args:
            data: Bytes to write

        Returns:
            int: Number of bytes written
        """
        raise NotImplementedError

    async def read_until_async(
        self, min_num_bytes: int, ending: bytes, timeout: float = 10.0, data_consumer=None
    ) -> bytes:
        """Read until ending pattern found.

        Args:
            min_num_bytes: Minimum number of bytes to read before checking for ending
            ending: Byte pattern to wait for
            timeout: Maximum time to wait in seconds
            data_consumer: Optional callback to consume data as it arrives

        Returns:
            bytes: All data read including ending pattern
        """
        raise NotImplementedError

    async def enter_raw_repl_async(
        self, soft_reset: bool = True, timeout_overall: float = 10.0
    ) -> None:
        """Enter raw REPL mode.

        Args:
            soft_reset: Whether to perform soft reset after entering raw REPL
            timeout_overall: Maximum time for operation in seconds
        """
        raise NotImplementedError

    async def exit_raw_repl_async(self) -> None:
        """Exit raw REPL mode."""
        raise NotImplementedError

    async def exec_raw_no_follow_async(self, command: str) -> None:
        """Execute command in raw REPL without following output.

        Args:
            command: Python code to execute
        """
        raise NotImplementedError

    async def follow_async(self, timeout: float, data_consumer=None) -> tuple:
        """Follow command execution and collect output.

        Args:
            timeout: Maximum time to wait for output
            data_consumer: Optional callback to consume output data

        Returns:
            tuple: (stdout_data, stderr_data)
        """
        raise NotImplementedError

    async def exec_raw_async(
        self, command: str, timeout: float = 10.0, data_consumer=None
    ) -> tuple:
        """Execute command in raw REPL and return output.

        Args:
            command: Python code to execute
            timeout: Maximum time to wait for completion
            data_consumer: Optional callback to consume output data

        Returns:
            tuple: (stdout_data, stderr_data)
        """
        raise NotImplementedError

    async def exec_async(self, command: str, data_consumer=None) -> bytes:
        """Execute command in normal REPL.

        Args:
            command: Python code to execute
            data_consumer: Optional callback to consume output

        Returns:
            bytes: Command output
        """
        raise NotImplementedError

    async def eval_async(self, expression: str, parse: bool = True):
        """Evaluate expression and return result.

        Args:
            expression: Python expression to evaluate
            parse: Whether to parse result as Python literal

        Returns:
            Evaluated result (parsed if parse=True, otherwise bytes)
        """
        raise NotImplementedError

    async def close_async(self) -> None:
        """Close transport connection."""
        raise NotImplementedError

    # Filesystem operations - async versions
    async def fs_listdir_async(self, src: str = ""):
        """List directory contents asynchronously.

        Args:
            src: Remote directory path

        Returns:
            list: Directory entries
        """
        buf = bytearray()

        def repr_consumer(b):
            buf.extend(b.replace(b"\x04", b""))

        cmd = "import os\nfor f in os.ilistdir(%s):\n print(repr(f), end=',')" % (
            ("'%s'" % src) if src else ""
        )
        from .transport import TransportExecError, _convert_filesystem_error, listdir_result

        try:
            buf.extend(b"[")
            await self.exec_async(cmd, data_consumer=repr_consumer)
            buf.extend(b"]")
        except TransportExecError as e:
            raise _convert_filesystem_error(e, src) from None

        return [
            listdir_result(*f) if len(f) == 4 else listdir_result(*(f + (0,)))
            for f in ast.literal_eval(buf.decode())
        ]

    async def fs_stat_async(self, src: str):
        """Get file/directory stats asynchronously.

        Args:
            src: Remote file or directory path

        Returns:
            tuple: File stats (mode, size, etc.)
        """
        result = await self.eval_async(f"import os; os.stat({src!r})")
        return result

    async def fs_readfile_async(
        self, src: str, chunk_size: int = 256, progress_callback=None
    ) -> bytes:
        """Read file from device asynchronously.

        Args:
            src: Remote file path
            chunk_size: Size of chunks to read
            progress_callback: Optional callback for progress updates

        Returns:
            bytes: File contents
        """
        # Implementation will be added by concrete transport classes
        # This is a placeholder that uses the sync implementation
        return self.fs_readfile(src, chunk_size, progress_callback)

    async def fs_writefile_async(
        self, dest: str, data: bytes, chunk_size: int = 256, progress_callback=None
    ) -> None:
        """Write file to device asynchronously.

        Args:
            dest: Remote file path
            data: File contents to write
            chunk_size: Size of chunks to write
            progress_callback: Optional callback for progress updates
        """
        # Implementation will be added by concrete transport classes
        # This is a placeholder that uses the sync implementation
        self.fs_writefile(dest, data, chunk_size, progress_callback)
