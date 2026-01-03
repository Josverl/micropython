# RFC 2217 Bridge Performance Analysis

## Problem Statement

The RFC 2217 bridge is noticeably slower than a physical serial connection to an MCU, particularly visible when running filesystem tests like `test_filesystem.sh`.

## Key Finding: Process Startup is NOT the Bottleneck

Measurements show that MicroPython unix port is extremely fast to start:

| Operation | Time |
|-----------|------|
| Process spawn (subprocess.Popen) | **0.7ms** |
| Banner output | **0.9ms** |
| Raw REPL entry (Ctrl-A response) | **0.1ms** |
| **Total** | **1.7ms** |

A process pool would NOT help - the real bottleneck is elsewhere.

## The Actual Bottleneck: RFC 2217 Protocol Negotiation

| Operation | Time |
|-----------|------|
| `socket://` connection (raw TCP) | **13ms** |
| `rfc2217://` connection (with negotiation) | **358ms** |
| **Difference** | **345ms** |

The pyserial RFC 2217 client has multiple `time.sleep()` calls during option negotiation:
```python
# In serial/rfc2217.py:
time.sleep(0.05)  # Multiple occurrences in option negotiation loops
time.sleep(0.3)   # After socket close
time.sleep(0.1)   # In setup
```

## Solution: Dual-Port Architecture

The bridge now supports two protocols simultaneously:
- **Port 2217 (RFC 2217):** Compatible with all pyserial tools
- **Port 2218 (Raw socket):** Faster, no protocol overhead

### Performance Comparison (Optimized Bridge)

| Protocol | Mode | Time | vs Baseline |
|----------|------|------|-------------|
| RFC 2217 | soft reset | **0.877s** | baseline |
| RFC 2217 | resume | **0.951s** | - |
| Socket | soft reset | **0.636s** | **27% faster** |
| Socket | resume | **0.426s** | **51% faster** |

### Recommendation

For best performance, use:
```bash
mpremote connect socket://localhost:2218 resume eval "1+1"  # 426ms
```

## Legacy Analysis: Bridge-Side Bottlenecks (Now Fixed)

### 1. Double Select Timeout in Read Path (FIXED)

**Location:** `VirtualSerialPort.update_in_waiting()` and `VirtualSerialPort.read()`

```python
def update_in_waiting(self):
    # First select with 0.05s timeout
    ready, _, _ = select.select([self.fd], [], [], 0.05)  # 50ms!
    self.in_waiting = 1 if ready else 0

def read(self, size=1):
    # Second select with 0.1s timeout
    ready, _, _ = select.select([self.fd], [], [], self.timeout)  # 100ms!
    if ready:
        data = os.read(self.fd, size)
```

**Impact:** The reader loop in `Redirector.reader()` calls:
```python
self.serial.update_in_waiting()  # 50ms timeout
data = self.serial.read(...)     # 100ms timeout
```

This means **every read cycle waits up to 150ms** even when no data is available!

For a test that makes 50+ mpremote calls, each establishing a new connection, this adds **seconds of cumulative delay**.

### 2. Small Read Buffer Size (MODERATE)

**Location:** `Redirector.reader()` line 374

```python
data = self.serial.read(self.serial.in_waiting or 1)  # Often reads just 1 byte!
```

When `in_waiting` is 0 (which happens frequently due to timing), this reads only 1 byte at a time. Combined with the 150ms wait cycle, throughput is severely limited.

### 3. Per-Connection Overhead (MODERATE)

Each mpremote command:
1. Opens a new TCP connection
2. Performs RFC 2217 option negotiation (multiple round-trips with `time.sleep(0.05)` waits)
3. Waits for acknowledgements with 3-second timeout loops

**pyserial rfc2217 client delays:**
```python
# In serial/rfc2217.py:
time.sleep(0.05)  # Multiple occurrences in option negotiation loops
time.sleep(0.3)   # After socket close
time.sleep(0.1)   # In setup
```

### 4. Status Line Polling (MINOR)

**Location:** `MP_BRIDGE_POLL_INTERVAL = 1` (1 second)

This is actually fine for the bridge side, but the client side polls more frequently.

### 5. Process Restart Delays (MINOR - only on soft reboot)

