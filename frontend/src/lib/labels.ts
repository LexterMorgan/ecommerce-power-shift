/** Presentation-only labels. Analytical / filter values stay unchanged. */

export const TRACKED_ENTITIES = [
  "Shopee",
  "Legacy Tokopedia",
  "TikTok Shop",
  "Combined Tokopedia + TikTok Shop",
] as const;

const METRIC_LABELS: Record<string, string> = {
  market_share_pct: "Market Share",
  gmv_estimate_usd_billion: "GMV Estimate (USD bn)",
};

const STATUS_LABELS: Record<string, string> = {
  OBSERVED: "Observed",
  DERIVED: "Derived",
  UNKNOWN: "Unknown",
  SCENARIO: "Scenario",
};

const COMPARABILITY_LABELS: Record<string, string> = {
  DIRECT: "Direct",
  CONDITIONAL: "Conditional",
  "NOT COMPARABLE": "Not Comparable",
};

const PHASE_LABELS: Record<string, string> = {
  phase1_historical_standalone: "2022–2024 Standalone",
  phase1_historical_tts: "TikTok Shop Historical",
  phase1_standalone: "2022–2024 Standalone",
  phase3_post_break: "2025 Post-Break",
  derived_baseline: "Derived Baseline",
};

const CONFIDENCE_LABELS: Record<string, string> = {
  HIGH: "High",
  MEDIUM: "Medium",
  LOW: "Low",
};

const DIRECTION_LABELS: Record<string, string> = {
  narrows: "Narrows",
  widens: "Widens",
  stable_to_wider: "Stable to wider",
};

/** Canonical entity label for UI (passthrough if already canonical). */
export function entityLabel(entity: string | null | undefined): string {
  if (!entity) return "";
  if (entity === "Tokopedia") return "Legacy Tokopedia";
  if (entity === "TTS" || entity === "TikTok") return "TikTok Shop";
  if (entity === "Combined" || entity === "Combined Tokopedia+TTS") {
    return "Combined Tokopedia + TikTok Shop";
  }
  if (entity.includes("Combined") && entity.includes("DERIVED")) {
    return "Combined Tokopedia + TikTok Shop (Derived)";
  }
  return entity;
}

/**
 * Compact chart axis/legend label. Always pair with microcopy clarifying
 * Combined ≠ Legacy Tokopedia when "Combined" is used.
 */
export function chartEntityLabel(entity: string): string {
  if (entity === "Combined Tokopedia + TikTok Shop") return "Combined";
  return entityLabel(entity);
}

export function metricLabel(metric: string | null | undefined): string {
  if (!metric) return "";
  return METRIC_LABELS[metric] ?? metric;
}

export function statusLabel(status: string | null | undefined): string {
  if (!status) return "";
  return STATUS_LABELS[status] ?? status;
}

export function comparabilityLabel(value: string | null | undefined): string {
  if (!value) return "";
  return COMPARABILITY_LABELS[value] ?? value;
}

export function phaseLabel(phase: string | null | undefined): string {
  if (!phase) return "";
  return PHASE_LABELS[phase] ?? phase;
}

export function confidenceLabel(value: string | null | undefined): string {
  if (!value) return "";
  return CONFIDENCE_LABELS[value] ?? value;
}

export function directionLabel(value: string | null | undefined): string {
  if (!value) return "";
  return DIRECTION_LABELS[value] ?? value;
}

/** Sort marketplace options in tracked-entity order; unknown last. */
export function sortTrackedEntities(entities: string[]): string[] {
  const rank = new Map(TRACKED_ENTITIES.map((e, i) => [e, i]));
  return [...entities].sort((a, b) => {
    const ra = rank.get(a as (typeof TRACKED_ENTITIES)[number]);
    const rb = rank.get(b as (typeof TRACKED_ENTITIES)[number]);
    if (ra !== undefined && rb !== undefined) return ra - rb;
    if (ra !== undefined) return -1;
    if (rb !== undefined) return 1;
    return a.localeCompare(b);
  });
}
