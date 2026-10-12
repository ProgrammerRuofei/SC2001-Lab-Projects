# Connected random graph generator

Implementation: `src/generation.cpp`. Contract/version: `include/generation.hpp`. Tests: `tests/test_generation.cpp`.

## Input and output

```cpp
GraphSpec spec{20, 80, 2001, 1, 1000};
EdgeListGraph edges = generate_connected_graph(spec);
MatrixGraph matrix = make_matrix(edges);
ListGraph list = make_list(edges);
```

The fields are vertex_count, edge_count, graph_seed, weight_min, weight_max. One call produces one canonical edge set shared by both representations. Source selection belongs to Dijkstra, not the generator.

The output is a simple connected undirected graph with exact n/m, sorted pairs u<v, no loops or duplicates, and inclusive integer weights in the requested range. Main experiments use positive weights; tests can request zero weights.

## Parameter validation

Reject n=0, negative/inverted weight ranges, weights at or above INF, m outside [n-1,n(n-1)/2], an unrepresentable maximum edge count, or a path-weight upper bound that reaches INF.

For n=1, only m=0 is allowed. The generator does not adjust impossible requests silently. Compute n(n-1)/2 by dividing one factor first and checking multiplication; validate path bounds using division before allocating graph storage.

## Connectivity before density

Create vertex IDs 0..n-1 and shuffle them with a local mt19937_64 seeded by graph_seed. Connect consecutive shuffled vertices to form a spanning path of n-1 edges. This makes every vertex reachable without relying on a connectivity repair loop.

Canonicalize endpoints to u<v and track chosen pairs. The same path edge is never inserted twice.

## Additional edges

Let extra=m-(n-1), remaining=n(n-1)/2-(n-1).

- Sparse branch, extra<=remaining/4: draw two vertex IDs, discard loops/repeated pairs, and continue until exact m. No full candidate list is allocated.
- Dense branch, extra>remaining/4: enumerate pairs not already in the path, shuffle them, and take exactly extra entries. Sampling without replacement avoids slow rejection near complete graphs.
- No extra edges: return the spanning path after assigning weights.

Both branches preserve the same graph contract. The graph distribution is not uniform across all connected graphs: the forced random path biases topology. Report this limitation. Different density configurations are not guaranteed nested.

## Weights and reproducibility

Sort selected pairs before assigning independently sampled integer weights from [weight_min,weight_max]. The RNG is local to each call; unrelated calls do not alter its state.

`kGraphGeneratorVersion` is `connected-path-v1`. Same spec/seed/version/toolchain reproduces topology and weights. Standard-library shuffle/distribution implementations can differ across toolchains; do not promise portable bit-for-bit reproduction without recording the environment.

## Costs

Sparse generation stores O(n+m) state and uses expected near-linear pair sampling at the chosen threshold, plus O(m log m) sorting. Dense generation enumerates O(n²) candidates and temporarily uses O(n²) memory, plus edge sorting. Hash membership is expected O(1).

These costs belong to input generation, not the timed Dijkstra calls. Never include generation or representation conversion in the main algorithm time curves.

## Verification

```bash
make all test-generation
```

Tests verify exact counts, canonical order, unique edges, weight range, raw-edge BFS connectivity, same-seed reproduction, matrix/list equivalence, and both Dijkstra results. They cover every feasible m for n=2..12 with three seeds, including zero and maximum uint64 seeds, plus single-vertex, fixed-weight, large-weight, sparse/dense/complete cases. There are 701 valid spec checks, each regenerated for reproducibility, plus invalid requests.

A separate correctness smoke check covers all four pilot configurations, including n=1600/m=639600 and n=3200/m=12800. It validates counts, uniqueness, weights and connectivity without reporting performance measurements.

The generator is callable through its C++ interface. The CLI now supports random-input parsing and check/timing/count modes; see running-guide.md. Python batch processing remains the next stage.
