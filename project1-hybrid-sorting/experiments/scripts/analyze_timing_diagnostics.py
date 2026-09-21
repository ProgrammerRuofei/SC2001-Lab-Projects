#!/usr/bin/env python3
"""Diagnose CPU-time distribution and session drift in a fixed-n run."""

from __future__ import annotations

import argparse
import statistics
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from analyze_fixed_n import load_rows, resolve_path, summarize


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Plot raw CPU times, median, mean, IQR, and execution-order "
            "drift without changing the formal Part (c)(ii) figures."
        )
    )
    parser.add_argument(
        "--input",
        default="results/fixed_n_1m_final_1_256.csv",
        help="raw fixed-n CSV",
    )
    parser.add_argument(
        "--output",
        default=(
            "figures/fixed_n_1m_timing_diagnostics/"
            "cpu_time_distribution_and_session_drift.png"
        ),
        help="diagnostic PNG path",
    )
    parser.add_argument("--min-s", type=int, default=32)
    parser.add_argument("--max-s", type=int, default=256)
    parser.add_argument(
        "--rolling-window",
        type=int,
        default=75,
        help="number of local observations in the rolling median",
    )
    return parser.parse_args()


def rolling_median(
    x_values: list[int], y_values: list[float], window: int
) -> tuple[list[int], list[float]]:
    if window < 3:
        raise ValueError("rolling window must be at least 3")
    if window > len(y_values):
        raise ValueError("rolling window exceeds the number of observations")

    half_window = window // 2
    rolled_x: list[int] = []
    rolled_y: list[float] = []
    for index in range(half_window, len(y_values) - half_window):
        start = index - half_window
        stop = index + half_window + 1
        rolled_x.append(x_values[index])
        rolled_y.append(statistics.median(y_values[start:stop]))
    return rolled_x, rolled_y


def main() -> int:
    args = parse_arguments()
    if args.min_s >= args.max_s:
        raise ValueError("--min-s must be smaller than --max-s")

    input_path = resolve_path(args.input)
    output_path = resolve_path(args.output)
    rows = load_rows(input_path)
    summary = summarize(rows)

    local_summary = [
        row
        for row in summary
        if args.min_s <= int(row["S"]) <= args.max_s
    ]
    local_rows = [
        (execution_index, row)
        for execution_index, row in enumerate(rows, start=1)
        if args.min_s <= int(row["S"]) <= args.max_s
    ]
    if len(local_summary) < 3:
        raise ValueError("selected S range contains fewer than three values")

    thresholds = [int(row["S"]) for row in local_summary]
    medians_ms = [
        float(row["median_cpu_seconds"]) * 1_000
        for row in local_summary
    ]
    means_ms = [
        float(row["mean_cpu_seconds"]) * 1_000
        for row in local_summary
    ]
    q1_ms = [
        float(row["q1_cpu_seconds"]) * 1_000 for row in local_summary
    ]
    q3_ms = [
        float(row["q3_cpu_seconds"]) * 1_000 for row in local_summary
    ]
    median_by_threshold = dict(zip(thresholds, medians_ms))

    grouped_rows: dict[int, list[dict[str, int | float]]] = defaultdict(list)
    for _execution_index, row in local_rows:
        grouped_rows[int(row["S"])].append(row)

    raw_x: list[float] = []
    raw_y: list[float] = []
    for threshold in thresholds:
        group = sorted(grouped_rows[threshold], key=lambda row: int(row["seed"]))
        group_size = len(group)
        for position, row in enumerate(group):
            # A small deterministic x offset keeps overlapping observations
            # visible without suggesting that S itself changed.
            offset = (position - (group_size - 1) / 2) * 0.045
            raw_x.append(threshold + offset)
            raw_y.append(float(row["cpu_seconds"]) * 1_000)

    execution_indices = [index for index, _row in local_rows]
    residuals_ms = [
        float(row["cpu_seconds"]) * 1_000
        - median_by_threshold[int(row["S"])]
        for _index, row in local_rows
    ]
    rolling_x, rolling_y = rolling_median(
        execution_indices, residuals_ms, args.rolling_window
    )

    input_size = int(local_summary[0]["n"])
    runs_per_threshold = int(local_summary[0]["runs"])

    figure, (distribution_axis, drift_axis) = plt.subplots(
        2,
        1,
        figsize=(11.5, 9.0),
        gridspec_kw={"height_ratios": [1.55, 1.0]},
    )

    distribution_axis.scatter(
        raw_x,
        raw_y,
        s=17,
        color="#587A9A",
        alpha=0.20,
        linewidths=0,
        label=f"Individual runs ({runs_per_threshold} per S)",
        zorder=1,
    )
    distribution_axis.fill_between(
        thresholds,
        q1_ms,
        q3_ms,
        color="#1769AA",
        alpha=0.12,
        linewidth=0,
        label="Middle 50% of runs (IQR)",
        zorder=2,
    )
    distribution_axis.plot(
        thresholds,
        medians_ms,
        color="#1769AA",
        marker="o",
        markersize=3.5,
        linewidth=2.0,
        label="Median CPU time",
        zorder=4,
    )
    distribution_axis.plot(
        thresholds,
        means_ms,
        color="#D95F02",
        linestyle="--",
        linewidth=1.7,
        label="Mean CPU time",
        zorder=3,
    )
    distribution_axis.set_xlim(args.min_s, args.max_s)
    distribution_axis.set_xticks(list(range(args.min_s, args.max_s + 1, 32)))
    distribution_axis.set_xlabel("Threshold, S")
    distribution_axis.set_ylabel("Sorting CPU time (ms)")
    distribution_axis.set_title(
        f"CPU-time distribution (fixed n = {input_size:,})"
    )
    distribution_axis.legend(frameon=False, ncol=2, loc="upper left")

    drift_axis.scatter(
        execution_indices,
        residuals_ms,
        s=13,
        color="#587A9A",
        alpha=0.24,
        linewidths=0,
        label="Individual run residual",
    )
    drift_axis.axhline(0, color="#6B7280", linewidth=1.0)
    drift_axis.plot(
        rolling_x,
        rolling_y,
        color="#D95F02",
        linewidth=2.2,
        label=f"Rolling median ({args.rolling_window} observations)",
    )
    drift_axis.set_xlim(1, len(rows))
    drift_axis.set_xlabel("Execution order in CSV")
    drift_axis.set_ylabel("CPU time minus median for the same S (ms)")
    drift_axis.set_title("Session drift after controlling for threshold")
    drift_axis.legend(frameon=False, loc="upper left")

    for axis in (distribution_axis, drift_axis):
        axis.grid(True, color="#E3E7ED", linewidth=0.8)
        axis.spines["top"].set_visible(False)
        axis.spines["right"].set_visible(False)

    figure.suptitle(
        "Part (c)(ii) CPU-time diagnostic",
        fontsize=15,
        y=0.995,
    )
    figure.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(figure)

    print(f"Read {len(rows)} raw rows from {input_path}")
    print(f"Plotted {len(local_rows)} runs for S={args.min_s}–{args.max_s}")
    print(f"Wrote diagnostic figure to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
