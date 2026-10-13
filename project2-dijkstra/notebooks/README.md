# Project 2 notebook

Open [project2_dijkstra.ipynb](project2_dijkstra.ipynb) for the English executable report. [project2_dijkstra.html](project2_dijkstra.html) is the exported reading version, with tables and figures embedded.

The notebook follows the previous Hybrid Merge Sort presentation's progression: principles, implementation, experimental setup, procedure, results, analysis and conclusions. It addresses Project 2 parts (a), (b) and (c) using the current C++ implementations and the completed `main-v1` experiment.

## Open and run

From `project2-dijkstra`:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r notebooks/requirements.txt
python -m notebook notebooks/project2_dijkstra.ipynb
```

Use Python 3.10+ and select the installed Python environment as the notebook kernel. Run **Restart Kernel and Run All**. Default execution builds and runs two small C++ fixtures and reads the existing experiment summaries; it does not rerun the main benchmark. Building the fixtures requires `make` and a C++17 compiler. Set `RUN_CPP_DEMOS=False` in the first code cell to execute only the teaching example and archived analysis without a compiler. Saved outputs are readable without executing code.

The first code cell is a collapsed support loader; expand it to change the run controls. Detailed initialization and rendering helpers live in [notebook_setup.py](notebook_setup.py), with an explanation in the notebook appendix. It also defines `RUN_FULL_TESTS=False` and `RERUN_MAIN_EXPERIMENT=False`. Enable the former to run the full existing test suite. Enable the latter only for an intentional new measurement: it creates timestamped output directories, while the report continues to describe `main-v1`. To report new measurements, update the selected evidence and review all numerical interpretations together. The notebook checks the C++ source/header hashes against the archived run; if those files change, that check deliberately fails so updated code is not silently presented as the measured version.

The project locator supports launching from the repository root, project root or notebook directory. Keep the notebook in the repository: source files, `experiments/configs/main.csv`, `results/main-v1` and `figures/main-v1` are required for execution. Raw rows in the ignored `results/raw/main-v1` directory are not required for the default analysis.

## Contents and editing

| Section | Contents |
|---|---|
| 1 | Guide requirements and research questions |
| 2 | Greedy rule, correctness argument, graph drawing, relaxation trace, representations |
| 3 | Actual C++ sources, array selection, indexed heap, demo and reconstructed paths |
| 4 | Time/space derivations and sparse/dense expectations |
| 5 | Generator, full 19-row parameter table, environment and timing boundaries |
| 6 | Procedure, archived-data checks, recomputed aggregates/ratios, counter invariants, chart provenance |
| 7 | S1/S2/S3 tables and plots, operation diagnostics, an editable normalized plot |
| 8 | Conditional recommendations, limitations and conclusion |
| 9 | Guide coverage, reproduction, references and contribution statement |

Edit explanatory Markdown directly in Jupyter or VS Code. Numeric tables are computed from CSVs and rendered as actual HTML tables, with explicit dark text, light backgrounds and cell borders for IDE theme compatibility. Results use fixed decimal precision and omit redundant row numbers; the cells remain selectable text rather than images. Source displays read the actual C++ files. The small Python trace is educational and is not the measured algorithm. Keep the distinction between worst-case bounds and observed timings, and between paired ratios and ratios of aggregate medians.

After edits, restart and run all cells, then export the reading version:

```bash
python -m nbconvert --to html notebooks/project2_dijkstra.ipynb --TagRemovePreprocessor.remove_input_tags='["hide-input"]' --TagRemovePreprocessor.remove_all_outputs_tags='["hide-output"]'
```

The original main run includes 19 configurations, 95 graphs, 1330 timing rows and 190 counter rows. For full raw-data reproduction, separately archive `results/raw/main-v1`; summary CSVs do not replace raw records. Review the team contribution statement before submission.
