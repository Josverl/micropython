#!/bin/bash
# Simulate Windows configuration: CPYTHON_COMPAT=1, BYTES_DECODE_IGNORE=0

# Create a temporary variant
mkdir -p variants/test_windows_sim
cat > variants/test_windows_sim/mpconfigvariant.h << 'VARIANT_EOF'
// Simulate Windows: CPYTHON_COMPAT enabled, but BYTES_DECODE_IGNORE disabled
#define MICROPY_CONFIG_ROM_LEVEL (MICROPY_CONFIG_ROM_LEVEL_CORE_FEATURES)
#define MICROPY_CPYTHON_COMPAT (1)
#define MICROPY_PY_BUILTINS_BYTES_DECODE_IGNORE (0)
VARIANT_EOF

cat > variants/test_windows_sim/mpconfigvariant.mk << 'VARIANT_MK_EOF'
# Minimal variant config
VARIANT_MK_EOF

# Build
make VARIANT=test_windows_sim clean
make VARIANT=test_windows_sim

# Test
echo "=== Testing simulated Windows build ==="
./build-test_windows_sim/micropython ../../tests/basics/bytes_decode_errors.py

# Cleanup
rm -rf variants/test_windows_sim
make VARIANT=test_windows_sim clean
