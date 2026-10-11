# Message to teammates

Hi both,

I have prepared the Project 2 framework and a detailed implementation/experiment plan. I may have limited time during the day tomorrow, Monday 12 October, so I will start my Member C work tomorrow evening. You can start the Member A and Member B implementations before then.

## Suggested allocation

**Member A:** implement the adjacency-matrix + array version in `src/dijkstra_matrix.cpp`, and extend `tests/test_matrix.cpp`. Follow the existing interfaces and counter definitions. Start with the supplied teaching graph, then add the boundary cases in the correctness plan.

**Member B:** implement the indexed binary min-heap in `src/min_heap.cpp`, then the adjacency-list version in `src/dijkstra_heap.cpp`. Extend `tests/test_heap.cpp` and `tests/test_heap_dijkstra.cpp`. Test the heap independently before integrating Dijkstra. Every distance improvement must update the corresponding heap key.

**Member C (me):** implement the random graph generator, independent reference checks, result/benchmark output, timing pipeline, and Python experiment/analysis scripts. I will also draft the theoretical analysis and coordinate the figures/report. Please help review the theory against your implementation; we will discuss part (c) together.

## What is already prepared

Everything is under `project2-dijkstra/`:

- Shared C++ interfaces for graph types, algorithm results, counters, the indexed heap, generation, output, and measurement configuration.
- Working graph conversion: `make_matrix()` and `make_list()` use the same canonical edge set.
- A fixed input in `include/examples.hpp`: `teaching_graph()`, source 0, expected distances `[0,3,1,4,7]`. You do not need to wait for my random generator to start.
- Basic result CSV formatting, a Makefile, fixed-input demo dispatch, and initial acceptance-test entry points.
- Explicit TODOs in the algorithm, generator, benchmark, reference, and Python scaffold files.
- Pilot and formal experiment configuration CSV files, plus a report draft.

The framework builds and the shared graph checks pass. Algorithm tests currently report **PENDING** until the TODOs are implemented. Full `make test` will therefore fail for now; this is expected. There are no experimental results yet.

## Documents to read

Start with these documents, relative to `project2-dijkstra/`:

1. [Team roles](team-roles.md): your files, implementation checklist, and handoff criteria.
2. [Framework guide](framework-guide.md): available helpers, build commands, and pending tasks.
3. [Architecture](architecture.md): shared interfaces, INF rules, tie-breaking, and counters.
4. [Correctness plan](correctness-plan.md): test cases and independent validation.
5. [Execution plan](execution-plan.md): how parts (a), (b), and (c) fit together.

The exact experiment settings are in [experiment-plan.md](experiment-plan.md) and `experiments/configs/`. [report-draft.md](report-draft.md) is the initial writing template.

## How to start

Get the shared scaffold branch/commit, then create your own task branch from that same starting point. Please avoid changing shared headers without coordinating first.

From `project2-dijkstra/`:

```bash
make
make test-graph
```

For Member A:

```bash
make test-matrix
./build/dijkstra_benchmark --demo matrix
```

For Member B:

```bash
make test-heap
make test-heap-dijkstra
./build/dijkstra_benchmark --demo heap
```

These algorithm commands become successful after your implementation is complete. Keep printing, graph generation, and timing outside the algorithm functions; return `DijkstraResult` using the existing interface.

## Suggested prompts for your agent

Member A:

> Read project2-dijkstra/docs/team-roles.md, framework-guide.md, architecture.md, and correctness-plan.md. I am Member A. Guide me through implementing src/dijkstra_matrix.cpp and extending tests/test_matrix.cpp using the existing interfaces. Explain initialization, linear minimum selection, relaxation, safe distance handling, and counters. Validate the teaching graph and boundary cases. Keep changes within my assigned files unless a shared-interface change is necessary, and explain any such change before making it. Do not run formal experiments yet.

Member B:

> Read project2-dijkstra/docs/team-roles.md, framework-guide.md, architecture.md, and correctness-plan.md. I am Member B. Guide me through implementing the indexed heap in src/min_heap.cpp, then src/dijkstra_heap.cpp, and extending tests/test_heap.cpp and tests/test_heap_dijkstra.cpp. Explain position tracking, heap restoration, decrease-key, and how heap priorities stay synchronized with distances. Test the heap independently, then validate shortest paths and counters. Keep changes within my assigned files unless a shared-interface change is necessary, and explain any such change before making it. Do not run formal experiments yet.

Before handoff, please send the code revision, your own test results, and any unresolved issues. Let us confirm correctness before collecting performance data.
