# Source Audit Log

**Project:** E-Commerce Power Shift: Shopee vs Tokopedia in Indonesia  
**Milestone:** Gate 1 — Data Availability Audit  
**Date investigated:** 2026-08-12  
**Investigator workflow:** Cursor + Grok (implementation/research execution)  
**Scope:** Availability audit only — **no datasets acquired**, no pipeline, no analysis results.

Primary research question: How did Shopee's competitive position in Indonesia change relative to Tokopedia, and what observable market factors help explain that shift?

**Neutrality note:** Sources were checked for evidence that could support **or** contradict narratives of Shopee dominance, Tokopedia resilience, structural breaks (GoTo/TikTok), or macro-driven market change. No predetermined causal explanation was assumed.

---

## A. Market share / GMV

### A1. Momentum Works — Ecommerce in Southeast Asia (public summaries + report pages)

- **Source:** Momentum Works annual ecommerce SEA reports and The Low Down posts
- **URL:** https://thelowdown.momentum.asia/new-report-southeast-asias-platform-ecommerce-reaches-us157-6b-in-2025-with-top-platforms-expanding-share-to-98-8/ ; https://thelowdown.momentum.asia/press-release-southeast-asia-ecommerce-achieves-us114-6-billion-gmv-in-2023-momentum-works/ ; https://momentum.asia/insights/detail/ecommerce-in-southeast-asia-2024 ; older: https://thelowdown.momentum.asia/new-report-ecommerce-in-southeast-asia-achieved-us-100-billion-gmv-in-2022/
- **Date investigated:** 2026-08-12
- **What was searched:** SEA/Indonesia ecommerce GMV, Shopee vs Tokopedia platform share, report access model
- **What was found:** Multi-year annual research programme estimating platform GMV and shares; public posts summarize SEA totals and some platform/country headlines; full reports sold as decision-support products; Indonesia often identified as largest market; platform competitive dynamics including Shopee, Tokopedia, Lazada, TikTok Shop discussed; later coverage treats TikTok Shop with Tokopedia as a combined competitive force in places
- **Relevant metrics:** Platform GMV; market share; country GMV
- **Time period:** Report editions covering roughly early-2020s through 2025 data years
- **Geography:** Southeast Asia with country breakdowns including Indonesia
- **Granularity:** Annual
- **Accessibility:** Partial free summaries; detailed matrices typically paid
- **Reliability:** Tier 2 (original industry research estimates)
- **Limitations:** Not official company data; methodology not fully public in free materials; restatements possible; entity definitions shift after TikTok–Tokopedia combination
- **Use later?** **Yes — primary candidate** for Indonesia competitive GMV/share if full or sufficiently cited Indonesia platform series acquired in Gate 2
- **Inclusion reason:** Best investigated source family for direct platform comparison over time

### A2. Secondary reproductions of Momentum Works (Bisnis, Databoks, Business Times, Digital in Asia)

- **Source:** News/data portals citing Momentum Works
- **URL examples:** https://teknologi.bisnis.com/read/20260508/266/1972413/shopee-kuasai-54-pasar-e-commerce-indonesia-transaksi-tembus-rp539-triliun ; https://databoks.katadata.co.id/en/technology-telecommunications/statistics/69e1a07207d12/indonesia-remains-southeast-asias-largest-e-commerce-market-in-2025 ; https://www.businesstimes.com.sg/international/asean/south-east-asia-e-commerce-gmv-grows-us157-6-billion-2025 ; https://digitalinasia.com/tiktok-shop-shopee-gmv-tracker/
- **Date investigated:** 2026-08-12
- **What was searched:** Indonesia-specific Shopee/Tokopedia share figures attributed to MW
- **What was found:** Articles reproduce selected annual figures and Indonesia market totals; some claim Indonesia platform shares; trackers mix SEA and Indonesia concepts — must not be averaged casually
- **Relevant metrics:** Reported GMV/share excerpts
- **Time period:** Article-specific years
- **Geography:** SEA and/or Indonesia depending on article
- **Granularity:** Annual excerpts
- **Accessibility:** Generally free; some portals may soft-gate
- **Reliability:** Tier 3 (secondary)
- **Limitations:** Not original publisher; transcription risk; incomplete methodology
- **Use later?** **Conditional** — only to locate/verify pointers back to MW originals; prefer buying/capturing original report tables
- **Inclusion/exclusion:** Include as citation bridge, not as primary truth

