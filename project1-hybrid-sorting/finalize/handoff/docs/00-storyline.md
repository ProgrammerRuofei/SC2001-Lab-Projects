# Presentation storyline

## One question, four stages

**Question:** Can replacing the small recursive subproblems of Merge Sort with Insertion Sort improve practical performance, and how should the switching threshold `S` be chosen?

| Stage | Question | Evidence and takeaway |
| --- | --- | --- |
| Part A | What did we implement? | Original Merge Sort and Hybrid Merge Sort share the same merge operation. Hybrid calls Insertion Sort when an inclusive subarray has `size <= S`. Correctness and comparison-count tests cover boundaries, duplicates, and reverse-sorted input. |
| Part B | How did we make inputs comparable? | Generate integers in `[1, x]` programmatically with `n`, `x`, and a recorded seed. C++ sorts and measures; Python runs parameter grids and records CSV rows. |
| Part C(i) | How does work grow with `n` at fixed `S`? | With `S = 20`, comparison counts track `n log₂n` from 1,000 to 10,000,000 items. This supports the fixed-`S` theoretical growth rate. |
| Part C(ii) | What happens as `S` changes at fixed `n`? | At `n = 1,000,000`, a broad search finds falling then rising CPU time. Dense comparison and balanced timing scans reveal discrete recursion-tree plateaus. Fewer comparisons do not necessarily mean lower CPU time. |
| Part C(iii) | Is one `S` suitable across input sizes? | Low-time structural regions vary with `n`, but those measured at 10k, 100k, and 1M overlap at `S = 123–155`. Choose `S = 128` as a simple representative. |
| Part D | Does the chosen Hybrid beat original Merge Sort at 10M? | On three same-seed input pairs, Hybrid at `S = 128` uses about 66.9% more key comparisons but about 54.6% less sorting CPU time (median paired changes). |

## How to tell the story

Start with the algorithmic trade-off, then show each experiment as a decision prompted by the previous result. For Part C(ii), do **not** begin with the dense final graph: show the initial `S = 1–128` scan, the extended `S = 32–4096` view, and only then the focused `S = 1–256` comparisons and balanced `S = 32–256` timing. Part C(iii) follows the same overview-to-zoom sequence for three input sizes. Finish with Part D's paired outcome, then add sensitivity and measurement limitations.

The result is specific to this implementation and machine. The phrase “suitable measured region” is safer than “the universal optimal threshold”. The exact numerical claim about Part D should always say **median of paired changes across three seeds**.

## Theory thread

For subproblem size `m`, Insertion Sort takes `O(m²)` key comparisons in the worst case. Original Merge Sort has `Θ(n log n)` work. For Hybrid Merge Sort with `1 <= S <= n`, a useful bound is merge work `Θ(n log(n/S))` plus insertion-leaf work `O(nS)`. For fixed `S`, this is `Θ(n log n)` in `n`; changing `S` changes practical overhead and the balance between fewer merges and more quadratic leaf work. This model describes the trend, not the exact CPU-time minimum.

## Main limitations to say aloud

The Part C timing experiments include a detected long-session slowdown; formal local CPU plots use the balanced retest. Part D has only three seed pairs on one machine. A separate `temporary.reserve(...)` sensitivity test shifts the fastest of nine sampled `S` values from 128 to 64 without changing key comparisons. Consequently, do not generalize the selected `S` to every C++ implementation or to Python.
