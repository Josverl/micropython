# Tests for mpremote

This directory contains a set of tests for `mpremote`.

## Test Categories

### Shell Script Tests (Bash)
Traditional integration tests using bash scripts (`.sh` files).

**Requirements:**
- A device running MicroPython connected to a serial port on the host.
- The device you are testing against must be flashed with a firmware of the same build
  as `mpremote`.
- If the device has an SDcard or other vfs mounted, the vfs's filesystem must be empty
  to pass the filesystem test.
- Python 3.x, `bash` and various Unix tools such as `find`, `mktemp`, `sed`, `sort`, `tr`.
- To test on Windows, you can either:
    - Run the (Linux) tests in WSL2 against a USB device that is passed though to WSL2.
    - Use the `Git Bash` terminal to run the tests against a device connected to a COM
      port. _Note:_ While the tests will run in `Git Bash`, several will throw false
      positive errors due to differences in the way that TMP files are logged and and
      several other details.

**To run the bash tests:**

    $ cd tools/mpremote/tests
    $ ./run-mpremote-tests.sh

**To run a single test:**

    $ ./run-mpremote-tests.sh test_filesystem.sh

Each test should print "OK" if it passed.  Otherwise it will print "CRASH", or "FAIL"
and a diff of the expected and actual test output.

### Python Tests

#### Unit Tests (No Hardware Required)
- `test_async_modules.py` - Tests module structure, imports, and API
- `test_async_transport.py` - Mock-based transport tests
- `test_async_coverage.py` - Mock-based coverage tests
- `test_async_comprehensive.py` - Integration tests without hardware
- `validate_implementation.py` - Validates async implementation completeness

**Run unit tests:**

    $ python test_async_modules.py

#### Hardware Integration Tests (Requires Device)
- `test_async_hardware.py` - Comprehensive async transport tests against real hardware

**Requirements:**
- A MicroPython device connected via serial or USB-CDC
- `pyserial-asyncio` installed

**Run with auto-detected device:**

    $ python test_async_hardware.py

**Run with specific port:**

    $ python test_async_hardware.py COM20
    $ python test_async_hardware.py /dev/ttyUSB0

**Run specific test:**

    $ python test_async_hardware.py COM20 TestAsyncHardware.test_basic_connection

#### REPL Tests
- `test_repl_async_integration.py` - Async REPL tests using MicroPython Unix port
- `test_repl_async_unix.py` - Unix-specific REPL tests

**Requirements:**
- MicroPython unix port binary (`ports/unix/build-standard/micropython`)

**Run REPL tests:**

    $ python test_repl_async_integration.py
