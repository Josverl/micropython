# MicroPython REPL Tests

Pytest-based tests for MicroPython REPL interaction, focused on Unicode handling.

## Setup

### Prerequisites

```bash
pip install pytest pexpect
```

### Build MicroPython

```bash
cd ~/micropython/ports/unix
make submodules
make
```

## Running Tests

```bash
cd ~/micropython/tests/pytest

# Run all tests
pytest -v

# Run specific test
pytest pytest_repl_simple.py::test_repl_output -v

# Skip unicode tests (known to fail due to issue #7585)
pytest -m "not unicode" -v

# Run only unicode tests
pytest -m unicode -v

# Custom MicroPython path
MICROPYTHON_PATH=/path/to/micropython pytest -v
```

## Test Structure

- **conftest.py** - Pytest configuration and fixtures
- **pytest_repl_simple.py** - REPL interaction tests

**Note:** Test files use `pytest_*.py` naming (not `test_*.py`) to clearly distinguish them from MicroPython's traditional test suite.

### Key Fixtures

- `micropython_path` - Provides path to MicroPython executable
- `repl` - Manages REPL session lifecycle (startup/cleanup)

### Helper Functions

- `send_and_expect()` - Send command and verify expected output

## Tests

### Basic Tests
- `test_repl_output` - Parametrized test for basic commands:
  - Print statements
  - Arithmetic evaluation
  - Unicode handling (demonstrates issue #7585)

### Special Character Tests
- `test_repl_backspace` - Backspace/delete key handling
- `test_repl_escape_sequences` - Tab, newline, quotes, backslashes
- `test_repl_ctrl_c_interrupt` - Ctrl-C interrupt handling

### Unicode Tests (marked with `@pytest.mark.unicode`)
- `test_repl_various_unicode` - Multiple Unicode scripts:
  - French (café) - Latin with diacritics
  - Chinese (你好) - CJK characters
  - Russian (Привет) - Cyrillic
  - Emoji (😀) - 4-byte UTF-8

**Note:** All Unicode tests currently fail due to issue #7585 where non-ASCII characters are lost during REPL input.

## Design Principles

- **DRY**: Single fixture handles REPL lifecycle
- **Clean**: No test classes, minimal noise
- **Focused**: Each test verifies one behavior
- **Graceful exit**: Tests use `os._exit(0)`, Ctrl-D, or terminate as fallback

## Framework Origin

Adapted from `feat/MP_Bridge_refactor` branch (`tools/mpremote/tests/`), simplified for direct unix port testing.

## Separation from Traditional Tests

This pytest framework is **completely separate** from MicroPython's traditional test suite:

- **Naming**: Uses `pytest_*.py` (not `test_*.py`) to avoid confusion
- **Purpose**: Interactive REPL testing vs. non-interactive script execution
- **Tool**: pytest framework vs. `run-tests.py` custom runner
- **Isolation**: Not picked up by `make test` or `./run-tests.py` - must run `pytest` explicitly
