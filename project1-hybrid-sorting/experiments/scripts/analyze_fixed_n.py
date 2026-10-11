#!/usr/bin/env python3
"""Summarize and plot Part (c)(ii): metrics versus S at fixed n."""

from __future__ import annotations

import argparse
import csv
import statistics
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, NullFormatter


PROJECT_DIR = Path(__file__).resolve().parents[2]
REQUIRED_FIELDS = {
    "study",
    "algorithm",
    "n",
    "S",
    "x",
    "seed",
    "key_comparisons",
    "cpu_seconds",
}
SUMMARY_FIELDS = [
    "S",
    "n",
    "runs",
    "mean_key_comparisons",
    "sd_key_comparisons",
    "baseline_S",
    "comparison_change_vs_baseline_percent",
    "mean_cpu_seconds",
    "median_cpu_seconds",
    "q1_cpu_seconds",
    "q3_cpu_seconds",
    "sd_cpu_seconds",
    "cpu_change_vs_baseline_percent",
]


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Analyze a fixed-n experiment CSV and create the Part (c)(ii) "
            "summary and figures."
        )
    )
    parser.add_argument(
        "--input",
        default="results/fixed_n_1m.csv",
        help="raw fixed-n CSV (default: results/fixed_n_1m.csv)",
    )
    parser.add_argument(
        "--summary",
        default="results/fixed_n_1m_summary.csv",
        help="derived summary CSV",
    )
    parser.add_argument(
        "--figure-dir",
        default="figures/fixed_n_1m",
        help="directory for generated PNG figures",
    )
    parser.add_argument(
        "--plot-s-values",
        nargs="+",
        type=int,
        metavar="S",
        help="show only these measured thresholds in the figures; keep the full summary CSV",
    )
    return parser.parse_args()


def resolve_path(path_text: str) -> Path:
    path = Path(path_text).expanduser()
    if not path.is_absolute():
        path = PROJECT_DIR / path
    return path.resolve()


def load_rows(
    path: Path, expected_studies: set[str] | None = None
) -> list[dict[str, int | float]]:
    if expected_studies is None:
        expected_studies = {"fixed-n"}
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames is None:
            raise ValueError("input CSV has no header")

        missing = REQUIRED_FIELDS.difference(reader.fieldnames)
        if missing:
            raise ValueError(
                "input CSV is missing fields: " + ", ".join(sorted(missing))
            )

        rows: list[dict[str, int | float]] = []
        seen_cases: set[tuple[int, int]] = set()
        for line_number, raw in enumerate(reader, start=2):
            if raw["study"] not in expected_studies:
                raise ValueError(
                    f"line {line_number}: expected study in "
                    f"{sorted(expected_studies)}"
                )
            if raw["algorithm"] != "hybrid":
                raise ValueError(
                    f"line {line_number}: expected algorithm=hybrid"
                )

            try:
                row = {
                    "n": int(raw["n"]),
                    "S": int(raw["S"]),
                    "x": int(raw["x"]),
                    "seed": int(raw["seed"]),
                    "key_comparisons": int(raw["key_comparisons"]),
                    "cpu_seconds": float(raw["cpu_seconds"]),
                }
            except ValueError as error:
                raise ValueError(
                    f"line {line_number}: invalid numeric value"
                ) from error

            if row["n"] < 1 or row["S"] < 1 or row["x"] < 1:
                raise ValueError(
                    f"line {line_number}: n, S, and x must be positive"
                )
            if row["seed"] < 0:
                raise ValueError(
                    f"line {line_number}: seed must be nonnegative"
                )
            if row["key_comparisons"] < 0 or row["cpu_seconds"] < 0:
                raise ValueError(
                    f"line {line_number}: measurements must be nonnegative"
                )

            case = (int(row["S"]), int(row["seed"]))
            if case in seen_cases:
                raise ValueError(
                    f"line {line_number}: duplicate S/seed case {case}"
                )
            seen_cases.add(case)
            rows.append(row)

    if not rows:
        raise ValueError("input CSV contains no data rows")

    input_sizes = {int(row["n"]) for row in rows}
    if len(input_sizes) != 1:
        raise ValueError(
            f"fixed-n input must contain one n value, found {input_sizes}"
        )

    maximum_values = {int(row["x"]) for row in rows}
    if len(maximum_values) != 1:
        raise ValueError(
            "fixed-n input must use one consistent maximum value x"
        )

    seeds_by_threshold: dict[int, set[int]] = defaultdict(set)
    for row in rows:
        seeds_by_threshold[int(row["S"])].add(int(row["seed"]))
    expected_seeds = next(iter(seeds_by_threshold.values()))
    for threshold, seeds in seeds_by_threshold.items():
        if seeds != expected_seeds:
            raise ValueError(
                f"S={threshold} uses seeds {sorted(seeds)}, expected "
                f"{sorted(expected_seeds)}"
            )

    return rows


