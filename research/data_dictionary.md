# Data Dictionary — Analysis Fields (Gates 5–6)

Portfolio-focused dictionary for fields actually used in competitive analysis and scenarios.  
Full technical companion: `docs/DATA_DICTIONARY.md` / `data/metadata/data_dictionary.csv`.

**Status vocabulary:** OBSERVED · DERIVED · SCENARIO · UNKNOWN

---

## Competitive panel (`data/processed/analysis_ready/competitive_panel.csv`)

| Field | Definition | Unit | Source | Transformation | Status | Years | Caveats |
|-------|------------|------|--------|----------------|--------|-------|---------|
| year | Calendar year of metric | year | Upstream market_position | numeric | — | 2020, 2022–2025 | 2021 absent |
| analytical_entity | Analysis entity name | text | Mapped from platform | Tokopedia→Legacy Tokopedia; combined→Combined Tokopedia + TikTok Shop | — | all | Do not collapse Combined into Legacy |
| source_platform | Platform string in market_position | text | Raw/processed MP | canonicalize | — | all | |
| entity_type | standalone / combined / combined_derived | text | market_position + prepare | lowercased; derived additive flagged | — | all | combined = structural break |
| metric | `market_share_pct` or `gmv_estimate_usd_billion` | text | market_position | long-form melt-style rows | — | all | |
| value | Metric value | % or USD bn | MW secondary | numeric; NA kept | OBSERVED / DERIVED / UNKNOWN | varies | UNKNOWN must stay null |
| unit | percent / USD_billions | text | assigned in prepare | — | — | all | |
| phase | Analytical phase label | text | Gate 6 story | assigned in prepare | — | all | phase1 vs phase3 |
| value_status | Evidence class | text | rules in prepare | OBSERVED/DERIVED/UNKNOWN | — | all | SCENARIO lives in gate6 outputs |
| comparability | DIRECT / CONDITIONAL / NOT COMPARABLE | text | Gate 5.5 rules | Combined 2025→NOT COMPARABLE vs Legacy | — | all | |
| source_publisher | Citation publisher | text | market_position | passthrough | — | all | |
| citation_url | Traceable URL | URL | market_position / docs | passthrough | — | all | |
| confidence | HIGH/MEDIUM/LOW | text | market_position | uppercased upstream | — | all | |
| notes | Caveats | text | prepare | — | — | all | |

### Key metric instances

| analytical_entity | metric | Example | Status | Years | Caveats |
|-------------------|--------|--------:|--------|-------|---------|
| Shopee | market_share_pct | 36→40→46→54 | OBSERVED | 2022–2025 | DIRECT within MW secondary family |
| Legacy Tokopedia | market_share_pct | 35→30→23 | OBSERVED | 2022–2024 | No 2025 fill |
| Legacy Tokopedia | market_share_pct | null | UNKNOWN | 2025 | Keep missing |
| Combined Tokopedia + TikTok Shop | market_share_pct | 38 | OBSERVED | 2025 | NOT Legacy Tokopedia |
| Combined Tokopedia + TikTok Shop | market_share_pct | 34 | DERIVED | 2024 | 23+11 additive baseline |
| Shopee | gmv_estimate_usd_billion | 26→31.2 | OBSERVED | 2024–2025 | Secondary estimate |
| Combined Tokopedia + TikTok Shop | gmv_estimate_usd_billion | 21.9 | OBSERVED | 2025 | Combined only |

---

## Gate 6 scenario inputs (`gate6_scenario_inputs.csv`)

| Field | Definition | Unit | Status usage | Caveats |
|-------|------------|------|--------------|---------|
| input_id | Stable ID | text | — | |
| phase | phase1_baseline / phase3_2025 | text | — | Matches Gate 6 phases |
| entity | Entity including Combined / Legacy | text | — | |
| metric | Share, GMV, gap, access | text | — | Access ≠ GMV |
| year | Year | year | — | |
| value | Starting evidence | varies | OBSERVED/DERIVED/UNKNOWN | Legacy 2025 null |
| value_type | Evidence class | text | OBSERVED/DERIVED/UNKNOWN | |
| comparability | DIRECT/CONDITIONAL/NOT COMPARABLE | text | — | |

---

## Gate 6 scenario outputs (`gate6_scenario_outputs.csv`)

| Field | Definition | Unit | Status | Caveats |
|-------|------------|------|--------|---------|
| scenario_id | A / B / C / ALL | text | — | ALL = shared UNKNOWN constraint |
| scenario_name | Human label | text | — | |
| metric | e.g. share gap band | text | — | |
| base_2025_value | Observed/derived start | varies | from inputs | 16 pp gap DERIVED from OBSERVED |
| scenario_low / scenario_high | Illustrative band | pp or label | **SCENARIO** | Not forecasts-as-fact |
| value_type | SCENARIO or UNKNOWN | text | — | Never write SCENARIO into OBSERVED history |
| direction | stable_to_wider / narrows / widens | text | SCENARIO | |

---

## Supporting metrics (not in competitive_panel)

| Field / metric | Definition | Status | Caveats |
|----------------|------------|--------|---------|
| TTS Indonesia GMV ~$13.1B | TTS-labeled GMV | OBSERVED | CONDITIONAL vs Combined; in 2025_comparable |
| APJII access shares | % internet users accessing platform | OBSERVED | ≠ GMV share |
| GoTo ecommerce service fee | IDR fee on combined GMV | OBSERVED | ≠ platform GMV |
| Indonesia total GMV | MW Indonesia total | OBSERVED | DIRECT vs 2024 total |

---

## Explicit non-fields

These must **not** appear as OBSERVED Legacy Tokopedia 2025 values:

- Combined − TTS residual GMV  
- APJII Tokopedia access relabeled as GMV share  
- Zero-filled missing shares
