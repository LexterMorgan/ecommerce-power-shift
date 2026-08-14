"""Cleaning transforms for each dataset. Does not invent missing values."""
from __future__ import annotations

import pandas as pd

from python.paths import PLATFORM_CANONICAL


def canonicalize_platform(value: object) -> object:
    if pd.isna(value):
        return value
    key = str(value).strip().lower()
    return PLATFORM_CANONICAL.get(key, str(value).strip())


def clean_market_position(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["platform"] = out["platform"].map(canonicalize_platform)
    out["country"] = "Indonesia"
    out["year"] = pd.to_numeric(out["year"], errors="coerce").astype("Int64")
    for col in ["gmv_estimate_usd_billion", "market_share_pct", "market_total_gmv_usd_billion", "rank"]:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")
    out["entity_type"] = out["entity_type"].astype(str).str.strip().str.lower()
    out["confidence"] = out["confidence"].astype(str).str.strip().str.upper()
    # Keep missing as NA — do not fill
    out = out.sort_values(["year", "rank", "platform"], na_position="last").reset_index(drop=True)
    return out


def clean_events(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["event_date"] = pd.to_datetime(out["event_date"], errors="coerce")
    out["event_end_date"] = pd.to_datetime(out["event_end_date"], errors="coerce")
    out["event_type"] = out["event_type"].astype(str).str.strip().str.lower()
    out["confidence"] = out["confidence"].astype(str).str.strip().str.upper()
    out["platform"] = out["platform"].astype(str).str.strip()
    out = out.sort_values("event_date").reset_index(drop=True)
    return out


def clean_company_metrics(df: pd.DataFrame, company_label: str) -> pd.DataFrame:
    out = df.copy()
    out["company"] = company_label
    out["value"] = pd.to_numeric(out["value"], errors="coerce")
    out["metric"] = out["metric"].astype(str).str.strip()
    out["unit"] = out["unit"].astype(str).str.strip()
    out["geography"] = out["geography"].astype(str).str.strip()
    return out.reset_index(drop=True)


def clean_macro(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["year"] = pd.to_numeric(out["year"], errors="coerce").astype("Int64")
    out["value"] = pd.to_numeric(out["value"], errors="coerce")
    out["country"] = "Indonesia"
    out = out.dropna(subset=["year"]).sort_values(["indicator_code", "year"]).reset_index(drop=True)
    # Drop rows where World Bank returned null values (explicit missing years)
    # Keep them actually — user said missing must remain missing. Keep null value rows.
    return out


def clean_structural_break(df: pd.DataFrame) -> pd.DataFrame:
    """Clean 2024→2025 entity-split evidence. Keeps UNKNOWN/missing values."""
    out = df.copy()
    out["year"] = pd.to_numeric(out["year"], errors="coerce").astype("Int64")
    out["value"] = pd.to_numeric(out["value"], errors="coerce")
    out["entity"] = out["entity"].astype(str).str.strip()
    out["metric"] = out["metric"].astype(str).str.strip()
    out["data_type"] = out["data_type"].astype(str).str.strip().str.upper()
    out["confidence"] = out["confidence"].astype(str).str.strip().str.upper()
    out["unit"] = out["unit"].astype(str).str.strip()
    # Do not drop UNKNOWN rows with null value — missing is intentional
    out = out.sort_values(["year", "entity", "metric", "data_type"], na_position="last").reset_index(drop=True)
    return out


def clean_entity_split(df: pd.DataFrame) -> pd.DataFrame:
    """Clean Gate 3B entity-split acquisition table. Preserves missing values."""
    out = df.copy()
    out["year"] = pd.to_numeric(out["year"], errors="coerce").astype("Int64")
    for col in ["value", "market_share", "gmv_usd"]:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")
    for col in ["entity", "metric", "unit", "geography", "methodology", "source", "source_type", "comparability", "confidence", "evidence_note"]:
        if col in out.columns:
            out[col] = out[col].astype(str).str.strip()
            out.loc[out[col].isin(["nan", "None", ""]), col] = pd.NA
    out["source_type"] = out["source_type"].astype(str).str.strip().str.upper()
    out["comparability"] = out["comparability"].astype(str).str.strip().str.upper()
    out["confidence"] = out["confidence"].astype(str).str.strip().str.upper()
    out = out.sort_values(["year", "entity", "metric", "source_type"], na_position="last").reset_index(drop=True)
    return out


def clean_google_trends(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    # Normalize column names
    rename = {}
    for c in out.columns:
        cl = str(c).strip().lower()
        if cl in {"week", "day", "month", "date", "time"}:
            rename[c] = "date"
        elif "shopee" in cl:
            rename[c] = "Shopee"
        elif "tokopedia" in cl:
            rename[c] = "Tokopedia"
    out = out.rename(columns=rename)
    if "date" not in out.columns:
        raise ValueError("Google Trends file missing a date/week column")
    for col in ["Shopee", "Tokopedia"]:
        if col not in out.columns:
            raise ValueError(f"Google Trends file missing column: {col}")
    out["date"] = pd.to_datetime(out["date"], errors="coerce")
    out["Shopee"] = pd.to_numeric(out["Shopee"], errors="coerce")
    out["Tokopedia"] = pd.to_numeric(out["Tokopedia"], errors="coerce")
    out = out.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)
    # Long format for analysis readiness
    long = out.melt(id_vars=["date"], value_vars=["Shopee", "Tokopedia"], var_name="term", value_name="interest")
    long["geo"] = "ID"
    long["source"] = "Google Trends"
    long["category"] = "All categories"
    long["search_type"] = "Web Search"
    long["interest"] = pd.to_numeric(long["interest"], errors="coerce")
    return long
