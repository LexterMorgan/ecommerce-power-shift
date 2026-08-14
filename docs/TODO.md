# TODO — Milestone Roadmap

Project: **E-Commerce Power Shift: Shopee vs Tokopedia in Indonesia**

Primary research question: How did Shopee's competitive position in Indonesia change relative to Tokopedia, and what observable market factors help explain that shift?

Status legend: `[ ]` pending · `[x]` complete · `[~]` optional / external / deferred

**Current status:** Analytical pipeline, analysis-ready panel, PostgreSQL/SQL layer, static React dashboard, Gate 9 validation, and Gate 10 production-readiness checks are **complete**. Remaining items are optional enhancements (e.g. Google Trends ingest, primary MW matrix) or manual external steps (Vercel connect, screenshots). Do **not** treat this roadmap as blocked before SQL/dashboard — those gates are already done.

---

## Gate 0 — Project Foundation

- [x] Project documentation structure
- [x] Architecture definition
- [x] Research methodology framework
- [x] Data-source framework
- [x] Cursor agent framework

---

## Gate 1 — Data Availability Audit

- [x] Investigate market-share / GMV data
- [x] Investigate Google Trends
- [x] Investigate company financial/business metrics
- [x] Investigate traffic / engagement data
- [x] Investigate government data
- [x] Investigate academic / industry research
- [x] Document source availability
- [x] Document source limitations

Deliverables: `docs/DATA_SOURCES.md`, `docs/DATA_AVAILABILITY.md`, `research/source_audit.md`

---

## Gate 2 — Data Acquisition

- [x] Acquire verified sources (market_position, events, company_context, macro)
- [x] Preserve raw files
- [x] Record provenance
- [x] Record access dates
- [x] Record granularity
- [~] Google Trends automated acquisition blocked (manual export pending; optional enhancement)
- [x] Python cleaning + validation pipeline
- [x] Data dictionary / inventory / quality docs
- [x] Final Gate 2 audit (`research/data_quality_validation_report.md`)

Status: **READY WITH DOCUMENTED LIMITATIONS** — Gate 2 closed for review. Gate 3 structural-break investigation completed separately (see Gate 3 section).

---

## Gate 3 — Structural Break & Tokopedia Comeback Investigation

Pipeline cleaning/validation (from Gate 2) plus Gate 3 research:

- [x] Define schemas (initial; documented in data dictionary)
- [x] Clean datasets (initial pipeline)
- [x] Validate data (initial automated report)
- [x] Produce processed datasets
- [x] Add tests / validation module
- [x] Verify TikTok–Tokopedia regulatory/transaction timeline from authoritative sources
- [x] Establish 2024 baseline with entity split (Shopee / Legacy Tokopedia / TTS)
- [x] Document 2025 structural break (Combined ≠ Legacy Tokopedia)
- [x] Build evidence matrix for H1/H2/H3 (`research/tokopedia_comeback_evidence_matrix.md`)
- [x] Build timeline (`research/tiktok_tokopedia_timeline.md`)
- [x] Document 2025 data requirements (`research/2025_data_requirements.md`)
- [x] Preliminary findings — not final conclusion (`research/tokopedia_comeback_preliminary_findings.md`)
- [x] Expand competitive events + structural_break dataset through pipeline
- [ ] Optional: ingest manual Google Trends CSV and re-validate
- [ ] Optional: acquire primary Momentum Works entity-split table

Status: **PRELIMINARY EVIDENCE COMPLETE** — H3 currently best supported among three; Legacy Tokopedia standalone recovery remains UNKNOWN. No SQL/dashboard yet.

### Gate 3B — Entity-level 2024–2025 acquisition

- [x] Acquire traceable entity-split evidence CSV
- [x] Process + validate `entity_split_2024_2025`
- [x] Document APJII access ≠ GMV; reject residual as observed
- [x] Write `research/entity_level_evidence_2024_2025.md`
- [x] Write `research/tokopedia_comeback_evidence.md`
- [x] Write `research/source_registry.md`
- [x] Update `data/raw/structural_break/PROVENANCE.md`
- [x] Smoke tests for entity split / no fabricated Legacy 2025 GMV
- [ ] Optional: primary paid MW entity-split matrix
- [ ] Optional: manual Google Trends CSV

Status: **ENTITY-SPLIT DEFENSIBLE WITH DOCUMENTED GAPS** — standalone Legacy Tokopedia 2025 GMV/share still MISSING; not fully ready for final causal attribution analysis.

---

## Gate 4 — Exploratory Analysis