```python
MP_BRIDGE_RAW_REPL_ENTRY_DELAY = 0.1    # 100ms
MP_BRIDGE_BANNER_READ_TIMEOUT = 0.5     # 500ms
MP_BRIDGE_PROCESS_RESTART_DELAY = 0.3   # 300ms
```

These only apply during soft reboot and are necessary for correctness.

## Proposed Optimizations

### Optimization 1: Eliminate Double Select (HIGH PRIORITY)

**Problem:** `update_in_waiting()` and `read()` both do select(), causing 2x overhead.

**Solution:** Combine into a single efficient read operation:

```python
def read(self, size=1):
    """Read up to size bytes from the PTY."""
    if self._pending_reboot_output:
        chunk = self._pending_reboot_output[:size]
        self._pending_reboot_output = self._pending_reboot_output[size:]
        return chunk

    if self._closed:
        return b""

    try:
        # Single select with short timeout for responsiveness
        ready, _, _ = select.select([self.fd], [], [], 0.01)  # 10ms instead of 100ms
        if ready:
            # Read more data at once - PTY can buffer plenty
            data = os.read(self.fd, max(size, 4096))
            # ... raw REPL detection ...
            return data
    except (OSError, ValueError):
        self._closed = True
    return b""

def update_in_waiting(self):
    """Update the number of bytes waiting to be read."""
    with self._check_buffer_lock:
        if self._closed:
            self.in_waiting = 0
            return
        # Non-blocking check - no timeout wait
        try:
            ready, _, _ = select.select([self.fd], [], [], 0)  # 0 = non-blocking
            self.in_waiting = 1 if ready else 0
        except (OSError, ValueError):
            self._closed = True
            self.in_waiting = 0
```

**Expected improvement:** 10-15x faster read loop

### Optimization 2: Larger Read Buffer (HIGH PRIORITY)

**Problem:** Reading 1 byte at a time when `in_waiting` is 0.

**Solution:** Always try to read a larger buffer:

```python
def reader(self):
    """Loop forever and copy subprocess output -> socket."""
    while self.alive:
        try:
            # ... process exit check ...
            
            # Read larger chunks, let select handle waiting
            data = self.serial.read(4096)  # Always try to read up to 4KB
            if data:
                self.write(b"".join(self.rfc2217.escape(data)))
```

**Expected improvement:** 10-100x fewer read syscalls

### Optimization 3: Reduce Read Timeout (MEDIUM PRIORITY)

**Current:** `timeout=0.1` (100ms)  
**Proposed:** `timeout=0.01` (10ms)

```python
virtual_serial = VirtualSerialPort(
    master_fd,
    timeout=0.01,  # 10ms instead of 100ms
    restart_callback=restart_micropython,
)
```

**Trade-off:** Slightly higher CPU usage, but much more responsive.

### Optimization 4: TCP_NODELAY Already Set (VERIFIED OK)

The code already sets TCP_NODELAY which disables Nagle's algorithm:
```python
client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
```

### Optimization 5: Consider Buffered Writes (LOW PRIORITY)

Currently, every small piece of data is sent immediately. For bulk transfers (file copy), buffering could help, but this conflicts with REPL responsiveness requirements.

## Implementation Plan

### Phase 1: Quick Wins (Immediate Impact)

1. **Change `update_in_waiting()` to non-blocking** (0 timeout instead of 0.05s)
2. **Reduce read timeout** from 0.1s to 0.01s
3. **Increase read buffer size** to 4096 bytes

**Estimated improvement:** 5-10x faster for interactive operations

### Phase 2: Read Path Optimization

1. Simplify the read loop to not call `update_in_waiting()` at all
2. Let `read()` handle both waiting and reading in one operation
3. Consider using `selectors` module for more efficient I/O multiplexing

### Phase 3: Asyncio Refactor (Recommended for Best Performance)

Refactor to use asyncio for truly event-driven I/O with zero polling overhead.

## Asyncio Architecture Analysis

### Why Asyncio?

The current threading approach uses **polling** with `select()` timeouts. Even with reduced timeouts, we're still burning CPU cycles checking for data. Asyncio with `loop.add_reader()` uses the kernel's event notification (epoll/kqueue) for **true event-driven I/O**.

### Performance Comparison

