# MicroPython Development Instructions

MicroPython is a Python 3.x implementation for microcontrollers and small embedded systems. This repository contains the core Python runtime, cross-compiler, platform-specific ports, extensive test suite, and documentation.

**ALWAYS reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.**

## Critical Build Timing and Cancellation Warnings

**NEVER CANCEL BUILD OR TEST COMMANDS**. Builds can take 45+ minutes, tests can take 15+ minutes.

- `mpy-cross` build: 15 seconds - NEVER CANCEL (timeout: 60+ seconds)
- Unix port `make submodules`: 6 seconds - NEVER CANCEL (timeout: 60+ seconds)  
- Unix port `make`: 33 seconds - NEVER CANCEL (timeout: 120+ seconds)
- STM32 port `make submodules`: 13 seconds - NEVER CANCEL (timeout: 120+ seconds)
- STM32 port `make BOARD=PYBV11`: 63 seconds - NEVER CANCEL (timeout: 180+ seconds)
- Test suites: 1-15 minutes - NEVER CANCEL (timeout: 30+ minutes)
- Full CI builds: 5-45 minutes - NEVER CANCEL (timeout: 60+ minutes)

## Working Effectively

Bootstrap, build, and test the repository in this exact order:

```bash
# Install essential dependencies
sudo apt-get update
sudo apt-get install build-essential libffi-dev git pkg-config

# For STM32 and other ARM ports, install ARM cross-compiler
sudo apt-get install gcc-arm-none-eabi libnewlib-arm-none-eabi

# Build mpy-cross (cross-compiler) - REQUIRED FIRST
cd mpy-cross
make  # Takes 15 seconds, NEVER CANCEL, set timeout 60+ seconds

# Build Unix port (primary development platform)
cd ../ports/unix
make submodules  # Takes 6 seconds, NEVER CANCEL, set timeout 60+ seconds
make  # Takes 33 seconds, NEVER CANCEL, set timeout 120+ seconds

# Test the build
echo 'print("Hello, MicroPython!")' | ./build-standard/micropython
```

## Running Tests

```bash
# Use CI script for comprehensive testing
source tools/ci.sh

# Run minimal tests (fastest validation)
ci_unix_minimal_build  # If not already built
ci_unix_minimal_run_tests  # Takes 1-5 minutes, NEVER CANCEL, timeout 30+ minutes

# Run standard tests
ci_unix_standard_run_tests  # Takes 5-15 minutes, NEVER CANCEL, timeout 30+ minutes

# Run coverage tests (most comprehensive)
ci_unix_coverage_setup  # Install test dependencies
ci_unix_coverage_build
ci_unix_coverage_run_tests  # Takes 10-15 minutes, NEVER CANCEL, timeout 30+ minutes
```

## Code Formatting and Quality

**ALWAYS run formatting and linting before committing or CI will fail:**

```bash
# Install uncrustify for C code formatting
source tools/ci.sh
ci_c_code_formatting_setup

# Check C code formatting
ci_c_code_formatting_run

# Install and setup pre-commit hooks (recommended)
pip install pre-commit
pre-commit install --hook-type pre-commit --hook-type commit-msg

# Run pre-commit manually on all files
pre-commit run --all-files

# Python code is checked with ruff (runs in CI)
```

## Building Different Ports

All ports require mpy-cross to be built first.

### Unix Port (Development/Testing)
```bash
cd ports/unix
make submodules  # Required once, 6 seconds, NEVER CANCEL
make VARIANT=minimal    # Minimal build, 6 seconds
make VARIANT=standard   # Standard build (default), 33 seconds  
make VARIANT=coverage   # Coverage build for testing
./build-standard/micropython  # Run the interpreter
```

### STM32 Port (Embedded ARM)
```bash
cd ports/stm32  
make submodules  # Required once, 13 seconds, NEVER CANCEL
make BOARD=PYBV11  # Build for PyBoard v1.1, 63 seconds, NEVER CANCEL, timeout 180+ seconds
# Other boards: PYBV10, PYBD_SF2, NUCLEO_F401RE, STM32F4DISC, etc.
# See ports/stm32/boards/ for all available boards
```

