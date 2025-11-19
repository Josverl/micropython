# Plan: Integrate asyncio into mpremote transport layer

Transform mpremote's blocking I/O architecture to async/await patterns while maintaining extensibility for multiple transport protocols (serial, WebSocket, Bluetooth, network sockets). This enables non-blocking concurrent operations, removes polling delays, and establishes a clean protocol abstraction layer.

## Migration Strategy

### Phase 1: Parallel Implementation
- Create async transport layer alongside existing sync code
- Implement `AsyncSerialTransport` with feature parity to `SerialTransport`
- Add async versions of core methods with `_async` suffix
- No breaking changes - both APIs coexist

### Phase 2: Command Layer Migration
- Convert command handlers to async
- Add sync wrappers using `asyncio.run()`
- Update `State` class with async methods
- Maintain backward compatibility via wrappers

### Phase 3: REPL and Console
- Implement async REPL loop with concurrent I/O
- Create async console abstractions
- Test on multiple platforms (Linux, macOS, Windows)
- Fallback to sync version if issues

### Phase 4: Testing and Documentation
- Port all tests in `tools/mpremote/tests/` to async versions
- Create new test suite for async transports
- Write migration guide for contributors
- Document new transport API for extensions
- Performance benchmarking

### Phase 5: Deprecation and Cleanup (Future)
- Mark sync API as deprecated in v2.0
- Remove sync code in v3.0
- Full async-only architecture

## Current Architecture Analysis

### Blocking I/O Patterns
The codebase is purely synchronous with pervasive blocking operations:

- **`read_until()` method** (transport_serial.py:124-159): Polls `serial.inWaiting()` every 10ms, blocks on `serial.read(1)`
- **`exec_raw_no_follow()` method** (transport_serial.py:254-291): Hardcoded 10ms delays between writes for rate limiting
- **`follow()` method** (transport_serial.py:202-216): Sequential blocking reads for stdout/stderr
- **`exec_raw` with raw paste** (transport_serial.py:219-249): Flow control uses blocking reads in a loop
- **REPL loop** (repl.py:7-53): Blocks on `console_in.waitchar()` using `select.select()` or polling
- **Console abstraction** (console.py): POSIX uses `select.select()`, Windows uses 10ms polling loops

### Current Transport Hierarchy

```python
# transport.py
class Transport:
    # Abstract base class (duck typing)
    # Implements filesystem operations via REPL commands
    def fs_listdir(src="")
    def fs_stat(src)
    def fs_readfile(src, chunk_size=256, progress_callback=None)
    def fs_writefile(dest, data, chunk_size=256, progress_callback=None)
    # ... more fs_* methods

# transport_serial.py
class SerialTransport(Transport):
    # ~1100 lines, serial-only implementation
    def __init__(device, baudrate=115200, wait=0, exclusive=True, timeout=None)
    def read_until(min_num_bytes, ending, timeout=10, data_consumer=None)
    def enter_raw_repl(soft_reset=True, timeout_overall=10)
    def exit_raw_repl()
    def exec_raw_no_follow(command)
    def exec_raw(command, timeout=10, data_consumer=None)
    def follow(timeout, data_consumer=None)
    def exec(command, data_consumer=None)
    def eval(expression, parse=True)
```

### Command Flow

```
User CLI → main.py → State object → ensure_raw_repl() → 
commands.py handlers → SerialTransport methods → 
blocking serial I/O → device
```

### Key Challenges

1. **Deep coupling**: REPL directly accesses `state.transport.serial` attribute
2. **No protocol abstraction**: Raw REPL protocol mixed with serial I/O
3. **Synchronous assumptions**: Every method assumes blocking I/O
4. **Global state**: Single `State` object manages connection
5. **Hardcoded delays**: 10ms sleeps throughout codebase
6. **Tight integration**: `TransportSerialIntercept` wraps serial for filesystem commands

## Implementation Steps

### 1. Create async transport abstraction layer

**Objective**: Define protocol-agnostic async transport interface

**New file**: `mpremote/transport_async.py`

```python
class AsyncTransport:
    """Abstract base class for async transport implementations"""
    
    async def read(self, size: int = 1) -> bytes:
        """Read up to size bytes from transport"""
        raise NotImplementedError
    
    async def write(self, data: bytes) -> int:
        """Write data to transport, return bytes written"""
        raise NotImplementedError
    
    async def read_until(self, ending: bytes, timeout: float = 10.0) -> bytes:
        """Read until ending pattern found"""
        raise NotImplementedError
    
    async def enter_raw_repl(self, soft_reset: bool = True) -> None:
        """Enter raw REPL mode"""
        raise NotImplementedError
    
    async def exit_raw_repl(self) -> None:
        """Exit raw REPL mode"""
        raise NotImplementedError
    
    async def exec_raw(self, command: str, timeout: float = 10.0, 
                       data_consumer=None) -> tuple[bytes, bytes]:
        """Execute command in raw REPL, return (stdout, stderr)"""
        raise NotImplementedError
    
    async def exec(self, command: str, data_consumer=None) -> bytes:
        """Execute command in normal REPL"""
        raise NotImplementedError
    
    async def eval(self, expression: str, parse: bool = True):
        """Evaluate expression and return result"""
        raise NotImplementedError
    
    async def close(self) -> None:
        """Close transport connection"""
        raise NotImplementedError
    
    # Filesystem operations (inherited from base Transport)
    async def fs_listdir(self, src: str = "") -> list:
        """List directory contents"""
        result = await self.eval(f"import os; os.listdir({src!r})")
        return result
    
    async def fs_stat(self, src: str) -> tuple:
        """Get file/directory stats"""
        result = await self.eval(f"import os; os.stat({src!r})")
        return result
    
    async def fs_readfile(self, src: str, chunk_size: int = 256, 
                          progress_callback=None) -> bytes:
        """Read file from device"""
        # Implementation using exec_raw with chunked reads
        pass
    
    async def fs_writefile(self, dest: str, data: bytes, 
                           chunk_size: int = 256, progress_callback=None) -> None:
        """Write file to device"""
        # Implementation using exec_raw with chunked writes
        pass
```

