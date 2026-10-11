#include "graph.hpp"

#include <algorithm>
#include <set>
#include <stdexcept>
#include <utility>

namespace project2 {
namespace {
// Conversion/validation is infrastructure and remains outside timing.
void validate(const EdgeListGraph& graph) {
    if (graph.vertex_count == 0) {
        throw std::invalid_argument("Graph needs at least one vertex");
    }
    std::set<std::pair<Vertex, Vertex>> seen;
    Weight maximum_weight = 0;
    for (const auto& edge : graph.edges) {
        if (edge.u >= graph.vertex_count || edge.v >= graph.vertex_count ||
            edge.u >= edge.v) {
            throw std::invalid_argument("Canonical edges require 0 <= u < v < n");
        }
        if (edge.weight < 0 || edge.weight >= kInfinity) {
            throw std::invalid_argument("Edge weight must be in [0, INF)");
        }
        if (!seen.emplace(edge.u, edge.v).second) {
            throw std::invalid_argument("Duplicate logical edge");
        }
        maximum_weight = std::max(maximum_weight, edge.weight);
    }
    if (maximum_weight > 0 && graph.vertex_count - 1 >
        static_cast<Vertex>((kInfinity - 1) / maximum_weight)) {
        throw std::invalid_argument("Simple-path distance bound exceeds INF");
    }
}
}  // namespace

MatrixGraph make_matrix(const EdgeListGraph& graph) {
    validate(graph);
    MatrixGraph result{graph.vertex_count,
        std::vector<std::vector<Weight>>(graph.vertex_count,
            std::vector<Weight>(graph.vertex_count, kInfinity))};
    for (Vertex v = 0; v < graph.vertex_count; ++v) result.weights[v][v] = 0;
    for (const auto& edge : graph.edges) {
        result.weights[edge.u][edge.v] = edge.weight;
        result.weights[edge.v][edge.u] = edge.weight;
    }
    return result;
}

ListGraph make_list(const EdgeListGraph& graph) {
    validate(graph);
    ListGraph result{graph.vertex_count,
        std::vector<std::vector<Neighbor>>(graph.vertex_count)};
    for (const auto& edge : graph.edges) {
        result.neighbors[edge.u].push_back({edge.v, edge.weight});
        result.neighbors[edge.v].push_back({edge.u, edge.weight});
    }
    for (auto& neighbors : result.neighbors) {
        std::sort(neighbors.begin(), neighbors.end(),
            [](const Neighbor& a, const Neighbor& b) { return a.vertex < b.vertex; });
    }
    return result;
}
}  // namespace project2
