# 2025 Data Requirements — Structural Break & Entity Split

**Gate 3** | Updated 2026-08-12  
**Purpose:** Track what is needed to distinguish Legacy Tokopedia vs TikTok Shop Indonesia vs Combined — without fabricating fills.

| Metric | Entity | Ideal Source | Current Availability | Acquisition Method | Reliability | Needed? |
|--------|--------|--------------|----------------------|--------------------|-------------|---------|
| Marketplace GMV share (standalone) | Legacy Tokopedia | Momentum Works primary / official GoTo segment if published | **MISSING for 2025** | Paid MW report or IR disclosure | HIGH if primary | **YES — highest priority** |
| Marketplace GMV share (standalone) | TikTok Shop Indonesia | Momentum Works / TikTok disclosures | 2024: 11% (secondary MW via Bisnis); 2025: share often not published separately when combined | Public press excerpts; paid MW | MEDIUM secondary | **YES** |
| Marketplace GMV (USD) | TikTok Shop Indonesia | Momentum Works | 2025: ~$13.1B (TechNode/Digital in Asia citing MW) | Secondary press | MEDIUM | YES — corroborate with primary MW |
| Marketplace GMV share / GMV | Combined Tokopedia + TTS | Momentum Works | 2025: 38% / ~$21.9B (Bisnis citing MW) | Secondary press | MEDIUM | Have (label combined) |
| Marketplace GMV share / GMV | Shopee Indonesia | Momentum Works | 2024–2025 in Gate 2 market_position | Secondary press | MEDIUM | Have |
| Indonesia total marketplace GMV | Market | Momentum Works | 2024 $56.5B; 2025 $57.7B | Secondary press | MEDIUM | Have |
| Method note: are TTS ID GMV and Combined GMV additive? | Combined vs TTS | Momentum Works methodology | **UNKNOWN** | Primary MW methodology chapter | HIGH if obtained | **YES — blocks residual Legacy calc** |
| GoTo Tokopedia GMV (standalone) | Legacy Tokopedia | GoTo filings / transcripts | Not published as clean Indonesia GMV share post-deal | IR PDF / transcript | HIGH if present | YES |
| GoTo ecommerce service fee | GoTo–Tokopedia link | GoTo IR | Present in Gate 2 company_context (fee ≠ GMV) | Already acquired | HIGH for fee | Keep; do not misuse as GMV |
| Seller counts / active sellers | Legacy vs TTS vs Combined | Company newsroom / MW | Partial qualitative; Seller Center launch documented | Official newsroom | LOW–MEDIUM | Useful if numeric |
| Seller Center adoption metrics | Combined seller ops | TikTok/Tokopedia newsroom | Launch dates OBSERVED; uplift sample claims LOW for national | Newsroom | HIGH event / LOW sample GMV | Context only unless audited |
| App rankings Indonesia | Legacy Tokopedia app vs TikTok | Sensor Tower / data.ai / App Annie public | Not acquired | Manual public export if free | MEDIUM | Nice-to-have |
| Website traffic | tokopedia.com vs shopee.co.id | Similarweb | Free long history blocked (Gate 2) | Paid Similarweb or short free snapshot | MEDIUM | Optional; not GMV |
| Google Trends Indonesia | Shopee vs Tokopedia | Google Trends | Automated 429; manual path documented | Manual CSV export | MEDIUM | YES for attention proxy |
| Live / affiliate commerce GMV | TikTok Shop Indonesia | Industry reports / MW | Not acquired as structured series | Press / paid reports | MEDIUM | Helps H3 |
| Regulatory / ownership timeline | All | GoTo, TikTok, KPPU, Mot | Acquired in timeline + events | Official web | HIGH | Have |
| KPPU case materials | Ownership confirmation | KPPU / ASEAN Competition | 75.01/24.99 confirmed | Public reporting | HIGH | Have |
| Category trackers (e.g. SKU/price monitors) | Platforms | Third-party monitors | Not used as national GMV | — | — | Only if methodology clear |

## Acquisition rules (unchanged)

- No fabricated or interpolated annual fills.
- No paywall / CAPTCHA / ToS-bypass scraping.
- Label PRIMARY / ESTIMATE / SECONDARY / DERIVED / CONTEXT.
- Keep missing as missing.
- Never treat Combined 2025 as Legacy Tokopedia.

## Priority order for next acquisition

1. Primary Momentum Works (or equivalent) table that **separates** Legacy Tokopedia, TikTok Shop Indonesia, and Combined for 2024–2025.
2. Explicit methodology on whether Indonesia “Tokopedia + TikTok Shop” GMV includes the same TTS GMV cited as “TikTok Shop Indonesia.”
3. Manual Google Trends export (instructions already in `data/raw/google_trends/`).
4. Any GoTo disclosure that isolates marketplace GMV or orders for Tokopedia app/site vs TikTok Shop.
