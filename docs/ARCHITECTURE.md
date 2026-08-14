# Architecture

## Purpose

This document describes the **intended** technical architecture for the project. Layers below are design targets for later gates. None of these runtime layers are implemented in Milestone 0B.

## Primary Research Question

How did Shopee's competitive position in Indonesia change relative to Tokopedia, and what observable market factors help explain that shift?

## Intended Pipeline

```
Public Data Sources
        ↓
Raw Data
        ↓
Python Data Acquisition / Cleaning
        ↓
Processed Canonical Dataset
        ↓
Python Analytics + SQL
        ↓
Forecasting / Scenario Analysis
        ↓
Dashboard Data Layer
        ↓
React + TypeScript + shadcn
        ↓
Vercel
```

## Current public deployment (Gates 10B–10C)

PostgreSQL/SQL remain the **analytical** data layer. The **public** dashboard is a static React/Vite app on Vercel that loads `frontend/public/data/dashboard_data.json` (no FastAPI, no runtime database credentials).

```
GitHub → Vercel → React/Vite → static dashboard_data.json
```

See `research/gate10_deployment.md` and `research/dashboard_data_contract.md`.

## Layer Responsibilities

### Public Data Sources

Candidate and (later) verified external sources: industry research, company disclosures, government statistics, search-interest tools, traffic estimators, academic work, and reputable publications.

Purpose: provide traceable inputs. Sources remain registered in `docs/DATA_SOURCES.md` before use.

### Raw Data (`data/raw/`)

Immutable extracts as obtained from sources.

Purpose: preserve originals for audit, reprocessing, and provenance. Raw files are never overwritten by cleaning logic.

### Python Data Acquisition / Cleaning

Scripts that fetch or ingest approved sources and transform raw extracts into consistent structures.

Purpose: make acquisition and cleaning reproducible, logged, and testable. Cleaning does not invent missing values to force continuity.

### Processed Canonical Dataset (`data/processed/`)

Cleaned, documented tables that become the analytical source of truth for downstream work.

Purpose: hold shared metric definitions, aligned time keys, and platform identifiers so analysis and dashboard layers do not redefine metrics independently.

### Python Analytics + SQL (`analysis/`, `sql/`)

Descriptive and comparative analysis over the canonical dataset.

Purpose: answer historical and relative-position questions, produce validated analytical outputs, and keep definitions outside the frontend.

### Forecasting / Scenario Analysis (`forecasting/`)

Forward-looking models and alternative scenarios, kept separate from descriptive analysis.

Purpose: project trajectories under explicit assumptions. Forecast outputs must not be mixed into historical fact tables without clear labeling.

### Dashboard Data Layer

Validated payloads or tables prepared specifically for presentation.

Purpose: expose only reviewed metrics to the UI. This layer consumes analytical outputs; it does not become a second source of truth.

### React + TypeScript + shadcn (`frontend/`)

Executive dashboard and interactive views.

Purpose: present competitive position, trends, events, drivers, and forecasts. The frontend is a presentation layer only.

### Vercel

Hosting/deployment target for the dashboard.

Purpose: publish the presentation layer after validation gates pass.

## Design Principles

- Raw data remains separate from processed data.
- Data provenance must be preserved.
- Analytical definitions should not live exclusively inside the frontend.
- The frontend consumes validated analytical outputs.
- Forecasting remains separate from descriptive analysis.
- Important transformations should be reproducible.
- Important transformations should eventually be tested.
- The dashboard is a presentation layer, not the source of truth.

## Repository Alignment

| Path | Architectural role |
|------|--------------------|
| `data/raw/` | Raw Data |
| `data/processed/` | Processed Canonical Dataset |
| `research/` | Source notes and qualitative research support |
| `analysis/` | Python analytics |
| `sql/` | SQL analytics |
| `forecasting/` | Forecasting / scenario analysis |
| `frontend/` | React + TypeScript + shadcn presentation |
| `tests/` | Transformation, metric, and payload validation |
| `docs/` | Control documents and methodology |
| `.cursor/` | Cursor agents and rules |

## Explicit Non-Implementation (Milestone 0B)

This milestone updates documentation only. It does not:

- Acquire or store datasets
- Implement Python pipelines
- Create SQL models
- Build forecasting models
- Build the dashboard or deploy to Vercel
