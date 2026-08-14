import { describe, expect, it } from "vitest";
import {
  FILTER_ALL,
  filterPanel,
  formatValue,
  isFilterActive,
  type PanelRow,
} from "./dashboardData";
import {
  chartEntityLabel,
  comparabilityLabel,
  entityLabel,
  metricLabel,
  sortTrackedEntities,
  statusLabel,
} from "./labels";

describe("formatValue", () => {
  it("renders Unknown for null", () => {
    expect(formatValue(null)).toBe("Unknown");
  });

  it("renders Unknown when status is UNKNOWN even if a number sneaks in", () => {
    expect(formatValue(0, "UNKNOWN")).toBe("Unknown");
  });

  it("renders observed numbers", () => {
    expect(formatValue(54)).toBe("54");
    expect(formatValue(9.57)).toBe("9.6");
  });
});

describe("filterPanel", () => {
  const rows: PanelRow[] = [
    {
      year: 2025,
      analytical_entity: "Legacy Tokopedia",
      metric: "market_share_pct",
      value: null,
      value_status: "UNKNOWN",
    },
    {
      year: 2025,
      analytical_entity: "Shopee",
      metric: "market_share_pct",
      value: 54,
      value_status: "OBSERVED",
    },
  ];

  it("filters UNKNOWN without coercing null to zero", () => {
    const out = filterPanel(rows, { value_status: "UNKNOWN" });
    expect(out).toHaveLength(1);
    expect(out[0].value).toBeNull();
  });

  it("treats all as unrestricted", () => {
    expect(filterPanel(rows, { marketplace: FILTER_ALL })).toHaveLength(2);
  });
});

describe("presentation labels", () => {
  it("maps internal enums to human labels", () => {
    expect(metricLabel("market_share_pct")).toBe("Market Share");
    expect(metricLabel("gmv_estimate_usd_billion")).toBe("GMV Estimate (USD bn)");
    expect(statusLabel("OBSERVED")).toBe("Observed");
    expect(statusLabel("UNKNOWN")).toBe("Unknown");
    expect(comparabilityLabel("NOT COMPARABLE")).toBe("Not Comparable");
  });

  it("keeps chart Combined short but entity full", () => {
    expect(chartEntityLabel("Combined Tokopedia + TikTok Shop")).toBe("Combined");
    expect(entityLabel("Combined Tokopedia + TikTok Shop")).toBe(
      "Combined Tokopedia + TikTok Shop",
    );
  });

  it("orders tracked marketplaces canonically", () => {
    expect(
      sortTrackedEntities([
        "TikTok Shop",
        "Combined Tokopedia + TikTok Shop",
        "Shopee",
        "Legacy Tokopedia",
      ]),
    ).toEqual([
      "Shopee",
      "Legacy Tokopedia",
      "TikTok Shop",
      "Combined Tokopedia + TikTok Shop",
    ]);
  });

  it("detects active filters", () => {
    expect(
      isFilterActive({
        year: FILTER_ALL,
        marketplace: FILTER_ALL,
        metric: FILTER_ALL,
        value_status: FILTER_ALL,
        comparability: FILTER_ALL,
      }),
    ).toBe(false);
    expect(
      isFilterActive({
        year: "2025",
        marketplace: FILTER_ALL,
        metric: FILTER_ALL,
        value_status: FILTER_ALL,
        comparability: FILTER_ALL,
      }),
    ).toBe(true);
  });
});
