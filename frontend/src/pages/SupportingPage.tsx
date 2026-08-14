import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { formatValue } from "../lib/dashboardData";
import { comparabilityLabel, entityLabel, metricLabel } from "../lib/labels";
import { useDashboard } from "../lib/DashboardContext";
import { PageHeader, StatusBadge } from "../components/Ui";

/** Presentation-only: keep access axes distinct from GMV/share entity names. */
function accessPresentationLabel(entity: string): string {
  const raw = entity.trim();
  if (raw.startsWith("Shopee")) return "Shopee — Internet access";
  if (raw.startsWith("TikTok")) return "TikTok Shop — Internet access";
  if (raw.includes("Tokopedia")) return "Legacy Tokopedia — Internet access";
  return `${raw} — Internet access`;
}

export function SupportingPage() {
  const { data, error, loading } = useDashboard();
  if (error) return <div className="error">{error}</div>;
  if (loading || !data) return <div className="loading">Loading supporting evidence…</div>;

  const access = data.access_metrics;
  const tts = data.tts_labeled_gmv;
  const gmv = data.gmv_estimates;

  const accessChart = access.map((r) => ({
    entity: accessPresentationLabel(String(r.entity ?? "")),
    value: r.value as number | null,
  }));

  return (
    <div>
      <PageHeader title="Supporting evidence">
        APJII access and TikTok Shop–labeled GMV from the static snapshot. Access is not GMV share
        and is separated from the primary market-share story.
      </PageHeader>

      <div className="break-banner" role="note">
        Access ≠ GMV share · Supporting evidence only — not interchangeable with market-share panels.
      </div>

      <div className="grid two">
        <div className="panel">
          <h2>APJII internet-user access (%)</h2>
          <p className="panel-note">
            Access percentages among internet users — not marketplace GMV or market share.
          </p>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={accessChart} margin={{ bottom: 28 }}>
              <CartesianGrid stroke="rgba(232,238,244,0.08)" />
              <XAxis
                dataKey="entity"
                stroke="#93a4b5"
                interval={0}
                tick={{ fontSize: 11 }}
              />
              <YAxis
                stroke="#93a4b5"
                domain={[0, 65]}
                label={{
                  value: "Access %",
                  angle: -90,
                  position: "insideLeft",
                  fill: "#93a4b5",
                  fontSize: 11,
                }}
              />
              <Tooltip formatter={(value) => [`${value}%`, "Internet access"]} />
              <Bar dataKey="value" fill="#4f8fbf" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="panel">
          <h2>TikTok Shop–labeled GMV</h2>
          <p className="panel-note">Labeled GMV evidence — not Combined market share.</p>
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
                {tts.map((r, i) => (
                  <tr key={i}>
                    <td>{entityLabel(String(r.entity))}</td>
                    <td>{metricLabel(String(r.metric)) || String(r.metric)}</td>
                    <td>
                      {r.value == null ? "Unknown" : `$${Number(r.value).toLocaleString()}`}
                    </td>
                    <td>
                      <StatusBadge status={String(r.evidence_type ?? "OBSERVED")} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div className="panel" style={{ marginTop: "1rem" }}>
        <h2>GMV estimates</h2>
        <p className="panel-note">
          Observed/derived non-null estimates for tracked entities only. Unknown Legacy Tokopedia
          2025 GMV is omitted here (kept Unknown in the panel).
        </p>
        <div className="table-wrap">
          <table className="data">
            <thead>
              <tr>
                <th>Year</th>
                <th>Entity</th>
                <th>Value (USD bn)</th>
                <th>Status</th>
                <th>Comparability</th>
              </tr>
            </thead>
            <tbody>
              {gmv.map((r, i) => (
                <tr key={i}>
                  <td>{String(r.year)}</td>
                  <td>{entityLabel(r.analytical_entity)}</td>
                  <td>{formatValue(r.value, r.value_status)}</td>
                  <td>
                    <StatusBadge status={r.value_status} />
                  </td>
                  <td>{comparabilityLabel(r.comparability)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
