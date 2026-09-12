from pytest_utils import require_success, run_mpremote, run_mpremote_bytes


def test_cat_preserves_crlf_bytes(device, tmp_path):
    content = b"first line\r\nsecond line\r\n"
    local = tmp_path / "crlf.txt"
    local.write_bytes(content)
    remote = ":crlf.txt"

    try:
        require_success(run_mpremote(device, "cp", str(local), remote))
        result = run_mpremote_bytes(device, "cat", remote)
        require_success(result)
        assert result.stdout == content
    finally:
        run_mpremote(device, "rm", remote)
