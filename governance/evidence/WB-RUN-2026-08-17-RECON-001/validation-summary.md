# Validation Summary — WB-RUN-2026-08-17-RECON-001

Run from the repository root on 2026-08-17 with the reconciliation applied:

- `python tools/validate_governance.py` — PASS: 60 repository records, 5 valid
  fixtures, 5 rejected fixtures. The new `WLD-RECON-001A` pair validates
  against the decision-record schema with `domain: world` and matching
  `setting_id`, and is indexed in the setting-local authority index.
- `python tools/validate_workspaces.py` — PASS: 4 work manifests, 3 setting
  manifests, 2 workflow evaluations, 4 rejected fixtures, including the
  worldbuilding-record schema over all amended structured records.
- `python -m unittest discover -s tools/tests` — PASS: 3 evidence-mode
  regression tests.
- `python tools/validate_repository.py` — PASS: complete repository and System
  validation, 125 non-CAL0 JSON files.
- `python tools/validate_governance.py --verify-current-accepted
  governance/evidence/WB-RUN-2026-08-17-RECON-001/WB-RUN-2026-08-17-RECON-001.workflow-evidence.json`
  — PASS at capture time: every source and target digest matches current
  repository bytes.