- [x] Analyze 2024→2025 structural break with entity discipline
- [x] Test H1 Legacy Tokopedia comeback (`research/tokopedia_comeback_final_test.md`)
- [x] Test H2 hybrid / H3 TikTok-led
- [x] Write `research/gate4_2025_structural_analysis.md`
- [x] Write `research/2025_end_state.md`
- [x] Produce `data/processed/gate4_entity_analysis.csv`
- [x] Update PROVENANCE + source_registry for Gate 4 consumption
- [ ] Optional: analyze Google Trends if/when manual CSV ingested
- [ ] Optional: deeper competitive-gap charts (still no SQL/dashboard)

Status: **EXPLORATORY COMPLETE WITH DOCUMENTED LIMITATIONS**  
Verdicts: H1 **UNSUPPORTED** · H2 **PARTIALLY SUPPORTED** (structure) · H3 **PARTIALLY SUPPORTED** (strongest).  
Legacy Tokopedia 2025 standalone GMV/share remains **MISSING**. No SQL/dashboard.
---

## Gate 5 — Competitive Analysis

- [x] Compare Shopee vs Legacy Tokopedia vs TTS vs Combined (entity-separated)
- [x] Investigate potential drivers with claim labels
- [x] Separate evidence from interpretation
- [x] Document limitations / unknowns
- [x] Write `research/gate5_competitive_analysis.md`
- [x] Write `research/2025_competitive_end_state.md`
- [x] Write `research/hypothesis_evidence_matrix.md`
- [x] Produce `data/processed/gate5_competitive_analysis.csv`
- [x] Update PROVENANCE + source_registry

Status: **COMPETITIVE ANALYSIS COMPLETE WITH DOCUMENTED GAPS**  
H1 **UNSUPPORTED** · H2 **PARTIALLY SUPPORTED** (structure) · H3 **PARTIALLY SUPPORTED** (strongest).  
No SQL/dashboard. Legacy Tokopedia 2025 GMV/share still MISSING.

### Gate 5.5 — Final 2025 comparable data search

- [x] Final Tier 1–3 search for 2025 platform metrics
- [x] Explicit search for standalone Legacy Tokopedia 2025 GMV/share
- [x] Create `data/raw/2025_comparable/platform_metrics_2025.csv`
- [x] Create processed mirror + PROVENANCE
- [x] Write `research/final_2025_data_search.md`
- [x] Update source_registry
- [x] Confirm STOP on Legacy Tokopedia 2025 GMV reconstruction

Status: **COMPLETE** — Legacy Tokopedia 2025 GMV/share remains **UNKNOWN**. Strongest DIRECT comparable = Shopee MW share series. Ready for Gate 6 **only with structural-break-aware scenarios**; still no SQL/dashboard.

---

## Gate 6 — Forecasting / Competitive Evolution & Scenarios

- [x] Phase 1: 2022–2024 competitive baseline (`research/gate6_competitive_evolution.md`)
- [x] Phase 2: Strategic rationale Tokopedia + TTS (`research/strategic_rationale_tokopedia_tiktok.md`)
- [x] Phase 3: 2025 Shopee vs Combined comparison (not Legacy)
- [x] Business interpretation of Combined challenger vs Shopee
- [x] Structural-break-aware scenarios A/B/C (`research/gate6_scenario_framework.md`)
- [x] Scenario inputs/outputs CSVs
- [x] Update source_registry
- [ ] Optional: quantitative forecast model only if methodology defensible without fabricating Legacy 2025

Status: **COMPLETE WITH STRUCTURAL-BREAK DISCIPLINE**  
Scenarios are directional bands (SCENARIO), not observed forecasts. Legacy Tokopedia 2025 GMV/share remains UNKNOWN. No SQL/dashboard.

### Gate — Data lineage & reproducible preparation

- [x] Audit raw → processed → analysis pipeline
- [x] Document `research/data_lineage_and_preparation.md`
- [x] Document `research/data_pipeline.md`
- [x] Document `research/data_dictionary.md` (Gates 5–6 fields)
- [x] Add `python/prepare_analysis_ready.py` + `scripts/prepare_analysis_ready.py`
- [x] Analysis-ready validation + smoke tests
- [x] Confirm historical data unchanged; Gate 6 conclusions untouched

Status: **COMPLETE** — lineage/portfolio data-prep demonstrable. Still no SQL/dashboard.

---

## Gate 7A — Analysis / Visualization Layer

- [x] Inspect analysis-ready panel + supporting processed files
- [x] Build reproducible `analysis/` load + charts + runner
- [x] Plot OBSERVED/DERIVED only; never UNKNOWN→0
- [x] Keep 2022–2024 standalone separate from 2025 Combined
- [x] Preserve value_status / comparability / provenance in table exports
- [x] Portfolio charts with structural-break labeling
- [x] Smoke tests (`tests/test_gate7a_analysis_smoke.py`)
- [x] Methodology (`research/gate7a_analysis_methodology.md`)
- [x] Confirm Gates 1–6 conclusions and historical values untouched

