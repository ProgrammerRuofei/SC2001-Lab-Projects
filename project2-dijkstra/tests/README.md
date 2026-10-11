# Planned correctness programs

Test programs and Makefile entry points exist. The graph conversion checks are available; algorithm/generator/reference tests remain pending until their TODO dependencies are implemented.

- test_graph.cpp: conversion equivalence, validation, exact generation, connectivity, reproducibility.
- test_matrix.cpp: hand-computed shortest paths and boundary cases.
- test_heap.cpp: ordering, decrease-key, positions, ties, invalid operations.
- test_heap_dijkstra.cpp: Member B shortest-path acceptance cases without dependencies on A/C implementations.
- test_dijkstra.cpp: compare both algorithms with an independent small Bellman-Ford reference.
- reference_bellman_ford.hpp: test-only reference; relax undirected edges in both directions.

See the [correctness plan](../docs/correctness-plan.md). See the framework guide for PASS/FAIL/PENDING behavior. Full algorithm correctness is not claimed.
