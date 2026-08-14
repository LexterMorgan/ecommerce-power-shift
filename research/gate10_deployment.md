# Gate 10 / 10B — Public static deployment

**Status:** Public dashboard is a **static** React/Vite app on Vercel.  
**Analytical DB:** PostgreSQL + SQL remain local/portfolio infrastructure and are **not** required at runtime by the public UI.

## Architecture decision (locked)

This is a historical portfolio analytics project, not a live-data application.

```
GitHub
  → Vercel
  → React/Vite
  → frontend/public/data/dashboard_data.json
```

No public FastAPI, no production Postgres credentials on Vercel, no CORS for the dashboard.

## Analytical workflow (preserved)

```
Raw sources
  → Python ETL / validation
  → PostgreSQL + SQL analytical layer (Gate 7B)
  → analysis-ready CSVs
  → scripts/export_dashboard_data.py
  → frontend/public/data/dashboard_data.json
  → React
```

## Regenerate static data

```bash
python3 scripts/export_dashboard_data.py
```

Contract: `research/dashboard_data_contract.md`

## Local UI

```bash
python3 scripts/export_dashboard_data.py
cd frontend && npm install && npm run dev
```

## Vercel (manual)

1. Import GitHub repo.
2. Root directory: `frontend`
3. Build: `npm run build` · Output: `dist`
4. No `DATABASE_URL`, `VITE_API_BASE`, or `CORS_ORIGINS` required for the public site.
5. Commit `frontend/public/data/dashboard_data.json` so the snapshot deploys with the app.

## What was removed from public deploy path

- FastAPI (`api/`), `scripts/run_api.py`
- API `Dockerfile` / `Procfile`
- Frontend `/api` client + `VITE_API_BASE`

## What was preserved

- `sql/schema.sql`, `python/build_dashboard_sql.py`, processed data, Gate 7A/7B/9 validation