Status: **COMPLETE** — static analysis outputs under `analysis/outputs/`. Still no SQL/React dashboard.

---

## Gate 7B — SQL / Dashboard Data Layer

- [x] Inspect Gate 7A outputs + canonical processed inputs
- [x] Define SQL schema/tables/views (`sql/schema.sql`) — **PostgreSQL canonical**
- [x] Build PostgreSQL DB + JSON payload + CSV view exports
- [x] Deprecate/remove SQLite artifact (`data/dashboard/SQLITE_DEPRECATED.md`)
- [x] Preserve OBSERVED/DERIVED/UNKNOWN; never UNKNOWN→0
- [x] Keep 2022–2024 standalone separate from 2025 Combined
- [x] Preserve provenance metadata columns
- [x] Support filters: year / marketplace / metric / value_status / comparability
- [x] Smoke tests (`tests/test_gate7b_dashboard_sql_smoke.py`)
- [x] Schema docs (`research/gate7b_dashboard_sql_schema.md`)
- [x] Confirm Gates 1–6 and Gate 7A methodology untouched

Status: **COMPLETE** — dashboard-ready PostgreSQL + JSON under `data/dashboard/`. Gate 8 React not started.

---

## Gate 7 — Dashboard Data Layer

- [x] Define dashboard schema
- [x] Generate dashboard payload
- [x] Validate metrics
- [x] Add tests

Note: Gate 7 checklist completed via Gate 7B. Presentation UI remains Gate 8.

---

## Gate 8 — Frontend (+ historical API layer)

- [x] Initialize React + TypeScript application (`frontend/`)
- [x] Build FastAPI read-only layer over Gate 7B PostgreSQL (`api/`) — **later removed from public path in Gate 10B**
- [x] Build dashboard shell + executive overview
- [x] Build competitive comparison (standalone vs post-break)
- [x] Build supporting evidence (access / TTS / GMV)
- [x] Build scenario section (SCENARIO-labeled)
- [x] Build data explorer with Gate 7B filters
- [x] Add responsive UI
- [x] Frontend smoke tests (API smoke tests removed with Gate 10B)
- [x] Architecture docs (`research/gate8_dashboard_architecture.md`)
- [~] Event timeline / driver analysis — **not fabricated**; outside Gate 7B dashboard views
- [~] Forecasting UI — covered by Gate 6 scenario bands only (no invented forecasts)

Status: **COMPLETE** — React UI retained. Public runtime is **static JSON** (Gate 10B); FastAPI is not part of the deployed architecture.

---

## Gate 9 — Validation

- [x] Test data transformations (panel schema / row counts)
- [x] Validate analytical metrics (locked shares + UNKNOWN nulls)
- [x] Validate dashboard metrics (manifest, share-gap, static snapshot + optional PostgreSQL parity)
- [x] Review analytical claims (Gate 5/6/8 claim-discipline phrases retained)
- [x] Review source provenance (OBSERVED citations present)
- [x] Write `research/gate9_validation_report.md` + `data/metadata/gate9_validation_results.json`
- [x] Smoke tests (`tests/test_gate9_validation_smoke.py`)

Status: **COMPLETE** — validation PASS. No metric/schema changes.

---

## Gate 10 — Documentation & Deployment

- [x] Portfolio-ready README
- [x] Document methodology / architecture pointers (Gates 7B–9 + production topology)
- [x] Document data-source / findings links without inventing new claims
- [x] Screenshot capture instructions (`docs/screenshots/README.md`) — images are manual
- [x] **Gate 10B:** public dashboard converted to static analysis-ready JSON (no FastAPI/public Postgres)
- [x] Static export (`scripts/export_dashboard_data.py` → `frontend/public/data/dashboard_data.json`)
- [x] Data contract (`research/dashboard_data_contract.md`)
- [x] Production-readiness check updated for static deploy
- [x] **Gate 10C:** final static-deployment audit (stale API/deploy refs cleaned; tests/build verified)
- [~] Live Vercel project connect — **manual external account**
- [~] Real screenshot assets — **manual after site is reachable**

Status: **COMPLETE (repo-ready, static public architecture)** — Vercel account linking remains manual. **READY TO PUSH** pending human commit.

---

## Operating rule

Gates 0–10 (repo scope) are complete. Prefer optional backlog items only when they improve evidence quality without inventing metrics. After any change, run tests/validation before claiming completion.