def summarize(
    rows: list[dict[str, int | float]],
) -> list[dict[str, int | float]]:
    grouped: dict[int, list[dict[str, int | float]]] = defaultdict(list)
    for row in rows:
        grouped[int(row["S"])].append(row)

    intermediate: list[dict[str, int | float]] = []
    for threshold in sorted(grouped):
        group = grouped[threshold]
        comparisons = [int(row["key_comparisons"]) for row in group]
        cpu_times = [float(row["cpu_seconds"]) for row in group]
        if len(cpu_times) > 1:
            cpu_quartiles = statistics.quantiles(
                cpu_times, n=4, method="inclusive"
            )
            q1_cpu = cpu_quartiles[0]
            q3_cpu = cpu_quartiles[2]
        else:
            q1_cpu = cpu_times[0]
            q3_cpu = cpu_times[0]
        intermediate.append(
            {
                "S": threshold,
                "n": int(group[0]["n"]),
                "runs": len(group),
                "mean_key_comparisons": statistics.fmean(comparisons),
                "sd_key_comparisons": (
                    statistics.stdev(comparisons)
                    if len(comparisons) > 1
                    else 0.0
                ),
                "mean_cpu_seconds": statistics.fmean(cpu_times),
                "median_cpu_seconds": statistics.median(cpu_times),
                "q1_cpu_seconds": q1_cpu,
                "q3_cpu_seconds": q3_cpu,
                "sd_cpu_seconds": (
                    statistics.stdev(cpu_times)
                    if len(cpu_times) > 1
                    else 0.0
                ),
            }
        )

    baseline_comparisons = float(intermediate[0]["mean_key_comparisons"])
    baseline_cpu = float(intermediate[0]["mean_cpu_seconds"])
    for row in intermediate:
        row["baseline_S"] = int(intermediate[0]["S"])
        row["comparison_change_vs_baseline_percent"] = (
            (float(row["mean_key_comparisons"]) / baseline_comparisons - 1)
            * 100
        )
        row["cpu_change_vs_baseline_percent"] = (
            (float(row["mean_cpu_seconds"]) / baseline_cpu - 1) * 100
        )

    return intermediate


def write_summary(
    path: Path, summary: list[dict[str, int | float]]
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=SUMMARY_FIELDS)
        writer.writeheader()
        for row in summary:
            writer.writerow(
                {
                    "S": row["S"],
                    "n": row["n"],
                    "runs": row["runs"],
                    "mean_key_comparisons": (
                        f"{row['mean_key_comparisons']:.1f}"
                    ),
                    "sd_key_comparisons": (
                        f"{row['sd_key_comparisons']:.2f}"
                    ),
                    "baseline_S": row["baseline_S"],
                    "comparison_change_vs_baseline_percent": (
                        f"{row['comparison_change_vs_baseline_percent']:.3f}"
                    ),
                    "mean_cpu_seconds": f"{row['mean_cpu_seconds']:.9f}",
                    "median_cpu_seconds": (
                        f"{row['median_cpu_seconds']:.9f}"
                    ),
                    "q1_cpu_seconds": f"{row['q1_cpu_seconds']:.9f}",
                    "q3_cpu_seconds": f"{row['q3_cpu_seconds']:.9f}",
                    "sd_cpu_seconds": f"{row['sd_cpu_seconds']:.9f}",
                    "cpu_change_vs_baseline_percent": (
                        f"{row['cpu_change_vs_baseline_percent']:.3f}"
                    ),
                }
            )


