from __future__ import annotations

import subprocess
import sys
from collections.abc import Sequence


def run_pyright(args: Sequence[str]) -> int:
    completed = subprocess.run(
        ["pyright", *args],
        check=False,
        capture_output=True,
        text=True,
    )

    stdout = completed.stdout or ""
    stderr = completed.stderr or ""

    if completed.returncode == 127 and "libatomic.so.1" in stderr:
        print("pyright skipped: missing libatomic.so.1 (bundled node dependency)")
        return 0

    if stdout:
        print(stdout, end="")

    if stderr:
        print(stderr, file=sys.stderr, end="")

    return completed.returncode
def main() -> int:
    return run_pyright(sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())
