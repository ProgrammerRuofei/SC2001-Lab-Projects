"""Run both algorithms sequentially on shared graph specifications."""
import argparse
import csv
from datetime import datetime
import io
import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

from experiment_common import digest, jobs_from_config, validate_records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--binary", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--run-id")
    parser.add_argument("--timeout", type=float, default=180)
    parser.add_argument("--build-flags", default="-std=c++17 -O2 -Wall -Wextra -Wpedantic")
    args = parser.parse_args()
    config, binary, output = args.config.resolve(), args.binary.resolve(), args.output_dir.resolve()
    jobs = jobs_from_config(config)
    if not binary.is_file() or args.timeout <= 0:
        parser.error("A built binary and positive timeout are required")
    output.mkdir(parents=True, exist_ok=False)
    run_id = args.run_id or output.name
    project = Path(__file__).resolve().parents[2]
    def git(*arguments):
        result = subprocess.run(["git", *arguments], cwd=project, capture_output=True, text=True)
        return result.stdout.strip() if result.returncode == 0 else "unavailable"
    compiler = subprocess.run(["c++", "--version"], capture_output=True, text=True)
    metadata = {
        "run_id": run_id, "status": "running", "jobs": jobs,
        "started_singapore": datetime.now(ZoneInfo("Asia/Singapore")).isoformat(),
        "platform": platform.platform(), "machine": platform.machine(), "processor": platform.processor(),
        "python": sys.version, "compiler": compiler.stdout.strip(),
        "reported_build_flags": args.build_flags, "binary_sha256": digest(binary),
        "config_sha256": digest(config), "git_revision": git("rev-parse", "HEAD"),
        "working_tree_status": git("status", "--porcelain", "--", "project2-dijkstra"),
        "source_hashes": {str(p.relative_to(project)): digest(p) for folder in ("src", "include", "experiments/scripts") for p in sorted((project/folder).glob("*")) if p.is_file()},
        "timing_scope": "algorithm call with fresh state; generation, conversion, validation and output excluded",
        "counter_runs": "separate invocations with the same graph seed/configuration",
        "timing_rows": 0, "count_rows": 0, "commands": [],
    }
    shutil.copyfile(config, output/"config.csv")
    def save():
        (output/"environment.json").write_text(json.dumps(metadata, indent=2)+"\n")
    save()
    streams = [(output/name).open("w", newline="", encoding="utf-8") for name in ("timings.csv", "counts.csv")]
    writers = [None, None]
    try:
        for index, job in enumerate(jobs):
            arguments = ["--n", str(job["n"]), "--m", str(job["m"]), "--seed", str(job["graph_seed"]),
                "--source", str(job["source"]), "--weight-min", str(job["weight_min"]),
                "--weight-max", str(job["weight_max"]), "--warmup", str(job["warmup_repeats"]),
                "--repeats", str(job["timing_repeats"]), "--order-seed", str(job["order_seed"]),
                "--run-id", run_id, "--suite", job["suite"]]
            records = []
            for mode in ("timing", "count"):
                command = [str(binary), *arguments, "--mode", mode]
                metadata["commands"].append(command)
                result = subprocess.run(command, capture_output=True, text=True, timeout=args.timeout)
                if result.returncode:
                    (output/f"failed-{index}-{mode}.stdout.csv").write_text(result.stdout)
                    (output/f"failed-{index}-{mode}.stderr.txt").write_text(result.stderr)
                    raise RuntimeError(f"{job['suite']} seed {job['graph_seed']}: {result.stderr.strip()}")
                records.append(list(csv.DictReader(io.StringIO(result.stdout))))
            job["graph_id"] = validate_records(*records, job, run_id)
            for k, rows in enumerate(records):
                if writers[k] is None:
                    writers[k] = csv.DictWriter(streams[k], fieldnames=list(rows[0]), lineterminator="\n")
                    writers[k].writeheader()
                writers[k].writerows(rows)
                streams[k].flush()
            metadata["timing_rows"] += len(records[0])
            metadata["count_rows"] += len(records[1])
            save()
            print(f"[{index+1}/{len(jobs)}] {job['suite']} n={job['n']} m={job['m']} seed={job['graph_seed']} verified", flush=True)
        metadata["status"] = "complete"
    except Exception as error:
        metadata["status"] = "failed"
        metadata["failure"] = str(error)
        raise
    finally:
        for stream in streams:
            stream.close()
        metadata["finished_singapore"] = datetime.now(ZoneInfo("Asia/Singapore")).isoformat()
        save()
    print(f"Complete: {metadata['timing_rows']} timing rows, {metadata['count_rows']} count rows -> {output}")


if __name__ == "__main__":
    main()
