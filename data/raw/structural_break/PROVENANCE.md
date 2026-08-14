# Provenance — Structural Break & Entity Split (Gate 3 / 3B)

**Updated:** 2026-08-12 (Gate 3B)  
**Purpose:** Trace every important 2024–2025 figure to a source; preserve entity distinctions; forbid fabricated fills.

## Datasets

| File | Role |
|------|------|
| `transition_2024_2025_evidence.csv` | Gate 3 initial evidence table (SECONDARY / DERIVED / UNKNOWN) |
| `entity_split_2024_2025.csv` | Gate 3B expanded entity-level acquisition with comparability flags |
| `../events/competitive_events.csv` | Timeline events (PRIMARY/SECONDARY) |

Processed mirrors under `data/processed/structural_break/`.

## Hard rules

1. Never write “Tokopedia rose from 23% (2024) to 38% (2025).”
2. **2025 Combined Tokopedia + TikTok Shop ≠ Legacy Tokopedia.**
3. Do **not** present `Combined GMV − TTS Indonesia GMV` as observed Legacy Tokopedia GMV — free sources do **not** establish additivity.
4. APJII figures are **internet-user access shares**, not GMV market share.
5. Magpie IQ figures are **FMCG tracked GMV**, not national all-category GMV.
6. GoTo e-commerce service fee is **not** platform GMV.
7. Keep missing values missing.

## Source hierarchy used

| Type | Examples in this folder |
|------|-------------------------|
| PRIMARY | GoTo PR (2024-01-31); TikTok Newsroom (TTS pause, partnership, Seller Center); Momentum Works Low Down public note (rationalisation language); MW CEO quotes via Kompas |
| SECONDARY_HIGH | Digital in Asia MW tracker; Kompas APJII summary; Kontan/Bisnis GoTo fee quoting CFO |
| SECONDARY | Bisnis.com MW Indonesia share table |
| DERIVED | 2024 implied GMV from share×total; additive Combined 2024 baseline |
| UNKNOWN | Standalone Legacy Tokopedia 2025 GMV / share |

## Key verified claims (with URLs)

### Market position (Indonesia, MW via secondary)

- Source: https://teknologi.bisnis.com/read/20260508/266/1972413/shopee-kuasai-54-pasar-e-commerce-indonesia-transaksi-tembus-rp539-triliun
- 2024: Shopee 46% / ~$26B; Tokopedia 23%; TTS 11%; Indonesia $56.5B
- 2025: Shopee 54% / $31.2B; **Combined** Tokopedia+TTS 38% / ~$21.9B; Indonesia $57.7B

### TTS Indonesia GMV (TTS-labeled)

- Digital in Asia: https://digitalinasia.com/tiktok-shop-shopee-gmv-tracker/ — Indonesia TTS ~$13.1B (2025)
- Kompas: https://www.kompas.id/artikel/en-indonesia-menjadi-pasar-terbesar-kedua-bagi-tiktok-shop

### MW rationalisation (PRIMARY public excerpt)

- https://thelowdown.momentum.asia/new-report-southeast-asias-platform-ecommerce-reaches-us157-6b-in-2025-with-top-platforms-expanding-share-to-98-8/
- Indonesia slowdown: Bukalapak exit + **Tokopedia’s GMV rationalisation**
- Combined TTS (incl. Tokopedia) reached **65.7% of Shopee’s** SEA GMV; TTS platform GMV separately discussed in Digital in Asia as $45.6B SEA

### APJII access (NOT GMV)

- https://tekno.kompas.com/read/2025/08/11/10230017/6-platform-toko-online-paling-banyak-diakses-di-indonesia
- 2025 access: Shopee 53.22%; TTS 27.37%; Tokopedia 9.57% (vs 41.65% / 12.20% / 9.40%)

### GoTo fee on combined GMV

- https://investasi.kontan.co.id/news/berapa-kontribusi-cuan-tokopedia-ke-keuangan-goto-di-2025
- CFO: fee based on **combined** Tokopedia and TikTok Shop GMV; Rp820B (2025)

### Transaction / integration

- GoTo completion: https://www.gotocompany.com/en/news/press/goto-and-tiktok-announce-transaction-completion-formalizing-strategic-partnership-for-indonesia
- TikTok Seller Center: https://newsroom.tiktok.com/in-id/tokopedia-dan-tiktok-shop-seller-center-resmi-diluncurkan

## Rejected / corrected interpretations

| Claim | Why rejected |
|-------|----------------|
| Digivestasi / some blogs: Tokopedia ~9.6% and TTS ~27.4% as **GMV** share | Those figures match **APJII access** shares, not MW GMV |
| Bisnis text labeling SEA Combined GMV as US$45.6B | Conflicts with Digital in Asia / MW distinction that US$45.6B is **TTS platform** GMV; Combined-with-Tokopedia is a different measure |
| Residual Legacy 2025 = 21.9 − 13.1 | Additivity not established; **not used as observed data** |

## Acquisition date

Gate 3B curation access date: **2026-08-12**.

---

## Gate 4 exploratory analysis (2026-08-12)

**No new raw market-position numbers were fabricated.** Gate 4 consumes Gate 3B `entity_split_2024_2025` and primary timeline sources.

| Artifact | Path |
|----------|------|
| Structural analysis | `research/gate4_2025_structural_analysis.md` |
| Comeback final test | `research/tokopedia_comeback_final_test.md` |
| 2025 end-state | `research/2025_end_state.md` |
| Entity analysis table | `data/processed/gate4_entity_analysis.csv` |

**Gate 4 verdicts:** H1 UNSUPPORTED · H2 PARTIALLY SUPPORTED (structure) · H3 PARTIALLY SUPPORTED (strongest).  
Legacy Tokopedia 2025 standalone GMV/share remains **MISSING**.

---

## Gate 5 competitive analysis (2026-08-12)

**No new fabricated Legacy Tokopedia 2025 GMV/share.** Gate 5 formalizes competitive conclusions from Gate 3B/4 evidence.

| Artifact | Path |
|----------|------|
| Competitive analysis | `research/gate5_competitive_analysis.md` |
| Competitive end-state | `research/2025_competitive_end_state.md` |
| Hypothesis matrix | `research/hypothesis_evidence_matrix.md` |
| Reproducible claim table | `data/processed/gate5_competitive_analysis.csv` |

**Gate 5 conclusion:** Shopee consolidated leadership; Tokopedia-side challenger is Combined under TikTok-led signals — Legacy comeback **UNSUPPORTED**.

---

## Gate 5.5 — Final 2025 comparable data search (2026-08-12)

Final pass for public 2025 platform metrics comparable to 2022–2024.  
**Result:** Legacy Tokopedia 2025 GMV/share still **UNKNOWN**. See `data/raw/2025_comparable/` and `research/final_2025_data_search.md`.  
Gate 4/5 conclusions unchanged.
