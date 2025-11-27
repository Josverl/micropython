#!/bin/bash
set -e

# Creates a RAM disk big enough to hold two copies of the test directory
# structure.
cat << EOF > "${TMP}/ramdisk.py"
class RAMBlockDev:
    def __init__(self, block_size, num_blocks):
        self.block_size = block_size
        self.data = bytearray(block_size * num_blocks)

    def readblocks(self, block_num, buf):
        for i in range(len(buf)):
            buf[i] = self.data[block_num * self.block_size + i]

    def writeblocks(self, block_num, buf):
        for i in range(len(buf)):
            self.data[block_num * self.block_size + i] = buf[i]

    def ioctl(self, op, arg):
        if op == 4: # get number of blocks
            return len(self.data) // self.block_size
        if op == 5: # get block size
            return self.block_size

import os

bdev = RAMBlockDev(512, 50)
os.VfsFat.mkfs(bdev)
os.mount(bdev, '/ramdisk')
os.chdir('/ramdisk')
EOF

# setup 
echo -----
$MPREMOTE $MPREMOTE_FLAGS run "${TMP}/ramdisk.py"
$MPREMOTE $MPREMOTE_FLAGS resume ls

echo -----
echo "empty tree"
$MPREMOTE $MPREMOTE_FLAGS resume tree :

echo -----
$MPREMOTE $MPREMOTE_FLAGS resume touch :a.py + touch :b.py  
$MPREMOTE $MPREMOTE_FLAGS resume mkdir :foo + touch :foo/aa.py + touch :foo/ba.py

echo "small tree - :" 
$MPREMOTE $MPREMOTE_FLAGS resume tree :

echo -----
echo "no path" 
$MPREMOTE $MPREMOTE_FLAGS resume tree 

echo -----
echo "path = '.'" 
$MPREMOTE $MPREMOTE_FLAGS resume tree .

echo -----
echo "path = ':.'" 
$MPREMOTE $MPREMOTE_FLAGS resume tree :.


echo -----
echo "multiple trees" 
$MPREMOTE $MPREMOTE_FLAGS resume mkdir :bar + touch :bar/aaa.py + touch :bar/bbbb.py
$MPREMOTE $MPREMOTE_FLAGS resume mkdir :bar/baz + touch :bar/baz/aaa.py + touch :bar/baz/bbbb.py
$MPREMOTE $MPREMOTE_FLAGS resume mkdir :bar/baz/quux + touch :bar/baz/quux/aaa.py + touch :bar/baz/quux/bbbb.py
$MPREMOTE $MPREMOTE_FLAGS resume mkdir :bar/baz/quux/xen + touch :bar/baz/quux/xen/aaa.py

$MPREMOTE $MPREMOTE_FLAGS resume tree

echo -----
echo single path
$MPREMOTE $MPREMOTE_FLAGS resume tree :foo

echo -----
echo "multiple paths" 
$MPREMOTE $MPREMOTE_FLAGS resume tree :foo :bar

echo -----
echo "subtree" 
$MPREMOTE $MPREMOTE_FLAGS resume tree bar/baz

echo -----
echo mountpoint
$MPREMOTE $MPREMOTE_FLAGS resume tree :/ramdisk

echo -----
echo non-existent folder : error
$MPREMOTE $MPREMOTE_FLAGS resume tree :not_there || echo "expect error: $?"

echo -----
echo file : error 
$MPREMOTE $MPREMOTE_FLAGS resume tree :a.py || echo "expect error: $?"

echo -----
echo "tree -s :"
mkdir -p "${TMP}/data"
dd if=/dev/zero of="${TMP}/data/file1.txt" bs=1 count=20 > /dev/null 2>&1
dd if=/dev/zero of="${TMP}/data/file2.txt" bs=1 count=204 > /dev/null 2>&1
dd if=/dev/zero of="${TMP}/data/file3.txt" bs=1 count=1096 > /dev/null 2>&1
dd if=/dev/zero of="${TMP}/data/file4.txt" bs=1 count=2192 > /dev/null 2>&1

$MPREMOTE $MPREMOTE_FLAGS resume cp -r "${TMP}/data" :
$MPREMOTE $MPREMOTE_FLAGS resume tree -s :
echo -----
echo "tree -s"
$MPREMOTE $MPREMOTE_FLAGS resume tree -s
echo -----
$MPREMOTE $MPREMOTE_FLAGS resume tree --human :
echo -----
$MPREMOTE $MPREMOTE_FLAGS resume tree -s --human : || echo "expect error: $?"
echo -----

