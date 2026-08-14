# Source Registry — Gate 3B Entity Split

Companion to `data/metadata/source_registry.csv` (pipeline-generated). This file documents sources used specifically for 2024–2025 entity-level acquisition.

| source_id | source_name | organization | url | source_type | datasets | access_method | access_date | reliability | notes |
|-----------|-------------|--------------|-----|-------------|----------|---------------|-------------|-------------|-------|
| SRC-MW-LOWDOWN-2026 | Ecommerce SEA 2026 public note | Momentum Works | https://thelowdown.momentum.asia/new-report-southeast-asias-platform-ecommerce-reaches-us157-6b-in-2025-with-top-platforms-expanding-share-to-98-8/ | PRIMARY (public excerpt) | structural_break | public webpage | 2026-08-12 | HIGH for qualitative; MEDIUM for reproduced stats | Tokopedia GMV rationalisation; Combined vs Shopee SEA 65.7%; SEA $157.6B |
| SRC-MW-BISNIS-2026 | Indonesia share table via Bisnis | Momentum Works via Bisnis.com | https://teknologi.bisnis.com/read/20260508/266/1972413/shopee-kuasai-54-pasar-e-commerce-indonesia-transaksi-tembus-rp539-triliun | SECONDARY | market_position; structural_break | public article | 2026-08-12 | MEDIUM | 2024 split + 2025 Combined; watch SEA $45.6B labeling conflict |
| SRC-DIA-TTS-TRACKER | TikTok Shop & Shopee GMV Tracker | Digital in Asia citing MW | https://digitalinasia.com/tiktok-shop-shopee-gmv-tracker/ | SECONDARY_HIGH | structural_break | public webpage | 2026-08-12 | MEDIUM–HIGH | Separates TTS platform $45.6B from Combined-with-Tokopedia; TTS ID $13.1B |
| SRC-KOMPAS-MW-TTS | Indonesia 2nd largest TTS market | Kompas citing MW/Tabcut | https://www.kompas.id/artikel/en-indonesia-menjadi-pasar-terbesar-kedua-bagi-tiktok-shop | SECONDARY_HIGH | structural_break | public article | 2026-08-12 | MEDIUM | Corroborates TTS ID ~$13.1B |
| SRC-KOMPAS-MW-IDN | Indonesia GMV slowdown / rationalisation | Kompas citing MW CEO | https://www.kompas.id/artikel/en-e-dagang-ri-masih-terbesar-di-asia-tenggara-tapi-transaksi-tumbuh-melambat-embargo-144-pk-5 | SECONDARY_HIGH | structural_break | public article | 2026-08-12 | MEDIUM–HIGH | Quotes Jianggan Li on Tokopedia rationalisation |
| SRC-APJII-KOMPAS | APJII marketplace access 2025 | APJII via Kompas | https://tekno.kompas.com/read/2025/08/11/10230017/6-platform-toko-online-paling-banyak-diakses-di-indonesia | SECONDARY_HIGH | structural_break | public article | 2026-08-12 | MEDIUM | Access shares; ~8700 respondents; NOT GMV |
| SRC-GOTO-PR-20240131 | Transaction completion | GoTo | https://www.gotocompany.com/en/news/press/goto-and-tiktok-announce-transaction-completion-formalizing-strategic-partnership-for-indonesia | PRIMARY | events; structural_break | official PR | 2026-08-12 | HIGH | Combined under PT Tokopedia; service fee |
| SRC-TIKTOK-PAUSE | TTS Indonesia pause | TikTok Newsroom | https://newsroom.tiktok.com/in-id/informasi-terkini-dari-tiktok-shop-indonesia | PRIMARY | events | official newsroom | 2026-08-12 | HIGH | 2023-10-04 |
| SRC-TIKTOK-PARTNER | Partnership announcement | TikTok Newsroom | https://newsroom.tiktok.com/in-id/goto-dan-tiktok-sepakati-kemitraan-strategis-e-commerce-untuk-mendorong-kemajuan-umkm-indonesia | PRIMARY | events | official newsroom | 2026-08-12 | HIGH | 2023-12-11 |
| SRC-TIKTOK-SELLER | Seller Center launch | TikTok Newsroom | https://newsroom.tiktok.com/in-id/tokopedia-dan-tiktok-shop-seller-center-resmi-diluncurkan | PRIMARY | events; structural_break | official newsroom | 2026-08-12 | HIGH | 2025-06-11 |
| SRC-GOTO-FEE-KONTAN | GoTo FY2025 fee / CFO quote | GoTo via Kontan | https://investasi.kontan.co.id/news/berapa-kontribusi-cuan-tokopedia-ke-keuangan-goto-di-2025 | SECONDARY_HIGH | structural_break; company_context | public article | 2026-08-12 | HIGH for fee existence | Fee on combined GMV; Rp820B |
| SRC-GOTO-FEE-BISNIS | GoTo FY2024 fee | GoTo via Bisnis | https://market.bisnis.com/read/20250313/192/1861104/goto-kantongi-komisi-jasa-rp62187-miliar-dari-tokopedia-tiktok-shop-pada-2024 | SECONDARY_HIGH | structural_break | public article | 2026-08-12 | HIGH for fee | ~11-month 2024 fee |
| SRC-MAGPIE-TTS-2026 | FMCG tracked TTS share | Magpie IQ | https://magpieiq.com/insights/tiktok-shop-indonesia-2026/ | SECONDARY | structural_break | public insight | 2026-08-12 | MEDIUM for tracked FMCG only | Explicitly not national all-category GMV |
| SRC-MAGPIE-METHOD | Magpie methodology | Magpie IQ | https://magpieiq.com/methodology/ | PRIMARY (methodology) | structural_break | public webpage | 2026-08-12 | HIGH for method limits | SKU Terjual × price; FMCG scope |

