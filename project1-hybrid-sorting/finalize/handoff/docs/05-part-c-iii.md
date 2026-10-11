# Part C(iii) — Choosing a suitable S across input sizes

## Question and search design

Does the favourable threshold region found at one million elements also work at other `n`? We studied `n = 10,000`, `100,000`, and `1,000,000`, using `x = 10,000,000` and 15 seeds (`2001–2015`) per configuration. A common initial scan tested 36 candidate thresholds through `S = 256`. Because the two smaller-input plots did not show a complete right-hand rise, we extended those scans to `S = 4096` and probed recursion boundaries. Timing for `n = 10,000` was repeated 100 times per configuration and for `n = 100,000` 10 times; each reported case timing is the mean of those repetitions. The million-element timing comes from the balanced Part C(ii) retest. Absolute CPU times across different repetition settings or sessions should not be directly compared.

## Figures in presentation order

1. [Sparse CPU overview](../figures/part-c-iii/overview_cpu_powers_of_two.png) and [relative comparison overview](../figures/part-c-iii/overview_comparisons_powers_of_two.png): show only measured powers-of-two values to communicate the overall decline and later rise. For the relative chart, each input size uses its **own S = 1 comparison count** as baseline. The 1M study ends at `S = 256`; do not imply that it was measured to `4096`.
2. [Panel-specific CPU zoom](../figures/part-c-iii/zoom_cpu_by_n.png): show the detailed low-time plateaus and upward boundaries. Panel ranges differ: `32–350` for 10k, `32–400` for 100k, and `32–256` for 1M. Each plotted dot is a measured `S` median and each band is the middle 50% (IQR). In the first panel the last visible measured point is `S = 313`; the line toward `S = 384` passes outside the frame. In the second the last visible measured point is `S = 391`; the line toward `S = 512` passes outside the frame. Neither line implies a new measurement at 350 or 400.
3. [Suitable-region intervals](../figures/part-c-iii/suitable_regions.png): compare the favourable structural regions directly and mark `S = 128` inside their intersection.

## Result and reasoning

| n | Lowest measured CPU-time structural region | Regional median CPU time |
| ---: | ---: | ---: |
| 10,000 | `S = 79–155` | 0.3069 ms |
| 100,000 | `S = 98–194` | 5.7687 ms |
| 1,000,000 | `S = 123–243` | 59.5000 ms |

The regions shift right as `n` changes because repeated halving creates different integer leaf sizes. Their intersection is `S = 123–155`; `128` lies inside all three, so it is a simple, defensible **representative** for Part D. This is not evidence that 128 is uniquely fastest for every input or machine. The staircase in comparison counts follows discrete recursion depths; CPU medians near the bottom of one plateau can differ slightly because of timing noise.

**Slide message:** A single threshold can be chosen from the overlap of measured favourable regions, even though the region boundaries depend on input size.

**Data:** [15-seed summary](../data/summary/part_c_iii_summary.csv) and the selected per-size raw CSVs in [`data/raw/`](../data/raw/); see [data guide](../data/README.md). The longer working derivation is in the repository's `docs/part-c-iii-analysis.md`.
