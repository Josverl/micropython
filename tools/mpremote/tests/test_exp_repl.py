from contextlib import contextmanager
from pathlib import Path
import shlex
import time
import pytest
import sys
import shutil

if sys.platform != "win32":
    # https://pexpect.readthedocs.io/en/stable/
    import pexpect
else:
    # https://wexpect.readthedocs.io/en/latest/
    import wexpect as pexpect

#  context manager
#  https://github.com/omf2097/openomf/blob/c4d71680f993e4bd1771094ca6565201840d98df/pytest/test_menus.py#L2
# per test
#  https://github.com/kimschles/securedrop/blob/185bd55b960170b873a6f9770662c141a9fa903b/admin/tests/test_integration.py#L439
#


class LogFile:
    def write(self, message: str):
        # todo: also log output to a file
        if message:
            print(f"\033[33m{message}\033[0m", end="")

    def flush(self):
        sys.stdout.flush()


class Tee(object):
    def __init__(self, name: Path, mode: str = "w"):
        self.name = name
        self.mode = mode
        self.file = None
        self._stdout = None

    def __enter__(self):
        self.file = open(self.name, self.mode)
        self._stdout = sys.stdout
        sys.stdout = self
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout = self._stdout
        if self.file:
            self.file.close()
            self.file = None
        self._stdout = None

    def write(self, data: bytes):
        if self.file:
            self.file.write(data.decode('utf-8') if isinstance(data, bytes) else data)
        if self._stdout:
            self._stdout.write(data.decode('utf-8') if isinstance(data, bytes) else data)

    def flush(self):
        if self.file:
            self.file.flush()

    def close(self):
        self.__exit__(None, None, None)


@contextmanager
def mpremote_exp(
    request: pytest.FixtureRequest, args: list[str] | str = "", check_output: bool = True
):
    if isinstance(args, str):
        args = shlex.split(args)
    elif not isinstance(args, list):
        raise TypeError("args must be a list or a string")
    args = args or []
    if args and args[0] == "mpremote":
        args = args[1:]

    # get the test name and file name
    test_name: str = request.node.name
    test_filename = Path(request.node.fspath)
    out_file = test_filename.with_name(f"{test_filename.name}_{test_name.lstrip('test_')}.out")
    exp_file = out_file.with_suffix(".exp")

    # Hacky
    MPREMOTE = "mpremote"
    TEST_DIR = "tools/mpremote/tests"
    MPREMOTE = f"{TEST_DIR}/../mpremote.py"

    with Tee(out_file, mode="w") as tee:
        child = pexpect.spawn(
            MPREMOTE,
            args=args,
            timeout=10,
            logfile=tee,
            echo=False,
        )
        child.linesep = '\r'
        try:
            yield child
        finally:
            child.close()

    if not check_output:
        # if check_output is False, just return
        return

    if not out_file.exists():
        raise FileNotFoundError(f"Output file {out_file} not found")
    if not exp_file.exists():
        # copy the output file to the expected file
        shutil.copy(out_file, exp_file)
        return

    # compare the output file with the expected file using difflib
    with open(out_file, "r") as f1, open(exp_file, "r") as f2:
        f1_lines = f1.readlines()
        f2_lines = f2.readlines()
    if f1_lines != f2_lines:
        # print the differences
        from difflib import unified_diff

        diff = unified_diff(f1_lines, f2_lines, fromfile=str(out_file), tofile=str(exp_file))
        for line in diff:
            if line.startswith("- "):
                print(f"\033[31m{line}\033[0m", end="")
            elif line.startswith("+ "):
                print(f"\033[32m{line}\033[0m", end="")
            else:
                print(line, end="")
        raise AssertionError(f"Output file {out_file} does not match expected file {exp_file}")


def test_mpremote_help(request):
    with mpremote_exp(request, "--help") as mpr:
        mpr.expect(
            'connect to serial port "/dev/ttyUSB3"',
            timeout=2,
        )
        mpr.expect(
            pexpect.EOF,
            timeout=2,
        )


def test_mpremote_devs(request):
    with mpremote_exp(request, "devs", check_output=False) as mpr:
        mpr.expect(
            pexpect.EOF,
            timeout=2,
        )


@pytest.mark.parametrize(
    "command",
    [
        "mpremote devs",
        "mpremote ls",
        "mpremote tree",
        "mpremote tree -h",
    ],
)
def test_mpremote_cmd(request, command):
    with mpremote_exp(request, command) as mpr:
        mpr.expect(
            pexpect.EOF,
            timeout=2,
        )


def test_mpremote_mount_remount(request):
    # with mpremote_exp(request, "mpremote mount . exec \"print('hello world')\" + repl") as mpr:
    with mpremote_exp(request, "mpremote mount . + repl") as mpr:
        # mpr.expect("hello world",timeout=2)
        mpr.expect("Local directory . is mounted at /remote")
        mpr.expect(">>>")
        mpr.sendcontrol("d")
        mpr.expect(">>>")
        mpr.expect(r"Remount local directory .*")
        # mpr.expect("Remount local directory ./ at /remote")
        mpr.expect(">>>")
        # mpr.expect(">>>")
        # mpr.sendline(b"import os; print(os.getcwd())")
        # mpr.expect(">>>")
        mpr.sendcontrol("]")
        mpr.read()
        mpr.expect(pexpect.EOF, timeout=2)
