# Dashboard static data contract (Gate 10B)

**File path:** `frontend/public/data/dashboard_data.json`  
**Generator:** `python3 scripts/export_dashboard_data.py`  
**Builder module:** `python/dashboard_data.py`  
**Contract version:** `1.0`

## Purpose

Version-controlled analysis-ready snapshot consumed by the React presentation layer.  
PostgreSQL/SQL remain the analytical infrastructure; the public dashboard does not connect to Postgres or FastAPI.

## Generation flow

```
analysis-ready CSVs (+ Gate 7A share-gap table)
        ↓
python/dashboard_data.py
        ↓
frontend/public/data/dashboard_data.json
        ↓
React (fetch at runtime)
```

Optional analytical path (not required by public UI):

```
CSVs → scripts/build_dashboard_sql.py → PostgreSQL views
```

## Top-level schema

| Field | Type | Notes |
|-------|------|-------|
| `contract_version` | string | e.g. `1.0` |
| `gate` | string | export gate label (`10B`) |
| `generated_at` | ISO timestamp | UTC |
| `deployment_mode` | string | always `static_snapshot` |
| `rules` | string[] | presentation rules |
| `sources` | object | relative paths to CSV inputs |
| `overview` | object | locked story KPIs + UNKNOWN rows |
| `standalone_shares` | array | 2022–2024 Shopee / Legacy OBSERVED |
| `post_break_shares` | array | 2025 Shopee / Combined OBSERVED |
| `legacy_unknown` | array | 2025 Legacy UNKNOWN (value null) |
| `gmv_estimates` | array | OBSERVED/DERIVED non-null GMV |
| `access_metrics` | array | APJII access OBSERVED |
| `tts_labeled_gmv` | array | TTS GMV OBSERVED |
| `scenarios` | array | Gate 6 SCENARIO gap bands |
| `share_gap_summary` | array | Gate 7A gap extract |
| `filter_keys` | array | distinct filter dimensions |
| `competitive_panel` | array | full panel rows |

## Panel / share row fields

| Field | Type | Semantics |
|-------|------|-----------|
| `year` | number \| null | calendar year |
| `analytical_entity` | string | marketplace / entity label |
| `entity_type` | string | standalone / combined / combined_derived |
| `metric` | string | e.g. `market_share_pct` |
| `value` | number \| **null** | null when UNKNOWN |
| `value_status` | string | `OBSERVED` \| `DERIVED` \| `UNKNOWN` |
| `comparability` | string | DIRECT / CONDITIONAL / NOT COMPARABLE… |
| `source_publisher` / `citation_url` / `confidence` / `notes` | string | provenance |

Scenario rows use `value_type=SCENARIO` (not OBSERVED history).

## Hard rules

1. UNKNOWN/null stays null — never zero.
2. 2022–2024 standalone dyad stays separate from 2025 Combined.
3. No new metrics invented in the export or React.
4. React must not recalculate business conclusions.

## Regenerate

```bash
python3 scripts/export_dashboard_data.py
```
