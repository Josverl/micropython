import pytest
from mpremote import main as mpremote_main


class DummyState:
    def __init__(self, use_async):
        self.use_async = use_async


def test_run_repl_sync_when_async_disabled(monkeypatch):
    """_run_repl should invoke the sync REPL when async mode is off."""

    state = DummyState(use_async=False)
    repl_args = object()
    called = {}

    def fake_sync_repl(state_arg, args_arg):
        called["sync"] = (state_arg, args_arg)
        return "sync-result"

    monkeypatch.setattr(mpremote_main, "do_repl", fake_sync_repl)

    async def unexpected_async(*_):  # pragma: no cover - defensive
        pytest.fail("async repl should not run when async mode is disabled")

    monkeypatch.setattr(mpremote_main, "do_repl_async", unexpected_async)

    result = mpremote_main._run_repl(state, repl_args)

    assert result == "sync-result"
    assert called["sync"] == (state, repl_args)


def test_run_repl_async_path(monkeypatch):
    """_run_repl should await the async REPL when async mode is enabled."""

    state = DummyState(use_async=True)
    repl_args = object()
    called = {}

    async def fake_async_repl(state_arg, args_arg):
        called["async"] = (state_arg, args_arg)
        return "async-result"

    def fake_sync_repl(*_):
        pytest.fail("sync repl should not run when async repl succeeds")

    monkeypatch.setattr(mpremote_main, "do_repl_async", fake_async_repl)
    monkeypatch.setattr(mpremote_main, "do_repl", fake_sync_repl)

    result = mpremote_main._run_repl(state, repl_args)

    assert result == "async-result"
    assert called["async"] == (state, repl_args)


def test_run_repl_falls_back_on_async_failure(monkeypatch, capsys):
    """If the async REPL raises a capability error, fall back to sync."""

    state = DummyState(use_async=True)
    repl_args = object()
    called = {}

    async def fake_async_repl(*_):
        raise TypeError("missing read_async")

    def fake_sync_repl(state_arg, args_arg):
        called["sync"] = (state_arg, args_arg)
        return "sync-result"

    monkeypatch.setattr(mpremote_main, "do_repl_async", fake_async_repl)
    monkeypatch.setattr(mpremote_main, "do_repl", fake_sync_repl)

    result = mpremote_main._run_repl(state, repl_args)

    assert result == "sync-result"
    assert called["sync"] == (state, repl_args)

    err = capsys.readouterr().err
    assert "async repl unavailable" in err
