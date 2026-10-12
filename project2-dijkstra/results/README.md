# Measured data and summaries

Main-v1 is complete: 19 configurations, 95 graphs, 1330 timing rows and 190 independent count rows. Pilot-batch-v1 checks the same three-script pipeline on four configurations. The earlier pilot-entrypoint-check is also retained locally.

```text
raw/<run_id>/timings.csv          Original timings; ignored by Git
raw/<run_id>/counts.csv           Original independent counts; ignored by Git
raw/<run_id>/environment.json     Commands, hashes, environment and completion status
raw/<run_id>/config.csv           Exact input configuration
<run_id>/per_graph.csv            Seven-call medians per graph/version
<run_id>/summary.csv              Median and Q1/Q3 across graph medians
<run_id>/paired_speedup.csv       Same-graph matrix/heap ratios
<run_id>/paired_speedup_summary.csv  Across-seed paired ratio summaries
<run_id>/validation.json          Completeness and aggregation method
<run_id>/environment.json         Copy of run metadata
```

Small validated summaries and metadata may be committed. Original raw rows must also be preserved or archived separately for reproducibility; they are not automatically pushed because raw/ is ignored. Do not overwrite a run or edit its timings. No large input graphs are stored.

See [main summary](main-v1/summary.csv) and [experimental report](../docs/report-draft.md). The result does not imply that heaps win on every possible graph or hardware platform.
