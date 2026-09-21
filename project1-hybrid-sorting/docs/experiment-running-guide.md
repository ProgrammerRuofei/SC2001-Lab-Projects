# Experiment running guide

This guide describes the shared process for running Project 1 experiments. The
parameter values below are team proposals, not additional course requirements.

## Responsibilities of each language

- C++ generates inputs, runs the sorting algorithms, counts key comparisons,
  measures sorting CPU time, verifies sorted output, and emits one CSV row.
- Python selects parameter combinations, invokes the C++ executable, collects
  rows, and records reproducibility metadata.
- Python does not reimplement or time the sorting algorithms.

The automation script uses only the Python standard library.

## Before running experiments

From the repository root:

```bash
git switch develop
git pull --ff-only origin develop
cd project1-hybrid-sorting
make -B test
make
```

All tests must pass. Formal results should be collected from a clean, recorded
Git commit.

## Single C++ run

```bash
./build/hybrid_sort hybrid 1000 20 10000000 2001
./build/hybrid_sort merge 1000 0 10000000 2001
```

The arguments are:

```text
algorithm n S x seed
```

The successful output is one CSV data row:

```text
algorithm,n,S,x,seed,key_comparisons,cpu_seconds
```

Input generation and sorted-result checking are outside the timed region.

## Python automation

Run commands from `project1-hybrid-sorting/`.

Preview a study without building, sorting, or creating files:

```bash
python3 experiments/scripts/run_experiments.py pilot \
  --output results/pilot.csv \
  --dry-run
```

Run a small pilot:

```bash
python3 experiments/scripts/run_experiments.py pilot \
  --output results/pilot.csv
```

The default pilot uses:

```text
n = 1,000; 10,000; 100,000
S = 1; 8; 20; 32; 64
seeds = 2001; 2002
x = 10,000,000
algorithms = original Merge Sort and Hybrid Merge Sort
```

For an even smaller smoke test:

```bash
python3 experiments/scripts/run_experiments.py pilot \
  --output results/smoke.csv \
  --n-values 1000 \
  --s-values 1 20 \
  --seeds 2001
```

Use `--overwrite` only when intentionally replacing an existing output.

## Part (c)(i): fixed S, varying n

```bash
python3 experiments/scripts/run_experiments.py fixed-s \
  --output results/fixed_s.csv \
  --fixed-s 20
```

Proposed defaults:

```text
S = 20
n = 1K; 10K; 100K; 1M; 10M
seeds = 2001-2005
x = 10M
```

Override input sizes with `--n-values` when needed.

## Part (c)(ii): fixed n, varying S

```bash
python3 experiments/scripts/run_experiments.py fixed-n \
  --output results/fixed_n.csv \
  --fixed-n 1000000
```

Proposed defaults:

```text
n = 1M
S = 1; 2; 4; 8; 16; 32; 64; 128
seeds = 2001-2005
x = 10M
```

Override thresholds with `--s-values`.

For the final fixed-`n` run, combine a small-`S` overview with a dense search
from `S = 32` to `S = 256`. Add the exact recursion-boundary values that the
step of four would otherwise miss:

```bash
python3 experiments/scripts/run_experiments.py fixed-n \
  --output results/fixed_n_1m_final_1_256.csv \
  --fixed-n 1000000 \
  --s-range 32 256 4 \
  --s-values 1 2 4 8 12 16 20 24 28 61 62 63 121 122 123 243 244 245 \
  --seeds 2001 2002 2003 2004 2005 2006 2007 2008 2009 2010 \
          2011 2012 2013 2014 2015 \
  --case-order-seed 2001
```

This runs 74 distinct thresholds with 15 seeds, for 1,110 measurements. The
small thresholds reveal the initial reduction in CPU time; the regular spacing
from 32 to 256 resolves the low-runtime region; and the additional boundary
values preserve the algorithmically important recursion changes. The fixed
case-order seed shuffles the execution sequence reproducibly so that larger
thresholds are not always measured later in the run.

Analyze the final result with:

```bash
python3 experiments/scripts/analyze_fixed_n.py \
  --input results/fixed_n_1m_final_1_256.csv \
  --summary results/fixed_n_1m_final_1_256_summary.csv \
  --figure-dir figures/fixed_n_1m_final_1_256
```

To inspect timing noise without replacing the formal figures, generate the
separate CPU-time diagnostic:

```bash
python3 experiments/scripts/analyze_timing_diagnostics.py \
  --input results/fixed_n_1m_final_1_256.csv \
  --output figures/fixed_n_1m_timing_diagnostics/cpu_time_distribution_and_session_drift.png
```

The upper panel shows every raw timing together with the median, mean, and IQR.
The lower panel subtracts the median for the corresponding threshold and plots
the residual in CSV execution order. This separates threshold effects from
timing drift during a long experiment session. The command reads the existing
CSV and does not modify the formal result or figure directories.

The shorter balanced CPU-time retest uses representative thresholds and three
blocks of five seeds:

```bash
python3 experiments/scripts/run_experiments.py fixed-n \
  --output results/fixed_n_1m_cpu_retest_balanced.csv \
  --fixed-n 1000000 \
  --s-values 32 48 60 61 62 63 64 96 121 122 123 128 160 192 224 243 244 245 256 \
  --seeds 2001 2002 2003 2004 2005 2006 2007 2008 2009 2010 \
          2011 2012 2013 2014 2015 \
  --case-order-seed 3101 \
  --block-size 5
```

Each block contains all 19 thresholds and five seeds, for 95 measurements per
block and 285 measurements overall. Cases are randomized independently inside
each block. This reduces the duration of one timing run while keeping every
threshold represented in every block.

