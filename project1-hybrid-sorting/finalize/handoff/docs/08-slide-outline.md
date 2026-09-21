# Suggested slide sequence

This is an outline for the group, not a fixed slide-count requirement. Keep the main deck readable; move the extra broad comparison view or diagnostics to an appendix if time is short.

| Section | Visual | What to say |
| --- | --- | --- |
| Problem and Part A | Small pseudocode or a recursion sketch created from the actual source | Merge Sort recurses until singleton leaves. Hybrid stops at `size <= S` and uses Insertion Sort. Define key comparison. |
| Part B | Compact input/measurement pipeline | Record `n`, `x`, seed, algorithm and `S`. Time sorting only. Generate large arrays; do not commit them. |
| Part C(i) | [Comparisons versus n](../figures/part-c-i/part_c_i_comparisons_vs_n.png), optionally [normalized view](../figures/part-c-i/part_c_i_normalized_comparisons.png) | Fixed `S = 20`; empirical counts are consistent with `Θ(n log n)`. The orange curve is fitted theory, not another run. |
| Part C(ii), broad search | [Initial `1–128`](../figures/part-c-ii/initial_cpu_time_s1_128.png), then [wide `32–4096` CPU](../figures/part-c-ii/broad_cpu_time_s32_4096.png) | The first scan ends before a right-hand rise. The second reveals the valley and motivates local study. Do not compare absolute times across those batches. |
| Part C(ii), local study | [Dense comparisons](../figures/part-c-ii/part_c_ii_comparisons_vs_s.png) and [balanced CPU zoom](../figures/part-c-ii/part_c_ii_cpu_time_zoom.png) | Recursion boundaries create comparison plateaus. The lowest timing region at 1M is `123–243`; choose 128 provisionally. |
| Part C(iii), across n | [Sparse CPU overview](../figures/part-c-iii/overview_cpu_powers_of_two.png), [local zoom](../figures/part-c-iii/zoom_cpu_by_n.png), [region intersection](../figures/part-c-iii/suitable_regions.png) | The favourable regions shift with `n` but overlap at `123–155`; 128 is a robust representative for the tested sizes. Optional [relative comparison overview](../figures/part-c-iii/overview_comparisons_powers_of_two.png) can go in appendix. |
| Part D | [Paired key comparisons](../figures/part-d/part_d_key_comparisons.png) and [paired CPU time](../figures/part-d/part_d_cpu_time.png) | On 10M, Hybrid makes 66.9% more comparisons yet uses 54.6% less CPU time (medians of three seed-paired changes). |
| Limitations / Q&A | One short list, optionally no chart | State three Part D seeds, session drift and balanced retest, reserve sensitivity, and the fact that `S = 128` is not universal. |

## Checks before exporting slides

- Keep the same meaning of `S`, `n`, key comparisons, CPU seconds, mean, median, and IQR throughout.
- Keep C(i)'s **mean** comparison plot distinct from C(ii)/(iii)'s **median** CPU timing plots.
- Do not describe a line between measured threshold points as a measured intermediate `S`.
- Do not label original Merge Sort as Hybrid with `S = 0`; `S = 0` in the CSV is only a not-applicable placeholder.
- Preserve slide citations to the packaged figure and CSV names so any teammate can audit a claim.
