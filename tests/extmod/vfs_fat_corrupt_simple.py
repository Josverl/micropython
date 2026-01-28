"""
Test for FAT VFS handling of corrupted filenames with invalid UTF-8.
This creates a simpler reproduction case by directly manipulating 
the filesystem data.
"""

try:
    import errno, os, vfs

    vfs.VfsFat
except (ImportError, AttributeError):
    print("SKIP")
    raise SystemExit


class RAMFS:
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

# Create FAT filesystem and mount it
fs = vfs.VfsFat(bdev)
vfs.mount(fs, "/ramdisk")

# Create a test file with a longer name that requires LFN
with fs.open("testfile_with_long_name.txt", "w") as f:
    f.write("hello")

# Verify file exists normally
items = list(fs.ilistdir())
print("Normal listing OK:", len(items) == 1 and "testfile" in items[0][0])

# Now corrupt the filesystem - find the directory entry and insert invalid UTF-8
# We'll search for the directory entry containing "TEST" (short name)
# and replace a character with an invalid UTF-8 byte sequence

# Search through the raw data for directory entries
found = False
test_patterns = [
    b"testfile_with_long_name.txt",  # The actual filename
    b"t\x00e\x00s\x00t\x00f\x00i\x00l\x00e\x00",  # UTF-16LE encoding (LFN format)
]

for pattern in test_patterns:
    if found:
        break
    for offset in range(0, len(bdev.data) - len(pattern)):
        if bdev.data[offset:offset + len(pattern)] == pattern:
            # Corrupt with invalid UTF-8/UTF-16 sequence
            # For UTF-16LE LFN entries, corrupt by creating invalid UTF-16
            # For plain text, use 0xC0 (invalid UTF-8 byte)
            print(f"Found pattern at offset {offset}, length {len(pattern)}")
            
            if b"\x00" in pattern:
                # UTF-16LE pattern - corrupt the UTF-16 data
                # Insert an unpaired surrogate or invalid UTF-16 sequence
                # 0xD800 is the start of high surrogates (must be paired)
                bdev.data[offset] = 0x00
                bdev.data[offset + 1] = 0xD8  # High surrogate without pair
                bdev.data[offset + 2] = 0x00  # null terminator (will end the string early)
                bdev.data[offset + 3] = 0x00
            else:
                # Plain ASCII/UTF-8 - corrupt with invalid UTF-8
                bdev.data[offset] = 0xC0
                bdev.data[offset + 1] = 0xC0
            
            found = True
            print("Corrupted filename in directory")
            break

if found:
    # Now try to list directory - this should handle the corruption gracefully
    # Currently raises UnicodeError, but should raise OSError
    try:
        result = list(fs.ilistdir())
        print("Unexpected: Listing succeeded despite corruption")
        print("Result:", result)
    except UnicodeError as e:
        print("Current behavior: UnicodeError -", type(e).__name__)
    except OSError as e:
        print("Desired behavior: OSError with errno", e.errno)
    except Exception as e:
        print("Unexpected error:", type(e).__name__, str(e))
else:
    print("Could not find directory entry - test inconclusive")

vfs.umount(fs)
