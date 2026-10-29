# Framework and Interfaces

## Call flow

```text
src/main.cpp
  -> Parse --case or custom arguments
  -> validate_problem()       src/input.cpp
  -> write_problem()          src/output.cpp
  -> solve_bottom_up()        src/knapsack.cpp (pending)
  -> write_solution()         src/output.cpp
```

The build entry point is Makefile. The program starts at main() in main.cpp, and the algorithm starts at solve_bottom_up() in knapsack.cpp. The main function handles interaction; the solver accepts a Problem and returns a Solution.

## Data contract

| Type or field | Meaning |
| --- | --- |
| Item.weight / Item.profit | Weight and profit of one item; positive int values |
| Problem.capacity | Capacity C; a nonnegative int |
| Problem.items | Nonempty vector of n item types; the index is the item ID |
| Solution.dp[c] | Maximum profit with total weight at most c |
| Profit | int64_t, allowing total profit to exceed the int range |

The table must contain `C+1` states, with `dp[0]=0`; the final answer is `dp[C]`. Convert C to size_t before adding 1 when allocating the table. The framework uses int for capacity and individual profits, so the profit bound for at most C items fits in int64_t. Practical capacity limits still depend on memory and O(nC) running time.

## Available and pending components

| Component | Current status | Next action |
| --- | --- | --- |
| Types, examples, validation, CLI, output | Implemented | All members review the interfaces |
| Core DP | Explicitly throws NotImplemented | A implements; B reviews |
| Framework and CLI checks | Runnable | C maintains |
| Fixed algorithm acceptance cases | Written; currently PENDING | Run after A's implementation; B adds independent enumeration |
| Theory | Prompts and template | A completes proof, pseudocode, and analysis |
| Subproblem graph | First-level illustration only | B completes nodes, edges, and base-case explanation |
| Report and results | Outline and saving instructions | C collects actual outputs; all members review |

Preserve public function signatures so members can work independently. If return fields or output formats change, update callers, tests, and documentation together.
