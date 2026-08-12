# Decision Policy

## Purpose

Decision records preserve what the Author chose, why it was chosen, its consequences, and what would justify reconsideration. They prevent an old discussion, a new draft, or an agent preference from masquerading as a changed decision.

## Required fields

Every binding decision records:

- stable decision ID;
- stable `author-decision://` URI and human display code;
- title and domain;
- workflow status, canon status, and scope;
- disposition date, Author confirmation, and approval evidence for `ACCEPTED`, `PROVISIONAL`, `DEFERRED`, or `REJECTED` decisions;
- question decided;
- selected option in operational language;
- alternatives considered;
- rationale and evidence;
- consequences and affected sources;
- dependencies and conflicts;
- residual unknowns;
- supersedes/superseded-by links;
- reopening conditions.

Use `governance/templates/decision-record.md` and validate structured records against the applicable governance schema.

An Author-approved deferral is complete decision work. Its selection must state
what is not being decided and its reopening conditions must define the
prerequisites for activation. Never fill a deferred value with a convenient
default.

Project-level reusable defaults must declare whether future works inherit them.
The default policy is explicit adoption in each work manifest; no independent
work is silently bound.

## Stable identifiers

- Preserve established CAL0 and architecture codes exactly.
- Give every new Author decision a stable URI of the form `author-decision://<domain>/<display-code>`; use the established code as its display code and routing label.
- Use `REP` for repository governance, `WLD` for setting, `CHR` for character, `SER` for series, `B##` for book-specific decisions, and `RET` for retcons unless a narrower accepted namespace exists.
- Never recycle an ID after rejection or supersession.
- A refinement may use a dotted child ID; a replacement receives a new ID and links to the old one.

## Reconsideration

An accepted decision may be reopened only when at least one of these is present:

- a concrete contradiction;
- failed validation or infeasible implementation;
- new evidence that materially changes the choice;
- a required story outcome that cannot be achieved inside the decision;
- an explicit Author request to reconsider.

Reopening does not erase the original decision. Create a proposal that maps affected canon, chapters, System behaviour, outlines, and future payoffs. A CAL0 architecture change additionally requires a successor register entry and regression evidence.

## Decision councils

For materially different options, reviewers analyse independently before deliberation. The orchestrator presents genuine choices, implications, reversibility, and a recommendation. It must not manufacture consensus, collapse distinct trade-offs, or record a decision before the Author selects it.
