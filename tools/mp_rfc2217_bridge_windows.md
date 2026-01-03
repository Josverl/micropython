# RFC 2217 Bridge - Windows Support

This document describes how to add Windows support to the `mp_rfc2217_bridge.py` tool using `pywinpty`.

## Background

The current implementation uses Unix PTY (pseudo-terminal) functionality which is not available on Windows. To support Windows, we need to use the Windows ConPTY (Console Pseudo Terminal) API, which is available on Windows 10 version 1809 and later.

## Solution: pywinpty

[pywinpty](https://github.com/andfoy/pywinpty) provides Python bindings for the Windows ConPTY API and the older winpty library. It enables pseudo-terminal functionality on Windows, allowing proper terminal emulation for the MicroPython REPL.

### Why pywinpty?

1. **True terminal emulation** - Raw REPL mode works correctly
2. **ConPTY support** - Uses native Windows 10+ pseudo-console
3. **Well maintained** - Used by VS Code, Windows Terminal, and other major projects
4. **Similar API** - Can be adapted to work like Unix PTY

## Installation

```bash
pip install pywinpty
```

Or add to optional dependencies:

```bash
pip install micropython-rfc2217-bridge[windows]
```

## Implementation Plan

### 1. Platform Detection and Conditional Imports

```python
import sys

IS_WINDOWS = sys.platform == 'win32'

if not IS_WINDOWS:
    import pty
else:
    try:
        import winpty
        HAS_WINPTY = True
    except ImportError:
        HAS_WINPTY = False
        winpty = None
```

### 2. Abstract Terminal Wrapper

Create an abstract base class that defines the interface for terminal operations:

```python
from abc import ABC, abstractmethod
from typing import Optional, Tuple
import subprocess


class TerminalWrapper(ABC):
    """Abstract wrapper for platform-specific terminal functionality."""

    @abstractmethod
    def read(self, size: int, timeout: float) -> bytes:
        """Read up to size bytes with timeout.
        
        Args:
            size: Maximum number of bytes to read
            timeout: Timeout in seconds (0 = non-blocking)
            
        Returns:
            Bytes read, or empty bytes if timeout/no data
        """
        pass

    @abstractmethod
    def write(self, data: bytes) -> int:
        """Write data to the terminal.
        
        Args:
            data: Bytes to write
            
        Returns:
            Number of bytes written
        """
        pass

    @abstractmethod
    def poll(self) -> Optional[int]:
        """Check if the process has exited.
        
        Returns:
            Exit code if process has exited, None if still running
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """Close the terminal and terminate the process."""
        pass

    @property
    @abstractmethod
    def process(self) -> subprocess.Popen:
        """Get the underlying process object."""
        pass
```

### 3. Unix Terminal Implementation

Refactor current PTY code into a class:

```python
class UnixTerminal(TerminalWrapper):
    """Unix PTY-based terminal wrapper."""

    def __init__(self, cmd: list, cwd: Optional[str] = None, env: Optional[dict] = None):
        """Create a new Unix terminal with PTY.
        
        Args:
            cmd: Command and arguments to run
            cwd: Working directory for the process
            env: Environment variables (None = inherit)
        """
        import pty
        import os
        
        self.master_fd, slave_fd = pty.openpty()
        
        self._process = subprocess.Popen(
            cmd,
            stdin=slave_fd,
            stdout=slave_fd,
            stderr=slave_fd,
            cwd=cwd,
            env=env,
            start_new_session=True,
        )
        
        # Close slave in parent - only child uses it
        os.close(slave_fd)
        self._closed = False

    def read(self, size: int, timeout: float) -> bytes:
        import select
        import os
        
        if self._closed:
            return b""
        
        try:
            ready, _, _ = select.select([self.master_fd], [], [], timeout)
            if ready:
                return os.read(self.master_fd, size)
        except (OSError, ValueError):
            self._closed = True
        return b""

    def write(self, data: bytes) -> int:
        import os
        
        if self._closed:
            return 0
        
        try:
            return os.write(self.master_fd, data)
        except (OSError, ValueError):
            self._closed = True
            return 0

    def poll(self) -> Optional[int]:
        return self._process.poll()

    def close(self) -> None:
        import os
        
        if not self._closed:
            self._closed = True
            try:
                os.close(self.master_fd)
            except OSError:
                pass
            self._process.terminate()
            try:
                self._process.wait(timeout=1)
            except subprocess.TimeoutExpired:
                self._process.kill()

    @property
    def process(self) -> subprocess.Popen:
        return self._process
```

### 4. Windows Terminal Implementation

```python
class WindowsTerminal(TerminalWrapper):
    """Windows ConPTY-based terminal wrapper using pywinpty."""

    def __init__(self, cmd: list, cwd: Optional[str] = None, env: Optional[dict] = None):
        """Create a new Windows terminal with ConPTY.
        
        Args:
            cmd: Command and arguments to run
            cwd: Working directory for the process
            env: Environment variables (None = inherit)
        
        Raises:
            ImportError: If pywinpty is not installed
        """
        import winpty
        
        # Create PTY with default size
        self._pty = winpty.PTY(cols=80, rows=24)
        
        # Build command line
        executable = cmd[0]
        cmdline = ' '.join(cmd) if len(cmd) > 1 else None
        
        # Spawn the process
        self._process_handle = self._pty.spawn(
            executable,
            cmdline=cmdline,
            cwd=cwd,
            env=env,
        )
        
        self._closed = False
        self._read_buffer = b""

    def read(self, size: int, timeout: float) -> bytes:
        """Read from the PTY with timeout.
        
        Note: pywinpty's read is non-blocking, so we implement
        timeout using polling.
        """
        import time
        
        if self._closed:
            return b""
        
        # Return from buffer first
        if self._read_buffer:
            chunk = self._read_buffer[:size]
            self._read_buffer = self._read_buffer[size:]
            return chunk
        
        start_time = time.time()
        while True:
            try:
                data = self._pty.read(size, blocking=False)
                if data:
                    # pywinpty returns string, convert to bytes
                    if isinstance(data, str):
                        data = data.encode('utf-8', errors='replace')
                    return data
            except Exception:
                self._closed = True
                return b""
            
            # Check timeout
            elapsed = time.time() - start_time
            if elapsed >= timeout:
                return b""
            
            # Small sleep to avoid busy-waiting
            time.sleep(0.01)

    def write(self, data: bytes) -> int:
        if self._closed:
            return 0
        
        try:
            # pywinpty expects string for write
            if isinstance(data, bytes):
                data_str = data.decode('utf-8', errors='replace')
            else:
                data_str = data
            
            self._pty.write(data_str)
            return len(data)
        except Exception:
            self._closed = True
            return 0

    def poll(self) -> Optional[int]:
        """Check if process has exited.
        
        Returns exit code if exited, None if still running.
        """
        if self._pty.isalive():
            return None
        return self._pty.exitstatus if hasattr(self._pty, 'exitstatus') else 0

    def close(self) -> None:
        if not self._closed:
            self._closed = True
            try:
                # Send Ctrl-C then Ctrl-D to gracefully exit
                self._pty.write('\x03\x04')
            except Exception:
                pass
            # Note: pywinpty handles process cleanup

    @property
    def process(self):
        """Return a process-like object for compatibility."""
        # Return a wrapper that provides poll() method
        return self
```

### 5. Factory Function

```python
def create_terminal(cmd: list, cwd: Optional[str] = None, env: Optional[dict] = None) -> TerminalWrapper:
    """Create a platform-appropriate terminal wrapper.
    
    Args:
        cmd: Command and arguments to run
        cwd: Working directory for the process
        env: Environment variables (None = inherit)
        
    Returns:
        TerminalWrapper instance for the current platform
        
    Raises:
        RuntimeError: If Windows and pywinpty is not installed
    """
    if IS_WINDOWS:
        if not HAS_WINPTY:
            raise RuntimeError(
                "pywinpty is required for Windows support.\n"
                "Install it with: pip install pywinpty"
            )
        return WindowsTerminal(cmd, cwd, env)
    else:
        return UnixTerminal(cmd, cwd, env)
```

### 6. Update VirtualSerialPort

Modify `VirtualSerialPort` to use the `TerminalWrapper` instead of raw fd:

```python
class VirtualSerialPort:
    """A virtual serial port that wraps a terminal."""

    def __init__(
        self,
        terminal: TerminalWrapper,
        timeout: float = 0.1,
        restart_callback=None,
    ):
        self.terminal = terminal
        self.timeout = timeout
        # ... rest of initialization

    def read(self, size=1):
        """Read up to size bytes from the terminal."""
        if self._pending_reboot_output:
            chunk = self._pending_reboot_output[:size]
            self._pending_reboot_output = self._pending_reboot_output[size:]
            return chunk

        if self._closed:
            return b""

        data = self.terminal.read(size, self.timeout)
        # ... raw REPL detection logic
        return data

    def write(self, data):
        """Write data to the terminal."""
        if self._closed:
            return 0

        # ... raw REPL tracking logic
        return self.terminal.write(data)
```

### 7. Update Main Function

```python
def main():
    # ... argument parsing ...

    def create_micropython_process():
        """Create and return a new MicroPython terminal."""
        return create_terminal(cmd, cwd=cwd, env=env)

    def restart_micropython():
        """Restart MicroPython process for soft reboot."""
        logging.info(f"Restarting MicroPython for soft reboot: {' '.join(cmd)}")
        return create_micropython_process()

    # Start MicroPython process immediately (persistent mode)
    logging.info(f"Starting MicroPython: {' '.join(cmd)}")
    terminal = create_micropython_process()

    # Create persistent virtual serial port
    virtual_serial = VirtualSerialPort(
        terminal,
        timeout=0.1,
        restart_callback=restart_micropython,
    )
```

## Package Dependencies

Add to `pyproject.toml`:

```toml
[project]
dependencies = [
    "pyserial>=3.4",
]

[project.optional-dependencies]
windows = [
    "pywinpty>=2.0",
]

[project.scripts]
mp-rfc2217-bridge = "tools.mp_rfc2217_bridge:main"
```

## Testing on Windows

### Prerequisites

1. Windows 10 version 1809 or later (for ConPTY support)
2. Python 3.8 or later
3. MicroPython unix port compiled for Windows (or use the Windows port)

### Test Commands

```powershell
# Install dependencies
pip install pyserial pywinpty

# Run the bridge
python tools/mp_rfc2217_bridge.py --port 2217

# In another terminal, connect with mpremote
mpremote connect rfc2217://localhost:2217 repl
```

### Known Limitations

1. **Windows Terminal recommended** - ConPTY works best in Windows Terminal or VS Code's integrated terminal
2. **Legacy console** - The old Windows console (conhost.exe) may have issues with some escape sequences
3. **Line endings** - Windows uses CRLF; the bridge may need to handle line ending conversion

## Troubleshooting

### "pywinpty not found" error

```bash
pip install pywinpty
```

If installation fails, ensure you have the Visual C++ Build Tools installed.

### "ConPTY not available" error

ConPTY requires Windows 10 version 1809 or later. Check your Windows version:

```powershell
winver
```

### Raw REPL not working

Ensure MicroPython is built with REPL support and that the terminal size is adequate:

```python
# Increase terminal size if needed
self._pty = winpty.PTY(cols=120, rows=40)
```

## References

- [pywinpty documentation](https://github.com/andfoy/pywinpty)
- [Windows ConPTY API](https://docs.microsoft.com/en-us/windows/console/creating-a-pseudoconsole-session)
- [MicroPython RFC 2217 Bridge](./mp_rfc2217_bridge.md)
