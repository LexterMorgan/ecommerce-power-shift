# Workflow

## Primary Research Question

How did Shopee's competitive position in Indonesia change relative to Tokopedia, and what observable market factors help explain that shift?

## Working Model

This project uses a fixed division of labor between ChatGPT (planning and review), Cursor + Grok (implementation), and the Human (approvals). There is **no Claude workflow**.

## Responsibilities

### ChatGPT

- Planning
- Architecture
- Research direction
- Methodology
- Analysis
- Review
- Challenging assumptions
- Milestone design
- Milestone approval

### Cursor + Grok

- Implementation
- Coding
- Repository changes
- Test implementation
- Defined research/data tasks
- Validation
- Reporting implementation results

### Human

- Approving major decisions
- Approving methodology changes
- Reviewing important findings
- Approving milestone completion

## Core Workflow

```
Research / Planning
        ↓
Specification
        ↓
Cursor + Grok
        ↓
Tests / Validation
        ↓
ChatGPT Review
        ↓
Milestone Approval
        ↓
Next Milestone
```

## Rules

- Do not skip milestones without approval.
- Do not silently change methodology.
- Do not invent data.
- Do not fabricate sources.
- Do not fabricate findings.
- Do not make unsupported causal claims.
- Keep changes scoped to the active milestone.
- Avoid unrelated refactors.
- Validate before reporting completion.
- Report changed files.
- Distinguish facts, estimates, assumptions, and inference.

## Research Principle in Practice

Do not begin any milestone with a predetermined explanation for Shopee's rise or for any competitive shift.

Incorrect framing: “Shopee won because of X.”

Correct framing: “Investigate whether X is supported by available evidence.”

Potential explanations remain hypotheses until evidence is documented and reviewed.

## Milestone Hand-off Checklist

When Cursor + Grok finishes a milestone, the report must include:

1. What was completed
2. Files created or modified
3. Validation performed
4. Assumptions made
5. What was deliberately not done
6. Any blockers or decisions required

Do not claim completion without actual validation against the active gate in `docs/TODO.md`.

## Active Milestone (Milestone 0B)

Documentation completion only. Do not acquire data. Do not begin Gate 1.
