#!/usr/bin/env python3
"""Summarize and plot Part (c)(i): key comparisons versus n at fixed S."""

from __future__ import annotations

import argparse
import csv
import math
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
    "n",
    "S",
    "runs",
    "mean_key_comparisons",
    "sd_key_comparisons",
    "comparisons_per_n",
    "comparisons_over_n_log2_n",
    "mean_cpu_seconds",
    "sd_cpu_seconds",
]


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Analyze a fixed-s experiment CSV and create the Part (c)(i) "
            "summary and figures."
        )
    )
    parser.add_argument(
        "--input",
        default="results/fixed_s.csv",
        help="raw fixed-s CSV (default: results/fixed_s.csv)",
    )
    parser.add_argument(
        "--summary",
        default="results/fixed_s_summary.csv",
        help="derived summary CSV",
    )
    parser.add_argument(
        "--figure-dir",
        default="figures",
        help="directory for generated PNG figures",
    )
    return parser.parse_args()


def resolve_path(path_text: str) -> Path:
    path = Path(path_text).expanduser()
    if not path.is_absolute():
        path = PROJECT_DIR / path
    return path.resolve()


def load_rows(path: Path) -> list[dict[str, int | float]]:
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
            if raw["study"] != "fixed-s":
                raise ValueError(
                    f"line {line_number}: expected study=fixed-s"
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

            case = (int(row["n"]), int(row["seed"]))
            if case in seen_cases:
                raise ValueError(
                    f"line {line_number}: duplicate n/seed case {case}"
                )
            seen_cases.add(case)
            rows.append(row)

    if not rows:
        raise ValueError("input CSV contains no data rows")

    thresholds = {int(row["S"]) for row in rows}
    if len(thresholds) != 1:
        raise ValueError(
            f"fixed-s input must contain one S value, found {thresholds}"
        )

    maximum_values = {int(row["x"]) for row in rows}
    if len(maximum_values) != 1:
        raise ValueError(
            "fixed-s input must use one consistent maximum value x"
        )

    seeds_by_n: dict[int, set[int]] = defaultdict(set)
    for row in rows:
        seeds_by_n[int(row["n"])].add(int(row["seed"]))
    expected_seeds = next(iter(seeds_by_n.values()))
    for n, seeds in seeds_by_n.items():
        if seeds != expected_seeds:
            raise ValueError(
                f"n={n} uses seeds {sorted(seeds)}, expected "
                f"{sorted(expected_seeds)}"
            )

    return rows


def summarize(
    rows: list[dict[str, int | float]],
) -> list[dict[str, int | float]]:
    grouped: dict[int, list[dict[str, int | float]]] = defaultdict(list)
    for row in rows:
        grouped[int(row["n"])].append(row)

    summary: list[dict[str, int | float]] = []
    for n in sorted(grouped):
        group = grouped[n]
        comparisons = [int(row["key_comparisons"]) for row in group]
        cpu_times = [float(row["cpu_seconds"]) for row in group]
        mean_comparisons = statistics.fmean(comparisons)
        mean_cpu = statistics.fmean(cpu_times)

        summary.append(
            {
                "n": n,
                "S": int(group[0]["S"]),
                "runs": len(group),
                "mean_key_comparisons": mean_comparisons,
                "sd_key_comparisons": (
                    statistics.stdev(comparisons)
                    if len(comparisons) > 1
                    else 0.0
                ),
                "comparisons_per_n": mean_comparisons / n,
                "comparisons_over_n_log2_n": (
                    mean_comparisons / (n * math.log2(n))
                ),
                "mean_cpu_seconds": mean_cpu,
                "sd_cpu_seconds": (
                    statistics.stdev(cpu_times)
                    if len(cpu_times) > 1
                    else 0.0
                ),
            }
        )

    return summary


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
                    "n": row["n"],
                    "S": row["S"],
                    "runs": row["runs"],
                    "mean_key_comparisons": (
                        f"{row['mean_key_comparisons']:.1f}"
                    ),
                    "sd_key_comparisons": (
                        f"{row['sd_key_comparisons']:.2f}"
                    ),
                    "comparisons_per_n": (
                        f"{row['comparisons_per_n']:.6f}"
                    ),
                    "comparisons_over_n_log2_n": (
                        f"{row['comparisons_over_n_log2_n']:.6f}"
                    ),
                    "mean_cpu_seconds": f"{row['mean_cpu_seconds']:.9f}",
                    "sd_cpu_seconds": f"{row['sd_cpu_seconds']:.9f}",
                }
            )


def thousands(value: float, _position: float) -> str:
    return f"{value:,.0f}"


def compact_number(value: float, _position: float) -> str:
    if value >= 1_000_000:
        return f"{value / 1_000_000:g}M"
    if value >= 1_000:
        return f"{value / 1_000:g}K"
    return f"{value:g}"


