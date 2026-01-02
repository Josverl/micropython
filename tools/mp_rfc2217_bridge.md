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
- pyserial package (usually `python3-serial` or `pip install pyserial`)
- MicroPython unix executable (built from `ports/unix/`)

## Usage

### Basic Usage

```bash
python3 tools/mp_rfc2217_bridge.py /path/to/micropython
```

This will start an RFC 2217 server on the default port 2217.

### With Options

```bash
python3 tools/mp_rfc2217_bridge.py -p 2217 -v ./ports/unix/build-standard/micropython
```

Options:
- `-p PORT, --port PORT`: Local TCP port to listen on (default: 2217)
- `-H HOST, --host HOST`: Local host/interface to bind to (default: all interfaces)
- `-v, --verbose`: Increase verbosity (can be repeated: -v, -vv, -vvv)
- `--micropython-args ARGS`: Additional arguments to pass to MicroPython

### Example with Additional Arguments

```bash
python3 tools/mp_rfc2217_bridge.py --micropython-args "-i script.py" ./micropython
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

⚠️ **Note**: mpremote has compatibility issues with the unix port of MicroPython because the unix port doesn't output the "soft reboot" message that mpremote expects after a soft reset. This is a limitation of the unix port, not the RFC2217 bridge.

As a workaround, you can use pyserial directly or use mpremote with embedded MicroPython builds (when exposing actual hardware boards via RFC2217).

For manual testing with the unix port:

```bash
# This will fail with "could not enter raw repl" error:
mpremote connect rfc2217://localhost:2217 eval "print('test')"

# Use pyserial-miniterm or Python/pyserial instead
```

## How It Works

1. **PTY Creation**: The tool creates a pseudo-terminal (PTY) pair, which simulates a real terminal device
2. **Process Spawning**: MicroPython is launched with its stdin/stdout/stderr connected to the PTY slave
3. **RFC 2217 Server**: A TCP server is created that implements the RFC 2217 protocol
4. **Data Bridging**: Data flows bidirectionally:
   - Client → Socket → RFC 2217 filter → PTY master → MicroPython
   - MicroPython → PTY master → RFC 2217 escape → Socket → Client
5. **Session Management**: Each connection creates a fresh MicroPython process, which is terminated when the connection closes

## Use Cases

- Remote access to MicroPython REPL without physical serial port
- Testing MicroPython code over the network
- Integration with serial port monitoring tools
- Automation and scripting with network-based REPL access
- Debugging and development from remote machines

## Limitations

- **No Security**: The bridge has no authentication or encryption. Use only on trusted networks or over VPN/SSH tunnels
- **Single Connection**: Only one client can connect at a time
- **No Persistence**: Each connection starts a fresh MicroPython instance
- **mpremote Incompatibility with Unix Port**: mpremote expects a "soft reboot" message that the unix port of MicroPython doesn't produce. This is a unix port limitation, not a bridge issue. Use pyserial or pyserial-miniterm instead, or use this bridge with embedded MicroPython builds that do output the soft reboot message.

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
$ python3 tools/mp_rfc2217_bridge.py -v ports/unix/build-standard/micropython
2026-01-02 20:00:00,000 - root - INFO - MicroPython RFC 2217 Bridge - type Ctrl-C to quit
2026-01-02 20:00:00,000 - root - INFO - MicroPython executable: ports/unix/build-standard/micropython
2026-01-02 20:00:00,000 - root - INFO - RFC 2217 server listening on 0.0.0.0:2217
2026-01-02 20:00:00,000 - root - INFO - Connect with: mpremote connect rfc2217://localhost:2217
2026-01-02 20:00:00,000 - root - INFO -           or: pyserial-miniterm rfc2217://localhost:2217 115200
2026-01-02 20:00:00,000 - root - INFO - Waiting for connection...
2026-01-02 20:00:10,000 - root - INFO - Connected by 127.0.0.1:54321
2026-01-02 20:00:10,000 - root - INFO - Starting MicroPython: ports/unix/build-standard/micropython
...
2026-01-02 20:00:20,000 - root - INFO - Disconnected
2026-01-02 20:00:20,000 - root - INFO - Terminating MicroPython process...
2026-01-02 20:00:20,000 - root - INFO - Waiting for connection...
```

## License

This tool is part of the MicroPython project and is licensed under the MIT License.
