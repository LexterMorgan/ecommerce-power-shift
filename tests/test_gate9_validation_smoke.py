"""Gate 9 validation smoke tests."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_JSON = ROOT / "data" / "metadata" / "gate9_validation_results.json"
REPORT_MD = ROOT / "research" / "gate9_validation_report.md"


def test_gate9_validation_passes():
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "run_gate9_validation.py")],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "GATE9_STATUS=PASS" in proc.stdout
    assert REPORT_JSON.exists()
    assert REPORT_MD.exists()
    payload = json.loads(REPORT_JSON.read_text())
    assert payload["status"] == "PASS"
    assert payload["checks_failed"] == 0
    assert payload["locked_story_reference"]["shopee_2025"] == 54.0
    assert payload["locked_story_reference"]["legacy_2025"] == "UNKNOWN"
    assert payload["dashboard_runtime"].get("static_snapshot") == "ok"


def test_gate9_report_lists_remaining_items():
    if not REPORT_JSON.exists():
        subprocess.check_call(
            [sys.executable, str(ROOT / "scripts" / "run_gate9_validation.py")],
            cwd=str(ROOT),
        )
    payload = json.loads(REPORT_JSON.read_text())
    blockers = payload["deployment_blockers_for_gate10"]
    assert any("Vercel" in b or "screenshot" in b.lower() for b in blockers)
    md = REPORT_MD.read_text()
    assert "Local run" in md
    assert "export_dashboard_data" in md