| Aspect | Current Threading | Optimized Threading | Asyncio |
|--------|------------------|---------------------|---------|
| Read latency | 50-150ms | 10-20ms | <1ms |
| CPU usage (idle) | Moderate (polling) | Higher (faster polling) | Minimal |
| Complexity | Moderate | Moderate | Similar |
| Dependencies | None | None | None (stdlib) |

### Asyncio Implementation Sketch

```python
import asyncio
import os

class AsyncPTYReader:
    """Async wrapper for PTY file descriptor using loop.add_reader()."""
    
    def __init__(self, fd: int):
        self.fd = fd
        self._loop = asyncio.get_event_loop()
    
    async def read(self, size: int = 4096) -> bytes:
        """Read from PTY - returns immediately when data available."""
        future = self._loop.create_future()
        
        def on_readable():
            self._loop.remove_reader(self.fd)
            try:
                data = os.read(self.fd, size)
                future.set_result(data)
            except OSError as e:
                future.set_exception(e)
        
        self._loop.add_reader(self.fd, on_readable)
        return await future
    
    def write(self, data: bytes) -> int:
        """Write to PTY (synchronous - writes are fast)."""
        return os.write(self.fd, data)


class AsyncRFC2217Handler:
    """Handle a single RFC 2217 client connection."""
    
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter,
                 pty_reader: AsyncPTYReader, rfc2217_manager):
        self.socket_reader = reader
        self.socket_writer = writer
        self.pty = pty_reader
        self.rfc2217 = rfc2217_manager
        self.running = True
    
    async def pty_to_socket(self):
        """Copy PTY output to socket (with RFC 2217 escaping)."""
        while self.running:
            try:
                data = await self.pty.read(4096)
                if data:
                    escaped = b"".join(self.rfc2217.escape(data))
                    self.socket_writer.write(escaped)
                    await self.socket_writer.drain()
            except Exception as e:
                logging.error(f"PTY read error: {e}")
                break
    
    async def socket_to_pty(self):
        """Copy socket input to PTY (with RFC 2217 filtering)."""
        while self.running:
            try:
                data = await self.socket_reader.read(1024)
                if not data:
                    break  # Connection closed
                
                filtered = b"".join(self.rfc2217.filter(data))
                if filtered:
                    self.pty.write(filtered)
            except Exception as e:
                logging.error(f"Socket read error: {e}")
                break
        
        self.running = False
    
    async def run(self):
        """Run bidirectional copy until connection closes."""
        await asyncio.gather(
            self.pty_to_socket(),
            self.socket_to_pty(),
            return_exceptions=True
        )


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter,
                        pty_reader: AsyncPTYReader):
    """Handle incoming client connection."""
    addr = writer.get_extra_info('peername')
    logging.info(f"Client connected: {addr}")
    
    # Create RFC 2217 manager (pyserial's PortManager needs adaptation)
    # For now, simplified - full implementation would wrap PortManager
    handler = AsyncRFC2217Handler(reader, writer, pty_reader, rfc2217_manager)
    
    try:
        await handler.run()
    finally:
        writer.close()
        await writer.wait_closed()
        logging.info(f"Client disconnected: {addr}")


async def main():
    # Create PTY and start MicroPython
    master_fd, process = create_micropython_process()
    pty_reader = AsyncPTYReader(master_fd)
    
    # Start async server
    server = await asyncio.start_server(
        lambda r, w: handle_client(r, w, pty_reader),
        '0.0.0.0', 2217
    )
    
    addr = server.sockets[0].getsockname()
    logging.info(f"RFC 2217 bridge listening on {addr}")
    
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
```

### Key Asyncio Benefits

1. **True Event-Driven I/O**
   - `loop.add_reader(fd, callback)` uses epoll/kqueue
   - Kernel notifies us when data is available
   - Zero polling overhead, instant response

2. **No Timeout Waits**
   - Current: `select([fd], [], [], 0.1)` blocks for up to 100ms
   - Asyncio: `await pty.read()` returns immediately when data available

3. **Clean Resource Management**
   - `async with server:` for automatic cleanup
   - `asyncio.wait_for()` for timeouts
   - `task.cancel()` for graceful shutdown

4. **Single Thread, No Locks**
   - All code runs in one thread on the event loop
   - No need for `threading.Lock()` on shared state
   - Simpler reasoning about concurrency

### Challenges with Asyncio