**Extract protocol logic**: Create `mpremote/protocol.py` for raw REPL protocol handling:

```python
class RawREPLProtocol:
    """Handles MicroPython raw REPL protocol"""
    
    RAW_REPL_ENTER = b'\r\x03\x03'  # Ctrl-C twice
    RAW_REPL_EXIT = b'\r\x02'       # Ctrl-B
    RAW_PASTE_START = b'\x05A\x01'  # Ctrl-E A \x01
    
    @staticmethod
    async def encode_command(command: str, use_raw_paste: bool = True) -> bytes:
        """Encode command for transmission"""
        pass
    
    @staticmethod
    async def decode_response(data: bytes) -> tuple[bytes, bytes]:
        """Decode response into (stdout, stderr)"""
        pass
```

### 2. Implement `AsyncSerialTransport` with asyncio-serial

**Objective**: Port SerialTransport to async using pyserial-asyncio

**Update file**: `mpremote/transport_serial.py` (or create `transport_serial_async.py`)

```python
import asyncio
import serial_asyncio

class AsyncSerialTransport(AsyncTransport):
    """Async serial transport using pyserial-asyncio"""
    
    def __init__(self, device: str, baudrate: int = 115200, 
                 wait: float = 0, exclusive: bool = True, timeout: float = None):
        self.device_name = device
        self.baudrate = baudrate
        self.in_raw_repl = False
        self.use_raw_paste = True
        self.reader: asyncio.StreamReader = None
        self.writer: asyncio.StreamWriter = None
    
    async def connect(self):
        """Establish async serial connection"""
        self.reader, self.writer = await serial_asyncio.open_serial_connection(
            url=self.device_name,
            baudrate=self.baudrate,
            timeout=self.timeout
        )
    
    async def read(self, size: int = 1) -> bytes:
        """Non-blocking read using asyncio streams"""
        return await self.reader.read(size)
    
    async def write(self, data: bytes) -> int:
        """Non-blocking write using asyncio streams"""
        self.writer.write(data)
        await self.writer.drain()
        return len(data)
    
    async def read_until(self, ending: bytes, timeout: float = 10.0, 
                         min_num_bytes: int = 1, data_consumer=None) -> bytes:
        """Read until ending pattern - async version"""
        data = b''
        try:
            async with asyncio.timeout(timeout):
                while not data.endswith(ending) or len(data) < min_num_bytes:
                    chunk = await self.reader.read(1)
                    if chunk:
                        data += chunk
                        if data_consumer:
                            data_consumer(chunk)
                    else:
                        # No data available, yield control
                        await asyncio.sleep(0)
        except asyncio.TimeoutError:
            pass
        return data
    
    async def enter_raw_repl(self, soft_reset: bool = True, 
                            timeout_overall: float = 10.0) -> None:
        """Enter raw REPL mode - async version"""
        # Convert blocking logic to async
        await self.write(b'\r\x03\x03')  # Ctrl-C twice
        await asyncio.sleep(0.1)
        
        # Flush input
        self.reader.feed_data(b'')  # Clear buffer
        
        await self.write(b'\r\x01')  # Ctrl-A: raw REPL
        data = await self.read_until(b'raw REPL; CTRL-B to exit\r\n>', timeout=timeout_overall)
        
        if soft_reset:
            await self.write(b'\x04')  # Ctrl-D: soft reset
            data = await self.read_until(b'soft reboot\r\n', timeout=timeout_overall)
            # Wait for startup
            await self.read_until(b'raw REPL; CTRL-B to exit\r\n')
        
        self.in_raw_repl = True
    
    async def exec_raw_no_follow(self, command: str) -> None:
        """Execute without following - async version"""
        command_bytes = command.encode('utf-8')
        
        if self.use_raw_paste:
            # Raw paste mode
            await self.write(b'\x05A\x01')  # Ctrl-E A \x01
            await self.write(len(command_bytes).to_bytes(4, 'little'))
            await self.write(command_bytes)
            await self.write(b'\x04')  # Ctrl-D
            
            # Wait for acknowledgment with flow control
            window_size = 32
            window_remain = window_size
            i = 0
            while i < len(command_bytes):
                while window_remain == 0 or self.reader.at_eof():
                    data = await self.read(1)
                    if data == b'\x01':
                        window_remain += window_size
                    elif data == b'\x04':
                        break
                
                # Send next chunk
                chunk_size = min(window_remain, len(command_bytes) - i)
                await self.write(command_bytes[i:i + chunk_size])
                window_remain -= chunk_size
                i += chunk_size
        else:
            # Standard raw REPL - send in chunks without delays
            for i in range(0, len(command_bytes), 256):
                chunk = command_bytes[i:min(i + 256, len(command_bytes))]
                await self.write(chunk)
                # Remove hardcoded sleep - async handles flow control
            
            await self.write(b'\x04')  # Ctrl-D to execute
            await self.read_until(b'OK')
    
    async def follow(self, timeout: float, data_consumer=None) -> tuple[bytes, bytes]:
        """Follow command execution - async version"""
        # Read stdout and stderr concurrently
        async def read_stream():
            return await self.read_until(b'\x04', timeout=timeout, 
                                        min_num_bytes=1, data_consumer=data_consumer)
        
        async def read_errors():
            return await self.read_until(b'\x04', timeout=timeout, min_num_bytes=1)
        
        # Run both reads concurrently instead of sequentially
        data, data_err = await asyncio.gather(read_stream(), read_errors())
        return data[:-1], data_err[:-1]
    
    async def exec_raw(self, command: str, timeout: float = 10.0, 
                       data_consumer=None) -> tuple[bytes, bytes]:
        """Execute command and follow - async version"""
        await self.exec_raw_no_follow(command)
        return await self.follow(timeout, data_consumer)
    
    async def close(self) -> None:
        """Close serial connection"""
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
```