### A3. Official monthly Indonesia platform GMV

- **Source:** Searched via Sea filings, GoTo filings, government stats
- **URL:** N/A (absence)
- **Date investigated:** 2026-08-12
- **What was searched:** Official monthly Shopee Indonesia GMV and Tokopedia GMV
- **What was found:** **NOT PUBLICLY AVAILABLE** as a continuous official dyad
- **Use later?** No as official monthly series
- **Exclusion reason:** Verified gap

---

## B. Company financial / operating disclosures

### B1. Sea Limited — investor releases & SEC materials

- **Source:** Sea Limited IR and SEC exhibits
- **URL:** https://www.sea.com/investor/home ; example FY2025 results exhibit https://www.sec.gov/Archives/edgar/data/1703399/000119312526088151/d106475dex991.htm ; Form 20-F archives via SEC/aggregators
- **Date investigated:** 2026-08-12
- **What was searched:** Shopee GMV, orders, revenue, Indonesia breakouts
- **What was found:** Regular quarterly/annual disclosure of Shopee GMV, gross orders, GAAP marketplace revenue; glossary defines GMV and orders; geographic revenue tables exist at company level in 20-F materials reviewed, but **standalone Indonesia Shopee GMV series was not verified as a standard public disclosure**
- **Relevant metrics:** GMV; orders; Shopee revenue; adjusted EBITDA (segment)
- **Time period:** Multi-year quarterly history
- **Geography:** Multi-market Shopee footprint
- **Granularity:** Quarterly / annual
- **Accessibility:** Free
- **Reliability:** Tier 1
- **Limitations:** Not Indonesia-only; not comparable to Tokopedia disclosures
- **Use later?** **Yes — contextual Shopee company performance**, with geography caveat
- **Inclusion reason:** Highest-quality Shopee operating definitions and history

### B2. GoTo — earnings, presentations, press

- **Source:** GoTo company newsroom / IR materials
- **URL:** https://www.gotocompany.com/en/news/press/goto-group-achieves-record-profitability-and-strong-growth-as-it-reports-2025-first-quarter-earnings ; FY25 materials referenced via earnings transcripts/presentations; glossary in presentations defines GTV/Core GTV
- **Date investigated:** 2026-08-12
- **What was searched:** Tokopedia GTV, ecommerce metrics, post-TikTok disclosure
- **What was found:** After TikTok transaction completion, Tokopedia is not consolidated like before; GoTo reports **e-commerce service fee from Tokopedia**; Core GTV / GTV definitions **exclude Tokopedia** from remaining e-commerce platforms; management notes fee linked to combined Tokopedia + TikTok Shop GMV scale without publishing that full GMV as GoTo GTV
- **Relevant metrics:** GTV; Core GTV; e-commerce service fee; ATU
- **Time period:** Multi-year with **Jan 2024 structural break**
- **Geography:** Indonesia-focused group
- **Granularity:** Quarterly
- **Accessibility:** Free
- **Reliability:** Tier 1
- **Limitations:** Post-deal Tokopedia GMV not fully public via GoTo; fee ≠ GMV; ecosystem users ≠ Tokopedia buyers
- **Use later?** **Yes — structural break + residual fee series**; **not** as clean Tokopedia GMV vs Shopee
- **Inclusion reason:** Essential for understanding what can/cannot be compared after 2024

### B3. Sea GMV vs GoTo GTV comparability check

- **Result:** **NOT COMPARABLE** for Indonesia competitive share
- **Reason:** Different metrics, geographies, and disclosure scopes; combining them would fabricate a false dyad

---

## C. Consumer search interest

### C1. Google Trends

