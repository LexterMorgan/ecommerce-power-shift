"""Load analysis inputs. Never fills UNKNOWN/null as zero."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
PANEL = PROCESSED / "analysis_ready" / "competitive_panel.csv"
COMPARABLE_2025 = PROCESSED / "2025_comparable" / "platform_metrics_2025_processed.csv"
SCENARIO_OUT = PROCESSED / "gate6_scenario_outputs.csv"
SCENARIO_IN = PROCESSED / "gate6_scenario_inputs.csv"

PLOTTABLE_STATUS = {"OBSERVED", "DERIVED"}


def load_competitive_panel() -> pd.DataFrame:
    df = pd.read_csv(PANEL)
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df


def filter_plottable(df: pd.DataFrame) -> pd.DataFrame:
    """OBSERVED/DERIVED with non-null values only. NEVER coerce UNKNOWN→0."""
    out = df[df["value_status"].isin(PLOTTABLE_STATUS)].copy()
    out = out[out["value"].notna()]
    # Safety: drop any accidental zeros that were UNKNOWN (should not exist)
    bad = df[(df["value_status"] == "UNKNOWN") & (df["value"].notna())]
    if len(bad):
        raise ValueError("UNKNOWN rows must have null values; refuse to plot")
    return out.reset_index(drop=True)


def historical_standalone_shares(panel: pd.DataFrame) -> pd.DataFrame:
    """2022–2024 Shopee vs Legacy Tokopedia market share (OBSERVED only)."""
    plot = filter_plottable(panel)
    out = plot[
        (plot["year"].between(2022, 2024))
        & (plot["metric"] == "market_share_pct")
        & (plot["analytical_entity"].isin(["Shopee", "Legacy Tokopedia"]))
        & (plot["value_status"] == "OBSERVED")
        & (plot["entity_type"] == "standalone")
    ].copy()
    return out.sort_values(["analytical_entity", "year"]).reset_index(drop=True)


def post_break_shopee_vs_combined(panel: pd.DataFrame) -> pd.DataFrame:
    """2025 Shopee vs Combined — NOT Legacy Tokopedia."""
    plot = filter_plottable(panel)
    out = plot[
        (plot["year"] == 2025)
        & (plot["metric"] == "market_share_pct")
        & (
            (
                (plot["analytical_entity"] == "Shopee")
                & (plot["value_status"] == "OBSERVED")
            )
            | (
                (plot["analytical_entity"] == "Combined Tokopedia + TikTok Shop")
                & (plot["value_status"] == "OBSERVED")
                & (plot["entity_type"] == "combined")
            )
        )
    ].copy()
    return out.sort_values("analytical_entity").reset_index(drop=True)


def derived_combined_baseline_2024(panel: pd.DataFrame) -> pd.DataFrame:
    plot = filter_plottable(panel)
    return plot[
        (plot["year"] == 2024)
        & (plot["analytical_entity"] == "Combined Tokopedia + TikTok Shop")
        & (plot["metric"] == "market_share_pct")
        & (plot["value_status"] == "DERIVED")
    ].copy()


def legacy_unknown_2025(panel: pd.DataFrame) -> pd.DataFrame:
    """Return UNKNOWN rows (for documentation; not for plotting values)."""
    return panel[
        (panel["year"] == 2025)
        & (panel["analytical_entity"] == "Legacy Tokopedia")
        & (panel["value_status"] == "UNKNOWN")
    ].copy()


def load_access_supporting() -> pd.DataFrame:
    """APJII access from 2025_comparable — not GMV."""
    df = pd.read_csv(COMPARABLE_2025)
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    out = df[
        (df["metric"] == "internet_user_access_share_pct")
        & (df["evidence_type"] == "OBSERVED")
        & (df["value"].notna())
    ].copy()
    return out.reset_index(drop=True)


def load_tts_labeled_gmv() -> pd.DataFrame:
    df = pd.read_csv(COMPARABLE_2025)
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    out = df[
        (df["entity"] == "TikTok Shop Indonesia")
        & (df["metric"] == "gmv_estimate_usd")
        & (df["evidence_type"] == "OBSERVED")
        & (df["value"].notna())
    ].copy()
    return out.reset_index(drop=True)


def load_scenario_gap_bands() -> pd.DataFrame:
    df = pd.read_csv(SCENARIO_OUT)
    out = df[
        (df["metric"] == "shopee_minus_combined_share_gap_pp")
        & (df["value_type"] == "SCENARIO")
    ].copy()
    for col in ["base_2025_value", "scenario_low", "scenario_high"]:
        out[col] = pd.to_numeric(out[col], errors="coerce")
    return out.reset_index(drop=True)


def share_gap_table(hist: pd.DataFrame, post: pd.DataFrame, derived: pd.DataFrame) -> pd.DataFrame:
    """Build a summary table with provenance columns preserved."""
    rows = []
    for year in [2022, 2023, 2024]:
        s = hist[(hist["year"] == year) & (hist["analytical_entity"] == "Shopee")]
        t = hist[(hist["year"] == year) & (hist["analytical_entity"] == "Legacy Tokopedia")]
        if len(s) != 1 or len(t) != 1:
            continue
        rows.append(
            {
                "panel": "phase1_standalone",
                "year": year,
                "shopee_share_pct": float(s.iloc[0]["value"]),
                "challenger_entity": "Legacy Tokopedia",
                "challenger_share_pct": float(t.iloc[0]["value"]),
                "gap_pp": float(s.iloc[0]["value"]) - float(t.iloc[0]["value"]),
                "value_status": "OBSERVED",
                "comparability": "DIRECT",
                "shopee_source": s.iloc[0].get("citation_url"),
                "challenger_source": t.iloc[0].get("citation_url"),
                "confidence": s.iloc[0].get("confidence"),
                "notes": "Standalone dyad; not Combined",
            }
        )
    if len(post):
        s = post[post["analytical_entity"] == "Shopee"]
        c = post[post["analytical_entity"] == "Combined Tokopedia + TikTok Shop"]
        if len(s) == 1 and len(c) == 1:
            rows.append(
                {
                    "panel": "phase3_post_break",
                    "year": 2025,
                    "shopee_share_pct": float(s.iloc[0]["value"]),
                    "challenger_entity": "Combined Tokopedia + TikTok Shop",
                    "challenger_share_pct": float(c.iloc[0]["value"]),
                    "gap_pp": float(s.iloc[0]["value"]) - float(c.iloc[0]["value"]),
                    "value_status": "OBSERVED",
                    "comparability": "NOT COMPARABLE to Legacy Tokopedia history",
                    "shopee_source": s.iloc[0].get("citation_url"),
                    "challenger_source": c.iloc[0].get("citation_url"),
                    "confidence": s.iloc[0].get("confidence"),
                    "notes": "STRUCTURAL BREAK — Combined ≠ Legacy Tokopedia",
                }
            )
    if len(derived) == 1:
        rows.append(
            {
                "panel": "derived_baseline",
                "year": 2024,
                "shopee_share_pct": pd.NA,
                "challenger_entity": "Combined Tokopedia + TikTok Shop (DERIVED)",
                "challenger_share_pct": float(derived.iloc[0]["value"]),
                "gap_pp": pd.NA,
                "value_status": "DERIVED",
                "comparability": "CONDITIONAL",
                "shopee_source": "",
                "challenger_source": derived.iloc[0].get("citation_url"),
                "confidence": derived.iloc[0].get("confidence"),
                "notes": "Additive 23+11 baseline for vs Combined 2025 only",
            }
        )
    return pd.DataFrame(rows)
