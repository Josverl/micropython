# Plan: AsyncIO Integration in mpremote

## Overview
This plan outlines the integration of asyncio into mpremote to handle communication between mpremote and the MCU asynchronously. The goal is to make the communication more efficient and extensible for other protocols.

## Phase 1: Core AsyncIO Transport Layer
**Goal:** Create an async-compatible transport layer that maintains backward compatibility.

### Tasks:
1. **Create AsyncTransport Base Class**
   - Location: `tools/mpremote/mpremote/transport_async.py`
   - Add async methods for core operations:
     - `async def read_async(self, size)` - asynchronous read
     - `async def write_async(self, data)` - asynchronous write
     - `async def exec_async(self, command)` - async command execution
     - `async def eval_async(self, expression)` - async expression evaluation
   - Maintain compatibility with existing synchronous Transport base class

2. **Create AsyncSerialTransport**
   - Location: `tools/mpremote/mpremote/transport_serial_async.py`
   - Extend SerialTransport with async capabilities
   - Use `asyncio` for serial I/O operations
   - Implement async versions of:
     - Connection management
     - Raw REPL entry/exit
     - Data read/write operations

3. **Add asyncio utility functions**
   - Location: `tools/mpremote/mpremote/async_utils.py`
   - Helper functions for async/sync interop
   - Async context managers
   - Timeout handlers

### Success Criteria:
- AsyncTransport class with core async methods implemented
- AsyncSerialTransport can connect and communicate with device
- Existing synchronous code continues to work
- Basic async read/write operations functional

## Phase 2: Async Command Layer
**Goal:** Enable async execution of mpremote commands.

### Tasks:
1. **Update commands.py for async support**
   - Add async versions of key commands:
     - `async_do_connect()` - async connection
     - `async_do_exec()` - async exec command
     - `async_do_eval()` - async eval command
     - `async_do_filesystem()` - async file operations
   - Keep synchronous wrappers for backward compatibility

2. **Create async filesystem operations**
   - Update Transport class in `transport.py`:
     - `async def fs_readfile_async()`
     - `async def fs_writefile_async()`
     - `async def fs_listdir_async()`
   - Enable concurrent file operations

3. **Add async state management**
   - Update State class in `main.py`
   - Add async context manager support
   - Manage async transport lifecycle

### Success Criteria:
- Async versions of common commands available
- File operations can be performed asynchronously
- Multiple operations can run concurrently
- Backward compatibility maintained

## Phase 3: Testing Infrastructure
**Goal:** Establish comprehensive testing for async functionality.

### Tasks:
1. **Create async test framework**
   - Location: `tools/mpremote/tests/test_async.py`
   - Test async transport layer
   - Test async command execution
   - Test concurrent operations

2. **Add Unix port testing support**
   - Build Unix port for testing: `ports/unix/build-standard/micropython`
   - Create test harness that uses Unix port instead of hardware
   - Mock serial communication for local testing

3. **Create example async scripts**
   - Location: `tools/mpremote/examples/async_example.py`
   - Demonstrate async command usage
   - Show concurrent operations
   - Document async patterns

### Success Criteria:
- Async tests pass without hardware
- Unix port can be used for local development
- Examples demonstrate async capabilities
- Documentation covers async usage

## Testing Without Hardware

### Unix Port Setup
```bash
# Build the Unix port
cd ports/unix
make submodules
make

# Run MicroPython REPL
./build-standard/micropython
```

### Mock Testing Approach
1. Use Unix port as a local MicroPython instance
2. Create a mock serial transport that communicates with Unix port via stdin/stdout
3. Test async operations against the local instance
4. Validate behavior before testing on actual hardware

### Environment Setup (Linux)
```bash
# Install dependencies
sudo apt-get update
sudo apt-get install build-essential libffi-dev git pkg-config

# Python dependencies
pip install -e tools/mpremote[dev]
pip install pytest pytest-asyncio
```

## Implementation Notes

### Key Design Principles:
1. **Backward Compatibility**: All existing synchronous code must continue to work
2. **Opt-in Async**: Async features are available but not required
3. **Minimal Changes**: Keep changes surgical and focused
4. **Extensibility**: Design for future protocol additions (WebREPL, BLE, etc.)

### Dependencies to Add:
- No new external dependencies required (asyncio is in standard library)
- Consider `pytest-asyncio` for testing (dev dependency only)

### Files to Modify:
- `tools/mpremote/mpremote/transport.py` - Add async method signatures
- `tools/mpremote/mpremote/main.py` - Add async state support (optional)
- `tools/mpremote/mpremote/commands.py` - Add async command versions (optional)

### Files to Create:
- `tools/mpremote/mpremote/transport_async.py` - Async transport base
- `tools/mpremote/mpremote/transport_serial_async.py` - Async serial transport
- `tools/mpremote/mpremote/async_utils.py` - Async utilities
- `tools/mpremote/tests/test_async.py` - Async tests
- `tools/mpremote/examples/async_example.py` - Usage examples

## Future Phases (Not in Scope)

### Phase 4: Protocol Extensibility
- Plugin architecture for new transport types
- WebREPL async support
- BLE async support
- Network socket support

### Phase 5: Performance Optimization
- Connection pooling
- Batch operations
- Smart caching
- Parallel device management

## References
- Python asyncio documentation: https://docs.python.org/3/library/asyncio.html
- MicroPython mpremote: https://docs.micropython.org/en/latest/reference/mpremote.html
