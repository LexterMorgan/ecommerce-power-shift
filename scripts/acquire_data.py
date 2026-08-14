#!/usr/bin/env python3
"""Acquire / refresh open datasets that can be pulled programmatically.

Currently refreshes World Bank Indonesia macro indicators.
Google Trends automated pull is rate-limited; see data/raw/google_trends/README_MANUAL_EXPORT.md.
Market-position / events / company context are curated CSVs (not scraped).
"""
from __future__ import annotations

import csv
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "raw" / "macro"

INDICATORS = {
    "NY.GDP.MKTP.CD": "GDP (current US$)",
    "NY.GDP.MKTP.KD.ZG": "GDP growth (annual %)",
    "NE.CON.PRVT.ZS": "Households and NPISHs final consumption expenditure (% of GDP)",
    "FP.CPI.TOTL.ZG": "Inflation, consumer prices (annual %)",
    "IT.NET.USER.ZS": "Individuals using the Internet (% of population)",
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for code, name in INDICATORS.items():
        url = f"https://api.worldbank.org/v2/country/IDN/indicator/{code}?format=json&date=2015:2025&per_page=100"
        with urllib.request.urlopen(url, timeout=60) as resp:
            payload = json.loads(resp.read().decode())
        (OUT / f"worldbank_{code.replace('.', '_')}_meta.json").write_text(
            json.dumps(
                {
                    "url": url,
                    "acquired_at": datetime.now(timezone.utc).isoformat(),
                    "indicator": code,
                    "name": name,
                },
                indent=2,
            )
        )
        (OUT / f"worldbank_{code.replace('.', '_')}.json").write_text(json.dumps(payload, indent=2))
        for item in payload[1] or []:
            rows.append(
                {
                    "indicator_code": code,
                    "indicator_name": name,
                    "country": "Indonesia",
                    "country_iso3": "IDN",
                    "year": item.get("date"),
                    "value": item.get("value"),
                    "source": "World Bank Open Data API",
                    "source_url": url,
                }
            )
    csv_path = OUT / "worldbank_indonesia_indicators_extract.csv"
    with csv_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {len(rows)} rows to {csv_path}")


if __name__ == "__main__":
    main()
