#!/usr/bin/env python3
"""
Test UTF-8 cursor movement and editing operations in MicroPython REPL.
This test needs to be run interactively or with a pseudo-terminal.
"""

import subprocess
import sys
import os


def test_utf8_with_pty():
    """Test UTF-8 editing with pseudo-terminal for proper escape sequence handling"""

    try:
        import pty
        import select
        import termios
    except ImportError:
        print("SKIP: pty module not available")
        return

    micropython = "/home/jos/micropython/ports/unix/build-standard/micropython"

    # Test cases: (input_bytes, expected_output)
    tests = [
        # Test 1: Type café, move left 2 times, backspace should delete 'f'
        {
            "name": "café + 2x left + backspace",
            # Type caf, then é (2 bytes), then left, left, backspace, then newline
            "input": b'caf\xc3\xa9\x1b[D\x1b[D\x08\rprint("test1 done")\r',
            "check": lambda out: "NameError: name 'caé'" in out,  # Should try to execute 'caé'
        },
        # Test 2: Type café, move left 1 time, backspace should delete 'é' (2 bytes)
        {
            "name": "café + 1x left + backspace",
            "input": b'caf\xc3\xa9\x1b[D\x08\rprint("test2 done")\r',
            "check": lambda out: "NameError: name 'caf'" in out,  # Should try to execute 'caf'
        },
        # Test 3: Type 你好, move left, delete should delete '好'
        {
            "name": "你好 + left + delete",
            "input": b'\xe4\xbd\xa0\xe5\xa5\xbd\x1b[D\x1b[3~\rprint("test3 done")\r',
            "check": lambda out: "NameError: name '你'" in out,  # Should try to execute '你'
        },
        # Test 4: Type abc😀def, move left 3 times, backspace should delete 😀
        {
            "name": "abc😀def + 3x left + backspace",
            "input": b'abc\xf0\x9f\x98\x80def\x1b[D\x1b[D\x1b[D\x08\rprint("test4 done")\r',
            "check": lambda out: "NameError: name 'abcdef'"
            in out,  # Should try to execute 'abcdef'
        },
    ]

    for test in tests:
        print(f"\nTest: {test['name']}")

        # Create pseudo-terminal
        master, slave = pty.openpty()

        # Start MicroPython with the slave end of PTY
        proc = subprocess.Popen(
            [micropython], stdin=slave, stdout=slave, stderr=slave, close_fds=True
        )
        os.close(slave)  # Close in parent

        try:
            # Wait a bit for MicroPython to start
            import time

            time.sleep(0.1)

            # Send test input
            os.write(master, test["input"])
            time.sleep(0.2)

            # Read output
            output = b""
            while True:
                r, _, _ = select.select([master], [], [], 0.1)
                if not r:
                    break
                chunk = os.read(master, 4096)
                if not chunk:
                    break
                output += chunk

            # Check result
            output_str = output.decode("utf-8", errors="replace")

            # Look for the expected output in the result
            if test["check"](output_str):
                print(f"  ✓ PASS")
            else:
                print(f"  ✗ FAIL - Output:")
                # Show relevant lines
                lines = output_str.split("\n")
                for i, line in enumerate(lines):
                    if "NameError" in line or ">>>" in line or "test" in line:
                        print(f"    {repr(line)}")

        except Exception as e:
            print(f"  Error: {e}")
        finally:
            proc.terminate()
            proc.wait(timeout=1)
            os.close(master)


if __name__ == "__main__":
    test_utf8_with_pty()
