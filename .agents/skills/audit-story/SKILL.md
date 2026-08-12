---
name: audit-story
description: "Audit one or more story artifacts for continuity, causal feasibility, character knowledge, plot-thread integrity, world-canon fit, prose defects, and CAL0 legality without rewriting them. Use for pre-draft checks, manuscript audits, cross-chapter regression, or investigating a suspected contradiction."
---

# Audit Story

Audit against explicit sources and distinguish defects from taste.

## Workflow

1. Define the audit scope, authoritative baseline, dimensions, and whether the run is chapter-local or cross-story.
2. Build a bounded evidence set: accepted prose/deltas, current derived state, outline/thread obligations, relevant world canon, and routed CAL0 guidance.
3. Run applicable specialist auditors independently: `continuity-auditor`, `character-pov-auditor`, `world-canon-auditor`, `cal0-mechanics-auditor`, `prose-editor`, and `story-architect` for plot/future alignment. Partition large scopes by dimension or chapter range; keep evidence boundaries identical where comparisons matter. Where project custom-agent types are unavailable, use generic subagents with the matching `.codex/agents/*.toml` role contract.
4. Record findings with stable IDs, severity, precise location, governing evidence, impact, smallest correction, and verification condition.
5. Reconcile duplicates and conflicts. Mark uncertainty when the source hierarchy cannot establish an answer.
6. Identify systemic patterns separately from isolated defects. Do not inflate repeated manifestations into unrelated findings.
7. Save the audit contract, source manifest, independent findings, reconciliation record, and validation results under `workbench/runs/<run-id>/`.
8. Recommend repair order based on dependency: authoritative fact or delta first, derived artifacts second, prose/outline dependants third.

## Boundaries

Remain read-only unless the Author separately requests repair. Do not promote interpretations to canon, decide between equally valid creative alternatives, or change CAL0 to legalize prose.

## Output

Return scope and baseline, findings by severity/category, clean dimensions, dependency-ordered repair plan, and decisions requiring the Author.
