#!/usr/bin/env python3
"""
Example script demonstrating how to use the MicroPython RFC2217 bridge.

This script connects to a running mp_rfc2217_bridge.py server and demonstrates:
1. Connecting to the RFC2217 server
2. Entering raw REPL mode
3. Executing Python code
4. Exiting raw REPL mode

Prerequisites:
    - mp_rfc2217_bridge.py server running on localhost:2217
    - pyserial installed (pip install pyserial)

Usage:
    python3 mp_rfc2217_example.py
"""

import serial
import time


def read_until(ser, end_str, timeout=5):
    """Read until we see end_str or timeout."""
    data = b''
    end_time = time.time() + timeout
    while time.time() < end_time:
        if ser.in_waiting:
            chunk = ser.read(ser.in_waiting)
            data += chunk
            if end_str in data:
                return data
        time.sleep(0.01)
    return data


def main():
    print("MicroPython RFC2217 Bridge - Example Client")
    print("=" * 60)
    
    # Connect to the RFC2217 server
    print("\n[1] Connecting to RFC2217 server at localhost:2217...")
    try:
        ser = serial.serial_for_url(
            'rfc2217://localhost:2217',
            baudrate=115200,
            timeout=2
        )
        print("✓ Connected successfully")
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        print("\nMake sure mp_rfc2217_bridge.py is running:")
        print("  python3 tools/mp_rfc2217_bridge.py -p 2217 ./micropython")
        return 1
    
    # Enter raw REPL mode
    print("\n[2] Entering raw REPL mode...")
    ser.write(b'\r\x03')  # Interrupt any running code
    time.sleep(0.2)
    
    # Flush input
    while ser.in_waiting > 0:
        ser.read(ser.in_waiting)
        time.sleep(0.05)
    
    ser.write(b'\r\x01')  # Enter raw REPL
    data = read_until(ser, b'raw REPL; CTRL-B to exit\r\n>', timeout=5)
    
    if not data.endswith(b'raw REPL; CTRL-B to exit\r\n>'):
        print(f"✗ Failed to enter raw REPL. Got: {repr(data)}")
        ser.close()
        return 1
    
    print("✓ Entered raw REPL mode")
    
    # Execute some Python code
    print("\n[3] Executing Python commands...")
    
    commands = [
        ("Print message", b'print("Hello from RFC2217 client!")'),
        ("Simple math", b'result = 42 * 2\nprint(f"Answer: {result}")'),
        ("List operations", b'items = [1, 2, 3, 4, 5]\nprint(sum(items))'),
        ("System info", b'import sys\nprint(f"Platform: {sys.platform}")'),
    ]
    
    for description, code in commands:
        print(f"\n   {description}:")
        print(f"   Code: {code.decode('utf-8')}")
        
        # Send command with Ctrl-D to execute
        ser.write(code + b'\x04')
        
        # Read response
        data = read_until(ser, b'\x04>', timeout=3)
        
        # Extract the output (between OK and \x04)
        if b'OK' in data:
            output = data.split(b'OK', 1)[1].split(b'\x04')[0]
            print(f"   Output: {output.decode('utf-8', errors='replace').strip()}")
            print("   ✓ Success")
        else:
            print(f"   ✗ Unexpected response: {repr(data)}")
    
    # Exit raw REPL
    print("\n[4] Exiting raw REPL mode...")
    ser.write(b'\x02')  # Ctrl-B to exit raw REPL
    time.sleep(0.3)
    
    data = read_until(ser, b'>>>', timeout=2)
    if b'>>>' in data:
        print("✓ Exited to friendly REPL")
    else:
        print("⚠ Could not confirm exit")
    
    # Close connection
    print("\n[5] Closing connection...")
    ser.close()
    print("✓ Connection closed")
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)
    
    return 0


if __name__ == '__main__':
    exit(main())
