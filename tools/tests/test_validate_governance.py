from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
FIXTURE_ROOT = ROOT / "litrpg-system/story-integration/fixtures/governance/valid"
VALIDATOR = ROOT / "tools/validate_governance.py"


def run_validator(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


class AcceptedOutcomeDigestModesTest(unittest.TestCase):
    def test_repository_mode_accepts_historical_digests(self) -> None:
        result = run_validator()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_capture_mode_accepts_current_digests(self) -> None:
        path = FIXTURE_ROOT / "accepted-outcome-current-digests.workflow-evidence.json"
        result = run_validator(
            "--verify-current-accepted", path.relative_to(ROOT).as_posix()
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_capture_mode_rejects_historical_digests_for_current_paths(self) -> None:
        path = FIXTURE_ROOT / "accepted-outcome-historical-digests.workflow-evidence.json"
        result = run_validator(
            "--verify-current-accepted", path.relative_to(ROOT).as_posix()
        )
        output = result.stdout + result.stderr
        self.assertNotEqual(0, result.returncode, output)
        self.assertIn("digest mismatch", output)


if __name__ == "__main__":
    unittest.main()
