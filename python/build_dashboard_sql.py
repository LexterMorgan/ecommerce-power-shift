"""
Gate 7B — Build PostgreSQL dashboard data layer from analysis-ready outputs.

Canonical database: PostgreSQL (SQLite is deprecated for this project).

Does NOT:
- invent business metrics
- convert UNKNOWN/null → 0
- merge 2022–2024 Legacy Tokopedia with 2025 Combined into one series
- modify Gates 1–6 conclusions or Gate 7A methodology
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

PANEL = ROOT / "data" / "processed" / "analysis_ready" / "competitive_panel.csv"
COMPARABLE = (
    ROOT / "data" / "processed" / "2025_comparable" / "platform_metrics_2025_processed.csv"
)
SCENARIO_IN = ROOT / "data" / "processed" / "gate6_scenario_inputs.csv"
SCENARIO_OUT = ROOT / "data" / "processed" / "gate6_scenario_outputs.csv"
SHARE_GAP = ROOT / "analysis" / "outputs" / "tables" / "share_gap_summary.csv"
SCHEMA = ROOT / "sql" / "schema.sql"

DASHBOARD_DIR = ROOT / "data" / "dashboard"
EXPORT_DIR = DASHBOARD_DIR / "exports"
PAYLOAD_PATH = DASHBOARD_DIR / "dashboard_payload.json"
MANIFEST_PATH = DASHBOARD_DIR / "manifest.json"
SQLITE_LEGACY_DB = DASHBOARD_DIR / "ecommerce_power_shift.db"
SQLITE_DEPRECATION = DASHBOARD_DIR / "SQLITE_DEPRECATED.md"

DEFAULT_DATABASE_URL = "postgresql+psycopg://localhost:5432/ecommerce_power_shift"


def database_url() -> str:
    """Return SQLAlchemy URL for the canonical PostgreSQL database."""
    raw = os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL).strip()
    if raw.startswith("postgres://"):
        raw = "postgresql://" + raw[len("postgres://") :]
    if raw.startswith("postgresql://") and "+psycopg" not in raw and "+psycopg2" not in raw:
        raw = "postgresql+psycopg://" + raw[len("postgresql://") :]
    return raw


def database_display_name(url: str) -> str:
    parsed = urlparse(url.replace("postgresql+psycopg", "postgresql").replace(
        "postgresql+psycopg2", "postgresql"
    ))
    db = (parsed.path or "/").lstrip("/") or "ecommerce_power_shift"
    host = parsed.hostname or "localhost"
    port = parsed.port or 5432
    return f"postgresql://{host}:{port}/{db}"


def get_engine() -> Engine:
    return create_engine(database_url(), future=True)


def _read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing required input: {path}")
    return pd.read_csv(path)


def _assert_unknown_null(df: pd.DataFrame, status_col: str, value_col: str = "value") -> None:
    unknown = df[df[status_col] == "UNKNOWN"]
    if len(unknown) and unknown[value_col].notna().any():
        raise ValueError(
            f"UNKNOWN rows must have null {value_col}; refusing to load dashboard SQL"
        )


def _to_sql_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure pandas NA becomes SQL NULL; never fill with 0."""
    out = df.copy()
    return out.where(pd.notnull(out), None)


def validate_locked_story(panel: pd.DataFrame) -> dict:
    """Assert key historical values match Gate 7A locked story (no reinterpretation)."""

    def _val(year: int, entity: str, metric: str) -> float:
        sub = panel[
            (panel["year"] == year)
            & (panel["analytical_entity"] == entity)
            & (panel["metric"] == metric)
            & (panel["value_status"].isin(["OBSERVED", "DERIVED"]))
        ]
        if len(sub) != 1 or pd.isna(sub.iloc[0]["value"]):
            raise AssertionError(f"Missing locked value {year} {entity} {metric}")
        return float(sub.iloc[0]["value"])

    checks = {
        "shopee_share_2022": _val(2022, "Shopee", "market_share_pct"),
        "legacy_share_2022": _val(2022, "Legacy Tokopedia", "market_share_pct"),
        "shopee_share_2024": _val(2024, "Shopee", "market_share_pct"),
        "legacy_share_2024": _val(2024, "Legacy Tokopedia", "market_share_pct"),
        "shopee_share_2025": _val(2025, "Shopee", "market_share_pct"),
        "combined_share_2025": _val(
            2025, "Combined Tokopedia + TikTok Shop", "market_share_pct"
        ),
        "combined_derived_2024": _val(
            2024, "Combined Tokopedia + TikTok Shop", "market_share_pct"
        ),
    }
    assert checks["shopee_share_2022"] == 36.0
    assert checks["legacy_share_2022"] == 35.0
    assert checks["shopee_share_2024"] == 46.0
    assert checks["legacy_share_2024"] == 23.0
    assert checks["shopee_share_2025"] == 54.0
    assert checks["combined_share_2025"] == 38.0
    assert checks["combined_derived_2024"] == 34.0

    unk = panel[
        (panel["year"] == 2025)
        & (panel["analytical_entity"] == "Legacy Tokopedia")
        & (panel["value_status"] == "UNKNOWN")
    ]
    assert len(unk) == 2
    assert unk["value"].isna().all()
    return checks


