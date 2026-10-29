#pragma once

#include <cstdint>
#include <vector>

namespace project3 {
using Profit = std::int64_t;

struct Item {
    int weight;
    int profit;
};

struct Problem {
    int capacity;
    std::vector<Item> items;  // The vector index is the item type ID.
};

struct Solution {
    // dp[c] is the best profit with total weight <= c, not exactly c.
    // Required size: capacity + 1. Required base case: dp[0] == 0.
    std::vector<Profit> dp;
};

// Throws invalid_argument for negative capacity, empty items, or nonpositive
// weights/profits. Zero capacity is supported as the DP base case.
void validate_problem(const Problem& problem);
}  // namespace project3
