# Part (d): original Merge Sort versus Hybrid Merge Sort

## Decision and scope

Compare the repository's current C++ implementations on arrays of
`n = 10,000,000` random integers. Use `S = 128` for Hybrid Merge Sort because
Part (c)(iii) places it inside the suitable region for each tested input size.
This is a practical, implementation-specific selection, not a universal
optimum. Do not add the experimental `temporary.reserve(...)` variant to one
algorithm while leaving the other unchanged. This plan uses the existing
formal implementation for both algorithms.

Record both **key comparisons** and **sorting CPU time**. The comparison-count
convention remains in [`comparison-counting.md`](comparison-counting.md).
The C++ runner times sorting with `std::clock`; input generation, copying,
and correctness validation are outside the timed interval.

## Proposed run

Use the same `n`, `x = 10,000,000`, and seed for each Merge/Hybrid pair. Three
seeds (`2001–2003`) are a starting proposal, not a course requirement. The
runner shuffles case order with a reproducible order seed and records the
actual `run_index`, reducing a fixed Merge-first ordering bias. Avoid other
heavy processes during timing. If the three paired times vary too much to
support a clear comparison, run two additional seeds in a **new** output
file; do not overwrite the first run.

Before the formal run, freeze the source version used for both algorithms and
record `git status` and the current commit. The runner's metadata also records
the commit, whether the worktree was dirty, compiler, platform, and exact
command. A dirty worktree is not a measurement failure, but the final report
must identify which code was actually tested. Do not merge new algorithm
changes halfway through the comparison.

From the `project1-hybrid-sorting` directory:

```bash
python3 experiments/scripts/run_experiments.py compare \
  --output results/part_d_original_vs_hybrid_s128.csv \
  --compare-threshold 128 \
  --n-values 10000000 \
  --max-value 10000000 \
  --seeds 2001 2002 2003 \
  --case-order-seed 7101 \
  --timing-repetitions 1 \
  --dry-run
```

Check that the dry run lists six cases: one `merge` and one `hybrid` case for
each of the three seeds. Then repeat the same command **without** `--dry-run`.
The actual run invokes `make test` and `make` before measuring. It creates
the CSV and a matching `.meta.json` file and refuses to overwrite existing
outputs unless `--overwrite` is explicitly supplied.
`S = 0` in a `merge` CSV row is a placeholder because original Merge Sort
does not use a threshold.

## Checks before reporting

1. Confirm six CSV data rows, with both algorithms present for each seed,
   identical `n` and `x`, and `S = 128` on the Hybrid rows.
2. Confirm that all runs passed the runner's sorted-output validation and
   reported nonnegative comparison counts and CPU times.
3. For each seed, compare Hybrid against original Merge Sort on that same
   generated input. Calculate the comparison reduction as
   `(merge comparisons - hybrid comparisons) / merge comparisons` and the
   CPU-time reduction analogously. Report the per-seed values and a median
   across seeds; retain the raw observations and units.
4. Discuss whether comparison and CPU-time differences point in the same
   direction. Timing includes implementation and machine effects; do not
   infer CPU-time savings solely from the comparison counts.
5. Record the compiler flags, machine, seeds, `x`, chosen `S`, and timing
   method from the metadata and repository. Do not mix results from the
   optional reserve sensitivity binary with this formal comparison.

The first three-seed run is complete. Its observations and interpretation
are documented in [`part-d-analysis.md`](part-d-analysis.md). Keep this plan
as the protocol for reproducing or extending the comparison.
