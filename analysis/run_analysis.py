"""
Gate 7A — Run analysis/visualization layer.

Reads analysis-ready + supporting processed files.
Writes tables, figures, and summary JSON.
Does not modify Gates 1–6 conclusions or historical data.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Writable matplotlib cache inside repo (sandbox-friendly)
ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".mplconfig"))

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.charts import (
    chart_access_supporting,
    chart_historical_standalone_shares,
    chart_post_break_comparison,
    chart_scenario_gap_bands,
    chart_structural_break_story,
)
from analysis.load import (
    derived_combined_baseline_2024,
    historical_standalone_shares,
    legacy_unknown_2025,
    load_access_supporting,
    load_competitive_panel,
    load_scenario_gap_bands,
    load_tts_labeled_gmv,
    post_break_shopee_vs_combined,
    share_gap_table,
)

OUT = ROOT / "analysis" / "outputs"
TABLES = OUT / "tables"
FIGURES = OUT / "figures"


def main() -> int:
    TABLES.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    panel = load_competitive_panel()
    hist = historical_standalone_shares(panel)
    post = post_break_shopee_vs_combined(panel)
    derived = derived_combined_baseline_2024(panel)
    unknown = legacy_unknown_2025(panel)
    access = load_access_supporting()
    tts = load_tts_labeled_gmv()
    scenarios = load_scenario_gap_bands()

    # Safety asserts
    assert hist["value"].notna().all()
    assert post["value"].notna().all()
    assert unknown["value"].isna().all(), "UNKNOWN must stay null"
    assert len(hist) == 6  # 3 years × 2 entities
    assert len(post) == 2

    gap = share_gap_table(hist, post, derived)
    gap_path = TABLES / "share_gap_summary.csv"
    gap.to_csv(gap_path, index=False)

    hist_path = TABLES / "phase1_standalone_shares.csv"
    hist.to_csv(hist_path, index=False)

    post_path = TABLES / "phase3_post_break_shares.csv"
    post.to_csv(post_path, index=False)

    unknown_path = TABLES / "legacy_tokopedia_2025_unknown.csv"
    unknown.to_csv(unknown_path, index=False)

    access_path = TABLES / "supporting_apjii_access.csv"
    access.to_csv(access_path, index=False)

    tts_path = TABLES / "supporting_tts_labeled_gmv.csv"
    tts.to_csv(tts_path, index=False)

    scen_path = TABLES / "scenario_gap_bands.csv"
    scenarios.to_csv(scen_path, index=False)

    figs = {
        "phase1_standalone_shares": chart_historical_standalone_shares(
            hist, FIGURES / "phase1_standalone_shares.png"
        ),
        "phase3_post_break": chart_post_break_comparison(
            post, derived, FIGURES / "phase3_post_break_shopee_vs_combined.png"
        ),
        "structural_break_story": chart_structural_break_story(
            hist, post, FIGURES / "structural_break_story.png"
        ),
        "supporting_access": chart_access_supporting(
            access, FIGURES / "supporting_apjii_access.png"
        ),
        "scenario_bands": chart_scenario_gap_bands(
            scenarios, FIGURES / "scenario_gap_bands.png"
        ),
    }

    # Key numbers for summary (from OBSERVED only)
    s22 = float(hist[(hist.year == 2022) & (hist.analytical_entity == "Shopee")].value.iloc[0])
    t22 = float(
        hist[(hist.year == 2022) & (hist.analytical_entity == "Legacy Tokopedia")].value.iloc[0]
    )
    s24 = float(hist[(hist.year == 2024) & (hist.analytical_entity == "Shopee")].value.iloc[0])
    t24 = float(
        hist[(hist.year == 2024) & (hist.analytical_entity == "Legacy Tokopedia")].value.iloc[0]
    )
    s25 = float(post[post.analytical_entity == "Shopee"].value.iloc[0])
    c25 = float(
        post[post.analytical_entity == "Combined Tokopedia + TikTok Shop"].value.iloc[0]
    )

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "gate": "7A",
        "canonical_input": str(ROOT / "data/processed/analysis_ready/competitive_panel.csv"),
        "rules": [
            "Plot OBSERVED and DERIVED only",
            "Never convert UNKNOWN/null to zero",
            "2022-2024 standalone separate from 2025 Combined",
            "Gate 1-6 conclusions unchanged",
        ],
        "phase1": {
            "shopee_2022": s22,
            "legacy_tokopedia_2022": t22,
            "gap_2022_pp": s22 - t22,
            "shopee_2024": s24,
            "legacy_tokopedia_2024": t24,
            "gap_2024_pp": s24 - t24,
        },
        "phase3": {
            "shopee_2025": s25,
            "combined_2025": c25,
            "gap_2025_pp": s25 - c25,
            "legacy_tokopedia_2025": "UNKNOWN",
        },
        "supporting": {
            "tts_labeled_gmv_usd": float(tts.iloc[0]["value"]) if len(tts) else None,
            "access_entities": list(access["entity"]) if len(access) else [],
        },
        "outputs": {
            "tables": [str(p.relative_to(ROOT)) for p in TABLES.glob("*.csv")],
            "figures": {k: str(v.relative_to(ROOT)) for k, v in figs.items()},
        },
    }
    (OUT / "analysis_summary.json").write_text(json.dumps(summary, indent=2))

    print("GATE7A_STATUS=PASS")
    print(f"Wrote tables → {TABLES}")
    print(f"Wrote figures → {FIGURES}")
    print(
        f"Phase1 gap 2022→2024: {s22 - t22:.0f} → {s24 - t24:.0f} pp | "
        f"Phase3 Shopee−Combined gap: {s25 - c25:.0f} pp | Legacy 2025=UNKNOWN"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
