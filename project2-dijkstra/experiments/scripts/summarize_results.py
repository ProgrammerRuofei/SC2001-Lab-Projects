"""Validate complete paired data; aggregate calls, then independent graph seeds."""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import shutil
from statistics import median

from experiment_common import ALGORITHMS, quantile, read_csv, validate_records, write_csv


def summarize(run_dir, output_dir):
    env = json.loads((run_dir/"environment.json").read_text())
    if env["status"] != "complete":
        raise ValueError("Cannot summarize an incomplete/failed run")
    timings, counts = read_csv(run_dir/"timings.csv"), read_csv(run_dir/"counts.csv")
    grouped_t, grouped_c = defaultdict(list), defaultdict(list)
    for row in timings:
        grouped_t[row["graph_id"]].append(row)
    for row in counts:
        grouped_c[row["graph_id"]].append(row)
    ids = {j["graph_id"] for j in env["jobs"]}
    if len(ids) != len(env["jobs"]) or set(grouped_t) != ids or set(grouped_c) != ids:
        raise ValueError("Unexpected/missing/duplicate graph IDs")
    if len(timings) != env["timing_rows"] or len(counts) != env["count_rows"]:
        raise ValueError("Row totals differ from metadata")
    per_graph, paired = [], []
    summary_groups, ratio_groups = defaultdict(list), defaultdict(list)
    for job in env["jobs"]:
        graph_id = job["graph_id"]
        validate_records(grouped_t[graph_id], grouped_c[graph_id], job, env["run_id"])
        base = {k: job[k] for k in ("suite", "n", "m", "source", "weight_min", "weight_max")}
        base = dict(run_id=env["run_id"], **base)
        configuration = tuple(base.values())
        medians = {}
        for algorithm in sorted(ALGORITHMS):
            rows = [r for r in grouped_t[graph_id] if r["algorithm"] == algorithm]
            values = [float(r["elapsed_ms"]) for r in rows]
            counter = next(r for r in grouped_c[graph_id] if r["algorithm"] == algorithm)
            item = dict(base, graph_id=graph_id, graph_seed=job["graph_seed"],
                        actual_density=float(rows[0]["actual_density"]), algorithm=algorithm,
                        sample_count=len(values), median_ms=median(values),
                        q1_ms=quantile(values,.25), q3_ms=quantile(values,.75))
            for field in ("min_scan_slots", "matrix_scan_slots", "adjacency_entries_scanned",
                          "relax_attempts", "relax_successes", "heap_inserts", "heap_extracts", "heap_decreases"):
                item[field] = int(counter[field])
            per_graph.append(item)
            summary_groups[(configuration, algorithm)].append(item)
            medians[algorithm] = item["median_ms"]
        ratio = dict(base, graph_id=graph_id, graph_seed=job["graph_seed"],
            actual_density=per_graph[-1]["actual_density"],
            matrix_median_ms=medians["matrix_array"], heap_median_ms=medians["list_indexed_heap"],
            speedup=medians["matrix_array"]/medians["list_indexed_heap"])
        paired.append(ratio)
        ratio_groups[configuration].append(ratio)
    summaries, ratios = [], []
    for (_, algorithm), rows in summary_groups.items():
        values = [r["median_ms"] for r in rows]
        item = {k: rows[0][k] for k in ("run_id", "suite", "n", "m", "source", "weight_min", "weight_max", "actual_density")}
        item.update(algorithm=algorithm, graph_count=len(rows), timing_repeats=rows[0]["sample_count"],
                    median_ms=median(values),q1_ms=quantile(values,.25),q3_ms=quantile(values,.75))
        for field in ("matrix_scan_slots", "adjacency_entries_scanned", "relax_successes", "heap_decreases"):
            item["median_"+field] = median([r[field] for r in rows])
        summaries.append(item)
    for rows in ratio_groups.values():
        values = [r["speedup"] for r in rows]
        item = {k: rows[0][k] for k in ("run_id", "suite", "n", "m", "source", "weight_min", "weight_max", "actual_density")}
        item.update(graph_count=len(rows),median_ratio=median(values),q1_ratio=quantile(values,.25),
                    q3_ratio=quantile(values,.75),heap_faster_graphs=sum(v>1 for v in values))
        ratios.append(item)
    output_dir.mkdir(parents=True,exist_ok=False)
    for name,rows in (("per_graph.csv",per_graph),("summary.csv",summaries),
                      ("paired_speedup.csv",paired),("paired_speedup_summary.csv",ratios)):
        write_csv(output_dir/name,rows)
    shutil.copyfile(run_dir/"environment.json",output_dir/"environment.json")
    validation = {"status":"complete","graphs":len(env["jobs"]),"timing_rows":len(timings),
        "count_rows":len(counts),"per_graph_rows":len(per_graph),"summary_rows":len(summaries),
        "paired_rows":len(paired),"configurations":len(ratios),
        "method":"median within graph; median and linear type-7 Q1/Q3 across graph medians; same-graph ratios"}
    (output_dir/"validation.json").write_text(json.dumps(validation,indent=2)+"\n")
    print(json.dumps(validation))
    return validation


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir",required=True,type=Path)
    parser.add_argument("--output-dir",required=True,type=Path)
    args=parser.parse_args()
    summarize(args.run_dir.resolve(),args.output_dir.resolve())


if __name__ == "__main__":
    main()
