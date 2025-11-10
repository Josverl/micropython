# Sleep Test Implementation Summary

## Overview
This implementation provides comprehensive tests for `machine.lightsleep()` and `machine.deepsleep()` that can be run against connected MicroPython hardware using the MicroPython test framework.

## Files Created

### Research and Documentation
1. **docs/sleep_test_research.md** (260 lines)
   - Comprehensive research on test framework patterns
   - Platform capability analysis (ESP32, RP2, etc.)
   - Wake source documentation (timer, GPIO, EXT0, EXT1, touchpad, ULP)
   - Implementation challenges and solutions
   - Testing strategies and best practices

### Test Files
2. **tests/extmod_hardware/machine_lightsleep.py** (168 lines)
   - Timer-based wake tests with multiple durations
   - State preservation validation
   - Variable and object persistence tests
   - Multiple consecutive sleep tests
   - Platform-agnostic implementation

3. **tests/extmod_hardware/machine_deepsleep.py** (244 lines)
   - Reset cause detection API tests
   - State file management utilities
   - Manual test examples with documentation
   - Platform-specific tests (ESP32 wake_reason)
   - Multi-stage test pattern examples

4. **tests/extmod_hardware/machine_lightsleep_gpio.py** (224 lines)
   - ESP32 EXT0 wake implementation
   - RP2 GPIO IRQ wake implementation
   - Hardware connection verification
   - Threading-based wake triggering
   - Manual test documentation

### Configuration Updates
5. **tests/target_wiring/esp32.py** (updated)
   - Added `sleep_wake_pin = 2`
   - Added `sleep_trigger_pin = 15`
   - Documented required connections

6. **tests/target_wiring/rp2.py** (updated)
   - Added `sleep_wake_pin = 2`
   - Added `sleep_trigger_pin = 3`
   - Documented required connections

### Documentation Updates
7. **tests/README.md** (updated with 63 new lines)
   - Added comprehensive sleep testing section
   - Usage examples for different test types
   - Hardware connection requirements
   - Reference links to detailed documentation

### Example Scripts
8. **tests/run_sleep_tests_example.py** (76 lines)
   - Interactive test runner
   - Hardware connection verification prompts
   - Step-by-step test execution
   - Helpful guidance and prerequisites

## Test Coverage

### Timer-Based Tests (No Hardware Required)
✅ Short sleep (100ms)
✅ Medium sleep (500ms)  
✅ Long sleep (1000ms)
✅ Multiple consecutive sleeps
✅ Zero-duration sleep
✅ State preservation across sleep
✅ Variable persistence validation
✅ Time advancement verification

### GPIO Wake Tests (Requires Pin Loopback)
✅ ESP32 EXT0 wake configuration
✅ ESP32 GPIO wake trigger
✅ RP2 IRQ-based wake
✅ Pin state verification
✅ Threading-based trigger coordination

### Deepsleep Tests (Informational)
✅ Reset cause API verification
✅ DEEPSLEEP_RESET constant availability
✅ State file utilities
✅ Multi-stage test patterns
✅ Manual test examples
✅ ESP32 wake_reason support

## Key Features

### 1. Platform Independence
- Auto-detection of platform capabilities
- Automatic test skipping on unsupported platforms
- Platform-specific implementations where needed
- Consistent unittest framework usage

### 2. Timing Tolerance
- 25% timing tolerance for all duration tests
- Accounts for interrupts and system load
- Platform-specific adjustments where needed
- Realistic expectations for embedded systems

### 3. Hardware Flexibility
- Basic tests require no external connections
- GPIO tests use documented loopback connections
- Configuration via target_wiring files
- Clear documentation of requirements

### 4. Test Patterns
- unittest.TestCase inheritance
- setUp/tearDown methods for resource management
- skipTest for conditional test execution
- Comprehensive assertion checks

### 5. Documentation
- Inline test documentation
- Separate research document
- Updated main test README
- Example scripts with guidance

## Usage Examples

