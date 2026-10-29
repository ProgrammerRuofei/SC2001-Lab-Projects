#pragma once

#include "types.hpp"

#include <stdexcept>

namespace project3 {
class NotImplemented : public std::logic_error {
public:
    using std::logic_error::logic_error;
};

// Unlimited copies of each item; unused capacity is allowed.
// Returns all states dp[0..capacity]. No printing or timing in this function.
// Target: O(n * capacity) time and O(capacity) auxiliary space.
Solution solve_bottom_up(const Problem& problem);
}  // namespace project3
