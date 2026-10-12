# Generated figures

Main-v1 has four main PNG/SVG figures: sparse-time-vs-n, dense-time-vs-n, density-time, density-speedup. overview combines these four views; operation-counts explains traversal and actual decrease-key work. Pilot-batch-v1 has a pipeline-validation chart.

Each directory has manifest.json recording input-data hashes, plot-script hash, plotting version and captions. Error bars are across-seed Q1–Q3 of graph medians (or paired graph ratios), not confidence intervals. Logarithmic axes are explicitly labeled.

[Overview](main-v1/overview.png) and [diagnostics](main-v1/operation-counts.png) support the [experimental report](../docs/report-draft.md). Keep source tables and manifests with charts; do not manually change values to force a theoretical trend or crossover.