**Dependencies to add** (pyproject.toml):
```toml
dependencies = [
    "pyserial >= 3.3",
    "pyserial-asyncio >= 0.6",  # NEW
    "importlib_metadata >= 1.4; python_version < '3.8'",
    "platformdirs >= 4.3.7",
]
```

### 3. Refactor REPL loop for async I/O multiplexing

**Objective**: Rewrite REPL to concurrently handle keyboard and device I/O

**Update file**: `mpremote/repl.py`

```python
import asyncio
from .console import AsyncConsole

async def do_repl_main_loop_async(state, console, capture_file=None):
    """Async REPL loop with concurrent keyboard and device I/O"""
    
    console_out_write = console.write
    if capture_file:
        console_out_write_orig = console_out_write
        def console_out_write(data):
            console_out_write_orig(data)
            capture_file.write(data)
    
    async def handle_keyboard_input():
        """Coroutine: read keyboard input and send to device"""
        while True:
            try:
                c = await console.readchar_async()
                
                if c == b"\x1d":  # GS/CTRL+]
                    return "exit"
                elif c == b"\x04":  # Ctrl-D
                    await state.transport.write_ctrl_d_async(console_out_write)
                elif c == b"\x0a" and console.exit_character == b"\x0a":
                    console_out_write(b"\r\n")
                    return "exit"
                else:
                    await state.transport.write(c)
            except Exception as e:
                print(f"Keyboard error: {e}")
                return "error"
    
    async def handle_device_output():
        """Coroutine: read device output and write to console"""
        while True:
            try:
                # Non-blocking read
                data = await state.transport.read(256)
                if data:
                    console_out_write(data)
                else:
                    await asyncio.sleep(0.01)  # Yield control
            except Exception as e:
                print(f"Device error: {e}")
                return "error"
    
    # Run both coroutines concurrently
    try:
        tasks = [
            asyncio.create_task(handle_keyboard_input(), name="keyboard"),
            asyncio.create_task(handle_device_output(), name="device")
        ]
        
        done, pending = await asyncio.wait(
            tasks, 
            return_when=asyncio.FIRST_COMPLETED
        )
        
        # Cancel remaining tasks
        for task in pending:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
    
    except KeyboardInterrupt:
        console.exit()
    
    console.exit()

# Keep synchronous wrapper for backward compatibility
def do_repl_main_loop(state, console_in, console_out_write, *args, **kwargs):
    """Synchronous wrapper for async REPL"""
    console = AsyncConsole(console_in, console_out_write)
    asyncio.run(do_repl_main_loop_async(state, console, *args, **kwargs))
```

**Update file**: `mpremote/console.py`

```python
import asyncio
import sys
import select

class AsyncConsolePosix:
    """Async POSIX console using asyncio streams"""
    
    def __init__(self):
        self.infd = sys.stdin.fileno()
        self.reader = None
    
    async def setup(self):
        """Setup async stdin reader"""
        loop = asyncio.get_event_loop()
        self.reader = asyncio.StreamReader(loop=loop)
        protocol = asyncio.StreamReaderProtocol(self.reader)
        await loop.connect_read_pipe(lambda: protocol, sys.stdin)
    
    async def readchar_async(self) -> bytes:
        """Async read single character from stdin"""
        if not self.reader:
            await self.setup()
        return await self.reader.read(1)
    
    def write(self, data: bytes):
        """Write to stdout (still synchronous)"""
        sys.stdout.buffer.write(data)
        sys.stdout.flush()

class AsyncConsoleWindows:
    """Async Windows console"""
    
    def __init__(self):
        import msvcrt
        self.msvcrt = msvcrt
    
    async def readchar_async(self) -> bytes:
        """Async read character on Windows"""
        while True:
            if self.msvcrt.kbhit():
                return self.msvcrt.getch()
            await asyncio.sleep(0.01)
    
    def write(self, data: bytes):
        """Write to stdout"""
        sys.stdout.buffer.write(data)
        sys.stdout.flush()

# Factory function
def AsyncConsole(*args, **kwargs):
    if sys.platform == "win32":
        return AsyncConsoleWindows(*args, **kwargs)
    else:
        return AsyncConsolePosix(*args, **kwargs)
```

### 4. Convert command handlers to async/await

**Objective**: Make all command handlers async and propagate through main

**Update file**: `mpremote/commands.py`

Convert handlers to async:

