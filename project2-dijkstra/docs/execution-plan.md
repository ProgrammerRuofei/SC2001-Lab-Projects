# Detailed execution plan: assignment parts (a), (b), and (c)

This plan describes how to complete the project from the current interface scaffold. **A compilable framework, shared conversion, fixed fixtures and output formatting are available. Core algorithm/generator/benchmark functions and Python processing are explicit TODOs; no experiments have been run.** Technical choices and parameters below are proposals, not additional course requirements.

Assignment parts (a)/(b)/(c) are distinct from Member A/B/C. Part (c) is a shared team deliverable, not exclusively Member C's task.

## 1. Deliverables and overall workflow

| Part | Required work | Evidence to produce |
| --- | --- | --- |
| (a) | Matrix + array Dijkstra; theoretical and empirical analysis | Correct implementation, quadratic cost derivation, measured time/counters |
| (b) | Adjacency-list array + min-heap Dijkstra; theoretical and empirical analysis | Correct indexed heap and algorithm, operation-based bound, measured time/counters |
| (c) | Compare implementations and circumstances | Same-graph ratios, sparse/dense analysis, conditional recommendations and limitations |

Let n be the number of vertices and m the number of logical edges. Proposed deliverables are code, correctness tests, configuration tables, original CSV, environment records, summary CSV, charts, and a report. Confirm the course's actual submission format and deadline separately.

Workflow:

```text
Shared contracts and graph conversion
        |
Matrix algorithm + independent heap + graph generator
        |
Heap algorithm + independent correctness checks
        |
Measurement CLI and Python automation
        |
Pilot -> formal experiments -> aggregation -> charts
        |
Analysis of (a)/(b) -> comparison (c) -> final report
```

## 2. Shared foundation

Current file/owner status is summarized in [framework guide](framework-guide.md) and [team roles](team-roles.md).

Use C++17 for algorithms, generation, and timing; Python for batch runs and plotting. Main experiments use simple connected undirected graphs, source 0, weights in [1,1000], and vertex IDs 0..n-1. Tests include zero-weight edges, disconnected inputs, and other sources.

Generate one canonical EdgeListGraph for each parameter/seed combination. Each undirected edge occurs once as u<v. Convert that same graph to a symmetric matrix and lists with 2m entries. Never generate the two algorithm inputs independently.

Use 64-bit distances, INF for absent matrix edges, and 0 on the diagonal. Validate safe distance bounds and skip INF before addition. Both algorithms return full distance and predecessor arrays and use fresh state on every call. Equal priorities are resolved by vertex ID; strictly shorter paths alone update predecessors.

### Implementation sequence

| Order | File/task | Purpose | Acceptance check |
| --- | --- | --- | --- |
| 1 | graph.cpp | Validate edges and convert representations | Same vertices, edges, weights; exactly 2m list entries |
| 2 | Makefile and minimal test entry points | Build modules and tests | Clean build; optimized/debug configurations distinguished |
| 3 | dijkstra_matrix.cpp | Complete algorithm for (a) | Hand-computed and boundary cases |
| 4 | min_heap.cpp | Independent indexed heap | Ordering, updates, position invariants |
| 5 | dijkstra_heap.cpp | Complete algorithm for (b) | Full distances agree with independent reference |
| 6 | generation.cpp | Exact reproducible n/m graphs | Counts, weight range, connectivity, reproducibility |
| 7 | main.cpp | Check/timing/count CLI | One graph completes a trustworthy measurement pipeline |
| 8 | Python scripts | Batch execution, aggregation, plotting | Pilot outputs can be traced and verified |

Graph generation and reference tests can progress alongside algorithm work. Formal measurement starts only after both algorithms pass correctness checks. Exact interface contracts are in [architecture](architecture.md).

## 3. Part (a): adjacency matrix and array

### A1. Implement the algorithm

Use MatrixGraph.weights, dist, settled, and parent arrays.

