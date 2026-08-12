# CAL0 context routing

The routing layer helps an agent retrieve only the System context relevant to a
scene or review. It is a selector, not a new authority.

## Route order

1. Identify the mechanic or selected-option ID involved.
2. Run `python3 tools/route_system_context.py --topic <topic>` or pass
   `--decision <selected-option-id>`.
3. Start with the story guide and worked scenarios.
4. Read only the returned specification sections.
5. Escalate to the calibration annex, registries, and executable implementation
   when the decision turns on numbers or model behaviour.
6. Record every binding mechanical conclusion with its decision reference and
   CAL0 bundle ID.

Examples:

```bash
python3 tools/route_system_context.py --topic skills
python3 tools/route_system_context.py --decision ATR3.4.2.0D
python3 tools/route_system_context.py --list-topics
```

If a question spans multiple mechanics, call the router once per topic. Do not
load the entire specification merely because more than one section is needed.

