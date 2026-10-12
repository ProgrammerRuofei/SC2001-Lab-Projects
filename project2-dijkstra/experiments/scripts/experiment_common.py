"""Shared validation and CSV helpers for reproducible experiments."""
import csv
import hashlib
import math
from pathlib import Path

ALGORITHMS = {"matrix_array", "list_indexed_heap"}
PARAMS = ("suite", "n", "m", "graph_seed", "source", "weight_min", "weight_max")


def read_csv(path):
    with Path(path).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def write_csv(path, rows):
    if not rows:
        raise ValueError("Cannot write an empty result table")
    with Path(path).open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def jobs_from_config(path):
    jobs, seen = [], set()
    for row in read_csv(path):
        base = {k: row[k] for k in ("suite", "n", "m", "source", "weight_min", "weight_max",
                                    "warmup_repeats", "timing_repeats")}
        if not base["suite"]:
            raise ValueError("Empty suite")
        for k in base:
            if k != "suite":
                base[k] = int(base[k])
        n, m = base["n"], base["m"]
        if n < 1 or not n - 1 <= m <= n * (n - 1) // 2:
            raise ValueError("Invalid connected graph size")
        if not 0 <= base["source"] < n or not 0 <= base["weight_min"] <= base["weight_max"]:
            raise ValueError("Invalid source/weights")
        if base["warmup_repeats"] < 0 or base["timing_repeats"] < 1:
            raise ValueError("Invalid repetition counts")
        seeds = [int(seed) for seed in row["graph_seeds"].split(";")]
        if not seeds or any(seed < 0 or seed >= 2**64 for seed in seeds):
            raise ValueError("Invalid seeds")
        if row.get("requested_density"):
            expected = math.floor(float(row["requested_density"]) * (n * (n - 1) // 2))
            if m != expected:
                raise ValueError("Requested density does not match m")
        for seed in seeds:
            job = dict(base, graph_seed=seed)
            identity = tuple(str(job[k]) for k in PARAMS)
            if identity in seen:
                raise ValueError("Duplicate graph configuration")
            seen.add(identity)
            job["order_seed"] = int.from_bytes(hashlib.sha256(repr(identity).encode()).digest()[:8], "big")
            jobs.append(job)
    if not jobs:
        raise ValueError("Empty configuration")
    return jobs


def validate_records(timing, counts, job, run_id):
    repeats, n, m = job["timing_repeats"], job["n"], job["m"]
    if len(timing) != 2 * repeats or len(counts) != 2:
        raise ValueError("Missing timing/count rows")
    graph_ids = {r["graph_id"] for r in timing + counts}
    if len(graph_ids) != 1:
        raise ValueError("Unpaired graph IDs")
    for row in timing + counts:
        for key in ("suite", "n", "m", "graph_seed"):
            if str(row[key]) != str(job[key]):
                raise ValueError(f"Parameter mismatch: {key}")
        if row["run_id"] != run_id or row["algorithm"] not in ALGORITHMS:
            raise ValueError("Wrong run ID/algorithm")
    pairs = {}
    density = m / (n * (n - 1) / 2) if n > 1 else 0
    for row in timing:
        for key in ("source", "weight_min", "weight_max", "order_seed"):
            if str(row[key]) != str(job[key]):
                raise ValueError(f"Timing parameter mismatch: {key}")
        value = float(row["elapsed_ms"])
        if not math.isfinite(value) or value <= 0 or row["status"] != "ok" or row["distances_match"] != "true":
            raise ValueError("Invalid/unverified timing")
        if not math.isclose(float(row["actual_density"]), density, rel_tol=1e-12, abs_tol=1e-12):
            raise ValueError("Wrong density")
        sample = int(row["sample_index"])
        if sample not in range(repeats):
            raise ValueError("Unexpected sample index")
        pairs.setdefault(sample, []).append(row)
    for sample in range(repeats):
        pair = pairs.get(sample, [])
        if len(pair) != 2 or {r["algorithm"] for r in pair} != ALGORITHMS or {r["order_in_pair"] for r in pair} != {"0", "1"}:
            raise ValueError("Missing/duplicate paired sample")
    if {r["algorithm"] for r in counts} != ALGORITHMS:
        raise ValueError("Missing/duplicate counter algorithm")
    for row in counts:
        fields = ("min_scan_slots", "matrix_scan_slots", "adjacency_entries_scanned", "relax_attempts",
                  "relax_successes", "heap_inserts", "heap_extracts", "heap_decreases")
        c = {k: int(row[k]) for k in fields}
        if any(value < 0 for value in c.values()) or c["relax_attempts"] != m:
            raise ValueError("Invalid operation counts")
        if not n - 1 <= c["relax_successes"] <= m:
            raise ValueError("Invalid successful relaxations")
        if row["algorithm"] == "matrix_array":
            if c["min_scan_slots"] != n*n or c["matrix_scan_slots"] != n*n or any(c[k] for k in ("adjacency_entries_scanned", "heap_inserts", "heap_extracts", "heap_decreases")):
                raise ValueError("Matrix counter invariant failed")
        elif c["adjacency_entries_scanned"] != 2*m or c["heap_inserts"] != n or c["heap_extracts"] != n or c["heap_decreases"] != c["relax_successes"]-(n-1) or c["min_scan_slots"] or c["matrix_scan_slots"]:
            raise ValueError("Heap counter invariant failed")
    return next(iter(graph_ids))


def quantile(values, q):
    """Linear interpolation at (N-1)*q, equivalent to the common type-7 quantile."""
    ordered = sorted(values)
    if not ordered:
        raise ValueError("No quantile data")
    position = (len(ordered) - 1) * q
    low = math.floor(position)
    high = math.ceil(position)
    return ordered[low] + (ordered[high] - ordered[low]) * (position - low)
