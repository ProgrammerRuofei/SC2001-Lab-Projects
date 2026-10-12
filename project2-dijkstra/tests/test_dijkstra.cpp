#include "dijkstra.hpp"
#include "examples.hpp"
#include "generation.hpp"
#include "reference_bellman_ford.hpp"
#include "test_support.hpp"

#include <random>

namespace {
using namespace project2;
void check(const EdgeListGraph& graph) {
    const auto matrix = make_matrix(graph);
    const auto list = make_list(graph);
    for (Vertex source = 0; source < graph.vertex_count; ++source) {
        const auto expected = reference_bellman_ford(graph, source);
        const auto a = dijkstra_matrix(matrix, source);
        const auto b = dijkstra_heap(list, source);
        require(a.distances == expected && b.distances == expected,
                "Both algorithms agree with independent edge-list oracle");
        require(a.parents == b.parents, "Shared tie-breaking and predecessor rules");
    }
}
}  // namespace

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
        check(teaching_graph());
        check({1, {}});
        check({4, {}});
        check({3, {{0, 1, 0}}});
        check({3, {{0, 1, (kInfinity - 1) / 2}, {1, 2, (kInfinity - 1) / 2}}});
        std::mt19937_64 rng(2012);
        for (int trial = 0; trial < 100; ++trial) {
            const Vertex n = 2 + rng() % 29;
            const auto capacity = n * (n - 1) / 2;
            const auto m = n - 1 + rng() % (capacity - (n - 1) + 1);
            check(generate_connected_graph({n, m, rng(), 0, 20}));
            EdgeListGraph disconnected{n, {}};
            for (Vertex u = 0; u < n; ++u)
                for (Vertex v = u + 1; v < n; ++v)
                    if (rng() % 100 < static_cast<unsigned>(trial % 5) * 25)
                        disconnected.edges.push_back({u, v, static_cast<Weight>(rng() % 21)});
            check(disconnected);
        }
        bool rejected = false;
        try { (void)reference_bellman_ford({0, {}}, 0); }
        catch (const std::invalid_argument&) { rejected = true; }
        require(rejected, "Reference rejects invalid source");
    });
}
