#!/usr/bin/env python3
"""Run reproducible SC2001 sorting experiments through the C++ executable."""

from __future__ import annotations

import argparse
import csv
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import NamedTuple


PROJECT_DIR = Path(__file__).resolve().parents[2]
EXECUTABLE = PROJECT_DIR / "build" / "hybrid_sort"
CSV_FIELDS = [
    "study",
    "algorithm",
    "n",
    "S",
    "x",
    "seed",
    "key_comparisons",
    "cpu_seconds",
]

DEFAULT_MAX_VALUE = 10_000_000
DEFAULT_SEEDS = [2001, 2002, 2003, 2004, 2005]
DEFAULT_PILOT_SEEDS = [2001, 2002]
DEFAULT_COMPARE_SEEDS = [2001, 2002, 2003]
DEFAULT_N_VALUES = [1_000, 10_000, 100_000, 1_000_000, 10_000_000]
DEFAULT_PILOT_N_VALUES = [1_000, 10_000, 100_000]
DEFAULT_OPTIMAL_N_VALUES = [10_000, 100_000, 1_000_000]
DEFAULT_S_VALUES = [1, 2, 4, 8, 16, 32, 64, 128]
DEFAULT_PILOT_S_VALUES = [1, 8, 20, 32, 64]


class ExperimentCase(NamedTuple):
    algorithm: str
    n: int
    threshold: int
    max_value: int
    seed: int


def positive_integer(text: str) -> int:
    value = int(text)
    if value < 1:
        raise argparse.ArgumentTypeError("value must be at least 1")
    return value


def nonnegative_integer(text: str) -> int:
    value = int(text)
    if value < 0:
        raise argparse.ArgumentTypeError("value must be nonnegative")
    return value


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run a configured experiment matrix through build/hybrid_sort and "
            "write reproducible CSV output."
        )
    )
    parser.add_argument(
        "study",
        choices=["pilot", "fixed-s", "fixed-n", "optimal-s", "compare"],
    )
    parser.add_argument("--output", required=True, help="CSV output path")
    parser.add_argument(
        "--max-value",
        type=positive_integer,
        default=DEFAULT_MAX_VALUE,
        help=f"inclusive x value (default: {DEFAULT_MAX_VALUE})",
    )
    parser.add_argument(
        "--seeds",
        nargs="+",
        type=nonnegative_integer,
        help="override the default seed list",
    )
    parser.add_argument(
        "--n-values",
        nargs="+",
        type=positive_integer,
        help="override the study's default n values",
    )
    parser.add_argument(
        "--s-values",
        nargs="+",
        type=positive_integer,
        help="override the candidate S values",
    )
    parser.add_argument(
        "--fixed-s",
        type=positive_integer,
        default=20,
        help="fixed S for the fixed-s study (default: 20)",
    )
    parser.add_argument(
        "--fixed-n",
        type=positive_integer,
        default=1_000_000,
        help="fixed n for the fixed-n study (default: 1000000)",
    )
    parser.add_argument(
        "--compare-threshold",
        type=positive_integer,
        help="selected Hybrid S; required for the compare study",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print planned commands without building or running them",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="replace an existing output CSV and metadata file",
    )
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="skip make test and make; use only after a verified build",
    )
    return parser.parse_args()


def unique(values: list[int]) -> list[int]:
    return list(dict.fromkeys(values))


def select_seeds(args: argparse.Namespace) -> list[int]:
    if args.seeds:
        return unique(args.seeds)
    if args.study == "pilot":
        return DEFAULT_PILOT_SEEDS
    if args.study == "compare":
        return DEFAULT_COMPARE_SEEDS
    return DEFAULT_SEEDS


def build_cases(args: argparse.Namespace) -> list[ExperimentCase]:
    seeds = select_seeds(args)
    max_value = args.max_value
    cases: list[ExperimentCase] = []

    if args.study == "pilot":
        n_values = unique(args.n_values or DEFAULT_PILOT_N_VALUES)
        s_values = unique(args.s_values or DEFAULT_PILOT_S_VALUES)
        for n in n_values:
            for seed in seeds:
                cases.append(ExperimentCase("merge", n, 0, max_value, seed))
                for threshold in s_values:
                    cases.append(
                        ExperimentCase(
                            "hybrid", n, threshold, max_value, seed
                        )
                    )

    elif args.study == "fixed-s":
        n_values = unique(args.n_values or DEFAULT_N_VALUES)
        for n in n_values:
            for seed in seeds:
                cases.append(
                    ExperimentCase(
                        "hybrid", n, args.fixed_s, max_value, seed
                    )
                )

    elif args.study == "fixed-n":
        n_values = unique(args.n_values or [args.fixed_n])
        s_values = unique(args.s_values or DEFAULT_S_VALUES)
        for n in n_values:
            for threshold in s_values:
                for seed in seeds:
                    cases.append(
                        ExperimentCase(
                            "hybrid", n, threshold, max_value, seed
                        )
                    )

    elif args.study == "optimal-s":
        n_values = unique(args.n_values or DEFAULT_OPTIMAL_N_VALUES)
        s_values = unique(args.s_values or DEFAULT_S_VALUES)
        for n in n_values:
            for threshold in s_values:
                for seed in seeds:
                    cases.append(
                        ExperimentCase(
                            "hybrid", n, threshold, max_value, seed
                        )
                    )

    else:
        if args.compare_threshold is None:
            raise ValueError(
                "compare requires --compare-threshold selected from Part (c)"
            )
        n_values = unique(args.n_values or [10_000_000])
        for n in n_values:
            for seed in seeds:
                cases.append(ExperimentCase("merge", n, 0, max_value, seed))
                cases.append(
                    ExperimentCase(
                        "hybrid",
                        n,
                        args.compare_threshold,
                        max_value,
                        seed,
                    )
                )

    return cases


