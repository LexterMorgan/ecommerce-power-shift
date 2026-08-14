#!/usr/bin/env python3
"""Export analysis-ready dashboard snapshot for the static React app."""
import runpy
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from python.dashboard_data import FRONTEND_DATA, write_dashboard_data


def main() -> int:
    path = write_dashboard_data()
    print("DASHBOARD_EXPORT=PASS")
    print("Wrote {}".format(path.relative_to(ROOT)))
    print("Regenerate: python3 scripts/export_dashboard_data.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
