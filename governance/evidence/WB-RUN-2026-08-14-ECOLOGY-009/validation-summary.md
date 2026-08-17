# Validation Summary — WB-RUN-2026-08-14-ECOLOGY-009

## Final-content gates before evidence registration

- Governance digest-mode unit tests: passed, 3 tests.
- Governance validation: passed, 42 repository records, 5 valid fixtures, and
  5 rejected fixtures.
- Workspace/evaluation validation: passed, 4 work manifests, 2 setting
  manifests, 2 workflow evaluations, and 3 rejected fixtures.
- Focused Project Hearthway story-integration validation: passed, 9 schemas,
  1 valid fixture, and 0 rejected fixtures.
- Complete repository validation: passed, including the content-pinned CAL0
  bundle, all 121 CAL0 regression tests, generated routing indexes,
  story-integration contracts, state derivation, and the context-router smoke
  test.
- Independent ecology/CAL0, governance/provenance, and recording-surface
  reviews: passed after two major and three minor wording corrections; no
  blocking, major, or minor finding remained.

## Capture-time and post-registration gates

The evidence manifest was created from the final source and target bytes.

- Post-registration governance validation: passed, 43 repository records,
  5 valid fixtures, and 5 rejected fixtures.
- Accepted-outcome current-byte verification: passed for
  `WB-RUN-2026-08-14-ECOLOGY-009.workflow-evidence.json`, including both source
  manifests and all 22 target artifacts.
- Post-registration workspace/evaluation validation: passed, 4 work manifests,
  2 setting manifests, 2 workflow evaluations, and 3 rejected fixtures.
- Post-registration focused story-integration validation: passed, 9 schemas,
  1 valid fixture, and 0 rejected fixtures.
- Post-registration complete repository validation: passed, including all 121
  CAL0 regression tests.
- `git diff --check` and the explicit 28-file transaction whitespace scan
  passed; intentional two-space Markdown hard breaks were permitted.

The older `WLD-ECOLOGY-006`, `WLD-ECOLOGY-007`, and
`WLD-ECOLOGY-008` evidence bundles remain historical content pins and were not
rewritten or current-byte verified against the later reconciled bytes.