- **Source:** Google Trends
- **URL:** https://trends.google.com/trends/ ; export help https://support.google.com/trends/answer/4365538 ; FAQ https://support.google.com/trends/answer/4365533
- **Date investigated:** 2026-08-12
- **What was searched:** Availability of Indonesia geo, multi-term compare, CSV export, limitations; terms Shopee / Tokopedia / variants
- **What was found:** Indonesia geography supported; multi-term comparison on shared 0–100 scale; CSV export documented by Google Help; data are sampled relative interest, not absolute volume; academic work (JIMU) demonstrates Indonesia platform keyword exports are used in research practice. Direct Trends explore fetch returned HTTP 429 during this audit — **capability still verified via official help docs and secondary research use**, with Gate 2 acquisition to perform the actual export.
- **Relevant metrics:** Relative search interest
- **Time period:** Multi-year selectable ranges
- **Geography:** Indonesia (`ID`)
- **Granularity:** Depends on range (daily/weekly/monthly)
- **Accessibility:** Free
- **Reliability:** Tier 5
- **Limitations:** Not market share; query choice; normalization; sampling
- **Use later?** **Yes — primary free dyad attention series**
- **Inclusion reason:** Reproducible, comparable across brands, Indonesia-scoped

### C2. Academic Trends usage (method reference)

- **Source:** JIMU article on Indonesia e-commerce platform popularity via Google Trends
- **URL:** https://ejurnal.ubharajaya.ac.id/index.php/JIMU/article/view/5324
- **Date investigated:** 2026-08-12
- **What was found:** Confirms feasibility of Indonesia multi-platform Trends collection and explicitly warns Trends ≠ transactions
- **Use later?** Method reference only
- **Inclusion reason:** Supports audit claim that Trends export is practically usable

---

## D. Web traffic / engagement

### D1. Similarweb

- **Source:** Similarweb packaging & developer docs
- **URL:** https://www.similarweb.com/packages/web/?type=Individuals ; https://developers.similarweb.com/docs/websites-dataset
- **Date investigated:** 2026-08-12
- **What was searched:** Free vs paid historical depth; Indonesia country filter; visit metrics
- **What was found:** Free web insights are shallow/high-level; paid packages unlock longer history (plan-dependent; developer materials claim up to ~61 months); metrics include visits and engagement; estimates
- **Relevant metrics:** Visits; engagement; geo distribution
- **Time period:** Short on free; multi-year on paid
- **Geography:** Country filters on paid products
- **Granularity:** Typically monthly
- **Accessibility:** Free limited; historical **paid**
- **Reliability:** Tier 4
- **Limitations:** Paid wall for useful history; estimates; traffic ≠ GMV
- **Use later?** **Only if paid access approved** or for labeled short snapshots — do not pretend paid history is in hand
- **Exclusion as default free dataset:** Insufficient free historical depth for long competitive audit

### D2. iPrice Map of eCommerce (historical)

- **Source:** iPrice historical Map of eCommerce / secondary reports
- **URL:** https://boxme.asia/wp-content/uploads/2019/12/iPrice-SE-Asia-Map-of-Ecommerce-Q3-2019.pdf ; https://techwireasia.com/2021/10/tokopedia-reclaim-its-position-from-shopee-as-the-most-visited-e-commerce-site-in-indonesia/ ; academic table reproductions citing iprice.co.id insights
- **Date investigated:** 2026-08-12
- **What was searched:** Historical Indonesia visit rankings for Shopee vs Tokopedia
- **What was found:** Public historical quarterly rankings existed and sometimes showed leadership flips in visits; continuity of a current official updating product was **not** verified in this pass
- **Relevant metrics:** Monthly web visits / rankings; some app rankings in editions
- **Time period:** Roughly 2019–2022 publicly evidenced; later continuity uncertain
- **Geography:** Indonesia
- **Granularity:** Quarterly snapshots
- **Accessibility:** Historical PDFs/articles free; full reconstruction effort required
- **Reliability:** Tier 4
- **Limitations:** Incomplete archive; traffic ≠ GMV
- **Use later?** **Conditional** historical traffic panel if tables can be recovered with citations
- **Inclusion reason:** One of few public historical dyad traffic series

---

## E. Government / regulatory

### E1. BPS Statistik E-Commerce