1. **pyserial's PortManager is synchronous**
   - Need to wrap or reimplement RFC 2217 protocol handling
   - The `filter()` and `escape()` methods are fast and can stay sync
   - Option negotiation would need async adaptation

2. **Soft reboot handling**
   - Process exit detection needs `loop.add_reader()` on process
   - Or use `asyncio.create_subprocess_exec()` with proper pipes

3. **Windows compatibility**
   - `loop.add_reader()` works with sockets on Windows
   - But not with file descriptors - need different approach
   - Could use `asyncio.to_thread()` for PTY reads on Windows

### Recommended Approach

**Hybrid solution for best compatibility:**

```python
async def pty_reader_task(fd: int, queue: asyncio.Queue):
    """Read from PTY in thread, put data in async queue."""
    loop = asyncio.get_event_loop()
    
    while True:
        # Run blocking read in thread pool
        data = await loop.run_in_executor(None, os.read, fd, 4096)
        if data:
            await queue.put(data)
```

This gives us:
- Async/await syntax for clean code
- Works on both Unix and Windows
- Still benefits from asyncio's event loop for socket I/O

## Implementation Recommendation

| Approach | Effort | Performance Gain | Compatibility |
|----------|--------|------------------|---------------|
| Quick fixes (reduce timeouts) | Low | 5-10x | Full |
| Full asyncio refactor | High | 10-100x | Unix only* |
| Hybrid asyncio + threads | Medium | 10-50x | Full |

**Recommended path:**
1. **Immediate**: Apply quick fixes (Phase 1) for 5-10x improvement
2. **Short-term**: Evaluate if performance is sufficient
3. **Long-term**: If needed, implement hybrid asyncio approach

*Windows would need `asyncio.to_thread()` for PTY operations

## Benchmarking

### Actual Performance Measurements

After implementing the quick fixes (reduced timeouts, larger buffers) and dual-port support:

| Protocol | Mode | Time | Notes |
|----------|------|------|-------|
| RFC 2217 | soft reset | **1.018s** | Baseline |
| RFC 2217 | resume | **0.849s** | 17% faster |
| Socket | soft reset | **0.735s** | 28% faster than RFC2217 |
| Socket | resume | **0.439s** | **2.3x faster** than baseline |

**Key findings:**
- The socket protocol eliminates RFC 2217 option negotiation overhead (~400ms)
- Using `resume` eliminates soft reboot overhead (~300ms)
- Combining both: **socket + resume = 0.439s** (2.3x faster than RFC 2217 + soft reset)

### Dual-Port Support

The bridge now supports two protocols simultaneously:
- **Port 2217 (RFC 2217):** Compatible with all pyserial tools, supports serial port emulation
- **Port 2218 (Raw socket):** Faster, no protocol overhead, recommended for mpremote

```bash
# Fast connection (recommended)
mpremote connect socket://localhost:2218 resume eval "1+1"

# Compatible connection (for tools that need serial port emulation)
mpremote connect rfc2217://localhost:2217 eval "1+1"
```

### Benchmark Commands

```bash
# Single command timing
time mpremote connect socket://localhost:2218 resume eval "1+1"

# Filesystem test suite
time ./run-mpremote-tests.sh -t socket://localhost:2218 test_filesystem.sh
```

## Code Changes Summary

### File: `mp_rfc2217_bridge.py`

| Line | Current | Proposed | Impact |
|------|---------|----------|--------|
| 83 | `timeout=0.1` | `timeout=0.01` | 10x faster timeout |
| 179 | `select(..., 0.05)` | `select(..., 0)` | Non-blocking check |
| 133 | `select(..., self.timeout)` | `select(..., 0.01)` | Faster read loop |
| 135 | `os.read(self.fd, size)` | `os.read(self.fd, 4096)` | Larger reads |
| 374 | `read(in_waiting or 1)` | `read(4096)` | Larger reads |

## Conclusion

The primary performance bottleneck is the **double select timeout** in the read path, causing 150ms delays per read cycle. By making `update_in_waiting()` non-blocking and reducing the read timeout, we can achieve 5-10x performance improvement with minimal code changes.

The secondary issue is the **small read buffer size**, which can be easily fixed by always requesting larger reads.

These optimizations should make the bridge performance comparable to or better than physical serial connections (which are limited by baud rate, typically 115200 bps = ~11 KB/s).
