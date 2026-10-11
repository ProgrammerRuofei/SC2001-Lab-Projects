#pragma once

#include "types.hpp"

#include <vector>

namespace project2 {

// Canonical simple undirected edge: u < v; each logical edge occurs once.
struct Edge {
    Vertex u;
    Vertex v;
    Weight weight;
};

struct EdgeListGraph {
    Vertex vertex_count;
    std::vector<Edge> edges;
};

struct Neighbor {
    Vertex vertex;
    Weight weight;
};

// Both graph representations use vertex IDs [0, vertex_count).
// Matrix cells use kInfinity for absent edges and 0 on the diagonal.
struct MatrixGraph {
    Vertex vertex_count;
    std::vector<std::vector<Weight>> weights;
};

struct ListGraph {
    Vertex vertex_count;
    std::vector<std::vector<Neighbor>> neighbors;
};

// Validate before conversion: valid IDs, unique pairs, 0 <= weight < kInfinity.
// For undirected graphs, populate both directions from each canonical edge.
MatrixGraph make_matrix(const EdgeListGraph& graph);
ListGraph make_list(const EdgeListGraph& graph);

}  // namespace project2
