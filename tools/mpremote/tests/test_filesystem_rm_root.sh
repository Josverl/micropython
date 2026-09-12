#!/bin/bash
set -e

TEST_DIR=$(dirname $0)

# The unix port exposes the host filesystem directly, so never run this test
# through a socket-based unix-port connection.
if [[ "${MPREMOTE_DEVICE}" == rfc2217://* ]] || [[ "${MPREMOTE_DEVICE}" == socket://* ]]; then
    echo "SKIP"
    exit 0
fi

$MPREMOTE exec "import os; os.VfsFat" || { echo "SKIP"; exit 0; }

mkdir -p "${TMP}/package/subpackage"
printf 'from .x import x\nfrom .subpackage import y\n' > "${TMP}/package/__init__.py"
printf 'def x():\n  print("x")\n' > "${TMP}/package/x.py"
printf 'from .y import y\n' > "${TMP}/package/subpackage/__init__.py"
printf 'def y():\n  print("y")\n' > "${TMP}/package/subpackage/y.py"

echo -----
# Removing the absolute root must be rejected.
$MPREMOTE soft-reset run "${TEST_DIR}/ramdisk.py"
$MPREMOTE touch :a.py
$MPREMOTE touch :b.py
$MPREMOTE cp -r "${TMP}/package" :
$MPREMOTE cp -r "${TMP}/package" :package2
$MPREMOTE rm -r :/ || echo "expect error"
$MPREMOTE ls :
$MPREMOTE ls :/ramdisk