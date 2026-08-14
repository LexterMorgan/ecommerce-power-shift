-- Gate 7B — Dashboard SQL schema (PostgreSQL — canonical)
-- Consumes existing analysis-ready / processed outputs only.
-- Does NOT invent business metrics or fill UNKNOWN as zero.
-- Regenerate via: python3 scripts/build_dashboard_sql.py
--
-- SQLite is deprecated for this project. Do not treat any *.db file as canonical.

-- ---------------------------------------------------------------------------
-- Base tables (loaded from CSV; schema matches source columns)
-- ---------------------------------------------------------------------------

DROP VIEW IF EXISTS v_dashboard_filter_keys CASCADE;
DROP VIEW IF EXISTS v_share_gap_summary CASCADE;
DROP VIEW IF EXISTS v_scenario_gap_bands CASCADE;
DROP VIEW IF EXISTS v_tts_labeled_gmv CASCADE;
DROP VIEW IF EXISTS v_access_metrics CASCADE;
DROP VIEW IF EXISTS v_gmv_estimates CASCADE;
DROP VIEW IF EXISTS v_legacy_tokopedia_unknown_2025 CASCADE;
DROP VIEW IF EXISTS v_market_share_post_break_2025 CASCADE;
DROP VIEW IF EXISTS v_market_share_standalone_2022_2024 CASCADE;
DROP VIEW IF EXISTS v_market_share_plottable CASCADE;
DROP VIEW IF EXISTS v_competitive_panel_all CASCADE;

DROP TABLE IF EXISTS fact_share_gap_summary CASCADE;
DROP TABLE IF EXISTS fact_scenario_outputs CASCADE;
DROP TABLE IF EXISTS fact_scenario_inputs CASCADE;
DROP TABLE IF EXISTS fact_supporting_2025 CASCADE;
DROP TABLE IF EXISTS fact_competitive_panel CASCADE;
DROP TABLE IF EXISTS dashboard_build_meta CASCADE;

CREATE TABLE dashboard_build_meta (
    build_id TEXT PRIMARY KEY,
    built_at_utc TEXT NOT NULL,
    gate TEXT NOT NULL,
    notes TEXT
);

CREATE TABLE fact_competitive_panel (
    year INTEGER,
    analytical_entity TEXT NOT NULL,
    source_platform TEXT,
    entity_type TEXT,
    metric TEXT NOT NULL,
    value DOUBLE PRECISION,         -- NULL allowed (UNKNOWN must stay NULL)
    unit TEXT,
    phase TEXT,
    value_status TEXT NOT NULL,     -- OBSERVED | DERIVED | UNKNOWN
    comparability TEXT,
    source_publisher TEXT,
    citation_url TEXT,
    confidence TEXT,
    notes TEXT
);

CREATE TABLE fact_supporting_2025 (
    year INTEGER,
    entity TEXT NOT NULL,
    metric TEXT NOT NULL,
    value DOUBLE PRECISION,         -- NULL allowed
    unit TEXT,
    market_share DOUBLE PRECISION,
    geography TEXT,
    period TEXT,
    source TEXT,
    source_url TEXT,
    source_date TEXT,
    source_type TEXT,
    methodology TEXT,
    comparability TEXT,
    confidence TEXT,
    evidence_type TEXT NOT NULL,    -- OBSERVED | UNKNOWN (and peers)
    notes TEXT
);

CREATE TABLE fact_scenario_inputs (
    input_id TEXT,
    phase TEXT,
    entity TEXT,
    metric TEXT,
    year INTEGER,
    value DOUBLE PRECISION,         -- NULL allowed for UNKNOWN
    unit TEXT,
    value_type TEXT,
    comparability TEXT,
    source TEXT,
    notes TEXT
);

CREATE TABLE fact_scenario_outputs (
    scenario_id TEXT,
    scenario_name TEXT,
    metric TEXT,
    unit TEXT,
    base_2025_value TEXT,           -- numeric or entity label as text
    scenario_low TEXT,
    scenario_high TEXT,
    value_type TEXT,                -- SCENARIO | UNKNOWN
    direction TEXT,
    mechanism TEXT,
    key_risk TEXT,
    notes TEXT
);

