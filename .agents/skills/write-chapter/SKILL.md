---
name: write-chapter
description: "Draft and iteratively review a chapter through a bounded writing council with one manuscript owner. Use when the Author asks to write or substantially redraft a chapter from an approved chapter contract and context pack, with continuity, world-canon, character, plot, prose, and CAL0 checks."
---

# Write Chapter

Use one manuscript owner and independent reviewers. Avoid committee prose and unbounded revision.

Read [references/council-protocol.md](references/council-protocol.md) before spawning the writing council.

## Preconditions

Require an explicitly Author-approved chapter card revision, authoritative predecessor, intended destination, non-expired bounded context pack, and its run/source manifest. If any item is absent or stale, invoke `$plan-chapter` and do not draft.

## Workflow

1. Create `workbench/runs/<run-id>/` and preserve the workflow contract, source manifest, approved card revision, context-pack ID, mode, role assignments, target manuscript revision, findings, change sets, validation results, and unresolved decisions throughout the run.
2. Ask `story-architect` for beat risks or a scene approach when structural uncertainty remains.
3. Assign `chapter-drafter` sole ownership of the initial manuscript. The drafter may make reversible scene-level choices but must flag new setting, character-history, or System facts.
4. Run independent post-draft review in waves of no more than three subagents, using the exact applicable roles:
   - `continuity-auditor` for continuity and causal state;
   - `character-pov-auditor` for motive, knowledge, agency, and viewpoint;
   - `world-canon-auditor` for setting fit and all new world facts;
   - `cal0-mechanics-auditor` for every System-bearing chapter;
   - `prose-editor` for line/scene quality in a later wave after structure is stable;
   - `story-architect` again for plot threads, chapter-contract compliance, setup/payoff, and future alignment.
5. Synthesize findings into one deduplicated change set with stable IDs, severity, evidence, and acceptance test. Resolve reviewer disagreement through a focused challenge round, not a group rewrite.
6. Assign `revision-editor` sole ownership of revisions. Preserve successful passages and apply only the accepted change set.
7. Re-run only affected gates. Limit normal work to two revision rounds; use a third only for a justified blocking issue, then escalate unresolved conflicts to the Author.
8. Produce the Author-facing draft delta and paired machine-readable `*.chapter-delta.json`. Use schema enum names for canon proposals. Preserve `MINOR` findings in run evidence, the Author-facing review, and the machine delta's `review.minor_findings` array; do not downcast them to `OPTIONAL`.
9. Save the final review summary, source manifest, exact manuscript/delta revisions, validation evidence, and unresolved findings in the run directory. Do not promote any draft artifact.

## Output

Return the workflow run path, exact manuscript and delta revisions, review summary, unresolved findings including preserved `MINOR` items, canon proposals, files changed, and whether the transaction is ready for `$accept-chapter`.