### Basic Timer Tests (No Hardware)
```bash
# Install unittest on device
mpremote mip install unittest

# Run lightsleep tests
./run-tests.py -t /dev/ttyACM0 tests/extmod_hardware/machine_lightsleep.py

# Run deepsleep tests
./run-tests.py -t /dev/ttyACM0 tests/extmod_hardware/machine_deepsleep.py
```

### GPIO Wake Tests (With Loopback)
```bash
# ESP32: Connect GPIO2 to GPIO15
# RP2: Connect GPIO2 to GPIO3

# Run GPIO wake tests
./run-tests.py -t /dev/ttyACM0 tests/extmod_hardware/machine_lightsleep_gpio.py
```

### Interactive Example
```bash
# Run interactive test script
cd tests
./run_sleep_tests_example.py /dev/ttyACM0
```

## Test Design Decisions

### Why unittest?
- Consistent with existing extmod_hardware tests
- Provides setUp/tearDown for resource management
- Supports conditional test skipping
- Clear pass/fail reporting

### Why not .exp files?
- Sleep timing varies too much for exact output matching
- unittest allows tolerance ranges in assertions
- More flexible for platform differences
- Better diagnostic output on failure

### Why separate files?
- Modular testing (timer vs GPIO vs deepsleep)
- Different hardware requirements
- Easier to maintain and extend
- Clear separation of concerns

### Why state files for deepsleep?
- Deepsleep causes device reset
- Need to track test progress across reboots
- Filesystem persists through reset
- Enables multi-stage test patterns

## Deepsleep Testing Challenges

### Challenge: Device resets after deepsleep
**Solution**: Use state files to track progress across reboots

### Challenge: Serial disconnect
**Solution**: Test framework handles reconnection; tests check reset_cause()

### Challenge: RAM cleared
**Solution**: Use filesystem or RTC memory for persistence

### Challenge: Automation difficulty  
**Solution**: Provide manual test examples and documentation

## Platform-Specific Notes

### ESP32
- Supports EXT0, EXT1, timer, touchpad, ULP wake sources
- wake_reason() available after wake
- reset_cause() detects DEEPSLEEP_RESET
- RTC memory can persist through deepsleep

### RP2
- GPIO IRQ wake supported
- Thread-safe lightsleep implementation
- USB serial may disconnect during sleep
- Additional tests in tests/ports/rp2/

### Unix Port
- Sleep functions stubbed
- Tests skipped automatically
- Used for syntax validation

## Future Enhancements

### Potential Additions
1. **More wake sources**: Touchpad, ULP, EXT1 multi-pin
2. **RTC memory tests**: State persistence in deepsleep
3. **Power consumption**: Monitor current during sleep
4. **External reset**: Test wake via reset pin
5. **More platforms**: Add nrf, samd, stm32 configurations

### Testing Infrastructure
1. **Automated hardware setup**: Robot framework integration
2. **Multi-device tests**: Test wake from external device
3. **Timing measurements**: More precise duration validation
4. **Stress tests**: Repeated sleep/wake cycles

## Validation

### Syntax Checking
All Python files validated with:
- Python AST parser
- py_compile module
- No syntax errors found

### Consistency Checking
- Follows existing test patterns
- Matches extmod_hardware style
- Uses standard unittest conventions
- Consistent with target_wiring pattern

### Documentation
- Comprehensive research document
- Updated main README
- Inline test documentation
- Example scripts provided

## Conclusion

This implementation provides a solid foundation for testing machine.lightsleep and machine.deepsleep across MicroPython platforms. The tests are:

- **Practical**: Run on real hardware with minimal setup
- **Comprehensive**: Cover timer, state, and GPIO wake scenarios
- **Documented**: Clear guidance and examples
- **Maintainable**: Follow established patterns
- **Extensible**: Easy to add platform-specific tests

The combination of timer-based tests (no hardware) and GPIO tests (with loopback) provides good coverage while keeping hardware requirements minimal.
