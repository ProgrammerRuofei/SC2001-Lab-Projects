# Project 2: Dijkstra's Algorithm

This project compares Dijkstra implementations using (a) an adjacency matrix and an array priority queue, and (b) an array of adjacency lists and a binary min-heap. Part (c) evaluates when each implementation is preferable.

**Current status: a compilable framework with graph conversion, fixed demo inputs, result CSV formatting, a Makefile, acceptance-test entry points, and explicit C++/Python TODOs. Core algorithms, generator, independent reference, and measurement/analysis logic remain pending. There are no measured results.**

## Start here

Read the [detailed execution plan](docs/execution-plan.md) for implementation steps, planned commands, experiment procedures, analysis, and acceptance criteria for parts (a), (b), and (c).

| Document | Purpose |
| --- | --- |
| [Requirements](docs/requirements.md) | Separate course requirements from proposed choices |
| [Execution plan](docs/execution-plan.md) | Carry the project from interfaces to final analysis |
| [Project schedule](docs/project-plan.md) | Dependencies, milestones, and daily deliverables |
| [Team handoff](docs/team-handoff.md) | Message and agent prompts for teammates |
| [Team roles](docs/team-roles.md) | A/B own algorithms; C owns generation, output, experiments and analysis |
| [Framework guide](docs/framework-guide.md) | Build commands, available helpers, and explicit pending modules |
| [Learning guide](docs/learning-guide.md) | Trace both implementations on one small graph |
| [Architecture](docs/architecture.md) | Types, graph representations, interfaces, and counters |
| [Correctness plan](docs/correctness-plan.md) | Hand-computed cases and independent validation |
| [Theory](docs/theory.md) | Time and space complexity derivations |
| [Experiment plan](docs/experiment-plan.md) | Exact parameters, timing rules, and aggregation |
| [Report outline](docs/report-outline.md) | Present evidence for parts (a), (b), and (c) |
| [Report draft](docs/report-draft.md) | Member C writing template with explicit pending results |

## Structure

```text
include/                 Existing C++ declarations and shared types
src/                     Shared helpers and algorithm/benchmark TODO files
tests/                   Acceptance tests and independent-reference TODO
experiments/configs/     Existing pilot, main, and optional parameter tables
experiments/scripts/     Python CLI scaffolds; processing pending
results/                 Output conventions; no measured data
figures/                 Figure checklist; no generated charts
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

These are internal proposals, not additional course requirements. Confirm the deadline, submission format, team size, and permitted libraries against course notices. Build and fixed-demo commands are documented in the framework guide. Batch measurement commands remain proposed until the corresponding TODOs are implemented.

## Available build entry points

```bash
make
make test-graph
./build/dijkstra_benchmark --help
```

See [framework guide](docs/framework-guide.md) for module-specific tests. Full `make test` deliberately fails while any required implementation is PENDING.