```python
async def do_filesystem_async(state, args):
    """Async filesystem operations"""
    await state.ensure_raw_repl()
    state.did_action()
    
    if args.command == "cp":
        if args.src.startswith(":"):
            # Copy from device to host
            src = args.src[1:]
            dest = args.dest
            data = await state.transport.fs_readfile(
                src, 
                progress_callback=show_progress_bar
            )
            with open(dest, "wb") as f:
                f.write(data)
        else:
            # Copy from host to device
            src = args.src
            dest = args.dest[1:] if args.dest.startswith(":") else args.dest
            with open(src, "rb") as f:
                data = f.read()
            await state.transport.fs_writefile(
                dest, 
                data, 
                progress_callback=show_progress_bar
            )
    # ... more operations

async def do_exec_async(state, args):
    """Async exec command"""
    await state.ensure_raw_repl()
    state.did_action()
    
    # Read command
    if args.command == "-":
        buf = sys.stdin.buffer.read()
    else:
        with open(args.command, "rb") as f:
            buf = f.read()
    
    # Execute
    await state.transport.exec_raw_no_follow(buf)
    
    if args.follow:
        ret, ret_err = await state.transport.follow(
            timeout=None, 
            data_consumer=stdout_write_bytes
        )
        if ret_err:
            stdout_write_bytes(ret_err)
            sys.exit(1)

async def do_eval_async(state, args):
    """Async eval command"""
    await state.ensure_raw_repl()
    state.did_action()
    
    result = await state.transport.eval(args.expression)
    print(result)

# Sync wrappers for backward compatibility
def do_filesystem(state, args):
    asyncio.run(do_filesystem_async(state, args))

def do_exec(state, args):
    asyncio.run(do_exec_async(state, args))

def do_eval(state, args):
    asyncio.run(do_eval_async(state, args))
```

**Update State class**:

```python
class State:
    def __init__(self):
        self.transport: AsyncTransport = None
        self._did_action = False
        self._auto_soft_reset = True
        self._loop = None
    
    async def ensure_connected_async(self):
        """Async connection establishment"""
        if self.transport is None:
            # Auto-connect logic
            pass
    
    async def ensure_raw_repl_async(self, soft_reset=None):
        """Async raw REPL entry"""
        await self.ensure_connected_async()
        if not self.transport.in_raw_repl:
            await self.transport.enter_raw_repl(
                soft_reset=soft_reset if soft_reset is not None else self._auto_soft_reset
            )
    
    # Sync wrappers
    def ensure_connected(self):
        asyncio.run(self.ensure_connected_async())
    
    def ensure_raw_repl(self, soft_reset=None):
        asyncio.run(self.ensure_raw_repl_async(soft_reset))
```

**Update main entry point** (`mpremote/main.py`):

```python
def main():
    """Main entry point - coordinates async execution"""
    config = load_user_config()
    prepare_command_expansions(config)
    state = State()
    
    # Parse commands
    while remaining_args:
        cmd = remaining_args.pop(0)
        handler_func, parser_func = _COMMANDS[cmd]
        args = parser_func(remaining_args)
        
        # Execute handler (may be async or sync)
        if asyncio.iscoroutinefunction(handler_func):
            asyncio.run(handler_func(state, args))
        else:
            handler_func(state, args)
    
    # Cleanup
    if state.transport:
        if asyncio.iscoroutinefunction(state.transport.close):
            asyncio.run(state.transport.close())
        else:
            state.transport.close()
```

### 5. Implement example alternative async transport

**Objective**: Demonstrate extensibility with WebSocket transport

**New file**: `mpremote/transport_websocket.py`

```python
import asyncio
import websockets
import json

class AsyncWebSocketTransport(AsyncTransport):
    """WebSocket transport for MicroPython over network"""
    
    def __init__(self, url: str, timeout: float = 10.0):
        self.url = url
        self.timeout = timeout
        self.ws = None
        self.in_raw_repl = False
    
    async def connect(self):
        """Connect to WebSocket REPL"""
        self.ws = await websockets.connect(
            self.url,
            ping_interval=None,
            close_timeout=self.timeout
        )
    
    async def read(self, size: int = 1) -> bytes:
        """Read from WebSocket"""
        if self.ws is None:
            await self.connect()
        
        try:
            data = await asyncio.wait_for(
                self.ws.recv(), 
                timeout=self.timeout
            )
            if isinstance(data, str):
                return data.encode('utf-8')
            return data
        except asyncio.TimeoutError:
            return b''
    
    async def write(self, data: bytes) -> int:
        """Write to WebSocket"""
        if self.ws is None:
            await self.connect()
        
        await self.ws.send(data)
        return len(data)
    
    async def read_until(self, ending: bytes, timeout: float = 10.0,
                         min_num_bytes: int = 1, data_consumer=None) -> bytes:
        """Read until pattern"""
        accumulated = b''
        try:
            async with asyncio.timeout(timeout):
                while not accumulated.endswith(ending) or len(accumulated) < min_num_bytes:
                    chunk = await self.read(1024)
                    accumulated += chunk
                    if data_consumer:
                        data_consumer(chunk)
        except asyncio.TimeoutError:
            pass
        return accumulated
    
    async def enter_raw_repl(self, soft_reset: bool = True, 
                            timeout_overall: float = 10.0) -> None:
        """Enter raw REPL over WebSocket"""
        # Send JSON command to enter raw REPL
        await self.write(json.dumps({
            "command": "enter_raw_repl",
            "soft_reset": soft_reset
        }).encode('utf-8'))
        
        response = await self.read_until(b'\n', timeout=timeout_overall)
        # Parse response
        self.in_raw_repl = True
    
    async def exec_raw(self, command: str, timeout: float = 10.0,
                       data_consumer=None) -> tuple[bytes, bytes]:
        """Execute command over WebSocket"""
        # Send command as JSON
        await self.write(json.dumps({
            "command": "exec",
            "code": command
        }).encode('utf-8'))
        
        # Wait for response
        response = await self.read_until(b'\n\n', timeout=timeout)
        
        # Parse JSON response with stdout/stderr
        result = json.loads(response)
        stdout = result.get("stdout", b"")
        stderr = result.get("stderr", b"")
        
        if isinstance(stdout, str):
            stdout = stdout.encode('utf-8')
        if isinstance(stderr, str):
            stderr = stderr.encode('utf-8')
        
        return stdout, stderr
    
    async def close(self) -> None:
        """Close WebSocket connection"""
        if self.ws:
            await self.ws.close()
```

