# Merge-call / heap-allocation diagnostic

Diagnostic-only build, kept for reproducibility of
[`../../../docs/merge-call-profiling.md`](../../../docs/merge-call-profiling.md).
Not part of the submitted algorithm and not used by `Makefile` or
`experiments/scripts/run_experiments.py`.

- `sorting.hpp` / `sorting.cpp`: copies of `include/sorting.hpp` and
  `src/sorting.cpp` with one addition — a `mergeCallCount` counter
  incremented at the top of `merge()`. The sorting logic itself is
  unmodified (verified: key-comparison counts match the formal Part (d) run
  exactly for the same `n`, `S`, and seed).
- `input.hpp` / `input.cpp`: unmodified copies of `include/input.hpp` and
  `src/input.cpp`, needed to build standalone.
- `alloc_counters.cpp`: global `operator new`/`operator delete` overrides
  that count allocation calls and bytes for the whole process.
- `diag_main.cpp`: standalone driver (not `src/main.cpp`) that runs one sort
  and prints `key_comparisons`, an instrumented `cpu_seconds` (not
  comparable to the formal Part (d) timing — the counters add overhead),
  `merge_call_count`, `new_calls`, `delete_calls`, `bytes_allocated`.

Build and run:

```bash
cd experiments/diagnostics/merge_call_profiling
c++ -std=c++17 -Wall -Wextra -Wpedantic -O2 -I. \
  diag_main.cpp sorting.cpp input.cpp alloc_counters.cpp -o diag_runner

./diag_runner merge 10000000 0 2001
./diag_runner hybrid 10000000 128 2001
# prints: algorithm,n,S,seed,key_comparisons,cpu_seconds,merge_call_count,new_calls,delete_calls,bytes_allocated
```

Raw output for seeds `2001–2003` is saved at
[`../../../results/merge_call_profiling_1e7_s128.csv`](../../../results/merge_call_profiling_1e7_s128.csv).