def millions(value: float, _position: float) -> str:
    return f"{value / 1_000_000:g}M"


def labeled_thresholds(thresholds: list[int]) -> list[int]:
    if len(thresholds) <= 10:
        return thresholds

    labels = [
        threshold
        for threshold in thresholds
        if threshold & (threshold - 1) == 0
    ]
    if thresholds[0] not in labels:
        labels.insert(0, thresholds[0])
    if thresholds[-1] not in labels:
        labels.append(thresholds[-1])
    return labels


def apply_common_style(axis: plt.Axes, thresholds: list[int]) -> None:
    axis.set_xscale("log", base=2)
    axis.set_xticks(labeled_thresholds(thresholds))
    axis.xaxis.set_major_formatter(
        FuncFormatter(lambda value, _position: f"{value:g}")
    )
    axis.xaxis.set_minor_formatter(NullFormatter())
    axis.grid(True, which="major", color="#D9DEE7", linewidth=0.8)
    axis.grid(True, which="minor", color="#EEF1F5", linewidth=0.5)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)


def plot_comparisons(
    path: Path, summary: list[dict[str, int | float]]
) -> None:
    thresholds = [int(row["S"]) for row in summary]
    means = [float(row["mean_key_comparisons"]) for row in summary]
    deviations = [float(row["sd_key_comparisons"]) for row in summary]
    n = int(summary[0]["n"])

    figure, axis = plt.subplots(figsize=(9.2, 5.6))
    axis.plot(
        thresholds,
        means,
        marker="o",
        markersize=5,
        linewidth=2.2,
        color="#1769AA",
        label="Mean key comparisons",
    )
    axis.fill_between(
        thresholds,
        [mean - deviation for mean, deviation in zip(means, deviations)],
        [mean + deviation for mean, deviation in zip(means, deviations)],
        color="#1769AA",
        alpha=0.12,
        linewidth=0,
        label="Variation across seeds (±1 SD)",
    )
    if 128 in thresholds and 128 < max(thresholds) <= 256:
        axis.axvline(
            128,
            color="#D95F02",
            linestyle="--",
            linewidth=1.6,
            label="S = 128 selected for Part (d)",
        )
    axis.set_ylim(bottom=0)
    axis.yaxis.set_major_formatter(FuncFormatter(millions))
    axis.set_xlabel("Threshold, S (log2 scale)")
    axis.set_ylabel("Key comparisons")
    axis.set_title(f"Key comparisons versus threshold (fixed n = {n:,})")
    axis.legend(frameon=False, loc="upper left")
    apply_common_style(axis, thresholds)
    figure.tight_layout()

    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(figure)


def plot_cpu_time(
    path: Path, summary: list[dict[str, int | float]]
) -> None:
    thresholds = [int(row["S"]) for row in summary]
    medians_ms = [
        float(row["median_cpu_seconds"]) * 1_000 for row in summary
    ]
    q1_ms = [float(row["q1_cpu_seconds"]) * 1_000 for row in summary]
    q3_ms = [float(row["q3_cpu_seconds"]) * 1_000 for row in summary]
    n = int(summary[0]["n"])

    figure, axis = plt.subplots(figsize=(9.2, 5.6))
    axis.plot(
        thresholds,
        medians_ms,
        marker="o",
        markersize=5,
        linewidth=2.2,
        color="#2A8C67",
        label="Median CPU time across seeds",
    )
    axis.fill_between(
        thresholds,
        q1_ms,
        q3_ms,
        color="#2A8C67",
        alpha=0.14,
        linewidth=0,
        label="Middle 50% of runs (IQR)",
    )
    lower = min(q1_ms)
    upper = max(q3_ms)
    padding = max((upper - lower) * 0.10, 0.5)
    axis.set_ylim(max(0, lower - padding), upper + padding)
    axis.set_xlabel("Threshold, S (log2 scale)")
    axis.set_ylabel("Sorting CPU time (ms)")
    axis.set_title(f"CPU time versus threshold (fixed n = {n:,})")
    axis.legend(frameon=False, loc="upper left")
    apply_common_style(axis, thresholds)
    figure.tight_layout()

    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(figure)


