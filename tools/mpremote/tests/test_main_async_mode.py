#!/usr/bin/env python3
"""Unit tests for mpremote main async flag parsing."""

from mpremote import main as mpremote_main


def test_default_mode_no_flags():
    use_async, args = mpremote_main._determine_async_mode(["exec", "1"], env={})
    assert use_async is False
    assert args == ["exec", "1"]


def test_environment_enables_async():
    use_async, args = mpremote_main._determine_async_mode(["exec"], env={"MPREMOTE_ASYNC": "1"})
    assert use_async is True
    assert args == ["exec"]


def test_environment_false_by_default():
    use_async, args = mpremote_main._determine_async_mode([], env={"MPREMOTE_ASYNC": "0"})
    assert use_async is False
    assert args == []


def test_cli_flag_overrides_env_true():
    use_async, args = mpremote_main._determine_async_mode(
        ["--no-async", "exec"], env={"MPREMOTE_ASYNC": "1"}
    )
    assert use_async is False
    assert args == ["exec"]


def test_cli_flag_last_wins():
    use_async, args = mpremote_main._determine_async_mode(
        ["--async", "exec", "--no-async", "run"], env={}
    )
    assert use_async is False
    assert args == ["exec", "run"]


def test_cli_flag_after_command_is_removed():
    use_async, args = mpremote_main._determine_async_mode(["exec", "foo", "--async"], env={})
    assert use_async is True
    assert args == ["exec", "foo"]
