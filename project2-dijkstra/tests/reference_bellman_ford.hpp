#pragma once
#include "graph.hpp"
#include <stdexcept>

// Test-only independent edge-list oracle; it never uses Dijkstra or its heap.
inline std::vector<project2::Distance> reference_bellman_ford(
    const project2::EdgeListGraph& graph, project2::Vertex source) {
    using namespace project2;
    if (source >= graph.vertex_count) throw std::invalid_argument("Invalid reference source");
    std::vector<Distance> distances(graph.vertex_count, kInfinity);
    distances[source] = 0;
    for (Vertex round = 1; round < graph.vertex_count; ++round) {
        bool changed = false;
        for (const auto& edge : graph.edges) {
            auto relax = [&](Vertex u, Vertex v) {
                if (distances[u] == kInfinity || edge.weight >= kInfinity - distances[u]) return;
                const auto candidate = distances[u] + edge.weight;
                if (candidate < distances[v]) { distances[v] = candidate; changed = true; }
            };
            relax(edge.u, edge.v);
            relax(edge.v, edge.u);
        }
        if (!changed) break;
    }
    return distances;
}
