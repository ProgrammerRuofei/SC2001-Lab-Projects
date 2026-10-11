# Result storage

There are no measured results. Configuration tables and theoretical expectations must not be presented as observations.

Planned layout:

```text
raw/<run_id>/timings.csv        Original timing rows; ignored by Git
raw/<run_id>/counts.csv         Separate diagnostic rows; ignored by Git
raw/<run_id>/environment.json   Environment/build settings
<run_id>/per_graph.csv          Per-graph algorithm medians
<run_id>/summary.csv            Across-graph configuration summaries
<run_id>/paired_speedup.csv     Same-graph matrix/heap ratios
<run_id>/environment.json       Copy of reproducibility metadata
```

Keep raw records locally or in an agreed team location and preserve run IDs. Small validated summaries and metadata may be versioned. Do not commit large graph inputs, manually modify timings, or overwrite a previous run silently.

Fields and aggregation are defined in the [experiment plan](../docs/experiment-plan.md).
