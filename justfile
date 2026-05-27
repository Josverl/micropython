# t1 - typing 1 

build_t1:
    mpbuild clean unix-typing1
    mpbuild build unix-typing1

build_t2:
    mpbuild clean unix-typing2
    mpbuild clean unix-typing2b
    mpbuild build unix-typing2
    mpbuild build unix-typing2b

run_t1:
    ports/unix/build-typing1/micropython 


[working-directory: 'tests']
test_t1 tests="typing typing/pep":
    echo 'Running tests...'
    MICROPY_MICROPYTHON=/home/jos/micropython.worktrees/runtime_typing/ports/unix/build-typing1/micropython \
        ./run-tests.py -d {{tests}}

[working-directory: 'tests']
test_t2 tests="typing typing/pep":
    echo 'Running tests...'
    MICROPY_MICROPYTHON=/home/jos/micropython.worktrees/runtime_typing/ports/unix/build-typing2/micropython \
        ./run-tests.py -d {{tests}}

[working-directory: 'tests']
test_t3 tests="typing typing/pep":
    echo 'Running tests...'
    MICROPY_MICROPYTHON=/home/jos/micropython.worktrees/runtime_typing/ports/unix/build-typing3/micropython \
        ./run-tests.py -d {{tests}}



report tests="typing typing/pep":
    uv run tools/make_report.py \
        --variant standard=/home/jos/micropython.worktrees/runtime_typing/ports/unix/build-standard/micropython \
        --variant 1_mp-stubs=/home/jos/micropython.worktrees/runtime_typing/ports/unix/build-typing1/micropython \
        --variant 2_typing_bundle=/home/jos/micropython.worktrees/runtime_typing/ports/unix/build-typing2/micropython \
        --variant 2_typing_bundle_XL=/home/jos/micropython.worktrees/runtime_typing/ports/unix/build-typing2b/micropython \
        --variant 3_builtintypingmodule=/home/jos/micropython.worktrees/runtime_typing/ports/unix/build-typing3/micropython \
        --out report.md \
        {{tests}}

