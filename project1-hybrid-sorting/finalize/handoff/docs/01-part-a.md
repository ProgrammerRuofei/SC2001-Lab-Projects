# Part A — Algorithm implementation and validation

## What the code does

The implementation uses inclusive array ranges `[left, right]` in [`src/sorting.cpp`](../../../src/sorting.cpp), declared in [`include/sorting.hpp`](../../../include/sorting.hpp). `merge()` receives two **already sorted** adjacent ranges `[left, middle]` and `[middle+1, right]`; it compares their first remaining elements, appends the smaller one to a temporary vector, copies any remainder, then writes the merged sequence back into the original range. It is an iterative helper, not a recursive sort by itself.

Original Merge Sort starts with the full range `[0, n-1]`. It returns at size 0 or 1, recursively sorts left and right halves, then invokes `merge()`. Hybrid Merge Sort has the same recursion except that it invokes `insertionSort()` and returns as soon as `size <= S`. The insertion-sort invariant is a sorted prefix followed by an unsorted suffix; each next key is shifted left into the sorted prefix. Equality is taken from the left during merge and stops shifting during insertion, preserving order among equal keys.

## Counting convention

Increment the counter when comparing two sorting values, including the insertion comparison that stops a shift. Do not count index/loop checks such as `j >= left`, the threshold check `size <= S`, or copying values. The counter is a `std::int64_t` alias passed by reference, so all helpers update the same total. See [`docs/comparison-counting.md`](../../../docs/comparison-counting.md).

## Why the algorithm has this complexity

- Insertion Sort: best case `O(m)` comparisons for already sorted input, worst case `O(m²)` for reverse order. On one nonempty inclusive range of `m` keys, the current counting logic gives `m-1` comparisons in the sorted case and `m(m-1)/2` in the reverse case.
- Original Merge Sort: `T(n) = 2T(n/2) + Θ(n)`, so `Θ(n log n)` for average and worst case. The merge work at each recursion depth totals `Θ(n)`.
- Hybrid: approximately `n/S` insertion leaves cost `O(S²)` each, giving `O(nS)` leaf work; approximately `log₂(n/S)` merge levels cost `Θ(n)` each. Thus `O(nS + n log(n/S))` for `1 <= S <= n`, and `Θ(n log n)` when `S` is a fixed positive constant.

The real split sizes are integers, so the formulas are asymptotic approximations; the exact recursion boundaries explain the plateaus seen in Part C.

## Verification before experiments

[`tests/test_sorting.cpp`](../../../tests/test_sorting.cpp) tests empty/single-element interfaces, two elements, already sorted and reverse-sorted arrays, duplicate keys, nonzero subarray bounds, and Hybrid thresholds including `S = 1` and `S >= n`. [`tests/test_input.cpp`](../../../tests/test_input.cpp) checks the generator. Run `make test` in the project directory. Reverse-sorted input here is a **correctness and worst-case test**, not the later `reserve` performance sensitivity study.

**Slide message:** Hybrid is Merge Sort with a different leaf algorithm; the merge and comparison-counting convention stay shared.
