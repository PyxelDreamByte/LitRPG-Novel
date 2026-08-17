# Validation Summary — WB-RUN-2026-08-14-GEOGRAPHY-001

## Pre-evidence validation

- `python tools/validate_governance.py` — passed with 30 repository records, 5
  valid fixtures, and 5 rejected fixtures before this evidence manifest was added.
- `python tools/validate_workspaces.py` — passed with 4 work manifests, 2
  setting manifests, 2 workflow evaluations, and 3 rejected fixtures.
- `python tools/validate_story_integration.py stories/series/project-hearthway-main/project-hearthway-main.work-manifest.json`
  — passed with 9 schemas, 1 valid fixture, and 0 rejected fixtures.

## Final validation

- `python -m unittest tools.tests.test_validate_governance -v` — passed 3 tests.
- `python tools/validate_governance.py` — passed with 31 repository records, 5
  valid fixtures, and 5 rejected fixtures.
- `python tools/validate_workspaces.py` — passed with 4 work manifests, 2
  setting manifests, 2 workflow evaluations, and 3 rejected fixtures.
- `python tools/validate_story_integration.py stories/series/project-hearthway-main/project-hearthway-main.work-manifest.json`
  — passed with 9 schemas, 1 valid fixture, and 0 rejected fixtures.
- `python tools/validate_governance.py --verify-current-accepted governance/evidence/WB-RUN-2026-08-14-GEOGRAPHY-001/WB-RUN-2026-08-14-GEOGRAPHY-001.workflow-evidence.json`
  — passed current-byte verification for the accepted-outcome evidence. The
  normalized repository-relative forward-slash path is required.
- `python tools/validate_repository.py` — complete repository validation passed,
  including the 121-test CAL0 regression suite.
- `git diff --check` and the explicit edited-file unexpected-trailing-whitespace
  scan passed; existing two-space Markdown hard breaks were treated as intentional.
