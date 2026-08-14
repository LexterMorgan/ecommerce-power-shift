#!/usr/bin/env python3
"""Wrapper: Gate 7B SQL/dashboard data layer."""
import runpy
from pathlib import Path

runpy.run_path(
    str(Path(__file__).resolve().parents[1] / "python" / "build_dashboard_sql.py"),
    run_name="__main__",
)