**Usage example**:

```python
# Connect via serial (existing)
transport = AsyncSerialTransport("/dev/ttyUSB0", baudrate=115200)
await transport.connect()

# OR connect via WebSocket (new)
transport = AsyncWebSocketTransport("ws://192.168.1.100:8266/repl")
await transport.connect()

# Same interface for both
await transport.enter_raw_repl()
stdout, stderr = await transport.exec_raw("print('Hello')")
await transport.close()
```



## Testing Strategy

### Unit Tests
```python
# tests/test_async_transport.py
import pytest
import asyncio

@pytest.mark.asyncio
async def test_async_serial_connect():
    transport = AsyncSerialTransport("/dev/ttyUSB0")
    await transport.connect()
    assert transport.reader is not None
    await transport.close()

@pytest.mark.asyncio
async def test_async_exec_raw():
    transport = AsyncSerialTransport("/dev/ttyUSB0")
    await transport.connect()
    await transport.enter_raw_repl()
    
    stdout, stderr = await transport.exec_raw("print('test')")
    assert b'test' in stdout
    assert stderr == b''
    
    await transport.close()

@pytest.mark.asyncio
async def test_concurrent_operations():
    transport = AsyncSerialTransport("/dev/ttyUSB0")
    await transport.connect()
    await transport.enter_raw_repl()
    
    # Run multiple commands concurrently
    results = await asyncio.gather(
        transport.exec_raw("print(1)"),
        transport.exec_raw("print(2)"),
        transport.exec_raw("print(3)")
    )
    
    assert len(results) == 3
    await transport.close()
```

### Integration Tests
- Port existing shell scripts in `tests/` to async
- Test serial, WebSocket, and mock transports
- Verify REPL functionality across platforms
- Performance tests: measure latency reduction, throughput improvement

### Compatibility Tests
- Ensure sync wrappers maintain exact behavior
- Test with existing user scripts
- Verify no breaking changes in CLI interface

## Performance Benefits

### Expected Improvements

1. **Removed polling delays**: Eliminate ~100+ `time.sleep(0.01)` calls per operation
2. **Concurrent I/O**: REPL can read keyboard and device simultaneously
3. **Better throughput**: No artificial rate limiting in `exec_raw_no_follow()`
4. **Scalability**: Support multiple device connections in single process
5. **Lower latency**: Immediate response to I/O events vs. polling

### Benchmarks to Track

- Time to execute 100 small commands: expect 30-50% reduction
- File transfer throughput: expect 2-3x improvement
- REPL responsiveness: measure input-to-echo latency
- Memory usage: async might use slightly more for tasks/coroutines

## Dependencies

### New Required Packages

```toml
[project]
dependencies = [
    "pyserial >= 3.3",
    "pyserial-asyncio >= 0.6",  # For AsyncSerialTransport
    "importlib_metadata >= 1.4; python_version < '3.8'",
    "platformdirs >= 4.3.7",
]

[project.optional-dependencies]
websocket = [
    "websockets >= 12.0",  # For WebSocket transport example
]
dev = [
    "pytest >= 7.0",
    "pytest-asyncio >= 0.21",  # For async test support
]
```

### Python Version Requirements

- Minimum: Python 3.8 (for `asyncio.run()` and walrus operator)
- Recommended: Python 3.11+ (for `asyncio.timeout()` and performance improvements)
- Consider: Python 3.12+ for best async performance

## Backward Compatibility Approach

Initial implementaion will use Option A: to reduce the risk of breaking changes while transitioning to async.

### Option A: Dual API (Recommended for v1.x → v2.0)

Keep both sync and async APIs:

```python
# Sync API (existing, maintained)
class SerialTransport(Transport):
    def exec_raw(self, command): ...

# Async API (new)
class AsyncSerialTransport(AsyncTransport):
    async def exec_raw(self, command): ...

# Sync wrappers over async
class SerialTransportV2(Transport):
    def __init__(self, *args, **kwargs):
        self._async_transport = AsyncSerialTransport(*args, **kwargs)
    
    def exec_raw(self, command):
        return asyncio.run(self._async_transport.exec_raw(command))
```

**Pros**: No breaking changes, gradual migration
**Cons**: Code duplication, maintenance burden

### Option B: Async-First with Sync Wrappers (v2.0)

Default to async, provide sync compatibility:

```python
# mpremote/commands.py
async def do_filesystem_async(state, args):
    # Async implementation
    pass

def do_filesystem(state, args):
    # Sync wrapper for CLI
    asyncio.run(do_filesystem_async(state, args))

# CLI remains synchronous-looking to users
# Internally everything is async
```

**Pros**: Clean async architecture, easier to maintain
**Cons**: Requires careful testing, potential subtle behavioral changes

### Option C: Hard Async Migration (v3.0)

Remove all sync code:

```python
# Everything is async, no wrappers
async def main():
    async with AsyncSerialTransport("/dev/ttyUSB0") as transport:
        await transport.exec_raw("print('hello')")

if __name__ == "__main__":
    asyncio.run(main())
```

**Pros**: Cleanest code, best performance
**Cons**: Breaking change, requires user script updates

**Recommendation**: Phases 1-2 use Option A, Phases 3-4 migrate to Option B, Phase 5 (v3.0) use Option C

