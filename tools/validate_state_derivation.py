#!/usr/bin/env python3
"""Regression gate for the bounded deterministic character-state reducer."""

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "litrpg-system/story-integration/fixtures/valid"


def run(command: list[str], expected_error: str | None = None) -> bool:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if expected_error is None:
        if result.returncode:
            print(result.stderr, file=sys.stderr, end="")
            return False
        return True
    if result.returncode == 0:
        print(f"state-derivation negative regression unexpectedly passed: {expected_error}", file=sys.stderr)
        return False
    if expected_error not in result.stderr:
        print(
            f"state-derivation negative regression lacked {expected_error!r}:\n{result.stderr}",
            file=sys.stderr,
        )
        return False
    return True


def main() -> int:
    base_command = [
        sys.executable,
        "tools/build_character_state.py",
        "--base", str(FIXTURES / "pre-chapter-001.character-state.json"),
        "--delta", str(FIXTURES / "chapter-001.chapter-delta.json"),
    ]
    command = [
        *base_command,
        "--snapshot-id", "snapshot://series/first-awakening/protagonist/book-01/001",
        "--check", str(FIXTURES / "protagonist.character-state.json"),
    ]
    if not run(command):
        return 1

    wrong_work = [
        *base_command,
        "--snapshot-id", "snapshot://novella/other-work/protagonist/book-01/001",
    ]
    if not run(wrong_work, "same work namespace"):
        return 1

    with tempfile.TemporaryDirectory(prefix="state-derivation-regression-") as temporary:
        temporary_root = Path(temporary)
        source = json.loads((FIXTURES / "chapter-001.chapter-delta.json").read_text(encoding="utf-8"))

        invalid_input = deepcopy(source)
        del invalid_input["review"]
        invalid_input_path = temporary_root / "invalid-input.chapter-delta.json"
        invalid_input_path.write_text(
            json.dumps(invalid_input, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        invalid_input_command = [
            sys.executable,
            "tools/build_character_state.py",
            "--base", str(FIXTURES / "pre-chapter-001.character-state.json"),
            "--delta", str(invalid_input_path),
            "--snapshot-id", "snapshot://series/first-awakening/protagonist/book-01/002",
        ]
        if not run(invalid_input_command, "input contract validation failed"):
            return 1

        invalid_result = deepcopy(source)
        invalid_result["character_changes"][0]["after"] = "0.03"
        invalid_result_path = temporary_root / "invalid-result.chapter-delta.json"
        invalid_result_path.write_text(
            json.dumps(invalid_result, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        invalid_result_command = [
            sys.executable,
            "tools/build_character_state.py",
            "--base", str(FIXTURES / "pre-chapter-001.character-state.json"),
            "--delta", str(invalid_result_path),
            "--snapshot-id", "snapshot://series/first-awakening/protagonist/book-01/003",
        ]
        if not run(invalid_result_command, "derived snapshot contract validation failed"):
            return 1

        threshold_crossing = deepcopy(source)
        threshold_crossing["progression_events"][0]["amount"] = "3"
        threshold_crossing["progression_events"][0]["after_value"] = "3"
        threshold_crossing_path = temporary_root / "threshold-crossing.chapter-delta.json"
        threshold_crossing_path.write_text(
            json.dumps(threshold_crossing, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        threshold_crossing_command = [
            sys.executable,
            "tools/build_character_state.py",
            "--base", str(FIXTURES / "pre-chapter-001.character-state.json"),
            "--delta", str(threshold_crossing_path),
            "--snapshot-id", "snapshot://series/first-awakening/protagonist/book-01/004",
        ]
        if not run(threshold_crossing_command, "XP crosses the next CAL0 threshold"):
            return 1

    print(
        "state-derivation regression passed: 1 accepted delta applied exactly; "
        "4 invalid identity/contract/threshold cases rejected"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
