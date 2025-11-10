#!/usr/bin/env python3
"""
Example script demonstrating how to run sleep tests on connected hardware.

This script shows different ways to test machine.lightsleep and machine.deepsleep
functionality on MicroPython boards.
"""

import subprocess
import sys

def run_test(test_path, device="/dev/ttyACM0"):
    """Run a single test on the specified device."""
    print(f"\n{'='*60}")
    print(f"Running: {test_path}")
    print(f"Device: {device}")
    print(f"{'='*60}\n")
    
    cmd = ["./run-tests.py", "-t", device, test_path]
    result = subprocess.run(cmd, cwd="tests")
    
    return result.returncode == 0


def main():
    """Main function to run sleep tests."""
    device = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyACM0"
    
    print("MicroPython Sleep Test Examples")
    print("=" * 60)
    print(f"Target device: {device}")
    print()
    print("Prerequisites:")
    print("  1. MicroPython board connected and accessible")
    print("  2. unittest module installed on board:")
    print("     $ mpremote mip install unittest")
    print("=" * 60)
    
    # Basic lightsleep tests (no hardware connections needed)
    print("\n\n1. BASIC LIGHTSLEEP TESTS (no wiring required)")
    print("-" * 60)
    success = run_test("extmod_hardware/machine_lightsleep.py", device)
    print(f"Result: {'PASS' if success else 'FAIL'}")
    
    # Deepsleep tests (informational)
    print("\n\n2. DEEPSLEEP TESTS (API verification)")
    print("-" * 60)
    success = run_test("extmod_hardware/machine_deepsleep.py", device)
    print(f"Result: {'PASS' if success else 'FAIL'}")
    
    # GPIO wake tests (requires hardware connections)
    print("\n\n3. GPIO WAKE TESTS (requires pin connections)")
    print("-" * 60)
    print("Required hardware connections:")
    print("  ESP32: GPIO2 <-> GPIO3")
    print("  RP2:   GPIO2 <-> GPIO3")
    print()
    
    response = input("Hardware connected? (y/n): ").strip().lower()
    if response == 'y':
        success = run_test("extmod_hardware/machine_lightsleep_gpio.py", device)
        print(f"Result: {'PASS' if success else 'FAIL'}")
    else:
        print("Skipping GPIO tests (hardware not connected)")
    
    print("\n\n" + "=" * 60)
    print("Test run complete!")
    print("\nFor more information:")
    print("  - See tests/README.md for test framework details")
    print("  - See docs/sleep_test_research.md for implementation details")
    print("  - See tests/target_wiring/*.py for platform pin configurations")
    print("=" * 60)


if __name__ == "__main__":
    main()
