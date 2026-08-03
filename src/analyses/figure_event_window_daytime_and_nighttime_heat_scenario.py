#!/usr/bin/env python3
"""Event-Window Daytime and Nighttime Heat Scenario.

Plan: Compare observed 2026 station temperatures with the calendar-matched
2021-2025 historical scenario for event days 0-29.
Framework: Section 5's descriptive station-heat design, Section 6's historical
median and observed minimum-maximum envelope, and Section 7 workflow steps 6-7.
"""
from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import pandas as pd
import seaborn as sns


ROOT = Path(__file__).resolve().parents[2]
EVENT_PATH = ROOT / "data/processed/kumamoto_jma_event_heat_daily_preprocessed.parquet"
HISTORICAL_PATH = (
    ROOT / "data/processed/kumamoto_jma_historical_heat_scenarios_preprocessed.parquet"
)
OUTPUT_PNG = (
    ROOT
    / "data/results/figures/Figure_03_event_window_daytime_nighttime_heat_scenario.png"
)
OUTPUT_PDF = (
    ROOT
    / "data/results/figures/Figure_03_event_window_daytime_nighttime_heat_scenario.pdf"
)

EVENT_START = date(2026, 7, 28)
EVENT_DAYS = list(range(30))
DAY_TICKS = [0, 5, 10, 15, 20, 25, 29]


def historical_summary(df: pd.DataFrame, value_col: str) -> pd.DataFrame:
    """Return the calendar-matched observed range and median for each event day."""
    counts = df.groupby("Event Day", observed=True)[value_col].count()
    if not (counts.reindex(EVENT_DAYS) == 10).all():
        raise ValueError(
            f"Expected 10 historical station-year observations per event day for {value_col}."
        )
    return (
        df.groupby("Event Day", observed=True)[value_col]
        .agg(historical_min="min", historical_median="median", historical_max="max")
        .reindex(EVENT_DAYS)
        .reset_index()
    )


def draw_panel(
    ax: plt.Axes,
    event: pd.DataFrame,
    historical: pd.DataFrame,
    value_col: str,
    threshold: float,
    y_label: str,
    station_colors: dict[str, tuple[float, float, float]],
) -> None:
    """Draw one daytime or nighttime scenario panel."""
    summary = historical_summary(historical, value_col)

    ax.fill_between(
        summary["Event Day"],
        summary["historical_min"],
        summary["historical_max"],
        color="#c8cdd3",
        alpha=0.52,
        linewidth=0,
        zorder=1,
    )
    ax.plot(
        summary["Event Day"],
        summary["historical_median"],
        color="#4a4f55",
        linewidth=1.8,
        linestyle="--",
        zorder=2,
    )
    ax.axhline(
        threshold,
        color="#b2182b",
        linewidth=1.4,
        linestyle=(0, (5, 3)),
        zorder=2,
    )

    for station, station_df in event.groupby("Station Name", sort=True, observed=True):
        station_df = station_df.sort_values("Event Day")
        color = station_colors[station]
        ax.plot(
            station_df["Event Day"],
            station_df[value_col],
            color=color,
            linewidth=1.6,
            alpha=0.92,
            zorder=3,
        )

        complete = station_df[station_df["Daily Record Status"].eq("complete")]
        partial = station_df[station_df["Daily Record Status"].eq("partial")]
        ax.scatter(
            complete["Event Day"],
            complete[value_col],
            s=35,
            color=color,
            edgecolor="white",
            linewidth=0.6,
            zorder=4,
        )
        ax.scatter(
            partial["Event Day"],
            partial[value_col],
            s=42,
            facecolor="white",
            edgecolor=color,
            linewidth=1.4,
            zorder=5,
        )

    tick_labels = []
    for day_number in DAY_TICKS:
        tick_date = EVENT_START + timedelta(days=day_number)
        tick_labels.append(f"{day_number}\n{tick_date.strftime('%b')} {tick_date.day}")

    ax.set_xlim(-0.5, 29.5)
    ax.set_xticks(DAY_TICKS, tick_labels)
    ax.set_ylabel(y_label)
    ax.grid(axis="y", color="#d8dce1", linewidth=0.7, alpha=0.75)
    ax.grid(axis="x", visible=False)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(axis="both", labelsize=9)


