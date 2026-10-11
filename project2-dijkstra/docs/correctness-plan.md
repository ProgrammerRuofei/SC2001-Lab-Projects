# Correctness plan

This is a test specification, not a record of passed tests.

## Hand-computed cases

| Case | Input | Expected distances |
| --- | --- | --- |
| Single vertex | n=1, source=0 | [0] |
| One edge | 0-1:5, source=0 | [0,5] |
| Teaching graph | Five vertices from learning-guide | [0,3,1,4,7] |
| Indirect route is shorter | 0-1:10, 0-2:1, 2-1:1 | [0,2,1] |
| Unreachable vertex | 0-1:2, isolated 2 | [0,2,INF] |
| Isolated source | Only 1-2:4, source=0 | [0,INF,INF] |
| Zero weights | 0-1:0, 1-2:0, 0-2:5 | [0,0,0] |
| Equal paths | 0-1:1, 0-2:1, 1-3:1, 2-3:1 | [0,1,1,2] |
| Other source | 0-1:5, source=1 | [5,0] |
| Large weights | Values above 32-bit range but below safe limits | No truncation or overflow |

Reject invalid vertex IDs, sources, self-loops, duplicate edges, negative weights, impossible edge counts, invalid weight ranges, and unsafe distance bounds.

## Representation and generator tests

Check canonical u<v edges, exact m, no duplicates, symmetric matrices, zero diagonal, INF absence, matching weights, and exactly 2m list entries. Test same-version/same-seed reproducibility. Independently check generator connectivity using BFS/DFS.

For connected generation, n>1 requires n-1<=m<=n(n-1)/2; n=1 requires m=0.

## Heap tests

Check ordered extraction, vertex-ID tie-breaking, decrease-key at different positions, repeated updates without duplicate entries, no-op equal/larger keys, single-element extraction, empty/invalid operations, and consistency of position after every swap.

Compare randomized heap actions against a simple linear-scan reference container; do not use the tested heap as its own oracle.

## Independent shortest-path checks

Write a small Bellman-Ford reference in tests. Relax each undirected edge in both directions for at most n-1 passes, skipping INF. It must not reuse Dijkstra's control flow or heap.

Use at least 100 deterministic cases with n=2..30, weights 0..20, varied density/connectivity, and varied source. Compare full distance arrays against both implementations.

Validate parents by reconstructing existing acyclic paths whose weight equals dist. Equal-length solutions may have different parents.

## Teaching-graph counters

For n=5,m=7 under the architecture's full scans:

- Matrix minimum scans=25; matrix row scans=25.
- List entries scanned=14.
- Heap inserts=5; extracts=5; decreases=3.
- Both versions have 7 strict distance improvements.

Disconnected inputs can stop early, so full-graph scan expectations need not hold.

## Gate before formal experiments

- [ ] Hand cases, graph validation, heap tests, and independent random checks pass.
- [ ] Every call uses fresh algorithm state.
- [ ] Timing builds use consistent optimization; debugging builds are separate.
- [ ] Each benchmark graph is checked outside timing using complete distance arrays.
- [ ] A mismatch stops measurement until investigated and fixed.
