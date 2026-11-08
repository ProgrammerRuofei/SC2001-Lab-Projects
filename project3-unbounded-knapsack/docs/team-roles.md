# Suggested Three-Person Work Allocation

Following the earlier projects, A, B, and C are member placeholders. This is an internal recommendation, not a course requirement. No names or current-user identity are assigned. Project 3 has one main DP algorithm, so the allocation covers algorithm design, independent validation and graph construction, and integration and reporting.

Follow the [detailed implementation workflow](execution-plan.md) for the task order, concurrent work, handoffs, exact commands, and completion checks for each member.

| Member | Main responsibilities | Primary files | Deliverables |
| --- | --- | --- | --- |
| A | Recurrence, correctness reasoning, bottom-up algorithm | src/knapsack.cpp, docs/theory.md | General DP implementation, pseudocode, complexity explanation |
| B | P(15) graph and independent validation | docs/subproblem-graph.md, tests/test_knapsack.cpp | Complete dependency graph, manual table, additional tests |
| C | Integration, execution evidence, report organization | src/main.cpp, src/output.cpp, tests/test_cli.py, results/, docs/report-outline.md | Two actual sample runs, reproducible commands, completed report |

## Member A: Algorithm and theory

1. Read types.hpp and knapsack.hpp; confirm the meaning of P(c) and unlimited supply.
2. Complete the correctness explanation and pseudocode in theory.md.
3. Implement solve_bottom_up, return the complete DP table, and remove the placeholder exception.
4. Run `make check-solution` and resolve boundary or numeric-type issues.
5. Explain state updates to B and review B's completed subproblem graph.

Handoff to C: working code, acceptance output, and report-ready recurrence and loop explanations. Preserve the shared interface and compute answers for general inputs.

## Member B: Graph, manual traces, and independent checks

1. Derive the specified examples manually and complete the P(15) dependency graph while A works on implementation.
2. Review existing acceptance cases and add small cases of your own.
3. Add an independent small-case enumerator to test_knapsack.cpp. Enumerate item counts and maximize profit within capacity; do not copy the DP transition as the reference.
4. Compare enumeration results with A's DP across small capacities and item combinations.
5. Check unlimited reuse, unused capacity, and equal weights with different profits; review A's implementation.

Handoff to C: the complete graph, passing tests, and manual explanations of the specified examples. The expected values 28 for (4a) and 16 for (4b) must be supported by actual program runs.

## Member C: Integration, results, and report

1. Read the argument-to-solver-to-output flow in main.cpp and run `make test`.
2. Prepare the report structure while A/B work; track missing figures, pseudocode, and results.
3. After integration, run both framework and algorithm checks. Compare --table output with B's manual table.
4. Save case-a.txt and case-b.txt, recording actual commands, compiler version, and code revision if committed.
5. Complete the result explanations, complexity discussion, and reproduction instructions.

The initial integration code is already provided. C can focus on requirement coverage, reproducing teammates' results, and explaining the DP table. If A/B need support, C can take a boundary-validation task. Large experiments are not needed merely to balance the allocation.

## Shared review

| Work | Lead | Review |
| --- | --- | --- |
| Recurrence, pseudocode, DP implementation | A | B checks correctness; C checks output/documentation consistency |
| Subproblem graph and independent enumeration | B | A checks dependencies; C compares with the DP table |
| CLI, result files, report | C | A checks algorithm explanations; B checks values and figures |

Every member should explain why capacity alone defines the state, why capacities are processed in ascending order, why an item type may be reused, and how both required answers are obtained.

Write all report sections, tables, captions, and diagram labels in English. Review the final report for language consistency as well as technical correctness.

Suggested task branches: `codex/project3-dp`, `codex/project3-graph-tests`, and `codex/project3-integration`. Agree on the shared headers first, then work in the assigned files. Coordinate any public-interface changes across the team.
