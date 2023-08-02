# test LOC
import os
import pytest
from unittest.mock import MagicMock, mock_open

# module under test
from mpremote.main import load_user_config

# Fake config file
read_data = """
commands = {
    "list": {
        "command": ["connect", "list"],
        "help": "List serial devices",
    },
}
"""
mock_open = mock_open(read_data=read_data)


def new_file_exists_mocker(mocker, prefix: str):
    "simple mock factory for os.path.exists to test load_user_config"

    def path_exists(path: str):
        return bool(path.startswith(prefix))

    m_path_exists: MagicMock = mocker.patch(
        "mpremote.main.os.path.exists", autospec=True, side_effect=path_exists
    )
    return m_path_exists


@pytest.mark.parametrize(
    "ok, env_var, env_path, prefix",
    [
        ("Y", "XDG_CONFIG_HOME", "/foo/xdg", "/foo/xdg"),
        ("Y", "XDG_CONFIG_HOME", "/foo/xdg", f"/foo/xdg{os.sep}.config"),
        ("Y", "HOME", "/foo/home", "/foo/home"),
        ("Y", "HOME", "/foo/home", f"/foo/home{os.sep}.config"),
        ("Y", "USERPROFILE", "\\user\\foo", "\\user\\foo"),
        ("Y", "USERPROFILE", "\\user\\foo", f"\\user\\foo{os.sep}.config"),
        ("Y", "APPDATA", "\\user\\foo\\AppData\\Roaming", "\\user\\foo\\AppData\\Roaming"),
        (
            "Y",
            "APPDATA",
            "\\user\\foo\\AppData\\Roaming",
            f"\\user\\foo\\AppData\\Roaming{os.sep}.config",
        ),
        ("N", "XDG_CONFIG_HOME", "/foo/xdg", "/bar/xdg"),
        ("N", "CONFIG_HOME", "/foo /xdg", "/bar/xdg"),
    ],
)
def test_load_user_config(
    monkeypatch: pytest.MonkeyPatch, mocker, ok: str, env_var: str, env_path: str, prefix: str
):
    "test load_user_config"
    # Disable all env vars
    monkeypatch.delenv("XDG_CONFIG_HOME", raising=False)
    monkeypatch.delenv("HOME", raising=False)
    monkeypatch.delenv("USERPROFILE", raising=False)
    monkeypatch.delenv("APPDATA", raising=False)

    monkeypatch.setenv(env_var, env_path)
    m_path_exists = new_file_exists_mocker(mocker, prefix)
    # # add test config
    m_open: MagicMock = mocker.patch("mpremote.main.open", mock_open)
    # fake chdir
    m_chdir: MagicMock = mocker.patch("mpremote.main.os.chdir", autospec=True)
    # method under test
    config = load_user_config()
    assert config
    if ok == "Y":
        # TEST CONFIG LOADED
        assert config.commands
        assert config.commands["list"]
    else:
        assert not config.commands