### RP2 Port (Raspberry Pi Pico)
```bash
cd ports/rp2
make submodules  # Initializes pico-sdk
make BOARD=RPI_PICO  # Default board
make BOARD=RPI_PICO_W  # Pico W with WiFi
```

## Validation Scenarios

**ALWAYS test actual functionality after making changes - starting/stopping is NOT sufficient:**

### Basic Functionality Test
```bash
cd ports/unix
# Test basic Python functionality
echo 'print(1 + 1)' | ./build-standard/micropython
# Expected output: 2

# Test import system
echo 'import sys; print(sys.version)' | ./build-standard/micropython
# Expected output: MicroPython version info

# Test file execution
echo 'print("File test")' > /tmp/test.py
./build-standard/micropython /tmp/test.py
# Expected output: File test
```

### Module and Library Test
```bash
# Test built-in modules
echo 'import json; print(json.dumps({"test": 123}))' | ./build-standard/micropython

# Test mathematical operations
echo 'import math; print(math.sqrt(16))' | ./build-standard/micropython
```

## Repository Structure and Navigation

Key directories and their purposes:
- `py/` - Core Python implementation (compiler, runtime, core library)
- `mpy-cross/` - MicroPython cross-compiler (build this first)
- `ports/unix/` - Unix/Linux port (primary development platform)
- `ports/stm32/` - STM32 microcontroller port
- `ports/rp2/` - Raspberry Pi RP2040 port
- `tests/` - Comprehensive test suite
- `tools/` - Development tools and CI scripts
- `docs/` - Documentation source (Sphinx/reStructuredText)
- `extmod/` - Extended modules (non-core) in C
- `lib/` - External dependencies as git submodules
- `examples/` - Example Python scripts

## Common Commands Reference

```bash
# Repository root listing
ls -la
# Output: py/ mpy-cross/ ports/ tests/ tools/ docs/ extmod/ lib/ examples/ 
#         README.md CONTRIBUTING.md CODECONVENTIONS.md LICENSE

# Check MicroPython version after build
./ports/unix/build-standard/micropython -c "import sys; print(sys.version)"

# Check submodule status
git submodule status

# CI script functions (source tools/ci.sh first)
ci_unix_minimal_build
ci_unix_standard_build  
ci_unix_coverage_build
ci_c_code_formatting_setup
ci_c_code_formatting_run
```

## CI and GitHub Actions

The repository uses extensive CI defined in `.github/workflows/`:
- `ports_unix.yml` - Tests Unix port with multiple configurations
- `code_formatting.yml` - Checks C code formatting with uncrustify
- `ruff.yml` - Checks Python code with ruff
- Multiple port-specific workflows for STM32, ESP32, RP2, etc.

CI uses functions from `tools/ci.sh`. Always test your changes using the same CI functions to ensure they will pass.

## Dependencies and Environment

### Required for all builds:
- Python 3.3+ (available as `python3`)
- GCC and build tools: `build-essential libffi-dev git pkg-config`
- GNU Make or gmake on BSD systems

### Port-specific dependencies:
- ARM cross-compiler: `gcc-arm-none-eabi libnewlib-arm-none-eabi`
- Some ports use CMake in addition to Make

### Development tools:
- uncrustify (for C code formatting)
- pre-commit (for automated formatting checks)
- ruff (for Python code checking, runs in CI)

## Performance Notes

Typical build times (add 50% buffer for timeouts):
- Clean mpy-cross build: 15 seconds
- Clean Unix standard build: 33 seconds  
- Clean STM32 PYBV11 build: 63 seconds
- Submodule initialization: 5-15 seconds
- Test runs: 1-15 minutes depending on scope

## Troubleshooting

If builds fail:
1. Ensure mpy-cross is built first
2. Check that all required dependencies are installed
3. Run `make submodules` in the port directory
4. For ARM ports, verify cross-compiler is in PATH
5. Check CI logs for the same failure pattern

Build artifacts are in `build-*` directories within each port. Clean with `make clean`.

## Working with Tests

The test system expects specific binary locations:
- Unix tests use `../ports/unix/build-standard/micropython`
- Minimal tests use `../ports/unix/build-minimal/micropython`
- Cross-compiler at `../mpy-cross/build/mpy-cross`

Always build the appropriate variant before running tests.