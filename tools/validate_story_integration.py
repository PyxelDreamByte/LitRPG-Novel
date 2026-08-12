#!/usr/bin/env python3
"""Repository-root entrypoint for the story-integration validator."""

from pathlib import Path
import runpy


VALIDATOR = (
    Path(__file__).resolve().parents[1]
    / "litrpg-system/story-integration/validators/validate.py"
)
runpy.run_path(str(VALIDATOR), run_name="__main__")

