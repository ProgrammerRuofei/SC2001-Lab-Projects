# Report outline

This is a proposed structure. Confirm actual submission format and length with course notices. Fill observations and numbers only after measurements.

1. **Problem and design:** single-source shortest paths, nonnegative weights, n/m definitions, graph family, common input/results, small trace.
2. **Part (a):** matrix and unsorted array, pseudocode, cost derivation, space, measured growth and fixed-n edge-count behavior.
3. **Part (b):** lists, indexed heap, position/decrease-key invariants, operation bounds, space, empirical behavior and actual improvement counts.
4. **Methods:** generator and actual parameters, correctness checks, same-graph pairing, machine/build, timing boundary, repetitions, aggregation, error bars.
5. **Part (c):** sparse/dense comparisons, paired ratios, observed crossover range if any, small-input overhead, theoretical storage and implementation trade-offs.
6. **Limitations and reproduction:** generator bias, weights, limited scale/seeds, one environment, conversion excluded; real build/test/run commands, run IDs, source data and contribution statement.

For every chart: describe an observation, connect it to work performed, investigate deviations, and state scope. Do not claim that heaps always win or that dense heaps must be slower by exactly log n.

Each member should explain why greedy settlement requires nonnegative weights, why matrix scans are quadratic, how positions support decrease-key, why undirected lists have 2m entries, and why repeated calls are different from independent graphs.
