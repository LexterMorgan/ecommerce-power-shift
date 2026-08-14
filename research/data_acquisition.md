# Data Acquisition Log — Milestone 2 / Gate 2

**Date:** 2026-08-12  
**Workflow:** Cursor + Grok execution  
**Status:** PARTIAL (primary market-position acquired; Google Trends automated acquisition blocked)

## Source decision matrix

| Dataset | Source | Data Type | Time Coverage | Geography | Unit of Observation | Main Metrics | Access | Reliability | Comparable? | Reproducible? | Role | Decision |
|---------|--------|-----------|---------------|-----------|---------------------|--------------|--------|-------------|-------------|---------------|------|----------|
| Indonesia platform GMV/share excerpts | Momentum Works via public secondary citations | Panel estimates | 2020, 2022–2025 (annual; 2021 not found in free citations) | Indonesia | year × platform | market_share_pct, gmv_estimate | Public articles (full MW paid, not purchased) | MEDIUM | CONDITIONALLY | Yes (citation-backed curation) | PRIMARY DATASET | **ACQUIRED (curated)** |
| Google Trends Shopee vs Tokopedia | Google Trends | Time series | Intended today 5-y | Indonesia | date × term | relative interest | Free UI/API but rate-limited | MEDIUM | DIRECTLY (as interest) | Yes when CSV present | PRIMARY DATASET | **BLOCKED automated; manual pending** |
| Competitive events | GoTo PR, Reuters, AP, legal explainers | Event timeline | 2021–2024 | Indonesia | event | dated events | Public | HIGH | N/A | Yes | SUPPORTING DATASET | **ACQUIRED** |
| Sea / Shopee official metrics | Sea SEC/IR | Company metrics | 2024–2026Q1 selected | Multi-country | period × metric | GMV, orders, revenue | Public | HIGH | NOT vs Tokopedia ID | Yes | SUPPORTING DATASET | **ACQUIRED (curated)** |
| GoTo / Tokopedia context | GoTo IR/press/transcripts | Company metrics | 2024–2025 selected | Indonesia-centric | period × metric | service fee, Core GTV, ATU | Public | HIGH | NOT vs Sea GMV | Yes | SUPPORTING DATASET | **ACQUIRED (curated)** |
| Indonesia macro | World Bank API | Macro indicators | 2015–2025 | Indonesia | year × indicator | GDP, inflation, internet, etc. | Public API | HIGH | N/A | Yes | SUPPORTING DATASET | **ACQUIRED** |
| Similarweb long history | Similarweb | Traffic estimates | multi-year | Indonesia possible | month × site | visits | Paid for useful history | MEDIUM | conditional | Paid-dependent | REJECTED (for now) | **REJECTED** — no paid access assumed |
| Full Momentum Works paid matrices | Momentum Works | Panel estimates | multi-year | SEA/Indonesia | year × platform | full GMV/share tables | Paid | MEDIUM-HIGH | conditional | Yes if purchased | REJECTED (this milestone) | **NOT ACQUIRED** — no paywall bypass |
| BPS Statistik E-Commerce PDFs | BPS | Sector survey | annual pubs | Indonesia | survey aggregates | business e-commerce stats | Free PDFs | HIGH | not platform dyad | Yes | CONTEXT ONLY | Deferred; World Bank covers macro need for Gate 2 |
| e-Conomy SEA PDFs | Google/Temasek/Bain | Sector GMV | annual | SEA/Indonesia | sector/country | digital economy GMV | Free reports | HIGH | not platform dyad | Yes | CONTEXT ONLY | Deferred |

## Acquisition actions performed

1. Created raw/processed/metadata directory layout.
2. Curated Indonesia market-position CSV from public MW citations (Youngster, CNBC, Bisnis, Kemendag journal).
3. Built competitive-events CSV from primary/reputable public sources.
4. Curated Sea and GoTo company-context CSVs from public disclosures.
5. Downloaded World Bank Indonesia indicator JSON/CSV via open API (`scripts/acquire_data.py`).
6. Attempted Google Trends automated acquisition → HTTP 429 rate limit; documented manual export path.

## Datasets rejected / deferred

- Similarweb paid history
- Momentum Works paid full report purchase (not executed)
- Fabricated monthly interpolations
- SEA-only platform GMV rows mixed into Indonesia market_position (excluded)

## Processing

Run:

```bash
python3 scripts/acquire_data.py   # refreshes World Bank raw extract
python3 scripts/process_data.py   # clean + validate + write processed
```

## Gate note

A credible primary analytical dataset (**market_position**) was acquired and validated. Google Trends remains a documented blocker pending manual CSV drop-in. Gate 2 status: **PARTIAL**.
