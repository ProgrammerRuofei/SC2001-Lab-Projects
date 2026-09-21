# Project 1 report and slide handoff

This package collects the selected evidence for SC2001 Project 1. It is a snapshot for the group to review and use in slides; it does not replace the original experiments in `results/`, the analysis in `docs/`, or the source code. No sorting implementation was changed to create it.

## Where to start

1. Read [the presentation storyline](docs/00-storyline.md) and [slide outline](docs/08-slide-outline.md).
2. Use the separate Part [A](docs/01-part-a.md), [B](docs/02-part-b.md), [C(i)](docs/03-part-c-i.md), [C(ii)](docs/04-part-c-ii.md), [C(iii)](docs/05-part-c-iii.md), and [D](docs/06-part-d.md) notes for methods, theory, observations, and claims.
3. Read [limitations and sensitivity checks](docs/07-sensitivity-and-limitations.md) before presenting a single “optimal S”.
4. Use `figures/` for slide-ready images and `data/` for the CSV observations and summaries that support them. [The data guide](data/README.md) maps every selected figure to its source.

The slide sequence follows the investigation: implement and validate the algorithm; generate reproducible inputs; confirm growth with fixed `S`; search `S` broadly, then locally; choose a threshold across input sizes; compare with original Merge Sort at ten million integers. The two sensitivity checks belong after the main result, not in place of it.

## Important reading rules

- Key comparisons count only comparisons between sorting values. The plots of CPU time measure sorting-only **process CPU time**, not wall-clock time.
- In Part C, `S = 128` is a representative inside a favourable measured region, not a universal or uniquely fastest threshold.
- The separate Part C batches ran under different machine conditions. Compare thresholds **within a batch**; do not subtract absolute times from different sessions.
- Part D percentages are medians of three **seed-paired percentage changes**. The diamonds in those plots are per-algorithm medians, not the inputs to the headline percentage.
- Only small CSV records are included. Ten-million-integer arrays are regenerated using `n`, `x`, and `seed`, not stored in Git. The generator uses `std::mt19937`; identical seeds reproduce inputs on the same standard-library implementation.
- The original measurement worktree was recorded as dirty in metadata. This package accurately reports the recorded results but is not a claim that the original measurement came from a clean commit.

## Scope of this package

`figures/` contains copies of the previously selected charts, organized by Part. `data/raw/` contains selected individual-run CSVs; `data/summary/` contains derived aggregations. `docs/` is written for the teammate preparing the report/slides. Additional exploratory plots and full metadata remain in the original repository folders. No new experiments were run for this handoff.
