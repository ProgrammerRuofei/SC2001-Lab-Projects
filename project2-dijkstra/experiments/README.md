# Completed experimental workflow

Pilot-batch-v1 and main-v1 have run through execution, validation, aggregation and visualization. Main-v1 contains all 19 planned configurations, 95 graphs, 1330 time samples and 190 counter records. No configurations failed.

- [pilot.csv](configs/pilot.csv): four pipeline/resource checks.
- [main.csv](configs/main.csv): S1 sparse growth, S2 dense growth, S3 fixed-n density sweep; used unchanged in main-v1.
- [optional-fixed-m.csv](configs/optional-fixed-m.csv): optional additional study, not run and not required for the main guide coverage.

```bash
python3 scripts/run_experiments.py --config configs/main.csv --binary ../build/dijkstra_benchmark --output-dir ../results/raw/new-run
python3 scripts/summarize_results.py --run-dir ../results/raw/new-run --output-dir ../results/new-run
python3 scripts/plot_results.py --input-dir ../results/new-run --output-dir ../figures/new-run
```

These commands run from experiments/. Use fresh names to preserve earlier output. Install plotting requirements in your chosen environment if needed. Config seeds are semicolon-separated; repetitions and warmups are per graph/version. Actual density is calculated from exact m, not the rounded requested label.

Read [results and guide coverage](../docs/report-draft.md), [measurement rules](../docs/experiment-plan.md), and [running guide](../docs/running-guide.md).
