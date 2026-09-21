# Merge-call and heap-allocation profiling for Part (d)

This is a diagnostic experiment, **not** a replacement for the Part (d)
measurements or a change to the submitted sorting algorithm. It exists to
check a specific explanation for the Part (d) result: Hybrid Merge Sort made
more key comparisons than original Merge Sort but used less CPU time. The
question is whether that gap is explained by the number of times `merge()`
runs and the heap allocations each call makes, none of which are counted by
`key_comparisons`.

## Method

A diagnostic binary was built from copies of `sorting.hpp`, `sorting.cpp`,
and `input.cpp` (unmodified sorting logic) plus two diagnostic-only
additions. None of this touches `src/` or `include/`; the diagnostic source
lives in
[`../experiments/diagnostics/merge_call_profiling/`](../experiments/diagnostics/merge_call_profiling/)
for reproducibility, with its own build instructions:

- a global counter `mergeCallCount`, incremented at the top of `merge()`;
- process-wide overrides of `operator new`/`operator delete` that count
  allocation calls and total bytes requested.

The overrides count every heap allocation in the process, so `new_calls`
includes the one allocation for `generateRandomInput`'s result and the one
copy made before timing, in addition to every `temporary` vector `merge()`
constructs. Both algorithms share that fixed overhead (same input generation,
one copy), so it does not affect the merge-versus-hybrid comparison below.

For each algorithm, the diagnostic binary generated the input, copied it,
sorted the copy, verified it was sorted, and printed `key_comparisons`,
an **instrumented** `cpu_seconds`, `merge_call_count`, `new_calls`,
`delete_calls`, and `bytes_allocated`. Ran with `n = 10,000,000`,
`x = 10,000,000`, `S = 128` for Hybrid, and seeds `2001–2003`, matching Part
(d). Git HEAD at the time was `50d24f1c4ca42f11efa6c44481da7ca4ab63a701`
(worktree dirty, as in Part (d)). Raw output is in
[`../results/merge_call_profiling_1e7_s128.csv`](../results/merge_call_profiling_1e7_s128.csv).

The `key_comparisons` from this diagnostic binary matched the formal Part (d)
CSV exactly for every seed (e.g., `220,100,979` / `367,358,957` for seed
`2001`), confirming the copied sorting logic is unchanged.

**The instrumented `cpu_seconds` in this experiment is not comparable to the
formal Part (d) timing.** The `operator new`/`operator delete` overrides add
per-allocation counting overhead, and this binary was built and run
separately from the Part (d) session. It is reported only as a rough sanity
check that the instrumented binary still shows Hybrid finishing faster.

## Results

`merge_call_count`, `new_calls`, `delete_calls`, and `bytes_allocated` were
identical across all three seeds for each algorithm, as expected: the
recursive split points depend only on subarray sizes (always
`floor`/`ceil` of the current size), not on the data values, so the shape of
the recursion tree and the vector-growth pattern inside each `merge()` call
do not depend on the seed.

| Metric | Original Merge Sort | Hybrid (S = 128) | Ratio (Merge / Hybrid) |
| --- | ---: | ---: | ---: |
| `merge()` calls | 9,999,999 | 131,071 | 76.3× |
| Heap allocations (`new` calls) | 33,708,517 | 1,310,693 | 25.7× |
| Bytes allocated (cumulative) | 3,015,919,108 | 2,281,177,092 | 1.32× |
| Key comparisons (seed 2001) | 220,100,979 | 367,358,957 | 0.60× |
| Instrumented CPU time (seed 2001, s) | 3.162 | 1.430 | 2.21× |

`merge()` calls fall from `9,999,999` (exactly `n - 1`, as expected for a
recursion tree with `n` singleton leaves) to `131,071` — about **76×** fewer,
not the naive `n / S ≈ 78,125` estimate. The difference is because the
recursion always splits a block into `floor(size/2)` and `ceil(size/2)` down
to size `≤ S`, so most leaf blocks end up smaller than `128`; measured leaf
count is `131,072 = 2^17`, consistent with `⌈log2(n / S)⌉ = 17` recursion
levels below the point a balanced split of `10,000,000` first drops at or
under `128`.

Heap allocation calls fall by about **25.7×** — less than the 76× drop in
`merge()` calls, because each `merge()` call can trigger more than one
reallocation as `temporary` grows via repeated `push_back` (capacity
doubling), and larger merges near the top of the tree need more
reallocations per call. Total bytes allocated fall by only about **1.32×**,
because both algorithms still perform the same large merges near the root of
the recursion (up to the full array), and those dominate byte volume
regardless of how many tiny merges happen underneath.

## Interpretation and limits

This supports the explanation in
[`part-d-analysis.md`](part-d-analysis.md): key-comparison count excludes
recursion and memory-management overhead, and Hybrid Merge Sort removes the
overwhelming majority of `merge()` calls (and their heap allocations) by
replacing the bottom of the recursion with in-place Insertion Sort. Insertion
Sort's extra comparisons are cheap per comparison (in-place array reads and
occasional shifts, no allocation, no recursive call); the comparisons Hybrid
avoids by not recursing further are each bundled with a `merge()` call that
was paying for vector construction, growth, and copy-back. The **call-count**
reduction, not the raw byte volume, tracks the CPU-time result most closely,
which is consistent with the [`reserve-sensitivity.md`](reserve-sensitivity.md)
finding that avoiding repeated `push_back` growth (a per-call cost) mattered
most at small `S`, where the call count is largest.

This diagnostic used one machine, one `(n, S)` pair, and instrumentation that
changes absolute timing. It establishes the mechanism (call count and
allocation count, not comparison count, track the CPU-time gap) but does not
by itself quantify how many CPU-seconds each allocation costs; a sampling
profiler (e.g., Instruments' Time Profiler, or macOS's `sample` tool) would
be needed to attribute wall-clock time to specific functions rather than
counting events.
