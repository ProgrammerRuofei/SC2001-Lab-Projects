# Project 1: Hybrid Merge Sort and Insertion Sort

This project studies a Merge Sort variant that switches to Insertion Sort when a subarray size is less than or equal to a threshold `S`.

The core sorting algorithms, comparison counting, input generation, and timing
program are written in C++. Python is used to automate experiment runs and
collect CSV data; later analysis scripts may process the CSV files and produce
plots.

## Structure

```text
include/       Public C++ declarations
src/           C++ implementation and program entry point
tests/         Small correctness-test program
experiments/   Python experiment runner and experiment notes
results/       Small summary outputs suitable for version control
figures/       Generated plots selected for version control
docs/          Measurement rules, experiment plan, and presentation notes
```

Large arrays should be generated programmatically for each run rather than stored in Git.

## Build

From this directory:

```bash
make
make test
```

The executables are placed under `build/`.

The experiment command-line interface and the recommended team workflow are
documented in
[`docs/experiment-running-guide.md`](docs/experiment-running-guide.md).

## Collaboration

The team workflow and branch conventions are documented in
[`docs/collaboration-guide.md`](docs/collaboration-guide.md). A proposed
three-person division of work is in
[`docs/team-roles.md`](docs/team-roles.md).
