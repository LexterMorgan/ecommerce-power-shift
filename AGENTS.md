# AGENTS.md

Repository-wide instructions for AI agents working on **E-Commerce Power Shift: Shopee vs Tokopedia in Indonesia**.

## Implementation Environment

**Current implementation environment: Cursor + Grok**

There is **no Claude workflow** for this project.

Do not create `.claude/`, `CLAUDE.md`, or Claude-specific agents, skills, or configs.

## Primary Research Question

How did Shopee's competitive position in Indonesia change relative to Tokopedia, and what observable market factors help explain that shift?

## Required Reading Before Changes

Agents must read the documents relevant to the task before editing:

- `docs/PRD.md`
- `docs/ARCHITECTURE.md`
- `docs/WORKFLOW.md`
- `docs/RESEARCH_METHOD.md`
- `docs/DATA_SOURCES.md`
- `docs/TODO.md`

## Agents Must

1. Read relevant documentation before making changes.
2. Follow the PRD.
3. Follow the architecture.
4. Follow the workflow.
5. Follow the research methodology.
6. Check the data-source registry before using external data.
7. Preserve raw datasets.
8. Never fabricate data.
9. Never fabricate sources.
10. Never invent historical values.
11. Never silently redefine metrics.
12. Never silently change methodology.
13. Never make unsupported causal claims.
14. Keep changes scoped to the current milestone.
15. Add appropriate tests when implementation begins.
16. Validate work before reporting completion.
17. Report exactly which files changed.
18. Distinguish facts, estimates, assumptions, and inference.

## Research Principle

Do not assume that Shopee's rise, or any competitive shift, was caused by a specific factor.

Potential explanations are hypotheses to investigate later. Do not present hypotheses as findings without evidence.

## Active Gate Discipline

Follow `docs/TODO.md`. Gate 0 and Gate 1 are complete. Gate 2 is **READY WITH DOCUMENTED LIMITATIONS** per `research/data_quality_validation_report.md`.

- Do not start SQL/dashboard/frontend until ChatGPT/human approval after Gate 2 review.
- Prefer original publishers; label Momentum Works public excerpts as secondary estimates.
- Preserve raw datasets; regenerate processed via `scripts/process_data.py`.
- Never invent missing years/GMV; never interpolate annual → monthly without explicit documented justification.
- Google Trends: if blocked, use manual export path in `data/raw/google_trends/README_MANUAL_EXPORT.md` — do not bypass rate limits/paywalls.
- Keep company metrics separate from Indonesia platform market-position data unless definitions are genuinely comparable.
- Treat 2025 `Tokopedia + TikTok Shop` as a combined entity, not standalone Tokopedia.

## If Something Cannot Be Completed

Report:

- What was completed
- What failed
- Why it failed
- What remains
- What decision is required

Do not claim completion without actual validation.

## Cursor Paths

- `.cursor/agents/` — optional Cursor agent definitions for this repo
- `.cursor/rules/` — optional Cursor rules for this repo

These paths support the Cursor + Grok workflow only.
