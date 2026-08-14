# Data Availability — Gate 2 Update

**Updated:** 2026-08-12 after acquisition attempt.

Primary research question: How did Shopee's competitive position in Indonesia change relative to Tokopedia, and what observable market factors help explain that shift?

## Acquisition outcome summary

| Dataset | Decision | Local raw path | Processed path | Status |
|---------|----------|----------------|----------------|--------|
| market_position | PRIMARY ACQUIRED | `data/raw/market_position/` | `data/processed/market_position/market_position_indonesia.csv` | PASS validation |
| google_trends | PRIMARY BLOCKED | blocker + manual instructions | not produced | HTTP 429 |
| competitive_events | SUPPORTING ACQUIRED | `data/raw/events/` | `data/processed/events/competitive_events.csv` | PASS |
| company_context | SUPPORTING ACQUIRED | `data/raw/sea/`, `data/raw/goto/` | `data/processed/company_context/company_metrics.csv` | PASS |
| macro | SUPPORTING ACQUIRED | `data/raw/macro/` | `data/processed/macro/indonesia_macro_indicators.csv` | PASS |

## Matrix (post-acquisition)

| Metric | Shopee | Tokopedia | Historical Coverage | Granularity | Source | Accessibility | Comparability | Recommended Use |
|--------|--------|-----------|---------------------|-------------|--------|---------------|---------------|-----------------|
| Market share (Indonesia) | Acquired for 2020,2022-2025 | Acquired standalone 2020,2022-2024; 2025 combined with TikTok Shop | Annual excerpts | Annual | MW public excerpts | Local CSV | CONDITIONALLY COMPARABLE | Primary competitive trajectory |
| GMV (Indonesia platform) | Partial (some years) | Partial / combined 2025 | Annual where published | Annual | MW public excerpts | Local CSV | CONDITIONALLY | With share; blanks retained |
| Search interest | BLOCKED this run | BLOCKED this run | — | — | Google Trends | Manual pending | DIRECTLY as interest | Acquire manually then re-run process |
| Competitive events | Yes | Yes | 2021-2024 | Event | Public PRs/news | Local CSV | N/A | Overlay only |
| Sea Shopee GMV/orders/revenue | Acquired selected | N/A | 2024-2026Q1 | Annual/quarter | Sea filings | Local CSV | NOT vs Tokopedia ID | Context |
| GoTo service fee / Core GTV | N/A | Fee link only; Core GTV excludes Tokopedia | 2025 selected | Quarter/annual | GoTo | Local CSV | NOT vs Sea GMV | Structural context |
| Macro GDP/internet/inflation | N/A | N/A | 2015-2025 | Annual | World Bank | Local CSV/JSON | N/A | Context |

## Remaining gaps

- Google Trends local series (rate-limited)
- 2021 Indonesia platform shares (not found in free citations used)
- Official monthly Indonesia platform GMV/revenue
- Paid full Momentum Works matrices
- Indonesia-only Sea Shopee operating metrics
- Standalone Tokopedia 2025 share in free MW reproductions used here

## Recommended next milestone

**Gate 3 enrichment + Gate 4 exploratory analysis** on acquired market_position + events + macro/company context, **after** optional manual Google Trends drop-in and re-running `scripts/process_data.py`.

Do not build SQL/dashboard yet.
