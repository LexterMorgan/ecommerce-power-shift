"""Smoke tests for Gate 7B PostgreSQL dashboard data layer."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from python.build_dashboard_sql import database_url, get_engine  # noqa: E402

PAYLOAD = ROOT / "data" / "dashboard" / "dashboard_payload.json"
MANIFEST = ROOT / "data" / "dashboard" / "manifest.json"
EXPORTS = ROOT / "data" / "dashboard" / "exports"
SCHEMA = ROOT / "sql" / "schema.sql"
PANEL = ROOT / "data" / "processed" / "analysis_ready" / "competitive_panel.csv"
SQLITE_DB = ROOT / "data" / "dashboard" / "ecommerce_power_shift.db"
SQLITE_NOTICE = ROOT / "data" / "dashboard" / "SQLITE_DEPRECATED.md"

REQUIRED_PANEL_COLS = {
    "year",
    "analytical_entity",
    "metric",
    "value",
    "value_status",
    "comparability",
    "source_publisher",
    "citation_url",
    "confidence",
}


def _ensure_built():
    subprocess.check_call(
        [sys.executable, str(ROOT / "scripts" / "build_dashboard_sql.py")],
        cwd=str(ROOT),
        env=os.environ.copy(),
    )


def test_schema_is_postgresql():
    assert SCHEMA.exists()
    text_sql = SCHEMA.read_text()
    assert "PostgreSQL" in text_sql or "postgresql" in text_sql.lower()
    assert "DOUBLE PRECISION" in text_sql
    assert "PRAGMA" not in text_sql
    assert "fact_competitive_panel" in text_sql
    assert "v_market_share_standalone_2022_2024" in text_sql
    assert "v_market_share_post_break_2025" in text_sql


def test_sqlite_artifact_deprecated():
    _ensure_built()
    assert not SQLITE_DB.exists(), "Legacy SQLite DB must not remain as canonical"
    assert SQLITE_NOTICE.exists()
    notice = SQLITE_NOTICE.read_text()
    assert "deprecated" in notice.lower()
    assert "PostgreSQL" in notice


def test_build_outputs_exist():
    _ensure_built()
    assert PAYLOAD.exists()
    assert MANIFEST.exists()
    manifest = json.loads(MANIFEST.read_text())
    assert manifest["database_engine"] == "postgresql"
    assert "postgresql://" in manifest["database"]
    assert (EXPORTS / "v_market_share_standalone_2022_2024.csv").exists()
    assert (EXPORTS / "v_market_share_post_break_2025.csv").exists()
    assert (EXPORTS / "v_legacy_tokopedia_unknown_2025.csv").exists()


def test_panel_row_count_matches_csv():
    _ensure_built()
    csv_n = len(pd.read_csv(PANEL))
    engine = get_engine()
    with engine.connect() as conn:
        db_n = conn.execute(text("SELECT COUNT(*) FROM fact_competitive_panel")).scalar_one()
    assert db_n == csv_n == 22
    entities = set(pd.read_csv(PANEL)["analytical_entity"])
    assert entities <= {
        "Shopee",
        "Legacy Tokopedia",
        "TikTok Shop",
        "Combined Tokopedia + TikTok Shop",
    }
    assert not entities & {"Bukalapak", "Lazada", "Blibli"}


def test_required_columns_present():
    _ensure_built()
    engine = get_engine()
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_schema = 'public'
                  AND table_name = 'fact_competitive_panel'
                """
            )
        ).fetchall()
    cols = {r[0] for r in rows}
    assert REQUIRED_PANEL_COLS.issubset(cols)


def test_unknown_never_zero_in_db():
    _ensure_built()
    engine = get_engine()
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                """
                SELECT analytical_entity, metric, value, value_status
                FROM fact_competitive_panel
                WHERE value_status = 'UNKNOWN'
                """
            )
        ).fetchall()
        assert len(rows) >= 2
        for _, _, value, status in rows:
            assert status == "UNKNOWN"
            assert value is None
        zeroed = conn.execute(
            text(
                """
                SELECT COUNT(*) FROM fact_competitive_panel
                WHERE value_status = 'UNKNOWN' AND value = 0
                """
            )
        ).scalar_one()
        assert zeroed == 0


