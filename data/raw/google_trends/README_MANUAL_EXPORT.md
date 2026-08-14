# Google Trends — manual acquisition instructions

Automated Google Trends extraction was attempted on 2026-08-12 and encountered repeated HTTP 429 rate limits on the multiline widget endpoint and the public explore page.

## Required manual export

1. Open: https://trends.google.com/trends/explore?date=today%205-y&geo=ID&q=Shopee,Tokopedia
2. Confirm:
   - Geography: Indonesia
   - Time: Past 5 years (or custom starting 2019-01-01 if available)
   - Category: All categories
   - Search type: Web Search
3. Download the Interest over time CSV.
4. Save as:

`data/raw/google_trends/google_trends_indonesia_shopee_tokopedia_manual.csv`

Expected columns (Google export may include extra header rows):

- Week or Day / Month
- Shopee
- Tokopedia

The processing script accepts either the manual filename above or any `*.csv` in this folder that contains Shopee and Tokopedia columns.

## Important

Google Trends is a relative attention index (0–100), not market share, GMV, or revenue.
