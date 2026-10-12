# Experiment parameters and measurement rules

**Formal main-suite parameters below remain proposed. Four pilot entry-point configurations have been executed successfully.** Algorithms, generation, independent validation and the C++ measurement CLI are implemented. Python batch/summary/plot processing remains pending; see running-guide.md for working commands and pilot records.

## Shared setup

Simple connected undirected graphs; m counts logical edges and lists have 2m entries. Maximum M=n(n-1)/2; actual density p=m/M. Source 0, integer weights uniformly sampled in [1,1000].

Main graph seeds: 2001..2005. For every graph and algorithm: two warmups and seven formal timing calls. Use an independently seeded, recorded order choice for each pair. Run both implementations on one machine with the same C++17 optimized build, proposed -O2. Time with steady_clock and preserve fractional milliseconds. Run diagnostic counts separately.

## Generator

Shuffle vertices, connect consecutive vertices into a spanning path, then add distinct non-loop pairs until exactly m edges exist. Assign weights and canonicalize/sort the edges; build both representations from that same edge set.

Validate n>=1 and feasible connected edge counts. This construction is not uniform sampling of all connected graphs. Dense generation may sample candidate pairs to avoid excessive rejection; record the generator version. Seed reproducibility is scoped to the recorded generator/toolchain, since distribution implementations may differ across environments.

## S1: sparse growth, m=4n

| n | m |
| ---: | ---: |
| 100 | 400 |
| 200 | 800 |
| 400 | 1600 |
| 800 | 3200 |
| 1600 | 6400 |
| 3200 | 12800 |

Plot time against n. Matrix scans grow as n²; the heap bound becomes O(n log n). Auxiliary normalization and doubling ratios can support interpretation without proving asymptotic behavior.

## S2: dense growth, target density 0.5

Use m=floor(0.5*M).

| n | m |
| ---: | ---: |
| 100 | 2475 |
| 200 | 9950 |
| 400 | 39900 |
| 800 | 159800 |
| 1600 | 639600 |

Plot time against n. Here m=Θ(n²). Matrix time is Θ(n²); heap worst-case upper bound is O(n²log n). Inspect actual successful relaxations/decreases rather than assuming the worst bound is attained.

## S3: fixed n=1000, varying density

M=499500; m=floor(p*M).

| Requested p | Exact m |
| ---: | ---: |
| 0.005 | 2497 |
| 0.01 | 4995 |
| 0.02 | 9990 |
| 0.05 | 24975 |
| 0.10 | 49950 |
| 0.25 | 124875 |
| 0.50 | 249750 |
| 0.90 | 449550 |

Plot time and paired speed ratio against actual density or m. Matrix scan counts stay fixed; list entries increase. Graphs at different densities are not guaranteed nested, but both algorithms share each graph within a configuration.

The [main table](../experiments/configs/main.csv) has 19 configurations: 95 graphs and 1330 formal timing samples, excluding warmups/checks/counting. These are planned totals, not observed results.

## Optional S4: fixed m=8000

Use n=200,400,800,1600,3200 with m=8000. Density changes as n grows; state this when interpreting. See [optional table](../experiments/configs/optional-fixed-m.csv). Complete main suites first.

## Pilot

The [pilot table](../experiments/configs/pilot.csv) uses (100,400), (400,39900), (1600,639600), and (3200,12800), seed 2001, one warmup and three timing calls per algorithm.

Check distance equality, counters, timing boundaries, output format, timing resolution, and resource usage. A 3200×3200 matrix of 8-byte cells alone needs 81,920,000 bytes, about 78.1 MiB; other live structures add memory. If necessary, record reduced parameters in an actual table without rewriting measured values.

## Per-graph execution

1. Generate and convert the graph outside timing.
2. Compare both full distance arrays outside timing; stop on mismatch.
3. Warm up both algorithms using fresh state.
4. Run seven pairs, each algorithm once per pair, recording order.
5. Time the algorithm function including auxiliary initialization/allocation and result creation; graphs are read-only.
6. Stop the clock before result validation, output, and subsequent result destruction. Consume results so unused work is not optimized away.
7. Run each algorithm once with diagnostic counters, outside formal timing.
8. Preserve failures and metadata; failures are not zero-time samples.

## Raw fields

Timing CSV:

```text
run_id,suite,graph_id,n,m,actual_density,graph_seed,source,
weight_min,weight_max,algorithm,sample_index,order_seed,order_in_pair,
elapsed_ms,distances_match,status
```

Count CSV:

```text
run_id,suite,graph_id,n,m,graph_seed,algorithm,
min_scan_slots,matrix_scan_slots,adjacency_entries_scanned,
relax_attempts,relax_successes,heap_inserts,heap_extracts,heap_decreases
```

Algorithm labels: matrix_array, list_indexed_heap. graph_id includes suite/parameters/seed/generator version. Only successful validated rows enter summaries; record missing/failed cases explicitly.

## Aggregation

First compute the median of seven calls for each graph/algorithm. Then compute the median and Q1/Q3 across five graph medians per configuration/algorithm. State the quantile convention. These represent five independent generated graphs, not 35 graphs; IQR is not automatically a confidence interval.

For each graph compute R=matrix_median/heap_median, then aggregate R across seeds. R>1 favors heap; R<1 favors matrix. Do not mix environments or use unpaired graphs for this ratio.

## Environment and limitations

Record run date/timezone, OS, CPU/RAM, compiler/version/flags, source revision or build identifier, uncommitted changes, Python/plotting versions, generator version, seeds, weights, repetitions, clock, and timing boundaries.

Report limited sizes/seeds, connected graph generation bias, weight distribution, single-machine scope, and exclusion of representation construction. See the [execution plan](execution-plan.md) for proposed commands and analysis steps.
