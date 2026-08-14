export type PanelRow = {
  year: number | null;
  analytical_entity: string;
  source_platform?: string | null;
  entity_type?: string | null;
  metric: string;
  value: number | null;
  unit?: string | null;
  phase?: string | null;
  value_status: string;
  comparability?: string | null;
  source_publisher?: string | null;
  citation_url?: string | null;
  confidence?: string | null;
  notes?: string | null;
};

export type Overview = {
  rules: string[];
  phase1_standalone: {
    shopee_2022: number | null;
    legacy_tokopedia_2022: number | null;
    shopee_2024: number | null;
    legacy_tokopedia_2024: number | null;
    gap_2022_pp: number | null;
    gap_2024_pp: number | null;
    note: string;
  };
  phase3_post_break: {
    shopee_2025: number | null;
    combined_2025: number | null;
    gap_2025_pp: number | null;
    legacy_tokopedia_2025: string;
    note: string;
  };
  legacy_unknown_rows: PanelRow[];
  share_gap_summary: Array<Record<string, unknown>>;
  structural_break: boolean;
};

export type DashboardData = {
  contract_version: string;
  gate: string;
  generated_at: string;
  deployment_mode: string;
  rules: string[];
  sources: Record<string, string>;
  overview: Overview;
  standalone_shares: PanelRow[];
  post_break_shares: PanelRow[];
  legacy_unknown: PanelRow[];
  gmv_estimates: PanelRow[];
  access_metrics: Array<Record<string, unknown>>;
  tts_labeled_gmv: Array<Record<string, unknown>>;
  scenarios: Array<Record<string, unknown>>;
  share_gap_summary: Array<Record<string, unknown>>;
  filter_keys: Array<Record<string, unknown>>;
  competitive_panel: PanelRow[];
};

const DATA_URL = `${import.meta.env.BASE_URL}data/dashboard_data.json`;

let cached: Promise<DashboardData> | null = null;

export function loadDashboardData(): Promise<DashboardData> {
  if (!cached) {
    cached = fetch(DATA_URL).then(async (res) => {
      if (!res.ok) {
        throw new Error(`Failed to load dashboard_data.json (${res.status})`);
      }
      return res.json() as Promise<DashboardData>;
    });
  }
  return cached;
}

export function filterPanel(
  rows: PanelRow[],
  params: {
    year?: string | number;
    marketplace?: string;
    metric?: string;
    value_status?: string;
    comparability?: string;
  },
): PanelRow[] {
  return rows.filter((r) => {
    if (params.year !== undefined && params.year !== "all" && Number(r.year) !== Number(params.year)) {
      return false;
    }
    if (params.marketplace && params.marketplace !== "all" && r.analytical_entity !== params.marketplace) {
      return false;
    }
    if (params.metric && params.metric !== "all" && r.metric !== params.metric) {
      return false;
    }
    if (params.value_status && params.value_status !== "all" && r.value_status !== params.value_status) {
      return false;
    }
    if (
      params.comparability &&
      params.comparability !== "all" &&
      r.comparability !== params.comparability
    ) {
      return false;
    }
    return true;
  });
}

/** Display helper — never coerces UNKNOWN/null to zero. */
export function formatValue(value: number | null | undefined, status?: string): string {
  if (status === "UNKNOWN" || value === null || value === undefined) return "Unknown";
  return Number.isInteger(value) ? String(value) : value.toFixed(1);
}

export const FILTER_ALL = "all";

export function isFilterActive(params: {
  year: string;
  marketplace: string;
  metric: string;
  value_status: string;
  comparability: string;
}): boolean {
  return (
    params.year !== FILTER_ALL ||
    params.marketplace !== FILTER_ALL ||
    params.metric !== FILTER_ALL ||
    params.value_status !== FILTER_ALL ||
    params.comparability !== FILTER_ALL
  );
}
