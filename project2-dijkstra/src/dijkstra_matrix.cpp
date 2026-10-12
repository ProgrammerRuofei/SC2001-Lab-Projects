#include "dijkstra.hpp"

#include <stdexcept>

namespace project2 {
DijkstraResult dijkstra_matrix(const MatrixGraph& graph, Vertex source,
                               OperationStats* stats) {
    // Graph conversion validates the representation outside algorithm timing.
    if (source >= graph.vertex_count) throw std::invalid_argument("Invalid source");
    const auto n = graph.vertex_count;
    DijkstraResult result{std::vector<Distance>(n, kInfinity),
                          std::vector<Vertex>(n, kNoVertex)};
    std::vector<bool> settled(n, false);
    result.distances[source] = 0;

    for (Vertex round = 0; round < n; ++round) {
        // An unsorted array priority queue implements extract-min by scanning.
        // Ascending IDs and strict comparison break equal-distance ties by ID.
        Vertex u = kNoVertex;
        for (Vertex v = 0; v < n; ++v) {
            if (stats) ++stats->min_scan_slots;
            if (settled[v]) continue;
            if (u == kNoVertex || result.distances[v] < result.distances[u]) u = v;
        }
        if (u == kNoVertex || result.distances[u] == kInfinity) break;
        settled[u] = true;

        // Inspect every column, including absent edges and settled vertices.
        for (Vertex v = 0; v < n; ++v) {
            if (stats) ++stats->matrix_scan_slots;
            const auto weight = graph.weights[u][v];
            if (settled[v] || weight == kInfinity) continue;
            if (stats) ++stats->relax_attempts;
            // Keep INF reserved for unreachable vertices and avoid overflow.
            if (weight >= kInfinity - result.distances[u]) continue;
            const auto candidate = result.distances[u] + weight;
            if (candidate >= result.distances[v]) continue;
            result.distances[v] = candidate;
            result.parents[v] = u;
            if (stats) ++stats->relax_successes;
        }
    }
    return result;
}
}  // namespace project2
