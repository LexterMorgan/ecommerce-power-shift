# Data Dictionary

Human-readable companion to `data/metadata/data_dictionary.csv`.

Primary research question: How did Shopee's competitive position in Indonesia change relative to Tokopedia, and what observable market factors help explain that shift?

## Datasets

### market_position (PRIMARY)

- **Grain:** year × platform
- **Geography:** Indonesia
- **Key metrics:** `market_share_pct`, optional `gmv_estimate_usd_billion`
- **Comparability:** CONDITIONALLY COMPARABLE for Shopee vs standalone Tokopedia within the same source methodology; 2025 `Tokopedia + TikTok Shop` is combined and must not be treated as standalone Tokopedia without adjustment
- **Missingness:** GMV left blank when not published; years without verified public citations omitted (e.g. 2021)

### google_trends (PRIMARY when present)

- **Grain:** date × term
- **Geography:** Indonesia (`ID`)
- **Key metric:** `interest` (0–100 relative index)
- **Comparability:** DIRECTLY COMPARABLE as attention under identical Trends settings
- **Status this milestone:** acquisition blocked by rate limits; pipeline ready for manual CSV

### competitive_events (SUPPORTING)

- **Grain:** one row per event
- **Use:** overlay / structural-break context only
- **Rule:** never treat proximity as causation
- **Gate 3:** expanded through 2025 Seller Center launch and KPPU notification fine

### structural_break (SUPPORTING — Gate 3)

- **Grain:** year × entity × metric × data_type
- **Entities:** Legacy Tokopedia · TikTok Shop Indonesia · Combined Tokopedia + TikTok Shop · Shopee · Indonesia market
- **Key fields:** `value`, `data_type` (`SECONDARY_ESTIMATE` / `DERIVED` / `UNKNOWN`), `formula_or_basis`, `confidence`
- **Rule:** Combined 2025 share/GMV is **not** Legacy Tokopedia; residual Legacy 2025 GMV is DERIVED/LOW confidence; UNKNOWN standalone share kept null
- **Paths:** `data/raw/structural_break/` → `data/processed/structural_break/`

### entity_split (SUPPORTING — Gate 3B)

- **Grain:** year × entity × metric
- **File:** `entity_split_2024_2025.csv` → `entity_split_2024_2025_processed.csv`
- **Key fields:** `value`, `source_type` (`PRIMARY` / `SECONDARY_HIGH` / `SECONDARY` / `DERIVED` / `UNKNOWN`), `comparability` (`DIRECT` / `CONDITIONAL` / `NOT COMPARABLE`), `confidence`, `evidence_note`
- **Includes:** MW GMV/share (secondary), APJII access shares (not GMV), GoTo combined fee, Magpie FMCG tracked context, timeline flags
- **Rule:** no fabricated Legacy Tokopedia 2025 GMV/share; residual Combined−TTS not stored as observed

### company_context (SUPPORTING)

- Combines Sea Limited and GoTo curated official/public metrics
- **NOT COMPARABLE** to Indonesia platform market-share series
- Sea metrics are multi-country unless explicitly Indonesia
- GoTo Core GTV excludes Tokopedia after 2024-01-31 deconsolidation; service fee ≠ GMV

### macro (SUPPORTING)

- World Bank Indonesia indicators (GDP, growth, household consumption share, inflation, internet users)
- Context only; not platform share

## Machine-readable dictionary

See `data/metadata/data_dictionary.csv`.
