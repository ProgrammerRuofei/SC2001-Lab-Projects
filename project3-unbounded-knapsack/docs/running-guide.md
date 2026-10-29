# Building and Running

A C++17 compiler and make are required. Python 3 is used only for CLI tests and requires no third-party packages.

From the repository root:

```bash
cd project3-unbounded-knapsack
make
make test
./build/knapsack --help
```

## Assignment datasets

```bash
./build/knapsack --case a --table
./build/knapsack --case b --table
./build/knapsack --case graph --table
```

`a` selects part (4a), capacity 16; `b` selects part (4b), capacity 12. `graph` selects the part (2) dataset with capacity 15; it does not draw a graph. `--table` displays the DP value for every capacity.

## Custom small cases

```bash
./build/knapsack --capacity 9 --weights 4 --profits 7 --table
./build/knapsack --capacity 10 --weights 6,5 --profits 9,7 --table
```

Comma-separated weights and profits must have matching lengths and no empty entries. Do not insert spaces inside the lists. Custom input cannot be combined with `--case`.

## Exit codes and acceptance checks

| Direct program exit code | Meaning |
| --- | --- |
| 0 | Success, including help output |
| 1 | Argument, input, or runtime error |
| 2 | Solver not implemented; stderr displays PENDING |

While the solver is pending, stdout contains only the input and no maximum_profit value. Make also reports an error when its child process exits with a nonzero status.

```bash
make check-solution
```

This is the algorithm acceptance entry point. `make test` permits an explicit PENDING response for valid inputs, so passing it does not establish that the DP is complete.

## Saving actual results

Run these commands only after implementation and successful algorithm acceptance:

```bash
./build/knapsack --case a --table > results/case-a.txt
./build/knapsack --case b --table > results/case-b.txt
```

Each command must exit with code 0. Redirection overwrites the named file, so inspect the saved content before submission and confirm it contains an actual maximum_profit value and DP table. Expected profits are 28 and 16 respectively. These are manually derived reference values, not outputs already produced by the pending framework.

To rebuild, run `make clean` followed by `make`. The repository's existing .gitignore excludes build/.
