# Experiments

This directory is reserved for experiment infrastructure, kept separate from the core sorting implementation.

Future Python scripts may automate program runs, process CSV output, and generate plots. They should call or consume results from the C++ program rather than reimplementing the sorting algorithms.

No plotting or experiment automation has been implemented yet.

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

Future Python automation should write the CSV header once, call this executable
for the selected combinations of `n`, `S`, and `seed`, and append successful
data rows. It must not reimplement the sorting algorithms.
