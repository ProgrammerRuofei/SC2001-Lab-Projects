# Part D — Original Merge Sort versus Hybrid at 10 million integers

## Fair comparison setup

We used `n = 10,000,000`, `x = 10,000,000`, and seeds `2001`, `2002`, `2003`. For each seed, both algorithms received the **same generated input**. Hybrid used `S = 128`, chosen from the overlapping suitable regions in Part C(iii). The six-case run order was shuffled with order seed `7101`. The C++ runner measured sorting-only **process CPU seconds** with `std::clock`; generating, copying, and validating the array were excluded from the timed sort. There was one timed sort per algorithm and seed. The formal source was the original implementation, **not** the separate `reserve` variant.

## Figures and exact headline

- [Paired key-comparison plot](../figures/part-d/part_d_key_comparisons.png)
- [Paired CPU-time plot](../figures/part-d/part_d_cpu_time.png)

Each dot is one seed-algorithm observation; a thin line connects the two observations from the same seed. The large diamond on each side is that algorithm's median. The annotations use the **median of the three seed-paired percentage changes**, not a percentage computed from the two diamond heights.

| Metric | Original Merge Sort median | Hybrid S=128 median | Median paired Hybrid change |
| --- | ---: | ---: | ---: |
| Key comparisons | 220,101,212 | 367,358,957 | 66.905% **more** |
| Sorting CPU time | 3.150718 s | 1.425589 s | 54.584% **less** |

The median paired time speedup was about `2.20×`. Hybrid was faster and made more key comparisons on **each** of the three seed pairs. This contrast is the main takeaway: comparisons measure only value-to-value comparisons, while CPU time also includes recursion, allocation, vector growth, copying, branches, and other operations.

## Why the result is plausible

The Hybrid algorithm skips many bottom-level merges. A separate **diagnostic**, not part of the formal timing, counted `merge()` calls and heap allocations on matching 10M configurations: original Merge Sort made `9,999,999` merge calls, versus `131,071` for Hybrid at `S = 128` (about `76.3×` fewer). The diagnostic counted `33,708,517` versus `1,310,693` heap allocation calls (about `25.7×` fewer). These counts support lower recursive and allocation overhead. They do **not** quantify exactly how many CPU seconds each cause saved, because instrumentation changes timing and does not attribute time per function.

## What not to claim

This was three paired random inputs on one machine; the exact percentages are observed results, not universal constants. One original Merge Sort time was noticeably higher than its other two runs. State the three-pair design and report the paired median, not a precise population speedup. Do not mix the instrumented profiling CPU times with the formal Part D times.

**Slide message:** Hybrid at the selected threshold made more sorting-key comparisons but finished much faster on these 10M inputs, demonstrating why both metrics are needed.

**Data:** [raw observations](../data/raw/part_d_original_vs_hybrid_s128.csv), [paired summary](../data/summary/part_d_original_vs_hybrid_s128_summary.csv), and [diagnostic counts](../data/raw/merge_call_profiling_1e7_s128.csv). The longer working discussion is in the repository's `docs/part-d-analysis.md`.
