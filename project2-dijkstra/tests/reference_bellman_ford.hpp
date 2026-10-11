#pragma once
#include "graph.hpp"
#include "scaffold.hpp"

inline std::vector<project2::Distance> reference_bellman_ford(
    const project2::EdgeListGraph& graph, project2::Vertex source) {
    // OWNER: Member C; test-only independent oracle, never timed as Dijkstra.
    // TODO: initialize distances; perform at most n-1 full edge passes.
    // Relax both directions of undirected edges, skip INF, guard additions.
    (void)graph; (void)source;
    throw project2::NotImplemented("Member C: independent test reference");
}
