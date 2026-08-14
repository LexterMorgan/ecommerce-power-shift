# Data Pipeline (Portfolio View)

**Purpose:** Show how evidence becomes analysis-ready data in this repository.

```
RAW SOURCES
  (Momentum Works via press, GoTo/TikTok PR, APJII via Kompas, World Bank, …)
        ↓
SOURCE / PROVENANCE REGISTRY
  research/source_registry.md
  data/raw/**/PROVENANCE.md
  data/metadata/source_registry.csv
        ↓
RAW DATA  (immutable)
  data/raw/market_position/
  data/raw/events/
  data/raw/structural_break/
  data/raw/2025_comparable/
  data/raw/sea/  data/raw/goto/  data/raw/macro/
  data/raw/google_trends/   ← BLOCKED (no CSV)
        ↓
DATA INSPECTION
  python/ingestion/load_raw.py
  validators (required columns, dtypes)
        ↓
CLEANING + STANDARDIZATION
  python/cleaning/clean.py
  • platform canonicalize
  • numeric/date coercion
  • KEEP missing as NA (no fabrication)
        ↓
TRANSFORM / DERIVED METRICS
  • entity_type standalone vs combined
  • DERIVED additive Combined 2024 (23+11) — labeled
  • Gate 4–6 curated claim/scenario tables
  • python/prepare_analysis_ready.py phase labels
        ↓
VALIDATION
  python/validation/validate.py
  prepare_analysis_ready validate_competitive_panel()
  tests/test_gate2_smoke.py
        ↓
PROCESSED / ANALYSIS-READY
  data/processed/market_position/…          ← historical + 2025 Combined
  data/processed/structural_break/…
  data/processed/2025_comparable/…
  data/processed/gate5_competitive_analysis.csv
  data/processed/gate6_scenario_*.csv
  data/processed/analysis_ready/competitive_panel.csv  ← unified panel
        ↓
GATE 5–6 ANALYSIS
  research/gate5_*.md
  research/gate6_*.md
        ↓
BUSINESS INSIGHTS / SCENARIOS
  Shopee leadership · Combined challenger · Legacy 2025 UNKNOWN
  Scenario A/B/C bands (SCENARIO — not OBSERVED)
```

## Structural break in the pipeline

```
2022 ── 2023 ── 2024                │  2025
standalone Shopee vs                │  Shopee DIRECT
Legacy Tokopedia                    │  vs Combined Tokopedia+TTS
(phase1_historical_standalone)      │  (phase3_post_break)
                                    │
                                    │  Legacy Tokopedia GMV/share
                                    │  = UNKNOWN (null, not zero)
```

**Do not draw a continuous Legacy Tokopedia GMV/share line through 2025.**

## Commands

```bash
python3 scripts/process_data.py
python3 scripts/prepare_analysis_ready.py
```
