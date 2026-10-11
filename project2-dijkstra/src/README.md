# C++ framework and implementation ownership

Shared conversion/formatting and demo dispatch are available. Algorithm, core heap, generator and benchmark files exist as explicit TODOs.

| File | Responsibility | Lead |
| --- | --- | --- |
| graph.cpp | Available shared validation/conversion | C coordinates changes; A/B review |
| generation.cpp | Generate exact connected n/m/seed graphs | C |
| dijkstra_matrix.cpp | Array minimum selection and matrix relaxation | A |
| min_heap.cpp | Indexed binary heap and decrease-key | B |
| dijkstra_heap.cpp | List relaxation using the heap | B |
| main.cpp / benchmark.cpp / output.cpp | CLI, results, timing, counters, CSV | C, reviewed by A/B |

Use existing headers. Algorithms return results without printing, generation, timing, or output. See [architecture](../docs/architecture.md) and [execution plan](../docs/execution-plan.md).
