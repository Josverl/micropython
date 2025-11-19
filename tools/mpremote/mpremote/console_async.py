#!/usr/bin/env python3
#
# This file is part of the MicroPython project, http://micropython.org/
#
# The MIT License (MIT)
#
# Copyright (c) 2023 Jim Mussared
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

"""Async console abstractions for mpremote.

This module provides async console I/O for both POSIX and Windows platforms,
enabling non-blocking keyboard input and output handling.
"""

import asyncio
import sys

try:
    import select
    import termios
except ImportError:
    termios = None
    select = None
    import msvcrt
    import signal


class AsyncConsolePosix:
    """Async POSIX console using asyncio streams."""
    
    def __init__(self):
        self.infd = sys.stdin.fileno()
        self.infile = sys.stdin.buffer
        self.outfile = sys.stdout.buffer
        if hasattr(self.infile, "raw"):
            self.infile = self.infile.raw
        if hasattr(self.outfile, "raw"):
            self.outfile = self.outfile.raw
        
        self.orig_attr = termios.tcgetattr(self.infd)
        self.reader = None
        self._loop = None
    
    def enter(self):
        """Enter raw terminal mode."""
        # attr is: [iflag, oflag, cflag, lflag, ispeed, ospeed, cc]
        attr = termios.tcgetattr(self.infd)
        attr[0] &= ~(
            termios.BRKINT | termios.ICRNL | termios.INPCK | termios.ISTRIP | termios.IXON
        )
        attr[1] = 0
        attr[2] = attr[2] & ~(termios.CSIZE | termios.PARENB) | termios.CS8
        attr[3] = 0
        attr[6][termios.VMIN] = 1
        attr[6][termios.VTIME] = 0
        termios.tcsetattr(self.infd, termios.TCSANOW, attr)
    
    def exit(self):
        """Restore original terminal mode."""
        termios.tcsetattr(self.infd, termios.TCSANOW, self.orig_attr)
    
    async def setup_async(self):
        """Setup async stdin reader."""
        if self.reader is None:
            self._loop = asyncio.get_event_loop()
            self.reader = asyncio.StreamReader(loop=self._loop)
            protocol = asyncio.StreamReaderProtocol(self.reader, loop=self._loop)
            await self._loop.connect_read_pipe(lambda: protocol, sys.stdin)
    
    async def readchar_async(self) -> bytes:
        """Async read single character from stdin.
        
        Returns:
            bytes: Single character read from keyboard
        """
        if self.reader is None:
            await self.setup_async()
        
        return await self.reader.read(1)
    
    def readchar(self):
        """Synchronous read character (for compatibility)."""
        res = select.select([self.infd], [], [], 0)
        if res[0]:
            return self.infile.read(1)
        else:
            return None
    
    def waitchar(self, transport_serial=None):
        """Wait for character (synchronous, for compatibility)."""
        if transport_serial:
            # TODO: transport_serial might not have fd
            select.select([self.infd, transport_serial.fd], [], [])
        else:
            select.select([self.infd], [], [])
    
    def write(self, buf: bytes):
        """Write to stdout.
        
        Args:
            buf: Bytes to write to console
        """
        self.outfile.write(buf)
        self.outfile.flush()


class AsyncConsoleWindows:
    """Async Windows console."""
    
    def __init__(self):
        self.ctrl_c = 0
        self._msvcrt = msvcrt
        self._signal = signal
    
    def _sigint_handler(self, signo, frame):
        """Handle Ctrl-C signal."""
        self.ctrl_c += 1
    
    def enter(self):
        """Setup signal handler."""
        self._signal.signal(self._signal.SIGINT, self._sigint_handler)
    
    def exit(self):
        """Restore signal handler."""
        self._signal.signal(self._signal.SIGINT, self._signal.SIG_DFL)
    
    def inWaiting(self):
        """Check if input is waiting (synchronous)."""
        return 1 if self.ctrl_c or self._msvcrt.kbhit() else 0
    
    async def readchar_async(self) -> bytes:
        """Async read character on Windows.
        
        Returns:
            bytes: Single character read from keyboard
        """
        while True:
            if self.ctrl_c:
                self.ctrl_c -= 1
                return b"\x03"
            
            if self._msvcrt.kbhit():
                ch = self._msvcrt.getch()
                # Handle arrow keys and function keys
                while ch in b"\x00\xe0":  # arrow or function key prefix?
                    if not self._msvcrt.kbhit():
                        await asyncio.sleep(0.01)
                        continue
                    ch = self._msvcrt.getch()  # second call returns the actual key code
                    # Map Windows key codes to ANSI escape sequences
                    KEY_MAP = {
                        b"H": b"A",  # UP
                        b"P": b"B",  # DOWN
                        b"M": b"C",  # RIGHT
                        b"K": b"D",  # LEFT
                        b"G": b"H",  # POS1
                        b"O": b"F",  # END
                        b"Q": b"6~",  # PGDN
                        b"I": b"5~",  # PGUP
                        b"S": b"3~",  # DEL
                        b"R": b"2~",  # INS
                    }
                    try:
                        ch = b"\x1b[" + KEY_MAP[ch]
                    except KeyError:
                        return None
                return ch
            
            # No key available, yield control
            await asyncio.sleep(0.01)
    
    def readchar(self):
        """Synchronous read character (for compatibility)."""
        if self.ctrl_c:
            self.ctrl_c -= 1
            return b"\x03"
        if self._msvcrt.kbhit():
            return self._msvcrt.getch()
        return None
    
    def waitchar(self, transport_serial):
        """Wait for character (synchronous, for compatibility)."""
        import time
        while not (self.inWaiting() or transport_serial.inWaiting()):
            time.sleep(0.01)
    
    def write(self, buf: bytes):
        """Write to stdout.
        
        Args:
            buf: Bytes to write to console
        """
        buf = buf.decode() if isinstance(buf, bytes) else buf
        sys.stdout.write(buf)
        sys.stdout.flush()


# Factory function
def AsyncConsole():
    """Create appropriate async console for platform.
    
    Returns:
        AsyncConsolePosix or AsyncConsoleWindows instance
    """
    if termios:
        return AsyncConsolePosix()
    else:
        return AsyncConsoleWindows()