## Documentation Requirements

### User-Facing Documentation

1. **Migration Guide**: How to update scripts using mpremote as a library
2. **Performance Guide**: When async provides benefits vs. sync
3. **Transport Guide**: How to implement custom async transports
4. **API Reference**: Document all async methods

### Developer Documentation

1. **Architecture Document**: Explain async design decisions
2. **Contributing Guide**: How to add async features
3. **Testing Guide**: How to write async tests
4. **Protocol Specification**: Document raw REPL protocol abstraction

### Code Examples

```python
# Simple async usage
import asyncio
from mpremote.transport_serial import AsyncSerialTransport

async def main():
    transport = AsyncSerialTransport("/dev/ttyUSB0")
    await transport.connect()
    await transport.enter_raw_repl()
    
    result = await transport.eval("2 + 2")
    print(result)  # 4
    
    await transport.close()

asyncio.run(main())

# Concurrent operations
async def run_multiple_commands():
    transport = AsyncSerialTransport("/dev/ttyUSB0")
    await transport.connect()
    await transport.enter_raw_repl()
    
    # Run commands concurrently
    results = await asyncio.gather(
        transport.exec_raw("import time; time.sleep(1); print('A')"),
        transport.exec_raw("import time; time.sleep(1); print('B')"),
        transport.exec_raw("import time; time.sleep(1); print('C')")
    )
    
    # All three complete in ~1 second instead of 3 seconds
    await transport.close()

# Custom transport
class AsyncBluetoothTransport(AsyncTransport):
    async def connect(self):
        # BLE connection logic
        pass
    
    async def read(self, size):
        # BLE read
        pass
    
    async def write(self, data):
        # BLE write
        pass
```

## Risk Assessment

### High Risk Areas

1. **Platform compatibility**: Async console I/O varies across Windows/Linux/macOS
2. **Serial driver issues**: Not all serial adapters play well with async
3. **Timing changes**: Removing sleeps might expose race conditions
4. **REPL protocol**: Async might change timing-sensitive protocol handshakes

### Mitigation Strategies

1. **Extensive testing**: Test on all major platforms with various hardware
2. **Fallback mechanisms**: Keep sync transport as fallback option
3. **Gradual rollout**: Use feature flags to enable async per-command
4. **Buffer management**: Carefully handle buffering in async streams
5. **Timeout tuning**: Adjust timeouts for async operations

### Rollback Plan

- Maintain sync transport code throughout v2.x
- Provide environment variable to force sync mode: `MPREMOTE_FORCE_SYNC=1`
- Document known issues and workarounds
- Quick-revert capability via feature flag

## Success Criteria

### Functional Goals

- ✅ All existing CLI commands work identically with async transport
- ✅ All unit tests pass with async implementation
- ✅ REPL functionality maintained on all platforms
- ✅ Filesystem operations work with same reliability
- ✅ At least one alternative transport (WebSocket) implemented

### Performance Goals

- ✅ 30%+ reduction in command execution time
- ✅ 2x+ improvement in file transfer throughput
- ✅ <10ms REPL input latency (vs. current ~20-30ms)
- ✅ Support 10+ concurrent device connections in single process

### Quality Goals

- ✅ 90%+ test coverage on async code
- ✅ Zero regression in existing functionality
- ✅ Complete API documentation
- ✅ Migration guide for library users

## Open Questions

2. **How to handle filesystem mounting with async?**
   - Current `TransportSerialIntercept` tightly coupled to serial
   - May need alternative approach for non-serial transports

3. **What to do about `` dependency in REPL?**
   - Currently couples REPL to serial transport
   - Need abstraction layer or alternative REPL approach

4. **Should async be opt-in or default?**
   - Recommendation: Default for new code, opt-in via CLI flag initially

5. **How to handle async in interactive Python sessions?**
   - Consider IPython async REPL support
   - Provide helper functions for common async patterns

## Hardware-less Development and Testing Approach

Based on PR #12802 (unix/main: Use standard pyexec/repl for unix port), we can develop and test the async transport layer without physical hardware by leveraging the MicroPython unix port.

### Unix Port as Test Target

**PR #12802 Background**:
- Consolidates REPL functionality across ports
- Unix port now uses standard `pyexec`/REPL implementation
- Enables `aiorepl` and consistent REPL behavior
- Maintains stdio in raw mode for consistency with other ports

**Key Advantages**:
1. Unix port executable runs locally without hardware
2. Supports all REPL modes (friendly, raw, raw paste)
3. Can test filesystem operations via VFS
4. Fast iteration without flashing firmware
5. Compatible with existing test infrastructure

### Mock Serial Transport for Development

Create a mock transport that communicates with the unix port via stdin/stdout pipes:

**New file**: `mpremote/transport_mock.py`

```python
import asyncio
import subprocess

class AsyncMockTransport(AsyncTransport):
    """Mock transport using unix port process for testing without hardware"""
    
    def __init__(self, micropython_path: str = None):
        self.micropython_path = micropython_path or "micropython"
        self.process = None
        self.in_raw_repl = False
        self.reader = None
        self.writer = None
    
    async def connect(self):
        """Start unix port as subprocess"""
        self.process = await asyncio.create_subprocess_exec(
            self.micropython_path,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        self.reader = self.process.stdout
        self.writer = self.process.stdin
    
    async def read(self, size: int = 1) -> bytes:
        """Read from process stdout"""
        return await self.reader.read(size)
    
    async def write(self, data: bytes) -> int:
        """Write to process stdin"""
        self.writer.write(data)
        await self.writer.drain()
        return len(data)
    
    async def close(self):
        """Terminate subprocess"""
        if self.process:
            self.process.terminate()
            await self.process.wait()
```

