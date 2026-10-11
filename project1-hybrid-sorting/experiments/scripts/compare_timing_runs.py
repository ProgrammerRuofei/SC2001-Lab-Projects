#!/usr/bin/env python3
"""Compare CPU-time stability between two fixed-n experiment CSV files."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from analyze_fixed_n import load_rows, resolve_path, summarize


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare medians and IQR widths for two fixed-n runs."
    )
    parser.add_argument("--original", required=True)
    parser.add_argument("--retest", required=True)
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def indexed_summary(path: Path) -> dict[int, dict[str, int | float]]:
    return {
        int(row["S"]): row for row in summarize(load_rows(path))
    }


def main() -> int:
    args = parse_arguments()
    original_path = resolve_path(args.original)
    retest_path = resolve_path(args.retest)
    output_path = resolve_path(args.output)

    original = indexed_summary(original_path)
    retest = indexed_summary(retest_path)
    thresholds = sorted(original.keys() & retest.keys())
    if len(thresholds) < 3:
        raise ValueError("the two inputs have fewer than three common S values")

    def values(
        source: dict[int, dict[str, int | float]], field: str
    ) -> list[float]:
        return [float(source[s][field]) * 1_000 for s in thresholds]

    original_median = values(original, "median_cpu_seconds")
    original_q1 = values(original, "q1_cpu_seconds")
    original_q3 = values(original, "q3_cpu_seconds")
    retest_median = values(retest, "median_cpu_seconds")
    retest_q1 = values(retest, "q1_cpu_seconds")
    retest_q3 = values(retest, "q3_cpu_seconds")
    original_iqr = [high - low for low, high in zip(original_q1, original_q3)]
    retest_iqr = [high - low for low, high in zip(retest_q1, retest_q3)]

    figure, (time_axis, iqr_axis) = plt.subplots(
        2,
        1,
        figsize=(10.8, 8.0),
        gridspec_kw={"height_ratios": [1.6, 1.0]},
    )

    time_axis.fill_between(
        thresholds,
        original_q1,
        original_q3,
        color="#7A7F87",
        alpha=0.14,
        linewidth=0,
        label="Original-session IQR",
    )
    time_axis.plot(
        thresholds,
        original_median,
        color="#7A7F87",
        linestyle="--",
        marker="o",
        markersize=3.5,
        linewidth=1.7,
        label="Original-session median",
    )
    time_axis.fill_between(
        thresholds,
        retest_q1,
        retest_q3,
        color="#1769AA",
        alpha=0.16,
        linewidth=0,
        label="Balanced-retest IQR",
    )
    time_axis.plot(
        thresholds,
        retest_median,
        color="#1769AA",
        marker="o",
        markersize=4,
        linewidth=2.1,
        label="Balanced-retest median",
    )
    time_axis.set_ylabel("Sorting CPU time (ms)")
    time_axis.set_title("CPU-time medians and middle 50% of runs")
    time_axis.legend(frameon=False, ncol=2, loc="upper left")

    iqr_axis.plot(
        thresholds,
        original_iqr,
        color="#7A7F87",
        linestyle="--",
        marker="o",
        markersize=3.5,
        linewidth=1.7,
        label="Original-session IQR width",
    )
    iqr_axis.plot(
        thresholds,
        retest_iqr,
        color="#1769AA",
        marker="o",
        markersize=4,
        linewidth=2.1,
        label="Balanced-retest IQR width",
    )
    iqr_axis.set_xlabel("Threshold, S")
    iqr_axis.set_ylabel("IQR width (ms)")
    iqr_axis.set_title("Timing variation at each threshold")
    iqr_axis.legend(frameon=False, loc="upper left")

    for axis in (time_axis, iqr_axis):
        axis.set_xlim(min(thresholds), max(thresholds))
        axis.set_xticks(list(range(32, 257, 32)))
        axis.grid(True, color="#E3E7ED", linewidth=0.8)
        axis.spines["top"].set_visible(False)
        axis.spines["right"].set_visible(False)

    figure.suptitle("Original long session versus balanced CPU-time retest")
    figure.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(figure)

    print(f"Compared {len(thresholds)} common thresholds")
    print(f"Wrote comparison figure to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