- **Source:** Badan Pusat Statistik publications
- **URL:** https://www.bps.go.id/id/publication/2025/11/28/647323224ecc656c2933571b/statistik-e-commerce-2024.html ; https://www.bps.go.id/id/publication/2025/01/30/d52af11843aee401403ecfa6/statistik-e-commerce-2023.html
- **Date investigated:** 2026-08-12
- **What was searched:** Official e-commerce statistics; platform shares
- **What was found:** Annual publications on e-commerce business profiles, workers, activity, transaction/revenue indicators; provincial estimates; **not** Shopee vs Tokopedia market share
- **Relevant metrics:** Sector e-commerce statistics
- **Time period:** Multi-year publication series
- **Geography:** Indonesia
- **Granularity:** Annual
- **Accessibility:** Free downloads
- **Reliability:** Tier 1
- **Limitations:** Not platform-competitive
- **Use later?** **Yes — macro context**
- **Inclusion reason:** Official adoption/sector backdrop

### E2. Bank Indonesia payment / e-commerce monitoring

- **Source:** BI SPIP + RDG press reporting
- **URL:** https://www.bi.go.id/id/statistik/ekonomi-keuangan/spip/Default.aspx ; example press https://www.antaranews.com/berita/5052357/bi-catat-transaksi-e-commerce-tembus-rp444-triliun-per-juli-2025
- **Date investigated:** 2026-08-12
- **What was searched:** Official e-commerce transaction value/volume; platform split
- **What was found:** Aggregate e-commerce transaction indicators reported; rich digital payments statistics; **no verified public Shopee/Tokopedia split**
- **Relevant metrics:** Aggregate e-commerce value/volume; QRIS/e-money/etc.
- **Time period:** Ongoing
- **Geography:** Indonesia
- **Granularity:** Monthly / as published
- **Accessibility:** Free
- **Reliability:** Tier 1
- **Limitations:** Aggregate only
- **Use later?** **Yes — macro/payments context**
- **Inclusion reason:** Official demand/payments environment

### E3. Ministry of Trade Regulation No. 31 of 2023 (social commerce restrictions)

- **Source:** Legal explainers + news on Mot Regulation 31/2023
- **URL:** https://www.allenandgledhill.com/sg/publication/articles/26694/bans-e-commerce-sales-on-social-media-platforms ; https://apnews.com/article/indonesia-tiktok-ecommerce-ban-china-62e5ef9f366d8cfd4a94427393bb5aba
- **Date investigated:** 2026-08-12
- **What was searched:** Regulatory change affecting social commerce / TikTok Shop
- **What was found:** Regulation dated 26 Sep 2023 restricting social-commerce payment facilitation; contemporaneous reporting that TikTok paused Shop transactions in Indonesia; later Tokopedia partnership enabled structured re-entry path
- **Relevant metrics:** Event (not a performance series)
- **Time period:** Sep–Oct 2023 episode
- **Geography:** Indonesia
- **Granularity:** Point-in-time
- **Accessibility:** Explainers free; capture official regulation text in Gate 2
- **Reliability:** Tier 1 (regulation) / Tier 3 (news)
- **Limitations:** Event ≠ proven cause of share shifts
- **Use later?** **Yes — event timeline**
- **Inclusion reason:** Major observable market/regulatory factor candidate (hypothesis only)

---

## F. Industry research (non-MW)

### F1. e-Conomy SEA (Google / Temasek / Bain)

- **Source:** Annual digital economy report
- **URL:** https://www.bain.com/insights/e-conomy-sea-2025/ ; https://blog.google/company-news/inside-google/around-the-globe/google-asia/sea-economy-2025/ ; https://www.temasek.com.sg/en/news-and-resources/news-room/news/2025/e-conomy-sea-2025-report-aseans-digital-economy-poised-to-surpass-300-billion
- **Date investigated:** 2026-08-12
- **What was searched:** Indonesia e-commerce GMV and platform shares
- **What was found:** Strong sector/country digital economy GMV and thematic insights; **not** a verified free Shopee-vs-Tokopedia share panel comparable to MW marketplace tracking
- **Relevant metrics:** Digital economy / e-commerce sector GMV (aggregate)
- **Time period:** Annual since 2016
- **Geography:** SEA/ASEAN including Indonesia
- **Granularity:** Annual
- **Accessibility:** Free report materials
- **Reliability:** Tier 2
- **Limitations:** Wrong unit of analysis for platform dyad
- **Use later?** **Yes — macro context only**
- **Inclusion reason:** Reputable Indonesia digital-economy backdrop

