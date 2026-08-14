"""Gate 10B static-dashboard readiness + export tests."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATIC = ROOT / "frontend" / "public" / "data" / "dashboard_data.json"
REPORT = ROOT / "data" / "metadata" / "gate10_production_readiness.json"


def test_export_dashboard_data():
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "export_dashboard_data.py")],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "DASHBOARD_EXPORT=PASS" in proc.stdout
    assert STATIC.exists()
    data = json.loads(STATIC.read_text())
    assert data["deployment_mode"] == "static_snapshot"
    assert data["overview"]["phase3_post_break"]["shopee_2025"] == 54.0
    assert data["overview"]["phase3_post_break"]["combined_2025"] == 38.0
    assert data["overview"]["phase3_post_break"]["legacy_tokopedia_2025"] == "UNKNOWN"
    assert len(data["standalone_shares"]) == 6
    assert len(data["post_break_shares"]) == 2
    assert all(r["value"] is None for r in data["legacy_unknown"])
    assert all(r.get("value_type") == "SCENARIO" for r in data["scenarios"])
    assert len(data["competitive_panel"]) == 22
    entities = {r["analytical_entity"] for r in data["competitive_panel"]}
    assert entities <= {
        "Shopee",
        "Legacy Tokopedia",
        "TikTok Shop",
        "Combined Tokopedia + TikTok Shop",
    }
    assert not entities & {"Bukalapak", "Lazada", "Blibli"}
    markets = {r["marketplace"] for r in data["filter_keys"]}
    assert not markets & {"Bukalapak", "Lazada", "Blibli"}


def test_production_readiness_static():
    subprocess.check_call(
        [sys.executable, str(ROOT / "scripts" / "export_dashboard_data.py")],
        cwd=str(ROOT),
    )
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_production_readiness.py")],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        env=os.environ.copy(),
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    payload = json.loads(REPORT.read_text())
    assert payload["status"] == "PASS"
    assert payload["public_requires_fastapi"] is False
    assert payload["public_requires_database_url"] is False
    assert payload["cors_required_for_public_ui"] is False


def test_no_api_package_or_dockerfile():
    assert not (ROOT / "api" / "main.py").exists()
    assert not (ROOT / "Dockerfile").exists()
    assert not (ROOT / "Procfile").exists()
    assert (ROOT / "sql" / "schema.sql").exists()
    assert (ROOT / "python" / "build_dashboard_sql.py").exists()


def test_contract_doc_exists():
    path = ROOT / "research" / "dashboard_data_contract.md"
    assert path.exists()
    text = path.read_text()
    assert "dashboard_data.json" in text
    assert "UNKNOWN" in text
    assert "export_dashboard_data.py" in text
