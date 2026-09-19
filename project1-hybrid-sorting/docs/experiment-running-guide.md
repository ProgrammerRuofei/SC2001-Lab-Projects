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

## Part (c)(iii): suitable S across input sizes

```bash
python3 experiments/scripts/run_experiments.py optimal-s \
  --output results/optimal_s.csv
```

Proposed defaults:

```text
n = 10K; 100K; 1M
S = 1; 2; 4; 8; 16; 32; 64; 128
seeds = 2001-2005
x = 10M
```

Use the coarse results to select a narrower S range for a later fine search.
Record both the comparison-optimal S and time-optimal S.

## Part (d): original versus Hybrid at 10M

Part (d) requires an S selected from Part (c). It is deliberately not given a
default.

```bash
python3 experiments/scripts/run_experiments.py compare \
  --output results/original_vs_hybrid.csv \
  --compare-threshold REPLACE_WITH_SELECTED_S
```

The default comparison uses `n=10M`, seeds 2001-2003, and `x=10M`. For each
seed, original and Hybrid receive the same reproducible input.

## Output files

Each run produces:

```text
results/example.csv
results/example.meta.json
```

The CSV columns are:

```text
study,algorithm,n,S,x,seed,key_comparisons,cpu_seconds
```

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

