# Gate 8 — React Dashboard Architecture (updated for Gate 10B)

**Status:** React presentation remains; **public data path is static JSON** (Gate 10B).  
**Canonical analytical DB:** PostgreSQL (Gate 7B) — not required at public runtime.  
**Public snapshot:** `frontend/public/data/dashboard_data.json`

## Purpose

Present locked Gate 7A/7B analysis-ready results in an executive dashboard. The UI does **not** invent metrics, coerce UNKNOWN→0, or reinterpret Gates 1–6 conclusions.

## Public data flow (Gate 10B)

```
analysis-ready CSVs
        ↓
scripts/export_dashboard_data.py
        ↓
frontend/public/data/dashboard_data.json
        ↓
React (`loadDashboardData()`)
```

FastAPI is **removed** from the public path. Historical Gate 8 API endpoints are deprecated and deleted.

## Frontend structure

```
frontend/src/
  App.tsx
  lib/dashboardData.ts
  lib/DashboardContext.tsx
  pages/*
```

Routes: `/` · `/competitive` · `/supporting` · `/scenarios` · `/explorer`

## Run locally

```bash
python3 scripts/export_dashboard_data.py
cd frontend && npm install && npm run dev
```

## Related docs

- Contract: `research/dashboard_data_contract.md`
- SQL layer: `research/gate7b_dashboard_sql_schema.md`
- Deploy (static Vercel): `research/gate10_deployment.md`
