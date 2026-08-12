#!/usr/bin/env python3
"""Run the complete imported-CAL0 and story-integration validation gate."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
CAL0_ROOT = ROOT / "litrpg-system/cal0"


def run(label: str, command: list[str], cwd: Path = ROOT, env: dict[str, str] | None = None) -> None:
    print(f"\n[{label}]", flush=True)
    subprocess.run(command, cwd=cwd, env=env, check=True)


def main() -> int:
    python = sys.executable
    cal0_env = os.environ.copy()
    cal0_env["PYTHONPATH"] = "src"
    try:
        run(
            "CAL0 content-pinned bundle",
            [python, "-m", "cal0.cli", "validate", "."],
            cwd=CAL0_ROOT,
            env=cal0_env,
        )
        run(
            "CAL0 regression suite (121 tests)",
            [python, "-m", "unittest", "discover", "-s", "tests"],
            cwd=CAL0_ROOT,
            env=cal0_env,
        )
        run("Generated routing indexes", [python, "tools/build_system_indexes.py", "--check"])
        run("Story-integration contracts", [python, "tools/validate_story_integration.py"])
        run("Context-router smoke test", [python, "tools/route_system_context.py", "--decision", "ATR3.4.2.0D", "--paths"])
    except subprocess.CalledProcessError as exc:
        print(f"\nSystem validation failed in command: {' '.join(exc.cmd)}", file=sys.stderr)
        return exc.returncode or 1
    print("\nComplete System validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

