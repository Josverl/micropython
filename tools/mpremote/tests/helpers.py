import subprocess
from pathlib import Path
from textwrap import dedent

def write_script(file_path: Path, code: str):
    """Write dedented code to a script file."""
    with open(file_path, "w") as f:
        f.write(dedent(code).strip())

def run_mpremote(mpremote_cmd:list[str], *args):
    """Run mpremote command and return output."""
    cmd = mpremote_cmd + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    return result
