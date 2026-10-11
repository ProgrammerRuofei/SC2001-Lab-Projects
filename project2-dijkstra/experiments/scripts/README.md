# Python script scaffolds

| Script | Input | Output | Lead |
| --- | --- | --- | --- |
| run_experiments.py | Configuration CSV and compiled C++ benchmark | Raw timings/counts and environment JSON | C |
| summarize_results.py | Raw run directory | Per-graph medians, configuration summaries, paired ratios | C, reviewed by A |
| plot_results.py | Summary directory | Four main charts and optional diagnostics | C, reviewed by A/B |

Use Python's CSV/JSON support and Matplotlib for plots; add dependencies when implementing. Script files and argument parsers exist, but actual processing explicitly exits PENDING. No experiments have been completed. Proposed CLI examples are in the [execution plan](../../docs/execution-plan.md).
