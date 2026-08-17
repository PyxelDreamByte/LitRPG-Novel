# Validation Summary — Basin Ecosystem Engine

## Pre-evidence checks

- `python tools/validate_governance.py` — PASS with 27 repository records,
  5 valid fixtures, and 5 rejected fixtures before the evidence manifest was added.
- `python tools/validate_workspaces.py` — PASS with 4 work manifests, 2 setting
  manifests, 2 workflow evaluations, and 3 rejected fixtures.
- `python tools/validate_story_integration.py stories/series/project-hearthway-main/project-hearthway-main.work-manifest.json`
  — PASS with 9 schemas and 1 valid fixture.
- Independent ecology and governance audits — PASS after minor terminology and
  stale-summary corrections.

## Capture and repository checks

- `git diff --check` — PASS with no whitespace errors.
- `python -m unittest tools.tests.test_validate_governance -v` — PASS with all
  3 evidence-mode regression tests.
- `python tools/validate_governance.py --verify-current-accepted governance/evidence/WB-RUN-2026-08-14-BASIN-ECOSYSTEM-001/WB-RUN-2026-08-14-BASIN-ECOSYSTEM-001.workflow-evidence.json`
  — PASS with 28 repository records, 5 valid fixtures, 5 rejected fixtures, and
  every accepted source and target digest verified against current bytes.
- `python tools/validate_repository.py` — PASS, including repository structure,
  governance, workspace, System routing, story-integration contracts,
  deterministic state derivation, and all 121 CAL0 regression tests.
