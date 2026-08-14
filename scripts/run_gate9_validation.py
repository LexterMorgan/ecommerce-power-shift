#!/usr/bin/env python3
"""Wrapper: Gate 9 validation."""
import runpy
from pathlib import Path

runpy.run_path(
    str(
        Path(__file__).resolve().parents[1]
        / "python"
        / "validation"
        / "gate9_validate.py"
    ),
    run_name="__main__",
)
