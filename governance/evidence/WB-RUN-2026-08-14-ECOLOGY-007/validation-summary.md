# Validation Summary — WB-RUN-2026-08-14-ECOLOGY-007

## Initial final-content gates

- Governance digest-mode unit tests: passed, 3 tests.
- Governance validation before evidence registration: passed, 36 repository
  records, 5 valid fixtures, and 5 rejected fixtures.
- Workspace/evaluation validation: passed, 4 work manifests, 2 setting
  manifests, 2 workflow evaluations, and 3 rejected fixtures.
- Focused Project Hearthway story-integration validation: passed, 9 schemas,
  1 valid fixture, and 0 rejected fixtures.
- Complete repository validation before evidence registration: passed,
  including the content-pinned CAL0 bundle, all 121 CAL0 regression tests,
  generated routing indexes, story-integration contracts, state derivation, and
  the context-router smoke test.
- Tracked-file whitespace check: passed.

## Capture-time gate

The evidence manifest was created from the final source and target bytes.

- Post-registration governance validation: passed, 37 repository records,
  5 valid fixtures, and 5 rejected fixtures.
- Accepted-outcome current-byte verification: passed for
  `WB-RUN-2026-08-14-ECOLOGY-007.workflow-evidence.json`.
- Post-registration complete repository validation: passed, including all 121
  CAL0 regression tests.
- `git diff --check` and the explicit 26-file unintended-trailing-whitespace
  scan passed; intentional two-space Markdown hard breaks were permitted.

The older `WLD-ECOLOGY-006` evidence bundle remains a historical content pin
and was not rewritten or reverified against the later reconciled bytes.
