# Gate 7A — Analysis / Visualization Methodology

**Status:** Implemented  
**Canonical GMV/share input:** `data/processed/analysis_ready/competitive_panel.csv`  
**Supporting inputs:** `data/processed/2025_comparable/platform_metrics_2025_processed.csv`, `data/processed/gate6_scenario_outputs.csv`  
**Runner:** `python analysis/run_analysis.py` or `python scripts/run_analysis.py`

## Purpose

Produce a reproducible analysis/visualization layer for the **Shopee vs Tokopedia** GMV/share story without reopening or reinterpreting Gates 1–6 conclusions.

This gate answers *how to plot and tabulate* locked findings. It does **not** invent missing Legacy Tokopedia 2025 values, convert UNKNOWN→0, or continuously join 2022–2024 Legacy Tokopedia shares to 2025 Combined shares.

## Architecture

```
data/processed/analysis_ready/competitive_panel.csv   # canonical GMV/share
data/processed/2025_comparable/...                   # APJII access, TTS-labeled GMV
data/processed/gate6_scenario_outputs.csv            # SCENARIO bands only

analysis/load.py          # filters + summary tables (never UNKNOWN→0)
analysis/charts.py        # matplotlib figures with structural-break labels
analysis/run_analysis.py  # orchestration → analysis/outputs/

analysis/outputs/tables/  # CSV extracts with provenance columns
analysis/outputs/figures/ # PNG charts
analysis/outputs/analysis_summary.json
```

Gates 1–6 research markdown and historical raw/processed market values are **read-only** for this gate.

## Plotting rules

1. **Plottable statuses:** `OBSERVED` and `DERIVED` only, and only where `value` is non-null.
2. **UNKNOWN / null:** never coerced to zero; Legacy Tokopedia 2025 GMV and share remain missing and are exported as documentation tables only.
3. **Phase separation:**
   - **Phase 1 (2022–2024):** Shopee vs **Legacy Tokopedia** (`entity_type=standalone`).
   - **Phase 3 (2025):** Shopee vs **Combined Tokopedia + TikTok Shop** (`entity_type=combined`).
4. **DERIVED Combined 2024 (23+11):** shown only as a labeled conditional baseline beside the 2025 post-break chart — not as a continuous time series glued to Legacy Tokopedia.
5. **SCENARIO** outputs are labeled `value_type=SCENARIO` and are not presented as observed history.
6. **Access ≠ GMV:** APJII internet-user access shares are a separate supporting chart.

## Outputs

| Artifact | Content |
|----------|---------|
| `tables/phase1_standalone_shares.csv` | 2022–2024 OBSERVED Shopee / Legacy shares + metadata |
| `tables/phase3_post_break_shares.csv` | 2025 OBSERVED Shopee / Combined shares + metadata |
| `tables/share_gap_summary.csv` | Gap pp by phase with comparability notes |
| `tables/legacy_tokopedia_2025_unknown.csv` | UNKNOWN rows (null values preserved) |
| `tables/supporting_apjii_access.csv` | APJII access OBSERVED |
| `tables/supporting_tts_labeled_gmv.csv` | TTS-labeled GMV OBSERVED |
| `tables/scenario_gap_bands.csv` | Gate 6 SCENARIO gap bands |
| `figures/phase1_standalone_shares.png` | Standalone dyad line chart |
| `figures/phase3_post_break_shopee_vs_combined.png` | Post-break bars + DERIVED baseline |
| `figures/structural_break_story.png` | Two-panel structural-break figure |
| `figures/supporting_apjii_access.png` | Access supporting chart |
| `figures/scenario_gap_bands.png` | Scenario gap bands |
| `analysis_summary.json` | Machine-readable run summary |

## Locked story numbers (from panel OBSERVED/DERIVED; not reinterpreted)

- 2022: Shopee 36% vs Legacy Tokopedia 35% (gap ~1 pp)
- 2024: Shopee 46% vs Legacy Tokopedia 23% (gap ~23 pp)
- 2025: Shopee 54% vs Combined 38% (gap ~16 pp)
- Legacy Tokopedia 2025 share/GMV: **UNKNOWN**
- Combined additive 2024 baseline: **34% DERIVED** (23+11), CONDITIONAL only

## Assumptions (explicit)

- `competitive_panel.csv` remains the sole canonical GMV/share series for charts in this layer.
- Secondary Momentum Works excerpts in the panel retain their upstream confidence / publisher labels; this layer does not upgrade confidence.
- Scenario bands reuse Gate 6 outputs without recalibrating mechanisms or claiming forecasts.
- Matplotlib `Agg` backend; figures are static portfolio assets, not a React dashboard (Gate 8 still pending).

## Non-claims

- No causal attribution beyond what Gates 4–6 already labeled.
- No continuous Tokopedia 23% → Combined 38% time series.
- No interpolation of annual → monthly.
- No SQL/dashboard payload generation (separate Gate 7 items remain).

## Validation

Run:

```bash
python analysis/run_analysis.py
python -m pytest tests/test_gate7a_analysis_smoke.py -q
```

Smoke checks assert: plottable extracts exclude UNKNOWN; Legacy 2025 values stay null; expected OBSERVED counts; figure/table files exist; Phase 1 and Phase 3 gaps match panel arithmetic.
