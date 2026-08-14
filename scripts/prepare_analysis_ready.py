#!/usr/bin/env python3
"""Wrapper: build analysis-ready competitive panel from processed data."""
import runpy
from pathlib import Path

runpy.run_path(
    str(Path(__file__).resolve().parents[1] / "python" / "prepare_analysis_ready.py"),
    run_name="__main__",
)
