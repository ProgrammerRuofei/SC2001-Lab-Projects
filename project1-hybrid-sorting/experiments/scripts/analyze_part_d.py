#!/usr/bin/env python3
"""Summarize and plot Part (d): original Merge Sort versus Hybrid Merge Sort."""

from __future__ import annotations

import argparse
import csv
import statistics
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


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
ALGORITHMS = ("merge", "hybrid")
COLORS = {"merge": "#1769AA", "hybrid": "#2A8C67"}
SUMMARY_FIELDS = [
    "seed",
    "merge_key_comparisons",
    "hybrid_key_comparisons",
    "comparison_change_percent",
    "merge_cpu_seconds",
    "hybrid_cpu_seconds",
    "cpu_reduction_percent",
]


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Summarize and plot the Part (d) original-Merge-Sort-versus-"
            "Hybrid comparison."
        )
    )
    parser.add_argument(
        "--input",
        default="results/part_d_original_vs_hybrid_s128.csv",
        help="raw compare-study CSV",
    )
    parser.add_argument(
        "--summary",
        default="results/part_d_original_vs_hybrid_s128_summary.csv",
        help="derived per-seed summary CSV",
    )
    parser.add_argument(
        "--figure-dir",
        default="figures/part_d",
        help="directory for generated PNG figures",
    )
    return parser.parse_args()


def resolve_path(path_text: str) -> Path:
    path = Path(path_text).expanduser()
    if not path.is_absolute():
        path = PROJECT_DIR / path
    return path.resolve()


