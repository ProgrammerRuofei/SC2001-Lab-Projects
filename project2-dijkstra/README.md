# Project 2: Dijkstra's Algorithm

This project compares Dijkstra implementations using (a) an adjacency matrix and an array priority queue, and (b) an array of adjacency lists and a binary min-heap. Part (c) evaluates when each implementation is preferable.

**Current status: both Dijkstra implementations and the indexed heap are implemented. Shared graph conversion, fixed fixtures, CSV result formatting and build/test entry points are available. Connected random generation is implemented and tested. The shared test reference, random-input CLI and measurement pipeline are implemented, and full tests pass. Four pilot configurations have run successfully. Python batch/summary/plot processing and the formal main experiment are complete: 19 configurations, 95 graphs, 1330 timing rows and 190 counter rows. Charts and an English empirical report are available.**

## Start here

Open the [English Jupyter report](notebooks/project2_dijkstra.ipynb) or its [HTML reading version](notebooks/project2_dijkstra.html) for principles, actual implementation, experimental setup/procedure, measured results and conclusions. See the [notebook guide](notebooks/README.md) for installation and execution.

Read the [detailed execution plan](docs/execution-plan.md) for implementation steps, planned commands, experiment procedures, analysis, and acceptance criteria for parts (a), (b), and (c).

| Document | Purpose |
| --- | --- |
| [Requirements](docs/requirements.md) | Separate course requirements from proposed choices |
| [Execution plan](docs/execution-plan.md) | Carry the project from interfaces to final analysis |
| [Project schedule](docs/project-plan.md) | Dependencies, milestones, and daily deliverables |
| [Team handoff](docs/team-handoff.md) | Message and agent prompts for teammates |
| [Team roles](docs/team-roles.md) | A/B own algorithms; C owns generation, output, experiments and analysis |
| [Completed results](docs/experiment-results.md) | Measured tables, figures and guide coverage |
| [Running guide](docs/running-guide.md) | Working random-input commands, CSV schemas and pilot records |
| [Framework guide](docs/framework-guide.md) | Build commands, available helpers, and explicit pending modules |
| [Generator walkthrough](docs/generator-implementation.md) | Input generation, validation, sampling and reproducibility |
| [Matrix walkthrough](docs/matrix-implementation.md) | Explain the completed matrix version and tests |
| [Learning guide](docs/learning-guide.md) | Trace both implementations on one small graph |
| [Architecture](docs/architecture.md) | Types, graph representations, interfaces, and counters |
| [Correctness plan](docs/correctness-plan.md) | Hand-computed cases and independent validation |
| [Theory](docs/theory.md) | Time and space complexity derivations |
| [Experiment plan](docs/experiment-plan.md) | Exact parameters, timing rules, and aggregation |
| [Report outline](docs/report-outline.md) | Present evidence for parts (a), (b), and (c) |
| [Experimental report](docs/report-draft.md) | Completed English report with theory, results and limitations |

## Structure

```text
include/                 Existing C++ declarations and shared types
src/                     Implemented graph, algorithms, generation and benchmarking
tests/                   Acceptance tests and independent shortest-path references
experiments/configs/     Existing pilot, main, and optional parameter tables
experiments/scripts/     Implemented batch, validation, summary and plotting tools
results/                 Pilot and main summaries; raw runs are ignored by Git
figures/                 Generated PNG/SVG charts and provenance manifests
notebooks/               English executable report and exported HTML
docs/                    English planning and learning documents
```

## Proposed choices

- C++17 for algorithms, graph generation, and timing; Python for automation and plotting.
- Simple connected undirected graphs for main experiments, integer weights in [1,1000], source vertex 0.
- An unsorted array with linear minimum selection for part (a).
- A custom indexed binary min-heap with decrease-key for part (b).
- The same canonical edge set and source for both implementations.
- Correctness checks before measurement; timing and diagnostic counting are separate runs.
- Member A and Member B implement algorithms; Member C (you) handles generation, output, experiments, theory, and report integration.

These are internal choices, not additional course requirements. Confirm the deadline, submission format, team size, and permitted libraries against course notices. Build, demo and batch commands are documented in the running guide; the main experiment is complete.

## Available build entry points

```bash
make
make test-graph
./build/dijkstra_benchmark --help
```

See [framework guide](docs/framework-guide.md) for module-specific tests. Full `make test` validates all C++ modules, the CLI and Python experiment processing.
