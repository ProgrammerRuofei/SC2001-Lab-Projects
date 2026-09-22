#!/usr/bin/env python3
"""Summarize the latest dense retest and create dependency-free SVG figures."""

from __future__ import annotations

import argparse
import csv
import math
import statistics
from collections import defaultdict
from pathlib import Path
from xml.sax.saxutils import escape


REGIONS = [
    ("32–60", 32, 60),
    ("61", 61, 61),
    ("62–121", 62, 121),
    ("122", 122, 122),
    ("123–243", 123, 243),
    ("244", 244, 244),
    ("245–260", 245, 260),
]


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--regions", required=True)
    parser.add_argument("--paired", required=True)
    parser.add_argument("--figure-dir", required=True)
    return parser.parse_args()


def quartiles(values: list[float]) -> tuple[float, float]:
    result = statistics.quantiles(values, n=4, method="inclusive")
    return result[0], result[2]


def load(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError("input contains no rows")
    return rows


def summarize(rows: list[dict[str, str]]) -> list[dict[str, float | int]]:
    grouped: dict[int, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[int(row["S"])].append(row)
    output: list[dict[str, float | int]] = []
    for threshold in sorted(grouped):
        group = grouped[threshold]
        comparisons = [int(row["key_comparisons"]) for row in group]
        cpu_ms = [float(row["cpu_seconds"]) * 1_000 for row in group]
        q1, q3 = quartiles(cpu_ms)
        output.append(
            {
                "S": threshold,
                "runs": len(group),
                "mean_comparisons": statistics.fmean(comparisons),
                "sd_comparisons": statistics.stdev(comparisons),
                "mean_cpu_ms": statistics.fmean(cpu_ms),
                "median_cpu_ms": statistics.median(cpu_ms),
                "q1_cpu_ms": q1,
                "q3_cpu_ms": q3,
            }
        )
    return output


def summarize_regions(rows: list[dict[str, str]]) -> list[dict[str, float | int | str]]:
    output: list[dict[str, float | int | str]] = []
    for label, start, stop in REGIONS:
        selected = [row for row in rows if start <= int(row["S"]) <= stop]
        cpu_ms = [float(row["cpu_seconds"]) * 1_000 for row in selected]
        q1, q3 = quartiles(cpu_ms)
        output.append(
            {
                "region": label,
                "thresholds": len({int(row["S"]) for row in selected}),
                "observations": len(selected),
                "mean_cpu_ms": statistics.fmean(cpu_ms),
                "median_cpu_ms": statistics.median(cpu_ms),
                "q1_cpu_ms": q1,
                "q3_cpu_ms": q3,
            }
        )
    return output


def two_sided_sign_test(positive: int, negative: int) -> float:
    non_ties = positive + negative
    if non_ties == 0:
        return 1.0
    tail = min(positive, negative)
    probability = 2 * sum(math.comb(non_ties, value) for value in range(tail + 1)) / (2**non_ties)
    return min(probability, 1.0)


def paired_analysis(rows: list[dict[str, str]]) -> list[dict[str, float | int | str]]:
    values = {
        (int(row["S"]), int(row["seed"])): float(row["cpu_seconds"]) * 1_000
        for row in rows
    }
    seeds = sorted({int(row["seed"]) for row in rows})
    output: list[dict[str, float | int | str]] = []
    for left, right in [(62, 63), (62, 64), (62, 65), (121, 122), (122, 123)]:
        differences = [values[(left, seed)] - values[(right, seed)] for seed in seeds]
        left_faster = sum(value < 0 for value in differences)
        right_faster = sum(value > 0 for value in differences)
        ties = sum(value == 0 for value in differences)
        output.append(
            {
                "comparison": f"S={left} minus S={right}",
                "seed_count": len(seeds),
                "left_faster": left_faster,
                "right_faster": right_faster,
                "ties": ties,
                "median_difference_ms": statistics.median(differences),
                "two_sided_sign_test_p": two_sided_sign_test(left_faster, right_faster),
            }
        )
    return output


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def svg_document(width: int, height: int, content: list[str]) -> str:
    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            '<rect width="100%" height="100%" fill="white"/>',
            '<style>text{font-family:Segoe UI,Arial,sans-serif;fill:#263238}.title{font-size:22px;font-weight:600}.axis{font-size:13px}.note{font-size:12px;fill:#546e7a}.grid{stroke:#e4e9ef;stroke-width:1}.frame{stroke:#607d8b;stroke-width:1.2}</style>',
            *content,
            "</svg>",
        ]
    )