def major_log_ticks(values: list[int]) -> list[int]:
    """Keep only powers of ten as labeled ticks on a logarithmic axis."""
    ticks = [
        value
        for value in values
        if math.isclose(
            math.log10(value), round(math.log10(value)), abs_tol=1e-12
        )
    ]
    if values[0] not in ticks:
        ticks.insert(0, values[0])
    if values[-1] not in ticks:
        ticks.append(values[-1])
    return ticks


def format_log_x_axis(axis: plt.Axes, n_values: list[int]) -> None:
    axis.set_xscale("log")
    axis.set_xticks(major_log_ticks(n_values))
    axis.xaxis.set_major_formatter(FuncFormatter(compact_number))
    axis.xaxis.set_minor_formatter(NullFormatter())


def apply_common_style(axis: plt.Axes) -> None:
    axis.grid(True, which="major", color="#D9DEE7", linewidth=0.8)
    axis.grid(True, which="minor", color="#EEF1F5", linewidth=0.5)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)


def plot_comparisons(
    path: Path, summary: list[dict[str, int | float]]
) -> None:
    n_values = [int(row["n"]) for row in summary]
    means = [float(row["mean_key_comparisons"]) for row in summary]
    deviations = [float(row["sd_key_comparisons"]) for row in summary]
    threshold = int(summary[0]["S"])

    n_log_n = [n * math.log2(n) for n in n_values]
    fitted_factor = sum(
        x * y for x, y in zip(n_log_n, means)
    ) / sum(x * x for x in n_log_n)
    fitted = [fitted_factor * x for x in n_log_n]

    figure, axis = plt.subplots(figsize=(9.2, 5.8))
    axis.errorbar(
        n_values,
        means,
        yerr=deviations,
        marker="o",
        markersize=6,
        linewidth=2.2,
        capsize=4,
        color="#1769AA",
        label="Mean key comparisons (5 seeds) ± 1 SD",
    )
    axis.plot(
        n_values,
        fitted,
        linestyle="--",
        linewidth=2,
        color="#D95F02",
        label=r"Fitted $k n\log_2 n$ reference",
    )

    format_log_x_axis(axis, n_values)
    axis.set_yscale("log")
    axis.yaxis.set_major_formatter(FuncFormatter(thousands))
    axis.set_xlabel("Input size, n (log scale)")
    axis.set_ylabel("Key comparisons (log scale)")
    axis.set_title(f"Key comparisons versus input size (fixed S = {threshold})")
    axis.legend(frameon=False, loc="upper left")
    apply_common_style(axis)
    figure.tight_layout()

    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(figure)


def plot_normalized(
    path: Path, summary: list[dict[str, int | float]]
) -> None:
    n_values = [int(row["n"]) for row in summary]
    normalized = [
        float(row["comparisons_over_n_log2_n"]) for row in summary
    ]
    threshold = int(summary[0]["S"])
    mean_ratio = statistics.fmean(normalized)

    figure, axis = plt.subplots(figsize=(9.2, 5.4))
    axis.plot(
        n_values,
        normalized,
        marker="o",
        markersize=6,
        linewidth=2.2,
        color="#2A8C67",
        label=r"$C(n)/(n\log_2 n)$",
    )
    axis.axhline(
        mean_ratio,
        linestyle="--",
        linewidth=1.8,
        color="#D95F02",
        label=f"Mean normalized ratio = {mean_ratio:.3f}",
    )

    format_log_x_axis(axis, n_values)
    axis.set_xlabel("Input size, n (log scale)")
    axis.set_ylabel(r"Normalized comparisons, $C(n)/(n\log_2 n)$")
    axis.set_title(
        f"Normalized key comparisons remain near constant (fixed S = {threshold})"
    )
    axis.legend(frameon=False, loc="best")
    apply_common_style(axis)
    figure.tight_layout()

    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(figure)


def main() -> int:
    args = parse_arguments()
    input_path = resolve_path(args.input)
    summary_path = resolve_path(args.summary)
    figure_dir = resolve_path(args.figure_dir)

    rows = load_rows(input_path)
    summary = summarize(rows)
    write_summary(summary_path, summary)

    comparisons_figure = figure_dir / "part_c_i_comparisons_vs_n.png"
    normalized_figure = figure_dir / "part_c_i_normalized_comparisons.png"
    plot_comparisons(comparisons_figure, summary)
    plot_normalized(normalized_figure, summary)

    print(f"Read {len(rows)} raw rows from {input_path}")
    print(f"Wrote {len(summary)} summary rows to {summary_path}")
    print(f"Wrote figure to {comparisons_figure}")
    print(f"Wrote figure to {normalized_figure}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
