# E-Commerce Power Shift: Shopee vs Tokopedia in Indonesia

Portfolio data-analytics project: a **static executive dashboard** over a reproducible research pipeline for Indonesia e-commerce competitive position.

## Portfolio overview — what this dashboard demonstrates

The dashboard presents **locked, evidence-labeled** market-share and supporting metrics for Shopee versus Tokopedia-related entities in Indonesia. It shows:

- **2022–2024 standalone dyad:** Shopee vs Legacy Tokopedia (OBSERVED shares)
- **2025 structural break:** Shopee vs **Combined Tokopedia + TikTok Shop** (not Legacy Tokopedia)
- **UNKNOWN handling:** Legacy Tokopedia 2025 GMV/share stays missing — never plotted as zero
- **Supporting evidence:** APJII access shares (access ≠ GMV) and TTS-labeled GMV
- **Scenario bands:** Gate 6 illustrative `SCENARIO` gap ranges — not forecasts-as-fact
- **Filterable panel:** year / marketplace / metric / value_status / comparability

It does **not** invent proprietary platform data, claim causal “why Shopee won” narratives, or treat Combined 38% as a Legacy Tokopedia comeback.

## Business / problem context

Strategy and commercial teams need a transparent view of how relative competitive position changed in Indonesia’s marketplace landscape, what remains uncertain, and what scenarios are plausible — without fabricating metrics or unsupported causal claims.

## Research question

How did Shopee's competitive position in Indonesia change relative to Tokopedia, and what observable market factors help explain that shift?

## Status

Gates **0–10B** are complete for the repository. Public hosting on Vercel is a **manual** account step. Analytical conclusions for Gates 1–9 are **LOCKED**.

## Architecture (locked)

**PostgreSQL and SQL are used as part of the analytical data layer. The public dashboard is deployed as a static React application using a validated analysis-ready data snapshot because the project analyzes historical data rather than requiring live data.**

### Analytical (local / portfolio infrastructure)

```
Raw sources
  → Python ETL / cleaning / validation
  → PostgreSQL + SQL (Gate 7B schema/views)
  → analysis-ready datasets
  → scripts/export_dashboard_data.py
```

### Public deployment

```
GitHub
  → Vercel
  → React/Vite (`frontend/`)
  → static `public/data/dashboard_data.json`
```

No FastAPI hosting, no public Postgres credentials, and no CORS configuration are required for the public dashboard.

## Analytical methodology (completed)

1. Acquire/preserve traceable public sources.
2. Clean into canonical datasets with provenance.
3. Investigate 2024→2025 structural break (Combined ≠ Legacy Tokopedia).
4. Label evidence OBSERVED / DERIVED / UNKNOWN / SCENARIO.
5. Analysis-ready panel + Gate 7A charts.
6. PostgreSQL analytical tables/views (Gate 7B).
7. Validation of locked values (Gate 9).
8. Static dashboard export for React (Gate 10B).

Locked reference shares (unchanged): Shopee 36%→46%→54%; Legacy 35%→23% then **UNKNOWN** in 2025; Combined 2025 **38%** OBSERVED.

## Environment variables

| Variable | Required by public UI? | Purpose |
|----------|------------------------|---------|
| `DATABASE_URL` | **No** | Local PostgreSQL for Gate 7B analytical load only |
| _(none)_ | Public Vercel site needs no API/DB secrets | Snapshot is shipped as JSON |

Template: `.env.example`

## Local setup

```bash
# Analytical layer (optional for UI; required for SQL portfolio work)
python3 -m pip install -r requirements.txt
export DATABASE_URL=postgresql://localhost:5432/ecommerce_power_shift
createdb ecommerce_power_shift   # once
python3 scripts/build_dashboard_sql.py

# Static dashboard snapshot (required before UI)
python3 scripts/export_dashboard_data.py

# Frontend
cd frontend && npm install && npm run dev

# Checks
python3 scripts/run_gate9_validation.py
python3 scripts/check_production_readiness.py
python3 -m pytest tests/ -q
cd frontend && npm test && npm run build
```

## Regenerate dashboard JSON

```bash
python3 scripts/export_dashboard_data.py
# → frontend/public/data/dashboard_data.json
```

Contract: [`research/dashboard_data_contract.md`](research/dashboard_data_contract.md)

## Production deployment (Vercel — manual)

1. Push repo to GitHub.
2. Create a Vercel project; **Root Directory** = `frontend`.
3. Build command `npm run build`, output `dist`.
4. Ensure `frontend/public/data/dashboard_data.json` is committed.
5. No `DATABASE_URL` / API URL env vars needed for the public site.

Details: [`research/gate10_deployment.md`](research/gate10_deployment.md)

## Known limitations

- Read-only historical snapshot (not live data).
- Legacy Tokopedia 2025 GMV/share = **UNKNOWN**.
- Combined ≠ Legacy Tokopedia.
- Access ≠ GMV; scenarios are `SCENARIO` only.
- Event/driver pages not fabricated (outside Gate 7B scope).
- Screenshots are captured manually after deploy.

## Key documentation

| Doc | Role |
|-----|------|
| [docs/TODO.md](docs/TODO.md) | Gate roadmap |
| [research/gate7b_dashboard_sql_schema.md](research/gate7b_dashboard_sql_schema.md) | PostgreSQL analytical layer |
| [research/dashboard_data_contract.md](research/dashboard_data_contract.md) | Static JSON contract |
| [research/gate9_validation_report.md](research/gate9_validation_report.md) | Validation |
| [research/gate10_deployment.md](research/gate10_deployment.md) | Static deploy |
| [AGENTS.md](AGENTS.md) | Agent instructions |
