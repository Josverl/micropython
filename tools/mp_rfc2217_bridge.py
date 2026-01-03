#!/usr/bin/env python3
#
# This file is part of the MicroPython project, http://micropython.org/
#
# The MIT License (MIT)
#
# Copyright (c) 2026 Jos Verlinde

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
MicroPython RFC 2217 Bridge

This tool exposes a MicroPython unix REPL as an RFC 2217 server, allowing remote
access to the REPL over a network connection by mpremote and other tools.

Usage:
    mp_rfc2217_bridge.py [options] [MICROPYTHON_PATH]

Example:
    mp_rfc2217_bridge.py
    mp_rfc2217_bridge.py ./ports/unix/build-standard/micropython
    mp_rfc2217_bridge.py -p 2217 -v ./micropython

Then connect with:
    mpremote connect rfc2217://localhost:2217
    or
    pyserial-miniterm rfc2217://localhost:2217 115200
"""

import argparse
import logging
import os
import pty
import select
import socket
import subprocess
import sys
import threading
import time
import tty

import serial.rfc2217

# Constants for mpremote compatibility
MPREMOTE_SOFT_REBOOT = b"soft reboot\r\n"
# Raw REPL soft reboot response that mpremote expects (mimics real MCU behavior)
MPREMOTE_RAW_REPL_SOFT_REBOOT = b"OK\r\nMPY: soft reboot\r\nraw REPL; CTRL-B to exit\r\n>"

# Bridge timing constants (in seconds)
MP_BRIDGE_RAW_REPL_ENTRY_DELAY = 0.05  # Delay after sending Ctrl-A to enter raw REPL
MP_BRIDGE_BANNER_READ_TIMEOUT = 0.2  # Timeout for reading banner
MP_BRIDGE_PROCESS_RESTART_DELAY = 0.1  # Delay after restarting process
MP_BRIDGE_POLL_INTERVAL = 1  # Status line poll interval
MP_BRIDGE_READ_TIMEOUT = 0.01  # Read timeout for PTY (10ms for responsiveness)
MP_BRIDGE_READ_BUFFER_SIZE = 4096  # Read buffer size for PTY


class VirtualSerialPort:
    """
    A virtual serial port that wraps a PTY file descriptor.
    This simulates a serial port interface for the RFC 2217 PortManager.
    Emulates soft reboot behavior for compatibility with mpremote.
    """

    def __init__(
        self,
        fd: int,
        timeout: float = MP_BRIDGE_READ_TIMEOUT,
        restart_callback=None,
    ):
        """Initialize with a PTY file descriptor.

        Args:
            fd: File descriptor for the PTY master
            timeout: Read timeout in seconds
            restart_callback: Optional callback to restart the process for soft reboot
        """
        self.fd = fd
        self.process = None  # Set externally after process creation
        self.timeout = timeout
        self.in_waiting = 0
        self.restart_callback = restart_callback
        self._in_raw_repl = False
        self._pending_reboot_output = b""
        # Simulate serial port settings
        self.baudrate = 115200
        self.bytesize = 8
        self.parity = "N"
        self.stopbits = 1
        self.rtscts = False
        self.dsrdtr = False
        self.xonxoff = False
        # Control lines (simulated, always active for subprocess)
        self.dtr = True
        self.rts = True
        self.cts = True
        self.dsr = True
        self.ri = False
        self.cd = True
        self.break_condition = False
        self._settings_backup = None
        self.name = "MicroPython REPL (subprocess)"
        self._check_buffer_lock = threading.Lock()
        self._closed = False

    def read(self, size=MP_BRIDGE_READ_BUFFER_SIZE):
        """Read up to size bytes from the PTY."""
        # If we have pending reboot output, return that first
        if self._pending_reboot_output:
            chunk = self._pending_reboot_output[:size]
            self._pending_reboot_output = self._pending_reboot_output[size:]
            return chunk

        if self._closed:
            return b""

        try:
            ready, _, _ = select.select([self.fd], [], [], self.timeout)
            if ready:
                # Always read larger chunks for efficiency
                data = os.read(self.fd, MP_BRIDGE_READ_BUFFER_SIZE)
                # Detect raw REPL entry from response
                if b"raw REPL; CTRL-B to exit" in data:
                    self._in_raw_repl = True
                # Detect raw REPL exit
                elif b">>>" in data and self._in_raw_repl:
                    self._in_raw_repl = False
                return data
        except (OSError, ValueError):
            self._closed = True
        return b""

    def write(self, data):
        """Write data to the PTY."""
        if self._closed:
            return 0

        # Track raw REPL state based on client commands
        # Ctrl-A (0x01) enters raw REPL, Ctrl-B (0x02) exits raw REPL
        if b"\x01" in data:
            self._in_raw_repl = True
        elif b"\x02" in data:
            self._in_raw_repl = False

        logging.getLogger("virtualserial").debug(f"write({len(data)} bytes): {data!r}")
        # When the process exits (from Ctrl-D or any other reason), the reader
        # thread detects it and handles the restart automatically.

        try:
            return os.write(self.fd, data)
        except (OSError, ValueError):
            self._closed = True
            return 0

    def update_in_waiting(self):
        """Update the number of bytes waiting to be read."""

        with self._check_buffer_lock:
            if self._closed:
                self.in_waiting = 0
                return

            # Non-blocking check - no timeout wait
            try:
                ready, _, _ = select.select([self.fd], [], [], 0)
                self.in_waiting = 1 if ready else 0
            except (OSError, ValueError):
                self._closed = True
                self.in_waiting = 0

    def get_settings(self):
        """Get current serial port settings."""
        return {
            "baudrate": self.baudrate,
            "bytesize": self.bytesize,
            "parity": self.parity,
            "stopbits": self.stopbits,
            "rtscts": self.rtscts,
            "dsrdtr": self.dsrdtr,
            "xonxoff": self.xonxoff,
        }

    def apply_settings(self, settings):
        """Apply serial port settings (stored but not actually used)."""
        self.baudrate = settings.get("baudrate", self.baudrate)
        self.bytesize = settings.get("bytesize", self.bytesize)
        self.parity = settings.get("parity", self.parity)
        self.stopbits = settings.get("stopbits", self.stopbits)
        self.rtscts = settings.get("rtscts", self.rtscts)
        self.dsrdtr = settings.get("dsrdtr", self.dsrdtr)
        self.xonxoff = settings.get("xonxoff", self.xonxoff)

    def reset_input_buffer(self):
        """Reset input buffer (no-op for subprocess)."""
        pass

    def reset_output_buffer(self):
        """Reset output buffer (no-op for subprocess)."""
        pass

    def send_break(self, duration=0.25):
        """Send break condition (no-op for subprocess)."""
        pass

    def flush(self):
        """Flush output buffer (no-op for PTY mode)."""
        pass


class Redirector:
    """
    Redirects data between a network socket and a virtual serial port (subprocess).
    Based on pyserial's rfc2217_server.py example.
    """

    def __init__(self, virtual_serial, socket_conn, debug=False):
        self.serial = virtual_serial
        self.socket = socket_conn
        self._write_lock = threading.Lock()
        # Note: PortManager expects a connection with write() method - Redirector provides this
        self.rfc2217 = serial.rfc2217.PortManager(
            self.serial,
            self,  # type: ignore[arg-type]
            logger=logging.getLogger("rfc2217.server") if debug else None,
        )
        self.log = logging.getLogger("redirector")
        self.alive = False

    def statusline_poller(self):
        """Poll for modem status line changes."""
        self.log.debug("status line poll thread started")
        while self.alive:
            time.sleep(MP_BRIDGE_POLL_INTERVAL)
            self.rfc2217.check_modem_lines()
        self.log.debug("status line poll thread terminated")

    def shortcircuit(self):
        """Connect the subprocess to the TCP port by copying data bidirectionally."""
        self.alive = True
        self.thread_read = threading.Thread(target=self.reader)
        self.thread_read.daemon = True
        self.thread_read.name = "subprocess->socket"
        self.thread_read.start()
        self.thread_poll = threading.Thread(target=self.statusline_poller)
        self.thread_poll.daemon = True
        self.thread_poll.name = "status line poll"
        self.thread_poll.start()
        self.writer()

    def reader(self):
        """Loop forever and copy subprocess output -> socket."""
        self.log.debug("reader thread started")
        while self.alive:
            try:
                # Check if process has exited (e.g., from Ctrl-D)
                if hasattr(self.serial, "process") and self.serial.process:
                    if self.serial.process.poll() is not None:
                        self.log.info(
                            "MicroPython process exited - performing auto-restart (soft reboot)"
                        )

                        # Remember if we were in raw REPL before restart
                        was_in_raw_repl = getattr(self.serial, "_in_raw_repl", False)
                        self.log.debug(f"was_in_raw_repl = {was_in_raw_repl}")

                        # Only send early soft reboot message if NOT in raw REPL
                        # (raw REPL mode sends a complete response after restart)
                        if not was_in_raw_repl:
                            try:
                                self.write(MPREMOTE_SOFT_REBOOT)
                            except:
                                pass

                        # Restart the process
                        if (
                            hasattr(self.serial, "restart_callback")
                            and self.serial.restart_callback
                        ):
                            try:
                                result = self.serial.restart_callback()
                                if result:
                                    self.serial.fd, self.serial.process = result
                                    # Reset state for the new process
                                    self.serial._in_raw_repl = False
                                    self.serial._closed = False
                                    self.log.info("Process restarted successfully")

                                    # Give process time to start and output banner
                                    time.sleep(MP_BRIDGE_PROCESS_RESTART_DELAY)

                                    # Read the banner from the new process (discard it)
                                    banner = b""
                                    try:
                                        ready, _, _ = select.select(
                                            [self.serial.fd], [], [], MP_BRIDGE_BANNER_READ_TIMEOUT
                                        )
                                        if ready:
                                            banner = os.read(self.serial.fd, 4096)
                                            self.log.debug(f"Read banner: {banner!r}")
                                    except Exception as e:
                                        self.log.error(f"Error reading banner: {e}")

                                    # If we were in raw REPL, re-enter it and send expected response
                                    if was_in_raw_repl:
                                        self.log.info(
                                            "Re-entering raw REPL mode after soft reboot"
                                        )
                                        try:
                                            # Send Ctrl-A to enter raw REPL
                                            os.write(self.serial.fd, b"\x01")
                                            time.sleep(MP_BRIDGE_RAW_REPL_ENTRY_DELAY)

                                            # Read and discard the raw REPL response from MicroPython
                                            ready, _, _ = select.select(
                                                [self.serial.fd],
                                                [],
                                                [],
                                                MP_BRIDGE_BANNER_READ_TIMEOUT,
                                            )
                                            if ready:
                                                raw_response = os.read(self.serial.fd, 4096)
                                                self.log.debug(
                                                    f"Raw REPL response: {raw_response!r}"
                                                )

                                            # Send the expected soft reboot response to the client
                                            self.write(
                                                b"".join(
                                                    self.rfc2217.escape(
                                                        MPREMOTE_RAW_REPL_SOFT_REBOOT
                                                    )
                                                )
                                            )
                                            self.serial._in_raw_repl = True
                                        except Exception as e:
                                            self.log.error(f"Error re-entering raw REPL: {e}")
                                            # Fallback: just send the soft reboot message
                                            self.write(
                                                b"".join(self.rfc2217.escape(MPREMOTE_SOFT_REBOOT))
                                            )
                                    else:
                                        # Not in raw REPL, forward the banner to the client
                                        try:
                                            if banner:
                                                self.write(b"".join(self.rfc2217.escape(banner)))
                                        except:
                                            pass
                            except Exception as e:
                                self.log.error(f"Process restart failed: {e}")
                                self.alive = False
                                break
                        else:
                            self.log.error("No restart callback available")
                            self.alive = False
                            break

                        continue

                # Read larger chunks for efficiency - let read() handle the wait
                data = self.serial.read(MP_BRIDGE_READ_BUFFER_SIZE)
                if data:
                    # Escape outgoing data when needed (Telnet IAC (0xff) character)
                    self.write(b"".join(self.rfc2217.escape(data)))
            except socket.error as msg:
                self.log.error("{}".format(msg))
                break
            except Exception as e:
                self.log.error("Reader error: {}".format(e))
                break
        self.alive = False
        self.log.debug("reader thread terminated")

    def write(self, data):
        """Thread-safe socket write with no data escaping."""
        with self._write_lock:
            try:
                self.socket.sendall(data)
            except socket.error:
                self.alive = False

    def writer(self):
        """Loop forever and copy socket -> subprocess input."""
        while self.alive:
            try:
                data = self.socket.recv(1024)
                if not data:
                    break

                # Filter RFC2217 control sequences
                filtered_data = b"".join(self.rfc2217.filter(data))

                if not filtered_data:
                    continue  # No data to write after filtering

                # Write data to serial port (including Ctrl-D)
                # Ctrl-D will cause unix port to exit, which we handle in reader
                self.serial.write(filtered_data)

            except socket.error as msg:
                self.log.error("{}".format(msg))
                break
            except Exception as e:
                self.log.error("Writer error: {}".format(e))
                break
        self.stop()

    def stop(self):
        """Stop copying data."""
        self.log.debug("stopping")
        if self.alive:
            self.alive = False
            if hasattr(self, "thread_read"):
                self.thread_read.join(timeout=1)
            if hasattr(self, "thread_poll"):
                self.thread_poll.join(timeout=1)


def main():
    # Determine default MicroPython path relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_micropython = os.path.join(
        script_dir, "..", "ports", "unix", "build-standard", "micropython"
    )
    default_micropython = os.path.normpath(default_micropython)

    parser = argparse.ArgumentParser(
        description="MicroPython RFC 2217 Bridge - Expose MicroPython REPL via RFC 2217.",
        epilog="""\
