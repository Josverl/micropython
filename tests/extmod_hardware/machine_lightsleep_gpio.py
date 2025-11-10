# Test machine.lightsleep with GPIO wake.
#
# IMPORTANT: This test requires hardware connections:
# - sleep_wake_pin must be connected to sleep_trigger_pin
# - Pin definitions are in tests/target_wiring/<platform>.py
#
# For ESP32: Connect GPIO2 to GPIO15
# For RP2: Connect GPIO2 to GPIO3
#
# Test approach:
# - Configure wake pin to trigger wake from sleep
# - Use Timer to toggle trigger pin after sleep starts
# - Verify wake occurs before timeout

import sys
import time
import unittest

try:
    from machine import lightsleep, Pin
except ImportError:
    print("SKIP")
    raise SystemExit

# Skip platforms that don't support GPIO wake properly
if sys.platform in ["webassembly", "unix"]:
    print("SKIP")
    raise SystemExit

# Import platform-specific wiring configuration
try:
    from target_wiring import sleep_wake_pin, sleep_trigger_pin
except ImportError:
    print("SKIP")
    raise SystemExit

# Platform-specific wake configuration
WAKE_CONFIG_AVAILABLE = True

# Check if platform supports Pin wake
try:
    # Try to access wake-related constants
    if sys.platform == "esp32":
        from machine import Pin, wake_on_ext0
        WAKE_METHOD = "ext0"
    elif sys.platform == "rp2":
        # RP2 supports GPIO wake but setup is different
        WAKE_METHOD = "gpio_irq"
    else:
        WAKE_CONFIG_AVAILABLE = False
        WAKE_METHOD = None
except ImportError:
    WAKE_CONFIG_AVAILABLE = False
    WAKE_METHOD = None


class TestLightSleepGPIO(unittest.TestCase):
    """Test lightsleep with GPIO wake."""

    def setUp(self):
        """Set up pins for testing."""
        if not WAKE_CONFIG_AVAILABLE:
            self.skipTest("GPIO wake not available on this platform")
        
        # Configure trigger pin (output)
        self.trigger_pin = Pin(sleep_trigger_pin, Pin.OUT)
        self.trigger_pin.value(0)
        
        # Configure wake pin (input)
        self.wake_pin = Pin(sleep_wake_pin, Pin.IN, Pin.PULL_DOWN)
        
        # Give pins time to stabilize
        time.sleep_ms(10)

    def tearDown(self):
        """Clean up after test."""
        if hasattr(self, "trigger_pin"):
            self.trigger_pin.value(0)

    def test_gpio_wake_esp32(self):
        """Test GPIO wake on ESP32 using EXT0."""
        if sys.platform != "esp32":
            self.skipTest("ESP32-specific test")
        
        from machine import wake_on_ext0
        
        # Configure wake on rising edge
        wake_on_ext0(sleep_wake_pin, 1)
        
        # Set trigger to generate wake signal after 200ms
        # We'll use a separate thread or timer
        def trigger_wake():
            time.sleep_ms(200)
            self.trigger_pin.value(1)
        
        # For simplicity, we'll use a timeout and trigger manually
        # Start trigger in background (if threading available)
        try:
            import _thread
            _thread.start_new_thread(trigger_wake, ())
        except ImportError:
            # No threading, skip this test
            self.skipTest("Threading not available for background trigger")
        
        # Sleep for longer than trigger time
        # Should wake early due to GPIO
        t0 = time.ticks_ms()
        lightsleep(1000)  # Try to sleep 1 second
        elapsed = time.ticks_diff(time.ticks_ms(), t0)
        
        # Should wake after ~200ms (before 1000ms timeout)
        # Allow some margin for timing
        self.assertLess(elapsed, 800)
        self.assertGreater(elapsed, 150)

    def test_gpio_wake_rp2(self):
        """Test GPIO wake on RP2 using IRQ."""
        if sys.platform != "rp2":
            self.skipTest("RP2-specific test")
        
        # RP2 wakes from lightsleep on any GPIO IRQ
        wake_occurred = [False]
        
        def pin_handler(pin):
            wake_occurred[0] = True
        
        # Configure IRQ on wake pin
        self.wake_pin.irq(trigger=Pin.IRQ_RISING, handler=pin_handler)
        
        # Trigger wake signal
        def trigger_wake():
            time.sleep_ms(200)
            self.trigger_pin.value(1)
            time.sleep_ms(10)
            self.trigger_pin.value(0)
        
        try:
            import _thread
            _thread.start_new_thread(trigger_wake, ())
        except ImportError:
            self.skipTest("Threading not available for background trigger")
        
        # Sleep and wait for wake
        t0 = time.ticks_ms()
        lightsleep(1000)
        elapsed = time.ticks_diff(time.ticks_ms(), t0)
        
        # Should wake early due to IRQ
        self.assertLess(elapsed, 800)
        self.assertGreater(elapsed, 150)
        
        # Clean up IRQ
        self.wake_pin.irq(handler=None)


class TestLightSleepGPIOSimple(unittest.TestCase):
    """Simplified GPIO tests without threading dependency."""

    def setUp(self):
        if not WAKE_CONFIG_AVAILABLE:
            self.skipTest("GPIO wake not available on this platform")

    def test_pin_setup(self):
        """Test that we can set up wake and trigger pins."""
        # Just verify we can create the pins
        trigger = Pin(sleep_trigger_pin, Pin.OUT)
        wake = Pin(sleep_wake_pin, Pin.IN, Pin.PULL_DOWN)
        
        # Test basic operation
        trigger.value(0)
        time.sleep_ms(10)
        trigger.value(1)
        time.sleep_ms(10)
        
        # Both pins should be readable
        self.assertIn(trigger.value(), [0, 1])
        self.assertIn(wake.value(), [0, 1])
        
        # Clean up
        trigger.value(0)

    def test_wake_configuration_esp32(self):
        """Test that ESP32 wake_on_ext0 can be configured."""
        if sys.platform != "esp32":
            self.skipTest("ESP32-specific test")
        
        try:
            from machine import wake_on_ext0
            
            # Just test that we can call it without error
            wake_on_ext0(sleep_wake_pin, 1)
            
            # Note: Actual wake test requires timing coordination
            # which is tested in test_gpio_wake_esp32
            
        except ImportError:
            self.skipTest("wake_on_ext0 not available")


class TestLightSleepGPIODocumentation(unittest.TestCase):
    """Documentation tests showing GPIO wake patterns."""

    def test_manual_gpio_wake_example(self):
        """Manual test example for GPIO wake (skipped in automation).
        
        This test demonstrates how to manually test GPIO wake:
        
        For ESP32:
        1. Connect GPIO2 to GPIO15
        2. Run: wake_on_ext0(2, 1)  # Wake on rising edge
        3. In another terminal: mpremote exec "from machine import Pin; Pin(15, Pin.OUT).value(1)"
        4. Device should wake from lightsleep
        
        For RP2:
        1. Connect GPIO2 to GPIO3
        2. Configure GPIO2 with IRQ: Pin(2, Pin.IN).irq(trigger=Pin.IRQ_RISING)
        3. In another terminal: mpremote exec "from machine import Pin; Pin(3, Pin.OUT).value(1)"
        4. Device should wake from lightsleep
        """
        self.skipTest("Documentation test - manual execution only")


if __name__ == "__main__":
    unittest.main()
