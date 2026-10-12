# Experiment scripts

All three processors are implemented and validated.

| Script | Input | Output |
| --- | --- | --- |
| run_experiments.py | Config CSV and optimized C++ binary | Paired raw timings/counts, config snapshot, environment/build metadata |
| summarize_results.py | Completed raw run directory | Per-graph medians, across-seed summaries, same-graph ratios, validation manifest |
| plot_results.py | Validated summary directory | PNG/SVG figures and plot/data provenance manifest |

experiment_common.py owns config/record validation and linear type-7 quantiles. Tests in tests/test_experiments.py check aggregation math and rejection of missing, duplicated, nonfinite, failed or unpaired data.

Runner/summary require Python 3.9+ standard libraries. Plotting additionally requires Matplotlib (see ../requirements.txt). Use one machine/build, preserve raw data, and create a fresh output directory per run. Plotting supports --overwrite for regenerating its named figure files after presentation changes.

Commands and completed main-v1 results are documented in [running guide](../../docs/running-guide.md) and [report](../../docs/report-draft.md).