def command_for(case: ExperimentCase) -> list[str]:
    return [
        str(EXECUTABLE),
        case.algorithm,
        str(case.n),
        str(case.threshold),
        str(case.max_value),
        str(case.seed),
    ]


def run_checked(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=PROJECT_DIR,
        check=True,
        text=True,
        capture_output=True,
    )


def build_and_test() -> None:
    print("Running correctness tests...", file=sys.stderr)
    subprocess.run(["make", "test"], cwd=PROJECT_DIR, check=True)
    print("Building experiment executable...", file=sys.stderr)
    subprocess.run(["make"], cwd=PROJECT_DIR, check=True)


def parse_cpp_row(case: ExperimentCase, output: str) -> dict[str, str]:
    lines = [line for line in output.splitlines() if line.strip()]
    if len(lines) != 1:
        raise ValueError(
            f"expected one CSV row from C++ runner, received {len(lines)}"
        )

    fields = next(csv.reader(lines))
    if len(fields) != 7:
        raise ValueError(
            f"expected 7 C++ CSV fields, received {len(fields)}: {fields}"
        )

    algorithm, n, threshold, max_value, seed, comparisons, cpu_seconds = fields
    expected = [
        case.algorithm,
        str(case.n),
        str(case.threshold),
        str(case.max_value),
        str(case.seed),
    ]
    if fields[:5] != expected:
        raise ValueError(
            f"C++ row parameters {fields[:5]} do not match request {expected}"
        )
    if int(comparisons) < 0 or float(cpu_seconds) < 0:
        raise ValueError("C++ runner returned a negative measurement")

    return {
        "algorithm": algorithm,
        "n": n,
        "S": threshold,
        "x": max_value,
        "seed": seed,
        "key_comparisons": comparisons,
        "cpu_seconds": cpu_seconds,
    }


def safe_command_output(command: list[str]) -> str:
    try:
        result = run_checked(command)
        return result.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"


def metadata(args: argparse.Namespace, cases: list[ExperimentCase]) -> dict:
    return {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "study": args.study,
        "case_count": len(cases),
        "max_value": args.max_value,
        "seeds": select_seeds(args),
        "git_commit": safe_command_output(["git", "rev-parse", "HEAD"]),
        "git_dirty": bool(
            safe_command_output(["git", "status", "--porcelain"])
        ),
        "hostname": platform.node(),
        "platform": platform.platform(),
        "python": platform.python_version(),
        "compiler": safe_command_output(["c++", "--version"]).splitlines()[0],
        "cpu_time_definition": (
            "std::clock CPU seconds around sorting only; input generation and "
            "sorted-result validation are excluded"
        ),
        "command": sys.argv,
    }


def resolve_output(path_text: str) -> Path:
    path = Path(path_text).expanduser()
    if not path.is_absolute():
        path = PROJECT_DIR / path
    return path.resolve()


def main() -> int:
    args = parse_arguments()

    try:
        cases = build_cases(args)
        output_path = resolve_output(args.output)

        if args.dry_run:
            print(f"Planned cases: {len(cases)}")
            for case in cases:
                print(" ".join(command_for(case)))
            return 0

        metadata_path = output_path.with_suffix(".meta.json")
        if not args.overwrite:
            existing = [
                path for path in (output_path, metadata_path) if path.exists()
            ]
            if existing:
                names = ", ".join(str(path) for path in existing)
                raise FileExistsError(
                    f"output already exists: {names}; use --overwrite to replace"
                )

        if not args.skip_build:
            build_and_test()
        elif not EXECUTABLE.exists():
            raise FileNotFoundError(
                f"experiment executable not found: {EXECUTABLE}"
            )

        output_path.parent.mkdir(parents=True, exist_ok=True)
        partial_path = output_path.with_suffix(output_path.suffix + ".partial")

        with partial_path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS)
            writer.writeheader()

            for index, case in enumerate(cases, start=1):
                print(
                    f"[{index}/{len(cases)}] "
                    f"{case.algorithm} n={case.n} S={case.threshold} "
                    f"seed={case.seed}",
                    file=sys.stderr,
                )
                result = run_checked(command_for(case))
                row = parse_cpp_row(case, result.stdout)
                writer.writerow({"study": args.study, **row})
                stream.flush()

        os.replace(partial_path, output_path)
        metadata_path.write_text(
            json.dumps(metadata(args, cases), indent=2) + "\n",
            encoding="utf-8",
        )

        print(f"Wrote {len(cases)} rows to {output_path}", file=sys.stderr)
        print(f"Wrote metadata to {metadata_path}", file=sys.stderr)
        return 0

    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