### Testing Strategy Without Hardware

#### 1. Unit Tests with Mock Transport

```python
# tests/test_async_transport_mock.py
import pytest
import asyncio
import os

MICROPYTHON = os.getenv("MICROPYTHON", "micropython")

@pytest.mark.asyncio
async def test_mock_transport_connect():
    """Test connection to unix port"""
    transport = AsyncMockTransport(MICROPYTHON)
    await transport.connect()
    assert transport.process is not None
    await transport.close()

@pytest.mark.asyncio
async def test_mock_transport_raw_repl():
    """Test entering raw REPL mode"""
    transport = AsyncMockTransport(MICROPYTHON)
    await transport.connect()
    
    await transport.enter_raw_repl()
    assert transport.in_raw_repl
    
    await transport.close()

@pytest.mark.asyncio
async def test_mock_transport_exec():
    """Test executing code"""
    transport = AsyncMockTransport(MICROPYTHON)
    await transport.connect()
    await transport.enter_raw_repl()
    
    stdout, stderr = await transport.exec_raw("print('hello async')")
    assert b'hello async' in stdout
    assert stderr == b''
    
    await transport.close()

@pytest.mark.asyncio
async def test_mock_transport_filesystem():
    """Test filesystem operations"""
    transport = AsyncMockTransport(MICROPYTHON)
    await transport.connect()
    await transport.enter_raw_repl()
    
    # Write file
    await transport.fs_writefile("/tmp/test.txt", b"test data")
    
    # Read file back
    data = await transport.fs_readfile("/tmp/test.txt")
    assert data == b"test data"
    
    await transport.close()
```

#### 2. Integration with Existing Test Infrastructure

Leverage the existing `tests/run-tests.py` and `tests/cmdline/repl_*.py` tests:

```python
# tests/test_async_repl_integration.py
"""Test async REPL against existing REPL test suite"""

import pytest
import asyncio
import os
from pathlib import Path

TESTS_DIR = Path(__file__).parent.parent / "tests" / "cmdline"

@pytest.mark.asyncio
@pytest.mark.parametrize("test_file", [
    "repl_basic.py",
    "repl_autocomplete.py",
    "repl_autoindent.py",
    "repl_paste.py",
])
async def test_repl_compatibility(test_file):
    """Run existing REPL tests with async transport"""
    test_path = TESTS_DIR / test_file
    exp_path = TESTS_DIR / f"{test_file}.exp"
    
    # Parse test file for commands
    with open(test_path, 'rb') as f:
        commands = parse_repl_test(f.read())
    
    # Execute via async transport
    transport = AsyncMockTransport()
    await transport.connect()
    
    output = await run_repl_commands(transport, commands)
    
    # Compare with expected output
    with open(exp_path, 'rb') as f:
        expected = normalize_output(f.read())
    
    assert normalize_output(output) == expected
    await transport.close()
```

#### 3. PTY-based Testing for Interactive REPL

For testing the async REPL loop with keyboard interaction:

```python
# tests/test_async_repl_pty.py
"""Test async REPL with PTY for keyboard simulation"""

import pytest
import asyncio
import os
import pty
import sys

if sys.platform == "win32":
    pytest.skip("PTY tests not supported on Windows", allow_module_level=True)

@pytest.mark.asyncio
async def test_async_repl_keyboard_input():
    """Test async REPL with simulated keyboard input"""
    master, slave = pty.openpty()
    
    # Start unix port with PTY as stdin/stdout
    process = await asyncio.create_subprocess_exec(
        "micropython",
        stdin=slave,
        stdout=slave,
        stderr=asyncio.subprocess.PIPE
    )
    
    # Simulate keyboard input
    os.write(master, b"print('test')\r")
    
    # Read output
    output = await asyncio.wait_for(
        asyncio.get_event_loop().run_in_executor(None, os.read, master, 1024),
        timeout=2.0
    )
    
    assert b"test" in output
    
    # Cleanup
    os.write(master, b"\x04")  # Ctrl-D to exit
    await process.wait()
    os.close(master)
    os.close(slave)
```

#### 4. Performance Benchmarking Without Hardware

```python
# tests/benchmark_async_transport.py
"""Benchmark async transport performance using unix port"""

import asyncio
import time
from mpremote.transport_mock import AsyncMockTransport

async def benchmark_exec_latency():
    """Measure command execution latency"""
    transport = AsyncMockTransport()
    await transport.connect()
    await transport.enter_raw_repl()
    
    iterations = 100
    start = time.perf_counter()
    
    for i in range(iterations):
        await transport.exec_raw(f"x = {i}")
    
    elapsed = time.perf_counter() - start
    avg_latency = (elapsed / iterations) * 1000  # ms
    
    print(f"Average command latency: {avg_latency:.2f}ms")
    
    await transport.close()
    return avg_latency

async def benchmark_concurrent_operations():
    """Measure concurrent execution performance"""
    transport = AsyncMockTransport()
    await transport.connect()
    await transport.enter_raw_repl()
    
    # Sequential execution
    start = time.perf_counter()
    for i in range(10):
        await transport.exec_raw("import time; time.sleep(0.1)")
    sequential_time = time.perf_counter() - start
    
    print(f"Sequential execution: {sequential_time:.2f}s")
    
    # Note: Unix port is single-process, so true concurrency not possible
    # But this tests the async infrastructure
    
    await transport.close()

if __name__ == "__main__":
    asyncio.run(benchmark_exec_latency())
    asyncio.run(benchmark_concurrent_operations())
```

### Development Workflow

#### Phase 0: Setup Development Environment

