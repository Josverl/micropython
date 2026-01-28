"""
Test for FAT VFS handling of corrupted filenames that are not valid UTF-8.
This simulates the case where a FAT filesystem has corrupted directory entries.
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

# Create a test file
with fs.open("test.txt", "w") as f:
    f.write("hello")

# Verify file exists normally
print("Normal listing:", list(fs.ilistdir()))

# Now corrupt the filesystem by finding the directory entry and replacing
# valid UTF-8 character with an invalid byte sequence
# In FAT, directory entries are 32 bytes each
# The filename "test.txt" should be stored in the directory entry
# We'll search for "TEST" (FAT stores 8.3 filenames in uppercase in the short name)

# Find the directory entry in the root directory
# Root directory typically starts after the FAT tables
# For a simple FAT filesystem, we can search for the pattern
found = False
for sector in range(len(bdev.data) // bdev.SEC_SIZE):
    offset = sector * bdev.SEC_SIZE
    sector_data = bdev.data[offset : offset + bdev.SEC_SIZE]
    
    # Look for "TEST    TXT" pattern (8.3 format with spaces)
    if b"TEST    TXT" in sector_data:
        # Found the directory entry
        idx = sector_data.index(b"TEST    TXT")
        abs_offset = offset + idx
        
        # Replace the 'e' in "TEST" with 0xC0 (invalid UTF-8 start byte)
        # 0xC0 and 0xC1 are invalid UTF-8 bytes
        print("Found directory entry at offset:", abs_offset)
        
        # Corrupt the short filename
        bdev.data[abs_offset + 1] = 0xC0  # Replace 'E' with invalid UTF-8
        found = True
        break

if not found:
    # Try to find it in long filename entry (LFN)
    # LFN entries have different structure
    for sector in range(len(bdev.data) // bdev.SEC_SIZE):
        offset = sector * bdev.SEC_SIZE
        sector_data = bdev.data[offset : offset + bdev.SEC_SIZE]
        
        # Look for "test.txt" in various encodings in LFN
        # LFN stores filename in UTF-16LE format
        if b"t\x00e\x00s\x00t\x00" in sector_data:
            idx = sector_data.index(b"t\x00e\x00s\x00t\x00")
            abs_offset = offset + idx + 2  # Position of 'e'
            print("Found LFN entry at offset:", abs_offset)
            # Corrupt by inserting invalid UTF-8/UTF-16
            bdev.data[abs_offset] = 0xC0
            found = True
            break

if found:
    print("Corrupted filesystem")
    
    # Now try to list directory - this should raise an error
    # Currently raises UnicodeError, but should raise OSError with appropriate errno
    try:
        result = list(fs.ilistdir())
        print("Listing succeeded (unexpected):", result)
    except UnicodeError as e:
        print("Got UnicodeError (current behavior):", type(e).__name__)
    except OSError as e:
        print("Got OSError (desired behavior):", e.errno)
else:
    print("Could not find directory entry to corrupt")
    print("SKIP")

vfs.umount(fs)
