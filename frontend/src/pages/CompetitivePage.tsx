import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { formatValue } from "../lib/dashboardData";
import { chartEntityLabel, entityLabel, phaseLabel } from "../lib/labels";
import { useDashboard } from "../lib/DashboardContext";
import { PageHeader, StatusBadge } from "../components/Ui";

export function CompetitivePage() {
  const { data, error, loading } = useDashboard();
  if (error) return <div className="error">{error}</div>;
  if (loading || !data) return <div className="loading">Loading competitive views…</div>;

  const standalone = data.standalone_shares;
  const post = data.post_break_shares;
  const gaps = data.share_gap_summary;

  const lineData = [2022, 2023, 2024].map((year) => ({
    year,
    Shopee: standalone.find((r) => r.year === year && r.analytical_entity === "Shopee")?.value ?? null,
    "Legacy Tokopedia":
      standalone.find((r) => r.year === year && r.analytical_entity === "Legacy Tokopedia")?.value ??
      null,
  }));

  const barData = post.map((r) => ({
    entity: chartEntityLabel(r.analytical_entity),
    fullName: r.analytical_entity,
    share: r.value,
    fill: r.analytical_entity === "Shopee" ? "#d96b3a" : "#3f9a74",
  }));

  return (
    <div>
      <PageHeader title="Competitive position">
        Two separated panels only — never a continuous Legacy Tokopedia → Combined time series.
        Values from the static analysis-ready snapshot.
      </PageHeader>

      <div className="break-banner" role="note">
        Structural break between panels. Combined Tokopedia + TikTok Shop ≠ Legacy Tokopedia.
      </div>

      <div className="grid two">
        <div className="panel">
          <h2>2022–2024 standalone</h2>
          <p className="panel-note">Shopee vs Legacy Tokopedia (observed share).</p>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={lineData}>
              <CartesianGrid stroke="rgba(232,238,244,0.08)" />
              <XAxis dataKey="year" stroke="#93a4b5" />
              <YAxis domain={[0, 55]} stroke="#93a4b5" />
              <Tooltip />
              <Legend />
              <Line dataKey="Shopee" stroke="#d96b3a" strokeWidth={2.5} connectNulls={false} />
              <Line
                dataKey="Legacy Tokopedia"
                stroke="#4f8fbf"
                strokeWidth={2.5}
                connectNulls={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
        <div className="panel">
          <h2>2025 post-break</h2>
          <p className="panel-note">
            “Combined” = Combined Tokopedia + TikTok Shop. Legacy Tokopedia 2025 share omitted
            (Unknown — not plotted as zero).
          </p>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={barData}>
              <CartesianGrid stroke="rgba(232,238,244,0.08)" />
              <XAxis dataKey="entity" stroke="#93a4b5" />
              <YAxis domain={[0, 70]} stroke="#93a4b5" />
              <Tooltip
                formatter={(value) => [`${value}%`, "Share"]}
                labelFormatter={(_l, payload) => {
                  const row = payload?.[0]?.payload as { fullName?: string } | undefined;
                  return row?.fullName ?? String(_l);
                }}
              />
              <Bar dataKey="share" radius={[8, 8, 0, 0]}>
                {barData.map((d) => (
                  <Cell key={d.entity} fill={d.fill} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="panel" style={{ marginTop: "1rem" }}>
        <h2>Share-gap summary</h2>
        <div className="table-wrap">
          <table className="data">
            <thead>
              <tr>
                <th>Panel</th>
                <th>Year</th>
                <th>Shopee</th>
                <th>Challenger</th>
                <th>Challenger share</th>
                <th>Gap pp</th>
                <th>Status</th>
                <th>Notes</th>
              </tr>
            </thead>
            <tbody>
              {gaps.map((g, i) => (
                <tr key={i}>
                  <td>{phaseLabel(String(g.panel ?? ""))}</td>
                  <td>{String(g.year ?? "")}</td>
                  <td>{formatValue(g.shopee_share_pct as number | null)}</td>
                  <td>{entityLabel(String(g.challenger_entity ?? ""))}</td>
                  <td>{formatValue(g.challenger_share_pct as number | null)}</td>
                  <td>{formatValue(g.gap_pp as number | null)}</td>
                  <td>
                    <StatusBadge status={String(g.value_status ?? "")} />
                  </td>
                  <td>{String(g.notes ?? "")}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
