#pragma once

#include <cstddef>
#include <cstdint>
#include <vector>

namespace sc2001 {

// Generate size integers uniformly in the inclusive range [1, maxValue].
// Using the same arguments reproduces the same sequence within the same
// standard-library implementation.
std::vector<int> generateRandomInput(
    std::size_t size,
    int maxValue,
    std::uint32_t seed
);

}  // namespace sc2001