NOTE: No security measures are implemented. Anyone can remotely connect
to this service over the network.

Only one connection at once is supported. When the connection is terminated,
it waits for the next connect.

The MicroPython process persists across connections (like a physical MCU).
Use 'mpremote resume' to preserve state between connections.

Examples:
  %(prog)s                           # Use default MicroPython
  %(prog)s -p 2217                   # Use port 2217 (default)
  %(prog)s ./my_micropython          # Use custom MicroPython path
  %(prog)s --cwd /tmp/mp_root        # Use /tmp/mp_root as filesystem root
  %(prog)s -O -O -X heapsize=4M      # Pass options to MicroPython
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "MICROPYTHON_PATH",
        nargs="?",
        default=default_micropython,
        help="Path to the MicroPython executable (default: %(default)s)",
    )

    parser.add_argument(
        "-p",
        "--port",
        type=int,
        help="Local TCP port (default: %(default)s)",
        metavar="PORT",
        default=2217,
    )

    parser.add_argument(
        "-H",
        "--host",
        help="Local host/interface to bind to (default: all interfaces)",
        metavar="HOST",
        default="",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbosity",
        action="count",
        help="Increase verbosity of the bridge (can be given multiple times)",
        default=0,
    )

    # MicroPython-specific arguments that get passed through
    mp_group = parser.add_argument_group(
        "MicroPython options",
        "These options are passed to the MicroPython executable",
    )

    mp_group.add_argument(
        "-O",
        dest="mp_optimize",
        action="count",
        default=0,
        help="Apply bytecode optimizations (can be given multiple times: -O, -OO, -OOO)",
    )

    mp_group.add_argument(
        "-X",
        dest="mp_impl_opts",
        action="append",
        default=[],
        metavar="OPTION",
        help="Implementation-specific options (e.g., -X heapsize=4M, -X emit=native)",
    )

    mp_group.add_argument(
        "--mp-verbose",
        dest="mp_verbose",
        action="count",
        default=0,
        help="MicroPython verbose mode (trace operations); can be given multiple times",
    )

    mp_group.add_argument(
        "--micropython-args",
        help='Additional arguments to pass to MicroPython (e.g., "-i")',
        default="",
        metavar="ARGS",
    )

    mp_group.add_argument(
        "--cwd",
        dest="cwd",
        help="Working directory for MicroPython (used as filesystem root for unix port)",
        default=None,
        metavar="DIR",
    )

    args = parser.parse_args()

    # Validate MicroPython path
    if not os.path.isfile(args.MICROPYTHON_PATH):
        print(f"Error: MicroPython executable not found: {args.MICROPYTHON_PATH}", file=sys.stderr)
        sys.exit(1)

    if not os.access(args.MICROPYTHON_PATH, os.X_OK):
        print(
            f"Error: MicroPython executable is not executable: {args.MICROPYTHON_PATH}",
            file=sys.stderr,
        )
        sys.exit(1)

    # Validate and resolve working directory
    if args.cwd:
        if not os.path.isdir(args.cwd):
            print(f"Error: Working directory does not exist: {args.cwd}", file=sys.stderr)
            sys.exit(1)
        args.cwd = os.path.abspath(args.cwd)

    # Set up logging
    if args.verbosity > 3:
        args.verbosity = 3
    level = (logging.WARNING, logging.INFO, logging.DEBUG, logging.NOTSET)[args.verbosity]
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logging.getLogger("rfc2217").setLevel(level)

    logging.info("MicroPython RFC 2217 Bridge - type Ctrl-C to quit")
    logging.info(f"MicroPython executable: {args.MICROPYTHON_PATH}")
    if args.cwd:
        logging.info(f"MicroPython working directory: {args.cwd}")
    if args.mp_verbose:
        logging.info(f"MicroPython verbosity: -{args.mp_verbose * 'v'}")
    if args.mp_optimize:
        logging.info(f"MicroPython optimization: -{args.mp_optimize * 'O'}")
    if args.mp_impl_opts:
        logging.info(f"MicroPython options: {', '.join(args.mp_impl_opts)}")

    # Create server socket
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        srv.bind((args.host, args.port))
        srv.listen(1)
    except OSError as e:
        logging.error(f"Could not bind to {args.host}:{args.port}: {e}")
        sys.exit(1)

    bind_addr = args.host or "0.0.0.0"
    logging.info(f"RFC 2217 server listening on {bind_addr}:{args.port}")
    logging.info("Connect with: mpremote connect rfc2217://localhost:{}".format(args.port))
    logging.info("          or: pyserial-miniterm rfc2217://localhost:{} 115200".format(args.port))
    logging.info("Persistent mode: MicroPython process persists across connections")

    # Prepare command for MicroPython (done once, outside connection loop)
    cmd = [args.MICROPYTHON_PATH]
    # Add -v options (can be repeated for more verbosity)
    for _ in range(args.mp_verbose):
        cmd.append("-v")
    # Add -O options (can be repeated for higher optimization)
    for _ in range(args.mp_optimize):
        cmd.append("-O")
    # Add -X options
    for opt in args.mp_impl_opts:
        cmd.extend(["-X", opt])
    # Add any additional micropython args (legacy support)
    if args.micropython_args:
        cmd.extend(args.micropython_args.split())

    # Persistent state - lives across connections
    master_fd = None
    process = None

    def create_micropython_process():
        """Create and return a new MicroPython process with PTY."""
        nonlocal master_fd, process

        # Close old master_fd if it exists
        if master_fd is not None:
            try:
                os.close(master_fd)
            except:
                pass

        # Create a pseudo-terminal for the process
        new_master_fd, new_slave_fd = pty.openpty()

        # Set the terminal to raw mode to avoid line buffering
        try:
            tty.setraw(new_master_fd)
        except:
            pass  # Ignore errors setting raw mode

        process = subprocess.Popen(
            cmd,
            stdin=new_slave_fd,
            stdout=new_slave_fd,
            stderr=new_slave_fd,
            cwd=args.cwd,
            close_fds=False,
        )

        # Close the slave fd in the parent process
        os.close(new_slave_fd)

        master_fd = new_master_fd
        return (new_master_fd, process)

    def restart_micropython():
        """Restart MicroPython process for soft reboot."""
        logging.info(f"Restarting MicroPython for soft reboot: {' '.join(cmd)}")
        return create_micropython_process()

    # Start MicroPython process immediately (persistent mode)
    logging.info(f"Starting MicroPython: {' '.join(cmd)}")
    master_fd, process = create_micropython_process()

    # Create persistent virtual serial port
    virtual_serial = VirtualSerialPort(
        master_fd,
        timeout=0.1,
        restart_callback=restart_micropython,
    )
    virtual_serial.process = process

    try:
        while True:
            try:
                logging.info("Waiting for connection...")
                client_socket, addr = srv.accept()
                logging.info(f"Connected by {addr[0]}:{addr[1]}")
                client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

                # Check if process is still alive, restart if needed
                if process.poll() is not None:
                    logging.info("MicroPython process has exited, restarting...")
                    master_fd, process = create_micropython_process()
                    virtual_serial.fd = master_fd
                    virtual_serial.process = process
                    virtual_serial._closed = False

                # Reset virtual serial state for new connection
                virtual_serial._in_raw_repl = False
                virtual_serial._pending_reboot_output = b""

                # Create redirector for this connection
                r = Redirector(virtual_serial, client_socket, args.verbosity > 0)

                try:
                    r.shortcircuit()
                finally:
                    logging.info("Disconnected")
                    r.stop()
                    client_socket.close()
                    # Note: In persistent mode, we do NOT close master_fd or terminate process
                    # The MicroPython process keeps running for the next connection

            except KeyboardInterrupt:
                sys.stdout.write("\n")
                break
            except socket.error as msg:
                logging.error(str(msg))
            except Exception as e:
                logging.error(f"Unexpected error: {e}", exc_info=args.verbosity > 1)

    finally:
        # Clean up - only on bridge shutdown
        logging.info("Shutting down bridge...")
        if master_fd is not None:
            try:
                os.close(master_fd)
            except:
                pass
        if process and process.poll() is None:
            logging.info("Terminating MicroPython process...")
            process.terminate()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                logging.warning("MicroPython process did not terminate, killing...")
                process.kill()
                process.wait()
        srv.close()
        logging.info("--- exit ---")


if __name__ == "__main__":
    main()
