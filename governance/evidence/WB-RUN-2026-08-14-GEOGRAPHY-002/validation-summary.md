# Validation Summary — WB-RUN-2026-08-14-GEOGRAPHY-002

## Final-content gates before evidence registration

- Governance digest-mode unit tests: passed, 3 tests.
- Governance validation: passed, 48 repository records, 5 valid fixtures, and
  5 rejected fixtures.
- Workspace/evaluation validation: passed, 4 work manifests, 2 setting
  manifests, 2 workflow evaluations, and 3 rejected fixtures.
- Focused Project Hearthway story-integration validation: passed, 9 schemas,
  1 valid fixture, and 0 rejected fixtures.
- Complete repository validation: passed with 108 non-CAL0 JSON files,
  including the content-pinned CAL0 bundle, all 121 CAL0 regression tests,
  generated routing indexes, story-integration contracts, state derivation,
  and the context-router smoke test.
- Independent geography, ecology/CAL0, and recording-surface reviews passed
  after the corrections recorded in `final-findings.md`; no blocking, major,
  or minor finding remained.
- `git diff --check` and an explicit 28-file source/target unintended-trailing-
  whitespace scan passed; intentional two-space Markdown hard breaks were
  permitted.

## Capture-time and post-registration gates

The evidence manifest was created from the final source and target bytes.

- Post-registration governance validation: passed, 49 repository records,
  5 valid fixtures, and 5 rejected fixtures.
- Accepted-outcome current-byte verification: passed for
  `WB-RUN-2026-08-14-GEOGRAPHY-002.workflow-evidence.json`, including both
  source manifests and all 26 target artifacts.
- Post-registration workspace/evaluation validation: passed, 4 work manifests,
  2 setting manifests, 2 workflow evaluations, and 3 rejected fixtures.
- Post-registration focused story-integration validation: passed, 9 schemas,
  1 valid fixture, and 0 rejected fixtures.
- Post-registration complete repository validation: passed with 109 non-CAL0
  JSON files and all 121 CAL0 regression tests.

The older `WLD-GEOGRAPHY-001` and `WLD-ECOLOGY-006`, `WLD-ECOLOGY-009`,
and `WLD-ECOLOGY-010` evidence bundles remain historical content pins and were
not rewritten or current-byte verified against the later reconciled bytes.
