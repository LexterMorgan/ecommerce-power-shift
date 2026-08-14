"""
Gate 9 — End-to-end validation (no metric reinterpretation).

Validates locked panel values, UNKNOWN null handling, structural-break
separation, dashboard/API consistency, claim-label presence, and provenance
columns. Does not modify Gates 1–8 conclusions or data.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
from sqlalchemy import text

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

PANEL = ROOT / "data" / "processed" / "analysis_ready" / "competitive_panel.csv"
SHARE_GAP = ROOT / "analysis" / "outputs" / "tables" / "share_gap_summary.csv"
MANIFEST = ROOT / "data" / "dashboard" / "manifest.json"
GATE5 = ROOT / "research" / "gate5_competitive_analysis.md"
GATE6 = ROOT / "research" / "gate6_competitive_evolution.md"
GATE8 = ROOT / "research" / "gate8_dashboard_architecture.md"
OUT_JSON = ROOT / "data" / "metadata" / "gate9_validation_results.json"
OUT_MD = ROOT / "research" / "gate9_validation_report.md"

LOCKED_SHARES = {
    (2022, "Shopee", "market_share_pct", "OBSERVED"): 36.0,
    (2022, "Legacy Tokopedia", "market_share_pct", "OBSERVED"): 35.0,
    (2024, "Shopee", "market_share_pct", "OBSERVED"): 46.0,
    (2024, "Legacy Tokopedia", "market_share_pct", "OBSERVED"): 23.0,
    (2025, "Shopee", "market_share_pct", "OBSERVED"): 54.0,
    (2025, "Combined Tokopedia + TikTok Shop", "market_share_pct", "OBSERVED"): 38.0,
    (2024, "Combined Tokopedia + TikTok Shop", "market_share_pct", "DERIVED"): 34.0,
}


def _check(name: str, ok: bool, detail: str) -> Dict[str, Any]:
    return {"check": name, "status": "PASS" if ok else "FAIL", "detail": detail}


def validate_transformations(panel: pd.DataFrame) -> List[Dict[str, Any]]:
    checks = []
    checks.append(
        _check(
            "panel_row_count",
            len(panel) == 22,
            f"rows={len(panel)} expected=22",
        )
    )
    entities = set(panel["analytical_entity"].astype(str))
    allowed = {
        "Shopee",
        "Legacy Tokopedia",
        "TikTok Shop",
        "Combined Tokopedia + TikTok Shop",
    }
    checks.append(
        _check(
            "panel_analytical_allowlist",
            entities <= allowed and not (entities & {"Bukalapak", "Lazada", "Blibli"}),
            f"entities={sorted(entities)}",
        )
    )
    required = {
        "year",
        "analytical_entity",
        "metric",
        "value",
        "value_status",
        "comparability",
        "citation_url",
        "confidence",
        "source_publisher",
    }
    missing = sorted(required - set(panel.columns))
    checks.append(
        _check("panel_required_columns", not missing, f"missing={missing or 'none'}")
    )
    return checks


def validate_analytical_metrics(panel: pd.DataFrame) -> List[Dict[str, Any]]:
    checks = []
    for (year, entity, metric, status), expected in LOCKED_SHARES.items():
        sub = panel[
            (panel["year"] == year)
            & (panel["analytical_entity"] == entity)
            & (panel["metric"] == metric)
            & (panel["value_status"] == status)
        ]
        ok = len(sub) == 1 and float(sub.iloc[0]["value"]) == expected
        checks.append(
            _check(
                f"locked_{year}_{entity}_{metric}_{status}",
                ok,
                f"expected={expected} got={None if sub.empty else sub.iloc[0]['value']}",
            )
        )

    unk = panel[
        (panel["year"] == 2025)
        & (panel["analytical_entity"] == "Legacy Tokopedia")
        & (panel["value_status"] == "UNKNOWN")
    ]
    checks.append(
        _check(
            "legacy_2025_unknown_null",
            len(unk) == 2 and unk["value"].isna().all(),
            f"rows={len(unk)} nulls={int(unk['value'].isna().sum())}",
        )
    )
    checks.append(
        _check(
            "unknown_never_zero",
            not ((panel["value_status"] == "UNKNOWN") & (panel["value"] == 0)).any(),
            "no UNKNOWN rows with value=0",
        )
    )
    return checks


def validate_structural_break(panel: pd.DataFrame) -> List[Dict[str, Any]]:
    standalone = panel[
        (panel["year"].between(2022, 2024))
        & (panel["metric"] == "market_share_pct")
        & (panel["analytical_entity"].isin(["Shopee", "Legacy Tokopedia"]))
        & (panel["entity_type"] == "standalone")
        & (panel["value_status"] == "OBSERVED")
        & (panel["value"].notna())
    ]
    post = panel[
        (panel["year"] == 2025)
        & (panel["metric"] == "market_share_pct")
        & (panel["value_status"] == "OBSERVED")
        & (panel["value"].notna())
        & (
            (panel["analytical_entity"] == "Shopee")
            | (
                (panel["analytical_entity"] == "Combined Tokopedia + TikTok Shop")
                & (panel["entity_type"] == "combined")
            )
        )
    ]
    return [
        _check("standalone_share_rows", len(standalone) == 6, f"n={len(standalone)}"),
        _check(
            "post_break_excludes_legacy",
            "Legacy Tokopedia" not in set(post["analytical_entity"]),
            f"entities={sorted(set(post['analytical_entity']))}",
        ),
        _check("post_break_share_rows", len(post) == 2, f"n={len(post)}"),
    ]


def validate_dashboard_layer(panel: pd.DataFrame) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    checks: List[Dict[str, Any]] = []
    meta: Dict[str, Any] = {"postgres": "skipped", "static_snapshot": "skipped"}

    if MANIFEST.exists():
        manifest = json.loads(MANIFEST.read_text())
        checks.append(
            _check(
                "dashboard_manifest_postgres",
                manifest.get("database_engine") == "postgresql",
                f"engine={manifest.get('database_engine')}",
            )
        )
        checks.append(
            _check(
                "sqlite_deprecated",
                manifest.get("sqlite_status") == "deprecated_removed",
                f"sqlite_status={manifest.get('sqlite_status')}",
            )
        )
    else:
        checks.append(_check("dashboard_manifest_present", False, "manifest.json missing"))

    if SHARE_GAP.exists():
        gaps = pd.read_csv(SHARE_GAP)
        p3 = gaps[gaps["panel"] == "phase3_post_break"]
        ok = len(p3) == 1 and abs(float(p3.iloc[0]["gap_pp"]) - 16.0) < 1e-9
        checks.append(_check("share_gap_2025_pp", ok, f"rows={len(p3)}"))
    else:
        checks.append(_check("share_gap_summary_present", False, "missing Gate 7A table"))

    # Static snapshot + optional PostgreSQL analytical parity
    try:
        from python.dashboard_data import build_dashboard_data

        snap = build_dashboard_data()
        ov = snap["overview"]
        checks.append(
            _check(
                "static_overview_shopee_2025",
                ov["phase3_post_break"]["shopee_2025"] == 54.0,
                f"got={ov['phase3_post_break']['shopee_2025']}",
            )
        )
        checks.append(
            _check(
                "static_overview_combined_2025",
                ov["phase3_post_break"]["combined_2025"] == 38.0,
                f"got={ov['phase3_post_break']['combined_2025']}",
            )
        )
        checks.append(
            _check(
                "static_overview_legacy_unknown_label",
                ov["phase3_post_break"]["legacy_tokopedia_2025"] == "UNKNOWN",
                f"got={ov['phase3_post_break']['legacy_tokopedia_2025']}",
            )
        )
        unk_rows = ov["legacy_unknown_rows"]
        checks.append(
            _check(
                "static_unknown_values_null",
                len(unk_rows) == 2 and all(r.get("value") is None for r in unk_rows),
                f"n={len(unk_rows)}",
            )
        )
        meta["static_snapshot"] = "ok"
    except Exception as exc:  # noqa: BLE001
        checks.append(_check("static_snapshot_build", False, str(exc)))
        meta["static_snapshot"] = f"error: {exc}"

    try:
        from python.db import get_engine

        engine = get_engine()
        with engine.connect() as conn:
            n = conn.execute(text("SELECT COUNT(*) FROM fact_competitive_panel")).scalar_one()
        checks.append(
            _check("postgres_panel_count", int(n) == len(panel), f"db={n} csv={len(panel)}")
        )
        meta["postgres"] = "ok"
    except Exception as exc:  # noqa: BLE001
        checks.append(
            _check(
                "postgres_analytical_reachable",
                False,
                f"PostgreSQL analytical DB unavailable (optional for static UI): {exc}",
            )
        )
        meta["postgres"] = f"error: {exc}"
    return checks, meta


def validate_claims_and_provenance(panel: pd.DataFrame) -> List[Dict[str, Any]]:
    checks = []
    for path, needles in [
        (GATE5, ["Not claimed", "UNSUPPORTED", "UNKNOWN", "Combined"]),
        (GATE6, ["SCENARIO", "structural", "UNKNOWN"]),
        (GATE8, ["PostgreSQL", "UNKNOWN", "Vercel"]),
    ]:
        if not path.exists():
            checks.append(_check(f"doc_exists_{path.name}", False, "missing"))
            continue
        text_body = path.read_text()
        missing = [n for n in needles if n not in text_body]
        checks.append(
            _check(
                f"claim_doc_{path.name}",
                not missing,
                f"missing_phrases={missing or 'none'}",
            )
        )

    observed = panel[panel["value_status"] == "OBSERVED"]
    missing_cite = int(observed["citation_url"].isna().sum()) + int(
        (observed["citation_url"].astype(str).str.strip() == "").sum()
    )
    checks.append(
        _check(
            "observed_have_citation",
            missing_cite == 0,
            f"observed_missing_citation={missing_cite}",
        )
    )
    checks.append(
        _check(
            "value_status_vocabulary",
            set(panel["value_status"]).issubset({"OBSERVED", "DERIVED", "UNKNOWN"}),
            f"statuses={sorted(set(panel['value_status']))}",
        )
    )
    return checks


def deployment_blockers() -> List[str]:
    return [
        "Public Vercel project may still need to be connected/published (manual).",
        "Regenerate frontend/public/data/dashboard_data.json after analytical refreshes.",
        "Real portfolio screenshots remain a manual capture step.",
        "Event timeline / driver pages intentionally out of Gate 7B scope.",
        "PostgreSQL remains local/analytical infrastructure (not required by the public static UI).",
    ]


def run_validation() -> Dict[str, Any]:
    if not PANEL.exists():
        raise FileNotFoundError(f"Missing canonical panel: {PANEL}")
    panel = pd.read_csv(PANEL)

    sections = {
        "transformations": validate_transformations(panel),
        "analytical_metrics": validate_analytical_metrics(panel),
        "structural_break": validate_structural_break(panel),
        "claims_provenance": validate_claims_and_provenance(panel),
    }
    dash_checks, dash_meta = validate_dashboard_layer(panel)
    sections["dashboard_metrics"] = dash_checks

    all_checks = [c for cs in sections.values() for c in cs]
    failed = [c for c in all_checks if c["status"] == "FAIL"]
    status = "PASS" if not failed else "FAIL"

    report = {
        "gate": "9",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "checks_total": len(all_checks),
        "checks_failed": len(failed),
        "sections": sections,
        "dashboard_runtime": dash_meta,
        "deployment_blockers_for_gate10": deployment_blockers(),
        "locked_story_reference": {
            "shopee_2022": 36.0,
            "legacy_2022": 35.0,
            "shopee_2024": 46.0,
            "legacy_2024": 23.0,
            "shopee_2025": 54.0,
            "combined_2025": 38.0,
            "legacy_2025": "UNKNOWN",
        },
        "next_gate": "10 — Documentation & Deployment",
    }
    return report


def write_report(report: Dict[str, Any]) -> None:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(report, indent=2))

    lines = [
        "# Gate 9 — Validation Report",
        "",
        f"**Status:** {report['status']}",
        f"**Generated (UTC):** {report['generated_at']}",
        f"**Checks:** {report['checks_total']} total · {report['checks_failed']} failed",
        "",
        "## Scope",
        "",
        "Validates Gates 1–8 locked outputs without changing metrics, schema, views, or conclusions.",
        "",
        "## Locked story reference (unchanged)",
        "",
        "| Item | Value |",
        "|------|------:|",
    ]
    for k, v in report["locked_story_reference"].items():
        lines.append(f"| `{k}` | {v} |")

    lines += ["", "## Check results", ""]
    for section, checks in report["sections"].items():
        lines.append(f"### {section}")
        lines.append("")
        for c in checks:
            lines.append(f"- **{c['status']}** `{c['check']}` — {c['detail']}")
        lines.append("")

    lines += [
        "## Dashboard runtime",
        "",
        f"- PostgreSQL: `{report['dashboard_runtime'].get('postgres')}`",
        f"- Static snapshot: `{report['dashboard_runtime'].get('static_snapshot')}`",
        "",
        "## Claim / provenance review",
        "",
        "- Gate 5/6 claim-discipline phrases remain present in research docs.",
        "- OBSERVED panel rows retain citation URLs.",
        "- UNKNOWN Legacy Tokopedia 2025 values remain null (not zero).",
        "- Combined ≠ Legacy structural-break separation retained in panel and API overview.",
        "",
        "## Local run (current system)",
        "",
        "```bash",
        "export DATABASE_URL=postgresql://localhost:5432/ecommerce_power_shift",
        "python3 scripts/build_dashboard_sql.py   # analytical PostgreSQL layer",
        "python3 scripts/export_dashboard_data.py # static React snapshot",
        "cd frontend && npm install && npm run dev",
        "python3 scripts/run_gate9_validation.py",
        "```",
        "",
        "## Remaining before public portfolio polish",
        "",
    ]
    for b in report["deployment_blockers_for_gate10"]:
        lines.append(f"- {b}")
    lines += [
        "",
        f"**Exact next gate:** {report['next_gate']}",
        "",
    ]
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    report = run_validation()
    write_report(report)
    print(f"GATE9_STATUS={report['status']}")
    print(f"Checks={report['checks_total']} failed={report['checks_failed']}")
    print(f"Report → {OUT_MD}")
    print(f"JSON → {OUT_JSON}")
    print(f"NEXT_GATE={report['next_gate']}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
