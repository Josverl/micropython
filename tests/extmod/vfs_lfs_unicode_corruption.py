"""
Test for LittleFS VFS UTF-8 validation and corruption handling.

This test validates that LittleFS VFS correctly detects and handles invalid UTF-8
in filenames, raising OSError(EIO) instead of UnicodeError.
"""

try:
    import errno, vfs

    vfs.VfsLfs2
except (ImportError, AttributeError):
    print("SKIP")
    raise SystemExit


class RAMBlockDevice:
    ERASE_BLOCK_SIZE = 1024

    def __init__(self, blocks):
        self.data = bytearray(blocks * self.ERASE_BLOCK_SIZE)

    def readblocks(self, block, buf, off):
        addr = block * self.ERASE_BLOCK_SIZE + off
        for i in range(len(buf)):
            buf[i] = self.data[addr + i]
        return 0

    def writeblocks(self, block, buf, off):
        addr = block * self.ERASE_BLOCK_SIZE + off
        for i in range(len(buf)):
            self.data[addr + i] = buf[i]
        return 0

    def ioctl(self, op, arg):
        if op == 4:  # block count
            return len(self.data) // self.ERASE_BLOCK_SIZE
        if op == 5:  # block size
            return self.ERASE_BLOCK_SIZE
        if op == 6:  # erase block
            return 0


try:
    bdev = RAMBlockDevice(30)
    vfs.VfsLfs2.mkfs(bdev)
except MemoryError:
    print("SKIP")
    raise SystemExit

fs = vfs.VfsLfs2(bdev)
vfs.mount(fs, "/lfs")

# Test 1: Normal operation with valid UTF-8
print("Test 1: Valid UTF-8 filenames")
with fs.open("test.txt", "w") as f:
    f.write("hello")

items = list(fs.ilistdir())
print("  Normal listing:", len(items) == 1)

# Test 2: Valid non-ASCII UTF-8
print("Test 2: Valid non-ASCII UTF-8")
try:
    with fs.open("café.txt", "w") as f:
        f.write("test")
    items = list(fs.ilistdir())
    found = False
    for item in items:
        if "caf" in item[0]:
            found = True
            break
    print("  UTF-8 support:", "yes" if found else "limited")
except (OSError, UnicodeError):
    print("  UTF-8 support: limited")

# Unmount before corruption
vfs.umount(fs)

# Test 3: Simulate corruption by injecting invalid UTF-8 into filename storage
# LittleFS stores filenames as raw bytes, so corruption is possible
print("Test 3: Corruption simulation")

# Find and corrupt a filename in the LittleFS data
# We'll search for the filename "test" and replace it with invalid UTF-8
corrupted = False
for offset in range(0, len(bdev.data) - 10):
    # Look for "test" in the data
    if bdev.data[offset:offset + 4] == b"test":
        # Check it's likely a filename (not other data)
        # In LittleFS, filenames are stored with length prefix
        if offset > 0 and bdev.data[offset - 1] in range(1, 20):
            print("  Found potential filename at offset", offset)
            # Corrupt with invalid UTF-8: 0xC0, 0xC1 are invalid
            bdev.data[offset] = 0xC0
            bdev.data[offset + 1] = 0xC1
            corrupted = True
            break

if corrupted:
    # Remount and try to list - should get OSError(EIO) if Unicode checking enabled
    fs = vfs.VfsLfs2(bdev)
    vfs.mount(fs, "/lfs")

    print("Test 4: Reading corrupted filename")
    try:
        items = list(fs.ilistdir())
        print("  Result: no error (checking disabled or entry unreadable)")
    except OSError as e:
        if e.errno == errno.EIO:
            print("  Result: OSError EIO (expected with Unicode checking)")
        else:
            print("  Result: OSError", e.errno)
    except UnicodeError:
        print("  Result: UnicodeError (bug - should be OSError)")

    vfs.umount(fs)
else:
    print("  Could not find filename to corrupt")

print("\nTest completed")
