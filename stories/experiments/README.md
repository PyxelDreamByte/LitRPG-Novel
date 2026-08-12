# Experiments

Experiments test voice, structure, scene approaches, or mechanics presentation. They are non-canonical by default and may not update world, character, or story state.

Evaluation experiments must declare `mode: EVALUATION`, `canonicality: NONCANONICAL_EVALUATION_ONLY`, and `promotion: FORBIDDEN` in their work manifest. Their workflow-eval manifests remain hash-bound static fixtures. Passing a static fixture does not prove live model behaviour.

Use a declared unit token and path, normally `fixture` at `units/fixture`. Hash-bound inputs remain read-only; mutable live-evaluation outputs go only beneath `runs_root/<run-id>/outputs/`.

Label any extracted idea as a proposal and route it through normal review before reuse.
