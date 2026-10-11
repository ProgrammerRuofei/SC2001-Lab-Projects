#pragma once
#include "graph.hpp"

namespace project2 {
// Fixed input shared by both teammates before the random generator is ready.
inline EdgeListGraph teaching_graph() {
    return {5, {{0, 1, 4}, {0, 2, 1}, {1, 2, 2}, {1, 3, 1},
                {1, 4, 7}, {2, 3, 5}, {3, 4, 3}}};
}
inline std::vector<Distance> teaching_distances() {
    return {0, 3, 1, 4, 7};
}
}  // namespace project2
