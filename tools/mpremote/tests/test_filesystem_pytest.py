import os

import pytest

from mpremote.transport import _quote_path
from pytest_utils import require_success, run_mpremote


@pytest.mark.parametrize(
    "path",
    [
        "normal.txt",
        "space name.txt",
        "quote'name.txt",
        'double"quote.txt',
        "a=b.txt",
        "日本語.txt",
        "emoji-🎉.txt",
        "line\nbreak.txt",
    ],
)
def test_quote_path_round_trip(path):
    assert eval(_quote_path(path)) == path


@pytest.mark.parametrize(
    "filename",
    [
        "space name.txt",
        "quote'name.txt",
        "a=b.txt",
        "日本語.txt",
        "emoji-🎉.txt",
    ],
)
def test_remote_filename(device, tmp_path, filename):
    local = tmp_path / filename
    local.write_bytes("Unicode content: café 世界\n".encode("utf-8"))
    remote = ":" + filename

    try:
        require_success(run_mpremote(device, "cp", str(local), remote))
        result = run_mpremote(device, "cat", remote)
        require_success(result)
        assert result.stdout == "Unicode content: café 世界\n"
    finally:
        run_mpremote(device, "rm", remote)


def test_recursive_unicode_path(device, tmp_path):
    # Physical devices have isolated storage, but the unix port exposes a real
    # filesystem, where recursive deletion could remove host or container files.
    if device.startswith(("rfc2217://", "socket://")):
        pytest.skip("unix port exposes the host filesystem")

    source = tmp_path / "目录"
    source.mkdir()
    (source / "a=b.txt").write_bytes(b"recursive content\n")

    try:
        require_success(run_mpremote(device, "cp", "--no-verbose", "-r", str(source), ":"))
        result = run_mpremote(device, "cat", ":目录/a=b.txt")
        require_success(result)
        assert result.stdout == "recursive content\n"
    finally:
        run_mpremote(device, "rm", "-r", ":目录")


@pytest.mark.skipif(os.name != "nt", reason="requires Windows console encodings")
@pytest.mark.parametrize("encoding", ["cp1252", "cp437"])
def test_remote_unicode_with_legacy_host_encoding(device, tmp_path, encoding):
    local = tmp_path / "日本語.txt"
    local.write_bytes("你好世界\n".encode("utf-8"))
    remote = ":日本語.txt"

    try:
        result = run_mpremote(
            device,
            "cp",
            str(local),
            remote,
            encoding=encoding,
            child_encoding=encoding,
        )

        require_success(result)
        assert "UnicodeEncodeError" not in result.stderr
    finally:
        run_mpremote(
            device,
            "rm",
            remote,
            encoding=encoding,
            child_encoding=encoding,
        )
