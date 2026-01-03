# MicroPython RFC 2217 Bridge

This tool exposes a MicroPython REPL as an RFC 2217 server, allowing remote access to the REPL over a network connection without requiring an intermediate serial port.

## Overview

RFC 2217 is a protocol that extends Telnet to support serial port control. This bridge creates a virtual serial port server that:

1. Starts a MicroPython executable in a pseudo-terminal (PTY)
2. Creates an RFC 2217 server on a specified network port
3. Bridges data bidirectionally between the RFC 2217 socket and the MicroPython process
4. Handles graceful shutdown and cleanup

## Requirements

- Python 3.x
- pyserial package (also used by mpremote)
- MicroPython unix executable (built from `ports/unix/`)

## Usage

### Basic Usage

```bash
# From the tools directory - uses default path automatically
cd tools
python3 mp_rfc2217_bridge.py

# From the repository root
python3 tools/mp_rfc2217_bridge.py

# With a custom MicroPython path
python3 tools/mp_rfc2217_bridge.py /path/to/micropython
```

The script automatically uses `../ports/unix/build-standard/micropython` relative to its location, so you don't need to specify a path when running from the MicroPython repository.

### Bridge Options

```bash
python3 tools/mp_rfc2217_bridge.py -p 2217 -v
```

Options:
- `MICROPYTHON_PATH`: Optional path to the MicroPython executable (default: `../ports/unix/build-standard/micropython` relative to script)
- `-p PORT, --port PORT`: Local TCP port to listen on (default: 2217)
- `-H HOST, --host HOST`: Local host/interface to bind to (default: all interfaces)
- `-v, --verbose`: Increase bridge verbosity (can be repeated: -v, -vv, -vvv)

### MicroPython Options

These options are passed through to the MicroPython executable:

- `-O`: Apply bytecode optimizations (can be repeated: `-O`, `-OO`, `-OOO`)
- `-X OPTION`: Implementation-specific options (e.g., `-X heapsize=4M`, `-X emit=native`)
- `--cwd DIR`: Working directory for MicroPython (used as filesystem root for unix port)
- `--mp-verbose`: MicroPython verbose mode (trace operations); can be repeated
- `--micropython-args ARGS`: Additional raw arguments to pass to MicroPython

### Examples

```bash
# Default MicroPython, default port
python3 tools/mp_rfc2217_bridge.py

# With bytecode optimization level 2
python3 tools/mp_rfc2217_bridge.py -O -O

# Use an empty directory as filesystem root
mkdir -p /tmp/mp_root
python3 tools/mp_rfc2217_bridge.py --cwd /tmp/mp_root

# With custom heap size and native code emission
python3 tools/mp_rfc2217_bridge.py -X heapsize=4M -X emit=native

# Custom MicroPython path with options
python3 tools/mp_rfc2217_bridge.py ./my_micropython -O -O -X heapsize=4M

# Bridge verbose and MicroPython verbose
python3 tools/mp_rfc2217_bridge.py -vv --mp-verbose
```

## Connecting to the Server

Once the bridge is running, you can connect using any RFC 2217 compatible client:

### Using Python with pyserial (Recommended)

```python
import serial

ser = serial.serial_for_url('rfc2217://localhost:2217', baudrate=115200, timeout=2)

# Read initial output
data = ser.read(1000)
print(data.decode('utf-8'))

# Send commands
ser.write(b'print("Hello World")\r\n')

# Read response
response = ser.read(1000)
print(response.decode('utf-8'))

ser.close()
```

### Using pyserial-miniterm

```bash
pyserial-miniterm rfc2217://localhost:2217 115200
```

### Using mpremote

The bridge fully supports mpremote commands:

```bash
# Standard mpremote commands (with soft reset):
mpremote connect rfc2217://localhost:2217 eval "print('Hello')"
mpremote connect rfc2217://localhost:2217 exec script.py

# Use 'resume' to preserve state across connections:
mpremote connect rfc2217://localhost:2217 resume exec "x = 42"
mpremote connect rfc2217://localhost:2217 resume exec "print(x)"  # prints 42
```

