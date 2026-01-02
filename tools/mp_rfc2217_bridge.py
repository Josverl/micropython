#!/usr/bin/env python3
#
# This file is part of the MicroPython project, http://micropython.org/
#
# The MIT License (MIT)
#
# Copyright (c) 2024 MicroPython Developers
#
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

This tool exposes a MicroPython REPL as an RFC 2217 server, allowing remote
access to the REPL over a network connection without requiring an intermediate
serial port.

Usage:
    mp_rfc2217_bridge.py [options] MICROPYTHON_PATH

Example:
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


class VirtualSerialPort:
    """
    A virtual serial port that wraps a subprocess's stdin/stdout.
    This simulates a serial port interface for the RFC 2217 PortManager.
    Supports lazy initialization to avoid losing the banner during RFC2217 negotiation.
    Emulates soft reboot behavior for compatibility with mpremote.
    """

    def __init__(self, fd_or_process, timeout=1, lazy_start_callback=None, restart_callback=None):
        """Initialize with either a process or a file descriptor.
        
        Args:
            fd_or_process: Either an integer file descriptor (PTY) or a process object
            timeout: Read timeout in seconds
            lazy_start_callback: Optional callback to start the process lazily
            restart_callback: Optional callback to restart the process for soft reboot
        """
        if isinstance(fd_or_process, int):
            # It's a file descriptor (PTY)
            self.fd = fd_or_process
            self.process = None
        else:
            # It's a process wrapper
            self.process = fd_or_process
            self.fd = None
        
        self.timeout = timeout
        self.in_waiting = 0
        self.lazy_start_callback = lazy_start_callback
        self.restart_callback = restart_callback
        self._started = False if lazy_start_callback else True
        self._in_raw_repl = False
        self._pending_reboot_output = b''
        # Simulate serial port settings
        self.baudrate = 115200
        self.bytesize = 8
        self.parity = 'N'
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
    
    def _ensure_started(self):
        """Ensure the process has been started (for lazy initialization)."""
        if not self._started and self.lazy_start_callback:
            self._started = True
            result = self.lazy_start_callback()
            if result:
                self.fd, self.process = result

    def read(self, size=1):
        """Read up to size bytes from the subprocess stdout or PTY."""
        self._ensure_started()
        
        # If we have pending reboot output, return that first
        if self._pending_reboot_output:
            chunk = self._pending_reboot_output[:size]
            self._pending_reboot_output = self._pending_reboot_output[size:]
            return chunk
        
        if self._closed:
            return b''
        
        if self.fd is not None:
            # PTY mode
            try:
                ready, _, _ = select.select([self.fd], [], [], self.timeout)
                if ready:
                    data = os.read(self.fd, size)
                    # Detect raw REPL entry
                    if b'raw REPL; CTRL-B to exit' in data:
                        self._in_raw_repl = True
                    # Detect raw REPL exit
                    elif b'>>>' in data and self._in_raw_repl:
                        self._in_raw_repl = False
                    return data
            except (OSError, ValueError):
                self._closed = True
            return b''
        else:
            # Process mode (old code)
            if not self.process or self.process.poll() is not None:
                return b''

            # Use select to check if data is available with timeout
            ready, _, _ = select.select([self.process.stdout], [], [], self.timeout)
            if ready:
                try:
                    data = os.read(self.process.stdout.fileno(), size)
                    return data
                except OSError:
                    return b''
            return b''

    def write(self, data):
        """Write data to the subprocess stdin or PTY."""
        self._ensure_started()
        
        if self._closed:
            return 0
        
        # Detect Ctrl-D (0x04) in raw REPL mode for soft reboot emulation
        if self._in_raw_repl and b'\x04' in data and self.restart_callback:
            # mpremote sends a standalone Ctrl-D after entering raw REPL to trigger soft reset
            # We need to detect this pattern and emulate the soft reboot
            if data == b'\x04' or data.strip() == b'\x04':
                logging.getLogger('virtualserial').info('Soft reboot requested via Ctrl-D')
                # Trigger restart and queue the soft reboot message
                self._perform_soft_reboot()
                # Return the length to indicate success
                return len(data)
        
        if self.fd is not None:
            # PTY mode
            try:
                return os.write(self.fd, data)
            except (OSError, ValueError):
                self._closed = True
                return 0
        else:
            # Process mode (old code)
            if not self.process or self.process.poll() is not None:
                return 0

            try:
                self.process.stdin.write(data)
                self.process.stdin.flush()
                return len(data)
            except (OSError, BrokenPipeError):
                return 0
    
    def _perform_soft_reboot(self):
        """Perform a soft reboot by restarting the process and queueing expected output."""
        if not self.restart_callback:
            return
        
        logging.getLogger('virtualserial').info('Performing soft reboot emulation...')
        
        # Close current process
        if self.fd is not None:
            try:
                os.close(self.fd)
            except:
                pass
        
        if self.process and self.process.poll() is None:
            try:
                self.process.terminate()
                self.process.wait(timeout=1)
            except:
                if self.process and self.process.poll() is None:
                    try:
                        self.process.kill()
                        self.process.wait()
                    except:
                        pass
        
        # Restart process
        result = self.restart_callback()
        if result:
            self.fd, self.process = result
            # Queue the soft reboot message that mpremote expects
            self._pending_reboot_output = b'OK'
            # Give process a moment to start
            time.sleep(0.1)
            # Queue additional output mpremote expects
            self._pending_reboot_output += b'soft reboot\r\n'
            # Reset raw REPL state - the new process starts in normal REPL mode
            # The client is responsible for entering raw REPL if needed
            self._in_raw_repl = False
            # Read and queue the actual banner from the new process
            time.sleep(0.2)
            try:
                # Read the real banner from the new process
                ready, _, _ = select.select([self.fd], [], [], 0.5)
                if ready:
                    banner = os.read(self.fd, 4096)
                    # Pass the banner through to the client as-is
                    # The client will decide whether to enter raw REPL mode
                    self._pending_reboot_output += banner
            except:
                # If we can't read the banner, just continue - the client will
                # receive output directly from the process
                pass

    def update_in_waiting(self):
        """Update the number of bytes waiting to be read."""
        # Don't start the process just to check if data is waiting
        if not self._started:
            self.in_waiting = 0
            return
            
        with self._check_buffer_lock:
            if self._closed:
                self.in_waiting = 0
                return
            
            if self.fd is not None:
                # PTY mode
                try:
                    ready, _, _ = select.select([self.fd], [], [], 0)
                    self.in_waiting = 1 if ready else 0
                except (OSError, ValueError):
                    self._closed = True
                    self.in_waiting = 0
            else:
                # Process mode (old code)
                if not self.process or self.process.poll() is not None:
                    self.in_waiting = 0
                    return

                # Check if data is available without blocking
                ready, _, _ = select.select([self.process.stdout], [], [], 0)
                if ready:
                    # There's data available, but we don't know exactly how much
                    # Set to 1 to indicate data is available
                    self.in_waiting = 1
                else:
                    self.in_waiting = 0

    def get_settings(self):
        """Get current serial port settings."""
        return {
            'baudrate': self.baudrate,
            'bytesize': self.bytesize,
            'parity': self.parity,
            'stopbits': self.stopbits,
            'rtscts': self.rtscts,
            'dsrdtr': self.dsrdtr,
            'xonxoff': self.xonxoff,
        }

    def apply_settings(self, settings):
        """Apply serial port settings (stored but not actually used)."""
        self.baudrate = settings.get('baudrate', self.baudrate)
        self.bytesize = settings.get('bytesize', self.bytesize)
        self.parity = settings.get('parity', self.parity)
        self.stopbits = settings.get('stopbits', self.stopbits)
        self.rtscts = settings.get('rtscts', self.rtscts)
        self.dsrdtr = settings.get('dsrdtr', self.dsrdtr)
        self.xonxoff = settings.get('xonxoff', self.xonxoff)

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
        """Flush output buffer."""
        if self._closed:
            return
        
        if self.fd is None and self.process and self.process.poll() is None:
            try:
                self.process.stdin.flush()
            except (OSError, BrokenPipeError):
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
        self.rfc2217 = serial.rfc2217.PortManager(
            self.serial,
            self,
            logger=logging.getLogger('rfc2217.server') if debug else None
        )
        self.log = logging.getLogger('redirector')
        self.alive = False

    def statusline_poller(self):
        """Poll for modem status line changes."""
        self.log.debug('status line poll thread started')
        while self.alive:
            time.sleep(1)
            self.rfc2217.check_modem_lines()
        self.log.debug('status line poll thread terminated')

    def shortcircuit(self):
        """Connect the subprocess to the TCP port by copying data bidirectionally."""
        self.alive = True
        self.thread_read = threading.Thread(target=self.reader)
        self.thread_read.daemon = True
        self.thread_read.name = 'subprocess->socket'
        self.thread_read.start()
        self.thread_poll = threading.Thread(target=self.statusline_poller)
        self.thread_poll.daemon = True
        self.thread_poll.name = 'status line poll'
        self.thread_poll.start()
        self.writer()

    def reader(self):
        """Loop forever and copy subprocess output -> socket."""
        self.log.debug('reader thread started')
        while self.alive:
            try:
                # Check if process has exited (e.g., from Ctrl-D)
                if hasattr(self.serial, 'process') and self.serial.process:
                    if self.serial.process.poll() is not None:
                        self.log.info('MicroPython process exited - performing auto-restart (soft reboot)')
                        
                        # Send "soft reboot" message that mpremote expects
                        try:
                            self.write(b'soft reboot\r\n')
                        except:
                            pass
                        
                        # Restart the process
                        if hasattr(self.serial, 'restart_callback') and self.serial.restart_callback:
                            try:
                                result = self.serial.restart_callback()
                                if result:
                                    self.serial.fd, self.serial.process = result
                                    # Reset state for the new process
                                    self.serial._in_raw_repl = False
                                    self.serial._closed = False
                                    self.log.info('Process restarted successfully')
                                    
                                    # Give process time to start and output banner
                                    time.sleep(0.3)

                                    # Read and forward the banner to the client
                                    # Let the client decide whether to enter raw REPL
                                    try:
                                        import select
                                        ready, _, _ = select.select([self.serial.fd], [], [], 0.5)
                                        if ready:
                                            import os

                                            banner = os.read(self.serial.fd, 4096)
                                            if banner:
                                                # Forward the banner to the client as-is
                                                self.write(b"".join(self.rfc2217.escape(banner)))
                                    except Exception as e:
                                        self.log.error(f"Error reading banner: {e}")
                            except Exception as e:
                                self.log.error(f'Process restart failed: {e}')
                                self.alive = False
                                break
                        else:
                            self.log.error('No restart callback available')
                            self.alive = False
                            break
                        
                        continue
                
                self.serial.update_in_waiting()
                data = self.serial.read(self.serial.in_waiting or 1)
                if data:
                    # Escape outgoing data when needed (Telnet IAC (0xff) character)
                    self.write(b''.join(self.rfc2217.escape(data)))
            except socket.error as msg:
                self.log.error('{}'.format(msg))
                break
            except Exception as e:
                self.log.error('Reader error: {}'.format(e))
                break
        self.alive = False
        self.log.debug('reader thread terminated')

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
                filtered_data = b''.join(self.rfc2217.filter(data))
                
                if not filtered_data:
                    continue  # No data to write after filtering
                
                # Write data to serial port (including Ctrl-D)
                # Ctrl-D will cause unix port to exit, which we handle in reader
                self.serial.write(filtered_data)
                
            except socket.error as msg:
                self.log.error('{}'.format(msg))
                break
            except Exception as e:
                self.log.error('Writer error: {}'.format(e))
                break
        self.stop()

    def stop(self):
        """Stop copying data."""
        self.log.debug('stopping')
        if self.alive:
            self.alive = False
            if hasattr(self, 'thread_read'):
                self.thread_read.join(timeout=1)
            if hasattr(self, 'thread_poll'):
                self.thread_poll.join(timeout=1)


