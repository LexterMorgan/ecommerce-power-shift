"""
Build the static dashboard data contract from analysis-ready CSVs.

No new metrics. Preserves OBSERVED/DERIVED/UNKNOWN/SCENARIO and UNKNOWN nulls.
Public React app consumes the exported JSON; PostgreSQL remains the analytical DB.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "data" / "processed" / "analysis_ready" / "competitive_panel.csv"
COMPARABLE = (
    ROOT / "data" / "processed" / "2025_comparable" / "platform_metrics_2025_processed.csv"
)
SCENARIO_OUT = ROOT / "data" / "processed" / "gate6_scenario_outputs.csv"
SHARE_GAP = ROOT / "analysis" / "outputs" / "tables" / "share_gap_summary.csv"

FRONTEND_DATA = ROOT / "frontend" / "public" / "data" / "dashboard_data.json"
CONTRACT_DOC = ROOT / "research" / "dashboard_data_contract.md"


def _records(df: pd.DataFrame) -> List[Dict[str, Any]]:
    # Preserve nulls as JSON null (never fill UNKNOWN with 0).
    return json.loads(df.where(pd.notnull(df), None).to_json(orient="records", date_format="iso"))


def _share(rows: List[dict], year: int, entity: str) -> Optional[float]:
    for r in rows:
        if int(r["year"]) == year and r["analytical_entity"] == entity and r.get("value") is not None:
            return float(r["value"])
    return None


def build_dashboard_data() -> Dict[str, Any]:
    if not PANEL.exists():
        raise FileNotFoundError("Missing {}".format(PANEL))
    panel = pd.read_csv(PANEL)
    supporting = pd.read_csv(COMPARABLE)
    scenarios = pd.read_csv(SCENARIO_OUT)
    share_gap = pd.read_csv(SHARE_GAP) if SHARE_GAP.exists() else pd.DataFrame()

    standalone = panel[
        (panel["year"].between(2022, 2024))
        & (panel["metric"] == "market_share_pct")
        & (panel["analytical_entity"].isin(["Shopee", "Legacy Tokopedia"]))
        & (panel["entity_type"] == "standalone")
        & (panel["value_status"] == "OBSERVED")
        & (panel["value"].notna())
    ].sort_values(["analytical_entity", "year"])

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
    ].sort_values("analytical_entity")

    legacy_unknown = panel[
        (panel["year"] == 2025)
        & (panel["analytical_entity"] == "Legacy Tokopedia")
        & (panel["value_status"] == "UNKNOWN")
    ].sort_values("metric")

    gmv = panel[
        (panel["metric"] == "gmv_estimate_usd_billion")
        & (panel["value_status"].isin(["OBSERVED", "DERIVED"]))
        & (panel["value"].notna())
    ].sort_values(["year", "analytical_entity"])

    access = supporting[
        (supporting["metric"] == "internet_user_access_share_pct")
        & (supporting["evidence_type"] == "OBSERVED")
        & (supporting["value"].notna())
    ].sort_values("entity")

    tts = supporting[
        (supporting["entity"] == "TikTok Shop Indonesia")
        & (supporting["metric"] == "gmv_estimate_usd")
        & (supporting["evidence_type"] == "OBSERVED")
        & (supporting["value"].notna())
    ].sort_values("entity")

    scen = scenarios[
        (scenarios["metric"] == "shopee_minus_combined_share_gap_pp")
        & (scenarios["value_type"] == "SCENARIO")
    ].sort_values("scenario_id")

    standalone_rows = _records(standalone)
    post_rows = _records(post)
    unknown_rows = _records(legacy_unknown)

    s22 = _share(standalone_rows, 2022, "Shopee")
    t22 = _share(standalone_rows, 2022, "Legacy Tokopedia")
    s24 = _share(standalone_rows, 2024, "Shopee")
    t24 = _share(standalone_rows, 2024, "Legacy Tokopedia")
    s25 = _share(post_rows, 2025, "Shopee")
    c25 = _share(post_rows, 2025, "Combined Tokopedia + TikTok Shop")

    filter_keys = (
        panel[["year", "analytical_entity", "metric", "value_status", "comparability", "entity_type", "phase"]]
        .drop_duplicates()
        .rename(columns={"analytical_entity": "marketplace"})
        .sort_values(["year", "marketplace", "metric"])
    )

    return {
        "contract_version": "1.0",
        "gate": "10B",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "deployment_mode": "static_snapshot",
        "rules": [
            "Presentation snapshot from analysis-ready CSVs",
            "OBSERVED / DERIVED / UNKNOWN / SCENARIO preserved",
            "UNKNOWN never converted to zero",
            "2022-2024 standalone separate from 2025 Combined",
            "No continuous merge across structural break",
            "PostgreSQL remains analytical infrastructure; public UI is static",
        ],
        "sources": {
            "competitive_panel": str(PANEL.relative_to(ROOT)),
            "supporting_2025": str(COMPARABLE.relative_to(ROOT)),
            "scenario_outputs": str(SCENARIO_OUT.relative_to(ROOT)),
            "share_gap_summary": str(SHARE_GAP.relative_to(ROOT)),
        },
        "overview": {
            "rules": [
                "Presentation only — values from analysis-ready panel",
                "UNKNOWN never coerced to zero",
                "2022-2024 standalone separate from 2025 Combined",
                "No new business metrics",
            ],
            "phase1_standalone": {
                "shopee_2022": s22,
                "legacy_tokopedia_2022": t22,
                "shopee_2024": s24,
                "legacy_tokopedia_2024": t24,
                "gap_2022_pp": None if s22 is None or t22 is None else s22 - t22,
                "gap_2024_pp": None if s24 is None or t24 is None else s24 - t24,
                "note": "Shopee vs Legacy Tokopedia (OBSERVED)",
            },
            "phase3_post_break": {
                "shopee_2025": s25,
                "combined_2025": c25,
                "gap_2025_pp": None if s25 is None or c25 is None else s25 - c25,
                "legacy_tokopedia_2025": "UNKNOWN",
                "note": "Shopee vs Combined Tokopedia + TikTok Shop — Combined ≠ Legacy",
            },
            "legacy_unknown_rows": unknown_rows,
            "share_gap_summary": _records(share_gap) if len(share_gap) else [],
            "structural_break": True,
        },
        "standalone_shares": standalone_rows,
        "post_break_shares": post_rows,
        "legacy_unknown": unknown_rows,
        "gmv_estimates": _records(gmv),
        "access_metrics": _records(access),
        "tts_labeled_gmv": _records(tts),
        "scenarios": _records(scen),
        "share_gap_summary": _records(share_gap) if len(share_gap) else [],
        "filter_keys": _records(filter_keys),
        "competitive_panel": _records(panel),
    }


def validate_dashboard_data(data: Dict[str, Any]) -> None:
    assert data["overview"]["phase1_standalone"]["shopee_2022"] == 36.0
    assert data["overview"]["phase1_standalone"]["legacy_tokopedia_2022"] == 35.0
    assert data["overview"]["phase1_standalone"]["shopee_2024"] == 46.0
    assert data["overview"]["phase1_standalone"]["legacy_tokopedia_2024"] == 23.0
    assert data["overview"]["phase3_post_break"]["shopee_2025"] == 54.0
    assert data["overview"]["phase3_post_break"]["combined_2025"] == 38.0
    assert data["overview"]["phase3_post_break"]["legacy_tokopedia_2025"] == "UNKNOWN"
    assert len(data["standalone_shares"]) == 6
    assert len(data["post_break_shares"]) == 2
    assert len(data["legacy_unknown"]) == 2
    assert all(r.get("value") is None for r in data["legacy_unknown"])
    assert "Legacy Tokopedia" not in {r["analytical_entity"] for r in data["post_break_shares"]}
    assert all(r.get("value_type") == "SCENARIO" for r in data["scenarios"])
    assert len(data["competitive_panel"]) == 22
    entities = {r["analytical_entity"] for r in data["competitive_panel"]}
    allowed = {
        "Shopee",
        "Legacy Tokopedia",
        "TikTok Shop",
        "Combined Tokopedia + TikTok Shop",
    }
    assert entities <= allowed
    assert not entities & {"Bukalapak", "Lazada", "Blibli"}


def write_dashboard_data(path: Path = FRONTEND_DATA) -> Path:
    data = build_dashboard_data()
    validate_dashboard_data(data)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))
    return path
