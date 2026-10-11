# Framework guide: available infrastructure and pending work

## Build and begin

Run from project2-dijkstra:

```bash
make
make test-graph
./build/dijkstra_benchmark --help
```

The framework builds a C++17 binary with warnings and -O2. Shared graph conversion is implemented and tested. Build products are ignored by Git.

```text
include/
  types.hpp           Vertex/Weight/Distance and INF conventions
  graph.hpp           Shared canonical edges, matrix/list types and conversions
  examples.hpp        Available fixed graph and expected distances
  dijkstra.hpp        Shared algorithm result and optional counters
  min_heap.hpp        Member B's heap interface
  generation.hpp      Member C's random input interface
  output.hpp          Available result formatter; C owns extensions
  benchmark.hpp       Member C's future check/timing/count entry point
  scaffold.hpp        Explicit NotImplemented exception
src/
  graph.cpp           IMPLEMENTED: validated symmetric conversion
  output.cpp          IMPLEMENTED: vertex,distance,parent CSV formatting
  main.cpp            AVAILABLE: help and fixed-input demo dispatch
  dijkstra_matrix.cpp TODO: Member A
  min_heap.cpp        TODO: Member B core heap operations
  dijkstra_heap.cpp    TODO: Member B
  generation.cpp      TODO: Member C
  benchmark.cpp       TODO: Member C
tests/
  test_graph.cpp      Available graph conversion/validation checks
  test_matrix.cpp     Initial A acceptance cases; extend before handoff
  test_heap.cpp       Initial B heap acceptance cases; extend before handoff
  test_heap_dijkstra.cpp  Independent B algorithm acceptance cases
  test_generation.cpp Initial C acceptance cases; extend before handoff
  test_dijkstra.cpp   Integration and independent-reference entry point
  reference_bellman_ford.hpp  TODO: Member C
experiments/scripts/
  run_experiments.py        TODO: Member C; --help is available
  summarize_results.py     TODO: Member C; --help is available
  plot_results.py          TODO: Member C; --help is available
```

## Individual development entry points

```bash
make test-matrix
make test-heap
make test-heap-dijkstra
make test-generation
make test-dijkstra
./build/dijkstra_benchmark --demo matrix
./build/dijkstra_benchmark --demo heap
```

Each test executable reports PASS (exit 0), FAIL (exit 1), or PENDING (exit 2). Until implementations are complete, relevant tests/demos report PENDING. make test compiles and runs all test programs and fails if any is pending or failing. A compiling scaffold is not evidence of correct Dijkstra.

A/B use teaching_graph(), make_matrix()/make_list(), source 0 and expected [0,3,1,4,7]. They can construct additional EdgeListGraph fixtures without generation.cpp. The fixed demos print actual algorithm results through write_result_csv; they never print the expected answer as a computed result.

## Planned pipeline entry points

The batch CLI arguments in execution-plan.md are still a target. The current C++ binary accepts only --help and --demo matrix/heap; random-input and measurement flags are not parsed yet.

Python scripts accept their planned path arguments and provide --help, then explicitly exit PENDING for actual processing. They create no fabricated data or charts.

Member C extends these scaffold entry points and synchronizes the supported CLI with documentation. Use run IDs and the existing parameter CSV, validate full distances before timing, and keep counting separate.

## Header and output handoff rules

Both teammates use existing DijkstraResult/OperationStats and return arrays of length n. Do not print/timestamp inside algorithm bodies. Coordinate before changing a header. Equal priorities use vertex-ID tie-breaking; absent matrix edges use INF, not 0.

Basic result CSV uses vertex,distance,parent, with INF for unreachable distance and NONE for source/unreachable parent. Member C adds timing/count fields from experiment-plan.md and path/report views if useful.

See [team roles](team-roles.md) for file ownership and [execution plan](execution-plan.md) for end-to-end steps.
