# Part C(ii) — Comparisons versus S at fixed n

## Question

At `n = 1,000,000`, how do key comparisons and CPU time change as the threshold `S` grows? Where is a **suitable measured region** for the current implementation? All main scans used values in `[1, 10,000,000]` and seeded random inputs.

## Why we ran the scans in stages

1. **Initial coarse scan:** `S = 1, 2, 4, 8, 16, 32, 64, 128`, five seeds. [The initial CPU chart](../figures/part-c-ii/initial_cpu_time_s1_128.png) falls toward its right edge. It cannot tell whether CPU time will rise again, so it cannot locate the valley alone.
2. **Wider scan:** a 23-threshold boundary-aware experiment to `S = 4096`, five seeds. The presentation [CPU overview](../figures/part-c-ii/broad_cpu_time_s32_4096.png) and [comparison overview](../figures/part-c-ii/broad_comparisons_s32_4096.png) show only the eight **measured** powers of two for readability; the source CSV retains all 23 values. CPU time rises strongly at large `S`, while key comparisons also rise. This narrows attention to the middle.
3. **Dense local comparisons:** 74 thresholds between `S = 1` and `S = 256`, including recursion-boundary probes and 15 seeds. The [dense comparison chart](../figures/part-c-ii/part_c_ii_comparisons_vs_s.png) shows discrete plateaus and jumps, not a smooth function.
4. **Balanced local CPU retest:** 19 representative thresholds, 15 seeds in three balanced five-seed blocks, 285 observations. The [formal local CPU chart](../figures/part-c-ii/part_c_ii_cpu_time_zoom.png) uses median timing and an IQR band. The long 1,110-run dense session showed late-session slowdown; its comparison counts remain valid, but its CPU times are not the formal local timing result.

These are separate sessions. Do not join or subtract their absolute CPU milliseconds as if they came from one experiment.

## Interpretation and theoretical link

Increasing `S` replaces more small merges with insertion-sorted leaves. This cuts recursive calls, temporary-vector creation, and merge/copy overhead. It also increases the amount of `O(S²)` insertion work per leaf. In the initial scan, `S = 1` and `2` had the lowest observed comparison count, but moderate `S` was faster in CPU time. Thus minimum comparisons and minimum CPU time differ.

For a given `n`, many neighbouring thresholds yield the same integer recursion tree. The measured `n = 1,000,000` low-time structural region is `S = 123–243`; all those thresholds have the same key-comparison count for a given seed because the leaf partition does not change. The local timing median is about `59.5–59.6 ms` for this region and rises after the `244–245` boundary. A pointwise minimum within the plateau is not evidence of a uniquely optimal integer `S`. We use `S = 128` as a convenient representative, then test whether that choice works at other sizes in Part C(iii).

The vertical-looking segments near adjacent boundary values in broad logarithmic plots connect **different measured S values** that are close on a log axis; they are not duplicate observations at one S. The local chart is the proper place to inspect those boundaries.

**Slide message:** Search broadly to find both sides of the timing valley, then inspect recursion-boundary plateaus. Select a region, not a noisy single-point winner.

**Data:** [initial raw](../data/raw/fixed_n_1m.csv), [wide raw](../data/raw/fixed_n_1m_extended.csv), [dense raw](../data/raw/fixed_n_1m_final_1_256.csv), and [balanced CPU raw](../data/raw/fixed_n_1m_cpu_retest_balanced.csv), plus their summaries in [`data/summary/`](../data/summary/). The longer working analysis is in the repository's `docs/part-c-ii-analysis.md`.