def line_chart(
    rows: list[dict[str, float | int]],
    path: Path,
    value_key: str,
    title: str,
    y_label: str,
    q1_key: str | None = None,
    q3_key: str | None = None,
) -> None:
    width, height = 1040, 570
    left, right, top, bottom = 92, 28, 70, 72
    plot_w, plot_h = width - left - right, height - top - bottom
    x_values = [int(row["S"]) for row in rows]
    y_values = [float(row[value_key]) for row in rows]
    if q1_key and q3_key:
        limits = [float(row[q1_key]) for row in rows] + [float(row[q3_key]) for row in rows]
    else:
        limits = y_values
    y_min, y_max = min(limits), max(limits)
    padding = max((y_max - y_min) * 0.12, 0.5)
    y_min -= padding
    y_max += padding

    def x_map(value: float) -> float:
        return left + (value - min(x_values)) / (max(x_values) - min(x_values)) * plot_w

    def y_map(value: float) -> float:
        return top + (y_max - value) / (y_max - y_min) * plot_h

    content = [f'<text x="{left}" y="36" class="title">{escape(title)}</text>']
    for step in range(6):
        value = y_min + (y_max - y_min) * step / 5
        y = y_map(value)
        label = f"{value:.1f}" if abs(value) < 1_000 else f"{value / 1_000_000:.1f}M"
        content.extend(
            [
                f'<line x1="{left}" y1="{y:.2f}" x2="{left + plot_w}" y2="{y:.2f}" class="grid"/>',
                f'<text x="{left - 10}" y="{y + 4:.2f}" text-anchor="end" class="axis">{label}</text>',
            ]
        )
    for tick in [32, 61, 62, 96, 122, 128, 160, 192, 224, 244, 260]:
        x = x_map(tick)
        content.append(f'<line x1="{x:.2f}" y1="{top}" x2="{x:.2f}" y2="{top + plot_h}" class="grid"/>')
        content.append(f'<text x="{x:.2f}" y="{top + plot_h + 24}" text-anchor="middle" class="axis">{tick}</text>')
    for boundary in [61.5, 122.5, 244.5]:
        x = x_map(boundary)
        content.append(f'<line x1="{x:.2f}" y1="{top}" x2="{x:.2f}" y2="{top + plot_h}" stroke="#ef6c00" stroke-width="1.5" stroke-dasharray="6 5"/>')
    if q1_key and q3_key:
        for row in rows:
            x = x_map(float(row["S"]))
            q1 = y_map(float(row[q1_key]))
            q3 = y_map(float(row[q3_key]))
            content.append(f'<line x1="{x:.2f}" y1="{q1:.2f}" x2="{x:.2f}" y2="{q3:.2f}" stroke="#90caf9" stroke-width="4"/>')
    points = " ".join(f'{x_map(float(row["S"])):.2f},{y_map(float(row[value_key])):.2f}' for row in rows)
    content.append(f'<polyline points="{points}" fill="none" stroke="#1565c0" stroke-width="2.2"/>')
    for row in rows:
        content.append(f'<circle cx="{x_map(float(row["S"])):.2f}" cy="{y_map(float(row[value_key])):.2f}" r="2.7" fill="#1565c0"/>')
    content.extend(
        [
            f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}" class="frame"/>',
            f'<line x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}" class="frame"/>',
            f'<text x="{left + plot_w / 2}" y="{height - 18}" text-anchor="middle" class="axis">Threshold S</text>',
            f'<text x="24" y="{top + plot_h / 2}" text-anchor="middle" class="axis" transform="rotate(-90 24 {top + plot_h / 2})">{escape(y_label)}</text>',
            f'<text x="{left + plot_w - 2}" y="{top + 18}" text-anchor="end" class="note">orange dashed lines: recursion transitions</text>',
        ]
    )
    path.write_text(svg_document(width, height, content), encoding="utf-8")