```text
Set all distances to INF, parents to empty, settled flags to false
Set dist[source] = 0
Repeat at most n rounds:
    Scan all vertex indices to find the minimum unsettled distance
    Stop if no finite candidate exists
    Mark the selected vertex u as settled
    Scan all n columns in matrix[u]:
        Skip settled vertices and absent edges
        Safely compute candidate = dist[u] + weight(u,v)
        If candidate < dist[v]:
            Update dist[v] and parent[v]
Return distances and parents
```

Build incrementally: initialization, minimum-selection loop, relaxation, then invalid-source/INF/overflow checks and optional counters. Use the five-vertex teaching graph before large random graphs.

The array priority queue is implemented by unsorted state arrays and linear extract-min behavior. Do not substitute sorting or a heap in this version.

### A2. Validate correctness

Cover a single vertex, one edge, the teaching graph, a shorter indirect route, unreachable vertices, an isolated source, zero weights, equal shortest paths, another source, and large safe weights.

The [teaching graph](learning-guide.md) must return [0,3,1,4,7]. Validate predecessor paths, allowing alternative equal-weight paths. Under full scans, its minimum-selection and matrix-row counters each equal 25.

Later run both versions against the independent test reference, not just against each other.

### A3. Derive complexity

Initialization costs O(n). Up to n linear minimum selections cost O(n²), and up to n full row scans cost O(n²). Thus simple-graph time is O(n²), and full connected traversal under these scans has Θ(n²) work.

Graph storage is Θ(n²); auxiliary state excluding input is Θ(n). Explain why few edges do not remove the matrix's absent-edge inspections.

### A4. Analyze its empirical results

All three shared suites run both algorithms. Filter matrix_array rows for the (a) write-up.

| Suite | Question | Diagnostic explanation |
| --- | --- | --- |
| S1 sparse growth | How does time grow with n when m=4n? | Both main scan counters are n² |
| S2 dense growth | How does time grow when density is fixed? | Main scans still n²; relaxation behavior can vary |
| S3 fixed n | What changes as m increases? | Scan counts fixed; useful updates and constants can change |

Optionally calculate T(2n)/T(n), ideally near 4 when quadratic work dominates, and T/n². These are supporting diagnostics, not proof; small sizes, allocation, cache behavior, and noise can affect ratios.

### A5. Completion criteria

- [ ] Required matrix/array structures are used.
- [ ] Hand cases, boundaries, and independent reference checks pass.
- [ ] Report derives the costs and explains sparse-graph scanning.
- [ ] Results from all main suites are traceable and interpreted.

## 4. Part (b): adjacency lists and indexed binary min-heap

### B1. Implement and test the heap independently

A heap entry contains (vertex,key), where key is tentative source distance. position[v] locates that vertex's entry or records its absence.

For zero-based index i: parent=(i-1)/2 when i>0, left=2i+1, right=2i+2.

Recommended method order:

1. precedes: compare key, then vertex ID.
2. swap_entries: exchange entries and update both positions.
3. sift_up: exchange with a larger parent until the invariant holds.
4. sift_down: exchange with the smaller child until the invariant holds.
5. push_or_decrease: append and sift up if absent; update and sift up if an existing key decreases; otherwise no change.
6. extract_min: save the root, replace it with the last entry, update positions, mark the removed vertex absent, and sift down. Handle empty/single-entry cases explicitly.

Test ordering, ties, repeated decreases, root/interior/leaf updates, invalid operations, and position consistency. Compare random actions against a simple linear-scan reference. Common bugs are forgotten position updates after swaps and after root replacement.

### B2. Integrate the heap with Dijkstra

```text
Initialize distances, predecessors, settled flags, and an empty indexed heap
Set dist[source] = 0 and insert source:0
While the heap is not empty:
    Extract the minimum vertex u and settle it
    Iterate only over actual entries (v,weight) in adj[u]:
        Skip settled v
        Safely compute candidate = dist[u] + weight
        If candidate < dist[v]:
            Update dist[v] and parent[v]
            Insert v if absent, or decrease its existing heap key
Return distances and parents
```

