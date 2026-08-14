#!/usr/bin/env python3
"""Wrapper: Gate 7A analysis/visualization layer."""
import runpy
from pathlib import Path

runpy.run_path(
    str(Path(__file__).resolve().parents[1] / "analysis" / "run_analysis.py"),
    run_name="__main__",
)
