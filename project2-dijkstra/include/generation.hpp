#pragma once

#include "graph.hpp"

#include <cstdint>

namespace project2 {

struct GraphSpec {
    Vertex vertex_count;
    std::size_t edge_count;
    std::uint64_t graph_seed;
    Weight weight_min = 1;
    Weight weight_max = 1000;
};

inline constexpr const char* kGraphGeneratorVersion = "connected-path-v1";

// Shuffled spanning path, then extra distinct edges.
// This is connected by construction, not uniform over all connected graphs.
// Reject infeasible sizes, invalid weights, and unsafe distance bounds.
EdgeListGraph generate_connected_graph(const GraphSpec& spec);

}  // namespace project2
