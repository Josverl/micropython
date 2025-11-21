#!/usr/bin/env python3
"""Test mpremote CLI commands: exec, eval, and run.

Tests both sync (default) and async (--async) modes.
Based on test_eval_exec_run.sh
"""

import tempfile

import pytest
from helpers import run_mpremote, write_script


@pytest.mark.cli
def test_exec_simple(mpremote_cmd, cli_mode):
    """Test simple exec command."""
    result = run_mpremote(mpremote_cmd, "exec", "print('mpremote')")

    assert result.returncode == 0, f"Command failed: {result.stderr}"
    assert "mpremote" in result.stdout, f"Expected 'mpremote' in output, got: {result.stdout}"


@pytest.mark.cli
def test_exec_with_sleep(mpremote_cmd, cli_mode):
    """Test exec command with sleep."""
    result = run_mpremote(
        mpremote_cmd,
        "exec",
        "print('before sleep'); import time; time.sleep(0.1); print('after sleep')",
    )

    assert result.returncode == 0, f"Command failed: {result.stderr}"
    assert "before sleep" in result.stdout
    assert "after sleep" in result.stdout


@pytest.mark.cli
def test_exec_no_follow(mpremote_cmd, cli_mode):
    """Test exec command with --no-follow flag."""
    result = run_mpremote(
        mpremote_cmd,
        "exec",
        "--no-follow",
        "print('before sleep'); import time; time.sleep(0.1); print('after sleep')",
    )

    assert result.returncode == 0, f"Command failed: {result.stderr}"
    # With --no-follow, we don't wait for output, so we might not see it


@pytest.mark.cli
def test_eval_simple(mpremote_cmd, cli_mode):
    """Test simple eval command."""
    result = run_mpremote(mpremote_cmd, "eval", "1+2")

    assert result.returncode == 0, f"Command failed: {result.stderr}"
    assert "3" in result.stdout, f"Expected '3' in output, got: {result.stdout}"


@pytest.mark.cli
def test_eval_complex(mpremote_cmd, cli_mode):
    """Test eval command with complex expression."""
    result = run_mpremote(mpremote_cmd, "eval", "[{'a': 'b'}, (1,2,3,), True]")

    assert result.returncode == 0, f"Command failed: {result.stderr}"
    # Check for key parts of the output
    assert "'a'" in result.stdout or '"a"' in result.stdout
    assert "'b'" in result.stdout or '"b"' in result.stdout
    assert "1" in result.stdout
    assert "2" in result.stdout
    assert "3" in result.stdout
    assert "True" in result.stdout


@pytest.mark.cli
def test_run_simple(mpremote_cmd, temp_script, cli_mode):
    """Test run command with simple script."""
    # Create script
    write_script(temp_script, 'print("run")')

    result = run_mpremote(mpremote_cmd, "run", temp_script)

    assert result.returncode == 0, f"Command failed: {result.stderr}"
    assert "run" in result.stdout, f"Expected 'run' in output, got: {result.stdout}"


@pytest.mark.cli
def test_run_with_loop(mpremote_cmd, temp_script, cli_mode):
    """Test run command with loop and sleep."""
    # Create script with loop
    write_script(
        temp_script,
        """
        import time
        for i in range(3):
            time.sleep(0.1)
            print("run")
    """,
    )

    result = run_mpremote(mpremote_cmd, "run", temp_script)

    assert result.returncode == 0, f"Command failed: {result.stderr}"
    # Should see "run" printed 3 times
    run_count = result.stdout.count("run")
    assert run_count == 3, f"Expected 3 'run' outputs, got {run_count}: {result.stdout}"


@pytest.mark.cli
def test_run_no_follow(mpremote_cmd, temp_script, cli_mode):
    """Test run command with --no-follow flag."""
    # Create script with loop
    write_script(
        temp_script,
        """
        import time
        for i in range(3):
            time.sleep(0.1)
            print("run")
    """,
    )

    result = run_mpremote(mpremote_cmd, "run", "--no-follow", temp_script)

    assert result.returncode == 0, f"Command failed: {result.stderr}"
    # With --no-follow, we don't wait for output


@pytest.mark.cli
def test_all_commands_comprehensive(mpremote_cmd, temp_script, cli_mode):
    """Comprehensive test running all commands in sequence."""
    print(f"\n{'=' * 60}")
    print(f"Comprehensive CLI test ({cli_mode} mode)")
    print(f"{'=' * 60}")

    # Test 1: exec
    result = run_mpremote(mpremote_cmd, "exec", "print('test1')")
    assert result.returncode == 0
    assert "test1" in result.stdout

    # Test 2: exec with sleep
    result = run_mpremote(
        mpremote_cmd, "exec", "print('before'); import time; time.sleep(0.05); print('after')"
    )
    assert result.returncode == 0
    assert "before" in result.stdout and "after" in result.stdout

    # Test 3: eval
    result = run_mpremote(mpremote_cmd, "eval", "42")
    assert result.returncode == 0
    assert "42" in result.stdout

    # Test 4: run
    write_script(temp_script, 'print("script")')
    result = run_mpremote(mpremote_cmd, "run", temp_script)
    assert result.returncode == 0
    assert "script" in result.stdout

    print(f"{'=' * 60}\n")
