#!/bin/bash
set -e

# Get the test directory (where this script and ramdisk.py are located)
TEST_DIR=$(dirname $0)

echo -----
# Test rm -r functionality
# start with a fresh ramdisk before each test
# rm -r MCU current working directory
$MPREMOTE run "${TEST_DIR}/ramdisk.py"
$MPREMOTE resume touch :a.py
$MPREMOTE resume touch :b.py
$MPREMOTE resume cp -r "${TMP}/package" :
$MPREMOTE resume rm -r -v :
$MPREMOTE resume ls :
$MPREMOTE resume ls :/ramdisk

echo -----
# rm -r relative subfolder
$MPREMOTE run "${TEST_DIR}/ramdisk.py"
$MPREMOTE resume touch :a.py
$MPREMOTE resume mkdir :testdir
$MPREMOTE resume cp -r "${TMP}/package" :testdir/package
$MPREMOTE resume ls :testdir
$MPREMOTE resume ls :testdir/package
$MPREMOTE resume rm -r :testdir/package
$MPREMOTE resume ls :/ramdisk
$MPREMOTE resume ls :testdir

echo -----
# rm -r non-existent path
$MPREMOTE run "${TEST_DIR}/ramdisk.py"
$MPREMOTE resume ls :
$MPREMOTE resume rm -r :nonexistent || echo "expect error"

echo -----
# rm -r relative mountpoint
$MPREMOTE run "${TEST_DIR}/ramdisk.py"
$MPREMOTE resume touch :a.py
$MPREMOTE resume touch :b.py
$MPREMOTE resume cp -r "${TMP}/package" :
$MPREMOTE resume exec "import os;os.chdir('/')"
$MPREMOTE resume rm -r -v :ramdisk
$MPREMOTE resume ls :/ramdisk

echo -----
# rm -r absolute mountpoint
$MPREMOTE run "${TEST_DIR}/ramdisk.py"
$MPREMOTE resume touch :a.py
$MPREMOTE resume touch :b.py
$MPREMOTE resume cp -r "${TMP}/package" :
$MPREMOTE resume exec "import os;os.chdir('/')"
$MPREMOTE resume rm -r -v :/ramdisk
$MPREMOTE resume ls :/ramdisk

echo -----
# try to delete existing folder in mounted filesystem
$MPREMOTE mount "${TMP}" + rm -rv :package || echo "expect error"
echo -----
# fs without command should raise error
$MPREMOTE fs 2>/dev/null || echo "expect error: $?"
echo -----
