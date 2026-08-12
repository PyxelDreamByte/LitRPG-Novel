# Writing Council Protocol

## Role sequence

1. The orchestrator locks inputs and permissions.
2. Review roles perform independent first passes; do not show them another reviewer's conclusions.
3. The orchestrator deduplicates findings and exposes only genuine conflicts for challenge.
4. One revision editor changes the manuscript.
5. Reviewers verify their accepted blocking or major findings; the reviser never approves its own work.

## Finding contract

Use `governance/templates/review-finding.md` exactly. Record each finding as:

- `finding_id`: stable within the workflow run;
- `reviewer_role`: the responsible specialist;
- `severity`: `BLOCKING`, `MAJOR`, `MINOR`, or `OPTIONAL`;
- `status`: normally `OPEN` until independently verified;
- `target`: precise artifact and passage or scene;
- `claim`: one defect or recommendation;
- `evidence`: governing source, target, and observed conflict;
- `consequence if unchanged`: reader, continuity, causality, character, world, or System impact;
- `smallest sufficient correction`: required outcome without an unauthorized line edit;
- `verification`: observable condition for closure.

Block only contradictions, impossible causality/mechanics, broken chapter contracts, viewpoint knowledge leakage, or defects that invalidate later state. Treat bounded local defects as minor and preference as optional. Only blocking and major findings reopen a normal review round.

## Modes

- `fast`: one drafter, continuity/character/CAL0 gates as relevant, one revision pass.
- `standard`: planning check, one drafter, all relevant independent reviewers, up to two revision rounds.
- `deep`: compare a small number of scene approaches before one drafter owns the manuscript; run the standard review afterward.

Default to `standard`. Use `deep` only when the Author requests it or a high-impact structural choice warrants the extra cost.

## Boundaries

Do not let agents silently change canon, CAL0 architecture, accepted future plot, or another agent's owned file. Keep reviewer outputs outside the manuscript. Escalate value conflicts and equally viable creative alternatives to the Author.

## Runtime mapping

In local Codex clients, spawn the matching project custom agent from `.codex/agents/`. In ChatGPT Work or another surface where project custom-agent types are not registered, spawn a generic subagent with one bounded role and include the matching TOML's `developer_instructions` in its task contract. Do not claim a custom agent type was used when the runtime did not expose it.
