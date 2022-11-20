# test LOC
import pytest
from mock import MagicMock

from .main import load_user_config


def test_load_user_config_xdg(monkeypatch:pytest.MonkeyPatch, mocker):
    "test load_user_config"
    monkeypatch.setattr('os.name', 'posix')
    monkeypatch.setenv('XDG_CONFIG_HOME', '/foo/xdg')
    m_path_exists:MagicMock = mocker.patch("mpremote.main.os.path.exists", autospec=True, return_value=False)
    config = load_user_config()
    m_path_exists.assert_called_with('/foo/xdg/mpremote/config.py')


def test_load_user_config_home(monkeypatch:pytest.MonkeyPatch, mocker):
    "test load_user_config"
    monkeypatch.setattr('os.name', 'posix')
    monkeypatch.delenv('XDG_CONFIG_HOME', raising=False)
    monkeypatch.setenv('HOME', '/foo/home')
    m_path_exists = mocker.patch("mpremote.main.os.path.exists", autospec=True, return_value=False)
    config = load_user_config()
    m_path_exists.assert_called_with('/foo/home/.config/mpremote/config.py')


def test_load_user_config_userprofile(monkeypatch:pytest.MonkeyPatch, mocker):
    "test load_user_config"
    monkeypatch.setattr('os.name', 'nt')
    monkeypatch.setenv('USERPROFILE', '/user/foo')
    m_path_exists = mocker.patch("mpremote.main.os.path.exists", autospec=True, return_value=False)
    # m_sys_platform = mocker.patch("mpremote.main.sys.platform", autospec=True, return_value="win32")
    config = load_user_config()
    m_path_exists.assert_called_with('/user/foo/mpremote/config.py')
