"""End-to-end checks for random-input CLI, CSV contracts and failure handling."""
import argparse
import csv
import io
import math
from pathlib import Path
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", type=Path, required=True)
    binary = parser.parse_args().binary.resolve()

    def run(args, ok=True):
        result = subprocess.run([str(binary), *args], capture_output=True, text=True, timeout=30)
        if ok:
            assert result.returncode == 0, result.stderr
            assert not result.stderr, result.stderr
        else:
            assert result.returncode != 0 and "ERROR:" in result.stderr, result
            assert not result.stdout, "Invalid request must not print measurements"
        return result

    assert "--mode check|timing|count" in run(["--help"]).stdout
    expected_demo = ["0", "3", "1", "4", "7"]
    for algorithm in ["matrix", "heap"]:
        rows = list(csv.DictReader(io.StringIO(run(["--demo", algorithm]).stdout)))
        assert [row["distance"] for row in rows] == expected_demo

    common = ["--n", "20", "--m", "80", "--seed", "2001", "--source", "3",
              "--weight-min", "0", "--weight-max", "20"]
    first = run(common).stdout
    assert first == run(common).stdout, "Seed reproduces full check output"
    rows = list(csv.DictReader(io.StringIO(first)))
    assert len(rows) == 40
    by_algorithm = {}
    for row in rows:
        by_algorithm.setdefault(row["algorithm"], []).append(row)
    assert set(by_algorithm) == {"matrix_array", "list_indexed_heap"}
    assert [r["distance"] for r in by_algorithm["matrix_array"]] == [
        r["distance"] for r in by_algorithm["list_indexed_heap"]]
    assert all(r["distance"] == "0" and r["parent"] == "NONE"
               for r in rows if r["vertex"] == "3")

    counts = list(csv.DictReader(io.StringIO(run(common + ["--mode", "count"]).stdout)))
    assert len(counts) == 2
    a, b = counts
    assert a["algorithm"] == "matrix_array" and b["algorithm"] == "list_indexed_heap"
    assert int(a["min_scan_slots"]) == 400 and int(a["matrix_scan_slots"]) == 400
    assert int(b["adjacency_entries_scanned"]) == 160
    assert int(a["relax_attempts"]) == 80 and int(b["relax_attempts"]) == 80
    assert int(b["heap_inserts"]) == 20 and int(b["heap_extracts"]) == 20

    metadata = 'quoted, "suite"'
    timing_args = common + ["--mode", "timing", "--warmup", "1", "--repeats", "3",
                            "--order-seed", "99", "--suite", metadata, "--run-id", metadata]
    timing = list(csv.DictReader(io.StringIO(run(timing_args).stdout)))
    repeated = list(csv.DictReader(io.StringIO(run(timing_args).stdout)))
    assert len(timing) == 6
    assert [(r["algorithm"], r["order_in_pair"]) for r in timing] == [
        (r["algorithm"], r["order_in_pair"]) for r in repeated]
    for sample in range(3):
        pair = [r for r in timing if int(r["sample_index"]) == sample]
        assert {r["algorithm"] for r in pair} == {"matrix_array", "list_indexed_heap"}
        assert {r["order_in_pair"] for r in pair} == {"0", "1"}
    for row in timing:
        assert row["suite"] == metadata and row["run_id"] == metadata
        assert row["status"] == "ok" and row["distances_match"] == "true"
        assert math.isfinite(float(row["elapsed_ms"])) and float(row["elapsed_ms"]) > 0
        assert math.isclose(float(row["actual_density"]), 80 / 190)
        assert "connected-path-v1" in row["graph_id"]

    single = list(csv.DictReader(io.StringIO(run(["--n", "1", "--m", "0"]).stdout)))
    assert len(single) == 2 and all(row["distance"] == "0" for row in single)
    with tempfile.TemporaryDirectory(prefix="sc2001-cli-") as folder:
        path = Path(folder) / "check.csv"
        assert not run(common + ["--output", str(path)]).stdout
        assert path.read_text() == first
        run(common + ["--output", str(Path(folder) / "missing" / "out.csv")], ok=False)

    for args in [
        ["--n", "20"], ["--m", "80"], ["--n"], ["--demo", "invalid"],
        ["--n", "0", "--m", "0"], ["--n", "3", "--m", "1"],
        ["--n", "3", "--m", "4"], ["--n", "-1", "--m", "0"],
        ["--n", "2x", "--m", "1"], ["--n", str(2**100), "--m", "1"],
        common + ["--n", "20"], common + ["--mode", "invalid"],
        common + ["--mode", "timing", "--repeats", "0"],
        common + ["--warmup", "-1"], common + ["--source", "20"],
        common + ["--seed", "-1"], common + ["--unknown", "1"],
        ["--n", "3", "--m", "2", "--weight-min", "-1"],
        common + ["--run-id", ""], common + ["--output", ""],
    ]:
        run(args, ok=False)
    print("PASS: random-input CLI, paired measurements, counters, CSV quoting and errors")


if __name__ == "__main__":
    main()
