# Experiments

This directory is reserved for experiment infrastructure, kept separate from the core sorting implementation.

Python automates program runs and collects CSV output by calling the C++
executable. It does not reimplement the sorting algorithms.

Team setup and study commands are documented in
[`docs/experiment-running-guide.md`](../docs/experiment-running-guide.md).

## Single-run C++ interface

Build the executable from the project directory:

```bash
make
```

Run one Hybrid Merge Sort experiment:

```bash
./build/hybrid_sort hybrid 1000 20 10000000 2001
```

Run original Merge Sort on the reproducible input identified by the same
`n`, `x`, and `seed`:

```bash
./build/hybrid_sort merge 1000 0 10000000 2001
```

The positional arguments are:

```text
algorithm n S x seed
```

- `algorithm` is `hybrid` or `merge`.
- `n` is the number of input integers.
- `S` is the positive Hybrid threshold; use `0` for original Merge Sort.
- `x` is the inclusive maximum generated value, so values are in `[1, x]`.
- `seed` identifies the reproducible pseudo-random input.

Successful runs write exactly one CSV data row to standard output:

```text
algorithm,n,S,x,seed,key_comparisons,cpu_seconds
```

Example:

```text
hybrid,1000,20,10000000,2001,9342,0.000081000
```

The displayed numbers above illustrate the format only; they are not recorded
experimental results.

Input generation happens before CPU timing begins. The sorted-result check
happens after timing ends. Errors and usage information are written to standard
error and return a nonzero exit status.

The automation entry point is:

```bash
python3 experiments/scripts/run_experiments.py --help
```

It writes a CSV header once, calls the executable for selected combinations of
`n`, `S`, and `seed`, validates each returned row, and records metadata.
Plotting remains a separate later stage.
