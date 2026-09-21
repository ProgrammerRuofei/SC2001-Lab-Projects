# Merge temporary-vector capacity sensitivity check

This is an implementation sensitivity check, **not** a replacement for the
Part (c) measurements or a change to the submitted sorting algorithm.

## Question and controlled change

Could repeated growth of the temporary vector in `merge()` be moving the
observed CPU-time minimum toward a larger threshold?

The tested variant was compiled from a temporary copy of `src/sorting.cpp`.
Its only source change was one line immediately after creating `temporary`:

```cpp
temporary.reserve(static_cast<std::size_t>(right-left+1));
```

The repository's `src/sorting.cpp` was not modified. Both binaries used the
same `src/main.cpp`, `src/input.cpp`, and `-std=c++17 -Wall -Wextra -Wpedantic
-O2` compiler flags. The variant passed the same sorting tests.

## Experiment design

- Fixed `n = 1,000,000`, `x = 10,000,000`.
- Tested `S = 8, 12, 16, 32, 64, 96, 128, 160, 256`.
- Used seeds 2001–2015, in three five-seed blocks.
- Ran baseline and reserve variants as adjacent pairs on the same seed and
  threshold, with randomized pair and within-pair order.
- Each invocation reported the sorting-only CPU time. Input generation,
  input copying, and correctness validation were outside the timed interval.
- The key-comparison counts agreed for every one of the 135 pairs.

The raw observations are in `results/reserve_sensitivity_1m.csv` (270 rows).

| S | Baseline median CPU (ms) | Reserve median CPU (ms) | Relative change |
| ---: | ---: | ---: | ---: |
| 8 | 153.171 | 120.781 | -21.1% |
| 12 | 153.575 | 120.632 | -21.5% |
| 16 | 135.220 | 113.877 | -15.8% |
| 32 | 121.730 | 107.094 | -12.0% |
| 64 | 114.652 | 105.025 | -8.4% |
| 96 | 115.690 | 105.572 | -8.7% |
| 128 | 113.755 | 107.041 | -5.9% |
| 160 | 114.573 | 107.429 | -6.2% |
| 256 | 123.571 | 119.492 | -3.3% |

The table's relative change is computed from the two displayed medians.
Across matched pairs, reserve was faster for all 15 seeds at `S = 8, 12, 16,
32, 64, 128, 160`; for 14 of 15 at `S = 96`; and for 13 of 15 at `S = 256`.

## Interpretation and limits

With the original implementation, `S = 128` was the fastest of the nine
sampled values. With `reserve`, `S = 64` was the fastest sampled value; it was
about 2.0 ms faster than `S = 128` in median CPU time. The minimum thus moved
toward a smaller threshold, but **not** to `S = 12`.

The improvement is largest at small thresholds because those runs make more
merge calls and create more temporary vectors. At `n = 1,000,000`, the
recursion tree makes 131,071 merge calls at `S = 12`, but 8,191 at `S = 128`.
Reserving space avoids vector growth within each merge; it does not remove the
vector construction or the merge itself. This is evidence that memory
allocation contributes to the original C++ optimum. It does not establish
what the optimum would be with a shared reusable buffer.

Absolute timings in this session were higher than in the earlier Part (c)
run, so the two sessions' milliseconds should not be compared directly. The
paired baseline-versus-variant comparisons within this session are the
relevant evidence. The test sampled only nine thresholds and was conducted on
one machine; it does not identify an exact new optimum or explain another
team's Python result on its own.
