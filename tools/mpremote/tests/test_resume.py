#!/usr/bin/env python3
"""Pytest replacements for legacy test_resume.sh."""

import pytest
from helpers import run_mpremote


@pytest.mark.cli
def test_exec_eval_chain_preserves_state(mpremote_cmd, cli_mode):
    """exec + eval within one invocation should keep interpreter state."""

    result = run_mpremote(mpremote_cmd, "exec", "a = 'hello'", "eval", "a")
    assert result.returncode == 0, result.stderr
    assert "hello" in result.stdout


@pytest.mark.cli
def test_auto_soft_reset_clears_state(mpremote_cmd, cli_mode):
    """A fresh eval should see a soft-reset and miss prior state."""

    result = run_mpremote(mpremote_cmd, "eval", "a")
    assert result.returncode != 0
    assert "NameError" in (result.stdout + result.stderr)


@pytest.mark.cli
def test_resume_skips_soft_reset(mpremote_cmd, cli_mode):
    result = run_mpremote(mpremote_cmd, "exec", "a = 'resume'")
    assert result.returncode == 0

    result = run_mpremote(mpremote_cmd, "resume", "eval", "a")
    assert result.returncode == 0
    assert "resume" in result.stdout


@pytest.mark.cli
def test_soft_reset_command(mpremote_cmd, cli_mode):
    cmd = [
        "exec",
        "a = 'soft-reset'",
        "eval",
        "a",
        "soft-reset",
        "eval",
        "1+1",
        "eval",
        "a",
    ]
    result = run_mpremote(mpremote_cmd, *cmd)
    assert result.returncode != 0
    assert "soft-reset" in result.stdout
    assert "2" in result.stdout
    assert "NameError" in (result.stdout + result.stderr)


@pytest.mark.cli
def test_disconnect_triggers_reconnect(mpremote_cmd, cli_mode):
    result = run_mpremote(
        mpremote_cmd,
        "eval",
        "1+2",
        "disconnect",
        "eval",
        "2+3",
    )
    assert result.returncode == 0
    assert "3" in result.stdout
    assert "5" in result.stdout
