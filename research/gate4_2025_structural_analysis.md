# Gate 4 — 2025 Structural Analysis

**Project:** E-Commerce Power Shift: Shopee vs Tokopedia in Indonesia  
**Gate:** 4 Exploratory Analysis  
**Date:** 2026-08-12  
**Status:** Exploratory — not final portfolio conclusion; no SQL/dashboard  

**Critical distinction (mandatory):**  
“Tokopedia was involved in the 2025 combined business” ≠ “Legacy Tokopedia itself recovered.”

**Method rules applied:**  
- Never treat 2025 Combined as Legacy Tokopedia  
- Never use Combined − TTS as observed Legacy GMV  
- Never convert APJII access into GMV  
- Label OBSERVED / DERIVED / INFERRED / UNKNOWN  
- Keep missing as missing  

**Evidence base:** Gate 3B `entity_split_2024_2025` + primary timeline sources (see `data/raw/structural_break/PROVENANCE.md`).

---

## 1. 2024 Baseline

What each number represents: **Indonesia platform e-commerce GMV share / GMV estimates** from Momentum Works as reproduced in secondary press (Bisnis), unless noted otherwise. These are **estimates**, not official company GMV filings.

| Entity | Metric | Value | Evidence type | What it means |
|--------|--------|------:|---------------|---------------|
| Shopee | Market share (GMV) | 46% | OBSERVED (SECONDARY) | Leading Indonesia marketplace by estimated GMV share |
| Shopee | GMV | ~US$26B | OBSERVED (SECONDARY) | Estimated absolute GMV |
| Legacy Tokopedia | Market share (GMV) | 23% | OBSERVED (SECONDARY) | **Standalone** Tokopedia in 2024 reporting |
| Legacy Tokopedia | Implied GMV | ~US$13.0B | DERIVED (56.5×0.23) | Not separately published; share × Indonesia total |
| TikTok Shop Indonesia | Market share (GMV) | 11% | OBSERVED (SECONDARY) | **Standalone** TTS in 2024 reporting |
| TikTok Shop Indonesia | Implied GMV | ~US$6.2B | DERIVED (56.5×0.11) | Same derivation caveat |
| Indonesia market | Total GMV | US$56.5B | OBSERVED (SECONDARY) | National platform ecommerce total |
| Combined (additive) | Share / GMV | 34% / ~US$19.2B | DERIVED (23+11) | Baseline only if 2024 Tokopedia and TTS are non-overlapping in MW methodology |
| Shopee / TTS / Tokopedia | APJII access | 41.65% / 12.20% / 9.40% | OBSERVED (SECONDARY_HIGH) | **Internet-user access**, not GMV |

**Baseline reading (OBSERVED + DERIVED):** In 2024 the market still published **separate** Tokopedia and TTS shares. Shopee led. An additive Combined baseline (~34%) is useful only for comparing to 2025 Combined (~38%), with additivity caveats.

---

## 2. 2025 Structural Break

### Why TikTok Shop and Tokopedia combined

**OBSERVED (PRIMARY / regulatory context):**

1. **Sep 2023 — Mot Reg 31/2023** restricted social-commerce checkout models (CONTEXT via legal summary).  
2. **4 Oct 2023 — TikTok Newsroom:** TTS Indonesia stopped facilitating e-commerce transactions.  
3. **11 Dec 2023 — TikTok Newsroom:** GoTo–TikTok partnership announced; businesses to combine under PT Tokopedia; TikTok controlling stake; shopping in TikTok app to be operated by enlarged Tokopedia entity.  
4. **31 Jan 2024 — GoTo PR:** Transaction completed; Tokopedia and TTS Indonesia businesses combined under PT Tokopedia; TikTok controlling stake; GoTo retains minority + **e-commerce service fee**.

**INFERRED (not a causal proof):** The combination was a regulatory/operating workaround so TikTok-linked commerce could continue in Indonesia through a licensed marketplace structure (Tokopedia), while TikTok retained control and discovery/content reach.

### Ownership / roles

| Party | Role (OBSERVED) |
|-------|-----------------|
| TikTok | Controlling owner (~75.01%); platform/control + content commerce side |
| GoTo | Minority (~24.99%); ecosystem partner; receives fee on **combined** Tokopedia + TTS GMV (CFO statement via Kontan) |
| PT Tokopedia | Legal/operating vehicle for combined businesses |
| Legacy Tokopedia brand/channel | Remains selectable in Seller Center (Tokopedia and/or TTS) — **capability**, not proof of Legacy GMV recovery |