def plot_cpu_time_zoom(
    path: Path, summary: list[dict[str, int | float]]
) -> bool:
    zoomed = [
        row for row in summary if 32 <= int(row["S"]) <= 256
    ]
    if len(zoomed) < 3:
        return False

    thresholds = [int(row["S"]) for row in zoomed]
    medians_ms = [
        float(row["median_cpu_seconds"]) * 1_000 for row in zoomed
    ]
    q1_ms = [float(row["q1_cpu_seconds"]) * 1_000 for row in zoomed]
    q3_ms = [float(row["q3_cpu_seconds"]) * 1_000 for row in zoomed]
    n = int(zoomed[0]["n"])
    runs = int(zoomed[0]["runs"])

    lower = min(q1_ms)
    upper = max(q3_ms)
    padding = max((upper - lower) * 0.12, 0.5)

    figure, axis = plt.subplots(figsize=(10.2, 5.8))
    axis.plot(
        thresholds,
        medians_ms,
        marker="o",
        markersize=4,
        linewidth=1.8,
        color="#2A8C67",
        label=f"Median CPU time across {runs} seeds",
    )
    axis.fill_between(
        thresholds,
        q1_ms,
        q3_ms,
        color="#2A8C67",
        alpha=0.14,
        linewidth=0,
        label="Middle 50% of runs (IQR)",
    )
    if 128 in thresholds and 128 < max(thresholds) <= 256:
        axis.axvline(
            128,
            color="#D95F02",
            linestyle="--",
            linewidth=1.6,
            label="S = 128 selected for Part (d)",
        )
    axis.set_ylim(max(0, lower - padding), upper + padding)
    axis.set_xlim(32, 256)
    axis.set_xticks(list(range(32, 257, 32)))
    axis.set_xlabel("Threshold, S")
    axis.set_ylabel("Sorting CPU time (ms)")
    axis.set_title(
        f"CPU time for S = 32–256 (fixed n = {n:,})"
    )
    axis.legend(frameon=False, loc="upper left")
    axis.grid(True, color="#E3E7ED", linewidth=0.8)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    figure.tight_layout()

    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(figure)
    return True


def main() -> int:
    args = parse_arguments()
    input_path = resolve_path(args.input)
    summary_path = resolve_path(args.summary)
    figure_dir = resolve_path(args.figure_dir)

    rows = load_rows(input_path)
    summary = summarize(rows)

    plot_summary = summary
    if args.plot_s_values is not None:
        requested = set(args.plot_s_values)
        available = {int(row["S"]) for row in summary}
        missing = requested - available
        if missing:
            raise ValueError(f"thresholds not measured in input CSV: {sorted(missing)}")
        if len(requested) < 2:
            raise ValueError("at least two distinct thresholds are needed for a plot")
        plot_summary = [row for row in summary if int(row["S"]) in requested]

    write_summary(summary_path, summary)

    comparisons_figure = figure_dir / "part_c_ii_comparisons_vs_s.png"
    cpu_figure = figure_dir / "part_c_ii_cpu_time_vs_s.png"
    cpu_zoom_figure = figure_dir / "part_c_ii_cpu_time_zoom.png"
    plot_comparisons(comparisons_figure, plot_summary)
    plot_cpu_time(cpu_figure, plot_summary)
    wrote_zoom = plot_cpu_time_zoom(cpu_zoom_figure, plot_summary)

    print(f"Read {len(rows)} raw rows from {input_path}")
    print(f"Wrote {len(summary)} summary rows to {summary_path}")
    print(f"Plotted {len(plot_summary)} measured thresholds")
    print(f"Wrote figure to {comparisons_figure}")
    print(f"Wrote figure to {cpu_figure}")
    if wrote_zoom:
        print(f"Wrote figure to {cpu_zoom_figure}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