1. **Install dependencies** (on Debian/Ubuntu/Mint-based systems):
   ```bash
   sudo apt install build-essential git python3 pkg-config libffi-dev
   ```
   
   For other systems, see [ports/unix/README.md](../../ports/unix/README.md) for specific requirements.

2. **Build MicroPython unix port from PR #12802**:
   ```bash
   # From the top-level micropython directory
   cd mpy-cross
   make
   
   cd ../ports/unix
   make submodules
   make
   # Binary created at: build-standard/micropython
   ```
   
   Note: `make submodules` can be skipped if you didn't clone from git.

3. **Set up mpremote test environment**:
   ```bash
   cd ../../tools/mpremote
   python3 -m venv venv
   source venv/bin/activate  # On Linux/macOS
   # On Windows use: venv/Scripts/activate
   pip install -e ".[dev]"  # Install with dev dependencies
   ```

4. **Verify unix port REPL**:
   ```bash
   # Test interactive REPL
   ../../ports/unix/build-standard/micropython
   # Use Ctrl-D to exit
   
   # Test raw REPL entry
   echo -e "\x01" | ../../ports/unix/build-standard/micropython
   
   # Test complete test suite
   cd ../../tests
   ./run-tests.py
   ```

#### Development Iteration Loop

```
1. Implement async transport feature
   ↓
2. Write unit test using AsyncMockTransport
   ↓
3. Run test against unix port: pytest tests/test_async_*.py
   ↓
4. Debug issues (no hardware flashing needed!)
   ↓
5. Verify with existing REPL tests: ./tests/run-tests.py cmdline/repl_*.py
   ↓
6. Benchmark performance changes
   ↓
7. Once stable, test on real hardware (optional for most changes)
```

### CI/CD Integration

Update GitHub Actions workflow to test without hardware:

```yaml
# .github/workflows/test-mpremote-async.yml
name: Test mpremote async

on: [push, pull_request]

jobs:
  test-async-transport:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest]
        python-version: ['3.8', '3.11', '3.12']
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Build MicroPython unix port
        run: |
          cd mpy-cross
          make
          cd ../ports/unix
          make submodules
          make
      
      - name: Install mpremote with dev dependencies
        run: |
          cd tools/mpremote
          pip install -e ".[dev]"
      
      - name: Run async transport tests
        run: |
          cd tools/mpremote
          pytest tests/ -v --cov=mpremote --cov-report=xml
        env:
          MICROPYTHON: ../../ports/unix/build-standard/micropython
      
      - name: Run REPL compatibility tests
        run: |
          cd tests
          ./run-tests.py --async-transport cmdline/repl_*.py
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

### Advantages of This Approach

1. **Fast iteration**: No hardware flashing, instant feedback
2. **Reproducible**: Unix port behavior is consistent across runs
3. **Automated**: Can run in CI/CD without physical devices
4. **Comprehensive**: Tests same code paths as real hardware
5. **Cross-platform**: Works on Linux, macOS, Windows (with WSL)
6. **Debugging**: Can use standard Python debuggers (pdb, IDE debuggers)
7. **Concurrent testing**: Run multiple test instances in parallel

### Limitations and Hardware Testing

While unix port testing covers most functionality, hardware testing is still needed for:

1. **Serial-specific issues**: Baud rate, flow control, USB quirks
2. **Platform variations**: Different boards may have REPL variations
3. **Timing edge cases**: Real serial latencies may expose race conditions
4. **Filesystem mounting**: `TransportSerialIntercept` behavior
5. **Device-specific commands**: Bootloader entry, device reset

**Recommendation**: 
- Develop 90% of async features using unix port
- Test 10% critical paths on 2-3 representative hardware platforms
- Maintain hardware test matrix: ESP32, RP2040, STM32

### Mock Transport Extensions

For more realistic testing, extend mock transport to simulate hardware behaviors:

```python
class AsyncMockTransportWithLatency(AsyncMockTransport):
    """Mock transport with simulated serial latency"""
    
    def __init__(self, *args, latency_ms=10, **kwargs):
        super().__init__(*args, **kwargs)
        self.latency_ms = latency_ms
    
    async def read(self, size: int = 1) -> bytes:
        """Simulate serial read latency"""
        await asyncio.sleep(self.latency_ms / 1000)
        return await super().read(size)
    
    async def write(self, data: bytes) -> int:
        """Simulate serial write latency"""
        await asyncio.sleep(self.latency_ms / 1000)
        return await super().write(data)

class AsyncMockTransportWithErrors(AsyncMockTransport):
    """Mock transport that simulates connection errors"""
    
    def __init__(self, *args, error_rate=0.01, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_rate = error_rate
    
    async def read(self, size: int = 1) -> bytes:
        """Randomly inject read errors"""
        if random.random() < self.error_rate:
            raise OSError("Simulated read error")
        return await super().read(size)
```

## Next Steps

1. **Setup**: Build unix port from PR #12802 and set up test environment
2. **Mock Transport**: Implement `AsyncMockTransport` for unix port communication
3. **Prototype**: Build minimal AsyncSerialTransport with basic exec_raw()
4. **Unit Tests**: Write comprehensive tests using mock transport
5. **Validate**: Test prototype on unix port across platforms (Linux, macOS, Windows/WSL)
6. **Hardware Validation**: Test on 2-3 representative hardware platforms
7. **Refine**: Adjust API based on prototype learnings
8. **Implement**: Follow phased implementation plan
9. **Review**: Get feedback from MicroPython community
10. **Document**: Write comprehensive migration guide
11. **Release**: Ship as experimental feature in v1.x, stabilize in v2.0
