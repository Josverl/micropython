#!/bin/bash
set -e

TEST_DIR=$(dirname $0)
MPREMOTE=${TEST_DIR}/../mpremote.py

if [ -z "$1" ]; then
    # Find tests matching test_*.sh
    TESTS=${TEST_DIR}/test_*.sh
else
    COVERAGE=false
    TESTS=()
    for arg in "$@"; do
        if [ "$arg" == "--coverage" ]; then
            COVERAGE=true
        else
            TESTS+=("$arg")
        fi
    done
    if [ ${#TESTS[@]} -eq 0 ]; then
        TESTS=${TEST_DIR}/test_*.sh
    fi
fi

if [ "$COVERAGE" = true ]; then
    # Check if coverage is installed
    if ! command -v coverage &> /dev/null; then
        echo "Coverage is not installed. Please install it to run tests with coverage."
        exit 1
    fi
    echo "Start coverage"
    # coverage erase
fi

for t in $TESTS; do
    TMP=$(mktemp -d)
    echo -n "${t}: "
    if [ "$COVERAGE" = true ]; then
        MPREMOTE="coverage run --append --context=${t} ${TEST_DIR}/../mpremote.py"
    fi
    # Strip CR and replace the random temp dir with a token.
    if env MPREMOTE="${MPREMOTE}" TMP="${TMP}" "${t}" 2>&1 | tr -d '\r' | sed "s,${TMP},"'${TMP},g' > "${t}.out"; then
        if diff "${t}.out" "${t}.exp" > /dev/null; then
            echo "OK"
        else
            echo "FAIL"
            diff "${t}.out" "${t}.exp" || true
        fi
    else
        echo "CRASH"
    fi
    rm -r "${TMP}"
done

if [ "$COVERAGE" = true ]; then
    # Generate coverage reports
    coverage report -m 
    coverage html --show-contexts
    coverage xml
fi
