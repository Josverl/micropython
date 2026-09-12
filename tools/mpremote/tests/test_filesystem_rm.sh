#!/bin/bash
set -e

TEST_DIR=$(dirname $0)

$MPREMOTE exec "import os; os.VfsFat" || { echo "SKIP"; exit 0; }

mkdir -p "${TMP}/package/subpackage"
printf 'from .x import x\nfrom .subpackage import y\n' > "${TMP}/package/__init__.py"
printf 'def x():\n  print("x")\n' > "${TMP}/package/x.py"
printf 'from .y import y\n' > "${TMP}/package/subpackage/__init__.py"
printf 'def y():\n  print("y")\n' > "${TMP}/package/subpackage/y.py"

echo -----
# Remove the current working directory contents.
$MPREMOTE soft-reset run "${TEST_DIR}/ramdisk.py"
$MPREMOTE touch :a.py
$MPREMOTE touch :b.py
$MPREMOTE cp -r "${TMP}/package" :
$MPREMOTE rm -r -v :
$MPREMOTE ls :
$MPREMOTE ls :/ramdisk

echo -----
# Remove a relative subdirectory.
$MPREMOTE soft-reset run "${TEST_DIR}/ramdisk.py"
$MPREMOTE touch :a.py
$MPREMOTE mkdir :testdir
$MPREMOTE cp -r "${TMP}/package" :testdir/package
$MPREMOTE ls :testdir
$MPREMOTE ls :testdir/package
$MPREMOTE rm -r :testdir/package
$MPREMOTE ls :/ramdisk
$MPREMOTE ls :testdir

echo -----
# Remove a non-existent path.
$MPREMOTE soft-reset run "${TEST_DIR}/ramdisk.py"
$MPREMOTE ls :
$MPREMOTE rm -r :nonexistent || echo "expect error"

echo -----
# Do not remove a relative VFS mount point itself.
$MPREMOTE soft-reset run "${TEST_DIR}/ramdisk.py"
$MPREMOTE touch :a.py
$MPREMOTE touch :b.py
$MPREMOTE cp -r "${TMP}/package" :
$MPREMOTE exec "import os;os.chdir('/')"
$MPREMOTE rm -r -v :ramdisk
$MPREMOTE ls :/ramdisk

echo -----
# Do not remove an absolute VFS mount point itself.
$MPREMOTE soft-reset run "${TEST_DIR}/ramdisk.py"
$MPREMOTE touch :a.py
$MPREMOTE touch :b.py
$MPREMOTE cp -r "${TMP}/package" :
$MPREMOTE exec "import os;os.chdir('/')"
$MPREMOTE rm -r -v :/ramdisk
$MPREMOTE ls :/ramdisk

echo -----
# Do not recursively remove a directory from a mounted host filesystem.
$MPREMOTE mount "${TMP}" + rm -rv :package || echo "expect error"

echo -----
# Invoking fs without a command should fail.
$MPREMOTE fs 2>/dev/null || echo "expect error: $?"

echo -----