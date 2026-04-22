#!/bin/bash
set -e

####################################################################################
#  mpremote mip
####################################################################################

echo -1---
# name, name@version
$MPREMOTE mip install __future__
$MPREMOTE mip install __future__@0.1.0

echo -2---
# github:org/repo, github:org/repo@branch,
$MPREMOTE mip install github:micropython/micropython-lib/python-stdlib/__future__/__future__.py
$MPREMOTE mip install github:micropython/micropython-lib/python-stdlib/__future__/__future__.py@master
$MPREMOTE mip install github:micropython/micropython-lib/python-stdlib/__future__/__future__.py@v1.28.0

echo -3---
# github:org/repo/<package>.json
$MPREMOTE mip install github:josverl/micropython-stubs/mip/typing_mpy.json

# TODO : gitlab, codeberg
# - package with dependencies
#  gitlab:org/repo, gitlab:org/repo@branch

echo -----