def main():
    parser = argparse.ArgumentParser(
        description="MicroPython RFC 2217 Bridge - Expose MicroPython REPL via RFC 2217.",
        epilog="""\
NOTE: No security measures are implemented. Anyone can remotely connect
to this service over the network.

Only one connection at once is supported. When the connection is terminated,
it waits for the next connect.

The MicroPython process is started fresh for each connection and terminated
when the connection closes.
""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        'MICROPYTHON_PATH',
        help='Path to the MicroPython executable'
    )

    parser.add_argument(
        '-p', '--port',
        type=int,
        help='Local TCP port (default: %(default)s)',
        metavar='PORT',
        default=2217
    )

    parser.add_argument(
        '-H', '--host',
        help='Local host/interface to bind to (default: all interfaces)',
        metavar='HOST',
        default=''
    )

    parser.add_argument(
        '-v', '--verbose',
        dest='verbosity',
        action='count',
        help='Increase verbosity (can be given multiple times)',
        default=0
    )

    parser.add_argument(
        '--micropython-args',
        help='Additional arguments to pass to MicroPython (e.g., "-i script.py")',
        default='',
        metavar='ARGS'
    )

    args = parser.parse_args()

    # Validate MicroPython path
    if not os.path.isfile(args.MICROPYTHON_PATH):
        print(f"Error: MicroPython executable not found: {args.MICROPYTHON_PATH}", file=sys.stderr)
        sys.exit(1)

    if not os.access(args.MICROPYTHON_PATH, os.X_OK):
        print(f"Error: MicroPython executable is not executable: {args.MICROPYTHON_PATH}", file=sys.stderr)
        sys.exit(1)

    # Set up logging
    if args.verbosity > 3:
        args.verbosity = 3
    level = (logging.WARNING, logging.INFO, logging.DEBUG, logging.NOTSET)[args.verbosity]
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logging.getLogger('rfc2217').setLevel(level)

    logging.info("MicroPython RFC 2217 Bridge - type Ctrl-C to quit")
    logging.info(f"MicroPython executable: {args.MICROPYTHON_PATH}")

    # Create server socket
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        srv.bind((args.host, args.port))
        srv.listen(1)
    except OSError as e:
        logging.error(f"Could not bind to {args.host}:{args.port}: {e}")
        sys.exit(1)

    bind_addr = args.host or '0.0.0.0'
    logging.info(f"RFC 2217 server listening on {bind_addr}:{args.port}")
    logging.info("Connect with: mpremote connect rfc2217://localhost:{}".format(args.port))
    logging.info("          or: pyserial-miniterm rfc2217://localhost:{} 115200".format(args.port))

    process = None

    try:
        while True:
            try:
                logging.info("Waiting for connection...")
                client_socket, addr = srv.accept()
                logging.info(f"Connected by {addr[0]}:{addr[1]}")
                client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

                # Prepare command for MicroPython
                cmd = [args.MICROPYTHON_PATH]
                if args.micropython_args:
                    cmd.extend(args.micropython_args.split())

                master_fd = None
                slave_fd = None
                process = None
                
                # Define helper to create process
                def create_micropython_process():
                    """Create and return a new MicroPython process with PTY."""
                    nonlocal process
                    
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
                        close_fds=False
                    )
                    
                    # Close the slave fd in the parent process
                    os.close(new_slave_fd)
                    
                    return (new_master_fd, process)
                
                # Define lazy start callback to start MicroPython after RFC2217 negotiation
                def start_micropython():
                    nonlocal master_fd, slave_fd, process
                    logging.info(f"Starting MicroPython (lazy): {' '.join(cmd)}")
                    master_fd, process = create_micropython_process()
                    return (master_fd, process)
                
                # Define restart callback for soft reboot emulation
                def restart_micropython():
                    nonlocal master_fd, process
                    logging.info(f"Restarting MicroPython for soft reboot: {' '.join(cmd)}")
                    master_fd, process = create_micropython_process()
                    return (master_fd, process)

                # Create virtual serial port with lazy initialization and restart callback
                # Pass None as fd initially, it will be set when start_micropython is called
                virtual_serial = VirtualSerialPort(
                    None,  # Will be set by lazy start
                    timeout=0.1,
                    lazy_start_callback=start_micropython,
                    restart_callback=restart_micropython
                )
                # Set fd to None to enable PTY mode after lazy start
                virtual_serial.fd = None
                settings = virtual_serial.get_settings()

                # Create redirector and start data transfer
                r = Redirector(
                    virtual_serial,
                    client_socket,
                    args.verbosity > 0
                )

                try:
                    r.shortcircuit()
                finally:
                    logging.info('Disconnected')
                    r.stop()
                    client_socket.close()

                    # Close the master fd if it was created
                    if master_fd is not None:
                        try:
                            os.close(master_fd)
                        except:
                            pass
                    
                    # Close slave fd if it wasn't closed yet
                    if slave_fd is not None:
                        try:
                            os.close(slave_fd)
                        except:
                            pass

                    # Terminate MicroPython process if it was started
                    if process and process.poll() is None:
                        logging.info("Terminating MicroPython process...")
                        process.terminate()
                        try:
                            process.wait(timeout=2)
                        except subprocess.TimeoutExpired:
                            logging.warning("MicroPython process did not terminate, killing...")
                            process.kill()
                            process.wait()
                    process = None

            except KeyboardInterrupt:
                sys.stdout.write('\n')
                break
            except socket.error as msg:
                logging.error(str(msg))
            except Exception as e:
                logging.error(f"Unexpected error: {e}", exc_info=args.verbosity > 1)

    finally:
        # Clean up
        if process and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
        srv.close()
        logging.info('--- exit ---')


if __name__ == '__main__':
    main()
