"""
Test for FAT VFS handling of corrupted filenames with invalid UTF-8.

This is a regression test for the fix that converts UnicodeError to OSError(EIO)
when filesystem corruption causes invalid UTF-8 byte sequences in filenames.

The test creates a custom block device that can inject corruption to simulate
real-world filesystem corruption scenarios where directory entries contain
invalid UTF-8 sequences (e.g., from CP437 codepage: b"Fr\x81hst\x81ck.wav").
"""

try:
    import errno, os, vfs

    vfs.VfsFat
except (ImportError, AttributeError):
    print("SKIP")
    raise SystemExit


class CorruptibleRAMFS:
    """RAM filesystem that can inject corruption on demand."""

    SEC_SIZE = 512

    def __init__(self, blocks):
        self.data = bytearray(blocks * self.SEC_SIZE)
        self.corrupt_pattern = None
        self.corrupt_replacement = None

    def set_corruption(self, pattern, replacement):
        """Set pattern to replace on next read - simulates corruption."""
        self.corrupt_pattern = pattern
        self.corrupt_replacement = replacement

    def readblocks(self, n, buf):
        for i in range(len(buf)):
            buf[i] = self.data[n * self.SEC_SIZE + i]

        # Apply corruption if set (simulates reading corrupted data)
        if self.corrupt_pattern is not None:
            buf_bytes = bytes(buf)
            if self.corrupt_pattern in buf_bytes:
                idx = buf_bytes.index(self.corrupt_pattern)
                for j, byte_val in enumerate(self.corrupt_replacement):
                    if idx + j < len(buf):
                        buf[idx + j] = byte_val
                # Only corrupt once, then reset
                self.corrupt_pattern = None
                self.corrupt_replacement = None

    def writeblocks(self, n, buf):
        for i in range(len(buf)):
            self.data[n * self.SEC_SIZE + i] = buf[i]

    def ioctl(self, op, arg):
        if op == 4:  # MP_BLOCKDEV_IOCTL_BLOCK_COUNT
            return len(self.data) // self.SEC_SIZE
        if op == 5:  # MP_BLOCKDEV_IOCTL_BLOCK_SIZE
            return self.SEC_SIZE


try:
    bdev = CorruptibleRAMFS(50)
    vfs.VfsFat.mkfs(bdev)
except MemoryError:
    print("SKIP")
    raise SystemExit

fs = vfs.VfsFat(bdev)
vfs.mount(fs, "/ramdisk")

# Test 1: Normal operation with valid UTF-8 filenames
print("Test 1: Valid UTF-8 filenames")
with fs.open("test.txt", "w") as f:
    f.write("hello")

# Should work normally
items = list(fs.ilistdir())
print("Normal listing:", len(items) == 1 and items[0][0] == "test.txt")

# Test 2: Test with filename that uses valid non-ASCII UTF-8
# Note: This tests that valid UTF-8 is not incorrectly flagged as corruption
print("\nTest 2: Valid non-ASCII UTF-8")
try:
    # File with valid UTF-8 (if supported by port)
    with fs.open("café.txt", "w") as f:
        f.write("test")
    items = list(fs.ilistdir())
    print("Valid UTF-8 works:", len(items) >= 1)
except (OSError, UnicodeError) as e:
    # Some ports may not support non-ASCII filenames
    print("UTF-8 filename support:", "limited")

# Test 3: Simulate corruption that would cause invalid UTF-8
# We inject invalid UTF-8 bytes (0xC0, 0xC1 are invalid in UTF-8)
# by corrupting the directory entry on read
print("\nTest 3: Corrupted filename simulation")

# This test verifies the fix is working by checking that when
# MICROPY_PY_BUILTINS_STR_UNICODE_CHECK is enabled, we get OSError(EIO)
# instead of UnicodeError for corrupted filenames

# Set up corruption: replace 'TEST' with invalid UTF-8 sequence
# 0xC0 and 0xC1 are invalid UTF-8 bytes (overlong encoding)
bdev.set_corruption(b"TEST", b"\xC0\xC1ST")

# Try to list directory - should handle corruption gracefully
try:
    items = list(fs.ilistdir())
    # If we get here, either:
    # 1. MICROPY_PY_BUILTINS_STR_UNICODE_CHECK is disabled (accepts invalid UTF-8)
    # 2. The corruption wasn't triggered (directory was cached)
    print("Corruption handling: no-check-or-cached")
except OSError as e:
    # This is the expected behavior with the fix:
    # OSError with errno EIO when corruption is detected
    if e.errno == errno.EIO:
        print("Corruption handling: OSError-EIO (correct)")
    else:
        print("Corruption handling: OSError-other")
except UnicodeError:
    # This would be the old behavior (bug):
    # UnicodeError when mp_obj_new_str_from_cstr validates UTF-8
    print("Corruption handling: UnicodeError (bug)")

# Test 4: Test getcwd with valid path
print("\nTest 4: getcwd with valid path")
try:
    cwd = fs.getcwd()
    print("getcwd works:", cwd == "/")
except OSError as e:
    print("getcwd error:", e.errno)

# Test 5: Byte listing should work even with invalid UTF-8
print("\nTest 5: Byte listing bypasses UTF-8 check")
try:
    # Set up corruption again
    bdev.set_corruption(b"TEST", b"\xC0\xC1ST")
    items = list(fs.ilistdir(b"/"))
    # Byte listing doesn't validate UTF-8, so it should work
    print("Byte listing works:", True)
except Exception as e:
    print("Byte listing error:", type(e).__name__)

vfs.umount(fs)

print("\nTests completed")
