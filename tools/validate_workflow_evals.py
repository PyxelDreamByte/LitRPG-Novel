#!/usr/bin/env python3
"""Run the deterministic workspace/evaluation manifest gate."""

from pathlib import Path
import runpy


RUNNER = Path(__file__).resolve().with_name("validate_workspaces.py")
runpy.run_path(str(RUNNER), run_name="__main__")

