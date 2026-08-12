# Canon Policy

## Canon status

Every substantive creative or mechanical record uses one of these states:

| State | Meaning | May downstream work rely on it? |
|---|---|---|
| `ACCEPTED` | Explicitly approved by the Author and present in its authoritative location | Yes |
| `PROVISIONAL` | Approved for bounded use while a named question remains open | Only within its declared scope |
| `PROPOSED` | Candidate material awaiting review | No; use only as a labelled possibility |
| `DEFERRED` | Intentionally postponed without rejection | No |
| `REJECTED` | Considered and declined | No |
| `SUPERSEDED` | Replaced by a later accepted record and retained for provenance | No, except for historical reconstruction |

`PROVISIONAL`, `DEFERRED`, and `REJECTED` may record completed Author
dispositions. They require the same identifiable Author, date, decision URI,
and approval evidence as `ACCEPTED`. `DEFERRED` means the Author decided not to
set the value yet; it is not an agent's unresolved draft.

`DECIDED` may appear inside the locked CAL0 specification and legacy records. Within repository governance it corresponds to accepted authority at that source's declared scope; it does not make fixtures or examples story canon.

Use the field name `canon_status` in new human-authored frontmatter. Older
governance records may retain `status` until migrated, where it has the same
meaning.

## Workflow status is separate

Workflow status describes where an artifact is in a review process; it never
grants authority. Use `workflow_status` in human-authored records.

| Workflow status | Meaning | Default canon status |
|---|---|---|
| `DRAFT` | Being authored; not ready for a gate | `PROPOSED` |
| `IN_REVIEW` | Under specialist or Author review | `PROPOSED` |
| `AWAITING_AUTHOR` | Review complete and awaiting an explicit Author decision | `PROPOSED` |
| `ACCEPTED` | The exact reviewed artifact passed its Author gate | `ACCEPTED` or explicitly scoped `PROVISIONAL` |
| `REJECTED` | The exact artifact was declined | `REJECTED` |
| `SUPERSEDED` | A later accepted artifact replaced it | `SUPERSEDED` |
| `DERIVED` | Rebuilt from declared source records; never independently authoritative | Inherits only the accepted/provisional scope of its sources |
| `OPEN` / `RESOLVED` | Finding-specific review state | `PROPOSED`; findings do not establish fictional truth |

The story-integration v1 JSON schemas currently call their workflow field
`status`; interpret that field as `workflow_status`. The paired human record
must also declare `canon_status`. `DEFERRED` and `PROVISIONAL` are canon
decisions, not implicit machine-workflow states. No workflow status alone can
promote canon.

Valid pairings are:

- `DRAFT`, `IN_REVIEW`, or `AWAITING_AUTHOR` with `PROPOSED`;
- workflow `ACCEPTED` with canon `ACCEPTED`, `PROVISIONAL`, or `DEFERRED`;
- workflow `REJECTED` with canon `REJECTED`;
- workflow `SUPERSEDED` with canon `SUPERSEDED`.

Any other pairing is invalid unless this policy is first changed by an Author
decision.

## Identifier contract

Machine-linked creative artifacts use stable URI identifiers as their primary
IDs. Human-friendly codes remain display and decision-routing labels.

| Artifact | Primary identifier | Display code example |
|---|---|---|
| Series | `series://<series-slug>` | `SER-001` |
| Book | `book://<series-slug>/book-01` | `SER-001-B01` |
| Chapter | `chapter://<series-slug>/book-01/001` | `SER-001-B01-C001` |
| Chapter delta | `delta://<series-slug>/book-01/001` | `SER-001-B01-C001-D01` |
| Character | `character://<series-slug>/<character-slug>` | `CHR-001` |
| Snapshot | `snapshot://<series-slug>/<character-slug>/book-01/001` | `CHR-001-B01-C001-END` |
| Author decision | `author-decision://<domain>/<display-code>` | `REP0.1A` |

IDs never change when a title, character name, or filename changes. A display
code must not be supplied where a story-integration schema requires a URI.

## Canon domains

Acceptance is scoped. A fact may be authoritative in one domain without crossing into another:

- **System canon:** CAL0 natural-law architecture and its controlled successors.
- **World canon:** setting facts independent of any one story.
- **Series canon:** facts binding across a named series.
- **Book canon:** facts binding within one book and compatible with higher scopes.
- **Story state:** events and consequences accepted as having occurred.
- **Character truth:** identity, history, internal state, and actual knowledge.
- **Presentation:** interface wording or prose disclosed to a character or reader.

## Reusable project defaults

A project-level default or guardrail is not automatically canon for every work
in this multi-work repository. A future work manifest must explicitly cite the
decision URI, adopted scope, and effective revision before using it. Silence is
non-adoption.

A work may override an adopted default only through its own scoped Author
decision. That override governs the named work and does not rewrite the
project-level default or bind independent works.

## Promotion rules

A proposed fact becomes canon only when all of the following are true:

1. It has a stable identifier or an unambiguous location in an accepted artifact.
2. Its scope, status, source, and dependencies are declared.
3. Relevant world, character, continuity, plot, and CAL0 implications have been reviewed.
4. Conflicts are resolved or explicitly accepted as intentional uncertainty.
5. The Author explicitly accepts it.
6. The authoritative record and relevant indexes are updated together.

Draft prose never silently promotes worldbuilding. A chapter's new facts remain proposed until the Author accepts both the manuscript and its chapter delta.

## Chapter acceptance transaction

Chapter acceptance is one logical transaction containing:

- the final manuscript identified by repository path, revision, and SHA-256 digest;
- the Author-approved chapter delta;
- continuity and character-state changes;
- progression and resource changes with provenance;
- world or series canon additions;
- plot-thread and knowledge changes;
- unresolved questions and deliberately withheld information.
- the exact Author decision URI, approval evidence, and decision date.

If any required part is missing or contradictory, the chapter remains unaccepted. Derived ledgers, indexes, summaries, and snapshots must rebuild from accepted deltas rather than becoming competing manual sources.

## Canon discovery during drafting

Classify every new fact as:

| Class | Treatment |
|---|---|
| `LOCAL_COLOUR` | Record in the chapter delta when it could constrain later prose; normally `CHAPTER_ACCEPTANCE` |
| `CHARACTER_STATE_CHANGE` | Require `CONTINUITY_REVIEW`; update derived state after acceptance |
| `SETTING_EXTENSION` | Require `WORLDBUILDING_REVIEW` |
| `SYSTEM_APPLICATION` | Require `CAL0_MECHANICS_REVIEW` and causal provenance |
| `SYSTEM_CHANGE` | Require `AUTHOR_DECISION_REQUIRED` and the governed successor workflow; block chapter acceptance while unresolved |
| `CONTRADICTION_OR_RETCON` | Require `AUTHOR_DECISION_REQUIRED`; block acceptance until resolved |

## Uncertainty

Absence of a canon fact is not permission to invent one silently. Mark uncertainty as unknown, contested, viewpoint-limited, deliberately flexible, or awaiting Author decision. Preserve the difference between what is true, what a source records, what a character can access, how they interpret it, how it is presented, and what the reader sees.
