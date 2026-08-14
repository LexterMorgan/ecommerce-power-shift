import type { ReactNode } from "react";
import { statusLabel } from "../lib/labels";

export function StatusBadge({ status }: { status: string }) {
  const cls =
    status === "OBSERVED"
      ? "observed"
      : status === "DERIVED"
        ? "derived"
        : status === "UNKNOWN"
          ? "unknown"
          : status === "SCENARIO"
            ? "scenario"
            : "";
  return (
    <span className={`badge ${cls}`} title={status || undefined}>
      {statusLabel(status) || status}
    </span>
  );
}

export function PageHeader({ title, children }: { title: string; children: ReactNode }) {
  return (
    <header className="page-head">
      <h1>{title}</h1>
      <p>{children}</p>
    </header>
  );
}
