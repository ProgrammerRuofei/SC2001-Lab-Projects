# Supplemental checks and limitations

These checks explain how strongly to interpret the main results. They are suitable for a limitations or Q&A slide, not replacements for the Part C/D plots.

## Long-session CPU slowdown and balanced retest

The dense `n = 1,000,000` Part C(ii) run had 1,110 cases and showed sustained late-session CPU slowdown after roughly 700 observations. Because key-comparison counts are deterministic for a fixed input and implementation, its comparison graph is still usable. Its CPU timing distributions were right-skewed and less stable. The formal local CPU figure instead uses a shorter, balanced 285-case retest: 19 thresholds, 15 seeds, three five-seed blocks, with independently randomized order in each block. On the matching 19-threshold subset, median IQR width fell from `3.521 ms` in the original session to `0.216 ms` in the retest. This is evidence of a measurement-session effect; it does not prove one specific hardware or OS cause. Do not silently delete the original run or compare absolute milliseconds across the sessions.

## `reserve` sensitivity, not `reverse` sorting

The sensitivity test changed one implementation detail in a **temporary copy** of the sorting source: after creating the local merge vector, it called `temporary.reserve(right-left+1)`. This reserves capacity to reduce vector growth; it does not change the sorting algorithm's comparisons. The repository's formal `src/sorting.cpp` and the Part C/D datasets were left unchanged.

At `n = 1,000,000`, nine sampled thresholds (`8, 12, 16, 32, 64, 96, 128, 160, 256`) were tested with 15 seeds as adjacent baseline/variant pairs. All 135 matched pairs had identical key-comparison counts. Within that session, the fastest sampled baseline was `S = 128`, whereas the fastest sampled `reserve` variant was `S = 64`. This shows that a CPU-time-optimal threshold depends on implementation overhead. It does **not** show that `S = 12` is best, identify an exact new optimum, or justify substituting reserve-variant timings into formal Part C/D plots. The session's absolute times were higher than the formal Part C batch; only within-session paired differences should be compared.

The term **reverse-sorted input** refers to a separate correctness/worst-case test in Part A. It is not this sensitivity experiment.

## Merge-call/allocation diagnostic

For Part D's 10M setting, diagnostic instrumentation counted about `76.3×` fewer `merge()` calls and `25.7×` fewer heap allocation calls for Hybrid. These are event counts from an instrumented binary, not a function-level CPU-time profile. The instrumented timing must not be placed alongside the formal Part D timing as though they were the same run. The event counts make the overhead explanation plausible but do not assign a precise fraction of saved CPU time to each operation.

## General limits

- “Suitable S” here means a favourable observed structural region on the tested C++ implementation and machine, using random integer inputs in `[1, 10,000,000]`. A Python implementation or a shared-buffer C++ implementation may have a different optimum.
- Part C(iii) compares three input sizes for threshold selection, not all sizes in the assignment range. Part C(i) covers the full 1k–10M range for growth, and Part D separately covers 10M for the two-algorithm comparison.
- Tiny point-to-point timing differences inside one recursion plateau should not be called meaningful without uncertainty-aware replication. For the final slide, report a region and a representative value.
- Original experiment metadata records a dirty worktree. The handoff provides the CSVs and methods, but the team should not describe the measurements as having been made from a pristine release commit.

**Sources:** [reserve raw data](../data/raw/reserve_sensitivity_1m.csv) and [profiling raw data](../data/raw/merge_call_profiling_1e7_s128.csv). The longer working records are in the repository's `docs/part-c-ii-analysis.md`, `docs/reserve-sensitivity.md`, and `docs/merge-call-profiling.md`.
