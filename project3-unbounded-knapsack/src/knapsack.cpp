#include "knapsack.hpp"

#include <algorithm>
#include <cstddef>

namespace project3 {
Solution solve_bottom_up(const Problem& problem) {
    validate_problem(problem);
    const auto capacity = static_cast<std::size_t>(problem.capacity);
    Solution solution{std::vector<Profit>(capacity + 1, 0)};
    for (std::size_t c = 1; c <= capacity; ++c) {
        for (const auto& item : problem.items) {
            const auto weight = static_cast<std::size_t>(item.weight);
            if (weight <= c) {
                solution.dp[c] = std::max(solution.dp[c],
                    solution.dp[c - weight] + static_cast<Profit>(item.profit));
            }
        }
    }
    return solution;
}
}  // namespace project3