def load_tables() -> dict[str, pd.DataFrame]:
    panel = _read_csv(PANEL)
    supporting = _read_csv(COMPARABLE)
    scen_in = _read_csv(SCENARIO_IN)
    scen_out = _read_csv(SCENARIO_OUT)
    share_gap = _read_csv(SHARE_GAP) if SHARE_GAP.exists() else pd.DataFrame()

    _assert_unknown_null(panel, "value_status")
    if "evidence_type" in supporting.columns:
        _assert_unknown_null(supporting, "evidence_type")
    if "value_type" in scen_in.columns:
        _assert_unknown_null(scen_in, "value_type")

    validate_locked_story(panel)

    return {
        "fact_competitive_panel": panel,
        "fact_supporting_2025": supporting,
        "fact_scenario_inputs": scen_in,
        "fact_scenario_outputs": scen_out,
        "fact_share_gap_summary": share_gap,
    }


def _split_sql_statements(sql: str) -> list[str]:
    """Split a simple DDL script into statements (no procedures/dollar-quotes)."""
    statements: list[str] = []
    buf: list[str] = []
    for line in sql.splitlines():
        if line.strip().startswith("--"):
            continue
        buf.append(line)
        if line.rstrip().endswith(";"):
            stmt = "\n".join(buf).strip()
            if stmt:
                statements.append(stmt)
            buf = []
    trailing = "\n".join(buf).strip()
    if trailing:
        statements.append(trailing)
    return statements


def apply_schema(engine: Engine) -> None:
    statements = _split_sql_statements(SCHEMA.read_text())
    with engine.begin() as conn:
        for stmt in statements:
            conn.execute(text(stmt))