def test_structural_break_views_separated():
    _ensure_built()
    engine = get_engine()
    standalone = pd.read_sql_query(
        text("SELECT * FROM v_market_share_standalone_2022_2024"), engine
    )
    post = pd.read_sql_query(
        text("SELECT * FROM v_market_share_post_break_2025"), engine
    )

    assert len(standalone) == 6
    assert set(standalone["year"]) == {2022, 2023, 2024}
    assert set(standalone["analytical_entity"]) == {"Shopee", "Legacy Tokopedia"}
    assert "Combined" not in " ".join(standalone["analytical_entity"])

    assert len(post) == 2
    assert set(post["analytical_entity"]) == {
        "Shopee",
        "Combined Tokopedia + TikTok Shop",
    }
    assert "Legacy Tokopedia" not in set(post["analytical_entity"])


def test_locked_historical_values():
    _ensure_built()
    engine = get_engine()

    def share(year, entity):
        with engine.connect() as conn:
            return conn.execute(
                text(
                    """
                    SELECT value FROM fact_competitive_panel
                    WHERE year = :year AND analytical_entity = :entity
                      AND metric = 'market_share_pct'
                      AND value_status IN ('OBSERVED', 'DERIVED')
                    """
                ),
                {"year": year, "entity": entity},
            ).scalar_one()

    assert float(share(2022, "Shopee")) == 36.0
    assert float(share(2022, "Legacy Tokopedia")) == 35.0
    assert float(share(2024, "Shopee")) == 46.0
    assert float(share(2024, "Legacy Tokopedia")) == 23.0
    assert float(share(2025, "Shopee")) == 54.0
    assert float(share(2025, "Combined Tokopedia + TikTok Shop")) == 38.0
    assert float(share(2024, "Combined Tokopedia + TikTok Shop")) == 34.0


def test_supporting_and_scenario_views():
    _ensure_built()
    engine = get_engine()
    with engine.connect() as conn:
        access_n = conn.execute(text("SELECT COUNT(*) FROM v_access_metrics")).scalar_one()
        tts_n = conn.execute(text("SELECT COUNT(*) FROM v_tts_labeled_gmv")).scalar_one()
        scen_n = conn.execute(text("SELECT COUNT(*) FROM v_scenario_gap_bands")).scalar_one()
        filt_n = conn.execute(
            text("SELECT COUNT(*) FROM v_dashboard_filter_keys")
        ).scalar_one()
    assert access_n >= 3
    assert tts_n == 1
    assert scen_n == 3
    assert filt_n >= 10


def test_payload_preserves_unknown_null():
    _ensure_built()
    payload = json.loads(PAYLOAD.read_text())
    assert payload["gate"] == "7B"
    assert payload.get("database_engine") == "postgresql"
    unknown = payload["slices"]["legacy_tokopedia_2025_unknown"]
    assert len(unknown) == 2
    assert all(row.get("value") is None for row in unknown)
    assert payload["locked_story_checks"]["shopee_share_2025"] == 54.0
    assert payload["locked_story_checks"]["combined_share_2025"] == 38.0


def test_methodology_doc_mentions_postgresql():
    path = ROOT / "research" / "gate7b_dashboard_sql_schema.md"
    assert path.exists()
    doc = path.read_text()
    assert "PostgreSQL" in doc
    assert "DATABASE_URL" in doc
    assert "v_market_share_post_break_2025" in doc
    assert "scripts/build_dashboard_sql.py" in doc
    assert "SQLite" in doc  # deprecation mentioned


def test_database_url_helper_defaults_to_postgres():
    url = database_url()
    assert "postgresql" in url
    # Ensure we can construct an engine object (does not require live query here)
    engine = create_engine(url, future=True)
    assert engine.url.drivername.startswith("postgresql")