def load_rows(path: Path) -> list[dict[str, int | float | str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames is None:
            raise ValueError("input CSV has no header")

        missing = REQUIRED_FIELDS.difference(reader.fieldnames)
        if missing:
            raise ValueError(
                "input CSV is missing fields: " + ", ".join(sorted(missing))
            )

        rows: list[dict[str, int | float | str]] = []
        for line_number, raw in enumerate(reader, start=2):
            if raw["study"] != "compare":
                raise ValueError(f"line {line_number}: expected study=compare")
            if raw["algorithm"] not in ALGORITHMS:
                raise ValueError(
                    f"line {line_number}: unexpected algorithm "
                    f"{raw['algorithm']!r}"
                )
            try:
                row = {
                    "algorithm": raw["algorithm"],
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
            rows.append(row)

    if not rows:
        raise ValueError("input CSV contains no data rows")

    input_sizes = {row["n"] for row in rows}
    if len(input_sizes) != 1:
        raise ValueError(f"expected a single n value, found {input_sizes}")

    hybrid_thresholds = {row["S"] for row in rows if row["algorithm"] == "hybrid"}
    if len(hybrid_thresholds) != 1:
        raise ValueError(
            f"expected a single hybrid threshold S, found {hybrid_thresholds}"
        )

    seeds_by_algorithm: dict[str, set[int]] = defaultdict(set)
    for row in rows:
        seeds_by_algorithm[str(row["algorithm"])].add(int(row["seed"]))
    seed_sets = list(seeds_by_algorithm.values())
    if any(seeds != seed_sets[0] for seeds in seed_sets):
        raise ValueError("merge and hybrid rows must share the same seeds")

    return rows


def pair_by_seed(
    rows: list[dict[str, int | float | str]],
) -> list[dict[str, int | float]]:
    by_seed_algorithm = {
        (int(row["seed"]), str(row["algorithm"])): row for row in rows
    }
    seeds = sorted({int(row["seed"]) for row in rows})
    pairs: list[dict[str, int | float]] = []
    for seed in seeds:
        merge_row = by_seed_algorithm[(seed, "merge")]
        hybrid_row = by_seed_algorithm[(seed, "hybrid")]
        merge_comparisons = int(merge_row["key_comparisons"])
        hybrid_comparisons = int(hybrid_row["key_comparisons"])
        merge_cpu = float(merge_row["cpu_seconds"])
        hybrid_cpu = float(hybrid_row["cpu_seconds"])
        pairs.append(
            {
                "seed": seed,
                "merge_comparisons": merge_comparisons,
                "hybrid_comparisons": hybrid_comparisons,
                "comparison_change_percent": (
                    (hybrid_comparisons / merge_comparisons - 1) * 100
                ),
                "merge_cpu_seconds": merge_cpu,
                "hybrid_cpu_seconds": hybrid_cpu,
                "cpu_reduction_percent": (1 - hybrid_cpu / merge_cpu) * 100,
            }
        )
    return pairs


def write_summary(path: Path, pairs: list[dict[str, int | float]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=SUMMARY_FIELDS)
        writer.writeheader()
        for pair in pairs:
            writer.writerow(
                {
                    "seed": pair["seed"],
                    "merge_key_comparisons": pair["merge_comparisons"],
                    "hybrid_key_comparisons": pair["hybrid_comparisons"],
                    "comparison_change_percent": (
                        f"{pair['comparison_change_percent']:.3f}"
                    ),
                    "merge_cpu_seconds": f"{pair['merge_cpu_seconds']:.9f}",
                    "hybrid_cpu_seconds": f"{pair['hybrid_cpu_seconds']:.9f}",
                    "cpu_reduction_percent": (
                        f"{pair['cpu_reduction_percent']:.3f}"
                    ),
                }
            )
        writer.writerow(
            {
                "seed": "median",
                "merge_key_comparisons": statistics.median(
                    pair["merge_comparisons"] for pair in pairs
                ),
                "hybrid_key_comparisons": statistics.median(
                    pair["hybrid_comparisons"] for pair in pairs
                ),
                "comparison_change_percent": (
                    f"{statistics.median(pair['comparison_change_percent'] for pair in pairs):.3f}"
                ),
                "merge_cpu_seconds": (
                    f"{statistics.median(pair['merge_cpu_seconds'] for pair in pairs):.9f}"
                ),
                "hybrid_cpu_seconds": (
                    f"{statistics.median(pair['hybrid_cpu_seconds'] for pair in pairs):.9f}"
                ),
                "cpu_reduction_percent": (
                    f"{statistics.median(pair['cpu_reduction_percent'] for pair in pairs):.3f}"
                ),
            }
        )


def finish_axis(axis: plt.Axes) -> None:
    axis.grid(True, axis="y", color="#E3E9EF", linewidth=0.8)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.spines["bottom"].set_visible(False)
    axis.tick_params(axis="x", length=0)


def millions(value: float, _position: float) -> str:
    return f"{value / 1_000_000:g}M"


def jitter_offsets(count: int, spread: float = 0.11) -> list[float]:
    if count == 1:
        return [0.0]
    return [(index - (count - 1) / 2) * spread for index in range(count)]


def plot_paired_metric(
    path: Path,
    merge_values: list[float],
    hybrid_values: list[float],
    seeds: list[int],
    n: int,
    threshold: int,
    y_label: str,
    title: str,
    y_formatter: FuncFormatter | None,
    change_label: str,
) -> None:
    merge_median = statistics.median(merge_values)
    hybrid_median = statistics.median(hybrid_values)

    figure, axis = plt.subplots(figsize=(7.0, 5.8))
    x_positions = [0, 1]
    offsets = jitter_offsets(len(seeds))
    for offset, merge_value, hybrid_value, seed in zip(
        offsets, merge_values, hybrid_values, seeds
    ):
        axis.plot(
            [0 + offset, 1 + offset],
            [merge_value, hybrid_value],
            color="#8A97A6",
            linewidth=1.1,
            alpha=0.75,
            zorder=1,
        )
        axis.scatter(
            [0 + offset],
            [merge_value],
            color=COLORS["merge"],
            s=55,
            zorder=3,
            edgecolor="white",
            linewidth=0.9,
        )
        axis.scatter(
            [1 + offset],
            [hybrid_value],
            color=COLORS["hybrid"],
            s=55,
            zorder=3,
            edgecolor="white",
            linewidth=0.9,
        )

    # The diamond is offset so it does not conceal an individual seed point.
    median_x = [position + 0.27 for position in x_positions]
    axis.scatter(
        median_x,
        [merge_median, hybrid_median],
        marker="D",
        s=85,
        color=[COLORS["merge"], COLORS["hybrid"]],
        edgecolor="white",
        linewidth=1.1,
        zorder=4,
    )

    axis.set_xticks(x_positions)
    axis.set_xticklabels(
        ["Original\nMerge Sort", f"Hybrid Merge Sort\n(S = {threshold})"]
    )
    axis.set_xlim(-0.45, 1.55)
    axis.set_ylim(0, max(merge_values + hybrid_values) * 1.22)
    axis.set_ylabel(y_label)
    if y_formatter is not None:
        axis.yaxis.set_major_formatter(y_formatter)
    axis.set_title(f"{title} (n = {n:,})")

    top = max(merge_values + hybrid_values)
    axis.annotate(
        change_label,
        xy=(0.5, top * 1.11),
        ha="center",
        va="bottom",
        fontsize=11,
        color="#243B53",
    )

    seed_label = ", ".join(str(seed) for seed in seeds)
    axis.text(
        0.5,
        -0.14,
        f"Dots: individual seeds {seed_label} (connected by seed). "
        "Diamonds: per-algorithm medians.",
        transform=axis.transAxes,
        ha="center",
        va="top",
        fontsize=8,
        color="#64748B",
    )

    finish_axis(axis)
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
    n = int(rows[0]["n"])
    threshold = next(int(row["S"]) for row in rows if row["algorithm"] == "hybrid")
    pairs = pair_by_seed(rows)
    write_summary(summary_path, pairs)

    seeds = [int(pair["seed"]) for pair in pairs]
    merge_comparisons = [float(pair["merge_comparisons"]) for pair in pairs]
    hybrid_comparisons = [float(pair["hybrid_comparisons"]) for pair in pairs]
    merge_cpu = [float(pair["merge_cpu_seconds"]) for pair in pairs]
    hybrid_cpu = [float(pair["hybrid_cpu_seconds"]) for pair in pairs]

    comparison_change = statistics.median(
        float(pair["comparison_change_percent"]) for pair in pairs
    )
    cpu_reduction = statistics.median(
        float(pair["cpu_reduction_percent"]) for pair in pairs
    )

    comparisons_figure = figure_dir / "part_d_key_comparisons.png"
    cpu_figure = figure_dir / "part_d_cpu_time.png"

    plot_paired_metric(
        comparisons_figure,
        merge_comparisons,
        hybrid_comparisons,
        seeds,
        n,
        threshold,
        y_label="Key comparisons",
        title="Key comparisons: original Merge Sort vs Hybrid",
        y_formatter=FuncFormatter(millions),
        change_label=(
            f"Median of paired comparison changes: "
            f"{comparison_change:+.1f}%"
        ),
    )
    plot_paired_metric(
        cpu_figure,
        merge_cpu,
        hybrid_cpu,
        seeds,
        n,
        threshold,
        y_label="Sorting CPU time (s)",
        title="Sorting CPU time: original Merge Sort vs Hybrid",
        y_formatter=None,
        change_label=(
            f"Median of paired CPU-time reductions: "
            f"{cpu_reduction:.1f}%"
        ),
    )

    print(f"Read {len(rows)} raw rows from {input_path}")
    print(f"Wrote {len(pairs)} paired rows (+ median) to {summary_path}")
    print(f"Wrote figure to {comparisons_figure}")
    print(f"Wrote figure to {cpu_figure}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
