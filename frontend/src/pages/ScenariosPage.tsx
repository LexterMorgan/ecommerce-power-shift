import {
  Bar,
  BarChart,
  CartesianGrid,
  ErrorBar,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { formatValue } from "../lib/dashboardData";
import { directionLabel } from "../lib/labels";
import { useDashboard } from "../lib/DashboardContext";
import { PageHeader, StatusBadge } from "../components/Ui";

export function ScenariosPage() {
  const { data, error, loading } = useDashboard();
  if (error) return <div className="error">{error}</div>;
  if (loading || !data) return <div className="loading">Loading scenarios…</div>;

  const rows = data.scenarios;
  const p3 = data.overview.phase3_post_break;
  const baseGap =
    rows.map((r) => Number(r.base_2025_value)).find((n) => Number.isFinite(n)) ??
    p3.gap_2025_pp;
  const chart = rows.map((r) => {
    const low = Number(r.scenario_low);
    const high = Number(r.scenario_high);
    const mid = (low + high) / 2;
    return {
      name: `${r.scenario_id}: ${r.scenario_name}`,
      mid,
      range: [mid - low, high - mid],
      low,
      high,
      base: Number(r.base_2025_value),
    };
  });

  return (
    <div>
      <PageHeader title="Scenario bands">
        Gate 6 illustrative Shopee − Combined Tokopedia + TikTok Shop share-gap bands from the
        static snapshot. These are scenario values — not observed forecasts.
      </PageHeader>

      <div className="break-banner" role="note">
        <StatusBadge status="SCENARIO" /> Illustrative ranges only. Legacy Tokopedia 2025 remains
        Unknown in all scenarios. Combined ≠ Legacy Tokopedia.
      </div>

      <div className="panel">
        <h2>Shopee − Combined gap (percentage points)</h2>
        <p className="panel-note">
          Base 2025 gap is {formatValue(baseGap)} pp (Shopee {formatValue(p3.shopee_2025)}% vs
          Combined Tokopedia + TikTok Shop {formatValue(p3.combined_2025)}%). Bands are illustrative,
          not forecasts.
        </p>
        <ResponsiveContainer width="100%" height={320}>
          <BarChart data={chart} layout="vertical" margin={{ left: 24, right: 24 }}>
            <CartesianGrid stroke="rgba(232,238,244,0.08)" />
            <XAxis type="number" domain={[0, 30]} stroke="#93a4b5" />
            <YAxis type="category" dataKey="name" width={210} stroke="#93a4b5" />
            <Tooltip
              formatter={(_v, _n, item) => {
                const p = item.payload as { low: number; high: number; base: number };
                return [`${p.low}–${p.high} pp (base ${p.base})`, "Band"];
              }}
            />
            <Bar dataKey="mid" fill="#c9a227" radius={[0, 8, 8, 0]}>
              <ErrorBar dataKey="range" width={6} strokeWidth={2} stroke="#e6d39a" />
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="panel" style={{ marginTop: "1rem" }}>
        <h2>Scenario table</h2>
        <div className="table-wrap">
          <table className="data">
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Base 2025</th>
                <th>Low</th>
                <th>High</th>
                <th>Direction</th>
                <th>Type</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((r, i) => (
                <tr key={i}>
                  <td>{String(r.scenario_id)}</td>
                  <td>{String(r.scenario_name)}</td>
                  <td>{String(r.base_2025_value)}</td>
                  <td>{String(r.scenario_low)}</td>
                  <td>{String(r.scenario_high)}</td>
                  <td>{directionLabel(String(r.direction ?? ""))}</td>
                  <td>
                    <StatusBadge status={String(r.value_type)} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
