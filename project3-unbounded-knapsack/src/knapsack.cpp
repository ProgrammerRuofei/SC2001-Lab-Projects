#include "knapsack.hpp"

namespace project3 {
Solution solve_bottom_up(const Problem& problem) {
    validate_problem(problem);

    // TODO (Member A): implement the bottom-up recurrence from docs/theory.md.
    // 1. Allocate capacity + 1 Profit entries, initialized to zero.
    //    Convert capacity to size_t BEFORE adding 1.
    // 2. Visit capacities in increasing order.
    // 3. Consider every item whose weight fits the current capacity.
    // 4. Update the current state's best profit using an already computed state.
    // 5. Return the full table in Solution; remove the exception below.
    // Keep arithmetic in Profit and do not hard-code the assignment answers.
    throw NotImplemented("Implement solve_bottom_up in src/knapsack.cpp");
}
}  // namespace project3
