# Final figure candidates

This folder holds selected report figures while the team reviews the final
presentation. It does not replace the raw CSVs in `results/` or the earlier
figures in `figures/`.

For a teammate preparing slides, start with the self-contained
[report handoff](handoff/README.md). It organizes the selected figures, small
CSV data copies, and Part A–D presentation notes without changing the
original results or charts below.

## Part (c)(i): fixed S = 20

- [`part_c_i/part_c_i_comparisons_vs_n.png`](part_c_i/part_c_i_comparisons_vs_n.png)
- [`part_c_i/part_c_i_normalized_comparisons.png`](part_c_i/part_c_i_normalized_comparisons.png)

Both are rendered from `results/fixed_s_dense.csv`. At each `n`, the blue
point is the arithmetic mean of five observed key-comparison counts (seeds
`2001`–`2005`); the error bar is one sample standard deviation. The orange
curve is a fitted `k n log2(n)` reference, not a second experiment. The
normalized view uses green for the observed ratio and orange for its mean.
These are the existing two Part (c)(i) analysis views with a clearer legend,
not a newly selected dataset.

## Part (c)(ii): fixed n = 1,000,000

Candidate presentation order, from a broad search to a local study:

1. [Initial coarse CPU scan, `S = 1–128`](part_c_ii/initial_cpu_time_s1_128.png)
   from `results/fixed_n_1m.csv`. Runtime falls toward the right edge, so
   this scan alone cannot establish the minimum.
2. [Extended CPU scan, `S = 32–4096`](part_c_ii/broad_cpu_time_s32_4096.png)
   from `results/fixed_n_1m_extended.csv`, with the corresponding
   [broad key-comparison view](part_c_ii/broad_comparisons_s32_4096.png).
   These two presentation figures show only the eight measured powers of two
   (`32, 64, 128, 256, 512, 1024, 2048, 4096`) so the large-scale trend is
   readable. The source CSV and summary retain all 23 measured thresholds;
   the [full boundary-probe chart](../figures/fixed_n_1m_extended/part_c_ii_cpu_time_vs_s.png)
   remains available for technical discussion. The increase at large `S`
   motivates focusing on the lower range. The
   initial and extended runs were separate batches: do not join their CPU
   points into one curve or compare their absolute milliseconds directly.
3. [Dense key-comparison view, `S = 1–256`](part_c_ii/part_c_ii_comparisons_vs_s.png)
   from `results/fixed_n_1m_final_1_256.csv`, followed by the
   [local CPU-time view, `S = 32–256`](part_c_ii/part_c_ii_cpu_time_zoom.png)
   from the balanced retest in `results/fixed_n_1m_cpu_retest_balanced.csv`.
   These locate a favorable structural region, not a uniquely optimal
   integer threshold.

The orange dashed line in the final local views identifies `S = 128`, chosen
as a representative for Part (d). It is not an extra observation or a
theoretical optimum. Shaded CPU-time bands show the interquartile range
across seeds. The dense 1,110-run session had timing drift, so use it for key
comparisons and the balanced retest for the formal local CPU-time result.

## Part (c)(iii): compare suitable S across input sizes

Read these candidates in order:

1. [Sparse CPU-time overview](part_c_iii/overview_cpu_powers_of_two.png) and
   [sparse relative-comparison overview](part_c_iii/overview_comparisons_powers_of_two.png)
   show the large-scale trend for `n = 10,000`, `100,000`, and `1,000,000`.
   Only measured powers of two are displayed: the first two studies extend
   through `S = 4096`, while the million-element study stops at `S = 256`.
   The relative-comparison curves each use that input size's `S = 1` result
   as a baseline. The CPU panels have separate vertical scales; compare the
   threshold pattern, not their raw heights.
2. [Dense, panel-specific CPU zoom](part_c_iii/zoom_cpu_by_n.png) shows the
   measured boundary points near each input size's low-time region, with
   `S = 32–350`, `32–400`, and `32–256` displayed respectively. The right-edge
   segments in the first two panels connect to measured samples outside the
   frame, as detailed in `docs/part-c-iii-analysis.md`; they are not extra
   measurements within the frame.
3. [Suitable structural regions](part_c_iii/suitable_regions.png) summarizes
   the full-data decision: `79–155`, `98–194`, and `123–243`. Their common
   intersection is `123–155`, with `S = 128` a convenient representative.

The overview filters displayed points only. The full comparison and CPU CSVs,
the 15-seed summary in `results/part_c_iii_summary.csv`, and the original
dense figures in `figures/part_c_iii/` are unchanged. The local zoom and
structural-region calculations use all available measurements, not just the
powers of two. Reproduce the sparse overview by adding `--sparse-overview`
to the `analyze_optimal_s.py` command in `docs/experiment-running-guide.md`.

## Part (d): original Merge Sort versus Hybrid

- [`part_d/part_d_key_comparisons.png`](part_d/part_d_key_comparisons.png)
- [`part_d/part_d_cpu_time.png`](part_d/part_d_cpu_time.png)

Both figures use `results/part_d_original_vs_hybrid_s128.csv`: three matched
seeds (`2001`–`2003`), `n = 10,000,000`, and Hybrid `S = 128`. Dots show raw
observations, thin lines join the two algorithms for the same seed, and
diamonds show each algorithm's median. The headline percentage is the median
of the three seed-paired percentage changes. It is not calculated from the
diamond heights.

The plotting sources are `experiments/scripts/analyze_fixed_s.py`,
`analyze_fixed_n.py`, `analyze_optimal_s.py`, and `analyze_part_d.py`. Earlier
figures in `figures/` remain available for comparison.

To reproduce the sparse extended figures, run `analyze_fixed_n.py` on
`results/fixed_n_1m_extended.csv` with
`--plot-s-values 32 64 128 256 512 1024 2048 4096`. This option filters
the plotted points only; the generated summary still contains all 23
thresholds.