Start with the source only and discover reachable vertices. There is at most one heap entry per vertex; unreachable vertices retain INF. Every distance improvement must also update the heap priority. Settled vertices are never reinserted.

This is not lazy deletion. If changing the design to repeated entries, change the contracts, tests, counters, and theoretical analysis together.

### B3. Validate correctness

Reuse (a)'s test cases and add graphs that improve the same vertex repeatedly. The teaching graph has 5 inserts, 5 extracts, and 3 decrease-key calls. Distances must match the hand answer and independent reference.

Write a small test-only Bellman-Ford implementation that relaxes each undirected edge in both directions for at most n-1 passes. Use at least 100 deterministic small cases with n=2..30, weights 0..20, varied connectivity/density/source. Check full distance arrays and valid predecessor paths. See [correctness plan](correctness-plan.md).

### B4. Derive complexity

Initialization is O(n). Lists contain 2m entries. Each vertex is inserted/extracted at most once; decrease-key occurs O(m) times at most. Each heap operation is O(log n), giving O((n+m)log n) for n>=2. The single-vertex case is constant.

Total graph-plus-state storage is O(n+m); auxiliary state excluding input is O(n). With q actual decreases, the more descriptive upper bound is O(n+m+(n+q)log n). Many scanned edges may not improve a distance.

### B5. Analyze its empirical results

Filter list_indexed_heap rows from the same shared measurements.

| Suite | Upper bound | Analysis focus |
| --- | --- | --- |
| S1, m=4n | O(n log n) | Growth difference from matrix/array |
| S2, fixed density | O(n²log n) | Edge scans and actual successful updates |
| S3, fixed n | O((n+m)log n) | More neighbors and changing heap work |

Record list scans, inserts, extracts, decreases, and successful relaxations. These different-cost operations must not be added as interchangeable units when comparing algorithms. Dense observed time need not attain the worst-case upper bound.

### B6. Completion criteria

- [ ] Heap ordering and position invariants pass independent tests.
- [ ] Every successful relaxation updates the corresponding key.
- [ ] Both algorithms pass hand, boundary, and independent randomized checks.
- [ ] Analysis describes the actual heap and its empirical behavior.

## 5. Running the experiments

### E1. Build the generator and benchmark entry point

Shuffle vertices, connect consecutive vertices into a spanning path, then add distinct pairs until exact m is reached. Assign weights and build both representations. This guarantees connectivity but is not uniform sampling of all connected graphs. Record the generator version.

main.cpp should support check, timing, and count modes. A measurement invocation handles one graph and both algorithms, preserves seed/parameters, validates full distances outside timing, warms up, and runs paired measurements with recorded order.

```text
Outside timing: generation, conversion, validation, full distance comparison
Inside timing: algorithm state initialization/allocation and Dijkstra call
Outside timing: consume/check results, print/write records
```

Use steady_clock and fractional milliseconds. Each call has fresh state and read-only input. Stop the clock before output and subsequent result destruction. Consume returned results to avoid optimizing away unused work. Both algorithms share the same optimization settings and measurement environment.

Timing calls pass stats=nullptr; separate count calls use fresh zero-initialized stats. Optional-counter branches remain part of the chosen implementation and should be documented.

### E2. Run the pilot first

Use [pilot.csv](../experiments/configs/pilot.csv): four configurations, seed 2001, one warmup and three timing calls per algorithm. Confirm correctness, output fields, scan counts, timing resolution, and resource limits, including the largest matrix and dense input.

If resolution is inadequate, increase size/repetitions or fix precision. If resources are insufficient, record an adjusted actual configuration table. Failed runs are not zero-millisecond measurements.

### E3. Run three formal suites

| Suite | n | m or density | Configurations |
| --- | --- | --- | ---: |
| S1 sparse | 100,200,400,800,1600,3200 | m=4n | 6 |
| S2 dense | 100,200,400,800,1600 | m=floor(0.5*n(n-1)/2) | 5 |
| S3 density | Fixed 1000 | p=0.005,0.01,0.02,0.05,0.10,0.25,0.50,0.90 | 8 |