def main() -> None:
    event = pd.read_parquet(EVENT_PATH)
    historical = pd.read_parquet(HISTORICAL_PATH)

    required_event = {
        "Station Name",
        "Event Day",
        "Daily Maximum Air Temperature C",
        "Daily Minimum Air Temperature C",
        "Daily Record Status",
    }
    required_historical = {
        "Station Name",
        "Historical Year",
        "Event Day",
        "Daily Maximum Air Temperature C",
        "Daily Minimum Air Temperature C",
    }
    if missing := required_event.difference(event.columns):
        raise ValueError(f"Missing event columns: {sorted(missing)}")
    if missing := required_historical.difference(historical.columns):
        raise ValueError(f"Missing historical columns: {sorted(missing)}")

    event = event[event["Event Day"].between(0, 29)].copy()
    historical = historical[historical["Event Day"].between(0, 29)].copy()
    stations = sorted(event["Station Name"].dropna().unique().tolist())
    if len(stations) != 5:
        raise ValueError(f"Expected five event stations, found {len(stations)}: {stations}")

    sns.set_theme(style="whitegrid", context="paper")
    palette = sns.color_palette("colorblind", n_colors=len(stations))
    station_colors = dict(zip(stations, palette, strict=True))

    fig, axes = plt.subplots(2, 1, figsize=(11.4, 8.5), sharex=True)
    draw_panel(
        axes[0],
        event,
        historical,
        "Daily Maximum Air Temperature C",
        threshold=35.0,
        y_label="Daily maximum air temperature (°C)",
        station_colors=station_colors,
    )
    draw_panel(
        axes[1],
        event,
        historical,
        "Daily Minimum Air Temperature C",
        threshold=25.0,
        y_label="Daily minimum air temperature (°C)",
        station_colors=station_colors,
    )
    axes[1].set_xlabel("Event day (Day 0 = 28 Jul 2026)")

    for label, ax in zip("ab", axes.flat, strict=True):
        ax.text(
            -0.065,
            1.015,
            label,
            transform=ax.transAxes,
            fontsize=12,
            fontweight="bold",
            va="bottom",
            ha="left",
        )

    legend_handles: list[object] = [
        Patch(
            facecolor="#c8cdd3",
            edgecolor="none",
            alpha=0.52,
            label="2021–2025 observed range (scenario, not forecast)",
        ),
        Line2D(
            [0],
            [0],
            color="#4a4f55",
            linewidth=1.8,
            linestyle="--",
            label="Historical median",
        ),
        Line2D(
            [0],
            [0],
            color="#b2182b",
            linewidth=1.4,
            linestyle=(0, (5, 3)),
            label="Heat threshold (35°C daytime; 25°C nighttime)",
        ),
    ]
    legend_handles.extend(
        Line2D(
            [0],
            [0],
            color=station_colors[station],
            marker="o",
            markersize=5,
            linewidth=1.6,
            label=station,
        )
        for station in stations
    )
    legend_handles.extend(
        [
            Line2D(
                [0],
                [0],
                marker="o",
                color="#555555",
                markerfacecolor="#555555",
                markeredgecolor="white",
                linewidth=0,
                markersize=6,
                label="Complete station-day",
            ),
            Line2D(
                [0],
                [0],
                marker="o",
                color="#555555",
                markerfacecolor="white",
                markeredgecolor="#555555",
                linewidth=0,
                markersize=6,
                label="Partial station-day",
            ),
        ]
    )
    fig.legend(
        handles=legend_handles,
        loc="lower center",
        bbox_to_anchor=(0.5, 0.005),
        ncol=3,
        frameon=False,
        fontsize=8.2,
        handlelength=2.6,
        columnspacing=1.5,
    )

    fig.subplots_adjust(left=0.105, right=0.985, top=0.985, bottom=0.235, hspace=0.24)
    OUTPUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_PNG, dpi=400, bbox_inches="tight", facecolor="white")
    fig.savefig(OUTPUT_PDF, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    complete_days = int(event["Daily Record Status"].eq("complete").sum())
    partial_days = int(event["Daily Record Status"].eq("partial").sum())
    print(f"Saved: {OUTPUT_PNG.relative_to(ROOT)}")
    print(f"Saved: {OUTPUT_PDF.relative_to(ROOT)}")
    print(
        f"Event observations: {len(event)} station-days "
        f"({complete_days} complete, {partial_days} partial); "
        f"historical observations: {len(historical)} station-days."
    )


if __name__ == "__main__":
    main()
