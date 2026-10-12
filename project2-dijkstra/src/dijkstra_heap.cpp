#include "dijkstra.hpp"
#include "min_heap.hpp"

#include <stdexcept>

namespace project2 {
DijkstraResult dijkstra_heap(const ListGraph& graph, Vertex source,
                             OperationStats* stats) {
    // Full graph validation belongs to conversion, outside algorithm timing.
    if (source >= graph.vertex_count) throw std::invalid_argument("Invalid source");
    DijkstraResult result{std::vector<Distance>(graph.vertex_count, kInfinity),
                          std::vector<Vertex>(graph.vertex_count, kNoVertex)};
    std::vector<bool> settled(graph.vertex_count, false);
    IndexedMinHeap heap(graph.vertex_count);
    result.distances[source] = 0;
    heap.push_or_decrease(source, 0);
    if (stats) ++stats->heap_inserts;

    while (!heap.empty()) {
        const auto u = heap.extract_min().vertex;
        if (stats) ++stats->heap_extracts;
        settled[u] = true;
        for (const auto& neighbor : graph.neighbors[u]) {
            if (stats) ++stats->adjacency_entries_scanned;
            const auto v = neighbor.vertex;
            if (settled[v]) continue;
            if (stats) ++stats->relax_attempts;
            // Keep INF reserved for unreachable vertices and avoid overflow.
            if (result.distances[u] == kInfinity ||
                neighbor.weight >= kInfinity - result.distances[u]) continue;
            const auto candidate = result.distances[u] + neighbor.weight;
            if (candidate >= result.distances[v]) continue;
            const bool present = heap.contains(v);
            heap.push_or_decrease(v, candidate);
            result.distances[v] = candidate;
            result.parents[v] = u;
            if (stats) {
                ++stats->relax_successes;
                if (present) ++stats->heap_decreases;
                else ++stats->heap_inserts;
            }
        }
    }
    return result;
}
}  // namespace project2
