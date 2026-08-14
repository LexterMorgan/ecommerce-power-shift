"""Matplotlib charts for Gate 7A. Plot OBSERVED/DERIVED only; never UNKNOWN→0."""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

# Distinct, non-generic palette (avoid purple-AI default)
COLOR_SHOPEE = "#C45C26"
COLOR_LEGACY = "#1F4E79"
COLOR_COMBINED = "#2E7D4F"
COLOR_TTS = "#5B2C6F"
COLOR_BREAK = "#666666"
COLOR_SCENARIO = "#8B6914"


def _style(ax, title: str, ylabel: str) -> None:
    ax.set_title(title, fontsize=12, pad=10)
    ax.set_ylabel(ylabel)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", linestyle=":", alpha=0.4)


def chart_historical_standalone_shares(hist: pd.DataFrame, out_path: Path) -> Path:
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for entity, color in [("Shopee", COLOR_SHOPEE), ("Legacy Tokopedia", COLOR_LEGACY)]:
        sub = hist[hist["analytical_entity"] == entity].sort_values("year")
        ax.plot(
            sub["year"].astype(int),
            sub["value"],
            marker="o",
            linewidth=2.2,
            color=color,
            label=f"{entity} (OBSERVED)",
        )
        for _, r in sub.iterrows():
            ax.annotate(
                f"{r['value']:.0f}%",
                (int(r["year"]), r["value"]),
                textcoords="offset points",
                xytext=(0, 8),
                ha="center",
                fontsize=8,
                color=color,
            )
    _style(
        ax,
        "Phase 1 — Indonesia GMV share: Shopee vs Legacy Tokopedia (2022–2024)",
        "GMV share (%)",
    )
    ax.set_xlabel("Year")
    ax.set_xticks([2022, 2023, 2024])
    ax.set_ylim(0, 55)
    ax.legend(frameon=False, loc="upper left")
    fig.text(
        0.01,
        0.01,
        "Source: Momentum Works via secondary citations in competitive_panel.csv · Standalone entities only · Not Combined",
        fontsize=7,
        color="#555555",
    )
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=160)
    plt.close(fig)
    return out_path


def chart_post_break_comparison(post: pd.DataFrame, derived: pd.DataFrame, out_path: Path) -> Path:
    fig, ax = plt.subplots(figsize=(8, 4.5))
    labels = []
    values = []
    colors = []
    # Order: Shopee, Combined 2025, optional DERIVED 2024 baseline as hatched reference
    s = post[post["analytical_entity"] == "Shopee"]
    c = post[post["analytical_entity"] == "Combined Tokopedia + TikTok Shop"]
    if len(s) == 1:
        labels.append("Shopee 2025\n(OBSERVED)")
        values.append(float(s.iloc[0]["value"]))
        colors.append(COLOR_SHOPEE)
    if len(c) == 1:
        labels.append("Combined Tokopedia+TTS 2025\n(OBSERVED)")
        values.append(float(c.iloc[0]["value"]))
        colors.append(COLOR_COMBINED)
    if len(derived) == 1:
        labels.append("Combined additive 2024\n(DERIVED 23+11)")
        values.append(float(derived.iloc[0]["value"]))
        colors.append("#A8D5BA")

    bars = ax.bar(labels, values, color=colors, width=0.55)
    for bar, v in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            v + 1,
            f"{v:.0f}%",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
        )
    _style(
        ax,
        "Phase 3 — STRUCTURAL BREAK: Shopee vs Combined (2025)",
        "GMV share (%)",
    )
    ax.set_ylim(0, 70)
    ax.axhline(0, color="#cccccc", linewidth=0.8)
    fig.text(
        0.5,
        0.92,
        "NOT equivalent to Shopee vs Legacy Tokopedia · Legacy Tokopedia 2025 share = UNKNOWN (not plotted)",
        ha="center",
        fontsize=8,
        color=COLOR_BREAK,
        style="italic",
    )
    fig.text(
        0.01,
        0.01,
        "Source: competitive_panel.csv · Combined ≠ Legacy Tokopedia · DERIVED baseline is conditional additivity",
        fontsize=7,
        color="#555555",
    )
    fig.tight_layout(rect=[0, 0.04, 1, 0.90])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=160)
    plt.close(fig)
    return out_path


