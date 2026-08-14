# Data Quality Assessment — Milestone 2

Companion to `research/data_quality_validation_report.md` (machine validation output).

## Quality scorecard

| Dataset | Completeness | Accuracy / credibility | Consistency | Timeliness | Reproducibility | Comparability | Coverage | Overall |
|---------|--------------|------------------------|------------|------------|-----------------|---------------|----------|---------|
| market_position | MEDIUM (missing 2021; some GMV blank) | MEDIUM (secondary MW reproductions) | MEDIUM (combined 2025 entity break) | HIGH (through 2025) | HIGH (citation per row) | MEDIUM (conditional) | MEDIUM | MEDIUM |
| google_trends | LOW this milestone (not acquired) | N/A until acquired | N/A | N/A | HIGH when manual CSV added | HIGH as interest | N/A | BLOCKED |
| competitive_events | MEDIUM (selected major events) | HIGH for dated corporate/regulatory facts | HIGH | HIGH | HIGH | N/A | MEDIUM | HIGH |
| company_context | LOW-MEDIUM (selected metrics only) | HIGH for disclosed figures; MEDIUM for YoY back-calcs | MEDIUM across companies | HIGH | HIGH | LOW vs platform dyad | LOW for Indonesia dyad | MEDIUM (as context) |
| macro | MEDIUM (WDI nulls in recent years) | HIGH | HIGH | MEDIUM-HIGH | HIGH | N/A | MEDIUM | HIGH (as context) |

## Validation execution

Automated validation was executed via `python/process_data.py` on 2026-08-12.

Results:

- market_position: PASS (24 raw / 24 processed)
- events: PASS (6 / 6)
- sea: PASS (8 / 8)
- goto: PASS (6 / 6)
- macro: PASS (55 / 55)
- google_trends: BLOCKED (no CSV)

Overall acquired-dataset validation: **PASS**  
Gate 2 completion considering Trends priority: **PARTIAL**

## Issues explicitly retained (not “fixed” by invention)

1. Missing 2021 Indonesia platform shares in free public citations.
2. Missing GMV dollar values for some year×platform cells.
3. 2025 Tokopedia represented only as combined Tokopedia + TikTok Shop in free MW reproductions used here.
4. Google Trends not in processed outputs due to rate limiting.
5. Sea metrics are not Indonesia-only.
6. GoTo Core GTV excludes Tokopedia post-deal; service fee is not GMV.

## Cleaning performed

- Platform name canonicalization
- Numeric coercion with NA retention
- Date parsing for events
- Macro year/value typing
- Company context concatenation with explicit company labels
- No imputation, no monthly interpolation, no synthetic rows
