# Data selected for the report

All CSVs here are byte-for-byte copies of existing files in the project's `results/` directory. They are **not** generated from the figures or modified for the handoff. `raw/` contains individual configurations/runs; `summary/` contains derived statistics. The original `.meta.json` run records remain next to the originals in `results/` and should be consulted for exact commands, machine, compiler, and run-order details. The original metadata reports a dirty worktree at measurement time.

| Part / purpose | Raw CSV copy | Summary copy | Presentation figure(s) |
| --- | --- | --- | --- |
| C(i), fixed `S = 20` | [fixed_s_dense.csv](raw/fixed_s_dense.csv) | [fixed_s_dense_summary.csv](summary/fixed_s_dense_summary.csv) | [`part-c-i/`](../figures/part-c-i/) |
| C(ii), initial `S = 1–128` | [fixed_n_1m.csv](raw/fixed_n_1m.csv) | [fixed_n_1m_summary.csv](summary/fixed_n_1m_summary.csv) | [`initial_cpu_time_s1_128.png`](../figures/part-c-ii/initial_cpu_time_s1_128.png) |
| C(ii), broad search to 4096 | [fixed_n_1m_extended.csv](raw/fixed_n_1m_extended.csv) | [fixed_n_1m_extended_summary.csv](summary/fixed_n_1m_extended_summary.csv) | [`broad_cpu_time_s32_4096.png`](../figures/part-c-ii/broad_cpu_time_s32_4096.png), [`broad_comparisons_s32_4096.png`](../figures/part-c-ii/broad_comparisons_s32_4096.png) |
| C(ii), dense comparisons | [fixed_n_1m_final_1_256.csv](raw/fixed_n_1m_final_1_256.csv) | [fixed_n_1m_final_1_256_summary.csv](summary/fixed_n_1m_final_1_256_summary.csv) | [`part_c_ii_comparisons_vs_s.png`](../figures/part-c-ii/part_c_ii_comparisons_vs_s.png) |
| C(ii), balanced formal local CPU | [fixed_n_1m_cpu_retest_balanced.csv](raw/fixed_n_1m_cpu_retest_balanced.csv) | [fixed_n_1m_cpu_retest_balanced_summary.csv](summary/fixed_n_1m_cpu_retest_balanced_summary.csv) | [`part_c_ii_cpu_time_zoom.png`](../figures/part-c-ii/part_c_ii_cpu_time_zoom.png) |
| C(iii), 10k left and extended scans | [left](raw/part_c_iii_n10k_left_repeated.csv), [extended](raw/part_c_iii_n10k_expanded_repeated.csv) | [common C(iii) summary](summary/part_c_iii_summary.csv) | [`part-c-iii/`](../figures/part-c-iii/) |
| C(iii), 100k left and extended scans | [left](raw/part_c_iii_n100k_left_repeated.csv), [extended](raw/part_c_iii_n100k_expanded_repeated.csv) | [common C(iii) summary](summary/part_c_iii_summary.csv) | [`part-c-iii/`](../figures/part-c-iii/) |
| C(iii), 1M left and balanced scans | [left](raw/part_c_iii_n1m_left_balanced.csv), [initial common scan](raw/part_c_iii_n1m_balanced.csv), [balanced local retest](raw/fixed_n_1m_cpu_retest_balanced.csv) | [common C(iii) summary](summary/part_c_iii_summary.csv) | [`part-c-iii/`](../figures/part-c-iii/) |
| D, original vs Hybrid `S = 128` | [part_d_original_vs_hybrid_s128.csv](raw/part_d_original_vs_hybrid_s128.csv) | [part_d_original_vs_hybrid_s128_summary.csv](summary/part_d_original_vs_hybrid_s128_summary.csv) | [`part-d/`](../figures/part-d/) |
| Supplemental reserve sensitivity | [reserve_sensitivity_1m.csv](raw/reserve_sensitivity_1m.csv) | Table in [sensitivity note](../docs/07-sensitivity-and-limitations.md) | No formal figure; do not mix with main Part C plots |
| Supplemental merge/allocation diagnostic | [merge_call_profiling_1e7_s128.csv](raw/merge_call_profiling_1e7_s128.csv) | Table in [Part D note](../docs/06-part-d.md) | No formal figure; instrumented timing is not comparable to Part D timing |

## How to read the files

- Each raw row is an observation for a given parameter combination; read the CSV header before aggregating. Several Part C(iii) source files use repeated timing for small inputs.
- Do not treat `S = 0` in the original Merge Sort Part D row as a Hybrid threshold; it denotes “not applicable”.
- The Part C(ii) wide presentation figures display only eight powers-of-two values, while the source wide CSV contains 23 measured thresholds. The Part C(iii) sparse overviews similarly display a subset of measured points; their local analysis uses the fuller source files.
- The reported Part D percentage is a median of same-seed **paired percentage changes**. Recomputing a percentage from the two marginal medians is a different statistic.
- Large random integer arrays are intentionally absent. To rerun, generate them from `n`, `x`, and `seed` with the C++ runner. See [Part B](../docs/02-part-b.md) and the repository's [experiment-running guide](../../../docs/experiment-running-guide.md).
