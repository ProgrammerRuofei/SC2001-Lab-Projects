# Project 3: Unbounded Knapsack and Dynamic Programming

Maximize total profit by choosing from `n` item types while keeping total weight at most capacity `C`. Each type has an unlimited supply. Items are indivisible, and unused capacity is allowed.

**Current status: the project framework is ready; the core DP algorithm remains a team implementation task.** The C++17 build, CLI entry point, assignment inputs, input validation, output formatting, and test entry points are provided. The pending solver prints `PENDING` and exits with code 2. Expected answers are never presented as computed results.

## Start here

1. Read the [requirements](docs/requirements.md) to understand the four assignment tasks.
2. Read the [framework guide](docs/framework-guide.md) for code entry points and pending functions.
3. Allocate work using the [three-person team plan](docs/team-roles.md), then follow the [execution plan](docs/project-plan.md).
4. After implementation, use the [running guide](docs/running-guide.md) and [correctness plan](docs/correctness-plan.md) to produce actual results.

## Quick start

Run these commands from this directory:

```bash
make
make test
./build/knapsack --help
./build/knapsack --case a --table
./build/knapsack --case b --table
make check-solution
```

`make test` checks the provided infrastructure. Both solver commands and `make check-solution` report `PENDING` until the algorithm is implemented. Make reports the nonzero child exit code as an error. This indicates incomplete implementation, not a successful algorithm acceptance check.

## Structure

```text
include/          Shared types, solver interface, assignment inputs, output declarations
src/main.cpp      Program entry point, argument parsing, module integration
src/input.cpp     Input validation (implemented)
src/knapsack.cpp  Core bottom-up DP (TODO; Member A leads)
src/output.cpp    Maximum-profit and full DP-table output (implemented)
tests/            Framework checks, CLI checks, and algorithm acceptance entry point
docs/             Requirements, theory prompts, graph template, roles, report outline
results/          Actual outputs to save after implementation
Makefile          Build, test, acceptance, and cleanup commands
```

## Additional documents

- [Theory and algorithm design prompts](docs/theory.md)
- [P(15) subproblem graph worksheet](docs/subproblem-graph.md)
- [Report outline](docs/report-outline.md)

All Project 3 documentation and report content must be written in English, including headings, tables, captions, diagram labels, and result explanations.

The assignment sheet does not require random-input generation, large timing experiments, or performance charts. This framework focuses on the four specified tasks. The proposed three-person allocation follows the earlier projects; replace member labels with actual names and agreed responsibilities. No submission deadline is assumed.
