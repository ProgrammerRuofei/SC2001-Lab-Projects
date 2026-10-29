#include "types.hpp"

#include <stdexcept>

namespace project3 {
void validate_problem(const Problem& problem) {
    if (problem.capacity < 0)
        throw std::invalid_argument("Capacity must be nonnegative");
    if (problem.items.empty())
        throw std::invalid_argument("At least one item type is required");
    for (const auto& item : problem.items) {
        if (item.weight <= 0 || item.profit <= 0)
            throw std::invalid_argument("Weights and profits must be positive integers");
    }
}
}  // namespace project3
