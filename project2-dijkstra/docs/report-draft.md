# Project 2 report draft

Owner: Member C, reviewed by Members A and B. This is a writing template, not a completed report. All observations, measurements, and performance conclusions remain pending.

## 1. Problem and implementation choices

Describe single-source shortest paths and the nonnegative-weight requirement. Define n and m. Explain the two required representation/priority-queue combinations and the chosen indexed binary heap.

Proposed main input family: simple connected undirected graphs, source 0, integer weights in [1,1000]. Distinguish proposed settings from actual settings after running.

## 2. Part (a): matrix and array

- Implementation/control-flow explanation: TODO after Member A handoff.
- Correctness evidence and source/build revision: TODO.
- Theory: derive initialization, linear selection, row scans, O(n²), input and auxiliary space. Verify against the final implementation.
- Empirical evidence: reference S1/S2/S3 CSV and charts after measurement.
- Observation -> operation-count explanation -> limitations: TODO; no assumed winner.

## 3. Part (b): lists and indexed heap

- Implementation and position/decrease-key invariants: TODO after Member B handoff.
- Heap and algorithm correctness evidence: TODO.
- Theory: derive list traversal, insert/extract/decrease counts, O((n+m)log n), and space. Explain actual decrease count q.
- Empirical evidence: reference the same S1/S2/S3 inputs and charts.
- Explain differences between actual behavior and worst-case bounds: TODO.

## 4. Experimental methods

Record actual parameter table, generation method/version, input equivalence, seeds, correctness oracle, machine/build, warmups/repeats, clock, timing boundaries, separate count runs, and failure handling.

Describe medians within each graph, then across five graph seeds, quantile convention, Q1-Q3 error bars, and same-graph speed ratios. Link the final run ID and reproducibility metadata.

## 5. Part (c): comparison

| Condition | Measured observation | Supporting figure/data | Explanation and scope |
| --- | --- | --- | --- |
| Sparse growth | Pending | Pending | Pending |
| Dense growth | Pending | Pending | Pending |
| Fixed n, changing m | Pending | Pending | Pending |
| Small sizes | Pending | Pending | Pending |

Discuss an observed crossover interval only if supported. Compare theoretical storage and implementation complexity; do not describe estimated bytes as measured peak memory.

## 6. Limitations and reproducibility

Address connected-generator bias, weight distribution, limited sizes/seeds, one-machine scope, and excluded graph construction costs. Add actual build/test/run commands, paths to data, and code revision. Do not label planned processing commands as completed runs.

## 7. Contributions and review

A: matrix implementation and own tests. B: indexed heap, list implementation and own tests. C: generator, output/measurement, independent reference, automation, theory/analysis and report integration. All: cross-review and comparison (c).

Replace placeholders with the actual contributions and unresolved limitations before submission.
