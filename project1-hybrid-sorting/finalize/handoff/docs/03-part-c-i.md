# Part C(i) — Comparisons versus input size at fixed S

## Question and method

With `S = 20` fixed, does Hybrid Merge Sort's key-comparison count grow like `n log n`? We tested 13 sizes from 1,000 to 10,000,000, each with five seeds (`2001–2005`) and values in `[1, 10,000,000]`. The plotted comparison count is the arithmetic mean over seeds; error bars indicate one sample standard deviation. CPU time is secondary here because the requirement asks specifically for key comparisons.

## Figures and evidence

1. [Comparison count versus n](../figures/part-c-i/part_c_i_comparisons_vs_n.png) compares the empirical mean with a fitted `k n log₂n` reference. The fitted curve is **not** a second dataset.
2. [Normalized comparisons](../figures/part-c-i/part_c_i_normalized_comparisons.png) plots `mean C(n)/(n log₂n)`. If the measured growth is proportional to `n log n`, this ratio should remain roughly stable.

The mean rose from `10,276` comparisons at `n = 1,000` to `242,310,784.6` at `n = 10,000,000`. The normalized ratio stayed roughly `0.986–1.086`. This is consistent with `Θ(n log n)` growth for fixed `S`; a finite experimental curve alone is not an asymptotic proof.

## Theory to present

Stopping at `S` leaves approximately `log₂(n/S)` merge levels, with `Θ(n)` merge work per level. About `n/S` insertion leaves each cost `O(S²)`, so the overall bound is `O(n log(n/S) + nS)`. With fixed `S = 20`, `log(n/S) = Θ(log n)` and `nS = O(n)`, hence the overall order is `Θ(n log n)`.

**Slide message:** Hybrid changes practical constants, but for fixed threshold it retains Merge Sort's `n log n` scaling.

**Data:** [raw five-seed runs](../data/raw/fixed_s_dense.csv) and [summary](../data/summary/fixed_s_dense_summary.csv). The longer working analysis is in the repository's `docs/part-c-i-analysis.md`; this handoff contains the presentation claim and its data independently.
