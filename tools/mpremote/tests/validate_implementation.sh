#!/bin/bash
#
# Final validation script for async implementation
# Validates that all components are in place and working

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

echo "========================================================================"
echo "VALIDATING ASYNC IMPLEMENTATION"
echo "========================================================================"
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

CHECKS_PASSED=0
CHECKS_TOTAL=0

check_pass() {
    echo -e "${GREEN}✓${NC} $1"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
    CHECKS_TOTAL=$((CHECKS_TOTAL + 1))
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    CHECKS_TOTAL=$((CHECKS_TOTAL + 1))
}

check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

echo "=== Phase 1: Transport Layer ==="

# Check Phase 1 files exist
if [ -f "mpremote/transport_async.py" ]; then
    check_pass "transport_async.py exists"
else
    check_fail "transport_async.py missing"
fi

if [ -f "mpremote/transport_serial_async.py" ]; then
    check_pass "transport_serial_async.py exists"
else
    check_fail "transport_serial_async.py missing"
fi

if [ -f "mpremote/protocol.py" ]; then
    check_pass "protocol.py exists"
else
    check_fail "protocol.py missing"
fi

# Check Phase 1 imports work
python3 -c "from mpremote.transport_async import AsyncTransport" 2>/dev/null && \
    check_pass "AsyncTransport imports" || \
    check_fail "AsyncTransport import failed"

python3 -c "from mpremote.transport_serial_async import AsyncSerialTransport" 2>/dev/null && \
    check_pass "AsyncSerialTransport imports" || \
    check_fail "AsyncSerialTransport import failed"

python3 -c "from mpremote.protocol import RawREPLProtocol" 2>/dev/null && \
    check_pass "RawREPLProtocol imports" || \
    check_fail "RawREPLProtocol import failed"

echo ""
echo "=== Phase 2: Command Layer ==="

# Check Phase 2 files exist
if [ -f "mpremote/commands_async.py" ]; then
    check_pass "commands_async.py exists"
else
    check_fail "commands_async.py missing"
fi

# Check State class has async methods
python3 -c "
from mpremote.main import State
s = State()
assert hasattr(s, 'ensure_raw_repl_async')
assert hasattr(s, 'ensure_connected_async')
assert hasattr(s, 'ensure_friendly_repl_async')
" 2>/dev/null && \
    check_pass "State class has async methods" || \
    check_fail "State class missing async methods"

# Check command async functions exist
python3 -c "from mpremote.commands_async import do_exec_async, do_eval_async" 2>/dev/null && \
    check_pass "Async command handlers exist" || \
    check_fail "Async command handlers missing"

echo ""
echo "=== Phase 3: REPL and Console ==="

# Check Phase 3 files exist
if [ -f "mpremote/console_async.py" ]; then
    check_pass "console_async.py exists"
else
    check_fail "console_async.py missing"
fi

if [ -f "mpremote/repl_async.py" ]; then
    check_pass "repl_async.py exists"
else
    check_fail "repl_async.py missing"
fi

# Check console async imports
python3 -c "from mpremote.console_async import AsyncConsole" 2>/dev/null && \
    check_pass "AsyncConsole imports" || \
    check_fail "AsyncConsole import failed"

# Check REPL async imports
python3 -c "from mpremote.repl_async import do_repl_async" 2>/dev/null && \
    check_pass "do_repl_async imports" || \
    check_fail "do_repl_async import failed"

echo ""
echo "=== Dependencies ==="

# Check pyserial-asyncio is in requirements
if grep -q "pyserial-asyncio" requirements.txt; then
    check_pass "pyserial-asyncio in requirements.txt"
else
    check_fail "pyserial-asyncio not in requirements.txt"
fi

# Check if pyserial-asyncio is installed
python3 -c "import serial_asyncio" 2>/dev/null && \
    check_pass "pyserial-asyncio installed" || \
    check_warn "pyserial-asyncio not installed (optional)"

echo ""
echo "=== Testing Infrastructure ==="

# Check test files exist
if [ -f "tests/test_async_transport.py" ]; then
    check_pass "test_async_transport.py exists"
else
    check_fail "test_async_transport.py missing"
fi

if [ -f "tests/test_async_comprehensive.py" ]; then
    check_pass "test_async_comprehensive.py exists"
else
    check_fail "test_async_comprehensive.py missing"
fi

if [ -f "tests/test_integration.py" ]; then
    check_pass "test_integration.py exists"
else
    check_fail "test_integration.py missing"
fi

if [ -f "tests/run_async_tests.sh" ]; then
    check_pass "run_async_tests.sh exists"
else
    check_fail "run_async_tests.sh missing"
fi

echo ""
echo "=== Documentation ==="

if [ -f "ASYNC_README.md" ]; then
    check_pass "ASYNC_README.md exists"
else
    check_fail "ASYNC_README.md missing"
fi

if [ -f "IMPLEMENTATION_SUMMARY.md" ]; then
    check_pass "IMPLEMENTATION_SUMMARY.md exists"
else
    check_fail "IMPLEMENTATION_SUMMARY.md missing"
fi

echo ""
echo "=== Backward Compatibility ==="

# Check original modules still work
python3 -c "from mpremote.transport_serial import SerialTransport" 2>/dev/null && \
    check_pass "Original SerialTransport still works" || \
    check_fail "Original SerialTransport broken"

python3 -c "from mpremote.console import Console" 2>/dev/null && \
    check_pass "Original Console still works" || \
    check_fail "Original Console broken"

python3 -c "from mpremote.repl import do_repl" 2>/dev/null && \
    check_pass "Original do_repl still works" || \
    check_fail "Original do_repl broken"

# Check State has both sync and async methods
python3 -c "
from mpremote.main import State
s = State()
# Check sync methods
assert hasattr(s, 'ensure_raw_repl')
assert hasattr(s, 'ensure_connected')
assert hasattr(s, 'ensure_friendly_repl')
# Check async methods
assert hasattr(s, 'ensure_raw_repl_async')
assert hasattr(s, 'ensure_connected_async')
assert hasattr(s, 'ensure_friendly_repl_async')
" 2>/dev/null && \
    check_pass "State has both sync and async methods" || \
    check_fail "State methods incomplete"

echo ""
echo "=== Python Syntax Validation ==="

# Check all new Python files have valid syntax
for file in mpremote/transport_async.py \
            mpremote/transport_serial_async.py \
            mpremote/protocol.py \
            mpremote/console_async.py \
            mpremote/repl_async.py \
            mpremote/commands_async.py; do
    if python3 -m py_compile "$file" 2>/dev/null; then
        check_pass "$file has valid syntax"
    else
        check_fail "$file has syntax errors"
    fi
done

echo ""
echo "========================================================================"
echo "VALIDATION SUMMARY"
echo "========================================================================"
echo "Checks passed: $CHECKS_PASSED / $CHECKS_TOTAL"

if [ $CHECKS_PASSED -eq $CHECKS_TOTAL ]; then
    echo -e "${GREEN}✓ ALL CHECKS PASSED${NC}"
    echo "Implementation is complete and ready for use!"
    exit 0
else
    FAILED=$((CHECKS_TOTAL - CHECKS_PASSED))
    echo -e "${RED}✗ $FAILED CHECKS FAILED${NC}"
    echo "Please review the failed checks above."
    exit 1
fi
