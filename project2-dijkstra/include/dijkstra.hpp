#pragma once

#include "graph.hpp"

#include <cstdint>
#include <vector>

namespace project2 {

struct DijkstraResult {
    std::vector<Distance> distances;
    // kNoVertex for the source and unreachable vertices.
    std::vector<Vertex> parents;
};

struct OperationStats {
    std::uint64_t min_scan_slots = 0;
    std::uint64_t matrix_scan_slots = 0;
    std::uint64_t adjacency_entries_scanned = 0;
    std::uint64_t relax_attempts = 0;
    std::uint64_t relax_successes = 0;
    std::uint64_t heap_inserts = 0;
    std::uint64_t heap_extracts = 0;
    std::uint64_t heap_decreases = 0;
};

// A nullptr disables diagnostic counters for timing runs.
// Non-null stats must refer to a fresh, zero-initialized object per run.
// Tie-break equal tentative distances by smaller vertex ID in both versions.
DijkstraResult dijkstra_matrix(
    const MatrixGraph& graph, Vertex source, OperationStats* stats = nullptr);
DijkstraResult dijkstra_heap(
    const ListGraph& graph, Vertex source, OperationStats* stats = nullptr);

}  // namespace project2
