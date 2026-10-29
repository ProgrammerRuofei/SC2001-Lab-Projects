#include "output.hpp"

#include <cstddef>
#include <ostream>
#include <stdexcept>

namespace project3 {
void write_problem(std::ostream& out, const Problem& problem) {
    out << "capacity=" << problem.capacity << '\n';
    out << "item,weight,profit\n";
    for (std::size_t i = 0; i < problem.items.size(); ++i)
        out << i << ',' << problem.items[i].weight << ','
            << problem.items[i].profit << '\n';
}

void write_solution(std::ostream& out, const Problem& problem,
                    const Solution& solution, bool show_table) {
    validate_problem(problem);
    if (solution.dp.size() != static_cast<std::size_t>(problem.capacity) + 1 ||
        solution.dp.front() != 0)
        throw std::invalid_argument("Solution must contain dp[0..C] with dp[0]=0");
    out << "maximum_profit=" << solution.dp.back() << '\n';
    if (show_table) {
        out << "capacity,maximum_profit\n";
        for (std::size_t c = 0; c < solution.dp.size(); ++c)
            out << c << ',' << solution.dp[c] << '\n';
    }
}
}  // namespace project3
