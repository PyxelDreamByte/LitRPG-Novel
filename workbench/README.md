# Workbench

The workbench holds disposable artifacts generated while a workflow is active:

- `proposals/` — temporary alternatives not yet placed in a domain proposal directory;
- `context-packs/` — reproducible bounded context assembled for one run;
- `runs/` — plans, independent findings, change sets, validation output, and run manifests.

Workbench material is non-canonical. It may be deleted or rebuilt. When the Author accepts an outcome, promote the authoritative decision, manuscript, delta, or canon record to its domain directory and link to any retained evidence.

Every run should use a stable run ID and record target revision, source manifest, workflow mode, agent roles, results, and expiry. Do not edit a stale context pack into a competing source of truth.

## Evidence promotion

The workbench is ignored by Git intentionally. Before an accepting commit,
copy the minimum evidence needed to audit the outcome into
`governance/evidence/<run-id>/` and add its manifest to the accepted decision or
chapter record. Retain final findings, change-set disposition, validation
summary, exact artifact digests, and Author approval evidence. Do not retain
whole context packs when stable source references and digests are sufficient.
