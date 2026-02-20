from __future__ import annotations

import subprocess
import sys

if __name__ == "__main__":
    result = subprocess.run(sys.argv[1:])

    if result.returncode == 127:
        print(
            "pyright skipped: required system library missing (likely libatomic)",
            file=sys.stderr,
        )
        raise SystemExit(0)

    raise SystemExit(result.returncode)
