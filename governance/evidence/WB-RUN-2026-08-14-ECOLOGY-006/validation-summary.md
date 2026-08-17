# Validation Summary — WB-RUN-2026-08-14-ECOLOGY-006

## Pre-evidence validation

- JSON parsing passed for the new structured decision and world record.
- `python tools/validate_governance.py` — passed with 33 repository records, 5
  valid fixtures, and 5 rejected fixtures before this evidence manifest was added.
- `python tools/validate_workspaces.py` — passed with 4 work manifests, 2
  setting manifests, 2 workflow evaluations, and 3 rejected fixtures.
- `python tools/validate_story_integration.py stories/series/project-hearthway-main/project-hearthway-main.work-manifest.json`
  — passed with 9 schemas, 1 valid fixture, and 0 rejected fixtures.

## Final validation

- Independent ecology, CAL0, provenance, parity, dependency, adoption, and
  discoverability audits — passed after exact wording corrections.
- `python -m unittest tools.tests.test_validate_governance -v` — passed 3 tests.
- `python tools/validate_governance.py` — passed with 34 repository records, 5
  valid fixtures, and 5 rejected fixtures.
- `python tools/validate_workspaces.py` — passed with 4 work manifests, 2
  setting manifests, 2 workflow evaluations, and 3 rejected fixtures.
- `python tools/validate_story_integration.py stories/series/project-hearthway-main/project-hearthway-main.work-manifest.json`
  — passed with 9 schemas, 1 valid fixture, and 0 rejected fixtures.
- `python tools/validate_governance.py --verify-current-accepted governance/evidence/WB-RUN-2026-08-14-ECOLOGY-006/WB-RUN-2026-08-14-ECOLOGY-006.workflow-evidence.json`
  — passed current-byte verification for the accepted outcome.
- `python tools/validate_repository.py` — complete repository validation passed,
  including the 121-test CAL0 regression suite.
- `git diff --check` and an explicit unexpected-trailing-whitespace scan of all
  28 touched files passed; intentional two-space Markdown hard breaks were allowed.