def write_tables(engine: Engine, tables: dict[str, pd.DataFrame]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for name, df in tables.items():
        if df is None or df.empty:
            counts[name] = 0
            continue
        clean = _to_sql_nulls(df)
        clean.to_sql(name, engine, if_exists="append", index=False, method="multi")
        counts[name] = len(clean)
    return counts


def export_views(engine: Engine) -> list[str]:
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    views = [
        "v_competitive_panel_all",
        "v_market_share_plottable",
        "v_market_share_standalone_2022_2024",
        "v_market_share_post_break_2025",
        "v_legacy_tokopedia_unknown_2025",
        "v_gmv_estimates",
        "v_access_metrics",
        "v_tts_labeled_gmv",
        "v_scenario_gap_bands",
        "v_share_gap_summary",
        "v_dashboard_filter_keys",
    ]
    written = []
    for view in views:
        df = pd.read_sql_query(text(f"SELECT * FROM {view}"), engine)
        path = EXPORT_DIR / f"{view}.csv"
        df.to_csv(path, index=False)
        written.append(str(path.relative_to(ROOT)))
    return written


def build_payload(tables: dict[str, pd.DataFrame], checks: dict) -> dict:
    panel = tables["fact_competitive_panel"]
    supporting = tables["fact_supporting_2025"]
    scen = tables["fact_scenario_outputs"]

    def records(df: pd.DataFrame) -> list:
        return json.loads(df.to_json(orient="records", date_format="iso"))

    access = supporting[
        (supporting["metric"] == "internet_user_access_share_pct")
        & (supporting["evidence_type"] == "OBSERVED")
        & (supporting["value"].notna())
    ]
    tts = supporting[
        (supporting["entity"] == "TikTok Shop Indonesia")
        & (supporting["metric"] == "gmv_estimate_usd")
        & (supporting["evidence_type"] == "OBSERVED")
        & (supporting["value"].notna())
    ]
    scen_gap = scen[
        (scen["metric"] == "shopee_minus_combined_share_gap_pp")
        & (scen["value_type"] == "SCENARIO")
    ]

    return {
        "gate": "7B",
        "database_engine": "postgresql",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "rules": [
            "Expose existing analysis-ready results only",
            "OBSERVED / DERIVED / UNKNOWN / SCENARIO semantics preserved",
            "UNKNOWN never converted to zero",
            "2022-2024 standalone separate from 2025 Combined",
            "No continuous merge across structural break",
            "PostgreSQL is the canonical project database",
        ],
        "locked_story_checks": checks,
        "sources": {
            "competitive_panel": str(PANEL.relative_to(ROOT)),
            "supporting_2025": str(COMPARABLE.relative_to(ROOT)),
            "scenario_inputs": str(SCENARIO_IN.relative_to(ROOT)),
            "scenario_outputs": str(SCENARIO_OUT.relative_to(ROOT)),
            "share_gap_summary": str(SHARE_GAP.relative_to(ROOT)),
        },
        "competitive_panel": records(panel),
        "supporting_2025": records(supporting),
        "scenario_inputs": records(tables["fact_scenario_inputs"]),
        "scenario_outputs": records(scen),
        "share_gap_summary": records(tables["fact_share_gap_summary"]),
        "slices": {
            "market_share_standalone_2022_2024": records(
                panel[
                    (panel["year"].between(2022, 2024))
                    & (panel["metric"] == "market_share_pct")
                    & (panel["analytical_entity"].isin(["Shopee", "Legacy Tokopedia"]))
                    & (panel["entity_type"] == "standalone")
                    & (panel["value_status"] == "OBSERVED")
                    & (panel["value"].notna())
                ]
            ),
            "market_share_post_break_2025": records(
                panel[
                    (panel["year"] == 2025)
                    & (panel["metric"] == "market_share_pct")
                    & (panel["value_status"] == "OBSERVED")
                    & (panel["value"].notna())
                    & (
                        (panel["analytical_entity"] == "Shopee")
                        | (
                            (panel["analytical_entity"] == "Combined Tokopedia + TikTok Shop")
                            & (panel["entity_type"] == "combined")
                        )
                    )
                ]
            ),
            "legacy_tokopedia_2025_unknown": records(
                panel[
                    (panel["year"] == 2025)
                    & (panel["analytical_entity"] == "Legacy Tokopedia")
                    & (panel["value_status"] == "UNKNOWN")
                ]
            ),
            "access_metrics": records(access),
            "tts_labeled_gmv": records(tts),
            "scenario_gap_bands": records(scen_gap),
        },
    }


def validate_db(engine: Engine, expected_panel_rows: int) -> dict:
    with engine.connect() as conn:
        panel_n = conn.execute(text("SELECT COUNT(*) FROM fact_competitive_panel")).scalar_one()
        assert panel_n == expected_panel_rows

        unk = conn.execute(
            text(
                """
                SELECT COUNT(*) AS n,
                       SUM(CASE WHEN value IS NULL THEN 1 ELSE 0 END) AS n_null
                FROM fact_competitive_panel
                WHERE value_status = 'UNKNOWN'
                """
            )
        ).mappings().one()
        assert unk["n"] >= 2
        assert unk["n"] == unk["n_null"], "Every UNKNOWN row must have NULL value"

        bad = conn.execute(
            text(
                """
                SELECT COUNT(*) FROM fact_competitive_panel
                WHERE value_status = 'UNKNOWN' AND value = 0
                """
            )
        ).scalar_one()
        assert bad == 0

        standalone_n = conn.execute(
            text("SELECT COUNT(*) FROM v_market_share_standalone_2022_2024")
        ).scalar_one()
        assert standalone_n == 6

        post_n = conn.execute(
            text("SELECT COUNT(*) FROM v_market_share_post_break_2025")
        ).scalar_one()
        assert post_n == 2

        legacy_in_post = conn.execute(
            text(
                """
                SELECT COUNT(*) FROM v_market_share_post_break_2025
                WHERE analytical_entity = 'Legacy Tokopedia'
                """
            )
        ).scalar_one()
        assert legacy_in_post == 0

        s25 = conn.execute(
            text(
                """
                SELECT value FROM v_market_share_post_break_2025
                WHERE analytical_entity = 'Shopee'
                """
            )
        ).scalar_one()
        c25 = conn.execute(
            text(
                """
                SELECT value FROM v_market_share_post_break_2025
                WHERE analytical_entity = 'Combined Tokopedia + TikTok Shop'
                """
            )
        ).scalar_one()
        assert float(s25) == 54.0
        assert float(c25) == 38.0

    return {
        "fact_competitive_panel_rows": int(panel_n),
        "unknown_rows": int(unk["n"]),
        "standalone_share_rows": int(standalone_n),
        "post_break_share_rows": int(post_n),
        "shopee_2025_share": float(s25),
        "combined_2025_share": float(c25),
    }


def deprecate_sqlite_artifact() -> None:
    """Remove legacy SQLite DB if present and leave an explicit deprecation notice."""
    if SQLITE_LEGACY_DB.exists():
        SQLITE_LEGACY_DB.unlink()
    SQLITE_DEPRECATION.write_text(
        "\n".join(
            [
                "# SQLite deprecated",
                "",
                "The Gate 7B dashboard data layer previously used",
                "`ecommerce_power_shift.db` (SQLite).",
                "",
                "**PostgreSQL is now the canonical project database.**",
                "",
                "Do not recreate or consume a SQLite `.db` file for this project.",
                "Rebuild with:",
                "",
                "```bash",
                "python3 scripts/build_dashboard_sql.py",
                "```",
                "",
                "Connection (override with `DATABASE_URL`):",
                f"`{database_display_name(database_url())}`",
                "",
            ]
        )
    )


def main() -> int:
    DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)
    deprecate_sqlite_artifact()

    tables = load_tables()
    checks = validate_locked_story(tables["fact_competitive_panel"])
    engine = get_engine()
    display = database_display_name(database_url())

    try:
        apply_schema(engine)
    except Exception as exc:  # noqa: BLE001 — surface connection/setup guidance
        raise SystemExit(
            "Failed to apply PostgreSQL schema.\n"
            f"DATABASE_URL={display}\n"
            "Ensure PostgreSQL is running and the database exists, e.g.:\n"
            "  createdb ecommerce_power_shift\n"
            "  export DATABASE_URL=postgresql://localhost:5432/ecommerce_power_shift\n"
            f"Original error: {exc}"
        ) from exc

    build_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                INSERT INTO dashboard_build_meta (build_id, built_at_utc, gate, notes)
                VALUES (:build_id, :built_at_utc, :gate, :notes)
                """
            ),
            {
                "build_id": build_id,
                "built_at_utc": datetime.now(timezone.utc).isoformat(),
                "gate": "7B",
                "notes": (
                    "PostgreSQL load from analysis-ready panel + supporting processed "
                    "files; Gate 7A locked; SQLite deprecated"
                ),
            },
        )

    counts = write_tables(engine, tables)
    db_validation = validate_db(engine, len(tables["fact_competitive_panel"]))
    exports = export_views(engine)

    payload = build_payload(tables, checks)
    PAYLOAD_PATH.write_text(json.dumps(payload, indent=2))

    manifest = {
        "gate": "7B",
        "database_engine": "postgresql",
        "database": display,
        "built_at_utc": datetime.now(timezone.utc).isoformat(),
        "payload": str(PAYLOAD_PATH.relative_to(ROOT)),
        "schema": str(SCHEMA.relative_to(ROOT)),
        "table_row_counts": counts,
        "db_validation": db_validation,
        "exports": exports,
        "sqlite_status": "deprecated_removed",
        "regenerate": "python3 scripts/build_dashboard_sql.py",
        "prerequisite": (
            "PostgreSQL reachable; competitive_panel.csv and Gate 7A "
            "share_gap_summary.csv exist"
        ),
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2))

    print("GATE7B_STATUS=PASS")
    print(f"DATABASE_ENGINE=postgresql")
    print(f"DB → {display}")
    print(f"Payload → {PAYLOAD_PATH}")
    print(f"Exports → {EXPORT_DIR}")
    print(f"SQLite → deprecated ({SQLITE_DEPRECATION.name})")
    print(
        f"Rows panel={counts.get('fact_competitive_panel')} "
        f"standalone_view=6 post_break_view=2 Legacy2025=UNKNOWN"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
