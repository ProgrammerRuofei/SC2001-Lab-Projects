# Running the random-input and measurement entry points

The C++ generator, matrix/array algorithm, indexed-heap algorithm, shared test reference, CLI and check/timing/count modes are implemented. Python batch/summary/plot processors are still TODOs.

## Build and full correctness gate

From project2-dijkstra:

```bash
make -j2 all test
```

This runs graph, matrix, heap, list-Dijkstra, independent Bellman-Ford integration, generator, and Python end-to-end CLI checks. No module should report PENDING now. The Python CLI test uses only the standard library.

## Fixed teaching input

```bash
./build/dijkstra_benchmark --demo matrix
./build/dijkstra_benchmark --demo heap
```

Both return distances [0,3,1,4,7] and the selected predecessors as vertex,distance,parent CSV.

## Random input: verify results

```bash
./build/dijkstra_benchmark --n 20 --m 80 --seed 2001 --mode check
```

The default mode is check. The generator makes one connected graph and converts it both ways. Both algorithms run and their complete distance arrays must agree before any output. Check CSV contains algorithm,vertex,distance,parent rows for both versions.

Optional settings: --source (default 0), --weight-min (1), --weight-max (1000). Valid weights are nonnegative, and the generator rejects unsafe path bounds. Same seed/configuration/toolchain reproduces input.

## Paired timing

```bash
./build/dijkstra_benchmark --n 1000 --m 4000 --seed 2001 \
  --mode timing --warmup 2 --repeats 7 --order-seed 42 \
  --run-id manual-v1 --suite sparse-check
```

Before timing, input generation, conversion and full cross-version distance checking are complete. Both versions are warmed up. Each formal pair runs each algorithm once; a separate seeded RNG chooses the order. Seven pairs produce 14 rows, excluding warmups.

steady_clock measures only each algorithm call, including its fresh state/allocation and result construction. Result validation, serialization, and later result destruction happen after the stop timestamp. Diagnostic counters are disabled during timing. Preserve fractional milliseconds.

Each returned result is checked against its version's baseline after measurement. A mismatch throws and the process exits nonzero, rather than reporting a valid zero-time result.

## Separate operation counts

```bash
./build/dijkstra_benchmark --n 1000 --m 4000 --seed 2001 \
  --mode count --run-id manual-v1 --suite sparse-check
```

This generates the same input under the same environment but records two independent counter calls, not timing samples. Connected full-scan expectations: matrix selection/row slots=n², list entries=2m, heap inserts/extracts=n. Counting does not reuse timing state.

## Write CSV to a file

Create the output directory first:

```bash
mkdir -p results/raw/manual-v1
./build/dijkstra_benchmark --n 20 --m 80 --seed 2001 --mode check \
  --output results/raw/manual-v1/check.csv
```

Without --output, CSV goes to stdout. With --output, the named file is written and stdout stays empty. An existing named output file is replaced; use a fresh run directory to preserve previous measurements. Commas, quotes, and newlines in --suite/--run-id metadata are CSV-escaped.

## CLI validation and failures

Random input requires both --n and --m. Numeric options accept decimal integers in range; missing/unknown/duplicate options, invalid modes, invalid source, impossible edge counts, invalid weights and zero timing repetitions are rejected. stderr reports ERROR and the process returns 1. --help lists defaults and supported options.

If a runtime error occurs after some timing rows were written, the nonzero exit marks the invocation incomplete. Batch processing must retain the failure, verify sample completeness and avoid treating a partial run as a complete configuration. The runner remains the next implementation stage.

## CSV schemas

Timing:

```text
run_id,suite,graph_id,n,m,actual_density,graph_seed,source,weight_min,weight_max,
algorithm,sample_index,order_seed,order_in_pair,elapsed_ms,distances_match,status
```

Count:

```text
run_id,suite,graph_id,n,m,graph_seed,algorithm,min_scan_slots,matrix_scan_slots,
adjacency_entries_scanned,relax_attempts,relax_successes,heap_inserts,heap_extracts,heap_decreases
```

Sample indices and pair positions start at 0. Successful timing rows use distances_match=true and status=ok. Graph IDs contain suite, generator version, n/m, graph seed, weight range and source. Actual density is m/(n(n-1)/2), or 0 for n=1.

The shared Bellman-Ford reference runs only in small correctness tests; large benchmark calls perform cross-version distance checking, not timed Bellman-Ford work.

## Completed pilot entry-point validation

Four pilot configurations were exercised in separate timing/count modes: (100,400), (400,39900), (1600,639600), (3200,12800). Each used seed 2001, one warmup and three measured pairs. Validated output comprises 24 timing rows and 8 count rows.

Local raw files are under results/raw/pilot-entrypoint-check/: timings.csv, counts.csv and environment.json. Metadata preserves commands, build flags, compiler/platform, revision/working-tree status and binary/config hashes. This checks the pipeline; it does not establish final performance conclusions. Raw files are ignored by Git.

Next: implement the three Python processors, retain metadata for formal runs, then execute main.csv and analyze within-graph medians, across-seed summaries, paired ratios and charts as described in experiment-plan.md.
