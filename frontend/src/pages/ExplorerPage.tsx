import { useMemo, useState } from "react";
import {
  FILTER_ALL,
  filterPanel,
  formatValue,
  isFilterActive,
} from "../lib/dashboardData";
import {
  comparabilityLabel,
  confidenceLabel,
  entityLabel,
  metricLabel,
  sortTrackedEntities,
  statusLabel,
} from "../lib/labels";
import { useDashboard } from "../lib/DashboardContext";
import { PageHeader, StatusBadge } from "../components/Ui";

const DEFAULT_FILTERS = {
  year: FILTER_ALL,
  marketplace: FILTER_ALL,
  metric: FILTER_ALL,
  valueStatus: FILTER_ALL,
  comparability: FILTER_ALL,
};

export function ExplorerPage() {
  const { data, error, loading } = useDashboard();
  const [year, setYear] = useState(DEFAULT_FILTERS.year);
  const [marketplace, setMarketplace] = useState(DEFAULT_FILTERS.marketplace);
  const [metric, setMetric] = useState(DEFAULT_FILTERS.metric);
  const [valueStatus, setValueStatus] = useState(DEFAULT_FILTERS.valueStatus);
  const [comparability, setComparability] = useState(DEFAULT_FILTERS.comparability);

  const options = useMemo(() => {
    const keys = data?.filter_keys ?? [];
    const markets = sortTrackedEntities(
      Array.from(new Set(keys.map((k) => String(k.marketplace)))),
    );
    return {
      years: Array.from(new Set(keys.map((k) => String(k.year)))).sort(),
      markets,
      metrics: Array.from(new Set(keys.map((k) => String(k.metric)))).sort(),
      statuses: Array.from(new Set(keys.map((k) => String(k.value_status)))).sort(),
      comps: Array.from(new Set(keys.map((k) => String(k.comparability)))).sort(),
    };
  }, [data]);

  const filters = { year, marketplace, metric, value_status: valueStatus, comparability };
  const active = isFilterActive(filters);

  const rows = useMemo(() => {
    if (!data) return [];
    return filterPanel(data.competitive_panel, filters);
  }, [data, year, marketplace, metric, valueStatus, comparability]);

  const resetFilters = () => {
    setYear(DEFAULT_FILTERS.year);
    setMarketplace(DEFAULT_FILTERS.marketplace);
    setMetric(DEFAULT_FILTERS.metric);
    setValueStatus(DEFAULT_FILTERS.valueStatus);
    setComparability(DEFAULT_FILTERS.comparability);
  };

  if (error) return <div className="error">{error}</div>;
  if (loading || !data) return <div className="loading">Loading panel explorer…</div>;

  const total = data.competitive_panel.length;

  return (
    <div>
      <PageHeader title="Data explorer">
        Inspect the scoped competitive panel (Shopee, Legacy Tokopedia, TikTok Shop, Combined
        Tokopedia + TikTok Shop). Unknown values stay Unknown — never coerced to zero.
      </PageHeader>

      <div className="panel">
        <div className="filters-toolbar">
          <div className="filters">
            <label>
              Year
              <select value={year} onChange={(e) => setYear(e.target.value)}>
                <option value={FILTER_ALL}>All</option>
                {options.years.map((y) => (
                  <option key={y} value={y}>
                    {y}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Marketplace
              <select value={marketplace} onChange={(e) => setMarketplace(e.target.value)}>
                <option value={FILTER_ALL}>All</option>
                {options.markets.map((m) => (
                  <option key={m} value={m}>
                    {entityLabel(m)}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Metric
              <select value={metric} onChange={(e) => setMetric(e.target.value)}>
                <option value={FILTER_ALL}>All</option>
                {options.metrics.map((m) => (
                  <option key={m} value={m}>
                    {metricLabel(m)}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Value status
              <select value={valueStatus} onChange={(e) => setValueStatus(e.target.value)}>
                <option value={FILTER_ALL}>All</option>
                {options.statuses.map((s) => (
                  <option key={s} value={s}>
                    {statusLabel(s)}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Comparability
              <select value={comparability} onChange={(e) => setComparability(e.target.value)}>
                <option value={FILTER_ALL}>All</option>
                {options.comps.map((c) => (
                  <option key={c} value={c}>
                    {comparabilityLabel(c)}
                  </option>
                ))}
              </select>
            </label>
          </div>
          {active ? (
            <button type="button" className="btn-ghost" onClick={resetFilters}>
              Reset filters
            </button>
          ) : null}
        </div>

        <div className="filter-meta">
          <span>
            Showing <strong>{rows.length}</strong> of {total} panel rows
          </span>
          {active ? <span className="muted">Filters active</span> : null}
        </div>

        {rows.length === 0 ? (
          <div className="empty-state">
            <p>No rows match the current filters.</p>
            <button type="button" className="btn-ghost" onClick={resetFilters}>
              Reset filters
            </button>
          </div>
        ) : (
          <div className="table-wrap">
            <table className="data">
              <thead>
                <tr>
                  <th>Year</th>
                  <th>Entity</th>
                  <th>Metric</th>
                  <th>Value</th>
                  <th>Status</th>
                  <th>Comparability</th>
                  <th>Confidence</th>
                  <th>Source</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((r, i) => (
                  <tr key={i}>
                    <td>{r.year}</td>
                    <td>{entityLabel(r.analytical_entity)}</td>
                    <td>{metricLabel(r.metric)}</td>
                    <td>{formatValue(r.value, r.value_status)}</td>
                    <td>
                      <StatusBadge status={r.value_status} />
                    </td>
                    <td>{comparabilityLabel(r.comparability)}</td>
                    <td>{confidenceLabel(r.confidence)}</td>
                    <td>
                      {r.citation_url ? (
                        <a href={r.citation_url} target="_blank" rel="noreferrer">
                          {r.source_publisher || "Source"}
                        </a>
                      ) : (
                        r.source_publisher
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
