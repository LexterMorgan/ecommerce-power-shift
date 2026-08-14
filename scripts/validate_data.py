#!/usr/bin/env python3
"""Wrapper: same as process_data (validation is included)."""
import runpy
from pathlib import Path

runpy.run_path(str(Path(__file__).resolve().parents[1] / "python" / "process_data.py"), run_name="__main__")