## Part (c)(iii): suitable S across input sizes

The completed study uses 15 seeds and three balanced blocks at each input size.
The two smaller-input studies extend to `S = 4,096`; the `n = 1,000,000`
study already shows the right-hand rise by `S = 256`.

```bash
python3 experiments/scripts/run_experiments.py optimal-s \
  --output results/part_c_iii_n10k_expanded_repeated.csv \
  --n-values 10000 \
  --s-values 32 48 60 61 62 63 64 78 79 80 96 121 122 123 128 155 156 157 160 192 224 243 244 245 256 311 312 313 384 512 624 625 768 1024 1249 1250 1536 2048 2499 2500 3000 4096 \
  --seeds 2001 2002 2003 2004 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014 2015 \
  --block-size 5 \
  --case-order-seed 5101 \
  --timing-repetitions 100
```

The `n = 100,000` run uses its own recursion-boundary list through `4,096`,
case-order seed `6101`, and `--timing-repetitions 10`. The stable balanced Part
(c)(ii) retest supplies the `n = 1,000,000` CPU result.

Generate the Part (c)(iii) summary and figures with:

```bash
python3 experiments/scripts/analyze_optimal_s.py \
  --comparison-inputs \
    results/part_c_iii_n10k_left_repeated.csv \
    results/part_c_iii_n10k_expanded_repeated.csv \
    results/part_c_iii_n100k_left_repeated.csv \
    results/part_c_iii_n100k_expanded_repeated.csv \
    results/part_c_iii_n1m_balanced.csv \
  --cpu-inputs \
    results/part_c_iii_n10k_left_repeated.csv \
    results/part_c_iii_n10k_expanded_repeated.csv \
    results/part_c_iii_n100k_left_repeated.csv \
    results/part_c_iii_n100k_expanded_repeated.csv \
    results/part_c_iii_n1m_left_balanced.csv \
    results/fixed_n_1m_cpu_retest_balanced.csv \
  --summary results/part_c_iii_summary.csv \
  --figure-dir figures/part_c_iii
```

The methodology and interpretation are documented in
[`part-c-iii-analysis.md`](part-c-iii-analysis.md). The raw long-session CPU
measurements are retained for audit but are not the formal timing result.

For short sorts, `--timing-repetitions` repeats the sort on fresh copies of the
same generated input and records the mean sorting CPU time. Input copying and
correctness validation remain outside each timed interval. The expanded final
scans use 100 repetitions for `n = 10,000`, 10 for `n = 100,000`, and extend
both threshold ranges to `S = 4,096` with recursion-boundary samples. Their
output files are:

```text
results/part_c_iii_n10k_expanded_repeated.csv
results/part_c_iii_n100k_expanded_repeated.csv
results/part_c_iii_n10k_left_repeated.csv
results/part_c_iii_n100k_left_repeated.csv
results/part_c_iii_n1m_left_balanced.csv
```

## Part (d): original versus Hybrid at 10M

Part (c)(iii) selected `S = 128` as a practical threshold for the current
implementation. See [`part-d-experiment-plan.md`](part-d-experiment-plan.md)
for the paired 10M-input procedure and reporting checks. The completed
three-seed run is analyzed in [`part-d-analysis.md`](part-d-analysis.md).

```bash
python3 experiments/scripts/run_experiments.py compare \
  --output results/part_d_original_vs_hybrid_s128.csv \
  --compare-threshold 128
```

The default comparison uses `n=10M`, seeds 2001-2003, and `x=10M`. For each
seed, original and Hybrid receive the same reproducible input.

Generate the Part (d) summary and figures with:

```bash
python3 experiments/scripts/analyze_part_d.py \
  --input results/part_d_original_vs_hybrid_s128.csv \
  --summary results/part_d_original_vs_hybrid_s128_summary.csv \
  --figure-dir figures/part_d
```

This writes the per-seed paired comparison/CPU-time percentages (plus a
median row) to the summary CSV, and two figures
(`part_d_key_comparisons.png`, `part_d_cpu_time.png`) that show each
algorithm's mean across seeds as a bar with the individual seeds plotted as
connected dots, so the seed-paired comparison stays visible alongside the
aggregate.

## Output files

Each run produces:

```text
results/example.csv
results/example.meta.json
```

Newly generated CSV files contain:

```text
study,algorithm,n,S,x,seed,timing_repetitions,key_comparisons,cpu_seconds,run_index,block
```

`run_index` records the actual execution order. `block` identifies a balanced
seed block when `--block-size` is used; otherwise it is `1`. Older CSV files
without these diagnostic columns remain valid inputs to the analyzers.
`timing_repetitions` records how many sorts were averaged for each timing.

The metadata records the Git commit, dirty-worktree status, machine, operating
system, Python version, compiler, invocation, and timing definition.

Do not manually edit measured CSV values. If a run fails, the script returns a
nonzero status and keeps any incomplete data in a `.partial` file.

## Team parallelism

- Teammates may run pilots and verify key comparisons on different machines.
- Use different output filenames to avoid Git conflicts.
- Do not combine CPU times from different machines into one formal timing
  dataset.
- Run the formal CPU-time experiments on one designated machine, from one
  recorded commit, without concurrent heavy workloads.
- Do not run multiple timing experiments simultaneously on that machine.
- Check the metadata before combining results.

Suggested separate filenames:

```text
results/pilot_member_a.csv
results/pilot_member_b.csv
results/pilot_member_c.csv
```

## After data collection

The next analysis stage will read the CSV files, compute summaries such as mean
key comparisons and median CPU time, and create the required plots. Plotting is
not part of this runner and must not alter the raw CSV files.