## Not used / rejected for GMV claims

- Digivestasi-style “Tokopedia 9.6% / TTS 27.4% GMV” — matches APJII **access**, not MW GMV.
- Residual Legacy GMV = Combined − TTS — additivity not established.
- Paid Momentum Works full matrices — not acquired (no paywall bypass).
- Google Trends — still blocked/manual pending.
- Similarweb long history — not acquired.

---

## Gate 4 analysis consumption (2026-08-12)

Gate 4 exploratory analysis used the sources above without adding fabricated Legacy Tokopedia 2025 GMV/share.

| Analysis artifact | Depends on |
|-------------------|------------|
| `research/gate4_2025_structural_analysis.md` | entity_split + timeline PRIMARY sources |
| `research/tokopedia_comeback_final_test.md` | same |
| `research/2025_end_state.md` | same |
| `data/processed/gate4_entity_analysis.csv` | derived comparison table from entity_split (labeled OBSERVED/DERIVED/UNKNOWN/INFERRED) |

**No new PRIMARY numeric GMV series was acquired in Gate 4.** Verdicts: H1 UNSUPPORTED; H2 PARTIAL (structure); H3 PARTIAL (strongest).

---

## Gate 5 competitive analysis (2026-08-12)

| Analysis artifact | Depends on |
|-------------------|------------|
| `research/gate5_competitive_analysis.md` | entity_split + Gate 4 synthesis + PRIMARY timeline |
| `research/2025_competitive_end_state.md` | same |
| `research/hypothesis_evidence_matrix.md` | same |
| `data/processed/gate5_competitive_analysis.csv` | claim-level reproduction table (OBSERVED/DERIVED/INFERRED/UNKNOWN) |

**Gate 5 conclusion:** Who drove the shift — Shopee share expansion (OBSERVED) + TikTok-led Combined challenger (H3 PARTIAL); H1 Legacy comeback UNSUPPORTED. No SQL/dashboard.

---

## Gate 5.5 final 2025 comparable search (2026-08-12)

| Artifact | Path |
|----------|------|
| Search report | `research/final_2025_data_search.md` |
| Raw metrics | `data/raw/2025_comparable/platform_metrics_2025.csv` |
| Processed metrics | `data/processed/2025_comparable/platform_metrics_2025_processed.csv` |
| Provenance | `data/raw/2025_comparable/PROVENANCE.md` |

**Outcome:** Standalone Legacy Tokopedia 2025 GMV/share **NOT FOUND** → remains UNKNOWN; **STOP** further search for that metric without new primary disclosure.  
**Strongest DIRECT 2025 comparable:** Shopee MW GMV share (54%) vs 2022–2024 Shopee series.  
Gate 4/5 conclusions **not modified**.

---

## Gate 6 competitive evolution & scenarios (2026-08-12)