The bridge behaves like a physical MCU:
- **Without `resume`**: Each command triggers a soft reset (clears RAM state)
- **With `resume`**: State persists between connections (process stays running)

## How It Works

1. **PTY Creation**: The tool creates a pseudo-terminal (PTY) pair, which simulates a real terminal device
2. **Process Spawning**: MicroPython is launched with its stdin/stdout/stderr connected to the PTY slave
3. **RFC 2217 Server**: A TCP server is created that implements the RFC 2217 protocol
4. **Data Bridging**: Data flows bidirectionally:
   - Client → Socket → RFC 2217 filter → PTY master → MicroPython
   - MicroPython → PTY master → RFC 2217 escape → Socket → Client
5. **Persistent Mode**: The MicroPython process persists across client connections, just like a physical MCU stays powered. State is preserved between connections when using `resume`. Soft resets (Ctrl-D) restart the process, matching real MCU behavior

## Use Cases

- Remote access to MicroPython REPL without physical serial port
- Testing MicroPython code over the network
- Integration with serial port monitoring tools
- Automation and scripting with network-based REPL access
- Debugging and development from remote machines

## Limitations

- **No Security**: The bridge has no authentication or encryption. Use only on trusted networks or over VPN/SSH tunnels
- **Single Connection**: Only one client can connect at a time
- **Persistent Mode**: The MicroPython process persists across connections (like a physical MCU). Use `mpremote resume` to preserve state between connections. Soft resets restart the process, clearing RAM state.
- **Filesystem**: The unix port uses the host filesystem with the current working directory as root. Use `--cwd DIR` to specify a dedicated directory. Files persist across soft resets (unlike RAM state).

## Security Considerations

⚠️ **WARNING**: This tool implements no security measures. Anyone who can reach the TCP port can access the MicroPython REPL, which provides full code execution capabilities.

For secure remote access, consider:
- Using SSH port forwarding: `ssh -L 2217:localhost:2217 remote-host`
- Running on localhost only: `-H localhost`
- Using a VPN or firewall to restrict access
- Running behind a reverse proxy with authentication

## Troubleshooting

### Connection refused or timeout
- Check that the server is running and listening on the expected port
- Verify firewall settings allow connections to the port
- Ensure the correct host/port in the client connection string

### No output from MicroPython
- The tool uses a PTY to ensure MicroPython outputs its banner
- If still no output, try with `-vv` for debug logging
- Check if the MicroPython executable is working: `./micropython -i`

### Process doesn't terminate
- The tool tries to gracefully terminate processes (SIGTERM)
- If that fails after 2 seconds, it forcefully kills them (SIGKILL)
- Zombie processes should be automatically reaped

## Example Session

```
$ python3 tools/mp_rfc2217_bridge.py -v -O -O
2026-01-03 12:00:00,000 - root - INFO - MicroPython RFC 2217 Bridge - type Ctrl-C to quit
2026-01-03 12:00:00,000 - root - INFO - MicroPython executable: /home/user/micropython/ports/unix/build-standard/micropython
2026-01-03 12:00:00,000 - root - INFO - MicroPython optimization: -OO
2026-01-03 12:00:00,000 - root - INFO - RFC 2217 server listening on 0.0.0.0:2217
2026-01-03 12:00:00,000 - root - INFO - Connect with: mpremote connect rfc2217://localhost:2217
2026-01-03 12:00:00,000 - root - INFO -           or: pyserial-miniterm rfc2217://localhost:2217 115200
2026-01-03 12:00:00,000 - root - INFO - Waiting for connection...
2026-01-03 12:00:10,000 - root - INFO - Connected by 127.0.0.1:54321
2026-01-03 12:00:10,000 - root - INFO - Starting MicroPython (lazy): /home/user/micropython/ports/unix/build-standard/micropython -O -O
...
2026-01-03 12:00:20,000 - root - INFO - Disconnected
2026-01-03 12:00:20,000 - root - INFO - Terminating MicroPython process...
2026-01-03 12:00:20,000 - root - INFO - Waiting for connection...
```

## License

This tool is part of the MicroPython project and is licensed under the MIT License.