def boundary_chart(
    rows: list[dict[str, str]],
    path: Path,
    thresholds: list[int],
    title: str,
) -> None:
    selected = [row for row in rows if int(row["S"]) in thresholds]
    grouped: dict[int, list[float]] = defaultdict(list)
    for row in selected:
        grouped[int(row["S"])].append(float(row["cpu_seconds"]) * 1_000)
    width, height = 760, 500
    left, right, top, bottom = 85, 35, 65, 70
    plot_w, plot_h = width - left - right, height - top - bottom
    all_values = [value for values in grouped.values() for value in values]
    y_min, y_max = min(all_values) - 0.6, max(all_values) + 0.6

    def x_map(value: int) -> float:
        return left + thresholds.index(value) / (len(thresholds) - 1) * plot_w

    def y_map(value: float) -> float:
        return top + (y_max - value) / (y_max - y_min) * plot_h

    content = [f'<text x="{left}" y="34" class="title">{escape(title)}</text>']
    for step in range(6):
        value = y_min + (y_max - y_min) * step / 5
        y = y_map(value)
        content.append(f'<line x1="{left}" y1="{y:.2f}" x2="{left + plot_w}" y2="{y:.2f}" class="grid"/>')
        content.append(f'<text x="{left - 10}" y="{y + 4:.2f}" text-anchor="end" class="axis">{value:.1f}</text>')
    for threshold in thresholds:
        values = sorted(grouped[threshold])
        q1, q3 = quartiles(values)
        median = statistics.median(values)
        x = x_map(threshold)
        content.append(f'<line x1="{x:.2f}" y1="{y_map(min(values)):.2f}" x2="{x:.2f}" y2="{y_map(max(values)):.2f}" stroke="#78909c"/>')
        content.append(f'<rect x="{x - 28:.2f}" y="{y_map(q3):.2f}" width="56" height="{y_map(q1) - y_map(q3):.2f}" fill="#bbdefb" stroke="#1565c0"/>')
        content.append(f'<line x1="{x - 28:.2f}" y1="{y_map(median):.2f}" x2="{x + 28:.2f}" y2="{y_map(median):.2f}" stroke="#0d47a1" stroke-width="3"/>')
        content.append(f'<text x="{x:.2f}" y="{top + plot_h + 25}" text-anchor="middle" class="axis">{threshold}</text>')
    content.extend(
        [
            f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}" class="frame"/>',
            f'<line x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}" class="frame"/>',
            f'<text x="{left + plot_w / 2}" y="{height - 18}" text-anchor="middle" class="axis">Threshold S</text>',
            f'<text x="24" y="{top + plot_h / 2}" text-anchor="middle" class="axis" transform="rotate(-90 24 {top + plot_h / 2})">CPU time (ms)</text>',
            f'<text x="{left + plot_w - 2}" y="{top + 17}" text-anchor="end" class="note">box: IQR; dark line: median; whisker: observed range</text>',
        ]
    )
    path.write_text(svg_document(width, height, content), encoding="utf-8")


