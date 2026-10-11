# Team allocation and handoff checklist

Member A and Member B are the two algorithm implementers. **Member C is the member requesting this plan**, available to start the generator/integration work on the next evening (12 October 2026, Singapore time). This is a proposed work start, not a confirmed deadline or scheduled reminder.

Assignment parts (a)/(b)/(c) are different from member names. Member C leads theory and empirical analysis for both (a) and (b); all members review and contribute to comparison (c).

## Available framework

Graph conversion, a fixed teaching graph, result CSV formatting, a Makefile, and test entry points are provided. Algorithm bodies, core heap operations, generator, independent reference, benchmark modes, and Python processing remain explicit TODOs. Pending functions throw NotImplemented rather than returning invented data.

A and B can begin now without the random generator: include examples.hpp, call teaching_graph(), and convert it with make_matrix/make_list. Main source is 0; expected distances are [0,3,1,4,7]. Add small manual edge sets for boundary cases.

## Member A: matrix/array algorithm

### Owned files

- src/dijkstra_matrix.cpp
- tests/test_matrix.cpp

### Work sequence

1. Read graph.hpp, types.hpp, dijkstra.hpp, and the matrix contract in architecture.md.
2. Initialize distances/parents/settled and validate source.
3. Write the linear minimum-selection loop with vertex-ID tie-breaking and INF termination.
4. Scan the full selected matrix row and safely relax existing edges to unsettled vertices.
5. Implement optional counters exactly as documented; nullptr disables accumulation.
6. Return real distance/parent arrays; never print or time inside the algorithm.
7. Complete teaching, single-vertex, zero-weight, unreachable, equal-path, other-source, invalid-source, and large-weight tests. Validate reconstructed paths.
8. Review Member B's Dijkstra relaxation and heap-key synchronization.

### Local commands

```bash
make
make test-matrix
./build/dijkstra_benchmark --demo matrix
```

The test and demo report PENDING until the algorithm is implemented. They are not expected to pass initially.

### Handoff to Member C

Provide the implementation, passing own-module tests, source/build revision, confirmation of counter semantics, and a brief explanation of initialization/minimum selection/relaxation. Teaching counters: min_scan_slots=25 and matrix_scan_slots=25. Return results through DijkstraResult, not a custom printed format.

## Member B: indexed heap and list algorithm

### Owned files

- src/min_heap.cpp
- src/dijkstra_heap.cpp
- tests/test_heap.cpp
- tests/test_heap_dijkstra.cpp
- Heap-specific additions to tests/test_dijkstra.cpp, coordinated with C

### Work sequence

1. Inspect min_heap.hpp; keep one entry per vertex and positions synchronized.
2. Implement swap_entries, sift_up, sift_down, push_or_decrease, and extract_min.
3. Test the heap independently before integrating graph traversal.
4. Initialize Dijkstra state and insert the source only.
5. Extract minimum, settle it, inspect actual list entries, and safely relax.
6. Update heap priority on every strict distance improvement; never reinsert settled vertices.
7. Implement counters and return DijkstraResult without printing/timing.
8. Extend heap cases for repeated decreases, ties, no-op updates, empty/invalid operations, and random actions against a linear-scan oracle.
9. Check algorithm hand/boundary cases; review A's INF handling and matrix scan rules.

### Local commands

```bash
make
make test-heap
make test-heap-dijkstra
./build/dijkstra_benchmark --demo heap
```

Full integration tests also require A's algorithm and C's independent reference. A pending integration dependency does not by itself mean B's local heap is incorrect; own-module tests must still pass before handoff.

### Handoff to Member C

Provide passing heap tests, working demo, fixed-input distances, counter values, and an explanation of position updates and decrease-key. On the teaching graph: inserts=5, extracts=5, decreases=3, list scans=14. Confirm this is the indexed-heap design, not lazy deletion.

## Member C: generator, output, measurement, theory and report

### Owned files

- src/generation.cpp and tests/test_generation.cpp
- src/main.cpp, src/benchmark.cpp, include/benchmark.hpp
- src/output.cpp and include/output.hpp (basic formatting is already provided)
- tests/reference_bellman_ford.hpp and integration/random checks in tests/test_dijkstra.cpp
- experiments/scripts/run_experiments.py
- experiments/scripts/summarize_results.py
- experiments/scripts/plot_results.py
- Theory, analysis, experiment-method, and report documents

### First evening: input and correctness integration

1. Confirm both teammate implementations use the existing headers unchanged.
2. Run their own-module tests and fixed demos; record pending tasks or failures.
3. Implement the connected graph generator with exact n/m/seed/weights; verify conversion, seed reproduction, and independent connectivity.
4. Implement the small Bellman-Ford test oracle and compare complete distances on deterministic small random graphs.
5. Agree how paths, INF, source parents, counters, and failures are output.

If A/B are still implementing, generator/reference/output work can proceed using the fixed shared types. Do not run formal performance experiments until full correctness checks pass.

### Next stage: measurement and data

1. Extend main.cpp from fixed demos to BenchmarkConfig argument parsing.
2. Implement check/timing/count modes in benchmark.cpp, outside-algorithm clocks and separate counter runs.
3. Implement runner using existing configuration CSV; retain raw rows and environment metadata.
4. Run pilot, fix timing/data issues, then run formal suites in one environment.
5. Validate completeness, aggregate within graphs then across seeds, compute same-graph ratios, and generate four main charts.

### Theory and reporting

Lead the derivations for both implementations, with A/B checking that explanations match their code. Derive matrix O(n²), heap O((n+m)log n), input/auxiliary space, and actual-operation explanations. Draft methods and limitations, analyze charts, and coordinate comparison (c) and final materials.

This workload covers programming as well as organizing results; it is not guaranteed to fit in one evening. If time becomes tight, A/B can take a runner/reference task after finishing their own implementations, with ownership explicitly reassigned.

## Shared review and final gate

| Work | Lead | Reviewer |
| --- | --- | --- |
| Matrix implementation/tests | A | B; C independent reference |
| Heap/list implementation/tests | B | A; C independent reference |
| Generator/reference | C | A checks matrix inputs; B checks lists and reference assumptions |
| Output/measurement/automation | C | A/B inspect timing boundaries and one raw sample |
| Theory (a)/(b) | C | A/B explain and verify their respective operation counts |
| Charts and comparison (c) | C coordinates | Both teammates verify one chart and conclusion |

Every member must understand both algorithms and the comparison. Formal measurements use one machine/build; do not concatenate timings from different members' computers.

The framework has been written in the current working directory. Agree the integration branch before committing; suggested short task branches are codex/project2-matrix, codex/project2-heap, and codex/project2-experiments. No push, merge, or teammate messaging is performed by this plan.
