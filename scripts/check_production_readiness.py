"""
Gate 10 — production-readiness checks for static Vercel deployment.

Does not modify Gate 9 analytical validation semantics.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "data" / "metadata" / "gate10_production_readiness.json"
STATIC_DATA = ROOT / "frontend" / "public" / "data" / "dashboard_data.json"

REQUIRED_FILES = [
    ROOT / ".env.example",
    ROOT / "frontend" / "vercel.json",
    ROOT / "frontend" / "public" / "data" / "dashboard_data.json",
    ROOT / "scripts" / "export_dashboard_data.py",
    ROOT / "python" / "dashboard_data.py",
    ROOT / "sql" / "schema.sql",
    ROOT / "README.md",
    ROOT / "research" / "dashboard_data_contract.md",
    ROOT / "research" / "gate10_deployment.md",
]


def _check(name: str, ok: bool, detail: str) -> dict:
    return {"check": name, "status": "PASS" if ok else "FAIL", "detail": detail}


def run_checks() -> dict:
    checks = []
    for path in REQUIRED_FILES:
        checks.append(
            _check(
                "file_{}".format(path.relative_to(ROOT)),
                path.exists(),
                "present" if path.exists() else "missing",
            )
        )

    # No FastAPI public surface
    checks.append(
        _check(
            "api_package_removed",
            not (ROOT / "api" / "main.py").exists(),
            "api/main.py absent",
        )
    )
    checks.append(
        _check(
            "dockerfile_removed",
            not (ROOT / "Dockerfile").exists(),
            "API Dockerfile absent",
        )
    )
    checks.append(
        _check(
            "procfile_removed",
            not (ROOT / "Procfile").exists(),
            "API Procfile absent",
        )
    )

    fe_src = ""
    src_root = ROOT / "frontend" / "src"
    if src_root.exists():
        for p in src_root.rglob("*"):
            if p.suffix in {".ts", ".tsx"}:
                fe_src += p.read_text()
    checks.append(
        _check(
            "frontend_no_api_fetch_paths",
            "/api/" not in fe_src and "VITE_API_BASE" not in fe_src,
            "no /api/ or VITE_API_BASE in frontend src",
        )
    )
    checks.append(
        _check(
            "frontend_loads_static_json",
            "dashboard_data.json" in fe_src,
            "static dashboard_data.json referenced",
        )
    )

    # Static contract values
    if STATIC_DATA.exists():
        data = json.loads(STATIC_DATA.read_text())
        checks.append(
            _check(
                "static_locked_shopee_2025",
                data["overview"]["phase3_post_break"]["shopee_2025"] == 54.0,
                str(data["overview"]["phase3_post_break"]["shopee_2025"]),
            )
        )
        checks.append(
            _check(
                "static_unknown_null",
                all(r.get("value") is None for r in data["legacy_unknown"]),
                "legacy unknown nulls",
            )
        )
        checks.append(
            _check(
                "static_deployment_mode",
                data.get("deployment_mode") == "static_snapshot",
                str(data.get("deployment_mode")),
            )
        )
    else:
        checks.append(_check("static_data_present", False, "missing dashboard_data.json"))

    # SQL analytical layer preserved
    checks.append(
        _check(
            "sql_schema_preserved",
            (ROOT / "sql" / "schema.sql").exists(),
            "sql/schema.sql present",
        )
    )
    checks.append(
        _check(
            "build_dashboard_sql_preserved",
            (ROOT / "python" / "build_dashboard_sql.py").exists(),
            "Gate 7B builder present",
        )
    )

    gitignore = (ROOT / ".gitignore").read_text() if (ROOT / ".gitignore").exists() else ""
    checks.append(_check("gitignore_env", ".env" in gitignore, ".env ignored"))

    readme = (ROOT / "README.md").read_text() if (ROOT / "README.md").exists() else ""
    checks.append(
        _check(
            "readme_static_architecture",
            "static" in readme.lower() and "PostgreSQL" in readme and "Vercel" in readme,
            "README describes static public + PostgreSQL analytical",
        )
    )

    failed = [c for c in checks if c["status"] == "FAIL"]
    return {
        "gate": "10B",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "PASS" if not failed else "FAIL",
        "checks_total": len(checks),
        "checks_failed": len(failed),
        "checks": checks,
        "manual_steps_remaining": [
            "Connect the GitHub repo to Vercel with root directory frontend/.",
            "Ensure frontend/public/data/dashboard_data.json is committed after export.",
            "Capture real screenshots after the static site is reachable.",
        ],
        "public_requires_database_url": False,
        "public_requires_fastapi": False,
        "cors_required_for_public_ui": False,
    }


def main() -> int:
    report = run_checks()
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(report, indent=2))
    print("GATE10_READINESS={}".format(report["status"]))
    print("Checks={} failed={}".format(report["checks_total"], report["checks_failed"]))
    print("JSON → {}".format(OUT_JSON))
    for step in report["manual_steps_remaining"]:
        print("MANUAL: {}".format(step))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