def timing_drift_chart(rows: list[dict[str, str]], path: Path) -> None:
    grouped: dict[int, list[float]] = defaultdict(list)
    for row in rows:
        grouped[int(row["S"])].append(float(row["cpu_seconds"]) * 1_000)
    medians = {threshold: statistics.median(values) for threshold, values in grouped.items()}
    residuals = [
        float(row["cpu_seconds"]) * 1_000 - medians[int(row["S"])]
        for row in rows
    ]
    window = 75
    half = window // 2
    rolling = [
        (index + 1, statistics.median(residuals[index - half : index + half + 1]))
        for index in range(half, len(residuals) - half)
    ]
    quarters = [
        residuals[index * len(residuals) // 4 : (index + 1) * len(residuals) // 4]
        for index in range(4)
    ]
    quarter_medians = [statistics.median(values) for values in quarters]

    width, height = 1080, 520
    left, right, top, bottom = 88, 30, 70, 72
    plot_w, plot_h = width - left - right, height - top - bottom
    limit = max(abs(min(residuals)), abs(max(residuals)), 1.0) * 1.08

    def x_map(value: float) -> float:
        return left + (value - 1) / (len(residuals) - 1) * plot_w

    def y_map(value: float) -> float:
        return top + (limit - value) / (2 * limit) * plot_h

    content = [f'<text x="{left}" y="36" class="title">Latest retest: timing residual by execution order</text>']
    for quarter in range(4):
        start = quarter * len(residuals) / 4 + 1
        stop = (quarter + 1) * len(residuals) / 4
        x = x_map(start)
        width_q = x_map(stop) - x
        fill = "#f6f8fa" if quarter % 2 == 0 else "#eef4f8"
        content.append(f'<rect x="{x:.2f}" y="{top}" width="{width_q:.2f}" height="{plot_h}" fill="{fill}"/>')
        content.append(f'<text x="{x + width_q / 2:.2f}" y="{top + 18}" text-anchor="middle" class="note">Q{quarter + 1}: {quarter_medians[quarter]:+.1f} ms</text>')
    for step in range(5):
        value = -limit + 2 * limit * step / 4
        y = y_map(value)
        content.append(f'<line x1="{left}" y1="{y:.2f}" x2="{left + plot_w}" y2="{y:.2f}" class="grid"/>')
        content.append(f'<text x="{left - 10}" y="{y + 4:.2f}" text-anchor="end" class="axis">{value:.1f}</text>')
    for index, residual in enumerate(residuals, start=1):
        content.append(f'<circle cx="{x_map(index):.2f}" cy="{y_map(residual):.2f}" r="1.35" fill="#607d8b" opacity="0.28"/>')
    points = " ".join(f"{x_map(index):.2f},{y_map(value):.2f}" for index, value in rolling)
    content.append(f'<polyline points="{points}" fill="none" stroke="#ef6c00" stroke-width="2.4"/>')
    content.append(f'<line x1="{left}" y1="{y_map(0):.2f}" x2="{left + plot_w}" y2="{y_map(0):.2f}" stroke="#263238" stroke-width="1.2"/>')
    for tick in [1, 285, 570, 855, 1140]:
        content.append(f'<text x="{x_map(tick):.2f}" y="{top + plot_h + 24}" text-anchor="middle" class="axis">{tick}</text>')
    content.extend(
        [
            f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}" class="frame"/>',
            f'<line x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}" class="frame"/>',
            f'<text x="{left + plot_w / 2}" y="{height - 18}" text-anchor="middle" class="axis">Execution order</text>',
            f'<text x="24" y="{top + plot_h / 2}" text-anchor="middle" class="axis" transform="rotate(-90 24 {top + plot_h / 2})">CPU time minus median for the same S (ms)</text>',
            f'<text x="{left + plot_w - 2}" y="{top + plot_h - 12}" text-anchor="end" class="note">orange: rolling median over 75 records</text>',
        ]
    )
    path.write_text(svg_document(width, height, content), encoding="utf-8")


def main() -> int:
    args = parse_arguments()
    rows = load(Path(args.input))
    summary = summarize(rows)
    regions = summarize_regions(rows)
    paired = paired_analysis(rows)
    write_csv(Path(args.summary), summary)
    write_csv(Path(args.regions), regions)
    write_csv(Path(args.paired), paired)
    figure_dir = Path(args.figure_dir)
    figure_dir.mkdir(parents=True, exist_ok=True)
    line_chart(
        summary,
        figure_dir / "cpu_time_vs_s.svg",
        "median_cpu_ms",
        "Latest dense retest: CPU time versus S",
        "CPU time (ms)",
        "q1_cpu_ms",
        "q3_cpu_ms",
    )
    line_chart(
        summary,
        figure_dir / "comparisons_vs_s.svg",
        "mean_comparisons",
        "Latest dense retest: key comparisons versus S",
        "Mean key comparisons",
    )
    boundary_chart(
        rows,
        figure_dir / "boundary_61_65.svg",
        [61, 62, 63, 64, 65],
        "Latest retest near the 61/62 boundary",
    )
    boundary_chart(
        rows,
        figure_dir / "boundary_121_123.svg",
        [121, 122, 123],
        "Latest retest near the 122/123 boundary",
    )
    timing_drift_chart(rows, figure_dir / "timing_session_drift.svg")
    print(f"Read {len(rows)} rows and summarized {len(summary)} thresholds")
    print(
        f"Wrote {args.summary}, {args.regions}, {args.paired}, "
        f"and SVG figures to {figure_dir}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
