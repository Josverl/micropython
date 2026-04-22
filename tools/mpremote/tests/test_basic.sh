#!/bin/bash
set -e

# Get the test directory (where this script and ramdisk.py are located)
TEST_DIR=$(dirname $0)

# retrieve connected port and device id
$MPREMOTE devs > "${TMP}/devices.txt"
dev_port=$(awk 'NR==1 {print $1}' "${TMP}/devices.txt")
dev_id=$(awk 'NR==1 {print $2}' "${TMP}/devices.txt")

echo -1---
# connect to specific port:
$MPREMOTE connect "${dev_port}" exec "print('connect <port>')" 
echo -2---
# connect to specific port:
$MPREMOTE connect "port:${dev_port}" exec "print('connect port:<port>')" 
echo -3---
# specific device id:
# only if device id is not "None"
if [ "$dev_id" != "None" ]; then
    $MPREMOTE connect "id:${dev_id}" exec "print('connect id:')"
else
    echo "SKIP : connect id: as device id is None"
fi
echo -4---
# mismatched  port:
$MPREMOTE connect "port:/dev/tty/ACM1234dead" exec "print('connect wrong port:')" || echo "expect error: $?"
echo -5---
# mismatched  device id:
$MPREMOTE connect "id:1234deadbeef" exec "print('connect wrong id:')" || echo "expect error: $?"

echo -6---
# set & get time
$MPREMOTE rtc --set && echo "set time success $?"
$MPREMOTE rtc > /dev/null && echo "get time success $?"

echo -----
