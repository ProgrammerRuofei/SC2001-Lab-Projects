# Theoretical analysis

Let n=|V| and m=|E|. Main graphs are simple and undirected, so m<=n(n-1)/2. Adjacency lists contain 2m entries.

Analyze algorithm calls, including auxiliary initialization but excluding graph generation, representation conversion, validation, and output. Disconnected inputs can stop early; bounds below cover complete traversal or the worst case.

## Part (a): matrix and unsorted array

| Work | Frequency | Cost per operation |
| --- | --- | --- |
| Initialize state | Once | O(n) |
| Linear minimum selection | At most n | O(n) |
| Full matrix-row scan | At most n | O(n) |
| Successful distance updates | O(m) | O(1) |

Total O(n²+m)=O(n²) for simple graphs. Under the full-scan contract on connected graphs, each selection and row-scan counter is exactly n², giving Θ(n²) work.

Input storage is Θ(n²); auxiliary state is Θ(n). Sparse graphs still require inspecting absent-edge positions.

## Part (b): lists and indexed binary heap

Initialization is O(n); list inspection is O(m). Each vertex is inserted/extracted at most once, and there are O(m) decrease-key operations. Each heap operation takes O(log n), since the heap has at most n entries and position lookup is O(1).

For n>=2, total time is O((n+m)log n). The n=1 case is constant. Let q be the actual decrease-key count: a more descriptive upper bound for a run is O(n+m+(n+q)log n). q can be much smaller than m.

Input plus auxiliary storage is Θ(n+m); auxiliary storage alone is O(n).

## Comparison

| Graph family | Matrix/array | Lists/binary heap |
| --- | --- | --- |
| Sparse, m=Θ(n) | Θ(n²) | O(n log n) |
| Dense, m=Θ(n²) | Θ(n²) | O(n²log n) upper bound |
| Fixed n, increasing m | Main scan counts unchanged | More list inspection; heap updates depend on improvements |

Dense measurements need not reach the heap's worst-case bound. Constants, allocation, cache behavior, and q affect practical time. Finite measurements support trend analysis, not a proof of asymptotic complexity.

Comparing n² with (n+m)log n suggests a rough scale near m=n²/log n for large n, but this is not a guaranteed crossover or a measured threshold.

Matrix construction itself requires Θ(n²) initialization; list construction is O(n+m). Neither is included in the main algorithm timing; do not claim that timing covers the full edge-list-to-answer pipeline.

## If the heap design changes

Lazy deletion inserts new entries after improvements and discards obsolete entries when popped. Queue storage can become O(m); analyze its actual entry count, for example O((n+m)log(n+m)), often expressed as O((n+m)log n) on simple graphs. Update the counters, tests, and report if adopting this design.