| Artifact | Path |
|----------|------|
| Competitive evolution | `research/gate6_competitive_evolution.md` |
| Strategic rationale | `research/strategic_rationale_tokopedia_tiktok.md` |
| Scenario framework | `research/gate6_scenario_framework.md` |
| Scenario inputs | `data/processed/gate6_scenario_inputs.csv` |
| Scenario outputs | `data/processed/gate6_scenario_outputs.csv` |

**Primary rationale sources used:** GoTo PR; TikTok Newsroom; TechCrunch/CNBC deal coverage; existing Gate 3 timeline.  
**Scenario values:** labeled SCENARIO (illustrative gap bands). No fabricated Legacy 2025 GMV/share.

---

## Data lineage & preparation (post–Gate 6)

| Artifact | Path |
|----------|------|
| Lineage / preparation | `research/data_lineage_and_preparation.md` |
| Pipeline diagram | `research/data_pipeline.md` |
| Analysis data dictionary | `research/data_dictionary.md` |
| Analysis-ready panel | `data/processed/analysis_ready/competitive_panel.csv` |
| Prepare script | `python/prepare_analysis_ready.py` |

Run: `python3 scripts/process_data.py` then `python3 scripts/prepare_analysis_ready.py`.

## Gate 7A — Analysis / visualization

| Artifact | Path |
|----------|------|
| Methodology | `research/gate7a_analysis_methodology.md` |
| Runner | `analysis/run_analysis.py` / `scripts/run_analysis.py` |
| Outputs | `analysis/outputs/` |
| Smoke tests | `tests/test_gate7a_analysis_smoke.py` |

Run: `python3 analysis/run_analysis.py` then `python3 -m pytest tests/test_gate7a_analysis_smoke.py -q`.

## Gate 7B — SQL / dashboard data layer

| Artifact | Path |
|----------|------|
| Schema / views (PostgreSQL) | `sql/schema.sql` |
| Builder | `python/build_dashboard_sql.py` / `scripts/build_dashboard_sql.py` |
| Canonical DB | PostgreSQL `ecommerce_power_shift` via `DATABASE_URL` |
| JSON payload | `data/dashboard/dashboard_payload.json` |
| CSV exports | `data/dashboard/exports/` |
| SQLite deprecation | `data/dashboard/SQLITE_DEPRECATED.md` |
| Docs | `research/gate7b_dashboard_sql_schema.md` |
| Smoke tests | `tests/test_gate7b_dashboard_sql_smoke.py` |

Run: `createdb ecommerce_power_shift` (once) → `python3 scripts/build_dashboard_sql.py` → `python3 -m pytest tests/test_gate7b_dashboard_sql_smoke.py -q`.

## Gate 8 — React dashboard (static data as of Gate 10B)

| Artifact | Path |
|----------|------|
| Architecture | `research/gate8_dashboard_architecture.md` |
| Frontend | `frontend/` |
| Static data | `frontend/public/data/dashboard_data.json` |
| Export | `scripts/export_dashboard_data.py` |

Run UI: `python3 scripts/export_dashboard_data.py && cd frontend && npm run dev`

## Gate 9 — Validation

| Artifact | Path |
|----------|------|
| Validator | `python/validation/gate9_validate.py` / `scripts/run_gate9_validation.py` |
| Report | `research/gate9_validation_report.md` |
| Results JSON | `data/metadata/gate9_validation_results.json` |
| Smoke tests | `tests/test_gate9_validation_smoke.py` |

Run: `python3 scripts/run_gate9_validation.py` then `python3 -m pytest tests/test_gate9_validation_smoke.py -q`.

## Gate 10 / 10B — Static documentation & deployment

| Artifact | Path |
|----------|------|
| Deployment docs | `research/gate10_deployment.md` |
| Data contract | `research/dashboard_data_contract.md` |
| Env template (analytical only) | `.env.example` |
| Frontend Vercel | `frontend/vercel.json` |
| Readiness check | `scripts/check_production_readiness.py` |
| Readiness JSON | `data/metadata/gate10_production_readiness.json` |
| Screenshots note | `docs/screenshots/README.md` |

Run: `python3 scripts/export_dashboard_data.py` then `python3 scripts/check_production_readiness.py`

PostgreSQL/SQL analytical layer preserved under `sql/` and `python/build_dashboard_sql.py`. Live Vercel project linking remains **manual**.
