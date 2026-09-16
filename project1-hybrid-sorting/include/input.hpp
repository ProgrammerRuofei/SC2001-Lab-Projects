#pragma once

#include <cstddef>
#include <cstdint>
#include <vector>

namespace sc2001 {

// Generate size integers in [1, maxValue]. maxValue must be positive.
// The same arguments reproduce the input within the same C++ library setup.
std::vector<int> generateRandomInput(std::size_t size,
                                     int maxValue,
                                     std::uint32_t seed);

}  // namespace sc2001
