#!/bin/bash
set -e

# The eval command will continue the state of the exec.
echo -----
$MPREMOTE $MPREMOTE_FLAGS exec "a = 'hello'" eval "a"

# Automatic soft reset. `a` will trigger NameError.
echo -----
$MPREMOTE $MPREMOTE_FLAGS eval "a" || true

# Resume will skip soft reset.
echo -----
$MPREMOTE $MPREMOTE_FLAGS exec "a = 'resume'"
$MPREMOTE $MPREMOTE_FLAGS resume eval "a"

# The eval command will continue the state of the exec.
echo -----
$MPREMOTE $MPREMOTE_FLAGS exec "a = 'soft-reset'" eval "a" soft-reset eval "1+1" eval "a" || true

# A disconnect will trigger auto-reconnect.
echo -----
$MPREMOTE $MPREMOTE_FLAGS eval "1+2" disconnect eval "2+3"
