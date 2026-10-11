#!/usr/bin/env python3
"""Analyze Part (c)(iii): suitable Hybrid Merge Sort thresholds across n."""

from __future__ import annotations

import argparse
import csv
import statistics
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter, NullFormatter

from analyze_fixed_n import load_rows, resolve_path, summarize


SUMMARY_FIELDS = [
    "n",
    "S",
    "comparison_runs",
    "mean_key_comparisons",
    "cpu_runs",
    "median_cpu_seconds",
    "q1_cpu_seconds",
    "q3_cpu_seconds",
]


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze suitable S regions across several input sizes."
    )
    parser.add_argument("--comparison-inputs", nargs="+", required=True)
    parser.add_argument("--cpu-inputs", nargs="+", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--figure-dir", required=True)
    parser.add_argument(
        "--sparse-overview",
        action="store_true",
        help="show measured powers of two only in overview plots; keep full local plots and summary",
    )
    return parser.parse_args()


def one_n(path_text: str) -> tuple[int, list[dict[str, int | float]]]:
    path = resolve_path(path_text)
    rows = load_rows(path, {"fixed-n", "optimal-s"})
    input_sizes = {int(row["n"]) for row in rows}
    if len(input_sizes) != 1:
        raise ValueError(f"{path} must contain exactly one n value")
    return next(iter(input_sizes)), summarize(rows)


def load_by_n(paths: list[str]) -> dict[int, list[dict[str, int | float]]]:
    result: dict[int, list[dict[str, int | float]]] = {}
    for path in paths:
        n, summary = one_n(path)
        existing_thresholds = {
            int(row["S"]) for row in result.get(n, [])
        }
        new_thresholds = {int(row["S"]) for row in summary}
        overlap = existing_thresholds & new_thresholds
        if overlap:
            values = ", ".join(str(value) for value in sorted(overlap))
            raise ValueError(
                f"input files for n={n} overlap at S={values}"
            )
        result.setdefault(n, []).extend(summary)
        result[n].sort(key=lambda row: int(row["S"]))
    return result


def comparison_plateaus(
    summary: list[dict[str, int | float]],
) -> list[list[dict[str, int | float]]]:
    plateaus: list[list[dict[str, int | float]]] = []
    for row in summary:
        comparison_key = round(float(row["mean_key_comparisons"]), 6)
        if not plateaus:
            plateaus.append([row])
            continue
        previous_key = round(
            float(plateaus[-1][-1]["mean_key_comparisons"]), 6
        )
        if comparison_key == previous_key:
            plateaus[-1].append(row)
        else:
            plateaus.append([row])
    return plateaus


def choose_suitable_region(
    comparison_summary: list[dict[str, int | float]],
    cpu_summary: list[dict[str, int | float]],
) -> tuple[int, int, float]:
    cpu_by_s = {
        int(row["S"]): float(row["median_cpu_seconds"]) * 1_000
        for row in cpu_summary
    }
    candidates: list[tuple[float, int, int]] = []
    for plateau in comparison_plateaus(comparison_summary):
        thresholds = [int(row["S"]) for row in plateau]
        timings = [cpu_by_s[s] for s in thresholds if s in cpu_by_s]
        if len(thresholds) >= 2 and len(timings) >= 2:
            candidates.append(
                (
                    statistics.median(timings),
                    thresholds[0],
                    thresholds[-1],
                )
            )
    if not candidates:
        raise ValueError("no multi-threshold comparison plateau has CPU data")
    regional_median, start, end = min(candidates)
    return start, end, regional_median


def write_summary(
    path: Path,
    comparisons: dict[int, list[dict[str, int | float]]],
    cpu: dict[int, list[dict[str, int | float]]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=SUMMARY_FIELDS)
        writer.writeheader()
        for n in sorted(comparisons):
            cpu_by_s = {int(row["S"]): row for row in cpu[n]}
            for row in comparisons[n]:
                threshold = int(row["S"])
                cpu_row = cpu_by_s.get(threshold)
                writer.writerow(
                    {
                        "n": n,
                        "S": threshold,
                        "comparison_runs": row["runs"],
                        "mean_key_comparisons": (
                            f"{float(row['mean_key_comparisons']):.1f}"
                        ),
                        "cpu_runs": cpu_row["runs"] if cpu_row else "",
                        "median_cpu_seconds": (
                            f"{float(cpu_row['median_cpu_seconds']):.9f}"
                            if cpu_row
                            else ""
                        ),
                        "q1_cpu_seconds": (
                            f"{float(cpu_row['q1_cpu_seconds']):.9f}"
                            if cpu_row
                            else ""
                        ),
                        "q3_cpu_seconds": (
                            f"{float(cpu_row['q3_cpu_seconds']):.9f}"
                            if cpu_row
                            else ""
                        ),
                    }
                )


def configure_log2_x(axis: plt.Axes, thresholds: list[int]) -> None:
    axis.set_xscale("log", base=2)
    maximum = max(thresholds)
    ticks: list[int] = []
    value = 1
    while value <= maximum:
        ticks.append(value)
        value *= 2
    axis.set_xticks(ticks)
    axis.xaxis.set_major_formatter(
        FuncFormatter(lambda value, _position: f"{value:g}")
    )
    axis.xaxis.set_minor_formatter(NullFormatter())
    axis.set_xlim(min(thresholds), max(thresholds))


def finish_axis(axis: plt.Axes) -> None:
    axis.grid(True, color="#E3E7ED", linewidth=0.8)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)


def powers_of_two_only(
    data: dict[int, list[dict[str, int | float]]],
) -> dict[int, list[dict[str, int | float]]]:
    return {
        n: [
            row for row in rows
            if (threshold := int(row["S"])) > 0
            and threshold & (threshold - 1) == 0
        ]
        for n, rows in data.items()
    }


def plot_comparisons(
    path: Path,
    comparisons: dict[int, list[dict[str, int | float]]],
    sparse_overview: bool = False,
) -> None:
    colors = ["#1769AA", "#D95F02", "#2A8C67"]
    figure, axis = plt.subplots(figsize=(9.6, 5.8))
    all_thresholds: list[int] = []
    for color, n in zip(colors, sorted(comparisons)):
        rows = comparisons[n]
        thresholds = [int(row["S"]) for row in rows]
        baseline = float(rows[0]["mean_key_comparisons"])
        relative = [
            float(row["mean_key_comparisons"]) / baseline
            for row in rows
        ]
        all_thresholds.extend(thresholds)
        axis.plot(
            thresholds,
            relative,
            marker="o",
            markersize=3.5,
            linewidth=1.8,
            color=color,
            label=f"n = {n:,}",
        )
    configure_log2_x(axis, all_thresholds)
    axis.set_xlabel("Threshold, S (log2 scale)")
    axis.set_ylabel("Key comparisons relative to S = 1")
    axis.set_title(
        "Comparison cost versus threshold across input sizes"
        + (" (powers of two)" if sparse_overview else "")
    )
    axis.legend(frameon=False)
    finish_axis(axis)
    figure.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(figure)


def plot_cpu(
    path: Path,
    cpu: dict[int, list[dict[str, int | float]]],
    sparse_overview: bool = False,
) -> None:
    colors = ["#1769AA", "#D95F02", "#2A8C67"]
    figure, axes = plt.subplots(3, 1, figsize=(9.8, 10.0), sharex=False)
    for index, (axis, color, n) in enumerate(
        zip(axes, colors, sorted(cpu))
    ):
        rows = cpu[n]
        thresholds = [int(row["S"]) for row in rows]
        median = [
            float(row["median_cpu_seconds"]) * 1_000 for row in rows
        ]
        q1 = [float(row["q1_cpu_seconds"]) * 1_000 for row in rows]
        q3 = [float(row["q3_cpu_seconds"]) * 1_000 for row in rows]
        axis.fill_between(
            thresholds,
            q1,
            q3,
            color=color,
            alpha=0.14,
            linewidth=0,
            label="Middle 50% across 15 seeds (IQR)",
        )
        axis.plot(
            thresholds,
            median,
            marker="o",
            markersize=4,
            linewidth=2.0,
            color=color,
            label="Median CPU time across 15 seeds",
        )
        axis.set_ylabel("CPU time (ms)")
        axis.set_title(f"n = {n:,}")
        configure_log2_x(axis, thresholds)
        finish_axis(axis)
        if sparse_overview and thresholds[-1] < max(
            int(row["S"]) for rows in cpu.values() for row in rows
        ):
            axis.annotate(
                f"Measured to S = {thresholds[-1]}",
                (thresholds[-1], median[-1]),
                xytext=(-8, 12),
                textcoords="offset points",
                ha="right",
                fontsize=8,
                color=color,
            )
        if index == 0:
            axis.legend(frameon=False, loc="upper left")
    for axis in axes:
        axis.set_xlabel("Threshold, S (log2 scale)")
    figure.suptitle(
        "Median CPU time and IQR across input sizes"
        + (" (powers of two)" if sparse_overview else ""),
        y=0.995,
    )
    figure.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(figure)


def plot_cpu_zoom(
    path: Path,
    cpu: dict[int, list[dict[str, int | float]]],
    maximum_threshold: int = 300,
    minimum_threshold: int = 1,
    maximum_by_n: dict[int, int] | None = None,
    connect_next_sample_by_n: set[int] | None = None,
) -> None:
    colors = ["#1769AA", "#D95F02", "#2A8C67"]
    figure, axes = plt.subplots(
        3, 1, figsize=(9.8, 10.0), sharex=maximum_by_n is None
    )
    for index, (axis, color, n) in enumerate(
        zip(axes, colors, sorted(cpu))
    ):
        panel_maximum = (
            maximum_by_n[n] if maximum_by_n is not None
            else maximum_threshold
        )
        rows = [
            row for row in cpu[n]
            if minimum_threshold <= int(row["S"]) <= panel_maximum
        ]
        if connect_next_sample_by_n and n in connect_next_sample_by_n:
            next_row = next(
                (
                    row for row in cpu[n]
                    if int(row["S"]) > panel_maximum
                ),
                None,
            )
            if next_row is not None:
                rows.append(next_row)
        thresholds = [int(row["S"]) for row in rows]
        median = [
            float(row["median_cpu_seconds"]) * 1_000 for row in rows
        ]
        q1 = [float(row["q1_cpu_seconds"]) * 1_000 for row in rows]
        q3 = [float(row["q3_cpu_seconds"]) * 1_000 for row in rows]
        axis.fill_between(
            thresholds,
            q1,
            q3,
            color=color,
            alpha=0.14,
            linewidth=0,
            label="Middle 50% across 15 seeds (IQR)",
        )
        axis.plot(
            thresholds,
            median,
            marker="o",
            markersize=3.5,
            linewidth=1.8,
            color=color,
            label="Median CPU time across 15 seeds",
        )
        axis.set_ylabel("CPU time (ms)")
        axis.set_title(
            f"n = {n:,} (S = {minimum_threshold}–{panel_maximum})"
            if maximum_by_n is not None else f"n = {n:,}"
        )
        axis.set_xlim(minimum_threshold, panel_maximum)
        if max(int(row["S"]) for row in cpu[n]) < panel_maximum:
            axis.text(
                thresholds[-1],
                max(q3),
                f"Measured only to S = {thresholds[-1]}",
                ha="right",
                va="bottom",
                fontsize=8,
                color=color,
            )
        finish_axis(axis)
        if maximum_by_n is not None:
            axis.set_xlabel("Threshold, S")
    if maximum_by_n is None:
        axes[-1].set_xlabel("Threshold, S")
    figure.suptitle(
        "CPU time near the minimum (panel-specific S ranges)"
        if maximum_by_n is not None else
        f"CPU time near the minimum (S = {minimum_threshold}–{maximum_threshold})",
        y=0.995,
    )
    figure.legend(
        handles=[
            Line2D([0], [0], color="#4A5561", marker="o",
                   label="Median CPU time across 15 seeds"),
            Patch(facecolor="#AAB6C2", alpha=0.45,
                  label="Middle 50% across 15 seeds (IQR)"),
        ],
        loc="lower center",
        bbox_to_anchor=(0.5, 0.005),
        ncol=2,
        frameon=False,
    )
    figure.tight_layout(rect=(0, 0.055, 1, 0.98))
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(figure)


def plot_regions(
    path: Path,
    regions: dict[int, tuple[int, int, float]],
    representative: int,
) -> None:
    figure, axis = plt.subplots(figsize=(9.0, 4.6))
    input_sizes = sorted(regions)
    y_positions = list(range(len(input_sizes)))
    for y, n in zip(y_positions, input_sizes):
        start, end, _regional_median = regions[n]
        axis.plot(
            [start, end],
            [y, y],
            color="#1769AA",
            linewidth=10,
            solid_capstyle="round",
        )
        axis.text(end + 4, y, f"S = {start}–{end}", va="center")
    axis.axvline(
        representative,
        color="#D95F02",
        linestyle="--",
        linewidth=2,
        label=f"Common representative S = {representative}",
    )
    axis.set_yticks(y_positions)
    axis.set_yticklabels([f"n = {n:,}" for n in input_sizes])
    axis.set_xlim(0, max(end for _start, end, _time in regions.values()) + 55)
    axis.set_xlabel("Threshold, S")
    axis.set_title("Suitable structural regions across input sizes")
    axis.legend(frameon=False, loc="upper left")
    finish_axis(axis)
    figure.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(figure)


def main() -> int:
    args = parse_arguments()
    comparisons = load_by_n(args.comparison_inputs)
    cpu = load_by_n(args.cpu_inputs)
    if set(comparisons) != set(cpu):
        raise ValueError("comparison and CPU inputs must cover the same n values")

    regions = {
        n: choose_suitable_region(comparisons[n], cpu[n])
        for n in comparisons
    }
    intersection_start = max(region[0] for region in regions.values())
    intersection_end = min(region[1] for region in regions.values())
    powers_of_two = [2**power for power in range(31)]
    representatives = [
        value
        for value in powers_of_two
        if intersection_start <= value <= intersection_end
    ]
    if not representatives:
        raise ValueError("suitable regions have no common power-of-two S")
    representative = representatives[0]

    summary_path = resolve_path(args.summary)
    figure_dir = resolve_path(args.figure_dir)
    write_summary(summary_path, comparisons, cpu)
    overview_comparisons = (
        powers_of_two_only(comparisons) if args.sparse_overview else comparisons
    )
    overview_cpu = powers_of_two_only(cpu) if args.sparse_overview else cpu
    plot_comparisons(
        figure_dir / "part_c_iii_comparisons_across_n.png",
        overview_comparisons,
        args.sparse_overview,
    )
    plot_cpu(
        figure_dir / "part_c_iii_cpu_time_across_n.png",
        overview_cpu,
        args.sparse_overview,
    )
    plot_cpu_zoom(
        figure_dir / "part_c_iii_cpu_time_zoom_1_300.png",
        cpu,
    )
    plot_cpu_zoom(
        figure_dir / "part_c_iii_cpu_time_zoom_32_512.png",
        cpu,
        maximum_threshold=512,
        minimum_threshold=32,
    )
    plot_cpu_zoom(
        figure_dir / "part_c_iii_cpu_time_zoom_by_n.png",
        cpu,
        minimum_threshold=32,
        maximum_by_n={10_000: 350, 100_000: 400, 1_000_000: 256},
        connect_next_sample_by_n={10_000, 100_000},
    )
    plot_regions(
        figure_dir / "part_c_iii_suitable_regions.png",
        regions,
        representative,
    )

    print(f"Wrote summary to {summary_path}")
    for n in sorted(regions):
        start, end, regional_median = regions[n]
        print(
            f"n={n}: suitable S={start}–{end}, "
            f"regional median CPU time={regional_median:.6f} ms"
        )
    print(
        f"Common intersection: S={intersection_start}–{intersection_end}; "
        f"representative S={representative}"
    )
    print(f"Wrote figures to {figure_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