-- Gate 7A presentation extract (not a new metric definition)
CREATE TABLE fact_share_gap_summary (
    panel TEXT,
    year INTEGER,
    shopee_share_pct DOUBLE PRECISION,
    challenger_entity TEXT,
    challenger_share_pct DOUBLE PRECISION,
    gap_pp DOUBLE PRECISION,
    value_status TEXT,
    comparability TEXT,
    shopee_source TEXT,
    challenger_source TEXT,
    confidence TEXT,
    notes TEXT
);

-- ---------------------------------------------------------------------------
-- Views for dashboard consumption (no continuous merge across break)
-- ---------------------------------------------------------------------------

CREATE VIEW v_competitive_panel_all AS
SELECT * FROM fact_competitive_panel;

-- Plottable GMV/share only: OBSERVED/DERIVED with non-null value
CREATE VIEW v_market_share_plottable AS
SELECT *
FROM fact_competitive_panel
WHERE metric = 'market_share_pct'
  AND value_status IN ('OBSERVED', 'DERIVED')
  AND value IS NOT NULL;

CREATE VIEW v_gmv_estimates AS
SELECT *
FROM fact_competitive_panel
WHERE metric = 'gmv_estimate_usd_billion'
  AND value_status IN ('OBSERVED', 'DERIVED')
  AND value IS NOT NULL;

-- Phase 1: 2022–2024 standalone Shopee vs Legacy Tokopedia
CREATE VIEW v_market_share_standalone_2022_2024 AS
SELECT *
FROM fact_competitive_panel
WHERE year BETWEEN 2022 AND 2024
  AND metric = 'market_share_pct'
  AND analytical_entity IN ('Shopee', 'Legacy Tokopedia')
  AND entity_type = 'standalone'
  AND value_status = 'OBSERVED'
  AND value IS NOT NULL;

-- Phase 3: 2025 post-break Shopee vs Combined (NOT Legacy)
CREATE VIEW v_market_share_post_break_2025 AS
SELECT *
FROM fact_competitive_panel
WHERE year = 2025
  AND metric = 'market_share_pct'
  AND value_status = 'OBSERVED'
  AND value IS NOT NULL
  AND (
        analytical_entity = 'Shopee'
     OR (analytical_entity = 'Combined Tokopedia + TikTok Shop'
         AND entity_type = 'combined')
  );

CREATE VIEW v_legacy_tokopedia_unknown_2025 AS
SELECT *
FROM fact_competitive_panel
WHERE year = 2025
  AND analytical_entity = 'Legacy Tokopedia'
  AND value_status = 'UNKNOWN';

CREATE VIEW v_access_metrics AS
SELECT *
FROM fact_supporting_2025
WHERE metric = 'internet_user_access_share_pct'
  AND evidence_type = 'OBSERVED'
  AND value IS NOT NULL;

CREATE VIEW v_tts_labeled_gmv AS
SELECT *
FROM fact_supporting_2025
WHERE entity = 'TikTok Shop Indonesia'
  AND metric = 'gmv_estimate_usd'
  AND evidence_type = 'OBSERVED'
  AND value IS NOT NULL;

CREATE VIEW v_scenario_gap_bands AS
SELECT *
FROM fact_scenario_outputs
WHERE metric = 'shopee_minus_combined_share_gap_pp'
  AND value_type = 'SCENARIO';

CREATE VIEW v_share_gap_summary AS
SELECT * FROM fact_share_gap_summary;

-- Distinct keys to support dashboard filters (no invented series)
CREATE VIEW v_dashboard_filter_keys AS
SELECT DISTINCT
    year,
    analytical_entity AS marketplace,
    metric,
    value_status,
    comparability,
    entity_type,
    phase
FROM fact_competitive_panel;
