# MicroPython Copilot Instructions

## Project Overview

MicroPython is an implementation of Python 3 for microcontrollers and embedded systems. This repository contains:

- **py/** - Core Python implementation (compiler, runtime, core library)
- **mpy-cross/** - Cross-compiler for bytecode generation
- **ports/** - Platform-specific code for 20+ different architectures
- **extmod/** - Additional modules implemented in C
- **lib/** - External dependencies (submodules)
- **tests/** - Test framework and test scripts
- **docs/** - Documentation in Sphinx reStructuredText
- **tools/** - Various development utilities (Python tools, with some utilities written in MicroPython)

## Multi-Port Architecture

MicroPython supports multiple hardware platforms (ports) found in the `ports/` directory:

### Tier 1 Ports (Most Active)
- **unix** - Linux, BSD, macOS, WSL (primary development/testing port)
- **windows** - Microsoft Windows
- **stm32** - STMicroelectronics STM32 MCUs
- **esp32** - Espressif ESP32 SoCs
- **rp2** - Raspberry Pi RP2040/RP2350
- **samd** - Microchip SAMD21/SAMD51
- **mimxrt** - NXP i.MX RT

### Tier 2 & 3 Ports
See `README.md` for complete list including esp8266, nrf, zephyr, webassembly, and others.

**Important**: While most development work uses the **unix port**, code changes must work across all relevant platforms. Always consider cross-platform compatibility, especially for core (`py/`) and extended modules (`extmod/`).

## Build Instructions

### Building the Unix Port (Primary Development Platform)

1. **Prerequisites** (Ubuntu/Debian):
   ```bash
   apt install build-essential git python3 pkg-config libffi-dev
   ```

2. **Build cross-compiler** (first time only):
   ```bash
   cd mpy-cross
   make
   ```

3. **Build unix port**:
   ```bash
   cd ports/unix
   make submodules
   make
   ```

4. **Run the executable**:
   ```bash
   ./build-standard/micropython
   ```

### Building Other Ports

Each port has specific build requirements. Always check the port's README:
- Most use `make` (some use `cmake` like esp32 and rp2)
- Many require specific toolchains (e.g., ARM cross-compiler for embedded targets)
- Always run `make submodules` first to fetch dependencies

## Testing

### Unix Port Tests

Run tests from the `ports/unix` directory:

```bash
# Run all tests
make test

# Run specific test patterns
make test//int              # Tests matching "int"
make test/ports/unix        # Unix-specific tests

# Re-run failed tests
make test-failures

# Clean up test artifacts
make clean-failures
```

### Other Ports

Most ports have their own test targets. Check port-specific documentation.

## Code Formatting and Style

### C Code

- **Auto-formatter**: Use `tools/codeformat.py` (wraps uncrustify v0.71 or v0.72)
- Run before committing:
  ```bash
  tools/codeformat.py [files...]
  ```
- **Style Guidelines**:
  - Use 4 spaces, no tabs
  - Braces on same line as statement
  - Use `// ` comments (not `/* */`)
  - Names: `underscore_case` for functions/variables, `CAPS_WITH_UNDERSCORE` for macros
  - Public APIs: prefix with `mp_` or `MP_`
  - Use `mp_int_t`/`mp_uint_t` for most integers (machine-word sized)
  - Memory allocation: use `m_new`, `m_renew`, `m_del` macros from `py/misc.h`

### Python Code

- **Auto-formatter**: Use `ruff format` (line length: 99)
- Run before committing:
  ```bash
  ruff format [files...]
  ```
- **Style Guidelines**:
  - Follow PEP 8
  - Module names: short, lowercase (e.g., `pyb`, `stm`)
  - Class names: CamelCase with uppercase abbreviations (e.g., `I2C`)
  - Functions: lowercase with underscores (e.g., `mem_read`)
  - Constants: UPPERCASE with underscores

### Pre-commit Hooks

Install pre-commit for automatic checking:
```bash
pre-commit install --hook-type pre-commit --hook-type commit-msg
```

### Spell Checking

Run codespell before submitting PRs:
```bash
pip install codespell tomli
codespell
```

## Commit Conventions

- **Format**: `path/to/file: Short description ending with period.`
- **Examples**:
  - `py/objstr: Add splitlines() method.`
  - `docs/machine: Fix typo in reset() description.`
  - `ports: Switch to use lib/foo instead of duplicated code.`
- First line max 72 characters
- Add detailed description after blank line if needed (75 chars/line)
- **Always sign off**: Use `git commit -s` to add "Signed-off-by:" line

## MicroPython-Specific Design Principles

### Memory Optimization (Critical!)

MicroPython runs on constrained devices (as small as 256KB flash + 16KB RAM). **Always minimize RAM and flash usage**:

1. **Minimize Firmware Growth**:
   - Keep code size small - every byte counts on MCUs
   - Avoid adding unnecessary features or dependencies
   - Use compact data structures
   - Consider using `#if MICROPY_PY_*` config guards for optional features

