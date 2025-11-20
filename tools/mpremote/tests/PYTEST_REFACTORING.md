# Pytest Refactoring of mpremote Async Tests

## Summary

The mpremote async tests have been refactored to run under pytest with proper fixtures for reducing code duplication, accounting for platform differences, and using pytest-native reporting.

## Refactored Test Files

The following test files have been converted from custom test runners or unittest to pytest:

1. **test_async_transport.py** - Basic async transport tests
2. **test_async_modules.py** - Module-level async tests  
3. **test_async_comprehensive.py** - Comprehensive async transport tests
4. **test_async_coverage.py** - Additional coverage tests for async modules
5. **test_async_hardware.py** - Hardware integration tests with real devices

## Key Improvements

### 1. Pytest Fixtures (conftest.py)

The `conftest.py` file provides reusable fixtures that reduce code duplication:

- **`async_modules`** - Provides async module imports if available
- **`platform_info`** - Platform detection (Windows/POSIX)
- **`event_loop`** - Async event loop setup/teardown
- **`hardware_device`** - Auto-detects MicroPython devices for hardware tests
- **`connected_transport`** - Creates and manages async transport connections

### 2. Platform-Specific Test Handling

Tests are now automatically skipped based on platform requirements using markers:

- **`@pytest.mark.windows_only`** - Runs only on Windows
- **`@pytest.mark.posix_only`** - Runs only on POSIX systems (Linux, macOS)
- **`@pytest.mark.async_required`** - Requires async modules
- **`@pytest.mark.serial_required`** - Requires pyserial-asyncio
- **`@pytest.mark.hardware_required`** - Requires connected hardware device

The `pytest_collection_modifyitems` hook automatically skips tests based on these markers.

### 3. Reduced Code Duplication

Before:
```python
import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    from mpremote.transport_async import AsyncTransport
    HAS_ASYNC = True
except ImportError:
    HAS_ASYNC = False

@unittest.skipUnless(HAS_ASYNC, "Async modules not available")
class TestProtocol(unittest.TestCase):
    def test_control_codes(self):
        self.assertEqual(RawREPLProtocol.CTRL_A, b"\x01")
```

After:
```python
import pytest

pytestmark = pytest.mark.async_required

def test_protocol_control_codes(async_modules):
    """Test protocol control codes are correct."""
    RawREPLProtocol = async_modules["RawREPLProtocol"]
    assert RawREPLProtocol.CTRL_A == b"\x01"
```

### 4. Native Pytest Assertions

All tests now use pytest's native assertion rewriting instead of unittest-style assertions:

- `self.assertEqual(a, b)` → `assert a == b`
- `self.assertTrue(x)` → `assert x is True`
- `self.assertIsNone(x)` → `assert x is None`

This provides better error messages and more pythonic test code.

## Running the Tests

### Run all refactored async tests:
```bash
pytest test_async_transport.py test_async_modules.py test_async_comprehensive.py test_async_coverage.py -v
```

### Run with specific markers:
```bash
# Run only Windows tests
pytest -m windows_only -v

# Run only POSIX tests
pytest -m posix_only -v

# Skip hardware tests
pytest -m "not hardware_required" -v
```

### Run with custom device for hardware tests:
```bash
pytest --device=COM20 test_async_hardware.py
pytest --device=/dev/ttyUSB0 test_async_hardware.py
```

## Test Statistics

After refactoring:
- **64 tests passed** (unit tests without hardware)
- **16 hardware integration tests** (require connected MicroPython device)
- **7 tests skipped** (platform-specific or missing dependencies)
- **0 tests failed**
- **Execution time: ~0.18 seconds** (unit tests only)

## Benefits

1. **Better Test Organization**: Tests are grouped logically with clear naming
2. **Automatic Platform Handling**: No manual platform checks needed
3. **Cleaner Code**: Less boilerplate, more readable tests
4. **Better Error Messages**: Pytest's assertion rewriting provides detailed failure information
5. **Consistent Reporting**: All reporting goes through pytest's standard output
6. **Easier Debugging**: Use `pytest --pdb` to drop into debugger on failure
7. **Flexible Test Selection**: Use markers and keywords to run specific test subsets

## Migration Notes

### For Test Authors

When adding new tests:

1. Mark the test file or individual tests with appropriate markers
2. Use fixtures from `conftest.py` instead of manual setup/teardown
3. Use pytest-style assertions (`assert`) instead of unittest assertions
4. Use the `async_modules` fixture to access async components

### For CI/CD

The tests can be integrated into CI/CD pipelines with standard pytest commands:

```bash
# Run all tests with coverage
pytest --cov=mpremote --cov-report=html

# Run with JUnit XML output for CI
pytest --junitxml=test-results.xml

# Run with specific verbosity
pytest -v --tb=short
```

## Future Enhancements

Potential improvements for the test suite:

1. Add `pytest-asyncio` support for native async test handling
2. Create more fixtures for common test scenarios
3. Add parametrized tests for testing multiple configurations
4. Implement test fixtures for mock devices
5. Add integration with hardware test farms

## Dependencies

Required for running the tests:
- `pytest>=7.0`
- `pytest-asyncio>=0.21` (optional, for better async support)

Optional dependencies:
- `pyserial-asyncio` (for hardware tests)
- `pytest-cov` (for coverage reporting)
- `pytest-xdist` (for parallel test execution)
