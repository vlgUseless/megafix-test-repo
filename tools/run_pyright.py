from __future__ import annotations

import subprocess
import sys
from collections.abc import Iterable
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMMANDS: tuple[tuple[str, ...], ...] = (
    ("pyright",),
    ("pyright", "--verifytypes", "itsdangerous", "--ignoreexternal"),
)


_SKIP_DEP_MESSAGE = (
    "pyright skipped: missing required system library libatomic.so.1. "
    "Install libatomic or run pyright in an environment that provides it.\n"
)


def _stream_output(result: subprocess.CompletedProcess[str]) -> None:
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)


def run_command(command: tuple[str, ...]) -> int:
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    if result.returncode == 0:
        _stream_output(result)
        return 0

    if "libatomic.so.1" in (result.stderr or ""):
        _stream_output(result)
        sys.stderr.write(_SKIP_DEP_MESSAGE)
        return 0

    _stream_output(result)
    return result.returncode


def main(commands: Iterable[tuple[str, ...]] = COMMANDS) -> int:
    for command in commands:
        code = run_command(command)
        if code != 0:
            return code

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
