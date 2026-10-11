# Architecture and interface contracts

## Data flow

```text
(n, m, graph_seed, weight range)
              |
     generate_connected_graph
              |
        EdgeListGraph
         /          \
   make_matrix     make_list
        |              |
   MatrixGraph      ListGraph
        |              |
 dijkstra_matrix   dijkstra_heap
         \           /
      Compare full distance arrays
              |
       Separate timing/count runs
              |
           Raw CSV
              |
      Python summaries and plots
```

Generate each graph once and build both representations from it. Generation, conversion, validation, and file output are outside algorithm timing.

## Modules

| Header | Planned source | Responsibility |
| --- | --- | --- |
| types.hpp | None | Vertex IDs, 64-bit weights/distances, INF |
| graph.hpp | graph.cpp | Canonical edges, representation conversion, input validation |
| generation.hpp | generation.cpp | Reproducible connected graphs with exact n and m |
| dijkstra.hpp | dijkstra_matrix.cpp | Matrix scans and array minimum selection |
| min_heap.hpp | min_heap.cpp | Indexed binary min-heap |
| dijkstra.hpp | dijkstra_heap.cpp | Adjacency-list relaxation and heap updates |
| None | main.cpp | CLI, validation, timing, diagnostic counts, CSV |

Algorithm functions return results; they do not print, generate input, write files, or call clocks. Python does not implement the algorithms being benchmarked.

## Input contracts

- n>=1; vertices are numbered 0..n-1; source is a valid vertex ID.
- The current graph contract is simple and undirected. Canonical edges have u<v and occur once.
- Conversion writes both matrix directions and both adjacency-list entries.
- Matrix diagonal is 0; absent edges use kInfinity, never 0.
- Weights are nonnegative integers below kInfinity; main experiments use [1,1000].
- Distance and Weight are signed 64-bit integers. kInfinity=INT64_MAX/4.
- Validate the safe simple-path bound (n-1)*maximum_weight < kInfinity without overflowing the validation calculation.
- Skip INF before addition and check that candidate additions are safe.
- Reject invalid IDs, duplicate edges, self-loops, negative weights, or invalid generation parameters; proposed exception: std::invalid_argument.
- Algorithm inputs must already satisfy the graph contract. Full representation validation is outside timing.

Disconnected graphs are valid test inputs; the main generator guarantees connectivity. Supporting directed graphs would require updating this contract and its tests.

## Algorithm results

```cpp
DijkstraResult dijkstra_matrix(const MatrixGraph&, Vertex source,
                               OperationStats* stats = nullptr);
DijkstraResult dijkstra_heap(const ListGraph&, Vertex source,
                             OperationStats* stats = nullptr);
```

Both arrays have n entries. Unreachable distances are kInfinity. The source and unreachable vertices have parent kNoVertex. Update distances and parents only for strictly shorter paths.

Compare full distance arrays. Different valid equal-length paths need not have identical parents; separately validate reconstructed paths. Break minimum-selection ties by (distance, vertex_id) and sort adjacency lists by neighbor ID.

Every invocation allocates fresh algorithm state. Input graphs are read-only.

## Matrix implementation

Use distance, settled, and parent arrays. In each of at most n rounds, scan all n indices to find the smallest unsettled finite distance. Stop if no finite candidate remains. Settle that vertex and scan all n matrix columns, skipping settled vertices and absent edges.

This implements an unsorted array priority queue through linear extract-min behavior.

## Heap implementation

Use the same state arrays plus IndexedMinHeap(n). Start with the source only. First discovery inserts a vertex; later improvements decrease its existing key. Settled vertices are never reinserted. Stop when the heap is empty.

The heap stores at most one entry per vertex and at most n entries overall. This is not a lazy-deletion implementation.

## Heap invariants

- heap_ is a complete binary tree stored in an array, ordered by (key, vertex).
- position_[v] gives v's heap index, or kNoVertex when absent.
- Every swap updates both corresponding positions.
- Insertion and decrease-key sift upward; extract-min replaces the root with the last entry and sifts downward.
- push_or_decrease ignores equal or larger keys for existing entries.
- Reject invalid IDs/keys; extracting from an empty heap should throw std::out_of_range.

## Diagnostic counters

| Counter | Definition |
| --- | --- |
| min_scan_slots | Every index inspected in array minimum selection, including settled indices |
| matrix_scan_slots | Every inspected matrix column, including absent edges and skipped vertices |
| adjacency_entries_scanned | Every visited list entry, including subsequently skipped neighbors |
| relax_attempts | Candidate-distance comparisons for existing edges to unsettled neighbors |
| relax_successes | Strict distance improvements |
| heap_inserts | First insertion of a vertex, including the source |
| heap_extracts | Successful extract-min calls |
| heap_decreases | Strict reductions of keys already in the heap |

For connected main graphs under complete scans: minimum scans=n², matrix scans=n², list scans=2m, heap inserts=heap extracts=n. Different counters represent different-cost operations and must not be summed as interchangeable work units.

Timing runs pass nullptr. Diagnostic runs use a fresh zero-initialized OperationStats and do not contribute formal timing samples.

## Build and CLI plan

Add a Makefile with C++17, common warnings, and optimized measurement builds such as -O2. Use debug/sanitizer builds for debugging, not performance comparisons.

Proposed CLI parameters: --n, --m, --seed, --source, --weight-min, --weight-max, --warmup, --repeats, --order-seed, --mode. Modes are check/timing/count. A failed run is an error, not a zero-millisecond sample.

Graph conversion and result formatting are implemented; algorithm/generator/measurement logic remains pending. Current help/demo and build commands are described in the [framework guide](framework-guide.md); full measurement CLI arguments remain proposed.
