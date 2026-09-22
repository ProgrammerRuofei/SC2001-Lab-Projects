#!/usr/bin/env python3
"""Compare execution-order timing drift between fixed-n experiment sessions."""

from __future__ import annotations

import argparse
import csv
import math
import statistics
from collections import defaultdict
from pathlib import Path


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", help="raw fixed-n CSV files")
    parser.add_argument("--min-s", type=int, default=32)
    parser.add_argument("--max-s", type=int, default=260)
    parser.add_argument("--rolling-window", type=int, default=75)
    return parser.parse_args()


def median_by(rows: list[dict[str, str]], field: str) -> dict[int, float]:
    values: dict[int, list[float]] = defaultdict(list)
    for row in rows:
        values[int(row["S"])].append(float(row[field]))
    return {threshold: statistics.median(group) for threshold, group in values.items()}


def four_chunks(values: list[float]) -> list[list[float]]:
    count = len(values)
    return [values[index * count // 4 : (index + 1) * count // 4] for index in range(4)]


def pearson(left: list[float], right: list[float]) -> float:
    left_mean = statistics.mean(left)
    right_mean = statistics.mean(right)
    numerator = sum(
        (left_value - left_mean) * (right_value - right_mean)
        for left_value, right_value in zip(left, right)
    )
    left_ss = sum((value - left_mean) ** 2 for value in left)
    right_ss = sum((value - right_mean) ** 2 for value in right)
    denominator = math.sqrt(left_ss * right_ss)
    return numerator / denominator if denominator else float("nan")


def rolling_medians(values: list[float], window: int) -> list[tuple[int, float]]:
    if window > len(values):
        raise ValueError("rolling window exceeds row count")
    half = window // 2
    return [
        (index + 1, statistics.median(values[index - half : index + half + 1]))
        for index in range(half, len(values) - half)
    ]


def format_values(values: list[float]) -> str:
    return ", ".join(f"{value:+.3f}" for value in values)


def analyze(path: Path, min_s: int, max_s: int, window: int) -> None:
    with path.open(newline="", encoding="utf-8") as handle:
        all_rows = list(csv.DictReader(handle))
    rows = [row for row in all_rows if min_s <= int(row["S"]) <= max_s]
    if not rows:
        raise ValueError(f"no rows in S range for {path}")

    cpu_medians = median_by(rows, "cpu_seconds")
    comparison_medians = median_by(rows, "key_comparisons")
    residuals_ms = [
        (float(row["cpu_seconds"]) - cpu_medians[int(row["S"])]) * 1_000
        for row in rows
    ]
    comparison_residuals = [
        float(row["key_comparisons"])
        - comparison_medians[int(row["S"])]
        for row in rows
    ]

    chunks = four_chunks(residuals_ms)
    block_values: dict[int, list[float]] = defaultdict(list)
    seed_values: dict[int, list[float]] = defaultdict(list)
    for row, residual in zip(rows, residuals_ms):
        block_values[int(row["block"])].append(residual)
        seed_values[int(row["seed"])].append(residual)

    rolled = rolling_medians(residuals_ms, window)
    rolling_max = max(rolled, key=lambda item: item[1])
    rolling_min = min(rolled, key=lambda item: item[1])
    s62 = [
        float(row["cpu_seconds"]) * 1_000 for row in rows if int(row["S"]) == 62
    ]

    print(f"\nSESSION: {path}")
    print(f"rows={len(rows)}, S={min_s}..{max_s}")
    print(
        "execution_quarter_residual_medians_ms="
        + format_values([statistics.median(chunk) for chunk in chunks])
    )
    print(
        "block_residual_medians_ms="
        + ", ".join(
            f"block {block}: {statistics.median(values):+.3f}"
            for block, values in sorted(block_values.items())
        )
    )
    print(
        "seed_residual_median_range_ms="
        f"{min(statistics.median(values) for values in seed_values.values()):+.3f}.."
        f"{max(statistics.median(values) for values in seed_values.values()):+.3f}"
    )
    print(
        "rolling_median_ms="
        f"min {rolling_min[1]:+.3f} at row {rolling_min[0]}, "
        f"max {rolling_max[1]:+.3f} at row {rolling_max[0]}"
    )
    print(
        "cpu_vs_comparison_residual_pearson="
        f"{pearson(residuals_ms, comparison_residuals):+.3f}"
    )
    if s62:
        quartiles = statistics.quantiles(s62, n=4, method="inclusive")
        print(
            "S62_cpu_ms="
            f"median {statistics.median(s62):.3f}, mean {statistics.mean(s62):.3f}, "
            f"IQR {quartiles[0]:.3f}..{quartiles[2]:.3f}"
        )


def main() -> int:
    args = parse_arguments()
    if args.min_s > args.max_s:
        raise ValueError("--min-s must not exceed --max-s")
    if args.rolling_window < 3 or args.rolling_window % 2 == 0:
        raise ValueError("--rolling-window must be an odd integer of at least 3")
    for input_name in args.inputs:
        analyze(Path(input_name), args.min_s, args.max_s, args.rolling_window)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
