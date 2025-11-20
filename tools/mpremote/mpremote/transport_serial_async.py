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

"""Async serial transport for MicroPython remote control.

This module provides an asyncio-based implementation of the MicroPython
serial transport, enabling non-blocking concurrent operations.
"""

import asyncio
import struct
import sys
import time

try:
    import serial_asyncio
except ImportError:
    serial_asyncio = None

from .transport import TransportError, TransportExecError
from .transport_async import AsyncTransport
from .protocol import RawREPLProtocol


class AsyncSerialTransport(AsyncTransport):
    """Async serial transport using pyserial-asyncio.

    This class provides an async implementation of the serial transport,
    allowing non-blocking I/O operations with MicroPython devices over
    serial connections.
    """

    fs_hook_mount = "/remote"  # MUST match the mount point in fs_hook_code

    def __init__(
        self,
        device: str,
        baudrate: int = 115200,
        wait: float = 1,
        exclusive: bool = None,
        timeout: float = None,
    ):
        """Initialize async serial transport.

        Args:
            device: Serial device path (e.g., '/dev/ttyUSB0', 'COM3')
            baudrate: Communication speed (default: 115200)
            wait: Time to wait for device to appear (seconds)
            exclusive: Whether to open port exclusively
            timeout: Read timeout (None for blocking)
        """
        if serial_asyncio is None:
            raise ImportError(
                "pyserial-asyncio is required for async serial transport. "
                "Install with: pip install pyserial-asyncio"
            )

        self.device_name = device
        self.baudrate = baudrate
        self.wait = wait
        self.exclusive = exclusive
        self.timeout = timeout
        self.in_raw_repl = False
        self.use_raw_paste = True
        self.mounted = False

        # Async stream objects
        self.reader: asyncio.StreamReader = None
        self.writer: asyncio.StreamWriter = None
        self._transport = None

    async def connect(self):
        """Establish async serial connection."""
        import serial

        # Set options, and exclusive if pyserial supports it
        serial_kwargs = {
            "baudrate": self.baudrate,
            "timeout": self.timeout,
            "interCharTimeout": 1,
        }
        if serial.__version__ >= "3.3":
            # On Windows, exclusive must be True (pyserial-asyncio limitation)
            # On other platforms, use the provided value or default to True
            if sys.platform == "win32":
                exclusive = True
            else:
                exclusive = self.exclusive if self.exclusive is not None else True
            serial_kwargs["exclusive"] = exclusive

        delayed = False
        last_error = None
        for attempt in range(int(self.wait) + 1):
            try:
                # Create async serial connection
                self.reader, self.writer = await serial_asyncio.open_serial_connection(
                    url=self.device_name, **serial_kwargs
                )
                break
            except (OSError, serial.SerialException) as e:
                last_error = e
                if self.wait == 0:
                    raise TransportError(f"failed to access {self.device_name}: {e}")
                if attempt == 0:
                    sys.stdout.write(f"Waiting {int(self.wait)} seconds for device ")
                    delayed = True
                await asyncio.sleep(1)
                sys.stdout.write(".")
                sys.stdout.flush()
        else:
            if delayed:
                print("")
            raise TransportError(f"failed to access {self.device_name}: {last_error}")

        if delayed:
            print("")

    async def close_async(self):
        """Close async serial connection."""
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()

    def close(self):
        """Synchronous close wrapper."""
        if self.writer:
            try:
                asyncio.get_running_loop()
                # We're in an async context, use async close
                raise RuntimeError("Use close_async() in async context")
            except RuntimeError:
                # Not in async context, create new loop
                asyncio.run(self.close_async())

    async def read_async(self, size: int = 1) -> bytes:
        """Non-blocking read using asyncio streams.

        Args:
            size: Number of bytes to read

        Returns:
            bytes: Data read from serial port
        """
        if not self.reader:
            raise TransportError("Not connected")

        try:
            data = await self.reader.read(size)
            return data
        except Exception as e:
            raise TransportError(f"Read error: {e}")

    async def write_async(self, data: bytes) -> int:
        """Non-blocking write using asyncio streams.

        Args:
            data: Bytes to write

        Returns:
            int: Number of bytes written
        """
        if not self.writer:
            raise TransportError("Not connected")

        try:
            self.writer.write(data)
            await self.writer.drain()
            return len(data)
        except Exception as e:
            raise TransportError(f"Write error: {e}")

    async def read_until_async(
        self,
        min_num_bytes: int,
        ending: bytes,
        timeout: float = 10.0,
        data_consumer=None,
        timeout_overall: float = None,
    ) -> bytes:
        """Read until ending pattern found - async version.

        Args:
            min_num_bytes: Minimum bytes to read (obsolete parameter for compatibility)
            ending: Byte pattern to wait for
            timeout: Timeout between characters in seconds
            data_consumer: Optional callback to consume data as it arrives
            timeout_overall: Overall timeout in seconds

        Returns:
            bytes: All data read including ending pattern
        """
        assert data_consumer is None or len(ending) == 1

        data = b""
        begin_overall = time.monotonic()
        begin_char = time.monotonic()

        try:
            while True:
                if data.endswith(ending):
                    break

                # Check overall timeout
                if timeout_overall is not None:
                    if time.monotonic() >= begin_overall + timeout_overall:
                        break

                # Check character timeout
                if timeout is not None:
                    if time.monotonic() >= begin_char + timeout:
                        # Use asyncio timeout for the read
                        try:
                            async with asyncio.timeout(0.01):  # Small timeout to avoid blocking
                                chunk = await self.reader.read(1)
                                if chunk:
                                    if data_consumer:
                                        data_consumer(chunk)
                                        data = chunk
                                    else:
                                        data += chunk
                                    begin_char = time.monotonic()
                        except asyncio.TimeoutError:
                            break
                    else:
                        # Still within timeout, try to read
                        try:
                            async with asyncio.timeout(0.01):
                                chunk = await self.reader.read(1)
                                if chunk:
                                    if data_consumer:
                                        data_consumer(chunk)
                                        data = chunk
                                    else:
                                        data += chunk
                                    begin_char = time.monotonic()
                        except asyncio.TimeoutError:
                            await asyncio.sleep(0.01)  # Yield control
                else:
                    # No timeout, just read
                    chunk = await self.reader.read(1)
                    if chunk:
                        if data_consumer:
                            data_consumer(chunk)
                            data = chunk
                        else:
                            data += chunk
                        begin_char = time.monotonic()
                    else:
                        await asyncio.sleep(0.01)  # Yield control if no data
        except asyncio.CancelledError:
            raise TransportError("Read cancelled")

        return data

    async def enter_raw_repl_async(self, soft_reset: bool = True, timeout_overall: float = 10.0):
        """Enter raw REPL mode - async version.

        Args:
            soft_reset: Whether to perform soft reset
            timeout_overall: Maximum time for operation in seconds
        """
        await self.write_async(b"\r\x03")  # ctrl-C: interrupt any running program

        # Flush input buffer
        await asyncio.sleep(0.1)  # Give time for data to arrive
        try:
            # Try to read any pending data with short timeout
            async with asyncio.timeout(0.1):
                while True:
                    await self.reader.read(1024)
        except asyncio.TimeoutError:
            pass  # No more data, buffer is flushed

        await self.write_async(b"\r\x01")  # ctrl-A: enter raw REPL

        if soft_reset:
            data = await self.read_until_async(
                1, b"raw REPL; CTRL-B to exit\r\n>", timeout_overall=timeout_overall
            )
            if not data.endswith(b"raw REPL; CTRL-B to exit\r\n>"):
                print(data)
                raise TransportError("could not enter raw repl")

            await self.write_async(b"\x04")  # ctrl-D: soft reset

            data = await self.read_until_async(
                1, b"soft reboot\r\n", timeout_overall=timeout_overall
            )
            if not data.endswith(b"soft reboot\r\n"):
                print(data)
                raise TransportError("could not enter raw repl")

        data = await self.read_until_async(
            1, b"raw REPL; CTRL-B to exit\r\n", timeout_overall=timeout_overall
        )
        if not data.endswith(b"raw REPL; CTRL-B to exit\r\n"):
            print(data)
            raise TransportError("could not enter raw repl")

        self.in_raw_repl = True

    async def exit_raw_repl_async(self):
        """Exit raw REPL mode - async version."""
        await self.write_async(b"\r\x02")  # ctrl-B: enter friendly REPL
        self.in_raw_repl = False

    async def follow_async(self, timeout: float, data_consumer=None) -> tuple:
        """Follow command execution - async version.

        Args:
            timeout: Maximum time to wait for output
            data_consumer: Optional callback to consume output

        Returns:
            tuple: (stdout, stderr) as bytes
        """
        # Wait for normal output
        data = await self.read_until_async(
            1, b"\x04", timeout=timeout, data_consumer=data_consumer
        )
        if not data.endswith(b"\x04"):
            raise TransportError("timeout waiting for first EOF reception")
        data = data[:-1]

        # Wait for error output
        data_err = await self.read_until_async(1, b"\x04", timeout=timeout)
        if not data_err.endswith(b"\x04"):
            raise TransportError("timeout waiting for second EOF reception")
        data_err = data_err[:-1]

        return data, data_err

    async def raw_paste_write_async(self, command_bytes: bytes):
        """Write command using raw paste mode - async version.

        Args:
            command_bytes: Command to execute as bytes
        """
        # Read initial header with window size
        data = await self.read_async(2)
        window_size = struct.unpack("<H", data)[0]
        window_remain = window_size

        # Write out the command_bytes data
        i = 0
        while i < len(command_bytes):
            # Check for flow control or data from device
            while window_remain == 0:
                data = await self.read_async(1)
                if data == b"\x01":
                    # Device indicated that a new window of data can be sent
                    window_remain += window_size
                elif data == b"\x04":
                    # Device indicated abrupt end. Acknowledge it and finish
                    await self.write_async(b"\x04")
                    return
                else:
                    raise TransportError(f"unexpected read during raw paste: {data}")

            # Send out as much data as possible that fits within the allowed window
            b = command_bytes[i : min(i + window_remain, len(command_bytes))]
            await self.write_async(b)
            window_remain -= len(b)
            i += len(b)

        # Indicate end of data
        await self.write_async(b"\x04")

        # Wait for device to acknowledge end of data
        data = await self.read_until_async(1, b"\x04", timeout=10.0)
        if not data.endswith(b"\x04"):
            raise TransportError(f"could not complete raw paste: {data}")

    async def exec_raw_no_follow_async(self, command: str):
        """Execute without following - async version.

        Args:
            command: Python code to execute
        """
        if isinstance(command, bytes):
            command_bytes = command
        else:
            command_bytes = bytes(command, encoding="utf8")

        # Check we have a prompt
        data = await self.read_until_async(1, b">", timeout=10.0)
        if not data.endswith(b">"):
            raise TransportError("could not enter raw repl")

        if self.use_raw_paste:
            # Try to enter raw-paste mode
            await self.write_async(b"\x05A\x01")
            data = await self.read_async(2)
            if data == b"R\x00":
                # Device understood raw-paste command but doesn't support it
                pass
            elif data == b"R\x01":
                # Device supports raw-paste mode, write out the command using this mode
                return await self.raw_paste_write_async(command_bytes)
            else:
                # Device doesn't support raw-paste, fall back to normal raw REPL
                data = await self.read_until_async(1, b"w REPL; CTRL-B to exit\r\n>", timeout=10.0)
                if not data.endswith(b"w REPL; CTRL-B to exit\r\n>"):
                    print(data)
                    raise TransportError("could not enter raw repl")
            # Don't try to use raw-paste mode again for this connection
            self.use_raw_paste = False

        # Write command using standard raw REPL
        # In async mode, we don't need artificial delays for flow control
        for i in range(0, len(command_bytes), 256):
            await self.write_async(command_bytes[i : min(i + 256, len(command_bytes))])
        await self.write_async(b"\x04")

        # Check if we could exec command
        data = await self.read_async(2)
        if data != b"OK":
            raise TransportError(f"could not exec command (response: {data!r})")

    async def exec_raw_async(
        self, command: str, timeout: float = 10.0, data_consumer=None
    ) -> tuple:
        """Execute command and follow - async version.

        Args:
            command: Python code to execute
            timeout: Maximum time to wait
            data_consumer: Optional callback to consume output

        Returns:
            tuple: (stdout, stderr) as bytes
        """
        await self.exec_raw_no_follow_async(command)
        return await self.follow_async(timeout, data_consumer)

    async def eval_async(self, expression: str, parse: bool = True):
        """Evaluate expression - async version.

        Args:
            expression: Python expression to evaluate
            parse: Whether to parse result as Python literal

        Returns:
            Evaluated result
        """
        import ast

        if parse:
            ret = await self.exec_async(f"print(repr({expression}))")
            ret = ret.strip()
            return ast.literal_eval(ret.decode())
        else:
            ret = await self.exec_async(f"print({expression})")
            ret = ret.strip()
            return ret

    async def exec_async(self, command: str, data_consumer=None) -> bytes:
        """Execute command in normal REPL - async version.

        Args:
            command: Python code to execute
            data_consumer: Optional callback to consume output

        Returns:
            bytes: Command output
        """
        ret, ret_err = await self.exec_raw_async(command, data_consumer=data_consumer)
        if ret_err:
            raise TransportExecError(ret, ret_err.decode())
        return ret
