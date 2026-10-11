#pragma once

#include <cstddef>
#include <cstdint>
#include <limits>

namespace project2 {

using Vertex = std::size_t;
using Weight = std::int64_t;
using Distance = std::int64_t;

inline constexpr Distance kInfinity = std::numeric_limits<Distance>::max() / 4;
inline constexpr Vertex kNoVertex = std::numeric_limits<Vertex>::max();

}  // namespace project2
