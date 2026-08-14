"""Smoke tests for Gate 7A analysis/visualization outputs."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "data" / "processed" / "analysis_ready" / "competitive_panel.csv"
OUT = ROOT / "analysis" / "outputs"
TABLES = OUT / "tables"
FIGURES = OUT / "figures"


def _ensure_outputs():
    if not (OUT / "analysis_summary.json").exists():
        env = {"MPLCONFIGDIR": str(ROOT / ".mplconfig")}
        subprocess.check_call(
            [sys.executable, str(ROOT / "analysis" / "run_analysis.py")],
            cwd=str(ROOT),
            env={**dict(**{k: v for k, v in __import__("os").environ.items()}), **env},
        )


def test_panel_canonical_exists():
    assert PANEL.exists()
    df = pd.read_csv(PANEL)
    assert "value_status" in df.columns
    unknown = df[
        (df["year"] == 2025)
        & (df["analytical_entity"] == "Legacy Tokopedia")
        & (df["value_status"] == "UNKNOWN")
    ]
    assert len(unknown) == 2
    assert unknown["value"].isna().all()


def test_run_analysis_outputs():
    _ensure_outputs()
    required_tables = [
        "phase1_standalone_shares.csv",
        "phase3_post_break_shares.csv",
        "share_gap_summary.csv",
        "legacy_tokopedia_2025_unknown.csv",
        "supporting_apjii_access.csv",
        "supporting_tts_labeled_gmv.csv",
        "scenario_gap_bands.csv",
    ]
    for name in required_tables:
        assert (TABLES / name).exists(), name

    required_figs = [
        "phase1_standalone_shares.png",
        "phase3_post_break_shopee_vs_combined.png",
        "structural_break_story.png",
        "supporting_apjii_access.png",
        "scenario_gap_bands.png",
    ]
    for name in required_figs:
        path = FIGURES / name
        assert path.exists(), name
        assert path.stat().st_size > 1000


def test_phase1_observed_only_no_combined():
    _ensure_outputs()
    hist = pd.read_csv(TABLES / "phase1_standalone_shares.csv")
    assert set(hist["year"]) == {2022, 2023, 2024}
    assert set(hist["analytical_entity"]) == {"Shopee", "Legacy Tokopedia"}
    assert (hist["value_status"] == "OBSERVED").all()
    assert hist["value"].notna().all()
    assert "Combined" not in " ".join(hist["analytical_entity"].astype(str))


def test_phase3_combined_not_legacy():
    _ensure_outputs()
    post = pd.read_csv(TABLES / "phase3_post_break_shares.csv")
    assert set(post["year"]) == {2025}
    assert set(post["analytical_entity"]) == {
        "Shopee",
        "Combined Tokopedia + TikTok Shop",
    }
    assert (post["value_status"] == "OBSERVED").all()
    assert post["value"].notna().all()
    assert "Legacy Tokopedia" not in set(post["analytical_entity"])


def test_unknown_never_zero():
    _ensure_outputs()
    unk = pd.read_csv(TABLES / "legacy_tokopedia_2025_unknown.csv")
    assert len(unk) == 2
    assert (unk["value_status"] == "UNKNOWN").all()
    assert unk["value"].isna().all()
    # Explicit anti-pattern: no zeros for UNKNOWN
    assert not ((unk["value"].fillna(-1) == 0).any())


def test_share_gap_arithmetic_matches_panel():
    _ensure_outputs()
    gap = pd.read_csv(TABLES / "share_gap_summary.csv")
    p1 = gap[gap["panel"] == "phase1_standalone"]
    r22 = p1[p1["year"] == 2022].iloc[0]
    r24 = p1[p1["year"] == 2024].iloc[0]
    assert abs(r22["gap_pp"] - (36 - 35)) < 1e-9
    assert abs(r24["gap_pp"] - (46 - 23)) < 1e-9
    p3 = gap[gap["panel"] == "phase3_post_break"].iloc[0]
    assert abs(p3["gap_pp"] - (54 - 38)) < 1e-9
    assert "STRUCTURAL BREAK" in str(p3["notes"])


def test_load_filter_plottable_rejects_unknown_fill():
    from analysis.load import filter_plottable, load_competitive_panel

    panel = load_competitive_panel()
    plot = filter_plottable(panel)
    assert (plot["value_status"].isin(["OBSERVED", "DERIVED"])).all()
    assert plot["value"].notna().all()
    assert not (
        (plot["year"] == 2025)
        & (plot["analytical_entity"] == "Legacy Tokopedia")
    ).any()


def test_summary_json_flags():
    _ensure_outputs()
    summary = json.loads((OUT / "analysis_summary.json").read_text())
    assert summary["gate"] == "7A"
    assert summary["phase3"]["legacy_tokopedia_2025"] == "UNKNOWN"
    assert abs(summary["phase1"]["gap_2024_pp"] - 23) < 1e-9
    assert abs(summary["phase3"]["gap_2025_pp"] - 16) < 1e-9


def test_methodology_doc_exists():
    path = ROOT / "research" / "gate7a_analysis_methodology.md"
    assert path.exists()
    text = path.read_text()
    assert "UNKNOWN" in text
    assert "STRUCTURAL" in text.upper() or "structural" in text
    assert "competitive_panel.csv" in text
