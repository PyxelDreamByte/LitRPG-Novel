---
run_id: "run://develop-worldbuilding/WB-RUN-2026-08-14-LINEAGE-II-004"
validated_on: "2026-08-14"
status: PASS
---

# Validation Summary — WLD-ECOLOGY-004

The promoted transaction was checked with:

- `git diff --check` — passed with no whitespace errors.
- `python tools/validate_governance.py` — passed with 16 repository records,
  3 valid fixtures, and 5 rejected fixtures.
- `python tools/validate_workspaces.py` — passed with 4 work manifests,
  2 setting manifests, 2 workflow evaluations, and 3 rejected fixtures.
- `python tools/validate_story_integration.py stories/series/project-hearthway-main/project-hearthway-main.work-manifest.json`
  — passed with 9 schemas and the focused manifest fixture.
- `python tools/validate_repository.py` — complete repository and System
  validation passed, including all 121 CAL0 regression tests.

The final post-evidence repository run verified 74 non-CAL0 JSON files, all 16
governance records, the workspace and story-integration contracts, generated
System indexes, deterministic state derivation, and all 121 CAL0 regression
tests. It completed with no failures.
