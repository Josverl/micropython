"""
Test for FAT VFS UTF-8 validation and corruption handling.

This test validates the fix that detects invalid UTF-8 in FAT filenames
and raises OSError(EIO) instead of UnicodeError.

Since we cannot easily inject invalid UTF-8 into FatFS's internal buffers
during runtime, this test uses a different approach: it creates files and
then physically corrupts the directory entries in the raw block device data.
"""

try:
    import errno, os, vfs

    vfs.VfsFat
except (ImportError, AttributeError):
    print("SKIP")
    raise SystemExit


class RAMFS:
    """Simple RAM block device for FAT filesystem."""

    SEC_SIZE = 512

    def __init__(self, blocks):
        self.data = bytearray(blocks * self.SEC_SIZE)

    def readblocks(self, n, buf):
        for i in range(len(buf)):
            buf[i] = self.data[n * self.SEC_SIZE + i]

    def writeblocks(self, n, buf):
        for i in range(len(buf)):
            self.data[n * self.SEC_SIZE + i] = buf[i]

    def ioctl(self, op, arg):
        if op == 4:  # MP_BLOCKDEV_IOCTL_BLOCK_COUNT
            return len(self.data) // self.SEC_SIZE
        if op == 5:  # MP_BLOCKDEV_IOCTL_BLOCK_SIZE
            return self.SEC_SIZE


try:
    bdev = RAMFS(50)
    vfs.VfsFat.mkfs(bdev)
except MemoryError:
    print("SKIP")
    raise SystemExit

# Create and mount filesystem
fs = vfs.VfsFat(bdev)
vfs.mount(fs, "/ramdisk")

# Test 1: Normal operation - valid UTF-8 filenames
print("Test 1: Normal operation")
with fs.open("test.txt", "w") as f:
    f.write("hello")

items = list(fs.ilistdir())
print("  Normal listing:", len(items) == 1)

# Test 2: Test getcwd returns valid path
print("Test 2: getcwd")
cwd = fs.getcwd()
print("  getcwd:", cwd == "/")

# Test 3: Create a file with non-ASCII but valid UTF-8 name (if supported)
print("Test 3: Valid UTF-8 with non-ASCII")
try:
    with fs.open("café.txt", "w") as f:
        f.write("test")
    items = list(fs.ilistdir())
    found_cafe = any("caf" in item[0] for item in items)
    print("  UTF-8 support:", "yes" if found_cafe else "limited")
except (OSError, UnicodeError):
    print("  UTF-8 support: limited")

# Unmount before corruption
vfs.umount(fs)

# Test 4: Simulate filesystem corruption
# We'll corrupt the directory entry by replacing valid characters with invalid UTF-8
print("Test 4: Corruption simulation")

# Find directory entries in the FAT data
# Directory entries are 32 bytes each, filename is at offset 0-10 (8.3 format)
# We look for the short filename "TEST" (uppercase, part of test.txt)
corrupted = False
for offset in range(0, len(bdev.data) - 32):
    # Check if this looks like a directory entry with "TEST"
    if bdev.data[offset:offset + 4] == b"TEST":
        # Found it - corrupt with invalid UTF-8
        # 0xC0 and 0xC1 are invalid UTF-8 start bytes (overlong encoding)
        print("  Found dir entry at offset", offset)
        bdev.data[offset] = 0xC0  # Invalid UTF-8
        bdev.data[offset + 1] = 0xC1  # Invalid UTF-8
        corrupted = True
        break

if corrupted:
    # Remount filesystem with corrupted data
    fs = vfs.VfsFat(bdev)
    vfs.mount(fs, "/ramdisk")

    # Try to list directory - should get OSError(EIO) if UTF-8 checking is enabled
    print("Test 5: Reading corrupted filename")
    try:
        items = list(fs.ilistdir())
        # If we get here, either:
        # 1. Unicode checking is disabled
        # 2. FatFS filtered out the corrupted entry
        print("  Result: no error (checking disabled or entry filtered)")
    except OSError as e:
        if e.errno == errno.EIO:
            print("  Result: OSError EIO (expected with Unicode checking)")
        else:
            print("  Result: OSError", e.errno)
    except UnicodeError:
        print("  Result: UnicodeError (old buggy behavior)")

    # Test 6: getcwd should also detect corruption if path is corrupted
    # We'll create a subdirectory and corrupt its name
    print("Test 6: getcwd with corruption")
    try:
        fs.mkdir("subdir")
        fs.chdir("subdir")
    except OSError:
        # Directory might be corrupted already
        print("  Setup: mkdir/chdir failed")
    else:
        vfs.umount(fs)

        # Corrupt "SUBDIR" in the filesystem
        for offset in range(0, len(bdev.data) - 32):
            if bdev.data[offset:offset + 6] == b"SUBDIR":
                print("  Found subdir at offset", offset)
                bdev.data[offset] = 0xFE  # 0xFE is invalid in UTF-8
                break

        # Remount and try getcwd
        fs = vfs.VfsFat(bdev)
        vfs.mount(fs, "/ramdisk")
        try:
            cwd = fs.getcwd()
            print("  getcwd result: no error")
        except OSError as e:
            if e.errno == errno.EIO:
                print("  getcwd result: OSError EIO (expected)")
            else:
                print("  getcwd result: OSError", e.errno)
        except UnicodeError:
            print("  getcwd result: UnicodeError (bug)")

    vfs.umount(fs)
else:
    print("  Could not find directory entry to corrupt")

print("\nTest completed")
