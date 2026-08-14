# Final 2025 Data Search (Gate 5.5)

**Date:** 2026-08-12  
**Scope:** Final targeted pass for publicly accessible 2025 Indonesia platform-level data comparable to 2022–2024.  
**Constraint:** Does **not** reopen Gate 3B; does **not** modify Gate 4/5 conclusions; does **not** fabricate Legacy Tokopedia 2025 GMV/share.

---

# 1. Search Objective

Determine:

1. What 2025 platform-level data actually exists.  
2. Which metrics are **DIRECT** vs **CONDITIONAL** vs **NOT COMPARABLE** to 2022–2024.  
3. Whether **standalone Legacy Tokopedia 2025 GMV/share** can be obtained.  
4. The strongest defensible 2025 comparison point if that metric remains unavailable.

---

# 2. 2025 Data Successfully Found

| Metric | Entity | Value | Source type | Comparability |
|--------|--------|------:|-------------|---------------|
| GMV share | Shopee Indonesia | 54% | SECONDARY (MW via Bisnis) | **DIRECT** vs 2022–2024 Shopee MW shares |
| GMV | Shopee Indonesia | US$31.2B | SECONDARY | **DIRECT** vs Shopee 2024 ~$26B same family |
| GMV share / GMV | Combined Tokopedia+TTS | 38% / ~US$21.9B | SECONDARY | **NOT COMPARABLE** to Legacy Tokopedia |
| Total GMV | Indonesia market | US$57.7B (+2.2%) | SECONDARY_HIGH | **DIRECT** vs Indonesia 2024 $56.5B MW |
| GMV | TikTok Shop Indonesia | ~US$13.1B | SECONDARY_HIGH | **CONDITIONAL** (TTS-labeled; additivity vs Combined unproven) |
| Access share | Shopee / TTS / Legacy Tokopedia | 53.22% / 27.37% / 9.57% | SECONDARY_HIGH (APJII) | **CONDITIONAL** as access; **NOT** GMV |
| GMV share | Lazada / Blibli | 6% / 3% | SECONDARY | **DIRECT** vs 2024 MW shares |
| Service fee | GoTo (combined base) | Rp820B | SECONDARY_HIGH | **NOT COMPARABLE** to platform GMV |
| Rationalisation note | Tokopedia GMV (qualitative) | flagged | PRIMARY (MW public) | CONTEXT |
| BI ecommerce tx | Indonesia aggregate | Rp134.67T (2025Q3) | SECONDARY_HIGH | **NOT COMPARABLE** (aggregate/quarterly) |

Dataset: `data/raw/2025_comparable/platform_metrics_2025.csv`

---

# 3. 2025 Standalone Tokopedia Evidence

## Can standalone Legacy Tokopedia 2025 GMV/share be measured?

**NO — remains UNKNOWN.**

### Searched / checked

| Channel | Result |
|---------|--------|
| Momentum Works free reproductions (Bisnis, Business Times, TechNode, Databoks, MW Low Down) | 2025 Tokopedia-side reported as **Combined** Tokopedia+TTS only |
| GoTo IR / FY2025 briefings (CNBC, Kontan) | Fee on **combined** Tokopedia+TTS GMV; **no** Legacy GMV/share |
| BPS / Bank Indonesia | Aggregate ecommerce activity; **no** annual platform GMV split matching MW |
| Kemendag PMSE materials | Cite **2024** Statista/MW-style splits; not a new 2025 Legacy standalone |
| Digivestasi / some blogs (~9.6% / ~27.4%) | **Rejected** — matches APJII **access**, not GMV |

### Decision rule applied

> Standalone Legacy Tokopedia 2025 GMV/share is not publicly observable from the available evidence.

**STOP** searching for that same metric without a new primary disclosure.  
Do **not** reconstruct via Combined − TTS.

---

# 4. Shopee 2025 Evidence

| Metric | Value | Comparability to 2022–24 |
|--------|------:|--------------------------|
| GMV share | 54% (vs 46% in 2024; 40% in 2023; 36% in 2022 MW series) | **DIRECT** (MW secondary family) |
| GMV | US$31.2B (vs ~$26B 2024) | **DIRECT** |
| APJII access | 53.22% (vs 41.65%) | **CONDITIONAL** (access series) |

**Strongest 2025 comparable metric overall:** **Shopee Indonesia GMV share (MW secondary family)** — continuous entity definition across 2022–2025.

---

# 5. TikTok Shop 2025 Evidence

| Metric | Value | Notes |
|--------|------:|-------|
| TTS-labeled Indonesia GMV | ~US$13.1B | OBSERVED SECONDARY_HIGH |
| Standalone TTS GMV share (MW Indonesia 2025 table) | **MISSING** | Combined published instead |
| APJII access | 27.37% (vs 12.20%) | Access ≠ GMV |
| SEA TTS platform GMV | US$45.6B | Regional CONTEXT; carefully not Combined |

Keep TTS separate from Legacy Tokopedia and from Combined.

---

# 6. Combined Tokopedia + TikTok Shop Evidence

| Metric | Value | Comparability |
|--------|------:|---------------|
| GMV share | 38% | **NOT COMPARABLE** to Legacy Tokopedia 2022–2024 |
| GMV | ~US$21.9B | Same |
| vs additive 2024 Combined (23+11=34%) | +4 pp | **CONDITIONAL** DERIVED baseline |