Use [main.csv](../experiments/configs/main.csv) for exact edge counts. Each configuration uses seeds 2001..2005. Each graph/algorithm has two warmups and seven formal calls. If all succeed: 19 configurations, 95 graphs, 1330 timing samples, and 190 separate count records.

Both versions participate in every suite; do not collect unrelated input batches separately for parts (a) and (b). Graphs across density settings need not be nested, but every within-graph comparison is paired.

The [fixed-m suite](../experiments/configs/optional-fixed-m.csv) is optional after the three main suites.

### E4. Implement the Python pipeline

| Script | Processing | Output |
| --- | --- | --- |
| run_experiments.py | Read config, iterate seeds, call C++, check return/status, retain original rows | timings.csv, counts.csv, environment.json |
| summarize_results.py | Validate completeness, aggregate within/across graphs, pair algorithms | per_graph.csv, summary.csv, paired_speedup.csv |
| plot_results.py | Read summaries, label charts and uncertainty | Four main figures, optional diagnostic charts |

Raw data goes to results/raw/<run_id>/; validated summaries/metadata to results/<run_id>/; figures to figures/<run_id>/. Preserve previous runs and keep build/environment settings consistent within a comparison. A mismatch stops affected measurements until fixed.

### E5. Planned command sequence

**The Makefile exists: make builds the scaffold; make test fails while tasks are pending. The batch commands below remain proposed processing interfaces: scripts provide --help but exit PENDING for actual work.** Run from the project2-dijkstra directory.

```bash
make
make test

python3 experiments/scripts/run_experiments.py \
  --config experiments/configs/pilot.csv \
  --binary build/dijkstra_benchmark \
  --output-dir results/raw/pilot-v1

python3 experiments/scripts/run_experiments.py \
  --config experiments/configs/main.csv \
  --binary build/dijkstra_benchmark \
  --output-dir results/raw/main-v1

python3 experiments/scripts/summarize_results.py \
  --run-dir results/raw/main-v1 \
  --output-dir results/main-v1

python3 experiments/scripts/plot_results.py \
  --input-dir results/main-v1 \
  --output-dir figures/main-v1
```

When implemented, document real dependencies, arguments, and build commands in experiments/README.md.

## 6. Data analysis

### D1. Validate before plotting

Check required fields, milliseconds, run/build/environment identifiers, valid sizes/density, successful full-distance validation, both algorithms for every graph, seven samples each, no duplicate sample IDs, and no warmups mixed into measurements.

Only successful validated rows enter aggregation. Record missing/failed cases instead of silently concealing them. Times must be finite and positive; fix zero-resolution problems and rerun rather than inventing values. A graph ID includes parameters, seed, and generator version, not seed alone.

### D2. Aggregate at two levels

First group by (run_id,suite,graph_id,algorithm) and take the median of seven calls. Then group by (run_id,suite,n,m,algorithm) and take the median and Q1/Q3 across five graph medians. Record the quantile convention.

Complete formal output has 190 per-graph rows and 38 configuration/algorithm summary rows. Error bars represent Q1-Q3 of five graph medians, not 35 independent graphs and not automatically confidence intervals.

### D3. Compute paired speed ratios

For each graph:

R = matrix time median / heap time median.

R>1 favors heap; R<1 favors matrix; values near 1 should be interpreted alongside variability. Save 95 graph ratios and summarize across the five seeds for each configuration. Do not substitute a ratio of unrelated or independently aggregated samples for this paired statistic.

### D4. Produce four main figures

| Figure | X axis | Y axis | Question |
| --- | --- | --- | --- |
| Sparse time | n | Time in ms, both algorithms | Does the growth gap widen? |
| Dense time | n | Time in ms, both algorithms | What happens with many edges? |
| Density time | Actual density or m | Time in ms, both algorithms | How does edge count affect each version? |
| Density ratio | Actual density | Paired R, reference line 1 | Does the faster version change? |

