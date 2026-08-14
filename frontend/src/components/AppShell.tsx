import { NavLink } from "react-router-dom";
import type { ReactNode } from "react";

const links = [
  { to: "/", label: "Executive overview" },
  { to: "/competitive", label: "Competitive position" },
  { to: "/supporting", label: "Supporting evidence" },
  { to: "/scenarios", label: "Scenarios" },
  { to: "/explorer", label: "Data explorer" },
];

export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <h1 className="brand">Power Shift</h1>
        <div className="brand-sub">Shopee vs Legacy Tokopedia / Combined · Indonesia</div>
        <nav className="nav">
          {links.map((l) => (
            <NavLink key={l.to} to={l.to} end={l.to === "/"}>
              {l.label}
            </NavLink>
          ))}
        </nav>
        <p className="footer-note">
          Static snapshot. Combined Tokopedia + TikTok Shop ≠ Legacy Tokopedia. PostgreSQL remains
          analytical infrastructure.
        </p>
      </aside>
      <main className="main">{children}</main>
    </div>
  );
}
