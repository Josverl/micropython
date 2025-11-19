#!/bin/bash
#
# Test runner for async transport implementation
# Runs all async-related tests

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

echo "========================================================================"
echo "RUNNING ALL ASYNC TRANSPORT TESTS"
echo "========================================================================"
echo ""

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Track results
TOTAL_TESTS=0
PASSED_TESTS=0

# Function to run a test
run_test() {
    local test_name="$1"
    local test_file="$2"
    
    echo "----------------------------------------"
    echo "Running: $test_name"
    echo "----------------------------------------"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    if python3 "$test_file"; then
        echo -e "${GREEN}✓ $test_name PASSED${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        echo ""
        return 0
    else
        echo -e "${RED}✗ $test_name FAILED${NC}"
        echo ""
        return 1
    fi
}

# Run all tests
run_test "Basic Async Transport Tests" "tests/test_async_transport.py"
run_test "Comprehensive Async Tests" "tests/test_async_comprehensive.py"
run_test "Integration Tests" "tests/test_integration.py"

# Summary
echo "========================================================================"
echo "TEST SUMMARY"
echo "========================================================================"
echo "Total tests: $TOTAL_TESTS"
echo "Passed: $PASSED_TESTS"
echo "Failed: $((TOTAL_TESTS - PASSED_TESTS))"

if [ $PASSED_TESTS -eq $TOTAL_TESTS ]; then
    echo -e "${GREEN}✓ ALL TESTS PASSED${NC}"
    echo "========================================================================"
    exit 0
else
    echo -e "${RED}✗ SOME TESTS FAILED${NC}"
    echo "========================================================================"
    exit 1
fi
