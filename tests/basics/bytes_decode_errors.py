# Test bytes.decode() with error handlers

# Test ignore mode with invalid UTF-8
print(repr(b'\xff\xfe'.decode('utf-8', 'ignore')))

# Test strict mode (default) with invalid UTF-8
try:
    b'\xff\xfe'.decode('utf-8')
except UnicodeError:
    print("UnicodeError")

try:
    b'\xff\xfe'.decode('utf-8', 'strict')
except UnicodeError:
    print("UnicodeError")

# Test with valid UTF-8
print(repr(b'hello'.decode('utf-8', 'ignore')))
print(repr(b'hello'.decode('utf-8')))

# Test mixed valid and invalid UTF-8
print(repr(b'hello\xffworld'.decode('utf-8', 'ignore')))

# Test multiple invalid bytes
print(repr(b'\x80\x81\x82'.decode('utf-8', 'ignore')))

# Test invalid continuation byte
print(repr(b'\xc0\x20'.decode('utf-8', 'ignore')))

# Test incomplete sequence at end
print(repr(b'hello\xc0'.decode('utf-8', 'ignore')))

# Test valid multi-byte UTF-8
print(repr(b'\xc2\xa9'.decode('utf-8', 'ignore')))  # © symbol

# Test bytearray as well
print(repr(bytearray(b'\xff\xfe').decode('utf-8', 'ignore')))
