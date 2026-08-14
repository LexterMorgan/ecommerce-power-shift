"""Load raw datasets from local raw/ directories."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import pandas as pd

from python.paths import RAW


def _read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def load_market_position() -> pd.DataFrame:
    path = RAW / "market_position" / "market_position_indonesia_mw_public_excerpts.csv"
    df = _read_csv(path)
    df.attrs["raw_path"] = str(path)
    df.attrs["dataset"] = "market_position"
    return df


def load_events() -> pd.DataFrame:
    path = RAW / "events" / "competitive_events.csv"
    df = _read_csv(path)
    df.attrs["raw_path"] = str(path)
    df.attrs["dataset"] = "events"
    return df


def load_sea() -> pd.DataFrame:
    path = RAW / "sea" / "sea_shopee_official_metrics_curated.csv"
    df = _read_csv(path)
    df.attrs["raw_path"] = str(path)
    df.attrs["dataset"] = "sea"
    return df


def load_goto() -> pd.DataFrame:
    path = RAW / "goto" / "goto_ecommerce_context_curated.csv"
    df = _read_csv(path)
    df.attrs["raw_path"] = str(path)
    df.attrs["dataset"] = "goto"
    return df


def load_macro() -> pd.DataFrame:
    path = RAW / "macro" / "worldbank_indonesia_indicators_extract.csv"
    df = _read_csv(path)
    df.attrs["raw_path"] = str(path)
    df.attrs["dataset"] = "macro"
    return df


def load_structural_break() -> pd.DataFrame:
    path = RAW / "structural_break" / "transition_2024_2025_evidence.csv"
    df = _read_csv(path)
    df.attrs["raw_path"] = str(path)
    df.attrs["dataset"] = "structural_break"
    return df


def load_entity_split() -> pd.DataFrame:
    path = RAW / "structural_break" / "entity_split_2024_2025.csv"
    df = _read_csv(path)
    df.attrs["raw_path"] = str(path)
    df.attrs["dataset"] = "entity_split"
    return df


def find_google_trends_csv() -> Optional[Path]:
    folder = RAW / "google_trends"
    preferred = [
        folder / "google_trends_indonesia_shopee_tokopedia_manual.csv",
        folder / "google_trends_indonesia_shopee_tokopedia_today5y.csv",
        folder / "google_trends_indonesia_shopee_tokopedia_2019_2026.csv",
    ]
    for p in preferred:
        if p.exists():
            return p
    candidates = sorted(folder.glob("*.csv"))
    return candidates[0] if candidates else None


def load_google_trends() -> Optional[pd.DataFrame]:
    path = find_google_trends_csv()
    if path is None:
        return None
    df = pd.read_csv(path)
    cols_lower = [str(c).lower() for c in df.columns]
    if not any("shopee" in c for c in cols_lower):
        df = pd.read_csv(path, skiprows=2)
    df.attrs["raw_path"] = str(path)
    df.attrs["dataset"] = "google_trends"
    return df


def load_trends_blocker() -> Optional[dict]:
    path = RAW / "google_trends" / "google_trends_access_blocker.json"
    if not path.exists():
        return None
    return json.loads(path.read_text())
