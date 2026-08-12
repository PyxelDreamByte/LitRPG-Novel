#!/usr/bin/env python3
"""Select bounded CAL0 context from generated routing indexes."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
ROUTING_PATH = ROOT / "litrpg-system/indices/topic-routing.json"
DECISIONS_PATH = ROOT / "litrpg-system/indices/architecture-decisions.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--topic")
    selection.add_argument("--decision")
    selection.add_argument("--list-topics", action="store_true")
    parser.add_argument("--paths", action="store_true", help="emit concise path and line selections")
    args = parser.parse_args()

    routing = json.loads(ROUTING_PATH.read_text(encoding="utf-8"))
    routes = {route["topic"]: route for route in routing["topics"]}
    if args.list_topics:
        for key, route in routes.items():
            print(f"{key}\t{route['description']}")
        return 0

    selected_decision = None
    if args.decision:
        decisions = json.loads(DECISIONS_PATH.read_text(encoding="utf-8"))["decisions"]
        selected_decision = next(
            (decision for decision in decisions if decision["selected_option_id"] == args.decision),
            None,
        )
        if selected_decision is None:
            print(f"unknown CAL0 selected-option ID: {args.decision}", file=sys.stderr)
            return 2
        matches = [route for route in routes.values() if args.decision in route["decision_refs"]]
        if len(matches) != 1:
            print(f"decision {args.decision} has {len(matches)} topic routes; regenerate indexes", file=sys.stderr)
            return 1
        route = matches[0]
    else:
        route = routes.get(args.topic)
        if route is None:
            print(f"unknown System topic: {args.topic}; use --list-topics", file=sys.stderr)
            return 2

    result = {
        "cal0_bundle_id": routing["cal0_bundle_id"],
        "topic": route["topic"],
        "description": route["description"],
        "selected_decision": selected_decision,
        "read_first": [
            "litrpg-system/cal0/guide/litrpg-system-story-guide.md",
            "litrpg-system/cal0/guide/litrpg-system-worked-scenarios.md",
        ],
        "specification_path": "litrpg-system/cal0/canonical/litrpg-system-specification.md",
        "specification_sections": route["specification_sections"],
        "numeric_escalation": [
            "litrpg-system/cal0/canonical/litrpg-system-calibration-annex.md",
            "litrpg-system/cal0/registries/",
            "litrpg-system/cal0/src/cal0/",
        ],
    }
    if args.paths:
        for path in result["read_first"]:
            print(path)
        for section in result["specification_sections"]:
            print(
                f"{result['specification_path']}:{section['line_start']}-{section['line_end']}"
                f"\t{section['section_code']}"
            )
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

