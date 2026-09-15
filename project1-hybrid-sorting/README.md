# Project 1: Hybrid Merge Sort and Insertion Sort

This project studies a Merge Sort variant that switches to Insertion Sort when a subarray size is less than or equal to a threshold `S`.

The core sorting algorithms and timing program will be written in C++. Python may later be used for experiment automation, CSV processing, plotting, and analysis.

## Structure

```text
include/       Public C++ declarations
src/           C++ implementation and program entry point
tests/         Small correctness-test program
experiments/   Experiment notes and future Python scripts
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

The executables are placed under `build/`. The sorting algorithms are intentionally left for students to implement.

## Collaboration

The team workflow and branch conventions are documented in
[`docs/collaboration-guide.md`](docs/collaboration-guide.md). A proposed
three-person division of work is in
[`docs/team-roles.md`](docs/team-roles.md).
