# Gate 7B — SQL / Dashboard Data Layer (PostgreSQL)

**Status:** Implemented (PostgreSQL canonical)  
**Prerequisite:** Gate 7A complete (`competitive_panel.csv` + `analysis/outputs/tables/share_gap_summary.csv`)  
**Runner:** `python3 scripts/build_dashboard_sql.py`  
**Canonical database:** PostgreSQL (`DATABASE_URL`, default `postgresql://localhost:5432/ecommerce_power_shift`)  
**JSON payload:** `data/dashboard/dashboard_payload.json`  
**SQLite:** **Deprecated** — see `data/dashboard/SQLITE_DEPRECATED.md` (do not treat `*.db` as canonical)

## Purpose

Expose existing analysis-ready results for an eventual dashboard. This layer does **not** invent metrics, reinterpret Gates 1–6, or change Gate 7A methodology.

## Source inputs (canonical)

| Role | Path |
|------|------|
| Canonical GMV/share | `data/processed/analysis_ready/competitive_panel.csv` |
| Access / TTS-labeled GMV / 2025 peers | `data/processed/2025_comparable/platform_metrics_2025_processed.csv` |
| Scenario inputs | `data/processed/gate6_scenario_inputs.csv` |
| Scenario outputs | `data/processed/gate6_scenario_outputs.csv` |
| Gate 7A gap extract | `analysis/outputs/tables/share_gap_summary.csv` |

## Architecture

```
sql/schema.sql                     # PostgreSQL DDL + views
python/build_dashboard_sql.py      # load → PostgreSQL → CSV exports → JSON payload
scripts/build_dashboard_sql.py     # wrapper

PostgreSQL database ecommerce_power_shift
data/dashboard/
  dashboard_payload.json
  manifest.json
  SQLITE_DEPRECATED.md
  exports/*.csv                    # view snapshots for frontend/tools
```

## Connection

```bash
# Create DB once (local Homebrew Postgres example)
createdb ecommerce_power_shift

# Optional override
export DATABASE_URL=postgresql://localhost:5432/ecommerce_power_shift

python3 scripts/build_dashboard_sql.py
```

The builder normalizes `DATABASE_URL` to SQLAlchemy `postgresql+psycopg://…`.

## Tables

| Table | Content |
|-------|---------|
| `dashboard_build_meta` | Build id / timestamp / gate |
| `fact_competitive_panel` | Full analysis-ready panel (incl. UNKNOWN nulls) |
| `fact_supporting_2025` | 2025 comparable metrics (access, TTS GMV, etc.) |
| `fact_scenario_inputs` | Gate 6 scenario inputs |
| `fact_scenario_outputs` | Gate 6 scenario outputs (SCENARIO / UNKNOWN) |
| `fact_share_gap_summary` | Gate 7A share-gap presentation extract |

## Views

| View | Purpose |
|------|---------|
| `v_competitive_panel_all` | Full panel |
| `v_market_share_plottable` | Share OBSERVED/DERIVED, non-null only |
| `v_market_share_standalone_2022_2024` | Phase 1 Shopee vs Legacy Tokopedia |
| `v_market_share_post_break_2025` | Phase 3 Shopee vs Combined (no Legacy) |
| `v_legacy_tokopedia_unknown_2025` | UNKNOWN rows (value IS NULL) |
| `v_gmv_estimates` | GMV OBSERVED/DERIVED non-null |
| `v_access_metrics` | APJII access OBSERVED |
| `v_tts_labeled_gmv` | TTS-labeled GMV OBSERVED |
| `v_scenario_gap_bands` | SCENARIO share-gap bands |
| `v_share_gap_summary` | Gate 7A gap table |
| `v_dashboard_filter_keys` | Distinct year / marketplace / metric / value_status / comparability |

## Filter support

Dashboard queries can filter `fact_competitive_panel` / `v_dashboard_filter_keys` by:

- `year`
- `analytical_entity` (marketplace)
- `metric`
- `value_status`
- `comparability`
- `entity_type` / `phase` where useful

Supporting and scenario tables keep their own entity / evidence_type / value_type columns.

## Hard rules

1. Preserve `OBSERVED` / `DERIVED` / `UNKNOWN` / `SCENARIO`.
2. UNKNOWN → SQL `NULL` only; never `0`.
3. Do not union Phase 1 Legacy Tokopedia shares with Phase 3 Combined into one continuous series.
4. No new business metrics beyond existing files.
5. Provenance columns (`source_publisher`, `citation_url`, `confidence`, `comparability`, notes) retained on the panel.
6. PostgreSQL is the only canonical database engine for Gate 7B+.

## Regenerate

```bash
# Optional if analysis tables missing:
python3 analysis/run_analysis.py

# Ensure Postgres is up and DB exists, then:
python3 scripts/build_dashboard_sql.py
python3 -m pytest tests/test_gate7b_dashboard_sql_smoke.py -q
```

## Example queries

```sql
-- Phase 1 standalone shares
SELECT year, analytical_entity, value, value_status, citation_url
FROM v_market_share_standalone_2022_2024
ORDER BY analytical_entity, year;

-- Phase 3 post-break (Combined ≠ Legacy)
SELECT analytical_entity, value, entity_type, comparability
FROM v_market_share_post_break_2025;

-- Confirm UNKNOWN stays null
SELECT analytical_entity, metric, value, value_status
FROM v_legacy_tokopedia_unknown_2025;
```

## Limitations before Gate 8

- No React app yet; consume PostgreSQL and/or `dashboard_payload.json` / `exports/*.csv`.
- No auth, API server, or live query endpoint.
- Secondary Momentum Works confidence labels are unchanged (not upgraded).
- Scenario bands remain illustrative (`value_type=SCENARIO`), not forecasts-as-fact.
- Access metrics remain access ≠ GMV.
- Legacy Tokopedia 2025 GMV/share remains UNKNOWN.