def chart_structural_break_story(hist: pd.DataFrame, post: pd.DataFrame, out_path: Path) -> Path:
    """Two-panel figure: standalone history | post-break comparison."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5), sharey=True)

    for entity, color in [("Shopee", COLOR_SHOPEE), ("Legacy Tokopedia", COLOR_LEGACY)]:
        sub = hist[hist["analytical_entity"] == entity].sort_values("year")
        ax1.plot(
            sub["year"].astype(int),
            sub["value"],
            marker="o",
            linewidth=2.2,
            color=color,
            label=entity,
        )
    ax1.set_title("2022–2024 standalone dyad")
    ax1.set_xlabel("Year")
    ax1.set_xticks([2022, 2023, 2024])
    ax1.set_ylabel("GMV share (%)")
    ax1.set_ylim(0, 60)
    ax1.legend(frameon=False, fontsize=8)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.grid(axis="y", linestyle=":", alpha=0.4)

    s = post[post["analytical_entity"] == "Shopee"]
    c = post[post["analytical_entity"] == "Combined Tokopedia + TikTok Shop"]
    labs, vals, cols = [], [], []
    if len(s) == 1:
        labs.append("Shopee")
        vals.append(float(s.iloc[0]["value"]))
        cols.append(COLOR_SHOPEE)
    if len(c) == 1:
        labs.append("Combined\nTokopedia+TTS")
        vals.append(float(c.iloc[0]["value"]))
        cols.append(COLOR_COMBINED)
    ax2.bar(labs, vals, color=cols, width=0.5)
    for i, v in enumerate(vals):
        ax2.text(i, v + 1, f"{v:.0f}%", ha="center", fontsize=9, fontweight="bold")
    ax2.set_title("2025 post-break (Combined ≠ Legacy)")
    ax2.set_xlabel("")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.grid(axis="y", linestyle=":", alpha=0.4)

    # Visual break marker between panels
    fig.text(
        0.5,
        0.5,
        "│\nSTRUCTURAL\nBREAK\n│",
        ha="center",
        va="center",
        fontsize=8,
        color=COLOR_BREAK,
        transform=fig.transFigure,
    )
    fig.suptitle(
        "Indonesia e-commerce GMV share — structural-break visualization",
        fontsize=12,
        y=1.02,
    )
    fig.text(
        0.01,
        0.01,
        "Legacy Tokopedia 2025 GMV/share UNKNOWN — intentionally omitted (not zero). OBSERVED values only.",
        fontsize=7,
        color="#555555",
    )
    fig.tight_layout(rect=[0, 0.05, 1, 0.98])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=160, bbox_inches="tight")
    plt.close(fig)
    return out_path


def chart_access_supporting(access: pd.DataFrame, out_path: Path) -> Path:
    """APJII access — explicitly not GMV."""
    fig, ax = plt.subplots(figsize=(8, 4.2))
    # Prefer a stable order
    order = [
        "Shopee Indonesia",
        "TikTok Shop Indonesia",
        "Legacy Tokopedia",
    ]
    # Map entity names in file
    present = list(access["entity"].unique())
    entities = [e for e in order if e in present] + [e for e in present if e not in order]
    colors = {
        "Shopee Indonesia": COLOR_SHOPEE,
        "TikTok Shop Indonesia": COLOR_TTS,
        "Legacy Tokopedia": COLOR_LEGACY,
    }
    vals = []
    labs = []
    cols = []
    for e in entities:
        sub = access[access["entity"] == e]
        if len(sub) != 1:
            continue
        labs.append(e.replace(" Indonesia", "").replace("TikTok Shop", "TTS"))
        vals.append(float(sub.iloc[0]["value"]))
        cols.append(colors.get(e, "#777777"))
    bars = ax.bar(labs, vals, color=cols, width=0.55)
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 0.8, f"{v:.1f}%", ha="center", fontsize=9)
    _style(
        ax,
        "Supporting — APJII internet-user access share (2025 survey)",
        "Access share (%)",
    )
    ax.set_ylim(0, 65)
    fig.text(
        0.5,
        0.93,
        "ACCESS ≠ GMV SHARE · Supporting evidence only · Legacy access near-flat vs TTS surge",
        ha="center",
        fontsize=8,
        color=COLOR_BREAK,
        style="italic",
    )
    fig.text(
        0.01,
        0.01,
        "Source: data/processed/2025_comparable (APJII via Kompas) · OBSERVED access metrics",
        fontsize=7,
        color="#555555",
    )
    fig.tight_layout(rect=[0, 0.04, 1, 0.90])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=160)
    plt.close(fig)
    return out_path


def chart_scenario_gap_bands(scenarios: pd.DataFrame, out_path: Path) -> Path:
    fig, ax = plt.subplots(figsize=(8, 4.2))
    scenarios = scenarios.sort_values("scenario_id")
    y_pos = range(len(scenarios))
    base = float(scenarios.iloc[0]["base_2025_value"])
    for i, (_, r) in enumerate(scenarios.iterrows()):
        low, high = float(r["scenario_low"]), float(r["scenario_high"])
        ax.barh(
            i,
            high - low,
            left=low,
            height=0.45,
            color=COLOR_SCENARIO,
            alpha=0.55,
            label="SCENARIO band" if i == 0 else None,
        )
        ax.plot([low, high], [i, i], color=COLOR_SCENARIO, linewidth=2)
        ax.text(high + 0.4, i, f"{low:.0f}–{high:.0f} pp", va="center", fontsize=8)
    ax.axvline(base, color=COLOR_SHOPEE, linestyle="--", linewidth=1.5, label=f"2025 OBSERVED gap ({base:.0f} pp)")
    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(
        [f"{r.scenario_id}: {r.scenario_name}" for _, r in scenarios.iterrows()],
        fontsize=8,
    )
    _style(
        ax,
        "Gate 6 scenarios — Shopee−Combined share gap bands (SCENARIO, not forecasts)",
        "Share gap (percentage points)",
    )
    ax.set_xlim(0, 30)
    ax.legend(frameon=False, fontsize=8, loc="lower right")
    fig.text(
        0.01,
        0.01,
        "value_type=SCENARIO · Illustrative ranges from gate6_scenario_outputs.csv · Not OBSERVED future shares",
        fontsize=7,
        color="#555555",
    )
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=160)
    plt.close(fig)
    return out_path
