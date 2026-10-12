# Planned correctness programs

Test programs and Makefile entry points exist. The graph conversion checks are available; both algorithm modules have executable validation; generator validation is available; shared-reference integration and end-to-end CLI checks are implemented.

- test_graph.cpp: conversion equivalence, validation, exact generation, connectivity, reproducibility.
- test_matrix.cpp: hand-computed shortest paths and boundary cases.
- test_heap.cpp: ordering, decrease-key, positions, ties, invalid operations.
- test_heap_dijkstra.cpp: Member B shortest-path acceptance cases without dependencies on A/C implementations.
- test_dijkstra.cpp: compare both algorithms with an independent small Bellman-Ford reference.
- reference_bellman_ford.hpp: implemented test-only reference; relax undirected edges in both directions.
- test_cli.py: random commands, schemas, seeded order, output files, CSV quoting and failure cases.

See the [correctness plan](../docs/correctness-plan.md). See the framework guide for PASS/FAIL/PENDING behavior. Full algorithm correctness is not claimed.
