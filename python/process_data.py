"""End-to-end process: load → clean → validate → write processed + reports."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from python.cleaning.clean import (
    clean_company_metrics,
    clean_entity_split,
    clean_events,
    clean_google_trends,
    clean_macro,
    clean_market_position,
    clean_structural_break,
)
from python.ingestion.load_raw import (
    load_entity_split,
    load_events,
    load_goto,
    load_google_trends,
    load_macro,
    load_market_position,
    load_sea,
    load_structural_break,
    load_trends_blocker,
)
from python.paths import METADATA, PROCESSED, REPORTS
from python.validation.validate import (
    format_report,
    validate_company,
    validate_entity_split,
    validate_events,
    validate_google_trends,
    validate_macro,
    validate_market_position,
    validate_structural_break,
)


def ensure_dirs() -> None:
    for p in [
        PROCESSED / "market_position",
        PROCESSED / "google_trends",
        PROCESSED / "events",
        PROCESSED / "company_context",
        PROCESSED / "macro",
        PROCESSED / "structural_break",
        METADATA,
        REPORTS,
    ]:
        p.mkdir(parents=True, exist_ok=True)


def write_inventory(rows: list) -> None:
    path = METADATA / "dataset_inventory.csv"
    pd.DataFrame(rows).to_csv(path, index=False)


def write_source_registry(rows: list) -> None:
    path = METADATA / "source_registry.csv"
    pd.DataFrame(rows).to_csv(path, index=False)


def main() -> int:
    ensure_dirs()
    results = []
    inventory = []
    sources = []
    acquired_at = datetime.now(timezone.utc).isoformat()

    # Market position
    raw_mp = load_market_position()
    proc_mp = clean_market_position(raw_mp)
    out_mp = PROCESSED / "market_position" / "market_position_indonesia.csv"
    proc_mp.to_csv(out_mp, index=False)
    res_mp = validate_market_position(raw_mp, proc_mp)
    results.append(res_mp)
    inventory.append({
        "dataset_name": "market_position",
        "dataset_role": "PRIMARY DATASET",
        "source": "Momentum Works via public secondary citations",
        "raw_path": raw_mp.attrs["raw_path"],
        "processed_path": str(out_mp),
        "format": "csv",
        "rows_raw": len(raw_mp),
        "rows_processed": len(proc_mp),
        "time_start": int(proc_mp["year"].min()),
        "time_end": int(proc_mp["year"].max()),
        "geography": "Indonesia",
        "grain": "year x platform",
        "status": res_mp.status,
        "limitations": "Secondary reproductions; paid full MW matrices not acquired; combined entity in 2025; missing years/GMV cells retained",
    })
    sources.append({
        "source_name": "Momentum Works public excerpts",
        "organization": "Momentum Works (via Youngster/CNBC/Bisnis/Kemendag journal)",
        "url": "multiple citation_url fields in raw CSV",
        "source_type": "industry_estimate_secondary",
        "dataset_provided": "market_position",
        "access_method": "manual curation of public articles",
        "access_date": "2026-08-12",
        "coverage": "Indonesia annual platform share/GMV excerpts 2020,2022-2025",
        "reliability": "MEDIUM",
        "comparability": "CONDITIONALLY COMPARABLE within methodology; combined 2025 break",
        "used_in_final_analysis_candidate": "yes",
    })

    # Events
    raw_ev = load_events()
    proc_ev = clean_events(raw_ev)
    out_ev = PROCESSED / "events" / "competitive_events.csv"
    proc_ev.to_csv(out_ev, index=False)
    res_ev = validate_events(raw_ev, proc_ev)
    results.append(res_ev)
    inventory.append({
        "dataset_name": "competitive_events",
        "dataset_role": "SUPPORTING DATASET",
        "source": "GoTo PR, Reuters, AP, legal explainers",
        "raw_path": raw_ev.attrs["raw_path"],
        "processed_path": str(out_ev),
        "format": "csv",
        "rows_raw": len(raw_ev),
        "rows_processed": len(proc_ev),
        "time_start": str(proc_ev["event_date"].min().date()),
        "time_end": str(proc_ev["event_date"].max().date()),
        "geography": "Indonesia",
        "grain": "one row per event",
        "status": res_ev.status,
        "limitations": "Not causal; selected major events only; Gate 3 expanded timeline through 2025 Seller Center + KPPU",
    })

    # Structural break evidence (Gate 3)
    raw_sb = load_structural_break()
    proc_sb = clean_structural_break(raw_sb)
    out_sb = PROCESSED / "structural_break" / "transition_2024_2025_evidence.csv"
    proc_sb.to_csv(out_sb, index=False)
    res_sb = validate_structural_break(raw_sb, proc_sb)
    results.append(res_sb)
    inventory.append({
        "dataset_name": "structural_break",
        "dataset_role": "SUPPORTING DATASET",
        "source": "Momentum Works via Bisnis/TechNode/Digital in Asia + DERIVED residuals",
        "raw_path": raw_sb.attrs["raw_path"],
        "processed_path": str(out_sb),
        "format": "csv",
        "rows_raw": len(raw_sb),
        "rows_processed": len(proc_sb),
        "time_start": int(proc_sb["year"].min()),
        "time_end": int(proc_sb["year"].max()),
        "geography": "Indonesia",
        "grain": "year x entity x metric x data_type",
        "status": res_sb.status,
        "limitations": "2025 Combined ≠ Legacy Tokopedia; residual Legacy GMV LOW confidence; UNKNOWN standalone 2025 Tokopedia share retained as missing",
    })
    sources.append({
        "source_name": "2024-2025 structural break evidence table",
        "organization": "Project curation from MW secondary citations + labeled DERIVED",
        "url": "see transition_2024_2025_evidence.csv source_url fields",
        "source_type": "secondary_estimate_and_derived",
        "dataset_provided": "structural_break",
        "access_method": "manual curation of public articles; arithmetic labeled DERIVED",
        "access_date": "2026-08-12",
        "coverage": "Indonesia 2024-2025 entity-split market position evidence",
        "reliability": "MEDIUM secondary; LOW for residual Legacy 2025",
        "comparability": "STRUCTURAL BREAK — Combined 2025 not comparable to Legacy Tokopedia 2024",
        "used_in_final_analysis_candidate": "yes_with_entity_labels",
    })

    # Gate 3B entity-split acquisition
    raw_es = load_entity_split()
    proc_es = clean_entity_split(raw_es)
    out_es = PROCESSED / "structural_break" / "entity_split_2024_2025_processed.csv"
    proc_es.to_csv(out_es, index=False)
    res_es = validate_entity_split(raw_es, proc_es)
    results.append(res_es)
    inventory.append({
        "dataset_name": "entity_split",
        "dataset_role": "SUPPORTING DATASET",
        "source": "MW public excerpts + APJII + GoTo/TikTok primary + Magpie FMCG context",
        "raw_path": raw_es.attrs["raw_path"],
        "processed_path": str(out_es),
        "format": "csv",
        "rows_raw": len(raw_es),
        "rows_processed": len(proc_es),
        "time_start": int(proc_es["year"].min()),
        "time_end": int(proc_es["year"].max()),
        "geography": "Indonesia (plus SEA context rows)",
        "grain": "year x entity x metric",
        "status": res_es.status,
        "limitations": "Legacy Tokopedia 2025 GMV/share UNKNOWN; residual Combined-TTS not used as observed; APJII≠GMV; Magpie≠national GMV",
    })

    # Company context combined
    raw_sea = load_sea()
    raw_goto = load_goto()
    proc_sea = clean_company_metrics(raw_sea, "Sea Limited")
    proc_goto = clean_company_metrics(raw_goto, "GoTo")
    proc_co = pd.concat([proc_sea, proc_goto], ignore_index=True)
    out_co = PROCESSED / "company_context" / "company_metrics.csv"
    proc_co.to_csv(out_co, index=False)
    res_sea = validate_company("sea", raw_sea, proc_sea)
    res_goto = validate_company("goto", raw_goto, proc_goto)
    results.extend([res_sea, res_goto])
    inventory.append({
        "dataset_name": "company_context",
        "dataset_role": "SUPPORTING DATASET",
        "source": "Sea SEC/IR + GoTo IR/transcripts",
        "raw_path": f"{raw_sea.attrs['raw_path']}; {raw_goto.attrs['raw_path']}",
        "processed_path": str(out_co),
        "format": "csv",
        "rows_raw": len(raw_sea) + len(raw_goto),
        "rows_processed": len(proc_co),
        "time_start": "2024",
        "time_end": "2026Q1",
        "geography": "Mixed (Sea multi-country; GoTo Indonesia-centric)",
        "grain": "period x metric x company",
        "status": "PASS" if res_sea.status == "PASS" and res_goto.status == "PASS" else "FAIL",
        "limitations": "NOT comparable to Indonesia platform dyad; Sea not Indonesia-only; GoTo excludes Tokopedia from Core GTV post-deal",
    })

    # Macro
    raw_macro = load_macro()
    proc_macro = clean_macro(raw_macro)
    out_macro = PROCESSED / "macro" / "indonesia_macro_indicators.csv"
    proc_macro.to_csv(out_macro, index=False)
    res_macro = validate_macro(raw_macro, proc_macro)
    results.append(res_macro)
    inventory.append({
        "dataset_name": "macro",
        "dataset_role": "SUPPORTING DATASET",
        "source": "World Bank Open Data API",
        "raw_path": raw_macro.attrs["raw_path"],
        "processed_path": str(out_macro),
        "format": "csv/json",
        "rows_raw": len(raw_macro),
        "rows_processed": len(proc_macro),
        "time_start": int(proc_macro["year"].min()),
        "time_end": int(proc_macro["year"].max()),
        "geography": "Indonesia",
        "grain": "year x indicator",
        "status": res_macro.status,
        "limitations": "Not platform-specific; some recent years null in WDI",
    })
    sources.append({
        "source_name": "World Bank Open Data",
        "organization": "World Bank",
        "url": "https://api.worldbank.org/v2/country/IDN/indicator/",
        "source_type": "official_open_data",
        "dataset_provided": "macro",
        "access_method": "public API",
        "access_date": "2026-08-12",
        "coverage": "Indonesia 2015-2025 selected indicators",
        "reliability": "HIGH",
        "comparability": "N/A (context)",
        "used_in_final_analysis_candidate": "yes_context",
    })

    # Google Trends (optional if present)
    blocker = load_trends_blocker()
    raw_gt = load_google_trends()
    if raw_gt is not None:
        proc_gt = clean_google_trends(raw_gt)
        out_gt = PROCESSED / "google_trends" / "google_trends_indonesia_long.csv"
        proc_gt.to_csv(out_gt, index=False)
        # also wide for convenience
        wide = proc_gt.pivot_table(index="date", columns="term", values="interest").reset_index()
        wide.to_csv(PROCESSED / "google_trends" / "google_trends_indonesia_wide.csv", index=False)
        res_gt = validate_google_trends(raw_gt, proc_gt)
        results.append(res_gt)
        inventory.append({
            "dataset_name": "google_trends",
            "dataset_role": "PRIMARY DATASET",
            "source": "Google Trends",
            "raw_path": raw_gt.attrs["raw_path"],
            "processed_path": str(out_gt),
            "format": "csv",
            "rows_raw": len(raw_gt),
            "rows_processed": len(proc_gt),
            "time_start": str(proc_gt["date"].min().date()),
            "time_end": str(proc_gt["date"].max().date()),
            "geography": "Indonesia (ID)",
            "grain": "date x term",
            "status": res_gt.status,
            "limitations": "Relative interest only; not market share",
        })
    else:
        inventory.append({
            "dataset_name": "google_trends",
            "dataset_role": "PRIMARY DATASET",
            "source": "Google Trends",
            "raw_path": "",
            "processed_path": "",
            "format": "csv",
            "rows_raw": 0,
            "rows_processed": 0,
            "time_start": "",
            "time_end": "",
            "geography": "Indonesia (ID)",
            "grain": "date x term",
            "status": "BLOCKED",
            "limitations": "Automated acquisition rate-limited (HTTP 429); manual export instructions in data/raw/google_trends/README_MANUAL_EXPORT.md",
        })
        sources.append({
            "source_name": "Google Trends",
            "organization": "Google",
            "url": "https://trends.google.com/trends/explore?date=today%205-y&geo=ID&q=Shopee,Tokopedia",
            "source_type": "search_interest",
            "dataset_provided": "google_trends",
            "access_method": "blocked automated; manual export pending",
            "access_date": "2026-08-12",
            "coverage": "intended today 5-y Indonesia",
            "reliability": "MEDIUM",
            "comparability": "DIRECTLY COMPARABLE as relative interest when acquired under same settings",
            "used_in_final_analysis_candidate": "yes_when_acquired",
        })

    write_inventory(inventory)
    # append more sources
    sources.extend([
        {
            "source_name": "GoTo disclosures",
            "organization": "PT GoTo Gojek Tokopedia Tbk",
            "url": "https://www.gotocompany.com/en/news/press/",
            "source_type": "company_filing_press",
            "dataset_provided": "company_context",
            "access_method": "manual curation from public IR/press/transcripts",
            "access_date": "2026-08-12",
            "coverage": "2024-2025 selected metrics",
            "reliability": "HIGH",
            "comparability": "NOT COMPARABLE to Sea GMV or MW Indonesia share",
            "used_in_final_analysis_candidate": "yes_context",
        },
        {
            "source_name": "Sea Limited disclosures",
            "organization": "Sea Limited",
            "url": "https://www.sea.com/investor/home",
            "source_type": "company_filing",
            "dataset_provided": "company_context",
            "access_method": "manual curation from SEC/IR",
            "access_date": "2026-08-12",
            "coverage": "2024-2026Q1 selected Shopee metrics",
            "reliability": "HIGH",
            "comparability": "NOT COMPARABLE as Indonesia dyad",
            "used_in_final_analysis_candidate": "yes_context",
        },
        {
            "source_name": "Competitive event sources",
            "organization": "GoTo/Reuters/AP/legal explainers",
            "url": "see events CSV source_url",
            "source_type": "event_timeline",
            "dataset_provided": "competitive_events",
            "access_method": "manual curation",
            "access_date": "2026-08-12",
            "coverage": "2021-2025 major events (reg, TTS pause, deal, Seller Center, KPPU)",
            "reliability": "HIGH",
            "comparability": "N/A",
            "used_in_final_analysis_candidate": "yes_context",
        },
    ])
    write_source_registry(sources)

    report = format_report(results, blocker=blocker)
    report_path = REPORTS / "data_quality_validation_report.md"
    report_path.write_text(report)
    (METADATA / "validation_results.json").write_text(
        json.dumps(
            {
                "generated_at": acquired_at,
                "results": [r.to_dict() for r in results],
                "trends_blocker": blocker,
            },
            indent=2,
            default=str,
        )
    )
    print(report)
    print(f"Wrote processed datasets under {PROCESSED}")
    print(f"Wrote validation report to {report_path}")

    # Gate status hint
    primary_ok = res_mp.status == "PASS"
    trends_ok = raw_gt is not None and results[-1].dataset == "google_trends" and results[-1].status == "PASS"
    if primary_ok and trends_ok:
        gate = "PASS"
    elif primary_ok:
        gate = "PARTIAL"
    else:
        gate = "BLOCKED"
    print(f"GATE2_STATUS={gate}")
    return 0 if primary_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
