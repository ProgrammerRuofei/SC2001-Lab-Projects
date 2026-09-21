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

## Part (c)(i) analysis

Install the plotting dependency once:

```bash
python3 -m pip install -r experiments/requirements.txt
```

After generating the dense fixed-`S` dataset, create its summary and figures
with:

```bash
python3 experiments/scripts/analyze_fixed_s.py \
  --input results/fixed_s_dense.csv \
  --summary results/fixed_s_dense_summary.csv \
  --figure-dir figures/fixed_s_dense
```

This preserves the raw experiment CSV and generates:

```text
results/fixed_s_dense_summary.csv
figures/fixed_s_dense/part_c_i_comparisons_vs_n.png
figures/fixed_s_dense/part_c_i_normalized_comparisons.png
```

The formulas, interpretation, report paragraph, and presentation points are in
[`docs/part-c-i-analysis.md`](../docs/part-c-i-analysis.md).

## Part (c)(ii) analysis

After generating `results/fixed_n_1m.csv`, run:

```bash
python3 experiments/scripts/analyze_fixed_n.py
```

This preserves the raw experiment CSV and generates:

```text
results/fixed_n_1m_summary.csv
figures/fixed_n_1m/part_c_ii_comparisons_vs_s.png
figures/fixed_n_1m/part_c_ii_cpu_time_vs_s.png
```

The formulas, trade-off analysis, report paragraph, and presentation points are
in [`docs/part-c-ii-analysis.md`](../docs/part-c-ii-analysis.md).

The first power-of-two scan identifies the approximate timing region. After
generating the boundary-aware extension, analyze it with:

```bash
python3 experiments/scripts/analyze_fixed_n.py \
  --input results/fixed_n_1m_extended.csv \
  --summary results/fixed_n_1m_extended_summary.csv \
  --figure-dir figures/fixed_n_1m_extended
```

This produces the complete extended summary, full comparison and CPU-time
plots, and a zoomed CPU-time plot around the observed minimum:

```text
results/fixed_n_1m_extended_summary.csv
figures/fixed_n_1m_extended/part_c_ii_comparisons_vs_s.png
figures/fixed_n_1m_extended/part_c_ii_cpu_time_vs_s.png
figures/fixed_n_1m_extended/part_c_ii_cpu_time_zoom.png
```

For the final fixed-`n` study, the runner combines selected small thresholds
with an inclusive arithmetic range from `S = 32` to `S = 256`. The complete
run and analysis commands are documented in
[`docs/experiment-running-guide.md`](../docs/experiment-running-guide.md).
The overview plots use a log2 x-axis; the detailed CPU-time plot uses a linear
32–256 x-axis, a median line, and a light IQR band for the middle 50% of
measured times. Means, medians, quartiles, and standard deviations remain
available in the summary CSV.

The formal CPU-time figure now comes from the shorter balanced retest:

```text
figures/fixed_n_1m_cpu_retest_balanced/part_c_ii_cpu_time_zoom.png
```

The long-session figures remain available as diagnostics and have not been
overwritten.

## Part (c)(iii) analysis

After generating the expanded repeated-timing scans for `n = 10,000` and
`100,000` and the balanced `n = 1,000,000` result, run the cross-size analyzer
command in
[`docs/experiment-running-guide.md`](../docs/experiment-running-guide.md).
It creates:

```text
results/part_c_iii_summary.csv
figures/part_c_iii/part_c_iii_comparisons_across_n.png
figures/part_c_iii/part_c_iii_cpu_time_across_n.png
figures/part_c_iii/part_c_iii_cpu_time_zoom_1_300.png
figures/part_c_iii/part_c_iii_suitable_regions.png
```

The full method, recursion-boundary explanation, result table, limitations,
and report-ready paragraph are in
[`docs/part-c-iii-analysis.md`](../docs/part-c-iii-analysis.md).
