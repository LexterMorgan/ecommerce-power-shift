# Data Sources — Gate 2 Registry

**Updated:** 2026-08-12 (Milestone 2 acquisition)  
Primary research question: How did Shopee's competitive position in Indonesia change relative to Tokopedia, and what observable market factors help explain that shift?

Machine-readable copy: `data/metadata/source_registry.csv`

## Sources used in acquired datasets

| Source name | Organization | URL | Source type | Dataset | Access method | Access date | Coverage | Metric definitions | Reliability | Comparability | Limitations | Used? |
|-------------|--------------|-----|-------------|---------|---------------|-------------|----------|--------------------|-------------|---------------|-------------|-------|
| Momentum Works public excerpts | Momentum Works via Youngster / CNBC / Bisnis / Kemendag journal | citation URLs in raw CSV | industry_estimate_secondary | market_position | manual curation | 2026-08-12 | ID annual 2020,2022-2025 | Estimated GMV/share | MEDIUM | CONDITIONALLY COMPARABLE | Paid full matrices not acquired; secondary transcription risk; 2025 combined entity | Yes |
| Google Trends | Google | https://trends.google.com/trends/explore?date=today%205-y&geo=ID&q=Shopee,Tokopedia | search_interest | google_trends | blocked automated (429); manual export pending | 2026-08-12 | intended today 5-y ID | Relative interest 0-100 | MEDIUM | DIRECTLY as interest | Rate limits; not share | Pending manual |
| GoTo press/IR/transcripts | GoTo | https://www.gotocompany.com/en/news/press/ | company_disclosure | company_context + events | manual curation | 2026-08-12 | 2024-2025 selected | Service fee, Core GTV, ATU | HIGH | NOT vs Sea/MW dyad | Tokopedia deconsolidated | Yes |
| Sea Limited SEC/IR | Sea Limited | https://www.sea.com/investor/home ; SEC exhibit | company_filing | company_context | manual curation | 2026-08-12 | 2024-2026Q1 selected | Shopee GMV/orders/revenue | HIGH | NOT Indonesia dyad | Multi-country | Yes |
| World Bank Open Data | World Bank | https://api.worldbank.org/v2/country/IDN/indicator/ | official_open_data | macro | public API | 2026-08-12 | 2015-2025 | WDI definitions | HIGH | N/A | Not platform-specific; some null years | Yes |
| Reuters / AP / legal explainers | Various | event `source_url` fields | news/legal | events | manual curation | 2026-08-12 | 2021-2024 events | Event facts | HIGH | N/A | Not causal | Yes |

## Rejected / not acquired this milestone

| Source | Reason |
|--------|--------|
| Momentum Works paid full report | No purchase executed; no paywall bypass |
| Similarweb historical | Paid for useful depth |
| Official monthly Indonesia platform GMV | NOT PUBLICLY AVAILABLE |
| Proprietary platform internals | Out of scope |

## Reliability tiers (reminder)

1 Official filings/government · 2 Original industry research · 3 Reputable news · 4 Aggregators · 5 Search/social
