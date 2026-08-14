# Gate 3 — Data acquisition notes (structural break)

**Date:** 2026-08-12  
**Scope:** Entity-split evidence for 2024→2025; no fabricated fills.

## Acquired / curated this gate

| Asset | Path | Method |
|-------|------|--------|
| Transition evidence table | `data/raw/structural_break/transition_2024_2025_evidence.csv` | Manual curation from public secondary MW citations + labeled DERIVED arithmetic |
| Provenance | `data/raw/structural_break/PROVENANCE.md` | Documentation |
| Competitive events (expanded) | `data/raw/events/competitive_events.csv` | Official newsroom / GoTo / KPPU secondary (10 events) |
| Processed structural_break | `data/processed/structural_break/transition_2024_2025_evidence.csv` | Pipeline clean/validate |

## Research artifacts (not datasets)

- `research/tiktok_tokopedia_timeline.md`
- `research/tokopedia_comeback_evidence_matrix.md`
- `research/2025_data_requirements.md`
- `research/tokopedia_comeback_preliminary_findings.md`

## Not acquired (remain missing / blocked)

- Standalone Legacy Tokopedia 2025 market share (UNKNOWN)
- Primary Momentum Works full matrices (paid)
- Google Trends CSV (automated 429; manual path documented)
- Free long-run Similarweb history

## Pipeline

`python3 scripts/process_data.py` now loads → cleans → validates → writes `structural_break` alongside existing datasets.
