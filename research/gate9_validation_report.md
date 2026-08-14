# Gate 9 — Validation Report

**Status:** PASS
**Generated (UTC):** 2026-08-14T10:27:42.768680+00:00
**Checks:** 28 total · 0 failed

## Scope

Validates Gates 1–8 locked outputs without changing metrics, schema, views, or conclusions.

## Locked story reference (unchanged)

| Item | Value |
|------|------:|
| `shopee_2022` | 36.0 |
| `legacy_2022` | 35.0 |
| `shopee_2024` | 46.0 |
| `legacy_2024` | 23.0 |
| `shopee_2025` | 54.0 |
| `combined_2025` | 38.0 |
| `legacy_2025` | UNKNOWN |

## Check results

### transformations

- **PASS** `panel_row_count` — rows=22 expected=22
- **PASS** `panel_analytical_allowlist` — entities=['Combined Tokopedia + TikTok Shop', 'Legacy Tokopedia', 'Shopee', 'TikTok Shop']
- **PASS** `panel_required_columns` — missing=none

### analytical_metrics

- **PASS** `locked_2022_Shopee_market_share_pct_OBSERVED` — expected=36.0 got=36.0
- **PASS** `locked_2022_Legacy Tokopedia_market_share_pct_OBSERVED` — expected=35.0 got=35.0
- **PASS** `locked_2024_Shopee_market_share_pct_OBSERVED` — expected=46.0 got=46.0
- **PASS** `locked_2024_Legacy Tokopedia_market_share_pct_OBSERVED` — expected=23.0 got=23.0
- **PASS** `locked_2025_Shopee_market_share_pct_OBSERVED` — expected=54.0 got=54.0
- **PASS** `locked_2025_Combined Tokopedia + TikTok Shop_market_share_pct_OBSERVED` — expected=38.0 got=38.0
- **PASS** `locked_2024_Combined Tokopedia + TikTok Shop_market_share_pct_DERIVED` — expected=34.0 got=34.0
- **PASS** `legacy_2025_unknown_null` — rows=2 nulls=2
- **PASS** `unknown_never_zero` — no UNKNOWN rows with value=0

### structural_break

- **PASS** `standalone_share_rows` — n=6
- **PASS** `post_break_excludes_legacy` — entities=['Combined Tokopedia + TikTok Shop', 'Shopee']
- **PASS** `post_break_share_rows` — n=2

### claims_provenance

- **PASS** `claim_doc_gate5_competitive_analysis.md` — missing_phrases=none
- **PASS** `claim_doc_gate6_competitive_evolution.md` — missing_phrases=none
- **PASS** `claim_doc_gate8_dashboard_architecture.md` — missing_phrases=none
- **PASS** `observed_have_citation` — observed_missing_citation=0
- **PASS** `value_status_vocabulary` — statuses=['DERIVED', 'OBSERVED', 'UNKNOWN']

### dashboard_metrics

- **PASS** `dashboard_manifest_postgres` — engine=postgresql
- **PASS** `sqlite_deprecated` — sqlite_status=deprecated_removed
- **PASS** `share_gap_2025_pp` — rows=1
- **PASS** `static_overview_shopee_2025` — got=54.0
- **PASS** `static_overview_combined_2025` — got=38.0
- **PASS** `static_overview_legacy_unknown_label` — got=UNKNOWN
- **PASS** `static_unknown_values_null` — n=2
- **PASS** `postgres_panel_count` — db=22 csv=22

## Dashboard runtime

- PostgreSQL: `ok`
- Static snapshot: `ok`

## Claim / provenance review

- Gate 5/6 claim-discipline phrases remain present in research docs.
- OBSERVED panel rows retain citation URLs.
- UNKNOWN Legacy Tokopedia 2025 values remain null (not zero).
- Combined ≠ Legacy structural-break separation retained in panel and API overview.

## Local run (current system)

```bash
export DATABASE_URL=postgresql://localhost:5432/ecommerce_power_shift
python3 scripts/build_dashboard_sql.py   # analytical PostgreSQL layer
python3 scripts/export_dashboard_data.py # static React snapshot
cd frontend && npm install && npm run dev
python3 scripts/run_gate9_validation.py
```

## Remaining before public portfolio polish

- Public Vercel project may still need to be connected/published (manual).
- Regenerate frontend/public/data/dashboard_data.json after analytical refreshes.
- Real portfolio screenshots remain a manual capture step.
- Event timeline / driver pages intentionally out of Gate 7B scope.
- PostgreSQL remains local/analytical infrastructure (not required by the public static UI).

**Exact next gate:** 10 — Documentation & Deployment