2. **RAM Efficiency**:
   - Prefer local variables (stored on stack) over globals (stored in heap dict)
   - Short variable names consume less RAM (identifiers stored in RAM)
   - Use `const()` with underscore prefix for true constants: `_Y = const(2)`
   - Avoid code that runs on import (consumes RAM before compilation of other modules)
   - Minimize object creation/destruction (reduces heap fragmentation)

3. **Frozen Bytecode**:
   - Python modules can be frozen into firmware to save RAM
   - Use `.mpy` precompiled bytecode to avoid parsing overhead
   - See `docs/reference/manifest.rst` for details

4. **Integer Types**:
   - Use `mp_int_t`/`mp_uint_t` for most integers (portable across 16/32/64-bit)
   - Use `size_t` for byte counts/object sizes
   - Avoid assuming int is 32-bit (may be 16-bit on some platforms)

### CPython Compatibility

**Strive for CPython compatibility where possible**, but MicroPython prioritizes:
1. Small firmware size
2. Efficient execution on microcontrollers
3. Subset of Python 3 functionality

**Design Decisions** (document these when deviating from CPython):
- Some Python 3 features are omitted or simplified for size/efficiency
- Module APIs may be subsets of their CPython equivalents
- See `docs/differences/python_*.rst` files for version-specific CPython differences
- See `docs/develop/optimizations.rst` for optimization strategies

### Cross-Platform Compatibility

- Core changes (`py/`, `extmod/`) must work on all platforms
- Use portable C code (avoid platform-specific assumptions)
- Test on unix port, but consider implications for embedded targets:
  - Limited RAM/flash
  - Different toolchains (GCC, Clang, MSVC, ARM compiler)
  - Different architectures (ARM, x86, RISC-V, MIPS, etc.)
  - No OS features on bare-metal ports

## Documentation

- **Location**: `docs/` directory (Sphinx reStructuredText)
- **Build docs**:
  ```bash
  cd docs
  make html
  ```
- Update documentation when changing:
  - Public APIs
  - Module interfaces
  - Build procedures
- Follow existing conventions:
  - Use `:func:\`foo\`` for function cross-refs
  - Use `:class:\`Foo\`` for class cross-refs
  - Use `:mod:\`module\`` for module cross-refs

## Security

- Never commit secrets or credentials
- Sanitize user input appropriately
- Be mindful of buffer overflows in C code
- Follow secure coding practices for embedded systems

## Common Pitfalls to Avoid

1. **Don't** add code that significantly increases firmware size without justification
2. **Don't** use CPython-only features without checking MicroPython compatibility
3. **Don't** assume 32-bit integers or 32-bit pointers
4. **Don't** add dependencies without checking impact on all ports
5. **Don't** forget to run code formatter before committing
6. **Don't** remove or modify working code unless absolutely necessary
7. **Don't** break existing tests (check with `make test` in unix port)

## Useful Resources

- [Documentation](https://docs.micropython.org/)
- [Contributors' Guidelines](https://github.com/micropython/micropython/wiki/ContributorGuidelines)
- [Code Conventions](CODECONVENTIONS.md)
- [Optimization Guide](docs/develop/optimizations.rst)
- [MCU Constraints](docs/reference/constrained.rst)
- [GitHub Discussions](https://github.com/micropython/micropython/discussions)
- [Discord](https://discord.gg/RB8HZSAExQ)

## Summary for Copilot Agent

When working on this repository:

1. **Default to unix port** for development/testing
2. **Keep changes minimal** - firmware size matters
3. **Maintain cross-platform compatibility** - consider all ports
4. **Follow code conventions** - run formatters before committing
5. **Test thoroughly** - use `make test` in ports/unix
6. **Document changes** - especially for public APIs
7. **Optimize for MCUs** - prefer efficiency over features
8. **Stay CPython-compatible** when possible without compromising size/efficiency
