#!/bin/bash
set -e

if [[ "$($MPREMOTE romfs query)" == "ROMFS is not enabled on this device" ]] ; then
    echo "SKIP"
    exit 0
fi
####################################################################################
# ROMFS 
####################################################################################
echo -1---
# create a romfs with some data 
$MPREMOTE romfs -o "${TMP}/image.romfs" build assets/romfs_source  

echo -2---
# deploy the romfs to the device
$MPREMOTE romfs deploy "${TMP}/image.romfs"
$MPREMOTE ls :/rom

echo -3---
# too much data 
mkdir -p "${TMP}/bigdata"
dd if=/dev/urandom of="${TMP}/bigdata/file21.bin" bs=1 count=500000 > /dev/null 2>&1
dd if=/dev/urandom of="${TMP}/bigdata/file22.bin" bs=1 count=600000 > /dev/null 2>&1
dd if=/dev/urandom of="${TMP}/bigdata/file23.bin" bs=1 count=700000 > /dev/null 2>&1
dd if=/dev/urandom of="${TMP}/bigdata/file24.bin" bs=1 count=800000 > /dev/null 2>&1
dd if=/dev/urandom of="${TMP}/bigdata/file25.bin" bs=1 count=900000 > /dev/null 2>&1

$MPREMOTE romfs -o "${TMP}/bigdata.romfs" build "${TMP}/bigdata" 
# deploy the romfs to the device
$MPREMOTE romfs deploy "${TMP}/bigdata.romfs" || echo "expect error: $?"
echo -4---
# not a romfs
dd if=/dev/urandom of="${TMP}/notreally.romfs" bs=1 count=5000 > /dev/null 2>&1
$MPREMOTE romfs deploy "${TMP}/notreally.romfs" || echo "expect error: $?"

echo -----
