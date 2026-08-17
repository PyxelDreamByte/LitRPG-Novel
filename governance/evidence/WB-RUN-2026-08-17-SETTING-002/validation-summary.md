# Validation Summary — WB-RUN-2026-08-17-SETTING-002

Run from the repository root on 2026-08-17 with the consolidation applied:

- `python tools/validate_governance.py` — PASS: 60 repository records, 5 valid
  fixtures, 5 rejected fixtures. The new `WLD-SETTING-002A` pair validates
  against the decision-record schema with `domain: world` and matching
  `setting_id`, and is indexed in the setting-local authority index.
- `python tools/validate_workspaces.py` — PASS: 4 work manifests, 3 setting
  manifests, 2 workflow evaluations, 4 rejected fixtures. The archived
  continuity-one tree is no longer scanned as a live setting.
- `python -m unittest discover -s tools/tests` — PASS: 3 evidence-mode
  regression tests.
- `python tools/validate_repository.py` — PASS: complete repository and System
  validation, 125 non-CAL0 JSON files.
- `python tools/validate_governance.py --verify-current-accepted
  governance/evidence/WB-RUN-2026-08-17-SETTING-002/WB-RUN-2026-08-17-SETTING-002.workflow-evidence.json`
  — PASS at capture time: every source and target digest matches current
  repository bytes.
