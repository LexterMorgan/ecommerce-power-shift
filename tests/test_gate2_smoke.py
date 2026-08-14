"""Smoke tests for Gate 2/3/3B processed outputs."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
RAW = ROOT / "data" / "raw"


def test_market_position_exists_and_valid():
    path = PROC / "market_position" / "market_position_indonesia.csv"
    assert path.exists()
    df = pd.read_csv(path)
    assert len(df) >= 1
    assert {"year", "platform", "market_share_pct"}.issubset(df.columns)
    assert df["market_share_pct"].between(0, 100).all()
    assert not df.duplicated(subset=["year", "platform", "entity_type"]).any()


def test_events_exist():
    path = PROC / "events" / "competitive_events.csv"
    assert path.exists()
    df = pd.read_csv(path)
    assert len(df) >= 1
    assert df["event_id"].is_unique


def test_structural_break_exists():
    path = PROC / "structural_break" / "transition_2024_2025_evidence.csv"
    assert path.exists()
    df = pd.read_csv(path)
    assert len(df) >= 1
    assert {"year", "entity", "metric", "data_type", "confidence"}.issubset(df.columns)
    combined_2025 = df[
        (df["year"] == 2025)
        & (df["entity"].str.contains("Combined", na=False))
        & (df["metric"] == "market_share_pct")
    ]
    assert len(combined_2025) >= 1
    unknown_legacy = df[
        (df["year"] == 2025)
        & (df["entity"] == "Legacy Tokopedia")
        & (df["metric"] == "market_share_pct")
        & (df["data_type"] == "UNKNOWN")
    ]
    assert len(unknown_legacy) == 1
    assert unknown_legacy["value"].isna().all()


def test_entity_split_gate3b():
    raw_path = RAW / "structural_break" / "entity_split_2024_2025.csv"
    proc_path = PROC / "structural_break" / "entity_split_2024_2025_processed.csv"
    assert raw_path.exists()
    assert proc_path.exists()
    df = pd.read_csv(proc_path)

    required_cols = {
        "year",
        "entity",
        "metric",
        "value",
        "source",
        "source_type",
        "comparability",
        "confidence",
    }
    assert required_cols.issubset(df.columns)

    # Valid years
    assert df["year"].between(2020, 2026).all()

    # Comparability assigned
    assert df["comparability"].isin(["DIRECT", "CONDITIONAL", "NOT COMPARABLE"]).all()

    # Derived labeled
    derived = df[df["source_type"] == "DERIVED"]
    assert len(derived) >= 1
    assert derived["value"].notna().all()

    # Non-missing important values have source
    valued = df[df["value"].notna() & (df["source_type"] != "UNKNOWN")]
    assert valued["source"].notna().all()
    assert (valued["source"].astype(str).str.len() > 0).all()

    # Legacy Tokopedia 2025 GMV/share remain missing (no fabricated fill)
    legacy_2025 = df[(df["year"] == 2025) & (df["entity"] == "Legacy Tokopedia")]
    legacy_gmv_share = legacy_2025[legacy_2025["metric"].isin(["market_share_pct", "gmv_estimate_usd"])]
    assert legacy_gmv_share["source_type"].eq("UNKNOWN").all()
    assert legacy_gmv_share["value"].isna().all()

    # Combined 2025 share must be NOT COMPARABLE to Legacy series
    combined_share = df[
        (df["year"] == 2025)
        & (df["entity"] == "Combined Tokopedia + TikTok Shop")
        & (df["metric"] == "market_share_pct")
    ]
    assert len(combined_share) == 1
    assert combined_share.iloc[0]["comparability"] == "NOT COMPARABLE"
    assert combined_share.iloc[0]["value"] == 38.0

    # APJII access metric present and not confused with GMV share naming
    apjii = df[df["metric"] == "internet_user_access_share_pct"]
    assert len(apjii) >= 3


def test_gate4_entity_analysis():
    path = PROC / "gate4_entity_analysis.csv"
    assert path.exists()
    df = pd.read_csv(path)
    assert len(df) >= 1
    assert {"entity", "metric", "evidence_type", "interpretation"}.issubset(df.columns)
    # No fabricated Legacy Tokopedia 2025 GMV/share fills
    legacy_share = df[(df["entity"] == "Legacy Tokopedia") & (df["metric"] == "market_share_pct")]
    assert len(legacy_share) == 1
    assert pd.isna(legacy_share.iloc[0]["year_2025_value"])
    legacy_gmv = df[(df["entity"] == "Legacy Tokopedia") & (df["metric"] == "gmv_estimate_usd")]
    assert len(legacy_gmv) == 1
    assert pd.isna(legacy_gmv.iloc[0]["year_2025_value"])
    # Combined 2025 share present and distinct
    combined = df[
        (df["entity"] == "Combined Tokopedia + TikTok Shop") & (df["metric"] == "market_share_pct")
    ]
    assert float(combined.iloc[0]["year_2025_value"]) == 38.0


def test_gate5_competitive_analysis():
    path = PROC / "gate5_competitive_analysis.csv"
    assert path.exists()
    df = pd.read_csv(path)
    required = {
        "claim_id",
        "entity",
        "metric",
        "grain",
        "year",
        "evidence_type",
        "comparability",
        "source",
        "conclusion_tag",
    }
    assert required.issubset(df.columns)
    assert df["claim_id"].is_unique
    assert df["evidence_type"].isin(
        ["OBSERVED", "DERIVED", "INFERRED", "UNKNOWN", "MIXED"]
    ).all()
    # No fabricated Legacy Tokopedia 2025 GMV/share
    legacy_2025 = df[
        (df["entity"] == "Legacy Tokopedia")
        & (df["year"] == 2025)
        & (df["metric"].isin(["market_share_pct", "gmv_estimate_usd"]))
    ]
    assert len(legacy_2025) >= 1
    assert legacy_2025["evidence_type"].eq("UNKNOWN").all()
    assert legacy_2025["value"].isna().all()
    # Combined 38 must not be labeled as Legacy Tokopedia
    combined = df[
        (df["entity"] == "Combined Tokopedia + TikTok Shop")
        & (df["metric"] == "market_share_pct")
        & (df["year"] == 2025)
    ]
    assert float(combined.iloc[0]["value"]) == 38.0
    assert combined.iloc[0]["comparability"] == "NOT COMPARABLE"
    # Hypothesis status rows present
    assert (df["conclusion_tag"] == "H1_UNSUPPORTED").any()
    assert (df["conclusion_tag"] == "H3_STRONGEST_PARTIAL").any()


def test_gate55_2025_comparable():
    raw = RAW / "2025_comparable" / "platform_metrics_2025.csv"
    proc = PROC / "2025_comparable" / "platform_metrics_2025_processed.csv"
    assert raw.exists() and proc.exists()
    df = pd.read_csv(proc)
    required = {
        "year",
        "entity",
        "metric",
        "value",
        "source",
        "source_url",
        "source_type",
        "comparability",
        "evidence_type",
    }
    assert required.issubset(df.columns)
    assert (df["year"] == 2025).all() or (df["year"] >= 2025).any()
    assert df["comparability"].isin(["DIRECT", "CONDITIONAL", "NOT COMPARABLE"]).all()
    # Legacy Tokopedia GMV/share remain missing
    legacy = df[
        (df["entity"] == "Legacy Tokopedia")
        & (df["metric"].isin(["market_share_pct", "gmv_estimate_usd"]))
    ]
    assert len(legacy) == 2
    assert legacy["value"].isna().all()
    assert legacy["evidence_type"].eq("UNKNOWN").all()
    # Combined not mislabeled as Legacy
    combined = df[
        (df["entity"] == "Combined Tokopedia + TikTok Shop")
        & (df["metric"] == "market_share_pct")
    ]
    assert float(combined.iloc[0]["value"]) == 38.0
    assert combined.iloc[0]["comparability"] == "NOT COMPARABLE"
    # Shopee DIRECT comparable present
    shopee = df[(df["entity"] == "Shopee Indonesia") & (df["metric"] == "market_share_pct")]
    assert float(shopee.iloc[0]["value"]) == 54.0
    assert shopee.iloc[0]["comparability"] == "DIRECT"


def test_gate6_scenarios():
    inputs = PROC / "gate6_scenario_inputs.csv"
    outputs = PROC / "gate6_scenario_outputs.csv"
    assert inputs.exists() and outputs.exists()
    dfi = pd.read_csv(inputs)
    dfo = pd.read_csv(outputs)
    assert {"input_id", "entity", "metric", "value_type", "comparability"}.issubset(dfi.columns)
    assert {"scenario_id", "value_type", "direction"}.issubset(dfo.columns)
    # Historical 2024 Legacy present; 2025 Legacy share missing
    leg24 = dfi[(dfi["entity"] == "Legacy Tokopedia") & (dfi["year"] == 2024) & (dfi["metric"] == "market_share_pct")]
    assert float(leg24.iloc[0]["value"]) == 23.0
    leg25 = dfi[(dfi["entity"] == "Legacy Tokopedia") & (dfi["year"] == 2025) & (dfi["metric"] == "market_share_pct")]
    assert leg25["value"].isna().all()
    assert leg25["value_type"].eq("UNKNOWN").all()
    # Combined 2025 correctly labeled
    comb = dfi[
        (dfi["entity"] == "Combined Tokopedia + TikTok Shop")
        & (dfi["year"] == 2025)
        & (dfi["metric"] == "market_share_pct")
    ]
    assert float(comb.iloc[0]["value"]) == 38.0
    assert comb.iloc[0]["comparability"] == "NOT COMPARABLE"
    # Scenario outputs are SCENARIO or UNKNOWN — never OBSERVED future shares
    assert dfo["value_type"].isin(["SCENARIO", "UNKNOWN"]).all()
    assert (dfo["scenario_id"] == "ALL").any()  # shared Legacy missing constraint


def test_analysis_ready_panel():
    path = PROC / "analysis_ready" / "competitive_panel.csv"
    assert path.exists(), "Run python3 scripts/prepare_analysis_ready.py"
    df = pd.read_csv(path)
    required = {
        "year",
        "analytical_entity",
        "metric",
        "value",
        "phase",
        "value_status",
        "comparability",
    }
    assert required.issubset(df.columns)
    assert df["value_status"].isin(["OBSERVED", "DERIVED", "SCENARIO", "UNKNOWN"]).all()
    # UNKNOWN not zero-filled
    unknown = df[df["value_status"] == "UNKNOWN"]
    assert len(unknown) >= 2
    assert unknown["value"].isna().all()
    # Historical unchanged
    s22 = df[
        (df["year"] == 2022)
        & (df["analytical_entity"] == "Shopee")
        & (df["metric"] == "market_share_pct")
        & (df["value_status"] == "OBSERVED")
    ]
    assert float(s22.iloc[0]["value"]) == 36.0
    # Structural break labels
    comb = df[
        (df["year"] == 2025)
        & (df["analytical_entity"] == "Combined Tokopedia + TikTok Shop")
        & (df["metric"] == "market_share_pct")
        & (df["value_status"] == "OBSERVED")
    ]
    assert float(comb.iloc[0]["value"]) == 38.0
    assert comb.iloc[0]["comparability"] == "NOT COMPARABLE"
    legacy = df[
        (df["year"] == 2025)
        & (df["analytical_entity"] == "Legacy Tokopedia")
        & (df["metric"] == "market_share_pct")
    ]
    assert legacy["value"].isna().all()
    assert legacy["value_status"].eq("UNKNOWN").all()
    # DERIVED distinguishable
    assert (df["value_status"] == "DERIVED").any()


def test_macro_exists():
    path = PROC / "macro" / "indonesia_macro_indicators.csv"
    assert path.exists()
    df = pd.read_csv(path)
    assert len(df) >= 1