**Mandatory:** Combined ≠ Legacy Tokopedia.

---

# 7. Indonesia Market Evidence

| Metric | Value | Comparability |
|--------|------:|---------------|
| Total platform GMV | US$57.7B | **DIRECT** vs 2024 $56.5B MW |
| YoY growth | +2.2% | **DIRECT** |
| MW explanation | Bukalapak exit + Tokopedia GMV rationalisation | OBSERVED qualitative |
| BI Q3 2025 ecommerce tx | Rp134.67T | **NOT COMPARABLE** to annual MW GMV |

---

# 8. Comparability Matrix

| Metric | Entity | 2025 Value | Source | Source Type | Methodology | Comparable to 2022–24? | Comparability | Notes |
|--------|--------|-----------:|--------|-------------|-------------|------------------------|---------------|-------|
| GMV share | Shopee | 54% | Bisnis/MW | SECONDARY | Platform GMV share | Yes | **DIRECT** | Best continuous series |
| GMV | Shopee | $31.2B | Bisnis/MW | SECONDARY | Platform GMV | Yes (2024) | **DIRECT** | |
| Total GMV | Indonesia | $57.7B | MW family | SECONDARY_HIGH | Platform total | Yes | **DIRECT** | |
| GMV share | Lazada | 6% | Bisnis/MW | SECONDARY | Platform GMV share | Yes | **DIRECT** | |
| GMV share | Blibli | 3% | Bisnis/MW | SECONDARY | Platform GMV share | Yes | **DIRECT** | |
| GMV share | Combined Tokopedia+TTS | 38% | Bisnis/MW | SECONDARY | Combined entity | No vs Legacy | **NOT COMPARABLE** | Structural break |
| GMV | Combined | $21.9B | Bisnis/MW | SECONDARY | Combined | No vs Legacy | **NOT COMPARABLE** | |
| GMV | TTS Indonesia | $13.1B | DIA/Kompas/MW | SECONDARY_HIGH | TTS-labeled | Partial | **CONDITIONAL** | Not Legacy; additivity vs Combined unproven |
| GMV share | Legacy Tokopedia | MISSING | — | UNKNOWN | — | No | **NOT COMPARABLE** | Keep missing |
| GMV | Legacy Tokopedia | MISSING | — | UNKNOWN | — | No | **NOT COMPARABLE** | Keep missing |
| Access | Shopee/TTS/Tokopedia | 53.22/27.37/9.57 | APJII | SECONDARY_HIGH | Survey access | Access YoY only | **CONDITIONAL** | ≠ GMV |
| Fee | GoTo | Rp820B | GoTo via press | SECONDARY_HIGH | Combined GMV fee | No | **NOT COMPARABLE** | ≠ GMV |
| BI tx | Indonesia | Rp134.67T Q3 | BI | SECONDARY_HIGH | Aggregate quarterly | No | **NOT COMPARABLE** | |

---

# 9. Remaining Data Gaps

1. Standalone Legacy Tokopedia 2025 **GMV**  
2. Standalone Legacy Tokopedia 2025 **GMV share**  
3. Standalone TTS 2025 **GMV share** in MW Indonesia table  
4. Confirmed additivity of TTS $13.1B inside Combined $21.9B  
5. Google Trends (still blocked/manual)  
6. Free long-run traffic / national seller counts  
7. Primary paid MW full matrices (not acquired; no paywall bypass)

---

# 10. Recommended 2025 Analytical Representation

**Do not force a continuous Legacy Tokopedia line through 2025.**

Recommended structure for final analysis / future Gate 6 inputs:

### 2022–2024 — historical competitive trajectory
- Platform-level MW secondary series: Shopee, Legacy Tokopedia, TTS (where published), Indonesia total  
- Grain: annual × entity  
- Entity definitions: **standalone**

### 2025 — observed end-state with structural break
1. **DIRECT comparable:** Shopee share/GMV; Indonesia total; Lazada/Blibli shares  
2. **Structural-break panel:** Combined Tokopedia+TTS (38% / $21.9B) — labeled Combined  
3. **TTS-labeled panel:** TTS Indonesia GMV ~$13.1B (CONDITIONAL)  
4. **Supporting non-GMV:** APJII access (Shopee / TTS / Legacy Tokopedia)  
5. **Explicit UNKNOWN:** Legacy Tokopedia 2025 GMV and share  

```
2022–2024:  Shopee vs Legacy Tokopedia vs TTS (standalone)
2025:       Shopee vs Combined Tokopedia+TTS  (+ TTS-labeled GMV)  [BREAK]
            Legacy Tokopedia GMV/share = UNKNOWN
```

Gate 4/5 conclusions are **unchanged** by this search: H1 Legacy comeback remains unsupported; H3 remains strongest partial reading; Combined ≠ Legacy.

---

## Gate 5.5 status

**FINAL 2025 SEARCH COMPLETE — LEGACY TOKOPEDIA 2025 GMV/SHARE STILL UNKNOWN**

Ready for Gate 6 **only if** forecasting/scenarios explicitly encode the structural break and keep Legacy 2025 GMV missing (or wait for primary MW entity-split). Still **no SQL/dashboard**.