Label graph family, units, weights, source, sample counts, aggregation, and error-bar meaning. Trace every figure to CSV/run ID. Theory curves, if included, must be clearly distinguished from observations.

Optional counters explain mechanisms: matrix scans versus n², list scans versus 2m, decreases versus m. For connected graphs under this implementation, inserts=extracts=n and decreases=successful_relaxations-(n-1), providing an additional consistency check.

### D5. Write one explanation per chart

Describe the observation; connect it to algorithm work and theoretical bounds; investigate unusual points using inputs, counters, measurement boundaries, builds, and completeness; state scope and limitations.

For example, dense heap time resembling quadratic growth can be consistent with a larger worst-case upper bound when actual decrease-key work is limited. Do not force measured curves to match a formula.

## 7. Part (c): comparison and recommendations

Part (c) normally needs analysis of the two implementations rather than a third shortest-path algorithm.

### C1. Compare theory and practical trade-offs

| Condition | Matrix/array | Lists/indexed binary heap |
| --- | --- | --- |
| m=Θ(n) | Θ(n²) | O(n log n) |
| m=Θ(n²) | Θ(n²) | O(n²log n) upper bound |
| Storage including input | Θ(n²) | Θ(n+m) |
| Implementation | Simpler scans | Heap and position maintenance |

Large sparse graphs favor the heap's lower growth bound. Dense conclusions depend on measured constants and actual updates. Storage is theoretical in this plan; estimated bytes are not measured peak memory.

### C2. Answer from evidence

1. Which version is faster across tested sparse sizes, and does the gap grow?
2. Which is faster on tested dense graphs, and what do counters explain?
3. Does fixed-n density produce an observed crossover? If so, report the tested interval.
4. How do small-input overhead, storage, and implementation complexity affect the choice?

Eight density points do not identify a universal exact threshold. If neighboring points clearly reverse the advantage, optionally add intermediate densities with multiple seeds and the same pairing rules. If no crossover is observed, report that fact within the tested range.

Write conclusions as condition + observation + explanation + scope. Fill directions and numbers only after actual measurements. Include generator bias, weight distribution, limited scale/seeds, one-machine scope, and excluded representation-construction costs.

## 8. Team responsibilities and schedule

Member A owns matrix Dijkstra and its tests. Member B owns the indexed heap, list Dijkstra and their tests. Member C (you) starts generation/integration on the next evening and owns the generator, independent reference, output, CLI, measurement, all Python scripts, theory, and report coordination. Shared graph conversion and the build framework are already provided. All members review theory and contribute to (c). Detailed file handoffs are in team-roles.md.

| Day | Main objective | Acceptance criterion |
| --- | --- | --- |
| D1 | Shared contracts, graphs, build entry points | Equivalent small inputs |
| D2 | Matrix, independent heap, generator | Matrix hand tests and heap checks |
| D3 | Heap Dijkstra and independent correctness | Both algorithms validated |
| D4 | CLI, runner, metadata | One graph completes pipeline |
| D5 | Pilot, theory, aggregation | Measurement rules/parameters fixed |
| D6 | Formal suites on one machine/build | Raw data complete |
| D7 | Charts and (a)/(b) explanations | Figures trace to measurements |
| D8 | Shared (c), report and reproduction | Every member explains conclusions |

These are relative working days, not known deadline dates. Allow one or two buffer days if possible. Each member reviews another member's code and figure. Formal timing stays in one environment; independent reproduction can use teammates' machines.

## 9. Immediate next step

A/B can immediately implement their algorithms using examples.hpp and the supplied conversion/build helpers. C starts the random generator, reference and measurement work on the next evening. Formal experiments wait for both algorithms and the independent correctness gate.

Reference documents: [architecture](architecture.md), [correctness](correctness-plan.md), [experiments](experiment-plan.md), [theory](theory.md), [roles](team-roles.md), [report](report-outline.md).
