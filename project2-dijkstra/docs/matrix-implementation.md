# Matrix/array Dijkstra: implementation walkthrough

Implementation: `src/dijkstra_matrix.cpp`. Acceptance tests: `tests/test_matrix.cpp`. The function follows the existing interface and does not generate graphs, print, or call clocks.

## 1. Input and output

`MatrixGraph` contains n and an n-by-n weight matrix. Conversion validates the graph before the algorithm: diagonal entries are 0, absent edges are kInfinity, and existing weights are nonnegative. The algorithm checks that source is within 0..n-1 but does not repeat full representation validation during timing.

`DijkstraResult` contains distances and parents, both length n. The source distance is 0; unreachable distance is INF. Source and unreachable parents are kNoVertex.

## 2. Initialization

Create distances filled with INF, parents filled with kNoVertex, and settled flags filled with false. Set only the source distance to 0. All state is fresh for each call.

A tentative distance means the shortest path found so far; it can improve. A settled vertex has its final shortest distance under the nonnegative-weight assumption.

## 3. Extract-min through an unsorted array

Repeat at most n rounds. Start u=kNoVertex, then scan every vertex index. Skip settled vertices and retain the unsettled vertex with smallest distance.

Indices are visited in ascending order and replacement uses a strict less-than comparison, so equal distances select the smaller ID. This matches the heap's (distance,vertex_id) ordering.

No sorted container or heap is used: the distance/settled arrays and linear minimum search provide the required array priority-queue behavior.

## 4. Stop or settle

If no candidate exists, or the best candidate still has INF distance, stop. In a disconnected graph, no remaining vertex can be reached from the source; keep their distances INF and parents empty.

Otherwise mark u settled. Nonnegative weights justify finalizing this minimum tentative distance: an alternative route through another unsettled vertex cannot produce a shorter value after adding nonnegative edges.

## 5. Scan a complete matrix row

Inspect v=0..n-1, including positions without edges. Skip already settled vertices and weights equal to INF. Because u has just been settled, its diagonal entry is skipped automatically.

Zero-weight edges are real edges and are not skipped. This is why absence must use INF rather than 0.

## 6. Safe relaxation

Before computing dist[u]+weight, check whether weight >= INF-dist[u]. Skip such a candidate to avoid overflow and reserve INF for unreachable state. dist[u] is finite because of the preceding stopping check.

If candidate >= dist[v], do nothing. Otherwise set dist[v]=candidate and parent[v]=u. Strict improvement leaves equal-cost predecessor choices unchanged and prevents unnecessary updates.

A parent chain reconstructs a chosen shortest path backward. It cannot acquire a cycle here: a new parent is already settled while the child is not.

## 7. Trace on the teaching graph

Vertex IDs A=0,B=1,C=2,D=3,E=4; source A.

| Newly settled | Distances after relaxation: A,B,C,D,E | Updates |
| --- | --- | --- |
| Initial | 0,INF,INF,INF,INF | Source initialization |
| A | 0,4,1,INF,INF | Discover B/C |
| C | 0,3,1,6,INF | Improve B, discover D |
| B | 0,3,1,4,10 | Improve D, discover E |
| D | 0,3,1,4,7 | Improve E |
| E | 0,3,1,4,7 | None |

Final parent array: NONE,2,0,1,3. Following E's parents yields E-D-B-C-A; reversing gives A-C-B-D-E, weight 7.

## 8. Counters and complexity

Counters are optional: nullptr disables accumulation; otherwise the caller supplies fresh zero-initialized stats.

- min_scan_slots counts every selection-array index, including settled positions.
- matrix_scan_slots counts every row column, including skipped positions.
- relax_attempts counts existing edges to unsettled neighbors that reach candidate evaluation.
- relax_successes counts strict distance improvements.
- Heap/list counters are not changed.

For connected n-vertex inputs, both scan counters equal n². In the teaching graph: 25 selection slots, 25 row slots, 7 relaxation attempts, 7 improvements.

If only r<n vertices are reachable, row slots=n*r. Minimum selection also performs one final unsuccessful scan, so slots=n*(r+1). At most n rounds are attempted.

Initialization is O(n); up to n minimum scans and n row scans each cost O(n). Overall time is O(n²), with Θ(n²) full connected traversal. Auxiliary space is O(n); input matrix storage is Θ(n²).

## 9. Verification

Run from project2-dijkstra:

```bash
make all test-matrix test-heap test-heap-dijkstra test-graph
./build/dijkstra_benchmark --demo matrix
```

Matrix tests check hand/boundary cases, safe large distances, invalid sources, paths, counters, counter-disabled consistency, and agreement with the merged heap implementation.

An independent test-only Floyd-Warshall implementation builds its own distance table from canonical edges. Tests exhaust all 729 four-vertex absent/zero/positive edge assignments and all four sources, then check all sources in 250 deterministic random graphs with n=2..30 and varied density.

This oracle is confined to matrix tests, not a new production shortest-path implementation. The shared Bellman-Ford reference, generator and C++ benchmark modes are now implemented, and full make test passes. Formal main experiments and Python processing remain separate tasks.
