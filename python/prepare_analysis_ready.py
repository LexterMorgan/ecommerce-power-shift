"""
Build analysis-ready competitive panel from existing processed datasets.

Does NOT:
- acquire new external data
- fabricate Legacy Tokopedia 2025 GMV/share
- overwrite raw or historical market_position files
- change Gate 6 conclusions

Flow: processed market_position (+ explicit UNKNOWN/structural-break rows)
    → standardize phase labels
    → validate
    → write data/processed/analysis_ready/
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from python.paths import PROCESSED, METADATA

ANALYSIS_READY = PROCESSED / "analysis_ready"

# Research scope: Shopee vs Tokopedia/TikTok Shop only.
# Full industry peers remain in raw/processed market_position for provenance.
ANALYTICAL_ENTITIES = frozenset(
    {
        "Shopee",
        "Legacy Tokopedia",
        "TikTok Shop",
        "Combined Tokopedia + TikTok Shop",
    }
)
CORE_SOURCE_PLATFORMS = frozenset(
    {
        "Shopee",
        "Tokopedia",
        "TikTok Shop",
        "Tokopedia + TikTok Shop",
    }
)


def load_market_position_processed() -> pd.DataFrame:
    path = PROCESSED / "market_position" / "market_position_indonesia.csv"
    if not path.exists():
        raise FileNotFoundError(
            f"Missing {path}. Run: python3 scripts/process_data.py first."
        )
    return pd.read_csv(path)


def build_competitive_panel(mp: pd.DataFrame) -> pd.DataFrame:
    """Long-form analysis panel with phase + value_status labels."""
    rows = []

    for _, r in mp.iterrows():
        year = int(r["year"])
        platform = str(r["platform"])
        entity_type = str(r["entity_type"]).lower()
        share = r.get("market_share_pct")
        gmv = r.get("gmv_estimate_usd_billion")

        # Choke point: exclude industry peers outside research question
        if platform not in CORE_SOURCE_PLATFORMS:
            continue

        # Phase assignment (Gate 6 locked story)
        if year <= 2024 and entity_type == "standalone":
            if platform in {"Shopee", "Tokopedia"}:
                phase = "phase1_historical_standalone"
            elif platform == "TikTok Shop":
                phase = "phase1_historical_tts"
            else:
                phase = "phase1_historical_other"
            analytical_entity = (
                "Legacy Tokopedia" if platform == "Tokopedia" else platform
            )
            comparability = "DIRECT"
        elif year == 2025 and platform == "Shopee" and entity_type == "standalone":
            phase = "phase3_post_break"
            analytical_entity = "Shopee"
            comparability = "DIRECT"
        elif year == 2025 and entity_type == "combined":
            phase = "phase3_post_break"
            analytical_entity = "Combined Tokopedia + TikTok Shop"
            comparability = "NOT COMPARABLE"  # vs Legacy Tokopedia history
        elif year == 2025:
            phase = "phase3_post_break"
            analytical_entity = platform
            comparability = "CONDITIONAL"
        else:
            phase = "context"
            analytical_entity = platform
            comparability = "CONDITIONAL"

        # Share row
        if pd.notna(share):
            rows.append(
                {
                    "year": year,
                    "analytical_entity": analytical_entity,
                    "source_platform": platform,
                    "entity_type": entity_type,
                    "metric": "market_share_pct",
                    "value": float(share),
                    "unit": "percent",
                    "phase": phase,
                    "value_status": "OBSERVED",
                    "comparability": comparability,
                    "source_publisher": r.get("source_publisher"),
                    "citation_url": r.get("citation_url"),
                    "confidence": r.get("confidence"),
                    "notes": "From processed market_position; secondary MW estimates",
                }
            )

        # GMV row (only when present — do not invent)
        if pd.notna(gmv):
            rows.append(
                {
                    "year": year,
                    "analytical_entity": analytical_entity,
                    "source_platform": platform,
                    "entity_type": entity_type,
                    "metric": "gmv_estimate_usd_billion",
                    "value": float(gmv),
                    "unit": "USD_billions",
                    "phase": phase,
                    "value_status": "OBSERVED",
                    "comparability": comparability,
                    "source_publisher": r.get("source_publisher"),
                    "citation_url": r.get("citation_url"),
                    "confidence": r.get("confidence"),
                    "notes": "From processed market_position; blank GMV cells stay missing upstream",
                }
            )

    # Explicit UNKNOWN for Legacy Tokopedia 2025 (do not fill zeros)
    for metric, unit in [
        ("market_share_pct", "percent"),
        ("gmv_estimate_usd_billion", "USD_billions"),
    ]:
        rows.append(
            {
                "year": 2025,
                "analytical_entity": "Legacy Tokopedia",
                "source_platform": "Tokopedia",
                "entity_type": "standalone",
                "metric": metric,
                "value": pd.NA,
                "unit": unit,
                "phase": "phase3_post_break",
                "value_status": "UNKNOWN",
                "comparability": "NOT COMPARABLE",
                "source_publisher": "Gate 5.5 final search",
                "citation_url": "research/final_2025_data_search.md",
                "confidence": "HIGH",
                "notes": "KEEP MISSING — not fabricated; Combined 38% is a different entity",
            }
        )

    # DERIVED 2024 additive Combined baseline (documented)
    tok_2024 = mp[(mp["year"] == 2024) & (mp["platform"] == "Tokopedia")]["market_share_pct"]
    tts_2024 = mp[(mp["year"] == 2024) & (mp["platform"] == "TikTok Shop")]["market_share_pct"]
    if len(tok_2024) == 1 and len(tts_2024) == 1 and pd.notna(tok_2024.iloc[0]) and pd.notna(tts_2024.iloc[0]):
        additive = float(tok_2024.iloc[0]) + float(tts_2024.iloc[0])
        rows.append(
            {
                "year": 2024,
                "analytical_entity": "Combined Tokopedia + TikTok Shop",
                "source_platform": "Tokopedia + TikTok Shop",
                "entity_type": "combined_derived",
                "metric": "market_share_pct",
                "value": additive,
                "unit": "percent",
                "phase": "phase1_historical_standalone",
                "value_status": "DERIVED",
                "comparability": "CONDITIONAL",
                "source_publisher": "Derived 23+11 from MW 2024 split",
                "citation_url": "data/processed/market_position/market_position_indonesia.csv",
                "confidence": "MEDIUM",
                "notes": "Additive baseline only if MW 2024 entities non-overlapping; used vs 2025 Combined",
            }
        )

    out = pd.DataFrame(rows)
    out["year"] = pd.to_numeric(out["year"], errors="coerce").astype("Int64")
    out["value"] = pd.to_numeric(out["value"], errors="coerce")
    out = out.sort_values(
        ["phase", "year", "analytical_entity", "metric"], na_position="last"
    ).reset_index(drop=True)
    return out


def validate_competitive_panel(df: pd.DataFrame) -> dict:
    """Lightweight validation; raises AssertionError on hard failures."""
    required = {
        "year",
        "analytical_entity",
        "metric",
        "value",
        "phase",
        "value_status",
        "comparability",
    }
    missing_cols = required - set(df.columns)
    assert not missing_cols, f"Missing columns: {missing_cols}"

    assert df["value_status"].isin(["OBSERVED", "DERIVED", "SCENARIO", "UNKNOWN"]).all()
    assert df["comparability"].isin(["DIRECT", "CONDITIONAL", "NOT COMPARABLE"]).all()

    # Shares in bounds when present
    shares = df[(df["metric"] == "market_share_pct") & df["value"].notna()]["value"]
    assert ((shares >= 0) & (shares <= 100)).all(), "Share out of bounds"

    # UNKNOWN must not be zero-filled
    unknown = df[df["value_status"] == "UNKNOWN"]
    assert unknown["value"].isna().all(), "UNKNOWN values must remain null (not 0)"

    # Structural break: Combined 2025 present; Legacy 2025 share UNKNOWN
    comb = df[
        (df["year"] == 2025)
        & (df["analytical_entity"] == "Combined Tokopedia + TikTok Shop")
        & (df["metric"] == "market_share_pct")
        & (df["value_status"] == "OBSERVED")
    ]
    assert len(comb) == 1 and float(comb.iloc[0]["value"]) == 38.0

    legacy = df[
        (df["year"] == 2025)
        & (df["analytical_entity"] == "Legacy Tokopedia")
        & (df["metric"] == "market_share_pct")
    ]
    assert len(legacy) >= 1
    assert legacy["value"].isna().all()
    assert legacy["value_status"].eq("UNKNOWN").all()

    # Historical 2022–2024 Shopee/Tokopedia shares present
    for year, shopee, tok in [(2022, 36.0, 35.0), (2023, 40.0, 30.0), (2024, 46.0, 23.0)]:
        s = df[
            (df["year"] == year)
            & (df["analytical_entity"] == "Shopee")
            & (df["metric"] == "market_share_pct")
            & (df["value_status"] == "OBSERVED")
        ]
        t = df[
            (df["year"] == year)
            & (df["analytical_entity"] == "Legacy Tokopedia")
            & (df["metric"] == "market_share_pct")
            & (df["value_status"] == "OBSERVED")
        ]
        assert float(s.iloc[0]["value"]) == shopee
        assert float(t.iloc[0]["value"]) == tok

    shopee_2025 = df[
        (df["year"] == 2025)
        & (df["analytical_entity"] == "Shopee")
        & (df["metric"] == "market_share_pct")
        & (df["value_status"] == "OBSERVED")
    ]
    assert float(shopee_2025.iloc[0]["value"]) == 54.0

    # Analytical-scope invariant
    entities = set(df["analytical_entity"].astype(str))
    extra = entities - ANALYTICAL_ENTITIES
    assert not extra, f"Non-analytical entities in competitive panel: {sorted(extra)}"
    assert entities <= ANALYTICAL_ENTITIES

    return {
        "rows": len(df),
        "observed": int((df["value_status"] == "OBSERVED").sum()),
        "derived": int((df["value_status"] == "DERIVED").sum()),
        "unknown": int((df["value_status"] == "UNKNOWN").sum()),
        "analytical_entities": sorted(entities),
        "status": "PASS",
    }


def main() -> int:
    ANALYSIS_READY.mkdir(parents=True, exist_ok=True)
    mp = load_market_position_processed()
    panel = build_competitive_panel(mp)
    report = validate_competitive_panel(panel)

    out_csv = ANALYSIS_READY / "competitive_panel.csv"
    panel.to_csv(out_csv, index=False)

    meta = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "upstream": str(PROCESSED / "market_position" / "market_position_indonesia.csv"),
        "output": str(out_csv),
        "validation": report,
        "rules": [
            "No fabricated Legacy Tokopedia 2025 GMV/share",
            "Combined 2025 != Legacy Tokopedia",
            "UNKNOWN values remain null",
            "Does not overwrite raw or historical market_position",
            "Analytical allowlist only: Shopee, Legacy Tokopedia, TikTok Shop, Combined",
        ],
    }
    (ANALYSIS_READY / "competitive_panel_validation.json").write_text(
        json.dumps(meta, indent=2)
    )
    (METADATA / "analysis_ready_validation.json").write_text(json.dumps(meta, indent=2))

    print("ANALYSIS_READY_STATUS=PASS")
    print(f"Wrote {out_csv} ({report['rows']} rows)")
    print(
        f"OBSERVED={report['observed']} DERIVED={report['derived']} UNKNOWN={report['unknown']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
