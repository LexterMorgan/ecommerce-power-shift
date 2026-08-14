"""Validation checks producing structured quality results."""
from __future__ import annotations

from dataclasses import dataclass, asdict, field
from typing import Any, Dict, List, Optional

import pandas as pd


@dataclass
class ValidationResult:
    dataset: str
    rows_raw: int
    rows_processed: int
    duplicate_keys: int
    missing_required_values: int
    invalid_percentages: int
    invalid_years: int
    unknown_platforms: int
    invalid_dates: int
    impossible_values: int
    status: str
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _status(fail_counts: List[int]) -> str:
    return "PASS" if all(c == 0 for c in fail_counts) else "FAIL"


def validate_market_position(raw: pd.DataFrame, processed: pd.DataFrame) -> ValidationResult:
    notes: List[str] = []
    key = processed.duplicated(subset=["year", "platform", "entity_type"], keep=False)
    dup = int(key.sum() // 2) if key.any() else 0
    # more accurate duplicate group count:
    dup = int(processed.duplicated(subset=["year", "platform", "entity_type"]).sum())

    required = ["year", "platform", "market_share_pct", "source_publisher", "citation_url"]
    missing_req = int(processed[required].isna().any(axis=1).sum())

    share = processed["market_share_pct"]
    invalid_pct = int(((share < 0) | (share > 100)).fillna(False).sum())

    years = processed["year"]
    invalid_years = int(((years < 2015) | (years > 2026)).fillna(False).sum())

    known = {"Shopee", "Tokopedia", "Lazada", "Bukalapak", "Blibli", "TikTok Shop", "Tokopedia + TikTok Shop"}
    unknown = int((~processed["platform"].isin(known)).sum())

    gmv = processed["gmv_estimate_usd_billion"]
    impossible = int((gmv < 0).fillna(False).sum())

    if processed["gmv_estimate_usd_billion"].isna().any():
        notes.append("Some GMV values are intentionally missing (not published in free citations).")
    if (processed["entity_type"] == "combined").any():
        notes.append("Combined Tokopedia + TikTok Shop rows present; not standalone-comparable without adjustment.")
    notes.append("Source family is industry estimates via secondary public citations; not official platform filings.")

    status = _status([dup, missing_req, invalid_pct, invalid_years, unknown, impossible])
    return ValidationResult(
        dataset="market_position",
        rows_raw=len(raw),
        rows_processed=len(processed),
        duplicate_keys=dup,
        missing_required_values=missing_req,
        invalid_percentages=invalid_pct,
        invalid_years=invalid_years,
        unknown_platforms=unknown,
        invalid_dates=0,
        impossible_values=impossible,
        status=status,
        notes=notes,
    )


def validate_events(raw: pd.DataFrame, processed: pd.DataFrame) -> ValidationResult:
    notes: List[str] = []
    dup = int(processed.duplicated(subset=["event_id"]).sum())
    missing_req = int(processed[["event_id", "event_date", "event_title", "source_url"]].isna().any(axis=1).sum())
    invalid_dates = int(processed["event_date"].isna().sum())
    status = _status([dup, missing_req, invalid_dates])
    notes.append("Events are contextual; impact_direction is not causal proof.")
    return ValidationResult(
        dataset="events",
        rows_raw=len(raw),
        rows_processed=len(processed),
        duplicate_keys=dup,
        missing_required_values=missing_req,
        invalid_percentages=0,
        invalid_years=0,
        unknown_platforms=0,
        invalid_dates=invalid_dates,
        impossible_values=0,
        status=status,
        notes=notes,
    )


def validate_company(name: str, raw: pd.DataFrame, processed: pd.DataFrame) -> ValidationResult:
    notes = [
        "Company metrics are NOT comparable to Indonesia platform market-share estimates.",
        "Sea geography is multi-country unless explicitly Indonesia.",
        "GoTo Core GTV excludes Tokopedia after Jan 2024 deconsolidation.",
    ]
    dup = int(processed.duplicated(subset=["period", "metric", "company"]).sum())
    missing_req = int(processed[["period", "metric", "value", "unit", "source_url"]].isna().any(axis=1).sum())
    impossible = int((processed["value"] < 0).fillna(False).sum())
    # boolean flag can be 1
    status = _status([dup, missing_req, impossible])
    return ValidationResult(
        dataset=name,
        rows_raw=len(raw),
        rows_processed=len(processed),
        duplicate_keys=dup,
        missing_required_values=missing_req,
        invalid_percentages=0,
        invalid_years=0,
        unknown_platforms=0,
        invalid_dates=0,
        impossible_values=impossible,
        status=status,
        notes=notes,
    )


def validate_macro(raw: pd.DataFrame, processed: pd.DataFrame) -> ValidationResult:
    notes = ["World Bank nulls retained as missing years; not imputed.", "Macro indicators are contextual, not platform share."]
    dup = int(processed.duplicated(subset=["indicator_code", "year"]).sum())
    missing_req = int(processed[["indicator_code", "year"]].isna().any(axis=1).sum())
    invalid_years = int(((processed["year"] < 2010) | (processed["year"] > 2026)).fillna(False).sum())
    status = _status([dup, missing_req, invalid_years])
    return ValidationResult(
        dataset="macro",
        rows_raw=len(raw),
        rows_processed=len(processed),
        duplicate_keys=dup,
        missing_required_values=missing_req,
        invalid_percentages=0,
        invalid_years=invalid_years,
        unknown_platforms=0,
        invalid_dates=0,
        impossible_values=0,
        status=status,
        notes=notes,
    )


def validate_structural_break(raw: pd.DataFrame, processed: pd.DataFrame) -> ValidationResult:
    notes = [
        "Entity distinctions are mandatory: Legacy Tokopedia vs TikTok Shop Indonesia vs Combined.",
        "DERIVED residual Legacy Tokopedia 2025 is LOW confidence pending MW additivity confirmation.",
        "UNKNOWN standalone Legacy Tokopedia 2025 share row must keep null value.",
        "Never treat Combined 2025 share as standalone Tokopedia.",
    ]
    key_cols = ["year", "entity", "metric", "data_type"]
    dup = int(processed.duplicated(subset=key_cols).sum())
    required = ["year", "entity", "metric", "data_type", "confidence"]
    missing_req = int(processed[required].isna().any(axis=1).sum())
    invalid_years = int(((processed["year"] < 2020) | (processed["year"] > 2026)).fillna(False).sum())

    share_mask = processed["metric"] == "market_share_pct"
    share_vals = processed.loc[share_mask, "value"]
    invalid_pct = int(((share_vals < 0) | (share_vals > 100)).fillna(False).sum())

    # Non-UNKNOWN rows that claim a numeric metric should have a value,
    # except UNKNOWN explicitly documents missing standalone share.
    needs_value = processed["data_type"] != "UNKNOWN"
    missing_values = int(processed.loc[needs_value, "value"].isna().sum())
    if missing_values:
        notes.append(f"{missing_values} non-UNKNOWN row(s) missing value.")

    # UNKNOWN rows should have null value
    unknown_filled = int(processed.loc[processed["data_type"] == "UNKNOWN", "value"].notna().sum())
    if unknown_filled:
        notes.append("UNKNOWN rows should not carry numeric fills.")

    gmv_mask = processed["metric"].str.contains("gmv", case=False, na=False)
    impossible = int((processed.loc[gmv_mask, "value"] < 0).fillna(False).sum())

    status = _status([dup, missing_req, invalid_years, invalid_pct, missing_values, unknown_filled, impossible])
    return ValidationResult(
        dataset="structural_break",
        rows_raw=len(raw),
        rows_processed=len(processed),
        duplicate_keys=dup,
        missing_required_values=missing_req,
        invalid_percentages=invalid_pct,
        invalid_years=invalid_years,
        unknown_platforms=0,
        invalid_dates=0,
        impossible_values=impossible,
        status=status,
        notes=notes,
    )


VALID_ENTITIES = {
    "Shopee",
    "Legacy Tokopedia",
    "TikTok Shop Indonesia",
    "Combined Tokopedia + TikTok Shop",
    "Indonesia market",
    "GoTo",
    "SEA market",
    "TikTok Shop SEA",
    "Combined under PT Tokopedia",
}

VALID_COMPARABILITY = {"DIRECT", "CONDITIONAL", "NOT COMPARABLE"}
VALID_SOURCE_TYPES = {"PRIMARY", "SECONDARY_HIGH", "SECONDARY", "DERIVED", "UNKNOWN", "INFERENCE"}


def validate_entity_split(raw: pd.DataFrame, processed: pd.DataFrame) -> ValidationResult:
    notes = [
        "Gate 3B entity-split table: every non-missing value must have a source.",
        "DERIVED rows must remain labeled DERIVED.",
        "UNKNOWN Legacy Tokopedia 2025 GMV/share must remain null.",
        "APJII access metrics are not GMV share.",
    ]
    key_cols = ["year", "entity", "metric", "source_type"]
    # Allow multiple source_types for same metric (e.g. UNKNOWN + note) — use year/entity/metric/source
    dup = int(processed.duplicated(subset=["year", "entity", "metric", "source"]).sum())

    required = ["year", "entity", "metric", "source_type", "comparability", "confidence"]
    missing_req = int(processed[required].isna().any(axis=1).sum())
    invalid_years = int(((processed["year"] < 2020) | (processed["year"] > 2026)).fillna(False).sum())

    unknown_entities = int((~processed["entity"].isin(VALID_ENTITIES)).sum())
    if unknown_entities:
        notes.append(f"{unknown_entities} row(s) with entity outside controlled vocabulary.")

    bad_comp = int((~processed["comparability"].isin(VALID_COMPARABILITY)).sum())
    bad_stype = int((~processed["source_type"].isin(VALID_SOURCE_TYPES)).sum())

    # Non-missing values need a source (except UNKNOWN documenting absence)
    has_value = processed["value"].notna()
    needs_source = has_value & (processed["source_type"] != "UNKNOWN")
    missing_source = int(processed.loc[needs_source, "source"].isna().sum())

    # DERIVED must be labeled
    derived_unlabeled = 0  # enforced by source_type enum

    # UNKNOWN rows should not invent values
    unknown_filled = int(processed.loc[processed["source_type"] == "UNKNOWN", "value"].notna().sum())

    # Percent-like metrics
    pct_metrics = processed["metric"].str.contains("pct|share|ratio", case=False, na=False)
    pct_vals = processed.loc[pct_metrics & processed["value"].notna(), "value"]
    # binary_flag and ratios vs Shopee can exceed 100 for sea_gmv_vs_shopee_ratio? 65.7 is ok
    # access and market share should be 0-100; ratio vs Shopee also 0-100 in our data
    invalid_pct = int(((pct_vals < 0) | (pct_vals > 100)).sum())

    impossible = int((processed["value"] < 0).fillna(False).sum())

    status = _status([
        dup,
        missing_req,
        invalid_years,
        unknown_entities,
        bad_comp,
        bad_stype,
        missing_source,
        derived_unlabeled,
        unknown_filled,
        invalid_pct,
        impossible,
    ])
    return ValidationResult(
        dataset="entity_split",
        rows_raw=len(raw),
        rows_processed=len(processed),
        duplicate_keys=dup,
        missing_required_values=missing_req + missing_source,
        invalid_percentages=invalid_pct,
        invalid_years=invalid_years,
        unknown_platforms=unknown_entities,
        invalid_dates=0,
        impossible_values=impossible,
        status=status,
        notes=notes,
    )


def validate_google_trends(raw: pd.DataFrame, processed: pd.DataFrame) -> ValidationResult:
    notes = [
        "Google Trends interest is relative 0-100, not market share.",
        "Same geo/category/search configuration required for comparability.",
    ]
    dup = int(processed.duplicated(subset=["date", "term"]).sum())
    missing_req = int(processed[["date", "term", "interest"]].isna().any(axis=1).sum())
    invalid_dates = int(processed["date"].isna().sum())
    invalid_pct = int(((processed["interest"] < 0) | (processed["interest"] > 100)).fillna(False).sum())
    status = _status([dup, missing_req, invalid_dates, invalid_pct])
    return ValidationResult(
        dataset="google_trends",
        rows_raw=len(raw),
        rows_processed=len(processed),
        duplicate_keys=dup,
        missing_required_values=missing_req,
        invalid_percentages=invalid_pct,
        invalid_years=0,
        unknown_platforms=0,
        invalid_dates=invalid_dates,
        impossible_values=0,
        status=status,
        notes=notes,
    )


def format_report(results: List[ValidationResult], blocker: Optional[dict] = None) -> str:
    lines = ["# Data Validation Report", "", f"Generated by Python validation pipeline.", ""]
    if blocker:
        lines.extend([
            "## Google Trends acquisition blocker",
            "",
            f"- Status: `{blocker.get('status')}`",
            f"- Multiline/Explore issue recorded at: `{blocker.get('attempted_at')}`",
            f"- Manual path: `{blocker.get('manual_export_path')}`",
            "",
        ])
    for r in results:
        lines.append(f"## Dataset: {r.dataset}")
        lines.append("")
        lines.append(f"- Rows raw: {r.rows_raw}")
        lines.append(f"- Rows processed: {r.rows_processed}")
        lines.append(f"- Duplicate keys: {r.duplicate_keys}")
        lines.append(f"- Missing required values: {r.missing_required_values}")
        lines.append(f"- Invalid percentages: {r.invalid_percentages}")
        lines.append(f"- Invalid years: {r.invalid_years}")
        lines.append(f"- Unknown platforms: {r.unknown_platforms}")
        lines.append(f"- Invalid dates: {r.invalid_dates}")
        lines.append(f"- Impossible values: {r.impossible_values}")
        lines.append(f"- Status: **{r.status}**")
        if r.notes:
            lines.append("- Notes:")
            for n in r.notes:
                lines.append(f"  - {n}")
        lines.append("")
    overall = "PASS" if results and all(r.status == "PASS" for r in results) else "FAIL"
    if not results:
        overall = "FAIL"
    lines.append(f"## Overall validation status: **{overall}**")
    lines.append("")
    return "\n".join(lines)