### Reporting break

**OBSERVED (SECONDARY MW via Bisnis):** 2025 Indonesia share for “Tokopedia + TikTok Shop” is published as **one Combined figure (38%)**. Free public reproductions do **not** publish standalone Legacy Tokopedia 2025 GMV/share.

---

## 3. Entity Evolution

| Entity | 2024 evidence | 2025 evidence | Change | Evidence type | Interpretation |
|--------|---------------|---------------|--------|---------------|----------------|
| Shopee | 46% / ~$26B GMV; APJII access 41.65% | 54% / $31.2B; APJII 53.22% | +8 pp share; +~$5.2B GMV; +11.6 pp access | OBSERVED (SECONDARY / SECONDARY_HIGH) | Shopee strengthened on both GMV-share and access |
| Legacy Tokopedia | 23% GMV share; implied ~$13.0B; APJII 9.40% | GMV/share **MISSING**; APJII 9.57% | Access +0.17 pp; GMV change **UNKNOWN** | OBSERVED access; UNKNOWN GMV | No demonstrated standalone GMV comeback; access near-flat |
| TikTok Shop Indonesia | 11% share; implied ~$6.2B; APJII 12.20% | TTS-labeled GMV ~$13.1B; APJII 27.37% | Access +15.2 pp; GMV scale large vs 2024 implied | OBSERVED TTS GMV + access; 2024 GMV DERIVED | Strong TTS-labeled scale and attention growth |
| Combined Tokopedia + TikTok Shop | Additive baseline 34% / ~$19.2B (DERIVED) | 38% / ~$21.9B (OBSERVED Combined) | +4 pp vs additive baseline; +~$2.7B vs derived baseline | DERIVED baseline + OBSERVED 2025 | Combined entity modestly larger; **not** Legacy Tokopedia |
| Indonesia total | $56.5B | $57.7B (+2.2%) | Slow growth | OBSERVED (SECONDARY_HIGH) | MW attributes slowdown partly to Tokopedia GMV **rationalisation** + Bukalapak exit |

**Invalid comparison:** Legacy Tokopedia 23% (2024) → Combined 38% (2025).

---

## 4. What actually changed (2024 → 2025)?

**OBSERVED:**

1. Indonesia platform GMV grew only ~2.2% ($56.5B → $57.7B).  
2. Shopee share rose 46% → 54%.  
3. Market reporting switched Tokopedia/TTS from **split** (2024) to **Combined** (2025).  
4. Combined entity ~38% / ~$21.9B.  
5. TTS Indonesia separately reported ~$13.1B GMV (TTS-labeled).  
6. APJII: TTS access surged; Tokopedia access flat; Shopee access surged.  
7. MW publicly cites **Tokopedia GMV rationalisation** after TikTok acquisition as a factor in Indonesia’s slow GMV growth.

**DERIVED (caveated):** Additive Combined 2024 (~34%) → Combined 2025 (38%) ≈ +4 pp — modest Combined gain while Shopee gained more.

**UNKNOWN:** Standalone Legacy Tokopedia 2025 GMV and share; exact split of Combined $21.9B between Legacy and TTS.

---

## 5. Hypothesis tests (summary)

Detailed tests: `research/tokopedia_comeback_final_test.md`  
End-state answers: `research/2025_end_state.md`

| Hypothesis | Status |
|------------|--------|
| H1 Legacy Tokopedia comeback | **UNSUPPORTED** (on available evidence; GMV path UNKNOWN/missing) |
| H2 Hybrid recovery | **PARTIALLY SUPPORTED** (structure/ops; not proven dual GMV contribution) |
| H3 TikTok-led growth | **PARTIALLY SUPPORTED** (strongest of three; Combined split still incomplete) |

---

## 6. Limitations

- MW figures are secondary reproductions of industry estimates.  
- TTS $13.1B and Combined $21.9B are **not** confirmed additive.  
- APJII is access, Magpie is FMCG tracked GMV — neither is national all-category GMV.  
- Google Trends and free long-run traffic still absent.  
- No fabricated Legacy Tokopedia 2025 GMV.

---

## 7. Gate 4 decision

Exploratory analysis can proceed on **Shopee trajectory**, **Combined vs additive baseline**, **TTS-labeled indicators**, and **access splits**.  

It **cannot** support a portfolio claim that “Tokopedia came back in 2025” as a standalone marketplace.  

**Next milestone recommendation:** Gate 5 competitive analysis with the same entity discipline — or acquire primary MW entity-split if available — before SQL/dashboard.
