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

# Minimum file size (in bytes) to use auto-detection and optimization.
# For smaller files, use a fixed 256-byte chunk to avoid memory query overhead.
MIN_FILE_SIZE_FOR_AUTO_DETECTION = 3 * 1024  # 3KB


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
        # Use exec_async with print(repr()) since eval_async can't handle imports
        result = await self.exec_async(f"import os\nprint(repr(os.stat({src!r})))")
        # Parse the repr() output back to tuple
        import ast

        return ast.literal_eval(result.decode().strip())

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
        # Read file contents using exec_async
        result = await self.exec_async(f"print(open({src!r}, 'rb').read())")
        # The result has b'...' format, need to decode it
        import ast

        return ast.literal_eval(result.decode().strip())

    async def detect_optimal_chunk_size_async(self) -> int:
        """Auto-detect optimal chunk size based on available device memory.

        This is called once per connection and cached. It queries free memory
        and selects an appropriate chunk size that balances performance with
        memory constraints.

        Returns:
            int: Recommended chunk size in bytes (256-2048)
        """
        if self._optimal_chunk_size is not None:
            return self._optimal_chunk_size

        try:
            # Try to get free memory using gc.mem_free()
            free_mem_bytes = await self.eval_async("__import__('gc').mem_free()", parse=False)
            free_mem_kb = int(free_mem_bytes.decode().strip()) / 1024
            self._free_memory_kb = free_mem_kb

            # Determine optimal chunk size based on available memory
            # Conservative approach: use ~1-2% of free memory for chunk
            # but cap at reasonable limits for performance
            if free_mem_kb >= 100:  # >100KB free: use large chunks
                chunk_size = 2048
            elif free_mem_kb >= 50:  # 50-100KB free: use medium chunks
                chunk_size = 1024
            elif free_mem_kb >= 20:  # 20-50KB free: use small chunks
                chunk_size = 512
            else:  # <20KB free: use minimal chunks
                chunk_size = 256

        except Exception:
            # If detection fails (no gc module, error, etc), use safe default
            chunk_size = 256
            self._free_memory_kb = None

        self._optimal_chunk_size = chunk_size
        return chunk_size

    async def fs_writefile_async(
        self, dest: str, data: bytes, chunk_size: int = None, progress_callback=None
    ) -> None:
        """Write file to device asynchronously.

        Args:
            dest: Remote file path
            data: File contents to write
            chunk_size: Size of chunks to write. If None (default), automatically
                       detects optimal size based on device free memory (once per connection).
                       For files <3KB, uses fixed 256-byte chunks to avoid detection overhead.
                       Manual values: 256 (safe), 512, 1024, 2048 (fast, needs RAM)
            progress_callback: Optional callback for progress updates

        Note:
            Automatic chunk size detection queries device memory once and caches the result.
            For constrained devices (<20KB free), uses conservative 256-byte chunks.
            For devices with ample memory (>100KB free), uses 2048-byte chunks for best performance.
        """
        # For small files, use single exec_async to avoid overhead
        if len(data) < MIN_FILE_SIZE_FOR_AUTO_DETECTION:
            # Single-shot write for small files - fastest approach
            await self.exec_async(f"f=open({dest!r},'wb');f.write({data!r});f.close()")
            if progress_callback:
                progress_callback(len(data), len(data))
            return

        # For larger files, use chunked approach with optimal chunk size
        if chunk_size is None:
            chunk_size = await self.detect_optimal_chunk_size_async()

        # Open file and write data in chunks
        await self.exec_async(f"f=open({dest!r},'wb')\nw=f.write")

        # Write data in chunks
        # Note: Each exec_async goes through raw REPL, so minimizing calls is important
        for i in range(0, len(data), chunk_size):
            chunk = data[i : i + chunk_size]
            await self.exec_async(f"w({chunk!r})")
            if progress_callback:
                progress_callback(i + len(chunk), len(data))

        # Close file
        await self.exec_async("f.close()")

    async def fs_exists_async(self, src: str) -> bool:
        """Check if file or directory exists asynchronously.

        Args:
            src: Remote file or directory path

        Returns:
            bool: True if path exists, False otherwise
        """
        try:
            await self.fs_stat_async(src)
            return True
        except OSError:
            return False

    async def fs_isdir_async(self, src: str) -> bool:
        """Check if path is a directory asynchronously.

        Args:
            src: Remote path

        Returns:
            bool: True if path is a directory, False otherwise
        """
        try:
            stat = await self.fs_stat_async(src)
            return bool(stat[0] & 0x4000)  # Check directory bit
        except OSError:
            return False

    async def fs_mkdir_async(self, path: str) -> None:
        """Create directory asynchronously.

        Args:
            path: Remote directory path
        """
        await self.exec_async(f"import os\nos.mkdir({path!r})")

    async def fs_rmdir_async(self, path: str) -> None:
        """Remove directory asynchronously.

        Args:
            path: Remote directory path
        """
        await self.exec_async(f"import os\nos.rmdir({path!r})")

    async def fs_rmfile_async(self, path: str) -> None:
        """Remove file asynchronously.

        Args:
            path: Remote file path
        """
        await self.exec_async(f"import os\nos.remove({path!r})")

    async def fs_touchfile_async(self, path: str) -> None:
        """Touch file (create if doesn't exist) asynchronously.

        Args:
            path: Remote file path
        """
        await self.exec_async(f"f=open({path!r},'a')\nf.close()")

    async def fs_hashfile_async(self, path: str, algo: str, chunk_size: int = 256) -> bytes:
        """Compute file hash asynchronously.

        Args:
            path: Remote file path
            algo: Hash algorithm (e.g., 'sha256', 'md5')
            chunk_size: Size of chunks to read

        Returns:
            bytes: Hash digest
        """
        # Compute hash on device
        await self.exec_async(
            f"import hashlib\n"
            f"h=hashlib.{algo}()\n"
            f"with open({path!r},'rb') as f:\n"
            f" while 1:\n"
            f"  b=f.read({chunk_size})\n"
            f"  if not b:break\n"
            f"  h.update(b)"
        )
        result = await self.eval_async("h.digest()", parse=False)
        return result

    async def fs_printfile_async(self, src: str, chunk_size: int = 256) -> None:
        """Print file contents asynchronously.

        Args:
            src: Remote file path
            chunk_size: Size of chunks to read
        """
        await self.exec_async(
            f"with open({src!r}, 'rb') as f:\n"
            f" while 1:\n"
            f"  b=f.read({chunk_size})\n"
            f"  if not b:break\n"
            f"  print(b,end='')"
        )
