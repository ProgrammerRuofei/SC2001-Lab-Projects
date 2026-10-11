#include "dijkstra.hpp"
#include "examples.hpp"
#include "reference_bellman_ford.hpp"
#include "test_support.hpp"

int main() {
    return run_test("integration and independent reference", [] {
        using namespace project2;
        const auto graph = teaching_graph();
        OperationStats stats{};
        const auto matrix = dijkstra_matrix(make_matrix(graph), 0);
        const auto heap = dijkstra_heap(make_list(graph), 0, &stats);
        require(matrix.distances == teaching_distances(), "Matrix hand answer");
        require(heap.distances == teaching_distances(), "Heap hand answer");
        require(heap.distances == reference_bellman_ford(graph, 0), "Independent oracle");
        require(stats.adjacency_entries_scanned == 14 && stats.heap_inserts == 5 &&
                stats.heap_extracts == 5 && stats.heap_decreases == 3, "Heap counters");
        // Member C: extend to deterministic random small graphs, disconnected
        // cases and different sources; A/B review complete-distance comparison.
    });
}
