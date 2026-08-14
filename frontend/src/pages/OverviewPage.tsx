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
import { chartEntityLabel, metricLabel } from "../lib/labels";
import { useDashboard } from "../lib/DashboardContext";
import { PageHeader, StatusBadge } from "../components/Ui";

export function OverviewPage() {
  const { data, error, loading } = useDashboard();
  if (error) return <div className="error">{error}</div>;
  if (loading || !data) return <div className="loading">Loading locked overview…</div>;

  const overview = data.overview;
  const p1 = overview.phase1_standalone;
  const p3 = overview.phase3_post_break;
  const standalone = data.standalone_shares;
  const post = data.post_break_shares;

  const lineData = [2022, 2023, 2024].map((year) => ({
    year,
    Shopee: standalone.find((r) => r.year === year && r.analytical_entity === "Shopee")?.value ?? null,
    "Legacy Tokopedia":
      standalone.find((r) => r.year === year && r.analytical_entity === "Legacy Tokopedia")?.value ??
      null,
  }));

  const barData = post.map((r) => ({
    name: chartEntityLabel(r.analytical_entity),
    fullName: r.analytical_entity,
    share: r.value,
    fill: r.analytical_entity === "Shopee" ? "#d96b3a" : "#3f9a74",
  }));

  return (
    <div>
      <PageHeader title="Executive overview">
        Locked competitive story from the analysis-ready static snapshot. No recalculation of source
        metrics. Legacy Tokopedia 2025 GMV/share remains Unknown.
      </PageHeader>

      <div className="break-banner" role="note">
        Structural break: 2022–2024 compares Shopee vs Legacy Tokopedia. 2025 compares Shopee vs
        Combined Tokopedia + TikTok Shop — not Legacy Tokopedia.
      </div>

      <div className="kpi-groups">
        <section className="kpi-group" aria-label="2022 to 2024 standalone panel">
          <div className="kpi-group-head">
            <h2 className="kpi-group-title">2022–2024 standalone</h2>
            <p className="kpi-group-sub">Shopee vs Legacy Tokopedia</p>
          </div>
          <div className="grid kpi kpi-pair">
            <div className="panel">
              <div className="kpi-label">Shopee share 2022</div>
              <div className="kpi-value">{formatValue(p1.shopee_2022)}%</div>
              <div className="kpi-note">
                <StatusBadge status="OBSERVED" /> vs Legacy Tokopedia{" "}
                {formatValue(p1.legacy_tokopedia_2022)}%
              </div>
            </div>
            <div className="panel">
              <div className="kpi-label">Shopee share 2024</div>
              <div className="kpi-value">{formatValue(p1.shopee_2024)}%</div>
              <div className="kpi-note">
                Gap vs Legacy Tokopedia {formatValue(p1.gap_2024_pp)} pp
              </div>
            </div>
          </div>
        </section>

        <section className="kpi-group kpi-group-break" aria-label="2025 post-break panel">
          <div className="kpi-group-head">
            <h2 className="kpi-group-title">2025 post-break</h2>
            <p className="kpi-group-sub">Shopee vs Combined Tokopedia + TikTok Shop</p>
          </div>
          <div className="grid kpi kpi-pair">
            <div className="panel">
              <div className="kpi-label">Shopee share 2025</div>
              <div className="kpi-value">{formatValue(p3.shopee_2025)}%</div>
              <div className="kpi-note">
                vs Combined Tokopedia + TikTok Shop {formatValue(p3.combined_2025)}%
              </div>
            </div>
            <div className="panel">
              <div className="kpi-label">Legacy Tokopedia 2025</div>
              <div className="kpi-value">Unknown</div>
              <div className="kpi-note">
                <StatusBadge status="UNKNOWN" /> not plotted as zero · different panel from Combined
              </div>
            </div>
          </div>
        </section>
      </div>

      <div className="grid two" style={{ marginTop: "1rem" }}>
        <div className="panel">
          <h2>2022–2024 — Shopee vs Legacy Tokopedia</h2>
          <p className="panel-note">Standalone dyad only. Combined entities are excluded here.</p>
          <ResponsiveContainer width="100%" height={260}>
            <LineChart data={lineData}>
              <CartesianGrid stroke="rgba(232,238,244,0.08)" />
              <XAxis dataKey="year" stroke="#93a4b5" />
              <YAxis stroke="#93a4b5" domain={[0, 55]} />
              <Tooltip />
              <Legend />
              <Line
                type="monotone"
                dataKey="Shopee"
                stroke="#d96b3a"
                strokeWidth={2.4}
                connectNulls={false}
              />
              <Line
                type="monotone"
                dataKey="Legacy Tokopedia"
                stroke="#4f8fbf"
                strokeWidth={2.4}
                connectNulls={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
        <div className="panel">
          <h2>2025 — Shopee vs Combined</h2>
          <p className="panel-note">
            Chart label “Combined” = Combined Tokopedia + TikTok Shop (≠ Legacy Tokopedia).
          </p>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={barData}>
              <CartesianGrid stroke="rgba(232,238,244,0.08)" />
              <XAxis dataKey="name" stroke="#93a4b5" />
              <YAxis stroke="#93a4b5" domain={[0, 70]} />
              <Tooltip
                formatter={(value) => [`${value}%`, "Share"]}
                labelFormatter={(_l, payload) => {
                  const row = payload?.[0]?.payload as { fullName?: string } | undefined;
                  return row?.fullName ?? String(_l);
                }}
              />
              <Bar dataKey="share" radius={[8, 8, 0, 0]}>
                {barData.map((d) => (
                  <Cell key={d.fullName} fill={d.fill} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="panel" style={{ marginTop: "1rem" }}>
        <h3>Unknown rows retained in snapshot</h3>
        <p className="panel-note">Legacy Tokopedia 2025 remains missing — not fabricated.</p>
        <div className="table-wrap">
          <table className="data">
            <thead>
              <tr>
                <th>Entity</th>
                <th>Metric</th>
                <th>Value</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {overview.legacy_unknown_rows.map((r) => (
                <tr key={`${r.metric}`}>
                  <td>{r.analytical_entity}</td>
                  <td>{metricLabel(r.metric)}</td>
                  <td>{formatValue(r.value, r.value_status)}</td>
                  <td>
                    <StatusBadge status={r.value_status} />
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