### F2. Redseer / McKinsey public Indonesia decks

- **Source:** Consultancy excerpts
- **Date investigated:** 2026-08-12
- **What was searched:** Free continuous Shopee vs Tokopedia historical quantitative panels
- **What was found:** No freely verified continuous comparable dyad series suitable as a primary dataset in this pass
- **Use later?** Not as primary until a specific public artifact is verified
- **Exclusion reason:** Insufficient verified open quantitative continuity

---

## G. Competitive events (context — not causes)

| Date | Event | Affected | Potential relevance | Source (primary preferred) | Use as cause? |
|------|-------|----------|---------------------|----------------------------|---------------|
| May 2021 | Gojek–Tokopedia combination into GoTo announced/finalized (merger period) | Tokopedia / GoTo | Ownership/strategy structure | Company history / reputable coverage (e.g. Wikipedia summary pointing to contemporaneous reporting) | No — hypothesis context only |
| 11 Apr 2022 | GoTo IPO / IDX listing | GoTo / Tokopedia ecosystem | Capital markets / strategy phase | https://www.businesswire.com/news/home/20220410005062/en/GoTo-Completes-Landmark-Listing-on-the-Indonesia-Stock-Exchange ; Reuters debut coverage | No |
| 26 Sep 2023 | Mot Regulation 31/2023 on e-commerce/social commerce | Social commerce operators incl. TikTok Shop | Regulatory constraint on social-commerce checkout | Legal explainers + AP | No |
| Oct 2023 | TikTok pauses Shop retail transactions in Indonesia (per reporting) | TikTok Shop | Temporary channel disruption | AP News | No |
| 31 Jan 2024 | GoTo–TikTok transaction completion; Tokopedia + TikTok Shop Indonesia combined under PT Tokopedia; TikTok controlling stake | Tokopedia, TikTok, GoTo | Major structural break for Tokopedia metrics and competitive set | https://www.gotocompany.com/en/news/press/goto-and-tiktok-announce-transaction-completion-formalizing-strategic-partnership-for-indonesia ; Reuters https://www.reuters.com/technology/tiktok-completes-deal-indonesias-top-e-commerce-platform-2024-01-31/ | No |

---

## H. Sources checked and rejected / deprioritized

| Source | Why rejected or deprioritized |
|--------|-------------------------------|
| Proprietary Shopee/Tokopedia internal data | Out of scope; not public |
| Inferring market share from Google Trends | Explicitly forbidden by methodology; Trends ≠ share |
| Free Similarweb as long-run dyad | Historical depth insufficient without paid plan |
| Unverified aggregator trackers mixing SEA & Indonesia | High risk of non-comparable mashups |
| Redseer/McKinsey without a specific free verified series | Not enough open continuity verified this pass |
| Fabricated monthly interpolation of annual MW figures | Forbidden |

---

## I. Access limitations encountered

1. Momentum Works full Indonesia platform matrices largely behind purchase.
2. Similarweb useful history behind subscription.
3. Google Trends live explore endpoint returned **429** during automated fetch; export still documented as available via UI for Gate 2.
4. Some news portals may soft-paywall; originals preferred.
5. Official Mot regulation text should be captured from official channels in Gate 2 (this audit relied partly on reputable legal/news explainers).

---

## J. Audit conclusion (availability only)

**Most valuable verified sources for the research question:**

1. Momentum Works Indonesia platform GMV/share estimates (paid/partial public)
2. Google Trends Indonesia Shopee vs Tokopedia
3. Primary event sources (GoTo PR, regulation/news on Mot 31, TikTok Shop pause)
4. Sea + GoTo filings for non-comparable but important context and structural breaks
5. BPS / BI / e-Conomy for macro context

**Do not acquire datasets in this milestone.** Gate 2 should acquire only the Recommended Analytical Dataset listed in `docs/DATA_AVAILABILITY.md`.
