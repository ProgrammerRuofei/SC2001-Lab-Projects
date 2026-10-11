# Part B — Random input and measurement pipeline

## Assignment requirement and our choices

The assignment asks for random integer arrays from `n = 1,000` up to `10,000,000`, with values in `[1, x]`. We chose `x = 10,000,000` for the reported experiments. The specific intermediate `n` values, seeds, and timing repetitions are **our experimental design**, not extra course requirements.

[`src/input.cpp`](../../../src/input.cpp) constructs a `std::mt19937` generator from a recorded integer `seed`, samples a uniform integer distribution on `[1, x]`, and fills a vector of length `n`. A seed sets the generator's starting state: for a fixed `n`, `x`, seed, and standard-library implementation, it reproduces the same input. Different seeds create independent-looking trials; the same seed lets two algorithms be compared on the same data. Cross-platform bit-for-bit identity is not promised here.

## Data flow and timing boundary

1. Python [`run_experiments.py`](../../../experiments/scripts/run_experiments.py) selects a configuration and invokes the compiled C++ runner.
2. The C++ runner generates the input, makes a working copy as needed, initializes the key-comparison counter, times the **sort only** with `std::clock`, checks the result, and emits a CSV row.
3. Python collects rows and metadata. Analysis scripts aggregate rows and create figures. Python does **not** implement or time the sorting algorithms.

Each observation records the algorithm, `n`, `S`, `x`, seed, key comparisons, and sorting CPU seconds. The original local `results/*.meta.json` records contain the full command, compiler, platform, and Git state; they are not copied into this compact package. The 10M-element arrays themselves were never added to the handoff; they are generated programmatically. This keeps Git small and allows parameterized repetition.

The timing measure is process CPU time, not wall-clock duration. Input generation, copy, and sorted-output validation are outside the timed sort interval. Because of timer noise and changing machine conditions, we compare observations within the same batch, use multiple seeds, and later use balanced randomized execution order.

## Practical reproduction

From the project directory, run `make test` and `make`. A single runner invocation uses:

```text
./build/hybrid_sort algorithm n S x seed
```

For example, `./build/hybrid_sort hybrid 1000 20 10000000 2001` sorts one generated input. Batch commands and flags are in [`docs/experiment-running-guide.md`](../../../docs/experiment-running-guide.md). The selected CSVs and their role are listed in [`data/README.md`](../data/README.md). Re-run into **new output paths** if another teammate wants to replicate; do not overwrite the packaged CSVs.

**Slide message:** Reproducible seeded inputs make the observations comparable, while the time boundary isolates sorting from data generation and validation.
