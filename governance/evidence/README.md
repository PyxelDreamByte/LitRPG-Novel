# Retained Workflow Evidence

This directory stores the minimum committed evidence required to audit an
accepted outcome or completed workflow evaluation. Use one directory per stable
run ID.

An accepted-outcome bundle contains:

- a source and target manifest with immutable revisions or SHA-256 digests;
- final independent findings and their dispositions;
- the approved revision change set;
- validation and evaluation summaries;
- exact Author approval evidence or a link to its accepted decision record;
- links to the authoritative artifacts promoted by the run.

Accepted-outcome digests are historical content pins. Later accepted
transactions may legitimately advance the same authoritative paths, so
repository validation confirms that those paths remain resolvable but does not
compare an earlier run's digests with the paths' current bytes. References that
are also listed in `retained_files` remain byte-checked.

Before recording a new accepted outcome, verify its then-current source and
target bytes explicitly:

```text
python tools/validate_governance.py --verify-current-accepted governance/evidence/<run-id>/<run-id>.workflow-evidence.json
```

Only record promotion after this capture-time check passes. Later ordinary
repository validation treats external references as historical receipts.

A live noncanonical evaluation is a separate evidence kind. It contains exact
source and raw-output hashes, evaluated targets, invariant verdicts,
prohibited-output checks, and a bounded evaluator conclusion. It must declare
`NONCANONICAL_EVALUATION_ONLY`, `FORBIDDEN`, and `approval: null`. Its target
artifact list may be empty for a read-only run. Retention does not promote the
fixture, output, or any creative fact.

Live-evaluation source references also become historical when mutable source
paths advance. Raw output and any other evidence files that must remain
byte-exact belong in `retained_files`; repository validation continues to
compare those retained references with their recorded SHA-256 digests.

Raw deliberation, duplicated context, caches, and abandoned runs remain in the
ignored workbench.

Name the structured manifest `<run-id>.workflow-evidence.json` and validate it against
`governance/schemas/workflow-evidence-manifest.schema.json`. Start from
`governance/templates/workflow-evidence-manifest.template.json` for an accepted
outcome or `governance/templates/live-evaluation-evidence-manifest.template.json`
for a live noncanonical evaluation.
